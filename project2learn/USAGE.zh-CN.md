# Project2Learn Skill 使用方法

Project2Learn 将成熟代码仓库转换为一门“从零重建”的中英双语项目课程，并在后续会话中提供分级提示、阶段评审和学习进度管理。

> 教学路线是根据最终代码反推的合理学习顺序，不代表项目作者真实的开发历史。

## 1. 最快开始

对本地仓库直接说：

```text
请使用 Project2Learn，把 /absolute/path/to/repository 转换成中英双语重建课程。先确认我的技术起点；如果有缺口，从第一个必要的前置补给开始，否则进入里程碑 1。
```

对 GitHub 仓库：

```text
请使用 Project2Learn 学习 https://github.com/owner/repository。
先生成完整的中英双语课程，再带我开始第一个阶段。
```

远程仓库没有合适的本地 clone 时，Skill 会先征求许可，再把仓库获取到独立参考缓存。

生成后首先阅读：

```text
<learning-workspace>/course/GETTING_STARTED.md
```

参考仓库始终只读。课程、学生代码、评审和进度保存在独立学习工作区：

```text
project2learn/<repository>/
├── course/
│   ├── GETTING_STARTED.md
│   ├── zh-CN/        # 含 readiness.md、foundations/、milestones/
│   └── en/
├── student/
├── reviews/
│   ├── zh-CN/
│   └── en/
└── progress.json
```

## 2. 模式总览

Skill 会根据你的请求判断模式。为了避免误判，建议在请求中提供参考仓库或学习工作区的明确路径。

| 模式 | 用途 | 典型说法 |
|---|---|---|
| `new_course` | 为新仓库生成课程 | “把这个仓库变成 Project2Learn 课程” |
| `readiness` | 确认技术起点、按零基础处理或豁免校准 | “我不会 Java，先补这个项目需要的内容” |
| `foundation` | 学习当前前置补给单元 | “继续当前 Java 最小补给” |
| `new_course_fanout` | 为足够大的仓库并行生成个性化课程 | “对这个大仓库运行并行 fan-out 课程生成” |
| `resume` | 继续已有学习工作区 | “继续上次的 Project2Learn 学习” |
| `hint` | 获取当前 foundation 或 milestone 的分级提示 | “我卡住了”或“给我伪代码” |
| `review` | 按当前阶段评审学生实现 | “评审 student/ 中的里程碑 3 实现” |
| `status` | 查询当前进度 | “我学到哪里了？” |
| `why` | 解释成熟项目的设计原因 | “为什么参考项目要这样设计？” |

普通源码解释、修 bug、实现功能、仓库摘要或普通代码评审不会自动进入 Project2Learn，除非你明确要求生成/继续重建课程。

---

## 3. `new_course`：生成新课程

### 适用场景

- 第一次学习某个仓库；
- 更换了参考仓库；
- 想改变课程范围或主学习路径；
- 小型和中型仓库，尤其是相关文件少于约 20 个或课程不超过 6 个里程碑。

### 推荐请求

```text
请使用 Project2Learn 分析 /path/to/repo。
学习工作区放到 /path/to/learning-root。
重点覆盖 CLI 的新增、查询、持久化和错误处理路径。
先用项目相关问题确认我的技术起点；生成完整中英双语课程后，让我从第一个必要单元开始，不要直接给参考实现。
```

可提供的信息：

- 参考仓库本地路径或 GitHub URL；
- 学习工作区根目录；
- 希望学习的产品、包、命令或端到端路径；
- 仓库 revision、tag 或 commit；
- 已掌握和不熟悉的知识；
- 明确排除的模块。

### Skill 会执行

1. 验证参考仓库，并保持只读；
2. 创建或恢复独立学习工作区；
3. 顺着一条真实用户路径分析输入、校验、状态、输出和失败路径；
4. 建立语言中立的仓库模型与项目所需能力 DAG，并递归展开真正需要的前置依赖；
5. 让你选择按零基础、短校准（通常 3–7 个能力问题，必要时一个微任务）或显式豁免；
6. 根据个人缺口生成 `readiness.md` 和 0–8 个短前置补给，不发送去学完整系统课；
7. 生成项目地图、架构、知识图谱、路线图和 5–12 对中英文项目里程碑；
8. 生成课程专属 `GETTING_STARTED.md`；
9. 校验双语能力 ID、补给、命令、来源、验收项和状态；
10. 将课程设为 `ready`。若里程碑 1 仍需补给，先进入 foundation 且 `current_milestone: 0`；否则进入里程碑 1。

### 完成后的回复应包含

- 选定的学习范围；
- 校准方式、个人缺口和补给单元数量；
- 项目里程碑数量；
- 重要未知项和教学性推断；
- 中英文 readiness 与路线图路径；
- 你的第一个具体动作及验证方法。

---

## 3A. `readiness` 与 `foundation`：只补这个项目需要的前置知识

Project2Learn 会先从选定项目路径提取能力依赖，再确认你的起点，而不是直接假设你会 Git、语言、框架或领域知识。

