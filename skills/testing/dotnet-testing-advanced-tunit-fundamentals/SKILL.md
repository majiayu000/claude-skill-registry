---
name: dotnet-testing-advanced-tunit-fundamentals
description: |
  TUnit 新世代測試框架入門完整指南。涵蓋 Source Generator 驅動測試發現、AOT 編譯支援、流暢式非同步斷言。包含專案建立、[Test] 屬性、生命週期管理、並行控制與 xUnit 語法對照。
  Keywords: TUnit, tunit testing, source generator testing, AOT testing, 新世代測試框架, [Test], [Arguments], TUnit.Assertions, Assert.That, Before(Test), After(Test), NotInParallel, TUnit.Templates, Microsoft.Testing.Platform, TUnit vs xUnit, 並行執行
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: "tunit, testing-framework, source-generator, aot, modern-testing, performance"
---

# TUnit 新世代測試框架入門基礎

## 技能概述

本技能涵蓋 TUnit 新世代 .NET 測試框架的入門基礎，從框架特色到實際專案建立與測試撰寫。

**核心主題：**

- TUnit 框架特色與設計理念
- Source Generator 驅動的測試發現
- AOT (Ahead-of-Time) 編譯支援
- 流暢式非同步斷言系統
- 專案建立與套件配置
- 與 xUnit 的語法差異比較

---

## TUnit 框架核心特色

### 1. Source Generator 驅動的測試發現

TUnit 與傳統測試框架最大的差異在於使用 Source Generator 在**編譯時期**完成測試發現：

**傳統框架的方式（xUnit）：**

```csharp
// xUnit 在執行時期透過反射掃描所有方法
public class TraditionalTests
{
    [Fact] // 執行時期才被發現
    public void TestMethod() { }
}
```

**TUnit 的創新做法：**

```csharp
// TUnit 在編譯時期就透過 Source Generator 產生測試註冊程式碼
public class ModernTests
{
    [Test] // 編譯時期就被處理和最佳化
    public async Task TestMethod() 
    {
        await Assert.That(true).IsTrue();
    }
}
```

**優勢：**

1. 避免反射成本：所有測試發現在編譯時期完成
2. AOT 相容：完全支援 Native AOT 編譯
3. 更快的啟動時間：特別是在大型測試專案中

### 2. AOT (Ahead-of-Time) 編譯支援

**JIT vs AOT 編譯流程：**

```text
傳統 JIT：C# 原始碼 → IL 中間碼 → 執行時期 JIT 編譯 → 機器碼 → 執行
AOT：    C# 原始碼 → 編譯時期直接產生 → 機器碼 → 直接執行
```

**AOT 編譯的優勢：**

- 超快啟動時間（無需等待 JIT 編譯）
- 更小的記憶體占用
- 可預測的效能
- 更適合容器化部署

**啟用 AOT 支援：**

```xml
<PropertyGroup>
    <PublishAot>true</PublishAot>
    <InvariantGlobalization>true</InvariantGlobalization>
</PropertyGroup>
```

**實際效能差異：**

```text
傳統 JIT 編譯測試啟動時間：約 1-2 秒
TUnit AOT 編譯測試啟動時間：約 50-100 毫秒
（大型專案可達 10-30 倍啟動時間改善）
```

### 3. Microsoft.Testing.Platform 採用

TUnit 建構在微軟最新的 Microsoft.Testing.Platform 之上，而非傳統的 VSTest 平台：

- 更輕量的測試執行器
- 更好的並行控制機制
- 原生支援最新的 IDE 整合

**重要注意事項：**
TUnit 專案**不需要**也**不應該**安裝 `Microsoft.NET.Test.Sdk` 套件。

### 4. 預設並行執行

TUnit 將並行執行設為預設，並提供精細的控制：

```csharp
// 預設所有測試都會並行執行
[Test]
public async Task ParallelTest1() { }

[Test]
public async Task ParallelTest2() { }

// 需要時可以控制並行行為
[Test]
[NotInParallel("DatabaseTests")]
public async Task DatabaseTest() { }
```

---

## TUnit 專案建立

### 方式一：手動建立（理解底層架構）

```bash
# 建立專案目錄
mkdir TUnitDemo
cd TUnitDemo

# 建立解決方案
dotnet new sln -n MyApp

# 建立主專案
dotnet new classlib -n MyApp.Core -o src/MyApp.Core

# 建立測試專案（使用 console 模板）
dotnet new console -n MyApp.Tests -o tests/MyApp.Tests

# 加入解決方案
dotnet sln add src/MyApp.Core/MyApp.Core.csproj
dotnet sln add tests/MyApp.Tests/MyApp.Tests.csproj

# 加入專案參考
dotnet add tests/MyApp.Tests/MyApp.Tests.csproj reference src/MyApp.Core/MyApp.Core.csproj
```

