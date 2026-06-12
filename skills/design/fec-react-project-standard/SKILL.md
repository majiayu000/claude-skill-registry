---
name: fec-react-project-standard
description: 用于设计或审查 React + TypeScript 项目结构、feature/module 边界、组件架构、hooks 组织、路由组合、状态/API/错误/样式默认约定或仓库级 React 规范。表单、数据获取、测试、无障碍、虚拟列表、动画或安全深挖优先使用更窄的 skill；中文触发词包括 React 项目规范、React 组件架构。
---

# React 项目规范

适用于 React + TypeScript 仓库中的中大型模块建设、页面重构和工程结构设计。

## 用途

为 React + TypeScript 项目提供工程结构、模块边界和默认实现约定，确保架构清晰、代码可维护。

## 流程

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
   - DTO、公共 props、泛型组件或 `tsconfig` 边界复杂时，先使用 TypeScript 项目规范流程收敛跨框架类型契约

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
   - 对明显架构性能风险做轻量筛查，如重型依赖边界、过宽 Context、高频派生值和懒加载 fallback；需要指标证据时进入性能优化 workflow

## 详细参考

按需要加载更细的参考文件：

- 项目目录、组件分层、组件边界和组件目录建议：加载 [references/react-project-structure.md](references/react-project-structure.md)。
- 组件模式、Hooks、路由、状态归属、API 层、错误处理和 Suspense/懒加载：加载 [references/react-runtime-patterns.md](references/react-runtime-patterns.md)。
- 样式、注释、TypeScript、测试、反模式和输出检查清单：加载 [references/react-quality-patterns.md](references/react-quality-patterns.md)。
- React 项目规范层面的轻量性能约定：加载 [references/react-performance-patterns.md](references/react-performance-patterns.md)。

## 约束

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
- 不把 React 性能建议写成无证据的全局 memo 化；先定位请求瀑布、bundle 边界、重复渲染或 effect 误用。

## 预期输出

- 组件边界清晰，pages/features/components 分层明确
- Props 类型完整且明确；复杂公共类型或外部数据收窄已分流到 TypeScript 项目规范流程
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
- 对性能相关 React 变更，说明触发的风险类别、证据来源和验证命令
