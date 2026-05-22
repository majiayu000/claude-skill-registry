---
name: autofixture-nsubstitute-integration
description: 協助在 .NET 測試中整合 AutoFixture 與 NSubstitute，實現自動模擬（Auto-Mocking）功能。當使用者需要測試有多個相依性的服務類別、建立自訂 AutoData 屬性、或使用 Frozen 機制確保測試一致性時，請使用此技能。
author: Kevin Tsen
license: MIT
version: 1.0.0
tags: [autofixture, nsubstitute, auto-mocking, dependency-injection, xunit, testing]
related_skills:
  - autofixture-basics
  - autofixture-customization
  - autodata-xunit-integration
  - nsubstitute-mocking
---

# AutoFixture + NSubstitute 自動模擬整合

## 技能概述

本技能介紹如何整合 AutoFixture 與 NSubstitute，透過 `AutoFixture.AutoNSubstitute` 套件實現自動模擬（Auto-Mocking）功能。這種整合方式可以大幅簡化具有多個相依性的服務類別測試，讓開發者專注於測試邏輯本身，而非繁瑣的物件建立過程。

### 適用情境

當被要求執行以下任務時，請使用此技能：

- 測試具有多個介面相依性的服務類別
- 建立自動模擬所有介面相依性的測試設定
- 使用 `[Frozen]` 屬性確保相依性實例在測試中保持一致
- 建立專案級的自訂 AutoData 屬性來整合多種客製化設定
- 結合固定測試值與自動產生物件的參數化測試

### 核心價值

- **減少樣板程式碼**：不需要手動為每個介面建立 `Substitute.For<T>()`
- **自動處理複雜相依圖**：AutoFixture 會自動解析並建立所需的物件
- **提升測試維護性**：當建構函式變更時，測試程式碼通常不需要同步修改
- **保持測試重點**：讓開發者專注於測試邏輯而非物件建立

---

## 套件安裝與設定

### 必要套件

```bash
# 核心套件
dotnet add package AutoFixture.AutoNSubstitute

# 相關套件（如尚未安裝）
dotnet add package AutoFixture
dotnet add package AutoFixture.Xunit2
dotnet add package NSubstitute
dotnet add package xunit
```

### NuGet 套件資訊

