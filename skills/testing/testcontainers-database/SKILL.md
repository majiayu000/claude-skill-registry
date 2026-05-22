---
name: testcontainers-database
description: 協助使用 Testcontainers for .NET 進行容器化資料庫整合測試。當使用者需要測試真實資料庫行為（PostgreSQL、MSSQL）、需要解決 EF Core InMemory 限制、或需要建立容器共享的測試架構時使用此技能。
license: MIT
---

# Testcontainers 資料庫整合測試指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 需要測試真實資料庫行為（交易、並發、預存程序等）
- EF Core InMemory 資料庫無法滿足測試需求
- 建立 PostgreSQL 或 MSSQL 的容器化測試環境
- 使用 Collection Fixture 模式共享容器實例
- 同時測試 EF Core 和 Dapper 的資料存取層
- 需要 SQL 腳本外部化策略

## EF Core InMemory 的限制

在選擇測試策略前，必須了解 EF Core InMemory 資料庫的重大限制：

### 1. 交易行為與資料庫鎖定

- **不支援資料庫交易 (Transactions)**：`SaveChanges()` 後資料立即儲存，無法進行 Rollback
- **無資料庫鎖定機制**：無法模擬並發 (Concurrency) 情境下的行為

### 2. LINQ 查詢差異

- **查詢翻譯差異**：某些 LINQ 查詢（複雜 GroupBy、JOIN、自訂函數）在 InMemory 中可執行，但轉換成 SQL 時可能失敗
- **Case Sensitivity**：InMemory 預設不區分大小寫，但真實資料庫依賴校對規則 (Collation)
- **效能模擬不足**：無法模擬真實資料庫的效能瓶頸或索引問題

### 3. 資料庫特定功能

InMemory 模式無法測試：

- 預存程序 (Stored Procedures) 與 Triggers
- Views
- 外鍵約束 (Foreign Key Constraints)、檢查約束 (Check Constraints)
- 資料類型精確度（decimal、datetime 等）
- Concurrency Tokens（RowVersion、Timestamp）

**結論**：當需要驗證複雜交易邏輯、並發處理、資料庫特定行為時，應使用 Testcontainers 進行整合測試。

## Testcontainers 核心概念

### 什麼是 Testcontainers？

Testcontainers 是一個測試函式庫，提供輕量好用的 API 來啟動 Docker 容器，專門用於整合測試。

### 核心優勢

1. **真實環境測試**：使用真實資料庫，測試實際 SQL 語法與資料庫限制
2. **環境一致性**：確保測試環境與正式環境使用相同服務版本
3. **清潔測試環境**：每個測試有獨立乾淨的環境，容器自動清理
4. **簡化開發環境**：開發者只需 Docker，不需安裝各種服務

## 必要套件

```xml
<ItemGroup>
  <!-- 測試框架 -->
  <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.8.0" />
  <PackageReference Include="xunit" Version="2.9.3" />
  <PackageReference Include="xunit.runner.visualstudio" Version="2.9.3" />
  <PackageReference Include="AwesomeAssertions" Version="9.1.0" />
  
  <!-- Testcontainers 核心套件 -->
  <PackageReference Include="Testcontainers" Version="3.10.0" />
  
  <!-- 資料庫容器 -->
  <PackageReference Include="Testcontainers.PostgreSql" Version="3.10.0" />
  <PackageReference Include="Testcontainers.MsSql" Version="3.10.0" />
  
  <!-- Entity Framework Core -->
  <PackageReference Include="Microsoft.EntityFrameworkCore" Version="9.0.0" />
  <PackageReference Include="Microsoft.EntityFrameworkCore.SqlServer" Version="9.0.0" />
  <PackageReference Include="Npgsql.EntityFrameworkCore.PostgreSQL" Version="9.0.0" />
  
  <!-- Dapper (可選) -->
  <PackageReference Include="Dapper" Version="2.1.35" />
  <PackageReference Include="Microsoft.Data.SqlClient" Version="5.2.2" />
</ItemGroup>
```

