---
name: test-output-logging
description: 協助開發者在 xUnit 測試中正確使用 ITestOutputHelper 與 ILogger 進行測試輸出與記錄。當使用者需要在測試中輸出診斷資訊、驗證記錄行為、或建立測試診斷工具時，請使用此技能。
license: MIT
---

# 測試輸出與記錄專家指南

本技能協助您在 .NET xUnit 測試專案中實作高品質的測試輸出與記錄機制。

## 核心原則

### 1. ITestOutputHelper 使用原則

**正確的注入方式**

- 透過建構式注入 `ITestOutputHelper`
- 每個測試類別的實例與測試方法綁定
- 不可在靜態方法或跨測試方法間共用

```csharp
public class MyTests
{
    private readonly ITestOutputHelper _output;
    
    public MyTests(ITestOutputHelper testOutputHelper)
    {
        _output = testOutputHelper;
    }
}
```

**常見錯誤**

- ❌ 靜態存取：`private static ITestOutputHelper _output`
- ❌ 在非同步測試中未等待即使用
- ❌ 嘗試在 Dispose 方法中使用

### 2. 結構化輸出格式設計

**建議的輸出結構**

```csharp
private void LogSection(string title)
{
    _output.WriteLine($"\n=== {title} ===");
}

private void LogKeyValue(string key, object value)
{
    _output.WriteLine($"{key}: {value}");
}

private void LogTimestamp(DateTime time)
{
    _output.WriteLine($"執行時間: {time:yyyy-MM-dd HH:mm:ss.fff}");
}
```

**輸出時機**

- 測試開始時：記錄測試設置與輸入資料
- 執行過程中：記錄重要的狀態變化
- 斷言前：記錄預期值與實際值
- 測試結束時：記錄執行時間與結果摘要

### 3. ILogger 測試策略

**挑戰：擴充方法無法直接 Mock**

`ILogger.LogError()` 是擴充方法，NSubstitute 無法直接攔截。需要攔截底層的 `Log<TState>` 方法：

```csharp
// ❌ 錯誤：直接 Mock 擴充方法會失敗
logger.Received().LogError(Arg.Any<string>());

// ✅ 正確：攔截底層方法
logger.Received().Log(
    LogLevel.Error,
    Arg.Any<EventId>(),
    Arg.Is<object>(o => o.ToString().Contains("預期訊息")),
    Arg.Any<Exception>(),
    Arg.Any<Func<object, Exception, string>>()
);
```

**解決方案：使用抽象層**

建立 `AbstractLogger<T>` 來簡化測試：

```csharp
public abstract class AbstractLogger<T> : ILogger<T>
{
    public IDisposable BeginScope<TState>(TState state) 
        => null;
    
    public bool IsEnabled(LogLevel logLevel) 
        => true;
    
    public void Log<TState>(
        LogLevel logLevel,
        EventId eventId,
        TState state,
        Exception exception,
        Func<TState, Exception, string> formatter)
    {
        Log(logLevel, exception, state?.ToString() ?? string.Empty);
    }
    
    public abstract void Log(LogLevel logLevel, Exception ex, string information);
}
```

**測試時使用**

```csharp
var logger = Substitute.For<AbstractLogger<MyService>>();
// 現在可以簡單驗證
logger.Received().Log(LogLevel.Error, Arg.Any<Exception>(), Arg.Is<string>(s => s.Contains("錯誤訊息")));
```

### 4. 診斷工具整合

**XUnitLogger：將記錄導向測試輸出**

```csharp
public class XUnitLogger<T> : ILogger<T>
{
    private readonly ITestOutputHelper _testOutputHelper;
    
    public XUnitLogger(ITestOutputHelper testOutputHelper)
    {
        _testOutputHelper = testOutputHelper;
    }
    
    public void Log<TState>(LogLevel logLevel, EventId eventId, TState state, 
        Exception exception, Func<TState, Exception, string> formatter)
    {
        var message = formatter(state, exception);
        _testOutputHelper.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] [{logLevel}] [{typeof(T).Name}] {message}");
        if (exception != null)
        {
            _testOutputHelper.WriteLine($"Exception: {exception}");
        }
    }
    
    // 其他必要的介面實作...
}
```

**CompositeLogger：同時支援驗證與輸出**

```csharp
public class CompositeLogger<T> : ILogger<T>
{
    private readonly ILogger<T>[] _loggers;
    
    public CompositeLogger(params ILogger<T>[] loggers)
    {
        _loggers = loggers;
    }
    
    public void Log<TState>(LogLevel logLevel, EventId eventId, TState state,
        Exception exception, Func<TState, Exception, string> formatter)
    {
        foreach (var logger in _loggers)
        {
            logger.Log(logLevel, eventId, state, exception, formatter);
        }
    }
    
    // 其他介面實作會委派給所有內部 logger...
}
```

**使用方式**

