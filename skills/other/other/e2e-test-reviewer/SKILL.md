---
name: e2e-test-reviewer
description: Use when reviewing, auditing, or improving existing E2E test specs. Triggers on tasks like "review tests", "improve test quality", "audit specs", "check test scenarios". Detects naming-assertion mismatch, missing Then, error swallowing, always-passing assertions, boolean traps, conditional bypass, raw DOM queries, render-only tests, duplicate scenarios, misleading names, over-broad assertions, hard-coded timeouts, flaky selectors, and YAGNI violations in Page Objects.
---

# E2E Test Scenario Quality Review

Systematic checklist for reviewing E2E **spec files AND Page Object Model (POM) files**. Framework-agnostic principles; code examples show Playwright, Cypress, and Puppeteer where they differ.

## Phase 1: Automated Grep Checks (Run First)

Once the review target files are determined, run the following Bash commands **before** LLM analysis to mechanically detect known anti-patterns.

```bash
echo "=== E2E Mechanical Anti-Pattern Check ==="
echo ""

# 3. Error Swallowing — .catch(() => {}) / .catch(() => false)
echo "--- #3 Error Swallowing ---"
grep -rn '\.catch(\s*() =>' e2e/ --include='*.ts' --include='*.js' --include='*.cy.*' | grep -v node_modules | grep -v '// justified'

# 4. Always-Passing — assertion that can never fail
echo "--- #4 Always-Passing ---"
grep -rn -E 'toBeGreaterThanOrEqual\(0\)|should\(.*(gte|greaterThan).*0\)' e2e/ --include='*.ts' --include='*.js' --include='*.cy.*'

# 5. Boolean Trap — toBeTruthy / should be.truthy
echo "--- #5 Boolean Trap ---"
grep -rn -E 'expect\(.*\)\.toBeTruthy\(\)|should\(.*(be\.truthy|be\.true)\)' e2e/ --include='*.spec.*' --include='*.test.*' --include='*.cy.*'

# 6. Conditional Bypass — expect inside if(isVisible)
echo "--- #6 Conditional Bypass ---"
grep -rn -E "if.*(isVisible|is\(.*:visible.*\))" e2e/ --include='*.spec.*' --include='*.test.*' --include='*.cy.*'

# 7. Raw DOM — document.querySelector in spec/test files
echo "--- #7 Raw DOM in specs ---"
grep -rn 'document\.querySelector' e2e/ --include='*.spec.*' --include='*.test.*' --include='*.cy.*'

# 12. Hard-coded Timeout — waitForTimeout / cy.wait(number)
echo "--- #12 Hard-coded Timeout ---"
grep -rn -E 'waitForTimeout|cy\.wait\(\d' e2e/ --include='*.ts' --include='*.js' --include='*.cy.*'

echo ""
echo "=== Done ==="
```

**Interpreting results:**
- Zero hits → no mechanical issues found, proceed to Phase 2
- Any hit → report each line as an issue (includes file:line)
- Lines with `// justified` comments are excluded (intentional usage)

**Output Phase 1 results as-is.** The LLM must not reinterpret them.

---

## Phase 2: LLM Review (Subjective Checks Only)