> **重要**：使用 `Microsoft.Data.SqlClient` 而非舊版 `System.Data.SqlClient`，提供更好的效能與安全性。

## 環境需求

### Docker Desktop 設定

- Windows 10 版本 2004 或更新版本
- 啟用 WSL 2 功能
- 8GB RAM（建議 16GB 以上）
- 64GB 可用磁碟空間

### 建議的 Docker Desktop Resources 設定

- Memory: 6GB（系統記憶體的 50-75%）
- CPUs: 4 cores
- Swap: 2GB
- Disk image size: 64GB

## 基本容器操作模式

### PostgreSQL 容器

```csharp
public class PostgreSqlTests : IAsyncLifetime
{
    private readonly PostgreSqlContainer _postgres;
    private UserDbContext _dbContext = null!;

    public PostgreSqlTests()
    {
        _postgres = new PostgreSqlBuilder()
            .WithImage("postgres:15-alpine")
            .WithDatabase("testdb")
            .WithUsername("testuser")
            .WithPassword("testpass")
            .WithPortBinding(5432, true)  // 自動分配主機埠號
            .Build();
    }

    public async Task InitializeAsync()
    {
        await _postgres.StartAsync();

        var options = new DbContextOptionsBuilder<UserDbContext>()
            .UseNpgsql(_postgres.GetConnectionString())
            .Options;

        _dbContext = new UserDbContext(options);
        await _dbContext.Database.EnsureCreatedAsync();
    }

    public async Task DisposeAsync()
    {
        await _dbContext.DisposeAsync();
        await _postgres.DisposeAsync();
    }
}
```

### SQL Server 容器

```csharp
public class SqlServerTests : IAsyncLifetime
{
    private readonly MsSqlContainer _container;
    private UserDbContext _dbContext = null!;

    public SqlServerTests()
    {
        _container = new MsSqlBuilder()
            .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
            .WithPassword("YourStrong@Passw0rd")
            .WithCleanUp(true)
            .Build();
    }

    public async Task InitializeAsync()
    {
        await _container.StartAsync();

        var options = new DbContextOptionsBuilder<UserDbContext>()
            .UseSqlServer(_container.GetConnectionString())
            .Options;

        _dbContext = new UserDbContext(options);
        await _dbContext.Database.EnsureCreatedAsync();
    }

    public async Task DisposeAsync()
    {
        await _dbContext.DisposeAsync();
        await _container.DisposeAsync();
    }
}
```

## Collection Fixture 模式：容器共享

### 為什麼需要容器共享？

在大型專案中，每個測試類別都建立新容器會遇到嚴重的效能瓶頸：

- **傳統方式**：每個測試類別啟動一個容器。若有 3 個測試類別，總耗時約 `3 × 10 秒 = 30 秒`
- **Collection Fixture**：所有測試類別共享同一個容器。總耗時僅約 `1 × 10 秒 = 10 秒`

**測試執行時間減少約 67%**

### Collection Fixture 實作

```csharp
/// <summary>
/// MSSQL 容器的 Collection Fixture
/// </summary>
public class SqlServerContainerFixture : IAsyncLifetime
{
    private readonly MsSqlContainer _container;

    public SqlServerContainerFixture()
    {
        _container = new MsSqlBuilder()
            .WithImage("mcr.microsoft.com/mssql/server:2022-latest")
            .WithPassword("Test123456!")
            .WithCleanUp(true)
            .Build();
    }

    public static string ConnectionString { get; private set; } = string.Empty;

    public async Task InitializeAsync()
    {
        await _container.StartAsync();
        ConnectionString = _container.GetConnectionString();
        
        // 等待容器完全啟動
        await Task.Delay(2000);
    }

    public async Task DisposeAsync()
    {
        await _container.DisposeAsync();
    }
}

/// <summary>
/// 定義測試集合
/// </summary>
[CollectionDefinition(nameof(SqlServerCollectionFixture))]
public class SqlServerCollectionFixture : ICollectionFixture<SqlServerContainerFixture>
{
    // 此類別只是用來定義 Collection，不需要實作內容
}
```

