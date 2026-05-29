---
name: fec-storybook-component-doc
description: Use when setting up or reviewing Storybook component documentation, stories, addons, decorators, MDX docs, isolated component development, component-state interaction tests, visual baselines, Chromatic, or design system documentation. For real-browser cross-page journeys or broader coverage planning, choose the matching testing workflow first; Chinese triggers include Storybook, 组件文档, Design System, 视觉回归.
---

# Storybook 组件文档化

## Purpose

为 UI 组件建立隔离开发、状态预览和可交互文档环境。

## Procedure

1. 初始化或识别现有 Storybook 配置，沿用项目框架适配器、stories glob、主题和构建命令。
2. 每个组件的 Story 覆盖默认态、主要变体、disabled、loading、error 和关键边缘状态。
3. 依赖 Router、Store、i18n、ThemeProvider 的组件用 decorators 包裹，不在 Story 中复制应用入口。
4. 复杂组件用 MDX 补充使用说明、Props、状态示例和源码展示。
5. 需要自动化时接入 interaction tests、addon-a11y、Chromatic 或 Storybook Test Runner；仅覆盖组件状态和文档场景，不承接跨页业务旅程。

## Detailed References

- Load [references/story-patterns.md](references/story-patterns.md) for `main.ts`, `preview.ts`, stories, decorators, MDX, interaction tests, and visual regression examples.

## Constraints

- Story 需随组件 prop 变更同步更新。
- Provider 依赖必须通过 decorator 补齐。
- Storybook 构建产物 `storybook-static/` 不应提交到 Git。
- Storybook 用于开发和组件文档，不替代生产页面 SEO。
- Storybook 视觉基线用于组件状态；跨页面截图和真实路由流程分流到 E2E workflow。
- 大型组件库需控制 stories glob 和 addon 开销。

## Expected Output

可交互的组件文档站点，每个组件状态都有可视化预览，Props 表格可生成，关键交互有可选 play 测试或视觉回归基线。
