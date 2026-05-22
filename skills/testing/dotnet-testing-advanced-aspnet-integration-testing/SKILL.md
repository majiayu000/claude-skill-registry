---
name: dotnet-testing-advanced-aspnet-integration-testing
description: |
  ASP.NET Core 整合測試的專門技能。當需要測試 Web API 端點、HTTP 請求/回應、中介軟體、依賴注入時使用。涵蓋 WebApplicationFactory、TestServer、HttpClient 測試、記憶體資料庫配置等。
  Keywords: integration testing, 整合測試, web api testing, WebApplicationFactory, TestServer, HttpClient testing, controller testing, endpoint testing, 端點測試, RESTful API testing, Microsoft.AspNetCore.Mvc.Testing, CreateClient, ConfigureWebHost, AwesomeAssertions.Web, Be200Ok, Be404NotFound, middleware testing, 中介軟體測試, dependency injection testing
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, ASP.NET Core, integration testing, WebApplicationFactory"
---

# ASP.NET Core 整合測試指南

## 概述

本技能指導如何在 ASP.NET Core 中建立有效的整合測試，使用 `WebApplicationFactory<T>` 和 `TestServer` 測試完整的 HTTP 請求/回應流程。

### 適用場景

- **Web API 端點測試**：驗證 RESTful API 的 CRUD 操作
- **HTTP 請求/回應驗證**：測試完整的請求處理管線
- **中介軟體測試**：驗證 Authentication、Authorization、Logging 等
- **依賴注入驗證**：確保 DI 容器設定正確
- **路由設定驗證**：確保 URL 路由正確對應到控制器動作
- **模型繫結測試**：驗證請求內容正確繫結到模型

### 必要套件

```xml
<PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.0.0" />
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
<PackageReference Include="AwesomeAssertions.Web" Version="1.9.6" />
<PackageReference Include="System.Net.Http.Json" Version="9.0.8" />
```

> ⚠️ **重要提醒**：使用 `AwesomeAssertions` 時，必須安裝 `AwesomeAssertions.Web`，而非 `FluentAssertions.Web`。

---

## 核心概念

### 整合測試的兩種定義

**定義一：多物件協作測試**

> 將兩個以上的類別做整合，並且測試它們之間的運作是不是正確的，測試案例一定是跨類別物件的

**定義二：外部資源整合測試**

> 會使用到外部資源，例如資料庫、外部服務、檔案、需要對測試環境進行特別處理等

### 為什麼需要整合測試？

- **確保多個模組在整合運作後，能夠正確工作**
- **單元測試無法涵蓋的整合點**：Routing、Middleware、Request/Response Pipeline
- **WebApplication 做了太多的整合與設定，單元測試無法確認到全部**
- **確認是否完善異常處理，減少更多問題的發生**

### 測試金字塔定位

| 測試類型   | 測試範圍      | 執行速度 | 維護成本 | 建議比例 |
| ---------- | ------------- | -------- | -------- | -------- |
| 單元測試   | 單一類別/方法 | 很快     | 低       | 70%      |
| 整合測試   | 多個元件      | 中等     | 中等     | 20%      |
| 端對端測試 | 完整流程      | 慢       | 高       | 10%      |

---

## 原則一：使用 WebApplicationFactory 建立測試環境

### 基本使用方式

```csharp
public class BasicIntegrationTest : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public BasicIntegrationTest(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task Get_首頁_應回傳成功()
    {
        // Arrange
        var client = _factory.CreateClient();

        // Act
        var response = await client.GetAsync("/");

        // Assert
        response.EnsureSuccessStatusCode();
    }
}
```

### 自訂 WebApplicationFactory

```csharp
public class CustomWebApplicationFactory<TProgram> : WebApplicationFactory<TProgram> 
    where TProgram : class
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // 移除原本的資料庫設定
            services.RemoveAll(typeof(DbContextOptions<AppDbContext>));
            
            // 加入記憶體資料庫
            services.AddDbContext<AppDbContext>(options =>
            {
                options.UseInMemoryDatabase("TestDatabase");
            });

            // 替換外部服務為測試版本
            services.Replace(ServiceDescriptor.Scoped<IEmailService, TestEmailService>());
        });

        // 設定測試環境
        builder.UseEnvironment("Testing");
    }
}
```

---

## 原則二：使用 AwesomeAssertions.Web 驗證 HTTP 回應

### HTTP 狀態碼斷言

