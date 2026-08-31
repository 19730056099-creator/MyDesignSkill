---
name: project2learn
description: Turn a mature local or GitHub code repository into a synchronized Chinese/English, evidence-grounded, personalized from-zero reconstruction course. Build a technology and troubleshooting map, diagnose project-relevant readiness and learning mode, introduce knowledge when project pressure makes it useful, and separate AI-assisted mechanical work from the learner's required hands-on practice, explanation, debugging, and transfer. Use whenever a user wants to learn by rebuilding a repository, reverse-engineer how a project could be constructed, convert source into a project course, assess readiness for such a course, continue a Project2Learn workspace, request milestone or foundation help, or review a stage implementation—not for an ordinary repository summary.
compatibility: Requires filesystem read access to the reference repository, write access to a separate learning workspace, Python 3 for bundled scripts, and network permission only when a remote repository must be fetched.
---

# Project2Learn

Reconstruct the learning journey behind a mature repository and personalize the route to the learner's actual starting point. Do not claim that the pedagogical sequence is the author's true development history.

## Non-negotiable contract

- Treat the reference repository as read-only. Put courses, student code, reviews, and state in a separate `project2learn/<repository>/` workspace.
- Produce synchronized `zh-CN` and `en` artifacts. Stable IDs, source locations, commands, milestone/foundation numbers, acceptance meaning, and review verdicts must match.
- Build language-neutral repository, competency, learner, and stage models before rendering either language. Do not derive one course by loosely translating the other.
- Label repository claims as `code_evidence`, `document_evidence`, or `teaching_inference`. Every teaching inference needs `confidence` and `rationale`. Store learner statements and diagnostic results separately as learner evidence.
- Do not assume that repository prerequisites are learner prerequisites already mastered. Calibrate the learner before finalizing the personalized route, unless the learner explicitly chooses `assume_beginner` or waives calibration with recorded risk.
- Teach only the transitive prerequisite subset needed by the selected project path. Use short foundation units rather than redirecting the learner to generic full courses.
- Reveal answers gradually. Start with the lowest useful hint, but honor an explicit request for a deeper hint or reference implementation.
- Review the learner against the current foundation or milestone. A simple early design may pass even when the mature project later replaces it.
- Explain every milestone as a causal evolution: previous value → new problem → introduced change → resolved pressure → deferred limit → next pressure. Keep this teaching reconstruction distinct from verified project history.
- Use `touch → understand → own`: first create a small observable encounter, then explain the mechanism, then require the learner to perform, explain, debug, or transfer the critical part.
- Build a minimal technology-layer and troubleshooting map before deep detail so the learner can place generated code, commands, data, and failures in the system.
- Declare an AI boundary for every new foundation and milestone. AI may reduce mechanical implementation cost, but it must not replace the learner's required manual action, explanation, or acceptance evidence.
- Select `product_builder`, `cs_depth`, or `balanced` learning mode from the learner's goal. Treat any 80/20 coding split as a heuristic, never a fixed quota.

## Route the request

Determine the session mode before loading detailed guidance:

| User intent | Mode | Read |
|---|---|---|
| Analyze a new repository or change scope | `new_course` | `references/repository-analysis.md`, `references/learner-readiness.md`, then `references/reconstruction-method.md` and `references/output-contract.md` |
| Answer readiness questions, request a beginner route, or calibrate prerequisites | `readiness` | `progress.json`, `references/learner-readiness.md`, relevant repository knowledge evidence, then paired `readiness.md` when present |
| Study or request help with a foundation unit | `foundation` | `progress.json`, current foundation pair, `references/learner-readiness.md`, then the relevant hint guidance in `references/tutor-and-review.md` |
| Analyze an oversized repository / monorepo, or a prior single-context run degraded | `new_course_fanout` | `references/fanout-generation.md`, plus the references above as needed per phase; collect a learner profile before full dispatch |
| Continue an existing workspace | `resume` | `progress.json`, current unit pair, `references/learner-readiness.md` when readiness/foundation work is active, then `references/tutor-and-review.md` |
| Ask for a hint | `hint` | `progress.json`, current unit pair, then the hint section of `references/tutor-and-review.md` |
| Submit an implementation for review | `review` | `progress.json`, current unit pair, acceptance evidence, `references/tutor-and-review.md`, and `references/output-contract.md` |
| Ask for progress or status | `status` | `progress.json` only; load other files only when needed to explain the next action |
| Ask why the mature project uses a design | `why` | Relevant evidence locations and `references/reconstruction-method.md`; distinguish evidence from inference |

Ordinary code explanation, bug fixing, feature implementation, generic code review, and repository summaries do not require this Skill unless the user also wants a reconstruction course or an existing Project2Learn session.

## New-course workflow

1. Resolve the reference.
   - For a local path, verify it is a directory.
   - For a GitHub URL, reuse a suitable local clone when available. Otherwise obtain permission before fetching into a separate reference cache.
   - Identify the repository name and revision when possible.
2. Choose a learning root outside the reference repository. Use the user's path when supplied; otherwise create a clearly separate `project2learn/` root in the active workspace.
3. Initialize safely:

   ```text
   python <skill-dir>/scripts/init_workspace.py --reference <reference-path> --output-root <learning-root> --revision <revision>
   ```

