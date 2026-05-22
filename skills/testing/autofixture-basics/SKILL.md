# AutoFixture 基礎：自動產生測試資料

---
name: autofixture-basics
description: 使用 AutoFixture 自動產生測試資料的基礎技術，包括匿名測試概念、Fixture 類別使用、Create<T>() 與 CreateMany<T>() 方法、複雜物件自動建構、循環參考處理，以及與 xUnit 的整合應用
---

## 觸發關鍵字

- autofixture
- auto fixture
- fixture.Create
- CreateMany
- anonymous testing
- 匿名測試
- 自動產生測試資料
- test data generation
- AutoFixture.Xunit2
- OmitOnRecursionBehavior
- ThrowingRecursionBehavior
- fixture.Build

## 概述

AutoFixture 是一個為 .NET 平台設計的測試資料自動產生工具，它的核心理念是「匿名測試」(Anonymous Testing)。這個概念認為，大部分的測試都不應該依賴於特定的資料值，而應該專注於驗證程式邏輯的正確性。

### 為什麼需要 AutoFixture？

傳統測試資料準備的痛點：

1. **樣板程式碼過多**：90% 的程式碼都在準備資料，真正的測試邏輯被埋沒
2. **測試焦點模糊**：很難快速理解這個測試在驗證什麼
3. **維護困難**：當物件結構改變時，所有相關測試都需要修改
4. **資料依賴性**：測試可能意外依賴於特定的資料值
5. **重複程式碼**：相同的資料準備邏輯在多個測試中重複出現

AutoFixture 可以看作是 **Test Data Builder Pattern 的自動化進化版**，能自動產生複雜的測試資料，讓我們專注於測試邏輯本身。

## 安裝套件

```xml
<PackageReference Include="AutoFixture" Version="4.18.1" />
<PackageReference Include="AutoFixture.Xunit2" Version="4.18.1" />
```

或透過命令列安裝：

```powershell
dotnet add package AutoFixture
dotnet add package AutoFixture.Xunit2
```

## 基本使用方式

### Fixture 類別與 Create<T>()

`Fixture` 是 AutoFixture 的核心類別，提供自動產生測試資料的能力：

```csharp
using AutoFixture;

[Fact]
public void AutoFixture_基本使用_應產生有效資料()
{
    // Arrange
    var fixture = new Fixture();

    // Act - 產生基本型別
    var id = fixture.Create<int>();           // 隨機正整數
    var name = fixture.Create<string>();      // 類似 GUID 格式的字串
    var price = fixture.Create<decimal>();    // 隨機十進位數
    var isActive = fixture.Create<bool>();    // 隨機布林值
    var date = fixture.Create<DateTime>();    // 隨機日期時間
    var guid = fixture.Create<Guid>();        // 新的 GUID

    // Assert
    id.Should().BePositive();
    name.Should().NotBeNullOrEmpty();
    guid.Should().NotBe(Guid.Empty);
}
```

### CreateMany<T>() 產生集合

```csharp
[Fact]
public void CreateMany_產生集合_應有多個元素()
{
    var fixture = new Fixture();

    // 預設產生 3 個元素
    var products = fixture.CreateMany<Product>().ToList();
    
    // 指定數量
    var moreProducts = fixture.CreateMany<Product>(10).ToList();

    products.Should().HaveCount(3);
    moreProducts.Should().HaveCount(10);
}
```

### 複雜物件自動建構

AutoFixture 能夠自動建構複雜的物件結構：

```csharp
public class Customer
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Email { get; set; }
    public Address Address { get; set; }        // 巢狀物件
    public List<Order> Orders { get; set; }     // 集合屬性
}

[Fact]
public void 複雜物件_應完整建構所有層級()
{
    var fixture = new Fixture();

    var customer = fixture.Create<Customer>();

    // 所有屬性自動填入值
    customer.Should().NotBeNull();
    customer.Id.Should().BePositive();
    customer.Name.Should().NotBeNullOrEmpty();
    customer.Address.Should().NotBeNull();
    customer.Address.Street.Should().NotBeNullOrEmpty();
    customer.Orders.Should().NotBeEmpty();
}
```

