---
name: code-coverage-analysis
description: 協助進行程式碼覆蓋率分析與報告解讀的完整指南。當使用者要求設定程式碼覆蓋率工具、產生覆蓋率報告、解讀覆蓋率數據，或詢問覆蓋率最佳實踐時使用此技能。
license: MIT
---

# 程式碼覆蓋率分析指南

## 適用情境

當被要求執行以下任務時，請使用此技能：

- 設定與執行程式碼覆蓋率分析
- 配置 Coverlet 或其他覆蓋率工具
- 產生與解讀覆蓋率報告
- 在 Visual Studio 或 VS Code 中檢視覆蓋率
- 評估測試完整性與品質
- 結合複雜度指標制定測試策略

## Code Coverage 核心概念

### 定義

**程式碼覆蓋率 (Code Coverage)** 是一種測量指標，用來統計測試執行時實際執行了多少程式碼。

### 正確認知

**Code Coverage 的實際價值：**

1. **找出測試盲點**：快速識別沒有被測試的程式碼
2. **評估測試完整性**：檢查重要邏輯是否都有測試
3. **輔助重構決策**：了解哪些區域需要更多關注
4. **增加測試信心**：確認關鍵路徑都有被驗證

### 常見誤解（必須避免）

❌ **錯誤認知：**

- 涵蓋率 100% 就沒有 Bug
- 涵蓋率數字越高越好
- 可以用涵蓋率當作 KPI

✅ **正確認知：**

- Code Coverage 只是提醒工具，告訴你哪些程式碼沒被測試
- **重點是測試的有效性，不是覆蓋率數字**
- 幫助判斷是否需要補充測試案例
- **絕對不應該當作 KPI 使用**

> ⚠️ **警告**：當 Code Coverage 被當作 KPI 時，開發者會為了衝數字而寫沒有 Assert 的測試，完全失去了測試的意義。

## .NET 專案的覆蓋率工具選擇

### 1. Visual Studio Enterprise（僅限企業版）

**優點：**

- 內建整合，無需額外設定
- 完整的 UI 支援
- 即時結果顯示

**限制：**

- **只有 Enterprise 版本才有此功能**
- Professional 和 Community 版本不支援

### 2. Fine Code Coverage（推薦免費方案）

**優點：**

- 完全免費
- 整合在 Visual Studio 中
- 即時顯示覆蓋率
- 程式碼編輯器直接標示

**安裝方式：**

1. 開啟 Visual Studio
2. 延伸模組 → 管理延伸模組
3. 搜尋 "Fine Code Coverage"
4. 安裝後重新啟動

**必要設定：**

- 工具 → 選項 → Fine Code Coverage
- Run (Common) → Enable：設為 `True`
- Editor Colouring Line Highlighting：設為 `True`

### 3. .NET CLI 工具

**使用場景：**

- CI/CD 流程整合
- 命令列自動化
- 跨平台開發

**安裝與使用：**

```powershell
# 安裝工具
dotnet tool install -g dotnet-coverage

# 執行測試並產生報告
dotnet-coverage collect dotnet test

# 或使用 Coverlet（推薦）
dotnet test --collect:"XPlat Code Coverage"
```

### 4. VS Code 內建測試覆蓋率

**優點：**

- 跨平台支援
- 內建功能，無需安裝擴充套件
- 整合式測試管理

**使用方式：**

1. 安裝 C# Dev Kit 擴充套件
2. 開啟測試總管（燒杯圖示）
3. 點選「執行涵蓋範圍測試」
4. 查看結果：測試涵蓋範圍視圖、編輯器內顯示、檔案總管顯示

## 執行覆蓋率分析

### 方法一：使用 .NET CLI（推薦用於 CI/CD）

```powershell
# 執行測試並收集覆蓋率
dotnet test --collect:"XPlat Code Coverage"

# 指定輸出格式
dotnet test --collect:"XPlat Code Coverage" --results-directory ./coverage

# 產生多種格式報告
dotnet test /p:CollectCoverage=true /p:CoverageReportFormat="cobertura;opencover;json"
```

### 方法二：使用 Fine Code Coverage

1. 在 Visual Studio 中執行測試
2. 檢視 → 其他視窗 → Fine Code Coverage
3. 自動顯示覆蓋率報告

### 方法三：使用 VS Code

1. 開啟測試總管
2. 點選「執行涵蓋範圍測試」圖示
3. 查看覆蓋率結果：
   - **測試涵蓋範圍**視圖：樹狀結構
   - **編輯器內顯示**：綠色/紅色標示
   - **檔案總管**：百分比顯示

## 設定 Coverlet

### 在 csproj 中配置

```xml
<Project Sdk="Microsoft.NET.Sdk">
  
  <PropertyGroup>
    <TargetFramework>net9.0</TargetFramework>
  </PropertyGroup>

  <ItemGroup>
    <!-- 測試框架套件 -->
    <PackageReference Include="xunit" Version="2.9.3" />
    <PackageReference Include="xunit.runner.visualstudio" Version="3.0.0" />
    <PackageReference Include="Microsoft.NET.Test.Sdk" Version="17.12.0" />
    
    <!-- 覆蓋率收集器 -->
    <PackageReference Include="coverlet.collector" Version="6.0.3">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
  </ItemGroup>

</Project>
```

