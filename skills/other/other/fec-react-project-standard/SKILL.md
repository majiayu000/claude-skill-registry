---
name: fec-react-project-standard
description: Use when designing or reviewing React + TypeScript project structure, feature/module boundaries, component architecture, hooks organization, routing composition, state/API/error/styling defaults, or repository-wide React conventions. Prefer narrower skills for forms, data fetching, tests, accessibility, virtualization, animation, or security deep dives; Chinese triggers include React 项目规范, React 组件架构.
---

# React 项目规范

适用于 React + TypeScript 仓库中的中大型模块建设、页面重构和工程结构设计。

## Purpose

为 React + TypeScript 项目提供工程结构、模块边界和默认实现约定，确保架构清晰、代码可维护。

## Procedure

本 skill 主要解决 React 工程任务“如何设计和落地”的问题，不重复声明基础编码底线。处理 React 工程化任务时，按以下顺序执行：

1. 识别仓库已有约定
   - 目录组织方式
   - 样式体系
   - 状态管理方案
   - 请求封装方式
   - 测试框架
   - UI 组件库 / 设计系统

2. 判断目标属于哪一层
   - 路由页面
   - 页面私有组件
   - feature 业务模块
   - 全局通用组件
   - hooks / services / stores / utils

3. 设计边界后再落代码
   - 哪些逻辑属于页面编排
   - 哪些逻辑属于 feature
   - 哪些逻辑应下沉为通用能力
   - 哪些状态应本地管理，哪些应交给 store / query / URL

4. 输出时补齐关键质量项
   - loading / error / empty / data 状态
   - 错误处理与重试
   - 类型约束
   - 关键测试入口
   - 必要的专项 skill 分流

## Detailed References

Load [references/react-project-details.md](references/react-project-details.md) when the task needs concrete React project structure, component patterns, Hooks, routing, state ownership, API layer shape, error handling, styling defaults, TypeScript conventions, or review checklists.

## Related Skills / Boundary

- `fec-form-handling` — React Hook Form、Zod、动态字段、文件上传和表单性能。
- `fec-data-fetching` — TanStack Query、server state、query key、mutation 和缓存失效。
- `fec-component-testing` / `fec-e2e-testing` — 组件契约测试或跨页用户路径测试。
- `fec-accessibility-check` / `fec-security-review` — 无障碍或安全专项深审。
- `fec-list-virtualization` / `fec-svg-animation` / `fec-canvas-threejs` — 性能或视觉专项实现。

## Constraints

- 默认遵守仓库现有全局规则和 React rule
- 若仓库已有明确目录结构、样式体系、状态管理或请求封装，优先沿用仓库约定
- 组件文件规模宜约 **300 行**内；逾 **500 行**或复杂度过高须拆分子组件、Hooks、utils、类型
- 禁止新增类组件（Error Boundary 用 `react-error-boundary` 等库）
- 禁止绕过模块出口，从 feature 深层路径导入
- 不要用 `useEffect + setState` 模拟本可直接计算的派生值
- 避免 prop drilling 过深却不考虑组合或局部封装

## Expected Output

- 组件边界清晰，pages/features/components 分层明确
- Props 类型完整且明确，无 `any` 滥用
- 可复用逻辑已提取为 hooks，loading/error/empty/data 状态齐全
- API 层具备类型约束和统一错误处理，状态管理符合就近原则
- 关键行为有测试覆盖，关键模块已用 `react-error-boundary` 包裹
- 超长列表已评估虚拟化，弹窗/复合组件具备键盘与焦点支持
- 先尊重仓库现状，再给推荐结构
- 给出必要的文件划分建议
- 必要时说明为什么这样分层
- 对新增模块，优先输出最小可落地结构，而不是一次性过度设计
- 对重构任务，优先保证可迁移性和风险可控