Patterns already detected in Phase 1 (#3, #4, #5 partial, #6, #7, #12) are **skipped**.
The LLM performs only these checks:

| # | Check | Reason |
|---|-------|--------|
| 1 | Name-Assertion Alignment | Requires semantic interpretation |
| 2 | Missing Then | Requires logic flow analysis |
| 8 | Render-Only | Requires test value judgment |
| 9 | Duplicate Scenarios | Requires similarity comparison |
| 10 | Misleading Names | Requires semantic interpretation |
| 11 | Over-Broad Assertions | Requires domain context |
| 13 | Flaky Selectors (partial) | Requires nth() justification judgment |
| 14 | YAGNI in POM | Requires usage grep then judgment |

---

## Review Checklist

Run each check against every **non-skipped** test and every **changed POM file**.

**Important:** `test.skip()` with a reason comment or reason string is intentional — do NOT flag or remove these. Only flag mid-test conditional skips that hide failures (see #6).

---

### Tier 1 — High-Impact Bugs (always check)

#### 1. Name-Assertion Alignment `[LLM-only]`

**Symptom:** Test name promises something the assertions don't verify.

```typescript
// BAD — name says "status" but only checks visibility
test('should display paragraph status', () => {
  await expect(status).toBeVisible();  // no status content check
});
```

**Rule:** Every noun in the test name must have a corresponding assertion. Add it or rename.

#### 2. Missing Then `[LLM-only]`

**Symptom:** Test acts but doesn't verify the final expected state.

```typescript
// BAD — toggles but doesn't verify the dismissed state
test('should cancel edit on Escape', () => {
  await input.click();
  await page.keyboard.press('Escape');
  await expect(text).toBeVisible();
  // input still hidden?
});
```

**Rule:** For toggle/cancel/close actions, verify both the restored state AND the dismissed state.

#### 3. Error Swallowing `[grep-detectable]`

**Symptom (spec):** `try/catch` wrapping assertions — test passes on error.

**Symptom (POM):** `.catch(() => {})` or `.catch(() => false)` on awaited operations — caller never sees the failure.

```typescript
// BAD spec — silent pass
try { await expect(header).toBeVisible(); }
catch { console.log('skipped'); }

// BAD POM — caller thinks execution succeeded
await runningIndicator.waitFor({ state: 'detached' }).catch(() => {});
```

**Rule (spec):** Never wrap assertions in try/catch. Use `test.skip()` in `beforeEach` if the test can't run.

**Rule (POM):** Remove `.catch(() => {})` / `.catch(() => false)` from wait/assertion methods. If the operation can legitimately fail, the caller should decide how to handle it. Only keep catch for UI stabilization like `editor.click({ force: true }).catch(() => textArea.focus())`.

#### 4. Always-Passing Assertions `[grep-detectable]`

**Symptom:** Assertion that can never fail.

```typescript
// BAD — count >= 0 is always true
expect(count).toBeGreaterThanOrEqual(0);
```

**Rule:** Search for `toBeGreaterThanOrEqual(0)`, `toBeTruthy()` on always-truthy strings, `||` chains that accept defaults as valid.

#### 5. Boolean Trap Assertions `[grep-detectable]`

**Symptom (spec):** `expect(bool).toBe(true)` — failure message is just "expected false to be true".

**Symptom (POM):** Method returns `Promise<boolean>` instead of exposing an element handle — forces spec into boolean trap.

```typescript
// BAD — boolean return forces spec into trap
async isEditorVisible(index = 0): Promise<boolean> {
  return await paragraph.locator('code-editor').isVisible();
}
expect(await page.isEditorVisible(0)).toBe(true);
```

**Rule (spec):** Use the framework's built-in assertion instead of extracting a boolean first:
- **Playwright:** `await expect(locator).toBeVisible()`
- **Cypress:** `cy.get(selector).should('be.visible')`
- **Puppeteer:** `await page.waitForSelector(selector, { visible: true })`

**Rule (POM):** Expose the element handle (Locator / selector string) instead of returning `Promise<boolean>`. Let specs use framework assertions directly.

#### 6. Conditional Bypass (Silent Pass / Hidden Skip) `[grep-detectable]`

**Symptom:** `expect()` inside `if` block, or mid-test `test.skip()` — test silently passes when feature is broken.

```typescript
// BAD — if spinner never appears, assertion never runs
if (await spinner.isVisible()) {
  await expect(spinner).toBeHidden({ timeout: 5000 });
}
```

**Rule:** Every test path must contain at least one `expect()`. Move environment checks to `beforeEach` or declaration-level `test.skip()`.

#### 7. Raw DOM Queries (Bypassing Framework API) `[grep-detectable]`

**Symptom:** Test drops into raw `document.querySelector*` / `document.getElementById` via `evaluate()` when the framework's element lookup API could do the same job.

```typescript
// BAD — no auto-wait, returns stale boolean
const has = await page.evaluate((i) => {
  return !!document.querySelectorAll('.para')[i]?.querySelector('.result');
}, 0);
expect(has).toBe(true);
```

**Why it matters:** No auto-waiting, no retry, boolean trap, framework error messages lost.

**Rule:** Use the framework's element API instead of raw DOM:
- **Playwright:** `page.locator()` + web-first assertions
- **Cypress:** `cy.get()` / `cy.find()` — avoid `cy.window().then(win => win.document.querySelector(...))`
- **Puppeteer:** `page.$()` / `page.waitForSelector()` — avoid `page.evaluate(() => document.querySelector(...))`

Only use `evaluate`/`waitForFunction` when the framework API can't express the condition (`getComputedStyle`, cross-element DOM relationships). In POM, add a comment explaining why.

---

### Tier 2 — Quality Improvements (check when time permits)

#### 8. Render-Only Tests (Low E2E Value) `[LLM-only]`

**Symptom:** Test only calls `toBeVisible()` with no interaction or content assertion.

**Rule:** Add at least one of: content assertion (`not.toBeEmpty()`, `toContainText()`), count assertion (`toHaveCount(n)`), or sibling element assertion.

#### 9. Duplicate Scenarios (DRY) `[LLM-only]`

**Symptom:** Two tests share >70% of their steps with minor variations.

**Rule (within file):** Merge tests that differ only in setup or a single assertion. Use the richer verification set from both.

**Rule (cross-file):** After reviewing all files in scope, cross-check tests with similar names across different spec files. If test A in `feature-settings.spec.ts` is a subset of test B in `feature-form-validation.spec.ts`, delete A and strengthen B.

#### 10. Misleading Test Names (KISS) `[LLM-only]`

**Symptom:** Name implies UI interaction but test uses API/REST, or name implies feature X but tests feature Y.

**Rule:** If the test uses REST API, reload, or indirect methods, the name must make that explicit.

#### 11. Over-Broad Assertions (KISS) `[LLM-only]`

**Symptom:** Assertion too loose to catch regressions.

```typescript
// BAD — any string containing '%' passes
expect(content.includes('%')).toBe(true);
```

**Rule:** Prefer exact matches or explicit value lists over `.includes()` or loose regex when valid values are known and small.

#### 12. Hard-coded Timeouts `[grep-detectable]`

**Symptom:** `waitForTimeout()` or magic timeout numbers scattered across tests and POM.

```typescript
// BAD — arbitrary sleep
await page.waitForTimeout(2000);

// BAD — magic number, no explanation
await element.waitFor({ state: 'visible', timeout: 30000 });
```

**Rule:** Never use explicit sleep (`waitForTimeout` / `cy.wait(ms)`) — rely on framework auto-wait or retry mechanisms. For custom timeouts, extract named constants with comments explaining why the default isn't sufficient.

#### 13. Flaky Selectors `[LLM-only]`

**Symptom:** Positional selectors or unstable text that breaks across environments.

```typescript
// BAD — breaks if DOM order changes
await expect(items.nth(2)).toContainText('Settings');
```

**Rule:** Prefer `data-testid`, role-based, or attribute-based selectors over `nth()` or raw text. If `nth()` is unavoidable, add a comment. For text selectors, use regex with `i` flag or `hasText` filter.

#### 14. YAGNI in Page Objects `[LLM-only]`

**Symptom:** POM has locators/methods never referenced by any spec.

**Procedure:**
1. List all public members of each changed POM file
2. Grep each member across all test files and other POMs
3. Classify: USED / INTERNAL-ONLY (`private`) / UNUSED (delete)

**Common patterns:** Convenience wrappers (`clickEdit()` when specs use `editButton.click()`), getter methods (`getCount()` when specs use `toHaveCount()`), state checkers (`isEditMode()` when specs assert on elements directly), pre-built "just in case" locators.

**Rule:** Delete unused members. Make internal-only members `private`. Shared utils must be used by 2+ specs.

**Output:**
```
| File | Member | Used In | Status |
|------|--------|---------|--------|
| page.ts | addLinks | (none) | DELETE |
| page.ts | searchDialog | internal only | PRIVATE |
```

---

## Output Format

Present findings grouped by severity:

```markdown
## [HIGH/MEDIUM/LOW] Task N: [filename] — [issue type]

### N-1. `[test name or POM method]`
- **Issue:** [description]
- **Fix:** [name change / assertion addition / merge / deletion]
- **Code:**
  ```typescript
  // concrete code to add or change
  ```
```

**Severity guide:**
- **HIGH:** Error swallowing, always-passing, conditional bypass, raw DOM queries — tests that silently pass when broken
- **MEDIUM:** Boolean traps, missing Then, duplicates — tests that work but give poor diagnostics or waste CI time
- **LOW:** Render-only, naming, YAGNI, timeouts — quality/maintenance improvements

## Quick Reference

| # | Check | Tier | Phase | Detection Signal |
|---|-------|------|-------|-----------------|
| 1 | Name-Assertion | T1 | LLM | Noun in name with no matching `expect()` |
| 2 | Missing Then | T1 | LLM | Action without final state verification |
| 3 | Error Swallowing | T1 | grep | `try/catch` in spec, `.catch(() => {})` in POM |
| 4 | Always-Passing | T1 | grep | `>=0`, truthy on non-empty, `\|\|` defaults |
| 5 | Boolean Trap | T1 | grep | `expect(bool).toBe(true)`, POM returns boolean |
| 6 | Conditional Bypass | T1 | grep | `expect()` inside `if`, mid-test `test.skip()` |
| 7 | Raw DOM Queries | T1 | grep | `document.querySelector` in `evaluate` bypassing framework API |
| 8 | Render-Only | T2 | LLM | Only `toBeVisible()`, no content/count |
| 9 | Duplicate | T2 | LLM | >70% shared steps, cross-file overlap |
| 10 | Misleading Name | T2 | LLM | API/reload in "should [UI verb]" test |
| 11 | Over-Broad | T2 | LLM | `.includes()` where enum values known |
| 12 | Hard-coded Timeout | T2 | grep | `waitForTimeout()`, magic numbers |
| 13 | Flaky Selectors | T2 | LLM | `nth()` without comment, raw text matching |
| 14 | YAGNI in POM | T2 | LLM | Public member not referenced in any spec |

---

## Suppression

When a grep-detected pattern is intentional, add a `// justified: [reason]` comment to the line. Phase 1 will exclude it.

Example: `await editor.click({ force: true }).catch(() => textArea.focus()); // justified: UI stabilization fallback`
