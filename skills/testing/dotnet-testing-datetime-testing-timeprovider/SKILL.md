---
name: dotnet-testing-datetime-testing-timeprovider
description: |
  使用 TimeProvider 測試時間相依邏輯的專門技能。當需要測試 DateTime、控制時間流逝、處理時區轉換、測試過期邏輯時使用。涵蓋 TimeProvider 抽象化、FakeTimeProvider 時間控制、時間凍結與快轉等。
  Keywords: datetime, time testing, 時間測試, TimeProvider, FakeTimeProvider, DateTime.Now, 時間相依, 快取過期, token 過期, Microsoft.Bcl.TimeProvider, GetUtcNow, SetUtcNow, Advance, time freeze, 時間凍結, 時間快轉
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, TimeProvider, DateTime, time testing"
---

# DateTime 與時間相依性測試指南

## 概述

本技能指導如何使用 Microsoft.Bcl.TimeProvider 解決時間相依程式碼的測試問題。透過時間抽象化，讓「現在時間」變得可控制、可預測、可重現。

### 適用場景

- **營業時間判斷**：系統根據當前時間決定是否允許操作
- **優惠活動控制**：特定日期或時段才生效的促銷邏輯
- **快取過期機制**：依據時間決定資料是否有效
- **排程任務觸發**：定時執行的背景作業
- **Token 有效期限**：驗證時間敏感的安全機制

### 必要套件

```xml
<!-- 正式程式碼 -->
<PackageReference Include="Microsoft.Bcl.TimeProvider" Version="9.0.0" />

<!-- 測試專案 -->
<PackageReference Include="Microsoft.Extensions.TimeProvider.Testing" Version="9.0.0" />
```

---

## 核心原則

### 原則一：時間抽象化 - 以 TimeProvider 取代 DateTime

**傳統問題程式碼**：

```csharp
// ❌ 無法測試 - 直接使用靜態時間
public class OrderService
{
    public bool CanPlaceOrder()
    {
        var now = DateTime.Now;
        return now.Hour >= 9 && now.Hour < 17;
    }
}
```

**可測試的重構**：

```csharp
// ✅ 可測試 - 透過依賴注入接收 TimeProvider
public class OrderService
{
    private readonly TimeProvider _timeProvider;
    
    public OrderService(TimeProvider timeProvider)
    {
        _timeProvider = timeProvider ?? throw new ArgumentNullException(nameof(timeProvider));
    }
    
    public bool CanPlaceOrder()
    {
        var now = _timeProvider.GetLocalNow();
        return now.Hour >= 9 && now.Hour < 17;
    }
}
```

**依賴注入設定**：

```csharp
// Program.cs - 生產環境使用系統時間
services.AddSingleton(TimeProvider.System);
services.AddScoped<OrderService>();
```

### 原則二：FakeTimeProvider 控制測試時間

FakeTimeProvider 提供完整的時間控制能力：

| 方法                             | 用途          | 使用時機            |
| -------------------------------- | ------------- | ------------------- |
| `SetUtcNow(DateTimeOffset)`      | 設定 UTC 時間 | 需要精確 UTC 時間時 |
| `SetLocalTimeZone(TimeZoneInfo)` | 設定本地時區  | 測試時區相關邏輯    |
| `Advance(TimeSpan)`              | 時間快轉      | 測試過期、延遲邏輯  |
| `GetUtcNow()`                    | 取得 UTC 時間 | 讀取當前模擬時間    |
| `GetLocalNow()`                  | 取得本地時間  | 讀取本地模擬時間    |

**建議擴充方法**：

```csharp
public static class FakeTimeProviderExtensions
{
    /// <summary>
    /// 設定 FakeTimeProvider 的本地時間
    /// </summary>
    public static void SetLocalNow(this FakeTimeProvider fakeTimeProvider, DateTime localDateTime)
    {
        fakeTimeProvider.SetLocalTimeZone(TimeZoneInfo.Local);
        var utcTime = TimeZoneInfo.ConvertTimeToUtc(localDateTime, TimeZoneInfo.Local);
        fakeTimeProvider.SetUtcNow(utcTime);
    }
}
```

### 原則三：每個測試使用獨立的時間環境

