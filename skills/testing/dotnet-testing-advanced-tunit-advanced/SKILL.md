---
name: dotnet-testing-advanced-tunit-advanced
description: |
  TUnit 進階應用完整指南 - 資料驅動測試、依賴注入與整合測試實戰。涵蓋 MethodDataSource、ClassDataSource、Matrix Tests、Properties 過濾。包含 Retry/Timeout 控制、WebApplicationFactory 整合、Testcontainers 多服務編排。
  Keywords: TUnit advanced, TUnit 進階, MethodDataSource, ClassDataSource, Matrix Tests, MatrixDataSource, MicrosoftDependencyInjectionDataSource, Property, Retry, Timeout, 資料驅動測試, 測試過濾, WebApplicationFactory TUnit, 多容器編排
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: "tunit, advanced-testing, data-driven, dependency-injection, integration-testing, testcontainers"
---

# TUnit 進階應用：資料驅動測試、依賴注入與整合測試實戰

## 技能概述

本技能涵蓋 TUnit 進階應用技巧，從資料驅動測試到依賴注入，從執行控制到 ASP.NET Core 整合測試實戰。

**核心主題：**

- 資料驅動測試進階技巧 (MethodDataSource、ClassDataSource、Matrix Tests)
- Properties 屬性標記與測試過濾
- 測試生命週期與依賴注入
- 執行控制 (Retry、Timeout、DisplayName)
- ASP.NET Core 整合測試 (WebApplicationFactory)
- 效能測試與負載測試
- TUnit + Testcontainers 複雜基礎設施編排
- TUnit Engine Modes 與疑難排解

---

## 資料驅動測試進階技巧

### 資料來源方式比較

| 資料來源方式         | 適用場景           | 優勢       | 注意事項         |
| :------------------- | :----------------- | :--------- | :--------------- |
| **Arguments**        | 簡單固定資料       | 語法簡潔   | 資料量不宜過大   |
| **MethodDataSource** | 動態資料、複雜物件 | 最大靈活性 | 需要額外方法定義 |
| **ClassDataSource**  | 共享資料、依賴注入 | 可重用性高 | 類別生命週期管理 |
| **Matrix Tests**     | 組合測試           | 覆蓋率高   | 容易產生過多測試 |

### MethodDataSource：方法作為資料來源

最靈活的資料提供方式，適合動態產生或從外部來源載入資料：

```csharp
[Test]
[MethodDataSource(nameof(GetOrderTestData))]
public async Task CreateOrder_各種情況_應正確處理(
    string customerId, 
    CustomerLevel level, 
    List<OrderItem> items, 
    decimal expectedTotal)
{
    // Arrange
    var orderService = new OrderService(_repository, _discountCalculator, _shippingCalculator, _logger);

    // Act
    var order = await orderService.CreateOrderAsync(customerId, level, items);

    // Assert
    await Assert.That(order).IsNotNull();
    await Assert.That(order.CustomerId).IsEqualTo(customerId);
    await Assert.That(order.TotalAmount).IsEqualTo(expectedTotal);
}

public static IEnumerable<object[]> GetOrderTestData()
{
    // 一般會員訂單
    yield return new object[]
    {
        "CUST001",
        CustomerLevel.一般會員,
        new List<OrderItem>
        {
            new() { ProductId = "PROD001", ProductName = "商品A", UnitPrice = 100m, Quantity = 2 }
        },
        200m
    };

    // VIP會員訂單
    yield return new object[]
    {
        "CUST002", 
        CustomerLevel.VIP會員,
        new List<OrderItem>
        {
            new() { ProductId = "PROD002", ProductName = "商品B", UnitPrice = 500m, Quantity = 1 }
        },
        500m
    };
}
```

**從檔案載入測試資料：**

```csharp
[Test]
[MethodDataSource(nameof(GetDiscountTestDataFromFile))]
public async Task CalculateDiscount_從檔案讀取_應套用正確折扣(
    string scenario, 
    decimal originalAmount, 
    CustomerLevel level, 
    string discountCode, 
    decimal expectedDiscount)
{
    var calculator = new DiscountCalculator(new MockDiscountRepository(), new MockLogger<DiscountCalculator>());
    var order = new Order
    {
        CustomerLevel = level,
        Items = [new OrderItem { UnitPrice = originalAmount, Quantity = 1 }]
    };

    var discount = await calculator.CalculateDiscountAsync(order, discountCode);

    await Assert.That(discount).IsEqualTo(expectedDiscount);
}

public static IEnumerable<object[]> GetDiscountTestDataFromFile()
{
    var filePath = Path.Combine("TestData", "discount-scenarios.json");
    var jsonData = File.ReadAllText(filePath);
    var scenarios = JsonSerializer.Deserialize<List<DiscountScenario>>(jsonData);
    if (scenarios == null) yield break;
    
    foreach (var s in scenarios)
    {
        yield return new object[] { s.Scenario, s.Amount, (CustomerLevel)s.Level, s.Code, s.Expected };
    }
}
```

