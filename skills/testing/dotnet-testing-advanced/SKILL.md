---
name: dotnet-testing-advanced
description: |
  .NET 進階測試技能總覽與引導中心。當使用者詢問「整合測試」、「API 測試」、「容器化測試」、「微服務測試」、「測試框架遷移」、「Testcontainers」、「Aspire 測試」等進階測試需求時觸發。會根據具體需求推薦適合的子技能組合，涵蓋整合測試、Testcontainers、Aspire 測試、框架升級等 8 個進階技能。
  Keywords: integration testing, 整合測試, API testing, advanced testing, 進階測試, testcontainers, aspire testing, WebApplicationFactory, TestServer, database test, 資料庫測試, EF Core test, MongoDB test, Redis test, Docker test, 容器測試, microservice test, 微服務測試, .NET Aspire, xUnit upgrade, TUnit, framework migration
license: MIT
metadata:
  author: Kevin Tseng
  version: "1.0.0"
  tags: ".NET, testing, integration, advanced, testcontainers, aspire"
  related_skills: "dotnet-testing"
  skill_count: 8
  skill_type: "overview"
---

# .NET 進階測試技能總覽

---

## 🤖 AI Agent 重要提示

**當您（AI Agent）被載入此進階入口 skill 時，請先閱讀以下指引**：

### 📋 本技能的定位

本檔案是「進階測試導航中心」，用於幫助找到正確的**進階子技能**。

#### 您的任務是

1. ✅ 根據使用者需求匹配對應的進階子技能
2. ✅ 使用 `Skill` tool 載入具體的子技能
3. ✅ 讓子技能提供專業的整合測試指引

#### 禁止行為

- ❌ 不要在本入口 skill 中直接提供整合測試程式碼
- ❌ 不要在沒有載入子技能的情況下開始實作測試
- ❌ 不要跳過子技能直接提供「一般性」整合測試建議

---

## 🎯 快速技能對照表（AI Agent 必讀）

**使用者提到的關鍵字 → 應載入的進階子技能**

### 整合測試技能

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **API 測試**、Controller 測試、端點測試 | `/skill dotnet-testing-advanced-aspnet-integration-testing` | 基礎 API 整合測試 |
| **完整 CRUD**、WebAPI 測試、業務流程測試 | `/skill dotnet-testing-advanced-webapi-integration-testing` | 完整 API 流程測試 |
| **WebApplicationFactory**、TestServer | `/skill dotnet-testing-advanced-aspnet-integration-testing` | WebApplicationFactory 使用 |

### 容器化測試技能

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **SQL Server 容器**、PostgreSQL、MySQL | `/skill dotnet-testing-advanced-testcontainers-database` | 關聯式資料庫容器測試 |
| **MongoDB**、Redis、Elasticsearch | `/skill dotnet-testing-advanced-testcontainers-nosql` | NoSQL 資料庫容器測試 |
| **真實資料庫**、EF Core 測試、Dapper 測試 | `/skill dotnet-testing-advanced-testcontainers-database` | 真實資料庫行為測試 |
| **Testcontainers**、容器測試、Docker 測試 | `/skill dotnet-testing-advanced-testcontainers-database` | Testcontainers 基礎 |

### 微服務測試技能

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **.NET Aspire**、微服務測試、分散式測試 | `/skill dotnet-testing-advanced-aspire-testing` | Aspire 微服務測試 |
| **DistributedApplication**、服務間通訊 | `/skill dotnet-testing-advanced-aspire-testing` | Aspire 應用測試 |

### 框架升級技能

| 使用者說... | 載入指令 | 用途說明 |
|------------|----------|----------|
| **xUnit 升級**、xUnit 3.x、版本升級 | `/skill dotnet-testing-advanced-xunit-upgrade-guide` | xUnit 2.x → 3.x 升級 |
| **TUnit**、新測試框架、TUnit 基礎 | `/skill dotnet-testing-advanced-tunit-fundamentals` | TUnit 基礎與遷移 |
| **TUnit 進階**、TUnit DI、平行執行 | `/skill dotnet-testing-advanced-tunit-advanced` | TUnit 進階功能 |

---

## ⚠️ 使用流程範例

### ✅ 正確流程

```
使用者：請幫我建立 ProductsController 的 API 整合測試

AI：我注意到您需要進行 API 整合測試。根據快速對照表，
    我應該載入 dotnet-testing-advanced-aspnet-integration-testing skill。

    [使用 Skill tool 載入子技能]

AI：現在按照 ASP.NET Core Integration Testing skill 的指引為您建立測試...
```

### ❌ 錯誤流程

```
使用者：請幫我建立 ProductsController 的 API 整合測試

AI：好的，我來寫整合測試...（直接開始寫程式碼，沒有載入子技能）
```

---

## 📚 完整技能清單

