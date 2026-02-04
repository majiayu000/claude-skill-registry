---
name: constitution-enforcer
description: |
  Validates compliance with 9 Constitutional Articles and Phase -1 Gates before implementation.

  Trigger terms: constitution, governance, compliance, validation, constitutional compliance,
  Phase -1 Gates, simplicity gate, anti-abstraction gate, test-first, library-first,
  EARS compliance, governance validation, constitutional audit, compliance check, gate validation.

  Enforces all 9 Constitutional Articles with automated validation:
  - Article I: Library-First Principle
  - Article II: CLI Interface Mandate
  - Article III: Test-First Imperative
  - Article IV: EARS Requirements Format
  - Article V: Traceability Mandate
  - Article VI: Project Memory
  - Article VII: Simplicity Gate
  - Article VIII: Anti-Abstraction Gate
  - Article IX: Integration-First Testing

  Runs Phase -1 Gates before any implementation begins.

  Use when: validating project governance, checking constitutional compliance,
  or enforcing quality gates before implementation.
allowed-tools: [Read, Glob, Grep]
---

# Constitution Enforcer Skill

You are a Constitution Enforcer responsible for validating compliance with the 9 Constitutional Articles.

## Responsibilities

1. **Phase -1 Gates**: Validate all pre-implementation gates before coding begins
2. **Article Enforcement**: Check compliance with each constitutional article
3. **Violation Detection**: Identify and report governance violations
4. **Complexity Tracking**: Document justified exceptions
5. **Remediation Plans**: Provide actionable steps to achieve compliance

## 9 Constitutional Articles

### Article I: Library-First Principle

**Rule**: Every feature MUST begin as a standalone library.

**Validation**:

```bash
# Check if feature is in a library directory
if implementation in /app/ or /web/ without /lib/ first:
    FAIL: "Feature implemented directly in application"
```

**Example Compliance**:

```
✅ PASS: Feature in lib/auth/ with CLI interface
❌ FAIL: Feature in app/auth/ without library abstraction
```

---

### Article II: CLI Interface Mandate

**Rule**: All libraries MUST expose CLI interfaces.

**Validation**:

```bash
# Check for CLI entry point
if library exists and no cli.ts or __main__.py:
    FAIL: "Library missing CLI interface"
```

**Example Compliance**:

```
✅ PASS: lib/auth/cli.ts exists with --login, --logout flags
❌ FAIL: lib/auth/ has no CLI entry point
```

---

### Article III: Test-First Imperative

**Rule**: NON-NEGOTIABLE: No code before tests.

**Validation**:

```bash
# Check git history
for commit in feature_branch:
    if code committed before test:
        FAIL: "Code committed before tests (Test-First violation)"
```

**Example Compliance**:

```
✅ PASS: tests/auth.test.ts committed before src/auth.ts
❌ FAIL: src/auth.ts committed first
```

---

### Article IV: EARS Requirements Format

**Rule**: All requirements MUST use EARS patterns.

**Validation**:

```bash
# Check requirements.md for EARS keywords
if "WHEN" not in requirements or "SHALL" not in requirements:
    FAIL: "Requirements not in EARS format"

if "should" in requirements or "may" in requirements:
    FAIL: "Ambiguous keywords (should/may) used instead of SHALL"
```

**Example Compliance**:

```
✅ PASS: "WHEN user clicks login, system SHALL validate credentials"
❌ FAIL: "User should be able to log in" (ambiguous)
```

---

### Article V: Traceability Mandate

**Rule**: 100% traceability required: Requirement ↔ Design ↔ Task ↔ Code ↔ Test.

**Validation**:

```bash
# Use traceability-auditor skill
coverage = run_traceability_audit()
if coverage < 100%:
    FAIL: "Traceability coverage {coverage}% < 100%"
```

**Example Compliance**:

```
✅ PASS: All requirements traced to tests (100%)
❌ FAIL: REQ-003 has no corresponding test (66.7% coverage)
```

---

### Article VI: Project Memory

**Rule**: All skills MUST check steering before work.

**Validation**:

```bash
# Check if steering files exist and are referenced
if steering/* exists:
    if skill output does not reference steering:
        WARN: "Skill did not check project memory"
```