### 方式二：使用 TUnit Template（推薦）

```bash
# 安裝 TUnit 專案模板
dotnet new install TUnit.Templates

# 使用 TUnit template 建立測試專案
dotnet new tunit -n MyApp.Tests -o tests/MyApp.Tests
```

### 測試專案 csproj 設定

```xml
<Project Sdk="Microsoft.NET.Sdk">

  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <!-- TUnit 核心套件 -->
    <PackageReference Include="TUnit" Version="0.57.24" />
    <!-- 程式碼覆蓋率支援 -->
    <PackageReference Include="Microsoft.Testing.Extensions.CodeCoverage" Version="17.12.4" />
    <!-- TRX 報告支援 -->
    <PackageReference Include="Microsoft.Testing.Extensions.TrxReport" Version="1.4.3" />
  </ItemGroup>

  <ItemGroup>
    <ProjectReference Include="..\..\src\MyApp.Core\MyApp.Core.csproj" />
  </ItemGroup>

</Project>
```

### GlobalUsings 設定

```csharp
// GlobalUsings.cs
global using TUnit.Core;
global using TUnit.Assertions;
global using MyApp.Core;
```

---

## 非同步測試方法（必要）

TUnit 的**所有測試方法都必須是非同步的**，這是框架的技術要求：

```csharp
// ❌ 錯誤：無法編譯
[Test]
public void WrongTest()
{
    Assert.That(1 + 1).IsEqualTo(2);
}

// ✅ 正確：使用 async Task
[Test]
public async Task CorrectTest()
{
    await Assert.That(1 + 1).IsEqualTo(2);
}
```

---

## 測試屬性與參數化

### 基本測試 [Test]

TUnit 統一使用 `[Test]` 屬性，不像 xUnit 區分 `[Fact]` 和 `[Theory]`：

```csharp
// TUnit：統一使用 [Test]
[Test]
public async Task Add_輸入1和2_應回傳3()
{
    var calculator = new Calculator();
    var result = calculator.Add(1, 2);
    await Assert.That(result).IsEqualTo(3);
}
```

### 參數化測試 [Arguments]

```csharp
// TUnit：使用 [Arguments]（相當於 xUnit 的 [InlineData]）
[Test]
[Arguments(1, 2, 3)]
[Arguments(-1, 1, 0)]
[Arguments(0, 0, 0)]
[Arguments(100, -50, 50)]
public async Task Add_多組輸入_應回傳正確結果(int a, int b, int expected)
{
    var calculator = new Calculator();
    var result = calculator.Add(a, b);
    await Assert.That(result).IsEqualTo(expected);
}
```

---

## TUnit.Assertions 斷言系統

TUnit 採用流暢式（Fluent）斷言設計，所有斷言都是非同步的：

### 基本相等性斷言

```csharp
[Test]
public async Task 基本相等性斷言範例()
{
    var expected = 42;
    var actual = 40 + 2;
    
    await Assert.That(actual).IsEqualTo(expected);
    await Assert.That(actual).IsNotEqualTo(43);
    
    // Null 檢查
    string? nullValue = null;
    await Assert.That(nullValue).IsNull();
    await Assert.That("test").IsNotNull();
}
```

### 布林值斷言

```csharp
[Test]
public async Task 布林值斷言範例()
{
    var condition = 1 + 1 == 2;
    
    await Assert.That(condition).IsTrue();
    await Assert.That(1 + 1 == 3).IsFalse();
    
    var number = 10;
    await Assert.That(number > 5).IsTrue();
}
```

### 數值比較斷言

```csharp
[Test]
public async Task 數值比較斷言範例()
{
    var actual = 10;
    
    await Assert.That(actual).IsGreaterThan(5);
    await Assert.That(actual).IsGreaterThanOrEqualTo(10);
    await Assert.That(actual).IsLessThan(15);
    await Assert.That(actual).IsBetween(5, 15);
}

[Test]
[Arguments(3.14159, 3.14, 0.01)]
public async Task 浮點數精確度控制(double actual, double expected, double tolerance)
{
    await Assert.That(actual)
        .IsEqualTo(expected)
        .Within(tolerance);
}
```

### 字串斷言

```csharp
[Test]
public async Task 字串斷言範例()
{
    var email = "user@example.com";
    
    await Assert.That(email).Contains("@");
    await Assert.That(email).StartsWith("user");
    await Assert.That(email).EndsWith(".com");
    await Assert.That(email).DoesNotContain(" ");
    await Assert.That("").IsEmpty();
    await Assert.That(email).IsNotEmpty();
}
```

### 集合斷言

