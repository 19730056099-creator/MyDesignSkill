# Project2Learn — Agent 指南（AGENTS.md）

> 本文件是对本 skill 的理解总结，供后续 agent 快速掌握本 skill 的定位、结构、
> 工作流与约束。权威细节以 `SKILL.md` 与 `references/*.md` 为准。

## 1. Skill 定位

**Project2Learn**：把一个成熟的本地或 GitHub 代码仓库，转换为一门「从零重建
（from-zero reconstruction）」的双语（zh-CN / en）项目式课程。

核心思想：**逆向推导教学顺序 + 学习者准备度校准** —— 从成熟能力倒推出项目所需能力、传递性前置知识、工程压力和最简劣化设计；再确认学习者真正掌握了什么，只为缺口生成短小的前置补给单元，最后正向排成 5–12 个可运行的项目里程碑。注意：教学序列 ≠ 作者真实的开发历史，不得如此声称。

**触发场景**：用户想通过重建仓库学习、要求把源码转为课程、继续已有学习工作区、
要里程碑提示、提交实现请求评审。普通代码解释 / 修 bug / 仓库摘要不触发本 skill。

## 2. 目录结构与职责

```
project2learn/
├── SKILL.md                    # 入口契约 + 路由表 + 核心工作流（必读）
├── AGENTS.md                   # 本文件
├── README.zh-CN.md / README.en.md
├── USAGE.zh-CN.md              # 中文完整用法（模式/示例/状态/维护命令）
├── references/
│   ├── repository-analysis.md  # 仓库分析 + 项目所需能力 DAG
│   ├── learner-readiness.md    # 学习者校准、传递依赖、前置补给、及时门控
│   ├── reconstruction-method.md# 重建方法论（补给与里程碑分离 + 倒推正排）
│   ├── output-contract.md      # 输出契约（目录树、双语同步、GETTING_STARTED 必备）
│   ├── tutor-and-review.md     # 辅导循环、5 级提示阶梯、阶段感知评审、状态机
│   └── fanout-generation.md    # 大仓库 fan-out v3（硬门控/浅依赖/单写者收尾）
├── scripts/
│   ├── init_workspace.py       # 初始化/恢复工作区（--reference --output-root --revision）
│   ├── validate_course.py      # 课程结构校验器（analyzing 阶段必须通过）
│   └── fanout_course.workflow.js # 大仓库编排脚本
├── assets/templates/           # zh-CN 与 en 成对模板（roadmap/milestone/review 等）
│   └─ progress.json            # 语言中立的状态模板
├── evals/                      # 评测用例 + fixture 小仓库（python-cli/web-api/infra-loop/session）
└── tests/                      # init/templates/validate/fan-out 契约测试
```

按需加载原则：不要一次性读完所有 reference；根据会话模式只读对应文件。

## 3. 会话路由（先定模式，再读文件）

| 用户意图 | 模式 | 读什么 |
|---|---|---|
| 分析新仓库 / 改变范围 | `new_course` | repository-analysis → learner-readiness → reconstruction-method → output-contract |
| 回答水平问题 / 按零基础制定 | `readiness` | progress.json + learner-readiness + 相关项目知识证据 |
| 学前置补给单元 | `foundation` | progress.json + 当前补给双语文件 + learner-readiness + tutor-and-review |
| 大仓库 / monorepo，且 ≥~20 个相关文件并需要 7–12 个里程碑 | `new_course_fanout` | fanout-generation + 按阶段所需其他 reference；先执行硬门控 |
| 继续已有工作区 | `resume` | progress.json + 当前里程碑双语文档 + tutor-and-review |
| 要提示 | `hint` | progress.json + 当前里程碑 + tutor-and-review 的提示章节 |
| 提交实现评审 | `review` | progress.json + 当前里程碑 + 验收证据 + tutor-and-review + output-contract |
| 问进度 | `status` | 只读 progress.json |
| 问成熟项目为何这样设计 | `why` | 相关证据位置 + reconstruction-method；区分证据与推断 |

## 4. 不可协商的契约

1. **参考仓库只读**。课程、学生代码、评审、状态全部写入独立的
   `<learning-root>/project2learn/<repository>/` 工作区。
