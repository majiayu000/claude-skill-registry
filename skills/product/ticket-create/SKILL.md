---
name: ticket-create
description: "Atomic Ticket Creator v2.0 - 5W1H 引導式建立與版本驅動管理。支援完整 5W1H 欄位設定、父子 Ticket 關係建立、版本號驅動任務分配。遵循 Single Responsibility Principle，每個 Ticket 必須有 One Action + One Target。"
---

# Ticket Create v2.0

Atomic Ticket 建立工具 - 5W1H 引導式建立與版本驅動管理。

## 核心原則

**Atomic Ticket = One Action + One Target (Single Responsibility)**

每個 Ticket 必須通過四項驗證：

1. **語義檢查**: 能用「動詞 + 單一目標」表達？
2. **修改原因檢查**: 只有一個原因會導致修改？
3. **驗收一致性**: 所有驗收條件指向同一目標？
4. **依賴獨立性**: 拆分後無循環依賴？

## 禁止的評估方法

**絕對不要用這些指標判斷是否需要拆分**:
- 時間估計（30 分鐘、1 小時）
- 程式碼行數（50 行、100 行）
- 檔案數量（2 個檔案、5 個檔案）
- 測試數量（5 個測試、10 個測試）

**只使用上面的四項 Single Responsibility 檢查**。

---

## Ticket YAML 格式

```yaml
---
# === 識別欄位 ===
id: 0.29.0-W1-001
title: "實作 XXX"
type: IMP | RES | ANA | INV | DOC
status: pending | in_progress | completed | blocked

# === 版本欄位 ===
version: 0.29.1          # 目標完成版本（小版本）
wave: 1
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

# === 驗收條件 ===
acceptance:
  - 任務實作完成
  - 相關測試通過
  - 無程式碼品質警告

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

## 命令

### 初始化版本目錄

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py init 0.29.0
```

建立版本目錄和 tickets 子目錄。

### 建立 Ticket（完整 5W1H）

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py create \
  --version 0.29.0 \
  --wave 1 \
  --action "實作" \
  --target "ticket-track SKILL 重構" \
  --who "parsley-flutter-developer" \
  --what "重新設計 ticket-track SKILL 以支援 5W1H 欄位" \
  --when "Phase 3b 開始時" \
  --where-layer "Infrastructure" \
  --where-files ".claude/skills/ticket-track/scripts/ticket-tracker.py" \
  --why "支援版本驅動任務管理和 5W1H 查詢" \
  --how-type "Implementation" \
  --how-strategy "TDD 循環：先寫測試 -> 實作 -> 重構" \
  --priority "P1"
```

**輸出**:
```text
[OK] 已建立 Ticket: 0.29.0-W1-001
   Location: docs/work-logs/v0.29.0/tickets/0.29.0-W1-001.md
```

### 建立 Ticket（快速模式）

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py create \
  --version 0.29.0 \
  --wave 1 \
  --action "實作" \
  --target "ticket-track SKILL 重構"
```

只需要 version, wave, action, target，其他欄位使用預設值。

### 建立子 Ticket

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py create-child \
  --parent-id 0.29.0-W1-001 \
  --wave 1 \
  --action "更新" \
  --target "Python 腳本" \
  --who "parsley-flutter-developer"
```

自動：
- 從 parent-id 解析 version
- 繼承 parent 的 priority、where.layer、why
- 更新 parent 的 children 欄位
- 設定 child 的 parent_id 欄位

**輸出**:
```text
[OK] 已建立子 Ticket: 0.29.0-W1-002
   Location: docs/work-logs/v0.29.0/tickets/0.29.0-W1-002.md
   Parent: 0.29.0-W1-001
   (已更新 parent 的 children)
```

### 列出 Tickets

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py list --version 0.29.0
```

**輸出**:
```text
[List] v0.29.0 Tickets (3 個)
----------------------------------------------------------------------
0.29.0-W1-001 | [待處理] | P1 | pending    | 實作 ticket-track SKILL 重構
0.29.0-W1-002 | [待處理] | P1 | parsley    | 更新 Python 腳本
0.29.0-W1-003 | [進行中] | P2 | sage       | 設計測試案例
```

### 顯示 Ticket 詳情

```bash
uv run .claude/skills/ticket-create/scripts/ticket-creator.py show --id 0.29.0-W1-001
```

顯示完整 5W1H 欄位和關係。

---

## 互動式建立流程

### Step 1: 需求收集

```text
Claude: 請描述你想要完成的任務：
```

等待用戶輸入。

### Step 2: 職責分析

分析用戶需求並識別獨立職責：

```text
Claude: 我識別到以下獨立職責：
1. [職責 1]
2. [職責 2]
...

每個職責將成為一個獨立的 Atomic Ticket。
```

