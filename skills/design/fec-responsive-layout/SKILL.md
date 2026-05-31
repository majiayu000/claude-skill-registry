---
name: fec-responsive-layout
description: Use when designing, implementing, or reviewing responsive frontend layouts, mobile-first breakpoints, container queries, fluid grids, data-dense tables, touch targets, safe areas, orientation changes, viewport overflow, or cross-device UI behavior; Chinese triggers include 响应式布局, 移动端适配, 断点, 容器查询, 横竖屏, 触摸目标.
---

# 响应式布局

适用于需要让页面、工具界面、表格、仪表盘或组件在多设备上稳定工作的前端任务。需要布局模式和检查清单时加载 [references/responsive-layout-patterns.md](references/responsive-layout-patterns.md)。

## Purpose

用内容优先、移动优先和容器感知的方式设计响应式布局，避免只靠固定断点修补溢出。

## Procedure

1. 明确信息优先级：小屏先保留核心任务、关键操作和反馈；次要信息折叠、延后或移入详情层。
2. 选择布局策略：简单页面用 mobile-first 断点；嵌套组件、卡片网格和侧栏优先考虑 container query。
3. 设计流式尺寸：用 `minmax()`、`clamp()`、`aspect-ratio`、`max-width`、`min-width: 0` 和稳定网格轨道控制伸缩。
4. 处理数据密集界面：表格、列表、看板和编辑器需要明确横向滚动、列优先级、冻结列或移动端摘要视图。
5. 保证触摸与键盘：触摸目标、焦点路径、hover 替代、虚拟键盘、安全区域和横竖屏切换都要复核。
6. 关联性能与资源：移动端减少首屏大图、重型图表、同步动画和不必要列渲染。
7. 验证断点之间：检查 375px、768px、1024px、1440px，以及断点中间值是否溢出、遮挡或跳变。

## Constraints

- 不把桌面版缩小当作移动端设计。
- 不让关键功能只依赖 hover 或宽屏侧栏。
- 不用固定高度掩盖内容变化；需要固定格式时用稳定约束和可滚动区域。
- 不用 viewport 字体缩放替代真实排版层级。
- 不让移动端横向溢出成为默认解决方案；只有数据表、画布或编辑器等明确场景可以局部横滚。

## Expected Output

输出响应式信息优先级、断点或容器策略、关键组件布局模式、触摸/键盘要求、数据密集区域处理方案和验证结果。完成后页面在常见视口和输入方式下不溢出、不遮挡、可操作。
