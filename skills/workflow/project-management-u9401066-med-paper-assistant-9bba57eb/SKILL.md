---
name: project-management
description: |
  研究專案的建立、切換、設定管理。
  LOAD THIS SKILL WHEN: 新專案、切換專案、專案設定、paper type、start exploration、convert exploration
  CAPABILITIES: create_project, list_projects, switch_project, get_current_project, setup_project_interactive, start_exploration, convert_exploration_to_project
---

# 專案管理技能

## 適用情境

| 觸發語 | 操作 |
|--------|------|
| 新專案、開始研究 | `create_project()` |
| 切換、換專案 | `switch_project()` |
| 設定 paper type | `setup_project_interactive()` |
| 先瀏覽文獻 | `start_exploration()` |
| 轉成正式專案 | `convert_exploration_to_project()` |

---

## MCP Tools 清單

### 專案 CRUD (mdpaper)

| 工具 | 參數 | 說明 |
|------|------|------|
| `create_project` | `name`, `description`, `paper_type` | 建立新專案 |
| `list_projects` | 無 | 列出所有專案 |
| `switch_project` | `slug` | 切換專案 |
| `get_current_project` | 無 | 取得目前專案資訊 |
| `get_project_paths` | 無 | 取得專案目錄路徑 |

### 專案設定 (mdpaper)

| 工具 | 參數 | 說明 |
|------|------|------|
| `setup_project_interactive` | 無 | 互動式設定（使用 elicitation）|
| `get_paper_types` | 無 | 列出可用論文類型 |
| `update_project_status` | `status` | 更新專案狀態 |
| `update_project_settings` | `paper_type`, `target_journal` | 更新設定 |

### 探索模式 (mdpaper)

| 工具 | 參數 | 說明 |
|------|------|------|
| `start_exploration` | 無 | 建立探索工作區 |
| `get_exploration_status` | 無 | 查看探索狀態 |
| `convert_exploration_to_project` | `name`, `description` | 轉換為正式專案 |

---

## 工作流程

### Flow A: 建立新專案

```
Step 1: 確認用戶需求
  - 問：專案名稱（英文）、描述、論文類型

Step 2: 建立專案
  create_project(
    name="Remimazolam Sedation Study",
    description="Comparing remimazolam with propofol in ICU",
    paper_type="original-research"
  )

Step 3: 互動式設定
  setup_project_interactive()
  → 選擇 paper type（如果 Step 2 未設定）
  → 設定互動偏好
  → 新增專案備註
```

**⚠️ 重要規則：**
- `name` 必須是英文！
- 若用戶給中文名稱，Agent 必須翻譯：
  - "死亡率預測" → "Mortality Prediction"
  - "鼻腔氣管插管" → "Nasotracheal Intubation"

---

### Flow B: 切換專案

```
Step 1: 列出專案
  list_projects()
  → 顯示所有專案及目前選中

Step 2: 切換
  switch_project(slug="remimazolam-sedation-study")

Step 3: 確認
  get_current_project()
  → 顯示專案統計資訊
```

---

### Flow C: 探索模式（先瀏覽再決定）

```
Step 1: 開始探索
  start_exploration()
  → 建立 ~exploration 臨時工作區

Step 2: 自由搜尋文獻
  (使用 pubmed-search MCP)
  → 儲存有興趣的文獻到探索區

Step 3: 查看探索成果
  get_exploration_status()
  → 顯示已儲存的文獻

Step 4: 決定方向後轉換
  convert_exploration_to_project(
    name="My Research Topic",
    description="Based on exploration findings"
  )
  → 文獻自動遷移到正式專案
```

---

## Paper Types

| 類型代碼 | 名稱 | 結構 |
|----------|------|------|
| `original-research` | 原創研究 | IMRAD |
| `systematic-review` | 系統性回顧 | PRISMA |
| `meta-analysis` | 統合分析 | PRISMA + Forest |
| `case-report` | 病例報告 | CARE |
| `review-article` | 回顧文章 | 敘事結構 |
| `letter` | 讀者來函 | 精簡結構 |

---

## Project Memory 同步

**切換專案後必須讀取：**
```
projects/{slug}/.memory/activeContext.md
→ 了解上次工作到哪裡、Agent 的想法
```

**離開專案前必須寫入：**
```
projects/{slug}/.memory/activeContext.md
→ Current Focus: 目前進度
→ Key References: 關鍵文獻
→ Memo: Agent 觀察筆記
```

---

## 常見問題

| 問題 | 解法 |
|------|------|
| 專案名稱有中文 | Agent 翻譯成英文再呼叫 |
| 不確定用哪個專案 | `list_projects()` 先列出 |
| 想先看文獻再決定 | `start_exploration()` |
| 探索區有文獻要保留 | `convert_exploration_to_project()` |
| 要改 paper type | `update_project_settings(paper_type="...")` |

---

## 相關技能

- `literature-review` - 文獻搜尋（探索模式後常用）
- `concept-development` - 概念發展（建立專案後）
- `memory-checkpoint` - 記憶同步（切換專案時）
