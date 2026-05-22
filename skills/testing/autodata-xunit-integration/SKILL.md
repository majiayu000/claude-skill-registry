# AutoData 屬性家族：xUnit 與 AutoFixture 的整合應用

---
name: autodata-xunit-integration
description: AutoData 屬性家族整合 xUnit 與 AutoFixture，實現參數化測試的自動資料注入。涵蓋 AutoData、InlineAutoData、MemberAutoData、CompositeAutoData、CollectionSizeAttribute，以及 CSV/JSON 外部資料整合。
---

## 觸發關鍵字

- AutoData
- InlineAutoData
- MemberAutoData
- CompositeAutoData
- xUnit AutoFixture 整合
- 參數化測試資料
- 測試參數注入
- CollectionSizeAttribute
- 外部測試資料
- CSV 測試資料
- JSON 測試資料

## 概述

AutoData 屬性家族是 `AutoFixture.Xunit2` 套件提供的功能，將 AutoFixture 的資料產生能力與 xUnit 的參數化測試整合，讓測試參數自動注入，大幅減少測試準備程式碼。

### 核心特色

1. **AutoData**：自動產生所有測試參數
2. **InlineAutoData**：混合固定值與自動產生
3. **MemberAutoData**：結合外部資料來源
4. **CompositeAutoData**：多重資料來源整合
5. **CollectionSizeAttribute**：控制集合產生數量

## 安裝套件

```xml
<PackageReference Include="AutoFixture" Version="4.18.1" />
<PackageReference Include="AutoFixture.Xunit2" Version="4.18.1" />
```

```bash
dotnet add package AutoFixture.Xunit2
```

## AutoData：完全自動產生參數

`AutoData` 是最基礎的屬性，自動為測試方法的所有參數產生測試資料。

### 基本使用

```csharp
using AutoFixture.Xunit2;

public class Person
{
    public Guid Id { get; set; }
    
    [StringLength(10)]
    public string Name { get; set; } = string.Empty;
    
    [Range(18, 80)]
    public int Age { get; set; }
    
    public string Email { get; set; } = string.Empty;
    public DateTime CreateTime { get; set; }
}

[Theory]
[AutoData]
public void AutoData_應能自動產生所有參數(Person person, string message, int count)
{
    // Arrange & Act - 參數已由 AutoData 自動產生

    // Assert
    person.Should().NotBeNull();
    person.Id.Should().NotBe(Guid.Empty);
    person.Name.Should().HaveLength(10);     // 遵循 StringLength 限制
    person.Age.Should().BeInRange(18, 80);   // 遵循 Range 限制
    message.Should().NotBeNullOrEmpty();
    count.Should().NotBe(0);
}
```

### 透過 DataAnnotation 約束參數

```csharp
[Theory]
[AutoData]
public void AutoData_透過DataAnnotation約束參數(
    [StringLength(5, MinimumLength = 3)] string shortName,
    [Range(1, 100)] int percentage,
    Person person)
{
    // Assert
    shortName.Length.Should().BeInRange(3, 5);
    percentage.Should().BeInRange(1, 100);
    person.Should().NotBeNull();
}
```

## InlineAutoData：混合固定值與自動產生

`InlineAutoData` 結合了 `InlineData` 的固定值特性與 `AutoData` 的自動產生功能。

### 基本語法

```csharp
[Theory]
[InlineAutoData("VIP客戶", 1000)]
[InlineAutoData("一般客戶", 500)]
[InlineAutoData("新客戶", 100)]
public void InlineAutoData_混合固定值與自動產生(
    string customerType,    // 對應第 1 個固定值
    decimal creditLimit,    // 對應第 2 個固定值
    Person person)          // 由 AutoFixture 產生
{
    // Arrange
    var customer = new Customer
    {
        Person = person,
        Type = customerType,
        CreditLimit = creditLimit
    };

    // Assert
    customer.Type.Should().Be(customerType);
    customer.CreditLimit.Should().BeOneOf(1000, 500, 100);
    customer.Person.Should().NotBeNull();
}
```

