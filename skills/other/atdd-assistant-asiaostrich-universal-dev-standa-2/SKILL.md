---
name: atdd
scope: partial
description: "[UDS] Guide through Acceptance Test-Driven Development workflow"
allowed-tools: Read, Write, Grep, Glob
argument-hint: "[feature or spec | 功能或規格]"
---

# ATDD Assistant | ATDD 助手

Guide through the Acceptance Test-Driven Development (ATDD) workflow for defining and validating user stories.

引導驗收測試驅動開發（ATDD）流程，用於定義和驗證使用者故事。

## ATDD Cycle | ATDD 循環

```
WORKSHOP ──► DISTILLATION ──► DEVELOPMENT ──► DEMO ──► DONE
    ^                              │              │
    └──────────────────────────────┴──────────────┘
                  (Refinement needed)
```

## Workflow | 工作流程

### 1. WORKSHOP - Define AC | 定義驗收條件
PO presents user story, team asks clarifying questions, define acceptance criteria together.

### 2. DISTILLATION - Convert to Tests | 轉換為測試
Convert AC to executable test format, remove ambiguity, get PO sign-off.

### 3. DEVELOPMENT - Implement | 實作
Run acceptance tests (should fail initially), use BDD/TDD for implementation, iterate until all pass.

### 4. DEMO - Present | 向利害關係人展示
Show passing acceptance tests, demonstrate working functionality, get formal acceptance.

### 5. DONE - Complete | 完成
PO accepted, code merged, story closed.

## INVEST Criteria | INVEST 準則

| Criterion | Description | 說明 |
|-----------|-------------|------|
| **I**ndependent | Can be developed separately | 可獨立開發 |
| **N**egotiable | Details can be discussed | 可協商細節 |
| **V**aluable | Delivers business value | 提供商業價值 |
| **E**stimable | Can estimate effort | 可估算工作量 |
| **S**mall | Fits in one sprint | 一個 Sprint 可完成 |
| **T**estable | Has clear acceptance criteria | 有明確驗收條件 |

## User Story Format | 使用者故事格式

```markdown
As a [role],
I want [feature],
So that [benefit].

### Acceptance Criteria
- Given [context], when [action], then [result]
```

## Usage | 使用方式

```
/atdd                              - Start interactive ATDD session | 啟動互動式 ATDD 會話
/atdd "user can reset password"    - ATDD for specific feature | 針對特定功能
/atdd US-123                       - ATDD for existing user story | 處理現有使用者故事
```

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [acceptance-test-driven-development.md](../../core/acceptance-test-driven-development.md)
