import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = SKILL_ROOT / "scripts" / "fanout_course.workflow.js"


class FanoutWorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.script = WORKFLOW.read_text(encoding="utf-8")

    def test_uses_supported_workflow_logging_and_literal_metadata(self) -> None:
        self.assertTrue(self.script.startswith("export const meta ="))
        self.assertNotIn("emit(", self.script)
        self.assertIn("log(", self.script)

    def test_hard_gate_rejects_small_repositories(self) -> None:
        self.assertIn("preflight.referenceFileCount < 20", self.script)
        self.assertIn("preflight.estimatedMilestones <= 6", self.script)
        self.assertIn("mode: 'single_required'", self.script)

    def test_planner_analyzes_once_and_milestones_are_one_parallel_wave(self) -> None:
        self.assertIn("language-neutral repository, competency, and project-evolution models", self.script)
        self.assertIn("paired course/<lang>/project-evolution.md", self.script)
        self.assertIn("Do not create a separate analysis execution unit", self.script)
        self.assertIn("depends_on: [render.id]", self.script)
        self.assertIn("await parallel(ready.map", self.script)

    def test_missing_learner_profile_returns_assessment_required(self) -> None:
        self.assertIn("const learnerProfile = args.learnerProfile || null", self.script)
        self.assertIn("mode: 'assessment_required'", self.script)
        self.assertIn("readiness-gate", self.script)
        self.assertIn("3-7 short calibration questions", self.script)

    def test_foundations_are_bounded_and_parallel_after_render(self) -> None:
        self.assertIn("foundationUnits.length > 6", self.script)
        self.assertIn("kind === 'foundations'", self.script)
        self.assertIn("depends_on: [render.id]", self.script)
        self.assertIn("foundation-defs/${foundationId}.json", self.script)

    def test_parallel_executors_do_not_write_shared_progress(self) -> None:
        self.assertIn("Do not edit progress.json", self.script)
        self.assertIn("unit-status/${unit.id}.json", self.script)
        self.assertIn("only post-planning writer of progress.json", self.script)

    def test_partial_execution_and_full_finalize_are_distinct(self) -> None:
        self.assertIn("validate_course.py ${workspace} --partial", self.script)
        self.assertIn("full validation without --partial", self.script)

    def test_agent_calls_have_stable_labels_and_structured_results(self) -> None:
        for label in ("fanout-gate", "fanout-planner", "fanout-finalize"):
            self.assertIn(label, self.script)
        for schema in ("PREFLIGHT_SCHEMA", "PLAN_SCHEMA", "EXEC_SCHEMA", "REVIEW_SCHEMA"):
            self.assertIn(schema, self.script)

    def test_agents_summary_documents_v3_safety_rules(self) -> None:
        agents = (SKILL_ROOT / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("Fan-out v3", agents)
        self.assertIn("≥~20 个相关文件", agents)
        self.assertIn("不得彼此串联", agents)
        self.assertIn("orchestration/unit-status/<ID>.json", agents)


if __name__ == "__main__":
    unittest.main()
