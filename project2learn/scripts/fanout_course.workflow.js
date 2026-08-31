export const meta = {
  name: 'project2learn_fanout',
  description: 'Generate large personalized Project2Learn courses with a hard size gate, learner-readiness gate, consolidated rendering, bounded foundation and milestone units, deterministic validation, and one final writer.',
  phases: [
    { title: '🔎 阶段1/4：并行适用性与学习准备检查' },
    { title: '📋 阶段2/4：分析与总规划' },
    { title: '⚙️ 阶段3/4：渲染、补给与并行里程碑' },
    { title: '✅ 阶段4/4：单写者收尾' },
  ],
};

const skillDir = args.skillDir;
const workspace = args.workspace;
const reference = args.reference;
const fastModel = args.fastModel || undefined;
const strongModel = args.strongModel || undefined;
const forceFanout = args.forceFanout === true;
const learnerProfile = args.learnerProfile || null;
const orchDir = `${workspace}/orchestration`;

const PREFLIGHT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['referenceFileCount', 'estimatedMilestones', 'oversized', 'reason'],
  properties: {
    referenceFileCount: { type: 'integer', minimum: 0 },
    estimatedMilestones: { type: 'integer', minimum: 1, maximum: 12 },
    oversized: { type: 'boolean' },
    reason: { type: 'string' },
  },
};

const READINESS_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['requiredCompetencies', 'calibrationQuestions', 'reason'],
  properties: {
    requiredCompetencies: {
      type: 'array',
      maxItems: 12,
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['id', 'capability', 'category', 'prerequisites', 'blocking'],
        properties: {
          id: { type: 'string' },
          capability: { type: 'string' },
          category: { type: 'string', enum: ['tooling', 'language', 'framework', 'domain', 'project_concept'] },
          prerequisites: { type: 'array', items: { type: 'string' } },
          blocking: { type: 'boolean' },
        },
      },
    },
    calibrationQuestions: { type: 'array', minItems: 1, maxItems: 7, items: { type: 'string' } },
    reason: { type: 'string' },
  },
};

const UNIT_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['id', 'title', 'kind', 'depends_on', 'inputs', 'outputs', 'acceptance', 'languages'],
  properties: {
    id: { type: 'string' },
    title: { type: 'string' },
    kind: { type: 'string', enum: ['render', 'foundations', 'milestones'] },
    depends_on: { type: 'array', items: { type: 'string' } },
    inputs: { type: 'array', items: { type: 'string' } },
    outputs: { type: 'array', items: { type: 'string' } },
    acceptance: { type: 'array', items: { type: 'string' } },
    languages: { type: 'array', items: { type: 'string' } },
  },
};

const PLAN_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['units', 'brief'],
  properties: {
    units: { type: 'array', minItems: 1, maxItems: 20, items: UNIT_SCHEMA },
    brief: { type: 'string' },
  },
};

const EXEC_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['validation', 'handoff', 'risks'],
  properties: {
    validation: { type: 'string', enum: ['pass', 'fail'] },
    handoff: { type: 'string' },
    risks: { type: 'string' },
  },
};

const REVIEW_SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['verdict', 'reason'],
  properties: {
    verdict: { type: 'string', enum: ['pass', 'fail'] },
    reason: { type: 'string' },
  },
};

function agentOptions(label, model, schema) {
  const options = { label };
  if (model) options.model = model;
  if (schema) options.schema = schema;
  return options;
}

function unique(values) {
  return [...new Set((values || []).filter(Boolean))];
}

function foundationIdFromUnit(unit) {
  const outputs = (unit.outputs || []).join(' ');
  const outputMatch = outputs.match(/foundations\/F(\d{1,2})-/i);
  const fallback = String(unit.id || '').match(/(\d{1,2})/);
  const number = outputMatch ? outputMatch[1] : (fallback ? fallback[1] : null);
  return number ? `foundation-${Number(number).toString().padStart(2, '0')}` : null;
}

