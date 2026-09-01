# Output contract

## Workspace tree

```text
<learning-root>/<repository>/
├── course/
│   ├── GETTING_STARTED.md
│   ├── design/                         # dense, language-neutral curriculum layer
│   │   ├── foundations/FNN-slug.json
│   │   └── milestones/NN-slug.json
│   ├── zh-CN/
│   │   ├── project-map.md              # optional learner reference
│   │   ├── architecture.md             # optional learner reference
│   │   ├── knowledge-graph.md           # optional learner reference
│   │   ├── readiness.md
│   │   ├── project-evolution.md         # optional learner reference
│   │   ├── roadmap.md                   # optional learner reference
│   │   ├── foundations/FNN-slug/01.md
│   │   └── milestones/NN-slug/{01,02,...}.md
│   └── en/                              # identical bundle names and lesson order
├── student/
├── reviews/
│   ├── zh-CN/
│   └── en/
└── progress.json
```

New workspaces use schema v4. `readiness.md` remains required. Foundation bundles may be absent when the learner is ready for every currently blocking prerequisite. A foundation has 1–3 learner lessons and does not count toward the required 5–12 project milestones; a milestone has 2–5 learner lessons. Existing schema-v1/v2/v3 workspaces keep their original single-file unit layout.

## Getting-started guide (mandatory)

`course/GETTING_STARTED.md` is the single entry point for first-time users. A schema-v4 course MUST render it before becoming `ready`, with frontmatter `artifact_id: getting-started` and `language: bilingual`. Required headings are `学习指南 / Learning Guide`, `课程是什么 / What This Course Is`, `文件总览与阅读顺序 / File Overview and Reading Order`, `各文件的用途速查 / Quick File Reference`, `使用规则 / Usage Rules`, and `现在就开始 / Start Now`.

Content requirements:

- an explicit numbered reading order that starts with `readiness.md` and the actual `current_lesson`, then sends the learner directly into its first small action;
- a quick-reference table that marks `project-map.md`, `project-evolution.md`, `knowledge-graph.md`, `architecture.md`, `roadmap.md`, and `course/design/` as optional reference or designer material rather than prerequisite textbook chapters;
- how to answer readiness questions, choose `assume_beginner`, select `product_builder`, `cs_depth`, or `balanced`, waive with risk, start a unit, request hints, submit review, and check progress;
- how to record direct practice and AI usage without treating an AI-generated successful run as mastery;
- the learner's concrete first action based on `current_unit` and `current_lesson`, not an unconditional milestone-01 link;
- a clear statement that later foundations are introduced just in time rather than front-loaded.

## Artifact metadata

Every localized Markdown artifact starts with:

```yaml
---
artifact_id: stable-language-neutral-id
language: zh-CN
---
```

The paired English file uses the same `artifact_id` and `language: en`. Paired filenames must match.

Review artifacts also include these language-neutral metadata keys in their frontmatter:

```yaml
review_id: review-NN-RR
milestone_id: milestone-NN
verdict: passed|needs_revision|skipped_with_risk
```

Foundation completion evidence is stored in schema-v2+ learner evidence and foundation status records. Schema v3+ additionally requires direct `practice_evidence` for passed units. The paired review artifact contract below remains specific to project milestones.

## Required course headings

