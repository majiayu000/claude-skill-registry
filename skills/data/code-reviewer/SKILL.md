---
name: code-reviewer
description: Comprehensive code review checking quality, security, and best practices. Triggers: CR, review, 審查, 檢查, check, 看一下, PR, code review, 品質, inspect, 檢視, 看看, 幫看, lint, quality check, 品質檢查, pull request, merge request, MR, diff, 程式碼審查.
version: 2.2.0
category: quality
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - ddd-architect
  - code-refactor
allowed-tools:
  - read_file
  - grep_search
  - semantic_search
  - get_errors
  - list_code_usages
  - run_in_terminal
---

# 程式碼審查技能

## 描述

對程式碼進行全面審查，檢查品質、安全性、效能和最佳實踐。

## 觸發條件

- 「review 這段程式碼」「CR」「審查」
- 「檢查程式碼」「看一下」「幫看」
- 「code review」「PR review」

---

## 🔧 操作步驟

### Step 1: 確定審查範圍

詢問或推斷審查目標：
- 特定檔案：`read_file("path/to/file.py")`
- 整個目錄：`grep_search` 取得概覽
- 特定功能：`semantic_search("功能名稱")`
- 最近變更：`get_changed_files()`

### Step 2: 執行靜態分析（Python 專案）

```powershell
# Ruff - 快速 linter (取代 flake8 + isort + pyupgrade)
uv run ruff check src/ --output-format=concise

# Mypy - 型別檢查
uv run mypy src/ --ignore-missing-imports

# Bandit - 安全性檢查
uv run bandit -r src/ -ll

# Vulture - 死碼偵測
uv run vulture src/ --min-confidence 80
```

### Step 3: 審查程式碼品質

| 檢查項目 | 標準 | 工具輔助 |
| -------- | ---- | -------- |
| 命名清晰度 | 名稱應描述用途 | 人工審查 |
| 函數長度 | < 50 行 | grep_search |
| 類別大小 | < 300 行 | grep_search |
| 複雜度 | McCabe < 10 | ruff --select=C901 |
| DRY 原則 | 無重複程式碼 | semantic_search |
| SOLID 原則 | 單一職責等 | 人工審查 |

### Step 4: 審查安全性

| 風險類型 | 檢查方式 | 嚴重程度 |
| -------- | -------- | -------- |
| SQL 注入 | 搜尋 raw SQL | 🔴 Critical |
| XSS | 搜尋未轉義輸出 | 🔴 Critical |
| 硬編碼密碼 | grep "password\|secret\|key" | 🔴 Critical |
| 路徑遍歷 | 搜尋未驗證路徑 | 🟠 High |
| 日誌洩漏 | 搜尋敏感資料輸出 | 🟡 Medium |

### Step 5: 審查效能

| 問題類型 | 偵測方式 |
| -------- | -------- |
| N+1 查詢 | 搜尋迴圈內的 DB 呼叫 |
| 無謂迴圈 | 審查巢狀迴圈 |
| 記憶體洩漏 | 檢查資源釋放 |
| 阻塞操作 | 審查 I/O 操作 |

### Step 6: 審查 DDD 架構

參考 `ddd-architect` 規則：
- Domain 層是否有外部依賴？
- Repository Interface 是否在 Domain 層？
- Application 層是否過度膨脹？

### Step 7: 產生審查報告

---

## 📊 審查報告格式

```markdown
# 程式碼審查報告

📁 審查範圍：`src/domain/`, `src/application/`
📅 日期：2026-01-15
👤 審查者：AI Assistant

---

## 📈 總覽

| 指標 | 分數 | 說明 |
| ---- | ---- | ---- |
| 品質 | 8/10 | 命名清晰，部分函數過長 |
| 安全 | 9/10 | 無明顯漏洞 |
| 效能 | 7/10 | 存在 N+1 查詢風險 |
| 架構 | 8/10 | 符合 DDD，但有小違規 |

---

## ✅ 優點

1. **清晰的領域模型**：User entity 封裝良好
2. **完整的錯誤處理**：使用自定義例外
3. **良好的測試覆蓋**：核心邏輯有單元測試

---

## ⚠️ 問題發現

### 🔴 Critical (必須修復)

#### 1. SQL 注入風險
- **位置**：[user_repository.py](src/infrastructure/repositories/user_repository.py#L45)
- **問題**：使用字串拼接建立 SQL
- **建議**：使用參數化查詢

```python
# ❌ 現有
query = f"SELECT * FROM users WHERE name = '{name}'"

# ✅ 建議
query = "SELECT * FROM users WHERE name = ?"
cursor.execute(query, (name,))
```

### 🟠 High (應該修復)

#### 2. 函數過長
- **位置**：[auth_service.py](src/application/services/auth_service.py#L20-L85)
- **問題**：`authenticate()` 函數 65 行
- **建議**：拆分為多個私有方法

### 🟡 Medium (建議改進)

#### 3. 缺少型別標註
- **位置**：多處
- **建議**：為公開 API 新增型別標註

---

## 📋 改進清單

- [ ] 修復 SQL 注入問題 (Critical)
- [ ] 重構 authenticate() 函數 (High)
- [ ] 新增型別標註 (Medium)
- [ ] 補充單元測試 (Low)
```

---

## 🔄 與其他 Skills 整合

| Skill | 整合方式 |
| ----- | -------- |
| `code-refactor` | 發現問題後調用進行重構 |
| `security-reviewer` | 深入安全審查時調用 |
| `test-generator` | 發現測試不足時調用 |
| `ddd-architect` | 架構違規時參考 |

---

## ⚠️ 注意事項

1. **避免過度批評**：指出問題同時肯定優點
2. **提供具體建議**：不只說「這裡有問題」，要說「建議這樣改」
3. **標註嚴重程度**：區分 Critical/High/Medium/Low
4. **考慮上下文**：原型專案和生產專案標準不同
5. **可操作性**：每個問題應有明確的修復方向