```csharp
response.Should().Be200Ok();          // HTTP 200
response.Should().Be201Created();     // HTTP 201
response.Should().Be204NoContent();   // HTTP 204
response.Should().Be400BadRequest();  // HTTP 400
response.Should().Be404NotFound();    // HTTP 404
response.Should().Be500InternalServerError();  // HTTP 500
```

### Satisfy<T> 強型別驗證

```csharp
[Fact]
public async Task GetShipper_當貨運商存在_應回傳成功結果()
{
    // Arrange
    await CleanupDatabaseAsync();
    var shipperId = await SeedShipperAsync("順豐速運", "02-2345-6789");

    // Act
    var response = await Client.GetAsync($"/api/shippers/{shipperId}");

    // Assert
    response.Should().Be200Ok()
            .And
            .Satisfy<SuccessResultOutputModel<ShipperOutputModel>>(result =>
            {
                result.Status.Should().Be("Success");
                result.Data.Should().NotBeNull();
                result.Data!.ShipperId.Should().Be(shipperId);
                result.Data.CompanyName.Should().Be("順豐速運");
                result.Data.Phone.Should().Be("02-2345-6789");
            });
}
```

### 與傳統方式的比較

```csharp
// ❌ 傳統方式 - 冗長且容易出錯
response.IsSuccessStatusCode.Should().BeTrue();
var content = await response.Content.ReadAsStringAsync();
var result = JsonSerializer.Deserialize<SuccessResultOutputModel<ShipperOutputModel>>(content,
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true });
result.Should().NotBeNull();
result!.Status.Should().Be("Success");

// ✅ 使用 Satisfy<T> - 簡潔且直觀
response.Should().Be200Ok()
        .And
        .Satisfy<SuccessResultOutputModel<ShipperOutputModel>>(result =>
        {
            result.Status.Should().Be("Success");
            result.Data!.CompanyName.Should().Be("測試公司");
        });
```

---

## 原則三：使用 System.Net.Http.Json 簡化 JSON 操作

### PostAsJsonAsync 簡化 POST 請求

```csharp
// ❌ 傳統方式
var createParameter = new ShipperCreateParameter { CompanyName = "測試公司", Phone = "02-1234-5678" };
var jsonContent = JsonSerializer.Serialize(createParameter);
var content = new StringContent(jsonContent, Encoding.UTF8, "application/json");
var response = await client.PostAsync("/api/shippers", content);

// ✅ 現代化方式
var createParameter = new ShipperCreateParameter { CompanyName = "測試公司", Phone = "02-1234-5678" };
var response = await client.PostAsJsonAsync("/api/shippers", createParameter);
```

### ReadFromJsonAsync 簡化回應讀取

```csharp
// ❌ 傳統方式
var responseContent = await response.Content.ReadAsStringAsync();
var result = JsonSerializer.Deserialize<SuccessResultOutputModel<ShipperOutputModel>>(responseContent,
    new JsonSerializerOptions { PropertyNameCaseInsensitive = true });

// ✅ 現代化方式
var result = await response.Content.ReadFromJsonAsync<SuccessResultOutputModel<ShipperOutputModel>>();
```

---

## 三個層級的整合測試策略

### Level 1：簡單的 WebApi 專案

**特色**：

- 沒有資料庫、Service 與 Repository 依賴
- 最簡單、基本的 WebApi 網站專案
- 直接使用 `WebApplicationFactory<Program>` 進行測試

**測試重點**：

- 各個 API 的輸入輸出驗證
- HTTP 動詞和路由正確性
- 模型綁定和序列化
- 狀態碼和回應格式驗證

```csharp
public class BasicApiControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly HttpClient _client;

    public BasicApiControllerTests(WebApplicationFactory<Program> factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetStatus_應回傳OK()
    {
        // Act
        var response = await _client.GetAsync("/api/status");

        // Assert
        response.Should().Be200Ok();
    }
}
```

### Level 2：相依 Service 的 WebApi 專案

**特色**：

- 沒有資料庫，但有 Service 依賴
- 使用 NSubstitute 建立 Service stub
- 在測試中配置依賴注入