| Artifact | `zh-CN` headings | `en` headings |
|---|---|---|
| `project-map.md` | 项目地图；项目目的；核心用户路径；子系统；技术层级地图；故障定位地图；证据台账；未覆盖范围 | Project Map; Purpose; Core User Journey; Subsystems; Technology Layer Map; Troubleshooting Map; Evidence Ledger; Uncovered Scope |
| `architecture.md` | 架构；系统上下文；组件；数据流；控制流；关键决策；证据台账 | Architecture; System Context; Components; Data Flow; Control Flow; Key Decisions; Evidence Ledger |
| `knowledge-graph.md` | 知识图谱；概念依赖；学习优先级；源码位置；最小练习；螺旋复现与理解深度 | Knowledge Graph; Concept Dependencies; Learning Priority; Source Locations; Minimal Exercises; Spiral Recurrence and Understanding Depth |
| `readiness.md` | 学习准备；项目所需能力；学习者基线；差距与决策；学习模式与 AI 边界；前置补给路线；进入项目的条件 | Learning Readiness; Project-Required Competencies; Learner Baseline; Gaps and Decisions; Learning Mode and AI Boundary; Foundation Route; Entry Conditions |
| `project-evolution.md` | 项目演变；最终问题与成熟能力；最小可用起点；演变总览；阶段因果链；最终架构如何形成；教学路线声明；证据台账 | Project Evolution; Final Problem and Mature Capabilities; Minimum Viable Starting Point; Evolution Overview; Stage Causal Chain; How the Final Architecture Emerges; Teaching-Route Disclaimer; Evidence Ledger |
| `roadmap.md` | 重构路线；路线原则；里程碑总览；覆盖范围；教学性推断 | Reconstruction Roadmap; Roadmap Principles; Milestone Overview; Coverage; Teaching Inferences |

Use one `#` for the first heading and `##` for the remaining headings. In schema v3+ pair project-map entries with stable `layer_id` and `failure_id` lines; readiness uses the same `learning_mode`; knowledge-graph recurrence uses matching `practice_depth` and `reappears_in` lines.

## Schema-v4 design layer and lesson bundles

Read `learning-experience-renderer.md` before rendering learner lessons. Every unit has one dense language-neutral JSON file under `course/design/`; repository evidence, competencies, causal fields, exact AI responsibility, acceptance, hints, deferred concepts, and source bridges belong there rather than in learner prose.

A design file contains `schema_version: 1`, `artifact_id`, `unit_id`, `kind`, `number`, `slug`, competencies, prerequisite-foundation links, `practice_design`, acceptance, exactly five ordered hints, source bridges, typed evidence, and lesson definitions. A foundation uses `why_now`; a milestone uses `causal_stage` with `current_version`, `previous_value`, `new_problem`, `introduced_change`, `resolved_pressure`, `deferred_limit`, and `next_pressure`.

Each lesson definition has one stable `id`, `artifact_id`, and `cognitive_goal`, plus `situation`, `friction`, `action`, `observable_result`, `concept_name`, `minimum_theory`, `project_delta`, `next_problem`, and optional `deferred`. A non-null deferral contains `concept`, `why_not_now`, and `revisit_when`.

Localized lessons use matching filenames (`01.md`, `02.md`, ...), order, unit/lesson IDs, commands, observable outcomes, and acceptance meaning. They start with frontmatter:

```yaml
---
artifact_id: milestone-01-lesson-01
language: zh-CN
unit_id: milestone-01
lesson_id: lesson-01
---
```

Required Chinese lesson headings are `先试一下`, `你看到了什么`, `只讲现在需要的`, `把它用回项目`, `停一下，自己做`, `现在你的项目可以`, and `下一步会遇到什么`. English uses `Try This First`, `What Did You Notice?`, `Only What You Need Now`, `Put It Back Into the Project`, `Stop and Do It Yourself`, `What Your Project Can Do Now`, and `The Next Problem`.

A lesson may contain at most one optional `现在先不讲 / Not Now` section. Do not expose design-layer headings such as current version, new problem, evidence ledger, or AI usage boundary. Express AI guidance naturally beside the learner-owned action. End with project growth and the next natural problem, not a knowledge checklist.

## Legacy schema-v1-v3 foundation headings

Chinese: `前置补给单元`, `为什么现在需要`, `依赖`, `最小概念`, `小例子`, `首次触摸`, `动手练习`, `AI 使用边界`, `理解与迁移检查`, `通过标准`, `项目桥接`, `暂不学习`, `完成结论`.

English: `Foundation Unit`, `Why It Is Needed Now`, `Dependencies`, `Minimal Concepts`, `Small Example`, `First Touch`, `Hands-on Exercise`, `AI Usage Boundary`, `Understanding and Transfer Check`, `Exit Criteria`, `Project Bridge`, `Not Learning Yet`, `Completion Decision`.

