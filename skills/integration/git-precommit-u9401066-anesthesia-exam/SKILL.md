---
name: git-precommit
description: 協調多個 Skills 完成 Git 提交前的所有準備工作。這是一個「編排器」Skill，負責調用其他 Skills。
---

---
name: git-precommit
description: Orchestrate pre-commit workflow including Memory Bank sync, README/CHANGELOG/ROADMAP updates. Triggers: GIT, gc, push, commit, 提交, 準備 commit, 要提交了, git commit, pre-commit, 推送, stage, 暫存, checkin, 簽入, submit, save, 準備發布, ready to commit, 要推了.
version: 2.2.0
category: workflow
compatibility:
  - claude-code
  - github-copilot
  - vscode
  - codex-cli
dependencies:
  - memory-updater
  - readme-updater
  - changelog-updater
  - roadmap-updater
  - ddd-architect
allowed-tools:
  - read_file
  - write_file
  - list_dir
  - grep_search
  - get_changed_files
  - run_in_terminal
---

# Git 提交前工作流（編排器）

## 描述

協調多個 Skills 完成 Git 提交前的所有準備工作。這是一個「編排器」Skill，負責調用其他 Skills。

## 觸發條件

- 「準備 commit」「GIT」「gc」
- 「要提交了」「git commit」
- 「推送」「push」

## 法規依據

- 憲法：CONSTITUTION.md 第三章
- 子法：.github/bylaws/git-workflow.md

---

## 🔧 操作步驟（編排流程）

### Step 1: 收集變更資訊

```powershell
git status --short
git diff --name-only --cached
```

使用工具：

```
get_changed_files()  # 取得變更清單
```

### Step 2: 執行 memory-updater（必要）

**呼叫條件**：永遠執行

```
調用 memory-updater skill：
- 更新 activeContext.md（當前焦點）
- 更新 progress.md（移動 Done/Doing）
```

### Step 3: 執行 readme-updater（條件）

**呼叫條件**：
- 新增功能（src/ 有新檔案）
- 依賴變更（pyproject.toml/package.json 變更）
- API 變更

```
若需要，調用 readme-updater skill
```

### Step 4: 執行 changelog-updater（條件）

**呼叫條件**：
- 有功能性變更（非純文檔）
- 有 bug 修復
- 有安全性修補

```
若需要，調用 changelog-updater skill
```

### Step 5: 執行 roadmap-updater（條件）

**呼叫條件**：
- 完成了 ROADMAP 中列出的功能

```
若需要，調用 roadmap-updater skill
```

### Step 6: 架構文檔檢查（條件）

**呼叫條件**：
- 有結構性變更（新增 domain/application 層）

```
若需要，更新 memory-bank/architect.md
```

### Step 7: 生成 Commit Message

依據 Conventional Commits 格式：

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**類型對照**：

| 變更內容 | type |
| -------- | ---- |
| 新功能 | feat |
| Bug 修復 | fix |
| 文檔 | docs |
| 重構 | refactor |
| 測試 | test |
| 建構/CI | chore |

### Step 8: 執行 Git 命令

```powershell
# 檢查狀態
git status

# Stage 變更
git add .

# 提交
git commit -m "feat(auth): 新增用戶認證模組"

# 推送（如果用戶確認）
git push origin main
```

---

## 📊 流程圖

```
┌─────────────────────────────────────────────────┐
│          Git Pre-Commit Orchestrator            │
├─────────────────────────────────────────────────┤
│  Step 1: 收集變更    [分析] get_changed_files   │
│  Step 2: memory-sync [必要] Memory Bank 同步    │
│  Step 3: readme      [條件] README 更新         │
│  Step 4: changelog   [條件] CHANGELOG 更新      │
│  Step 5: roadmap     [條件] ROADMAP 更新        │
│  Step 6: architect   [條件] 架構文檔檢查        │
│  Step 7: message     [生成] Commit Message      │
│  Step 8: commit      [執行] git add/commit/push │
└─────────────────────────────────────────────────┘
```

---

## 🎮 參數選項

| 指令 | 效果 |
| ---- | ---- |
| `「準備 commit」` | 完整流程 |
| `「快速 commit」` | 只執行 memory-sync |
| `「commit 跳過 readme」` | 跳過 README 更新 |
| `「只更新文檔然後 commit」` | 只執行文檔相關步驟 |

---

## 📝 輸出格式

```
🚀 Git Pre-Commit 工作流

[1/6] 變更分析
  └─ 變更檔案：5 個
  └─ 新增：src/auth/login.py
  └─ 修改：README.md

[2/6] Memory Bank 同步 ✅
  └─ progress.md: 新增 1 個 Done 項目
  └─ activeContext.md: 已更新焦點

[3/6] README 更新 ✅
  └─ 新增「用戶認證」功能說明

[4/6] CHANGELOG 更新 ✅
  └─ 添加到 [Unreleased] > Added

[5/6] ROADMAP 更新 ⏭️ (無匹配項目)

[6/6] Commit 準備 ✅

📋 Staged files (5):
  M  README.md
  M  CHANGELOG.md
  A  src/auth/login.py
  A  src/auth/models.py
  M  memory-bank/progress.md

建議 Commit Message：
───────────────────────
feat(auth): 新增用戶認證模組

- 實作登入/登出功能
- 新增 User model
───────────────────────

確認提交？(y/n/edit)
```

---

## ⚠️ 注意事項

1. **Memory Bank 同步是必要的**：即使用 --quick，也要執行
2. **不要自動 push**：除非用戶明確要求
3. **保留未 stage 的檔案**：不要自動 `git add .` 所有檔案
4. **確認 Commit Message**：讓用戶有機會修改

---

## 🔄 與其他 Skills 關係

這是**編排器** Skill，負責調用：

```
git-precommit (編排器)
├── memory-updater (必要)
├── readme-updater (條件)
├── changelog-updater (條件)
├── roadmap-updater (條件)
└── ddd-architect (架構檢查參考)
```
