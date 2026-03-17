---
name: technical-debt-manager
description: Analyze repo for technical debt, research language-specific best practices, create prioritized GitHub issue
argument-hint: "[--focus area] [--label label-name]"
allowed-tools: Bash, Read, Glob, Grep, WebSearch, WebFetch, Task, AskUserQuestion
user-invocable: true
---

# Technical Debt Manager

Analyze current repo for technical debt by exploring codebase and researching version-specific best practices. Produces a single GitHub issue with prioritized checklist of findings rated across 4 axes (impact, effort, contagion, business alignment) with concrete, actionable fix descriptions and measurement recommendations.

## Arguments

Parse from `$ARGUMENTS`:

- **--focus:** Optional — Narrow analysis to specific area (e.g., `error-handling`, `tests`, `dependencies`, `architecture`). Default: full scan.
- **--label:** Optional — GitHub issue label. Default: `tech-debt`

---

## Workflow

### Phase 1: Repo Discovery

**1a. Detect language & framework:**

- Read project config files to identify stack:
  - `package.json`, `tsconfig.json` → TypeScript/JavaScript + framework (React, Next.js, Express, etc.)
  - `go.mod` → Go
  - `pyproject.toml`, `setup.py`, `requirements.txt` → Python + framework
  - `Cargo.toml` → Rust
  - `Gemfile` → Ruby
  - `pom.xml`, `build.gradle` → Java/Kotlin
  - `mise.toml`, `.tool-versions` → Additional tool hints
- Identify test framework, linter, formatter from config
- Note monorepo structure if applicable

**1b. Codebase overview:**

- `Glob` for directory structure (top 2 levels)
- Count files per language
- Identify entry points, main modules
- Check for CI/CD config (`.github/workflows/`, `Makefile`, etc.)

**1c. Check existing debt tracking:**

- Search for existing `tech-debt` labeled issues: `gh issue list --label tech-debt --state open`
- Read CLAUDE.md, README, CONTRIBUTING for known debt/conventions
- Note any existing TODO/FIXME/HACK conventions

### Phase 2: Research Modern Practices

**2a. Detect specific versions:**

- Extract language VERSION from config (e.g., `"engines": {"node": ">=20"}`, `go 1.22` in go.mod, `python_requires` in pyproject.toml)
- Extract framework VERSION (e.g., `"react": "^18.2"`, `"next": "14.1"`)
- Note: version-specific best practices differ significantly (e.g., Go 1.22 vs 1.18, React 18 vs 17)

**2b. Monorepo handling:**

- If monorepo detected (multiple `package.json`, workspace config, `apps/` + `packages/`), research separately per app/package
- Note shared dependencies and cross-package patterns

**2c. Use WebSearch to find current best practices for detected language/framework.**

Search queries (adapt to detected stack — include detected version):

- `"{language} {version} best practices {year}" maintainable code`
- `"{framework} {version} common anti-patterns {year}"`
- `"{language} {version} migration guide" breaking changes` (if version is behind latest)
- `"{language} code architecture patterns {year}"`
- `"{language} technical debt indicators checklist"`
- `"{language} dependency management best practices {year}"`

**Extract from research:**

- Current idiomatic patterns for the **specific language version** in use
- Common anti-patterns specific to the **framework version**
- Version-specific deprecations (are they using deprecated APIs for their version?)
- Recommended project structure
- Error handling conventions
- Testing best practices
- Dependency management guidelines
- Performance pitfalls

**Save research summary internally for Phase 3 comparison.**

### Phase 3: Codebase Analysis

Run analysis across these categories. For each finding, record: file:line, description, why it matters, fix approach.

**3a. Code Quality (SATD & Complexity)**

- Search for `TODO`, `FIXME`, `HACK`, `XXX`, `WORKAROUND` comments with `Grep`
  - Extract 3 lines context around each match
  - Classify severity: `TODO` (low) → `FIXME` (medium) → `HACK` (high) → `XXX` (critical)
  - Check age via `git blame` on flagged lines — older = higher priority
  - Group by theme clusters (e.g., "error handling TODOs", "performance FIXMEs")
