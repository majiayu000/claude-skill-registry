---
name: OWASP 資安模式庫
description: 基於 OWASP Top 10 2025 的可重用安全程式碼模式，供跨專案參考
version: 1.0.0
category: shared
triggers:
  - /security-patterns
  - 資安模式
  - OWASP patterns
  - 安全模式
updated: 2026-02-02
---

# OWASP 資安模式庫

> **用途**: 提供可重用的安全程式碼模式，預防 OWASP Top 10 2025 漏洞
> **適用專案**: CK_Showcase, CK_GPS, CK_Missive, CK_lvrland_Webmap, shared-modules

---

## 快速導覽

| OWASP 類別 | 模式檔案                                       | 說明           |
| ---------- | ---------------------------------------------- | -------------- |
| A01        | [access-control.md](./A01-access-control.md)   | 存取控制模式   |
| A02        | [security-config.md](./A02-security-config.md) | 安全配置模式   |
| A03        | [supply-chain.md](./A03-supply-chain.md)       | 供應鏈安全模式 |
| A04        | [cryptographic.md](./A04-cryptographic.md)     | 加密安全模式   |
| A05        | [injection.md](./A05-injection.md)             | 注入防護模式   |
| A06        | [secure-design.md](./A06-secure-design.md)     | 安全設計模式   |
| A07        | [authentication.md](./A07-authentication.md)   | 認證安全模式   |
| A08        | [integrity.md](./A08-integrity.md)             | 完整性驗證模式 |
| A09        | [logging.md](./A09-logging.md)                 | 日誌監控模式   |
| A10        | [error-handling.md](./A10-error-handling.md)   | 錯誤處理模式   |

---

## 使用方式

### 1. 新開發時參考

開發新功能時，參考對應類別的安全模式：

```
開發「用戶登入功能」→ 參考 A07-authentication.md
開發「檔案上傳功能」→ 參考 A01-access-control.md + A05-injection.md
開發「API 端點」→ 參考 A02-security-config.md + A01-access-control.md
```

### 2. 修復問題時參考

從資安管理中心收到問題通知後：

```
問題類別 A05 (Injection) → 查看 A05-injection.md 修復範例
問題類別 A03 (Supply Chain) → 查看 A03-supply-chain.md 更新依賴
```

### 3. Code Review 時檢查

```bash
# 使用自動化檢查腳本
python scripts/security-pattern-check.py --file src/api/users.py
```

---

## 跨專案整合

### 同步機制

此模式庫透過 Skills 同步機制自動同步到所有專案：

```powershell
# 從 shared-modules 同步到各專案
..\.claude\sync-skills.ps1
```

### 各專案 Security Center 整合

各專案的資安管理中心會自動讀取這些模式，提供：

- 問題修復建議連結
- 合規檢查對照表
- 程式碼範例快速參考

---

## 貢獻指南

### 新增模式

1. 在對應的類別檔案中新增模式
2. 包含：問題說明、錯誤範例、正確範例、適用情境
3. 更新此索引檔案
4. 提交 PR 並標記 `security` label

### 更新現有模式

1. 確保向後相容
2. 新增版本說明
3. 更新 `updated` 日期

---

**建立日期**: 2026-02-02
**最後更新**: 2026-02-02
**維護團隊**: 乾坤測繪資安小組
