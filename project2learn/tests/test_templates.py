import json
import sys
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.validate_course import (
    REVIEW_HEADINGS,
    V3_CORE_HEADINGS,
    V3_FOUNDATION_HEADINGS,
    V3_MILESTONE_HEADINGS,
)


class TemplateContractTests(unittest.TestCase):
    def test_localized_templates_contain_validator_headings(self) -> None:
        templates = SKILL_ROOT / "assets" / "templates"
        for language in ("zh-CN", "en"):
            for filename, headings in V3_CORE_HEADINGS[language].items():
                lines = set((templates / language / filename).read_text(encoding="utf-8").splitlines())
                self.assertTrue(set(headings).issubset(lines), f"{language}/{filename}")
            foundation_lines = set(
                (templates / language / "foundation.md").read_text(encoding="utf-8").splitlines()
            )
            self.assertTrue(set(V3_FOUNDATION_HEADINGS[language]).issubset(foundation_lines))
            milestone_lines = set(
                (templates / language / "milestone.md").read_text(encoding="utf-8").splitlines()
            )
            self.assertTrue(set(V3_MILESTONE_HEADINGS[language]).issubset(milestone_lines))
            review = (templates / language / "review.md").read_text(encoding="utf-8")
            self.assertTrue(set(REVIEW_HEADINGS[language]).issubset(set(review.splitlines())))
            for key in ("artifact_id:", "language:", "review_id:", "milestone_id:", "verdict:"):
                self.assertIn(key, review)

    def test_progress_template_contains_required_language_neutral_fields(self) -> None:
        progress = json.loads(
            (SKILL_ROOT / "assets" / "templates" / "progress.json").read_text(encoding="utf-8")
        )
        required = {
            "schema_version",
            "repository",
            "course_status",
            "learning_phase",
            "current_unit",
            "current_milestone",
            "learner_profile",
            "assessment_history",
            "practice_evidence",
            "foundation_units",
            "milestones",
            "hint_history",
            "open_improvements",
            "learner_choices",
            "last_review",
            "recommended_next_action",
        }
        self.assertEqual(set(progress), required)
        self.assertEqual(progress["schema_version"], 3)
        self.assertEqual(progress["learning_phase"], "assessing")
        self.assertEqual(progress["current_unit"], {"kind": "assessment", "id": "readiness"})
        self.assertEqual(progress["learner_profile"]["learning_mode"], "pending")
        self.assertEqual(progress["practice_evidence"], [])


if __name__ == "__main__":
    unittest.main()
