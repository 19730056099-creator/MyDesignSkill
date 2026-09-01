# Learning experience renderer

Use this renderer only after the language-neutral repository, competency, learner-gap, and causal unit models are complete. Its job is not to redesign the route. Its job is to hide curriculum machinery and turn each unit into a sequence the learner can experience.

## 1. Separate the two layers

The design layer is dense and machine-readable. It keeps causal stages, competencies, evidence, prerequisites, AI boundaries, acceptance, hints, source bridges, and deferred concepts under `course/design/`.

The learner layer contains short bilingual lessons under `course/<lang>/foundations/<unit>/` and `course/<lang>/milestones/<unit>/`. It must not read like an analysis report, evidence ledger, architecture specification, or course contract.

Do not copy design-field labels into lessons. In particular, learner lessons must not expose headings such as `Current Version`, `New Problem`, `Evidence Ledger`, or `AI Usage Boundary`. The design model may remain highly structured; the learner surface should feel simple.

## 2. Render causality as experience

Internally, preserve:

```text
previous_value → new_problem → concept/change → resolution → deferred_limit → next_pressure
```

Render it as:

```text
do one small thing
→ observe a result or friction
→ stop and ask one question
→ try the smallest useful response
→ name the idea only now
→ explain only what the next action needs
→ apply it to the project
→ see what the product can do now
→ meet the next natural problem
```

Do not tell the learner the whole causal chain before they act. Let them pass through it.

## 3. Lesson rules

1. **One lesson, one cognitive goal.** Split a unit when it asks the learner to hold unrelated concepts at once.
2. **Situation before concept.** A concept earns its name only after a visible need or friction appears.
3. **Experience before explanation.** The first useful action and result come before theory.
4. **Minimum theory required now.** Explain enough to support the current action, not the mature system.
5. **Prefer prose over taxonomy.** Use short paragraphs and code/output. Avoid tables and dense label lists unless comparison itself is the cognitive goal.
6. **Pause often.** After a small amount of prose, ask for one small action, prediction, inspection, or edit. Use language such as “先别往下看 / Stop here before reading on.”
7. **One result per step.** The learner should be able to say what changed in the running product.
8. **End with product growth.** Summarize what the project can now do, not a checklist of terms learned.
9. **End on the next problem.** Create continuity without teaching the next solution early.
10. **Keep lessons small.** A foundation normally has 1–3 lessons; a milestone normally has 2–5. Split by learner activity, never by API names.

For example, split persistence as “write one record → read it after restart → represent several records → turn one line back into an object → reconnect it to the product,” not `fopen → fprintf → fgets → strtok`.

## 4. Required learner-facing shape

Each localized lesson uses these sections:

Chinese:

```text
# 第 N 课：<result-oriented title>
## 先试一下
## 你看到了什么
## 只讲现在需要的
## 把它用回项目
## 停一下，自己做
## 现在你的项目可以
## 下一步会遇到什么
```

English:

```text
# Lesson N: <result-oriented title>
## Try This First
## What Did You Notice?
## Only What You Need Now
## Put It Back Into the Project
## Stop and Do It Yourself
## What Your Project Can Do Now
## The Next Problem
```

The section titles establish rhythm, not a requirement to fill every section with the same kind of paragraph. Keep each section focused on the lesson’s single cognitive goal.

## 5. “Not now” is a teaching mechanism

A lesson may include at most one optional section:

```text
## 现在先不讲
## Not Now
```

Use it only when the learner is likely to notice a real limitation. State both:

- why the concept is unnecessary for the current result;
- what future pressure will make the course return to it.

Never use deferral to omit trust-boundary validation, data-loss prevention, security, or another requirement necessary for the current result.

## 6. Make AI guidance sound like tutoring

Keep the precise AI boundary in the design JSON. In the lesson, express it naturally near the relevant action:

> 这一小段建议你自己写。遍历并比较 ID 后面还会反复出现。卡住时先让 AI 给提示，不要先生成完整函数。

Avoid recurring policy blocks such as “AI may / learner must / learner-critical action.” The learner still owns the manual action, explanation, debugging, or transfer check recorded by the design layer and `progress.json`.

## 7. Design JSON contract

Each unit has one language-neutral file:

```text
course/design/foundations/FNN-slug.json
course/design/milestones/NN-slug.json
```

It stores at least:

- stable unit ID, number, slug, and kind;
- `why_now` for a foundation or the full causal stage for a milestone;
- competencies and prerequisite foundation links;
- exact acceptance, five-level hints, source bridges, and typed evidence;
- `practice_design.ai_allowed`, `learner_owned`, `must_explain`, and `transfer_checks`;
- lesson definitions with one `cognitive_goal`, situation, friction, action, observable result, concept name, minimum theory, project delta, next problem, and optional deferral containing `why_not_now` plus `revisit_when`.

The localized lessons share IDs, order, commands, acceptance meaning, and observable outcomes, but the prose must be idiomatic rather than sentence-by-sentence translation.

## 8. Final renderer check

Before publishing, ask:

> Is this page explaining how the course was designed, or is the learner currently making something happen?

Revise if design explanation dominates. Also reject a lesson when it starts with a definition, exposes evidence/competency metadata, has more than one cognitive goal, gives the solution before the first attempt, ends with a knowledge checklist, or lacks a small observable action.