function milestoneIdFromUnit(unit) {
  const outputs = (unit.outputs || []).join(' ');
  const outputMatch = outputs.match(/milestones\/(\d{1,2})-/i);
  const fallback = String(unit.id || '').match(/(\d{1,2})/);
  const number = outputMatch ? outputMatch[1] : (fallback ? fallback[1] : null);
  return number ? `milestone-${Number(number).toString().padStart(2, '0')}` : null;
}

function normalizePlan(rawUnits) {
  const units = Array.isArray(rawUnits) ? rawUnits : [];
  if (!units.length || units.length > 20) {
    return { error: `plan must contain 1-20 units, found ${units.length}` };
  }

  const ids = units.map(unit => unit.id);
  if (ids.some(id => !/^U[A-Za-z0-9_-]+$/.test(id)) || new Set(ids).size !== ids.length) {
    return { error: 'plan unit IDs must be unique and match /^U[A-Za-z0-9_-]+$/' };
  }

  const renderUnits = units.filter(unit => unit.kind === 'render');
  const foundationUnits = units.filter(unit => unit.kind === 'foundations');
  const milestoneUnits = units.filter(unit => unit.kind === 'milestones');
  if (!renderUnits.length) return { error: 'plan requires at least one render unit' };
  if (foundationUnits.length > 6) {
    return { error: `plan permits at most 6 just-enough foundation units, planner produced ${foundationUnits.length}` };
  }
  if (!milestoneUnits.length || milestoneUnits.length > 12) {
    return { error: `plan requires 1-12 milestones, planner produced ${milestoneUnits.length}` };
  }
  const singleRequired = milestoneUnits.length < 7;

  const render = {
    id: 'U-RENDER-ALL',
    title: 'Consolidated bilingual core render and milestone definitions',
    kind: 'render',
    depends_on: [],
    inputs: unique(renderUnits.flatMap(unit => unit.inputs)),
    outputs: unique(renderUnits.flatMap(unit => unit.outputs)),
    acceptance: unique(renderUnits.flatMap(unit => unit.acceptance)),
    languages: ['zh-CN', 'en'],
  };

  const foundations = foundationUnits.map(unit => {
    const foundationId = foundationIdFromUnit(unit);
    const definition = foundationId ? `orchestration/foundation-defs/${foundationId}.json` : null;
    return {
      ...unit,
      depends_on: [render.id],
      inputs: unique([...(unit.inputs || []), definition]),
      languages: ['zh-CN', 'en'],
    };
  });

  const milestones = milestoneUnits.map(unit => {
    const milestoneId = milestoneIdFromUnit(unit);
    const definition = milestoneId ? `orchestration/milestone-defs/${milestoneId}.json` : null;
    return {
      ...unit,
      depends_on: [render.id],
      inputs: unique([...(unit.inputs || []), definition]),
      languages: ['zh-CN', 'en'],
    };
  });

  const normalized = [render, ...foundations, ...milestones];
  const outputOwners = {};
  for (const unit of normalized) {
    for (const output of unit.outputs || []) {
      if (outputOwners[output]) {
        return { error: `output collision: ${output} belongs to ${outputOwners[output]} and ${unit.id}` };
      }
      outputOwners[output] = unit.id;
    }
  }
  return {
    units: normalized,
    singleRequired,
    reason: singleRequired ? `fan-out requires at least 7 milestones; planner produced ${milestoneUnits.length}` : '',
  };
}

// A direct workflow invocation still gets a cheap gate. Normal skill routing
// should count files before launching and avoid this workflow for small repos.
phase('🔎 阶段1/4：并行适用性与学习准备检查');
log(`checking whether fan-out is appropriate for ${reference}`);
const preflight = await agent([
  `Inspect the reference repository at ${reference} without modifying it.`,
  `Count relevant source, test, manifest, example, and documentation files; exclude dependencies, vendor trees, generated output, caches, binaries, and large data assets.`,
  `Estimate how many pressure-driven Project2Learn milestones are justified (5-12).`,
  `Return only the requested structured result. This is a fast sizing pass, not full analysis.`,
].join('\n'), agentOptions('fanout-gate', fastModel, PREFLIGHT_SCHEMA));

