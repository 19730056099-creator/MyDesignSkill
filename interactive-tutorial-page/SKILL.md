---
name: interactive-tutorial-page
description: 用「交互式动画 + 自主操作」向零基础用户讲解任意学科知识点时使用（纯静态、无框架、file:// 可离线打开的单页教程）。适用于数学、物理、编程、算法、语言、经济等任何需要图解演示的学习主题。
---

# 零基础交互式图解页面通用方法论

从多个教学页面项目沉淀的通用规范，适用于**任何学科**。新建/修改此类「零基础交互式图解」页面时默认遵循。

## 1. 项目定位

- 用「交互式动画 + 自主操作」向**零基础**用户讲解知识点，不限学科。
- 纯静态：无框架、无外部 CDN 资源，`file://` 双击可用，离线运行。
- 页面结构 = Hero 开篇 + 若干章节（每章一个小实验）+ 总结；配 README。
- 单个课程固定四件套：`README.md` / `index.html` / `style.css` / `app.js`。
- 多课程时加首页（导航卡片、搜索筛选、localStorage 学习进度）+ `shared/` 共享样式。

## 2. 教学节奏（最重要，学科无关）

每章统一四步：

1. **自动演示**：进入章节即自动播放（IntersectionObserver 触发，`data-autodemo` + `dataset.done` 保证每章只播一次）
2. **状态栏逐步解说**：`aria-live="polite"` 状态栏用口语化文字配合动画推进
3. **「轮到你了」动手区**：`—— 轮到你了 👇 ——` 分隔，用户自由操作
4. **小结卡片**：章节底部 3 张 mini-card，各讲一个知识点

核心手法：
- **生活化比喻 + emoji 强化概念**：把抽象概念映射到日常事物。例：
  - 栈 = 🥞 一摞盘子、内存堆 = 🏬 仓库、函数调用 = 🍳 做饭流水线
  - 可类推：概率 = 🎲 掷骰子、电流 = 💧 水流、复利 = 🌱 滚雪球、供需 = ⚖️ 天平
- **让用户亲手制造现象**：不只看动画，要能亲手触发错误/边界情况（溢出崩溃、除零、越界、失衡……），印象最深
- **抽象概念可视化**：数字→便签、变量→盒子、公式→滑杆实时联动、不可见量→颜色/动画暗示
- **错误也教**：答错题附讲解 + 章节回链；做完给鼓励性评语
- **结尾总结**：一句话 motto + 复习回链 + 进阶彩蛋（指向更深入的主题）
- 内容基于公开资料整理，README 列参考来源

## 3. 视觉风格（style.css）

### 设计令牌（:root CSS 变量）
- 背景 `--bg: #f2f6fc`；正文 `--ink: #1b2a41`；弱化 `--muted: #5c6b82`
- **每个核心概念一种主题色 + soft 浅色背景**，全站一致。示例：
  - 橙 `#f97316` / `#fff3e6`、青 `#0d9488` / `#e6faf6`、紫 `#7c3aed` / `#f1ecfe`
  - 对错 `--ok: #16a34a` / `--bad: #dc2626`
- 圆角 `--radius: 20px`，柔和阴影 `--shadow: 0 10px 34px rgba(15,23,42,.08)`

### 组件规范
- 按钮 `.btn`：圆角 14px、min-height 48px、`:active` 缩放 .96；变体 primary/danger/ghost/sm/big
- 卡片：`.card` 大白卡；`.mini-card` 三列小结（`repeat(3,1fr)`）
- 章节头：胶囊编号标签（随章节主题变色）+ 大标题 + 目标句
- 演示卡片 `.demo-card`：左场景右控件两栏 grid；状态栏带色点；`.tip` 浅黄提示、`.warn` 浅红警告
- Hero：径向渐变背景 + 对比动画 + 渐变标题文字（background-clip: text）+ 自动循环动画

