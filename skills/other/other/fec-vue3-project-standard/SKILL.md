---
name: fec-vue3-project-standard
description: Use when designing or reviewing Vue 3 + TypeScript project structure, SFC/component boundaries, composables organization, route composition, Pinia ownership, API/error/styling defaults, directives, or repository-wide Vue conventions. Prefer narrower skills for forms, data fetching, tests, accessibility, virtualization, animation, or security deep dives; Chinese triggers include Vue 3 项目规范, Vue 组件架构.
---

# Vue 3 项目规范

适用于使用 Vue 3 + TypeScript 的仓库。

## Purpose

为 Vue 3 + TypeScript 项目提供工程结构、组件边界、Composables 和默认实现约定，确保约定式开发和类型安全。

## Procedure

1. 识别仓库已有 Vue 约定：目录、路由、Pinia、请求层、样式体系、组件库和测试框架。
2. 划分页面、业务组件、通用组件、composables、stores、services 和 utils 的边界。
3. 优先沿用 `<script setup lang="ts">`、组合式 API 和仓库现有自动导入/模块出口约定。
4. 输出时补齐状态归属、API 层、错误处理、样式隔离和专项 skill 分流。

## Detailed References

Load [references/vue3-project-details.md](references/vue3-project-details.md) when the task needs concrete Vue 3 project structure, component patterns, Composables, slots, Provide/Inject, routing, Pinia, API layer, error handling, directives, styling, TypeScript, testing, performance, or review checklists.

## Constraints

- 使用 `<script setup lang="ts">`，禁止使用 Options API 新增组件
- 组件文件规模宜约 **300 行**内；逾 **500 行**或复杂度过高须拆子组件与 Composables
- Props / Emits 必须使用 TypeScript interface 定义，禁止使用 `any`
- Composable 返回 `readonly` 引用，防止外部意外修改
- 不要在 store 中存放 UI 临时状态（modal 开关、表单输入等）
- 服务端数据优先用请求库管理，而非手动存入 Pinia
- 避免在 `v-for` 中使用 `v-if`（提取为 computed 过滤）
- 禁止直接从 feature 内部深层路径导入，绕过 `index.ts`

## Expected Output

- 组件使用 `<script setup lang="ts">`，Props / Emits 类型完整
- 可复用逻辑已提取到 composable，返回 `readonly` 引用
- Loading / Error / Empty / Data 状态均已处理
- 路由组件使用动态 import 加载，状态管理符合就近原则
- API 调用有类型约束和统一错误处理
- 样式使用 scoped 隔离，关键行为有测试覆盖
- 文件结构与项目约定一致（pages / features / components 分离）
