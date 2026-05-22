---
name: coverage-report
description: "Generate code coverage reports. Supports Vitest (--unit-only), Playwright E2E (--e2e-only), and combined (default) modes. Outputs HTML + text-summary + LCOV reports. Includes automatic overlap analysis and coverage gap detection."
---

# Coverage Report

Generate code coverage reports via `coverage.mjs` directly.

## Usage

```
/coverage-report                    # Full run: Vitest + Playwright + merge (default)
/coverage-report --unit-only        # Vitest only (fast, no browser)
/coverage-report --e2e-only         # Playwright only (needs build)
```

**No args = full combined run.** Always runs both Vitest and Playwright with coverage
AND HTML test reporters enabled. No partial reports — all or nothing every time.
`--combined` is accepted but redundant (it's the default).

## Modes

### Combined mode (default)

Runs Vitest + Playwright coverage, then merges into a single report.
**This is the default** — ensures all three report directories always exist.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel)
cd "$REPO_ROOT" && node quality/scripts/coverage.mjs --combined [--skip-build]
# or merge existing reports only:
cd "$REPO_ROOT" && node quality/scripts/coverage-combine.mjs
```

Reports:
- `quality/reports/coverage/vitest/` — unit/integration coverage
- `quality/reports/coverage/playwright/` — E2E server-side coverage
- `quality/reports/coverage/combined/` — merged report (HTML via genhtml + LCOV)

### Unit-only mode (`--unit-only`)

Runs Vitest unit + integration tests with V8 coverage. Fast, no browser needed.

```bash
cd "$REPO_ROOT" && node quality/scripts/coverage.mjs --unit-only
```

Reports: `quality/reports/coverage/vitest/` (HTML + LCOV + text-summary)

### E2E-only mode (`--e2e-only`)

Starts the Next.js production server with `NODE_V8_COVERAGE`, runs Playwright
tests, then sends SIGTERM for a clean exit that flushes V8 coverage files.
Uses c8 to process the V8 data — source maps from `.next/server/chunks/ssr/`
map compiled code back to `src/` automatically.

```bash
cd "$REPO_ROOT" && node quality/scripts/coverage.mjs
```

Reports: `quality/reports/coverage/playwright/` (HTML + LCOV + text-summary)

**Note:** `--skip-build` skips the Next.js build if `.next/` already exists.

## Execution

Always run from the repo root. The scripts handle dependency installation
automatically (`@vitest/coverage-v8`, rollup native module).

Requires `genhtml` for the combined HTML report:
```bash
brew install lcov   # macOS
```

### Viewing reports (MANDATORY post-run step)

After the coverage script completes, **always** start a local HTTP server to serve
the reports directory. The Vitest HTML test report is a Vue SPA that requires HTTP
to load its data — `file://` URLs won't work.

```bash
npx serve quality/reports -p 7463 &
open http://localhost:7463/quality-report.html
```

This serves ALL reports (coverage, test reports, quality report) from one URL.
The server runs in the background on port 7463. Key URLs:
- `http://localhost:7463/quality-report.html` — quality summary (primary)
- `http://localhost:7463/coverage/index.html` — coverage index
- `http://localhost:7463/test-report-vitest/` — Vitest test report
- `http://localhost:7463/test-report-playwright/` — Playwright test report

### Quality report

Every run automatically generates `quality/reports/quality-report.html` via `quality-report-html.mjs`. It contains:

- **Test inventory** — all test files broken down by category (unit, hook, component, API/route, E2E) with file and test counts
- **Test quality analysis** — bullshit test detection: vacuous assertions, infra-YAML tests, CSS string tests, source file content assertions, static page copy tests
- **Complexity analysis** — cyclomatic complexity per function with risk categorization (LOW/MODERATE/HIGH/VERY HIGH), distribution chart, top 15 most complex functions, and auto-generated recommendations
- **Coverage summary** — lines/functions/branches for Vitest, Playwright, and Combined, parsed directly from LCOV files with correct numbers
- **Overlapping coverage** — automatically detected loki twin pairs, issue-numbered cluster files, and over-tested sources (BUILT-IN, no manual step needed)
- **Coverage gaps** — files below 20% coverage with >10 lines, sorted by coverage ascending, with risk labels (BUILT-IN)
- **Test reports** — links to Vitest and Playwright HTML test reports (when generated)

Can also be regenerated standalone (does NOT re-run tests, uses existing LCOV):

```bash
node quality/scripts/quality-report-html.mjs
```

### Complexity analysis (standalone)

Run cyclomatic complexity analysis independently (no tests needed):

```bash
node quality/scripts/complexity-analysis.mjs
```

Outputs:
- `quality/reports/complexity/complexity-report.json` — machine-readable per-function data
- `quality/reports/complexity/index.html` — standalone Fenrir-styled complexity report