```csharp
// ✅ 正確：每個測試獨立建立 FakeTimeProvider
public class OrderServiceTests
{
    [Fact]
    public void CanPlaceOrder_在營業時間內_應回傳True()
    {
        // Arrange - 獨立實例
        var fakeTimeProvider = new FakeTimeProvider();
        fakeTimeProvider.SetLocalNow(new DateTime(2024, 3, 15, 14, 0, 0));
        var sut = new OrderService(fakeTimeProvider);
        
        // Act
        var result = sut.CanPlaceOrder();
        
        // Assert
        result.Should().BeTrue();
    }
}

// ❌ 避免：多個測試共用靜態實例
public class BadTestClass
{
    private static readonly FakeTimeProvider SharedProvider = new(); // 會互相干擾
}
```

---

## 進階時間控制技術

### 時間凍結

當需要驗證多個操作發生在「同一時間點」：

```csharp
[Fact]
public void ProcessBatch_在固定時間點_應產生相同時間戳()
{
    var fakeTimeProvider = new FakeTimeProvider();
    var fixedTime = new DateTime(2024, 12, 25, 10, 30, 0);
    fakeTimeProvider.SetLocalNow(fixedTime);
    
    var processor = new BatchProcessor(fakeTimeProvider);
    
    var result1 = processor.ProcessItem("Item1");
    var result2 = processor.ProcessItem("Item2");
    
    // 時間被凍結，兩次操作的時間戳相同
    result1.Timestamp.Should().Be(result2.Timestamp);
}
```

### 時間快轉 (Advance)

測試快取過期、Token 失效等時間敏感邏輯：

```csharp
[Fact]
public void Cache_經過過期時間_應清除項目()
{
    var fakeTimeProvider = new FakeTimeProvider();
    fakeTimeProvider.SetLocalNow(new DateTime(2024, 3, 15, 10, 0, 0));
    
    var cache = new TimedCache(fakeTimeProvider, TimeSpan.FromMinutes(5));
    cache.Set("key", "value");
    
    // 3 分鐘後 - 尚未過期
    fakeTimeProvider.Advance(TimeSpan.FromMinutes(3));
    cache.Get("key").Should().Be("value");
    
    // 再 3 分鐘後（共 6 分鐘）- 已過期
    fakeTimeProvider.Advance(TimeSpan.FromMinutes(3));
    cache.Get("key").Should().BeNull();
}
```

> **重要**：`Advance()` 是非阻塞的，瞬間完成時間跳躍，不會真正等待。

### 時間倒轉

測試歷史資料處理或重播場景：

```csharp
[Fact]
public void HistoricalDataProcessor_回到過去時間_應正確處理()
{
    var fakeTimeProvider = new FakeTimeProvider();
    var historicalTime = new DateTime(2020, 1, 15, 9, 0, 0);
    fakeTimeProvider.SetLocalNow(historicalTime);
    
    var processor = new HistoricalDataProcessor(fakeTimeProvider);
    var result = processor.ProcessDataForDate(historicalTime.Date);
    
    result.ProcessedAt.Should().Be(historicalTime);
}
```

---

## 實戰測試模式

### 模式一：參數化邊界測試

```csharp
[Theory]
[InlineData(8, false)]   // 上午 8 點 - 營業時間前
[InlineData(9, true)]    // 上午 9 點 - 剛開始營業
[InlineData(12, true)]   // 中午 12 點 - 營業時間內
[InlineData(16, true)]   // 下午 4 點 - 營業時間內
[InlineData(17, false)]  // 下午 5 點 - 剛結束營業
[InlineData(18, false)]  // 下午 6 點 - 營業時間後
public void CanPlaceOrder_不同時間點_應回傳正確結果(int hour, bool expected)
{
    var fakeTimeProvider = new FakeTimeProvider();
    fakeTimeProvider.SetLocalNow(new DateTime(2024, 3, 15, hour, 0, 0));
    
    var sut = new OrderService(fakeTimeProvider);
    
    sut.CanPlaceOrder().Should().Be(expected);
}
```

### 模式二：交易時間窗口測試

```csharp
[Theory]
[InlineData("09:30:00", true)]   // 上午交易時間
[InlineData("12:00:00", false)]  // 中午休息
[InlineData("14:30:00", true)]   // 下午交易時間
[InlineData("15:30:00", false)]  // 交易結束後
public void IsInTradingHours_不同時間_應回傳正確結果(string timeStr, bool expected)
{
    var fakeTimeProvider = new FakeTimeProvider();
    var testTime = DateTime.Today.Add(TimeSpan.Parse(timeStr));
    fakeTimeProvider.SetLocalNow(testTime);
    
    var sut = new TradingService(fakeTimeProvider);
    
    sut.IsInTradingHours().Should().Be(expected);
}
```