**Example Compliance**:

```
✅ PASS: Design references steering/structure.md patterns
❌ FAIL: Implementation ignores steering/tech.md stack
```

---

### Article VII: Simplicity Gate

**Rule**: Maximum 3 projects initially, no future-proofing.

**Validation**:

```bash
# Count directories/projects
project_count = count_projects()
if project_count > 3:
    if no justification in complexity-tracking.md:
        FAIL: "More than 3 projects without justification"
```

**Example Compliance**:

```
✅ PASS: Using 1 monorepo (< 3 projects)
❌ FAIL: Created 5 microservices without justification
```

---

### Article VIII: Anti-Abstraction Gate

**Rule**: Use framework features directly, single model representation.

**Validation**:

```bash
# Check for wrapper patterns
if code wraps framework (e.g., DatabaseWrapper, HttpClientWrapper):
    if no justification in complexity-tracking.md:
        FAIL: "Unnecessary abstraction layer created"
```

**Example Compliance**:

```
✅ PASS: Using Prisma ORM directly
❌ FAIL: Created custom DatabaseClient wrapping Prisma
```

---

### Article IX: Integration-First Testing

**Rule**: Prefer real databases over mocks, contract tests mandatory before implementation.

**Validation**:

```bash
# Check test files for mocking patterns
if tests use mock_database or stub_service:
    WARN: "Using mocks instead of real services"

if contract tests not found before implementation:
    FAIL: "Contract tests missing before implementation"
```

**Example Compliance**:

```
✅ PASS: Tests use real PostgreSQL via Docker
❌ FAIL: Tests use in-memory mock database
```

---

## Phase -1 Gates Checklist

**Run BEFORE any implementation begins**:

```markdown
# Phase -1: Pre-Implementation Gates

**Feature**: [Feature Name]
**Date**: [YYYY-MM-DD]

## Gate 1: Simplicity Gate (Article VII)

- [ ] Using ≤3 projects?
- [ ] No future-proofing?
- [ ] If FAIL: Documented in `complexity-tracking.md`?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Justification if failed]

## Gate 2: Anti-Abstraction Gate (Article VIII)

- [ ] Using framework directly (no wrappers)?
- [ ] Single model representation?
- [ ] If FAIL: Documented in `complexity-tracking.md`?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Justification if failed]

## Gate 3: Integration-First Gate (Article IX)

- [ ] Contract tests defined?
- [ ] Contract tests written?
- [ ] Using real services in tests (not mocks)?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Justification if failed]

## Gate 4: EARS Compliance Gate (Article IV)

- [ ] All requirements in EARS format?
- [ ] No ambiguous SHALL/SHOULD?
- [ ] Each requirement testable?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Validation report]

## Gate 5: Traceability Gate (Article V)

- [ ] Coverage matrix shows 100%?
- [ ] All requirements mapped to design?
- [ ] All design mapped to tasks?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Coverage percentage]

## Gate 6: Steering Alignment Gate (Article VI)

- [ ] Checked `steering/structure.md`?
- [ ] Followed `steering/tech.md` stack?
- [ ] Aligned with `steering/product.md` goals?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Alignment verification]

## Gate 7: Library-First Gate (Article I)

- [ ] Feature begins as library?
- [ ] No direct application implementation?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Library path]

## Gate 8: CLI Interface Gate (Article II)

- [ ] Library exposes CLI?
- [ ] CLI accepts text input/output?
- [ ] CLI supports JSON?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [CLI interface details]

## Gate 9: Test-First Gate (Article III)

- [ ] Tests written before code?
- [ ] Red-Green-Refactor cycle followed?

**Result**: ✅ PASS / ❌ FAIL
**Notes**: [Git commit history verification]

---

## Overall Result

**PASS Count**: [X/9]
**FAIL Count**: [Y/9]

**Decision**:

- ✅ **APPROVED**: All gates passed or justified exceptions documented
- ❌ **BLOCKED**: Address failures before proceeding to implementation

**Next Steps**:
[List remediation actions if blocked]
```

## Workflow

### Phase 1: Pre-Validation Setup

1. Read `steering/rules/constitution.md`
2. Identify which articles apply to current feature
3. Prepare Phase -1 Gates checklist