The complexity data is automatically included in `quality-report.html` when available.
Risk categories: LOW (1-5), MODERATE (6-10), HIGH (11-20), VERY HIGH (21+).

---

## Overlap Analysis — Automatic

The HTML report automatically runs overlap analysis on every generation. No extra command needed. It detects:

### Loki Twin Pairs
Files where `foo.loki.test.ts` exists alongside `foo.test.ts`, both importing the same source module. Loki's edge cases belong in the parent file, not a permanent twin.

**Action:** Merge unique cases from loki twin into parent → delete loki file.

### Issue-Numbered Clusters
Files named `thing-1234.test.ts` or `thing-1234-loki.test.ts` that share the same base module. These are bug-fix branches that were never consolidated back into a canonical suite.

**Action:** Collapse all files in cluster → one `thing.test.ts` + one `thing-regressions.test.ts`.

### Over-Tested Sources
Source files with average LCOV hit count > 20× (already saturated by many callers). Every new test that primarily adds coverage here is wasted effort.

**Action:** Do not add more tests to these files.

### Coverage Gaps
Source files with > 10 lines and < 20% line coverage, sorted by coverage ascending with risk labelling (HIGH/MED/LOW). These are where new tests deliver real value.

**Action:** File issues for HIGH-risk gaps first.

---

## Post-Run Cull Prompt (MANDATORY)

After every `/coverage-report` run, you MUST:

**1. Read the cull list:**
```bash
cat quality/reports/cull-list.json
```

**2. Present the cull table** — render it as markdown in your response:

```
### 🗑️ Recommended Test Culls

N files · M tests (X% of suite) should be deleted. They do not test behaviour.

| # | File | Tests | Pattern |
|---|------|------:|---------|
| 1 | `path/to/file.test.ts` | 19 | Vacuous Assertions |
| 2 | `path/to/file.test.ts` | 49 | CSS String Assertions |
...

**File an issue to cull all N files in one shot? [yes / no]**
```

**3. Also present the overlap summary** from the HTML report sections:

```
### 🔀 Overlap Summary

| Problem | Files | Tests |
|---------|------:|------:|
| Loki twin pairs | N | ~M redundant |
| Issue-numbered clusters | N | M excess files |

**File a consolidation issue? [yes / no]**
```

**4. Wait for Odin's response.**

---

## If Odin Says YES (Bullshit Culls) — Cull Issue + Rule Hardening

Execute all three steps immediately without further prompting.

### Step A — File the GitHub Issue

```bash
gh issue create \
  --title "Delete N bullshit test files — hollow tests poisoning the suite" \
  --label "bug,normal" \
  --body "$(cat <<'EOF'
## Description

The quality report identified N test files (M total tests) that assert on static
text, config structure, or always-true conditions. These are not tests — they are
noise that inflates counts, breaks on refactors, and masks real coverage gaps.

## Files to Delete

<!-- paste the cull table here -->

## Acceptance Criteria

- [ ] All listed files deleted
- [ ] `npx vitest run` still green after deletion
- [ ] `quality/reports/quality-report.html` regenerated — bullshit count = 0

## Why These Were Written

These tests were generated by agents (Loki + FiremanDecko) before the banned
patterns were explicit enough. This issue also hardens the agent rules so they
cannot come back.

skip-refinement

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

Capture the issue number. Add to board:
```bash
SCRIPT_DIR="$(git rev-parse --show-toplevel)/.claude/skills/fire-next-up/scripts"
node "$SCRIPT_DIR/pack-status.mjs" --move <ISSUE_NUMBER> up-next
```

### Step B — Harden `.claude/agents/loki.md`

Read the flagged patterns from `cull-list.json`. For each pattern found, add a
**concrete, named example** to the "Banned Test Categories" section in `loki.md`.
The rule must name the pattern AND give a file-path example so future Loki instances
recognise it immediately.

Append under the existing "Banned Test Categories" block in `loki.md`:

```markdown
### Banned Pattern Examples (learned from cull — do NOT recreate)

The following pattern types were found in this repo and deleted. If you are about
to write something that looks like this, STOP. File a question on the issue instead.

- **Vacuous assertion** (`gke/gke-api-routes.test.ts`): `expect(true).toBe(true)`.
  Route structure is verified by running the server, not by asserting `true`.
- **Infrastructure YAML** (`gke/pod-disruption-budget.test.ts`): `readFileSync` on
  `pdb.yaml` + string asserts. Helm/K8s manifests are not code — don't test them.
- **CSS string assertion** (`chronicles/chronicle-agent-css.test.ts`): `readFileSync`
  on a `.css` file + `toContain('.some-class')`. CSS classes are not behaviour.
- **Source file content** (`chronicles/chronicle-1050-loki-qa.test.ts`): `readFileSync`
  on a `.ts` file + `toContain('functionName')`. This tests that you typed the code,
  not that the code works.
