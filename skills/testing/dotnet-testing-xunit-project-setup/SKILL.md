---
name: dotnet-testing-xunit-project-setup
description: |
  xUnit 測試專案建立與設定的專門技能。當需要建立測試專案、設定專案結構、配置 NuGet 套件、組織測試資料夾時使用。涵蓋 csproj 設定、套件管理、專案結構、xunit.runner.json 配置等。
  Keywords: xunit project, xunit setup, 測試專案建立, test project setup, 建立測試專案, project structure, 專案結構, folder structure, xunit package, nuget packages, 測試套件, 如何建立測試專案, xunit configuration
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, xUnit, project setup, configuration"
---

# xUnit 測試專案設定指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 建立新的 xUnit 測試專案
- 設定 .NET 測試專案結構
- 配置 xUnit 相依套件與 NuGet 套件
- 規劃測試專案的資料夾組織
- 設定程式碼覆蓋率收集工具
- 理解測試專案的 csproj 設定

## 專案結構最佳實踐

### 建議的解決方案結構

```text
MyProject/
├── src/                          # 主程式碼目錄
│   └── MyProject.Core/
│       ├── MyProject.Core.csproj
│       ├── Calculator.cs
│       ├── Services/
│       └── Models/
├── tests/                        # 測試程式碼目錄
│   └── MyProject.Core.Tests/
│       ├── MyProject.Core.Tests.csproj
│       ├── CalculatorTests.cs
│       ├── Services/
│       └── Models/
└── MyProject.sln
```

**結構原則：**

1. **src 與 tests 分離**：清楚區分生產程式碼與測試程式碼
2. **命名慣例**：測試專案名稱為 `{主專案名稱}.Tests`
3. **目錄對應**：測試專案的資料夾結構應對應主專案的結構
4. **一對一映射**：每個主專案應有對應的測試專案

## 建立 xUnit 測試專案

### 方法一：使用 .NET CLI（推薦）

#### 步驟 1：建立解決方案與專案

```powershell
# 建立解決方案
dotnet new sln -n MyProject

# 建立主專案（類別庫）
dotnet new classlib -n MyProject.Core -o src/MyProject.Core

# 建立測試專案（xUnit 範本）
dotnet new xunit -n MyProject.Core.Tests -o tests/MyProject.Core.Tests

# 將專案加入解決方案
dotnet sln add src/MyProject.Core/MyProject.Core.csproj
dotnet sln add tests/MyProject.Core.Tests/MyProject.Core.Tests.csproj

# 建立專案參考（測試專案參考主專案）
dotnet add tests/MyProject.Core.Tests/MyProject.Core.Tests.csproj reference src/MyProject.Core/MyProject.Core.csproj
```

#### 步驟 2：安裝程式碼覆蓋率工具

```powershell
# 切換到測試專案目錄
cd tests/MyProject.Core.Tests

# 安裝 coverlet.collector（用於收集程式碼覆蓋率）
dotnet add package coverlet.collector
```

### 方法二：使用 Visual Studio

1. **建立解決方案**
   - File → New → Project
   - 選擇「Blank Solution」
   - 命名為專案名稱

2. **加入主專案**
   - 右鍵解決方案 → Add → New Project
   - 選擇「Class Library」
   - 命名為 `MyProject.Core`

3. **加入測試專案**
   - 右鍵解決方案 → Add → New Project
   - 搜尋並選擇「xUnit Test Project」
   - 命名為 `MyProject.Core.Tests`

4. **設定專案參考**
   - 右鍵測試專案 → Add → Project Reference
   - 勾選主專案

## xUnit 測試專案的 csproj 設定

### 標準 xUnit 測試專案 csproj

請參考同目錄下的 `templates/xunit-test-project.csproj` 範本檔案。

**核心相依套件說明：**

1. **xunit**（2.9.3+）
   - xUnit 測試框架的核心套件
   - 提供 `[Fact]`、`[Theory]` 等測試屬性
   - 包含 `Assert` 類別與斷言方法

2. **xunit.runner.visualstudio**（3.0.0+）
   - Visual Studio Test Explorer 整合
   - 讓測試能在 VS Code、Visual Studio、Rider 中被探索與執行
   - 支援測試結果的即時顯示

3. **Microsoft.NET.Test.Sdk**（17.12.0+）
   - .NET 測試平台的 SDK
   - 讓 `dotnet test` 指令能夠執行測試
   - 支援測試結果報告與測試探索

4. **coverlet.collector**（6.0.3+）
   - 程式碼覆蓋率收集工具
   - 與 `dotnet test` 整合
   - 產生覆蓋率報告（支援 Cobertura、OpenCover 等格式）

