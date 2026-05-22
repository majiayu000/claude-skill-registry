---
name: version-release
description: "版本發布整合工具，處理 worklog 檢查、文件更新、合併推送等完整流程。三步驟流程：Pre-flight 檢查 → Document Updates → Git Operations。支援 check / update-docs / release 子命令，包含 --dry-run 預覽模式。"
---

# Version Release Skill

版本發布整合工具，處理完整的版本發布流程。結合工作日誌檢查、CHANGELOG 更新、Git 操作（合併、Tag、推送、清理）。

## 核心功能

**目的**: 自動化版本發布流程，確保所有檢查通過後再進行 Git 操作

**工作流程**:
1. **Pre-flight 檢查** - 驗證 worklog 完成度、技術債務狀態、版本同步
2. **文件更新** - 清理 todolist、更新 CHANGELOG、確認版本號
3. **Git 操作** - 合併、建立 Tag、推送、清理分支

## 三步驟發布流程

### Step 1: Pre-flight 檢查

驗證發布前置條件是否滿足：

```python
def preflight_check(version: str):
    """
    1.1 確認 worklog 目標達成
        - 掃描 docs/work-logs/v{VERSION}*.md
        - 檢查主工作日誌中的 Phase 是否都標記完成 (✅)
        - 驗證 Phase 0-4 都已執行並記錄

    1.2 檢查技術債務狀態
        - 讀取 todolist.md 的「技術債務追蹤」區塊
        - 確認當前版本的 TD 是否都已處理或延遲到下一版本
        - 驗證沒有未分類的 TD

    1.3 版本同步檢查
        - pubspec.yaml 版本 vs worklog 版本一致
        - 當前分支是否為 feature/v{VERSION}
        - 工作目錄是否乾淨（沒有未提交的修改）

    1.4 檔案存在檢查
        - CHANGELOG.md 存在
        - 主工作日誌存在 (v{VERSION}.0-main.md)
        - todolist.md 存在
    """
```

**檢查項目**:
- ✅ 所有 Phase 工作日誌已完成
- ✅ 技術債務已分類和處理
- ✅ 版本號在所有地方一致
- ✅ 當前分支正確
- ✅ 工作目錄乾淨

### Step 2: 文件更新

更新 CHANGELOG、todolist 等文件：

```python
def update_documents(version: str):
    """
    2.1 清理 todolist.md
        - 找出當前版本系列在任務表格中的行
        - 標記該版本為已完成
        - 更新版本狀態表格的 「開發狀態」 列
        - 格式: ✅ Phase 3b 完成 → ✅ 已完成

    2.2 更新 CHANGELOG.md（Keep a Changelog 格式）
        - 讀取工作日誌提取功能變動
        - 生成版本區塊: ## [X.Y.Z] - YYYY-MM-DD
        - 分類: Added, Changed, Fixed, Removed
        - 複製到 CHANGELOG.md 頂部（在其他版本之前）

    2.3 確認 pubspec.yaml 版本號正確
        - 驗證 version: X.Y.Z 行存在
        - 與 worklog 版本號一致
    """
```

**更新檔案**:
- `docs/todolist.md` - 標記版本為已完成
- `CHANGELOG.md` - 新增版本變動記錄
- `pubspec.yaml` - 驗證版本號

### Step 3: Git 操作

執行 Git 相關操作：

```python
def git_merge_and_push(version: str, dry_run: bool = False):
    """
    3.1 提交所有變更（如果有未提交的）
        git add docs/todolist.md CHANGELOG.md
        git commit -m "docs: 版本 {version} 發布準備"

    3.2 切換到 main 分支
        git checkout main

    3.3 git pull origin main（確保最新）
        git pull origin main

    3.4 合併 feature 分支（--no-ff 保留合併記錄）
        git merge feature/v{VERSION} --no-ff -m "Merge v{VERSION}"

    3.5 建立 Tag（v{VERSION}-final，如 v0.19-final）
        git tag v{VERSION}-final
        git tag -a v{VERSION}-final -m "Release v{VERSION}"

    3.6 推送到遠端（包含 tag）
        git push origin main
        git push origin v{VERSION}-final

    3.7 刪除本地和遠端 feature 分支
        git branch -d feature/v{VERSION}
        git push origin --delete feature/v{VERSION}
    """
```