如需查看完整的 8 個進階技能清單、詳細決策樹、學習路徑建議，請繼續閱讀本檔案後續內容。

**人類開發者參考**：如需快速查找，請查看 [SKILLS_QUICK_INDEX.md](/SKILLS_QUICK_INDEX.md)

---

## 適用情境

當您需要以下進階測試能力時，我會協助您找到正確的技能：

- 測試完整的 Web API 端點與 HTTP 流程
- 在測試中使用真實的資料庫（容器化）
- 測試 NoSQL 資料庫（MongoDB、Redis 等）
- 測試微服務架構與分散式系統
- 升級測試框架版本（xUnit 2.x → 3.x）
- 遷移到新測試框架（TUnit）
- 建立端到端的整合測試

## 快速決策樹

### 我需要哪種進階測試？

#### 情境 1：測試 ASP.NET Core Web API

**選項 A - 基礎 API 測試**
→ `dotnet-testing-advanced-aspnet-integration-testing`

**適合**：
- 簡單的 API 端點測試
- 不需要真實資料庫（使用記憶體資料庫）
- 測試路由、模型綁定、HTTP 回應

**涵蓋內容**：
- WebApplicationFactory 使用
- TestServer 設定
- HTTP 回應驗證
- 記憶體資料庫配置

---

**選項 B - 完整的 WebAPI 流程測試**
→ `dotnet-testing-advanced-webapi-integration-testing`

**適合**：
- 完整的 CRUD API 測試
- 需要測試完整的業務流程
- 需要測試資料準備與清理

**涵蓋內容**：
- 完整的 GET、POST、PUT、DELETE 測試
- 錯誤處理驗證
- 測試基底類別模式
- 資料準備策略

---

#### 情境 2：測試需要真實資料庫

**選項 A - 關聯式資料庫（SQL Server、PostgreSQL、MySQL）**
→ `dotnet-testing-advanced-testcontainers-database`

**適合**：
- Entity Framework Core 測試
- Dapper 測試
- 真實資料庫行為驗證
- 需要測試資料庫特定功能（stored procedures、triggers 等）

**支援資料庫**：
- SQL Server
- PostgreSQL
- MySQL
- MariaDB

---

**選項 B - NoSQL 資料庫（MongoDB、Redis、Elasticsearch）**
→ `dotnet-testing-advanced-testcontainers-nosql`

**適合**：
- MongoDB 文件操作測試
- Redis 快取測試
- Elasticsearch 搜尋測試
- NoSQL 特有功能測試

**支援資料庫**：
- MongoDB
- Redis
- Elasticsearch

---

#### 情境 3：測試微服務架構

→ `dotnet-testing-advanced-aspire-testing`

**適合**：
- .NET Aspire 專案
- 分散式應用測試
- 服務間通訊測試
- 微服務整合測試

**涵蓋內容**：
- DistributedApplication 測試
- 服務依賴管理
- 跨服務測試
- 測試容器編排

---

#### 情境 4：升級或遷移測試框架

**選項 A - xUnit 升級（2.x → 3.x）**
→ `dotnet-testing-advanced-xunit-upgrade-guide`

**適合**：
- 現有專案使用 xUnit 2.x
- 想升級到 xUnit 3.x
- 了解版本差異

**涵蓋內容**：
- 重大變更說明
- 升級步驟指引
- 相容性問題處理
- 最佳實踐

---

**選項 B - 遷移到 TUnit（基礎）**
→ `dotnet-testing-advanced-tunit-fundamentals`

**適合**：
- 評估是否遷移到 TUnit
- 了解 TUnit 基礎
- 學習 TUnit 與 xUnit 的差異

**涵蓋內容**：
- TUnit 核心概念
- 與 xUnit 對比
- 遷移步驟
- 基本使用方式

---

**選項 C - TUnit 進階功能**
→ `dotnet-testing-advanced-tunit-advanced`

**適合**：
- 已使用 TUnit 基礎
- 想深入使用 TUnit 功能
- 需要平行執行、依賴注入等進階特性

**涵蓋內容**：
- 資料驅動測試
- 依賴注入
- 平行執行控制
- 進階特性

---

## 技能分類地圖

### 1. 整合測試（4 個技能）- Web API 測試

| 技能名稱 | 測試範圍 | 資料庫 | 適用場景 |
|---------|---------|--------|---------|
| `dotnet-testing-advanced-aspnet-integration-testing` | WebApplicationFactory、TestServer、HTTP 回應 | 記憶體資料庫 | 基礎 API 整合測試 |
| `dotnet-testing-advanced-webapi-integration-testing` | 完整 CRUD、錯誤處理、業務流程 | 記憶體/真實 | 真實 API 專案測試 |
| `dotnet-testing-advanced-testcontainers-database` | SQL Server、PostgreSQL、MySQL | 真實（容器化） | 需要真實資料庫行為 |
| `dotnet-testing-advanced-testcontainers-nosql` | MongoDB、Redis、Elasticsearch | 真實（容器化） | NoSQL 資料庫測試 |

