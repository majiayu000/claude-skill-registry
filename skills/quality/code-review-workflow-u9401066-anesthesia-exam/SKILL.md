---
name: code-review-workflow
description: 完整的 PR/MR 審查流程，整合自動化檢查和多維度審查。
---

---
name: code-review-workflow
description: Complete code review workflow for PR/MR with multiple reviewers and automated checks. Triggers: PRW, 審查流程, review workflow, PR review, MR review, pull request, merge request, 程式碼審查流程, full review, 完整審查.
version: 1.0.0
category: workflow
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
orchestrates:
  - code-reviewer
  - security-reviewer
  - test-generator
  - ddd-architect
allowed-tools:
  - read_file
  - grep_search
  - semantic_search
  - get_errors
  - get_changed_files
  - run_in_terminal
---

# 程式碼審查工作流

## 描述

完整的 PR/MR 審查流程，整合自動化檢查和多維度審查。

## 觸發條件

- 「審查 PR」「review PR」「審查流程」
- 「PRW: [PR 連結或分支]」

---

## 🔍 審查流程

```
┌─────────────────────────────────────────────────────────────┐
│                Code Review Workflow                          │
├─────────────────────────────────────────────────────────────┤
│  Phase 1: 📋 概覽 (Overview)                                 │
│  ├─ 列出變更檔案                                             │
│  ├─ 統計變更行數                                             │
│  └─ 識別變更範圍                                             │
├─────────────────────────────────────────────────────────────┤
│  Phase 2: 🤖 自動化檢查 (Automated)                          │
│  ├─ 靜態分析 (ruff, mypy)                                   │
│  ├─ 死碼檢測 (vulture)                                       │
│  ├─ 安全掃描 (bandit)                                        │
│  └─ 測試執行                                                 │
├─────────────────────────────────────────────────────────────┤
│  Phase 3: 🏗️ 架構審查 (Architecture)                        │
│  ├─ [ddd-architect] DDD 合規檢查                            │
│  ├─ 依賴方向驗證                                             │
│  └─ 模組化評估                                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 4: 🔒 安全審查 (Security)                             │
│  ├─ [security-reviewer] OWASP 檢查                          │
│  ├─ 敏感資料偵測                                             │
│  └─ 認證/授權審查                                            │
├─────────────────────────────────────────────────────────────┤
│  Phase 5: 📝 程式碼審查 (Code)                               │
│  ├─ [code-reviewer] 品質審查                                │
│  ├─ 可讀性評估                                               │
│  ├─ 效能考量                                                 │
│  └─ 測試覆蓋率                                               │
├─────────────────────────────────────────────────────────────┤
│  Phase 6: 📊 總結 (Summary)                                  │
│  ├─ 生成審查報告                                             │
│  ├─ 建議修改項目                                             │
│  └─ 批准/請求修改                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 使用範例

### 基本用法

```
「審查 PR」

AI 執行：
1. 📋 取得變更檔案列表
2. 🤖 執行自動化檢查
3. 🏗️ 驗證 DDD 架構
4. 🔒 執行安全審查
5. 📝 逐檔案程式碼審查
6. 📊 生成審查報告
```

### 指定檔案

```
「PRW: 審查 src/auth/ 目錄的變更」

AI 執行：
1. 僅審查指定目錄
2. 重點關注認證相關安全問題
```

---

## 📊 輸出格式

```markdown
## 📋 程式碼審查報告

### 變更概覽

| 項目 | 數量 |
|------|------|
| 變更檔案 | 8 |
| 新增行數 | +245 |
| 刪除行數 | -32 |
| 測試檔案 | 3 |

### 🤖 自動化檢查

| 檢查項目 | 狀態 | 詳情 |
|----------|------|------|
| ruff lint | ✅ | 0 issues |
| mypy | ⚠️ | 2 warnings |
| vulture | ✅ | 0 dead code |
| bandit | ✅ | 0 security issues |
| pytest | ✅ | 42/42 passed |

### 🏗️ 架構審查

- ✅ DDD 層級正確分離
- ✅ 依賴方向符合規範
- ⚠️ `UserService` 建議拆分 (180 行)

### 🔒 安全審查

- ✅ 無 OWASP Top 10 風險
- ✅ 無硬編碼敏感資料
- ⚠️ 建議加入 rate limiting

### 📝 程式碼審查

#### 必須修改 (Blocking)
1. **src/auth/service.py:45**
   - 問題：缺少 None 檢查
   - 建議：加入防禦性檢查

#### 建議修改 (Non-blocking)
1. **src/auth/dto.py:12**
   - 問題：命名不夠清晰
   - 建議：`data` → `user_credentials`

#### 優點 (Positive)
- 測試覆蓋完整 (92%)
- 錯誤處理得當
- 文檔清楚

### 📊 總結

| 項目 | 評分 |
|------|------|
| 品質 | ⭐⭐⭐⭐ |
| 安全 | ⭐⭐⭐⭐⭐ |
| 架構 | ⭐⭐⭐⭐ |
| 測試 | ⭐⭐⭐⭐⭐ |

**結論**: 🟡 **請求修改** - 修復 1 個 blocking issue 後可合併
```

---

## ⚙️ 配置選項

| 參數 | 說明 | 預設值 |
|------|------|--------|
| `--quick` | 快速審查（僅自動化） | false |
| `--security-only` | 僅安全審查 | false |
| `--skip-tests` | 跳過測試執行 | false |