Use matching IDs such as `foundation-01`, filenames such as `F01-java-minimum.md`, competency lines such as `competency_id: language.java.classes`, affected milestone lines such as `required_by: milestone-01`, and acceptance IDs such as `f01-a01`. Schema-v3 practice uses stable `practice_id`, `manual_action_id`, `ai_boundary_id`, `transfer_check_id`, and optional `reappears_in` lines. Commands, IDs, and technical tokens remain identical across languages.

Every foundation must explain what the learner does **not** need to study yet. `First Touch` gives a minimal scene, action, and immediate result before full explanation. The AI boundary distinguishes generated scaffolding from manual critical practice and required explanation. The transfer check changes at least one detail. Exit criteria must be observable and normally completable without copying the mature implementation.

## Project-evolution artifact

Create it from the language-neutral evolution model, not by expanding one localized roadmap. Each stage in `阶段因果链` / `Stage Causal Chain` must state the current version, previous value, new problem, introduced change, resolved pressure, deferred limit, and next pressure. Milestone IDs and source locations must match the roadmap, unit design JSON, and lesson bundles. The final section must explicitly say that the route is a teaching reconstruction and is not verified author chronology unless repository history directly supports a narrower claim.

## Legacy schema-v1-v3 milestone headings

Chinese: `里程碑`, `当前版本`, `上一版本解决了什么`, `用户遇到的新问题`, `本阶段引入什么`, `目标`, `可观察结果`, `本阶段解决什么`, `范围`, `暂时不解决什么`, `前置知识`, `首次触摸`, `任务`, `AI 使用边界`, `理解与迁移检查`, `验收`, `提示 1` through `提示 5`, `下一阶段为什么会出现`, `源码桥接`, `证据台账`, `完成结论`.

English: `Milestone`, `Current Version`, `What the Previous Version Solved`, `New User Problem`, `What This Stage Introduces`, `Goal`, `Observable Result`, `What This Stage Solves`, `Scope`, `Not Solving Yet`, `Prerequisites`, `First Touch`, `Tasks`, `AI Usage Boundary`, `Understanding and Transfer Check`, `Acceptance`, `Hint 1` through `Hint 5`, `Why the Next Stage Appears`, `Source Bridge`, `Evidence Ledger`, `Completion Decision`.

Milestone 1 compares against the minimum viable starting point from `project-evolution.md`; later milestones compare against the preceding milestone's accepted observable result. Keep causal sections concrete and short rather than repeating the task list.

Use matching milestone IDs such as `milestone-01`, filenames such as `01-minimal-value.md`, competency lines such as `competency_id: domain.http.request-response`, optional foundation links such as `foundation_id: foundation-02`, acceptance IDs such as `m01-a01`, and matching schema-v3 `practice_id`, `manual_action_id`, `ai_boundary_id`, `transfer_check_id`, and `reappears_in` lines.

## Review headings

Chinese: `阶段评审`, `优点`, `正确性`, `验收证据`, `当前阶段权衡`, `下一项规模压力`, `参考项目对比`, `必须修改`, `可选改进`, `结论`.

English: `Stage Review`, `Strengths`, `Correctness`, `Acceptance Evidence`, `Current-Stage Tradeoffs`, `Next Scale Pressure`, `Reference Comparison`, `Required Changes`, `Optional Improvements`, `Verdict`.

Review pairs use the same `artifact_id`, review ID, unit or milestone ID, evidence, and verdict.

## Evidence entries

Use exact machine-readable keys for repository claims:

```text
evidence: code_evidence|document_evidence|teaching_inference
source: repository/relative/path::symbol-or-section
confidence: low|medium|high
rationale: concise explanation
```

`confidence` is required for `teaching_inference` and optional for other repository evidence types. `rationale` and `source` are always required.

Learner mastery evidence belongs in `progress.json`, not this ledger. Its types are `learner_statement`, `diagnostic_task`, `student_work`, or `explicit_waiver`.

## Progress state: schema v4

New workspaces use UTF-8 schema-v4 JSON with English, language-neutral keys:

