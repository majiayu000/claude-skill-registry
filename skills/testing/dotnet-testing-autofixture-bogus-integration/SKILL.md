---
name: dotnet-testing-autofixture-bogus-integration
description: |
  AutoFixture 與 Bogus 整合完整指南。結合匿名測試資料與真實感語意化資料產生。涵蓋 SpecimenBuilder 整合、混合產生器、測試資料工廠與循環參考處理。
  Keywords: autofixture bogus integration, autofixture bogus, bogus integration, Faker, EmailSpecimenBuilder, PhoneSpecimenBuilder, NameSpecimenBuilder, 真實感測試資料, 語意化資料, 混合產生器, HybridTestDataGenerator, OmitOnRecursionBehavior, 循環參考
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: "autofixture, bogus, test-data, faker, integration, semantic-data"
---

# AutoFixture 與 Bogus 整合應用指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 整合 AutoFixture 與 Bogus 兩套工具
- 建立混合測試資料產生器
- 設計 ISpecimenBuilder 整合 Bogus 資料產生
- 建立自訂 AutoData 屬性使用 Bogus
- 處理循環參考問題
- 建立統一的測試資料工廠
- 設計測試基底類別整合資料產生功能

---

## 核心概念

### 為什麼需要整合？

**AutoFixture 的優勢**：

- 快速產生匿名測試資料
- 自動處理複雜物件結構
- 良好的循環參考處理機制

**Bogus 的優勢**：

- 產生真實感的語意化資料
- 豐富的資料類型支援（Email、Phone、Address 等）
- 對驗證比較友善的資料格式

**整合後的效果**：

```csharp
// 整合前的問題
var user = fixture.Create<User>();
// user.Email 可能是 "Email1a2b3c4d"，不像真實 Email

// 整合後
var user = integratedFixture.Create<User>();
// user.Email 是 "john.doe@example.com"
// user.FirstName 是 "John"
// 其他屬性由 AutoFixture 自動填充
```

---

## 套件安裝

```xml
<PackageReference Include="AutoFixture" Version="4.18.1" />
<PackageReference Include="AutoFixture.Xunit2" Version="4.18.1" />
<PackageReference Include="Bogus" Version="35.6.3" />
<PackageReference Include="xunit" Version="2.9.3" />
<PackageReference Include="AwesomeAssertions" Version="9.1.0" />
```

---

## 整合架構

### 整合方式總覽

| 整合方式                     | 適用場景           | 複雜度 |
| ---------------------------- | ------------------ | ------ |
| 屬性層級 SpecimenBuilder     | 特定屬性使用 Bogus | 低     |
| 類型層級 SpecimenBuilder     | 整個類型使用 Bogus | 中     |
| 混合產生器 (HybridGenerator) | 統一 API 整合      | 中     |
| 整合工廠 (IntegratedFactory) | 完整測試場景建構   | 高     |
| 自訂 AutoData 屬性           | xUnit 整合         | 低     |

---

## 核心整合技術

### 1. 屬性層級 SpecimenBuilder

透過 `ISpecimenBuilder` 介面，根據屬性名稱決定是否使用 Bogus：

```csharp
public class EmailSpecimenBuilder : ISpecimenBuilder
{
    private readonly Faker _faker = new();

    public object Create(object request, ISpecimenContext context)
    {
        if (request is PropertyInfo property && 
            property.Name.Contains("Email", StringComparison.OrdinalIgnoreCase))
        {
            return _faker.Internet.Email();
        }
        
        return new NoSpecimen();
    }
}
```

**常用 SpecimenBuilder**：