if (!preflight) {
  return { mode: 'incomplete', error: 'fan-out preflight returned no result' };
}
const smallRepository = preflight.referenceFileCount < 20 || preflight.estimatedMilestones <= 6;
if (smallRepository && !forceFanout) {
  log(`fan-out rejected: ${preflight.referenceFileCount} relevant files, about ${preflight.estimatedMilestones} milestones`);
  return {
    mode: 'single_required',
    reason: 'Cold-start and coordination overhead exceed the benefit below 20 files or at 6 milestones or fewer.',
    preflight,
  };
}
const learningMode = learnerProfile && learnerProfile.learning_mode;
const validLearningMode = ['product_builder', 'cs_depth', 'balanced'].includes(learningMode);
if (!learnerProfile || !validLearningMode) {
  log('learner profile or v3 learning mode missing; producing a project-specific calibration instead of a fixed course');
  const readiness = await agent([
    `Inspect only the manifests, entry points, acceptance commands, and documented primary path at ${reference}; do not modify the repository.`,
    `Read ${skillDir}/references/learner-readiness.md.`,
    `Identify the transitive high-impact tooling, language, framework, domain, and project-concept prerequisites needed to begin the selected path.`,
    `Use capability wording, not beginner/intermediate labels. Do not require Git unless the learning workflow genuinely needs Git operations.`,
    `Return 3-7 short questions total: project-specific readiness plus one concise product_builder/cs_depth/balanced learning-mode choice. The user may instead choose assume_beginner or explicit waiver with risk.`,
    `This is a bounded readiness scan, not the full repository analysis.`,
  ].join('\n'), agentOptions('readiness-gate', fastModel, READINESS_SCHEMA));
  return {
    mode: 'assessment_required',
    reason: 'A learner profile plus product_builder, cs_depth, or balanced learning mode is required before personalized fan-out generation.',
    preflight,
    readiness,
  };
}
if (!fastModel) log('fastModel was not supplied; executor speed will use the runtime default');
if (!strongModel) log('strongModel was not supplied; planner/finalizer will use the runtime default');

phase('📋 阶段2/4：分析与总规划');
log('running one planner that also writes the neutral analysis model');
const planner = await agent([
  `You are the planner for Project2Learn fan-out generation v3.`,
  `Skill dir: ${skillDir}. Reference repository (READ-ONLY): ${reference}. Workspace: ${workspace}.`,
  `Read ${skillDir}/references/fanout-generation.md, repository-analysis.md, learner-readiness.md, reconstruction-method.md, and output-contract.md.`,
  `Schema-v3 learner profile and learning mode: ${JSON.stringify(learnerProfile)}. Treat learner statements as learner evidence, never repository evidence. Do not turn the learning mode into a fixed percentage of learner-written code.`,
  `Analyze the repository once and write the language-neutral repository, competency, project-evolution, technology-layer, troubleshooting, and spiral-practice models to ${workspace}/course/model/analysis-model.md. Do not create a separate analysis execution unit.`,
  `Write ${orchDir}/conventions.md, ${orchDir}/brief.md (at most 500 words), and ${orchDir}/plan.json. Initialize schema-v3 progress.json and its orchestration object once, preserving prior history; executors must not edit progress.json.`,
  `Compute the learner-specific transitive prerequisite gap. Plan 0-6 independent, just-enough foundation units and 7-12 independent project milestone units; foundations do not count as milestones.`,
  `Static project-map, architecture, knowledge-graph, readiness, project-evolution, and roadmap files may appear as render units; the workflow will consolidate them into one writer.`,
  `Render outputs must include paired course/<lang>/project-evolution.md, a project map with technology layers and troubleshooting paths, ${orchDir}/foundation-defs/<FOUNDATION-ID>.json for every foundation, and ${orchDir}/milestone-defs/<MILESTONE-ID>.json for every milestone. Evolution and milestone definitions must share one causal chain. Every unit definition must also contain first_touch, manual_actions, ai_allowed, must_explain, transfer_check, and reappears_in. Every execution unit consumes only its own definition and must not depend on another foundation or milestone.`,
  `Do not create a getting-started execution unit; finalize writes course/GETTING_STARTED.md.`,
  `The execution brief must include concise output budgets: normally 500-900 words per localized core artifact, 400-800 words per localized foundation, and 700-1200 words per localized milestone, with no copied source implementation.`,
  `Return only the requested structured plan and the exact brief text.`,
].join('\n'), agentOptions('fanout-planner', strongModel, PLAN_SCHEMA));