### Step 3: Single Responsibility 檢查

對每個識別的職責執行四項檢查：

```text
Claude: 職責 1 "[描述]" Single Responsibility 檢查：
[OK] 語義：能表達為「[動詞] + [目標]」
[OK] 修改原因：只有「[原因]」會導致修改
[OK] 驗收一致：所有條件指向 [目標]
[OK] 依賴獨立：無循環依賴
-> 符合 Atomic Ticket 標準
```

若未通過，建議進一步拆分：

```text
Claude: [Warning] 職責 2 "[描述]" 需要進一步拆分：
[Error] 修改原因：有兩個修改原因
   - 原因 A: [描述]
   - 原因 B: [描述]
-> 建議拆分為：
   - Ticket A: [動詞] [目標 A]
   - Ticket B: [動詞] [目標 B]
```

### Step 4: Ticket 建立確認

```text
Claude: 建議建立以下 Atomic Tickets：

| ID | Action | Target | Agent | Version |
|----|--------|--------|-------|---------|
| 0.29.0-W1-001 | 實作 | XXX | parsley | 0.29.1 |
| 0.29.0-W1-002 | 實作 | YYY | parsley | 0.29.1 |
| 0.29.0-W2-001 | 實作 | ZZZ | parsley | 0.29.2 |

確認建立？(Y/n)
```

### Step 5: 執行建立

確認後，為每個 Ticket 執行 create 命令。

---

## Ticket ID 格式

```text
{Version}-W{Wave}-{Seq}
```

**範例**:
- `0.29.0-W1-001` - v0.29.0, Wave 1, Ticket 1
- `0.29.0-W2-003` - v0.29.0, Wave 2, Ticket 3

### Wave 定義（依賴層級）

| Wave | 意義 | 可執行時機 |
|------|------|------------|
| W1 | 無依賴 | 立即，可並行 |
| W2 | 依賴部分 W1 tickets | W1 依賴完成後 |
| W3 | 依賴部分 W2 tickets | W2 依賴完成後 |

**Wave 分配規則**: 無依賴 -> W1, 依賴 W1 -> W2, 依此類推。

---

## 命名規範

**Action（動詞）**:
- `實作` / `Implement` - 建立新功能
- `修復` / `Fix` - 修正錯誤
- `新增` / `Add` - 新增測試或文件
- `重構` / `Refactor` - 改善結構
- `移除` / `Remove` - 刪除功能
- `更新` / `Update` - 修改現有內容

**Target（名詞）**:
- 具體方法: `startScan() 方法`
- 具體類別: `ISBNValidator 類別`
- 具體測試: `ISBNValidator.validate() 測試`
- 具體檔案: `ticket-create SKILL.md`

---

## 版本驅動任務分配

### 版本號層級

```text
v1.0.0（大版本）
├── v0.29.0（中版本）- Feature 級別
│   ├── v0.29.1（小版本）- 無依賴 Tickets（可並行）
│   ├── v0.29.2（小版本）- 依賴 v0.29.1 的 Tickets
│   └── v0.29.3（小版本）- 技術債務處理
├── v0.30.0（中版本）- 下一個 Feature
└── ...
```

### 版本分配原則

| 情況 | 版本分配 |
|------|---------|
| 無依賴任務 | 同小版本（可並行） |
| 有依賴任務 | 不同小版本（序列） |
| 技術債務 | 專用小版本或下個中版本 |

---

## 常見錯誤

| 錯誤 | 問題 | 正確做法 |
|------|------|---------|
| 實作掃描和離線支援 | 兩個目標 | 拆分為兩個 Tickets |
| 修復所有 ISBN 測試 | 多個目標 | 每個測試一個 Ticket |
| 重構並優化 SearchService | 兩個動作 | 拆分為兩個 Tickets |

---

## 狀態追蹤

狀態透過 Ticket 檔案的 frontmatter 欄位追蹤。

| 欄位 | 類型 | 描述 |
|------|------|------|
| `status` | string | "pending", "in_progress", "completed", "blocked" |
| `assigned` | boolean | 是否已被認領 |
| `started_at` | datetime | 開始時間（ISO 8601） |
| `completed_at` | datetime | 完成時間（ISO 8601） |

使用 `/ticket-track` 命令更新狀態：
- `claim` - 標記為進行中
- `complete` - 標記為已完成
- `release` - 釋放回待處理

---

## 相關 Skills

- `/ticket-track` - 追蹤和更新 Ticket 狀態

## 資源

### 腳本
- `.claude/skills/ticket-create/scripts/ticket-creator.py` - 主要建立腳本

### 參考
- `.claude/methodologies/atomic-ticket-methodology.md` - Atomic Ticket 完整方法論
- `.claude/methodologies/ticket-lifecycle-management-methodology.md` - Ticket 生命週期管理
