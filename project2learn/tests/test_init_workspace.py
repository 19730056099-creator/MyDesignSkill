import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.init_workspace import initialize_workspace


def snapshot_tree(root: Path) -> dict[str, tuple[int, str]]:
    snapshot = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        snapshot[str(path.relative_to(root))] = (
            path.stat().st_mtime_ns,
            hashlib.sha256(path.read_bytes()).hexdigest(),
        )
    return snapshot


class InitializeWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        root = Path(self.temporary.name)
        self.reference = root / "Sample Repo"
        self.reference.mkdir()
        (self.reference / "README.md").write_text("# Sample\n", encoding="utf-8")
        self.output_root = root / "learning"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_creates_bilingual_directories_and_progress(self) -> None:
        workspace = initialize_workspace(self.reference, self.output_root)

        self.assertEqual(workspace.name, "Sample-Repo")
        self.assertTrue((workspace / "course" / "zh-CN" / "foundations").is_dir())
        self.assertTrue((workspace / "course" / "en" / "foundations").is_dir())
        self.assertTrue((workspace / "course" / "zh-CN" / "milestones").is_dir())
        self.assertTrue((workspace / "course" / "en" / "milestones").is_dir())
        self.assertTrue((workspace / "student").is_dir())
        self.assertTrue((workspace / "reviews" / "zh-CN").is_dir())
        self.assertTrue((workspace / "reviews" / "en").is_dir())
        progress = json.loads((workspace / "progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress["schema_version"], 3)
        self.assertEqual(progress["course_status"], "analyzing")
        self.assertEqual(progress["learning_phase"], "assessing")
        self.assertEqual(progress["current_unit"], {"kind": "assessment", "id": "readiness"})
        self.assertEqual(progress["learner_profile"]["assessment_mode"], "pending")
        self.assertEqual(progress["learner_profile"]["learning_mode"], "pending")
        self.assertEqual(progress["practice_evidence"], [])
        self.assertEqual(progress["repository"]["name"], "Sample Repo")
        self.assertEqual(progress["repository"]["source"], str(self.reference.resolve()))

    def test_resume_does_not_overwrite_progress(self) -> None:
        workspace = initialize_workspace(self.reference, self.output_root)
        progress_path = workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "in_progress"
        progress["current_milestone"] = 2
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        initialize_workspace(self.reference, self.output_root)

        resumed = json.loads(progress_path.read_text(encoding="utf-8"))
        self.assertEqual(resumed["course_status"], "in_progress")
        self.assertEqual(resumed["current_milestone"], 2)

    def test_reference_repository_is_unchanged(self) -> None:
        before = snapshot_tree(self.reference)

        initialize_workspace(self.reference, self.output_root)

        self.assertEqual(snapshot_tree(self.reference), before)

    def test_rejects_workspace_inside_reference(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not overlap"):
            initialize_workspace(self.reference, self.reference / "project2learn")

    def test_rejects_final_workspace_equal_to_reference(self) -> None:
        repository = Path(self.temporary.name) / "repo"
        repository.mkdir()

        with self.assertRaisesRegex(ValueError, "must not overlap"):
            initialize_workspace(repository, repository.parent)

    def test_rejects_existing_workspace_owned_by_different_reference(self) -> None:
        first = Path(self.temporary.name) / "first" / "same-name"
        second = Path(self.temporary.name) / "second" / "same-name"
        first.mkdir(parents=True)
        second.mkdir(parents=True)
        initialize_workspace(first, self.output_root)

        with self.assertRaisesRegex(ValueError, "belongs to a different reference"):
            initialize_workspace(second, self.output_root)

    def test_revision_change_marks_course_for_reanalysis(self) -> None:
        workspace = initialize_workspace(self.reference, self.output_root, revision="abc123")

        initialize_workspace(self.reference, self.output_root, revision="def456")

        progress = json.loads((workspace / "progress.json").read_text(encoding="utf-8"))
        self.assertEqual(progress["repository"]["revision"], "def456")
        self.assertEqual(progress["repository"]["previous_revision"], "abc123")
        self.assertEqual(progress["course_status"], "analyzing")
        self.assertEqual(progress["recommended_next_action"], "reanalyze_repository")

    def test_rejects_existing_workspace_redirected_to_reference(self) -> None:
        self.output_root.mkdir()
        redirected = self.output_root / "Sample-Repo"
        try:
            os.symlink(self.reference, redirected, target_is_directory=True)
        except OSError as error:
            self.skipTest(f"directory symlinks unavailable: {error}")

        with self.assertRaisesRegex(ValueError, "must not overlap"):
            initialize_workspace(self.reference, self.output_root)


if __name__ == "__main__":
    unittest.main()