### ClassDataSource：類別作為資料提供者

當測試資料需要共享給多個測試類別時使用：

```csharp
[Test]
[ClassDataSource<OrderValidationTestData>]
public async Task ValidateOrder_各種驗證情況_應回傳正確結果(OrderValidationScenario scenario)
{
    var validator = new OrderValidator(_discountRepository, _logger);
    var result = await validator.ValidateAsync(scenario.Order);

    await Assert.That(result.IsValid).IsEqualTo(scenario.ExpectedValid);
    if (!scenario.ExpectedValid)
    {
        await Assert.That(result.ErrorMessage).Contains(scenario.ExpectedErrorKeyword);
    }
}

public class OrderValidationTestData : IEnumerable<OrderValidationScenario>
{
    public IEnumerator<OrderValidationScenario> GetEnumerator()
    {
        yield return new OrderValidationScenario
        {
            Name = "有效的一般訂單",
            Order = CreateValidOrder(),
            ExpectedValid = true,
            ExpectedErrorKeyword = null
        };

        yield return new OrderValidationScenario
        {
            Name = "客戶ID為空",
            Order = CreateOrderWithEmptyCustomerId(),
            ExpectedValid = false,
            ExpectedErrorKeyword = "客戶ID"
        };
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    private static Order CreateValidOrder() => new()
    {
        CustomerId = "CUST001",
        CustomerLevel = CustomerLevel.一般會員,
        Items = new List<OrderItem>
        {
            new() { ProductId = "PROD001", ProductName = "測試商品", UnitPrice = 100m, Quantity = 1 }
        }
    };

    private static Order CreateOrderWithEmptyCustomerId() => new()
    {
        CustomerId = "",
        CustomerLevel = CustomerLevel.一般會員,
        Items = new List<OrderItem>
        {
            new() { ProductId = "PROD001", ProductName = "測試商品", UnitPrice = 100m, Quantity = 1 }
        }
    };
}
```

**AutoFixture 整合：**

```csharp
public class AutoFixtureOrderTestData : IEnumerable<Order>
{
    private readonly Fixture _fixture;

    public AutoFixtureOrderTestData()
    {
        _fixture = new Fixture();
        
        _fixture.Customize<Order>(composer => composer
            .With(o => o.CustomerId, () => $"CUST{_fixture.Create<int>() % 1000:D3}")
            .With(o => o.CustomerLevel, () => _fixture.Create<CustomerLevel>())
            .With(o => o.Items, () => _fixture.CreateMany<OrderItem>(Random.Shared.Next(1, 5)).ToList()));

        _fixture.Customize<OrderItem>(composer => composer
            .With(oi => oi.ProductId, () => $"PROD{_fixture.Create<int>() % 1000:D3}")
            .With(oi => oi.ProductName, () => $"測試商品{_fixture.Create<int>() % 100}")
            .With(oi => oi.UnitPrice, () => Math.Round(_fixture.Create<decimal>() % 1000 + 1, 2))
            .With(oi => oi.Quantity, () => _fixture.Create<int>() % 10 + 1));
    }

    public IEnumerator<Order> GetEnumerator()
    {
        for (int i = 0; i < 5; i++)
        {
            yield return _fixture.Create<Order>();
        }
    }

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();
}
```

### Matrix Tests：組合測試

自動產生所有參數組合的測試案例：

