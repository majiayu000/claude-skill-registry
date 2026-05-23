---
name: tdd-phase1-split
description: "TDD Phase 1 SOLID 原則驅動拆分輔助工具。在 Phase 1（功能設計）階段分析功能範圍，識別獨立職責，產出拆分建議和版本號分配。確保設計階段就考慮 DIP、LSP、ISP，才能實踐 SRP 和 OCP。"
---

# TDD Phase 1 Split v1.0

SOLID 原則驅動的功能拆分輔助工具 - 在設計階段就進行拆分，而非實作階段。

## 核心理念

```text
Phase 1（功能設計）就要考慮：
- DIP（依賴反轉）→ 介面設計
- LSP（里氏替換）→ 繼承規劃
- ISP（介面隔離）→ 介面拆分
           ↓
     才能實踐
- SRP（單一職責）
- OCP（開閉原則）

拆分時機：Phase 1，不是 Phase 3a
```

**關鍵原則**：設計階段就要拆分，不是等到實作才發現需要拆分。

---

## SOLID 原則檢查清單

### SRP（Single Responsibility Principle）

**檢查問題**：
- 這個功能有幾個獨立的修改原因？
- 能用「動詞 + 單一目標」描述嗎？
- 所有驗收條件都指向同一目標嗎？

**拆分信號**：
- 有 2+ 個修改原因
- 需要用「和」連接描述
- 驗收條件指向不同目標

### OCP（Open-Closed Principle）

**檢查問題**：
- 未來擴展需要修改現有程式碼嗎？
- 有沒有可以抽象的變化點？

**拆分信號**：
- 需要 switch/case 或 if/else 處理不同類型
- 未來新增類型需要修改現有程式碼

### LSP（Liskov Substitution Principle）

**檢查問題**：
- 有繼承關係嗎？
- 子類別能完全替換父類別嗎？

**拆分信號**：
- 子類別需要覆寫並改變父類別行為
- 某些方法在子類別中沒有意義

### ISP（Interface Segregation Principle）

**檢查問題**：
- 介面有沒有強迫實作不需要的方法？
- 一個介面服務多少個不同的客戶端？

**拆分信號**：
- 實作類別有空方法或拋出 NotImplemented
- 不同客戶端只使用介面的一部分

### DIP（Dependency Inversion Principle）

**檢查問題**：
- 高層模組是否依賴低層模組？
- 依賴的是抽象還是具體實作？

**拆分信號**：
- 直接 import 具體類別
- 無法獨立測試（依賴外部服務）

---

## 命令

### 分析功能

```bash
uv run .claude/skills/tdd-phase1-split/scripts/tdd-phase1-split.py analyze \
  --description "實作書籍搜尋功能"
```

互動式分析，產出 SOLID 檢查報告。

### 產出拆分建議

```bash
uv run .claude/skills/tdd-phase1-split/scripts/tdd-phase1-split.py suggest \
  --description "實作書籍搜尋功能" \
  --version 0.29.0
```

**輸出範例**：
```text
[Split] 功能拆分建議

原始需求：實作書籍搜尋功能

SOLID 分析結果：
[SRP] 識別 3 個獨立職責
[DIP] 需要 2 個介面抽象
[ISP] 建議拆分 1 個介面

拆分建議：
----------------------------------------------------------------------
| 子功能 | 描述 | 架構層 | 版本 | 依賴 |
|--------|------|--------|------|------|
| A | SearchQuery 值物件 | Domain | 0.29.1 | 無 |
| B | SearchResult Entity | Domain | 0.29.1 | 無 |
| C | ISearchRepository 介面 | Domain | 0.29.1 | 無 |
| D | SearchBooksUseCase | Application | 0.29.2 | A, B, C |
| E | SearchRepository 實作 | Infrastructure | 0.29.2 | C |
| F | SearchWidget | Presentation | 0.29.3 | D |

版本分配說明：
- v0.29.1：無依賴任務（A, B, C 可並行）
- v0.29.2：依賴 v0.29.1 的任務（D, E）
- v0.29.3：依賴 v0.29.2 的任務（F）
```

### 建立拆分 Tickets

```bash
uv run .claude/skills/tdd-phase1-split/scripts/tdd-phase1-split.py create-tickets \
  --description "實作書籍搜尋功能" \
  --version 0.29.0 \
  --wave 3
```

根據分析結果建立父 Ticket 和子 Tickets。

### 驗證拆分

```bash
uv run .claude/skills/tdd-phase1-split/scripts/tdd-phase1-split.py validate \
  --ticket-id 0.29.0-W3-001
```

驗證已拆分的 Tickets 是否符合 SOLID 原則。

---

## 拆分流程

### Step 1: 功能範圍分析

```text
lavender 收到功能需求
    |
    v
識別功能邊界
    |
    +-- 輸入是什麼？
    +-- 輸出是什麼？
    +-- 涉及哪些實體？
    +-- 需要哪些操作？
```

### Step 2: SOLID 原則應用

```text
對每個識別的元素
    |
    +-- SRP：有幾個修改原因？
    +-- OCP：如何支援擴展？
    +-- LSP：繼承關係正確嗎？
    +-- ISP：介面需要拆分嗎？
    +-- DIP：依賴方向正確嗎？
```

### Step 3: 拆分決策

```text
根據 SOLID 分析
    |
    +-- 識別獨立職責 → 各自一個 Ticket
    +-- 識別需要的介面 → 介面定義 Ticket
    +-- 識別依賴關係 → 決定版本分配
```