## Build<T>() 模式：精確控制

當需要對特定屬性進行控制時，使用 `Build<T>()` 模式：

```csharp
[Fact]
public void Build模式_指定特定屬性()
{
    var fixture = new Fixture();

    var customer = fixture.Build<Customer>()
        .With(x => x.Name, "測試客戶")           // 指定固定值
        .With(x => x.Age, 25)                    // 指定固定值
        .Without(x => x.InternalId)              // 排除屬性
        .Create();

    customer.Name.Should().Be("測試客戶");
    customer.Age.Should().Be(25);
    customer.InternalId.Should().Be(default);
}
```

### OmitAutoProperties() 控制自動設定

```csharp
[Fact]
public void OmitAutoProperties_僅設定必要屬性()
{
    var fixture = new Fixture();

    var customer = fixture.Build<Customer>()
        .OmitAutoProperties()           // 不自動設定任何屬性
        .With(x => x.Id, 123)          // 只設定關心的屬性
        .With(x => x.Name, "測試客戶")
        .Create();

    customer.Id.Should().Be(123);
    customer.Name.Should().Be("測試客戶");
    customer.Email.Should().BeNullOrEmpty();  // 保持預設值
    customer.Age.Should().Be(0);              // 保持預設值
}
```

## 循環參考處理

當物件包含循環參考時，AutoFixture 提供兩種處理策略：

### 預設行為：ThrowingRecursionBehavior

```csharp
// 預設會拋出例外
[Fact]
public void 循環參考_預設行為_拋出例外()
{
    var fixture = new Fixture();
    
    // Category 有 Parent 屬性指向自己，造成循環參考
    Action act = () => fixture.Create<Category>();
    
    act.Should().Throw<ObjectCreationException>();
}
```

### OmitOnRecursionBehavior：忽略循環參考

```csharp
[Fact]
public void 循環參考_使用OmitOnRecursion_成功建立()
{
    var fixture = new Fixture();
    
    // 移除預設的拋出例外行為
    fixture.Behaviors.OfType<ThrowingRecursionBehavior>().ToList()
        .ForEach(b => fixture.Behaviors.Remove(b));
    
    // 加入忽略循環參考行為
    fixture.Behaviors.Add(new OmitOnRecursionBehavior());

    var category = fixture.Create<Category>();

    category.Should().NotBeNull();
    category.Name.Should().NotBeNullOrEmpty();
}
```

### 共用基底類別

建議建立基底類別來統一處理循環參考：

```csharp
public abstract class AutoFixtureTestBase
{
    protected Fixture CreateFixture()
    {
        var fixture = new Fixture();

        fixture.Behaviors.OfType<ThrowingRecursionBehavior>().ToList()
            .ForEach(b => fixture.Behaviors.Remove(b));
        fixture.Behaviors.Add(new OmitOnRecursionBehavior());

        return fixture;
    }
}

public class CustomerServiceTests : AutoFixtureTestBase
{
    [Fact]
    public void ProcessOrder_正常訂單_應處理成功()
    {
        var fixture = CreateFixture();
        var customer = fixture.Create<Customer>();
        
        // 測試邏輯...
    }
}
```

## xUnit 整合

### 使用 Fixture 共享客製化

```csharp
public class ProductServiceTests
{
    private readonly Fixture _fixture;

    public ProductServiceTests()
    {
        _fixture = new Fixture();
        
        // 共同的客製化設定
        _fixture.Customize<ProductCreateRequest>(c => c
            .With(x => x.Price, () => _fixture.Create<decimal>() % 10000)
            .With(x => x.Name, () => $"Product-{_fixture.Create<string>()[..8]}")
        );
    }

    [Fact]
    public void CreateProduct_使用共享Fixture_應成功建立()
    {
        var productData = _fixture.Create<ProductCreateRequest>();
        var service = new ProductService();

        var result = service.CreateProduct(productData);

        result.Should().NotBeNull();
        productData.Price.Should().BeLessThan(10000);
    }
}
```