```csharp
[Test]
[MatrixDataSource]
public async Task CalculateShipping_客戶等級與金額組合_應遵循運費規則(
    [Matrix(0, 1, 2, 3)] CustomerLevel customerLevel, // 0=一般會員, 1=VIP會員, 2=白金會員, 3=鑽石會員
    [Matrix(100, 500, 1000, 2000)] decimal orderAmount)
{
    // Arrange
    var calculator = new ShippingCalculator();
    var order = new Order
    {
        CustomerLevel = customerLevel,
        Items = [new OrderItem { UnitPrice = orderAmount, Quantity = 1 }]
    };

    // Act
    var shippingFee = calculator.CalculateShippingFee(order);
    var isFreeShipping = calculator.IsEligibleForFreeShipping(order);

    // Assert
    if (isFreeShipping)
    {
        await Assert.That(shippingFee).IsEqualTo(0m);
    }
    else
    {
        await Assert.That(shippingFee).IsGreaterThan(0m);
    }

    // 驗證特定規則
    switch (customerLevel)
    {
        case CustomerLevel.鑽石會員:
            await Assert.That(shippingFee).IsEqualTo(0m); // 鑽石會員永遠免運
            break;
        case CustomerLevel.VIP會員 or CustomerLevel.白金會員:
            if (orderAmount < 1000m)
                await Assert.That(shippingFee).IsEqualTo(40m); // VIP+ 運費半價
            break;
        case CustomerLevel.一般會員:
            if (orderAmount < 1000m)
                await Assert.That(shippingFee).IsEqualTo(80m); // 一般會員標準運費
            break;
    }
}
```

**⚠️ Matrix Tests 注意事項：**

- 使用 `[MatrixDataSource]` 屬性標記測試方法
- 由於 C# 屬性限制，enum 必須用數值表示
- 限制參數組合數量，避免超過 50-100 個案例
- 這會產生 4 × 4 = 16 個測試案例

---

## Properties 屬性標記與測試過濾

### 基本 Properties 使用

```csharp
[Test]
[Property("Category", "Database")]
[Property("Priority", "High")]
public async Task DatabaseTest_高優先級_應能透過屬性過濾()
{
    await Assert.That(true).IsTrue();
}

[Test]
[Property("Category", "Unit")]
[Property("Priority", "Medium")]
public async Task UnitTest_中等優先級_基本驗證()
{
    await Assert.That(1 + 1).IsEqualTo(2);
}

[Test]
[Property("Category", "Integration")]
[Property("Priority", "Low")]
[Property("Environment", "Development")]
public async Task IntegrationTest_低優先級_僅開發環境執行()
{
    await Assert.That("Hello World").Contains("World");
}
```

### 建立一致的屬性命名規範

```csharp
public static class TestProperties
{
    // 測試類別
    public const string CATEGORY_UNIT = "Unit";
    public const string CATEGORY_INTEGRATION = "Integration";
    public const string CATEGORY_E2E = "E2E";
    
    // 優先級
    public const string PRIORITY_CRITICAL = "Critical";
    public const string PRIORITY_HIGH = "High";
    public const string PRIORITY_MEDIUM = "Medium";
    public const string PRIORITY_LOW = "Low";
    
    // 環境
    public const string ENV_DEVELOPMENT = "Development";
    public const string ENV_STAGING = "Staging";
    public const string ENV_PRODUCTION = "Production";
}

[Test]
[Property("Category", TestProperties.CATEGORY_UNIT)]
[Property("Priority", TestProperties.PRIORITY_HIGH)]
public async Task ExampleTest_使用常數_確保一致性()
{
    await Assert.That(1 + 1).IsEqualTo(2);
}
```

### TUnit 測試過濾執行

TUnit 使用 `dotnet run` 而不是 `dotnet test`：

```bash
# 只執行單元測試
dotnet run --treenode-filter "/*/*/*/*[Category=Unit]"

# 只執行高優先級測試
dotnet run --treenode-filter "/*/*/*/*[Priority=High]"

# 組合條件：執行高優先級的單元測試
dotnet run --treenode-filter "/*/*/*/*[(Category=Unit)&(Priority=High)]"

# 或條件：執行單元測試或冒煙測試
dotnet run --treenode-filter "/*/*/*/*[(Category=Unit)|(Suite=Smoke)]"

# 執行特定功能的測試
dotnet run --treenode-filter "/*/*/*/*[Feature=OrderProcessing]"
```

**過濾語法注意事項：**
- 路徑模式 `/*/*/*/*` 代表 Assembly/Namespace/Class/Method 層級
- 屬性名稱大小寫敏感
- 組合條件必須用括號正確包圍

---

## 測試生命週期管理

### 生命週期方法概述

| 生命週期方法      | 執行時機                 | 適用場景                         |
| :---------------- | :----------------------- | :------------------------------- |
| `[Before(Class)]` | 類別中第一個測試開始前   | 昂貴的資源初始化（如資料庫連線） |
| `建構式`          | 每個測試開始前           | 測試實例的基本設定               |
| `[Before(Test)]`  | 每個測試方法執行前       | 測試特定的前置作業               |
| `測試方法`        | 實際測試執行             | 測試邏輯本身                     |
| `[After(Test)]`   | 每個測試方法執行後       | 測試特定的清理作業               |
| `Dispose`         | 測試實例銷毀時           | 釋放測試實例的資源               |
| `[After(Class)]`  | 類別中最後一個測試完成後 | 清理共享資源                     |