#### 技能詳細說明

**aspnet-integration-testing**

**核心價值**：
- 學習 WebApplicationFactory 基礎
- 理解整合測試概念
- 測試 HTTP 端點而不啟動真實伺服器

**適合情境**：
- API 端點基礎測試
- 路由驗證
- 中介軟體測試
- 不需要真實資料庫

**學習難度**：⭐⭐ 中等

**前置技能**：
- `dotnet-testing-unit-test-fundamentals`（必須）
- `dotnet-testing-awesome-assertions-guide`（建議）

---

**webapi-integration-testing**

**核心價值**：
- 完整的 API 測試流程
- 測試資料管理策略
- 錯誤處理驗證
- 真實業務場景測試

**適合情境**：
- 正式專案的 API 測試
- 完整的 CRUD 流程
- 複雜的業務邏輯驗證
- 需要測試資料準備與清理

**學習難度**：⭐⭐⭐ 中高

**前置技能**：
- `dotnet-testing-advanced-aspnet-integration-testing`（必須）
- `dotnet-testing-nsubstitute-mocking`（建議）

---

**testcontainers-database**

**核心價值**：
- 使用真實資料庫測試
- 自動化容器管理
- 測試資料庫特定功能
- 隔離的測試環境

**適合情境**：
- EF Core 測試
- Dapper 測試
- Stored Procedures 測試
- 資料庫遷移測試

**學習難度**：⭐⭐⭐ 中高

**前置技能**：
- `dotnet-testing-unit-test-fundamentals`（必須）
- Docker 基礎知識（必須）

**技術需求**：
- Docker Desktop 已安裝
- WSL2（Windows 環境）

---

**testcontainers-nosql**

**核心價值**：
- 測試 NoSQL 資料庫操作
- 容器化 NoSQL 環境
- 真實資料庫行為驗證

**適合情境**：
- MongoDB 文件操作
- Redis 快取邏輯
- Elasticsearch 搜尋功能

**學習難度**：⭐⭐⭐ 中高

**前置技能**：
- `dotnet-testing-advanced-testcontainers-database`（建議）
- NoSQL 資料庫基礎知識

---

### 2. 微服務測試（1 個技能）- 分散式系統

| 技能名稱 | 測試範圍 | 架構 | 適用場景 |
|---------|---------|------|---------|
| `dotnet-testing-advanced-aspire-testing` | .NET Aspire 分散式應用 | 微服務 | 雲原生、微服務架構 |

#### 技能詳細說明

**aspire-testing**

**核心價值**：
- 測試 .NET Aspire 專案
- 分散式應用整合測試
- 服務依賴管理
- 端到端流程驗證

**適合情境**：
- .NET Aspire 微服務專案
- 多服務協作測試
- 服務發現測試
- 分散式追蹤驗證

**學習難度**：⭐⭐⭐⭐ 高

**前置技能**：
- `dotnet-testing-advanced-aspnet-integration-testing`（必須）
- `dotnet-testing-advanced-testcontainers-database`（建議）
- .NET Aspire 基礎知識（必須）

**技術需求**：
- .NET 8+
- .NET Aspire Workload
- Docker Desktop

**涵蓋內容**：
- DistributedApplication 測試
- 服務間通訊測試
- 依賴服務管理
- 測試容器編排

---

### 3. 框架遷移（3 個技能）- 測試框架升級

| 技能名稱 | 遷移路徑 | 難度 | 適用場景 |
|---------|---------|------|---------|
| `dotnet-testing-advanced-xunit-upgrade-guide` | xUnit 2.x → 3.x | ⭐⭐ 中等 | 升級現有 xUnit 專案 |
| `dotnet-testing-advanced-tunit-fundamentals` | xUnit → TUnit（基礎） | ⭐⭐ 中等 | 評估或遷移到 TUnit |
| `dotnet-testing-advanced-tunit-advanced` | TUnit 進階功能 | ⭐⭐⭐ 中高 | 深入使用 TUnit |

#### 技能詳細說明

**xunit-upgrade-guide**

**核心價值**：
- 了解 xUnit 3.x 新特性
- 處理升級問題
- 遷移步驟指引

**適合情境**：
- 專案使用 xUnit 2.x
- 想升級到最新版本
- 了解版本差異

**學習難度**：⭐⭐ 中等

**涵蓋內容**：
- 重大變更清單
- 套件升級步驟
- 相容性問題處理
- 升級檢查清單

**何時升級**：
- 需要 xUnit 3.x 新功能
- .NET 9+ 專案
- 解決已知問題

---