### 动效
- 进出用 `transform + opacity` 过渡，弹性曲线 `cubic-bezier(.34,1.4,.64,1)`
- 错误反馈：shake 抖动、红色闪烁 box-shadow
- **必须支持 `@media (prefers-reduced-motion: reduce)`**：动画压到 .01ms

### 响应式断点
- **900px**：双栏 → 单栏
- **640px**：触控布局（按钮全宽、表格单列、格子减列、输入框全宽）

## 4. 代码规范（app.js）

- 原生 JS 严格模式 `'use strict'`，零依赖；工具 `$ = querySelector`、`wait(ms)`
- **常量集中定义并与 CSS 保持一致**（如容量、尺寸魔数），必要时 `getComputedStyle` 读 CSS 变量
- 状态管理：数据存数组/对象 + `renderXxx()` 全量重绘 DOM
- **busy 标志防重入**：演示期间禁用该章节所有控件按钮，防止动画错乱
- 自动演示写成步骤数组 `{ msg, fn, delay, pause }`，async 函数顺序 await
- 动画类名驱动（entering/leaving/appear）+ `requestAnimationFrame` 双次触发过渡
- 危险实验（崩溃类效果）用全屏遮罩覆盖演示区，可一键恢复
- 测验模式：题目数组 `{ q, ans, why, link, linkTxt }`，答错带讲解和回链，进度圆点三态 + 计分 + 重玩

## 5. 无障碍与兼容

- `aria-live="polite"` 播报、`aria-label`、语义化标签、动态区域 `aria-busy`
- 触控友好：按钮 ≥ 44–48px、`-webkit-tap-highlight-color: transparent`
- iOS Safari：`backdrop-filter` 加 `-webkit-` 前缀、`viewport-fit=cover`
- 字体栈：`"PingFang SC", "HarmonyOS Sans SC", "Microsoft YaHei", "Noto Sans SC", system-ui`

## 6. 完成定义（DoD）

一个页面任务只有同时满足以下条件才算完成：

- [ ] 内容完整非占位页；至少一个核心实验可实际操作，所有按钮有有效行为
- [ ] 遵循「自动演示 → 解说 → 轮到你了 → 小结」节奏
- [ ] 动画有 busy 防重入；重置/重播后状态正确
- [ ] `file://` 离线可开，无框架、无 CDN、无外部资源
- [ ] 有 aria-live、键盘可操作、44–48px 触控目标、prefers-reduced-motion
- [ ] 900px / 640px 下无明显横向溢出
- [ ] README 含快速开始、实验说明、文件结构、参考资料、兼容性
- [ ] JS 通过 `node --check`；Playwright 验证通过；控制台无错误

推荐验证方式：`.verify/` 放 Playwright 脚本 —— 三端截图（1280×800 / 768×1024 / 390×844，窄屏另加 320px）+ 交互冒烟 + 控制台错误捕获 + 布局检查（横向溢出/越界/文本截断/触控尺寸）。命令示例：
`PLAYWRIGHT_BROWSERS_PATH=$PWD/browsers node verify-xxx.js`

## 7. 反模式（禁止）

- ❌ 用框架或外部 CDN 资源（必须零依赖可离线）
- ❌ 演示可被重复触发导致动画错乱（必须 busy 标志 + dataset.done）
- ❌ 纯文字灌输不给动手环节（必须有「轮到你了」）
- ❌ 忘写 prefers-reduced-motion、忘做 640px 触控布局
- ❌ JS 与 CSS 魔数不同步（常量要对齐）

## 8. 新学科上手清单

为某学科建第一个交互页面时的思考顺序：

1. 这个主题里**最反直觉 / 最容易误解**的 3–5 个点是什么？（它们就是章节）
2. 每个点对应什么**生活比喻**和 **emoji**？
3. 用户能**亲手做什么操作**？能制造什么「啊原来如此」的现象？
4. 各概念分别用什么**主题色**？
5. 结尾的 motto 和进阶彩蛋指向哪里？