```csharp
public class ServiceStubWebApplicationFactory : WebApplicationFactory<Program>
{
    private readonly IExampleService _serviceStub;

    public ServiceStubWebApplicationFactory(IExampleService serviceStub)
    {
        _serviceStub = serviceStub;
    }

    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureTestServices(services =>
        {
            services.RemoveAll<IExampleService>();
            services.AddScoped(_ => _serviceStub);
        });
    }
}

public class ServiceDependentControllerTests
{
    [Fact]
    public async Task GetData_應回傳服務資料()
    {
        // Arrange
        var serviceStub = Substitute.For<IExampleService>();
        serviceStub.GetDataAsync().Returns("測試資料");
        
        var factory = new ServiceStubWebApplicationFactory(serviceStub);
        var client = factory.CreateClient();

        // Act
        var response = await client.GetAsync("/api/data");

        // Assert
        response.Should().Be200Ok();
    }
}
```

### Level 3：完整的 WebApi 專案

**特色**：

- 完整的 Solution 架構
- 包含真實的資料庫操作
- 使用 InMemory 或真實測試資料庫

```csharp
public class FullDatabaseWebApplicationFactory : WebApplicationFactory<Program>
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            // 移除原本的資料庫設定
            var descriptor = services.SingleOrDefault(
                d => d.ServiceType == typeof(DbContextOptions<AppDbContext>));
            if (descriptor != null)
            {
                services.Remove(descriptor);
            }

            // 加入記憶體資料庫
            services.AddDbContext<AppDbContext>(options =>
            {
                options.UseInMemoryDatabase("TestDatabase");
            });

            // 建立資料庫並加入測試資料
            var serviceProvider = services.BuildServiceProvider();
            using var scope = serviceProvider.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
            
            context.Database.EnsureCreated();
        });
    }
}
```

---

## 測試基底類別模式

### 建立可重用的測試基底類別

```csharp
public abstract class IntegrationTestBase : IDisposable
{
    protected readonly CustomWebApplicationFactory Factory;
    protected readonly HttpClient Client;

    protected IntegrationTestBase()
    {
        Factory = new CustomWebApplicationFactory();
        Client = Factory.CreateClient();
    }

    protected async Task<int> SeedShipperAsync(string companyName, string phone = "02-12345678")
    {
        using var scope = Factory.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        
        var shipper = new Shipper
        {
            CompanyName = companyName,
            Phone = phone,
            CreatedAt = DateTime.UtcNow
        };
        
        context.Shippers.Add(shipper);
        await context.SaveChangesAsync();
        
        return shipper.ShipperId;
    }

    protected async Task CleanupDatabaseAsync()
    {
        using var scope = Factory.Services.CreateScope();
        var context = scope.ServiceProvider.GetRequiredService<AppDbContext>();
        
        context.Shippers.RemoveRange(context.Shippers);
        await context.SaveChangesAsync();
    }

    public void Dispose()
    {
        Client?.Dispose();
        Factory?.Dispose();
    }
}
```

---

## CRUD 操作測試範例

### GET 請求測試

```csharp
[Fact]
public async Task GetShipper_當貨運商存在_應回傳成功結果()
{
    // Arrange
    await CleanupDatabaseAsync();
    var shipperId = await SeedShipperAsync("順豐速運", "02-2345-6789");

    // Act
    var response = await Client.GetAsync($"/api/shippers/{shipperId}");

    // Assert
    response.Should().Be200Ok()
            .And
            .Satisfy<SuccessResultOutputModel<ShipperOutputModel>>(result =>
            {
                result.Status.Should().Be("Success");
                result.Data!.ShipperId.Should().Be(shipperId);
                result.Data.CompanyName.Should().Be("順豐速運");
            });
}

[Fact]
public async Task GetShipper_當貨運商不存在_應回傳404NotFound()
{
    // Arrange
    var nonExistentShipperId = 9999;

    // Act
    var response = await Client.GetAsync($"/api/shippers/{nonExistentShipperId}");

    // Assert
    response.Should().Be404NotFound();
}
```

### POST 請求測試

```csharp
[Fact]
public async Task CreateShipper_輸入有效資料_應建立成功()
{
    // Arrange
    await CleanupDatabaseAsync();
    var createParameter = new ShipperCreateParameter
    {
        CompanyName = "黑貓宅急便",
        Phone = "02-1234-5678"
    };

    // Act
    var response = await Client.PostAsJsonAsync("/api/shippers", createParameter);

    // Assert
    response.Should().Be201Created()
            .And
            .Satisfy<SuccessResultOutputModel<ShipperOutputModel>>(result =>
            {
                result.Status.Should().Be("Success");
                result.Data!.ShipperId.Should().BeGreaterThan(0);
                result.Data.CompanyName.Should().Be("黑貓宅急便");
            });
}
```

