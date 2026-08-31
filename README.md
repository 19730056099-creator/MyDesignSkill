# MyDesignSkill

一组面向 AI 助手的可复用 Skills，覆盖学习、考试复习、代码简化以及 Word、PDF、PPT 文档处理。每个子目录都是一个相对独立的 Skill，详细触发条件、工作流程和限制见对应的 `SKILL.md`。

## 当前 Skills

| Skill | 用途 | 入口 |
|---|---|---|
| [`interactive-tutorial-page`](interactive-tutorial-page/) | 用交互式动画和自主操作，为零基础用户讲解数学、物理、编程、算法、语言、经济等知识 | [`SKILL.md`](interactive-tutorial-page/SKILL.md) |
| [`project2learn`](project2learn/) | 将成熟代码仓库转换成中英双语的“从零重建”学习课程，支持准备度与学习模式诊断、技术层级/故障定位地图、Touch → Understand → Own 实践、里程碑和阶段评审 | [`SKILL.md`](project2learn/SKILL.md) · [中文说明](project2learn/README.zh-CN.md) · [完整用法](project2learn/USAGE.zh-CN.md) |
| [`college-final-exam-ai-skill`](college-final-exam-ai-skill/) | 根据课程 PPT、考试重点和往年题，建立面向得分的大学期末考试知识系统 | [`SKILL.md`](college-final-exam-ai-skill/SKILL.md) · [项目说明](college-final-exam-ai-skill/README.md) |
| [`docx`](docx/) | 创建、读取、编辑和分析 Word 文档（`.docx`） | [`SKILL.md`](docx/SKILL.md) |
| [`pdf`](pdf/) | 读取、提取、合并、拆分、填写和生成 PDF 文件 | [`SKILL.md`](pdf/SKILL.md) |
| [`pptx`](pptx/) | 读取、创建、编辑和检查 PowerPoint 演示文稿（`.pptx`） | [`SKILL.md`](pptx/SKILL.md) |
| [`ponytail`](ponytail/) | 以最小可行方案解决代码任务，优先使用标准库和平台能力，避免过度设计 | [README](ponytail/README.md) · [`SKILL.md`](ponytail/skills/ponytail/SKILL.md) |
| [`skill-creator`](skill-creator/) | 创建、修改、评估和优化 AI Skill | [`SKILL.md`](skill-creator/SKILL.md) |

## 快速使用

直接在请求中描述目标，或指定需要使用的 Skill：

```text
使用 interactive-tutorial-page，制作一个“二分查找”的零基础交互式教程。

使用 project2learn，把这个代码仓库变成一门从零开始的学习课程。

使用 build-exam-knowledge-system，根据我上传的 PPT 和往年题制定期末复习方案。

使用 docx，把这份内容整理成格式规范的 Word 报告。

使用 pdf，提取这个 PDF 的表格并合并指定页面。

使用 pptx，根据这份材料制作一套演示文稿。

使用 ponytail，给出能工作的最简单实现，不要增加不必要的抽象。

使用 skill-creator，创建一个处理某类任务的新 Skill，并设计验证方法。
```

Skill 被触发后，助手会按对应 `SKILL.md` 的规则工作。文档类 Skill 只在请求涉及相应文件类型时使用；学习类 Skill 会根据目标和基础选择合适的教学或复习流程。Project2Learn 会先进行项目相关准备度校准（或按零基础/显式豁免处理），并记录 AI 使用与学习者的亲手实践证据。

## Project2Learn v3

Project2Learn 当前使用 schema v3：每个 foundation 和 milestone 都声明首次触摸、AI 使用边界、关键亲手实践以及理解/迁移检查；通过单元还需要匹配的实践证据。旧 schema v1/v2 工作区可以渐进迁移，不会重置历史进度。

## 项目结构

```text
.
├── README.md
├── interactive-tutorial-page/
├── project2learn/
├── college-final-exam-ai-skill/
├── docx/
├── pdf/
├── pptx/
├── ponytail/
└── skill-creator/
```

每个 Skill 通常包含以下内容：

- `SKILL.md`：Skill 的名称、触发条件、核心规则和完成标准
- `references/`：按需读取的详细参考资料
- `templates/`：可复用的输出模板
- `examples/`：示例或评测材料
- `scripts/`：重复性任务的辅助脚本

## 使用建议

1. 先阅读目标目录中的 `SKILL.md`，确认它是否匹配当前任务。
2. 涉及文档或演示文稿时，明确输入文件类型和期望输出格式。
3. 涉及课程或代码学习时，提供已有材料、目标和当前基础，结果会更准确。
4. 需要扩展能力时，优先复用现有 Skill 的模板和参考资料。

## 相关说明

- [`project2learn/README.zh-CN.md`](project2learn/README.zh-CN.md)：Project2Learn 中文介绍与使用示例。
- [`college-final-exam-ai-skill/README.md`](college-final-exam-ai-skill/README.md)：大学期末考试 Skill 的完整说明。
- [`ponytail/README.md`](ponytail/README.md)：Ponytail 的完整介绍、示例和基准测试。
- [`college-final-exam-ai-skill/website/README.md`](college-final-exam-ai-skill/website/README.md)：期末考试 Skill 配套网站的开发说明。

## 许可

各 Skill 的许可和使用限制可能不同，请以对应目录中的 `LICENSE`、`LICENSE.txt` 或项目说明为准。
