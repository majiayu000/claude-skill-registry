# AutoFixture 進階：自訂化測試資料生成策略

---
name: autofixture-customization
description: AutoFixture 進階自訂化技術，包括 DataAnnotations 自動整合、屬性範圍控制、自訂 ISpecimenBuilder 實作、DateTime 與數值範圍建構器、泛型化設計與擴充方法
---

## 觸發關鍵字

- autofixture customization
- autofixture customize
- ISpecimenBuilder
- specimen builder
- DataAnnotations autofixture
- 屬性範圍控制
- fixture.Customizations
- Insert(0)
- RandomDateTimeSequenceGenerator
- NumericRangeBuilder
- 自訂建構器
- custom builder autofixture

## 概述

本技能涵蓋 AutoFixture 的進階自訂化功能，讓您能根據業務需求精確控制測試資料的生成邏輯。從 DataAnnotations 自動整合到自訂 `ISpecimenBuilder` 實作，掌握這些技術能讓測試資料更符合實際業務需求。

### 核心技術

1. **DataAnnotations 整合**：AutoFixture 自動識別 `[StringLength]`、`[Range]` 等驗證屬性
2. **屬性範圍控制**：使用 `.With()` 配合 `Random.Shared` 動態產生隨機值
3. **自訂 ISpecimenBuilder**：實作精確控制特定屬性的建構器
4. **優先順序管理**：理解 `Insert(0)` vs `Add()` 的差異
5. **泛型化設計**：建立支援多種數值型別的可重用建構器

## 安裝套件

```xml
<PackageReference Include="AutoFixture" Version="4.18.1" />
<PackageReference Include="AutoFixture.Xunit2" Version="4.18.1" />
```

## DataAnnotations 自動整合

AutoFixture 能自動識別 `System.ComponentModel.DataAnnotations` 的驗證屬性：

```csharp
using System.ComponentModel.DataAnnotations;

public class Person
{
    public Guid Id { get; set; }
    
    [StringLength(10)]
    public string Name { get; set; } = string.Empty;
    
    [Range(10, 80)]
    public int Age { get; set; }
    
    public DateTime CreateTime { get; set; }
}

[Fact]
public void AutoFixture_應能識別DataAnnotations()
{
    var fixture = new Fixture();

    var person = fixture.Create<Person>();

    person.Name.Length.Should().Be(10);        // StringLength(10)
    person.Age.Should().BeInRange(10, 80);     // Range(10, 80)
}

[Fact]
public void AutoFixture_批量產生_都符合限制()
{
    var fixture = new Fixture();

    var persons = fixture.CreateMany<Person>(10).ToList();

    persons.Should().AllSatisfy(person =>
    {
        person.Name.Length.Should().Be(10);
        person.Age.Should().BeInRange(10, 80);
    });
}
```

## 使用 .With() 控制屬性範圍

### 固定值 vs 動態值

```csharp
// ❌ 固定值：只執行一次，所有物件相同值
.With(x => x.Age, Random.Shared.Next(30, 50))

// ✅ 動態值：每個物件都重新計算
.With(x => x.Age, () => Random.Shared.Next(30, 50))
```

### 完整範例

```csharp
[Fact]
public void With方法_固定值vs動態值的差異()
{
    var fixture = new Fixture();

    // 固定值：所有物件年齡相同
    var fixedAgeMembers = fixture.Build<Member>()
        .With(x => x.Age, Random.Shared.Next(30, 50))
        .CreateMany(5)
        .ToList();

    // 動態值：每個物件年齡不同
    var dynamicAgeMembers = fixture.Build<Member>()
        .With(x => x.Age, () => Random.Shared.Next(30, 50))
        .CreateMany(5)
        .ToList();

    // 固定值：只有一種年齡
    fixedAgeMembers.Select(m => m.Age).Distinct().Count().Should().Be(1);

    // 動態值：通常有多種年齡
    dynamicAgeMembers.Select(m => m.Age).Distinct().Count().Should().BeGreaterThan(1);
}
```

### Random.Shared 的優點

| 特性       | `new Random()`             | `Random.Shared`      |
| ---------- | -------------------------- | -------------------- |
| 實例化方式 | 每次建立新實例             | 全域共用單一實例     |
| 執行緒安全 | ❌ 不是                    | ✅ 是                |
| 效能       | 多次建立有負擔，可能重複值 | 效能更佳，避免重複值 |
| 用途建議   | 單執行緒、短期用途         | 多執行緒、全域共用   |

## 自訂 ISpecimenBuilder

### RandomRangedDateTimeBuilder：精確控制 DateTime 屬性

`RandomDateTimeSequenceGenerator` 會影響**所有** DateTime 屬性。若需控制特定屬性，需自訂建構器：