### 驗證錯誤測試

```csharp
[Fact]
public async Task CreateShipper_當公司名稱為空_應回傳400BadRequest()
{
    // Arrange
    var createParameter = new ShipperCreateParameter
    {
        CompanyName = "",
        Phone = "02-1234-5678"
    };

    // Act
    var response = await Client.PostAsJsonAsync("/api/shippers", createParameter);

    // Assert
    response.Should().Be400BadRequest()
            .And
            .Satisfy<ValidationProblemDetails>(problem =>
            {
                problem.Status.Should().Be(400);
                problem.Errors.Should().ContainKey("CompanyName");
            });
}
```

### 集合資料測試

```csharp
[Fact]
public async Task GetAllShippers_應回傳所有貨運商()
{
    // Arrange
    await CleanupDatabaseAsync();
    await SeedShipperAsync("公司A", "02-1111-1111");
    await SeedShipperAsync("公司B", "02-2222-2222");

    // Act
    var response = await Client.GetAsync("/api/shippers");

    // Assert
    response.Should().Be200Ok()
            .And
            .Satisfy<SuccessResultOutputModel<List<ShipperOutputModel>>>(result =>
            {
                result.Data!.Count.Should().Be(2);
                result.Data.Should().Contain(s => s.CompanyName == "公司A");
                result.Data.Should().Contain(s => s.CompanyName == "公司B");
            });
}
```

---

## 專案結構建議

```text
tests/
├── Sample.WebApplication.UnitTests/           # 單元測試
├── Sample.WebApplication.Integration.Tests/   # 整合測試
│   ├── Controllers/                           # 控制器整合測試
│   │   └── ShippersControllerTests.cs
│   ├── Infrastructure/                        # 測試基礎設施
│   │   └── CustomWebApplicationFactory.cs
│   ├── IntegrationTestBase.cs                 # 測試基底類別
│   └── GlobalUsings.cs
└── Sample.WebApplication.E2ETests/            # 端對端測試
```

---

## 套件相容性故障排除

### 常見錯誤

```text
error CS1061: 'ObjectAssertions' 未包含 'Be200Ok' 的定義
```

### 解決方案

| 基礎斷言庫                 | 正確的套件              |
| -------------------------- | ----------------------- |
| FluentAssertions < 8.0.0   | FluentAssertions.Web    |
| FluentAssertions >= 8.0.0  | FluentAssertions.Web.v8 |
| AwesomeAssertions >= 8.0.0 | AwesomeAssertions.Web   |

```xml
<!-- 正確：使用 AwesomeAssertions 應該安裝 AwesomeAssertions.Web -->
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
<PackageReference Include="AwesomeAssertions.Web" Version="1.9.6" />
```

---

## 最佳實踐

### 應該做的 ✅

1. **獨立測試專案**：整合測試專案應與單元測試分離
2. **測試資料隔離**：每個測試案例有獨立的資料準備和清理
3. **使用基底類別**：共用的設定和輔助方法放在基底類別
4. **明確的命名**：使用三段式命名法（方法_情境_預期）
5. **適當的測試範圍**：專注於整合點，不要過度測試

### 應該避免的 ❌

1. **混合測試類型**：不要將單元測試和整合測試放在同一專案
2. **測試相依性**：每個測試應該獨立，不依賴其他測試的執行順序
3. **過度模擬**：整合測試應該盡量使用真實的元件
4. **忽略清理**：測試完成後要清理測試資料
5. **硬編碼資料**：使用工廠方法或 Builder 模式建立測試資料

---

## 相關技能

- `unit-test-fundamentals` - 單元測試基礎
- `nsubstitute-mocking` - 使用 NSubstitute 進行模擬
- `awesome-assertions-guide` - AwesomeAssertions 流暢斷言
- `testcontainers-database` - 使用 Testcontainers 進行容器化資料庫測試

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 19 - 整合測試入門：基礎架構與應用場景**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376335
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day19

### 官方文件

- [ASP.NET Core 整合測試文件](https://docs.microsoft.com/aspnet/core/test/integration-tests)
- [WebApplicationFactory 使用指南](https://docs.microsoft.com/aspnet/core/test/integration-tests#basic-tests-with-the-default-webapplicationfactory)
- [AwesomeAssertions.Web GitHub](https://github.com/AwesomeAssertions/AwesomeAssertions.Web)
- [AwesomeAssertions.Web NuGet](https://www.nuget.org/packages/AwesomeAssertions.Web)
