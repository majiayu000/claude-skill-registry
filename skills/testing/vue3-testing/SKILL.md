---
name: vue3-testing
description: Vue 3 测试体系：Vitest + Vue Test Utils 单测，Playwright E2E；关注行为而非实现。
---

# Vue 3 测试

此 skill 用于建立前端的“快测 + 回归保障”。

## 何时使用此 Skill

- 为组件/composable 编写单元测试（Vitest）
- 为路由/Pinia 集成行为编写测试
- 编写端到端测试（Playwright），覆盖关键用户流

## 关键最佳实践

- **单测关注行为**：断言用户可见结果，而非内部实现细节。
- **mock 外部依赖**：API 调用、路由、Pinia 插件等。
- **E2E 覆盖关键路径**：登录、下单、提交表单等。

## 与本仓库已有 skill 的配合

- 端到端自动化优先复用：`webapp-testing`（Playwright 工具与调试能力）。

## 常见反模式

- 只测快照，不测交互与状态变化
- 测试依赖真实后端，导致不稳定
- 断言选择器依赖脆弱 CSS class（建议 data-testid 或 role）

## 使用示例（提示语模板）

- “为该组件补单测：覆盖 props、emits、slot 渲染，以及点击后的 UI 状态变化。”
- “为登录流程写 Playwright E2E：输入账号密码、提交、等待跳转、验证导航栏用户名展示。”