### Before/After 屬性家族

```csharp
// Before 屬性
[Before(Test)]           // 實例方法 - 每個測試前執行
[Before(Class)]          // 靜態方法 - 類別第一個測試前執行一次
[Before(Assembly)]       // 靜態方法 - 組件第一個測試前執行一次
[Before(TestSession)]    // 靜態方法 - 測試會話開始前執行一次

// After 屬性
[After(Test)]           // 實例方法 - 每個測試後執行
[After(Class)]          // 靜態方法 - 類別最後一個測試後執行一次
[After(Assembly)]       // 靜態方法 - 組件最後一個測試後執行一次
[After(TestSession)]    // 靜態方法 - 測試會話結束後執行一次

// 全域鉤子
[BeforeEvery(Test)]     // 靜態方法 - 每個測試前都執行（全域）
[AfterEvery(Test)]      // 靜態方法 - 每個測試後都執行（全域）
```

### 實際範例

```csharp
public class LifecycleTests
{
    private readonly StringBuilder _logBuilder;
    private static readonly List<string> ClassLog = [];

    public LifecycleTests()
    {
        Console.WriteLine("1. 建構式執行 - 測試實例建立");
        _logBuilder = new StringBuilder();
    }

    [Before(Class)]
    public static async Task BeforeClass()
    {
        Console.WriteLine("2. BeforeClass 執行 - 類別層級初始化");
        ClassLog.Add("BeforeClass 執行");
        await Task.Delay(10);
    }

    [Before(Test)]
    public async Task BeforeTest()
    {
        Console.WriteLine("3. BeforeTest 執行 - 測試前置設定");
        _logBuilder.AppendLine("BeforeTest 執行");
        await Task.Delay(5);
    }

    [Test]
    public async Task TestMethod_應按正確順序執行生命週期方法()
    {
        Console.WriteLine("4. TestMethod 執行");
        await Assert.That(ClassLog).Contains("BeforeClass 執行");
    }

    [After(Test)]
    public async Task AfterTest()
    {
        Console.WriteLine("5. AfterTest 執行 - 測試後清理");
        await Task.Delay(5);
    }

    [After(Class)]
    public static async Task AfterClass()
    {
        Console.WriteLine("6. AfterClass 執行 - 類別層級清理");
        await Task.Delay(10);
    }
}
```

**重要觀察：**

1. **建構式優先級**：永遠在所有 TUnit 生命週期屬性之前執行
2. **BeforeClass 只執行一次**：在所有測試開始前執行一次
3. **測試執行是並行的**：多個測試方法可能同時執行
4. **AfterClass 只執行一次**：在所有測試完成後執行一次

---

## 依賴注入模式

### TUnit 依賴注入核心概念

TUnit 的依賴注入建構在 Data Source Generators 基礎上：

```csharp
public class MicrosoftDependencyInjectionDataSourceAttribute : DependencyInjectionDataSourceAttribute<IServiceScope>
{
    private static readonly IServiceProvider ServiceProvider = CreateSharedServiceProvider();

    public override IServiceScope CreateScope(DataGeneratorMetadata dataGeneratorMetadata)
    {
        return ServiceProvider.CreateScope();
    }

    public override object? Create(IServiceScope scope, Type type)
    {
        return scope.ServiceProvider.GetService(type);
    }

    private static IServiceProvider CreateSharedServiceProvider()
    {
        return new ServiceCollection()
            .AddSingleton<IOrderRepository, MockOrderRepository>()
            .AddSingleton<IDiscountCalculator, MockDiscountCalculator>()
            .AddSingleton<IShippingCalculator, MockShippingCalculator>()
            .AddSingleton<ILogger<OrderService>, MockLogger<OrderService>>()
            .AddTransient<OrderService>()
            .BuildServiceProvider();
    }
}
```

### 使用 TUnit 依賴注入

