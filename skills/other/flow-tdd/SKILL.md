---
name: flow-tdd
description: "Enforces TDD Iron Law in flow-dev. NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST."
---

# Flow TDD - Test-Driven Development Enforcement

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

This is NON-NEGOTIABLE. No exceptions. No "just this once."

## The TDD Cycle

```
RED:    Write a failing test
        → Run it
        → Confirm it FAILS
        → If it passes immediately → ERROR (invalid test)

GREEN:  Write minimal code to pass
        → Only enough to make the test pass
        → No extra features
        → No "while I'm here" additions

REFACTOR: Clean up
        → Keep tests green
        → Improve structure
        → Remove duplication
```

## Enforcement in flow-dev

### Phase 2: Tests First

```yaml
TASKS.md Phase 2 (Tests):
  - Write contract tests
  - Write integration tests
  - Write unit tests
  - Run all tests → ALL MUST FAIL

⚠️ TEST VERIFICATION CHECKPOINT:
  → Run: npm test (or equivalent)
  → Expected: All new tests FAIL
  → If any test passes immediately → STOP
  → Passing test = invalid test or code already exists
```

### Phase 3: Implementation

```yaml
TASKS.md Phase 3 (Implementation):
  - Implement to make tests pass
  - One test at a time
  - Minimal code only

After each implementation:
  → Run tests
  → Verify previously failing test now passes
  → Verify no regressions
```

## What If Code Already Exists?

If you've written code before tests:

```yaml
Option A: DELETE AND RESTART (Recommended)
  1. Delete the implementation code
  2. Keep only the interface/contract
  3. Write failing tests
  4. Re-implement with TDD

Option B: WRITE TESTS THAT FAIL FIRST
  1. Comment out the implementation
  2. Write tests
  3. Run tests → verify they fail
  4. Uncomment implementation
  5. Run tests → verify they pass

NEVER: Keep code and write passing tests
  → This is "testing after" disguised as TDD
  → Tests that pass immediately prove nothing
```

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Too simple to test" | Simple code breaks. Test takes 30 seconds. |
| "I'll test after" | Tests passing immediately prove nothing. |
| "Tests after achieve same goals" | Tests-after = "what does this do?" Tests-first = "what should this do?" |
| "Already manually tested" | Ad-hoc ≠ systematic. No record, can't re-run. |
| "Deleting X hours is wasteful" | Sunk cost fallacy. Keeping unverified code is technical debt. |
| "Keep as reference, write tests first" | You'll adapt it. That's testing after. Delete means delete. |
| "Need to explore first" | Fine. Throw away exploration, start with TDD. |
| "Test hard = design unclear" | Listen to test. Hard to test = hard to use. |
| "TDD slows me down" | TDD faster than debugging. Pragmatic = test-first. |
| "This is different because..." | No. This is rationalization. Follow the law. |
| "Spirit not letter" | Violating letter IS violating spirit. No loopholes. |
| "I'm being pragmatic, not dogmatic" | TDD IS pragmatic. Shortcuts = debugging in production = slower. |
| "Just this once" | No exceptions. Rules exist for this exact moment. |

## Red Flags - STOP

If you find yourself:
- Writing code before tests
- Tests passing immediately
- Saying "just this once"
- Keeping "exploration" code
- Writing tests that describe existing code

**STOP. Delete the code. Write the test first.**

## Test Quality Requirements

```yaml
Good Tests:
  ✅ Test behavior, not implementation
  ✅ Use realistic data
  ✅ Cover edge cases
  ✅ Independent (no shared state)
  ✅ Fast (< 1 second each)
  ✅ Descriptive names

Bad Tests (Cheater Tests):
  ❌ assert True
  ❌ assert result is not None
  ❌ Mock everything, test nothing
  ❌ Test implementation details
  ❌ Depend on execution order
```

## Error Recording Protocol

当测试失败或构建错误发生时，必须立即记录到 ERROR_LOG.md:

```yaml
Error Recording Workflow:
  1. Capture Error Context:
     - Phase (flow-dev / T###)
     - Error Type (Test Failure | Build Error | Runtime Error)
     - Full error message
     - Timestamp

  2. Create ERROR_LOG.md if not exists:
     → Use .claude/docs/templates/ERROR_LOG_TEMPLATE.md
     → Location: devflow/requirements/${REQ_ID}/ERROR_LOG.md

  3. Append Error Record:
     ## [TIMESTAMP] E###: TITLE
     **Phase**: flow-dev / T###
     **Error Type**: Test Failure
     **Error Message**:
     ```
     [完整错误信息]
     ```
     **Root Cause**: [分析后填写]
     **Resolution**: [解决后填写]
     **Prevention**: [可选]

  4. Debug with Error Context:
     → Read ERROR_LOG.md for similar past errors
     → Apply attention refresh (Protocol 4)
     → Fix the root cause, not symptoms

  5. Update Record After Fix:
     → Fill Root Cause
     → Fill Resolution
     → Add Prevention if applicable
```

### Error Recording Example

```markdown
## [2026-01-08T14:30:00] E001: Test Failure - User Login Validation

**Phase**: flow-dev / T005
**Error Type**: Test Failure
**Error Message**:
\`\`\`
FAIL src/auth/login.test.ts
  × should reject invalid email format
    Expected: false
    Received: true
\`\`\`

**Root Cause**: 正则表达式 `/^.+@.+$/` 过于宽松，接受了 `user@` 这样的无效邮箱
**Resolution**: 更新正则为 `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` 要求至少有域名和顶级域
**Prevention**: 扩充测试用例，添加边界情况（无域名、无顶级域、特殊字符等）
```

## Integration with Constitution

- **Article I**: Complete implementation includes tests
- **Article VI**: TDD Mandate (this skill)
- **Article IX**: Integration-first testing

## Integration with Attention Refresh

- **Protocol 4**: Error Recovery 时读取 ERROR_LOG.md
- 避免重复犯相同错误
- 从历史错误中学习

## Cross-Reference

- [flow-attention-refresh](../flow-attention-refresh/SKILL.md) - Protocol 4
- [ERROR_LOG_TEMPLATE.md](../../docs/templates/ERROR_LOG_TEMPLATE.md)
- [rationalization-library.md](../../rules/rationalization-library.md#article-vi-test-first-development---rationalization-table)
- [project-constitution.md](../../rules/project-constitution.md#article-vi-test-first-development-测试优先开发)

---

**[PROTOCOL]**: 变更时更新此头部，然后检查 CLAUDE.md
