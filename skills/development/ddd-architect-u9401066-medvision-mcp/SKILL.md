---
name: ddd-architect
description: 確保前後端程式碼遵循 DDD 架構與 DAL 分離原則。
---

---
name: ddd-architect
description: Ensure code follows DDD architecture and DAL separation for both frontend and backend. Triggers: DDD, arch, 架構, 新功能, 新模組, new feature, scaffold, 骨架, domain, layer, 分層, structure, 結構, backend, frontend, React, Vue, Python, TypeScript, 前端, 後端, component, 元件.
version: 2.1.0
category: architecture
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies: []
allowed-tools:
  - read_file
  - write_file
  - create_file
  - create_directory
  - list_dir
  - grep_search
  - semantic_search
---

# DDD 架構輔助技能

## 描述
確保前後端程式碼遵循 DDD 架構與 DAL 分離原則。

## 觸發條件
- 「建立新功能」「新增模組」
- 「架構檢查」
- 建立新檔案時自動檢查
- 「前端架構」「後端架構」

## 法規依據
- 憲法：CONSTITUTION.md 第 1、2 條
- 子法：.github/bylaws/ddd-architecture.md

---

## 🔧 後端 DDD 結構 (Python/Go/Rust)

### 新功能腳手架
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

### 層級職責

| 層級 | 職責 | 可依賴 |
|------|------|--------|
| **Domain** | 業務規則、Entity、Value Object | 無外部依賴 |
| **Application** | Use Case、DTO、編排 | Domain |
| **Infrastructure** | Repository 實作、外部 API | Domain |
| **Presentation** | API、CLI、UI | Application |

---

## ⚛️ 前端 DDD 結構 (React/Vue)

### React 專案結構

```
「新增 User 管理功能 (React)」

生成：
src/
├── domain/
│   ├── models/
│   │   └── User.ts              # Entity 類型定義
│   ├── types/
│   │   └── UserTypes.ts         # Value Object 類型
│   └── rules/
│       └── userValidation.ts    # 純業務規則（無框架依賴）
│
├── application/
│   ├── hooks/
│   │   └── useUser.ts           # 業務邏輯 Hook
│   ├── stores/
│   │   └── userStore.ts         # 狀態管理 (Zustand/Redux)
│   └── services/
│       └── UserService.ts       # 應用服務（編排）
│
├── infrastructure/
│   ├── api/
│   │   └── userApi.ts           # API Client (fetch/axios)
│   ├── storage/
│   │   └── userStorage.ts       # LocalStorage/SessionStorage
│   └── adapters/
│       └── userAdapter.ts       # API Response → Domain Model
│
└── presentation/
    ├── components/
    │   └── UserCard.tsx         # UI 元件
    ├── pages/
    │   └── UserListPage.tsx     # 頁面
    └── layouts/
        └── UserLayout.tsx       # 佈局
```

### Vue 3 專案結構

```
「新增 Product 管理功能 (Vue)」

生成：
src/
├── domain/
│   ├── models/
│   │   └── Product.ts
│   ├── types/
│   │   └── ProductTypes.ts
│   └── rules/
│       └── productValidation.ts
│
├── application/
│   ├── composables/
│   │   └── useProduct.ts        # Composition API
│   ├── stores/
│   │   └── productStore.ts      # Pinia Store
│   └── services/
│       └── ProductService.ts
│
├── infrastructure/
│   ├── api/
│   │   └── productApi.ts
│   └── adapters/
│       └── productAdapter.ts
│
└── presentation/
    ├── components/
    │   └── ProductCard.vue
    ├── views/
    │   └── ProductListView.vue
    └── layouts/
        └── ProductLayout.vue
```

### 前端層級對照

| 層級 | React | Vue 3 | 職責 |
|------|-------|-------|------|
| **Domain** | models/, types/, rules/ | 同左 | 純 TypeScript，無框架 |
| **Application** | hooks/, stores/ | composables/, stores/ | 業務邏輯封裝 |
| **Infrastructure** | api/, adapters/ | 同左 | 外部服務對接 |
| **Presentation** | components/, pages/ | components/, views/ | UI 元件 |

---

## 🔍 架構違規檢查

### 後端違規

偵測並警告：
- ❌ Domain 層導入 Infrastructure
- ❌ 直接在 Domain 操作資料庫
- ❌ Application 層直接操作資料庫
- ❌ Repository 實作放在 Domain 層

### 前端違規

偵測並警告：
- ❌ Domain 層導入 React/Vue（應為純 TypeScript）
- ❌ 元件直接呼叫 API（應透過 hooks/composables）
- ❌ 將業務邏輯寫在元件內
- ❌ API Response 直接用於 UI（應經過 adapter 轉換）

### 依賴方向驗證

```
✅ Presentation → Application → Domain
✅ Infrastructure → Domain (實作介面)
❌ Domain → Infrastructure
❌ Domain → Application
❌ Domain → React/Vue/框架
```

---

## 📋 檢查範本

### 後端輸出

```
🏗️ DDD 架構檢查 (Backend)

✅ 依賴方向正確
✅ DAL 正確分離
⚠️ 警告：
  - src/Domain/Services/UserService.py:15
    導入了 Infrastructure 模組

建議：
  將資料庫操作移至 Repository
```

### 前端輸出

```
🏗️ DDD 架構檢查 (Frontend - React)

✅ Domain 層無框架依賴
✅ API 呼叫正確封裝於 infrastructure/
⚠️ 警告：
  - src/presentation/components/UserCard.tsx:23
    直接呼叫 fetch()，應使用 useUser hook

建議：
  將 API 呼叫移至 src/application/hooks/useUser.ts
```

---

## 🎯 快速生成指令

```
「建立後端 Order 領域」    → 生成 Python DDD 結構
「建立前端 User 功能」     → 詢問 React/Vue，生成對應結構
「架構檢查」               → 掃描全專案違規
「前端架構檢查」           → 僅掃描前端
```