```csharp
[MicrosoftDependencyInjectionDataSource]
public class DependencyInjectionTests(OrderService orderService)
{
    [Test]
    public async Task CreateOrder_使用TUnit依賴注入_應正確運作()
    {
        // Arrange - 依賴已經透過 TUnit DI 自動注入
        var items = new List<OrderItem>
        {
            new() { ProductId = "PROD001", ProductName = "測試商品", UnitPrice = 100m, Quantity = 2 }
        };

        // Act
        var order = await orderService.CreateOrderAsync("CUST001", CustomerLevel.VIP會員, items);

        // Assert
        await Assert.That(order).IsNotNull();
        await Assert.That(order.CustomerId).IsEqualTo("CUST001");
        await Assert.That(order.CustomerLevel).IsEqualTo(CustomerLevel.VIP會員);
    }

    [Test]
    public async Task TUnitDependencyInjection_驗證自動注入_服務應為正確類型()
    {
        await Assert.That(orderService).IsNotNull();
        await Assert.That(orderService.GetType().Name).IsEqualTo("OrderService");
    }
}
```

### TUnit DI vs 手動依賴建立比較

| 特性           | TUnit DI                 | 手動依賴建立               |
| :------------- | :----------------------- | :------------------------- |
| **設定複雜度** | 一次設定，重複使用       | 每個測試都需要手動建立     |
| **可維護性**   | 依賴變更只需修改一個地方 | 需要修改所有使用的測試     |
| **一致性**     | 與產品程式碼的 DI 一致   | 可能與實際應用程式不一致   |
| **測試可讀性** | 專注於測試邏輯           | 被依賴建立程式碼干擾       |
| **範圍管理**   | 自動管理服務範圍         | 需要手動管理物件生命週期   |
| **錯誤風險**   | 框架保證依賴正確注入     | 可能遺漏或錯誤建立某些依賴 |

---

## 執行控制與測試品質

### Retry 機制：智慧重試策略

```csharp
[Test]
[Retry(3)] // 如果失敗，重試最多 3 次
[Property("Category", "Flaky")]
public async Task NetworkCall_可能不穩定_使用重試機制()
{
    var random = new Random();
    var success = random.Next(1, 4) == 1; // 約 33% 的成功率

    if (!success)
    {
        throw new HttpRequestException("模擬網路錯誤");
    }

    await Assert.That(success).IsTrue();
}
```

**適合使用 Retry 的情況：**

1. 外部服務呼叫：API 請求、資料庫連線可能因網路問題暫時失敗
2. 檔案系統操作：在 CI/CD 環境中，檔案鎖定可能導致暫時性失敗
3. 並行測試競爭：多個測試同時存取共享資源時的競爭條件

**不適合使用 Retry 的情況：**

1. 邏輯錯誤：程式碼本身的錯誤重試多少次都不會成功
2. 預期的例外：測試本身就是要驗證例外情況
3. 效能測試：重試會影響效能測量的準確性

### Timeout 控制：長時間測試管理

```csharp
[Test]
[Timeout(5000)] // 5 秒超時
[Property("Category", "Performance")]
public async Task LongRunningOperation_應在時限內完成()
{
    await Task.Delay(1000); // 1 秒操作，應該在 5 秒限制內
    await Assert.That(true).IsTrue();
}

[Test]
[Timeout(1000)] // 確保不會超過 1 秒
[Property("Category", "Performance")]
[Property("Baseline", "true")]
public async Task SearchFunction_效能基準_應符合SLA要求()
{
    var stopwatch = Stopwatch.StartNew();
    
    var searchResults = await PerformSearch("test query");
    
    stopwatch.Stop();
    
    await Assert.That(searchResults).IsNotNull();
    await Assert.That(searchResults.Count()).IsGreaterThan(0);
    await Assert.That(stopwatch.ElapsedMilliseconds).IsLessThan(500);
}
```

### DisplayName：自訂測試名稱

```csharp
[Test]
[DisplayName("自訂測試名稱：驗證使用者註冊流程")]
public async Task UserRegistration_CustomDisplayName_測試名稱更易讀()
{
    await Assert.That("user@example.com").Contains("@");
}

// 參數化測試的動態顯示名稱
[Test]
[Arguments("valid@email.com", true)]
[Arguments("invalid-email", false)]
[Arguments("", false)]
[DisplayName("電子郵件驗證：{0} 應為 {1}")]
public async Task EmailValidation_參數化顯示名稱(string email, bool expectedValid)
{
    var isValid = !string.IsNullOrEmpty(email) && email.Contains("@") && email.Contains(".");
    await Assert.That(isValid).IsEqualTo(expectedValid);
}

// 業務場景驅動的顯示名稱
[Test]
[Arguments(CustomerLevel.一般會員, 1000, 0)]
[Arguments(CustomerLevel.VIP會員, 1000, 50)]
[Arguments(CustomerLevel.白金會員, 1000, 100)]
[DisplayName("會員等級 {0} 購買 ${1} 應獲得 ${2} 折扣")]
public async Task MemberDiscount_根據會員等級_計算正確折扣(
    CustomerLevel level, decimal amount, decimal expectedDiscount)
{
    var calculator = new DiscountCalculator();
    var discount = await calculator.CalculateDiscountAsync(amount, level);
    await Assert.That(discount).IsEqualTo(expectedDiscount);
}
```

