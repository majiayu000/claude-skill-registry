---
name: dotnet-testing
description: .NET 測試基礎技能總覽與引導中心。當使用者詢問「如何寫 .NET 測試」、「.NET 測試入門」、「需要哪些測試工具」、「測試最佳實踐」、「從零開始學測試」等一般性測試需求時觸發。會根據具體需求推薦適合的子技能組合，涵蓋測試基礎、測試資料、斷言、模擬、特殊場景等 19 個基礎技能。

triggers:
  # 入口關鍵字
  - dotnet testing
  - .NET 測試
  - 測試入門
  - testing guide
  - 如何寫測試
  - 測試最佳實踐
  - testing overview
  - test fundamentals overview

  # 測試基礎
  - unit test
  - 單元測試
  - xunit
  - test project
  - 測試專案
  - 3A pattern
  - FIRST principles
  - FIRST 原則
  - test fundamentals
  - 測試基礎

  # 斷言相關
  - assertion
  - 斷言
  - Should()
  - FluentAssertions
  - BeEquivalentTo
  - 流暢斷言
  - assert
  - verify

  # 模擬與測試替身
  - mock
  - stub
  - spy
  - NSubstitute
  - Substitute.For
  - 模擬
  - 測試替身
  - mock object
  - test double

  # 測試資料生成
  - test data
  - 測試資料
  - AutoFixture
  - Bogus
  - Builder Pattern
  - Create<>
  - CreateMany
  - Faker
  - fake data
  - 假資料
  - test data builder
  - 測試資料生成

  # 驗證器測試
  - validator
  - 驗證器
  - FluentValidation
  - CreateUserValidator
  - UpdateValidator
  - validation testing
  - 驗證測試

  # 時間測試
  - DateTime
  - TimeProvider
  - FakeTimeProvider
  - 時間測試
  - DateTime.Now
  - time testing

  # 檔案系統測試
  - IFileSystem
  - MockFileSystem
  - 檔案測試
  - 檔案系統
  - file testing
  - filesystem

  # 程式碼覆蓋率
  - code coverage
  - 覆蓋率
  - Coverlet
  - coverage report

  # 測試輸出與日誌
  - ITestOutputHelper
  - ILogger
  - test output
  - 測試輸出
  - logging

  # 私有成員測試
  - Private method
  - Internal class
  - InternalsVisibleTo
  - 私有方法
  - 內部類別

  # 測試命名
  - test naming
  - 測試命名
  - naming convention
  - 命名規範

license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, xUnit, overview, guide, fundamentals"
  related_skills: "dotnet-testing-advanced"
  skill_count: 19
  skill_type: "overview"
---

# .NET 測試基礎技能總覽

---

## 🤖 AI Agent 重要提示

**當您（AI Agent）被載入此入口 skill 時，請先閱讀以下指引**：

### 📋 本技能的定位

本檔案是「導航中心」，用於幫助找到正確的**子技能**。

#### 您的任務是

1. ✅ 根據使用者需求匹配對應的子技能
2. ✅ 使用 `Skill` tool 載入具體的子技能
3. ✅ 讓子技能提供專業的測試指引

#### 禁止行為

- ❌ 不要在本入口 skill 中直接提供測試程式碼
- ❌ 不要在沒有載入子技能的情況下開始實作測試
- ❌ 不要跳過子技能直接提供「一般性」測試建議

---

## 🎯 快速技能對照表（AI Agent 必讀）

**使用者提到的關鍵字 → 應載入的子技能**

### 最常用技能（必須熟記）

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **Validator**、驗證器、CreateUserValidator | `/skill dotnet-testing-fluentvalidation-testing` | FluentValidation 測試 |
| **Mock**、模擬、IRepository、IService | `/skill dotnet-testing-nsubstitute-mocking` | 模擬外部依賴 |
| **AutoFixture**、測試資料生成 | `/skill dotnet-testing-autofixture-basics` | 自動產生測試資料 |
| **斷言**、Should()、BeEquivalentTo | `/skill dotnet-testing-awesome-assertions-guide` | 流暢斷言（必學） |
| **DateTime**、時間測試、TimeProvider | `/skill dotnet-testing-datetime-testing-timeprovider` | 時間相關測試 |
| **File**、檔案系統、IFileSystem | `/skill dotnet-testing-filesystem-testing-abstractions` | 檔案系統測試 |
| **Bogus**、假資料、Faker | `/skill dotnet-testing-bogus-fake-data` | 擬真資料生成 |
| **Builder Pattern**、WithXxx | `/skill dotnet-testing-test-data-builder-pattern` | Test Data Builder |
| **深層比對**、DTO 比對、Excluding | `/skill dotnet-testing-complex-object-comparison` | 複雜物件比對 |

