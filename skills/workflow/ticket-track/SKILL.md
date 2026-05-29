---
name: ticket-track
description: "Ticket 追蹤系統 v2.1 - 欄位化操作與批量處理。提供兩種核心能力：(1) READ 操作 - 查詢 ticket 資訊包含 5W1H 欄位、版本進度、樹狀關係、代理人進度、完整內容、執行日誌；(2) UPDATE 操作 - 更新狀態、5W1H 欄位、父子關係、Phase 記錄、批量操作、日誌追加。支援版本驅動的任務管理，強制使用指令操作而非直接讀寫 ticket 檔案。"
---

# Ticket Track v2.1

Ticket 追蹤系統 - 欄位化操作與批量處理。

**重要**：禁止直接使用 Read/Edit 工具操作 ticket 檔案，必須使用本指令集。

## 核心設計

```text
Main Thread              Ticket (YAML/MD)             Agent
    |                           |                        |
    |  READ (query/version/     |                        |
    |       tree/agent/5W1H)    |                        |
    |-------------------------->|                        |
    |<--------------------------|                        |
    |                           |                        |
    |                           |  UPDATE (claim/complete/
    |                           |         phase/set-*)   |
    |                           |<-----------------------|
    |                           |                        |
```

**主要功能**:
- 5W1H 欄位查詢和更新
- 版本驅動進度管理
- 父子 Ticket 關係追蹤
- Phase 歷史記錄

---

## Ticket YAML 格式

```yaml
---
# === 識別欄位 ===
id: 0.29.0-W1-001
title: "[動詞] [目標]"
type: IMP | RES | ANA | INV | DOC
status: pending | in_progress | completed | blocked

# === 版本欄位 ===
version: 0.29.1          # 目標完成版本（小版本）
priority: P0 | P1 | P2 | P3

# === 關係欄位 ===
parent_id: null           # 父 Ticket（如有）
children: []              # 子 Ticket IDs（如有）
blockedBy: []             # 依賴的 Ticket IDs

# === 5W1H 欄位 ===
who:
  current: parsley-flutter-developer
  history:
    phase1: lavender-interface-designer
    phase2: sage-test-architect
    phase3a: pepper-test-implementer
    phase3b: parsley-flutter-developer
    phase4: null
what: "任務描述"
when: "觸發時機"
where:
  layer: Domain
  files:
    - lib/path/to/file.dart
why: "需求依據"
how:
  task_type: Implementation
  strategy: "實作策略"

# === 狀態追蹤 ===
assigned: false
started_at: null
completed_at: null

# === 元資料 ===
created: 2026-01-23
updated: 2026-01-23
---
```

---

## READ 操作

### 查詢單一 Ticket

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py query 0.29.0-W1-001
```

輸出完整 Ticket 資訊，包含 5W1H 欄位和關係。

### 列出 Tickets

```bash
# 列出所有
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py list

# 過濾狀態
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py list --pending
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py list --in-progress
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py list --completed
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py list --blocked
```

### 快速摘要

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py summary
```

**輸出範例**:
```text
[Summary] v0.29.0 (2/5 完成)
   [已完成]: 2 | [進行中]: 1 | [待處理]: 2 | [被阻塞]: 0
--------------------------------------------------------------------------------
0.29.0-W1-001 | [已完成] | parsley    | 重新設計 ticket-track SKILL
0.29.0-W1-002 | [進行中] | parsley    | 重新設計 ticket-create SKILL (已 30m)
0.29.0-W2-001 | [待處理] | pending    | 建立 tdd-phase1-split SKILL
```

### 版本進度查詢

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py version 0.29.0
```

按小版本分組顯示進度。

**輸出範例**:
```text
[Version] v0.29.0 進度報告
============================================================

0.29.1 (2/3 完成)
----------------------------------------
  0.29.0-W1-001 | [已完成] | 重新設計 ticket-track
  0.29.0-W1-002 | [已完成] | 重新設計 ticket-create
  0.29.0-W2-001 | [待處理] | 建立 tdd-phase1-split

0.29.2 (0/2 完成)
----------------------------------------
  0.29.0-W3-001 | [待處理] | 更新 CLAUDE.md
  0.29.0-W3-002 | [待處理] | 更新 tdd-collaboration-flow
```

### 樹狀查詢

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py tree 0.29.0-W1-001
```

顯示 Parent -> Current -> Children 關係。

**輸出範例**:
```text
[Tree] 0.29.0-W1-001
========================================
Parent: 0.29.0-W0-001 [待處理] - Ticket 系統重構總覽

Current: 0.29.0-W1-001 [已完成] - 重新設計 ticket-track SKILL

Children:
  - 0.29.0-W1-001-A [已完成] - 更新 Python 腳本
  - 0.29.0-W1-001-B [已完成] - 更新 SKILL.md
```

### 代理人進度查詢

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py agent parsley
```

**輸出範例**:
```text
[Agent] parsley (3/5 完成)
   [已完成]: 3 | [進行中]: 1 | [待處理]: 1