if (!planner) return { mode: 'incomplete', error: 'planner returned no result' };
const normalized = normalizePlan(planner.units);
if (normalized.singleRequired && !forceFanout) {
  log(normalized.reason);
  return { mode: 'single_required', reason: normalized.reason, preflight };
}
if (normalized.error) return { mode: 'incomplete', error: normalized.error };
const plan = normalized.units;
const brief = String(planner.brief || '');
const foundationCount = plan.filter(unit => unit.kind === 'foundations').length;
const milestoneCount = plan.filter(unit => unit.kind === 'milestones').length;
log(`plan normalized to ${plan.length} execution units: 1 consolidated render + ${foundationCount} foundations + ${milestoneCount} milestones`);

phase('⚙️ 阶段3/4：渲染、补给与并行里程碑');
const handoffs = {};
const status = {};
const settled = new Set();
for (const unit of plan) status[unit.id] = 'pending';

function executorPrompt(unit, attempt, rejection) {
  const upstream = (unit.depends_on || []).map(id => `${id}: ${handoffs[id] || '(missing handoff)'}`).join('\n');
  const selectedOutputs = (unit.outputs || []).map(path => `--only ${path}`).join(' ');
  return [
    `You are execution unit ${unit.id} in Project2Learn fan-out v3. The reference is READ-ONLY: ${reference}. Workspace: ${workspace}.`,
    `Authoritative execution brief:`,
    brief,
    `Your unit: ${JSON.stringify(unit)}`,
    upstream ? `Upstream handoffs:\n${upstream}` : '',
    `Read only declared inputs and files needed to verify source evidence. Write only declared outputs plus your unique status file ${orchDir}/unit-status/${unit.id}.json.`,
    `Do not edit progress.json; the finalizer is its only post-planning writer.`,
    `Keep prose within the brief's output budgets. Use the schema-v3 Touch → Understand → Own sections. State AI allowance, learner-owned critical practice, explanation, and transfer checks explicitly. Do not duplicate mature source code or repeat the same evidence explanation across sections.`,
    `After writing, run isolated validation: python3 ${skillDir}/scripts/validate_course.py ${workspace} --partial ${selectedOutputs}`,
    `Fix errors in your declared outputs and rerun. --only isolates this unit from files being published concurrently; never run workspace-wide or full validation here.`,
    rejection ? `Previous attempt failed: ${rejection}` : '',
    `Write the unique unit-status JSON with unit_id, attempt (${attempt}), validation, files, and risks. Return only the requested structured result; handoff must be at most 200 words.`,
  ].filter(Boolean).join('\n\n');
}

async function runExecutor(unit, attempt, rejection) {
  return agent(
    executorPrompt(unit, attempt, rejection),
    agentOptions(`exec-${unit.id}-a${attempt}`, fastModel, EXEC_SCHEMA),
  );
}

async function reviewUnit(unit, attempt, reason) {
  return agent([
    `Review Project2Learn unit ${unit.id} without editing files.`,
    `Outputs: ${JSON.stringify(unit.outputs)}. Acceptance: ${JSON.stringify(unit.acceptance)}.`,
    `Check concise scope, required evidence, and zh-CN/en semantic synchronization.`,
    reason ? `The executor reported this problem: ${reason}` : '',
    `Return only the requested structured verdict.`,
  ].filter(Boolean).join('\n'), agentOptions(`review-${unit.id}-a${attempt}`, fastModel, REVIEW_SCHEMA));
}