```csharp
[Test]
public async Task 集合斷言範例()
{
    var numbers = new List<int> { 1, 2, 3, 4, 5 };
    
    await Assert.That(numbers).HasCount(5);
    await Assert.That(numbers).IsNotEmpty();
    await Assert.That(numbers).Contains(3);
    await Assert.That(numbers).DoesNotContain(10);
    await Assert.That(numbers.First()).IsEqualTo(1);
    await Assert.That(numbers.Last()).IsEqualTo(5);
}
```

### 例外斷言

```csharp
[Test]
public async Task 例外斷言範例()
{
    var calculator = new Calculator();
    
    // 檢查特定例外類型
    await Assert.That(() => calculator.Divide(10, 0))
        .Throws<DivideByZeroException>();
    
    // 檢查例外訊息
    await Assert.That(() => calculator.Divide(10, 0))
        .Throws<DivideByZeroException>()
        .WithMessage("除數不能為零");
    
    // 檢查不拋出例外
    await Assert.That(() => calculator.Add(1, 2))
        .DoesNotThrow();
}
```

### And / Or 條件組合

```csharp
[Test]
public async Task 條件組合範例()
{
    var number = 10;
    
    // And：所有條件都必須成立
    await Assert.That(number)
        .IsGreaterThan(5)
        .And.IsLessThan(15)
        .And.IsEqualTo(10);
    
    // Or：任一條件成立即可
    await Assert.That(number)
        .IsEqualTo(5)
        .Or.IsEqualTo(10)
        .Or.IsEqualTo(15);
}
```

---

## 測試生命週期管理

### 建構式與 Dispose 模式

```csharp
public class BasicLifecycleTests : IDisposable
{
    private readonly Calculator _calculator;

    public BasicLifecycleTests()
    {
        _calculator = new Calculator();
    }

    [Test]
    public async Task Add_基本測試()
    {
        await Assert.That(_calculator.Add(1, 2)).IsEqualTo(3);
    }

    public void Dispose()
    {
        // 清理資源
    }
}
```

### Before / After 屬性

TUnit 提供更細緻的生命週期控制：

```csharp
public class LifecycleTests
{
    private static TestDatabase? _database;

    // 類別層級：所有測試執行前只執行一次
    [Before(Class)]
    public static async Task ClassSetup()
    {
        _database = new TestDatabase();
        await _database.InitializeAsync();
    }

    // 測試層級：每個測試執行前都會執行
    [Before(Test)]
    public async Task TestSetup()
    {
        await _database!.ClearDataAsync();
    }

    [Test]
    public async Task 測試使用者建立()
    {
        var userService = new UserService(_database!);
        var user = await userService.CreateUserAsync("test@example.com");
        await Assert.That(user.Id).IsNotEqualTo(Guid.Empty);
    }

    // 測試層級：每個測試執行後都會執行
    [After(Test)]
    public async Task TestTearDown()
    {
        // 記錄測試結果
    }

    // 類別層級：所有測試執行後只執行一次
    [After(Class)]
    public static async Task ClassTearDown()
    {
        if (_database != null)
        {
            await _database.DisposeAsync();
        }
    }
}
```

### 生命週期屬性種類

| 屬性                 | 類型     | 說明                     |
| -------------------- | -------- | ------------------------ |
| `[Before(Test)]`     | 實例方法 | 每個測試執行前           |
| `[Before(Class)]`    | 靜態方法 | 類別中第一個測試執行前   |
| `[Before(Assembly)]` | 靜態方法 | 組件中第一個測試執行前   |
| `[After(Test)]`      | 實例方法 | 每個測試執行後           |
| `[After(Class)]`     | 靜態方法 | 類別中最後一個測試執行後 |
| `[After(Assembly)]`  | 靜態方法 | 組件中最後一個測試執行後 |

### 執行順序

```text
1. Before(Class)
2. 建構式
3. Before(Test)
4. 測試方法
5. After(Test)
6. Dispose
7. After(Class)
```

---

## 並行執行控制

### NotInParallel 屬性

```csharp
// 預設並行執行
[Test]
public async Task 並行測試1() { }

[Test]
public async Task 並行測試2() { }

// 控制特定測試不要並行
[Test]
[NotInParallel("DatabaseTests")]
public async Task 資料庫測試1_不並行執行()
{
    // 這個測試不會與其他 "DatabaseTests" 群組並行執行
}

[Test]
[NotInParallel("DatabaseTests")]
public async Task 資料庫測試2_不並行執行()
{
    // 與資料庫測試1 依序執行
}
```

---

## xUnit 與 TUnit 語法對照

| 功能           | xUnit                                 | TUnit                                            |
| -------------- | ------------------------------------- | ------------------------------------------------ |
| **基本測試**   | `[Fact]`                              | `[Test]`                                         |
| **參數化測試** | `[Theory]` + `[InlineData]`           | `[Test]` + `[Arguments]`                         |
| **基本斷言**   | `Assert.Equal(expected, actual)`      | `await Assert.That(actual).IsEqualTo(expected)`  |
| **布林斷言**   | `Assert.True(condition)`              | `await Assert.That(condition).IsTrue()`          |
| **例外測試**   | `Assert.Throws<T>(() => action())`    | `await Assert.That(() => action()).Throws<T>()`  |
| **Null 檢查**  | `Assert.Null(value)`                  | `await Assert.That(value).IsNull()`              |
| **字串檢查**   | `Assert.Contains("text", fullString)` | `await Assert.That(fullString).Contains("text")` |

