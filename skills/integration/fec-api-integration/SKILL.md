---
name: fec-api-integration
description: Use when designing, implementing, or reviewing frontend-to-backend API integration, typed API clients, REST/tRPC/OpenAPI client choices, auth refresh, API error mapping, upload flows, SSE/WebSocket/polling choices, CORS-facing frontend behavior, or cross-boundary loading/error states. Do not use for backend-only service architecture or TanStack Query cache policy alone; Chinese triggers include API 集成, 前后端联调, typed API client, 接口错误处理, SSE, WebSocket.
---

# API 集成

适用于前端与后端边界的类型、错误、鉴权、上传、实时通信和用户状态设计。需要具体代码模式时加载 [integration-patterns.md](references/integration-patterns.md)。

## Purpose

规范前端 API 集成边界，让请求、错误、鉴权和实时数据可维护。

## Procedure

1. 明确接口所有权
   - 同团队 TypeScript 全栈可考虑 tRPC 或共享 schema。
   - 多语言或多消费者 API 优先 OpenAPI/GraphQL codegen。
   - 小型内部应用可用 typed fetch wrapper，但类型必须集中维护。
   - 不在组件里散落 `fetch`、URL、header、错误解析和 token 逻辑。
   - 公共接口需要明确版本、兼容窗口、废弃字段策略和调用方范围。

2. 建立客户端边界
   - 用一个 API client 处理 base URL、credentials、JSON 解析、超时、取消和统一错误。
   - 环境变量只读取公开前缀，私密 token 不进入客户端 bundle。
   - 组件只消费 domain 函数或 query/mutation hook，不直接拼接接口路径。
   - 204、空响应、非 JSON 错误和网络断开要有明确行为。
   - TypeScript contract 必须覆盖请求、响应、错误形状和分页/游标元数据。

3. 映射用户可理解的错误
   - 401：刷新失败后引导登录。
   - 403：说明权限不足，不重复重试。
   - 404：展示缺失状态或返回上级入口。
   - 409：提示冲突和下一步操作。
   - 422：映射字段级错误。
   - 429/5xx/网络错误：允许退避重试或展示稍后再试。
   - 未识别错误要落到统一 fallback，不把原始后端异常暴露给用户。
   - 所有错误都应归一到用户可恢复动作：重试、重新登录、修改输入、返回上级、联系支持或稍后再试。
   - 错误对象要保留面向日志的 trace id / request id，但 UI 不暴露内部堆栈、SQL、服务名或敏感字段。

4. 管理接口演进
   - 兼容新增字段；删除或改名字段必须走迁移期、适配层或双写/双读策略。
   - 用 schema、类型生成物或 contract test 捕捉破坏性变更。
   - 对前后端协作项记录状态码、错误码、幂等性、重试语义和时区/金额/枚举规则。

5. 处理鉴权刷新
   - Access token 生命周期短，refresh 优先放在 httpOnly cookie 或服务端会话。
   - 401 后只允许单次刷新队列，避免多个请求同时刷新。
   - 刷新失败要清理本地身份状态并跳转登录。
   - 不把 bearer token 放在 URL、localStorage 或日志里。

6. 选择上传与实时方案
   - 小文件可用 multipart；大文件优先预签名直传或分片上传。
   - 只需要服务端推送时用 SSE；双向协作、聊天或多人状态用 WebSocket。
   - 简单状态刷新、低频任务进度可用 polling，并设置停止条件。
   - 上传和实时连接都需要取消、重连、超时和错误 UI。

7. 验证集成质量
   - 检查 loading、empty、error、unauthorized、offline、retrying 状态。
   - 用浏览器网络面板确认 base URL、credentials、CORS 和状态码行为。
   - 用 mock 或测试服务覆盖 401、403、422、500、断网和取消请求。
   - 确认客户端 bundle 不包含私密环境变量、服务端密钥或内部地址。
   - 对关键 API client 行为补最小测试，证明超时、取消、错误映射和刷新队列可预期。
   - 验证错误边界与请求层协作：渲染异常进 Error Boundary，请求失败进可恢复 UI，不互相吞掉。

## Constraints

- 不在页面组件中直接管理 token refresh、错误格式解析或重试策略。
- 不对 4xx 业务错误做盲目自动重试。
- 不把后端异常栈、内部错误码或原始 SQL/服务名暴露给用户。
- 不用 localStorage 存储高价值 token；若遗留系统无法避免，必须联动安全审查。
- 不用 WebSocket 替代简单轮询，也不用轮询实现高频双向协作。
- 不让上传经过 API 服务器转发大文件，除非有明确合规或扫描需求。
- 不在公共接口里直接暴露临时字段、数据库字段名或后端内部错误结构。

## Expected Output

输出应包含 API client 边界、接口类型来源、错误映射、鉴权刷新策略、上传/实时方案和验证结果。完成后组件不散落请求细节，用户状态完整，失败场景可恢复，客户端不会泄露服务端密钥。