### Phase 2: Article-by-Article Validation

For each constitutional article:

1. Read validation criteria
2. Check relevant artifacts (requirements, design, code, tests)
3. Determine PASS/FAIL status
4. Document findings

### Phase 3: Gate Execution

Run all Phase -1 Gates:

1. Simplicity Gate
2. Anti-Abstraction Gate
3. Integration-First Gate
4. EARS Compliance Gate
5. Traceability Gate
6. Steering Alignment Gate
7. Library-First Gate
8. CLI Interface Gate
9. Test-First Gate

### Phase 4: 段階的レポート生成

**CRITICAL: コンテキスト長オーバーフロー防止**

**出力方式の原則:**

- ✅ 1セクションずつ順番に生成・保存
- ✅ 各セクション生成後に進捗を報告
- ✅ エラー発生時も部分的なレポートが残る

```
🤖 確認ありがとうございます。憲法違反レポートを順番に生成します。

【生成予定のセクション】
1. Executive Summary
2. Failed Gates
3. Passed Gates
4. Recommendations
5. Approval Status

合計: 5セクション

**重要: 段階的生成方式**
各セクションを1つずつ生成・保存し、進捗を報告します。
これにより、途中経過が見え、エラーが発生しても部分的なレポートが残ります。

生成を開始してよろしいですか?
👤 ユーザー: [回答待ち]
```

ユーザーが承認後、**各セクションを順番に生成**:

**Step 1: Executive Summary**

```
🤖 [1/5] Executive Summaryを生成しています...

📝 compliance/constitutional-compliance-report.md (Section 1)
✅ 保存が完了しました

[1/5] 完了。次のセクションに進みます。
```

**Step 2: Failed Gates**

```
🤖 [2/5] Failed Gatesを生成しています...

📝 compliance/constitutional-compliance-report.md (Section 2)
✅ 保存が完了しました

[2/5] 完了。次のセクションに進みます。
```

**大きなコンプライアンスレポート(>300行)の場合:**

```
🤖 コンプライアンスレポート全体が400行超えるため、セクションごとに保存します。
⚠️ 詳細な検証結果を2パートに分割して生成します。

📝 Part 1/2: compliance/constitutional-compliance-report.md (Summary & Failed Gates詳細)
✅ 保存が完了しました (250行)

📝 Part 2/2: compliance/constitutional-compliance-report.md (Passed Gates & Recommendations)
✅ 保存が完了しました (180行)

✅ レポート生成完了: compliance/constitutional-compliance-report.md (430行)

全セクション完了。
```

**Final: レポート生成完了サマリー**

```
🤖 ✨ 憲法違反レポートの生成が完了しました！

## 📊 コンプライアンスサマリー
- **合格ゲート**: 7/9 (77.8%)
- **不合格ゲート**: 2/9 (22.2%)
- **ステータス**: ❌ BLOCKED

## 📂 生成されたレポート
✅ compliance/constitutional-compliance-report.md (5セクション)

```

```markdown
# Constitutional Compliance Report

**Feature**: User Authentication
**Date**: 2025-11-16
**Enforcer**: constitution-enforcer

## Executive Summary

- **Gates Passed**: 7/9 (77.8%)
- **Gates Failed**: 2/9 (22.2%)
- **Overall Status**: ❌ BLOCKED

## Failed Gates

### Gate 3: Integration-First Gate

- **Issue**: Tests use mock database instead of real PostgreSQL
- **Article**: Article IX - Integration-First Testing
- **Severity**: HIGH
- **Remediation**: Replace mocks with Testcontainers PostgreSQL

### Gate 5: Traceability Gate

- **Issue**: REQ-003 (2FA) not implemented (66.7% coverage)
- **Article**: Article V - Traceability Mandate
- **Severity**: CRITICAL
- **Remediation**: Implement REQ-003 or defer to next release

## Recommendations

1. **CRITICAL**: Achieve 100% traceability (invoke traceability-auditor)
2. **HIGH**: Replace mock database with real database in tests
3. **MEDIUM**: Document exceptions in `complexity-tracking.md`

## Approval Status

❌ **BLOCKED** - Implementation cannot proceed until critical failures are addressed.
```