| Builder                    | 匹配條件                    | Bogus 方法                           |
| -------------------------- | --------------------------- | ------------------------------------ |
| EmailSpecimenBuilder       | 包含 "Email"                | `Internet.Email()`                   |
| PhoneSpecimenBuilder       | 包含 "Phone"                | `Phone.PhoneNumber()`                |
| NameSpecimenBuilder        | FirstName/LastName/FullName | `Person.FirstName/LastName/FullName` |
| AddressSpecimenBuilder     | Street/City/Postal/Country  | `Address.*`                          |
| WebsiteSpecimenBuilder     | 包含 "Website"              | `Internet.Url()`                     |
| CompanyNameSpecimenBuilder | Company 類型的 Name         | `Company.CompanyName()`              |

### 2. 類型層級 SpecimenBuilder

為整個類型建立完整的 Bogus 產生器：

```csharp
public class BogusSpecimenBuilder : ISpecimenBuilder
{
    private readonly Dictionary<Type, object> _fakers;

    public BogusSpecimenBuilder()
    {
        _fakers = new Dictionary<Type, object>();
        RegisterFakers();
    }

    private void RegisterFakers()
    {
        _fakers[typeof(User)] = new Faker<User>()
            .RuleFor(u => u.Id, f => f.Random.Guid())
            .RuleFor(u => u.FirstName, f => f.Person.FirstName)
            .RuleFor(u => u.Email, (f, u) => f.Internet.Email(u.FirstName))
            .Ignore(u => u.Company); // 避免循環參考

        _fakers[typeof(Address)] = new Faker<Address>()
            .RuleFor(a => a.Street, f => f.Address.StreetAddress())
            .RuleFor(a => a.City, f => f.Address.City());
    }

    public object Create(object request, ISpecimenContext context)
    {
        if (request is Type type && _fakers.TryGetValue(type, out var faker))
        {
            return GenerateWithFaker(faker);
        }
        return new NoSpecimen();
    }
}
```

### 3. 擴充方法整合

```csharp
public static class FixtureExtensions
{
    /// <summary>
    /// 為 AutoFixture 加入 Bogus 整合功能
    /// </summary>
    public static IFixture WithBogus(this IFixture fixture)
    {
        // 先處理循環參考
        fixture.WithOmitOnRecursion();

        // 加入屬性層級整合
        fixture.Customizations.Add(new EmailSpecimenBuilder());
        fixture.Customizations.Add(new PhoneSpecimenBuilder());
        fixture.Customizations.Add(new NameSpecimenBuilder());
        fixture.Customizations.Add(new AddressSpecimenBuilder());

        // 加入類型層級整合
        fixture.Customizations.Add(new BogusSpecimenBuilder());

        return fixture;
    }

    /// <summary>
    /// 處理循環參考
    /// </summary>
    public static IFixture WithOmitOnRecursion(this IFixture fixture)
    {
        fixture.Behaviors.OfType<ThrowingRecursionBehavior>()
            .ToList()
            .ForEach(b => fixture.Behaviors.Remove(b));
        fixture.Behaviors.Add(new OmitOnRecursionBehavior());
        return fixture;
    }

    /// <summary>
    /// 設定隨機種子
    /// </summary>
    public static IFixture WithSeed(this IFixture fixture, int seed)
    {
        Bogus.Randomizer.Seed = new Random(seed);
        return fixture;
    }
}
```

---

## 循環參考處理

### 為什麼循環參考很重要？

```csharp
public class User
{
    public Company? Company { get; set; }  // User 參考 Company
}

public class Company
{
    public List<User> Employees { get; set; } = new();  // Company 參考 User
}
```

**問題**：User → Company → Employees(User) → Company → ... 無限循環

### 解決方案：OmitOnRecursionBehavior

```csharp
var fixture = new Fixture();
fixture.Behaviors.OfType<ThrowingRecursionBehavior>()
    .ToList()
    .ForEach(b => fixture.Behaviors.Remove(b));
fixture.Behaviors.Add(new OmitOnRecursionBehavior());
```

**效果**：

- ✅ 避免 StackOverflowException
- ✅ 循環參考的屬性設為 null 或空集合
- ⚠️ 某些深層屬性可能為 null（這是預期行為）