### 基礎入門技能

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **從零開始**、測試基礎、FIRST 原則 | `/skill dotnet-testing-unit-test-fundamentals` | 單元測試基礎 |
| **測試命名**、如何命名測試 | `/skill dotnet-testing-test-naming-conventions` | 命名規範 |
| **建立測試專案**、xUnit 設定 | `/skill dotnet-testing-xunit-project-setup` | 專案建置 |

### 進階技能組合

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| AutoFixture + Bogus | `/skill dotnet-testing-autofixture-bogus-integration` | 自動化+擬真資料 |
| AutoFixture + NSubstitute | `/skill dotnet-testing-autofixture-nsubstitute-integration` | 自動建立 Mock |
| AutoData、Theory 測試 | `/skill dotnet-testing-autodata-xunit-integration` | 參數化測試 |
| 測試輸出、ITestOutputHelper | `/skill dotnet-testing-test-output-logging` | 測試日誌 |
| 覆蓋率、Coverlet | `/skill dotnet-testing-code-coverage-analysis` | 程式碼覆蓋率 |

---

## ⚠️ 使用流程範例

### ✅ 正確流程

```
使用者：請幫我建立 CreateUserValidator 的測試

AI：我注意到您需要測試 Validator。根據快速對照表，
    我應該載入 dotnet-testing-fluentvalidation-testing skill。

    [使用 Skill tool 載入子技能]

AI：現在按照 FluentValidation Testing skill 的指引為您建立測試...
```

### ❌ 錯誤流程

```
使用者：請幫我建立 CreateUserValidator 的測試

AI：好的，我來寫測試...（直接開始寫程式碼，沒有載入子技能）
```

---

## 📚 完整技能清單

如需查看完整的 19 個基礎技能清單、詳細決策樹、學習路徑建議，請繼續閱讀本檔案後續內容。

**人類開發者參考**：如需快速查找，請查看 [SKILLS_QUICK_INDEX.md](/SKILLS_QUICK_INDEX.md)

---

## 適用情境

當您遇到以下情況時，我會協助您找到正確的技能：

- 剛開始學習 .NET 測試，不知從何下手
- 想為現有專案建立測試，需要完整指引
- 需要改善測試品質，尋找最佳實踐
- 遇到特定測試場景，不確定該用哪個工具
- 想了解測試資料生成、斷言、模擬等技術
- 希望提升測試可讀性與維護性
- 需要處理時間、檔案系統等特殊測試場景

## 快速決策樹

### 我應該從哪裡開始？

#### 情境 1：完全新手，從未寫過測試

**推薦學習路徑**：
1. `dotnet-testing-unit-test-fundamentals` - 理解 FIRST 原則與 3A Pattern
2. `dotnet-testing-test-naming-conventions` - 學習命名規範
3. `dotnet-testing-xunit-project-setup` - 建立第一個測試專案

**為什麼這樣學**：
- FIRST 原則是所有測試的基礎，先建立正確的觀念
- 命名規範讓測試易讀易維護
- 實際動手建立專案，將理論轉化為實踐

---

#### 情境 2：會寫基礎測試，但測試資料準備很麻煩

**推薦技能（擇一或組合）**：

**選項 A - 自動化優先**
→ `dotnet-testing-autofixture-basics`
適合：需要大量測試資料、減少樣板程式碼

**選項 B - 擬真資料優先**
→ `dotnet-testing-bogus-fake-data`
適合：需要真實感的測試資料（姓名、地址、Email 等）

**選項 C - 語意清晰優先**
→ `dotnet-testing-test-data-builder-pattern`
適合：需要高可讀性、明確表達測試意圖

**選項 D - 兩者兼具**
→ `dotnet-testing-autofixture-basics` + `dotnet-testing-autofixture-bogus-integration`
適合：同時需要自動化和擬真資料

---

#### 情境 3：有外部依賴（資料庫、API、第三方服務）需要模擬

**推薦技能組合**：
1. `dotnet-testing-nsubstitute-mocking` - NSubstitute Mock 框架基礎
2. `dotnet-testing-autofixture-nsubstitute-integration` - （可選）整合 AutoFixture 與 NSubstitute

**何時需要第二個技能**：
- 如果您已經在使用 AutoFixture 產生測試資料
- 想要自動建立 Mock 物件，減少手動設定

---

#### 情境 4：測試中有特殊場景

**時間相關測試**
→ `dotnet-testing-datetime-testing-timeprovider`
處理：DateTime.Now、時區轉換、時間計算

**檔案系統測試**
→ `dotnet-testing-filesystem-testing-abstractions`
處理：檔案讀寫、目錄操作、路徑處理

**私有/內部成員測試**
→ `dotnet-testing-private-internal-testing`
處理：需要測試 private、internal 成員（但應謹慎使用）

---

#### 情境 5：需要更好的斷言方式