- **Static page copy** (`components/marketing-navbar.test.tsx`): `screen.getByText('Sign In')`.
  Copy changes. Section order changes. These tests break on copywriter edits.
```

Adapt the examples to the actual files that were culled in the current run.

### Step C — Harden `.claude/agents/fireman-decko.md`

Add a matching "Banned Test Patterns" section to `fireman-decko.md` under "Test Ownership":

```markdown
### Banned Test Patterns (UNBREAKABLE — do not write these)

Read `.claude/agents/loki.md` § "Banned Test Categories" for the full list.
The summary for implementation sessions:

- Never `readFileSync` a `.css`, `.yaml`, `.yml`, `.ts`, or `.mjs` file in a test
  and assert on its string content. That is not a test.
- Never write `expect(true).toBe(true)` or any tautological assertion.
- Never test Helm/K8s/Terraform YAML structure — it is config, not code.
- Never test marketing page copy, section order, or heading text.
- Never assert on CSS class names in rendered output.

If you're unsure whether a test is valid: ask yourself "would this test fail if I
introduced a logic bug but did not change any config or text?" If the answer is NO,
don't write it.
```

### Step D — Report back to Odin

```
**Cull Issue Filed:** #<N> — <title>
**Board:** Up Next

**Agent rules hardened:**
- `.claude/agents/loki.md` — added banned pattern examples with file references
- `.claude/agents/fireman-decko.md` — added banned test patterns section

These N test types are now explicitly documented with named examples from this
repo. Future agents will recognise the pattern before writing it.
```

---

## If Odin Says YES (Overlap Consolidation) — File Consolidation Issue

```bash
gh issue create \
  --title "Consolidate loki twin pairs and issue-numbered cluster files" \
  --label "chore,normal" \
  --body "$(cat <<'EOF'
## Description

The quality report identified overlapping test files that cover already-saturated
source modules. Consolidating them removes redundant test budget without losing
coverage.

## Loki Twins to Merge

<!-- List twin pairs: merge edge cases from .loki. file into parent, delete loki file -->

## Issue Clusters to Consolidate

<!-- List cluster files: collapse into canonical base file + regressions file -->

## Acceptance Criteria

- [ ] All loki twin files deleted (unique cases merged into parent)
- [ ] Issue-numbered files collapsed into canonical files
- [ ] `npx vitest run` still green after all changes
- [ ] `quality/reports/quality-report.html` regenerated — overlap twin count = 0

skip-refinement

---
Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

---

## If Odin Says NO

Acknowledge and move on. The cull list remains in `quality/reports/cull-list.json`
and the overlap data remains in `quality/reports/quality-report.html` for the next run.
Do not file the issue or modify the agent files.

## Styling the HTML report

Drop a custom CSS file at `quality/scripts/coverage.css`. It will be picked
up automatically by `coverage-combine.mjs` and passed to genhtml via
`--css-file`. The file completely replaces genhtml's default stylesheet.

genhtml's default classes to target: `coverFile`, `coverBar`, `coverPerHi`
(green), `coverPerMed` (yellow), `coverPerLo` (red), `title`, `tableHead`.

## How E2E coverage works

1. Next.js production build creates `.next/standalone/server.js` (standalone output mode).
2. Server starts via `node .next/standalone/server.js` with `NODE_V8_COVERAGE` + `PORT=9653`.
   Node writes raw V8 coverage JSON to `quality/.coverage-tmp/` on clean exit.
3. SIGTERM → server exits cleanly → coverage files written.
4. c8 reads V8 JSON and produces LCOV with `.next/server/app/` paths (source maps in compiled
   route files are empty — c8 cannot resolve back to `src/` automatically).
5. `normalizeLcov()` in `coverage.mjs` post-processes the playwright LCOV:
   - Remaps `.next/server/app/foo/route.js` → `src/app/foo/route.ts` (extension resolved
     from disk: `.tsx` → `.ts` → `.js` priority)
   - Drops `node_modules/` blocks entirely
6. `coverage-combine.mjs` merges Vitest + Playwright LCOVs — paths now align on `src/`
   so both sources contribute to the combined report.

### Line number accuracy

V8 coverage line numbers reflect the compiled `.js` file, not the TypeScript source.
File-level and function-level coverage is accurate; line-level detail may be off.
The combined report shows correct file coverage counts.

## Notes

- Reports are overwritten on every run (no dated directories)
- `quality/reports/` is in `.gitignore`
- `quality/.coverage-tmp/` is kept after each run for inspection (also gitignored)
- E2E coverage is server-side only — client-rendered components show 0% unless
  they also run server-side (RSC, API routes, middleware)
- `coverage-combine.mjs` can be run standalone to re-merge existing LCOV files
  without re-running tests
- `quality/reports/quality-report.md` must NOT exist — HTML only