### 結合 Theory 測試

```csharp
[Theory]
[InlineData(CustomerType.Regular)]
[InlineData(CustomerType.Premium)]
[InlineData(CustomerType.VIP)]
public void CalculateDiscount_不同客戶類型_應套用正確折扣(CustomerType customerType)
{
    var fixture = new Fixture();
    
    var customer = fixture.Build<Customer>()
        .With(x => x.Type, customerType)
        .Create();
        
    var order = fixture.Create<Order>();
    var calculator = new DiscountCalculator();

    var discount = calculator.Calculate(customer, order);

    switch (customerType)
    {
        case CustomerType.Regular:
            discount.Should().Be(0);
            break;
        case CustomerType.Premium:
            discount.Should().BeInRange(0.05m, 0.10m);
            break;
        case CustomerType.VIP:
            discount.Should().BeInRange(0.15m, 0.25m);
            break;
    }
}
```

## 匿名測試原則

### 核心概念

測試應該關注「行為」而不是「資料」。在大多數情況下，我們並不在乎具體的資料值是什麼：

```csharp
// ✅ 好的做法：專注於測試邏輯
[Fact]
public void AddCustomer_任何有效客戶_應成功新增()
{
    var fixture = new Fixture();
    var customer = fixture.Create<Customer>();
    var repository = new CustomerRepository();

    var result = repository.Add(customer);

    result.Should().BeTrue();
}

// ❌ 避免：依賴隨機值的具體內容
[Fact]
public void BadTest_依賴隨機值()
{
    var fixture = new Fixture();
    var customer = fixture.Create<Customer>();

    // 錯誤：假設隨機產生的年齡會大於 18
    customer.Age.Should().BeGreaterThan(18); // 可能失敗
}

// ✅ 正確：明確設定關鍵值
[Fact]
public void GoodTest_明確設定關鍵值()
{
    var fixture = new Fixture();
    var customer = fixture.Build<Customer>()
        .With(x => x.Age, 25)  // 明確設定
        .Create();

    var validator = new CustomerValidator();
    var isValid = validator.IsAdult(customer);

    isValid.Should().BeTrue();  // 穩定的結果
}
```

## 進化比較：Test Data Builder vs AutoFixture

### 傳統 Test Data Builder (Day 03)

```csharp
// 需要手動建立 Builder 類別 (40+ 行)
public class OrderBuilder
{
    private int _id = 1;
    private Customer _customer = new Customer { Name = "Default" };
    private List<OrderItem> _items = new();
    
    public OrderBuilder WithCustomer(Customer customer)
    {
        _customer = customer;
        return this;
    }
    
    public OrderBuilder WithItems(params OrderItem[] items)
    {
        _items = items.ToList();
        return this;
    }
    
    public Order Build() => new Order
    {
        Id = _id,
        Customer = _customer,
        Items = _items
    };
}
```

### AutoFixture 方式 (Day 10)

```csharp
// 零設定成本，專注於測試邏輯 (5 行)
var fixture = new Fixture();
var order = fixture.Build<Order>()
    .With(x => x.Status, OrderStatus.Completed)
    .Create();
```

### 比較摘要

| 層面       | Test Data Builder      | AutoFixture        |
| ---------- | ---------------------- | ------------------ |
| 程式碼行數 | 40+ 行 Builder + 測試  | 5 行測試           |
| 維護成本   | 物件改變需更新 Builder | 自動適應變化       |
| 開發時間   | 先寫 Builder 再寫測試  | 直接寫測試         |
| 大量資料   | 需要迴圈               | `CreateMany(100)`  |
| 可讀性     | 業務語意明確           | 需理解 AutoFixture |