------------------------------------------------------------
0.29.0-W1-001 | [已完成] | 重新設計 ticket-track SKILL
0.29.0-W1-002 | [已完成] | 重新設計 ticket-create SKILL
0.29.0-W2-001 | [進行中] | 建立 tdd-phase1-split SKILL
```

### 5W1H 單欄位查詢

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py who 0.29.0-W1-001
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py what 0.29.0-W1-001
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py when 0.29.0-W1-001
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py where 0.29.0-W1-001
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py why 0.29.0-W1-001
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py how 0.29.0-W1-001
```

**輸出範例**:
```text
[WHO] 0.29.0-W1-001
   current: parsley-flutter-developer
   history: {'phase1': 'lavender', 'phase2': 'sage', 'phase3b': 'parsley'}
```

### 完整 Ticket 內容（取代 Read）

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py full 0.29.0-W1-001
```

輸出 ticket 的完整原始內容，包含 frontmatter 和 body。

### 執行日誌輸出（body only）

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py log 0.29.0-W1-001
```

只輸出 ticket 的 body 部分（執行日誌區段）。

### 批量查詢狀態

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py batch-status "0.29.0-W1-001,0.29.0-W1-002,0.29.0-W1-003"
```

一次查詢多個 ticket 的狀態。

---

## UPDATE 操作

### 接手 Ticket

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py claim 0.29.0-W1-001
```

更新 status, assigned, started_at。

### 完成 Ticket

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py complete 0.29.0-W1-001
```

更新 status, completed_at。

### 放棄 Ticket

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py release 0.29.0-W1-001
```

重置 status, assigned, started_at。

### 更新 Phase

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py phase 0.29.0-W1-001 phase2 sage-test-architect
```

更新 who.history 和 who.current。

### 添加子 Ticket

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py add-child 0.29.0-W0-001 0.29.0-W1-001
```

更新 parent 的 children 和 child 的 parent_id。

### 設定 5W1H 欄位

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-who 0.29.0-W1-001 parsley
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-what 0.29.0-W1-001 "更新的任務描述"
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-when 0.29.0-W1-001 "Phase 3b 開始"
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-where 0.29.0-W1-001 Domain
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-why 0.29.0-W1-001 "需求變更"
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-how 0.29.0-W1-001 Implementation
```

### 更新版本

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-version 0.29.0-W1-001 0.29.2
```

### 更新優先級

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py set-priority 0.29.0-W1-001 P0
```

有效值: P0, P1, P2, P3

### 批量認領

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py batch-claim "0.29.0-W1-001,0.29.0-W1-002,0.29.0-W1-003"
```

一次認領多個 ticket。

### 批量完成

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py batch-complete "0.29.0-W1-001,0.29.0-W1-002,0.29.0-W1-003"
```

一次完成多個 ticket。

### 追加執行日誌

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py append-log 0.29.0-W1-001 --section "Problem Analysis" "發現依賴版本衝突問題"
```

追加內容到指定區段，自動加上時間戳。區段名稱如: Problem Analysis, Solution, Test Results, Notes 等。

### 勾選驗收條件

```bash
uv run .claude/skills/ticket-track/scripts/ticket-tracker.py check-acceptance 0.29.0-W1-001 0
```

勾選或取消勾選指定索引的驗收條件（索引從 0 開始）。

---

## 狀態圖示

| 圖示 | 狀態 | 條件 |
|------|--------|-----------|
| [待處理] | Pending | `status: "pending"` |
| [進行中] | In Progress | `status: "in_progress"` |
| [已完成] | Completed | `status: "completed"` |
| [被阻塞] | Blocked | `status: "blocked"` |

---

## 最佳實踐

### 主線程

- **使用 `summary`** 快速了解版本進度
- **使用 `version`** 查詢版本的小版本進度
- **使用 `tree`** 查詢 Ticket 的拆分關係
- **使用 `agent`** 追蹤特定代理人的工作量

### 代理人

- **開始前** 執行 `claim`
- **完成後** 執行 `complete`
- **Phase 轉換時** 執行 `phase` 記錄歷史
- **遇到阻塞** 執行 `release` 並回報

---

## 檔案結構

```text
docs/work-logs/
├── v0.29.0/
│   ├── tickets/
│   │   ├── 0.29.0-W1-001.md
│   │   ├── 0.29.0-W1-002.md
│   │   └── ...
│   └── v0.29.0-ticket-system-refactor.md
```

---

## 相關 Skills

- `/ticket-create` - 建立 Atomic Tickets（5W1H 引導式）

## 資源

### 腳本
- `.claude/skills/ticket-track/scripts/ticket-tracker.py` - 主要追蹤腳本

### 參考
- `.claude/methodologies/atomic-ticket-methodology.md` - Atomic Ticket 方法論
- `.claude/methodologies/ticket-lifecycle-management-methodology.md` - Ticket 生命週期管理
