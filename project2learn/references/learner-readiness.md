# Learner readiness and prerequisite protocol

Use this protocol when creating a course, calibrating an existing course, entering a milestone with new prerequisites, or tutoring a foundation unit.

## 1. Separate project requirements from learner readiness

Maintain two models:

- The repository knowledge graph states which competencies the selected project path requires and why.
- The learner model states which of those competencies are ready, uncertain, missing, being learned, or explicitly waived.

Do not infer learner readiness from repository complexity, job title, years of experience, or confident wording. Learner statements are useful evidence but are not repository `code_evidence` or `document_evidence`.

## 2. Analyze enough before asking

First inspect the selected path, manifests, entry points, acceptance commands, and relevant source so the questions are project-specific. Do not finalize the personalized route or start milestone 1 yet.

Build a language-neutral competency DAG. Each competency needs:

- a stable `competency_id`;
- category: `tooling`, `language`, `framework`, `domain`, or `project_concept`;
- the smallest capability the learner must demonstrate;
- prerequisite competency IDs;
- `required_by` milestone IDs;
- whether it blocks the affected milestone;
- repository source locations or a labeled teaching inference;
- a tiny diagnostic and, if needed, a foundation-unit candidate.

Include the transitive prerequisite closure. For example, a Spring MVC controller may depend on HTTP basics, Java classes and methods, annotation syntax, and dependency injection. Do not collapse all of that into “know Spring Boot.”

Operational skills are prerequisites only when the learning workflow actually needs them. Do not require a full Git course merely because the reference is a Git repository; teach the minimal `status`/`diff`/commit subset only if course actions or review evidence require it.

## 3. Offer a low-friction calibration

Give the learner three explicit choices:

1. `assume_beginner` — create the necessary foundation route without a quiz;
2. `self_report` or `mixed` — answer a short project-specific familiarity check, with micro-diagnostics only for uncertain high-impact nodes;
3. `waived` — skip calibration after a concise risk explanation.

Prefer one short batch of roughly 3–7 high-impact questions over a generic technology questionnaire. Reuse facts the learner already supplied. Ask follow-ups only for blockers whose status would change the route.

Use capability wording rather than vague labels. Ask “Can you read a Java class with a constructor and predict a method result?” rather than “Are you intermediate at Java?”

A micro-diagnostic should normally take 2–10 minutes and produce observable evidence: predict a small program, make a tiny change, run one command, interpret an error, or explain one request/response flow. It is low-stakes and ungraded.

## 4. Record learner evidence separately

For each competency, store:

- `state`: `unknown`, `ready`, `needs_refresh`, `learning`, or `waived`;
- `evidence_level`: `none`, `self_reported`, `demonstrated`, or `waived`;
- concise evidence records such as `learner_statement`, `diagnostic_task`, `student_work`, or `explicit_waiver`;
- prerequisites, affected milestones, and blocking status.

Use `demonstrated` only for observable work. A learner may choose to proceed based on self-report for low-risk nodes. For an unverified blocking node, prefer one micro-diagnostic or a short foundation unit rather than a long examination.

## 5. Generate just-enough foundation units

Foundation units are not project reconstruction milestones. Keep the 5–12 milestone route driven by project value and engineering pressure.

Create a foundation unit only for a required gap. Topologically order units by competency dependencies and attach each unit to the milestone(s) it unlocks. Merge tightly related basics; split units that would introduce unrelated concepts.

Every localized foundation unit must contain:

- why the competency is needed now;
- prerequisite dependencies;
- a minimal explanation limited to the selected project path;
- a small example that does not copy the mature implementation;
- one hands-on exercise;
- observable exit criteria;
- the bridge to affected milestone IDs and source locations;
- an explicit “not learning yet” boundary;
- a completion decision.

A useful unit is usually 10–30 minutes. Avoid sending the learner to a full generic language or framework course when a small project-specific bridge is enough.

## 6. Gate milestones just in time

Before starting each milestone, inspect the blocking competencies whose `required_by` includes that milestone.

- `ready`: proceed.
- `needs_refresh` or `unknown`: offer the smallest diagnostic or foundation unit.
- `learning`: continue the current foundation unit.
- `waived`: proceed only with recorded risk notes.

Front-load only the foundations needed for the first milestone. Later framework, persistence, concurrency, or deployment concepts should appear immediately before the first milestone that uses them.

A foundation unit passes only with its exit evidence. After it passes, mark its competencies `ready` with `evidence_level: demonstrated`, then select the next topologically available foundation or project milestone.

## 7. Existing workspace migration

Do not invalidate or restart a schema-v1 course merely because it lacks a learner model. Preserve its current milestone and reviews. Before the next not-yet-started milestone, run a concise readiness checkpoint for that milestone, create the schema-v2 learner fields and any required foundation pairs, validate, then continue.

If the learner is already in the middle of a milestone, do not interrupt with a broad assessment. Check only a concrete prerequisite that is visibly blocking progress.

## 8. Readiness decisions

The course may be structurally generated while the learner is still preparing, but the tutor must not claim that the learner is ready for milestone 1 until one of these is true:

- all blocking prerequisites for milestone 1 are ready;
- the learner completed the required foundation units; or
- the learner explicitly waived the remaining gaps and accepted recorded risks.

Keep `current_milestone: 0` while a foundation unit is current. Use `current_unit` and `learning_phase` to distinguish assessment, foundation learning, and project reconstruction.
