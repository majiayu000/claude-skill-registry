---
name: vue3-architecture
description: Vue 3 + TypeScript + Composition API 的工程化架构实践：组件边界、composables 抽取、目录组织与可维护性。
---

# Vue 3 架构

此 skill 用于构建可扩展的 Vue 3 应用：

- `<script setup lang="ts">` 作为默认
- 组件职责清晰：展示型 vs 容器型
- 逻辑沉淀到 composables（`useXxx`）

## 何时使用此 Skill

- 新建 Vue 3 项目结构（Vite + TS）
- 重构组件：拆分过大的组件、提取 composables
- 建立跨页面复用能力（表单、数据获取、权限、埋点等）

## 前置条件

- 遵守 `.github/instructions/vuejs3.instructions.md` 的规则（Composition API、TS、Pinia、测试、性能等）。

## 关键最佳实践

- **功能/领域分组**：按 feature/领域组织 `components/`, `composables/`, `stores/`, `api/`。
- **依赖方向**：页面/容器组件依赖展示组件；展示组件尽量纯净（props + emits + slots）。
- **composables 单一职责**：一个 composable 解决一个横切问题（如 `useFetch`, `useAuth`）。
- **副作用清理**：watch/事件监听/定时器在 `onUnmounted` 或 cleanup 中释放。

## 常见反模式

- 组件里同时做数据获取、权限、表单、渲染，难测难改
- 在多个组件重复同一段业务逻辑而不抽 composable
- 过度 provide/inject，导致依赖隐式且难追踪

## 使用示例（提示语模板）

- “把这个 800 行组件拆成容器 + 3 个展示组件 + 2 个 composables，并保持类型严格。”
- “为列表页提取一个 usePagination/useQueryParams composable，保证路由参数与 UI 状态同步。”
