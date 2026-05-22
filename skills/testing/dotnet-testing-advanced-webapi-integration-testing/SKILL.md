---
name: dotnet-testing-advanced-webapi-integration-testing
description: |
  ASP.NET Core WebApi 整合測試完整指南。涵蓋 WebApplicationFactory、IExceptionHandler、ProblemDetails 標準格式驗證。包含 Testcontainers 多容器編排、Flurl URL 建構、AwesomeAssertions HTTP 驗證。
  Keywords: webapi integration testing, WebApplicationFactory, asp.net core integration test, webapi 整合測試, IExceptionHandler, ProblemDetails, ValidationProblemDetails, AwesomeAssertions, Flurl, Respawn, Be201Created, Be400BadRequest, 多容器測試, Collection Fixture, 全域例外處理
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: "webapi, integration-testing, testcontainers, aspnetcore, clean-architecture"
---

# WebApi 整合測試

## 技能概述

**技能等級**: 進階  
**所需前置知識**: xUnit 基礎、ASP.NET Core 基礎、Testcontainers 基礎、Clean Architecture  
**預計學習時間**: 60-90 分鐘

## 學習目標

完成本技能學習後，您將能夠：

1. 建立完整的 WebApi 整合測試架構
2. 使用 `IExceptionHandler` 實作現代化異常處理
3. 驗證 `ProblemDetails` 和 `ValidationProblemDetails` 標準格式
4. 使用 Flurl 簡化 HTTP 測試的 URL 建構
5. 使用 AwesomeAssertions 進行精確的 HTTP 回應驗證
6. 建立多容器 (PostgreSQL + Redis) 測試環境

## 核心概念

### IExceptionHandler - 現代化異常處理

ASP.NET Core 8+ 引入的 `IExceptionHandler` 介面提供了比傳統 middleware 更優雅的錯誤處理方式：

```csharp
/// <summary>
/// 全域異常處理器
/// </summary>
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;

    public GlobalExceptionHandler(ILogger<GlobalExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        _logger.LogError(exception, "發生未處理的異常: {Message}", exception.Message);

        var problemDetails = CreateProblemDetails(exception);

        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        httpContext.Response.ContentType = "application/problem+json";

        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);
        return true;
    }

    private static ProblemDetails CreateProblemDetails(Exception exception)
    {
        return exception switch
        {
            KeyNotFoundException => new ProblemDetails
            {
                Type = "https://httpstatuses.com/404",
                Title = "資源不存在",
                Status = 404,
                Detail = exception.Message
            },
            ArgumentException => new ProblemDetails
            {
                Type = "https://httpstatuses.com/400",
                Title = "參數錯誤",
                Status = 400,
                Detail = exception.Message
            },
            _ => new ProblemDetails
            {
                Type = "https://httpstatuses.com/500",
                Title = "內部伺服器錯誤",
                Status = 500,
                Detail = "發生未預期的錯誤"
            }
        };
    }
}
```

### ProblemDetails 標準格式

RFC 7807 定義的統一錯誤回應格式：

| 欄位       | 說明               |
| ---------- | ------------------ |
| `type`     | 問題類型的 URI     |
| `title`    | 簡短的錯誤描述     |
| `status`   | HTTP 狀態碼        |
| `detail`   | 詳細的錯誤說明     |
| `instance` | 發生問題的實例 URI |

### ValidationProblemDetails - 驗證錯誤專用

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "detail": "輸入的資料包含驗證錯誤",
  "errors": {
    "Name": ["產品名稱不能為空"],
    "Price": ["產品價格必須大於 0"]
  }
}
```

### FluentValidation 異常處理器

```csharp
/// <summary>
/// FluentValidation 專用異常處理器
/// </summary>
public class FluentValidationExceptionHandler : IExceptionHandler
{
    private readonly ILogger<FluentValidationExceptionHandler> _logger;

