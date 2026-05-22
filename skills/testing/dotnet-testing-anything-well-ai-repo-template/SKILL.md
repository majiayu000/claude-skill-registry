---
name: dotnet-testing
description: .NET 测试策略与落地：领域单测、应用层单测、ASP.NET Core 集成测试（WebApplicationFactory/TestServer）、鉴权 mock。
---

# .NET 测试

此 skill 用于建立“分层可测试性”与“可回归的质量门槛”。

## 何时使用此 Skill

- 为领域模型/应用服务补齐单元测试
- 为 ASP.NET Core API 增加集成测试（真实管道 + HttpClient）
- 需要在测试里替换数据库、注入 fake 外部依赖、mock 认证

## 关键最佳实践（含权威依据）

### 1) 集成测试首选 WebApplicationFactory

- 使用 `WebApplicationFactory<TEntryPoint>` 启动 SUT，并用 `CreateClient()` 发 HTTP 请求。
- Minimal API 场景如果 `Program` 是隐式 internal，可在 `Program.cs` 增加：`public partial class Program { }` 以便测试项目引用。

参考（Microsoft Learn）：

- Integration tests in ASP.NET Core（WebApplicationFactory、ContentRoot 推断、mock authentication）
- Test ASP.NET Core MVC apps（建议测试 host 尽量贴近生产 host）

### 2) 测试命名与风格一致

- 参考仓库 DDD 指令：`MethodName_Condition_ExpectedResult()` 命名模式。
- 不要写 Arrange/Act/Assert 注释（遵循仓库 C# 指令）。

### 3) Mock 认证/授权

- 通过 `ConfigureTestServices` 注入测试用 AuthenticationHandler，确保 scheme 与应用一致。

## 常见反模式

- 只测 Controller，不测领域规则（导致业务规则回归风险高）
- 集成测试依赖真实外部服务、不可重复
- 测试用例共享状态导致互相污染

## 使用示例（提示语模板）

- “为该 Minimal API 添加集成测试：覆盖 200/400/401，并用 WebApplicationFactory 替换为 InMemory 数据库。”
- “为该聚合的不变量写单测，命名遵循 MethodName_Condition_ExpectedResult。”
