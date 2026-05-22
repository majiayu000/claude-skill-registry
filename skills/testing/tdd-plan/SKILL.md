---
name: tdd-plan
description: Create implementation plans following TDD methodology with test-first approach. Use this skill when creating implementation plans in plan mode, when user requests TDD-based development, or when planning features that require test-driven development. Ensures tests are planned BEFORE implementation code.
---

# TDD Implementation Plan

このスキルは、実装計画をTDD（テスト駆動開発）の原則に従って構成します。

## Core Principle

**テストが先、実装が後** - Tests come FIRST, implementation comes AFTER.

## Plan Structure (Required Order)

### ✅ Correct TDD Order

| Step | Phase | Content |
|------|-------|---------|
| 1 | **Red Phase** | Test files - Write failing tests first |
| 2 | **Green Phase** | Implementation - Minimal code to pass tests |
| 3 | **Refactor Phase** | Verification & cleanup |

### ❌ Wrong Order (Avoid)

| Step | Content | Problem |
|------|---------|---------|
| 1-3 | Implementation | Code before tests |
| 4 | Tests | Tests last = NOT TDD |

## Plan Template

```
# Plan: [Feature Name]

## Goal
[What this plan achieves]

---

## Files to Modify

### 1. Test Files (Red Phase - FIRST)
| File | Change |
|------|--------|
| tests/... | Add failing tests for [feature] |

### 2. Implementation (Green Phase)
| File | Change |
|------|--------|
| src/... | Implement to pass tests |

---

## Implementation Steps

### Step 1: Test Files (Red Phase - 失敗するテストを先に書く)
- Write tests for expected behavior
- **Tests MUST fail initially** (no implementation yet)

### Step 2: Implementation (Green Phase - テストを通す最小実装)
- Implement minimal changes to pass tests
- Keep implementation simple

### Step 3: Verification (Refactor Phase - 品質改善)
- Run all tests
- Type checking (if applicable)
- Code quality review
```

## Checklist Before Completing Plan

- [ ] Test files are listed BEFORE implementation files
- [ ] Step 1 is always about writing tests
- [ ] Each implementation step references which tests it should pass
- [ ] Red → Green → Refactor phases are clearly labeled

## Notes

- テスト言語・フレームワークはプロジェクトの対象言語に依存
- テスト粒度（unit/integration等）はプロジェクトの性質に依存
- 具体的なテストコマンドはプロジェクトの設定に従う
