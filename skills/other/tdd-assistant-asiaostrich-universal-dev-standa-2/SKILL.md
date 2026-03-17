---
name: tdd
scope: partial
description: "[UDS] Guide through Test-Driven Development workflow"
allowed-tools: Read, Write, Grep, Glob, Bash(npm test:*), Bash(npx vitest:*)
argument-hint: "[feature or file | 功能或檔案]"
---

# TDD Assistant | TDD 助手

Guide through the Test-Driven Development workflow: Red-Green-Refactor.

引導測試驅動開發（TDD）流程：紅-綠-重構。

## TDD Cycle | TDD 循環

```
    ┌─────┐       ┌───────┐       ┌──────────┐
    │ RED │ ────► │ GREEN │ ────► │ REFACTOR │
    └─────┘       └───────┘       └──────────┘
       ▲                                │
       └────────────────────────────────┘
```

## Workflow | 工作流程

### Phase 1: RED - Write Failing Test | 紅燈 - 撰寫失敗測試

- Write a test that describes the desired behavior | 撰寫描述預期行為的測試
- Run tests - confirm it **fails** for the right reason | 執行測試 - 確認正確地失敗
- Use AAA pattern (Arrange-Act-Assert) | 使用 AAA 模式

### Phase 2: GREEN - Make Test Pass | 綠燈 - 讓測試通過

- Write **minimum** code to pass the test | 撰寫最少的程式碼讓測試通過
- Hardcoding is acceptable at this stage | 此階段可以硬編碼
- Run tests - confirm it **passes** | 執行測試 - 確認通過

### Phase 3: REFACTOR - Improve Code | 重構 - 改善程式碼

- Remove duplication (DRY) | 移除重複
- Improve naming and structure | 改善命名與結構
- Run tests after **every** change | 每次變更後執行測試
- No new functionality added | 不新增功能

## FIRST Principles | FIRST 原則

| Principle | Description | 說明 |
|-----------|-------------|------|
| **F**ast | Tests run quickly (< 100ms/unit) | 快速執行 |
| **I**ndependent | No shared state between tests | 測試間無共享狀態 |
| **R**epeatable | Same result every time | 每次結果相同 |
| **S**elf-validating | Clear pass/fail result | 明確的通過/失敗 |
| **T**imely | Written before production code | 在產品程式碼之前撰寫 |

## Usage | 使用方式

- `/tdd` - Start interactive TDD session
- `/tdd calculateTotal` - TDD for specific function
- `/tdd "user can login"` - TDD for user story

## Reference | 參考

- Detailed guide: [guide.md](./guide.md)
- Core standard: [test-driven-development.md](../../core/test-driven-development.md)
