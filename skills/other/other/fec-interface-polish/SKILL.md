---
name: fec-interface-polish
description: Use when improving UI polish details such as spacing, typography, radius, shadows, borders, icon alignment, hit areas, text wrapping, tabular numbers, transitions, hover/active/focus states, or visual QA. Use fec-ui-design-direction first when the product design direction is unclear; Chinese triggers include UI 打磨, 界面微调, 视觉还原, 交互状态.
---

# 界面质感打磨

适用于对已有 UI 做细节级 polish、视觉 QA 或交互状态补齐。

## Purpose

用可执行的设计工程规则提升界面的精致度和稳定感。

## Procedure

1. 建立检查清单
   - 先扫描目标文件中的 spacing、radius、border、shadow、transition、focus、hover、active、disabled。
   - 记录只影响目标界面的局部问题，避免顺手重构无关样式系统。

2. 修正几何与视觉关系
   - 嵌套圆角遵循“外层圆角约等于内层圆角 + 间距”的光学关系。
   - 非对称图标、播放三角、箭头、星标等需要按视觉中心微调。
   - 图像边缘容易融入背景时，用中性 alpha 内描边，而不是品牌色描边。

3. 稳定文本与数字
   - 标题和短文本可使用 `text-wrap: balance` 或 `text-wrap: pretty`。
   - 表格、价格、计数器、计时器使用 `font-variant-numeric: tabular-nums`。
   - 按钮和紧凑控件的最长文案必须换行、缩放或改布局，不允许溢出。

4. 明确交互状态
   - 小控件点击区域至少 40x40px，空间允许时优先 44x44px。
   - focus ring 用于键盘定位，hover/active 用于鼠标反馈，disabled 不只靠透明度表达。
   - 弹层、菜单、抽屉需要进入、退出和焦点恢复状态。

5. 收敛动效
   - 优先使用可中断的 CSS transition；一次性入场或 loading 才使用 keyframes。
   - 只声明实际变化的属性，禁止 `transition: all` 和 `will-change: all`。
   - 退出动效应比进入动效更短、更安静，并尊重 `prefers-reduced-motion`。

## Constraints

- 不为了质感添加大面积装饰、模糊光斑或无语义渐变。
- 不把所有元素都加阴影；边框用于分隔，阴影用于层级。
- 不用负 letter-spacing 或视口宽度驱动字号。
- 不让扩展命中区域相互重叠。
- 不在全局样式中粗暴覆盖第三方组件，除非该项目已有同类约定。

## Expected Output

输出应说明修正了哪些 polish 维度，并给出文件、属性或组件状态。复核时界面应无文本溢出、无跳动布局、状态反馈完整，动效克制且可访问。

## Related Skills / Boundary

- `fec-ui-design-direction` — 产品语气、首屏结构、视觉方向不清时先使用。
- `fec-accessibility-check` — 焦点管理、键盘交互和 ARIA 需要专项审查时使用。
- `fec-frontend-code-review` — 当问题跨越架构、类型、渲染性能和样式时使用。
