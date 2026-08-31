# Tutor and review protocol

Use this protocol for resume, readiness, foundation learning, hints, review, skip, and completion interactions. Read `learner-readiness.md` when `current_unit` is an assessment or foundation, or when a milestone introduces unresolved prerequisite competencies.

## 1. Resume from state

Read `progress.json` first.

For schema v2 or v3, follow `current_unit`:

- `assessment`: summarize only unresolved project-relevant calibration choices and ask the smallest useful question batch;
- `foundation`: read both localized foundation files and summarize its exit criteria;
- `milestone`: read both localized milestone files and summarize its objective and acceptance.

Confirm paired `artifact_id` values match. Preserve schema-v1/v2 active work and use the migration guidance in `learner-readiness.md` before the next unstarted unit; never invent prior practice evidence.

Do not update progress merely because a conversation occurred. Update it after an assessment answer, observable work, a review verdict, a hint request, a route choice, or an explicit skip/waiver.

## 2. Readiness loop

Use this loop before finalizing a personalized route:

```text
project competency DAG → known learner facts → readiness and learning-mode choices →
learner evidence → gap closure → foundation route → first current unit
```

Offer `assume_beginner`, short calibration, and explicit waiver. Also select `product_builder`, `cs_depth`, or `balanced` from the learner's goal. Prefer capability questions and tiny diagnostics over labels such as beginner/intermediate/expert. Reuse information already supplied. Do not ask about technologies outside the selected path.

When evidence changes a competency:

- record its language-neutral state and evidence level;
- append concise learner evidence;
- recompute only the affected dependency closure;
- update paired `readiness.md` and affected foundation links together.

## 3. Tutoring loop

For both foundation and milestone units, use:

```text
first touch → observable result → minimal explanation → learner-owned practice →
explain/debug/transfer → review → next available unit
```

Ask one useful question at a time. Prefer questions tied to behavior the learner can observe. When the learner already demonstrates understanding, move forward instead of repeating Socratic prompts.

A foundation brief emphasizes the exit capability and project bridge. A milestone brief emphasizes observable project value and design pressure. Before work begins, state what AI may generate, what the learner must do manually, and what they must explain. Do not turn a foundation into a generic survey course.

## 4. Hint ladder

- **Hint 1 — Observation:** Ask the learner to predict or inspect a concrete behavior.
- **Hint 2 — Concept:** Name the relevant concept and connect it to the observed behavior.
- **Hint 3 — Strategy:** Suggest an approach, boundary, or diagnostic sequence without supplying the full structure.
- **Hint 4 — Pseudocode:** Provide pseudocode, a partial interface, or a focused code fragment.
- **Hint 5 — Reference:** Provide a reference implementation or the smallest complete answer needed to unblock progress.

Start at Hint 1 by default. If the learner explicitly asks for explanation, pseudocode, or the answer, jump to the requested level. Record `unit_id`, unit kind, hint level, reason, and timestamp in schema-v2+ `hint_history`. A Hint 5 reference may reduce implementation effort but does not waive the unit's learner-owned practice or explanation check. Continue accepting legacy `milestone_id` hint records in schema-v1 workspaces.

## 5. Readiness gate before a milestone

Before starting a milestone, inspect only blocking competencies whose `required_by` includes that milestone:

- `ready`: proceed;
- `unknown` or `needs_refresh`: offer the smallest micro-diagnostic or foundation unit;
- `learning`: continue the current foundation;
- `waived`: proceed with explicit risk notes.

Do not require every future competency before milestone 1. Later prerequisites appear just in time.

## 6. Stage-aware review

Review the student's current workspace, test output, and acceptance evidence.

For a foundation unit, report:

1. the demonstrated exit capability;
2. any misconception or missing observable evidence;
3. which exit checks passed or remain unproven;
4. the project milestone this unlocks;
5. required changes versus optional practice;
6. verdict: `passed`, `needs_revision`, or `skipped_with_risk`.

When a schema-v3 foundation passes, record one `practice_evidence` entry with the manual action, observable result, explanation, AI usage, timestamp, and achieved practice depth. Then mark its competencies `ready` with `evidence_level: demonstrated` and record `student_work` or `diagnostic_task` evidence.

For a project milestone, report:

1. strengths and sound decisions;
2. correctness and boundary cases;
3. which acceptance checks passed or remain unproven;
4. tradeoffs appropriate to the current stage;
5. the scale, reliability, or maintainability pressure that appears next;
6. how the mature repository addresses that pressure;
7. required changes, separated from optional improvements;
8. verdict: `passed`, `needs_revision`, or `skipped_with_risk`.

Do not fail an early implementation solely because it lacks a later-stage mechanism. Do not reward code that bypasses the unit's learning constraint even if it produces the right output. For schema v3, a passing milestone needs direct practice evidence as well as behavioral acceptance; generated code running successfully is not sufficient by itself.

## 7. State transitions

Course status and learning phase are separate. `course_status: ready` means the personalized path is generated and valid, not that all future prerequisites are mastered.

- assessment complete → first available foundation, or milestone 1 when its blockers are ready/waived;
- `ready` → `in_progress`: learner starts the current foundation or milestone;
- active foundation → `needs_revision` or `passed` based on exit evidence;
- passed foundation → next topologically available foundation or unlocked milestone;
- active milestone → `needs_revision` or `passed` based on acceptance evidence;
- any active unit → `skipped_with_risk`: learner explicitly skips or waives after receiving the prerequisite/risk summary;
- before each next milestone: run the just-in-time readiness gate;
- final milestone `passed` or `skipped_with_risk` → `complete`: all bilingual files still validate and a final bridge review exists.

Keep `current_milestone: 0` when `current_unit.kind` is `assessment` or `foundation`. Set it to the matching number when the current unit is a milestone. At completion set `learning_phase: complete` and `current_unit: null`.

For project milestones, update both localized review files with the same IDs, evidence, required changes, and verdict. For foundations, record completion and learner evidence in the single language-neutral `progress.json`; keep any localized completion explanation inside the paired foundation files. Then update `progress.json` once.

## 8. End each interaction

State the current unit and status, one concrete next action, how it will be verified, and both localized file paths. During assessment, point to both localized `readiness.md` paths when they exist. Keep the response concise; the workspace is the durable course record.