---

## 自訂 AutoData 屬性

### BogusAutoDataAttribute

```csharp
public class BogusAutoDataAttribute : AutoDataAttribute
{
    public BogusAutoDataAttribute() 
        : base(() => new Fixture().WithBogus())
    {
    }
}
```

### 使用方式

```csharp
[Theory]
[BogusAutoData]
public void 使用整合資料測試(User user, Address address)
{
    user.Email.Should().Contain("@");
    user.FirstName.Should().NotBeNullOrEmpty();
    address.City.Should().NotBeNullOrEmpty();
}
```

---

## 混合產生器

### ITestDataGenerator 介面

```csharp
public interface ITestDataGenerator
{
    T Generate<T>();
    IEnumerable<T> Generate<T>(int count);
    T Generate<T>(Action<T> configure);
}
```

### HybridTestDataGenerator 實作

```csharp
public class HybridTestDataGenerator : ITestDataGenerator
{
    private readonly IFixture _fixture;

    public HybridTestDataGenerator(int? seed = null)
    {
        _fixture = new Fixture()
            .WithBogus()
            .WithOmitOnRecursion();

        if (seed.HasValue)
        {
            Bogus.Randomizer.Seed = new Random(seed.Value);
        }
    }

    public T Generate<T>() => _fixture.Create<T>();

    public IEnumerable<T> Generate<T>(int count) 
        => Enumerable.Range(0, count).Select(_ => Generate<T>());

    public T Generate<T>(Action<T> configure)
    {
        var item = Generate<T>();
        configure(item);
        return item;
    }
}
```

---

## 整合測試資料工廠

### IntegratedTestDataFactory

```csharp
public class IntegratedTestDataFactory
{
    private readonly IFixture _fixture;
    private readonly Dictionary<Type, object> _cache = new();

    public IntegratedTestDataFactory(int? seed = null)
    {
        _fixture = new Fixture()
            .WithBogus()
            .WithOmitOnRecursion()
            .WithRepeatCount(3);

        if (seed.HasValue)
        {
            _fixture.WithSeed(seed.Value);
        }
    }

    public T CreateFresh<T>() => _fixture.Create<T>();

    public List<T> CreateMany<T>(int count = 3) 
        => _fixture.CreateMany<T>(count).ToList();

    public T GetCached<T>() where T : class
    {
        var type = typeof(T);
        if (_cache.TryGetValue(type, out var cached))
            return (T)cached;

        var instance = CreateFresh<T>();
        _cache[type] = instance;
        return instance;
    }

    public void ClearCache() => _cache.Clear();

    /// <summary>
    /// 建立完整測試場景
    /// </summary>
    public TestScenario CreateTestScenario()
    {
        var company = CreateFresh<Company>();
        var users = CreateMany<User>(5);
        var orders = CreateMany<Order>(10);

        // 建立關聯
        foreach (var user in users)
        {
            user.Company = company;
        }

        company.Employees = users;

        return new TestScenario
        {
            Company = company,
            Users = users,
            Orders = orders
        };
    }
}
```

---

## 測試基底類別

### TestBase 實作

```csharp
public abstract class TestBase
{
    protected readonly IFixture Fixture;
    protected readonly HybridTestDataGenerator Generator;
    protected readonly IntegratedTestDataFactory Factory;

    protected TestBase(int? seed = null)
    {
        Fixture = new Fixture()
            .WithBogus()
            .WithOmitOnRecursion()
            .WithRepeatCount(3);

        if (seed.HasValue)
        {
            Fixture.WithSeed(seed.Value);
        }

        Generator = new HybridTestDataGenerator(seed);
        Factory = new IntegratedTestDataFactory(seed);
    }

    protected T Create<T>() => Fixture.Create<T>();

    protected List<T> CreateMany<T>(int count = 3) 
        => Fixture.CreateMany<T>(count).ToList();

    protected T Create<T>(Action<T> configure)
    {
        var instance = Create<T>();
        configure(instance);
        return instance;
    }
}
```