**基礎需求 - 流暢斷言**
→ `dotnet-testing-awesome-assertions-guide`
所有專案都應該使用，提升測試可讀性

**進階需求 - 複雜物件比較**
→ `dotnet-testing-complex-object-comparison`
處理：深層物件比較、DTO 驗證、Entity 比對

**驗證規則測試**
→ `dotnet-testing-fluentvalidation-testing`
處理：測試 FluentValidation 驗證器

---

#### 情境 6：想了解測試覆蓋率

→ `dotnet-testing-code-coverage-analysis`
學習：使用 Coverlet 分析程式碼覆蓋率、產生報告

## 技能分類地圖

### 1. 測試基礎（3 個技能）- 必學基礎

| 技能名稱 | 核心價值 | 適合新手 | 何時使用 |
|---------|---------|---------|---------|
| `dotnet-testing-unit-test-fundamentals` | 理解 FIRST 原則、3A Pattern、測試金字塔等基礎概念 | ⭐⭐⭐ | 所有測試的起點，建立正確的測試觀念 |
| `dotnet-testing-test-naming-conventions` | 學習三段式命名法、中文命名建議 | ⭐⭐⭐ | 提升測試可讀性與可維護性 |
| `dotnet-testing-xunit-project-setup` | 建立標準的 xUnit 測試專案結構 | ⭐⭐⭐ | 建立新測試專案時 |

**學習順序建議**：fundamentals → naming-conventions → xunit-project-setup

**核心收穫**：
- **FIRST 原則**：Fast、Independent、Repeatable、Self-Validating、Timely
- **3A Pattern**：Arrange-Act-Assert 結構化測試
- **命名規範**：`[被測方法]_[測試情境]_[預期行為]`
- **專案結構**：tests/ 目錄、.csproj 設定、NuGet 套件管理

---

### 2. 測試資料生成（5 個技能）- 提升效率

| 技能名稱 | 特點 | 優勢 | 何時使用 |
|---------|------|------|---------|
| `dotnet-testing-autofixture-basics` | 自動產生匿名測試資料 | 減少樣板程式碼、快速建立測試物件 | 需要大量測試資料、測試資料內容不重要時 |
| `dotnet-testing-autofixture-customization` | 客製化 AutoFixture 行為 | 控制資料生成規則、符合業務邏輯 | 需要特定規則的測試資料 |
| `dotnet-testing-bogus-fake-data` | 產生擬真假資料（姓名、地址、Email 等） | 資料看起來真實、易於除錯 | 需要真實感的測試資料、展示用途 |
| `dotnet-testing-test-data-builder-pattern` | 使用 Builder Pattern 建立測試資料 | 語意清晰、表達測試意圖 | 需要高可讀性、複雜物件建構 |
| `dotnet-testing-autofixture-bogus-integration` | 結合 AutoFixture 與 Bogus | 兩者優勢互補 | 同時需要自動化和擬真資料 |

**選擇指南**：

```
需要大量資料 + 不在乎真實感？
  → autofixture-basics

需要看起來真實的資料？
  → bogus-fake-data

需要高度可讀性和語意清晰？
  → test-data-builder-pattern

需要靈活控制生成規則？
  → autofixture-basics + autofixture-customization

需要自動化 + 擬真？
  → autofixture-basics + autofixture-bogus-integration
```

**學習路徑**：
- 入門：autofixture-basics 或 bogus-fake-data
- 進階：autofixture-customization + test-data-builder-pattern
- 整合：autofixture-bogus-integration

---

### 3. 測試替身（2 個技能）- 處理依賴

| 技能名稱 | 用途 | 涵蓋範圍 | 何時使用 |
|---------|------|---------|---------|
| `dotnet-testing-nsubstitute-mocking` | NSubstitute Mock 框架 | Mock、Stub、Spy、驗證呼叫 | 有外部依賴需要模擬 |
| `dotnet-testing-autofixture-nsubstitute-integration` | AutoFixture + NSubstitute 整合 | 自動建立 Mock 物件 | 使用 AutoFixture 且有大量依賴 |

**核心概念**：
- **Mock**：模擬物件並驗證互動
- **Stub**：提供預設回應
- **Spy**：記錄呼叫並驗證

**學習順序建議**：
1. 先學 nsubstitute-mocking（理解 Mock 基礎）
2. 如果已使用 AutoFixture，再學 integration（提升效率）

**常見用途**：
- 模擬資料庫存取層（Repository）
- 模擬外部 API 呼叫
- 模擬第三方服務
- 驗證方法是否被正確呼叫

---

### 4. 斷言驗證（3 個技能）- 寫出清晰測試