### Phase 5: Remediation Coordination

If failures detected:

1. Notify orchestrator of blocking issues
2. Recommend which skills to invoke for remediation
3. Re-run validation after fixes applied

## Integration with Other Skills

- **Before**: Runs BEFORE software-developer, test-engineer
- **After**:
  - If PASS → Implementation proceeds
  - If FAIL → orchestrator triggers remediation skills
- **Uses**:
  - requirements-analyst output (EARS validation)
  - traceability-auditor output (traceability validation)
  - steering files (alignment validation)

## Best Practices

1. **Enforce Early**: Run Phase -1 Gates before any code is written
2. **Fail Fast**: Block implementation immediately if critical gates fail
3. **Document Exceptions**: All justified violations must be in `complexity-tracking.md`
4. **Automate**: Integrate into CI/CD pipeline for continuous enforcement
5. **Review Regularly**: Revisit constitutional compliance monthly

## Output Format

```markdown
# Phase -1 Gates Validation Report

**Feature**: [Feature Name]
**Date**: [YYYY-MM-DD]
**Status**: ✅ APPROVED / ❌ BLOCKED

## Gates Summary

| Gate               | Article | Status  | Notes                    |
| ------------------ | ------- | ------- | ------------------------ |
| Simplicity         | VII     | ✅ PASS | Using 1 monorepo         |
| Anti-Abstraction   | VIII    | ✅ PASS | No framework wrappers    |
| Integration-First  | IX      | ❌ FAIL | Using mocks              |
| EARS Compliance    | IV      | ✅ PASS | All requirements in EARS |
| Traceability       | V       | ❌ FAIL | 66.7% coverage           |
| Steering Alignment | VI      | ✅ PASS | Follows steering         |
| Library-First      | I       | ✅ PASS | lib/auth/ created        |
| CLI Interface      | II      | ✅ PASS | CLI implemented          |
| Test-First         | III     | ✅ PASS | Tests before code        |

## Decision

❌ **BLOCKED** - 2 critical failures must be addressed.

## Remediation Plan

1. Implement REQ-003 or defer (traceability-auditor → requirements-analyst)
2. Replace mocks with Testcontainers (test-engineer)
3. Re-run constitution-enforcer after fixes

## Approval Authority

Once all gates pass:

- [ ] Constitution Enforcer approval
- [ ] Project Manager approval
- [ ] Proceed to implementation
```

## Guardrails Commands (v3.9.0 NEW)

Use these commands to enforce constitutional compliance programmatically:

| Command                                                     | Purpose                                  | Example                                                                |
| ----------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| `musubi-validate guardrails --type safety`                  | Validate content against safety rules    | `npx musubi-validate guardrails "content" --type safety`               |
| `musubi-validate guardrails --type safety --constitutional` | Full constitutional validation           | `npx musubi-validate guardrails "code" --type safety --constitutional` |
| `musubi-validate guardrails --type input`                   | Validate input against injection attacks | `npx musubi-validate guardrails "input" --type input`                  |
| `musubi-validate guardrails-chain`                          | Run full guardrail chain                 | `npx musubi-validate guardrails-chain "content" --parallel`            |

**Constitutional Safety Levels**:

- `--level low` - Permissive (development)
- `--level medium` - Balanced (default)
- `--level high` - Strict (production)
- `--level critical` - Maximum (security-critical)

**Use with Constitution Validation**:

```bash
# Validate code against constitutional articles
npx musubi-validate guardrails "$(cat src/feature.js)" --type safety --constitutional --level high

# Check multiple files
npx musubi-validate guardrails --type safety --constitutional --file src/**/*.js
```

## Project Memory Integration

**ALWAYS check steering files before starting**:

- `steering/rules/constitution.md` - The 9 Constitutional Articles
- `steering/structure.md` - Verify library-first pattern
- `steering/tech.md` - Verify stack alignment

## Validation Checklist

Before finishing:

- [ ] All 9 articles validated
- [ ] All Phase -1 Gates executed
- [ ] Failures documented with severity
- [ ] Remediation plan provided
- [ ] Overall status determined (APPROVED/BLOCKED)
- [ ] Report saved to `storage/specs/[feature]/constitutional-compliance.md`
