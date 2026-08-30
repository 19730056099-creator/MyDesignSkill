# Fan-out course generation (large repositories)

Use fan-out only when context isolation is worth its cold-start cost: an oversized
repository, a monorepo, a route requiring 7–12 milestones, or a demonstrated
single-context quality failure. The automation boundary is personalized course generation. Readiness calibration remains an interactive gate: a direct workflow invocation without a learner profile returns `assessment_required` with project-specific questions instead of generating a one-size-fits-all route. Tutoring, hints, and learner review remain interactive after the course is ready.

## Hard routing gate

Before launching the workflow, count relevant source, test, manifest, example,
and documentation files. Exclude dependencies, vendor trees, generated output,
caches, binaries, and large data assets.

- Fewer than about 20 relevant files **or** at most 6 justified milestones:
  use the linear `new_course` workflow.
- At least about 20 relevant files **and** 7–12 justified milestones: fan-out may
  help when units are coarse and independent.
- An explicit `forceFanout: true` may override the gate for diagnosis, but it is
  not the normal course-generation path.

The reusable workflow performs a second cheap preflight so a direct invocation
cannot accidentally dispatch a large agent fleet for a small repository.

## v3 topology

```text
Gate        sizing plus learner-readiness gate; missing profile returns assessment_required
Plan        one strong planner writes repository, competency, learner-gap, and route models
Render      one consolidated executor writes paired core artifacts + unit definitions
Foundations 0–6 just-enough prerequisite pairs, independent after Render
Milestones  7–12 project milestone pairs, independent after Render
Finalize    one strong writer creates GETTING_STARTED, aggregates state, validates
```

The planner performs the full repository analysis itself. Before the workflow is launched, normal skill routing should collect `assume_beginner`, a short calibration result, or an explicit waiver. If a direct invocation lacks that input, one bounded readiness scan returns questions and stops before planning. The consolidated render unit keeps project-map, architecture, knowledge-graph, readiness, project-evolution, and roadmap semantically aligned.

## Phase P — analysis and master plan

The planner writes under `<workspace>/orchestration/`:

1. `conventions.md` — bilingual IDs/commands/source rules, evidence rules,
   naming/layout, read-only reference rule, output budgets, and validator commands.
2. `brief.md` — at most 500 words; the authoritative executor context.
3. `plan.json` — machine-readable render and milestone tasks.
4. `foundation-defs/<FOUNDATION-ID>.json` paths for 0–6 learner-specific prerequisite bridges. Each definition contains competency IDs, dependencies, affected milestone IDs, exit checks, and scope exclusions.
5. `milestone-defs/<MILESTONE-ID>.json` paths for 7–12 project milestones. Each definition contains title, goal, pressure, competency IDs, acceptance IDs, and key source/API locations.
6. Initial schema-v2 `progress.json.orchestration` state, preserving the supplied learner profile.

It also writes the language-neutral repository model to:

```text
course/model/analysis-model.md
```

A plan unit has this shape:

```json
{
  "id": "U07",
  "title": "Milestone 03 pair",
  "kind": "render | milestones",
  "depends_on": [],
  "inputs": ["orchestration/milestone-defs/milestone-03.json"],
  "outputs": [
    "course/zh-CN/milestones/03-example.md",
    "course/en/milestones/03-example.md"
  ],
  "acceptance": ["matching IDs, commands, evidence, and acceptance meaning"],
  "languages": ["zh-CN", "en"]
}
```

The runtime validates IDs, cardinality, output ownership, foundation bounds, and milestone count. It consolidates all render tasks into one `U-RENDER-ALL` writer and rewrites every foundation and milestone dependency to that unit. Execution units must never depend on another foundation or milestone; pedagogical prerequisite order is recorded in definitions and `progress.json`, while file rendering remains parallel.

`course/GETTING_STARTED.md` is intentionally not an execution unit. The finalizer
creates it after all filenames and ordering are known.