**tunit-fundamentals**

**核心價值**：
- 了解 TUnit 新世代測試框架
- 學習 TUnit 核心概念
- 評估遷移可行性

**適合情境**：
- 考慮從 xUnit 遷移
- 新專案選擇測試框架
- 了解現代測試框架

**學習難度**：⭐⭐ 中等

**涵蓋內容**：
- TUnit vs xUnit 對比
- 基本測試撰寫
- 屬性與斷言
- 遷移建議

**TUnit 優勢**：
- 更好的效能
- 原生支援依賴注入
- 更靈活的測試組織
- 現代化的 API 設計

---

**tunit-advanced**

**核心價值**：
- 深入使用 TUnit 進階功能
- 平行執行控制
- 依賴注入整合
- 資料驅動測試

**適合情境**：
- 已使用 TUnit 基礎
- 需要進階功能
- 大型測試專案

**學習難度**：⭐⭐⭐ 中高

**前置技能**：
- `dotnet-testing-advanced-tunit-fundamentals`（必須）

**涵蓋內容**：
- 進階資料驅動測試
- 依賴注入容器
- 測試執行控制
- 自訂測試框架行為

---

## 常見任務映射表

### 任務 1：測試 ASP.NET Core Web API（基礎）

**情境**：為簡單的 ProductsController 建立整合測試

**推薦技能**：
- `dotnet-testing-advanced-aspnet-integration-testing`

**適用條件**：
- 簡單的 CRUD API
- 不需要真實資料庫
- 測試基本的 HTTP 端點

**實施步驟**：
1. 建立 CustomWebApplicationFactory
2. 設定記憶體資料庫
3. 撰寫 GET、POST 測試
4. 使用 FluentAssertions.Web 驗證回應

**提示詞範例**：
```
請使用 dotnet-testing-advanced-aspnet-integration-testing skill
為我的 ProductsController 建立整合測試。Controller 有 GetAll 和 GetById 兩個端點。
```

**預期程式碼結構**：
```csharp
public class ProductsControllerTests : IClassFixture<CustomWebApplicationFactory>
{
    private readonly HttpClient _client;

    public ProductsControllerTests(CustomWebApplicationFactory factory)
    {
        _client = factory.CreateClient();
    }

    [Fact]
    public async Task GetAll_ShouldReturnProducts()
    {
        // Act
        var response = await _client.GetAsync("/api/products");

        // Assert
        response.Should().Be200Ok();
        var products = await response.Content.ReadFromJsonAsync<List<Product>>();
        products.Should().NotBeEmpty();
    }
}
```

---

### 任務 2：測試 ASP.NET Core Web API（完整流程）

**情境**：為 ShippersController 建立完整的 CRUD 測試

**推薦技能**：
- `dotnet-testing-advanced-webapi-integration-testing`

**適用條件**：
- 完整的 CRUD API
- 需要測試錯誤處理
- 需要測試資料準備與清理

**實施步驟**：
1. 建立測試基底類別（BaseIntegrationTest）
2. 實作 IAsyncLifetime 進行資料準備/清理
3. 測試所有 CRUD 端點
4. 驗證錯誤處理（404、400、409 等）

**提示詞範例**：
```
請使用 dotnet-testing-advanced-webapi-integration-testing skill
為我的 ShippersController 建立完整的 CRUD 測試。需要測試：
- GET /api/shippers（取得所有）
- GET /api/shippers/{id}（取得單一）
- POST /api/shippers（新增）
- PUT /api/shippers/{id}（更新）
- DELETE /api/shippers/{id}（刪除）
並且驗證錯誤情境（如找不到資源）。
```

**預期測試涵蓋**：
- ✅ GET 成功回傳資料
- ✅ GET 不存在的 ID 回傳 404
- ✅ POST 新增成功
- ✅ POST 無效資料回傳 400
- ✅ PUT 更新成功
- ✅ PUT 不存在的 ID 回傳 404
- ✅ DELETE 刪除成功
- ✅ DELETE 不存在的 ID 回傳 404

---

### 任務 3：測試需要真實資料庫的程式碼（SQL）

**情境**：測試 OrderRepository（使用 SQL Server）

**推薦技能**：
- `dotnet-testing-advanced-testcontainers-database`

**適用條件**：
- 使用 EF Core 或 Dapper
- 需要測試真實資料庫行為
- 需要測試資料庫特定功能

**實施步驟**：
1. 設定 Testcontainers.MsSql
2. 執行資料庫遷移
3. 測試 Repository 方法
4. 每個測試後清理資料

**提示詞範例**：
```
請使用 dotnet-testing-advanced-testcontainers-database skill
為我的 OrderRepository 建立測試。Repository 使用 EF Core 連接 SQL Server。
需要測試 GetById、Create、Update、Delete 方法。
```