| 套件名稱                      | 用途                            | NuGet 連結                                                               |
| ----------------------------- | ------------------------------- | ------------------------------------------------------------------------ |
| `AutoFixture.AutoNSubstitute` | AutoFixture 與 NSubstitute 整合 | [nuget.org](https://www.nuget.org/packages/AutoFixture.AutoNSubstitute/) |
| `AutoFixture.Xunit2`          | xUnit 整合（AutoData 屬性）     | [nuget.org](https://www.nuget.org/packages/AutoFixture.Xunit2/)          |
| `NSubstitute`                 | 模擬框架                        | [nuget.org](https://www.nuget.org/packages/NSubstitute/)                 |

---

## 核心概念

### AutoNSubstituteCustomization 的作用

當在 AutoFixture 中加入 `AutoNSubstituteCustomization` 時，它會自動：

1. **偵測介面類型**：當 AutoFixture 遇到介面或抽象類別時
2. **自動建立替身**：使用 NSubstitute 的 `Substitute.For<T>()` 建立 Mock 物件
3. **注入相依性**：將這些替身物件注入到需要的建構函式中
4. **保持實例一致性**：確保相同類型的替身在同一個測試中保持一致

```csharp
using AutoFixture;
using AutoFixture.AutoNSubstitute;

// 建立包含 AutoNSubstitute 功能的 Fixture
var fixture = new Fixture().Customize(new AutoNSubstituteCustomization());

// 自動建立服務和其相依性
// MyService 的所有介面相依性都會自動變成 NSubstitute 的替身
var service = fixture.Create<MyService>();
```

### FrozenAttribute 凍結機制

`[Frozen]` 屬性用來控制測試中某個類型的實例：

- 當參數被標註為 `[Frozen]` 時，AutoFixture 會建立這個類別的一個實例並**凍結**它
- 後續在測試方法中都會使用同一個已凍結的實例
- 這對於需要設定相依性行為然後驗證 SUT 的測試特別重要

```csharp
[Theory]
[AutoData]
public async Task TestMethod(
    [Frozen] IRepository repository,  // 這個 repository 會被凍結
    MyService sut)                    // sut 會使用同一個 repository
{
    // 設定凍結實例的行為
    repository.GetAsync(Arg.Any<int>()).Returns(someData);
    
    // SUT 內部使用的是同一個 repository 實例
    var result = await sut.DoSomething();
}
```

### 參數順序的重要性

使用 `[Frozen]` 時，**參數順序非常重要**：

```csharp
// ✅ 正確：Frozen 參數在 SUT 之前
public async Task TestMethod(
    [Frozen] IRepository repository,
    MyService sut)

// ❌ 錯誤：SUT 會使用不同的 repository 實例
public async Task TestMethod(
    MyService sut,
    [Frozen] IRepository repository)  // 太晚凍結了
```

---

## 傳統方式 vs AutoNSubstitute 方式

### 傳統手動方式

```csharp
[Fact]
public async Task TraditionalWay()
{
    // Arrange - 手動建立每個相依性
    var repository = Substitute.For<IRepository>();
    var logger = Substitute.For<ILogger<OrderService>>();
    var notificationService = Substitute.For<INotificationService>();
    var cacheService = Substitute.For<ICacheService>();
    
    var sut = new OrderService(repository, logger, notificationService, cacheService);

    // 設定替身行為
    repository.GetOrderAsync(Arg.Any<int>()).Returns(someOrder);
    
    // Act
    var result = await sut.GetOrderAsync(orderId);
    
    // Assert
    result.Should().NotBeNull();
}
```

**問題**：

- 當服務增加新相依性時，所有測試都需要修改
- 大量重複的 `Substitute.For<T>()` 呼叫
- 測試程式碼冗長，難以快速理解測試意圖

### 使用 AutoNSubstitute 方式

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task WithAutoNSubstitute(
    [Frozen] IRepository repository,
    OrderService sut)
{
    // Arrange - 相依性已自動建立，只需設定需要的行為
    repository.GetOrderAsync(Arg.Any<int>()).Returns(someOrder);
    
    // Act
    var result = await sut.GetOrderAsync(orderId);
    
    // Assert
    result.Should().NotBeNull();
}
```

**優勢**：

- 只需宣告需要互動的相依性
- 其他相依性（logger, notificationService, cacheService）自動建立
- 建構函式變更時，測試通常不需要修改

---

## 自訂 AutoData 屬性

### 為什麼需要自訂 AutoData 屬性？

在實際專案中，通常需要整合多種客製化設定：

- **AutoNSubstituteCustomization**：自動為介面建立 NSubstitute 替身
- **專案特定的 Customization**：如 Mapper 設定、驗證器設定等
- **一致的測試基礎設施**：確保整個專案使用相同的設定

### AutoDataWithCustomizationAttribute 實作

```csharp
using AutoFixture;
using AutoFixture.AutoNSubstitute;
using AutoFixture.Xunit2;

namespace MyProject.Tests.AutoFixtureConfigurations;

/// <summary>
/// 包含客製化設定的 AutoData 屬性
/// </summary>
public class AutoDataWithCustomizationAttribute : AutoDataAttribute
{
    /// <summary>
    /// 建構函式
    /// </summary>
    public AutoDataWithCustomizationAttribute() : base(CreateFixture)
    {
    }

    private static IFixture CreateFixture()
    {
        var fixture = new Fixture()
            .Customize(new AutoNSubstituteCustomization())
            .Customize(new MapsterMapperCustomization())  // 專案特定設定
            .Customize(new DomainCustomization());        // 領域模型設定

        return fixture;
    }
}
```

### InlineAutoDataWithCustomizationAttribute 實作

用於結合固定測試值與自動產生物件：

```csharp
using AutoFixture;
using AutoFixture.AutoNSubstitute;
using AutoFixture.Xunit2;

namespace MyProject.Tests.AutoFixtureConfigurations;

/// <summary>
/// 包含客製化設定的 InlineAutoData 屬性
/// </summary>
public class InlineAutoDataWithCustomizationAttribute : InlineAutoDataAttribute
{
    /// <summary>
    /// 建構函式
    /// </summary>
    /// <param name="values">固定值（將填入測試方法的前幾個參數）</param>
    public InlineAutoDataWithCustomizationAttribute(params object[] values)
        : base(new AutoDataWithCustomizationAttribute(), values)
    {
    }
}
```

### 重要實作細節

**為什麼使用 `new AutoDataWithCustomizationAttribute()` 而不是 `CreateFixture` 方法？**

```csharp
// ❌ 錯誤：InlineAutoDataAttribute 需要 AutoDataAttribute，不是 Func<IFixture>
public InlineAutoDataWithCustomizationAttribute(params object[] values)
    : base(CreateFixture, values)  // 編譯錯誤或行為異常

// ✅ 正確：傳遞 AutoDataAttribute 實例
public InlineAutoDataWithCustomizationAttribute(params object[] values)
    : base(new AutoDataWithCustomizationAttribute(), values)
```

原因：

- `InlineAutoDataAttribute` 繼承自 `CompositeDataAttribute`
- 它需要接收一個 `AutoDataAttribute` 實例作為資料來源提供者
- 這樣可以重用 `AutoDataWithCustomizationAttribute` 的所有設定

---

## 常見相依性的客製化處理

### IMapper 客製化（Mapster 範例）

某些相依性不適合使用 Mock，而應該使用真實實例：

```csharp
using AutoFixture;
using Mapster;
using MapsterMapper;

namespace MyProject.Tests.AutoFixtureConfigurations;

/// <summary>
/// Mapster 對應器客製化
/// </summary>
public class MapsterMapperCustomization : ICustomization
{
    private IMapper? _mapper;

    public void Customize(IFixture fixture)
    {
        fixture.Register(() => this.Mapper);
    }

    private IMapper Mapper
    {
        get
        {
            if (this._mapper is not null)
            {
                return this._mapper;
            }

            var typeAdapterConfig = new TypeAdapterConfig();
            typeAdapterConfig.Scan(typeof(ServiceMapRegister).Assembly);
            this._mapper = new Mapper(typeAdapterConfig);
            return this._mapper;
        }
    }
}
```

**為什麼 IMapper 不用 Mock？**

1. **工具型相依性**：Mapper 不是業務邏輯，是物件對應工具
2. **驗證對應邏輯**：測試需要驗證對應是否正確，Mock 會失去這個能力
3. **設定複雜度**：為每個對應方法設定 Returns 反而增加複雜度
4. **測試意圖**：我們要測試業務邏輯，不是 Mapper 的行為

### AutoMapper 客製化範例

```csharp
using AutoFixture;
using AutoMapper;

namespace MyProject.Tests.AutoFixtureConfigurations;

public class AutoMapperCustomization : ICustomization
{
    private IMapper? _mapper;

    public void Customize(IFixture fixture)
    {
        fixture.Register(() => this.Mapper);
    }

    private IMapper Mapper
    {
        get
        {
            if (this._mapper is not null)
            {
                return this._mapper;
            }

            var configuration = new MapperConfiguration(cfg =>
            {
                cfg.AddMaps(typeof(MappingProfile).Assembly);
            });

            this._mapper = configuration.CreateMapper();
            return this._mapper;
        }
    }
}
```

---

## 測試實作範例

### 基本測試：無需設定相依行為

當測試只需要驗證 SUT 本身的邏輯（如參數驗證）時：

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task IsExistsAsync_輸入的ShipperId為0時_應拋出ArgumentOutOfRangeException(
    ShipperService sut)
{
    // Arrange
    var shipperId = 0;

    // Act
    var exception = await Assert.ThrowsAsync<ArgumentOutOfRangeException>(
        () => sut.IsExistsAsync(shipperId));

    // Assert
    exception.Message.Should().Contain(nameof(shipperId));
}
```

### 進階測試：設定相依行為

使用 `[Frozen]` 取得相依性並設定其行為：

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task IsExistsAsync_輸入的ShipperId_資料不存在_應回傳false(
    [Frozen] IShipperRepository shipperRepository,
    ShipperService sut)
{
    // Arrange
    var shipperId = 99;
    shipperRepository.IsExistsAsync(Arg.Any<int>()).Returns(false);

    // Act
    var actual = await sut.IsExistsAsync(shipperId);

    // Assert
    actual.Should().BeFalse();
}
```

### 使用自動產生的測試資料

AutoFixture 同時產生 SUT 和測試資料：

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task GetAsync_輸入的ShipperId_資料有存在_應回傳model(
    [Frozen] IShipperRepository shipperRepository,
    ShipperService sut,
    ShipperModel model)  // AutoFixture 自動產生
{
    // Arrange
    var shipperId = model.ShipperId;
    shipperRepository.IsExistsAsync(Arg.Any<int>()).Returns(true);
    shipperRepository.GetAsync(Arg.Any<int>()).Returns(model);

    // Act
    var actual = await sut.GetAsync(shipperId);

    // Assert
    actual.Should().NotBeNull();
    actual.ShipperId.Should().Be(shipperId);
}
```

### 參數化測試：InlineAutoData

結合固定測試值與自動產生的 SUT：

```csharp
[Theory]
[InlineAutoDataWithCustomization(0, 10, nameof(from))]
[InlineAutoDataWithCustomization(-1, 10, nameof(from))]
[InlineAutoDataWithCustomization(1, 0, nameof(size))]
[InlineAutoDataWithCustomization(1, -1, nameof(size))]
public async Task GetCollectionAsync_from與size輸入不合規格內容_應拋出ArgumentOutOfRangeException(
    int from,
    int size,
    string parameterName,
    ShipperService sut)  // 自動產生
{
    // Act
    var exception = await Assert.ThrowsAsync<ArgumentOutOfRangeException>(
        () => sut.GetCollectionAsync(from, size));

    // Assert
    exception.Message.Should().Contain(parameterName);
}
```

### 使用 CollectionSize 控制集合大小

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task GetAllAsync_資料表裡有10筆資料_回傳的集合裡有10筆(
    [Frozen] IShipperRepository shipperRepository,
    ShipperService sut,
    [CollectionSize(10)] IEnumerable<ShipperModel> models)
{
    // Arrange
    shipperRepository.GetAllAsync().Returns(models);

    // Act
    var actual = await sut.GetAllAsync();

    // Assert
    actual.Should().NotBeEmpty();
    actual.Should().HaveCount(10);
}
```

### 複雜資料設定：使用 IFixture

當需要精確控制測試資料時：

```csharp
[Theory]
[AutoDataWithCustomization]
public async Task SearchAsync_companyName輸入資料_有符合條件的資料_回傳集合應包含符合條件的資料(
    IFixture fixture,
    [Frozen] IShipperRepository shipperRepository,
    ShipperService sut)
{
    // Arrange
    const string companyName = "test";
    
    var models = fixture.Build<ShipperModel>()
                        .With(x => x.CompanyName, companyName)
                        .CreateMany(1);

    shipperRepository.GetTotalCountAsync().Returns(1);
    shipperRepository.SearchAsync(Arg.Any<string>(), Arg.Any<string>())
                     .Returns(models);

    // Act
    var actual = await sut.SearchAsync(companyName, string.Empty);

    // Assert
    actual.Should().NotBeEmpty();
    actual.Should().HaveCount(1);
    actual.Any(x => x.CompanyName == companyName).Should().BeTrue();
}
```

### Nullable 參考類型處理

測試 null 或空值參數時的處理方式：

```csharp
[Theory]
[InlineAutoDataWithCustomization(null!, null!)]
[InlineAutoDataWithCustomization("", "")]
[InlineAutoDataWithCustomization("   ", "   ")]
public async Task SearchAsync_companyName與phone都為空白_應拋出ArgumentException(
    string? companyName,
    string? phone,
    ShipperService sut)
{
    // Act & Assert
    var exception = await Assert.ThrowsAsync<ArgumentException>(
        () => sut.SearchAsync(companyName!, phone!));
    
    exception.Message.Should().Contain("companyName 與 phone 不可都為空白");
}
```

**處理說明**：

1. **參數宣告使用 `string?`**：因為測試需要傳入 `null` 值
2. **InlineAutoData 中使用 `null!`**：告訴編譯器這是刻意的測試資料
3. **方法呼叫使用 `!` 運算子**：在測試中使用 null-forgiving 運算子

---

## 適用場景判斷

### 建議使用的場景

| 場景             | 原因                               |
| ---------------- | ---------------------------------- |
| 服務層測試       | 通常有多個相依性，自動模擬效益最大 |
| 複雜相依圖       | AutoFixture 自動處理多層相依性     |
| 參數化測試       | 結合固定值與自動產生資料           |
| 需要大量測試資料 | 減少手動建立測試資料的工作         |
| 快速迭代開發     | 建構函式變更時測試通常不需修改     |

### 謹慎使用的場景

| 場景                   | 原因                                     |
| ---------------------- | ---------------------------------------- |
| 單一相依性測試         | 手動建立可能更清晰直覺                   |
| 精確控制屬性值         | 需要額外的 `fixture.Build().With()` 設定 |
| 團隊不熟悉 AutoFixture | 學習成本可能影響開發效率                 |
| 除錯困難的場景         | 自動產生的物件可能讓除錯變複雜           |
| 效能敏感的測試         | 物件建立的開銷可能影響執行速度           |

---

## 最佳實踐

### 導入策略

1. **漸進式採用**
   - 從簡單的服務類別開始
   - 逐步擴展到複雜場景
   - 讓團隊逐漸熟悉模式

2. **團隊培訓**
   - 確保團隊理解 Frozen 機制
   - 說明參數順序的重要性
   - 分享除錯技巧

3. **建立規範**
   - 何時使用自動產生 vs 手動建立
   - 自訂 Customization 的命名與組織
   - 測試資料的控制策略

### 程式碼組織

```text
MyProject.Tests/
├── AutoFixtureConfigurations/
│   ├── AutoDataWithCustomizationAttribute.cs
│   ├── InlineAutoDataWithCustomizationAttribute.cs
│   ├── AutoMapperCustomization.cs
│   └── DomainCustomization.cs
├── Services/
│   ├── OrderServiceTests.cs
│   └── ShipperServiceTests.cs
└── ...
```

### 命名慣例

- **自訂 AutoData 屬性**：`[專案名稱]AutoDataAttribute` 或 `AutoDataWithCustomizationAttribute`
- **Customization 類別**：`[功能]Customization`（如 `MapsterMapperCustomization`）
- **測試方法**：維持 `方法_情境_預期` 的命名模式

---

## 注意事項與限制

### 常見陷阱

1. **參數順序錯誤**

   ```csharp
   // ❌ Frozen 參數在 SUT 之後，不會生效
   public void Test(MyService sut, [Frozen] IRepository repo)
   
   // ✅ Frozen 參數必須在 SUT 之前
   public void Test([Frozen] IRepository repo, MyService sut)
   ```

2. **遺忘 AutoNSubstituteCustomization**

   ```csharp
   // ❌ 沒有 AutoNSubstitute，介面會產生異常
   var fixture = new Fixture();
   
   // ✅ 加入 AutoNSubstituteCustomization
   var fixture = new Fixture().Customize(new AutoNSubstituteCustomization());
   ```

3. **過度依賴自動產生**

   ```csharp
   // ❌ 測試意圖不明確
   public void Test(Order order, Customer customer, MyService sut)
   {
       var result = sut.Process(order);
       result.Should().NotBeNull();  // 驗證什麼？
   }
   
   // ✅ 明確控制關鍵屬性
   public void Test(IFixture fixture, MyService sut)
   {
       var order = fixture.Build<Order>()
                          .With(o => o.Status, OrderStatus.Pending)
                          .Create();
       
       var result = sut.Process(order);
       result.Status.Should().Be(OrderStatus.Processed);
   }
   ```

### 效能考量

- 每個測試方法都會建立新的 Fixture 和所有相依性
- 複雜物件圖可能增加測試執行時間
- 考慮使用 `[ClassData]` 或 `IClassFixture<T>` 共享設定

---

## 相關技能

| 技能名稱                     | 關聯說明                               |
| ---------------------------- | -------------------------------------- |
| `autofixture-basics`         | AutoFixture 基礎使用，本技能的前置知識 |
| `autofixture-customization`  | 自訂 Customization 的進階用法          |
| `autodata-xunit-integration` | AutoData 屬性家族的完整說明            |
| `nsubstitute-mocking`        | NSubstitute 基礎，Mock 設定的詳細說明  |

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 13 - AutoFixture 整合 NSubstitute：自動建立 Mock 對象**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375114
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day13

### 官方文件

- [AutoFixture.AutoNSubstitute NuGet Package](https://www.nuget.org/packages/AutoFixture.AutoNSubstitute/)
- [AutoFixture Documentation - Auto Mocking](https://autofixture.readthedocs.io/en/stable/)
- [NSubstitute Documentation](https://nsubstitute.github.io/help/getting-started/)

### 延伸閱讀

- [使用 AutoFixture.AutoData 來改寫以前的測試程式碼 | mrkt的程式學習筆記](https://www.dotblogs.com.tw/mrkt/2024/09/29/191300)

---

## 範例檔案

請參考同目錄下的範例程式碼：

- [custom-autodata-attributes.cs](templates/custom-autodata-attributes.cs) - 自訂 AutoData 屬性範本
- [frozen-patterns.cs](templates/frozen-patterns.cs) - Frozen 機制使用模式
- [service-testing-examples.cs](templates/service-testing-examples.cs) - 服務層測試完整範例