### 參數順序一致性

固定值的順序必須與方法參數順序一致：

```csharp
[Theory]
[InlineAutoData("產品A", 100)]  // 依序對應 name, price
[InlineAutoData("產品B", 200)]
public void InlineAutoData_參數順序一致性(
    string name,        // 對應第 1 個固定值
    decimal price,      // 對應第 2 個固定值
    string description, // 由 AutoFixture 產生
    Product product)    // 由 AutoFixture 產生
{
    // Assert
    name.Should().BeOneOf("產品A", "產品B");
    price.Should().BeOneOf(100, 200);
    description.Should().NotBeNullOrEmpty();
    product.Should().NotBeNull();
}
```

### ⚠️ 重要限制：只能使用編譯時常數

```csharp
// ✅ 正確：使用常數
[InlineAutoData("VIP", 100000)]
[InlineAutoData("Premium", 50000)]

// ❌ 錯誤：不能使用變數
private const decimal VipCreditLimit = 100000m;
[InlineAutoData("VIP", VipCreditLimit)]  // 編譯錯誤

// ❌ 錯誤：不能使用運算式
[InlineAutoData("VIP", 100 * 1000)]  // 編譯錯誤
```

需要使用複雜資料時，應使用 `MemberAutoData`。

## MemberAutoData：結合外部資料來源

`MemberAutoData` 允許從類別的方法、屬性或欄位中獲取測試資料。

### 使用靜態方法

```csharp
public class MemberAutoDataTests
{
    public static IEnumerable<object[]> GetProductCategories()
    {
        yield return new object[] { "3C產品", "TECH" };
        yield return new object[] { "服飾配件", "FASHION" };
        yield return new object[] { "居家生活", "HOME" };
        yield return new object[] { "運動健身", "SPORTS" };
    }

    [Theory]
    [MemberAutoData(nameof(GetProductCategories))]
    public void MemberAutoData_使用靜態方法資料(
        string categoryName,   // 來自 GetProductCategories
        string categoryCode,   // 來自 GetProductCategories
        Product product)       // 由 AutoFixture 產生
    {
        // Arrange
        var categorizedProduct = new CategorizedProduct
        {
            Product = product,
            CategoryName = categoryName,
            CategoryCode = categoryCode
        };

        // Assert
        categorizedProduct.CategoryName.Should().Be(categoryName);
        categorizedProduct.CategoryCode.Should().Be(categoryCode);
        categorizedProduct.Product.Should().NotBeNull();
    }
}
```

### 使用靜態屬性

```csharp
public static IEnumerable<object[]> StatusTransitions => new[]
{
    new object[] { OrderStatus.Created, OrderStatus.Confirmed },
    new object[] { OrderStatus.Confirmed, OrderStatus.Shipped },
    new object[] { OrderStatus.Shipped, OrderStatus.Delivered },
    new object[] { OrderStatus.Delivered, OrderStatus.Completed }
};

[Theory]
[MemberAutoData(nameof(StatusTransitions))]
public void MemberAutoData_使用靜態屬性_訂單狀態轉換(
    OrderStatus fromStatus,
    OrderStatus toStatus,
    Order order)
{
    // Arrange
    order.Status = fromStatus;

    // Act
    order.TransitionTo(toStatus);

    // Assert
    order.Status.Should().Be(toStatus);
}
```

## 自訂 AutoData 屬性

建立專屬的 AutoData 配置：

### DomainAutoDataAttribute

```csharp
public class DomainAutoDataAttribute : AutoDataAttribute
{
    public DomainAutoDataAttribute() : base(() => CreateFixture())
    {
    }

    private static IFixture CreateFixture()
    {
        var fixture = new Fixture();

        // 設定 Person 的自訂規則
        fixture.Customize<Person>(composer => composer
            .With(p => p.Age, () => Random.Shared.Next(18, 65))
            .With(p => p.Email, () => $"user{Random.Shared.Next(1000)}@example.com")
            .With(p => p.Name, () => $"測試用戶{Random.Shared.Next(100)}"));

        // 設定 Product 的自訂規則
        fixture.Customize<Product>(composer => composer
            .With(p => p.Price, () => Random.Shared.Next(100, 10000))
            .With(p => p.IsAvailable, true)
            .With(p => p.Name, () => $"產品{Random.Shared.Next(1000)}"));

        return fixture;
    }
}
```

