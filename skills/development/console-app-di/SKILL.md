---
name: console-app-di
description: 'Console Application에서 GenericHost와 DI를 사용한 의존성 주입 패턴'
---

# Console Application DI 패턴

.NET Console Application에서 GenericHost를 사용한 의존성 주입 구현 가이드입니다.

## 1. 필수 NuGet 패키지

```xml
<ItemGroup>
  <PackageReference Include="Microsoft.Extensions.Hosting" Version="9.0.*" />
</ItemGroup>
```

## 2. 기본 구현

### 2.1 Program.cs

```csharp
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

var host = Host.CreateDefaultBuilder(args)
    .ConfigureServices((context, services) =>
    {
        services.AddSingleton<IMyService, MyService>();
        services.AddSingleton<App>();
    })
    .Build();

var app = host.Services.GetRequiredService<App>();
await app.RunAsync();
```

### 2.2 App.cs

```csharp
namespace MyApp;

public sealed class App(IMyService myService)
{
    private readonly IMyService _myService = myService;

    public async Task RunAsync()
    {
        await _myService.DoWorkAsync();
    }
}
```

## 3. Service Lifetime

| Lifetime | 설명 | 사용 시점 |
|----------|------|----------|
| `Singleton` | 앱 전체 단일 인스턴스 | 상태 없는 서비스 |
| `Scoped` | 요청당 단일 인스턴스 | DbContext |
| `Transient` | 주입마다 새 인스턴스 | 경량 서비스 |

## 4. Configuration 통합

```csharp
var host = Host.CreateDefaultBuilder(args)
    .ConfigureAppConfiguration((context, config) =>
    {
        config.AddJsonFile("appsettings.json", optional: true);
    })
    .ConfigureServices((context, services) =>
    {
        services.Configure<AppSettings>(
            context.Configuration.GetSection("AppSettings"));
        services.AddSingleton<App>();
    })
    .Build();
```

## 5. Logging 통합

```csharp
public sealed class App(ILogger<App> logger)
{
    public Task RunAsync()
    {
        logger.LogInformation("애플리케이션 시작");
        return Task.CompletedTask;
    }
}
```

## 6. 주의사항

### ⚠️ Service Locator 패턴 금지

```csharp
// ❌ 나쁜 예
public sealed class BadService(IServiceProvider provider)
{
    public void DoWork()
    {
        var service = provider.GetRequiredService<IMyService>();
    }
}

// ✅ 좋은 예
public sealed class GoodService(IMyService myService)
{
    public void DoWork() { }
}
```

### ⚠️ Captive Dependency

- Singleton이 Scoped/Transient를 주입받으면 안 됨

## 7. 참고 문서

- [.NET Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host)
