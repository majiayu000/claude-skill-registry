---
name: dotnet-testing-advanced-xunit-upgrade-guide
description: |
  xUnit 2.9.x 到 3.x 升級完整指南。涵蓋破壞性變更、套件更新、async void 修正、IAsyncLifetime 調整。包含新功能介紹: Assert.Skip、Explicit Tests、Matrix Theory、Assembly Fixtures。
  Keywords: xunit upgrade, xunit v3, xunit 3.x, xunit migration, xunit 升級, xunit.v3, OutputType Exe, IAsyncLifetime v3, Assert.Skip, SkipUnless, SkipWhen, Explicit attribute, MatrixTheoryData, AssemblyFixture, 破壞性變更
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: "xunit, upgrade, migration, v3, breaking-changes, testing-framework"
---

# xUnit 升級指南：從 2.9.x 到 3.x

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 將現有 xUnit 2.x 測試專案升級到 xUnit 3.x
- 評估 xUnit 升級的影響範圍
- 解決 xUnit 升級過程中的編譯錯誤
- 使用 xUnit 3.x 新功能改進測試

## 核心概念

### 套件命名變革

xUnit v3 採用全新的套件命名策略：

| v1~v2 套件名稱              | v3 套件名稱                         | 說明         |
| --------------------------- | ----------------------------------- | ------------ |
| `xunit`                     | `xunit.v3`                          | 主要測試框架 |
| `xunit.assert`              | `xunit.v3.assert`                   | 斷言函式庫   |
| `xunit.core`                | `xunit.v3.core`                     | 核心元件     |
| `xunit.abstractions`        | (移除)                              | 不再需要     |
| `xunit.runner.visualstudio` | `xunit.runner.visualstudio` (3.x.y) | 測試執行器   |

**重要**：使用 `xunit.v3` 套件名稱，不是 `xunit`。

### 最低運行時需求

xUnit 3.x 的嚴格要求：

- **.NET Framework 4.7.2+** 或
- **.NET 8.0+** (推薦)

**不支援的版本**：

- .NET Core 3.1
- .NET 5、6、7

---

## 破壞性變更清單

### 1. 測試專案變成可執行檔

```xml
<!-- xUnit 2.x (Library) -->
<PropertyGroup>
  <OutputType>Library</OutputType>
</PropertyGroup>

<!-- xUnit 3.x (Exe) - 必須變更 -->
<PropertyGroup>
  <OutputType>Exe</OutputType>
</PropertyGroup>
```

### 2. async void 測試不再支援

```csharp
// ❌ xUnit 2.x - 3.x 中會失敗
[Fact]
public async void 測試某個非同步功能()
{
    var result = await SomeAsyncMethod();
    Assert.True(result);
}

// ✅ xUnit 3.x - 正確寫法
[Fact]
public async Task 測試某個非同步功能()
{
    var result = await SomeAsyncMethod();
    Assert.True(result);
}
```

### 3. IAsyncLifetime 變更

在 xUnit 3.x 中，`IAsyncLifetime` 繼承 `IAsyncDisposable`。如果同時實作 `IAsyncLifetime` 和 `IDisposable`，只會呼叫 `DisposeAsync`，不會呼叫 `Dispose`。

```csharp
// ⚠️ 需要注意的模式
public class MyTestClass : IAsyncLifetime, IDisposable
{
    public async Task InitializeAsync() { /* ... */ }
    public async Task DisposeAsync() { /* 會被呼叫 */ }
    public void Dispose() { /* 在 3.x 中不會被呼叫 */ }
}

// ✅ 建議：將清理邏輯統一放在 DisposeAsync
public class MyTestClass : IAsyncLifetime
{
    public async Task InitializeAsync() { /* 初始化 */ }
    public async Task DisposeAsync() { /* 所有清理邏輯 */ }
}
```

### 4. SkippableFact/SkippableTheory 移除

```csharp
// ❌ xUnit 2.x - 已移除
[SkippableFact]
public void 可跳過的測試()
{
    Skip.If(某個條件, "跳過原因");
    // 測試邏輯
}

// ✅ xUnit 3.x - 使用 Assert.Skip
[Fact]
public void 可跳過的測試()
{
    if (某個條件)
    {
        Assert.Skip("跳過原因");
    }
    // 測試邏輯
}
```

### 5. 僅支援 SDK-style 專案

檢查專案檔案開頭是否為：

```xml
<Project Sdk="Microsoft.NET.Sdk">
```

如果是傳統格式，必須先轉換為 SDK-style。

---

## 升級步驟

### 步驟 1：建立升級分支

```bash
git checkout -b feature/upgrade-xunit-v3
```