**預期程式碼結構**：
```csharp
public class OrderRepositoryTests : IAsyncLifetime
{
    private MsSqlContainer _container;
    private OrderDbContext _context;
    private OrderRepository _sut;

    public async Task InitializeAsync()
    {
        // 啟動 SQL Server 容器
        _container = new MsSqlBuilder().Build();
        await _container.StartAsync();

        // 建立 DbContext
        var options = new DbContextOptionsBuilder<OrderDbContext>()
            .UseSqlServer(_container.GetConnectionString())
            .Options;

        _context = new OrderDbContext(options);
        await _context.Database.MigrateAsync();

        _sut = new OrderRepository(_context);
    }

    [Fact]
    public async Task GetById_ExistingOrder_ShouldReturnOrder()
    {
        // Arrange
        var order = new Order { /* ... */ };
        await _context.Orders.AddAsync(order);
        await _context.SaveChangesAsync();

        // Act
        var result = await _sut.GetById(order.Id);

        // Assert
        result.Should().NotBeNull();
        result.Id.Should().Be(order.Id);
    }

    public async Task DisposeAsync()
    {
        await _container.DisposeAsync();
    }
}
```

---

### 任務 4：測試 NoSQL 資料庫（MongoDB、Redis）

**情境**：測試 CacheService（使用 Redis）

**推薦技能**：
- `dotnet-testing-advanced-testcontainers-nosql`

**適用條件**：
- 使用 MongoDB、Redis、Elasticsearch
- 需要測試 NoSQL 特定功能

**實施步驟**：
1. 設定 Testcontainers.Redis
2. 測試快取邏輯
3. 驗證過期時間
4. 測試快取失效

**提示詞範例**：
```
請使用 dotnet-testing-advanced-testcontainers-nosql skill
為我的 CacheService 建立測試。Service 使用 Redis 做快取。
需要測試 Set、Get、Remove 以及過期時間。
```

**預期測試涵蓋**：
- ✅ Set 成功儲存資料
- ✅ Get 成功取得資料
- ✅ Get 不存在的鍵回傳 null
- ✅ 過期時間正確運作
- ✅ Remove 成功移除資料

---

### 任務 5：測試微服務架構（.NET Aspire）

**情境**：測試 .NET Aspire 微服務專案

**推薦技能**：
- `dotnet-testing-advanced-aspire-testing`

**適用條件**：
- 使用 .NET Aspire
- 多服務協作
- 分散式應用

**實施步驟**：
1. 建立 DistributedApplication 測試
2. 設定服務依賴
3. 測試服務間通訊
4. 驗證完整流程

**提示詞範例**：
```
請使用 dotnet-testing-advanced-aspire-testing skill
為我的 .NET Aspire 專案建立測試。專案包含 API Service 和 Worker Service。
需要測試兩個服務的協作。
```

---

### 任務 6：升級 xUnit 到 3.x

**情境**：現有專案使用 xUnit 2.9.x，想升級到 3.x

**推薦技能**：
- `dotnet-testing-advanced-xunit-upgrade-guide`

**實施步驟**：
1. 了解重大變更
2. 更新套件版本
3. 處理相容性問題
4. 驗證測試執行

**提示詞範例**：
```
請使用 dotnet-testing-advanced-xunit-upgrade-guide skill
協助我升級專案中的 xUnit 到 3.x 版本。目前使用 2.9.2。
```

---

### 任務 7：評估是否遷移到 TUnit

**情境**：考慮從 xUnit 遷移到 TUnit

**推薦技能**：
1. `dotnet-testing-advanced-tunit-fundamentals`（了解基礎）
2. `dotnet-testing-advanced-tunit-advanced`（評估進階功能）

**實施步驟**：
1. 了解 TUnit 與 xUnit 差異
2. 評估遷移成本
3. 試驗性遷移一個測試檔案
4. 決定是否全面遷移

**提示詞範例**：
```
請使用 dotnet-testing-advanced-tunit-fundamentals skill
評估是否應將專案從 xUnit 遷移到 TUnit。專案目前有 500+ 測試。
```

---

## 整合測試層級對應

根據專案複雜度，選擇適合的測試策略：

### Level 1：簡單的 WebApi 專案

**專案特徵**：
- 簡單的 CRUD API
- 無外部依賴或使用記憶體實作
- 業務邏輯簡單

**推薦技能**：
- `dotnet-testing-advanced-aspnet-integration-testing`

**測試重點**：
- 路由驗證
- 模型綁定
- HTTP 回應
- 基本業務邏輯

**範例專案**：
- TodoList API
- 簡單的產品目錄

---

### Level 2：相依 Service 的 WebApi 專案

**專案特徵**：
- 有業務邏輯層（Services）
- 依賴外部服務（可以 Mock）
- 中等複雜度