    public FluentValidationExceptionHandler(ILogger<FluentValidationExceptionHandler> logger)
    {
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        if (exception is not ValidationException validationException)
        {
            return false; // 讓下一個處理器處理
        }

        _logger.LogWarning(validationException, "驗證失敗: {Message}", validationException.Message);

        var problemDetails = new ValidationProblemDetails
        {
            Type = "https://tools.ietf.org/html/rfc9110#section-15.5.1",
            Title = "One or more validation errors occurred.",
            Status = 400,
            Detail = "輸入的資料包含驗證錯誤",
            Instance = httpContext.Request.Path
        };

        foreach (var error in validationException.Errors)
        {
            if (problemDetails.Errors.ContainsKey(error.PropertyName))
            {
                var errors = problemDetails.Errors[error.PropertyName].ToList();
                errors.Add(error.ErrorMessage);
                problemDetails.Errors[error.PropertyName] = errors.ToArray();
            }
            else
            {
                problemDetails.Errors.Add(error.PropertyName, new[] { error.ErrorMessage });
            }
        }

        httpContext.Response.StatusCode = 400;
        httpContext.Response.ContentType = "application/problem+json";
        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }
}
```

### 註冊順序很重要

異常處理器按照註冊順序執行，特定處理器必須在全域處理器之前：

```csharp
// Program.cs
builder.Services.AddProblemDetails();

// 順序很重要！特定處理器先註冊
builder.Services.AddExceptionHandler<FluentValidationExceptionHandler>();
builder.Services.AddExceptionHandler<GlobalExceptionHandler>();

// Middleware
app.UseExceptionHandler();
```

## 整合測試基礎設施

### TestWebApplicationFactory

```csharp
public class TestWebApplicationFactory : WebApplicationFactory<Program>, IAsyncLifetime
{
    private PostgreSqlContainer? _postgresContainer;
    private RedisContainer? _redisContainer;
    private FakeTimeProvider? _timeProvider;

    public PostgreSqlContainer PostgresContainer => _postgresContainer
        ?? throw new InvalidOperationException("PostgreSQL container 尚未初始化");

    public RedisContainer RedisContainer => _redisContainer
        ?? throw new InvalidOperationException("Redis container 尚未初始化");

    public FakeTimeProvider TimeProvider => _timeProvider
        ?? throw new InvalidOperationException("TimeProvider 尚未初始化");

    public async Task InitializeAsync()
    {
        _postgresContainer = new PostgreSqlBuilder()
            .WithImage("postgres:16-alpine")
            .WithDatabase("test_db")
            .WithUsername("testuser")
            .WithPassword("testpass")
            .WithCleanUp(true)
            .Build();

        _redisContainer = new RedisBuilder()
            .WithImage("redis:7-alpine")
            .WithCleanUp(true)
            .Build();

        _timeProvider = new FakeTimeProvider(new DateTimeOffset(2024, 1, 1, 0, 0, 0, TimeSpan.Zero));

        await _postgresContainer.StartAsync();
        await _redisContainer.StartAsync();
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureAppConfiguration(config =>
        {
            config.Sources.Clear();
            config.AddInMemoryCollection(new Dictionary<string, string?>
            {
                ["ConnectionStrings:DefaultConnection"] = PostgresContainer.GetConnectionString(),
                ["ConnectionStrings:Redis"] = RedisContainer.GetConnectionString(),
                ["Logging:LogLevel:Default"] = "Warning"
            });
        });

        builder.ConfigureServices(services =>
        {
            // 替換 TimeProvider
            services.Remove(services.Single(d => d.ServiceType == typeof(TimeProvider)));
            services.AddSingleton<TimeProvider>(TimeProvider);
        });

        builder.UseEnvironment("Testing");
    }

