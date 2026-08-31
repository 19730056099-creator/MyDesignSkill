# Repository analysis protocol

Use this protocol for a new course, a repository revision change, or a scope change.

## 1. Establish identity and boundaries

Record the resolved source, repository name, revision when available, languages, build system, and declared purpose. Create a before-analysis inventory of reference files when practical. Never write analysis artifacts into the reference.

Exclude generated outputs, dependencies, vendor trees, caches, binaries, and large data assets unless they are central to the user journey. Record every exclusion.

For a monorepo or repository with multiple products:

1. Produce a low-resolution map of top-level products.
2. Rank candidate learning tracks by centrality, observability, and prerequisite burden.
3. Use the user's choice when given; otherwise select the main documented user path.
4. Mark all other products as uncovered scope.

## 2. Inspect in evidence order

Inspect evidence in this order, adapting to the repository:

1. README, design documents, examples, and usage instructions.
2. Dependency/build manifests and executable entry points.
3. Tests, fixtures, and public interfaces.
4. Configuration, schemas, protocols, persistence, and external integrations.
5. Core modules along the selected end-to-end path.
6. Error handling, concurrency, resource lifecycle, observability, and extension points.
7. Commit history only when it can resolve a specific uncertainty.

Do not mistake a directory listing for analysis. Follow at least one meaningful user action through input, validation, transformation, state, output, and failure paths.

## 3. Build the neutral analysis model

Capture these language-neutral fields before writing localized prose:

- `purpose`: problem, intended user, observable value.
- `journey`: ordered steps for the main user action.
- `subsystems`: stable ID, responsibility, inputs, outputs, dependencies, source locations.
- `flows`: data and control edges between subsystem IDs.
- `technology_map`: the minimum learner-facing layers from user action through runtime, network/process boundaries, application components, and storage; include only layers present in the selected path.
- `troubleshooting_map`: observable failure, likely layer, first inspection action, and the next boundary to check. This is an orientation map, not a generic operations syllabus.
- `decisions`: design mechanism, pressure it addresses, alternatives visible in evidence.
- `pressure_candidates`: mature capability or mechanism, the problem it addresses, the simplest inferior design that would expose that problem, and supporting evidence. These are inputs to a teaching reconstruction, not chronology claims.
- `knowledge`: competency ID, category (`tooling`, `language`, `framework`, `domain`, or `project_concept`), smallest required capability, project need, prerequisite IDs, `required_by` milestone candidates, blocking status, source locations, learning priority, micro-diagnostic, foundation-unit candidate, and later units where the capability can recur at `touched`, `explained`, `debugged`, or `transferred` depth.
- `unknowns`: unresolved questions and their impact.
- `uncovered_scope`: intentionally omitted parts and why.
- `evidence`: typed entries supporting the fields above.

## 4. Evidence ledger

Use one of these exact forms:

```text
evidence: code_evidence
source: path/to/file.ext::symbol
rationale: What the source demonstrates.
```

```text
evidence: document_evidence
source: README.md#section
rationale: What the project documentation claims.
```

```text
evidence: teaching_inference
confidence: low|medium|high
rationale: Why this is a useful or plausible teaching interpretation.
source: One or more evidence locations that informed the inference.
```

Keep facts and inferences separate even when they appear in the same section.

## 5. Build the project-required competency DAG

The repository model describes project requirements, not the learner's mastery. Before asking about technical level:

1. Trace the competencies needed by the selected end-to-end path and its acceptance commands.
2. Expand each competency to its transitive prerequisites. Do not use broad labels such as “Java” or “Spring Boot” when the route needs only classes/methods, annotation syntax, dependency injection, and one MVC request path.
3. Separate operational tooling from project concepts. Git is blocking only if the course workflow actually requires Git operations.
4. Give every node a stable ID, a smallest observable capability, affected milestone candidates, and a tiny diagnostic.
5. Read `learner-readiness.md` before deciding which nodes become personalized foundation units.

Do not infer the learner's state in this repository analysis. Store learner statements and diagnostic results later in the learner model, not in the repository evidence ledger.

## 6. Architecture and knowledge checks

Before readiness calibration and reconstruction, confirm that the analysis answers:

- What useful result does the project produce?
- What is the smallest end-to-end path that demonstrates that value?
- Which subsystems are essential on that path?
- Where do data and control cross subsystem boundaries?
- Can a beginner place each command, generated file, runtime process, and common failure on a minimal technology-layer map?
- Does every high-frequency failure have a smallest first inspection step rather than an open-ended “debug it” instruction?
- What failures or scale pressures explain the mature mechanisms?
- What minimum useful V0 could expose the first pressure without prematurely copying the mature architecture?
- Which concepts are prerequisites, what is their transitive dependency order, and which can be learned just before the milestone that first uses them?
- Which operational skills are genuinely required by the course workflow rather than merely present in the repository ecosystem?
- What important area remains uninspected or unverified?

If runtime verification is unavailable, label static conclusions and list the commands that would verify them.