**推薦技能組合**：
1. `dotnet-testing-advanced-aspnet-integration-testing`（基礎）
2. `dotnet-testing-nsubstitute-mocking`（模擬依賴）

**測試策略**：
- 使用 NSubstitute 建立 Service stub
- 測試 Controller 與 Service 的互動
- 驗證錯誤處理

**範例專案**：
- 電商 API（有庫存、訂單服務）
- CMS 系統

---

### Level 3：完整的 WebApi 專案

**專案特徵**：
- 複雜的業務邏輯
- 需要真實資料庫
- 可能有外部 API 整合
- 完整的錯誤處理

**推薦技能組合**：
1. `dotnet-testing-advanced-webapi-integration-testing`（完整流程）
2. `dotnet-testing-advanced-testcontainers-database`（真實資料庫）
3. `dotnet-testing-advanced-testcontainers-nosql`（如有使用 NoSQL）

**測試策略**：
- 使用 Testcontainers 建立真實資料庫
- 完整的端到端測試
- 測試資料準備與清理
- 驗證所有錯誤情境

**範例專案**：
- 大型電商平台
- 企業級管理系統
- SaaS 應用

---

## 學習路徑建議

### 整合測試入門（1 週）

**目標**：掌握整合測試基礎，能為 Web API 建立測試

#### Day 1-2：基礎整合測試

**技能**：`dotnet-testing-advanced-aspnet-integration-testing`

**學習重點**：
- WebApplicationFactory 概念
- TestServer 使用
- HTTP 回應驗證
- 記憶體資料庫配置

**實作練習**：
- 為簡單的 API 建立整合測試
- 測試 GET、POST 端點

---

#### Day 3-4：完整 WebAPI 測試

**技能**：`dotnet-testing-advanced-webapi-integration-testing`

**學習重點**：
- 完整 CRUD 測試
- 測試基底類別設計
- 資料準備與清理
- 錯誤處理驗證

**實作練習**：
- 為完整的 Controller 建立測試
- 實作測試資料管理

---

#### Day 5-6：容器化資料庫測試

**技能**：`dotnet-testing-advanced-testcontainers-database`

**學習重點**：
- Testcontainers 概念
- SQL Server 容器設定
- 資料庫遷移執行
- 測試隔離

**實作練習**：
- 為 Repository 建立測試
- 使用真實資料庫

---

#### Day 7：NoSQL 資料庫測試

**技能**：`dotnet-testing-advanced-testcontainers-nosql`

**學習重點**：
- MongoDB 容器設定
- Redis 容器設定
- NoSQL 特定測試模式

**實作練習**：
- 測試 MongoDB Repository
- 測試 Redis Cache Service

---

### 微服務測試專精（3-5 天）

**前置條件**：完成整合測試入門

**技能**：`dotnet-testing-advanced-aspire-testing`

**學習重點**：
- .NET Aspire 架構理解
- DistributedApplication 測試
- 服務依賴管理
- 分散式測試策略

**實作練習**：
- 測試 Aspire 微服務專案
- 驗證服務間通訊

---

### 框架遷移路徑（依需求）

#### xUnit 升級（1-2 天）

**技能**：`dotnet-testing-advanced-xunit-upgrade-guide`

**學習重點**：
- xUnit 3.x 新特性
- 重大變更處理
- 升級步驟
- 相容性測試

**實施步驟**：
1. 了解版本差異
2. 更新套件
3. 處理編譯錯誤
4. 驗證測試執行

---

#### TUnit 遷移（2-5 天）

**基礎（2-3 天）**
技能：`dotnet-testing-advanced-tunit-fundamentals`

**學習重點**：
- TUnit 核心概念
- 與 xUnit 對比
- 基本測試撰寫
- 遷移建議

---

**進階（2-3 天）**
技能：`dotnet-testing-advanced-tunit-advanced`

**學習重點**：
- 資料驅動測試
- 依賴注入
- 平行執行控制
- 進階特性

---

## 技能組合建議

根據不同的專案需求，推薦以下技能組合：

### 組合 1：完整 API 測試專案

**適合**：建立正式專案的完整測試套件

**技能組合**：
1. `dotnet-testing-advanced-aspnet-integration-testing`（基礎）
2. `dotnet-testing-advanced-testcontainers-database`（真實資料庫）
3. `dotnet-testing-advanced-webapi-integration-testing`（完整流程）

**學習順序**：
1. 先學 aspnet-integration-testing 理解基礎
2. 再學 testcontainers-database 掌握資料庫測試
3. 最後學 webapi-integration-testing 整合應用

**預期成果**：
- 能為 Web API 專案建立完整測試
- 使用真實資料庫驗證行為
- 測試所有 CRUD 端點與錯誤處理

---

### 組合 2：微服務測試方案

**適合**：微服務架構、分散式系統

