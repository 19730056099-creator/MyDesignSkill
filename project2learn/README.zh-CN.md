# Project2Learn

Project2Learn 把成熟代码仓库转换成“从零重新发明它”的中英双语学习旅程，而不是简单解释最终源码。

## 核心能力

- 只读分析本地或 GitHub 仓库
- 提取项目所需能力 DAG，并用短问答/微任务确认学习者真实起点和 `product_builder`、`cs_depth` 或 `balanced` 学习模式
- 只为个人缺口生成传递依赖有序的前置补给，再进入 5–12 个项目里程碑
- 用 `project-evolution.md` 和里程碑因果章节解释“上一版价值 → 新压力 → 设计变化 → 新限制”
- 建立技术层级与故障定位地图，按“首次触摸 → 理解 → 亲手承担”组织实践
- 明确每个单元中 AI 可生成什么、学习者必须操作/编写/解释和迁移什么
- 同步维护 `zh-CN` 与 `en` 两套课程文件
- 区分代码证据、文档证据和教学性推断
- 提供五级提示、阶段化代码评审和跨会话进度
- 使用脚本检查双语 ID、能力节点、补给、来源、验收项、命令、评审和状态一致性

## 详细使用方法

完整模式说明、请求示例、状态流转与维护者命令见 [`USAGE.zh-CN.md`](USAGE.zh-CN.md)。

## 典型请求

```text
把这个仓库变成 Project2Learn 课程；我可能完全不会它使用的语言和框架，请先确认水平，只补项目需要的前置知识。
继续上次的 Project2Learn 学习阶段。
给我当前里程碑的第一级提示。
按照当前阶段评审 student/ 中的实现。
```

## 工作区

原仓库不会被修改。课程写入单独目录：

```text
project2learn/<repo>/
├── course/zh-CN/    # 含 readiness、project-evolution、foundations、milestones
├── course/en/
├── student/
├── reviews/zh-CN/
├── reviews/en/
└── progress.json
```

## 脚本

```text
python scripts/init_workspace.py --reference <repo> --output-root <learning-root> --revision <revision>
python scripts/validate_course.py <learning-workspace>
```

安装包是 `project2learn.skill`。源码目录中的 `evals/` 包含三类新课程测试和五类交互测试；官方安装包会按 Skill 打包规则排除评测夹具。