| 技能名稱 | 特色 | 提升幅度 | 何時使用 |
|---------|------|---------|---------|
| `dotnet-testing-awesome-assertions-guide` | FluentAssertions 流暢斷言 | ⭐⭐⭐ 高 | 所有測試（強烈推薦） |
| `dotnet-testing-complex-object-comparison` | 深層物件比對技巧 | ⭐⭐⭐ 高 | DTO、Entity、複雜物件驗證 |
| `dotnet-testing-fluentvalidation-testing` | 測試 FluentValidation 驗證器 | ⭐⭐ 中 | 使用 FluentValidation 的專案 |

**FluentAssertions 範例對比**：

```csharp
// 傳統斷言
Assert.Equal(expected.Name, actual.Name);
Assert.Equal(expected.Age, actual.Age);
Assert.True(actual.IsActive);

// FluentAssertions（更易讀）
actual.Should().BeEquivalentTo(expected, options => options
    .Including(x => x.Name)
    .Including(x => x.Age));
actual.IsActive.Should().BeTrue();
```

**學習路徑**：
1. awesome-assertions-guide（所有專案必學）
2. complex-object-comparison（處理複雜比對）
3. fluentvalidation-testing（特定需求）

---

### 5. 特殊場景（3 個技能）- 解決棘手問題

| 技能名稱 | 解決問題 | 實務價值 | 學習難度 |
|---------|---------|---------|---------|
| `dotnet-testing-datetime-testing-timeprovider` | 時間相關測試（使用 .NET 8+ TimeProvider） | ⭐⭐⭐ 高 | 中等 |
| `dotnet-testing-filesystem-testing-abstractions` | 檔案系統抽象化測試 | ⭐⭐⭐ 高 | 中等 |
| `dotnet-testing-private-internal-testing` | 測試私有/內部成員 | ⭐⭐ 中 | 簡單 |

**時間測試常見問題**：
```csharp
// 問題：難以測試
public bool IsExpired()
{
    return DateTime.Now > ExpiryDate;  // DateTime.Now 無法控制
}

// 解決：使用 TimeProvider
public bool IsExpired(TimeProvider timeProvider)
{
    return timeProvider.GetUtcNow() > ExpiryDate;  // 可在測試中注入假時間
}
```

**檔案系統測試常見問題**：
```csharp
// 問題：難以測試
public void SaveToFile(string content)
{
    File.WriteAllText("data.txt", content);  // 真實檔案操作
}

// 解決：使用 IFileSystem 抽象
public void SaveToFile(string content, IFileSystem fileSystem)
{
    fileSystem.File.WriteAllText("data.txt", content);  // 可在測試中使用記憶體檔案系統
}
```

**何時需要這些技能**：
- **TimeProvider**：排程系統、有效期檢查、時間計算
- **FileSystem**：檔案上傳、報表產生、設定檔讀寫
- **Private Testing**：重構遺留程式碼（但應優先考慮重構設計）

---

### 6. 測試度量（1 個技能）- 品質監控

| 技能名稱 | 用途 | 工具 | 何時使用 |
|---------|------|------|---------|
| `dotnet-testing-code-coverage-analysis` | 程式碼覆蓋率分析與報告 | Coverlet、ReportGenerator | 評估測試完整性、CI/CD 整合 |

**涵蓋內容**：
- 使用 Coverlet 收集覆蓋率資料
- 產生 HTML 報告
- 設定覆蓋率門檻
- CI/CD 整合

**重要提醒**：
- 高覆蓋率 ≠ 高品質測試
- 目標是有意義的測試，而非追求 100% 覆蓋率
- 覆蓋率是參考指標，不是絕對標準

---

### 7. 框架整合（2 個技能）- 進階整合

| 技能名稱 | 整合對象 | 價值 | 何時使用 |
|---------|---------|------|---------|
| `dotnet-testing-autodata-xunit-integration` | AutoFixture + xUnit Theory | 簡化參數化測試 | 使用 xUnit Theory 且需要測試資料 |
| `dotnet-testing-test-output-logging` | ITestOutputHelper + ILogger | 測試輸出與除錯 | 需要查看測試執行過程、除錯複雜測試 |

**AutoData 範例**：

```csharp
// 傳統寫法
[Theory]
[InlineData("user1", "pass1")]
[InlineData("user2", "pass2")]
public void Login_ValidCredentials_Success(string username, string password)
{
    // ...
}

// 使用 AutoData
[Theory, AutoData]
public void Login_ValidCredentials_Success(string username, string password)
{
    // username 和 password 自動產生
}
```

**Test Output 範例**：

```csharp
public class MyTests
{
    private readonly ITestOutputHelper _output;

    public MyTests(ITestOutputHelper output)
    {
        _output = output;
    }

    [Fact]
    public void Test()
    {
        _output.WriteLine("Debug information");  // 在測試輸出中顯示
    }
}
```

## 常見任務映射表

### 任務 1：從零建立測試專案

**情境**：全新專案，需要建立完整的測試基礎設施