### 測試類別整合

```csharp
[Collection(nameof(SqlServerCollectionFixture))]
public class EfCoreTests : IDisposable
{
    private readonly ECommerceDbContext _dbContext;

    public EfCoreTests(ITestOutputHelper testOutputHelper)
    {
        var connectionString = SqlServerContainerFixture.ConnectionString;

        var options = new DbContextOptionsBuilder<ECommerceDbContext>()
            .UseSqlServer(connectionString)
            .EnableSensitiveDataLogging()
            .LogTo(testOutputHelper.WriteLine, LogLevel.Information)
            .Options;

        _dbContext = new ECommerceDbContext(options);
        _dbContext.Database.EnsureCreated();
    }

    public void Dispose()
    {
        // 按照外鍵約束順序清理資料
        _dbContext.Database.ExecuteSqlRaw("DELETE FROM OrderItems");
        _dbContext.Database.ExecuteSqlRaw("DELETE FROM Orders");
        _dbContext.Database.ExecuteSqlRaw("DELETE FROM Products");
        _dbContext.Database.ExecuteSqlRaw("DELETE FROM Categories");
        _dbContext.Dispose();
    }
}
```

## SQL 腳本外部化策略

### 為什麼需要外部化 SQL 腳本？

- **關注點分離**：C# 程式碼專注於測試邏輯，SQL 腳本專注於資料庫結構
- **可維護性**：修改資料庫結構時，只需編輯 `.sql` 檔案
- **可讀性**：C# 程式碼變得更簡潔
- **工具支援**：SQL 檔案可獲得編輯器的語法高亮和格式化支援
- **版本控制友善**：SQL 變更可在版本控制系統中清楚追蹤

### 資料夾結構

```text
tests/DatabaseTesting.Tests/
├── SqlScripts/
│   ├── Tables/
│   │   ├── CreateCategoriesTable.sql
│   │   ├── CreateProductsTable.sql
│   │   ├── CreateOrdersTable.sql
│   │   └── CreateOrderItemsTable.sql
│   └── StoredProcedures/
│       └── GetProductSalesReport.sql
```

### .csproj 設定

```xml
<ItemGroup>
  <Content Include="SqlScripts\**\*.sql">
    <CopyToOutputDirectory>Always</CopyToOutputDirectory>
  </Content>
</ItemGroup>
```

### 腳本載入實作

```csharp
private void EnsureTablesExist()
{
    var scriptDirectory = Path.Combine(AppContext.BaseDirectory, "SqlScripts");
    if (!Directory.Exists(scriptDirectory)) return;

    // 按照依賴順序執行表格建立腳本
    var orderedScripts = new[]
    {
        "Tables/CreateCategoriesTable.sql",
        "Tables/CreateProductsTable.sql",
        "Tables/CreateOrdersTable.sql",
        "Tables/CreateOrderItemsTable.sql"
    };

    foreach (var scriptPath in orderedScripts)
    {
        var fullPath = Path.Combine(scriptDirectory, scriptPath);
        if (File.Exists(fullPath))
        {
            var script = File.ReadAllText(fullPath);
            _dbContext.Database.ExecuteSqlRaw(script);
        }
    }
}
```

## Wait Strategy 最佳實務

### 內建 Wait Strategy

```csharp
// 等待特定埠號可用
var postgres = new PostgreSqlBuilder()
    .WithWaitStrategy(Wait.ForUnixContainer()
        .UntilPortIsAvailable(5432))
    .Build();

// 等待日誌訊息出現
var sqlServer = new MsSqlBuilder()
    .WithWaitStrategy(Wait.ForUnixContainer()
        .UntilPortIsAvailable(1433)
        .UntilMessageIsLogged("SQL Server is now ready for client connections"))
    .Build();
```

