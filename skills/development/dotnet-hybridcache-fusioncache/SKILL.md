---
name: dotnet-hybridcache-fusioncache
description: .NET HybridCache 与 FusionCache 的 L1/L2 多级缓存实践。
---

# HybridCache + FusionCache (L1/L2)

## 1. 选型指南

- **HybridCache (原生)**：适用于标准 .NET 9+ 项目，提供统一抽象、Stampede protection 和 Tag 失效。
- **FusionCache**：适用于对容错要求极高（Fail-safe）、倾向于软负载均衡或快速响应（Timeouts）的场景。
- **推荐方案**：业务层依赖 `HybridCache` 接口，DI 中使用 `AddFusionCache().AsHybridCache()`。

## 2. 核心指令 (Directives)

- **命名规范**：Key 格式必须为 `"{domain}:{entity}:{id/slug}"`。
- **多节点一致性**：多实例部署**必须**配置 Backplane (Redis/NATS)，禁止只配 L2 而忽略 L1 失效广播。
- **序列化防护**：必须显式注册 `IFusionCacheSerializer`；Redis 下推荐 `FusionCacheSystemTextJsonSerializer`。
- **安全性**：禁止将未处理的用户输入直接用于缓存 Key；敏感对象缓存前需考虑 DTO 转换。
- **不可变性**：缓存对象应设为 `sealed` 且属性只读，避免对取出对象进行原地修改。

## 3. 配置配方 (Recipes)

### A. 基础 HybridCache (Redis)

```csharp
builder.Services.AddHybridCache(options => {
    options.DefaultEntryOptions = new() { Expiration = TimeSpan.FromHours(1) };
});
builder.Services.AddStackExchangeRedisCache(o => o.Configuration = "redis_connection");
```

### B. 高韧性 FusionCache (Backplane + Fail-safe)

```csharp
builder.Services.AddFusionCache()
    .WithDefaultOptions(o => {
        o.Duration = TimeSpan.FromMinutes(5);
        o.IsFailSafeEnabled = true;
        o.FactorySoftTimeout = TimeSpan.FromMilliseconds(100);
    })
    .WithSerializer(new FusionCacheSystemTextJsonSerializer())
    .WithDistributedCache(new RedisCache(...))
    .WithBackplane(new RedisBackplane(...));
```

### C. 桥接模式 (HybridCache API + FusionCache Engine)

```csharp
builder.Services.AddFusionCache().AsHybridCache();
```

## 4. 严禁行为 (Anti-Patterns)

- **❌ 孤立 L2**：配置分布式缓存却不配置 Backplane 同步 L1（导致各节点数据不一致）。
- **❌ 侧漏修改**：修改从缓存取出的引用对象（引发内存并发安全性问题）。
- **❌ 盲目缓存**：在频繁变动且无热点的 Key 上使用 L2（增加网络 IO 负担）。
- **❌ 忽略取消令牌**：在异步方法中调用 `GetOrCreateAsync` 却不传递 `CancellationToken`。

## 5. 提示词示例 (Prompting)

- "将这段 `IMemoryCache` 代码重构为 `HybridCache`，并添加 100ms 的 Soft Timeout。"
- "为该服务添加 Backplane 配置，确保多节点下缓存主动失效一致。"