**推薦技能組合**：
1. `dotnet-testing-xunit-project-setup` - 建立專案結構
2. `dotnet-testing-test-naming-conventions` - 設定命名規範
3. `dotnet-testing-unit-test-fundamentals` - 撰寫第一個測試

**實施步驟**：
1. 使用 xunit-project-setup 建立測試專案
2. 配置 .csproj 檔案與 NuGet 套件
3. 學習命名規範，制定團隊標準
4. 按照 3A Pattern 撰寫第一個測試

**提示詞範例**：
```
請使用 dotnet-testing-xunit-project-setup skill 為我的專案建立測試結構，
專案名稱是 MyProject，然後使用 dotnet-testing-unit-test-fundamentals skill
為 Calculator 類別建立第一個測試。
```

---

### 任務 2：為有依賴的服務類別寫測試

**情境**：UserService 依賴 IUserRepository 和 IEmailService

**推薦技能組合**：
1. `dotnet-testing-unit-test-fundamentals` - 測試結構
2. `dotnet-testing-nsubstitute-mocking` - 模擬依賴
3. `dotnet-testing-autofixture-basics` - 產生測試資料
4. `dotnet-testing-awesome-assertions-guide` - 清晰斷言

**實施步驟**：
1. 使用 NSubstitute 建立 Repository 和 EmailService 的 Mock
2. 用 AutoFixture 產生 User 測試資料
3. 按照 3A Pattern 撰寫測試
4. 使用 FluentAssertions 驗證結果

**提示詞範例**：
```
請使用 dotnet-testing-nsubstitute-mocking 和 dotnet-testing-autofixture-basics skills
為 UserService 建立測試。UserService 的建構函式需要 IUserRepository 和 IEmailService。
請測試 CreateUser 方法。
```

**預期程式碼結構**：
```csharp
[Fact]
public void CreateUser_ValidUser_ShouldSaveAndSendEmail()
{
    // Arrange - 使用 NSubstitute 建立 Mock
    var repository = Substitute.For<IUserRepository>();
    var emailService = Substitute.For<IEmailService>();

    // 使用 AutoFixture 產生測試資料
    var fixture = new Fixture();
    var user = fixture.Create<User>();

    var sut = new UserService(repository, emailService);

    // Act
    sut.CreateUser(user);

    // Assert - 使用 FluentAssertions
    repository.Received(1).Save(Arg.Is<User>(u => u.Email == user.Email));
    emailService.Received(1).SendWelcomeEmail(user.Email);
}
```

---

### 任務 3：測試有時間邏輯的程式碼

**情境**：OrderService 判斷訂單是否過期

**推薦技能組合**：
1. `dotnet-testing-datetime-testing-timeprovider` - TimeProvider 抽象化
2. `dotnet-testing-unit-test-fundamentals` - 測試基礎
3. `dotnet-testing-nsubstitute-mocking` - Mock TimeProvider

**實施步驟**：
1. 重構程式碼，注入 TimeProvider
2. 在測試中使用 FakeTimeProvider
3. 控制時間進行測試

**提示詞範例**：
```
請使用 dotnet-testing-datetime-testing-timeprovider skill 協助重構 OrderService，
使其可測試時間相關邏輯。訂單在建立 30 天後視為過期。
```

**預期程式碼結構**：
```csharp
// 重構前
public class OrderService
{
    public bool IsExpired(Order order)
    {
        return DateTime.Now > order.CreatedDate.AddDays(30);  // 無法測試
    }
}

// 重構後
public class OrderService
{
    private readonly TimeProvider _timeProvider;

    public OrderService(TimeProvider timeProvider)
    {
        _timeProvider = timeProvider;
    }

    public bool IsExpired(Order order)
    {
        return _timeProvider.GetUtcNow() > order.CreatedDate.AddDays(30);
    }
}

// 測試
[Fact]
public void IsExpired_Order31DaysOld_ShouldReturnTrue()
{
    // Arrange
    var fakeTime = new FakeTimeProvider();
    fakeTime.SetUtcNow(new DateTimeOffset(2024, 1, 31, 0, 0, 0, TimeSpan.Zero));

    var order = new Order
    {
        CreatedDate = new DateTimeOffset(2024, 1, 1, 0, 0, 0, TimeSpan.Zero)
    };

    var sut = new OrderService(fakeTime);

    // Act
    var result = sut.IsExpired(order);

    // Assert
    result.Should().BeTrue();
}
```

---

### 任務 4：改善測試可讀性

**情境**：現有測試難以理解，維護困難

**推薦技能組合**：
1. `dotnet-testing-test-naming-conventions` - 命名規範
2. `dotnet-testing-awesome-assertions-guide` - 流暢斷言
3. `dotnet-testing-test-data-builder-pattern` - 清晰的測試資料