**Git 操作順序**:
1. 提交檔案變更
2. 切換到 main 分支
3. 拉取最新 main
4. 合併 feature 分支（保留合併記錄）
5. 建立 Tag
6. 推送 main + Tag
7. 刪除本地/遠端 feature 分支

## CLI 介面設計

### 主要使用方式

```bash
# 自動偵測當前版本
uv run .claude/skills/version-release/scripts/version_release.py release

# 指定版本
uv run .claude/skills/version-release/scripts/version_release.py release --version 0.19

# 預覽模式（不實際執行 git 操作）
uv run .claude/skills/version-release/scripts/version_release.py release --dry-run

# 只執行檢查
uv run .claude/skills/version-release/scripts/version_release.py check

# 只更新文件
uv run .claude/skills/version-release/scripts/version_release.py update-docs
```

### 子命令說明

#### `release` - 完整發布流程

```bash
uv run .claude/skills/version-release/scripts/version_release.py release [options]

Options:
  --version TEXT        指定版本號 (format: X.Y 或 X.Y.Z, 如 0.19 或 0.19.8)
  --dry-run            預覽模式，不執行實際 git 操作
  --force              強制執行，跳過一些檢查（不推薦）
  --help               顯示幫助
```

**範例**:
```bash
# 自動偵測並發布
uv run .claude/skills/version-release/scripts/version_release.py release

# 指定 0.19 版本並預覽
uv run .claude/skills/version-release/scripts/version_release.py release --version 0.19 --dry-run

# 發布 0.19.8
uv run .claude/skills/version-release/scripts/version_release.py release --version 0.19.8
```

#### `check` - 只執行檢查

```bash
uv run .claude/skills/version-release/scripts/version_release.py check [--version X.Y]

# 檢查當前版本
uv run .claude/skills/version-release/scripts/version_release.py check

# 檢查特定版本
uv run .claude/skills/version-release/scripts/version_release.py check --version 0.19
```

#### `update-docs` - 只更新文件

```bash
uv run .claude/skills/version-release/scripts/version_release.py update-docs [--version X.Y] [--dry-run]

# 更新當前版本文件
uv run .claude/skills/version-release/scripts/version_release.py update-docs

# 預覽文件更新
uv run .claude/skills/version-release/scripts/version_release.py update-docs --dry-run
```

## 版本偵測邏輯

工具使用以下策略自動偵測版本號：

1. **命令行參數優先** - 如果指定 `--version`，使用該版本
2. **git 分支名稱** - 從 `feature/v{VERSION}` 提取版本
3. **pubspec.yaml** - 讀取 `version: X.Y.Z` 行
4. **git 標籤** - 查詢最新的版本標籤

**偵測流程**:
```
--version 參數 → git branch (feature/vX.Y) → pubspec.yaml → git tag
```

## 輸出範例

### 完整發布流程（release）

