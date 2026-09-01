import json
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.validate_course import (
    LEGACY_MILESTONE_HEADINGS,
    V3_CORE_HEADINGS,
    V3_MILESTONE_HEADINGS,
    V4_LESSON_HEADINGS,
    validate_selected_files,
    validate_workspace,
)


CORE_HEADINGS = {
    "zh-CN": {
        "project-map.md": ["# 项目地图", "## 项目目的", "## 核心用户路径", "## 子系统", "## 证据台账", "## 未覆盖范围"],
        "architecture.md": ["# 架构", "## 系统上下文", "## 组件", "## 数据流", "## 控制流", "## 关键决策", "## 证据台账"],
        "knowledge-graph.md": ["# 知识图谱", "## 概念依赖", "## 学习优先级", "## 源码位置", "## 最小练习"],
        "roadmap.md": ["# 重构路线", "## 路线原则", "## 里程碑总览", "## 覆盖范围", "## 教学性推断"],
    },
    "en": {
        "project-map.md": ["# Project Map", "## Purpose", "## Core User Journey", "## Subsystems", "## Evidence Ledger", "## Uncovered Scope"],
        "architecture.md": ["# Architecture", "## System Context", "## Components", "## Data Flow", "## Control Flow", "## Key Decisions", "## Evidence Ledger"],
        "knowledge-graph.md": ["# Knowledge Graph", "## Concept Dependencies", "## Learning Priority", "## Source Locations", "## Minimal Exercises"],
        "roadmap.md": ["# Reconstruction Roadmap", "## Roadmap Principles", "## Milestone Overview", "## Coverage", "## Teaching Inferences"],
    },
}


READINESS_HEADINGS = {
    "zh-CN": ["# 学习准备", "## 项目所需能力", "## 学习者基线", "## 差距与决策", "## 前置补给路线", "## 进入项目的条件"],
    "en": ["# Learning Readiness", "## Project-Required Competencies", "## Learner Baseline", "## Gaps and Decisions", "## Foundation Route", "## Entry Conditions"],
}

EVOLUTION_HEADINGS = {
    "zh-CN": ["# 项目演变", "## 最终问题与成熟能力", "## 最小可用起点", "## 演变总览", "## 阶段因果链", "## 最终架构如何形成", "## 教学路线声明", "## 证据台账"],
    "en": ["# Project Evolution", "## Final Problem and Mature Capabilities", "## Minimum Viable Starting Point", "## Evolution Overview", "## Stage Causal Chain", "## How the Final Architecture Emerges", "## Teaching-Route Disclaimer", "## Evidence Ledger"],
}

FOUNDATION_HEADINGS = {
    "zh-CN": ["# 前置补给单元", "## 为什么现在需要", "## 依赖", "## 最小概念", "## 小例子", "## 动手练习", "## 通过标准", "## 项目桥接", "## 暂不学习", "## 完成结论"],
    "en": ["# Foundation Unit", "## Why It Is Needed Now", "## Dependencies", "## Minimal Concepts", "## Small Example", "## Hands-on Exercise", "## Exit Criteria", "## Project Bridge", "## Not Learning Yet", "## Completion Decision"],
}

MILESTONE_HEADINGS = {
    "zh-CN": ["# 里程碑", "## 当前版本", "## 上一版本解决了什么", "## 用户遇到的新问题", "## 本阶段引入什么", "## 目标", "## 可观察结果", "## 本阶段解决什么", "## 范围", "## 暂时不解决什么", "## 前置知识", "## 任务", "## 验收", "## 提示 1", "## 提示 2", "## 提示 3", "## 提示 4", "## 提示 5", "## 下一阶段为什么会出现", "## 源码桥接", "## 证据台账", "## 完成结论"],
    "en": ["# Milestone", "## Current Version", "## What the Previous Version Solved", "## New User Problem", "## What This Stage Introduces", "## Goal", "## Observable Result", "## What This Stage Solves", "## Scope", "## Not Solving Yet", "## Prerequisites", "## Tasks", "## Acceptance", "## Hint 1", "## Hint 2", "## Hint 3", "## Hint 4", "## Hint 5", "## Why the Next Stage Appears", "## Source Bridge", "## Evidence Ledger", "## Completion Decision"],
}

REVIEW_HEADINGS = {
    "zh-CN": ["# 阶段评审", "## 优点", "## 正确性", "## 验收证据", "## 当前阶段权衡", "## 下一项规模压力", "## 参考项目对比", "## 必须修改", "## 可选改进", "## 结论"],
    "en": ["# Stage Review", "## Strengths", "## Correctness", "## Acceptance Evidence", "## Current-Stage Tradeoffs", "## Next Scale Pressure", "## Reference Comparison", "## Required Changes", "## Optional Improvements", "## Verdict"],
}