---

## ASP.NET Core 整合測試

### WebApplicationFactory 與 TUnit 的整合

```csharp
public class WebApiIntegrationTests : IDisposable
{
    private readonly WebApplicationFactory<Program> _factory;
    private readonly HttpClient _client;

    public WebApiIntegrationTests()
    {
        _factory = new WebApplicationFactory<Program>()
            .WithWebHostBuilder(builder =>
            {
                builder.ConfigureServices(services =>
                {
                    services.AddLogging();
                });
            });

        _client = _factory.CreateClient();
    }

    [Test]
    public async Task WeatherForecast_Get_應回傳正確格式的資料()
    {
        var response = await _client.GetAsync("/weatherforecast");

        await Assert.That(response.IsSuccessStatusCode).IsTrue();

        var content = await response.Content.ReadAsStringAsync();
        await Assert.That(content).IsNotNull();
        await Assert.That(content.Length).IsGreaterThan(0);
    }

    [Test]
    [Property("Category", "Integration")]
    public async Task WeatherForecast_ResponseHeaders_應包含ContentType標頭()
    {
        var response = await _client.GetAsync("/weatherforecast");

        await Assert.That(response.IsSuccessStatusCode).IsTrue();
        
        var contentType = response.Content.Headers.ContentType?.MediaType;
        await Assert.That(contentType).IsEqualTo("application/json");
    }

    public void Dispose()
    {
        _client?.Dispose();
        _factory?.Dispose();
    }
}
```

### 效能測試與負載測試

```csharp
[Test]
[Property("Category", "Performance")]
[Timeout(10000)]
public async Task WeatherForecast_ResponseTime_應在合理範圍內()
{
    var stopwatch = Stopwatch.StartNew();

    var response = await _client.GetAsync("/weatherforecast");
    stopwatch.Stop();

    await Assert.That(response.IsSuccessStatusCode).IsTrue();
    await Assert.That(stopwatch.ElapsedMilliseconds).IsLessThan(5000);
}

[Test]
[Property("Category", "Load")]
[Timeout(30000)]
public async Task WeatherForecast_並行請求_應能正確處理()
{
    const int concurrentRequests = 50;
    var tasks = new List<Task<HttpResponseMessage>>();

    for (int i = 0; i < concurrentRequests; i++)
    {
        tasks.Add(_client.GetAsync("/weatherforecast"));
    }

    var responses = await Task.WhenAll(tasks);

    await Assert.That(responses.Length).IsEqualTo(concurrentRequests);
    await Assert.That(responses.All(r => r.IsSuccessStatusCode)).IsTrue();

    foreach (var response in responses)
    {
        response.Dispose();
    }
}
```

---

## TUnit + Testcontainers 基礎設施編排

### 使用 [Before(Assembly)] 和 [After(Assembly)] 管理容器

```csharp
public static class GlobalTestInfrastructureSetup
{
    public static PostgreSqlContainer? PostgreSqlContainer { get; private set; }
    public static RedisContainer? RedisContainer { get; private set; }
    public static KafkaContainer? KafkaContainer { get; private set; }
    public static INetwork? Network { get; private set; }

    [Before(Assembly)]
    public static async Task SetupGlobalInfrastructure()
    {
        Console.WriteLine("=== 開始設置全域測試基礎設施 ===");

        // 建立網路
        Network = new NetworkBuilder()
            .WithName("global-test-network")
            .Build();

        await Network.CreateAsync();

        // 建立 PostgreSQL 容器
        PostgreSqlContainer = new PostgreSqlBuilder()
            .WithDatabase("test_db")
            .WithUsername("test_user")
            .WithPassword("test_password")
            .WithNetwork(Network)
            .WithCleanUp(true)
            .Build();

        await PostgreSqlContainer.StartAsync();

        // 建立 Redis 容器
        RedisContainer = new RedisBuilder()
            .WithNetwork(Network)
            .WithCleanUp(true)
            .Build();

        await RedisContainer.StartAsync();

        // 建立 Kafka 容器
        KafkaContainer = new KafkaBuilder()
            .WithNetwork(Network)
            .WithCleanUp(true)
            .Build();

        await KafkaContainer.StartAsync();

        Console.WriteLine("=== 全域測試基礎設施設置完成 ===");
    }

    [After(Assembly)]
    public static async Task TeardownGlobalInfrastructure()
    {
        Console.WriteLine("=== 開始清理全域測試基礎設施 ===");

        if (KafkaContainer != null)
            await KafkaContainer.DisposeAsync();

        if (RedisContainer != null)
            await RedisContainer.DisposeAsync();

        if (PostgreSqlContainer != null)
            await PostgreSqlContainer.DisposeAsync();

        if (Network != null)
            await Network.DeleteAsync();

        Console.WriteLine("=== 全域測試基礎設施清理完成 ===");
    }
}
```