```csharp
// 同時進行行為驗證與測試輸出
var mockLogger = Substitute.For<AbstractLogger<MyService>>();
var xunitLogger = new XUnitLogger<MyService>(_output);
var compositeLogger = new CompositeLogger<MyService>(mockLogger, xunitLogger);

var service = new MyService(compositeLogger);
```

## 實作指南

### 效能測試中的時間點記錄

```csharp
[Fact]
public async Task ProcessLargeDataSet_效能測試()
{
    // Arrange
    var stopwatch = Stopwatch.StartNew();
    var checkpoints = new List<(string Stage, TimeSpan Elapsed)>();
    
    _output.WriteLine("開始處理大型資料集...");
    
    // Act & Monitor
    await processor.LoadData(dataSet);
    checkpoints.Add(("資料載入", stopwatch.Elapsed));
    _output.WriteLine($"資料載入完成: {stopwatch.Elapsed.TotalMilliseconds:F2} ms");
    
    await processor.ProcessData();
    checkpoints.Add(("資料處理", stopwatch.Elapsed));
    _output.WriteLine($"資料處理完成: {stopwatch.Elapsed.TotalMilliseconds:F2} ms");
    
    stopwatch.Stop();
    
    // Assert & Report
    _output.WriteLine("\n=== 效能報告 ===");
    foreach (var (stage, elapsed) in checkpoints)
    {
        _output.WriteLine($"{stage}: {elapsed.TotalMilliseconds:F2} ms");
    }
}
```

### 診斷測試基底類別

```csharp
public abstract class DiagnosticTestBase
{
    protected readonly ITestOutputHelper Output;
    
    protected DiagnosticTestBase(ITestOutputHelper output)
    {
        Output = output;
    }
    
    protected void LogTestStart(string testName)
    {
        Output.WriteLine($"\n=== {testName} ===");
        Output.WriteLine($"執行時間: {DateTime.Now:yyyy-MM-dd HH:mm:ss.fff}");
    }
    
    protected void LogTestData(object data)
    {
        Output.WriteLine($"測試資料: {JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true })}");
    }
    
    protected void LogAssertionFailure(string field, object expected, object actual)
    {
        Output.WriteLine("\n=== 斷言失敗 ===");
        Output.WriteLine($"欄位: {field}");
        Output.WriteLine($"預期值: {expected}");
        Output.WriteLine($"實際值: {actual}");
    }
}
```

## DO - 建議做法

1. **適當使用 ITestOutputHelper**
   - ✅ 在複雜測試中記錄重要步驟
   - ✅ 採用一致的結構化輸出格式
   - ✅ 測試失敗時提供診斷資訊
   - ✅ 在效能測試中記錄時間點

2. **Logger 測試策略**
   - ✅ 使用抽象層（AbstractLogger）簡化測試
   - ✅ 驗證記錄層級而非完整訊息
   - ✅ 使用 CompositeLogger 結合 Mock 與實際輸出
   - ✅ 確保敏感資料不被記錄

3. **結構化輸出**
   - ✅ 使用章節標題分隔不同階段
   - ✅ 包含時間戳記便於追蹤
   - ✅ 提供足夠的上下文資訊

## DON'T - 避免做法

1. **不要過度使用輸出**
   - ❌ 避免在每個測試中都大量輸出
   - ❌ 不要記錄敏感資訊（密碼、金鑰）
   - ❌ 避免影響測試執行效能

2. **不要硬編碼記錄驗證**
   - ❌ 避免驗證完整的記錄訊息（易碎）
   - ❌ 不要驗證記錄呼叫的確切次數（過度指定）
   - ❌ 避免測試內部實作細節

3. **不要忽略生命週期**
   - ❌ 不要在靜態方法中使用 ITestOutputHelper
   - ❌ 不要嘗試跨測試方法共用實例
   - ❌ 避免在非同步測試中遺漏等待

## 範例參考

參考 `templates/` 目錄下的完整範例：

- `itestoutputhelper-example.cs` - ITestOutputHelper 使用範例
- `ilogger-testing-example.cs` - ILogger 測試策略範例
- `diagnostic-tools.cs` - XUnitLogger 與 CompositeLogger 實作

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 08 - 測試輸出與記錄：xUnit ITestOutputHelper 與 ILogger**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374584
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day08

### 官方文件

- [xUnit Capturing Output](https://xunit.net/docs/capturing-output)

### 相關技能

- `unit-test-fundamentals` - 單元測試基礎
- `xunit-project-setup` - xUnit 專案設定
- `nsubstitute-mocking` - 測試替身與模擬

## 測試清單

在實作測試輸出與記錄時，確認以下檢查項目：

- [ ] ITestOutputHelper 透過建構式正確注入
- [ ] 使用結構化的輸出格式（章節、時間戳記）
- [ ] Logger 測試使用抽象層或 CompositeLogger
- [ ] 驗證記錄層級而非完整訊息
- [ ] 效能測試包含時間點記錄
- [ ] 沒有在輸出中洩漏敏感資訊
- [ ] 非同步測試正確等待記錄完成
- [ ] 測試失敗時提供足夠的診斷資訊