### 重要 csproj 設定項目

```xml
<PropertyGroup>
  <TargetFramework>net9.0</TargetFramework>
  <ImplicitUsings>enable</ImplicitUsings>
  <Nullable>enable</Nullable>
  <IsPackable>false</IsPackable>
  <IsTestProject>true</IsTestProject>
</PropertyGroup>
```

**設定說明：**

- `IsPackable=false`：測試專案不應被打包成 NuGet 套件
- `IsTestProject=true`：明確標記為測試專案，讓工具識別
- `Nullable=enable`：啟用可為 Null 的參考型別檢查

## 測試類別基本結構

### 標準測試類別範本

```csharp
namespace MyProject.Core.Tests;

public class CalculatorTests
{
    private readonly Calculator _calculator;

    // 建構函式：每個測試執行前都會被呼叫
    public CalculatorTests()
    {
        _calculator = new Calculator();
    }
}
```

### 測試生命週期（重要概念）

xUnit 的測試隔離機制：

1. **每個測試方法都會創建新的測試類別實例**
2. **建構函式**：在每個測試方法執行前被呼叫
3. **測試方法**：執行測試邏輯
4. **Dispose()**：如果實作 `IDisposable`，在每個測試方法執行後被呼叫

**執行順序範例：**

```text
執行 Test1：
  → 建構函式 → Test1 方法 → Dispose()

執行 Test2：
  → 建構函式 → Test2 方法 → Dispose()
```

這確保了 **測試隔離**，符合 FIRST 原則的 **I (Independent)**。

## 執行測試

### 使用 .NET CLI

```powershell
# 建置專案
dotnet build

# 執行所有測試
dotnet test

# 執行測試並收集程式碼覆蓋率
dotnet test --collect:"XPlat Code Coverage"

# 執行特定測試專案
dotnet test tests/MyProject.Core.Tests/MyProject.Core.Tests.csproj

# 執行測試並產生詳細輸出
dotnet test --verbosity detailed
```

### 在 IDE 中執行

#### VS Code（需安裝 C# Dev Kit）