def render_artifact(artifact_id: str, language: str, headings: list[str]) -> str:
    body = ["---", f"artifact_id: {artifact_id}", f"language: {language}", "---"]
    for heading in headings:
        body.extend([heading, "Content."])
    body.extend([
        "evidence: teaching_inference",
        "source: fixture.py::symbol",
        "confidence: medium",
        "rationale: The ordering exposes one engineering pressure at a time.",
    ])
    return "\n\n".join(body) + "\n"


def render_lesson(unit_id: str, lesson_number: int, language: str) -> str:
    lesson_id = f"lesson-{lesson_number:02d}"
    body = [
        "---",
        f"artifact_id: {unit_id}-{lesson_id}",
        f"language: {language}",
        f"unit_id: {unit_id}",
        f"lesson_id: {lesson_id}",
        "---",
        f"# {'第' if language == 'zh-CN' else 'Lesson'} {lesson_number}",
    ]
    for heading in V4_LESSON_HEADINGS[language]:
        body.extend([heading, "Do one small thing and observe the result."])
    return "\n\n".join(body) + "\n"


def render_design(number: int) -> dict:
    unit_id = f"milestone-{number:02d}"
    return {
        "schema_version": 1,
        "artifact_id": f"{unit_id}-design",
        "unit_id": unit_id,
        "kind": "milestone",
        "number": number,
        "slug": "stage",
        "causal_stage": {
            "current_version": "A runnable previous version.",
            "previous_value": "It already produces one result.",
            "new_problem": "A visible limitation now appears.",
            "introduced_change": "Add the smallest mechanism that addresses it.",
            "resolved_pressure": "The visible limitation is removed.",
            "deferred_limit": "A later limit remains deliberate.",
            "next_pressure": "The next user action exposes another problem.",
        },
        "competencies": [],
        "prerequisite_foundations": [],
        "practice_design": {
            "ai_allowed": ["scaffolding"],
            "learner_owned": ["critical action"],
            "must_explain": ["observed behavior"],
            "transfer_checks": ["change one input"],
        },
        "acceptance": [{"id": f"m{number:02d}-a01", "result": "observable"}],
        "hints": [{"level": level, "content": "hint"} for level in range(1, 6)],
        "source_bridge": ["fixture.py::symbol"],
        "evidence": [{
            "type": "teaching_inference",
            "source": "fixture.py::symbol",
            "confidence": "medium",
            "rationale": "The sequence exposes one pressure at a time.",
        }],
        "lessons": [
            {
                "id": f"lesson-{lesson:02d}",
                "artifact_id": f"{unit_id}-lesson-{lesson:02d}",
                "cognitive_goal": "Notice and resolve one friction.",
                "situation": "Run the current version.",
                "friction": "One behavior is inconvenient.",
                "action": "Make one small change.",
                "observable_result": "The behavior changes visibly.",
                "concept_name": "One useful concept.",
                "minimum_theory": "Only enough explanation for this change.",
                "project_delta": "The project can now do one more thing.",
                "next_problem": "A new natural limitation appears.",
                "deferred": None,
            }
            for lesson in range(1, 3)
        ],
    }


def render_foundation_design(number: int) -> dict:
    design = render_design(number)
    unit_id = f"foundation-{number:02d}"
    design.update({
        "artifact_id": f"{unit_id}-design",
        "unit_id": unit_id,
        "kind": "foundation",
        "slug": "basics",
        "why_now": "This capability blocks the first project action.",
        "acceptance": [{"id": f"f{number:02d}-a01", "result": "observable"}],
    })
    design.pop("causal_stage")
    design["lessons"] = design["lessons"][:1]
    design["lessons"][0]["artifact_id"] = f"{unit_id}-lesson-01"
    return design


def write_review_pair(
    workspace: Path,
    *,
    review_id: str = "review-05-01",
    milestone_id: str = "milestone-05",
    verdict: str = "passed",
) -> None:
    filename = "milestone-05-review-01.md"
    for language in ("zh-CN", "en"):
        body = [
            "---",
            f"artifact_id: {review_id}",
            f"language: {language}",
            f"review_id: {review_id}",
            f"milestone_id: {milestone_id}",
            f"verdict: {verdict}",
            "---",
        ]
        for heading in REVIEW_HEADINGS[language]:
            body.extend([heading, "Content."])
        body.extend([
            "evidence: code_evidence",
            "source: student/app.py::main",
            "rationale: The implementation supplies acceptance evidence.",
        ])
        (workspace / "reviews" / language / filename).write_text(
            "\n\n".join(body) + "\n", encoding="utf-8"
        )


class ValidateWorkspaceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.workspace = Path(self.temporary.name) / "course-workspace"
        for language in ("zh-CN", "en"):
            course = self.workspace / "course" / language
            (course / "milestones").mkdir(parents=True)
            (self.workspace / "reviews" / language).mkdir(parents=True)
            for filename, headings in CORE_HEADINGS[language].items():
                artifact_id = filename.removesuffix(".md")
                (course / filename).write_text(
                    render_artifact(artifact_id, language, headings), encoding="utf-8"
                )
            for number in range(1, 6):
                milestone_id = f"milestone-{number:02d}"
                (course / "milestones" / f"{number:02d}-stage.md").write_text(
                    render_artifact(milestone_id, language, MILESTONE_HEADINGS[language]),
                    encoding="utf-8",
                )
        (self.workspace / "student").mkdir()
        (self.workspace / "course" / "GETTING_STARTED.md").write_text(
            """---
artifact_id: getting-started
language: zh-CN
---
# 学习指南
## 课程是什么
Test course.
## 文件总览与阅读顺序
1. Read the project map.
## 各文件的用途速查
Use each milestone in order.
## 使用规则
Implement under student/.
## 现在就开始
Open milestone 01.
""",
            encoding="utf-8",
        )
        progress = {
            "schema_version": 1,
            "repository": {"name": "sample", "source": "reference", "revision": "abc123"},
            "course_status": "ready",
            "current_milestone": 1,
            "milestones": [
                {
                    "id": f"milestone-{number:02d}",
                    "number": number,
                    "status": "ready",
                    "acceptance": [f"m{number:02d}-a01"],
                    "risk_notes": [],
                }
                for number in range(1, 6)
            ],
            "hint_history": [],
            "open_improvements": [],
            "learner_choices": [],
            "last_review": None,
            "recommended_next_action": "start_milestone_01",
        }
        (self.workspace / "progress.json").write_text(
            json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def upgrade_to_schema2(self) -> dict:
        for language in ("zh-CN", "en"):
            course = self.workspace / "course" / language
            (course / "foundations").mkdir(exist_ok=True)
            (course / "readiness.md").write_text(
                render_artifact("readiness", language, READINESS_HEADINGS[language]),
                encoding="utf-8",
            )
            (course / "project-evolution.md").write_text(
                render_artifact("project-evolution", language, EVOLUTION_HEADINGS[language]),
                encoding="utf-8",
            )
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress.update({
            "schema_version": 2,
            "learning_phase": "milestones",
            "current_unit": {"kind": "milestone", "id": "milestone-01"},
            "current_milestone": 1,
            "learner_profile": {
                "assessment_mode": "self_report",
                "goals": [],
                "constraints": [],
                "competencies": [],
            },
            "assessment_history": [{
                "mode": "self_report",
                "summary": "Learner baseline recorded for the selected path.",
                "timestamp": "2025-01-01T00:00:00Z",
            }],
            "foundation_units": [],
        })
        progress_path.write_text(json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8")
        return progress

    def upgrade_to_schema3(self) -> dict:
        progress = self.upgrade_to_schema2()
        progress["schema_version"] = 3
        progress["learner_profile"]["learning_mode"] = "balanced"
        progress["practice_evidence"] = []
        for language in ("zh-CN", "en"):
            course = self.workspace / "course" / language
            for filename in ("project-map.md", "knowledge-graph.md", "readiness.md"):
                artifact_id = filename.removesuffix(".md")
                text = render_artifact(artifact_id, language, V3_CORE_HEADINGS[language][filename])
                if filename == "readiness.md":
                    text += "learning_mode: balanced\n"
                (course / filename).write_text(text, encoding="utf-8")
            for number in range(1, 6):
                milestone_id = f"milestone-{number:02d}"
                (course / "milestones" / f"{number:02d}-stage.md").write_text(
                    render_artifact(milestone_id, language, V3_MILESTONE_HEADINGS[language]),
                    encoding="utf-8",
                )
        (self.workspace / "course" / "GETTING_STARTED.md").write_text(
            """---
artifact_id: getting-started
language: bilingual
---
# 学习指南 / Learning Guide
## 课程是什么 / What This Course Is
Test course.
## 文件总览与阅读顺序 / File Overview and Reading Order
1. Read readiness, project evolution, and the current unit.
## 各文件的用途速查 / Quick File Reference
Use each file for its stated purpose.
## 使用规则 / Usage Rules
Record manual practice and AI usage.
## 现在就开始 / Start Now
Open the current unit.
""",
            encoding="utf-8",
        )
        (self.workspace / "progress.json").write_text(
            json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return progress

    def upgrade_to_schema4(self) -> dict:
        progress = self.upgrade_to_schema3()
        progress["schema_version"] = 4
        progress["current_lesson"] = {"unit_id": "milestone-01", "id": "lesson-01"}
        design_root = self.workspace / "course" / "design"
        (design_root / "foundations").mkdir(parents=True)
        (design_root / "milestones").mkdir(parents=True)
        for number in range(1, 6):
            stem = f"{number:02d}-stage"
            for language in ("zh-CN", "en"):
                (self.workspace / "course" / language / "milestones" / f"{stem}.md").unlink()
            (design_root / "milestones" / f"{stem}.json").write_text(
                json.dumps(render_design(number), ensure_ascii=False, indent=2), encoding="utf-8"
            )
            for language in ("zh-CN", "en"):
                lesson_root = self.workspace / "course" / language / "milestones" / stem
                lesson_root.mkdir()
                for lesson in range(1, 3):
                    (lesson_root / f"{lesson:02d}.md").write_text(
                        render_lesson(f"milestone-{number:02d}", lesson, language),
                        encoding="utf-8",
                    )
        (self.workspace / "progress.json").write_text(
            json.dumps(progress, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return progress

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_valid_bilingual_course_has_no_errors(self) -> None:
        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema1_accepts_legacy_milestone_headings(self) -> None:
        for language in ("zh-CN", "en"):
            for number in range(1, 6):
                milestone_id = f"milestone-{number:02d}"
                milestone = self.workspace / "course" / language / "milestones" / f"{number:02d}-stage.md"
                milestone.write_text(
                    render_artifact(
                        milestone_id, language, LEGACY_MILESTONE_HEADINGS[language]
                    ),
                    encoding="utf-8",
                )

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_valid_schema2_course_has_no_errors(self) -> None:
        self.upgrade_to_schema2()

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_valid_schema3_course_has_no_errors(self) -> None:
        self.upgrade_to_schema3()

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_valid_schema4_course_has_lightweight_lesson_bundles(self) -> None:
        self.upgrade_to_schema4()

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema4_accepts_foundation_lesson_bundle_as_current_unit(self) -> None:
        progress = self.upgrade_to_schema4()
        design = render_foundation_design(1)
        design_path = self.workspace / "course" / "design" / "foundations" / "F01-basics.json"
        design_path.write_text(json.dumps(design, ensure_ascii=False, indent=2), encoding="utf-8")
        for language in ("zh-CN", "en"):
            lesson_root = self.workspace / "course" / language / "foundations" / "F01-basics"
            lesson_root.mkdir()
            (lesson_root / "01.md").write_text(
                render_lesson("foundation-01", 1, language), encoding="utf-8"
            )
            readiness = self.workspace / "course" / language / "readiness.md"
            readiness.write_text(
                readiness.read_text(encoding="utf-8")
                + "competency_id: language.python.functions\nstate: learning\nfoundation_id: foundation-01\n",
                encoding="utf-8",
            )
        progress["learning_phase"] = "foundations"
        progress["current_unit"] = {"kind": "foundation", "id": "foundation-01"}
        progress["current_lesson"] = {"unit_id": "foundation-01", "id": "lesson-01"}
        progress["current_milestone"] = 0
        progress["learner_profile"]["competencies"] = [{
            "id": "language.python.functions",
            "category": "language",
            "state": "learning",
            "evidence_level": "none",
            "practice_depth": "unseen",
            "prerequisites": [],
            "required_by": ["milestone-01"],
            "blocking": True,
            "evidence": [],
        }]
        progress["foundation_units"] = [{
            "id": "foundation-01",
            "number": 1,
            "status": "ready",
            "competencies": ["language.python.functions"],
            "required_by": ["milestone-01"],
            "acceptance": ["f01-a01"],
            "risk_notes": [],
        }]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema4_rejects_design_metadata_leaking_into_lesson(self) -> None:
        self.upgrade_to_schema4()
        lesson = self.workspace / "course" / "en" / "milestones" / "01-stage" / "01.md"
        lesson.write_text(lesson.read_text(encoding="utf-8") + "\n## Evidence Ledger\nHidden data.\n", encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("exposes design-layer heading" in error for error in errors))

    def test_schema4_current_lesson_must_exist_in_design(self) -> None:
        progress = self.upgrade_to_schema4()
        progress["current_lesson"]["id"] = "lesson-99"
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        self.assertIn("current_lesson references unknown lesson", validate_workspace(self.workspace))

    def test_schema4_selected_validation_requires_complete_lesson_bundle(self) -> None:
        self.upgrade_to_schema4()
        selected = [
            "course/design/milestones/01-stage.json",
            "course/zh-CN/milestones/01-stage/01.md",
            "course/en/milestones/01-stage/01.md",
        ]

        errors = validate_selected_files(self.workspace, selected)

        self.assertTrue(any("must declare lessons" in error for error in errors))

    def test_schema3_requires_learning_mode_decision(self) -> None:
        progress = self.upgrade_to_schema3()
        progress["learner_profile"]["learning_mode"] = "pending"
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertIn("active schema-v3 course requires a learning_mode decision", errors)

    def test_schema3_requires_touch_ai_and_transfer_sections(self) -> None:
        self.upgrade_to_schema3()
        milestone = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        milestone.write_text(
            milestone.read_text(encoding="utf-8").replace("## First Touch", "## Try It"),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing heading: ## First Touch" in error for error in errors))

    def test_schema3_requires_complete_bilingual_getting_started(self) -> None:
        self.upgrade_to_schema3()
        guide = self.workspace / "course" / "GETTING_STARTED.md"
        guide.write_text(
            guide.read_text(encoding="utf-8").replace(
                "## 使用规则 / Usage Rules", "## Usage"
            ),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertIn(
            "course/GETTING_STARTED.md missing heading: ## 使用规则 / Usage Rules", errors
        )

    def test_schema3_passed_unit_requires_practice_evidence(self) -> None:
        progress = self.upgrade_to_schema3()
        progress["milestones"][0]["status"] = "passed"
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertIn("passed milestone requires practice evidence: milestone-01", errors)

    def test_schema3_accepts_passed_unit_with_practice_evidence(self) -> None:
        progress = self.upgrade_to_schema3()
        progress["milestones"][0]["status"] = "passed"
        progress["practice_evidence"] = [{
            "unit_id": "milestone-01",
            "depth": "explained",
            "manual_action": "Ran the command and changed the critical branch.",
            "observable_result": "The acceptance command passed.",
            "explanation": "Explained the input-to-output control flow.",
            "ai_usage": "AI generated scaffolding; learner authored the branch.",
            "timestamp": "2025-01-02T00:00:00Z",
        }]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema2_active_course_requires_readiness_decision(self) -> None:
        progress = self.upgrade_to_schema2()
        progress["learner_profile"]["assessment_mode"] = "pending"
        progress["assessment_history"] = []
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")
        errors = validate_workspace(self.workspace)
        self.assertIn("active schema-v2+ course requires a readiness decision", errors)
        self.assertIn("active schema-v2+ course requires assessment_history", errors)

    def test_schema2_requires_readiness_pair(self) -> None:
        self.upgrade_to_schema2()
        (self.workspace / "course" / "en" / "readiness.md").unlink()

        errors = validate_workspace(self.workspace)

        self.assertIn("missing course/en/readiness.md", errors)

    def test_schema2_requires_project_evolution_pair(self) -> None:
        self.upgrade_to_schema2()
        (self.workspace / "course" / "en" / "project-evolution.md").unlink()

        errors = validate_workspace(self.workspace)

        self.assertIn("missing course/en/project-evolution.md", errors)

    def test_schema2_milestone_requires_causal_evolution_headings(self) -> None:
        self.upgrade_to_schema2()
        milestone = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        milestone.write_text(
            milestone.read_text(encoding="utf-8").replace(
                "## New User Problem", "## Problem"
            ),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing heading: ## New User Problem" in error for error in errors))

    def test_schema2_blocks_milestone_with_unresolved_competency(self) -> None:
        progress = self.upgrade_to_schema2()
        progress["learner_profile"]["competencies"] = [{
            "id": "language.java.classes",
            "category": "language",
            "state": "unknown",
            "evidence_level": "none",
            "prerequisites": [],
            "required_by": ["milestone-01"],
            "blocking": True,
            "evidence": [],
        }]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("unresolved blocking competencies" in error for error in errors))

    def test_schema2_accepts_foundation_as_current_unit(self) -> None:
        progress = self.upgrade_to_schema2()
        for language in ("zh-CN", "en"):
            path = self.workspace / "course" / language / "foundations" / "F01-java-minimum.md"
            text = render_artifact("foundation-01", language, FOUNDATION_HEADINGS[language])
            text += "competency_id: language.java.classes\nrequired_by: milestone-01\nacceptance_id: f01-a01\n"
            path.write_text(text, encoding="utf-8")
            readiness = self.workspace / "course" / language / "readiness.md"
            readiness.write_text(
                readiness.read_text(encoding="utf-8")
                + "competency_id: language.java.classes\nstate: learning\nfoundation_id: foundation-01\n",
                encoding="utf-8",
            )
        progress["learning_phase"] = "foundations"
        progress["current_unit"] = {"kind": "foundation", "id": "foundation-01"}
        progress["current_milestone"] = 0
        progress["learner_profile"]["competencies"] = [{
            "id": "language.java.classes",
            "category": "language",
            "state": "learning",
            "evidence_level": "none",
            "prerequisites": [],
            "required_by": ["milestone-01"],
            "blocking": True,
            "evidence": [],
        }]
        progress["foundation_units"] = [{
            "id": "foundation-01",
            "number": 1,
            "status": "ready",
            "competencies": ["language.java.classes"],
            "required_by": ["milestone-01"],
            "acceptance": ["f01-a01"],
            "risk_notes": [],
        }]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema2_preserves_legacy_hint_history(self) -> None:
        progress = self.upgrade_to_schema2()
        progress["hint_history"] = [{
            "milestone_id": "milestone-01",
            "level": 1,
            "reason": "legacy hint",
            "timestamp": "2025-01-01T00:00:00Z",
        }]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")
        self.assertEqual(validate_workspace(self.workspace), [])

    def test_schema2_rejects_competency_cycle(self) -> None:
        progress = self.upgrade_to_schema2()
        progress["learner_profile"]["competencies"] = [
            {
                "id": "language.java.classes",
                "category": "language",
                "state": "unknown",
                "evidence_level": "none",
                "prerequisites": ["framework.spring.mvc"],
                "required_by": ["milestone-02"],
                "blocking": False,
                "evidence": [],
            },
            {
                "id": "framework.spring.mvc",
                "category": "framework",
                "state": "unknown",
                "evidence_level": "none",
                "prerequisites": ["language.java.classes"],
                "required_by": ["milestone-02"],
                "blocking": False,
                "evidence": [],
            },
        ]
        (self.workspace / "progress.json").write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertIn("learner competency prerequisites must be acyclic", errors)

    def test_missing_localized_required_file_is_reported(self) -> None:
        (self.workspace / "course" / "zh-CN" / "architecture.md").unlink()

        self.assertIn(
            "missing course/zh-CN/architecture.md", validate_workspace(self.workspace)
        )

    def test_partial_validation_allows_core_artifacts_not_created_yet(self) -> None:
        for language in ("zh-CN", "en"):
            (self.workspace / "course" / language / "architecture.md").unlink()

        self.assertEqual(validate_workspace(self.workspace, partial=True), [])

    def test_partial_validation_rejects_unpaired_core_artifact(self) -> None:
        (self.workspace / "course" / "zh-CN" / "architecture.md").unlink()

        errors = validate_workspace(self.workspace, partial=True)

        self.assertIn("unpaired partial core artifact: architecture.md", errors)

    def test_selected_validation_ignores_other_units_mid_publish(self) -> None:
        (self.workspace / "course" / "en" / "milestones" / "02-stage.md").unlink()
        for language in ("zh-CN", "en"):
            milestone = self.workspace / "course" / language / "milestones" / "01-stage.md"
            milestone.write_text(
                render_artifact("milestone-01", language, V3_MILESTONE_HEADINGS[language]),
                encoding="utf-8",
            )
        selected = [
            "course/zh-CN/milestones/01-stage.md",
            "course/en/milestones/01-stage.md",
        ]

        self.assertEqual(validate_selected_files(self.workspace, selected), [])

    def test_selected_validation_requires_its_own_language_pair(self) -> None:
        errors = validate_selected_files(
            self.workspace,
            ["course/zh-CN/milestones/01-stage.md"],
        )

        self.assertIn(
            "selected milestone is missing its declared language pair: 01-stage.md",
            errors,
        )

    def test_milestone_missing_hint_level_is_reported(self) -> None:
        milestone = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        milestone.write_text(
            milestone.read_text(encoding="utf-8").replace("## Hint 5", "## Reference"),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing heading: ## Hint 5" in error for error in errors))

    def test_teaching_inference_requires_confidence(self) -> None:
        project_map = self.workspace / "course" / "en" / "project-map.md"
        project_map.write_text(
            project_map.read_text(encoding="utf-8").replace("confidence: medium\n\n", ""),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("teaching_inference requires confidence" in error for error in errors))

    def test_mismatched_bilingual_artifact_id_is_reported(self) -> None:
        roadmap = self.workspace / "course" / "en" / "roadmap.md"
        roadmap.write_text(
            roadmap.read_text(encoding="utf-8").replace("artifact_id: roadmap", "artifact_id: different-roadmap"),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("artifact_id mismatch for roadmap.md" in error for error in errors))

    def test_mismatched_milestone_sets_are_reported(self) -> None:
        (self.workspace / "course" / "en" / "milestones" / "05-stage.md").unlink()

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("milestone file sets differ" in error for error in errors))

    def test_mismatched_source_locations_are_reported(self) -> None:
        milestone = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        milestone.write_text(
            milestone.read_text(encoding="utf-8").replace(
                "rationale: The ordering exposes one engineering pressure at a time.",
                "source: different/file.py::symbol\n\nrationale: The ordering exposes one engineering pressure at a time.",
            ),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("source locations differ" in error for error in errors))

    def test_mismatched_acceptance_ids_are_reported(self) -> None:
        zh = self.workspace / "course" / "zh-CN" / "milestones" / "01-stage.md"
        en = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        zh.write_text(zh.read_text(encoding="utf-8") + "acceptance_id: m01-a01\n", encoding="utf-8")
        en.write_text(en.read_text(encoding="utf-8") + "acceptance_id: different\n", encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("acceptance IDs differ" in error for error in errors))

    def test_mismatched_commands_are_reported(self) -> None:
        zh = self.workspace / "course" / "zh-CN" / "milestones" / "01-stage.md"
        en = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        zh.write_text(zh.read_text(encoding="utf-8") + "command: python app.py\n", encoding="utf-8")
        en.write_text(en.read_text(encoding="utf-8") + "command: python other.py\n", encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("commands differ" in error for error in errors))

    def test_schema3_practice_ids_must_match_across_languages(self) -> None:
        self.upgrade_to_schema3()
        zh = self.workspace / "course" / "zh-CN" / "milestones" / "01-stage.md"
        en = self.workspace / "course" / "en" / "milestones" / "01-stage.md"
        zh.write_text(zh.read_text(encoding="utf-8") + "practice_id: m01-p01\n", encoding="utf-8")
        en.write_text(en.read_text(encoding="utf-8") + "practice_id: m01-p02\n", encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("practice IDs differ" in error for error in errors))

    def test_inference_cannot_borrow_confidence_from_later_evidence(self) -> None:
        project_map = self.workspace / "course" / "en" / "project-map.md"
        text = project_map.read_text(encoding="utf-8").replace("confidence: medium\n\n", "")
        text += "\nevidence: code_evidence\nconfidence: high\nrationale: Later fact.\n"
        project_map.write_text(text, encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("teaching_inference requires confidence" in error for error in errors))

    def test_invalid_progress_status_is_reported(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "unknown"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("invalid course_status: unknown" in error for error in errors))

    def test_course_and_unit_status_vocabularies_are_separate(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "passed"
        progress["milestones"][0]["status"] = "complete"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertIn("invalid course_status: passed", errors)
        self.assertIn("milestones[0] has invalid status: complete", errors)

    def test_milestone_filename_numbers_must_be_consecutive(self) -> None:
        for language in ("zh-CN", "en"):
            source = self.workspace / "course" / language / "milestones" / "02-stage.md"
            source.rename(source.with_name("06-stage.md"))

        errors = validate_workspace(self.workspace)

        self.assertIn("milestone filename numbers must be consecutive from 1", errors)

    def test_missing_artifact_id_is_reported(self) -> None:
        roadmap = self.workspace / "course" / "en" / "roadmap.md"
        roadmap.write_text(
            roadmap.read_text(encoding="utf-8").replace("artifact_id: roadmap\n\n", ""),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing artifact_id" in error for error in errors))

    def test_body_metadata_cannot_replace_opening_frontmatter(self) -> None:
        roadmap = self.workspace / "course" / "en" / "roadmap.md"
        text = roadmap.read_text(encoding="utf-8")
        body = text.split("---", 2)[-1] + "\nartifact_id: roadmap\nlanguage: en\n"
        roadmap.write_text(body, encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing opening frontmatter" in error for error in errors))

    def test_evidence_bearing_artifact_requires_an_entry(self) -> None:
        project_map = self.workspace / "course" / "en" / "project-map.md"
        project_map.write_text(
            project_map.read_text(encoding="utf-8").replace("evidence: teaching_inference\n\n", ""),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("requires at least one evidence entry" in error for error in errors))

    def test_every_evidence_entry_requires_source(self) -> None:
        project_map = self.workspace / "course" / "en" / "project-map.md"
        project_map.write_text(
            project_map.read_text(encoding="utf-8").replace("source: fixture.py::symbol\n\n", ""),
            encoding="utf-8",
        )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("evidence requires source" in error for error in errors))

    def test_progress_milestone_requires_contract_fields(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        del progress["milestones"][0]["risk_notes"]
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("milestones[0] missing risk_notes" in error for error in errors))

    def test_progress_milestone_ids_must_match_course(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["milestones"][0]["id"] = "different"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("progress milestone IDs do not match" in error for error in errors))

    def test_milestone_id_must_match_filename_number(self) -> None:
        for language in ("zh-CN", "en"):
            milestone = self.workspace / "course" / language / "milestones" / "01-stage.md"
            milestone.write_text(
                milestone.read_text(encoding="utf-8").replace(
                    "artifact_id: milestone-01", "artifact_id: milestone-99"
                ),
                encoding="utf-8",
            )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("must use artifact_id milestone-01" in error for error in errors))

    def test_current_milestone_must_be_in_bounds(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["current_milestone"] = 6
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("current_milestone out of bounds" in error for error in errors))

    def test_complete_course_requires_terminal_milestone_statuses(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "complete"
        progress["current_milestone"] = 5
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("complete course has unfinished milestones" in error for error in errors))

    def test_complete_course_requires_final_paired_review(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "complete"
        progress["current_milestone"] = 5
        for milestone in progress["milestones"]:
            milestone["status"] = "passed"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("complete course requires a final paired review" in error for error in errors))

    def test_staged_course_with_milestones_requires_five_to_twelve_pairs(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "analyzing"
        progress["current_milestone"] = 0
        progress_path.write_text(json.dumps(progress), encoding="utf-8")
        for language in ("zh-CN", "en"):
            (self.workspace / "course" / language / "milestones" / "05-stage.md").unlink()

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("course requires 5-12 milestone pairs" in error for error in errors))

    def test_hint_history_requires_valid_level_and_milestone(self) -> None:
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["hint_history"] = [{"milestone_id": "missing", "level": 7, "reason": "asked", "timestamp": "now"}]
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("hint_history[0] has invalid level" in error for error in errors))
        self.assertTrue(any("hint_history[0] references unknown milestone" in error for error in errors))

    def test_unpaired_review_is_reported(self) -> None:
        review = self.workspace / "reviews" / "zh-CN" / "milestone-01-review-01.md"
        text = render_artifact("review-01-01", "zh-CN", REVIEW_HEADINGS["zh-CN"])
        text += "review_id: review-01-01\nmilestone_id: milestone-01\nverdict: passed\n"
        review.write_text(text, encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("review file sets differ" in error for error in errors))

    def test_review_verdicts_must_match(self) -> None:
        filename = "milestone-01-review-01.md"
        for language, verdict in (("zh-CN", "passed"), ("en", "needs_revision")):
            review = self.workspace / "reviews" / language / filename
            body = [
                "---",
                "artifact_id: review-01-01",
                f"language: {language}",
                "review_id: review-01-01",
                "milestone_id: milestone-01",
                f"verdict: {verdict}",
                "---",
            ]
            for heading in REVIEW_HEADINGS[language]:
                body.extend([heading, "Content."])
            body.extend([
                "evidence: code_evidence",
                "source: student/app.py::main",
                "rationale: Acceptance evidence.",
            ])
            review.write_text("\n\n".join(body) + "\n", encoding="utf-8")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("review verdict differs" in error for error in errors))

    def test_review_requires_language_neutral_metadata(self) -> None:
        filename = "milestone-01-review-01.md"
        for language in ("zh-CN", "en"):
            review = self.workspace / "reviews" / language / filename
            review.write_text(
                render_artifact("review-01-01", language, REVIEW_HEADINGS[language]),
                encoding="utf-8",
            )

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("missing review_id" in error for error in errors))

    def test_review_verdict_must_be_allowed(self) -> None:
        write_review_pair(self.workspace, verdict="excellent")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("invalid review verdict" in error for error in errors))

    def test_review_milestone_must_exist(self) -> None:
        write_review_pair(self.workspace, milestone_id="milestone-99")

        errors = validate_workspace(self.workspace)

        self.assertTrue(any("review references unknown milestone" in error for error in errors))

    def test_complete_course_accepts_valid_final_review(self) -> None:
        write_review_pair(self.workspace)
        progress_path = self.workspace / "progress.json"
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
        progress["course_status"] = "complete"
        progress["current_milestone"] = 5
        progress["last_review"] = "review-05-01"
        for milestone in progress["milestones"]:
            milestone["status"] = "passed"
        progress_path.write_text(json.dumps(progress), encoding="utf-8")

        self.assertEqual(validate_workspace(self.workspace), [])


if __name__ == "__main__":
    unittest.main()