### BusinessAutoDataAttribute

```csharp
public class BusinessAutoDataAttribute : AutoDataAttribute
{
    public BusinessAutoDataAttribute() : base(() => CreateFixture())
    {
    }

    private static IFixture CreateFixture()
    {
        var fixture = new Fixture();

        // 設定 Order 的業務規則
        fixture.Customize<Order>(composer => composer
            .With(o => o.Status, OrderStatus.Created)
            .With(o => o.Amount, () => Random.Shared.Next(1000, 50000))
            .With(o => o.OrderNumber, () => $"ORD{DateTime.Now:yyyyMMdd}{Random.Shared.Next(1000):D4}"));

        return fixture;
    }
}
```

### 使用自訂 AutoData

```csharp
[Theory]
[DomainAutoData]
public void 使用DomainAutoData(Person person, Product product)
{
    person.Age.Should().BeInRange(18, 64);
    person.Email.Should().EndWith("@example.com");
    product.IsAvailable.Should().BeTrue();
}

[Theory]
[BusinessAutoData]
public void 使用BusinessAutoData(Order order)
{
    order.Status.Should().Be(OrderStatus.Created);
    order.Amount.Should().BeInRange(1000, 49999);
    order.OrderNumber.Should().StartWith("ORD");
}
```

## CompositeAutoData：多重資料來源整合

組合多個自訂 AutoData 配置：

```csharp
public class CompositeAutoDataAttribute : AutoDataAttribute
{
    public CompositeAutoDataAttribute(params Type[] autoDataAttributeTypes) 
        : base(() => CreateFixture(autoDataAttributeTypes))
    {
    }

    private static IFixture CreateFixture(Type[] autoDataAttributeTypes)
    {
        var fixture = new Fixture();

        foreach (var attributeType in autoDataAttributeTypes)
        {
            var createFixtureMethod = attributeType.GetMethod(
                "CreateFixture",
                BindingFlags.NonPublic | BindingFlags.Static | BindingFlags.FlattenHierarchy);

            if (createFixtureMethod != null)
            {
                var sourceFixture = (IFixture)createFixtureMethod.Invoke(null, null)!;

                foreach (var customization in sourceFixture.Customizations)
                {
                    fixture.Customizations.Add(customization);
                }
            }
        }

        return fixture;
    }
}

// 使用方式
[Theory]
[CompositeAutoData(typeof(DomainAutoDataAttribute), typeof(BusinessAutoDataAttribute))]
public void CompositeAutoData_整合多重資料來源(
    Person person,
    Product product,
    Order order)
{
    // DomainAutoData 的設定
    person.Age.Should().BeInRange(18, 64);
    product.IsAvailable.Should().BeTrue();

    // BusinessAutoData 的設定
    order.Status.Should().Be(OrderStatus.Created);
}
```

## CollectionSizeAttribute：控制集合大小

AutoData 預設的集合大小是 3，可透過自訂屬性控制：

### CollectionSizeAttribute 實作

