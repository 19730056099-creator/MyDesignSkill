# Project2Learn

Project2Learn converts a mature repository into a bilingual journey for reinventing it from zero instead of merely explaining the final source tree.

## Core capabilities

- Analyze local or GitHub repositories without modifying the reference
- Build the project-required competency DAG and calibrate the learner with short questions or micro-tasks
- Generate only the transitive prerequisite bridges the learner needs, then 5–12 project milestones
- Maintain synchronized `zh-CN` and `en` course trees
- Separate code evidence, document evidence, and teaching inference
- Provide five hint levels, stage-aware code review, and persistent progress
- Validate bilingual IDs, competency nodes, foundations, sources, acceptance items, commands, reviews, and state

## Typical requests

```text
Turn this repository into a Project2Learn course. I may not know its language or framework, so calibrate me first and teach only the prerequisites this project needs.
Continue my previous Project2Learn milestone.
Give me the first-level hint for the current milestone.
Review the implementation in student/ against the current stage.
```

## Workspace

The reference repository remains unchanged. Learning artifacts live separately:

```text
project2learn/<repo>/
├── course/zh-CN/    # readiness, foundations, milestones
├── course/en/
├── student/
├── reviews/zh-CN/
├── reviews/en/
└── progress.json
```

## Scripts

```text
python scripts/init_workspace.py --reference <repo> --output-root <learning-root> --revision <revision>
python scripts/validate_course.py <learning-workspace>
```

Install `project2learn.skill`. The source tree's `evals/` directory contains three new-course and three interaction scenarios; the official Skill packager excludes evaluation fixtures from the installable archive.