### 使用 runsettings 檔案

請參考 `templates/runsettings-template.xml` 檔案，用於更進階的覆蓋率設定：

- 排除特定檔案或命名空間
- 設定覆蓋率閾值
- 自訂報告格式

**使用方式：**

```powershell
dotnet test --settings coverage.runsettings
```

## 解讀覆蓋率報告

### 顏色標示說明

在程式碼編輯器中：

- **綠色**：已被測試覆蓋
- **黃色**：部分覆蓋（部分分支未測試）
- **紅色**：未被覆蓋

### 覆蓋率指標

1. **Line Coverage（行覆蓋率）**
   - 被執行的程式碼行數 / 總程式碼行數
   - 最基本的指標

2. **Branch Coverage（分支覆蓋率）**
   - 被執行的分支數 / 總分支數
   - 比行覆蓋率更準確
   - 確保 if/else、switch 等所有分支都被測試

3. **Method Coverage（方法覆蓋率）**
   - 被執行的方法數 / 總方法數

### 報告解讀策略

1. **優先處理紅色區域**
   - 完全沒被測試的程式碼
   - 可能是關鍵業務邏輯

2. **檢查黃色區域**
   - 確認所有條件分支都有測試
   - 特別注意 if/else、try/catch 等

3. **評估必要性**
   - 簡單的 getter/setter 可能不需要測試
   - 自動產生的程式碼可以排除
   - 專注於業務邏輯與複雜運算

## 結合複雜度指標

### 循環複雜度（Cyclomatic Complexity）

**定義：**
程式中獨立邏輯路徑的數量

**與測試案例的關係：**

- 循環複雜度 = 至少需要的測試案例數量
- 每個 if、for、while、case、&&、|| 都會增加複雜度

**範例：**

```csharp
public int Max(int[] array)
{
    if (array == null || array.Length == 0)  // +2 (null 判斷 + 長度判斷)
    {
        throw new ArgumentException("array must not be empty.");
    }

    int max = array[0];

    for (int i = 1; i < array.Length; i++)  // +1 (迴圈)
    {
        if (array[i] > max)  // +1 (條件判斷)
        {
            max = array[i];
        }
    }

    return max;  // +1 (方法本身)
}
// 總複雜度 = 5
```

**測試策略：**

循環複雜度為 5，至少需要 5 個測試案例：

1. 傳入 null → 測試 `array == null`
2. 傳入空陣列 → 測試 `array.Length == 0`
3. 單一元素 → 不進入迴圈
4. 最大值在開頭 → 迴圈不更新 max
5. 最大值在中間 → 迴圈更新 max

### Visual Studio 擴充套件

**CodeMaintainability：**

- 顯示可維護性指標
- 計算循環複雜度
- 評估程式碼品質

**CodeMaid：**

- Spade 功能：視覺化程式碼結構
- 顯示每個方法的複雜度
- 幫助識別需要重構的程式碼

## 改善覆蓋率的策略

### 1. 漸進式改善

```text
目前覆蓋率 → 識別關鍵模組 → 補充測試 → 提升至目標值 → 持續監控
```

**建議流程：**

1. **第一階段**：覆蓋核心業務邏輯（目標 60-70%）
2. **第二階段**：補充邊界條件測試（目標 70-80%）
3. **第三階段**：處理異常情境（目標 80-85%）
4. **維持階段**：新增功能必須有測試

### 2. 優先順序排序

**高優先級（必須測試）：**

- 業務邏輯核心
- 金融計算
- 資料驗證
- 權限控制
- 異常處理

**中優先級（建議測試）：**

- 資料轉換
- 格式化邏輯
- 查詢邏輯

**低優先級（可選測試）：**

- 簡單的 getter/setter
- DTO 類別
- 自動產生的程式碼

### 3. 排除不必要的程式碼

在程式碼或 runsettings 中排除：

```csharp
// 使用屬性排除
[ExcludeFromCodeCoverage]
public class GeneratedCode
{
    // ...
}
```

## 實戰建議與最佳實踐

### 測試案例數量決策

1. **基於需求分析**
   - 列出方法的使用案例
   - 識別邊界條件和異常情況
   - 考慮業務邏輯的各種情境

2. **參考複雜度指標**
   - 循環複雜度提供測試案例下限
   - 高複雜度方法需要更多測試
   - 考慮重構降低複雜度

3. **平衡覆蓋率與品質**
   - 不以 100% 覆蓋率為唯一目標
   - 專注於關鍵業務邏輯
   - 確保測試的實際價值

### 測試策略

**四大測試類型：**

1. **邊界測試**：測試輸入值的上下限
2. **異常測試**：驗證錯誤處理邏輯
3. **主流程測試**：覆蓋正常的業務流程
4. **條件分支測試**：確保所有分支都有測試

### 持續改善