### Step 4: 版本號分配

```text
依賴分析
    |
    +-- 無依賴 → 同小版本（可並行）
    +-- 有依賴 → 不同小版本（序列）
    |
    v
產出版本分配建議
```

### Step 5: Ticket 建立

```text
為每個獨立職責建立 Ticket
    |
    +-- 父 Ticket（功能總覽）
    +-- 子 Tickets（各自 TDD 循環）
    +-- 設定 blockedBy 關係
    +-- 設定版本號
```

---

## 拆分範例

### 範例：書籍搜尋功能

**原始需求**：「實作書籍搜尋功能」

**Step 1: 功能範圍分析**
- 輸入：搜尋關鍵字、篩選條件
- 輸出：搜尋結果列表
- 實體：SearchQuery, SearchResult, Book
- 操作：查詢、篩選、排序、分頁

**Step 2: SOLID 分析**

| 原則 | 分析結果 | 建議 |
|------|---------|------|
| SRP | 搜尋查詢建立、搜尋執行、結果呈現是 3 個職責 | 拆分為 3+ 個 Ticket |
| OCP | 未來可能有不同搜尋來源（本地、API） | 定義 ISearchRepository |
| LSP | 無繼承需求 | - |
| ISP | Repository 可能同時有讀寫 | 考慮 ISearchRepository 只負責搜尋 |
| DIP | UseCase 不應依賴具體 Repository | 定義介面 |

**Step 3: 拆分結果**

```text
0.29.0-W3-001（父 Ticket）書籍搜尋功能
├── version: 0.29.3（整體完成版本）
└── children: [W3-002, W3-003, W3-004, W3-005, W3-006]

0.29.0-W3-002（子）SearchQuery 值物件
├── version: 0.29.1
├── blockedBy: []
└── where: Domain

0.29.0-W3-003（子）SearchResult Entity
├── version: 0.29.1
├── blockedBy: []
└── where: Domain

0.29.0-W3-004（子）ISearchRepository 介面
├── version: 0.29.1
├── blockedBy: []
└── where: Domain

0.29.0-W3-005（子）SearchBooksUseCase
├── version: 0.29.2
├── blockedBy: [W3-002, W3-003, W3-004]
└── where: Application

0.29.0-W3-006（子）SearchWidget
├── version: 0.29.3
├── blockedBy: [W3-005]
└── where: Presentation
```

**Step 4: 執行順序**

```text
v0.29.1：W3-002 + W3-003 + W3-004（並行）
v0.29.2：W3-005（序列）
v0.29.3：W3-006（序列）
```

---

## 版本號分配規則

### 小版本分配原則

| 情況 | 版本分配 | 範例 |
|------|---------|------|
| 無依賴任務 | 同小版本 | Domain Entities → v0.29.1 |
| 依賴前一批 | 下一個小版本 | UseCases → v0.29.2 |
| 依賴多批次 | 最後依賴的下一版 | Widget → v0.29.3 |

### 並行判斷

| 條件 | 可並行 |
|------|--------|
| 同一小版本 | 是 |
| 無 blockedBy | 是 |
| 不同架構層但無依賴 | 是 |
| 有 blockedBy | 否 |

---

## 輸出格式

### 拆分報告

```markdown
## Phase 1 拆分報告

### 原始需求
- **描述**: [需求描述]
- **預估複雜度**: 高

### SOLID 分析

| 原則 | 分析結果 | 拆分建議 |
|------|---------|---------|
| SRP | [結果] | [建議] |
| OCP | [結果] | [建議] |
| LSP | [結果] | [建議] |
| ISP | [結果] | [建議] |
| DIP | [結果] | [建議] |

### 拆分清單

| ID | 描述 | 層級 | 版本 | 依賴 | 代理人 |
|----|------|------|------|------|--------|
| A | [描述] | Domain | 0.29.1 | - | lavender |
| B | [描述] | Domain | 0.29.1 | - | lavender |

### 執行計畫

1. **v0.29.1**（並行）
   - Ticket A
   - Ticket B

2. **v0.29.2**（序列）
   - Ticket C（依賴 A, B）

### 建議行動
- 建立父 Ticket
- 建立子 Tickets
- 設定依賴關係
```

---

## 與其他 SKILL 的整合

### 與 ticket-create 整合

拆分完成後，使用 `/ticket-create` 建立 Tickets：

```bash
# 建立父 Ticket
uv run .claude/skills/ticket-create/scripts/ticket-creator.py create \
  --version 0.29.0 --wave 3 \
  --action "實作" --target "書籍搜尋功能"

# 建立子 Tickets
uv run .claude/skills/ticket-create/scripts/ticket-creator.py create-child \
  --parent-id 0.29.0-W3-001 --wave 3 \
  --action "建立" --target "SearchQuery 值物件"
```

### 與 ticket-track 整合

追蹤拆分後的 Tickets：

```bash
# 查詢拆分樹狀結構
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py tree 0.29.0-W3-001

# 查詢版本進度
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py version 0.29.0
```

---

## 相關文件

- [TDD 流程]($CLAUDE_PROJECT_DIR/.claude/rules/flows/tdd-flow.md)
- [Atomic Ticket 方法論]($CLAUDE_PROJECT_DIR/.claude/methodologies/atomic-ticket-methodology.md)
- [主線程決策樹]($CLAUDE_PROJECT_DIR/.claude/rules/core/decision-tree.md)
- [任務拆分指南]($CLAUDE_PROJECT_DIR/.claude/rules/guides/task-splitting.md)