async function executeUnit(unit) {
  status[unit.id] = 'running';
  let output = await runExecutor(unit, 1, '');
  let rejection = '';

  if (!output || output.validation !== 'pass') {
    const diagnostic = await reviewUnit(unit, 1, output ? output.risks : 'executor returned no result');
    rejection = diagnostic ? diagnostic.reason : 'partial validation failed and reviewer returned no diagnosis';
  } else if (unit.kind === 'render') {
    // Exactly one deterministic semantic review: the consolidated render unit.
    const semantic = await reviewUnit(unit, 1, '');
    if (!semantic || semantic.verdict !== 'pass') rejection = semantic ? semantic.reason : 'render reviewer returned no result';
  }

  if (rejection) {
    log(`${unit.id} retrying once: ${rejection}`);
    output = await runExecutor(unit, 2, rejection);
    if (!output || output.validation !== 'pass') {
      status[unit.id] = 'review_failed';
      handoffs[unit.id] = output ? output.handoff : 'executor returned no result';
      return false;
    }
    if (unit.kind === 'render') {
      const secondReview = await reviewUnit(unit, 2, 'verify the corrected consolidated render');
      if (!secondReview || secondReview.verdict !== 'pass') {
        status[unit.id] = 'review_failed';
        handoffs[unit.id] = secondReview ? secondReview.reason : 'reviewer returned no result';
        return false;
      }
    }
  }

  status[unit.id] = 'done';
  handoffs[unit.id] = output.handoff;
  return true;
}

while (settled.size < plan.length) {
  const ready = plan.filter(unit =>
    !settled.has(unit.id) && (unit.depends_on || []).every(id => status[id] === 'done')
  );
  if (!ready.length) break;
  log(`dispatching parallel wave: ${ready.map(unit => unit.id).join(', ')}`);
  await parallel(ready.map(unit => async () => {
    const result = await executeUnit(unit);
    settled.add(unit.id);
    log(`${unit.id}: ${status[unit.id]}`);
    return { id: unit.id, ok: result };
  }));
}

for (const unit of plan) {
  if (!settled.has(unit.id) && status[unit.id] === 'pending') status[unit.id] = 'blocked';
}
const failed = plan.filter(unit => status[unit.id] !== 'done').map(unit => unit.id);

phase('✅ 阶段4/4：单写者收尾');
log(failed.length ? `finalizing with failed/blocked units: ${failed.join(', ')}` : 'all execution units done; running full validation');
const report = await agent([
  `Finalize Project2Learn fan-out v3 as the only post-planning writer of progress.json.`,
  `Workspace: ${workspace}. Reference: ${reference}. Skill dir: ${skillDir}.`,
  `Unit statuses: ${JSON.stringify(status)}. Failed or blocked: ${JSON.stringify(failed)}.`,
  `Read ${orchDir}/conventions.md, unit-status files, course artifacts, and Phase F of fanout-generation.md.`,
  `Create the course-specific bilingual course/GETTING_STARTED.md here; there is intentionally no separate getting-started executor. Use artifact_id getting-started, language bilingual, every required bilingual heading from output-contract.md, and point to readiness, project-evolution, the technology map, and the actual current foundation or milestone.`,
  `Aggregate orchestration statuses, the schema-v3 learner profile and learning mode, competency practice depths, empty initial practice_evidence, foundation records, milestone records, handoffs, and risks into schema-v3 progress.json without discarding history.`,
  `Run full validation without --partial: python3 ${skillDir}/scripts/validate_course.py ${workspace}. Fix structural and cross-unit errors, then rerun.`,
  `Only if every required unit is done and validation passes, set course_status to ready. If milestone 1 still has required foundation work, set learning_phase to foundations, current_unit to the first topologically available foundation, and current_milestone to 0. Otherwise set learning_phase to milestones, current_unit to milestone-01, and current_milestone to 1. Then run full validation again.`,
  `Return a concise Chinese report: scope, readiness decision, foundation and milestone counts, unit statuses, uncertainties, both readiness/roadmap paths, and the learner's first action.`,
].join('\n'), agentOptions('fanout-finalize', strongModel, null));

return {
  mode: failed.length ? 'incomplete' : 'fanout',
  preflight,
  failedUnits: failed,
  statuses: status,
  report,
};
