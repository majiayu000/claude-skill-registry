---
name: literature-filter
description: |
  Filter, validate and organize literature search results.
  LOAD THIS SKILL WHEN: User has search results and needs to "過濾", "篩選", "filter", "選擇文獻" | reviewing search results | narrowing down papers.
  CAPABILITIES: Relevance filtering, duplicate detection, inclusion/exclusion criteria, Zotero integration.
---

# 文獻過濾技能 (Literature Filter)

## 描述

對搜尋結果進行過濾、驗證和整理，支援自動和人工篩選模式。

## 觸發條件

- 「過濾文獻」「篩選結果」「選擇相關論文」
- "filter papers", "screen articles", "apply criteria"
- 收到搜尋結果後需要縮小範圍

## 可用 Tools

### MCP Tools (pubmed-search)

| Tool | 用途 | 參數 |
|------|------|------|
| `fetch_article_details` | 取得完整摘要 | pmids |
| `get_citation_metrics` | 引用指標篩選 | pmids, min_citations, min_rcr |
| `analyze_fulltext_access` | 檢查全文可用性 | pmids |

### MCP Tools (zotero-keeper)

| Tool | 用途 | 參數 |
|------|------|------|
| `check_articles_owned` | 檢查重複 | pmids |
| `advanced_search` | 搜尋已有文獻 | q, item_type |

### Agent 自主判斷

Agent 會根據以下標準自主過濾：

1. **相關性判斷** - 摘要是否符合研究主題
2. **品質判斷** - 期刊影響力、研究設計
3. **時效性判斷** - 是否為最新研究
4. **語言判斷** - 是否為可讀語言

## 執行流程

### 1. 自動過濾模式

```
輸入：PMID 清單
    ↓
fetch_article_details(pmids)  ← 取得完整資訊
    ↓
Agent 根據標準自動評分
    ↓
get_citation_metrics(pmids, min_rcr=1.0)  ← 過濾低影響力
    ↓
analyze_fulltext_access(pmids)  ← 標記全文可用性
    ↓
輸出：篩選後清單 + 排除原因
```

### 2. 互動式過濾模式

```
輸入：PMID 清單
    ↓
顯示每篇文章摘要
    ↓
詢問用戶：「這篇是否相關？」
    ↓
記錄 Include/Exclude 決定
    ↓
輸出：PRISMA 風格流程圖數據
```

### 3. 標準過濾模式 (Inclusion/Exclusion Criteria)

```python
# 定義納入排除標準
criteria = {
    "inclusion": [
        "研究類型: RCT, 前瞻性研究",
        "發表年份: 2020-2025",
        "語言: English, Chinese"
    ],
    "exclusion": [
        "病例報告",
        "會議摘要",
        "動物研究"
    ]
}

# Agent 自動應用標準
for article in articles:
    if matches_inclusion(article) and not matches_exclusion(article):
        include(article)
    else:
        exclude(article, reason=...)
```

## 輸出格式

```markdown
## 文獻篩選結果

### 篩選流程
- 初始筆數: 100 篇
- 去除重複: -5 篇
- 標題篩選: -30 篇
- 摘要篩選: -25 篇
- 全文篩選: -10 篇
- **最終納入: 30 篇**

### 納入文獻

| # | PMID | 標題 | 納入原因 |
|---|------|------|----------|
| 1 | 12345678 | Title... | RCT, 高品質 |

### 排除文獻

| PMID | 排除原因 |
|------|----------|
| 87654321 | 病例報告 |
| ... | ... |

### PRISMA 流程圖數據
- Identification: 100
- Screening: 65
- Eligibility: 40
- Included: 30
```

## 使用範例

**範例 1：快速過濾**
```
用戶：「幫我過濾這些文獻，只留 RCR > 1.5 的」
執行：get_citation_metrics(pmids, min_rcr=1.5)
```

**範例 2：標準過濾**
```
用戶：「用系統性回顧標準篩選，排除病例報告和動物研究」
執行：
1. fetch_article_details(pmids)
2. Agent 自動判斷每篇文章
3. 輸出納入/排除清單
```

## 相關技能

- `literature-search` - 搜尋文獻
- `literature-retrieval` - 組合技能：搜尋 + 過濾