1. 安裝 [C# Dev Kit](https://marketplace.visualstudio.com/items?itemName=ms-dotnettools.csdevkit)
2. 開啟 Test Explorer（測試總管）
3. 點擊測試旁的播放按鈕執行

#### Visual Studio

1. 開啟 Test Explorer（測試 → Test Explorer）
2. 點擊「Run All」執行所有測試
3. 可以右鍵單一測試執行或偵錯

#### JetBrains Rider

1. 測試方法旁會出現綠色執行圖示
2. 點擊執行或偵錯測試
3. 使用 Unit Tests 視窗管理測試

## 專案參考設定原則

### 參考方向規則

```text
測試專案 → 主專案   ✅ 正確
主專案 → 測試專案   ❌ 錯誤
```

**測試專案應該參考主專案，但主專案絕對不應參考測試專案。**

### 設定專案參考

```powershell
# 讓測試專案參考主專案
dotnet add tests/MyProject.Core.Tests/MyProject.Core.Tests.csproj reference src/MyProject.Core/MyProject.Core.csproj
```

在 csproj 中會產生：

```xml
<ItemGroup>
  <ProjectReference Include="..\..\src\MyProject.Core\MyProject.Core.csproj" />
</ItemGroup>
```

## 進階：多個測試專案的組織

當專案變大時，可能需要多個測試專案：

```text
MyProject/
├── src/
│   ├── MyProject.Core/
│   ├── MyProject.Web/
│   └── MyProject.Infrastructure/
├── tests/
│   ├── MyProject.Core.Tests/           # 單元測試
│   ├── MyProject.Web.Tests/            # Web 層測試
│   ├── MyProject.Infrastructure.Tests/ # 基礎設施測試
│   └── MyProject.Integration.Tests/    # 整合測試
└── MyProject.sln
```

**命名慣例建議：**

- `*.Tests` - 單元測試
- `*.Integration.Tests` - 整合測試
- `*.Acceptance.Tests` - 驗收測試
- `*.Performance.Tests` - 效能測試

### 實際工作專案的命名規範

在實際的工作專案中，建議使用更明確的命名格式來區分測試類型：

**推薦的命名格式：**

```text
MyProject/
├── src/
│   ├── MyProject.Core/
│   └── MyProject.WebApi/
├── tests/
│   ├── MyProject.Core.Test.Unit/              # 單元測試（明確標示）
│   ├── MyProject.WebApi.Test.Unit/            # WebApi 單元測試
│   └── MyProject.WebApi.Test.Integration/     # WebApi 整合測試
└── MyProject.sln
```

**命名規則：**

- **單元測試**：`{專案名稱}.Test.Unit`
  - 範例：`MyProject.Core.Test.Unit`
  - 特性：不依賴外部資源（資料庫、API、檔案系統等）
  - 執行速度：快速（毫秒級）

- **整合測試**：`{專案名稱}.Test.Integration`
  - 範例：`MyProject.WebApi.Test.Integration`
  - 特性：測試多個元件的整合，可能依賴外部資源
  - 執行速度：較慢（秒級）

**這種命名的優勢：**

1. **清晰度**：一眼就能分辨測試類型
2. **執行策略**：可以在 CI/CD 中分階段執行

   ```powershell
   # 快速回饋：只執行單元測試
   dotnet test --filter "FullyQualifiedName~.Test.Unit"
   
   # 完整驗證：執行整合測試
   dotnet test --filter "FullyQualifiedName~.Test.Integration"
   ```

3. **相依性管理**：整合測試可以有不同的套件相依（如 Testcontainers）
4. **團隊協作**：新成員能快速理解專案結構

**CLI 建立範例：**

```powershell
# 建立單元測試專案
dotnet new xunit -n MyProject.Core.Test.Unit -o tests/MyProject.Core.Test.Unit
dotnet add tests/MyProject.Core.Test.Unit reference src/MyProject.Core

# 建立整合測試專案
dotnet new xunit -n MyProject.WebApi.Test.Integration -o tests/MyProject.WebApi.Test.Integration
dotnet add tests/MyProject.WebApi.Test.Integration reference src/MyProject.WebApi
```

> **💡 提示**：雖然本範例中為了簡化說明使用 `.Tests` 格式，但在實際專案中強烈建議使用 `.Test.Unit` 和 `.Test.Integration` 這種更明確的格式。

## 常見問題與解決方案

### Q1: 測試探索失敗，Test Explorer 看不到測試？

**檢查清單：**

1. 確認已安裝 `xunit.runner.visualstudio` 套件
2. 確認已安裝 `Microsoft.NET.Test.Sdk` 套件
3. 執行 `dotnet build` 重新建置
4. 重啟 IDE 或重新載入 Test Explorer

### Q2: 測試可以在 CLI 執行但在 IDE 中無法執行？

**解決方案：**

- 確認 IDE 已安裝相關擴充套件（VS Code 需要 C# Dev Kit）
- 清除快取：刪除 `bin/` 和 `obj/` 資料夾後重新建置
- 檢查 `.csproj` 中的 `IsTestProject` 屬性是否為 `true`

### Q3: 如何在測試專案中使用 Internal 類別？

在主專案的 `.csproj` 或 `AssemblyInfo.cs` 中加入：

```csharp
[assembly: InternalsVisibleTo("MyProject.Core.Tests")]
```

或在 csproj 中：

```xml
<ItemGroup>
  <InternalsVisibleTo Include="MyProject.Core.Tests" />
</ItemGroup>
```

## 範本檔案

請參考同目錄下的範本檔案以快速建立專案：

- `templates/project-structure.md` - 完整的專案結構範例
- `templates/xunit-test-project.csproj` - xUnit 測試專案的 csproj 範本

## 檢查清單

建立 xUnit 測試專案時，請確認以下項目：

- [ ] 測試專案命名為 `{主專案名稱}.Tests`
- [ ] 測試專案位於 `tests/` 目錄下
- [ ] 已安裝 `xunit`、`xunit.runner.visualstudio`、`Microsoft.NET.Test.Sdk` 套件
- [ ] 已安裝 `coverlet.collector` 用於程式碼覆蓋率
- [ ] 測試專案已參考主專案
- [ ] `IsPackable` 設為 `false`
- [ ] `IsTestProject` 設為 `true`
- [ ] 可以執行 `dotnet test` 成功
- [ ] IDE 的 Test Explorer 可以探索到測試

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 02 - xUnit 框架深度解析**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10373952
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day02

- **Day 03 - xUnit 進階功能與測試資料管理**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374064
  - 範例程式碼：https://github.com/kevintsengtw/30Days_in_Testing_Samples/tree/main/day03

### 官方文件

- [xUnit 官方文件](https://xunit.net/)
- [.NET 測試最佳實踐](https://learn.microsoft.com/dotnet/core/testing/)

### 相關技能

- `unit-test-fundamentals` - 單元測試基礎與 FIRST 原則
- `test-naming-conventions` - 測試命名規範
- `code-coverage-analysis` - 程式碼覆蓋率分析