### 步驟 2：更新專案檔案

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <OutputType>Exe</OutputType>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
  </PropertyGroup>

  <ItemGroup>
    <!-- xUnit v3 套件 -->
    <PackageReference Include="xunit.v3" Version="3.0.1" />
    <PackageReference Include="xunit.runner.visualstudio" Version="3.1.4">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.13.0" />
    
    <!-- 常用輔助套件 -->
    <PackageReference Include="AwesomeAssertions" Version="8.1.0" />
    <PackageReference Include="NSubstitute" Version="5.3.0" />
  </ItemGroup>
</Project>
```

### 步驟 3：修正 async void 測試

使用 IDE 搜尋：

```regex
async\s+void.*\[(Fact|Theory)\]
```

將所有 `async void` 改為 `async Task`。

### 步驟 4：更新 using 陳述式

```csharp
// 移除 (不再需要)
// using Xunit.Abstractions;

// 保留
using Xunit;
```

### 步驟 5：編譯與測試

```bash
dotnet clean
dotnet restore
dotnet build
dotnet test --verbosity normal
```

---

## xUnit 3.x 新功能

### 動態跳過測試

**聲明式 (SkipUnless/SkipWhen)**：

```csharp
[Fact(SkipUnless = nameof(IsWindowsEnvironment), 
      Skip = "此測試只在 Windows 環境執行")]
public void 只在Windows上執行的測試()
{
    // 測試邏輯
}

public static bool IsWindowsEnvironment => 
    RuntimeInformation.IsOSPlatform(OSPlatform.Windows);
```

**命令式 (Assert.Skip)**：

```csharp
[Fact]
public void 根據環境變數跳過的測試()
{
    var enableTests = Environment.GetEnvironmentVariable("ENABLE_INTEGRATION_TESTS");
    
    if (string.IsNullOrEmpty(enableTests) || enableTests.ToLower() != "true")
    {
        Assert.Skip("整合測試已停用。設定 ENABLE_INTEGRATION_TESTS=true 來執行");
    }
    
    // 測試邏輯...
}
```

### 明確測試 (Explicit Tests)

```csharp
[Fact(Explicit = true)]
public void 昂貴的整合測試()
{
    // 這個測試預設不會執行，除非明確要求
    // 適用於效能測試、長時間執行的測試
}
```

### [Test] 屬性

```csharp
// 三種寫法功能相同
[Test]
public void 使用Test屬性的測試() { Assert.True(true); }

[Fact] 
public void 使用Fact屬性的測試() { Assert.True(true); }
```

### 矩陣理論資料 (Matrix Theory Data)

```csharp
public static TheoryData<int, string> TestData =>
    new MatrixTheoryData<int, string>(
        [1, 2, 3],                    // 數字資料
        ["Hello", "World", "Test"]    // 字串資料
    );
    // 這會產生 3×3=9 個測試案例

[Theory]
[MemberData(nameof(TestData))]
public void 矩陣測試範例(int number, string text)
{
    number.Should().BePositive();
    text.Should().NotBeNullOrEmpty();
}
```

### Assembly Fixtures

```csharp
public class DatabaseAssemblyFixture : IAsyncLifetime
{
    public string ConnectionString { get; private set; }
    
    public async Task InitializeAsync()
    {
        // 建立測試資料庫
        ConnectionString = await CreateTestDatabaseAsync();
    }
    
    public async Task DisposeAsync()
    {
        // 清理測試資料庫
        await DropTestDatabaseAsync();
    }
}

// 註冊 Assembly Fixture
[assembly: AssemblyFixture(typeof(DatabaseAssemblyFixture))]

// 在測試中使用
public class UserServiceTests
{
    private readonly DatabaseAssemblyFixture _dbFixture;
    
    public UserServiceTests(DatabaseAssemblyFixture dbFixture)
    {
        _dbFixture = dbFixture;
    }
    
    [Fact]
    public void Test1() { /* 使用 _dbFixture.ConnectionString */ }
}
```

### Test Pipeline Startup

```csharp
public class TestPipelineStartup : ITestPipelineStartup
{
    public async Task ConfigureAsync(ITestPipelineBuilder builder, 
                                     CancellationToken cancellationToken)
    {
        // 全域初始化邏輯
        Console.WriteLine("初始化測試環境...");
        await InitializeDatabaseAsync();
    }
}

// 註冊
[assembly: TestPipelineStartup(typeof(TestPipelineStartup))]
```

---

## xunit.runner.json 設定

```json
{
  "$schema": "https://xunit.net/schema/v3/xunit.runner.schema.json",
  "parallelAlgorithm": "conservative",
  "maxParallelThreads": 4,
  "diagnosticMessages": true,
  "internalDiagnosticMessages": false,
  "methodDisplay": "classAndMethod",
  "preEnumerateTheories": true,
  "stopOnFail": false
}
```

---

## 測試報告格式

xUnit 3.x 支援多種報告格式：

```bash
# 產生 CTRF 格式報告
dotnet run -- -ctrf results.json