### 遷移範例

**xUnit 原始程式碼：**

```csharp
[Theory]
[InlineData("test@example.com", true)]
[InlineData("invalid", false)]
public void IsValidEmail_各種輸入_應回傳正確驗證結果(string email, bool expected)
{
    var result = _validator.IsValidEmail(email);
    Assert.Equal(expected, result);
}
```

**TUnit 轉換後：**

```csharp
[Test]
[Arguments("test@example.com", true)]
[Arguments("invalid", false)]
public async Task IsValidEmail_各種輸入_應回傳正確驗證結果(string email, bool expected)
{
    var result = _validator.IsValidEmail(email);
    await Assert.That(result).IsEqualTo(expected);
}
```

**主要變更：**

1. `[Theory]` → `[Test]`
2. `[InlineData]` → `[Arguments]`
3. 方法改為 `async Task`
4. 所有斷言加上 `await`
5. 流暢式斷言語法

---

## 執行與偵錯

### CLI 執行

```bash
# 建置專案
dotnet build

# 執行所有測試
dotnet test

# 詳細輸出
dotnet test --verbosity normal

# 產生覆蓋率報告
dotnet test --coverage

# 過濾特定測試
dotnet test --filter "ClassName=CalculatorTests"
dotnet test --filter "TestName~Add"
```

### AOT 編譯執行

```bash
# 發佈為 AOT 編譯版本
dotnet publish -c Release -p:PublishAot=true

# 執行 AOT 編譯的測試
./bin/Release/net9.0/publish/MyApp.Tests.exe
```

### IDE 整合

**Visual Studio 2022：**

- 版本需 17.13+
- 啟用 "Use testing platform server mode"

**VS Code：**

- 安裝 C# Dev Kit 擴充套件
- 啟用 "Use Testing Platform Protocol"

**JetBrains Rider：**

- 啟用 "Testing Platform support"

---

## 效能比較

| 場景             | xUnit   | TUnit   | TUnit AOT | 效能提升  |
| ---------------- | ------- | ------- | --------- | --------- |
| **簡單測試執行** | 1,400ms | 1,000ms | 60ms      | 23x (AOT) |
| **非同步測試**   | 1,400ms | 930ms   | 26ms      | 54x (AOT) |
| **並行測試**     | 1,425ms | 999ms   | 54ms      | 26x (AOT) |

---

## 常見問題與解決方案

### 問題 1：套件相容性

**錯誤：** 安裝了 `Microsoft.NET.Test.Sdk` 導致測試無法發現

**解決方案：** 移除 `Microsoft.NET.Test.Sdk`，TUnit 使用新的測試平台

### 問題 2：IDE 整合問題

**症狀：** 測試在 IDE 中無法顯示或執行

**解決方案：**

1. 確認 IDE 版本支援 Microsoft.Testing.Platform
2. 啟用相關預覽功能
3. 重新載入專案或重啟 IDE

### 問題 3：非同步斷言遺忘

**症狀：** 編譯錯誤或斷言無法正常執行

**解決方案：** 所有斷言都需要 `await`，測試方法必須是 `async Task`

---

## 適用場景評估

### 適合使用 TUnit

1. **全新專案**：沒有歷史包袱
2. **效能要求高**：大型測試套件（1000+ 測試）
3. **技術棧先進**：使用 .NET 8+，計劃採用 AOT
4. **CI/CD 重度使用**：測試執行時間直接影響部署頻率
5. **容器化部署**：快速啟動時間很重要

### 暫時不建議

1. **Legacy 專案**：已有大量 xUnit 測試
2. **保守團隊**：需要穩定性勝過創新性
3. **複雜測試生態**：大量使用 xUnit 特定套件
4. **舊版 .NET**：還在 .NET 6/7

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 28 - TUnit 入門 - 下世代 .NET 測試框架探索**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10377828
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day28

### 官方資源

- [TUnit 官方網站](https://tunit.dev/)
- [TUnit GitHub](https://github.com/thomhurst/TUnit)
- [從 xUnit 遷移指南](https://tunit.dev/docs/migration/xunit)

### Microsoft 官方文件

- [Microsoft.Testing.Platform 介紹](https://learn.microsoft.com/dotnet/core/testing/microsoft-testing-platform-intro)
- [原生 AOT 部署](https://learn.microsoft.com/zh-tw/dotnet/core/deploying/native-aot)
