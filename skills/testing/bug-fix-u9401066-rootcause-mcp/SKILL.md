---
name: bug-fix
description: 結構化的 Bug 修復流程，包含根因分析和回歸測試。
---

---
name: bug-fix
description: Structured bug fixing workflow with root cause analysis and regression prevention. Triggers: BF, 修 bug, fix bug, debug, 除錯, 錯誤, error, 問題, issue, 修復, fix, 故障, fault, 異常, exception, 失敗, failure, 不能用, broken, 壞掉.
version: 1.0.0
category: workflow
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
orchestrates:
  - test-generator
  - code-reviewer
  - memory-updater
  - git-precommit
allowed-tools:
  - read_file
  - write_file
  - grep_search
  - semantic_search
  - run_in_terminal
  - get_errors
  - list_code_usages
---

# Bug 修復工作流

## 描述

結構化的 Bug 修復流程，包含根因分析和回歸測試。

## 觸發條件

- 「修 bug」「fix bug」「除錯」
- 「BF: [問題描述]」

---

## 🐛 Bug 修復流程

```
┌─────────────────────────────────────────────────────────────┐
│                  Bug Fix Workflow                            │
├─────────────────────────────────────────────────────────────┤
│  Step 1: 🔍 重現 (Reproduce)                                 │
│  ├─ 確認重現步驟                                             │
│  ├─ 收集錯誤訊息/日誌                                        │
│  └─ 建立最小重現案例                                         │
├─────────────────────────────────────────────────────────────┤
│  Step 2: 🎯 定位 (Locate)                                    │
│  ├─ 分析錯誤堆疊                                             │
│  ├─ 追蹤程式碼路徑                                           │
│  └─ 識別問題根因                                             │
├─────────────────────────────────────────────────────────────┤
│  Step 3: 🧪 測試先行 (Test First)                            │
│  ├─ 撰寫失敗的測試案例                                       │
│  ├─ 確認測試能重現問題                                       │
│  └─ 這將成為回歸測試                                         │
├─────────────────────────────────────────────────────────────┤
│  Step 4: 🔧 修復 (Fix)                                       │
│  ├─ 實施修復                                                 │
│  ├─ 最小化變更範圍                                           │
│  └─ 確認測試通過                                             │
├─────────────────────────────────────────────────────────────┤
│  Step 5: ✅ 驗證 (Verify)                                    │
│  ├─ 執行完整測試套件                                         │
│  ├─ 檢查是否引入新問題                                       │
│  └─ [code-reviewer] 審查修復                                │
├─────────────────────────────────────────────────────────────┤
│  Step 6: 📝 記錄 (Document)                                  │
│  ├─ 更新 Memory Bank                                        │
│  ├─ 記錄根因分析                                             │
│  └─ 更新相關文檔                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 使用範例

### 基本用法

```
「修 bug：用戶登入時出現 500 錯誤」

AI 執行：
1. 🔍 要求提供錯誤日誌和重現步驟
2. 🎯 分析堆疊追蹤，定位問題
3. 🧪 建立失敗測試案例
4. 🔧 實施修復
5. ✅ 驗證修復
6. 📝 記錄修復過程
```

### 帶錯誤訊息

```
「BF: TypeError: 'NoneType' object is not subscriptable at line 45」

AI 執行：
1. 讀取相關檔案的第 45 行
2. 分析為什麼變數是 None
3. 建立邊界條件測試
4. 加入 None 檢查或修正邏輯
```

---

## 📊 輸出格式

```markdown
## 🐛 Bug 修復報告

### 問題描述
用戶登入時出現 500 Internal Server Error

### 根因分析
- **位置**: `src/application/services/auth_service.py:45`
- **原因**: 當 user 不存在時，直接存取 `user.password_hash` 導致 NoneType 錯誤
- **類型**: 邊界條件未處理

### 修復方案

#### 回歸測試（先撰寫）
```python
def test_login_with_nonexistent_user():
    """登入不存在的用戶應返回 401"""
    result = auth_service.login("nonexistent@test.com", "password")
    assert result.is_error
    assert result.error_code == "USER_NOT_FOUND"
```

#### 程式碼修復
```python
# Before
def login(self, email: str, password: str):
    user = self.user_repo.find_by_email(email)
    if not bcrypt.verify(password, user.password_hash):  # 💥 NoneType!
        ...

# After
def login(self, email: str, password: str):
    user = self.user_repo.find_by_email(email)
    if user is None:
        return Result.failure("USER_NOT_FOUND")
    if not bcrypt.verify(password, user.password_hash):
        ...
```

### 驗證結果
- ✅ 回歸測試通過
- ✅ 原有測試套件通過 (42/42)
- ✅ 無新增 lint 錯誤

### 預防措施
- 類似的 None 檢查已在 5 個相關方法中加入
- 建議：啟用 mypy strict mode
```

---

## 🎯 根因分類

| 類型 | 描述 | 預防 |
|------|------|------|
| **邊界條件** | 未處理 null/empty/邊界值 | 加強邊界測試 |
| **競爭條件** | 並發存取導致 | 加入鎖定機制 |
| **類型錯誤** | 類型不匹配 | 啟用 strict typing |
| **邏輯錯誤** | 業務邏輯不正確 | 加強 domain 測試 |
| **整合問題** | 外部服務互動 | 加強整合測試 |
