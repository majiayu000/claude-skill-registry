---
name: Git Worktree Design
description: 當使用者的需求是新增多個功能，或判斷使用者的需求適合拆分成多個 feature branch 並行開發時，或是提到 "worktree"、"git worktree"、"多分支開發"、"parallel branches"，自動觸發此 Skill。先分析需求並建議 worktree 拆分方案，經使用者確認後執行建立。
---

# Git Worktree Design — 智慧拆分平行開發

分析使用者需求，判斷是否適合以 `git worktree` 拆分成多個 feature branch 平行開發，提供建議方案並執行。

---

## 流程

### 1. 分析當前狀態

執行以下指令了解 repo 狀態：

```bash
# 確認當前分支
git branch --show-current

# 列出既有 worktree
git worktree list

# 取得 remote 資訊
git remote -v

# 確認工作目錄狀態
git status --short
```

若有未提交的變更，提醒使用者先處理（commit 或 stash）再繼續。

---

### 2. 全局設計（拆分方案 + Feature Spec）

在建立任何 worktree 之前，先從全局視角完成所有 feature 的設計。這一步同時產出 **拆分方案** 和每個 feature 的 **Spec 草案**，讓使用者一次 review 整體規劃。

#### 2a. 需求拆分

根據使用者需求，分析並拆分成多個獨立的 feature branch。

**拆分原則：**

| 原則 | 說明 |
|------|------|
| **功能獨立性** | 每個 worktree 負責一個獨立功能，減少跨分支衝突 |
| **最小相依** | 盡量避免分支間互相依賴，可獨立開發與測試 |
| **合理粒度** | 不宜太細（增加管理負擔），不宜太粗（失去平行開發優勢） |
| **命名語意** | 分支名清楚描述功能，格式 `feature/<功能名>` |

#### 2b. 設計各 Feature Spec

針對每個拆分出來的 feature，根據使用者的原始需求和專案現況，**自動推導**出完整的 Spec 內容（不是丟空白範本）。

**每份 Spec 應包含：**

| 區塊 | 說明 |
|------|------|
| **目標** | 這個 feature branch 要達成什麼 |
| **實作範圍** | 具體的任務 checklist，粒度到 AI 看了就能直接動手 |
| **驗收標準** | 可測試的行為或 UI 狀態描述 |
| **技術約束** | 專案慣例、不可引入的依賴、需相容的介面等 |
| **跨分支備註** | 與其他 feature 的相依關係、建議合併順序等 |

> **重點**：在全局設計階段就考慮跨分支相依，例如 feature A 產出的共用元件是否影響 feature B，合併順序是否有先後。

#### 2c. 呈現完整方案給使用者

以表格 + 各 feature spec 摘要的形式向使用者呈現**完整方案**：

```
📋 Worktree 拆分方案（共 N 個分支）

| # | 分支名稱 | Worktree 目錄 | 負責功能 |
|---|----------|---------------|----------|
| 1 | feature/hero-redesign | ../project-hero | Hero 區塊重新設計 |
| 2 | feature/pricing-page | ../project-pricing | 定價頁面 |
| 3 | feature/testimonials | ../project-testimonials | 用戶見證區塊 |

---

📝 Feature Spec 摘要：

### 1. feature/hero-redesign
- 目標：重新設計 Hero 區塊，加入動態背景與 CTA
- 驗收：首屏載入 < 2s，CTA 按鈕可點擊跳轉
- 相依：無，可獨立開發

### 2. feature/pricing-page
- 目標：新增月/年切換的定價頁面
- 驗收：切換月/年時價格正確更新，手機版排版正常
- 相依：無，可獨立開發

### 3. feature/testimonials
- 目標：新增用戶見證輪播區塊
- 驗收：輪播自動播放，手動切換無 bug
- 相依：無，可獨立開發

---

建議合併順序：1 → 2 → 3（無強制相依，可任意順序）

確認執行？(Y/n)
```

使用 `notify_user` 工具向使用者展示完整方案（拆分 + Spec 摘要）並等待確認。

---

### 3. 建立 Worktree

使用者確認後，依序執行：

```bash
# 建立各 worktree（新分支）
git worktree add -b <branch_name> <worktree_path>
```

#### Worktree 目錄命名規則

- 目錄放在當前 repo 的**同層級**（`../`）
- 格式：`../<project-name>-<feature-short-name>`
- 取 repo 目錄名作為 `<project-name>` 前綴，避免與其他專案混淆

---

### 4. 安裝依賴

偵測專案使用的套件管理器並安裝依賴：

```bash
# 偵測 lock file 判斷套件管理器
# pnpm-lock.yaml → pnpm install
# yarn.lock → yarn install
# package-lock.json → npm install
# bun.lockb → bun install
```

對每個 worktree 執行：

```bash
cd <worktree_path> && <package_manager> install
```

> **注意**：每個 worktree 有獨立的工作目錄，`node_modules` 不會共享，必須各自安裝。

---

### 5. 寫入 Feature Spec 檔案

將步驟 2 設計好的 Spec 內容，使用 `write_to_file` 工具寫入到每個 worktree 的根目錄 `<worktree_path>/git-worktree-spec.md`。

#### Spec 檔案格式

```markdown
# Feature Spec: <功能名稱>

> 此文件由 Git Worktree Design Skill 自動產生，供 AI Agent 作為開發指引。

## 分支資訊

| 項目 | 值 |
|------|-----|
| 分支名稱 | `feature/<name>` |
| 基於分支 | `<base_branch>` |
| Worktree 路徑 | `<absolute_path>` |
| 建立時間 | `<timestamp>` |

## 目標

（從步驟 2 的設計內容填入）

## 實作範圍

- [ ] 具體任務 1
- [ ] 具體任務 2
- [ ] 具體任務 3

## 驗收標準

- 條件 A 成立時，應有行為 X
- 條件 B 成立時，應有行為 Y

## 技術約束

- 不得引入新的 npm 依賴（視情況填寫）
- 需相容既有的設計系統 / API 介面
## 跨分支備註

與其他 worktree 分支的相依關係、合併順序建議等。
```

---

### 6. 確認結果

所有 worktree 建立完成後，執行：

```bash
git worktree list
```

以表格形式展示結果：

```
✅ Worktree 建立完成！

| Worktree 目錄 | 分支 | 狀態 | Spec |
|---------------|------|------|------|
| /path/to/project-hero | feature/hero-redesign | ✅ 就緒 | ✅ 已寫入 |
| /path/to/project-pricing | feature/pricing-page | ✅ 就緒 | ✅ 已寫入 |
| /path/to/project-testimonials | feature/testimonials | ✅ 就緒 | ✅ 已寫入 |

💡 提示：
- 切換工作目錄到對應 worktree 即可開始開發
- 所有 worktree 共享同一個 .git，commit 歷史互通
```

---

## 邊界情況處理

- **分支已存在**：偵測到分支已存在時，改用不帶 `-b` 的指令（`git worktree add <path> <existing-branch>`），並提示使用者確認
- **目錄已存在**：提示衝突並建議替代目錄名
- **有未提交變更**：提醒先 commit 或 stash
- **遠端分支同步**：建議先 `git fetch` 取得最新遠端狀態
- **Worktree 清理**：提醒使用者開發完成後用 `git worktree remove` 和 `git branch -d` 清理

---

## 常用維護指令

```bash
# 列出所有 worktree
git worktree list

# 移除 worktree（保留分支）
git worktree remove <path>

# 強制移除（有未提交變更時）
git worktree remove --force <path>

# 清理失效的 worktree 參照
git worktree prune

# 刪除分支（合併後）
git branch -d <branch_name>
```