```csharp
using AutoFixture.Kernel;
using System.Reflection;

public class RandomRangedDateTimeBuilder : ISpecimenBuilder
{
    private readonly DateTime _minDate;
    private readonly DateTime _maxDate;
    private readonly HashSet<string> _targetProperties;

    public RandomRangedDateTimeBuilder(
        DateTime minDate, 
        DateTime maxDate, 
        params string[] targetProperties)
    {
        _minDate = minDate;
        _maxDate = maxDate;
        _targetProperties = new HashSet<string>(targetProperties);
    }

    public object Create(object request, ISpecimenContext context)
    {
        if (request is PropertyInfo propertyInfo &&
            propertyInfo.PropertyType == typeof(DateTime) &&
            _targetProperties.Contains(propertyInfo.Name))
        {
            var range = _maxDate - _minDate;
            var randomTicks = (long)(Random.Shared.NextDouble() * range.Ticks);
            return _minDate.AddTicks(randomTicks);
        }

        return new NoSpecimen();
    }
}
```

### 使用範例

```csharp
[Fact]
public void 只控制特定DateTime屬性()
{
    var fixture = new Fixture();

    var minDate = new DateTime(2025, 1, 1);
    var maxDate = new DateTime(2025, 12, 31);
    
    // 只控制 UpdateTime 屬性
    fixture.Customizations.Add(
        new RandomRangedDateTimeBuilder(minDate, maxDate, "UpdateTime"));

    var member = fixture.Create<Member>();

    // UpdateTime 在指定範圍
    member.UpdateTime.Should().BeOnOrAfter(minDate).And.BeOnOrBefore(maxDate);
    
    // CreateTime 不受影響
}
```

### NoSpecimen 的重要性

`NoSpecimen` 表示此建構器無法處理請求，交由責任鏈中下一個建構器處理：

```csharp
public object Create(object request, ISpecimenContext context)
{
    // 不是我們的目標 → 回傳 NoSpecimen
    if (request is not PropertyInfo propertyInfo)
        return new NoSpecimen();
        
    if (propertyInfo.PropertyType != typeof(DateTime))
        return new NoSpecimen();
        
    if (!_targetProperties.Contains(propertyInfo.Name))
        return new NoSpecimen();
    
    // 是我們的目標 → 產生值
    return GenerateRandomDateTime();
}
```

## 優先順序管理：Insert(0) vs Add()

### 問題：內建建構器優先順序更高

AutoFixture 內建的 `RangeAttributeRelay`、`NumericSequenceGenerator` 可能比自訂建構器有更高優先順序：

```csharp
// ❌ 可能失效：被內建建構器攔截
fixture.Customizations.Add(new MyNumericBuilder(30, 50, "Age"));

// ✅ 正確：確保最高優先順序
fixture.Customizations.Insert(0, new MyNumericBuilder(30, 50, "Age"));
```

### 改進版數值範圍建構器

```csharp
public class ImprovedRandomRangedNumericSequenceBuilder : ISpecimenBuilder
{
    private readonly int _min;
    private readonly int _max;
    private readonly Func<PropertyInfo, bool> _predicate;

    public ImprovedRandomRangedNumericSequenceBuilder(
        int min, 
        int max, 
        Func<PropertyInfo, bool> predicate)
    {
        _min = min;
        _max = max;
        _predicate = predicate;
    }

    public object Create(object request, ISpecimenContext context)
    {
        if (request is PropertyInfo propertyInfo &&
            propertyInfo.PropertyType == typeof(int) &&
            _predicate(propertyInfo))
        {
            return Random.Shared.Next(_min, _max);
        }

        return new NoSpecimen();
    }
}
```

### 使用 Insert(0) 確保優先順序

```csharp
[Fact]
public void 使用Insert0確保優先順序()
{
    var fixture = new Fixture();
    
    // 使用 Insert(0) 確保最高優先順序
    fixture.Customizations.Insert(0, 
        new ImprovedRandomRangedNumericSequenceBuilder(
            30, 50, 
            prop => prop.Name == "Age" && prop.DeclaringType == typeof(Member)));

    var members = fixture.CreateMany<Member>(20).ToList();

    members.Should().AllSatisfy(m => m.Age.Should().BeInRange(30, 49));
}
```

## 泛型化數值範圍建構器

### NumericRangeBuilder<TValue>

```csharp
public class NumericRangeBuilder<TValue> : ISpecimenBuilder
    where TValue : struct, IComparable, IConvertible
{
    private readonly TValue _min;
    private readonly TValue _max;
    private readonly Func<PropertyInfo, bool> _predicate;

    public NumericRangeBuilder(
        TValue min, 
        TValue max, 
        Func<PropertyInfo, bool> predicate)
    {
        _min = min;
        _max = max;
        _predicate = predicate;
    }

    public object Create(object request, ISpecimenContext context)
    {
        if (request is PropertyInfo propertyInfo &&
            propertyInfo.PropertyType == typeof(TValue) &&
            _predicate(propertyInfo))
        {
            return GenerateRandomValue();
        }

        return new NoSpecimen();
    }

    private TValue GenerateRandomValue()
    {
        var minDecimal = Convert.ToDecimal(_min);
        var maxDecimal = Convert.ToDecimal(_max);
        var range = maxDecimal - minDecimal;
        var randomValue = minDecimal + (decimal)Random.Shared.NextDouble() * range;

        return typeof(TValue).Name switch
        {
            nameof(Int32) => (TValue)(object)(int)randomValue,
            nameof(Int64) => (TValue)(object)(long)randomValue,
            nameof(Int16) => (TValue)(object)(short)randomValue,
            nameof(Byte) => (TValue)(object)(byte)randomValue,
            nameof(Single) => (TValue)(object)(float)randomValue,
            nameof(Double) => (TValue)(object)(double)randomValue,
            nameof(Decimal) => (TValue)(object)randomValue,
            _ => throw new NotSupportedException($"Type {typeof(TValue).Name} is not supported")
        };
    }
}
```