你可以选择：

```text
按完全零基础处理，不用考我；只生成这个项目真正需要的前置补给。
```

```text
先做快速校准。每次只问项目相关的能力问题，不要问泛泛的“初级/中级”。
```

```text
跳过准备度校准。我接受可能在里程碑中卡住的风险，请记录 waived 和风险。
```

短校准通常先问 3–7 个高影响能力问题，只在答案会改变路线时追加 2–10 分钟微任务。能力按传递依赖展开，例如 Spring MVC 可能依赖 HTTP、Java 类与方法、注解和依赖注入；已经掌握的节点会跳过。

缺口会变成独立的双语前置补给：

```text
course/zh-CN/readiness.md
course/en/readiness.md
course/zh-CN/foundations/F01-*.md
course/en/foundations/F01-*.md
```

每个补给只讲项目当前会用到的最小子集，包含小例子、动手练习、可观察通过标准、项目桥接和“暂不学习”边界。补给不计入 5–12 个项目里程碑。

只前置里程碑 1 真正需要的内容。数据库、并发、部署等知识会在第一个使用它的里程碑前及时补充，而不是开课前全部塞给你。

---

## 4. `new_course_fanout`：大仓库并行生成

### 硬门槛

默认只有同时满足以下条件才使用 fan-out：

- 至少约 20 个相关源码、测试、清单、示例或文档文件；
- 教学路线确实需要 7–12 个里程碑。

依赖目录、vendor、生成文件、缓存、二进制和大型数据资产不计入相关文件。

如果任一条件不满足，Skill 返回 `single_required` 并改用线性模式，因为多 Agent 的冷启动、重复阅读、评审和交接成本通常比并行收益更高。

### 如何明确启用

```text
请使用 Project2Learn 对 /path/to/large-repo 运行并行 fan-out 生成。
先做规模门控；满足条件才并行，否则自动退回单 Agent。
```

在支持 workflow 的运行环境里，最好明确使用“并行”“fan-out”或“运行 workflow”等措辞。

完整 fan-out 前也必须提供学习者画像：按零基础、短校准结果或显式豁免。直接调用但缺少画像时只返回 `assessment_required` 和项目相关问题，不继续生成固定路线。

### v3 并行拓扑

```text
Gate        规模判断 + 学习准备门控
Plan        一次完成仓库、能力 DAG、个人缺口和任务图
Render      一个 writer 生成全部核心双语文件和单元定义
Foundations 0–6 个独立补给文件并行生成
Milestones  7–12 个独立项目里程碑在一波中并行
Finalize    一个 writer 汇总 schema-v2 状态、选择首单元并完整校验
```

关键规则：

- 里程碑不能互相依赖；否则会退化为串行；
- Executor 只校验自己的声明输出；
- Executor 不得并发修改 `progress.json`；
- 每个单元写独立的 `orchestration/unit-status/<ID>.json`；
- 通过隔离校验的里程碑默认不再启动 Reviewer；
- Finalizer 是共享进度的唯一收尾写者；
- 小仓库不要用 `forceFanout`，该参数只适合诊断。

如果运行器支持指定模型，可将较快模型用于 Gate/Executor/Reviewer，将较强模型用于 Planner/Finalizer。

---

## 5. `resume`：继续已有课程

### 推荐请求

```text
继续 /path/to/project2learn/repository 的学习。
先读取 progress.json，只告诉我当前阶段、未解决反馈和下一步动作。
```

Skill 会先读取 `progress.json`，再按 schema-v2 的 `current_unit` 读取 readiness、foundation 或 milestone 双语文件。旧 schema-v1 课程不会被重置，而是在下一个尚未开始的里程碑前渐进补齐学习者模型。

不会因为“继续学习”而重新生成整个课程。如果参考仓库 revision 与记录不一致，则课程转回 `analyzing`，保留旧 revision，并在重新分析后继续。

首次进入一个已有工作区时，仍应先查看：

```text
course/GETTING_STARTED.md
```

---

## 6. `hint`：获取分级提示

默认从最低有用级别开始，不会立即泄露答案。

| 级别 | 内容 | 示例请求 |
|---|---|---|
| Hint 1 | 观察或预测具体行为 | “我卡住了，给我最低级提示” |
| Hint 2 | 点明相关概念 | “解释一下这里涉及什么概念” |
| Hint 3 | 给出策略或诊断顺序 | “告诉我应该采用什么思路” |
| Hint 4 | 伪代码、局部接口或代码片段 | “直接给我伪代码” |
| Hint 5 | 最小完整答案或参考实现 | “给我参考实现，我接受直接看答案” |

示例：

```text
我在当前里程碑卡住了，先只给 Hint 1。
```

```text
我已经尝试过两种方案，请跳到 Hint 4，给我核心伪代码，但不要贴完整参考实现。
```

每次提示会在 `progress.json.hint_history` 中记录里程碑、级别、原因和时间。明确请求更高级提示时可以直接跳级。