2. **中英严格同步**：同一 `artifact_id`、文件名、里程碑编号、命令、验收含义、
   评审结论必须一致。先建语言中立的分析模型，再分别渲染两语，禁止由一语翻译出另一语。
3. **证据标注纪律**：
   - `code_evidence`（代码证据）/ `document_evidence`（README 等文档声明，
     不等于已验证行为）/ `teaching_inference`（教学推断，必须带 `confidence`
     和 `rationale`）。
   - 测试证明期望行为而非所有实现路径；commit 历史支持时间线但不定义最佳教学顺序；
     必须说明未检查/无法运行/不确定的部分。
4. **渐进揭示**：默认从最低有用提示开始；学习者明确索要更深提示或参考实现时照办。
5. **阶段感知评审**：早期简单设计只要满足当前单元即可通过，不因缺少后期机制而挂科；但绕过学习约束的取巧代码即使输出正确也不给过。
6. **不得假设水平**：项目知识图谱不等于学习者已掌握。最终个性化路线前必须让用户选择按零基础、短校准或显式豁免；学习者证据与仓库证据分开记录。
7. **只补项目所需子集**：递归展开前置依赖，但只生成当前路线需要的 10–30 分钟补给单元；补给不计入 5–12 个项目里程碑。

## 5. 新课程工作流（线性模式）

1. 解析参考源（本地路径验证存在；GitHub URL 优先复用本地 clone，需许可才拉取缓存）。
2. 选参考仓库之外的学习根目录（用户指定或当前工作区下的 `project2learn/`）。
3. `python <skill-dir>/scripts/init_workspace.py --reference ... --output-root ... --revision ...`
4. 按 repository-analysis.md 盘点仓库，选定一条主端到端路径（monorepo 先低分辨率全图再显式裁剪）。
5. 形成语言中立仓库模型与项目所需能力 DAG：稳定 competency ID、类别、传递依赖、阻塞性、required_by、微诊断和证据。
6. 复用用户已说明的水平，让用户选择 `assume_beginner`、3–7 个项目相关的短校准，或显式豁免并记录风险；等待必要答案时保持 analyzing、current_milestone 0。
7. 计算个人缺口，按拓扑生成 0–8 个短前置补给；只前置里程碑 1 所需内容，后续依赖及时补。
8. 按 output-contract.md 渲染双语 project-map / architecture / knowledge-graph / readiness / roadmap、foundation 与 milestone，以及 `GETTING_STARTED.md`。
9. 按 reconstruction-method.md 重建 5–12 个项目里程碑；补给单元不占里程碑数量。
10. 填充 schema-v2 learner_profile、foundation、milestone 与 current_unit，保持 analyzing。
11. 运行 `validate_course.py`，修复错误直至通过。
12. 通过后置 ready：若里程碑 1 有缺口，current_unit 指向第一个 foundation 且 current_milestone 0；否则指向 milestone-01 且 current_milestone 1。再跑完整校验。
13. 汇报范围、校准决策、补给/里程碑数、不确定项、双语 readiness/roadmap 路径和第一个动作。

### Fan-out v3（仅大仓库）

**硬门控**：先排除 dependency/vendor/generated/cache/binary/大数据资产，再计数。
只有“≥~20 个相关文件”且“教学路线需要 7–12 个里程碑”时才默认 fan-out；任一条件
不满足就走线性模式。脚本内部还会做一次快速 preflight，防止直接调用误派发。
`forceFanout: true` 只用于显式诊断，不是常规路径。

拓扑必须保持浅依赖：

1. Gate：规模判断 + 学习者准备度门控；缺 learnerProfile 时返回 `assessment_required`，不生成固定路线。
2. Plan：一个强 planner 一次完成仓库分析、能力 DAG、个人缺口、语言中立模型与 plan；**禁止再派一个 analysis agent 重复读仓库**。
3. Render：把 project-map / architecture / knowledge-graph / readiness / roadmap 及所有 unit-def 合并给一个双语 writer。
4. Foundations：0–6 个补给只依赖 Render 和自己的 foundation-def；文件可并行生成，学习顺序由 DAG 和 progress 控制。
5. Milestones：7–12 个项目里程碑只依赖 Render 和自己的 milestone-def，不得彼此串联，必须一波并行。
6. Finalize：唯一共享状态写者；生成 `GETTING_STARTED.md`、聚合 schema-v2 状态、选择第一个 foundation 或 milestone 并完整校验。

