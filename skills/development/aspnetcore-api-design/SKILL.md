---
name: aspnetcore-api-design
description: ASP.NET Core API 设计与实现最佳实践：错误处理（ProblemDetails/RFC 7807）、一致响应、版本化、可观测性与安全。
---

# ASP.NET Core API 设计

此 skill 聚焦“对外 API 的契约质量”，让接口具备：

- 一致的错误模型（ProblemDetails / RFC 7807）
- 可测试（集成测试友好）
- 可观测（traceId/correlationId）
- 可演进（版本化、向后兼容）

## 何时使用此 Skill

- 新增/重构 ASP.NET Core Minimal APIs 或 Controllers API
- 统一异常处理、状态码页（4xx/5xx）与错误响应体
- 设计 API 版本化、OpenAPI/Swagger 文档与响应约定
- 设计认证授权策略（JWT / OIDC / Entra ID 等）

## 关键最佳实践（含权威依据）

### 1) 统一错误响应：ProblemDetails

- 推荐使用 `AddProblemDetails()` + `UseExceptionHandler()` + `UseStatusCodePages()` 生成标准化 ProblemDetails。
- 生产环境不要回传敏感错误信息。

参考（Microsoft Learn）：

- Handle errors in ASP.NET Core APIs（ProblemDetails / UseExceptionHandler 示例）
- Handle errors in ASP.NET Core（ProblemDetails service、IProblemDetailsService）

### 2) 少用异常做控制流

异常应该是“非常规/不可预期”的分支；热路径避免 throw/catch。

参考：ASP.NET Core Best Practices（Minimize exceptions）。

### 3) 契约优先

- 对外 DTO 与内部领域对象隔离（DTO ≠ Entity）
- OpenAPI 文档与响应类型（包含错误响应）同步维护

### 4) 高性能 I/O 与 负载优化

- **分页是标配**：返回集合时始终使用分页（PageSize/PageIndex），对于大列表优先使用 `IAsyncEnumerable<T>` 进行流式返回。
- **异步读取 Body**：始终使用 `ReadFormAsync` 替代 `Request.Form`；对 Request Stream 使用异步 API。
- **响应优化**：生产环境建议开启响应压缩（Response Compression）并对前端资源进行合并与压缩（Bundling & Minification）。
- **HttpClient 复用**：必须通过 `IHttpClientFactory` 管理连接池。

## 常见模式

- **输入验证**：在应用层验证 DTO，返回 400 + ProblemDetails
- **全局异常处理**：异常 → 500 + ProblemDetails（必要时映射业务异常为 4xx）
- **一致响应头**：traceId/correlationId 贯穿日志与错误响应

## 常见反模式

- 每个 Controller/Endpoint 自己 try/catch 拼接错误 JSON
- 错误码散落，且同一业务错误不同 endpoint 返回不同格式
- 返回 `BadRequest()` 但没有 body，前端无法精确展示

## 使用示例（提示语模板）

- “为该 API 增加全局异常处理与 ProblemDetails（Minimal API 方案），并保证 404/400 也有一致的 ProblemDetails body。”
- “为某业务异常映射到 409/422，并保持 ProblemDetails 的 type/title/detail 语义一致。”
