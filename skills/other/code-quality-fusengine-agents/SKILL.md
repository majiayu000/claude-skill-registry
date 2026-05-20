---
name: code-quality
description: Code quality validation with linters, SOLID principles, DRY detection, error detection, and architecture compliance across all languages.
argument-hint: "[file-or-directory]"
user-invocable: true
---

# Code Quality Skill

## 🚨 MANDATORY 7-PHASE WORKFLOW

```
PHASE 1: Exploration (explore-codebase) → BLOCKER
PHASE 2: Documentation (research-expert) → BLOCKER
PHASE 3: Impact Analysis (Grep usages) → BLOCKER
PHASE 3.5: DRY Detection (jscpd duplication) → NON-BLOCKING
PHASE 4: Error Detection (linters)
PHASE 5: Precision Correction (with docs + impact + DRY)
PHASE 6: Verification (re-run linters, tests, duplication)
```

**CRITICAL**: Phases 1-3 are BLOCKERS. Never skip them.
**DRY**: Phase 3.5 is non-blocking but findings inform Phase 5 corrections.

---

## PHASE 1: Architecture Exploration

**Launch explore-codebase agent FIRST**:
```
> Use Task tool with subagent_type="explore-codebase"
```

**Gather**:
1. Programming language(s) detected
2. Existing linter configs (.eslintrc, .prettierrc, pyproject.toml)
3. Package managers and installed linters
4. Project structure and conventions
5. Framework versions (package.json, go.mod, Cargo.toml)
6. Architecture patterns (Clean, Hexagonal, MVC)
7. State management (Zustand, Redux, Context)
8. Interface/types directories location

---

## PHASE 2: Documentation Research

**Launch research-expert agent**:
```
> Use Task tool with subagent_type="research-expert"
> Request: Verify [library/framework] documentation for [error type]
> Request: Find [language] best practices for [specific issue]
```

**Request for each error**:
- Official API documentation
- Current syntax and deprecations
- Best practices for error patterns
- Version-specific breaking changes
- Security advisories
- Language-specific SOLID patterns

---

## PHASE 3: Impact Analysis

**For EACH element to modify**: Grep usages → assess risk → document impact.

| Risk | Criteria | Action |
|------|----------|--------|
| 🟢 LOW | Internal, 0-1 usages | Proceed |
| 🟡 MEDIUM | 2-5 usages, compatible | Proceed with care |
| 🔴 HIGH | 5+ usages OR breaking | Flag to user FIRST |

---

## PHASE 3.5: Code Duplication Detection (DRY)

**Tool**: `jscpd` — 150+ languages — `npx jscpd ./src --threshold 5 --reporters console,json`

| Level | Threshold | Action |
|-------|-----------|--------|
| 🟢 Excellent | < 3% | No action needed |
| 🟡 Good | 3-5% | Document, fix if time |
| 🟠 Acceptable | 5-10% | Extract shared logic |
| 🔴 Critical | > 10% | Mandatory refactoring |

See [references/duplication-thresholds.md](references/duplication-thresholds.md) for per-language thresholds, config, and extraction patterns.
See [references/linter-commands.md](references/linter-commands.md) for language-specific jscpd commands.

---

## Linter Commands
See [references/linter-commands.md](references/linter-commands.md) for language-specific commands.

---

## Error Priority Matrix

| Priority | Type | Examples | Action |
|----------|------|----------|--------|
| **Critical** | Security | SQL injection, XSS, CSRF, auth bypass | Fix IMMEDIATELY |
| **High** | Logic | SOLID violations, memory leaks, race conditions | Fix same session |
| **High** | DRY | Code duplication > 10%, copy-paste logic blocks | Mandatory refactoring |
| **Medium** | DRY | Code duplication 5-10%, repeated patterns | Extract shared logic |
| **Medium** | Performance | N+1 queries, deprecated APIs, inefficient algorithms | Fix if time |
| **Low** | Style | Formatting, naming, missing docs | Fix if time |

---

## SOLID Validation
See [references/solid-validation.md](references/solid-validation.md) for S-O-L-I-D detection patterns and fix examples.

---

## File Size Rules
See [references/file-size-rules.md](references/file-size-rules.md) for LoC limits, calculation, and split strategies.

---

## Architecture Rules
See [references/architecture-patterns.md](references/architecture-patterns.md) for project structures and patterns.

---

## Validation Report Format
See [references/validation-report.md](references/validation-report.md) for the complete sniper report template.

---

## Complete Workflow Example
See [references/examples.md](references/examples.md) for detailed walkthrough.

---

## Forbidden Behaviors

### Workflow Violations
- ❌ Skip PHASE 1 (explore-codebase)
- ❌ Skip PHASE 2 (research-expert)
- ❌ Skip PHASE 3 (impact analysis)
- ❌ Skip PHASE 3.5 (DRY detection)
- ❌ Jump to corrections without completing Phases 1-3
- ❌ Proceed when BLOCKER is active

### Code Quality Violations
- ❌ Leave ANY linter errors unfixed
- ❌ Apply fixes that introduce new errors
- ❌ Ignore SOLID violations
- ❌ Ignore DRY violations > 5% duplication
- ❌ Copy-paste code instead of extracting shared logic
- ❌ Create tests if project has none

### Architecture Violations
- ❌ Interfaces in component files (ZERO TOLERANCE)
- ❌ Business logic in components (must be in hooks)
- ❌ Monolithic components (must section)
- ❌ Files >100 LoC without split
- ❌ Local state for global data (use stores)

### Safety Violations
- ❌ High-risk changes without user approval
- ❌ Breaking backwards compatibility silently
- ❌ Modifying public APIs without deprecation