## EF Core 進階功能測試

### Include/ThenInclude 多層關聯查詢

```csharp
[Fact]
public async Task GetProductWithCategoryAndTagsAsync_載入完整關聯資料_應正確載入()
{
    // Arrange
    await CreateProductWithCategoryAndTagsAsync();

    // Act
    var product = await _repository.GetProductWithCategoryAndTagsAsync(1);

    // Assert
    product.Should().NotBeNull();
    product!.Category.Should().NotBeNull();
    product.ProductTags.Should().NotBeEmpty();
}
```

### AsSplitQuery 避免笛卡兒積

```csharp
[Fact]
public async Task GetProductsByCategoryWithSplitQueryAsync_使用分割查詢_應避免笛卡兒積()
{
    // Arrange
    await CreateMultipleProductsWithTagsAsync();

    // Act
    var products = await _repository.GetProductsByCategoryWithSplitQueryAsync(1);

    // Assert
    products.Should().NotBeEmpty();
    products.All(p => p.ProductTags.Any()).Should().BeTrue();
}
```

> **笛卡兒積問題**：當一個查詢 JOIN 多個一對多關聯時，會為每個可能的組合產生一列資料。`AsSplitQuery()` 將查詢分解成多個獨立 SQL 查詢，在記憶體中組合結果，避免此問題。

### N+1 查詢問題驗證

```csharp
[Fact]
public async Task N1QueryProblemVerification_對比Repository方法_應展示效率差異()
{
    // Arrange
    await CreateCategoriesWithProductsAsync();

    // Act 1: 測試有問題的方法
    var categoriesWithProblem = await _repository.GetCategoriesWithN1ProblemAsync();

    // Act 2: 測試最佳化方法
    var categoriesOptimized = await _repository.GetCategoriesWithProductsOptimizedAsync();

    // Assert
    categoriesOptimized.All(c => c.Products.Any()).Should().BeTrue();
}
```

### AsNoTracking 唯讀查詢最佳化

```csharp
[Fact]
public async Task GetProductsWithNoTrackingAsync_唯讀查詢_不應追蹤實體()
{
    // Arrange
    await CreateMultipleProductsAsync();

    // Act
    var products = await _repository.GetProductsWithNoTrackingAsync(500m);

    // Assert
    products.Should().NotBeEmpty();
    var trackedEntities = _dbContext.ChangeTracker.Entries<Product>().Count();
    trackedEntities.Should().Be(0, "AsNoTracking 查詢不應追蹤實體");
}
```

## Dapper 進階功能測試

### 基本 CRUD 測試

```csharp
[Collection(nameof(SqlServerCollectionFixture))]
public class DapperCrudTests : IDisposable
{
    private readonly IDbConnection _connection;
    private readonly IProductRepository _productRepository;

    public DapperCrudTests()
    {
        var connectionString = SqlServerContainerFixture.ConnectionString;
        _connection = new SqlConnection(connectionString);
        _connection.Open();

        _productRepository = new DapperProductRepository(connectionString);
        EnsureTablesExist();
    }

    public void Dispose()
    {
        _connection.Execute("DELETE FROM Products");
        _connection.Execute("DELETE FROM Categories");
        _connection.Close();
        _connection.Dispose();
    }
}
```

### QueryMultiple 一對多關聯處理

```csharp
public async Task<Product?> GetProductWithTagsAsync(int productId)
{
    const string sql = @"
        SELECT * FROM Products WHERE Id = @ProductId;
        SELECT t.* FROM Tags t
        INNER JOIN ProductTags pt ON t.Id = pt.TagId
        WHERE pt.ProductId = @ProductId;";

    using var multi = await _connection.QueryMultipleAsync(sql, new { ProductId = productId });
    var product = await multi.ReadSingleOrDefaultAsync<Product>();
    if (product != null)
    {
        product.Tags = (await multi.ReadAsync<Tag>()).ToList();
    }
    return product;
}
```

