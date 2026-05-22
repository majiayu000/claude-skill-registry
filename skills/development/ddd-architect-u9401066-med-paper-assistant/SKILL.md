---
name: ddd-architect
description: DDD 架構輔助與檢查。觸發：架構、新功能、新模組、domain、structure。
---

# DDD 架構輔助技能

## 觸發條件

| 用戶說法 | 觸發 |
|----------|------|
| 新增功能、新模組 | ✅ |
| 架構檢查、設計 | ✅ |
| 建立新檔案時 | ✅ 自動檢查 |

---

## 可用工具

此技能使用標準檔案操作：

| 操作 | 工具 |
|------|------|
| 搜尋 import | `grep_search(query="from.*import", isRegexp=True)` |
| 檢查目錄 | `list_dir()` |
| 讀取檔案 | `read_file()` |
| 建立檔案 | `create_file()` |

---

## DDD 層級結構

```
src/
├── domain/           # 領域層（核心業務邏輯）
│   ├── entities/     # 實體
│   ├── value_objects/# 值物件
│   ├── aggregates/   # 聚合根
│   ├── repositories/ # Repository 介面（抽象）
│   └── services/     # 領域服務
├── application/      # 應用層
│   ├── use_cases/    # 用例
│   └── dtos/         # 資料傳輸物件
├── infrastructure/   # 基礎設施層
│   ├── persistence/  # 資料庫實作
│   └── services/     # 外部服務實作
└── interfaces/       # 介面層
    ├── api/          # REST API
    └── mcp/          # MCP Server
```

---

## 依賴規則

```
✅ 允許的依賴方向：
Presentation → Application → Domain
Infrastructure → Domain (實作介面)

❌ 禁止的依賴：
Domain → Infrastructure
Domain → Application
Application → Presentation
```

---

## 標準工作流程

### 流程 A：建立新功能腳手架

```python
# 「新增 Order 領域」

# 1. 建立 Domain 層
create_file("src/domain/entities/order.py", "class Order: ...")
create_file("src/domain/repositories/order_repository.py", "class IOrderRepository(ABC): ...")

# 2. 建立 Application 層
create_file("src/application/use_cases/create_order.py", "class CreateOrder: ...")
create_file("src/application/dtos/order_dto.py", "@dataclass class OrderDTO: ...")

# 3. 建立 Infrastructure 層
create_file("src/infrastructure/persistence/order_repository.py", "class OrderRepository(IOrderRepository): ...")
```

### 流程 B：架構違規檢查

```python
# 檢查 Domain 層是否導入 Infrastructure
grep_search(
    query="from.*infrastructure.*import",
    isRegexp=True,
    includePattern="**/domain/**/*.py"
)

# 如果有結果 → 違規！
```

---

## 違規類型與修復

| 違規 | 問題 | 修復 |
|------|------|------|
| Domain → Infrastructure | 領域層不應依賴基礎設施 | 使用 Repository 介面 |
| 直接 SQL 在 Domain | 資料存取應在 Infrastructure | 抽出到 Repository |
| Application → DB | 應用層不應直接操作資料庫 | 透過 Repository |

---

## 輸出範例

```
🏗️ DDD 架構檢查

✅ 依賴方向正確
✅ DAL 正確分離
⚠️ 警告：
  - src/domain/services/user_service.py:15
    導入了 infrastructure 模組

建議：
  將資料庫操作移至 Repository
```

---

## 相關技能

- `code-refactor` - 重構違規程式碼
- `code-reviewer` - 審查程式碼品質