### 使用全域容器進行測試

```csharp
public class ComplexInfrastructureTests
{
    [Test]
    [Property("Category", "Integration")]
    [Property("Infrastructure", "Complex")]
    [DisplayName("多服務協作：PostgreSQL + Redis + Kafka 完整測試")]
    public async Task CompleteWorkflow_多服務協作_應正確執行()
    {
        var dbConnectionString = GlobalTestInfrastructureSetup.PostgreSqlContainer!.GetConnectionString();
        var redisConnectionString = GlobalTestInfrastructureSetup.RedisContainer!.GetConnectionString();
        var kafkaBootstrapServers = GlobalTestInfrastructureSetup.KafkaContainer!.GetBootstrapAddress();

        await Assert.That(dbConnectionString).IsNotNull();
        await Assert.That(dbConnectionString).Contains("test_db");

        await Assert.That(redisConnectionString).IsNotNull();
        await Assert.That(redisConnectionString).Contains("127.0.0.1");

        await Assert.That(kafkaBootstrapServers).IsNotNull();
        await Assert.That(kafkaBootstrapServers).Contains("127.0.0.1");
    }

    [Test]
    [Property("Category", "Database")]
    [DisplayName("PostgreSQL 資料庫連線驗證")]
    public async Task PostgreSqlDatabase_連線驗證_應成功建立連線()
    {
        var connectionString = GlobalTestInfrastructureSetup.PostgreSqlContainer!.GetConnectionString();

        await Assert.That(connectionString).Contains("test_db");
        await Assert.That(connectionString).Contains("test_user");
    }
}
```

**Assembly 級別容器共享的好處：**

1. **大幅減少啟動時間**：容器只在 Assembly 開始時啟動一次
2. **顯著降低資源消耗**：避免每個測試類別重複建立容器
3. **提升測試穩定性**：減少容器啟動失敗的風險
4. **保持測試隔離**：測試間仍然可以獨立清理資料

---

## TUnit Engine Modes

### Source Generation Mode（預設模式）

```text
████████╗██╗   ██╗███╗   ██╗██╗████████╗
╚══██╔══╝██║   ██║████╗  ██║██║╚══██╔══╝
   ██║   ██║   ██║██╔██╗ ██║██║   ██║
   ██║   ██║   ██║██║╚██╗██║██║   ██║
   ██║   ╚██████╔╝██║ ╚████║██║   ██║
   ╚═╝    ╚═════╝ ╚═╝  ╚═══╝╚═╝   ╚═╝

   Engine Mode: SourceGenerated
```

**特色與優勢：**

- **編譯時期產生**：所有測試發現邏輯在編譯時產生，不需要執行時反射
- **效能優異**：比反射模式快數倍
- **型別安全**：編譯時期驗證測試配置和資料來源
- **AOT 相容**：完全支援 Native AOT 編譯

### Reflection Mode（反射模式）

```bash
# 啟用反射模式
dotnet run -- --reflection

# 或設定環境變數
$env:TUNIT_EXECUTION_MODE = "reflection"
dotnet run
```

**適用場景：**

- 動態測試發現
- F# 和 VB.NET 專案（自動使用）
- 某些依賴反射的測試模式

### Native AOT 支援

```xml
<PropertyGroup>
    <PublishAot>true</PublishAot>
</PropertyGroup>
```

```bash
dotnet publish -c Release
```

---

## 常見問題與疑難排解

### 測試統計顯示異常問題

**問題現象：** `測試摘要: 總計: 0, 失敗: 0, 成功: 0`

**解決步驟：**

1. **確保專案檔設定正確：**

```xml
<PropertyGroup>
    <IsTestProject>true</IsTestProject>
</PropertyGroup>
```