- Identify dead code: unused exports, unreachable branches, commented-out code blocks
- Find overly complex functions (deeply nested, very long)
- Detect code duplication patterns
- Check error handling: bare catches, swallowed errors, missing error propagation
- Compare patterns found against Phase 2 research findings

> **Pattern Heuristics (Grep-able):**
>
> - Bare exception handlers: `except:`, `catch {}`, `catch(Exception`, `catch (...)`
> - Swallowed errors: empty catch blocks (catch + next line is `}`)
> - God objects: files >1000 lines with many public methods/exports
> - Commented-out code: `// ` followed by valid syntax patterns across 3+ consecutive lines
> - Deep nesting: 4+ levels of indentation in control flow

**3b. Architecture**

- Check for circular dependencies or tightly coupled modules
- Identify inconsistent patterns (e.g., mixed async styles, inconsistent naming)
- Look for missing abstractions (repeated boilerplate across files)
- Verify separation of concerns (business logic vs infrastructure)
- Compare project structure against language-specific recommendations from Phase 2

> **Pattern Heuristics (Grep-able):**
>
> - Mixed async: `Promise` + `callback` in same module, `.then()` + `async/await` mixed
> - Circular imports: mutual import chains (A→B→A)
> - Feature envy: functions accessing another module's internals more than their own
> - Barrel file bloat: re-export files >50 entries

**3c. Dependencies**

- Check for outdated dependencies: `gh api repos/{owner}/{repo}/dependabot/alerts` or manual check
- Look for unused dependencies (imported but not used in code)
- Identify pinning issues (too loose or too strict version ranges)
- Check for deprecated packages
- Compare against Phase 2 dependency management recommendations

> **Pattern Heuristics (Grep-able):**
>
> - Version pin extremes: `"*"`, `"latest"`, or exact pins without range (`"1.2.3"` vs `"^1.2.3"`)
> - Duplicate dependency: same lib in multiple package managers or lock files
> - Vendored copies: lib source copied into `vendor/` or `lib/` that's also in deps

**3d. Testing**

- Identify untested modules (no corresponding test file)
- Check test quality: look for tests without assertions, overly mocked tests
- Find flaky test indicators (sleep, timing-dependent, order-dependent)
- Check for missing edge case coverage (error paths, boundary conditions)
- Compare test patterns against Phase 2 testing best practices

> **Pattern Heuristics (Grep-able):**
>
> - Tests without assertions: `test(` or `it(` blocks without `assert`/`expect`/`should`
> - Sleep-based tests: `time.Sleep`, `setTimeout`, `sleep(` in test files
> - Overly mocked: test files where mock count > assertion count

**3e. DevOps & Tooling**

- Linter/formatter configured and matching language standards?
- CI pipeline running all quality gates?
- Pre-commit hooks in place?
- Security scanning configured?

> **Pattern Heuristics (Grep-able):**
>
> - Missing lint step: CI config without `lint`, `check`, or `fmt` step
> - No lockfile: `package.json` without `package-lock.json`/`yarn.lock`/`pnpm-lock.yaml`
> - Hardcoded CI versions: pinned action versions without Dependabot/Renovate for updates

**3f. Documentation Debt**

- Compare doc comments vs actual function signatures — outdated params, return types
- Find stub docs: `@param x - x parameter`, `@returns the result`, auto-generated placeholders
- Check for missing error documentation (thrown exceptions, error return values)
- Identify public API surface without usage examples
- README accuracy: does it match current setup steps, config, and features?

> **Pattern Heuristics (Grep-able):**
>
> - Stub `@param`: `@param \w+ - \w+ parameter` or `@param \w+ - the \w+`
> - Stub `@returns`: `@returns the result`, `@returns {void}`
> - Missing doc on exports: `export (function|class|const)` without preceding `/**`
> - Stale README commands: `npm start` / `go run` in README that don't match `package.json` scripts or `Makefile`

**3g. Security Debt**

- Bare exception handlers that swallow security-relevant errors
- Hardcoded secrets patterns: API keys, tokens, passwords in source
- Unvalidated inputs at system boundaries (HTTP handlers, CLI args, file reads)
- Known CVE patterns in dependencies (cross-reference with `gh api repos/{owner}/{repo}/dependabot/alerts`)
- Missing rate limiting, auth checks, or CORS configuration