---

## 7. `review`：阶段感知代码评审

把实现放在学习工作区的 `student/` 下，并提供测试或运行证据。

### 推荐请求

```text
请按照当前 Project2Learn 里程碑评审 student/ 中的实现。
运行验收命令，区分必须修改和可选改进，并同步生成中英文评审。
```

也可以指定证据：

```text
这是里程碑 2 的实现。命令 `python -m pytest -q` 已通过。
请检查它是否违反当前阶段的约束，不要用最终仓库架构要求我。
```

评审会覆盖：

1. 优点和合理决策；
2. 正确性与边界情况；
3. 已通过和未证明的验收项；
4. 当前阶段合理的权衡；
5. 下一项规模、可靠性或可维护性压力；
6. 成熟参考仓库如何应对；
7. 必须修改与可选改进；
8. 结论。

可能结论：

- `passed`：当前里程碑验收证据充分；
- `needs_revision`：存在当前阶段必须修复的问题；
- `skipped_with_risk`：学习者明确跳过并接受风险。

简单的早期设计可以通过；不会仅因为缺少后期架构而判失败。但绕过当前里程碑学习约束的取巧实现，即使输出正确，也可能需要修改。

评审文件保存在：

```text
reviews/zh-CN/
reviews/en/
```

两种语言共享相同的 `review_id`、`milestone_id`、验收证据和 verdict。

---

## 8. `status`：查询进度

### 请求示例

```text
查看 /path/to/workspace 的 Project2Learn 进度。
```

```text
我现在学到哪里、有哪些跳过风险、下一步是什么？
```

该模式优先只读取 `progress.json`，不会重新分析仓库或改动进度。典型输出包括：

- `course_status`；
- 当前里程碑及其状态；
- 最近一次评审；
- 已使用的提示；
- 跳过风险和未解决改进；
- `recommended_next_action`。

---

## 9. `why`：理解成熟项目设计

### 请求示例

```text
为什么参考项目使用存储接口，而不是在处理函数里直接访问数据库？
请区分源码证据、文档声明和教学推断。
```

```text
成熟仓库为什么在这里引入队列？这是文档写明的，还是从最终代码推断的？
```

回答应明确标注：

- `code_evidence`：代码实际展示的机制；
- `document_evidence`：README 或设计文档的声明；
- `teaching_inference`：根据证据形成的教学解释，附 `confidence` 和 `rationale`。

最终代码能证明“现在如何实现”，通常不能单独证明“作者当初为什么这样实现”。

---

## 10. 跳过里程碑

如果确实不想完成当前阶段：

```text
我想跳过当前里程碑。先告诉我缺失的前置知识和后续风险，然后标记为 skipped_with_risk。
```

Skill 不会静默跳过。只有你明确确认后，才会记录风险并继续。

课程只有在全部里程碑为 `passed` 或 `skipped_with_risk`、双语文件仍对齐、且存在最终桥接评审时，才能进入 `complete`。

## 11. 状态流转

```text
analyzing → ready → in_progress
                      ├─→ needs_revision → passed
                      ├─→ passed
                      └─→ skipped_with_risk

全部里程碑结束 + 最终评审 + 双语校验 → complete
```

聊天本身不会改变进度。只有可观察工作、提示请求、评审结论、路线选择或明确跳过才会更新状态。

## 12. 维护者命令

初始化或恢复工作区：

```bash
python3 <skill-dir>/scripts/init_workspace.py \
  --reference <reference-repository> \
  --output-root <learning-root> \
  --revision <revision>
```

完整校验：

```bash
python3 <skill-dir>/scripts/validate_course.py <learning-workspace>
```

fan-out 生成期间的部分校验：

```bash
python3 <skill-dir>/scripts/validate_course.py <learning-workspace> --partial
```

并行单元隔离校验：

```bash
python3 <skill-dir>/scripts/validate_course.py <learning-workspace> --partial \
  --only course/zh-CN/milestones/01-example.md \
  --only course/en/milestones/01-example.md
```

设置 `ready` 或 `complete` 前必须执行完整校验，不能使用 `--partial`。

## 13. 常见问题

### 为什么没有并行生成？

仓库可能没有通过 fan-out 硬门槛。对于少于约 20 个相关文件或不超过 6 个里程碑的课程，单 Agent 通常更快。

### 为什么没有直接给我答案？

默认采用渐进提示。明确说“给我伪代码”或“给我参考实现”即可跳到 Hint 4 或 Hint 5。

### 为什么课程重新进入 analyzing？

通常是参考 revision、学习范围或课程结构发生变化，需要重新确认代码证据和双语一致性。

### 我可以把学生代码写进参考仓库吗？

不可以。参考仓库只读；所有学习实现应放在独立工作区的 `student/`。

### 中英文内容必须逐字翻译吗？

不需要逐字一致，但稳定 ID、文件名、命令、源码位置、验收含义、阶段顺序和评审结论必须一致。
