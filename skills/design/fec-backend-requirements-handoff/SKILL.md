---
name: fec-backend-requirements-handoff
description: Use when frontend work needs to communicate data, action, state, permission, validation, or business-rule needs to backend teams without dictating endpoint design, field names, database shape, or implementation details; Chinese triggers include 前后端需求交接, 后端需求, API 需求澄清, 数据需求说明.
---

# 前后端需求交接

## Purpose

把前端页面和交互所需的数据、动作、状态和疑问整理成后端可讨论的需求说明。

## Procedure

1. 明确功能上下文
   - 说明页面、流程或组件是什么，面向哪类用户，以及用户完成任务的成功状态。
   - 如果已有设计稿、路由、用户故事或权限角色，先把它们作为事实来源。

2. 描述前端展示需求
   - 按屏幕或组件列出需要展示的信息、信息之间的关系、排序/过滤/分页需求和可见性规则。
   - 使用业务语言描述“需要展示什么”，不要提前规定 endpoint、字段名、DTO、数据库表或响应嵌套结构。

3. 描述用户动作和结果
   - 列出用户能执行的动作、期望结果、成功反馈、失败反馈和是否需要乐观更新。
   - 标出幂等性、撤销、确认、危险操作、批量操作或长任务进度等对 UI 有影响的行为。

4. 补齐状态和业务规则
   - 覆盖 loading、empty、error、partial、permission denied、expired、conflict、offline 和 retrying 等状态。
   - 记录影响 UI 的权限、生命周期、金额/时区/枚举、校验、可编辑条件和边界规则。

5. 输出讨论文档
   - 默认写到 `docs/backend-requirements/<feature-name>.md`；若仓库已有需求文档目录，沿用现有位置。
   - 文档包含 Context、Screens/Components、Data Needs、User Actions、UI States、Business Rules、Uncertainties、Questions for Backend 和 Decision Log。
   - 若用户只需要聊天回复，可以直接输出同样结构的 Markdown，不创建文件。

## Constraints

- 不替后端规定 URL、HTTP 方法、字段名、数据库 schema、缓存实现或服务拆分。
- 不把前端猜测写成事实；不确定的业务规则必须进入 Uncertainties 或 Questions。
- 不忽略错误、空态、权限和部分数据；这些状态决定接口协作质量。
- 不把内部错误栈、数据库字段或敏感实现细节要求暴露给 UI。
- 不与 API 集成流程重复：本 skill 描述需求，客户端边界、类型来源和错误映射实现应在后续实现阶段处理。

## Expected Output

产出一份前端视角的后端需求交接说明，清楚描述 UI 需要什么数据和行为、哪些规则仍需确认，以及后续前后端需要共同决定的问题。