## Phase E — execution

Every executor receives only:

- the embedded `brief.md` text;
- its normalized unit slice;
- declared input paths;
- upstream handoff notes;
- workspace/reference/validator paths.

Do not make every executor reread the full Skill references or complete plan.
Files remain the cross-agent memory, but context should be bounded.

Executor sequence:

1. Read declared inputs and only the source files needed for evidence.
2. Write declared outputs.
3. Run partial validation:

   ```text
   python3 <skill-dir>/scripts/validate_course.py <workspace> --partial \
     --only <declared-output-1> --only <declared-output-2>
   ```

4. Fix errors in declared outputs and rerun isolated partial validation. `--only`
   prevents another concurrent unit's half-published language pair from causing
   a transient failure.
5. Write only its unique status file:

   ```text
   orchestration/unit-status/<UNIT-ID>.json
   ```

6. Return structured `validation`, `handoff`, and `risks` fields.

Executors must not edit `progress.json`; concurrent read-modify-write operations
lose updates. The finalizer is the only post-planning writer of shared state.

### Output budgets

Cold-started agents tend to overproduce. Unless repository complexity clearly
requires more, use these targets:

- each localized core artifact, including project evolution: roughly 500–900 words;
- each localized foundation: roughly 400–800 words;
- each localized milestone: roughly 700–1200 words;
- handoff note: at most 200 words.

Do not copy mature source implementations, repeat the same evidence explanation
across headings, or expand prose merely because an executor owns only one file.

## Review policy

Deterministic validation is the first gate. Do not dispatch a reviewer after
every successful milestone.

- Partial validation failure: one reviewer diagnoses the problem, then one redo.
- Consolidated render: one deterministic semantic bilingual review, because the
  validator cannot prove equivalent natural-language meaning.
- Milestone with passing partial validation: no LLM reviewer by default.
- Finalizer performs the whole-course consistency check.

A second failed attempt becomes `review_failed`. Downstream units whose required
upstream failed become `blocked`; failed work is never treated as a satisfied
dependency.

## Phase F — single-writer finalize

One finalizer:

1. Reads artifacts, unit-status files, conventions, and failure ledger.
2. Creates the course-specific bilingual `course/GETTING_STARTED.md`, pointing to readiness, project evolution, and the actual first unit.
3. Aggregates the learner profile, competency states, foundation/milestone statuses, attempts, handoffs, and risks into schema-v2 `progress.json` without deleting history.
4. Runs the full validator **without** `--partial` and fixes cross-unit errors.
5. Sets `course_status: ready` only when all required units are done. When milestone 1 has prerequisite work, it sets the first topologically available foundation as `current_unit` and keeps `current_milestone: 0`; otherwise it selects milestone 1. It then runs full validation again.
6. Reports scope, readiness decision, foundation/milestone counts, statuses, uncertainties, both readiness/roadmap paths, and the first learner action.

## Model routing and bounds

Pass a faster model as `fastModel` for gate/execution/review and a stronger model
as `strongModel` for planning/finalize when known model IDs are available. If
omitted, the workflow uses the runtime default and logs that speed is not
optimized.

Keep the plan bounded to at most 20 execution units, 0–6 foundation units, and 7–12 milestone units.
Use stable unit IDs and unique agent labels. Concurrency is only an upper bound;
speed comes from a shallow dependency graph, not from setting a large number.

## Failure and resume

- Status files are independent, so interruption cannot corrupt shared progress.
- On resume, reconcile `orchestration/unit-status/*.json` into `progress.json`
  through one writer before dispatching pending work.
- Re-run only missing/failed units and units downstream of changed outputs.
- If planning fails twice, or the hard gate rejects fan-out, return to the linear
  new-course workflow.
- Never let an executor edit another unit's outputs or the reference repository.

Reusable implementation: `scripts/fanout_course.workflow.js`.