---

## Seed 管理與可重現性

### 重要限制

由於 AutoFixture 和 Bogus 有不同的隨機數管理機制：

- ✅ Seed 確保測試行為穩定性
- ✅ Seed 確保資料格式一致性
- ❌ 無法保證所有屬性值完全相同

### 建議做法

```csharp
// 使用 Seed 確保穩定性
var factory = new IntegratedTestDataFactory(seed: 12345);

// 如果需要完全可重現，使用單一工具
var faker = new Faker<User>();
faker.UseSeed(12345);
```

---

## 使用範例

### 基本整合使用

```csharp
[Fact]
public void AutoFixture_整合_Bogus_應能產生真實感資料()
{
    // Arrange
    var fixture = new Fixture().WithBogus();

    // Act
    var user = fixture.Create<User>();

    // Assert
    user.Email.Should().Contain("@");
    user.FirstName.Should().NotBeNullOrEmpty();
    user.Phone.Should().MatchRegex(@"[\d\-\(\)\s]+");
}
```

### 使用工廠建立測試場景

```csharp
[Fact]
public void 工廠_應能建立完整的測試場景()
{
    // Arrange
    var factory = new IntegratedTestDataFactory(seed: 42);

    // Act
    var scenario = factory.CreateTestScenario();

    // Assert
    scenario.Company.Should().NotBeNull();
    scenario.Users.Should().HaveCount(5);
    scenario.Orders.Should().HaveCount(10);
    
    scenario.Users.Should().AllSatisfy(user =>
    {
        user.Company.Should().Be(scenario.Company);
        user.Email.Should().Contain("@");
    });
}
```

---

## 最佳實踐

### 建議做法

1. **永遠先處理循環參考**

   ```csharp
   fixture.WithOmitOnRecursion().WithBogus();
   ```

2. **為常用實體建立專用 SpecimenBuilder**

3. **使用 Seed 確保測試穩定性**

4. **建立測試基底類別統一資料產生邏輯**

5. **適當使用快取提升效能**

### 避免事項

1. ❌ 過度設計，保持簡單實用
2. ❌ 期望整合環境完全可重現
3. ❌ 忽略循環參考處理
4. ❌ 在每個測試中重新建立 Fixture

---

## 整合與 AutoFixture/Bogus 的比較

| 面向         | 純 AutoFixture | 純 Bogus      | 整合方案 |
| ------------ | -------------- | ------------- | -------- |
| 資料真實感   | 低             | 高            | 高       |
| 設定複雜度   | 低             | 中            | 中       |
| 物件關聯處理 | 自動           | 手動          | 自動     |
| 循環參考處理 | 內建           | 無            | 整合     |
| 可重現性     | 高             | 高            | 中       |
| 適用場景     | 單元測試       | 整合測試/原型 | 兩者皆可 |

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 15 - AutoFixture 與 Bogus 整合：結合兩者優勢**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375620
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day15

### 官方文件

- [AutoFixture GitHub](https://github.com/AutoFixture/AutoFixture)
- [Bogus GitHub Repository](https://github.com/bchavez/Bogus)

---

## 相關技能

- [autofixture-basics](../autofixture-basics/) - AutoFixture 基礎使用
- [autofixture-customization](../autofixture-customization/) - AutoFixture 自訂化策略
- [autodata-xunit-integration](../autodata-xunit-integration/) - AutoData 屬性整合
- [bogus-fake-data](../bogus-fake-data/) - Bogus 假資料產生器

---

## 程式碼範例

請參考同目錄下的範例檔案：

- `templates/specimen-builders.cs` - SpecimenBuilder 實作範例
- `templates/hybrid-generator.cs` - 混合產生器與擴充方法
- `templates/integrated-factory.cs` - 整合工廠與測試基底類別
