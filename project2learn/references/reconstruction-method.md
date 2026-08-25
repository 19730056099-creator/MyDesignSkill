# Reconstruction method

Use this protocol after the repository model and project-required competency DAG are coherent enough to support one learning track. Read `learner-readiness.md` before finalizing the personalized route.

## 1. Work backward, then present forward

1. List the mature capabilities on the selected user path.
2. For each capability, identify prerequisites, the engineering pressure it addresses, and the simplest inferior design that would expose that pressure.
3. Remove capabilities until only a minimal observable value remains. This becomes the V0/V1 candidate.
4. Order removed capabilities back into a forward sequence where every stage can be explained by a previous limitation.
5. Merge stages that do not create a meaningful learner decision; split stages that introduce multiple unrelated concepts.
6. Keep the final route between 5 and 12 milestones.

The result is a teaching reconstruction. It is not a claim about the author's actual chronology.

## 2. Keep foundations separate from milestones

A foundation unit closes a learner-specific prerequisite gap. A milestone reconstructs observable project value under engineering pressure. Do not inflate the 5–12 milestone route with generic language, framework, terminal, or Git lessons.

Attach competency IDs and any required foundation IDs to the first milestone that uses them. Front-load only the prerequisite closure for milestone 1; place later foundations just before the affected milestone. If the learner already demonstrates a competency, keep the project milestone and omit the redundant foundation.

## 3. Milestone quality contract

Every milestone needs:

- one stable ID shared across languages;
- a runnable, observable, or statically testable outcome;
- the problem and design pressure visible at this point;
- explicit scope and temporary constraints;
- stable competency IDs for prerequisites introduced just in time, with blocking status and any foundation-unit bridge;
- implementation tasks that leave design choices to the learner;
- concrete acceptance evidence;
- five progressively revealing hint levels;
- the next pressure that motivates the following stage;
- a source bridge to relevant mature-project files or symbols;
- an evidence ledger and completion decision.

Introduce an abstraction only when the learner has encountered the pressure it resolves. Avoid teaching a final architecture as ceremony.

## 4. Useful stage patterns

Choose patterns based on repository evidence, not project category labels:

- hard-coded result → parameterized input → validation → persistence;
- single request → repeated requests → concurrency/resource pressure;
- direct dependencies → boundary/interface → replaceable implementation;
- happy path → explicit errors → recovery/observability;
- in-memory state → serialization → durability/consistency;
- one component → protocol → distributed coordination;
- manual workflow → automation → scheduling/retries/idempotency.

## 5. Reject weak routes

Revise the route when it:

- mirrors folders, classes, or commit order without problem pressure;
- uses stages such as “add the service layer” without an observable reason;
- introduces several major concepts in one stage;
- cannot be accepted with evidence;
- requires a language, framework, domain, or tooling capability that is neither ready, explicitly waived, nor supplied by a just-in-time foundation unit;
- sends a learner to a broad external course instead of teaching the minimal project-relevant prerequisite subset;
- treats the mature implementation as the only valid solution;
- claims certainty about motivation not documented by the repository;
- gives the complete reference solution before the learner can attempt the task.

## 6. Bilingual rendering

Create a neutral stage record first. Render Chinese and English from that record. Pair files by identical filename and `artifact_id`. Keep code identifiers, repository paths, commands, configuration keys, API names, and protocol tokens unchanged. Translate explanation, pedagogy, constraints, and review language while preserving technical meaning.

Before marking the route ready, compare every pair for readiness decisions, competency IDs/states, foundation count/order, stage count/order, acceptance meaning, evidence sources, hint escalation, next pressure, and completion decision.