### DynamicParameters 動態查詢

```csharp
public async Task<IEnumerable<Product>> SearchProductsAsync(
    int? categoryId = null,
    decimal? minPrice = null,
    bool? isActive = null)
{
    var sql = new StringBuilder("SELECT * FROM Products WHERE 1=1");
    var parameters = new DynamicParameters();

    if (categoryId.HasValue)
    {
        sql.Append(" AND CategoryId = @CategoryId");
        parameters.Add("CategoryId", categoryId.Value);
    }

    if (minPrice.HasValue)
    {
        sql.Append(" AND Price >= @MinPrice");
        parameters.Add("MinPrice", minPrice.Value);
    }

    if (isActive.HasValue)
    {
        sql.Append(" AND IsActive = @IsActive");
        parameters.Add("IsActive", isActive.Value);
    }

    return await _connection.QueryAsync<Product>(sql.ToString(), parameters);
}
```

## Repository Pattern 設計原則

### 介面分離原則 (ISP) 的應用

```csharp
/// <summary>
/// 基礎 CRUD 操作介面
/// </summary>
public interface IProductRepository
{
    Task<IEnumerable<Product>> GetAllAsync();
    Task<Product?> GetByIdAsync(int id);
    Task AddAsync(Product product);
    Task UpdateAsync(Product product);
    Task DeleteAsync(int id);
}

/// <summary>
/// EF Core 特有的進階功能介面
/// </summary>
public interface IProductByEFCoreRepository
{
    Task<Product?> GetProductWithCategoryAndTagsAsync(int productId);
    Task<IEnumerable<Product>> GetProductsByCategoryWithSplitQueryAsync(int categoryId);
    Task<int> BatchUpdateProductPricesAsync(int categoryId, decimal priceMultiplier);
    Task<IEnumerable<Product>> GetProductsWithNoTrackingAsync(decimal minPrice);
}

/// <summary>
/// Dapper 特有的進階功能介面
/// </summary>
public interface IProductByDapperRepository
{
    Task<Product?> GetProductWithTagsAsync(int productId);
    Task<IEnumerable<Product>> SearchProductsAsync(int? categoryId, decimal? minPrice, bool? isActive);
    Task<IEnumerable<ProductSalesReport>> GetProductSalesReportAsync(decimal minPrice);
}
```

### 設計優勢

1. **單一職責原則 (SRP)**：每個介面專注於特定職責
2. **介面隔離原則 (ISP)**：使用者只需依賴所需的介面
3. **依賴反轉原則 (DIP)**：高層模組依賴抽象而非具體實作
4. **測試隔離性**：可針對特定功能進行精準測試

## 常見問題處理

### Docker 容器啟動失敗

```bash
# 檢查連接埠是否被佔用
netstat -an | findstr :5432

# 清理未使用的映像檔
docker system prune -a
```

### 記憶體不足問題

- 調整 Docker Desktop 記憶體配置
- 限制同時執行的容器數量
- 使用 Collection Fixture 共享容器

### 測試資料隔離

```csharp
public void Dispose()
{
    // 按照外鍵約束順序清理資料
    _dbContext.Database.ExecuteSqlRaw("DELETE FROM OrderItems");
    _dbContext.Database.ExecuteSqlRaw("DELETE FROM Orders");
    _dbContext.Database.ExecuteSqlRaw("DELETE FROM Products");
    _dbContext.Database.ExecuteSqlRaw("DELETE FROM Categories");
    _dbContext.Dispose();
}
```

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 20 - Testcontainers 初探：使用 Docker 架設測試環境**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375882
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day20

- **Day 21 - Testcontainers 整合測試：MSSQL + EF Core 以及 Dapper 基礎應用**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375990
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day21

### 官方文件

- [Testcontainers 官方網站](https://testcontainers.com/)
- [Testcontainers for .NET](https://dotnet.testcontainers.org/)
- [Testcontainers for .NET / Modules](https://dotnet.testcontainers.org/modules/)
