---
name: vue3-state-management
description: Pinia 状态管理最佳实践：分域 store、actions 组织异步、状态规范化、持久化与调试。
---

# Vue 3 状态管理（Pinia）

此 skill 适用于用 Pinia 构建可维护的全局状态。

## 何时使用此 Skill

- 需要跨组件/跨页面共享状态（用户会话、权限、全局配置、购物车等）
- 需要可测试的异步流程（请求、缓存、乐观更新）
- 需要持久化（例如刷新保持登录态/过滤条件）

## 关键最佳实践

- **按领域拆分 store**：`useAuthStore`, `useCartStore` 等，避免“全局大 store”。
- **异步进 actions**：把请求、副作用放在 actions；组件只负责调用与展示状态。
- **派生状态用 getters**：避免重复计算与重复存储。
- **状态规范化**：列表/字典结构分离，减少更新成本。

## 常见反模式

- 把组件局部状态塞进 Pinia（导致 store 臃肿）
- store 里直接操作 DOM 或路由（耦合过高）
- actions 不处理 loading/error，导致 UI 很难统一展示

## 使用示例（提示语模板）

- “为 auth 模块建立 Pinia store：包含 user、token、isAuthenticated、login/logout/refresh actions，并严格 TS 类型。”
- “把页面里分散的 loading/error 状态迁移到 store，并提供统一的错误展示策略。”