> **Pattern Heuristics (Grep-able):**
>
> - Hardcoded secrets: `password\s*=\s*"`, `api_key\s*=\s*"`, `token\s*=\s*"`, `secret\s*=\s*"`
> - SQL injection: string concatenation in queries (`"SELECT.*" \+`, f-strings with SQL)
> - Insecure random: `Math.random()` in security context, `rand.Intn` without crypto/rand
> - Disabled TLS verification: `InsecureSkipVerify`, `verify=False`, `NODE_TLS_REJECT_UNAUTHORIZED`

**If `--focus` specified:** Only run the matching sub-phase (3a-3g).

### Phase 4: Prioritize Findings

Rate each finding on 4 axes:

| Rating | Impact | Effort | Contagion | Business Alignment |
|--------|--------|--------|-----------|-------------------|
| **High** | Causes bugs, security risk, blocks features | >1 day, architectural change | Foundational — touches architecture, affects many modules | Blocks product goals, compliance, or release velocity |
| **Medium** | Degrades DX, slows development, tech debt compounds | Hours, localized change | Spreads — affects 2-5 modules or shared patterns | Slows feature delivery but doesn't block |
| **Low** | Style, minor inconsistency, nice-to-have | Minutes, simple fix | Isolated — contained to 1 module | No direct business impact |

> **Contagion** (from Riot Games tech debt taxonomy): How far does this debt spread? Isolated debt in a single module is less urgent than foundational debt baked into architecture that every new feature inherits.
>
> **Business Alignment**: Does fixing this unblock product goals, compliance requirements, or improve release velocity? Debt aligned with business priorities gets promoted.

**Priority matrix:**

- 🔴 **Critical Path Block:** High impact + High contagion → Do first even if high effort (architectural rot spreads)
- 🔴 **Quick Wins:** High impact + Low effort + Low contagion → Do immediately
- 🟠 **Strategic:** High impact + High effort → Plan & schedule, consider business alignment for ordering
- 🟡 **Velocity Improvers:** Medium impact + Low effort + reduces dev friction → Batch together
- ⚪ **Backlog:** Low impact or high contagion with unresolved upstream deps → Track, do opportunistically

### Phase 5: Create GitHub Issue

**5a. Verify repo has GitHub remote:**

- `gh repo view --json nameWithOwner -q .nameWithOwner`
- If no remote, save as local markdown file instead: `./findings/tech-debt/debt-report-{date}.md`

**5b. Check for existing label:**

- `gh label list --search tech-debt`
- If missing: `gh label create tech-debt --description "Technical debt items" --color "D93F0B"`

**5c. Create issue with this structure:**

```markdown
Title: Tech Debt Audit: {repo-name} ({date})

Body:
## 📊 Tech Debt Audit

**Repo:** {repo-name}
**Stack:** {language} / {framework}
**Date:** {date}
**Scope:** {full | focused area}

## 🔬 Research Context

Key best practices for {language}/{framework} ({year}):
- {Practice 1 — compared against codebase}
- {Practice 2 — compared against codebase}
- {Practice 3 — compared against codebase}

Sources: {URLs from Phase 2}

## 🔴 Critical Path Blocks (High Impact, High Contagion)

- [ ] **{Finding title}** — `file:line` or module-level
  Impact: {why this matters}
  Contagion: {how far it spreads}
  Fix: {concrete approach with specific code reference}
  Effort: {what's involved}

## 🔴 Quick Wins (High Impact, Low Effort, Low Contagion)

- [ ] **{Finding title}** — `file:line`
  Impact: {why this matters}
  Fix: {concrete approach — see actionability examples below}
  Ref: {link to best practice if applicable}

## 🟠 Strategic (High Impact, High Effort)

- [ ] **{Finding title}** — `file:line` or module-level
  Impact: {why this matters}
  Business Alignment: {blocks what goal?}
  Fix: {approach + considerations}
  Effort: {what's involved}

## 🟡 Velocity Improvers (Medium Impact, Low Effort)

- [ ] **{Finding title}** — `file:line`
  Fix: {concrete approach}
  DX Gain: {what dev friction it removes}

## ⚪ Backlog

- [ ] **{Finding title}** — {brief description}

## 📈 Summary

| Category | Items | Critical | Quick Wins | Strategic | Velocity | Backlog |
|----------|-------|----------|------------|-----------|----------|---------|
| Code Quality | N | N | N | N | N | N |
| Architecture | N | N | N | N | N | N |
| Dependencies | N | N | N | N | N | N |
| Testing | N | N | N | N | N | N |
| DevOps | N | N | N | N | N | N |
| Documentation | N | N | N | N | N | N |
| Security | N | N | N | N | N | N |

**Recommended next action:** {Single most impactful thing to do first}
```