**實施步驟**：
1. 重新命名測試方法，遵循三段式命名
2. 使用 FluentAssertions 改寫斷言
3. 使用 Builder Pattern 建立測試資料

**提示詞範例**：
```
請使用 dotnet-testing-awesome-assertions-guide 和 dotnet-testing-test-naming-conventions skills
檢視並改善這些測試的可讀性：
[貼上測試程式碼]
```

---

### 任務 5：產生大量測試資料

**情境**：效能測試需要 1000 筆 Customer 資料

**推薦技能組合**：
1. `dotnet-testing-autofixture-basics` - 自動產生
2. `dotnet-testing-bogus-fake-data` - 擬真資料（可選）
3. `dotnet-testing-autofixture-bogus-integration` - 結合兩者優勢（可選）

**實施步驟**：
1. 使用 AutoFixture.CreateMany<T>() 產生大量資料
2. （可選）使用 Bogus 讓資料更真實
3. （可選）整合兩者，自動化 + 擬真

**提示詞範例**：
```
請使用 dotnet-testing-autofixture-basics skill 為效能測試產生 1000 筆 Customer 資料，
每筆資料需要有 Name、Email、PhoneNumber 等欄位。
```

---

### 任務 6：測試 FluentValidation 驗證器

**情境**：CreateUserValidator 有多條驗證規則

**推薦技能**：
- `dotnet-testing-fluentvalidation-testing`

**實施步驟**：
1. 使用 FluentValidation.TestHelper
2. 測試每條驗證規則
3. 測試組合情境

**提示詞範例**：
```
請使用 dotnet-testing-fluentvalidation-testing skill 為 CreateUserValidator 建立測試。
驗證器的規則包括：Name 必填、Email 格式驗證、Age 必須大於 18。
```

---

### 任務 7：測試檔案上傳功能

**情境**：FileUploadService 需要儲存上傳的檔案

**推薦技能**：
- `dotnet-testing-filesystem-testing-abstractions`

**實施步驟**：
1. 重構程式碼，使用 IFileSystem
2. 在測試中使用 MockFileSystem
3. 驗證檔案操作

**提示詞範例**：
```
請使用 dotnet-testing-filesystem-testing-abstractions skill 協助測試 FileUploadService。
該服務會將上傳的檔案儲存到 uploads/ 目錄。
```

## 學習路徑建議

### 新手路徑（1-2 週）

**目標**：建立測試基礎，能夠撰寫基本的單元測試

#### 階段 1：建立基礎（Day 1-5）

**Day 1-2：測試基礎概念**
- 技能：`dotnet-testing-unit-test-fundamentals`
- 學習重點：
  - FIRST 原則
  - 3A Pattern
  - [Fact] 與 [Theory] 的使用
  - 基本斷言方法
- 實作練習：為簡單的 Calculator 類別寫測試

**Day 3：命名規範**
- 技能：`dotnet-testing-test-naming-conventions`
- 學習重點：
  - 三段式命名法
  - 中文命名建議
  - 測試類別命名
- 實作練習：重新命名 Day 1-2 的測試

**Day 4-5：建立測試專案**
- 技能：`dotnet-testing-xunit-project-setup`
- 學習重點：
  - 專案結構規劃
  - .csproj 設定
  - NuGet 套件管理
  - xunit.runner.json 設定
- 實作練習：為現有專案建立測試專案

#### 階段 2：提升品質（Day 6-10）

**Day 6-7：流暢斷言**
- 技能：`dotnet-testing-awesome-assertions-guide`
- 學習重點：
  - FluentAssertions 基礎
  - 集合斷言
  - 例外斷言
  - 物件比對
- 實作練習：改寫之前的測試，使用 FluentAssertions

**Day 8：測試輸出**
- 技能：`dotnet-testing-test-output-logging`
- 學習重點：
  - ITestOutputHelper 使用
  - 整合 ILogger
  - 除錯技巧
- 實作練習：為複雜測試加入輸出

**Day 9-10：處理依賴**
- 技能：`dotnet-testing-nsubstitute-mocking`
- 學習重點：
  - Mock vs Stub vs Spy
  - 基本模擬設定
  - 驗證呼叫
  - Returns 和 Throws
- 實作練習：測試有 Repository 依賴的 Service

#### 階段 3：自動化測試資料（Day 11-14）

**Day 11-12：AutoFixture 基礎**
- 技能：`dotnet-testing-autofixture-basics`
- 學習重點：
  - 匿名測試資料
  - Create 和 CreateMany
  - 減少測試樣板程式碼
- 實作練習：使用 AutoFixture 簡化測試

**Day 13-14：整合應用**
- 技能：
  - `dotnet-testing-autodata-xunit-integration`
  - `dotnet-testing-autofixture-nsubstitute-integration`
- 學習重點：
  - AutoData 屬性
  - 自動建立 Mock
  - 組合使用