1. **定期檢視報告**
   - 每次提交前檢查涵蓋率變化
   - Pull Request 時審查覆蓋率

2. **識別風險區域**
   - 關注未覆蓋的關鍵程式碼
   - 優先處理高複雜度未測試區域

3. **漸進式改善**
   - 逐步提升重要模組的測試覆蓋率
   - 新功能必須包含測試

4. **團隊協作**
   - 建立測試標準和流程
   - Code Review 包含測試檢查

## CI/CD 整合

### GitHub Actions 範例

```yaml
name: Test with Coverage

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup .NET
        uses: actions/setup-dotnet@v3
        with:
          dotnet-version: '9.0.x'
      
      - name: Run tests with coverage
        run: dotnet test --collect:"XPlat Code Coverage"
      
      - name: Generate coverage report
        run: |
          dotnet tool install -g dotnet-reportgenerator-globaltool
          reportgenerator -reports:**/coverage.cobertura.xml -targetdir:coverage -reporttypes:Html
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

### Azure DevOps 範例

```yaml
- task: DotNetCoreCLI@2
  displayName: 'Run tests with coverage'
  inputs:
    command: 'test'
    arguments: '--collect:"XPlat Code Coverage"'
    publishTestResults: true

- task: PublishCodeCoverageResults@1
  inputs:
    codeCoverageTool: 'Cobertura'
    summaryFileLocation: '$(Agent.TempDirectory)/**/*coverage.cobertura.xml'
```

## 常見問題與解決方案

### Q1: 覆蓋率顯示 0%？

**檢查清單：**

1. 確認已安裝 `coverlet.collector` 套件
2. 檢查 runsettings 設定是否正確
3. 確認測試有實際執行
4. 查看是否有排除設定過於廣泛

### Q2: Visual Studio 看不到覆蓋率？

**解決方案：**

- Community/Professional 版本：安裝 Fine Code Coverage 擴充套件
- Enterprise 版本：使用內建功能
- 確認已啟用覆蓋率收集

### Q3: VS Code 無法顯示覆蓋率？

**解決方案：**

1. 確認已安裝 C# Dev Kit
2. 重新執行「執行涵蓋範圍測試」
3. 檢查 lcov 檔案是否產生
4. 嘗試重新載入視窗

### Q4: 如何提升覆蓋率？

**策略：**

1. 識別未覆蓋的關鍵程式碼（紅色區域）
2. 補充邊界條件測試
3. 測試所有條件分支
4. 加入異常情境測試
5. 考慮重構過於複雜的方法

## 範本檔案

請參考同目錄下的範本檔案：

- `templates/runsettings-template.xml` - 覆蓋率設定範本
- `templates/coverage-workflow.md` - 完整的工作流程說明

## 檢查清單

設定程式碼覆蓋率時，請確認以下項目：

- [ ] 已安裝 `coverlet.collector` 套件
- [ ] 可以執行 `dotnet test --collect:"XPlat Code Coverage"`
- [ ] 工具可以正常顯示覆蓋率結果
- [ ] 了解覆蓋率數字的真正意義（不是 KPI）
- [ ] 已排除不必要的程式碼（如自動產生的程式碼）
- [ ] 團隊理解覆蓋率是輔助工具而非目標
- [ ] 專注於測試品質而非覆蓋率數字

## 相關技能

- `unit-test-fundamentals` - 單元測試基礎與 FIRST 原則
- `xunit-project-setup` - xUnit 測試專案設定
- `test-naming-conventions` - 測試命名規範

## 核心理念

> **程式碼覆蓋率是手段，不是目的。**
>
> 重點不在於數字有多高，而在於：
>
> - 關鍵業務邏輯是否都有測試
> - 測試是否真正驗證了預期行為
> - 是否能在重構時提供信心

## 參考資源

### 原始文章

本技能內容提煉自「老派軟體工程師的測試修練 - 30 天挑戰」系列文章：

- **Day 06 - Code Coverage 程式碼涵蓋範圍實戰指南**
  - 鐵人賽文章：https://ithelp.ithome.com.tw/articles/10374355
  - 範例程式碼：無（本章節為概念說明）

### 官方文件

- [.NET 的單元測試最佳做法](https://learn.microsoft.com/dotnet/core/testing/unit-testing-best-practices)
- [使用程式碼涵蓋範圍進行單元測試](https://learn.microsoft.com/dotnet/core/testing/unit-testing-code-coverage)
- [dotnet-coverage 工具](https://learn.microsoft.com/dotnet/core/additional-tools/dotnet-coverage)
- [VS Code Testing](https://code.visualstudio.com/docs/editor/testing)

### 工具

- [Fine Code Coverage](https://marketplace.visualstudio.com/items?itemName=FortuneNgwenya.FineCodeCoverage2022)
- [Coverlet](https://github.com/coverlet-coverage/coverlet)
- [ReportGenerator](https://github.com/danielpalme/ReportGenerator)

### 相關技能

- `unit-test-fundamentals` - 單元測試基礎與 FIRST 原則
- `xunit-project-setup` - xUnit 專案設定