执行者只接收 ≤500 词 brief、自己的任务切片、声明输入和上游 handoff；用
`validate_course.py <workspace> --partial --only <声明输出>...` 隔离自验，避免并行发布时
看到其他单元尚未成对写完的临时状态。通过的 milestone 默认不派 reviewer；
只审 partial 失败项和唯一的合并 Render，失败最多重做一次。执行者不得改
`progress.json`，只能写独立的 `orchestration/unit-status/<ID>.json`，避免并行覆盖；
Finalize 再单写聚合。核心文件建议每语 500–900 词，补给每语 400–800 词，里程碑每语 700–1200 词，
防止独立 agent 过度展开。传入 `fastModel` 给 gate/execute/review，`strongModel` 给
plan/finalize；未提供时会退回运行时默认模型，速度不作保证。

并发数只是上限；真正的加速来自“大任务 + 浅依赖 + 少 reviewer + 单写共享状态”。
自动化边界止于 `course_status: ready`，辅导仍在主对话中进行。

## 6. 交互工作流（resume/hint/review/status/why）

1. 先读 `progress.json`（双语言共享的唯一状态源）。若参考仓库 revision 变化：保留旧版本、转回 `analyzing`、重新做仓库分析后再辅导。
2. schema v2 按 `current_unit` 读取 readiness、foundation 或 milestone 双语文件；schema v1 不重置，在下一个未开始里程碑前做渐进迁移。
3. 项目里程碑开始前只检查其 blocking + required_by 能力；unknown/needs_refresh 先微诊断或补给，waived 必须有风险记录。
4. 辅导循环：brief → 学习者尝试 → 观察证据 → 定向提问/提示 → 修改 → 评审 → 下一个可用单元。
   一次只问一个有用的问题；学习者已懂就前进，不重复苏格拉底式追问。
5. **提示阶梯**（默认 Hint 1 起，明确索要则跳到对应级别，并记录 hint_history）：
   - H1 观察（预测/检查具体行为）→ H2 概念 → H3 策略 → H4 伪代码/局部接口 → H5 参考实现。
6. 评审报告八要素：优点 → 正确性/边界 → 验收通过情况 → 当前阶段合理权衡 →
   下一个规模/可靠性/可维护性压力 → 成熟仓库如何应对 → 必改 vs 可选 → 结论
   （`passed` / `needs_revision` / `skipped_with_risk`）。
7. 状态机：
   `ready→in_progress→(needs_revision↔passed)`；
   任一活动里程碑可显式跳过为 `skipped_with_risk`；
   全部 passed/skipped 且双语校验通过且存在最终桥接评审 → `complete`。
8. 中英评审文件同 review ID 同步更新，最后更新一次语言中立的 progress.json。
   仅在可观察的工作发生后才更新进度，不因聊天本身更新。

## 7. 完成门槛

- 课程 `ready` = 双语树通过校验 + readiness 决策 + 0–8 对补给 + 5–12 对项目里程碑；不代表未来所有前置能力已掌握。
- Foundation `passed` = 退出能力有可观察证据，并把相关 competency 置为 ready/demonstrated。
- 里程碑开始 = 其 blocking competency 已 ready 或显式 waived 并记录风险。
- 里程碑 `passed` = 有具体验收证据。
- 课程 `complete` = 所有里程碑 passed 或 skipped_with_risk + 双语仍对齐 +
  最终评审说明学习旅程如何衔接回成熟仓库。

## 8. 每次交互收尾必含

当前 readiness/foundation/milestone 单元与状态、学习者的下一个具体动作及验证方式、相关的中文和英文文件路径。
首次进入工作区时，先指向 `course/GETTING_STARTED.md`（若仍是占位符立即替换为课程专属指南）。