4. Read `references/repository-analysis.md`. Inventory the repository, select a primary end-to-end path, and form a language-neutral repository model. For a monorepo or oversized project, map the whole at low resolution and explicitly scope one learning track.
5. Read `references/learner-readiness.md`. Build the project-required competency DAG, including transitive tooling, language, framework, domain, and project-concept prerequisites. Record what each competency unlocks, where it reappears at deeper practice levels, and why the selected path needs it.
6. Calibrate readiness and learning mode before finalizing the personalized route.
   - Reuse technical-level information already supplied by the learner.
   - Offer `assume_beginner`, a short self-report/micro-diagnostic calibration, or explicit waiver with risk.
   - Select `product_builder`, `cs_depth`, or `balanced`; infer only from an explicit goal or ask one concise choice.
   - Ask only project-relevant, capability-based questions. Do not issue a generic technology survey.
   - Keep `course_status: analyzing`, `learning_phase: assessing`, and `current_milestone: 0` while awaiting required answers.
7. Compute the learner-specific prerequisite gap and topological foundation route. Create only units that close required gaps; front-load only those needed for milestone 1 and attach later units just in time.
8. Read `references/reconstruction-method.md`. Build a language-neutral evolution model and reconstruct 5–12 causally connected project milestones driven by prerequisites and engineering pressure, not directory order or commit chronology. Give each unit a first-touch action, AI boundary, manual critical practice, explanation/transfer check, and later recurrence where useful. Foundation units do not count toward the 5–12 milestone range.
9. Read `references/output-contract.md`. Render matching `project-map.md`, `architecture.md`, `knowledge-graph.md`, `readiness.md`, `project-evolution.md`, and `roadmap.md` files, plus paired foundation and milestone files and the mandatory bilingual `course/GETTING_STARTED.md`. The project map must include technology layers and a minimal failure-location path.
10. Populate schema-v3 language-neutral competency, practice-evidence, foundation, milestone, and current-unit records while keeping `course_status: analyzing`.
11. Validate the staged course:

    ```text
    python <skill-dir>/scripts/validate_course.py <learning-workspace>
    ```

    Fix validation errors while the course remains `analyzing`.
12. After validation:
    - If milestone 1 has unmet prerequisites, set `course_status: ready`, `learning_phase: foundations`, `current_unit` to the first topologically available foundation, and `current_milestone: 0`.
    - Otherwise set `course_status: ready`, `learning_phase: milestones`, `current_unit` to milestone 1, and `current_milestone: 1`.
    Run the validator again. If final validation fails, restore `analyzing` and fix the errors.
13. Report the selected scope, assessment decision, personalized gaps, foundation count, milestone count, important uncertainties, both localized roadmap/readiness paths, and the first concrete action. Keep long course content in files rather than dumping it into chat.

## Fan-out generation (large repositories)

Use fan-out only when the repository has at least about 20 relevant files **and** the justified route has 7–12 milestones, unless the user explicitly requests a diagnostic override. Collect or explicitly waive a learner profile before full generation. A direct workflow invocation without one returns `assessment_required` instead of manufacturing a fixed route. The v3 workflow uses one planner for the repository, competency, and evolution models, consolidates paired core rendering (including `project-evolution.md`), and runs bounded foundation and milestone units in a shallow parallel wave. Executors use isolated validation, write unique unit-status files, and never edit shared `progress.json`; one finalizer selects the first foundation or milestone and runs full validation. Full contract: `references/fanout-generation.md`. Script: `scripts/fanout_course.workflow.js`.

## Interactive workflow

1. Read `progress.json` first. It is the shared state source for both languages. Resolve the current reference revision; if it differs from the stored non-empty revision, retain the previous revision, transition to `analyzing`, and re-run repository analysis before tutoring resumes.
2. For schema v2 or v3, follow `current_unit`:
   - `assessment`: read readiness context and finish only the unresolved calibration;
   - `foundation`: read both localized foundation files and verify IDs/exit criteria;
   - `milestone`: read both localized milestone files and verify IDs/acceptance meaning.
3. Preserve schema-v1/v2 workspaces. Before the next not-yet-started unit, migrate only the fields required by v3 without resetting milestones, reviews, hints, or learner evidence.
4. Before any milestone begins, gate only the blocking competencies required by that milestone. Offer a diagnostic or foundation unit for unresolved gaps. Honor an explicit waiver and record its risks.
5. Follow `references/tutor-and-review.md` for tutoring, hints, reviews, skips, and state transitions. Load `references/output-contract.md` before creating or updating review artifacts.
6. Update paired localized artifacts together. Update `progress.json` once, using language-neutral values. Run the validator after changing course structure, foundation/milestone IDs, learner readiness gates, or completion state.
7. End each turn with the current unit and status, the learner's next concrete action and verification method, and the relevant Chinese and English paths. On first entry, point to `course/GETTING_STARTED.md`; replace the init placeholder before calling the course ready.

## Evidence discipline

- Cite repository-relative file paths and symbols whenever possible.
- A README claim is `document_evidence`, not automatically verified behavior.
- A test demonstrates expected behavior; it does not prove every implementation path.
- Commit history may support chronology, but it does not define the best teaching sequence.
- Design motivation inferred from final code is `teaching_inference`, even when plausible.
- Learner evidence uses learner-model records such as `learner_statement`, `diagnostic_task`, `student_work`, or `explicit_waiver`; it is never repository evidence.
- State what was not inspected, could not run, or remains uncertain.

## Completion gates

A schema-v3 course is `ready` only when both language trees validate, include the paired project-evolution artifact, technology/troubleshooting maps, unit AI boundaries, 5–12 paired milestones, and readiness plus learning-mode decisions. “Ready” means the personalized learning path is ready; it does not imply every future prerequisite is already mastered. A foundation unit passes only with exit evidence and, in schema v3, matching direct practice evidence. A project milestone may start only when its blocking competencies are ready or explicitly waived with risk. A schema-v3 milestone passes only with behavioral acceptance plus the learner's manual action, observable result, explanation, AI-usage record, and achieved practice depth. The course is `complete` only when all milestones are passed or explicitly skipped with risk, both language trees remain aligned, and the final review connects the learner's journey back to the mature repository.