### 模式三：排程觸發邏輯測試

```csharp
[Theory]
[InlineData("2024-03-15 14:30:00", "2024-03-15 14:00:00", true)]   // 已到執行時間
[InlineData("2024-03-15 13:30:00", "2024-03-15 14:00:00", false)]  // 尚未到時間
public void ShouldExecuteJob_根據時間判斷_應回傳正確結果(
    string currentTimeStr, string scheduledTimeStr, bool expected)
{
    var fakeTimeProvider = new FakeTimeProvider();
    fakeTimeProvider.SetLocalNow(DateTime.Parse(currentTimeStr));
    
    var schedule = new JobSchedule { NextExecutionTime = DateTime.Parse(scheduledTimeStr) };
    var sut = new ScheduleService(fakeTimeProvider);
    
    sut.ShouldExecuteJob(schedule).Should().Be(expected);
}
```

---

## AutoFixture 整合

### FakeTimeProviderCustomization

```csharp
public class FakeTimeProviderCustomization : ICustomization
{
    public void Customize(IFixture fixture)
    {
        fixture.Register(() => new FakeTimeProvider());
    }
}
```

### AutoDataWithCustomization 屬性

```csharp
public class AutoDataWithCustomizationAttribute : AutoDataAttribute
{
    public AutoDataWithCustomizationAttribute() : base(CreateFixture)
    {
    }
    
    private static IFixture CreateFixture()
    {
        return new Fixture()
            .Customize(new AutoNSubstituteCustomization())
            .Customize(new FakeTimeProviderCustomization());
    }
}
```

### 使用 Matching.DirectBaseType

```csharp
[Theory]
[AutoDataWithCustomization]
public void GetTimeBasedDiscount_週五_應回傳九折優惠(
    [Frozen(Matching.DirectBaseType)] FakeTimeProvider fakeTimeProvider,
    OrderService sut)
{
    // Matching.DirectBaseType 讓 AutoFixture 知道：
    // 當需要 TimeProvider（基底類型）時，使用 FakeTimeProvider（衍生類型）
    
    var fridayTime = new DateTime(2024, 3, 15, 14, 0, 0); // 週五
    fakeTimeProvider.SetLocalNow(fridayTime);
    
    sut.GetTimeBasedDiscount().Should().Be("週五快樂：九折優惠");
}
```

> **關鍵**：必須使用 `[Frozen(Matching.DirectBaseType)]`，否則 AutoFixture 無法正確將 FakeTimeProvider 注入到需要 TimeProvider 的建構式中。

---

## 最佳實踐檢查清單

### ✅ 程式碼設計

- [ ] 所有時間相依類別透過建構式接收 `TimeProvider`
- [ ] 使用 `_timeProvider.GetLocalNow()` 取代 `DateTime.Now`
- [ ] 使用 `_timeProvider.GetUtcNow()` 取代 `DateTime.UtcNow`
- [ ] DI 容器註冊 `TimeProvider.System` 作為生產環境實作

### ✅ 測試設計

- [ ] 每個測試方法使用獨立的 `FakeTimeProvider` 實例
- [ ] 使用 `SetLocalNow()` 擴充方法簡化時間設定
- [ ] 使用 `Advance()` 測試時間敏感邏輯（快取、過期、延遲）
- [ ] 測試涵蓋邊界條件（開始時間、結束時間、臨界點）

### ✅ 進階考量

- [ ] FakeTimeProvider 是執行緒安全的，可用於並行測試
- [ ] 使用 `IDisposable` 模式正確釋放 FakeTimeProvider
- [ ] 時區測試使用 `SetLocalTimeZone()` 明確設定時區

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 16 - 測試日期與時間：Microsoft.Bcl.TimeProvider 取代 DateTime**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10375821
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day16

### 官方文件

- [TimeProvider API](https://learn.microsoft.com/zh-tw/dotnet/api/system.timeprovider)
- [Microsoft.Bcl.TimeProvider NuGet](https://www.nuget.org/packages/Microsoft.Bcl.TimeProvider/)
- [Microsoft.Extensions.TimeProvider.Testing NuGet](https://www.nuget.org/packages/Microsoft.Extensions.TimeProvider.Testing/)

### 相關技能

- `autofixture-basics` - AutoFixture 自動測試資料生成
- `nsubstitute-mocking` - 測試替身與模擬
- `autodata-xunit-integration` - xUnit 與 AutoFixture 的 AutoData 整合
