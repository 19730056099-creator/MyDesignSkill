#!/usr/bin/env python3
"""Validate a bilingual Project2Learn course workspace."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


LANGUAGES = ("zh-CN", "en")
COURSE_STATUSES = {"analyzing", "ready", "in_progress", "complete"}
UNIT_STATUSES = {"ready", "in_progress", "needs_revision", "passed", "skipped_with_risk"}
ACTIVE_STATUSES = COURSE_STATUSES - {"analyzing"}
LEARNING_PHASES = {"assessing", "foundations", "milestones", "complete"}
ASSESSMENT_MODES = {
    "pending", "assume_beginner", "self_report", "micro_diagnostic", "mixed", "waived"
}
LEARNING_MODES = {"pending", "product_builder", "cs_depth", "balanced"}
PRACTICE_DEPTHS = {"unseen", "touched", "explained", "debugged", "transferred"}
COMPETENCY_CATEGORIES = {"tooling", "language", "framework", "domain", "project_concept"}
COMPETENCY_STATES = {"unknown", "ready", "needs_refresh", "learning", "waived"}
EVIDENCE_LEVELS = {"none", "self_reported", "demonstrated", "waived"}
LEARNER_EVIDENCE_TYPES = {
    "learner_statement", "diagnostic_task", "student_work", "explicit_waiver"
}

CORE_HEADINGS = {
    "zh-CN": {
        "project-map.md": ["# 项目地图", "## 项目目的", "## 核心用户路径", "## 子系统", "## 证据台账", "## 未覆盖范围"],
        "architecture.md": ["# 架构", "## 系统上下文", "## 组件", "## 数据流", "## 控制流", "## 关键决策", "## 证据台账"],
        "knowledge-graph.md": ["# 知识图谱", "## 概念依赖", "## 学习优先级", "## 源码位置", "## 最小练习"],
        "readiness.md": ["# 学习准备", "## 项目所需能力", "## 学习者基线", "## 差距与决策", "## 前置补给路线", "## 进入项目的条件"],
        "project-evolution.md": ["# 项目演变", "## 最终问题与成熟能力", "## 最小可用起点", "## 演变总览", "## 阶段因果链", "## 最终架构如何形成", "## 教学路线声明", "## 证据台账"],
        "roadmap.md": ["# 重构路线", "## 路线原则", "## 里程碑总览", "## 覆盖范围", "## 教学性推断"],
    },
    "en": {
        "project-map.md": ["# Project Map", "## Purpose", "## Core User Journey", "## Subsystems", "## Evidence Ledger", "## Uncovered Scope"],
        "architecture.md": ["# Architecture", "## System Context", "## Components", "## Data Flow", "## Control Flow", "## Key Decisions", "## Evidence Ledger"],
        "knowledge-graph.md": ["# Knowledge Graph", "## Concept Dependencies", "## Learning Priority", "## Source Locations", "## Minimal Exercises"],
        "readiness.md": ["# Learning Readiness", "## Project-Required Competencies", "## Learner Baseline", "## Gaps and Decisions", "## Foundation Route", "## Entry Conditions"],
        "project-evolution.md": ["# Project Evolution", "## Final Problem and Mature Capabilities", "## Minimum Viable Starting Point", "## Evolution Overview", "## Stage Causal Chain", "## How the Final Architecture Emerges", "## Teaching-Route Disclaimer", "## Evidence Ledger"],
        "roadmap.md": ["# Reconstruction Roadmap", "## Roadmap Principles", "## Milestone Overview", "## Coverage", "## Teaching Inferences"],
    },
}

FOUNDATION_HEADINGS = {
    "zh-CN": ["# 前置补给单元", "## 为什么现在需要", "## 依赖", "## 最小概念", "## 小例子", "## 动手练习", "## 通过标准", "## 项目桥接", "## 暂不学习", "## 完成结论"],
    "en": ["# Foundation Unit", "## Why It Is Needed Now", "## Dependencies", "## Minimal Concepts", "## Small Example", "## Hands-on Exercise", "## Exit Criteria", "## Project Bridge", "## Not Learning Yet", "## Completion Decision"],
}

V3_FOUNDATION_HEADINGS = {
    "zh-CN": [*FOUNDATION_HEADINGS["zh-CN"], "## 首次触摸", "## AI 使用边界", "## 理解与迁移检查"],
    "en": [*FOUNDATION_HEADINGS["en"], "## First Touch", "## AI Usage Boundary", "## Understanding and Transfer Check"],
}

LEGACY_MILESTONE_HEADINGS = {
    "zh-CN": ["# 里程碑", "## 目标", "## 可观察结果", "## 设计压力", "## 范围", "## 约束", "## 前置知识", "## 任务", "## 验收", "## 提示 1", "## 提示 2", "## 提示 3", "## 提示 4", "## 提示 5", "## 下一项压力", "## 源码桥接", "## 证据台账", "## 完成结论"],
    "en": ["# Milestone", "## Goal", "## Observable Result", "## Design Pressure", "## Scope", "## Constraints", "## Prerequisites", "## Tasks", "## Acceptance", "## Hint 1", "## Hint 2", "## Hint 3", "## Hint 4", "## Hint 5", "## Next Pressure", "## Source Bridge", "## Evidence Ledger", "## Completion Decision"],
}

MILESTONE_HEADINGS = {
    "zh-CN": ["# 里程碑", "## 当前版本", "## 上一版本解决了什么", "## 用户遇到的新问题", "## 本阶段引入什么", "## 目标", "## 可观察结果", "## 本阶段解决什么", "## 范围", "## 暂时不解决什么", "## 前置知识", "## 任务", "## 验收", "## 提示 1", "## 提示 2", "## 提示 3", "## 提示 4", "## 提示 5", "## 下一阶段为什么会出现", "## 源码桥接", "## 证据台账", "## 完成结论"],
    "en": ["# Milestone", "## Current Version", "## What the Previous Version Solved", "## New User Problem", "## What This Stage Introduces", "## Goal", "## Observable Result", "## What This Stage Solves", "## Scope", "## Not Solving Yet", "## Prerequisites", "## Tasks", "## Acceptance", "## Hint 1", "## Hint 2", "## Hint 3", "## Hint 4", "## Hint 5", "## Why the Next Stage Appears", "## Source Bridge", "## Evidence Ledger", "## Completion Decision"],
}

V3_MILESTONE_HEADINGS = {
    "zh-CN": [*MILESTONE_HEADINGS["zh-CN"], "## 首次触摸", "## AI 使用边界", "## 理解与迁移检查"],
    "en": [*MILESTONE_HEADINGS["en"], "## First Touch", "## AI Usage Boundary", "## Understanding and Transfer Check"],
}

V3_CORE_HEADINGS = {
    language: {filename: list(headings) for filename, headings in files.items()}
    for language, files in CORE_HEADINGS.items()
}
V3_CORE_HEADINGS["zh-CN"]["project-map.md"] += ["## 技术层级地图", "## 故障定位地图"]
V3_CORE_HEADINGS["en"]["project-map.md"] += ["## Technology Layer Map", "## Troubleshooting Map"]
V3_CORE_HEADINGS["zh-CN"]["knowledge-graph.md"] += ["## 螺旋复现与理解深度"]
V3_CORE_HEADINGS["en"]["knowledge-graph.md"] += ["## Spiral Recurrence and Understanding Depth"]
V3_CORE_HEADINGS["zh-CN"]["readiness.md"] += ["## 学习模式与 AI 边界"]
V3_CORE_HEADINGS["en"]["readiness.md"] += ["## Learning Mode and AI Boundary"]

V4_LESSON_HEADINGS = {
    "zh-CN": [
        "## 先试一下", "## 你看到了什么", "## 只讲现在需要的",
        "## 把它用回项目", "## 停一下，自己做", "## 现在你的项目可以",
        "## 下一步会遇到什么",
    ],
    "en": [
        "## Try This First", "## What Did You Notice?", "## Only What You Need Now",
        "## Put It Back Into the Project", "## Stop and Do It Yourself",
        "## What Your Project Can Do Now", "## The Next Problem",
    ],
}

V4_FORBIDDEN_LEARNER_HEADINGS = {
    "## 当前版本", "## 上一版本解决了什么", "## 用户遇到的新问题", "## 本阶段引入什么",
    "## 证据台账", "## AI 使用边界", "## Current Version",
    "## What the Previous Version Solved", "## New User Problem",
    "## What This Stage Introduces", "## Evidence Ledger", "## AI Usage Boundary",
}

GETTING_STARTED_HEADINGS = [
    "# 学习指南 / Learning Guide",
    "## 课程是什么 / What This Course Is",
    "## 文件总览与阅读顺序 / File Overview and Reading Order",
    "## 各文件的用途速查 / Quick File Reference",
    "## 使用规则 / Usage Rules",
    "## 现在就开始 / Start Now",
]

REVIEW_HEADINGS = {
    "zh-CN": ["# 阶段评审", "## 优点", "## 正确性", "## 验收证据", "## 当前阶段权衡", "## 下一项规模压力", "## 参考项目对比", "## 必须修改", "## 可选改进", "## 结论"],
    "en": ["# Stage Review", "## Strengths", "## Correctness", "## Acceptance Evidence", "## Current-Stage Tradeoffs", "## Next Scale Pressure", "## Reference Comparison", "## Required Changes", "## Optional Improvements", "## Verdict"],
}


def _frontmatter(text: str) -> dict[str, str] | None:
    match = re.match(r"\A---[ \t]*\r?\n(.*?)\r?\n---[ \t]*(?:\r?\n|$)", text, re.DOTALL)
    if not match:
        return None
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def _metadata(text: str, key: str) -> str | None:
    metadata = _frontmatter(text)
    return metadata.get(key) if metadata else None


def _values(text: str, key: str) -> list[str]:
    return sorted(
        match.group(1).strip()
        for match in re.finditer(rf"^{re.escape(key)}:\s*(.+?)\s*$", text, re.MULTILINE)
    )


def _check_headings(path: Path, headings: list[str], errors: list[str]) -> str:
    text = path.read_text(encoding="utf-8")
    lines = {line.strip() for line in text.splitlines()}
    relative = path.as_posix()
    for heading in headings:
        if heading not in lines:
            errors.append(f"{relative} missing heading: {heading}")
    return text


def _core_headings(language: str, filename: str, schema_version: int | None) -> list[str]:
    headings = V3_CORE_HEADINGS if schema_version == 3 else CORE_HEADINGS
    return headings[language][filename]


def _foundation_headings(language: str, schema_version: int | None) -> list[str]:
    headings = V3_FOUNDATION_HEADINGS if schema_version == 3 else FOUNDATION_HEADINGS
    return headings[language]


def _check_milestone_headings(
    path: Path, language: str, schema_version: int | None, errors: list[str]
) -> str:
    if schema_version == 1:
        text = path.read_text(encoding="utf-8")
        lines = {line.strip() for line in text.splitlines()}
        if all(heading in lines for heading in MILESTONE_HEADINGS[language]):
            return text
        return _check_headings(path, LEGACY_MILESTONE_HEADINGS[language], errors)
    headings = V3_MILESTONE_HEADINGS if schema_version == 3 else MILESTONE_HEADINGS
    return _check_headings(path, headings[language], errors)


def _check_getting_started(path: Path, errors: list[str], *, strict: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if "init_workspace.py" in text and "MUST replace" in text:
        errors.append("course/GETTING_STARTED.md is still the init placeholder")
    if _metadata(text, "artifact_id") != "getting-started":
        errors.append("course/GETTING_STARTED.md missing artifact_id: getting-started")
    if strict:
        if _metadata(text, "language") != "bilingual":
            errors.append("course/GETTING_STARTED.md schema-v3+ guide requires language: bilingual")
        lines = {line.strip() for line in text.splitlines()}
        for heading in GETTING_STARTED_HEADINGS:
            if heading not in lines:
                errors.append(f"course/GETTING_STARTED.md missing heading: {heading}")


def _check_evidence(path: Path, text: str, errors: list[str]) -> int:
    evidence_blocks = list(re.finditer(r"^evidence:\s*(\S+)\s*$", text, re.MULTILINE))
    for index, match in enumerate(evidence_blocks):
        end = evidence_blocks[index + 1].start() if index + 1 < len(evidence_blocks) else len(text)
        block = text[match.start():end]
        evidence_type = match.group(1)
        if evidence_type not in {"code_evidence", "document_evidence", "teaching_inference"}:
            errors.append(f"{path.as_posix()} has invalid evidence type: {evidence_type}")
        if not re.search(r"^source:\s*\S.+$", block, re.MULTILINE):
            errors.append(f"{path.as_posix()} evidence requires source")
        if not re.search(r"^rationale:\s*\S.+$", block, re.MULTILINE):
            errors.append(f"{path.as_posix()} evidence requires rationale")
        if evidence_type == "teaching_inference" and not re.search(
            r"^confidence:\s*(low|medium|high)\s*$", block, re.MULTILINE
        ):
            errors.append(f"{path.as_posix()} teaching_inference requires confidence")
    return len(evidence_blocks)


def _check_v4_design(
    path: Path, kind: str, expected_number: int, errors: list[str]
) -> tuple[dict | None, dict[str, dict]]:
    relative = path.as_posix()
    try:
        design = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid unit design {relative}: {error}")
        return None, {}
    if not isinstance(design, dict):
        errors.append(f"{relative} design must be object")
        return None, {}

    for key in (
        "schema_version", "artifact_id", "unit_id", "kind", "number", "slug",
        "competencies", "prerequisite_foundations", "practice_design", "acceptance",
        "hints", "source_bridge", "evidence", "lessons",
    ):
        if key not in design:
            errors.append(f"{relative} design missing {key}")
    if design.get("schema_version") != 1:
        errors.append(f"{relative} design schema_version must be 1")
    if design.get("kind") != kind:
        errors.append(f"{relative} design kind must be {kind}")
    if design.get("number") != expected_number:
        errors.append(f"{relative} design number must be {expected_number}")
    expected_id = f"{'foundation' if kind == 'foundation' else 'milestone'}-{expected_number:02d}"
    if design.get("unit_id") != expected_id:
        errors.append(f"{relative} design unit_id must be {expected_id}")
    if design.get("artifact_id") != f"{expected_id}-design":
        errors.append(f"{relative} design artifact_id must be {expected_id}-design")
    if not isinstance(design.get("slug"), str) or not design.get("slug"):
        errors.append(f"{relative} design slug must be non-empty string")
    else:
        filename_slug = re.sub(r"^(?:F)?\d{2}-", "", path.stem, flags=re.IGNORECASE)
        if design["slug"] != filename_slug:
            errors.append(f"{relative} design slug must match filename: {filename_slug}")
    for key in ("competencies", "prerequisite_foundations", "acceptance", "source_bridge", "evidence"):
        if not isinstance(design.get(key), list):
            errors.append(f"{relative} design {key} must be list")

    if kind == "foundation":
        if not isinstance(design.get("why_now"), str) or not design.get("why_now"):
            errors.append(f"{relative} foundation design requires why_now")
    else:
        causal = design.get("causal_stage")
        causal_keys = (
            "current_version", "previous_value", "new_problem", "introduced_change",
            "resolved_pressure", "deferred_limit", "next_pressure",
        )
        if not isinstance(causal, dict):
            errors.append(f"{relative} milestone design requires causal_stage object")
        else:
            for key in causal_keys:
                if not isinstance(causal.get(key), str) or not causal[key]:
                    errors.append(f"{relative} causal_stage.{key} must be non-empty string")

    practice = design.get("practice_design")
    if not isinstance(practice, dict):
        errors.append(f"{relative} design practice_design must be object")
    else:
        for key in ("ai_allowed", "learner_owned", "must_explain", "transfer_checks"):
            if not isinstance(practice.get(key), list):
                errors.append(f"{relative} practice_design.{key} must be list")

    acceptance = design.get("acceptance")
    if isinstance(acceptance, list):
        if not acceptance:
            errors.append(f"{relative} design requires at least one acceptance item")
        for index, item in enumerate(acceptance):
            if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
                errors.append(f"{relative} acceptance[{index}] requires non-empty id")

    hints = design.get("hints")
    if not isinstance(hints, list) or [hint.get("level") for hint in hints if isinstance(hint, dict)] != [1, 2, 3, 4, 5]:
        errors.append(f"{relative} design requires hint levels 1-5 in order")
    elif any(not isinstance(hint.get("content"), str) or not hint["content"] for hint in hints):
        errors.append(f"{relative} design hint content must be non-empty")

    evidence = design.get("evidence")
    if isinstance(evidence, list):
        if not evidence:
            errors.append(f"{relative} design requires at least one evidence entry")
        for index, entry in enumerate(evidence):
            prefix = f"{relative} evidence[{index}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be object")
                continue
            evidence_type = entry.get("type")
            if evidence_type not in {"code_evidence", "document_evidence", "teaching_inference"}:
                errors.append(f"{prefix} has invalid type: {evidence_type}")
            for key in ("source", "rationale"):
                if not isinstance(entry.get(key), str) or not entry[key]:
                    errors.append(f"{prefix}.{key} must be non-empty string")
            if evidence_type == "teaching_inference" and entry.get("confidence") not in {"low", "medium", "high"}:
                errors.append(f"{prefix} teaching_inference requires confidence")

    lessons = design.get("lessons")
    minimum, maximum = (1, 3) if kind == "foundation" else (2, 5)
    if not isinstance(lessons, list) or not minimum <= len(lessons) <= maximum:
        errors.append(f"{relative} {kind} design requires {minimum}-{maximum} lessons")
        return design, {}
    lesson_map: dict[str, dict] = {}
    required_lesson_fields = (
        "id", "artifact_id", "cognitive_goal", "situation", "friction", "action",
        "observable_result", "concept_name", "minimum_theory", "project_delta", "next_problem",
    )
    for index, lesson in enumerate(lessons, 1):
        prefix = f"{relative} lessons[{index - 1}]"
        if not isinstance(lesson, dict):
            errors.append(f"{prefix} must be object")
            continue
        expected_lesson_id = f"lesson-{index:02d}"
        if lesson.get("id") != expected_lesson_id:
            errors.append(f"{prefix}.id must be {expected_lesson_id}")
        expected_artifact = f"{expected_id}-{expected_lesson_id}"
        if lesson.get("artifact_id") != expected_artifact:
            errors.append(f"{prefix}.artifact_id must be {expected_artifact}")
        for key in required_lesson_fields:
            if not isinstance(lesson.get(key), str) or not lesson[key]:
                errors.append(f"{prefix}.{key} must be non-empty string")
        deferred = lesson.get("deferred")
        if deferred is not None:
            if not isinstance(deferred, dict):
                errors.append(f"{prefix}.deferred must be null or object")
            else:
                for key in ("concept", "why_not_now", "revisit_when"):
                    if not isinstance(deferred.get(key), str) or not deferred[key]:
                        errors.append(f"{prefix}.deferred.{key} must be non-empty string")
        lesson_map[f"{index:02d}.md"] = lesson
    return design, lesson_map


def _check_v4_lesson(
    path: Path, language: str, unit_id: str, lesson: dict, errors: list[str]
) -> str:
    text = _check_headings(path, V4_LESSON_HEADINGS[language], errors)
    relative = path.as_posix()
    metadata = _frontmatter(text)
    if metadata is None:
        errors.append(f"{relative} missing opening frontmatter")
        return text
    expected = {
        "artifact_id": lesson.get("artifact_id"),
        "language": language,
        "unit_id": unit_id,
        "lesson_id": lesson.get("id"),
    }
    for key, value in expected.items():
        if metadata.get(key) != value:
            errors.append(f"{relative} {key} must be {value}")
    lines = {line.strip() for line in text.splitlines()}
    leaked = sorted(lines & V4_FORBIDDEN_LEARNER_HEADINGS)
    for heading in leaked:
        errors.append(f"{relative} exposes design-layer heading: {heading}")
    optional = "## 现在先不讲" if language == "zh-CN" else "## Not Now"
    optional_count = text.count(optional)
    if optional_count > 1:
        errors.append(f"{relative} may contain at most one {optional} section")
    if lesson.get("deferred") is None and optional_count:
        errors.append(f"{relative} has an undeclared {optional} section")
    if lesson.get("deferred") is not None and optional_count != 1:
        errors.append(f"{relative} must render its declared {optional} section")
    return text


def _validate_v4_bundles(
    workspace: Path, kind: str, errors: list[str], *, partial: bool
) -> tuple[list[str], dict[str, list[str]]]:
    plural = "foundations" if kind == "foundation" else "milestones"
    design_root = workspace / "course" / "design" / plural
    if not design_root.is_dir():
        if not partial:
            errors.append(f"missing course/design/{plural} directory")
        return [], {}
    design_paths = sorted(design_root.glob("*.json"))
    design_stems = {path.stem for path in design_paths}
    localized_stems = {}
    for language in LANGUAGES:
        localized_root = workspace / "course" / language / plural
        localized_stems[language] = {
            path.name for path in localized_root.iterdir() if path.is_dir()
        } if localized_root.is_dir() else set()
        legacy_files = sorted(path.name for path in localized_root.glob("*.md"))
        if legacy_files:
            errors.append(
                f"schema-v4 {plural} must use lesson directories, not single files: {legacy_files}"
            )
    if localized_stems["zh-CN"] != localized_stems["en"]:
        errors.append(f"{kind} lesson bundle sets differ between zh-CN and en")
    if not partial:
        for stem in sorted(design_stems - localized_stems["zh-CN"]):
            errors.append(f"missing bilingual {kind} lesson bundle: {stem}")
        for stem in sorted(localized_stems["zh-CN"] - design_stems):
            errors.append(f"{kind} lesson bundle lacks design JSON: {stem}")

    ids: list[str] = []
    unit_lessons: dict[str, list[str]] = {}
    numbers: list[int] = []
    pattern = r"^F(\d{2})-" if kind == "foundation" else r"^(\d{2})-"
    for design_path in design_paths:
        match = re.match(pattern, design_path.name, re.IGNORECASE if kind == "foundation" else 0)
        if not match:
            errors.append(f"{kind} design filename lacks numeric prefix: {design_path.name}")
            continue
        number = int(match.group(1))
        numbers.append(number)
        design, lesson_map = _check_v4_design(design_path, kind, number, errors)
        if design is None:
            continue
        unit_id = design.get("unit_id")
        if isinstance(unit_id, str):
            ids.append(unit_id)
            unit_lessons[unit_id] = [lesson.get("id") for lesson in lesson_map.values()]
        if design_path.stem not in localized_stems["zh-CN"] & localized_stems["en"]:
            continue
        expected_files = set(lesson_map)
        texts: dict[tuple[str, str], str] = {}
        for language in LANGUAGES:
            unit_root = workspace / "course" / language / plural / design_path.stem
            actual_files = {path.name for path in unit_root.glob("*.md")}
            if actual_files != expected_files:
                errors.append(
                    f"course/{language}/{plural}/{design_path.stem} lesson files "
                    f"must be {sorted(expected_files)}"
                )
            for filename in sorted(actual_files & expected_files):
                lesson_path = unit_root / filename
                texts[(language, filename)] = _check_v4_lesson(
                    lesson_path, language, unit_id, lesson_map[filename], errors
                )
        for filename in sorted(expected_files):
            zh = texts.get(("zh-CN", filename))
            en = texts.get(("en", filename))
            if zh is None or en is None:
                continue
            for key in ("artifact_id", "unit_id", "lesson_id"):
                if _metadata(zh, key) != _metadata(en, key):
                    errors.append(f"{key} differs for {plural}/{design_path.stem}/{filename}")
    if sorted(numbers) != list(range(1, len(numbers) + 1)):
        errors.append(f"{kind} design numbers must be consecutive from 1")
    return ids, unit_lessons


def _validate_v4_reviews(
    workspace: Path, milestone_ids: list[str], errors: list[str]
) -> dict[str, dict[str, str]]:
    review_paths = {
        language: sorted((workspace / "reviews" / language).glob("*.md"))
        for language in LANGUAGES
    }
    names = {language: {path.name for path in paths} for language, paths in review_paths.items()}
    if names["zh-CN"] != names["en"]:
        errors.append("review file sets differ between zh-CN and en")
    reviews: dict[str, dict[str, str]] = {}
    for filename in sorted(names["zh-CN"] & names["en"]):
        texts = {}
        for language in LANGUAGES:
            path = workspace / "reviews" / language / filename
            text = _check_headings(path, REVIEW_HEADINGS[language], errors)
            texts[language] = text
            for key in ("artifact_id", "review_id", "milestone_id", "verdict"):
                if not _metadata(text, key):
                    errors.append(f"{path.relative_to(workspace).as_posix()} missing {key}")
            if _metadata(text, "language") != language:
                errors.append(f"{path.relative_to(workspace).as_posix()} has incorrect language metadata")
            if _check_evidence(path.relative_to(workspace), text, errors) == 0:
                errors.append(f"{path.relative_to(workspace).as_posix()} requires at least one evidence entry")
        for key in ("artifact_id", "review_id", "milestone_id", "verdict"):
            if _metadata(texts["zh-CN"], key) != _metadata(texts["en"], key):
                errors.append(f"review {key} differs for {filename}")
        for key, label in (("source", "review source locations"), ("acceptance_id", "review acceptance IDs"), ("command", "review commands")):
            if _values(texts["zh-CN"], key) != _values(texts["en"], key):
                errors.append(f"{label} differ for {filename}")
        review_id = _metadata(texts["zh-CN"], "review_id")
        milestone_id = _metadata(texts["zh-CN"], "milestone_id")
        verdict = _metadata(texts["zh-CN"], "verdict")
        if verdict not in {"passed", "needs_revision", "skipped_with_risk"}:
            errors.append(f"invalid review verdict for {filename}: {verdict}")
        if milestone_id not in milestone_ids:
            errors.append(f"review references unknown milestone for {filename}: {milestone_id}")
        if review_id and milestone_id and verdict:
            reviews[review_id] = {"milestone_id": milestone_id, "verdict": verdict}
    return reviews


def _validate_v4_workspace(
    workspace: Path, progress: dict, *, partial: bool
) -> list[str]:
    errors: list[str] = []
    core_texts: dict[str, dict[str, str]] = {language: {} for language in LANGUAGES}
    if not (workspace / "student").is_dir():
        errors.append("missing student directory")
    for language in LANGUAGES:
        if not (workspace / "reviews" / language).is_dir():
            errors.append(f"missing reviews/{language} directory")
        course_root = workspace / "course" / language
        for filename in CORE_HEADINGS[language]:
            path = course_root / filename
            relative = path.relative_to(workspace)
            if not path.is_file():
                if not partial:
                    errors.append(f"missing {relative.as_posix()}")
                continue
            text = _check_headings(path, V3_CORE_HEADINGS[language][filename], errors)
            core_texts[language][filename] = text
            if _metadata(text, "artifact_id") is None:
                errors.append(f"{relative.as_posix()} missing artifact_id")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            evidence_count = _check_evidence(relative, text, errors)
            if filename in {"project-map.md", "architecture.md", "project-evolution.md", "roadmap.md"} and evidence_count == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
    for filename in CORE_HEADINGS["en"]:
        zh = core_texts["zh-CN"].get(filename)
        en = core_texts["en"].get(filename)
        if zh is None or en is None:
            if partial and (zh is None) != (en is None):
                errors.append(f"unpaired partial core artifact: {filename}")
            continue
        if _metadata(zh, "artifact_id") != _metadata(en, "artifact_id"):
            errors.append(f"artifact_id mismatch for {filename}")
        if _values(zh, "source") != _values(en, "source"):
            errors.append(f"source locations differ for {filename}")
        if filename == "readiness.md":
            for key, label in (
                ("competency_id", "competency IDs"), ("state", "competency states"),
                ("required_by", "readiness milestone links"),
                ("foundation_id", "readiness foundation IDs"), ("learning_mode", "learning modes"),
            ):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")
        if filename == "project-map.md":
            for key, label in (("layer_id", "technology layer IDs"), ("failure_id", "troubleshooting failure IDs")):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")
        if filename == "knowledge-graph.md":
            for key, label in (("practice_depth", "practice depths"), ("reappears_in", "spiral recurrence links")):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")

    foundation_ids, foundation_lessons = _validate_v4_bundles(
        workspace, "foundation", errors, partial=partial
    )
    milestone_ids, milestone_lessons = _validate_v4_bundles(
        workspace, "milestone", errors, partial=partial
    )
    if len(foundation_ids) > 8:
        errors.append("foundation route must stay bounded to at most 8 units")
    status = progress.get("course_status")
    if not partial and (status in ACTIVE_STATUSES or milestone_ids) and not 5 <= len(milestone_ids) <= 12:
        errors.append(f"course requires 5-12 milestone bundles, found {len(milestone_ids)}")

    guide = workspace / "course" / "GETTING_STARTED.md"
    if status in ACTIVE_STATUSES:
        if not guide.is_file():
            errors.append("missing course/GETTING_STARTED.md learning-order guide")
        else:
            _check_getting_started(guide, errors, strict=True)
    reviews = _validate_v4_reviews(workspace, milestone_ids, errors)

    readiness = core_texts["zh-CN"].get("readiness.md")
    profile = progress.get("learner_profile")
    if readiness is not None and isinstance(profile, dict):
        if _values(readiness, "learning_mode") != [profile.get("learning_mode")]:
            errors.append("readiness learning_mode does not match progress learner profile")
        records = profile.get("competencies")
        if isinstance(records, list):
            expected_ids = sorted(record.get("id") for record in records if isinstance(record, dict) and isinstance(record.get("id"), str))
            expected_states = sorted(record.get("state") for record in records if isinstance(record, dict) and isinstance(record.get("state"), str))
            if _values(readiness, "competency_id") != expected_ids:
                errors.append("readiness competency IDs do not match progress learner profile")
            if _values(readiness, "state") != expected_states:
                errors.append("readiness competency states do not match progress learner profile")
        foundation_records = progress.get("foundation_units")
        if isinstance(foundation_records, list):
            expected_foundations = sorted(
                record.get("id") for record in foundation_records
                if isinstance(record, dict) and isinstance(record.get("id"), str)
            )
            if _values(readiness, "foundation_id") != expected_foundations:
                errors.append("readiness foundation IDs do not match progress foundation units")
    unit_lessons = {**foundation_lessons, **milestone_lessons}
    _validate_progress(
        progress, foundation_ids, milestone_ids, reviews, errors, unit_lessons=unit_lessons
    )
    return errors


def _load_progress(workspace: Path, errors: list[str]) -> dict | None:
    progress_path = workspace / "progress.json"
    if not progress_path.is_file():
        errors.append("missing progress.json")
        return None
    try:
        progress = json.loads(progress_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"invalid progress.json: {error}")
        return None
    return progress


def _has_cycle(dependencies: dict[str, list[str]]) -> bool:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for dependency in dependencies.get(node, []):
            if dependency in dependencies and visit(dependency):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in dependencies)


def _validate_learner_profile(
    progress: dict,
    milestone_ids: list[str],
    errors: list[str],
    schema_version: int,
) -> dict[str, dict]:
    profile = progress.get("learner_profile")
    if not isinstance(profile, dict):
        errors.append("progress.json learner_profile must be object")
        return {}
    required_profile_keys = ["assessment_mode", "goals", "constraints", "competencies"]
    if schema_version in {3, 4}:
        required_profile_keys.append("learning_mode")
    for key in required_profile_keys:
        if key not in profile:
            errors.append(f"progress.json learner_profile missing {key}")
    if profile.get("assessment_mode") not in ASSESSMENT_MODES:
        errors.append(f"invalid learner assessment_mode: {profile.get('assessment_mode')}")
    if schema_version in {3, 4} and profile.get("learning_mode") not in LEARNING_MODES:
        errors.append(f"invalid learner learning_mode: {profile.get('learning_mode')}")
    for key in ("goals", "constraints", "competencies"):
        if not isinstance(profile.get(key), list):
            errors.append(f"progress.json learner_profile.{key} must be list")

    competencies: dict[str, dict] = {}
    records = profile.get("competencies")
    if not isinstance(records, list):
        return competencies
    dependencies: dict[str, list[str]] = {}
    for index, record in enumerate(records):
        prefix = f"learner_profile.competencies[{index}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be object")
            continue
        required = [
            "id", "category", "state", "evidence_level", "prerequisites",
            "required_by", "blocking", "evidence",
        ]
        if schema_version in {3, 4}:
            required.append("practice_depth")
        for key in required:
            if key not in record:
                errors.append(f"{prefix} missing {key}")
        competency_id = record.get("id")
        if not isinstance(competency_id, str) or not competency_id:
            errors.append(f"{prefix}.id must be non-empty string")
            continue
        if competency_id in competencies:
            errors.append(f"duplicate competency id: {competency_id}")
        competencies[competency_id] = record
        if record.get("category") not in COMPETENCY_CATEGORIES:
            errors.append(f"{prefix} has invalid category: {record.get('category')}")
        state = record.get("state")
        level = record.get("evidence_level")
        if state not in COMPETENCY_STATES:
            errors.append(f"{prefix} has invalid state: {state}")
        if level not in EVIDENCE_LEVELS:
            errors.append(f"{prefix} has invalid evidence_level: {level}")
        if schema_version in {3, 4} and record.get("practice_depth") not in PRACTICE_DEPTHS:
            errors.append(f"{prefix} has invalid practice_depth: {record.get('practice_depth')}")
        if state == "ready" and level not in {"self_reported", "demonstrated"}:
            errors.append(f"{prefix} ready state requires learner evidence")
        if state == "waived" and level != "waived":
            errors.append(f"{prefix} waived state requires waived evidence_level")
        if not isinstance(record.get("blocking"), bool):
            errors.append(f"{prefix}.blocking must be boolean")
        for key in ("prerequisites", "required_by", "evidence"):
            if not isinstance(record.get(key), list):
                errors.append(f"{prefix}.{key} must be list")
        prereqs = record.get("prerequisites")
        dependencies[competency_id] = prereqs if isinstance(prereqs, list) else []
        required_by = record.get("required_by")
        if isinstance(required_by, list):
            for milestone_id in required_by:
                if milestone_ids and milestone_id not in milestone_ids:
                    errors.append(f"{prefix} references unknown milestone: {milestone_id}")
        evidence = record.get("evidence")
        if isinstance(evidence, list):
            for evidence_index, entry in enumerate(evidence):
                evidence_prefix = f"{prefix}.evidence[{evidence_index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{evidence_prefix} must be object")
                    continue
                if entry.get("type") not in LEARNER_EVIDENCE_TYPES:
                    errors.append(f"{evidence_prefix} has invalid type: {entry.get('type')}")
                for key in ("summary", "timestamp"):
                    if not isinstance(entry.get(key), str) or not entry[key]:
                        errors.append(f"{evidence_prefix}.{key} must be non-empty string")

    for competency_id, prereqs in dependencies.items():
        for dependency in prereqs:
            if dependency not in competencies:
                errors.append(f"competency {competency_id} references unknown prerequisite: {dependency}")
    if _has_cycle(dependencies):
        errors.append("learner competency prerequisites must be acyclic")
    return competencies


def _validate_progress(
    progress: dict | None,
    foundation_ids: list[str],
    milestone_ids: list[str],
    reviews: dict[str, dict[str, str]],
    errors: list[str],
    *,
    unit_lessons: dict[str, list[str]] | None = None,
) -> None:
    if progress is None:
        return
    required_types = {
        "schema_version": int,
        "repository": dict,
        "course_status": str,
        "current_milestone": int,
        "milestones": list,
        "hint_history": list,
        "open_improvements": list,
        "learner_choices": list,
        "recommended_next_action": str,
    }
    for key, expected_type in required_types.items():
        if key not in progress:
            errors.append(f"progress.json missing {key}")
        elif not isinstance(progress[key], expected_type) or (
            expected_type is int and isinstance(progress[key], bool)
        ):
            errors.append(f"progress.json {key} must be {expected_type.__name__}")
    if "last_review" not in progress:
        errors.append("progress.json missing last_review")
    elif progress["last_review"] is not None and not isinstance(progress["last_review"], str):
        errors.append("progress.json last_review must be null or string")
    elif isinstance(progress["last_review"], str) and progress["last_review"] not in reviews:
        errors.append("progress.json last_review references unknown paired review")
    schema_version = progress.get("schema_version")
    if schema_version not in {1, 2, 3, 4}:
        errors.append(f"unsupported schema_version: {schema_version}")

    repository = progress.get("repository")
    if isinstance(repository, dict):
        for key in ("name", "source", "revision"):
            if not isinstance(repository.get(key), str):
                errors.append(f"progress.json repository.{key} must be string")

    status = progress.get("course_status")
    if status not in COURSE_STATUSES:
        errors.append(f"invalid course_status: {status}")

    competencies: dict[str, dict] = {}
    if schema_version in {2, 3, 4}:
        for key, expected_type in {
            "learning_phase": str,
            "learner_profile": dict,
            "assessment_history": list,
            "foundation_units": list,
        }.items():
            if key not in progress:
                errors.append(f"progress.json missing {key}")
            elif not isinstance(progress[key], expected_type):
                errors.append(f"progress.json {key} must be {expected_type.__name__}")
        if progress.get("learning_phase") not in LEARNING_PHASES:
            errors.append(f"invalid learning_phase: {progress.get('learning_phase')}")
        if "current_unit" not in progress:
            errors.append("progress.json missing current_unit")
        elif progress["current_unit"] is not None and not isinstance(progress["current_unit"], dict):
            errors.append("progress.json current_unit must be object or null")
        competencies = _validate_learner_profile(progress, milestone_ids, errors, schema_version)
        history = progress.get("assessment_history")
        if status in ACTIVE_STATUSES:
            profile_value = progress.get("learner_profile")
            profile_mode = profile_value.get("assessment_mode") if isinstance(profile_value, dict) else None
            if profile_mode == "pending":
                errors.append("active schema-v2+ course requires a readiness decision")
            if schema_version in {3, 4} and isinstance(profile_value, dict) and profile_value.get("learning_mode") == "pending":
                errors.append(f"active schema-v{schema_version} course requires a learning_mode decision")
            if isinstance(history, list) and not history:
                errors.append("active schema-v2+ course requires assessment_history")
        if isinstance(history, list):
            for index, entry in enumerate(history):
                prefix = f"assessment_history[{index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{prefix} must be object")
                    continue
                if entry.get("mode") not in ASSESSMENT_MODES - {"pending"}:
                    errors.append(f"{prefix} has invalid mode: {entry.get('mode')}")
                for key in ("summary", "timestamp"):
                    if not isinstance(entry.get(key), str) or not entry[key]:
                        errors.append(f"{prefix}.{key} must be non-empty string")

    practice_unit_ids: set[str] = set()
    if schema_version in {3, 4}:
        practice = progress.get("practice_evidence")
        if not isinstance(practice, list):
            errors.append("progress.json practice_evidence must be list")
        else:
            known_units = set(foundation_ids + milestone_ids)
            for index, entry in enumerate(practice):
                prefix = f"practice_evidence[{index}]"
                if not isinstance(entry, dict):
                    errors.append(f"{prefix} must be object")
                    continue
                unit_id = entry.get("unit_id")
                if unit_id not in known_units:
                    errors.append(f"{prefix} references unknown unit: {unit_id}")
                else:
                    practice_unit_ids.add(unit_id)
                if entry.get("depth") not in PRACTICE_DEPTHS - {"unseen"}:
                    errors.append(f"{prefix} has invalid depth: {entry.get('depth')}")
                for key in ("manual_action", "observable_result", "explanation", "ai_usage", "timestamp"):
                    if not isinstance(entry.get(key), str) or not entry[key]:
                        errors.append(f"{prefix}.{key} must be non-empty string")

    records = progress.get("milestones")
    progress_ids: list[str] = []
    progress_numbers: list[int] = []
    if isinstance(records, list):
        for index, record in enumerate(records):
            if not isinstance(record, dict):
                errors.append(f"milestones[{index}] must be object")
                continue
            for key in ("id", "number", "status", "acceptance", "risk_notes"):
                if key not in record:
                    errors.append(f"milestones[{index}] missing {key}")
            if isinstance(record.get("id"), str):
                progress_ids.append(record["id"])
            else:
                errors.append(f"milestones[{index}].id must be string")
            number = record.get("number")
            if isinstance(number, int) and not isinstance(number, bool):
                progress_numbers.append(number)
            else:
                errors.append(f"milestones[{index}].number must be integer")
            if record.get("status") not in UNIT_STATUSES:
                errors.append(f"milestones[{index}] has invalid status: {record.get('status')}")
            if not isinstance(record.get("acceptance"), list):
                errors.append(f"milestones[{index}].acceptance must be list")
            if not isinstance(record.get("risk_notes"), list):
                errors.append(f"milestones[{index}].risk_notes must be list")
        if len(progress_ids) != len(set(progress_ids)):
            errors.append("progress milestone IDs must be unique")
        if len(progress_numbers) != len(set(progress_numbers)):
            errors.append("progress milestone numbers must be unique")
        if progress_numbers and progress_numbers != list(range(1, len(progress_numbers) + 1)):
            errors.append("progress milestone numbers must be consecutive from 1")
        if status in ACTIVE_STATUSES and progress_ids != milestone_ids:
            errors.append("progress milestone IDs do not match bilingual course files")
        if schema_version in {3, 4}:
            for record in records:
                if isinstance(record, dict) and record.get("status") == "passed" and record.get("id") not in practice_unit_ids:
                    errors.append(f"passed milestone requires practice evidence: {record.get('id')}")

    foundation_progress_ids: list[str] = []
    if schema_version in {2, 3, 4}:
        foundation_records = progress.get("foundation_units")
        foundation_numbers: list[int] = []
        if isinstance(foundation_records, list):
            if len(foundation_records) > 8:
                errors.append("foundation route must stay bounded to at most 8 units")
            for index, record in enumerate(foundation_records):
                prefix = f"foundation_units[{index}]"
                if not isinstance(record, dict):
                    errors.append(f"{prefix} must be object")
                    continue
                for key in (
                    "id", "number", "status", "competencies", "required_by",
                    "acceptance", "risk_notes",
                ):
                    if key not in record:
                        errors.append(f"{prefix} missing {key}")
                unit_id = record.get("id")
                if isinstance(unit_id, str):
                    foundation_progress_ids.append(unit_id)
                else:
                    errors.append(f"{prefix}.id must be string")
                number = record.get("number")
                if isinstance(number, int) and not isinstance(number, bool):
                    foundation_numbers.append(number)
                else:
                    errors.append(f"{prefix}.number must be integer")
                if record.get("status") not in UNIT_STATUSES:
                    errors.append(f"{prefix} has invalid status: {record.get('status')}")
                for key in ("competencies", "required_by", "acceptance", "risk_notes"):
                    if not isinstance(record.get(key), list):
                        errors.append(f"{prefix}.{key} must be list")
                for competency_id in record.get("competencies", []) if isinstance(record.get("competencies"), list) else []:
                    if competency_id not in competencies:
                        errors.append(f"{prefix} references unknown competency: {competency_id}")
                for milestone_id in record.get("required_by", []) if isinstance(record.get("required_by"), list) else []:
                    if milestone_ids and milestone_id not in milestone_ids:
                        errors.append(f"{prefix} references unknown milestone: {milestone_id}")
            if len(foundation_progress_ids) != len(set(foundation_progress_ids)):
                errors.append("progress foundation IDs must be unique")
            if foundation_numbers and foundation_numbers != list(range(1, len(foundation_numbers) + 1)):
                errors.append("progress foundation numbers must be consecutive from 1")
            if status in ACTIVE_STATUSES and foundation_progress_ids != foundation_ids:
                errors.append("progress foundation IDs do not match bilingual course files")
            if schema_version in {3, 4}:
                for record in foundation_records:
                    if isinstance(record, dict) and record.get("status") == "passed" and record.get("id") not in practice_unit_ids:
                        errors.append(f"passed foundation requires practice evidence: {record.get('id')}")

    current = progress.get("current_milestone")
    if schema_version == 1:
        if status in ACTIVE_STATUSES and isinstance(current, int):
            if not milestone_ids or not 1 <= current <= len(milestone_ids):
                errors.append("current_milestone out of bounds")
    elif schema_version in {2, 3, 4}:
        current_unit = progress.get("current_unit")
        if status == "complete":
            if current_unit is not None:
                errors.append("complete course requires current_unit to be null")
            if progress.get("learning_phase") != "complete":
                errors.append("complete course requires learning_phase complete")
        elif isinstance(current_unit, dict):
            kind = current_unit.get("kind")
            unit_id = current_unit.get("id")
            if kind not in {"assessment", "foundation", "milestone"}:
                errors.append(f"current_unit has invalid kind: {kind}")
            if not isinstance(unit_id, str) or not unit_id:
                errors.append("current_unit.id must be non-empty string")
            if kind == "assessment":
                if unit_id != "readiness" or current != 0:
                    errors.append("assessment current_unit requires id readiness and current_milestone 0")
                if status in ACTIVE_STATUSES:
                    errors.append("active course cannot remain on readiness assessment")
            elif kind == "foundation":
                if unit_id not in foundation_ids:
                    errors.append("current_unit references unknown foundation")
                if current != 0:
                    errors.append("foundation current_unit requires current_milestone 0")
            elif kind == "milestone":
                if unit_id not in milestone_ids:
                    errors.append("current_unit references unknown milestone")
                elif current != milestone_ids.index(unit_id) + 1:
                    errors.append("current_milestone does not match current_unit milestone")
                unresolved = [
                    competency_id
                    for competency_id, competency in competencies.items()
                    if competency.get("blocking") is True
                    and unit_id in competency.get("required_by", [])
                    and competency.get("state") not in {"ready", "waived"}
                ]
                if unresolved:
                    errors.append(
                        "current milestone has unresolved blocking competencies: "
                        + ", ".join(sorted(unresolved))
                    )
                waived = [
                    competency_id
                    for competency_id, competency in competencies.items()
                    if competency.get("blocking") is True
                    and unit_id in competency.get("required_by", [])
                    and competency.get("state") == "waived"
                ]
                matching_record = next(
                    (record for record in records or [] if isinstance(record, dict) and record.get("id") == unit_id),
                    None,
                )
                if waived and (not matching_record or not matching_record.get("risk_notes")):
                    errors.append("waived blocking competencies require milestone risk_notes")

    if schema_version == 4:
        if "current_lesson" not in progress:
            errors.append("progress.json missing current_lesson")
        current_lesson = progress.get("current_lesson")
        current_unit = progress.get("current_unit")
        if status == "complete" or (
            isinstance(current_unit, dict) and current_unit.get("kind") == "assessment"
        ):
            if current_lesson is not None:
                errors.append("assessment or complete course requires current_lesson null")
        elif isinstance(current_unit, dict):
            unit_id = current_unit.get("id")
            if not isinstance(current_lesson, dict):
                errors.append("active schema-v4 unit requires current_lesson object")
            else:
                if current_lesson.get("unit_id") != unit_id:
                    errors.append("current_lesson.unit_id must match current_unit.id")
                lesson_id = current_lesson.get("id")
                known_lessons = (unit_lessons or {}).get(unit_id, [])
                if lesson_id not in known_lessons:
                    errors.append("current_lesson references unknown lesson")

    hints = progress.get("hint_history")
    if isinstance(hints, list):
        for index, hint in enumerate(hints):
            if not isinstance(hint, dict):
                errors.append(f"hint_history[{index}] must be object")
                continue
            level = hint.get("level")
            if not isinstance(level, int) or isinstance(level, bool) or not 1 <= level <= 5:
                errors.append(f"hint_history[{index}] has invalid level")
            if schema_version == 1:
                if hint.get("milestone_id") not in milestone_ids:
                    errors.append(f"hint_history[{index}] references unknown milestone")
            else:
                if "unit_id" not in hint and hint.get("milestone_id") in milestone_ids:
                    # Preserve schema-v1 hint history during a non-destructive v2 migration.
                    pass
                else:
                    unit_kind = hint.get("unit_kind")
                    unit_id = hint.get("unit_id")
                    if unit_kind not in {"foundation", "milestone"}:
                        errors.append(f"hint_history[{index}] has invalid unit_kind")
                    known_ids = foundation_ids if unit_kind == "foundation" else milestone_ids
                    if unit_id not in known_ids:
                        errors.append(f"hint_history[{index}] references unknown unit")
            for key in ("reason", "timestamp"):
                if not isinstance(hint.get(key), str) or not hint[key]:
                    errors.append(f"hint_history[{index}].{key} must be non-empty string")

    if status == "complete" and isinstance(records, list):
        terminal = {"passed", "skipped_with_risk"}
        if any(not isinstance(record, dict) or record.get("status") not in terminal for record in records):
            errors.append("complete course has unfinished milestones")
        last_review = progress.get("last_review")
        review = reviews.get(last_review) if isinstance(last_review, str) else None
        if (
            review is None
            or not milestone_ids
            or review.get("milestone_id") != milestone_ids[-1]
            or review.get("verdict") not in terminal
        ):
            errors.append("complete course requires a final paired review")


def _validate_selected_files_legacy(workspace: Path, selected: list[str]) -> list[str]:
    """Validate one execution unit's declared outputs in isolation.

    Other fan-out agents may be publishing files concurrently, so selected-file
    validation deliberately ignores every undeclared artifact in the workspace.
    Localized Markdown outputs must still select and satisfy their language pair.
    Unknown output types (for example neutral models and milestone definitions)
    are checked for existence only.
    """
    workspace = Path(workspace).resolve()
    errors: list[str] = []
    core: dict[tuple[str, str], str] = {}
    foundations: dict[tuple[str, str], str] = {}
    milestones: dict[tuple[str, str], str] = {}
    reviews: dict[tuple[str, str], str] = {}

    for raw in unique_preserving_order(selected):
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"--only path must be workspace-relative: {raw}")
            continue
        path = workspace / relative
        if not path.is_file():
            errors.append(f"missing declared output: {relative.as_posix()}")
            continue
        parts = relative.parts
        text = path.read_text(encoding="utf-8") if path.suffix == ".md" else ""

        if len(parts) == 3 and parts[0] == "course" and parts[1] in LANGUAGES:
            language, filename = parts[1], parts[2]
            if filename in CORE_HEADINGS[language]:
                _check_headings(path, V3_CORE_HEADINGS[language][filename], errors)
                if _frontmatter(text) is None:
                    errors.append(f"{relative.as_posix()} missing opening frontmatter")
                if not _metadata(text, "artifact_id"):
                    errors.append(f"{relative.as_posix()} missing artifact_id")
                if _metadata(text, "language") != language:
                    errors.append(f"{relative.as_posix()} has incorrect language metadata")
                evidence_count = _check_evidence(relative, text, errors)
                if filename in {"project-map.md", "architecture.md", "project-evolution.md", "roadmap.md"} and evidence_count == 0:
                    errors.append(f"{relative.as_posix()} requires at least one evidence entry")
                core[(language, filename)] = text
            continue

        if len(parts) == 4 and parts[0] == "course" and parts[1] in LANGUAGES and parts[2] == "foundations":
            language, filename = parts[1], parts[3]
            _check_headings(path, V3_FOUNDATION_HEADINGS[language], errors)
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
            foundations[(language, filename)] = text
            continue

        if len(parts) == 4 and parts[0] == "course" and parts[1] in LANGUAGES and parts[2] == "milestones":
            language, filename = parts[1], parts[3]
            _check_headings(path, V3_MILESTONE_HEADINGS[language], errors)
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
            milestones[(language, filename)] = text
            continue

        if len(parts) == 3 and parts[0] == "reviews" and parts[1] in LANGUAGES:
            language, filename = parts[1], parts[2]
            _check_headings(path, REVIEW_HEADINGS[language], errors)
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            for key in ("artifact_id", "review_id", "milestone_id", "verdict"):
                if not _metadata(text, key):
                    errors.append(f"{relative.as_posix()} missing {key}")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
            reviews[(language, filename)] = text
            continue

        if relative.as_posix() == "course/GETTING_STARTED.md":
            _check_getting_started(path, errors, strict=True)

    for filename in {name for _, name in core}:
        zh = core.get(("zh-CN", filename))
        en = core.get(("en", filename))
        if zh is None or en is None:
            errors.append(f"selected core artifact is missing its declared language pair: {filename}")
            continue
        if _metadata(zh, "artifact_id") != _metadata(en, "artifact_id"):
            errors.append(f"artifact_id mismatch for {filename}")
        if _values(zh, "source") != _values(en, "source"):
            errors.append(f"source locations differ for {filename}")
        if filename == "readiness.md":
            for key, label in (
                ("competency_id", "competency IDs"),
                ("state", "competency states"),
                ("required_by", "readiness milestone links"),
                ("foundation_id", "readiness foundation IDs"),
                ("learning_mode", "learning modes"),
            ):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")
        if filename == "project-map.md":
            for key, label in (("layer_id", "technology layer IDs"), ("failure_id", "troubleshooting failure IDs")):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")
        if filename == "knowledge-graph.md":
            for key, label in (("practice_depth", "practice depths"), ("reappears_in", "spiral recurrence links")):
                if _values(zh, key) != _values(en, key):
                    errors.append(f"{label} differ for {filename}")

    for filename in {name for _, name in foundations}:
        zh = foundations.get(("zh-CN", filename))
        en = foundations.get(("en", filename))
        if zh is None or en is None:
            errors.append(f"selected foundation is missing its declared language pair: {filename}")
            continue
        number_match = re.match(r"^F(\d{2})-", filename, re.IGNORECASE)
        expected_id = f"foundation-{int(number_match.group(1)):02d}" if number_match else None
        if expected_id is None:
            errors.append(f"foundation filename lacks FNN prefix: {filename}")
        for language, text in (("zh-CN", zh), ("en", en)):
            if expected_id and _metadata(text, "artifact_id") != expected_id:
                errors.append(f"course/{language}/foundations/{filename} must use artifact_id {expected_id}")
        for key, label in (
            ("source", "source locations"),
            ("competency_id", "competency IDs"),
            ("required_by", "foundation milestone links"),
            ("acceptance_id", "acceptance IDs"),
            ("command", "commands"),
            ("practice_id", "practice IDs"),
            ("manual_action_id", "manual action IDs"),
            ("ai_boundary_id", "AI boundary IDs"),
            ("transfer_check_id", "transfer check IDs"),
            ("reappears_in", "spiral recurrence links"),
        ):
            if _values(zh, key) != _values(en, key):
                errors.append(f"{label} differ for foundation {filename}")

    for filename in {name for _, name in milestones}:
        zh = milestones.get(("zh-CN", filename))
        en = milestones.get(("en", filename))
        if zh is None or en is None:
            errors.append(f"selected milestone is missing its declared language pair: {filename}")
            continue
        number_match = re.match(r"^(\d{2})-", filename)
        expected_id = f"milestone-{int(number_match.group(1)):02d}" if number_match else None
        if expected_id is None:
            errors.append(f"milestone filename lacks numeric prefix: {filename}")
        for language, text in (("zh-CN", zh), ("en", en)):
            if expected_id and _metadata(text, "artifact_id") != expected_id:
                errors.append(f"course/{language}/milestones/{filename} must use artifact_id {expected_id}")
        if _metadata(zh, "artifact_id") != _metadata(en, "artifact_id"):
            errors.append(f"artifact_id mismatch for milestone {filename}")
        for key, label in (
            ("source", "source locations"), ("acceptance_id", "acceptance IDs"),
            ("command", "commands"), ("practice_id", "practice IDs"),
            ("manual_action_id", "manual action IDs"), ("ai_boundary_id", "AI boundary IDs"),
            ("transfer_check_id", "transfer check IDs"), ("reappears_in", "spiral recurrence links"),
        ):
            if _values(zh, key) != _values(en, key):
                errors.append(f"{label} differ for milestone {filename}")

    for filename in {name for _, name in reviews}:
        zh = reviews.get(("zh-CN", filename))
        en = reviews.get(("en", filename))
        if zh is None or en is None:
            errors.append(f"selected review is missing its declared language pair: {filename}")
            continue
        for key, label in (("artifact_id", "review artifact_id"), ("review_id", "review ID"), ("milestone_id", "review milestone ID"), ("verdict", "review verdict")):
            if _metadata(zh, key) != _metadata(en, key):
                errors.append(f"{label} differs for {filename}")
        for key, label in (("source", "review source locations"), ("acceptance_id", "review acceptance IDs"), ("command", "review commands")):
            if _values(zh, key) != _values(en, key):
                errors.append(f"{label} differ for {filename}")

    return errors


def _validate_selected_v4(workspace: Path, selected: list[str]) -> list[str]:
    workspace = Path(workspace).resolve()
    errors: list[str] = []
    nested: dict[tuple[str, str], dict[str, set[str]]] = {}
    legacy_selected: list[str] = []
    for raw in unique_preserving_order(selected):
        relative = Path(raw)
        if relative.is_absolute() or ".." in relative.parts:
            errors.append(f"--only path must be workspace-relative: {raw}")
            continue
        path = workspace / relative
        if not path.is_file():
            errors.append(f"missing declared output: {relative.as_posix()}")
            continue
        parts = relative.parts
        if (
            len(parts) == 5 and parts[0] == "course" and parts[1] in LANGUAGES
            and parts[2] in {"foundations", "milestones"} and path.suffix == ".md"
        ):
            language, plural, stem, filename = parts[1], parts[2], parts[3], parts[4]
            nested.setdefault((plural, stem), {}).setdefault(filename, set()).add(language)
        else:
            legacy_selected.append(raw)
    errors.extend(_validate_selected_files_legacy(workspace, legacy_selected))

    for (plural, stem), files in nested.items():
        kind = "foundation" if plural == "foundations" else "milestone"
        match = re.match(r"^F(\d{2})-", stem, re.IGNORECASE) if kind == "foundation" else re.match(r"^(\d{2})-", stem)
        if not match:
            errors.append(f"{kind} lesson bundle lacks numeric prefix: {stem}")
            continue
        design_path = workspace / "course" / "design" / plural / f"{stem}.json"
        if not design_path.is_file():
            errors.append(f"missing unit design: course/design/{plural}/{stem}.json")
            continue
        design, lesson_map = _check_v4_design(design_path, kind, int(match.group(1)), errors)
        if design is None:
            continue
        expected_files = set(lesson_map)
        if set(files) != expected_files:
            errors.append(f"selected {kind} bundle {stem} must declare lessons {sorted(expected_files)}")
        unit_id = design.get("unit_id")
        for filename, languages in files.items():
            if languages != set(LANGUAGES):
                errors.append(f"selected lesson is missing its language pair: {plural}/{stem}/{filename}")
                continue
            lesson = lesson_map.get(filename)
            if lesson is None:
                errors.append(f"selected lesson not declared by design: {plural}/{stem}/{filename}")
                continue
            texts = {}
            for language in LANGUAGES:
                path = workspace / "course" / language / plural / stem / filename
                texts[language] = _check_v4_lesson(path, language, unit_id, lesson, errors)
            for key in ("artifact_id", "unit_id", "lesson_id"):
                if _metadata(texts["zh-CN"], key) != _metadata(texts["en"], key):
                    errors.append(f"{key} differs for {plural}/{stem}/{filename}")
    return errors


def validate_selected_files(workspace: Path, selected: list[str]) -> list[str]:
    progress_path = Path(workspace) / "progress.json"
    try:
        schema_version = json.loads(progress_path.read_text(encoding="utf-8")).get("schema_version")
    except (OSError, json.JSONDecodeError, AttributeError):
        schema_version = None
    if schema_version == 4:
        return _validate_selected_v4(workspace, selected)
    return _validate_selected_files_legacy(workspace, selected)


def unique_preserving_order(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def validate_workspace(workspace: Path, *, partial: bool = False) -> list[str]:
    """Validate a workspace.

    ``partial`` is for fan-out execution units while the course is still being
    assembled. It validates every artifact that already exists, bilingual
    pairing, evidence, and progress structure without requiring not-yet-created
    core artifacts or the final 5-12 milestone count. Finalization must always
    run the default full validation.
    """
    workspace = Path(workspace).resolve()
    errors: list[str] = []
    progress = _load_progress(workspace, errors)
    schema_version = progress.get("schema_version") if isinstance(progress, dict) else None
    if schema_version == 4:
        return _validate_v4_workspace(workspace, progress, partial=partial)
    core_texts: dict[str, dict[str, str]] = {language: {} for language in LANGUAGES}

    if not (workspace / "student").is_dir():
        errors.append("missing student directory")
    for language in LANGUAGES:
        if not (workspace / "reviews" / language).is_dir():
            errors.append(f"missing reviews/{language} directory")

    for language in LANGUAGES:
        course_root = workspace / "course" / language
        for filename, headings in CORE_HEADINGS[language].items():
            if filename in {"readiness.md", "project-evolution.md"} and schema_version == 1:
                continue
            path = course_root / filename
            relative = path.relative_to(workspace).as_posix()
            if not path.is_file():
                if not partial:
                    errors.append(f"missing {relative}")
                continue
            text = _check_headings(path, _core_headings(language, filename, schema_version), errors)
            core_texts[language][filename] = text
            if _frontmatter(text) is None:
                errors.append(f"{relative} missing opening frontmatter")
            if not _metadata(text, "artifact_id"):
                errors.append(f"{relative} missing artifact_id")
            if _metadata(text, "language") != language:
                errors.append(f"{relative} has incorrect language metadata")
            evidence_count = _check_evidence(path.relative_to(workspace), text, errors)
            if filename in {"project-map.md", "architecture.md", "project-evolution.md", "roadmap.md"} and evidence_count == 0:
                errors.append(f"{relative} requires at least one evidence entry")

    for filename in CORE_HEADINGS["en"]:
        zh_text = core_texts["zh-CN"].get(filename)
        en_text = core_texts["en"].get(filename)
        if zh_text is None or en_text is None:
            if partial and (zh_text is None) != (en_text is None):
                errors.append(f"unpaired partial core artifact: {filename}")
            continue
        zh_id = _metadata(zh_text, "artifact_id")
        en_id = _metadata(en_text, "artifact_id")
        if zh_id != en_id:
            errors.append(f"artifact_id mismatch for {filename}: {zh_id} != {en_id}")
        if _values(zh_text, "source") != _values(en_text, "source"):
            errors.append(f"source locations differ for {filename}")
        if filename == "readiness.md":
            for key, label in (
                ("competency_id", "competency IDs"),
                ("state", "competency states"),
                ("required_by", "readiness milestone links"),
                ("foundation_id", "readiness foundation IDs"),
                ("learning_mode", "learning modes"),
            ):
                if _values(zh_text, key) != _values(en_text, key):
                    errors.append(f"{label} differ for {filename}")
        if schema_version == 3 and filename == "project-map.md":
            for key, label in (("layer_id", "technology layer IDs"), ("failure_id", "troubleshooting failure IDs")):
                if _values(zh_text, key) != _values(en_text, key):
                    errors.append(f"{label} differ for {filename}")
        if schema_version == 3 and filename == "knowledge-graph.md":
            for key, label in (("practice_depth", "practice depths"), ("reappears_in", "spiral recurrence links")):
                if _values(zh_text, key) != _values(en_text, key):
                    errors.append(f"{label} differ for {filename}")

    foundation_paths = {
        language: sorted((workspace / "course" / language / "foundations").glob("*.md"))
        for language in LANGUAGES
    }
    foundation_names = {
        language: {path.name for path in paths} for language, paths in foundation_paths.items()
    }
    if foundation_names["zh-CN"] != foundation_names["en"]:
        errors.append("foundation file sets differ between zh-CN and en")
    if schema_version in {2, 3} and len(foundation_paths["zh-CN"]) > 8:
        errors.append("foundation route must stay bounded to at most 8 units")

    foundation_ids: list[str] = []
    foundation_file_numbers: list[int] = []
    for filename in sorted(foundation_names["zh-CN"] & foundation_names["en"]):
        texts = {}
        for language in LANGUAGES:
            path = workspace / "course" / language / "foundations" / filename
            relative = path.relative_to(workspace)
            text = _check_headings(path, _foundation_headings(language, schema_version), errors)
            texts[language] = text
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
        number_match = re.match(r"^F(\d{2})-", filename, re.IGNORECASE)
        expected_id = f"foundation-{int(number_match.group(1)):02d}" if number_match else None
        if expected_id is None:
            errors.append(f"foundation filename lacks FNN prefix: {filename}")
        else:
            foundation_file_numbers.append(int(number_match.group(1)))
            for language in LANGUAGES:
                if _metadata(texts[language], "artifact_id") != expected_id:
                    errors.append(
                        f"course/{language}/foundations/{filename} must use artifact_id {expected_id}"
                    )
        zh_id = _metadata(texts["zh-CN"], "artifact_id")
        en_id = _metadata(texts["en"], "artifact_id")
        if zh_id and zh_id == en_id:
            foundation_ids.append(zh_id)
        if zh_id != en_id:
            errors.append(f"artifact_id mismatch for foundation {filename}: {zh_id} != {en_id}")
        for key, label in (
            ("source", "source locations"),
            ("competency_id", "competency IDs"),
            ("required_by", "foundation milestone links"),
            ("acceptance_id", "acceptance IDs"),
            ("command", "commands"),
            ("practice_id", "practice IDs"),
            ("manual_action_id", "manual action IDs"),
            ("ai_boundary_id", "AI boundary IDs"),
            ("transfer_check_id", "transfer check IDs"),
            ("reappears_in", "spiral recurrence links"),
        ):
            if _values(texts["zh-CN"], key) != _values(texts["en"], key):
                errors.append(f"{label} differ for foundation {filename}")
    if sorted(foundation_file_numbers) != list(range(1, len(foundation_file_numbers) + 1)):
        errors.append("foundation filename numbers must be consecutive from 1")

    milestone_paths = {
        language: sorted((workspace / "course" / language / "milestones").glob("*.md"))
        for language in LANGUAGES
    }
    milestone_names = {
        language: {path.name for path in paths} for language, paths in milestone_paths.items()
    }
    if milestone_names["zh-CN"] != milestone_names["en"]:
        errors.append("milestone file sets differ between zh-CN and en")

    status = progress.get("course_status") if progress else None
    guide = workspace / "course" / "GETTING_STARTED.md"
    if status in {"ready", "complete", "in_progress"}:
        if not guide.is_file():
            errors.append("missing course/GETTING_STARTED.md learning-order guide")
        else:
            _check_getting_started(guide, errors, strict=schema_version == 3)
    count = len(milestone_paths["zh-CN"])
    if not partial and (status in ACTIVE_STATUSES or count > 0) and not 5 <= count <= 12:
        errors.append(f"course requires 5-12 milestone pairs, found {count}")

    milestone_ids: list[str] = []
    milestone_file_numbers: list[int] = []
    for filename in sorted(milestone_names["zh-CN"] & milestone_names["en"]):
        texts = {}
        for language in LANGUAGES:
            path = workspace / "course" / language / "milestones" / filename
            relative = path.relative_to(workspace)
            text = _check_milestone_headings(path, language, schema_version, errors)
            texts[language] = text
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            if not _metadata(text, "artifact_id"):
                errors.append(f"{relative.as_posix()} missing artifact_id")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
        zh_id = _metadata(texts["zh-CN"], "artifact_id")
        en_id = _metadata(texts["en"], "artifact_id")
        number_match = re.match(r"^(\d{2})-", filename)
        expected_id = f"milestone-{int(number_match.group(1)):02d}" if number_match else None
        if expected_id is None:
            errors.append(f"milestone filename lacks numeric prefix: {filename}")
        else:
            milestone_file_numbers.append(int(number_match.group(1)))
            for language in LANGUAGES:
                if _metadata(texts[language], "artifact_id") != expected_id:
                    errors.append(
                        f"course/{language}/milestones/{filename} must use artifact_id {expected_id}"
                    )
        if zh_id and en_id and zh_id == en_id:
            milestone_ids.append(zh_id)
        if zh_id != en_id:
            errors.append(
                f"artifact_id mismatch for milestone {filename}: "
                f"{zh_id} != {en_id}"
            )
        if _values(texts["zh-CN"], "source") != _values(texts["en"], "source"):
            errors.append(f"source locations differ for milestone {filename}")
        if _values(texts["zh-CN"], "acceptance_id") != _values(texts["en"], "acceptance_id"):
            errors.append(f"acceptance IDs differ for milestone {filename}")
        if _values(texts["zh-CN"], "command") != _values(texts["en"], "command"):
            errors.append(f"commands differ for milestone {filename}")
        if _values(texts["zh-CN"], "competency_id") != _values(texts["en"], "competency_id"):
            errors.append(f"competency IDs differ for milestone {filename}")
        if _values(texts["zh-CN"], "foundation_id") != _values(texts["en"], "foundation_id"):
            errors.append(f"foundation IDs differ for milestone {filename}")
        for key, label in (
            ("practice_id", "practice IDs"), ("manual_action_id", "manual action IDs"),
            ("ai_boundary_id", "AI boundary IDs"), ("transfer_check_id", "transfer check IDs"),
            ("reappears_in", "spiral recurrence links"),
        ):
            if _values(texts["zh-CN"], key) != _values(texts["en"], key):
                errors.append(f"{label} differ for milestone {filename}")
    if sorted(milestone_file_numbers) != list(range(1, len(milestone_file_numbers) + 1)):
        errors.append("milestone filename numbers must be consecutive from 1")

    review_paths = {
        language: sorted((workspace / "reviews" / language).glob("*.md"))
        for language in LANGUAGES
    }
    review_names = {language: {path.name for path in paths} for language, paths in review_paths.items()}
    if review_names["zh-CN"] != review_names["en"]:
        errors.append("review file sets differ between zh-CN and en")
    reviews_by_id: dict[str, dict[str, str]] = {}
    for filename in sorted(review_names["zh-CN"] & review_names["en"]):
        texts = {}
        for language in LANGUAGES:
            path = workspace / "reviews" / language / filename
            relative = path.relative_to(workspace)
            text = _check_headings(path, REVIEW_HEADINGS[language], errors)
            texts[language] = text
            if _frontmatter(text) is None:
                errors.append(f"{relative.as_posix()} missing opening frontmatter")
            if not _metadata(text, "artifact_id"):
                errors.append(f"{relative.as_posix()} missing artifact_id")
            for key in ("review_id", "milestone_id", "verdict"):
                if not _metadata(text, key):
                    errors.append(f"{relative.as_posix()} missing {key}")
            if _metadata(text, "language") != language:
                errors.append(f"{relative.as_posix()} has incorrect language metadata")
            if _check_evidence(relative, text, errors) == 0:
                errors.append(f"{relative.as_posix()} requires at least one evidence entry")
        for key, label in (
            ("artifact_id", "review artifact_id"),
            ("review_id", "review ID"),
            ("milestone_id", "review milestone ID"),
            ("verdict", "review verdict"),
        ):
            if _metadata(texts["zh-CN"], key) != _metadata(texts["en"], key):
                errors.append(f"{label} differs for {filename}")
        for key, label in (
            ("source", "review source locations"),
            ("acceptance_id", "review acceptance IDs"),
            ("command", "review commands"),
        ):
            if _values(texts["zh-CN"], key) != _values(texts["en"], key):
                errors.append(f"{label} differ for {filename}")

        review_id = _metadata(texts["zh-CN"], "review_id")
        milestone_id = _metadata(texts["zh-CN"], "milestone_id")
        verdict = _metadata(texts["zh-CN"], "verdict")
        if verdict and verdict not in {"passed", "needs_revision", "skipped_with_risk"}:
            errors.append(f"invalid review verdict for {filename}: {verdict}")
        if milestone_id and milestone_id not in milestone_ids:
            errors.append(f"review references unknown milestone for {filename}: {milestone_id}")
        if review_id and milestone_id and verdict:
            if review_id in reviews_by_id:
                errors.append(f"duplicate review_id: {review_id}")
            else:
                reviews_by_id[review_id] = {
                    "milestone_id": milestone_id,
                    "verdict": verdict,
                }

    if schema_version in {2, 3} and isinstance(progress, dict):
        readiness = core_texts["zh-CN"].get("readiness.md")
        profile = progress.get("learner_profile")
        if readiness is not None and isinstance(profile, dict):
            if schema_version == 3:
                expected_mode = profile.get("learning_mode")
                if _values(readiness, "learning_mode") != [expected_mode]:
                    errors.append("readiness learning_mode does not match progress learner profile")
            competency_records = profile.get("competencies")
            if isinstance(competency_records, list):
                expected_ids = sorted(
                    record.get("id") for record in competency_records
                    if isinstance(record, dict) and isinstance(record.get("id"), str)
                )
                expected_states = sorted(
                    record.get("state") for record in competency_records
                    if isinstance(record, dict) and isinstance(record.get("state"), str)
                )
                if _values(readiness, "competency_id") != expected_ids:
                    errors.append("readiness competency IDs do not match progress learner profile")
                if _values(readiness, "state") != expected_states:
                    errors.append("readiness competency states do not match progress learner profile")
            foundation_records = progress.get("foundation_units")
            if isinstance(foundation_records, list):
                expected_foundations = sorted(
                    record.get("id") for record in foundation_records
                    if isinstance(record, dict) and isinstance(record.get("id"), str)
                )
                if _values(readiness, "foundation_id") != expected_foundations:
                    errors.append("readiness foundation IDs do not match progress foundation units")

    _validate_progress(progress, foundation_ids, milestone_ids, reviews_by_id, errors)
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a bilingual Project2Learn workspace.")
    parser.add_argument("workspace", type=Path)
    parser.add_argument(
        "--partial",
        action="store_true",
        help="validate existing artifacts during fan-out assembly; finalization must omit this flag",
    )
    parser.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="RELATIVE_PATH",
        help="validate only one fan-out unit's declared output; repeat for paired files",
    )
    args = parser.parse_args(argv)
    errors = (
        validate_selected_files(args.workspace, args.only)
        if args.only
        else validate_workspace(args.workspace, partial=args.partial)
    )
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("VALID")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
