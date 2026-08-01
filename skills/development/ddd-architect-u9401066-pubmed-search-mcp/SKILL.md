---
name: ddd-architect
description: 確保程式碼遵循 DDD 架構與 DAL 分離原則。
---

---
name: ddd-architect
description: Ensure code follows DDD architecture and DAL separation principles. Triggers: DDD, arch, 架構, 新功能, 新模組, new feature, scaffold, 骨架, domain.
---

# DDD 架構輔助技能

## 描述
確保程式碼遵循 DDD 架構與 DAL 分離原則。

## 觸發條件
- 「建立新功能」「新增模組」
- 「架構檢查」
- 建立新檔案時自動檢查

## 法規依據
- 憲法：CONSTITUTION.md 第 1、2 條
- 子法：.github/bylaws/ddd-architecture.md

## 功能

### 1. 新功能腳手架
當建立新功能時，自動生成 DDD 結構：

```
「新增 Order 領域」

生成：
src/
├── Domain/
│   ├── Entities/Order.py
│   ├── ValueObjects/OrderId.py
│   ├── Aggregates/OrderAggregate.py
│   └── Repositories/IOrderRepository.py
├── Application/
│   ├── UseCases/CreateOrder.py
│   └── DTOs/OrderDTO.py
└── Infrastructure/
    └── Persistence/Repositories/OrderRepository.py
```

### 2. 架構違規檢查

偵測並警告：
- ❌ Domain 層導入 Infrastructure
- ❌ 直接在 Domain 操作資料庫
- ❌ Application 層直接操作資料庫
- ❌ Repository 實作放在 Domain 層

### 3. 依賴方向驗證

```
✅ Presentation → Application → Domain
✅ Infrastructure → Domain (實作介面)
❌ Domain → Infrastructure
❌ Domain → Application
```

## 輸出格式

```
🏗️ DDD 架構檢查

✅ 依賴方向正確
✅ DAL 正確分離
⚠️ 警告：
  - src/Domain/Services/UserService.py:15
    導入了 Infrastructure 模組

建議：
  將資料庫操作移至 Repository
```
