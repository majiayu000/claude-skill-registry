---
name: aspire-testing
description: 協助使用 .NET Aspire Testing 框架建立分散式應用的整合測試。當使用者要求建立 Aspire 測試、從 Testcontainers 遷移到 Aspire Testing、或需要測試雲原生 .NET 應用時使用此技能。
license: MIT
---

# .NET Aspire Testing 整合測試框架

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 為 .NET Aspire 分散式應用建立整合測試
- 從 Testcontainers 遷移到 .NET Aspire Testing
- 設定 AppHost 專案進行測試
- 使用 DistributedApplicationTestingBuilder 建立測試環境
- 需要測試多個服務間的互動（資料庫、快取、API 等）
- 建立雲原生 .NET 應用的整合測試架構

## 前置需求

- .NET 8 SDK 或更高版本
- Docker Desktop（WSL 2 或 Hyper-V）
- AppHost 專案（.NET Aspire 應用編排）

## 核心概念

### .NET Aspire Testing 定位

**.NET Aspire Testing 是封閉式整合測試框架**，專為分散式應用設計：

- 在測試中重現與正式環境相同的服務架構
- 使用真實容器而非模擬服務
- 自動管理容器生命週期

### AppHost 專案的必要性

使用 .NET Aspire Testing 必須建立 AppHost 專案：

- 定義完整的應用架構和容器編排
- 測試重用 AppHost 配置建立環境
- 沒有 AppHost 就無法使用 Aspire Testing

### 與 Testcontainers 的差異

| 特性     | .NET Aspire Testing | Testcontainers |
| -------- | ------------------- | -------------- |
| 設計目標 | 雲原生分散式應用    | 通用容器測試   |
| 配置方式 | AppHost 宣告式定義  | 程式碼手動配置 |
| 服務編排 | 自動處理            | 手動管理       |
| 學習曲線 | 較高                | 中等           |
| 適用場景 | 已用 Aspire 的專案  | 傳統 Web API   |

## 專案結構

```text
MyApp/
├── src/
│   ├── MyApp.Api/                    # WebApi 層
│   ├── MyApp.Application/            # 應用服務層  
│   ├── MyApp.Domain/                 # 領域模型
│   └── MyApp.Infrastructure/         # 基礎設施層
├── MyApp.AppHost/                    # Aspire 編排專案 ⭐
│   ├── MyApp.AppHost.csproj
│   └── Program.cs
└── tests/
    └── MyApp.Tests.Integration/      # Aspire Testing 整合測試
        ├── MyApp.Tests.Integration.csproj
        ├── Infrastructure/
        │   ├── AspireAppFixture.cs
        │   ├── IntegrationTestCollection.cs
        │   ├── IntegrationTestBase.cs
        │   └── DatabaseManager.cs
        └── Controllers/
            └── MyControllerTests.cs
```

## 必要套件

### AppHost 專案

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <Sdk Name="Aspire.AppHost.Sdk" Version="9.0.0" />

  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
    <IsAspireHost>true</IsAspireHost>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Aspire.Hosting.AppHost" Version="9.1.0" />
    <PackageReference Include="Aspire.Hosting.PostgreSQL" Version="9.1.0" />
    <PackageReference Include="Aspire.Hosting.Redis" Version="9.1.0" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\src\MyApp.Api\MyApp.Api.csproj" />
  </ItemGroup>
</Project>
```

### 測試專案

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Aspire.Hosting.Testing" Version="9.1.0" />
    <PackageReference Include="AwesomeAssertions" Version="9.1.0" />
    <PackageReference Include="Microsoft.AspNetCore.Mvc.Testing" Version="9.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.12.0" />
    <PackageReference Include="Respawn" Version="6.2.1" />
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="2.8.2" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\MyApp.AppHost\MyApp.AppHost.csproj" />
  </ItemGroup>
</Project>
```

## 容器生命週期管理

使用 `ContainerLifetime.Session` 確保測試資源自動清理：

```csharp
var postgres = builder.AddPostgres("postgres")
                     .WithLifetime(ContainerLifetime.Session);

var redis = builder.AddRedis("redis")
                  .WithLifetime(ContainerLifetime.Session);
```

- **Session**：測試會話結束後自動清理（推薦）
- **Persistent**：容器持續運行，需手動清理

## 等待服務就緒

容器啟動與服務就緒是兩個階段，需要等待機制：

```csharp
private async Task WaitForPostgreSqlReadyAsync()
{
    const int maxRetries = 30;
    const int delayMs = 1000;

    for (int i = 0; i < maxRetries; i++)
    {
        try
        {
            var connectionString = await GetConnectionStringAsync();
            await using var connection = new NpgsqlConnection(connectionString);
            await connection.OpenAsync();
            return;
        }
        catch (Exception ex) when (i < maxRetries - 1)
        {
            await Task.Delay(delayMs);
        }
    }
    throw new InvalidOperationException("PostgreSQL 服務未能就緒");
}
```