**技能組合**：
1. `dotnet-testing-advanced-aspire-testing`（核心）
2. `dotnet-testing-advanced-testcontainers-database`（資料庫）
3. `dotnet-testing-advanced-testcontainers-nosql`（NoSQL）

**學習順序**：
1. 先學 testcontainers（資料庫測試基礎）
2. 再學 aspire-testing（微服務測試）

**預期成果**：
- 測試 .NET Aspire 專案
- 驗證服務間通訊
- 使用容器化環境測試

---

### 組合 3：框架現代化

**適合**：測試框架升級或遷移

#### 選項 A：xUnit 升級
**技能**：
- `dotnet-testing-advanced-xunit-upgrade-guide`

**適合**：
- 現有專案使用 xUnit 2.x
- 想升級到最新版本

---

#### 選項 B：TUnit 遷移
**技能組合**：
1. `dotnet-testing-advanced-tunit-fundamentals`（基礎）
2. `dotnet-testing-advanced-tunit-advanced`（進階）

**適合**：
- 新專案選擇測試框架
- 考慮從 xUnit 遷移

**學習順序**：
1. 先學 fundamentals 了解基礎
2. 再學 advanced 掌握進階功能

---

## 前置技能要求

學習進階技能前，建議先掌握以下基礎技能（來自 `dotnet-testing` 基礎技能集）：

### 必備技能

#### 1. dotnet-testing-unit-test-fundamentals
**為什麼必須**：
- 整合測試也遵循 3A Pattern
- FIRST 原則同樣適用
- 需要理解測試基礎概念

---

#### 2. dotnet-testing-xunit-project-setup
**為什麼必須**：
- 需要建立測試專案
- 理解專案結構
- 了解套件管理

---

#### 3. dotnet-testing-awesome-assertions-guide
**為什麼必須**：
- 整合測試需要驗證 HTTP 回應
- FluentAssertions.Web 提供強大的 API 斷言
- 提升測試可讀性

---

### 推薦技能

#### 1. dotnet-testing-nsubstitute-mocking
**為什麼推薦**：
- 整合測試中可能需要 Mock 外部服務
- WebApplicationFactory 需要替換服務

---

#### 2. dotnet-testing-autofixture-basics
**為什麼推薦**：
- 快速產生測試資料
- 減少整合測試的樣板程式碼

---

## 引導對話範例

以下範例展示 AI 如何與您互動，幫助您選擇正確的進階技能。

### 範例 1：API 測試需求

**您**：我想測試 Web API

**AI**：我會協助您建立 Web API 測試！請先確認您的測試需求：

**1. API 複雜度**：
- [ ] 簡單的 API（幾個端點）
- [ ] 中型 API（完整的 CRUD）
- [ ] 複雜 API（多層架構、複雜業務邏輯）

**2. 資料庫需求**：
- [ ] 不需要資料庫
- [ ] 記憶體資料庫即可
- [ ] 需要真實資料庫

**3. 資料庫類型**（如需要真實資料庫）：
- [ ] SQL Server / PostgreSQL / MySQL
- [ ] MongoDB / Redis / Elasticsearch
- [ ] 兩者都有

請告訴我您的選擇，我會推薦適合的技能組合。

---

**您**：中型 API，需要真實的 SQL Server 資料庫

**AI**：完美！根據您的需求，我推薦以下技能組合：

**第一步：學習基礎整合測試（1-2 天）**
`dotnet-testing-advanced-aspnet-integration-testing`
- 理解 WebApplicationFactory
- 學習 HTTP 測試基礎

**第二步：加入真實資料庫（2 天）**
`dotnet-testing-advanced-testcontainers-database`
- 使用 Testcontainers 設定 SQL Server
- 學習資料庫測試隔離

**第三步：完整流程測試（2-3 天）**
`dotnet-testing-advanced-webapi-integration-testing`
- 實作完整的 CRUD 測試
- 測試資料管理策略
- 錯誤處理驗證

**預期成果**：
完成後您將能夠為 API 專案建立完整的整合測試套件，使用真實的 SQL Server 資料庫驗證行為。

需要我使用這些 skills 協助您開始嗎？

---

### 範例 2：微服務測試

**您**：我的專案是 .NET Aspire 微服務架構，要怎麼測試？

**AI**：.NET Aspire 微服務測試需要特殊的方法！我推薦使用 `dotnet-testing-advanced-aspire-testing` skill。

**前置確認**：
1. 您已安裝 .NET Aspire Workload？
   - 如果沒有：`dotnet workload install aspire`

2. 您的專案有哪些服務？
   - API Service
   - Worker Service
   - 其他服務

3. 是否使用資料庫？
   - 如果有，我們會搭配 `dotnet-testing-advanced-testcontainers-database`

**測試重點**：
- DistributedApplication 測試
- 服務間通訊驗證
- 依賴服務管理
- 端到端流程測試