```
╔════════════════════════════════════════════════════════════════╗
║           📋 Version Release Tool - v0.19.8                    ║
╚════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 1: Pre-flight Check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Worklog 目標達成
     - docs/work-logs/v0.19.0-main.md: Phase 0-4 ✅
     - docs/work-logs/v0.19.1-phase1-feature-design.md: ✅
     - docs/work-logs/v0.19.2-phase2-test-design.md: ✅
     - docs/work-logs/v0.19.3-phase3a-strategy.md: ✅
     - docs/work-logs/v0.19.4-phase3b-implementation.md: ✅
     - docs/work-logs/v0.19.8-phase4-final-evaluation.md: ✅

  ✅ 技術債務已處理
     - 4 個 TD 已分類到 v0.20.0
     - 當前版本無待處理 TD

  ✅ 版本同步
     - pubspec.yaml: v0.19.8 ✅
     - 當前分支: feature/v0.19 ✅
     - 工作目錄: 乾淨 ✅

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 2: Document Updates
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📝 更新 docs/todolist.md
     - 標記 v0.19.x 為 ✅ 已完成

  📝 更新 CHANGELOG.md
     - 新增版本區塊 [0.19.8] - 2026-01-06
     - 分類: Added (8 items) | Changed (3 items) | Fixed (2 items)

  ✅ 確認 pubspec.yaml 版本號: v0.19.8

  ✅ 檔案變更已提交 (hash: abc1234)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3: Git Operations
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔀 合併 feature/v0.19 → main
     ✅ main 分支已更新到最新
     ✅ 已合併 feature/v0.19 (hash: def5678)

  🏷️ 建立 Tag: v0.19.8-final
     ✅ Tag 已建立 (v0.19.8-final)

  📤 推送到遠端
     ✅ main 已推送 (sync: main)
     ✅ Tag 已推送 (v0.19.8-final)

  🗑️ 清理 feature 分支
     ✅ 本地分支已刪除: feature/v0.19
     ✅ 遠端分支已刪除: origin/feature/v0.19

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 版本 v0.19.8 發布成功！

📊 發布統計:
   - 合併提交: 1
   - 文件更新: 2
   - Tag 建立: 1
   - 分支清理: 1 本地 + 1 遠端

🎉 版本已推送到 main 分支
```

### 預覽模式（--dry-run）

```
╔════════════════════════════════════════════════════════════════╗
║           📋 Version Release Tool - v0.19.8 (DRY RUN)          ║
╚════════════════════════════════════════════════════════════════╝

⚠️ 預覽模式：不會執行實際的 git 操作

[相同的 Pre-flight Check 和 Document Updates]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Step 3: Git Operations (預覽)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔀 [預覽] 將合併 feature/v0.19 → main
     指令: git merge feature/v0.19 --no-ff

  🏷️ [預覽] 將建立 Tag: v0.19.8-final
     指令: git tag v0.19.8-final

  📤 [預覽] 將推送到遠端
     指令: git push origin main
     指令: git push origin v0.19.8-final

  🗑️ [預覽] 將清理 feature 分支
     指令: git branch -d feature/v0.19
     指令: git push origin --delete feature/v0.19

✅ 預覽完成。執行不含 --dry-run 參數進行實際發布
```

### 只檢查（check）

```
╔════════════════════════════════════════════════════════════════╗
║           📋 Version Release - Pre-flight Check                ║
╚════════════════════════════════════════════════════════════════╝

✅ 所有檢查通過！該版本已準備好發布

發布指令:
  uv run .claude/skills/version-release/scripts/version_release.py release

或預覽:
  uv run .claude/skills/version-release/scripts/version_release.py release --dry-run
```

### 錯誤情況

```
❌ Pre-flight Check 失敗

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

❌ 問題 1: Worklog 未完成
   位置: docs/work-logs/v0.19.4-phase3b-implementation.md
   描述: Phase 3b 標記為 🔄 進行中，需要完成
   修復: 完成 Phase 3b 並標記為 ✅

❌ 問題 2: 版本號不同步
   pubspec.yaml 版本: v0.19.8
   工作日誌版本: v0.19.4
   修復: 確認 pubspec.yaml 版本號是否正確

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

修復後重新執行:
  uv run .claude/skills/version-release/scripts/version_release.py check
```

## 支援的版本格式

工具支援以下版本格式：

| 格式 | 範例 | 說明 |
|-----|------|------|
| 完整版本 | `0.19.8` | 三段版本號 |
| 中版本 | `0.19` | 二段版本號（自動加 .0） |
| 當前版本 | 不指定 | 自動偵測 |

**版本偵測範例**:
```bash
uv run .claude/skills/version-release/scripts/version_release.py release --version 0.19
# → 自動轉換為 0.19.0（或查詢最新的 0.19.x）

uv run .claude/skills/version-release/scripts/version_release.py release --version 0.19.8
# → 使用 0.19.8

uv run .claude/skills/version-release/scripts/version_release.py release
# → 自動偵測版本（從 git branch/pubspec.yaml）
```

## 依賴和前置條件

### 系統要求
- Python 3.10+
- Git 2.0+（用於合併和 Tag 操作）