**5d. Create the issue:**

```bash
gh issue create --title "Tech Debt Audit: {repo} ({date})" --label tech-debt --body "..."
```

### Phase 6: Measurement Recommendations

Include the following "Measurement" section in the issue body (after the Summary table):

```markdown
## 📏 Measurement & Tracking

### Baseline Metrics (from this audit)
- Total findings: {count}
- Critical/Quick Win ratio: {critical+quick_wins}/{total}
- Categories with most debt: {top 2-3 categories}
- Estimated total effort: {rough sum}

### Re-audit Cadence
- **Quarterly:** Full re-audit recommended (run this skill again)
- **Monthly:** Spot-check top 3 priority items
- **Per-sprint:** Address at least 1 quick win

### KPIs to Track
- **Complexity trend:** Average cyclomatic complexity per module (should decrease)
- **Bug density:** Bugs per KLOC in debt-heavy modules vs clean modules
- **Release frequency:** Time between deployments (debt reduction should improve)
- **SATD count:** Total TODO/FIXME/HACK comments (should decrease quarterly)
- **Dependency freshness:** % of deps within 1 major version of latest
```

### Phase 7: Summary

Display in chat:

```
✅ Tech debt audit complete

Issue: {issue-url}
Findings: {total-count}
  🔴 Critical + Quick wins: {count}
  🟠 Strategic: {count}
  🟡 Velocity improvers: {count}
  ⚪ Backlog: {count}

Top recommendation: {single most impactful action}
```

---

## Error Handling

- **No GitHub remote:** Save report as `./findings/tech-debt/debt-report-{date}.md` instead
- **No findings:** Create issue noting clean audit, mention practices verified
- **Rate limited on web search:** Proceed with codebase analysis only, note limited research in issue
- **Very large repo:** Focus on src/lib/app directories, skip vendor/generated/node_modules
- **`--focus` area not applicable:** Inform user, suggest valid areas for this repo

## Actionability Standard

Every finding's "Fix" field must be specific enough for a developer to implement without guessing.

**Bad examples:**

- ❌ "Improve error handling"
- ❌ "Refactor this module"
- ❌ "Add better tests"
- ❌ "Consider using a different approach"

**Good examples:**

- ✅ "Replace bare `except:` at `src/api.py:42` with `except ValueError as e: logger.error(f'Invalid input: {e}')`"
- ✅ "Extract `parseConfig()` from `main.go:120-185` into `pkg/config/parser.go` — currently 65 lines with 4 nested ifs"
- ✅ "Add missing `t.Parallel()` to `TestUserCreate` at `user_test.go:28` — currently runs sequentially, blocking CI"
- ✅ "Pin `lodash` from `*` to `^4.17.21` in `package.json:15` — wildcard allows breaking changes"

**Litmus test:** Can a developer implement the fix within 2 days without architectural redesign? If no, break into smaller items.

## Quality Checklist

Before creating issue:

- [ ] Language and framework correctly identified (including version)
- [ ] Web research completed with current-year sources
- [ ] Every finding has file:line reference (or module-level for architecture)
- [ ] Every finding has concrete fix approach (passes actionability standard above)
- [ ] All 4 priority axes rated (Impact, Effort, Contagion, Business Alignment)
- [ ] Findings grouped by priority matrix
- [ ] Summary table counts are accurate
- [ ] No duplicate findings
- [ ] Research context section links findings to best practices
- [ ] Each fix is implementable within 2 days (or broken into sub-items)
- [ ] Security findings prioritized regardless of effort