需要我使用 `dotnet-testing-advanced-aspire-testing` skill 協助您建立測試嗎？

---

### 範例 3：框架升級

**您**：我的專案使用 xUnit 2.9，應該升級到 3.x 嗎？

**AI**：這是個好問題！我會協助您評估。讓我先了解您的情況：

**1. 升級動機**：
- [ ] 需要 xUnit 3.x 的新功能
- [ ] 解決已知問題
- [ ] 只是想跟上最新版本
- [ ] 其他原因

**2. 專案規模**：
- [ ] 小型（< 100 個測試）
- [ ] 中型（100-500 個測試）
- [ ] 大型（> 500 個測試）

**3. 升級時程壓力**：
- [ ] 不急，可以慢慢遷移
- [ ] 需要儘快完成

---

**您**：中型專案，主要是想跟上最新版本，不急

**AI**：了解！我推薦使用 `dotnet-testing-advanced-xunit-upgrade-guide` skill。

**升級計劃**：

**階段 1：了解差異（1 天）**
- 閱讀重大變更清單
- 了解哪些功能受影響
- 評估遷移工作量

**階段 2：準備升級（半天）**
- 備份目前程式碼
- 更新 .csproj 套件版本
- 檢查編譯錯誤

**階段 3：處理相容性（1-2 天）**
- 修正編譯錯誤
- 處理執行階段問題
- 驗證所有測試通過

**總工時估計**：2-3 天

**風險評估**：⭐⭐ 中低
xUnit 3.x 升級通常很順利，大部分變更都有向後相容。

需要我使用 `dotnet-testing-advanced-xunit-upgrade-guide` skill 協助您開始升級嗎？

---

### 範例 4：TUnit 評估

**您**：我聽說 TUnit 很不錯，應該遷移嗎？

**AI**：TUnit 確實是很有潛力的測試框架！讓我協助您評估。

**TUnit 主要優勢**：
1. ⚡ **更好的效能**：平行執行優化
2. 💉 **原生依賴注入**：不需要額外設定
3. 🎯 **現代化 API**：更直覺的設計
4. 🔧 **靈活性**：更多自訂選項

**評估重點**：

**1. 專案狀況**：
- 新專案 → 可以考慮直接使用 TUnit
- 現有專案 → 需評估遷移成本

**2. 團隊技能**：
- 團隊對 xUnit 熟悉度
- 學習新框架的意願

**3. 遷移成本**：
- 測試數量
- 特殊測試模式（如 Theory、ClassFixture 等）

**我的建議**：

**如果是新專案**：
使用 `dotnet-testing-advanced-tunit-fundamentals` skill 了解 TUnit，考慮直接採用。

**如果是現有專案**：
1. 先用 `dotnet-testing-advanced-tunit-fundamentals` 了解基礎
2. 試驗性遷移一個測試檔案
3. 評估實際遷移工作量
4. 決定是否全面遷移

需要我協助您評估嗎？

---

## 與基礎技能的關係

進階技能建立在基礎技能之上：

**基礎測試能力** → `dotnet-testing`（基礎技能集）
- 單元測試基礎
- 測試資料生成
- 斷言與模擬
- 特殊場景處理

**↓ 進階應用**

**進階整合測試** → `dotnet-testing-advanced`（本技能集）
- Web API 整合測試
- 容器化測試
- 微服務測試
- 框架升級

**學習建議**：
先完成 `dotnet-testing` 基礎技能集的核心技能，再進入本進階技能集。

---

## 相關資源

### 原始資料來源

- **iThome 鐵人賽系列文章**：[老派軟體工程師的測試修練 - 30 天挑戰](https://ithelp.ithome.com.tw/users/20066083/ironman/8276)
  🏆 2025 iThome 鐵人賽 Software Development 組冠軍

- **完整範例程式碼**：[30Days_in_Testing_Samples](https://github.com/kevintsengtw/30Days_in_Testing_Samples)
  包含所有範例專案的可執行程式碼

### 技術需求

**整合測試技能**：
- .NET 8+
- Docker Desktop
- WSL2（Windows 環境）

**Aspire 測試技能**：
- .NET 8+
- .NET Aspire Workload
- Docker Desktop

---

## 下一步

選擇符合您需求的進階技能開始學習，或告訴我您的具體情況，我會推薦最適合的學習路徑！

**快速開始**：
- 想測試 API → 從 `dotnet-testing-advanced-aspnet-integration-testing` 開始
- 需要真實資料庫 → 從 `dotnet-testing-advanced-testcontainers-database` 開始
- 微服務專案 → 使用 `dotnet-testing-advanced-aspire-testing`
- 框架升級 → 使用對應的升級指南
- 不確定 → 告訴我您的專案情況，我會幫您分析
