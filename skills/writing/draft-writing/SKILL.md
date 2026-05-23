---
name: draft-writing
description: |
  論文草稿的撰寫、讀取、引用管理。
  LOAD THIS SKILL WHEN: 寫草稿、draft、撰寫、Introduction、Methods、Results、Discussion、引用、citation、字數
  CAPABILITIES: write_draft, draft_section, read_draft, list_drafts, insert_citation, sync_references, count_words, get_section_template
---

# 草稿撰寫技能

## 適用情境

| 觸發語 | 操作 |
|--------|------|
| 寫草稿、撰寫 section | `draft_section()` 或 `write_draft()` |
| 看草稿、讀取 | `read_draft()` |
| 有哪些草稿 | `list_drafts()` |
| 加引用、插入引用 | `insert_citation()` |
| 整理引用、生成 References | `sync_references()` |
| 字數、word count | `count_words()` |
| 怎麼寫這個 section | `get_section_template()` |

---

## ⚠️ 前置條件

**撰寫任何草稿前必須：**
1. 確認專案已選定：`get_current_project()`
2. 確認 concept.md 存在且包含 🔒 區塊
3. 結構驗證通過（🔒 NOVELTY + 🔒 SELLING POINTS 不為空）

**例外**：寫 `concept.md` 本身不需要驗證

---

## MCP Tools 清單

### 撰寫工具 (mdpaper)

| 工具 | 參數 | 說明 |
|------|------|------|
| `write_draft` | `filename`, `content`, `project` | 建立/覆寫草稿檔案 |
| `draft_section` | `topic`, `notes`, `project` | 根據筆記產出特定 section |
| `read_draft` | `filename`, `project` | 讀取草稿結構與內容 |
| `list_drafts` | `project` | 列出所有草稿 |

### 引用工具 (mdpaper)

| 工具 | 參數 | 說明 |
|------|------|------|
| `insert_citation` | `filename`, `target_text`, `pmid` | 在指定位置插入引用 |
| `sync_references` | `filename`, `project` | 掃描 [[wikilinks]] 生成 References |
| `count_words` | `filename`, `section` | 計算字數 |
| `get_section_template` | `section` | 取得 section 寫作指南 |

---

## 工作流程

### Flow A: 撰寫新 Section

```
Step 1: 確認專案和驗證狀態
  get_current_project()
  validate_for_section(section="Introduction")
  → ✅ CAN WRITE / ❌ CANNOT WRITE

Step 2: 讀取 concept 和受保護內容
  read_draft(filename="concept.md")
  → 提取 🔒 NOVELTY STATEMENT
  → 提取 🔒 KEY SELLING POINTS

Step 3: 取得寫作指南
  get_section_template(section="Introduction")
  → 返回該 section 的結構建議

Step 4: 撰寫內容
  draft_section(
    topic="Introduction",
    notes="Background on remimazolam... Gap in literature..."
  )
  或
  write_draft(
    filename="drafts/introduction.md",
    content="..."
  )

Step 5: 確認字數
  count_words(filename="drafts/introduction.md")
```

---

### Flow B: 插入引用

**方法 1: Wikilink 格式（推薦）**
```markdown
先前研究指出 [[greer2017_27345583]] 使用 propofol 有其限制。
```

然後執行：
```
sync_references(filename="drafts/introduction.md")
→ 轉換為 [1] 格式
→ 生成 References 區塊
```

**方法 2: 定點插入**
```
insert_citation(
  filename="drafts/introduction.md",
  target_text="先前研究指出",
  pmid="27345583"
)
```

---

### Flow C: 整理 References

```
Step 1: 確認草稿有 wikilinks
  read_draft(filename="drafts/full_manuscript.md")
  → 檢查是否有 [[citation_key]] 格式

Step 2: 同步引用
  sync_references(filename="drafts/full_manuscript.md")
  → 輸出：
    | # | Citation Key | Title |
    | 1 | greer2017_27345583 | Review of... |
    | 2 | smith2020_12345678 | Analysis of... |

Step 3: 確認未找到的引用
  → ⚠️ Not found: chen2019_87654321
  → 需要先 save_reference_mcp(pmid="87654321")
```

---

## 🔒 受保護內容規則

| 受保護區塊 | 出現位置 | 規則 |
|------------|----------|------|
| 🔒 NOVELTY STATEMENT | concept.md | Introduction 必須體現 |
| 🔒 KEY SELLING POINTS | concept.md | Discussion 必須強調全部 |

**撰寫時的強制要求：**
```
✅ Introduction 開頭或結尾必須呼應 NOVELTY
✅ Discussion 必須逐條強調 SELLING POINTS
❌ 不可刪除或弱化 🔒 區塊內容
❌ 修改 🔒 區塊前必須詢問用戶
```

---

## Section 寫作指南

### Introduction (400-600 words)
```
1. Background - 研究領域背景（2-3 段）
2. Gap - 現有研究的不足
3. Objective - 本研究目的（含 🔒 NOVELTY）
```

### Methods (800-1200 words)
```
1. Study Design - 研究設計
2. Participants - 納入排除標準
3. Intervention - 介入措施
4. Outcomes - 結果指標
5. Statistics - 統計方法
```

### Results (600-1000 words)
```
1. Participants - 收案流程、基線特徵
2. Primary Outcome - 主要結果
3. Secondary Outcomes - 次要結果
4. Tables/Figures - 圖表說明
```

### Discussion (1000-1500 words)
```
1. Main Findings - 主要發現（含 🔒 SELLING POINTS）
2. Comparison - 與現有文獻比較
3. Implications - 臨床意義
4. Limitations - 研究限制
5. Conclusion - 結論
```

### Abstract (250-350 words)
```
Structured: Background / Methods / Results / Conclusions
Unstructured: 依期刊要求
```

---

## Wikilink 格式

**正確格式：**
```
[[author2024_12345678]]  ← 作者年份_PMID
[[greer2017_27345583]]
```

**會被自動修復的格式：**
```
[[12345678]] → [[author2024_12345678]]
[[PMID:12345678]] → [[author2024_12345678]]
Author 2024 [[12345678]] → [[author2024_12345678]]
```

---

## 常見問題

| 問題 | 解法 |
|------|------|
| 草稿被阻擋 | 檢查 concept.md 的 🔒 區塊是否填寫 |
| 引用找不到 | 先 `save_reference_mcp()` 儲存文獻 |
| 字數太多 | `count_words()` 逐 section 檢查 |
| 不知道怎麼寫 | `get_section_template()` 取得指南 |
| Wikilink 格式錯誤 | `validate_wikilinks()` 自動修復 |

---

## 相關技能

- `concept-development` - 發展 concept（撰寫前）
- `concept-validation` - 驗證 concept（撰寫前）
- `reference-management` - 管理引用文獻
- `word-export` - 匯出為 Word