# 產生 TRX 格式報告  
dotnet run -- -trx results.trx

# 產生 XML 格式報告
dotnet run -- -xml results.xml

# 產生多種格式報告
dotnet run -- -xml results.xml -ctrf results.json -trx results.trx
```

---

## 常見問題與解決方案

### 問題 1：找不到 xunit.abstractions

**錯誤**：`The type or namespace name 'Abstractions' does not exist`

**解決**：移除 `using Xunit.Abstractions;`，相關類型已移到 `Xunit` 命名空間。

### 問題 2：自訂 DataAttribute 無法運作

```csharp
// ❌ xUnit 2.x 的實作
public class CustomDataAttribute : DataAttribute
{
    public override IEnumerable<object[]> GetData(MethodInfo testMethod)
    {
        // 舊的實作
    }
}

// ✅ xUnit 3.x 的實作
public class CustomDataAttribute : DataAttribute
{
    public override async Task<IReadOnlyCollection<ITheoryDataRow>> GetDataAsync(
        MethodInfo method, 
        DisposalTracker disposalTracker)
    {
        var data = await GenerateDataAsync();
        return data.Select(item => new TheoryDataRow(item)).ToList();
    }
}
```

### 問題 3：IDE 無法發現測試

確認 IDE 版本符合要求：

- Visual Studio 2022 17.8+
- Rider 2023.3+
- VS Code (最新版)

如仍有問題，可暫時停用 Microsoft Testing Platform：

```xml
<PropertyGroup>
  <EnableMicrosoftTestingPlatform>false</EnableMicrosoftTestingPlatform>
</PropertyGroup>
```

---

## 升級檢查清單

### 升級前

- [ ] 確認目標框架版本 (.NET 8+ 或 .NET Framework 4.7.2+)
- [ ] 檢查專案檔案格式 (SDK-style)
- [ ] 識別所有 async void 測試方法
- [ ] 檢查 IAsyncLifetime 實作
- [ ] 評估相依套件相容性
- [ ] 建立備份分支

### 升級過程

- [ ] 更新套件參考 (使用 `xunit.v3`)
- [ ] 移除 `xunit.abstractions` 參考
- [ ] 修改 OutputType 為 Exe
- [ ] 修正所有 async void 測試方法
- [ ] 更新 using 陳述式
- [ ] 重構自訂屬性 (如有)
- [ ] 驗證編譯成功
- [ ] 執行所有測試

### 升級後驗證

- [ ] 功能完整性測試
- [ ] 效能基準比較
- [ ] CI/CD Pipeline 驗證
- [ ] 文檔更新
- [ ] 團隊培訓

---

## IDE 與工具支援

### IDE 版本需求

| IDE           | 最低版本   |
| ------------- | ---------- |
| Visual Studio | 2022 17.8+ |
| VS Code       | 最新版     |
| Rider         | 2023.3+    |

### Microsoft Testing Platform

xUnit 3.x 預設啟用 Microsoft Testing Platform：

```xml
<PropertyGroup>
  <EnableMicrosoftTestingPlatform>true</EnableMicrosoftTestingPlatform>
  <OutputType>Exe</OutputType>
</PropertyGroup>
```

---

## 效能改進

xUnit 3.x 帶來的效能改進：

1. **獨立進程執行**：測試在獨立進程中執行，更好的隔離性
2. **改進的並行演算法**：更智慧的負載平衡
3. **更快的啟動時間**：可執行檔直接執行
4. **更好的記憶體隔離**：減少測試之間的干擾

---

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 26 - xUnit 升級指南：從 2.9.x 到 3.x 的轉換**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10377477
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day26

### 官方文件

- [xUnit.net 官方網站](https://xunit.net/)
- [xUnit v3 新功能文件](https://xunit.net/docs/getting-started/v3/whats-new)
- [xUnit 2.x → 3.x 官方遷移指南](https://xunit.net/docs/getting-started/v3/migration)
- [xunit.v3 NuGet 套件](https://www.nuget.org/packages/xunit.v3)

## 範例參考

請參考同目錄下的範例檔案：

- `templates/xunit-v3-project.csproj` - xUnit 3.x 專案設定範本
- `templates/upgrade-checklist.md` - 升級檢查清單
- `templates/code-migration-examples.cs` - 程式碼遷移範例
- `templates/new-features-examples.cs` - 新功能使用範例