```json
{
  "schema_version": 4,
  "repository": {"name": "", "source": "", "revision": ""},
  "course_status": "analyzing",
  "learning_phase": "assessing",
  "current_unit": {"kind": "assessment", "id": "readiness"},
  "current_lesson": null,
  "current_milestone": 0,
  "learner_profile": {
    "assessment_mode": "pending",
    "learning_mode": "pending",
    "goals": [],
    "constraints": [],
    "competencies": []
  },
  "assessment_history": [],
  "practice_evidence": [],
  "foundation_units": [],
  "milestones": [],
  "hint_history": [],
  "open_improvements": [],
  "learner_choices": [],
  "last_review": null,
  "recommended_next_action": "analyze_repository_then_assess_prerequisites"
}
```

Allowed `course_status` values are `analyzing`, `ready`, `in_progress`, and `complete`. Unit status values are `ready`, `in_progress`, `needs_revision`, `passed`, and `skipped_with_risk`. Allowed `learning_phase` values are `assessing`, `foundations`, `milestones`, and `complete`.

Allowed `current_unit.kind` values are `assessment`, `foundation`, and `milestone`. `current_unit` is null only after completion. Keep `current_milestone: 0` while assessment or a foundation is current; set it to the active project milestone number when `current_unit.kind` is `milestone`.

Allowed learner `assessment_mode` values are `pending`, `assume_beginner`, `self_report`, `micro_diagnostic`, `mixed`, and `waived`. Allowed `learning_mode` values are `pending`, `product_builder`, `cs_depth`, and `balanced`. An active schema-v4 course cannot keep either decision pending.

Each competency record contains:

```json
{
  "id": "language.java.classes",
  "category": "language",
  "state": "unknown",
  "evidence_level": "none",
  "practice_depth": "unseen",
  "prerequisites": [],
  "required_by": ["milestone-01"],
  "blocking": true,
  "evidence": []
}
```

Allowed competency states are `unknown`, `ready`, `needs_refresh`, `learning`, and `waived`. Practice depth progresses through `unseen`, `touched`, `explained`, `debugged`, and `transferred`; do not advance it merely because AI generated working code. Allowed evidence levels are `none`, `self_reported`, `demonstrated`, and `waived`.

Each schema-v3+ `practice_evidence` record contains `unit_id`, `depth`, `manual_action`, `observable_result`, `explanation`, `ai_usage`, and `timestamp`. A passed foundation or milestone requires one matching record. The record documents responsibility and understanding; it is not a percentage of learner-written code.

Each learner evidence record contains `type`, `summary`, and `timestamp`. Each assessment-history record contains `mode`, `summary`, and `timestamp`. Foundation records contain `id`, `number`, `status`, `competencies`, `required_by`, `acceptance`, and `risk_notes`; milestone records contain `id`, `number`, `status`, `acceptance`, and `risk_notes`.

A milestone may be current only when every blocking competency whose `required_by` includes it is `ready` or explicitly `waived`. Waived blockers require risk notes.

`current_lesson` is null during assessment and after completion. While a foundation or milestone is active, it contains the matching `unit_id` and a lesson ID declared by that unit's design JSON. Advance it only after the learner completes the current lesson's observable action; completing chat alone does not advance it.

## Schema-v1/v2/v3 compatibility

The validator continues to accept existing schema-v1, schema-v2, and schema-v3 workspaces. Do not silently reset or restructure them. Keep old single-file units readable. Before the next not-yet-started unit, add only the missing learning-mode/practice fields needed by that workspace; migrate to lesson bundles only when the learner requests regeneration or a scope/revision change. Preserve milestone status, hints, reviews, learner choices, revision history, and existing evidence.

## Bilingual parity

Both language trees must contain the same core files, foundation/milestone bundle names, lesson filenames, and lesson order. Paired lessons share stable artifact/unit/lesson IDs and the observable meaning declared by the single language-neutral design JSON. Design JSON is the authority for repository sources, commands, competencies, readiness links, acceptance IDs, stage order, AI boundaries, learner-owned practice, transfer checks, and causal meaning. Natural-language lessons should read idiomatically in each language rather than as line-by-line translations; code identifiers and technical tokens remain unchanged.

Run `scripts/validate_course.py` before setting a course to `ready` or `complete`.