    public new async Task DisposeAsync()
    {
        if (_postgresContainer != null) await _postgresContainer.DisposeAsync();
        if (_redisContainer != null) await _redisContainer.DisposeAsync();
        await base.DisposeAsync();
    }
}
```

### Collection Fixture 模式

```csharp
[CollectionDefinition("Integration Tests")]
public class IntegrationTestCollection : ICollectionFixture<TestWebApplicationFactory>
{
    public const string Name = "Integration Tests";
}
```

### 測試基底類別

```csharp
[Collection("Integration Tests")]
public abstract class IntegrationTestBase : IAsyncLifetime
{
    protected readonly TestWebApplicationFactory Factory;
    protected readonly HttpClient HttpClient;
    protected readonly DatabaseManager DatabaseManager;
    protected readonly IFlurlClient FlurlClient;

    protected IntegrationTestBase(TestWebApplicationFactory factory)
    {
        Factory = factory;
        HttpClient = factory.CreateClient();
        DatabaseManager = new DatabaseManager(factory.PostgresContainer.GetConnectionString());
        FlurlClient = new FlurlClient(HttpClient);
    }

    public virtual async Task InitializeAsync()
    {
        await DatabaseManager.InitializeDatabaseAsync();
    }

    public virtual async Task DisposeAsync()
    {
        await DatabaseManager.CleanDatabaseAsync();
        FlurlClient.Dispose();
    }

    protected void ResetTime()
    {
        Factory.TimeProvider.SetUtcNow(new DateTimeOffset(2024, 1, 1, 0, 0, 0, TimeSpan.Zero));
    }

    protected void AdvanceTime(TimeSpan timeSpan)
    {
        Factory.TimeProvider.Advance(timeSpan);
    }
}
```

## Flurl 簡化 URL 建構

Flurl 提供流暢的 API 來建構複雜的 URL：

```csharp
// 傳統方式
var url = $"/products?pageSize={pageSize}&page={page}&keyword={keyword}";

// 使用 Flurl
var url = "/products"
    .SetQueryParam("pageSize", 5)
    .SetQueryParam("page", 2)
    .SetQueryParam("keyword", "特殊");
```

## 測試範例

### 成功建立產品測試

```csharp
[Fact]
public async Task CreateProduct_使用有效資料_應成功建立產品()
{
    // Arrange
    var request = new ProductCreateRequest { Name = "新產品", Price = 299.99m };

    // Act
    var response = await HttpClient.PostAsJsonAsync("/products", request);

    // Assert
    response.Should().Be201Created()
        .And.Satisfy<ProductResponse>(product =>
        {
            product.Id.Should().NotBeEmpty();
            product.Name.Should().Be("新產品");
            product.Price.Should().Be(299.99m);
        });
}
```

### 驗證錯誤測試

```csharp
[Fact]
public async Task CreateProduct_當產品名稱為空_應回傳400BadRequest()
{
    // Arrange
    var invalidRequest = new ProductCreateRequest { Name = "", Price = 100.00m };

    // Act
    var response = await HttpClient.PostAsJsonAsync("/products", invalidRequest);

    // Assert
    response.Should().Be400BadRequest()
        .And.Satisfy<ValidationProblemDetails>(problem =>
        {
            problem.Type.Should().Be("https://tools.ietf.org/html/rfc9110#section-15.5.1");
            problem.Title.Should().Be("One or more validation errors occurred.");
            problem.Errors.Should().ContainKey("Name");
            problem.Errors["Name"].Should().Contain("產品名稱不能為空");
        });
}
```

### 資源不存在測試

```csharp
[Fact]
public async Task GetById_當產品不存在_應回傳404且包含ProblemDetails()
{
    // Arrange
    var nonExistentId = Guid.NewGuid();

    // Act
    var response = await HttpClient.GetAsync($"/Products/{nonExistentId}");

    // Assert
    response.Should().Be404NotFound()
        .And.Satisfy<ProblemDetails>(problem =>
        {
            problem.Type.Should().Be("https://httpstatuses.com/404");
            problem.Title.Should().Be("產品不存在");
            problem.Status.Should().Be(404);
        });
}
```

### 分頁查詢測試

```csharp
[Fact]
public async Task GetProducts_使用分頁參數_應回傳正確的分頁結果()
{
    // Arrange
    await TestHelpers.SeedProductsAsync(DatabaseManager, 15);

    // Act - 使用 Flurl 建構 QueryString
    var url = "/products"
        .SetQueryParam("pageSize", 5)
        .SetQueryParam("page", 2);

    var response = await HttpClient.GetAsync(url);

    // Assert
    response.Should().Be200Ok()
        .And.Satisfy<PagedResult<ProductResponse>>(result =>
        {
            result.Total.Should().Be(15);
            result.PageSize.Should().Be(5);
            result.Page.Should().Be(2);
            result.Items.Should().HaveCount(5);
        });
}
```

## 資料管理策略

### TestHelpers 設計

```csharp
public static class TestHelpers
{
    public static ProductCreateRequest CreateProductRequest(
        string name = "測試產品",
        decimal price = 100.00m)
    {
        return new ProductCreateRequest { Name = name, Price = price };
    }

