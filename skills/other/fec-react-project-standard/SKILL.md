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
   - 状态归属复杂时使用状态管理流程先做状态清单
   - DTO、公共 props 或泛型组件复杂时使用 TypeScript 类型安全流程先收敛类型契约

4. 输出时补齐关键质量项
   - loading / error / empty / data 状态
   - 错误处理与重试
   - 类型约束
   - 关键测试入口
   - 必要的专项 skill 分流
   - 依赖是否已存在于 `package.json`，缺失时先给安装命令再使用
   - 重型 UI 能力（动效、图表、3D、编辑器、地图）是否隔离为 leaf component 并按需加载
   - 图片、视频、字体等资源是否本地化、可缓存，并避免占位 URL 进入交付
   - 页面级 Error Boundary、模块级 fallback、API 错误映射和用户可恢复动作是否一致
   - Tailwind token/variant 或响应式布局需求是否应分流到对应专项 skill

## Detailed References

需要具体 React 项目结构、组件模式、Hooks、路由、状态归属、API 层形状、错误处理、样式默认值、TypeScript 约定或审查清单时，加载 [references/react-project-details.md](references/react-project-details.md)。

## Constraints

- 默认遵守仓库现有全局规则和 React rule
- 若仓库已有明确目录结构、样式体系、状态管理或请求封装，优先沿用仓库约定
- 组件文件规模宜约 **300 行**内；逾 **500 行**或复杂度过高须拆分子组件、Hooks、utils、类型
- 禁止新增类组件（Error Boundary 用 `react-error-boundary` 等库）
- 禁止绕过模块出口，从 feature 深层路径导入
- 不要用 `useEffect + setState` 模拟本可直接计算的派生值
- 避免 prop drilling 过深却不考虑组合或局部封装
- 不在通用页面组件里同步引入 GSAP、Three.js、Lottie、富文本编辑器或地图 SDK；需要时用动态导入、路由级分包或叶子组件隔离。
- 不在 React 组件中散落裸 `fetch`、API URL、token refresh 或上传流程；跨边界请求应收敛到 API 集成层。
- 不用 Error Boundary 处理普通 API 失败；请求错误应优先落到 loading/error/empty/data 状态和可恢复操作。

## Expected Output

- 组件边界清晰，pages/features/components 分层明确
- Props 类型完整且明确，无 `any` 滥用
- 可复用逻辑已提取为 hooks，loading/error/empty/data 状态齐全
- API 层具备类型约束和统一错误处理，状态管理符合就近原则
- URL 状态、服务端状态、表单状态和全局客户端状态边界明确
- 关键行为有测试覆盖，关键模块已用 `react-error-boundary` 包裹
- 超长列表已评估虚拟化，弹窗/复合组件具备键盘与焦点支持
- 先尊重仓库现状，再给推荐结构
- 给出必要的文件划分建议
- 必要时说明为什么这样分层
- 对新增模块，优先输出最小可落地结构，而不是一次性过度设计
- 对重构任务，优先保证可迁移性和风险可控
