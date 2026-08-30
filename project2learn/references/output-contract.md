# Output contract

## Workspace tree

```text
<learning-root>/<repository>/
├── course/
│   ├── GETTING_STARTED.md
│   ├── zh-CN/
│   │   ├── project-map.md
│   │   ├── architecture.md
│   │   ├── knowledge-graph.md
│   │   ├── readiness.md
│   │   ├── project-evolution.md
│   │   ├── roadmap.md
│   │   ├── foundations/FNN-slug.md
│   │   └── milestones/NN-slug.md
│   └── en/
│       ├── project-map.md
│       ├── architecture.md
│       ├── knowledge-graph.md
│       ├── readiness.md
│       ├── project-evolution.md
│       ├── roadmap.md
│       ├── foundations/FNN-slug.md
│       └── milestones/NN-slug.md
├── student/
├── reviews/
│   ├── zh-CN/
│   └── en/
└── progress.json
```

`readiness.md` is required for new schema-v2 courses. Foundation directories may be empty when the learner is ready for every currently blocking prerequisite. Foundation units are personalized bridges and do not count toward the required 5–12 project milestones.

## Getting-started guide (mandatory)

`course/GETTING_STARTED.md` is the single entry point for first-time users. It MUST be rendered before the course is marked `ready`, with frontmatter `artifact_id: getting-started` and `language: zh-CN` (or a clearly marked bilingual file). Required headings: Chinese — `学习指南`; `课程是什么`; `文件总览与阅读顺序`; `各文件的用途速查`; `使用规则`; `现在就开始`. English equivalents — `Learning Guide`; `What This Course Is`; `File Overview and Reading Order`; `Quick File Reference`; `Usage Rules`; `Start Now`.

Content requirements:

- an explicit numbered reading order including `readiness.md`, any current foundation, `project-evolution.md`, and project milestones;
- a table mapping every file type to its purpose and when to read it, distinguishing `project-evolution.md` (why stages appear) from `roadmap.md` (what to build and in what order);
- how to answer readiness questions, choose `assume_beginner`, waive with risk, start a unit, request hints, submit review, and check progress;
- the learner's concrete first action based on `current_unit`, not an unconditional milestone-01 link;
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

Foundation completion evidence is stored in schema-v2 learner evidence and foundation status records. The paired review artifact contract below remains specific to project milestones.

## Required course headings

| Artifact | `zh-CN` headings | `en` headings |
|---|---|---|
| `project-map.md` | 项目地图；项目目的；核心用户路径；子系统；证据台账；未覆盖范围 | Project Map; Purpose; Core User Journey; Subsystems; Evidence Ledger; Uncovered Scope |
| `architecture.md` | 架构；系统上下文；组件；数据流；控制流；关键决策；证据台账 | Architecture; System Context; Components; Data Flow; Control Flow; Key Decisions; Evidence Ledger |
| `knowledge-graph.md` | 知识图谱；概念依赖；学习优先级；源码位置；最小练习 | Knowledge Graph; Concept Dependencies; Learning Priority; Source Locations; Minimal Exercises |
| `readiness.md` | 学习准备；项目所需能力；学习者基线；差距与决策；前置补给路线；进入项目的条件 | Learning Readiness; Project-Required Competencies; Learner Baseline; Gaps and Decisions; Foundation Route; Entry Conditions |
| `project-evolution.md` | 项目演变；最终问题与成熟能力；最小可用起点；演变总览；阶段因果链；最终架构如何形成；教学路线声明；证据台账 | Project Evolution; Final Problem and Mature Capabilities; Minimum Viable Starting Point; Evolution Overview; Stage Causal Chain; How the Final Architecture Emerges; Teaching-Route Disclaimer; Evidence Ledger |
| `roadmap.md` | 重构路线；路线原则；里程碑总览；覆盖范围；教学性推断 | Reconstruction Roadmap; Roadmap Principles; Milestone Overview; Coverage; Teaching Inferences |

Use one `#` for the first heading and `##` for the remaining headings.

## Foundation headings

Chinese: `前置补给单元`, `为什么现在需要`, `依赖`, `最小概念`, `小例子`, `动手练习`, `通过标准`, `项目桥接`, `暂不学习`, `完成结论`.

English: `Foundation Unit`, `Why It Is Needed Now`, `Dependencies`, `Minimal Concepts`, `Small Example`, `Hands-on Exercise`, `Exit Criteria`, `Project Bridge`, `Not Learning Yet`, `Completion Decision`.

Use matching IDs such as `foundation-01`, filenames such as `F01-java-minimum.md`, competency lines such as `competency_id: language.java.classes`, affected milestone lines such as `required_by: milestone-01`, and acceptance IDs such as `f01-a01`. Commands and technical tokens remain identical across languages.

Every foundation must explain what the learner does **not** need to study yet. The exit criteria must be observable and normally completable without copying the mature project implementation.

## Project-evolution artifact

