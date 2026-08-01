---
name: git-precommit
description: 協調多個 Skills 完成 Git 提交前的所有準備工作。
---

---
name: git-precommit
description: Orchestrate pre-commit workflow including Memory Bank sync, README/CHANGELOG/ROADMAP updates, and MCP tool count sync. Triggers: GIT, gc, push, commit, 提交, 準備 commit, 要提交了, git commit, pre-commit, 推送.
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
│  Step 2: tool-count-sync [必要] MCP 工具數量同步 │
│  Step 3: readme-update   [可選] README 更新      │
│  Step 4: changelog-update[可選] CHANGELOG 更新   │
│  Step 5: roadmap-update  [可選] ROADMAP 更新     │
│  Step 6: arch-check      [條件] 架構文檔檢查     │
│  Step 7: commit-prepare  [最終] 準備提交         │
└─────────────────────────────────────────────────┘
```

## 必要步驟：MCP 工具數量同步

每次 commit 前**必須**執行工具統計腳本，確保文檔中的工具數量和列表與程式碼同步：

```bash
uv run python scripts/count_mcp_tools.py --update-docs
```

此腳本會自動更新：
- `README.md` - 工具數量
- `README.zh-TW.md` - 工具數量
- `.github/copilot-instructions.md` - 工具數量 + 完整列表
- `src/.../TOOLS_INDEX.md` - 完整工具索引

## 參數

| 參數 | 說明 | 預設 |
|------|------|------|
| `--skip-readme` | 跳過 README 更新 | false |
| `--skip-changelog` | 跳過 CHANGELOG 更新 | false |
| `--skip-roadmap` | 跳過 ROADMAP 更新 | false |
| `--skip-tool-sync` | 跳過工具統計同步 | false |
| `--dry-run` | 只預覽不修改 | false |
| `--quick` | 只執行必要步驟 (memory-sync + tool-sync) | false |

## 使用範例

```
「準備 commit」           # 完整流程
「快速 commit」           # 等同 --quick
「commit --skip-readme」  # 跳過 README
```

## 輸出格式

```
🚀 Git Pre-Commit 工作流

[1/7] Memory Bank 同步 ✅
  └─ progress.md: 更新 2 項
  └─ activeContext.md: 已更新

[2/7] MCP 工具統計同步 ✅
  └─ 工具數量: 40 (12 categories)
  └─ README.md: 已更新
  └─ copilot-instructions.md: 已更新

[3/7] README 更新 ✅
  └─ 新增功能說明

[4/7] CHANGELOG 更新 ✅
  └─ 添加 v0.2.0 條目

[5/7] ROADMAP 更新 ⏭️ (無變更)

[6/7] 架構文檔 ⏭️ (無結構性變更)

[7/7] Commit 準備 ✅
  └─ 建議訊息：feat: 新增用戶認證模組

📋 Staged files:
  - src/auth/...
  - docs/...

準備好了！確認提交？
```
