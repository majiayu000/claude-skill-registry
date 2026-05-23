---
name: errors
description: |
  設計一致的錯誤碼，遵循 PREFIX_CATEGORY_NUMBER 格式。
  使用時機：定義錯誤碼、建立錯誤處理、設計 API。
  關鍵字：error code, error handling, error format, API errors, 錯誤碼, 錯誤處理。
source: ../../../../skills/error-code-guide/SKILL.md
source_version: 1.0.0
translation_version: 1.0.0
last_synced: 2026-01-08
status: current
---

# 錯誤碼指南

> **語言**: [English](../../../../skills/error-code-guide/SKILL.md) | 繁體中文

**版本**: 1.0.0
**最後更新**: 2025-12-30
**適用範圍**: Claude Code Skills

---

## 目的

此技能幫助設計一致的錯誤碼，遵循標準格式，實現更好的除錯、監控和使用者體驗。

## 快速參考

### 錯誤碼格式

```
<前綴>_<類別>_<編號>
```

| 元素 | 說明 | 範例 |
|------|------|------|
| 前綴 (PREFIX) | 應用/服務識別碼 | AUTH, PAY, USR |
| 類別 (CATEGORY) | 錯誤類別 | VAL, SYS, BIZ |
| 編號 (NUMBER) | 唯一數字識別碼 | 001, 100, 404 |

### 範例

```
AUTH_VAL_001    → 認證驗證錯誤
PAY_SYS_503     → 付款系統無法使用
USR_BIZ_100     → 使用者商業規則違規
API_NET_408     → API 網路逾時
```

### 錯誤類別

| 類別 | 全名 | 說明 | HTTP 狀態碼 |
|------|------|------|-------------|
| **VAL** | Validation | 客戶端輸入驗證失敗 | 400 |
| **BIZ** | Business | 商業規則違規 | 422 |
| **SYS** | System | 內部系統錯誤 | 500 |
| **NET** | Network | 通訊錯誤 | 502/503/504 |
| **AUTH** | Auth | 安全相關錯誤 | 401/403 |

### 類別編號範圍

| 範圍 | 說明 | 範例 |
|------|------|------|
| *_VAL_001-099 | 欄位驗證 | 缺少必填欄位 |
| *_VAL_100-199 | 格式驗證 | 電子郵件格式無效 |
| *_VAL_200-299 | 約束驗證 | 密碼太短 |
| *_BIZ_001-099 | 狀態違規 | 訂單已取消 |
| *_BIZ_100-199 | 規則違規 | 超過 30 天無法退貨 |
| *_BIZ_200-299 | 限制違規 | 超過每日限制 |
| *_AUTH_001-099 | 認證 | 帳號密碼錯誤 |
| *_AUTH_100-199 | 授權 | 權限不足 |
| *_AUTH_200-299 | Token/Session | Token 已過期 |

## HTTP 狀態碼對應

| 類別 | HTTP 狀態碼 | 說明 |
|------|-------------|------|
| VAL | 400 | Bad Request |
| BIZ | 422 | Unprocessable Entity |
| AUTH (001-099) | 401 | Unauthorized |
| AUTH (100-199) | 403 | Forbidden |
| SYS | 500 | Internal Server Error |
| NET | 502/503/504 | Gateway errors |

## 詳細指南

完整標準請參考：
- [錯誤碼標準](../../core/error-code-standards.md)

### AI 優化格式（節省 Token）

AI 助手可使用 YAML 格式檔案以減少 Token 使用量：
- 基礎標準：`ai/standards/error-codes.ai.yaml`

## 錯誤回應格式

### 單一錯誤

```json
{
  "success": false,
  "error": {
    "code": "AUTH_VAL_001",
    "message": "電子郵件為必填欄位",
    "field": "email",
    "requestId": "req_abc123"
  }
}
```

### 多個錯誤

```json
{
  "success": false,
  "errors": [
    {
      "code": "AUTH_VAL_001",
      "message": "電子郵件為必填欄位",
      "field": "email"
    },
    {
      "code": "AUTH_VAL_201",
      "message": "密碼至少需要 8 個字元",
      "field": "password"
    }
  ],
  "requestId": "req_abc123"
}
```

## 內部錯誤物件

```typescript
interface ApplicationError {
  // 核心欄位
  code: string;          // "AUTH_VAL_001"
  message: string;       // 技術訊息（用於日誌）

  // 使用者介面
  userMessage: string;   // 本地化使用者訊息
  userMessageKey: string; // i18n 鍵值: "error.auth.val.001"

  // 上下文
  field?: string;        // 相關欄位: "email"
  details?: object;      // 附加資訊

  // 除錯
  timestamp: string;     // ISO 8601
  requestId: string;     // 關聯 ID
}
```

## 國際化 (i18n)

### 訊息鍵值格式

```
error.<前綴>.<類別>.<編號>
```

### 翻譯檔案範例

```yaml
# en.yaml
error:
  auth:
    val:
      001: "Email is required"
      101: "Invalid email format"
    auth:
      001: "Invalid credentials"

# zh-TW.yaml
error:
  auth:
    val:
      001: "電子郵件為必填欄位"
      101: "電子郵件格式無效"
    auth:
      001: "帳號或密碼錯誤"
```

## 範例

### ✅ 良好的錯誤碼

```javascript
AUTH_VAL_001  // 缺少必填欄位: email
AUTH_VAL_101  // 電子郵件格式無效
ORDER_BIZ_001 // 訂單已取消
ORDER_BIZ_201 // 超過每日購買限制
DB_SYS_001    // 資料庫查詢失敗
SEC_AUTH_001  // 帳號密碼錯誤
SEC_AUTH_201  // Token 已過期
```

### ❌ 不良的錯誤碼

```javascript
ERR_001       // 太模糊，沒有前綴或類別
INVALID       // 不具描述性
error         // 不是錯誤碼
AUTH_ERROR    // 缺少編號
```

## 檢查清單

- [ ] 每個錯誤有唯一代碼
- [ ] 類別符合錯誤類型
- [ ] 使用者訊息已本地化
- [ ] HTTP 狀態碼正確
- [ ] 錯誤已記錄文件
- [ ] 代碼已加入註冊表

---

## 設定偵測

此技能支援專案特定設定。

### 偵測順序

1. 檢查程式碼庫中現有的錯誤碼模式
2. 檢查 `CONTRIBUTING.md` 中的錯誤碼指南
3. 若無找到，**預設使用 PREFIX_CATEGORY_NUMBER 格式**

### 首次設定

若未找到錯誤碼標準：

1. 建議：「此專案尚未設定錯誤碼標準。您要建立錯誤碼註冊表嗎？」
2. 建議建立 `errors/registry.ts`：

```typescript
export const ErrorCodes = {
  AUTH_VAL_001: {
    code: 'AUTH_VAL_001',
    httpStatus: 400,
    messageKey: 'error.auth.val.001',
    description: '電子郵件欄位為必填',
  },
  // ... 更多錯誤碼
} as const;
```

---

## 相關標準

- [錯誤碼標準](../../core/error-code-standards.md)
- [日誌標準](../../core/logging-standards.md)

---

## 版本歷史

| 版本 | 日期 | 變更 |
|------|------|------|
| 1.0.0 | 2025-12-30 | 初始發布 |

---

## 授權

此技能採用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) 授權。

**來源**: [universal-dev-standards](https://github.com/AsiaOstrich/universal-dev-standards)