## 資料庫初始化

Aspire 啟動容器但不自動建立資料庫：

```csharp
private async Task EnsureDatabaseExistsAsync(string connectionString)
{
    var builder = new NpgsqlConnectionStringBuilder(connectionString);
    var databaseName = builder.Database;
    builder.Database = "postgres"; // 連到預設資料庫
    
    await using var connection = new NpgsqlConnection(builder.ToString());
    await connection.OpenAsync();
    
    var checkDbQuery = $"SELECT 1 FROM pg_database WHERE datname = '{databaseName}'";
    var dbExists = await new NpgsqlCommand(checkDbQuery, connection).ExecuteScalarAsync();
    
    if (dbExists == null)
    {
        await new NpgsqlCommand($"CREATE DATABASE \"{databaseName}\"", connection)
            .ExecuteNonQueryAsync();
    }
}
```

## Respawn 配置

使用 PostgreSQL 時必須指定適配器：

```csharp
_respawner = await Respawner.CreateAsync(connection, new RespawnerOptions
{
    TablesToIgnore = new Table[] { "__EFMigrationsHistory" },
    SchemasToInclude = new[] { "public" },
    DbAdapter = DbAdapter.Postgres  // 關鍵！
});
```

## Collection Fixture 最佳實踐

避免每個測試類別重複啟動容器：

```csharp
[CollectionDefinition("Integration Tests")]
public class IntegrationTestCollection : ICollectionFixture<AspireAppFixture>
{
}

[Collection("Integration Tests")]
public class MyControllerTests : IntegrationTestBase
{
    public MyControllerTests(AspireAppFixture fixture) : base(fixture) { }
}
```

## 時間可測試性

使用 `TimeProvider` 抽象化時間依賴：

```csharp
// 服務實作
public class ProductService
{
    private readonly TimeProvider _timeProvider;
    
    public ProductService(TimeProvider timeProvider)
    {
        _timeProvider = timeProvider;
    }
    
    public async Task<Product> CreateAsync(ProductCreateRequest request)
    {
        var now = _timeProvider.GetUtcNow();
        var product = new Product
        {
            CreatedAt = now,
            UpdatedAt = now
        };
        // ...
    }
}

// DI 註冊
builder.Services.AddSingleton<TimeProvider>(TimeProvider.System);
```

## 選擇建議

### 選擇 .NET Aspire Testing

- 專案已使用 .NET Aspire
- 需要測試多服務互動
- 重視統一的開發測試體驗
- 雲原生應用架構

### 選擇 Testcontainers

- 傳統 .NET 專案
- 需要精細的容器控制
- 與非 .NET 服務整合
- 團隊對 Aspire 不熟悉

## 常見問題

### 端點配置衝突

不要手動配置已由 Aspire 自動處理的端點：

```csharp
// ❌ 錯誤：會造成衝突
builder.AddProject<Projects.MyApp_Api>("my-api")
       .WithHttpEndpoint(port: 8080, name: "http");

// ✅ 正確：讓 Aspire 自動處理
builder.AddProject<Projects.MyApp_Api>("my-api")
       .WithReference(postgresDb)
       .WithReference(redis);
```

### Dapper 欄位映射

PostgreSQL snake_case 與 C# PascalCase 的映射：

```csharp
// 在 Program.cs 初始化
DapperTypeMapping.Initialize();

// 或使用 SQL 別名
const string sql = @"
    SELECT id, name, price, 
           created_at AS CreatedAt, 
           updated_at AS UpdatedAt
    FROM products";
```

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 24 - .NET Aspire Testing 入門基礎介紹**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376333
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day24

- **Day 25 - .NET Aspire 整合測試實戰：從 Testcontainers 到 .NET Aspire Testing**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10376439
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day25

### 官方文件

- [.NET Aspire 官方文件](https://learn.microsoft.com/dotnet/aspire/)
- [Aspire Testing 文件](https://learn.microsoft.com/dotnet/aspire/testing)

## 程式碼範例

請參考同目錄下的範例檔案：

- `templates/apphost-program.cs` - AppHost 編排定義
- `templates/aspire-app-fixture.cs` - 測試基礎設施
- `templates/integration-test-collection.cs` - Collection Fixture 設定
- `templates/integration-test-base.cs` - 測試基底類別
- `templates/database-manager.cs` - 資料庫管理員
- `templates/controller-tests.cs` - 控制器測試範例
- `templates/test-project.csproj` - 測試專案設定
- `templates/apphost-project.csproj` - AppHost 專案設定
