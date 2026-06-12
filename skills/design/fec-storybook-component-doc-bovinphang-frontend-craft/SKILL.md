---
name: fec-storybook-component-doc
description: 用于设置或审查 Storybook 组件文档、设计系统展示、隔离组件状态预览、stories、addons、decorators、MDX 文档、组件状态交互检查、视觉基线或 Chromatic。真实浏览器跨页面旅程或更广覆盖规划优先选择对应测试工作流；中文触发词包括 Storybook、组件文档、Design System、视觉回归。
---

# Storybook 组件文档化

## 用途

为 UI 组件建立文档化、设计系统展示和隔离状态预览环境；交互与视觉测试只覆盖 Storybook 场景内的组件状态。

## 流程

1. 初始化或识别现有 Storybook 配置，沿用项目框架适配器、stories glob、主题和构建命令。
2. 每个组件的 Story 覆盖默认态、主要变体、尺寸、语义 tone、disabled、loading、error、empty、selected、invalid 和关键边缘状态。
3. 依赖 Router、Store、i18n、ThemeProvider 的组件用 decorators 包裹，不在 Story 中复制应用入口。
4. 复杂组件用 MDX 补充使用说明、Props、slots/children、variant 矩阵、状态示例、可访问性要求和源码展示。
5. 需要自动化时接入 interaction tests、addon-a11y、Chromatic 或 Storybook Test Runner；这些能力服务于组件文档和设计系统展示，不承接跨页业务旅程。
6. 设计系统组件应记录 token 来源、Tailwind/class 变体、暗色模式、响应式尺寸和不支持的组合，避免消费者靠猜测拼装。

## 详细参考

- 需要 `main.ts`、`preview.ts`、stories、decorators、MDX、交互测试和视觉回归示例时，加载 [references/story-patterns.md](references/story-patterns.md)。

## 约束

- Story 需随组件 prop 变更同步更新。
- Provider 依赖必须通过 decorator 补齐。
- Storybook 构建产物 `storybook-static/` 不应提交到 Git。
- Storybook 用于开发和组件文档，不替代生产页面 SEO。
- Storybook 视觉基线用于组件状态；跨页面截图和真实路由流程分流到 E2E workflow。
- 大型组件库需控制 stories glob 和 addon 开销。
- 不用 Storybook 隐藏组件 API 问题；若变体组合爆炸，应先收敛组件职责或拆分组件。

## 预期输出

可交互的组件文档和设计系统展示站点，每个组件状态都有隔离预览，Props 表格可生成，关键 Storybook 场景有可选 play 测试或视觉回归基线。