    public static async Task SeedProductsAsync(DatabaseManager dbManager, int count)
    {
        var tasks = Enumerable.Range(1, count)
            .Select(i => SeedSpecificProductAsync(dbManager, $"產品 {i:D2}", i * 10.0m));
        await Task.WhenAll(tasks);
    }
}
```

### SQL 指令碼外部化

```text
tests/Integration/
└── SqlScripts/
    └── Tables/
        └── CreateProductsTable.sql
```

## 最佳實務

### 1. 測試結構設計

- **單一職責**：每個測試專注於一個特定場景
- **3A 模式**：清楚區分 Arrange、Act、Assert
- **清晰命名**：方法名稱表達測試意圖

### 2. 錯誤處理驗證

- **ValidationProblemDetails**：驗證錯誤回應格式
- **ProblemDetails**：驗證業務異常回應
- **HTTP 狀態碼**：確認正確的狀態碼

### 3. 效能考量

- **容器共享**：使用 Collection Fixture
- **資料清理**：測試後清理資料，不重建容器
- **並行執行**：確保測試獨立性

## 相依套件

```xml
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
<PackageReference Include="Testcontainers.PostgreSql" Version="4.0.0" />
<PackageReference Include="Testcontainers.Redis" Version="4.0.0" />
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.0.0" />
<PackageReference Include="Flurl" Version="4.0.0" />
<PackageReference Include="Respawn" Version="6.2.1" />
```

## 專案結構

```text
src/
├── Api/                          # WebApi 層
├── Application/                  # 應用服務層
├── Domain/                       # 領域模型
└── Infrastructure/               # 基礎設施層
tests/
└── Integration/
    ├── Fixtures/
    │   ├── TestWebApplicationFactory.cs
    │   ├── IntegrationTestCollection.cs
    │   └── IntegrationTestBase.cs
    ├── Handlers/
    │   ├── GlobalExceptionHandler.cs
    │   └── FluentValidationExceptionHandler.cs
    ├── Helpers/
    │   ├── DatabaseManager.cs
    │   └── TestHelpers.cs
    ├── SqlScripts/
    │   └── Tables/
    └── Controllers/
        └── ProductsControllerTests.cs
```

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 23 - 整合測試實戰：WebApi 服務的整合測試**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376873
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day23

### 官方文件

- [ASP.NET Core 整合測試](https://docs.microsoft.com/aspnet/core/test/integration-tests)
- [IExceptionHandler 文件](https://learn.microsoft.com/aspnet/core/fundamentals/error-handling)
- [ProblemDetails RFC 7807](https://tools.ietf.org/html/rfc7807)
- [Testcontainers for .NET](https://dotnet.testcontainers.org/)
- [AwesomeAssertions](https://awesomeassertions.org/)
- [Flurl HTTP Client](https://flurl.dev/)
- [Respawn](https://github.com/jbogard/Respawn)
