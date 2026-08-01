---
name: git-precommit
description: 協調多個 Skills 完成 Git 提交前的所有準備工作。
---

---
name: git-precommit
description: Orchestrate pre-commit workflow including Memory Bank sync, README/CHANGELOG/ROADMAP updates. Triggers: GIT, gc, push, commit, 提交, 準備 commit, 要提交了, git commit, pre-commit, 推送.
---

# Git 提交前工作流（編排器）

## 描述
協調多個 Skills 完成 Git 提交前的所有準備工作。

## 觸發條件
- 「準備 commit」「要提交了」「git commit」

## 法規依據
- 憲法：CONSTITUTION.md 第三章
- 子法：.github/bylaws/git-workflow.md

## 執行流程

```
┌─────────────────────────────────────────────────┐
│              Git Pre-Commit Orchestrator        │
├─────────────────────────────────────────────────┤
│  Step 1: memory-sync     [必要] Memory Bank 同步 │
│  Step 2: readme-update   [可選] README 更新      │
│  Step 3: changelog-update[可選] CHANGELOG 更新   │
│  Step 4: roadmap-update  [可選] ROADMAP 更新     │
│  Step 5: arch-check      [條件] 架構文檔檢查     │
│  Step 6: commit-prepare  [最終] 準備提交         │
└─────────────────────────────────────────────────┘
```

## 參數

| 參數 | 說明 | 預設 |
|------|------|------|
| `--skip-readme` | 跳過 README 更新 | false |
| `--skip-changelog` | 跳過 CHANGELOG 更新 | false |
| `--skip-roadmap` | 跳過 ROADMAP 更新 | false |
| `--dry-run` | 只預覽不修改 | false |
| `--quick` | 只執行必要步驟 (memory-sync) | false |

## 使用範例

```
「準備 commit」           # 完整流程
「快速 commit」           # 等同 --quick
「commit --skip-readme」  # 跳過 README
```

## 輸出格式

```
🚀 Git Pre-Commit 工作流

[1/6] Memory Bank 同步 ✅
  └─ progress.md: 更新 2 項
  └─ activeContext.md: 已更新

[2/6] README 更新 ✅
  └─ 新增功能說明

[3/6] CHANGELOG 更新 ✅
  └─ 添加 v0.2.0 條目

[4/6] ROADMAP 更新 ⏭️ (無變更)

[5/6] 架構文檔 ⏭️ (無結構性變更)

[6/6] Commit 準備 ✅
  └─ 建議訊息：feat: 新增用戶認證模組

📋 Staged files:
  - src/auth/...
  - docs/...

準備好了！確認提交？
```