### Python 依賴
- `pyyaml` - YAML 格式解析（pubspec.yaml）
- `click` - CLI 框架（可選，用於改進 CLI）

### 前置條件
- 完成 Phase 4 重構評估
- 所有工作日誌已記錄
- 技術債務已分類
- 在 feature/v{VERSION} 分支上
- pubspec.yaml 版本號已更新

## 功能特性

### 1. 智慧版本偵測
- 支援多種版本格式輸入
- 自動從 git 分支、pubspec.yaml、git tag 偵測
- 完整性檢查和版本驗證

### 2. 多層級檢查
- 工作日誌完成度驗證
- 技術債務分類檢查
- 版本號同步驗證
- Git 分支和工作目錄檢查

### 3. 文件自動更新
- CHANGELOG.md 自動生成
- todolist.md 自動標記
- pubspec.yaml 驗證

### 4. 安全的 Git 操作
- --dry-run 預覽模式
- 詳細的操作日誌
- 錯誤恢復指引
- 分支清理確認

### 5. 詳細的報告輸出
- 彩色化進度指示
- 結構化錯誤報告
- 逐步執行提示
- 統計資訊總結

## 錯誤處理和恢復

### 常見問題

| 問題 | 原因 | 解決方式 |
|------|------|---------|
| 版本偵測失敗 | 分支名稱不符 | 確認在 `feature/vX.Y` 分支上 |
| Worklog 檢查失敗 | Phase 未完成 | 完成所有 Phase 工作日誌 |
| 技術債務未分類 | TD 沒有版本標記 | 更新 todolist.md 技術債務表格 |
| Git 操作失敗 | 遠端衝突或權限 | 檢查 git status，解決衝突後重試 |
| 文件更新失敗 | 檔案格式變化 | 檢查 CHANGELOG.md 或 todolist.md 格式 |

### 恢復指引

**問題**: `VersionDetectionError: Unable to detect version`

```bash
# 1. 確認當前分支
git branch

# 2. 確保在 feature/vX.Y 分支
git checkout feature/v0.19

# 3. 或明確指定版本
uv run .claude/skills/version-release/scripts/version_release.py check --version 0.19
```

**問題**: `WorklogError: Phase X not completed`

```bash
# 1. 檢查工作日誌檔案
cat docs/work-logs/v0.19.4-phase3b-implementation.md

# 2. 確認 Phase 標記為 ✅ 完成
# 3. 更新 Phase 狀態
# 4. 重新執行檢查

uv run .claude/skills/version-release/scripts/version_release.py check
```

**問題**: Git 合併失敗

```bash
# 1. 檢查 git 狀態
git status

# 2. 解決衝突
# 3. 繼續合併或中止
git merge --abort

# 4. 重新執行發布流程
uv run .claude/skills/version-release/scripts/version_release.py release
```

## 相關工具和指令

### 前置 Skills
- `tech-debt-capture` - 從 Phase 4 提取技術債務並建立 Ticket

### 後置操作
- GitHub Release 建立（手動或透過 GitHub Actions）
- 版本公告發佈（手動）

### 相關文件
- `docs/todolist.md` - 版本狀態和技術債務追蹤
- `CHANGELOG.md` - 版本變動記錄
- `pubspec.yaml` - 應用程式版本號
- `docs/work-logs/` - 所有 Phase 工作日誌

## Skill 開發參考

**版本**: v1.0
**建立日期**: 2026-01-06
**執行引擎**: Python 3.10+ with PEP 723 UV Single-File
**適用場景**: UC 版本發布（工作日誌完成後）
**維護責任**: basil-hook-architect

## 使用流程檢查清單

- [ ] 所有 Phase 工作日誌已完成
- [ ] Phase 0-4 都標記為 ✅
- [ ] 技術債務已分類到 todolist.md
- [ ] 運行 `check` 確認所有檢查通過
- [ ] 運行 `release --dry-run` 預覽
- [ ] 運行 `release` 完成發布
- [ ] 驗證 main 分支已更新
- [ ] 驗證 Tag 已建立
- [ ] 確認 feature 分支已清理