## 實務應用場景

### Entity 測試

```csharp
[Theory]
[InlineData(0, CustomerLevel.Bronze)]
[InlineData(15000, CustomerLevel.Silver)]
[InlineData(60000, CustomerLevel.Gold)]
[InlineData(120000, CustomerLevel.Diamond)]
public void GetLevel_不同消費金額_應回傳正確等級(decimal totalSpent, CustomerLevel expected)
{
    var fixture = new Fixture();
    var customer = fixture.Build<Customer>()
        .With(x => x.TotalSpent, totalSpent)
        .Create();

    var level = customer.GetLevel();

    level.Should().Be(expected);
}
```

### DTO 驗證

```csharp
[Fact]
public void ValidateRequest_有效資料_應通過驗證()
{
    var fixture = new Fixture();
    
    var request = fixture.Build<CreateCustomerRequest>()
        .With(x => x.Name, fixture.Create<string>()[..50])
        .With(x => x.Email, fixture.Create<MailAddress>().Address)
        .With(x => x.Age, Random.Shared.Next(18, 78))
        .Create();

    var context = new ValidationContext(request);
    var results = new List<ValidationResult>();
    var isValid = Validator.TryValidateObject(request, context, results, true);

    isValid.Should().BeTrue();
}
```

### 大量資料測試

```csharp
[Fact]
public void ProcessBatch_大量資料_應正確處理()
{
    var fixture = new Fixture();
    var records = fixture.CreateMany<DataRecord>(1000).ToList();
    var processor = new DataProcessor();

    var stopwatch = Stopwatch.StartNew();
    var result = processor.ProcessBatch(records);
    stopwatch.Stop();

    result.ProcessedCount.Should().Be(1000);
    result.ErrorCount.Should().Be(0);
    stopwatch.ElapsedMilliseconds.Should().BeLessThan(10000);
}
```

## 最佳實踐

### 應該做

1. **使用匿名測試概念** - 專注於測試邏輯而非具體資料
2. **只在必要時固定特定值** - 使用 `Build<T>().With()` 設定關鍵屬性
3. **建立共用基底類別** - 統一處理循環參考等共同配置
4. **合理的集合大小** - 根據測試目的調整 `CreateMany()` 數量

### 應該避免

1. **過度依賴隨機值** - 不要假設隨機值的具體內容
2. **忽略邊界值** - 仍需要明確測試邊界情況
3. **濫用自動產生** - 簡單測試可能用固定值更清楚

## 混合策略建議

結合兩種方式的優點：

```csharp
public static class TestDataFactory
{
    private static readonly Fixture _fixture = new();
    
    // 用 AutoFixture 建立基礎資料，再用 Builder 加工
    public static OrderBuilder AnOrder()
    {
        var baseOrder = _fixture.Create<Order>();
        return new OrderBuilder(baseOrder);
    }
    
    // 大量隨機資料產生
    public static IEnumerable<User> CreateRandomUsers(int count)
    {
        return _fixture.CreateMany<User>(count);
    }
}
```

## 程式碼範本

請參考 [templates](./templates) 資料夾中的範例檔案：

- [basic-autofixture-usage.cs](./templates/basic-autofixture-usage.cs) - 基本 AutoFixture 使用方式
- [complex-object-scenarios.cs](./templates/complex-object-scenarios.cs) - 複雜物件與循環參考處理
- [xunit-integration.cs](./templates/xunit-integration.cs) - xUnit 整合與 Theory 測試

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 10 - AutoFixture 基礎：自動產生測試資料**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374799
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day10

### 官方文件

- [AutoFixture GitHub](https://github.com/AutoFixture/AutoFixture)
- [AutoFixture 官方網站](https://autofixture.github.io/)
- [AutoFixture 快速入門](https://autofixture.github.io/docs/quick-start/)
- [AutoFixture NuGet](https://www.nuget.org/packages/autofixture)