### 流暢介面擴充方法

```csharp
public static class FixtureRangedNumericExtensions
{
    public static IFixture AddRandomRange<T, TValue>(
        this IFixture fixture, 
        TValue min, 
        TValue max, 
        Func<PropertyInfo, bool> predicate)
        where TValue : struct, IComparable, IConvertible
    {
        fixture.Customizations.Insert(0, 
            new NumericRangeBuilder<TValue>(min, max, predicate));
        return fixture;
    }
}
```

### 完整使用範例

```csharp
public class Product
{
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public int Quantity { get; set; }
    public double Rating { get; set; }
    public float Discount { get; set; }
}

[Fact]
public void 多重數值型別範圍控制()
{
    var fixture = new Fixture();

    fixture
        .AddRandomRange<Product, decimal>(
            50m, 500m,
            prop => prop.Name == "Price" && prop.DeclaringType == typeof(Product))
        .AddRandomRange<Product, int>(
            1, 50,
            prop => prop.Name == "Quantity" && prop.DeclaringType == typeof(Product))
        .AddRandomRange<Product, double>(
            1.0, 5.0,
            prop => prop.Name == "Rating" && prop.DeclaringType == typeof(Product))
        .AddRandomRange<Product, float>(
            0.0f, 0.5f,
            prop => prop.Name == "Discount" && prop.DeclaringType == typeof(Product));

    var products = fixture.CreateMany<Product>(10).ToList();

    products.Should().AllSatisfy(product =>
    {
        product.Price.Should().BeInRange(50m, 500m);
        product.Quantity.Should().BeInRange(1, 49);
        product.Rating.Should().BeInRange(1.0, 5.0);
        product.Discount.Should().BeInRange(0.0f, 0.5f);
    });
}
```

## int vs DateTime 處理差異

### 為何 DateTime 建構器用 Add() 就能生效？

| 型別       | 內建建構器                                        | 優先順序影響               |
| ---------- | ------------------------------------------------- | -------------------------- |
| `int`      | `RangeAttributeRelay`、`NumericSequenceGenerator` | 會被攔截，需用 `Insert(0)` |
| `DateTime` | 無特定建構器                                      | 不會被攔截，`Add()` 即可   |

## 最佳實踐

### 應該做

1. **善用 DataAnnotations**
   - 充分利用現有模型驗證規則
   - AutoFixture 自動產生符合限制的資料

2. **使用 Random.Shared**
   - 避免重複值問題
   - 執行緒安全、效能更好

3. **Insert(0) 確保優先順序**
   - 自訂數值建構器務必用 `Insert(0)`
   - 避免被內建建構器覆蓋

4. **泛型化設計**
   - 建立可重用的泛型建構器
   - 使用擴充方法提供流暢介面

### 應該避免

1. **忽略建構器優先順序**
   - 不要假設 `Add()` 一定生效
   - 測試驗證建構器是否正常運作

2. **過度複雜的邏輯**
   - 建構器保持單一職責
   - 複雜業務邏輯放在測試或服務層

3. **使用 new Random()**
   - 可能產生重複值
   - 非執行緒安全

## 程式碼範本

請參考 [templates](./templates) 資料夾中的範例檔案：

- [dataannotations-integration.cs](./templates/dataannotations-integration.cs) - DataAnnotations 自動整合
- [custom-specimen-builders.cs](./templates/custom-specimen-builders.cs) - 自訂 ISpecimenBuilder 實作
- [numeric-range-extensions.cs](./templates/numeric-range-extensions.cs) - 泛型化數值範圍建構器與擴充方法

## 與其他技能的關係

- **autofixture-basics**：本技能的前置知識，需先掌握基礎用法
- **autodata-xunit-integration**：下一步學習目標，將自訂化與 xUnit 整合
- **autofixture-nsubstitute-integration**：進階整合，結合 Mock 與自訂資料生成

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 11 - AutoFixture 進階：自訂化測試資料生成策略**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374913
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day11

### 官方文件

- [AutoFixture GitHub](https://github.com/AutoFixture/AutoFixture)
- [AutoFixture 官方文件](https://autofixture.github.io/)
- [ISpecimenBuilder 介面](https://autofixture.github.io/docs/fixture-customization/)
