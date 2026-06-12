---
name: fec-vue3-project-standard
description: 用于设计或审查 Vue 3 + TypeScript 项目结构、SFC/组件边界、composables 组织、路由组合、Pinia 归属、API/错误/样式默认约定、directives 或仓库级 Vue 规范。表单、数据获取、测试、无障碍、虚拟列表、动画或安全深挖优先使用更窄的 skill；中文触发词包括 Vue 3 项目规范、Vue 组件架构。
---

# Vue 3 项目规范

适用于使用 Vue 3 + TypeScript 的仓库。

## 用途

为 Vue 3 + TypeScript 项目提供工程结构、组件边界、Composables 和默认实现约定，确保约定式开发和类型安全。

## 流程

1. 识别仓库已有 Vue 约定：目录、路由、Pinia、请求层、样式体系、组件库和测试框架。
2. 划分页面、业务组件、通用组件、composables、stores、services 和 utils 的边界。
3. 优先沿用 `<script setup lang="ts">`、组合式 API 和仓库现有自动导入/模块出口约定。
4. 输出时补齐状态归属、API 层、错误处理、样式隔离和专项 skill 分流。
5. 页面和模块要有可恢复错误 UI；全局 `errorHandler`、`onErrorCaptured`、请求错误映射和路由错误页分工明确。
6. Tailwind token/variant 或响应式布局需求应分流到对应专项 skill，避免把样式系统规则塞进 Vue 组件规范。
7. 状态归属复杂时先做状态清单；DTO、公共 props、泛型 composable 或 `tsconfig` 边界复杂时，先使用 TypeScript 项目规范流程收敛跨框架类型契约。
8. 设计可复用 composable 时明确输入是否支持 plain value、ref、computed 或 getter；测试 Vue 组件时覆盖 Pinia、Router、Teleport、Suspense 和 async setup 的常见边界。

## 详细参考

按需要加载更细的参考文件：

- 项目目录、组件分层、组件规范、注释和 TypeScript：加载 [references/vue3-project-structure.md](references/vue3-project-structure.md)。
- Composables、slots、Provide/Inject 和路由组织：加载 [references/vue3-composables-routing.md](references/vue3-composables-routing.md)。
- Pinia、API 层、错误处理、指令、样式、测试、反模式和输出检查清单：加载 [references/vue3-state-api-quality.md](references/vue3-state-api-quality.md)。
- Vue 项目规范层面的轻量性能约定：加载 [references/vue3-performance-patterns.md](references/vue3-performance-patterns.md)。

## 约束

- 使用 `<script setup lang="ts">`，禁止使用 Options API 新增组件
- 组件文件规模宜约 **300 行**内；逾 **500 行**或复杂度过高须拆子组件与 Composables
- Props / Emits 必须使用 TypeScript interface 定义，禁止使用 `any`
- Composable 返回 `readonly` 引用，防止外部意外修改
- 不要在 store 中存放 UI 临时状态（modal 开关、表单输入等）
- 服务端数据优先用请求库管理，而非手动存入 Pinia
- 避免在 `v-for` 中使用 `v-if`（提取为 computed 过滤）
- 禁止直接从 feature 内部深层路径导入，绕过 `index.ts`
- 不用全局错误处理吞掉组件内可恢复的 API、表单或权限错误。
- 不把函数型参数误当 getter 自动调用；composable 参数若可能是回调，应避免使用 getter 型输入约定。
- 不依赖快照作为 Vue 组件唯一断言；异步组件、Teleport 和 Pinia 场景要有用户可见行为断言。

## 预期输出

- 组件使用 `<script setup lang="ts">`，Props / Emits 类型完整
- 可复用逻辑已提取到 composable，返回 `readonly` 引用
- Loading / Error / Empty / Data 状态均已处理
- 路由组件使用动态 import 加载，状态管理符合就近原则
- URL 状态、服务端状态、表单状态和 Pinia 全局状态边界明确
- API 调用有类型约束和统一错误处理
- 样式使用 scoped 隔离，关键行为有测试覆盖
- 文件结构与项目约定一致（pages / features / components 分离）
- 可复用 composable 的输入响应性、Pinia/Router 边界和异步组件测试策略已说明