2. **確保 GlobalUsings.cs 正確：**

```csharp
global using System;
global using System.Collections.Generic;
global using System.Linq;
global using System.Threading.Tasks;
global using TUnit.Core;
global using TUnit.Assertions;
global using TUnit.Assertions.Extensions;
```

3. **整合測試的特殊設定：**

```csharp
// 在 WebApi 專案的 Program.cs 最後加上
public partial class Program { }  // 讓整合測試可以存取
```

4. **清理和重建：**

```bash
dotnet clean; dotnet build
dotnet test --verbosity normal
```

### Source Generator 相關問題

**問題：測試類別無法被發現**

- **解決**：確保專案完全重建 (`dotnet clean; dotnet build`)

**問題：編譯時出現奇怪錯誤**

- **解決**：檢查是否有其他 Source Generator 套件，考慮更新到相容版本

### 診斷選項

```ini
# .editorconfig
tunit.enable_verbose_diagnostics = true
```

```xml
<PropertyGroup>
    <TUnitEnableVerboseDiagnostics>true</TUnitEnableVerboseDiagnostics>
</PropertyGroup>
```

---

## 實務建議

### 資料驅動測試的選擇策略

- **MethodDataSource**：適合動態資料、複雜物件、外部檔案載入
- **ClassDataSource**：適合共享資料、AutoFixture 整合、跨測試類別重用
- **Matrix Tests**：適合組合測試，但要注意參數數量避免爆炸性增長

### 執行控制最佳實踐

- **Retry**：只用於真正不穩定的外部依賴測試
- **Timeout**：為效能敏感的測試設定合理限制
- **DisplayName**：讓測試報告更符合業務語言

### 整合測試策略

- 使用 WebApplicationFactory 進行完整的 Web API 測試
- 運用 TUnit + Testcontainers 建立複雜多服務測試環境
- 透過屬性注入系統管理複雜的依賴關係
- 只測試實際存在的功能，避免測試不存在的端點

---

## 範本檔案

| 檔案名稱                                                                 | 說明                                   |
| ------------------------------------------------------------------------ | -------------------------------------- |
| [data-source-examples.cs](templates/data-source-examples.cs)             | MethodDataSource、ClassDataSource 範例 |
| [matrix-tests-examples.cs](templates/matrix-tests-examples.cs)           | Matrix Tests 組合測試範例              |
| [lifecycle-di-examples.cs](templates/lifecycle-di-examples.cs)           | 生命週期管理與依賴注入範例             |
| [execution-control-examples.cs](templates/execution-control-examples.cs) | Retry、Timeout、DisplayName 範例       |
| [aspnet-integration-tests.cs](templates/aspnet-integration-tests.cs)     | ASP.NET Core 整合測試範例              |
| [testcontainers-examples.cs](templates/testcontainers-examples.cs)       | Testcontainers 基礎設施編排範例        |

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 29 - TUnit 進階應用：資料驅動測試與依賴注入深度實戰**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10377970
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day29

- **Day 30 - TUnit 進階應用 - 執行控制與測試品質和 ASP.NET Core 整合測試實戰**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10378176
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day30

### TUnit 官方資源

- [TUnit 官方網站](https://tunit.dev/)
- [TUnit GitHub Repository](https://github.com/thomhurst/TUnit)

### 進階功能文件

- [TUnit Method Data Source 文件](https://tunit.dev/docs/test-authoring/method-data-source)
- [TUnit Class Data Source 文件](https://tunit.dev/docs/test-authoring/class-data-source)
- [TUnit Matrix Tests 文件](https://tunit.dev/docs/test-authoring/matrix-tests)
- [TUnit Properties 文件](https://tunit.dev/docs/test-lifecycle/properties)
- [TUnit Dependency Injection 文件](https://tunit.dev/docs/test-lifecycle/dependency-injection)
- [TUnit Retrying 文件](https://tunit.dev/docs/execution/retrying)
- [TUnit Timeouts 文件](https://tunit.dev/docs/execution/timeouts)
- [TUnit Engine Modes 文件](https://tunit.dev/docs/execution/engine-modes)
- [TUnit ASP.NET Core 文件](https://tunit.dev/docs/examples/aspnet)
- [TUnit Complex Test Infrastructure](https://tunit.dev/docs/examples/complex-test-infrastructure-orchestration)

### Testcontainers 相關資源

- [Testcontainers.NET 官方網站](https://dotnet.testcontainers.org/)
- [Testcontainers.NET GitHub](https://github.com/testcontainers/testcontainers-dotnet)