- 實作練習：綜合應用 AutoFixture + NSubstitute

#### 階段 4：總結與實戰（Day 15）

- 為一個小型專案建立完整測試
- 應用所學的所有技能
- 設定 Code Coverage

---

### 進階路徑（2-3 週）

**前置條件**：完成新手路徑

#### 第一週：測試資料專精

**Day 1-2：AutoFixture 進階**
- 技能：`dotnet-testing-autofixture-customization`
- 學習重點：
  - Customizations
  - Specimens
  - Behaviors
  - 自訂生成規則

**Day 3-4：擬真資料**
- 技能：`dotnet-testing-bogus-fake-data`
- 學習重點：
  - Faker 使用
  - 真實感資料生成
  - 本地化資料

**Day 5：Builder Pattern**
- 技能：`dotnet-testing-test-data-builder-pattern`
- 學習重點：
  - 建立 Test Data Builder
  - Fluent Interface
  - 預設值設定

**Day 6-7：整合應用**
- 技能：`dotnet-testing-autofixture-bogus-integration`
- 學習重點：
  - 整合 AutoFixture 與 Bogus
  - 選擇合適的工具

#### 第二週：特殊場景處理

**Day 1-2：時間測試**
- 技能：`dotnet-testing-datetime-testing-timeprovider`
- 學習重點：
  - TimeProvider 抽象化
  - FakeTimeProvider 使用
  - 時區處理

**Day 3-4：檔案系統測試**
- 技能：`dotnet-testing-filesystem-testing-abstractions`
- 學習重點：
  - IFileSystem 介面
  - MockFileSystem 使用
  - 檔案操作測試

**Day 5-6：複雜物件比對**
- 技能：`dotnet-testing-complex-object-comparison`
- 學習重點：
  - 深層物件比對
  - 排除特定屬性
  - 自訂比對規則

**Day 7：私有成員測試**
- 技能：`dotnet-testing-private-internal-testing`
- 學習重點：
  - InternalsVisibleTo
  - 測試策略
  - 何時應避免

#### 第三週：品質與整合

**Day 1-2：驗證測試**
- 技能：`dotnet-testing-fluentvalidation-testing`
- 學習重點：
  - TestHelper 使用
  - 驗證規則測試
  - 錯誤訊息驗證

**Day 3-4：程式碼覆蓋率**
- 技能：`dotnet-testing-code-coverage-analysis`
- 學習重點：
  - Coverlet 使用
  - 報告產生
  - CI/CD 整合

**Day 5-7：綜合實戰**
- 為中型專案建立完整測試
- 應用所有學到的技能
- 建立測試最佳實踐文件

---

### 快速參考：我該先學什麼？

**我是新手，完全沒寫過測試**
→ 新手路徑階段 1：unit-test-fundamentals → test-naming-conventions → xunit-project-setup

**我會寫基礎測試，想提升品質**
→ 新手路徑階段 2：awesome-assertions-guide → nsubstitute-mocking

**我想提升測試效率**
→ 進階路徑第一週：測試資料生成系列

**我遇到特殊場景（時間、檔案系統）**
→ 進階路徑第二週：特殊場景處理系列

**我想評估測試品質**
→ code-coverage-analysis

## 引導對話範例

以下範例展示 AI 如何與您互動，幫助您選擇正確的技能。

---

### 範例 1：新手入門

**您**：我想學習 .NET 測試

**AI**：我很樂意協助您學習 .NET 測試！為了提供最適合的指引，請告訴我：

1. **您的測試經驗**：
   - [ ] 完全沒寫過測試
   - [ ] 寫過一些基礎測試
   - [ ] 有一定經驗，想深入學習

2. **您的專案情況**：
   - [ ] 新專案，從零開始
   - [ ] 現有專案，想加入測試
   - [ ] 改善現有測試品質

請告訴我您的情況，我會推薦適合的學習路徑。

**您**：完全沒寫過測試，是新專案

**AI**：太好了！我會為您規劃一個循序漸進的學習路徑。建議您從以下三個技能開始：

**第一步：理解測試基礎（1-2 天）**
使用 `dotnet-testing-unit-test-fundamentals` skill
學習重點：FIRST 原則、3A Pattern、基本測試結構

**第二步：學習命名規範（半天）**
使用 `dotnet-testing-test-naming-conventions` skill
學習重點：三段式命名法、提升可讀性

**第三步：建立測試專案（1 天）**
使用 `dotnet-testing-xunit-project-setup` skill
學習重點：專案結構、套件設定

需要我使用這些 skills 協助您開始嗎？

---

### 範例 2：處理依賴

**您**：我需要為 UserService 寫測試，但它依賴資料庫和外部 API

**AI**：了解！您的情況需要模擬（Mock）外部依賴。我推薦以下技能組合：