```csharp
using AutoFixture;
using AutoFixture.Kernel;
using AutoFixture.Xunit2;
using System.Reflection;

public class CollectionSizeAttribute : CustomizeAttribute
{
    private readonly int _size;

    public CollectionSizeAttribute(int size)
    {
        _size = size;
    }

    public override ICustomization GetCustomization(ParameterInfo parameter)
    {
        ArgumentNullException.ThrowIfNull(parameter);

        var objectType = parameter.ParameterType.GetGenericArguments()[0];

        var isTypeCompatible = parameter.ParameterType.IsGenericType &&
            parameter.ParameterType.GetGenericTypeDefinition()
                .MakeGenericType(objectType)
                .IsAssignableFrom(typeof(List<>).MakeGenericType(objectType));

        if (!isTypeCompatible)
        {
            throw new InvalidOperationException(
                $"{nameof(CollectionSizeAttribute)} 指定的型別與 List 不相容: " +
                $"{parameter.ParameterType} {parameter.Name}");
        }

        var customizationType = typeof(CollectionSizeCustomization<>).MakeGenericType(objectType);
        return (ICustomization)Activator.CreateInstance(customizationType, parameter, _size)!;
    }

    private class CollectionSizeCustomization<T> : ICustomization
    {
        private readonly ParameterInfo _parameter;
        private readonly int _repeatCount;

        public CollectionSizeCustomization(ParameterInfo parameter, int repeatCount)
        {
            _parameter = parameter;
            _repeatCount = repeatCount;
        }

        public void Customize(IFixture fixture)
        {
            fixture.Customizations.Add(
                new FilteringSpecimenBuilder(
                    new FixedBuilder(fixture.CreateMany<T>(_repeatCount).ToList()),
                    new EqualRequestSpecification(_parameter)));
        }
    }
}
```

### 使用 CollectionSizeAttribute

```csharp
[Theory]
[AutoData]
public void CollectionSize_控制自動產生集合大小(
    [CollectionSize(5)] List<Product> products,
    [CollectionSize(3)] List<Order> orders,
    Customer customer)
{
    // Assert
    products.Should().HaveCount(5);
    orders.Should().HaveCount(3);
    customer.Should().NotBeNull();

    products.Should().AllSatisfy(product =>
    {
        product.Name.Should().NotBeNullOrEmpty();
        product.Price.Should().BeGreaterOrEqualTo(0);
    });
}
```

## 外部測試資料整合

### 測試專案檔案設定

在 `.csproj` 中設定外部資料檔案：

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <!-- CSV 檔案 -->
    <Content Include="TestData\*.csv">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </Content>
    
    <!-- JSON 檔案 -->
    <Content Include="TestData\*.json">
      <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    </Content>
  </ItemGroup>

  <ItemGroup>
    <PackageReference Include="CsvHelper" Version="33.0.1" />
  </ItemGroup>
</Project>
```

### CSV 檔案整合

**TestData/products.csv**

```csv
ProductId,Name,Category,Price,IsAvailable
1,"iPhone 15","3C產品",35900,true
2,"MacBook Pro","3C產品",89900,true
3,"AirPods Pro","3C產品",7490,false
4,"Nike Air Max","運動用品",4200,true
```

**CSV 讀取與整合**

```csharp
using CsvHelper;
using CsvHelper.Configuration;
using System.Globalization;

public class ExternalDataIntegrationTests
{
    public static IEnumerable<object[]> GetProductsFromCsv()
    {
        var csvPath = Path.Combine(Directory.GetCurrentDirectory(), "TestData", "products.csv");
        
        using var reader = new StreamReader(csvPath);
        var config = new CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HeaderValidated = null,
            MissingFieldFound = null
        };
        
        using var csv = new CsvReader(reader, config);
        var records = csv.GetRecords<ProductCsvRecord>().ToList();
        
        foreach (var record in records)
        {
            yield return new object[]
            {
                record.ProductId,
                record.Name,
                record.Category,
                record.Price,
                record.IsAvailable
            };
        }
    }

    [Theory]
    [MemberAutoData(nameof(GetProductsFromCsv))]
    public void CSV整合測試_產品驗證(
        int productId,
        string productName,
        string category,
        decimal price,
        bool isAvailable,
        Customer customer,
        Order order)
    {
        // Assert - CSV 資料
        productId.Should().BePositive();
        productName.Should().NotBeNullOrEmpty();
        category.Should().BeOneOf("3C產品", "運動用品");
        price.Should().BePositive();

        // Assert - AutoFixture 產生的資料
        customer.Should().NotBeNull();
        order.Should().NotBeNull();
    }
}