Create it from the language-neutral evolution model, not by expanding one localized roadmap. Each stage in `阶段因果链` / `Stage Causal Chain` must state the current version, previous value, new problem, introduced change, resolved pressure, deferred limit, and next pressure. Milestone IDs and source locations must match the roadmap and milestone files. The final section must explicitly say that the route is a teaching reconstruction and is not verified author chronology unless repository history directly supports a narrower claim.

## Milestone headings

Chinese: `里程碑`, `当前版本`, `上一版本解决了什么`, `用户遇到的新问题`, `本阶段引入什么`, `目标`, `可观察结果`, `本阶段解决什么`, `范围`, `暂时不解决什么`, `前置知识`, `任务`, `验收`, `提示 1` through `提示 5`, `下一阶段为什么会出现`, `源码桥接`, `证据台账`, `完成结论`.

English: `Milestone`, `Current Version`, `What the Previous Version Solved`, `New User Problem`, `What This Stage Introduces`, `Goal`, `Observable Result`, `What This Stage Solves`, `Scope`, `Not Solving Yet`, `Prerequisites`, `Tasks`, `Acceptance`, `Hint 1` through `Hint 5`, `Why the Next Stage Appears`, `Source Bridge`, `Evidence Ledger`, `Completion Decision`.

Milestone 1 compares against the minimum viable starting point from `project-evolution.md`; later milestones compare against the preceding milestone's accepted observable result. Keep causal sections concrete and short rather than repeating the task list.

Use matching milestone IDs such as `milestone-01`, filenames such as `01-minimal-value.md`, competency lines such as `competency_id: domain.http.request-response`, optional foundation links such as `foundation_id: foundation-02`, and acceptance IDs such as `m01-a01`.

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

## Progress state: schema v2

New workspaces use UTF-8 schema-v2 JSON with English, language-neutral keys:

```json
{
  "schema_version": 2,
  "repository": {"name": "", "source": "", "revision": ""},
  "course_status": "analyzing",
  "learning_phase": "assessing",
  "current_unit": {"kind": "assessment", "id": "readiness"},
  "current_milestone": 0,
  "learner_profile": {
    "assessment_mode": "pending",
    "goals": [],
    "constraints": [],
    "competencies": []
  },
  "assessment_history": [],
  "foundation_units": [],
  "milestones": [],
  "hint_history": [],
  "open_improvements": [],
  "learner_choices": [],
  "last_review": null,
  "recommended_next_action": "analyze_repository_then_assess_prerequisites"
}
```

Allowed `learning_phase` values: `assessing`, `foundations`, `milestones`, `complete`.

Allowed `current_unit.kind` values: `assessment`, `foundation`, `milestone`. `current_unit` is null only after completion. Keep `current_milestone: 0` while assessment or a foundation is current; set it to the active project milestone number when `current_unit.kind` is `milestone`.

Allowed learner `assessment_mode` values: `pending`, `assume_beginner`, `self_report`, `micro_diagnostic`, `mixed`, `waived`.

Each competency record contains:

```json
{
  "id": "language.java.classes",
  "category": "language",
  "state": "unknown",
  "evidence_level": "none",
  "prerequisites": [],
  "required_by": ["milestone-01"],
  "blocking": true,
  "evidence": []
}
```

Allowed competency states: `unknown`, `ready`, `needs_refresh`, `learning`, `waived`. Allowed evidence levels: `none`, `self_reported`, `demonstrated`, `waived`. Competency prerequisites must form an acyclic graph. A `ready` competency requires self-reported or demonstrated evidence; a `waived` competency requires waiver evidence.

Each learner evidence record contains `type`, `summary`, and `timestamp`. Each assessment-history record contains `mode`, `summary`, and `timestamp`; a schema-v2 course cannot become active while `assessment_mode` is `pending` or assessment history is empty. Each foundation record contains `id`, `number`, `status`, `competencies`, `required_by`, `acceptance`, and `risk_notes`. Each milestone record retains `id`, `number`, `status`, `acceptance`, and `risk_notes`.

A milestone may be current only when every blocking competency whose `required_by` includes that milestone is `ready` or explicitly `waived`. Waived blockers must have risk notes.

## Schema-v1 compatibility

The validator continues to accept existing schema-v1 workspaces. Do not silently reset them. Upgrade to schema v2 at a readiness checkpoint before the next not-yet-started milestone, preserving milestone status, hint history, reviews, learner choices, and revision history.

## Bilingual parity

Both language trees must contain the same core files, foundation filenames, and milestone filenames. Paired artifacts must share stable IDs, repository source locations, commands, competency IDs, readiness states, `required_by` milestone IDs, acceptance item IDs, verdicts, stage order, and the causal meaning of each stage's current version, new problem, introduced change, deferred limit, and next pressure. Natural-language explanations should read idiomatically in each language; code identifiers and technical tokens remain unchanged.

Run `scripts/validate_course.py` before setting a course to `ready` or `complete`.