**必要技能**：
1. `dotnet-testing-nsubstitute-mocking` - 模擬資料庫與 API 依賴
   用途：建立 IUserRepository 和 IApiClient 的 Mock 物件

**建議搭配**：
2. `dotnet-testing-autofixture-basics` - 自動產生測試資料
   用途：快速產生 User 測試物件

3. `dotnet-testing-awesome-assertions-guide` - 清晰的斷言
   用途：讓測試更易讀

**實施建議**：
1. 先使用 NSubstitute 為依賴建立 Mock
2. 用 AutoFixture 產生 User 測試資料
3. 按照 3A Pattern 撰寫測試
4. 使用 FluentAssertions 驗證結果

需要我使用這些 skills 協助您建立測試嗎？

---

### 範例 3：特定問題

**您**：我的程式碼用 DateTime.Now，要怎麼測試？

**AI**：這是時間相關測試的經典問題！我推薦使用 `dotnet-testing-datetime-testing-timeprovider` skill。

**問題分析**：
`DateTime.Now` 每次執行都不同，無法寫出可重複的測試（違反 FIRST 原則中的 Repeatable）。

**解決方案**：
1. 重構程式碼，注入 `TimeProvider`
2. 在測試中使用 `FakeTimeProvider` 控制時間
3. 這樣就能測試特定時間點的行為

**範例**：
```csharp
// 重構前（難以測試）
public bool IsExpired()
{
    return DateTime.Now > ExpiryDate;
}

// 重構後（可測試）
public bool IsExpired(TimeProvider timeProvider)
{
    return timeProvider.GetUtcNow() > ExpiryDate;
}
```

需要我使用 `dotnet-testing-datetime-testing-timeprovider` skill 協助您重構並建立測試嗎？

---

### 範例 4：改善現有測試

**您**：我的測試很難讀，維護困難

**AI**：測試可讀性問題很常見！我建議從以下三個方向改善：

**1. 命名規範**
使用 `dotnet-testing-test-naming-conventions` skill
- 採用三段式命名：`[方法]_[情境]_[預期]`
- 讓測試名稱自我說明

**2. 流暢斷言**
使用 `dotnet-testing-awesome-assertions-guide` skill
- 使用 FluentAssertions 取代傳統斷言
- 大幅提升可讀性

**3. 清晰的測試資料**
使用 `dotnet-testing-test-data-builder-pattern` skill
- 使用 Builder Pattern 建立測試資料
- 讓測試意圖更明確

**快速範例**：
```csharp
// 改善前
[Fact]
public void Test1()
{
    var u = new User { Name = "test", Age = 20 };
    var r = svc.Validate(u);
    Assert.True(r);
}

// 改善後
[Fact]
public void Validate_AdultUser_ShouldReturnTrue()
{
    // Arrange
    var user = new UserBuilder()
        .WithName("test")
        .WithAge(20)
        .Build();

    // Act
    var result = _service.Validate(user);

    // Assert
    result.Should().BeTrue();
}
```

要不要我協助您改善特定的測試？請貼上您的測試程式碼。

## 與進階技能的關係

完成基礎技能後，如果您需要進行整合測試、API 測試、容器化測試或微服務測試，請參考：

**進階整合測試** → `dotnet-testing-advanced`
- ASP.NET Core 整合測試
- 容器化測試（Testcontainers）
- 微服務測試（.NET Aspire）
- 測試框架升級與遷移

## 相關資源

### 原始資料來源

- **iThome 鐵人賽系列文章**：[老派軟體工程師的測試修練 - 30 天挑戰](https://ithelp.ithome.com.tw/users/20066083/ironman/8276)
  🏆 2025 iThome 鐵人賽 Software Development 組冠軍

- **完整範例程式碼**：[30Days_in_Testing_Samples](https://github.com/kevintsengtw/30Days_in_Testing_Samples)
  包含所有範例專案的可執行程式碼

### 學習文檔

本技能集基於以下完整教材提煉而成：

- **Agent Skills：從架構設計到實戰應用** (docs/Agent_Skills_Mastery.pdf)
  完整涵蓋 Agent Skills 從理論到實踐

- **Claude Code Skills: 讓 AI 變身專業工匠** (docs/Agent_Skills_Architecture.pdf)
  深入解析 Agent Skills 的架構設計

- **.NET Testing：寫得更好、跑得更快** (docs/NET_Testing_Write_Better_Run_Faster.pdf)
  測試執行優化與除錯技巧

## 下一步

選擇符合您需求的技能開始學習，或告訴我您的具體情況，我會推薦最適合的學習路徑！

**快速開始**：
- 新手 → 從 `dotnet-testing-unit-test-fundamentals` 開始
- 有經驗 → 告訴我您遇到的具體問題
- 不確定 → 告訴我您的專案情況，我會幫您分析