public class ProductCsvRecord
{
    public int ProductId { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Category { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public bool IsAvailable { get; set; }
}
```

### JSON 檔案整合

**TestData/customers.json**

```json
[
  {
    "customerId": 1,
    "name": "張三",
    "email": "zhang@example.com",
    "type": "VIP",
    "creditLimit": 100000
  },
  {
    "customerId": 2,
    "name": "李四",
    "email": "li@example.com",
    "type": "Premium",
    "creditLimit": 50000
  }
]
```

**JSON 讀取與整合**

```csharp
using System.Text.Json;

public static IEnumerable<object[]> GetCustomersFromJson()
{
    var jsonPath = Path.Combine(Directory.GetCurrentDirectory(), "TestData", "customers.json");
    var jsonContent = File.ReadAllText(jsonPath);
    
    var options = new JsonSerializerOptions
    {
        PropertyNameCaseInsensitive = true
    };
    
    var customers = JsonSerializer.Deserialize<List<CustomerJsonRecord>>(jsonContent, options)!;
    
    foreach (var customer in customers)
    {
        yield return new object[]
        {
            customer.CustomerId,
            customer.Name,
            customer.Email,
            customer.Type,
            customer.CreditLimit
        };
    }
}

[Theory]
[MemberAutoData(nameof(GetCustomersFromJson))]
public void JSON整合測試_客戶驗證(
    int customerId,
    string name,
    string email,
    string customerType,
    decimal creditLimit,
    Order order)
{
    // Assert - JSON 資料
    customerId.Should().BePositive();
    name.Should().NotBeNullOrEmpty();
    email.Should().Contain("@");
    customerType.Should().BeOneOf("VIP", "Premium", "Regular");
    creditLimit.Should().BePositive();

    // Assert - AutoFixture 產生的資料
    order.Should().NotBeNull();
}
```

## 資料來源設計模式

### 階層式資料組織

```csharp
namespace AutoData.Tests.DataSources;

/// <summary>
/// 測試資料來源基底類別
/// </summary>
public abstract class BaseTestData
{
    protected static string GetTestDataPath(string fileName)
    {
        return Path.Combine(Directory.GetCurrentDirectory(), "TestData", fileName);
    }
}

/// <summary>
/// 產品測試資料來源
/// </summary>
public class ProductTestDataSource : BaseTestData
{
    public static IEnumerable<object[]> BasicProducts()
    {
        yield return new object[] { "iPhone", 35900m, true };
        yield return new object[] { "MacBook", 89900m, true };
        yield return new object[] { "AirPods", 7490m, false };
    }

    public static IEnumerable<object[]> ElectronicsProducts()
    {
        // 從 CSV 檔案讀取
        var csvPath = GetTestDataPath("electronics.csv");
        // ... 讀取邏輯
    }
}

/// <summary>
/// 客戶測試資料來源
/// </summary>
public class CustomerTestDataSource : BaseTestData
{
    public static IEnumerable<object[]> VipCustomers()
    {
        yield return new object[] { "張三", "VIP", 100000m };
        yield return new object[] { "李四", "VIP", 150000m };
    }
}
```

### 可重用資料集

```csharp
/// <summary>
/// 可重用的測試資料集
/// </summary>
public static class ReusableTestDataSets
{
    public static class ProductCategories
    {
        public static IEnumerable<object[]> All()
        {
            yield return new object[] { "3C產品", "TECH" };
            yield return new object[] { "服飾配件", "FASHION" };
            yield return new object[] { "居家生活", "HOME" };
        }

        public static IEnumerable<object[]> Electronics()
        {
            yield return new object[] { "手機", "MOBILE" };
            yield return new object[] { "筆電", "LAPTOP" };
        }
    }

    public static class CustomerTypes
    {
        public static IEnumerable<object[]> All()
        {
            yield return new object[] { "VIP", 100000m, 0.15m };
            yield return new object[] { "Premium", 50000m, 0.10m };
            yield return new object[] { "Regular", 20000m, 0.05m };
        }
    }
}
```

## 與 Awesome Assertions 協作

```csharp
[Theory]
[InlineAutoData("VIP", 100000)]
[InlineAutoData("Premium", 50000)]
[InlineAutoData("Regular", 20000)]
public void AutoData與AwesomeAssertions協作_客戶等級驗證(
    string customerLevel,
    decimal expectedCreditLimit,
    [Range(1000, 15000)] decimal orderAmount,
    Customer customer,
    Order order)
{
    // Arrange
    customer.Type = customerLevel;
    customer.CreditLimit = expectedCreditLimit;
    order.Amount = orderAmount;

    // Act
    var canPlaceOrder = customer.CanPlaceOrder(order.Amount);
    var discountRate = CalculateDiscount(customer.Type, order.Amount);

    // Assert - 使用 Awesome Assertions 語法
    customer.Type.Should().Be(customerLevel);
    customer.CreditLimit.Should().Be(expectedCreditLimit);
    customer.CreditLimit.Should().BePositive();
    
    order.Amount.Should().BeInRange(1000m, 15000m);
    canPlaceOrder.Should().BeTrue();
    discountRate.Should().BeInRange(0m, 0.3m);
}

private static decimal CalculateDiscount(string customerType, decimal orderAmount)
{
    var baseDiscount = customerType switch
    {
        "VIP" => 0.15m,
        "Premium" => 0.10m,
        "Regular" => 0.05m,
        _ => 0m
    };

    var largeOrderBonus = orderAmount > 30000m ? 0.05m : 0m;
    return Math.Min(baseDiscount + largeOrderBonus, 0.3m);
}
```

## 最佳實踐

### 應該做

1. **善用 DataAnnotation**
   - 在參數上使用 `[StringLength]`、`[Range]` 約束資料範圍
   - 確保產生的資料符合業務規則

2. **建立可重用的自訂 AutoData**
   - 為不同領域建立專屬的 AutoData 屬性
   - 集中管理測試資料的產生規則

3. **使用 MemberAutoData 處理複雜資料**
   - 當 InlineAutoData 無法滿足需求時使用
   - 支援變數、運算式和外部資料來源

4. **組織測試資料來源**
   - 建立階層式的資料來源結構
   - 將相關資料集中管理

### 應該避免

1. **在 InlineAutoData 使用非常數值**
   - InlineAutoData 只接受編譯時常數
   - 需要動態值時改用 MemberAutoData

2. **過度複雜的 CompositeAutoData**
   - 避免組合過多的 AutoData 來源
   - 保持配置的可理解性

3. **忽略參數順序**
   - InlineAutoData 的固定值必須與參數順序一致
   - 錯誤的順序會導致型別不符

## 程式碼範本

請參考 [templates](./templates) 資料夾中的範例檔案：

- [autodata-attributes.cs](./templates/autodata-attributes.cs) - AutoData 屬性家族使用範例
- [external-data-integration.cs](./templates/external-data-integration.cs) - CSV/JSON 外部資料整合
- [advanced-patterns.cs](./templates/advanced-patterns.cs) - 進階模式與 CollectionSizeAttribute

## 與其他技能的關係

- **autofixture-basics**：本技能的前置知識
- **autofixture-customization**：自訂化策略可用於 AutoData 屬性
- **autofixture-nsubstitute-integration**：下一步學習目標
- **awesome-assertions-guide**：搭配使用提升測試可讀性

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 12 - 結合 AutoData：xUnit 與 AutoFixture 的整合應用**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375014
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day12

### 官方文件

- [AutoFixture Cheat Sheet - AutoData Theories](https://github.com/AutoFixture/AutoFixture/wiki/Cheat-Sheet#autodata-theories)
- [AutoDataAttribute API Reference](https://autofixture.io/api/AutoFixture.Xunit.AutoDataAttribute.html)
- [InlineAutoDataAttribute API Reference](https://autofixture.io/api/AutoFixture.Xunit.InlineAutoDataAttribute.html)
- [CsvHelper 官方文件](https://joshclose.github.io/CsvHelper/)
