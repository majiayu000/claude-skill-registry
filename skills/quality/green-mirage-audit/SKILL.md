---
name: green-mirage-audit
description: "Use when reviewing test suites, after test runs pass, or when user asks about test quality"
version: 1.0.0
---

# Green Mirage Audit

<ROLE>
Test Quality Auditor with Red Team instincts. Reputation depends on finding tests that pass but don't protect production.
</ROLE>

## Invariant Principles

1. **Passage Not Presence** - Test value = catching failures, not passing. Question: "Would broken code fail this?"
2. **Consumption Validates** - Assertions must USE outputs (parse, compile, execute), not just check existence
3. **Complete Over Partial** - Full object assertions expose truth; substring/partial checks hide bugs
4. **Trace Before Judge** - Follow test -> production -> return -> assertion path completely before verdict
5. **Evidence-Based Findings** - Every finding requires exact line, exact fix code, traced failure scenario

## Reasoning Schema

<analysis>
For each test:
1. CLAIM: What does name/docstring promise?
2. PATH: What code actually executes?
3. CHECK: What do assertions verify?
4. ESCAPE: What garbage passes this test?
5. IMPACT: What breaks in production?
</analysis>

<reflection>
Before concluding:
- Every test traced through production code?
- All 8 patterns checked per test?
- Each finding has line number + fix code + effort?
- Dependencies between findings identified?
</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Test files | Yes | Test suite to audit (directory or file paths) |
| Production files | Yes | Source code the tests are meant to protect |
| Test run results | No | Recent test output showing pass/fail status |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Audit report | File | YAML + markdown at `$SPELLBOOK_CONFIG_DIR/docs/<project-encoded>/audits/green-mirage-audit-<timestamp>.md` |
| Summary | Inline | Test counts, mirage counts, fix time estimate |
| Next action | Inline | Suggested `/fixing-tests [path]` invocation |

## 8 Green Mirage Patterns

| # | Pattern | Symptom | Question |
|---|---------|---------|----------|
| 1 | Existence vs Validity | `assert file.exists()`, `assert len(x) > 0` | Would garbage pass? |
| 2 | Partial Assertions | `assert 'SELECT' in query`, `in`, substring | What's NOT checked? |
| 3 | Shallow Matching | keyword present, structure unchecked | Broken syntax passes? |
| 4 | Lack of Consumption | Output never parsed/compiled/executed | Who validates content? |
| 5 | Mocking Reality | System-under-test mocked, not dependencies | Actual code runs? |
| 6 | Swallowed Errors | `except: pass`, unchecked return codes | Would exception fail test? |
| 7 | State Mutation | Side effect triggered, result unverified | State actually changed? |
| 8 | Incomplete Branches | Happy path only, no error/edge cases | Invalid input tested? |

## Execution Protocol

### Phase 1: Inventory
List all test files + production files + test counts before reading.
For 5+ files: consider parallel subagents per file.

### Phase 2: Line-by-Line Audit
Per test function:
```
**Test:** `test_name` (file:line)
**Setup:** [what, mocks introduced, concerns]
**Action:** [operation, code path traced]
**Assertions:** Line X: catches [Y] / misses [Z]
**Verdict:** SOLID | GREEN MIRAGE | PARTIAL
**Gap:** [scenario passing test, breaking production]
**Fix:** [exact code]
```

### Phase 3: Pattern Check
Every test against ALL 8 patterns. No exceptions.

### Phase 4: Cross-Test Analysis
- Untested functions/methods
- Untested error paths
- Edge cases (empty, max, boundary, concurrent)
- Test isolation issues (order dependency, shared state)

### Phase 5: Report (YAML + Human-Readable)

Output to: `$SPELLBOOK_CONFIG_DIR/docs/<project-encoded>/audits/green-mirage-audit-<YYYY-MM-DD>-<HHMMSS>.md`

```yaml
---
audit_metadata:
  timestamp: "ISO8601"
  test_files_audited: N
summary:
  total_tests: N
  solid: N
  green_mirage: N
  partial: N
patterns_found:
  pattern_1_existence_vs_validity: N
  # ... all 8
findings:
  - id: "finding-1"
    priority: critical|important|minor
    test_file: "path"
    test_function: "name"
    line_number: N
    pattern: N
    pattern_name: "Name"
    effort: trivial|moderate|significant
    depends_on: []
    blind_spot: "scenario"
    production_impact: "consequence"
remediation_plan:
  phases:
    - phase: 1
      name: "descriptive"
      findings: ["finding-1"]
      rationale: "why first"
  total_effort_estimate: "X hours"
---
```

Effort: trivial (<5min, single assertion) | moderate (5-30min, read prod code) | significant (30+min, new infrastructure)

### Phase 6: User Output
After writing file:
```
Report: [path]
Summary: X tests, Y mirages, Z fix time
Next: /fixing-tests [path]
```

## Anti-Patterns

<FORBIDDEN>
- Surface conclusions: "looks comprehensive", "good coverage"
- Vague findings: "should be more thorough", "consider adding"
- Missing specifics: no line numbers, no exact fix code
- Skipping: stopping before full audit, not tracing paths
</FORBIDDEN>

## Self-Check

Before completing:
- [ ] Every line of every test file read?
- [ ] Every test traced through production?
- [ ] Every test checked against all 8 patterns?
- [ ] Every finding has: exact line, exact fix, effort, depends_on?
- [ ] YAML block at START with all required fields?
- [ ] Remediation plan with dependency-ordered phases?

If ANY unchecked: STOP and go back.
