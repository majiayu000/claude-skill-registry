---
name: fec-tailwind-design-system
description: 用于设计、实现或审查 Tailwind CSS 设计系统、Token 映射、主题扩展、工具类治理、组件变体、暗色模式、响应式工具、safelist 或可维护的 class 组合；中文触发词包括 Tailwind、设计 Token、组件变体、暗色模式、class 管理。
---

# Tailwind 设计系统

适用于用 Tailwind CSS 承载产品设计系统、组件变体和主题规则的前端任务。需要具体配置、variant、class 组织和迁移细节时加载 [references/tailwind-system-patterns.md](references/tailwind-system-patterns.md)。

## 用途

让 Tailwind 项目中的 token、主题、组件变体和响应式样式可维护，而不是把一次性 utility class 散落到业务代码里。

## 流程

1. 识别现状：确认 Tailwind 版本、配置位置、暗色模式策略、组件库、CSS 变量、设计 token 和 class 合并工具。
2. 建立 token 边界：颜色、间距、圆角、阴影、字体、z-index 和断点优先从项目 token 或 `theme.extend` 派生。
3. 设计组件变体：按钮、输入框、卡片、弹窗、表格等基础组件用集中 variant API 表达尺寸、语义、状态和密度。
4. 控制 class 复杂度：重复组合沉淀为组件、slot、variant 或局部 helper；不要把长 class 字符串复制到多个页面。
5. 处理主题和暗色模式：明确 `class`、`data-theme` 或 CSS 变量方案，避免首次渲染闪烁和对比度回归。
6. 接入响应式：移动优先组织 utility；复杂布局交给响应式布局工作流，不要只靠堆叠断点前缀碰运气。
7. 验证样式结果：检查 hover、active、focus-visible、disabled、loading、selected、invalid、dark 和不同断点。

## 约束

- 不把 Tailwind class 当作设计系统本身；真正的系统是 token、组件 API、状态矩阵和使用约束。
- 不为单个页面随意扩展全局 token；新增 token 必须有语义名称和复用场景。
- 不使用拼接的动态 class 破坏构建扫描；必要时使用 safelist、映射表或 variant 工具。
- 不在组件外部覆盖基础组件内部结构来实现变体。
- 不让暗色模式只靠反色；状态色、边框、阴影、图表和图片都要重新检查。

## 预期输出

输出 Tailwind token 映射、主题配置边界、组件 variant 设计、class 复用策略、暗色模式和响应式验证结果。完成后样式应能被项目组件复用、可搜索、可测试，并与设计系统规则一致。
