---
name: ln-162-skill-reviewer
description: "Universal skill reviewer: SKILL mode (D1-D9 + M1-M5) or COMMAND mode (.claude/commands review)"
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# ln-162-skill-reviewer

**Type:** L3 Worker (standalone-capable)
**Category:** 1XX Documentation Pipeline
**Coordinator:** ln-160-docs-skill-extractor (optional)

Universal skill reviewer with two auto-detected modes. Invocable standalone or by ln-160 coordinator.

---

## Mode Detection

| Condition | Mode | Review Profile |
|-----------|------|----------------|
| `ln-*/SKILL.md` files exist in CWD | **SKILL** | Full D1-D9 + M1-M5 |
| `.claude/commands/*.md` files exist | **COMMAND** | Structural + actionability |
| Both exist | **SKILL** (default) | Override: `$ARGUMENTS = commands` |

---

## Input

`$ARGUMENTS` options:
- Empty -> auto-detect mode + auto-detect scope
- `ln-400 ln-500` -> SKILL mode, specific skills
- `commands` -> COMMAND mode, all `.claude/commands/*.md`
- `deploy.md run-tests.md` -> COMMAND mode, specific files

When invoked by ln-160 coordinator: receives list of file paths to review in COMMAND mode.

---

## SKILL Mode

Review SKILL.md files against 9 structural dimensions + 5 intent checks. Fix in-place. Report with PASS/FAIL verdict.

### Phase 1: Scope Detection

**If `$ARGUMENTS` provided:** treat each token as a skill directory prefix (e.g., `ln-400` matches `ln-400-story-executor/`). Glob `{prefix}*/SKILL.md` per token.

**If `$ARGUMENTS` empty:** auto-detect from git:
```bash
git diff --name-only HEAD
git diff --name-only --cached
git ls-files --others --exclude-standard
```
Extract unique skill dirs (pattern `ln-\d+-[^/]+`) and shared paths (`shared/`). If shared files changed, Grep all `ln-*/SKILL.md` for references to changed filenames.

**Build scope:**
1. **Primary** -- skills with directly changed files
2. **Affected** -- skills referencing changed shared files
3. **Dependencies** -- for each primary skill, extract `ln-\d{3,4}` references from its SKILL.md (callers, callees, worker tables)

Deduplicate. Report: `Scope: N primary, M affected, K dependency skills.`

### Phase 2: Automated Verification

Run the automated checks script against all SKILL.md files in scope:

```bash
bash references/run_checks.sh {scoped SKILL.md files}
```

Record failures -- they feed D7/D8 as pre-verified violations. Every FAIL is confirmed -- no judgment needed, no skipping. Check definitions: `references/automated_checks_skill_mode.md`.

### Phase 3: Nine-Dimension Review

**MANDATORY READ:** Load `references/dimensions_d1_d9.md` and `docs/architecture/SKILL_ARCHITECTURE_GUIDE.md`

Read every SKILL.md in scope. Check ALL dimensions across ALL skills. Phase 2 failures are pre-verified -- include directly, do not re-check.

### Phase 4: Intent Review

**MANDATORY READ:** Load `references/intent_m1_m5.md`

Evaluate DESIGN INTENT of changes. Applies to primary skills only. For each primary skill, read the git diff (`git diff HEAD -- {skill_dir}/`).

### Phase 5: Fix

For each finding:
- **Fixable** (wrong path, stale ref, missing bidirectional ref, duplicated content) -- fix immediately via Edit
- **Ambiguous** (conflicting thresholds where correct value unclear) -- list in report, do NOT guess
- **SIMPLIFY** (from Phase 4) with unambiguous action -- fix immediately
- **REVERT** (from Phase 4) -- roll back the change via Edit
- **RETHINK** (from Phase 4) -- do NOT fix, pass to Phase 6 report

### Phase 6: Report

**Verdict rules:**
- Any D1-D9 violation NOT auto-fixed -> **FAIL**
- Only RETHINK findings (no unfixed violations) -> **PASS with CONCERNS**
- Zero findings -> **PASS**

```
## Skill Coherence Review -- {PASS|PASS with CONCERNS|FAIL}

**Scope:** {list of reviewed skills}
**Verdict:** {verdict}

### Automated Checks (Phase 2)
| Check | Result | Failures |
|-------|--------|----------|
| Frontmatter (D7) | {PASS/FAIL} | {list or --} |
| Version/Date (D7) | {PASS/FAIL} | {list or --} |
| Size <=800 (D8) | {PASS/FAIL} | {list or --} |
| Description <=200 (D8) | {PASS/FAIL} | {list or --} |
| MANDATORY READ paths (D2) | {PASS/FAIL} | {list or --} |
| Orphan references (D7) | {PASS/FAIL} | {list or --} |
| Passive file refs (D2) | {PASS/FAIL} | {list or --} |
| Definition of Done (D7) | {PASS/FAIL} | {list or --} |
| Meta-Analysis L1/L2 (D7) | {PASS/FAIL} | {list or --} |
| Marketplace paths (D8, optional) | {PASS/FAIL/SKIP} | {list or --} |
| Root docs stale names (D6) | {PASS/FAIL} | {list or --} |
| Skill count accuracy (D8) | {PASS/FAIL} | {list or --} |

### Fixed ({count})
| # | Skill | Dim | Issue | Fix Applied |
|---|-------|-----|-------|-------------|

### Intent Findings ({count})
**M5 Classification:** {R} requested, {D} derived, {S} speculative ({K} kept, {V} reverted)

| # | Skill | Dim | Finding | Category |
|---|-------|-----|---------|----------|

### Remaining Concerns ({count})
| # | Skill | Dim | Issue | Why Not Auto-Fixed |
|---|-------|-----|-------|--------------------|

### Clean
Dimensions with no findings: {list}
```

If zero findings: `All 9 structural dimensions + 5 intent checks clean. PASS.`

### Phase 7: Volatile Numbers Cleanup

Skill/plugin/category counts go stale after every add/remove. One rule: **counts ONLY in README.md badge** (`skills-NNN`). Everywhere else -- no hardcoded counts.

**Remove from any file** (including marketplace.json descriptions, CLAUDE.md, AGENTS.md, CHANGELOG.md, SKILL.md):
- Total skill counts, per-plugin counts, per-category counts
- Worker/coordinator counts referencing OTHER skills (a skill's OWN internals are fine)

Phase 2 automated check verifies README badge matches actual skill count on disk -- fix if FAIL.

---

## COMMAND Mode

Review `.claude/commands/*.md` files against structural + actionability criteria.

**MANDATORY READ:** Load `references/command_review_criteria.md`

### Phase 1: Scope Detection

**If file paths provided:** review those files.
**If `commands` keyword:** Glob `.claude/commands/*.md`.
**If invoked by ln-160:** use file list from coordinator.

### Phase 2: Review

For each command file, apply all criteria from `references/command_review_criteria.md`.

### Phase 3: Fix

Auto-fix where possible (add missing frontmatter, truncate description). Flag unfixable issues.

### Phase 4: Report

```
## Command Review -- {N} files

| File | Verdict | Issues |
|------|---------|--------|

Verdicts: PASS / FIXED / WARN
Pass rate: {X}%
```

---

## Rules

- Automated checks (Phase 2) are NON-NEGOTIABLE -- every FAIL must appear in report
- Do NOT skip any dimension for any skill in scope
- If unsure whether something violates a rule -- it violates the rule (strict interpretation)
- Read ALL skills in scope before reporting
- Fix errors immediately, do not defer
- Do NOT update versions or dates unless user explicitly requests it
- `shared/` changes affect every skill that references them -- check reverse dependencies
- Intent review (M1-M5) evaluates DESIGN, not correctness -- findings are judgment-based
- RETHINK findings are advisory -- explain WHY, author decides WHETHER to act
- REVERT findings are executed immediately -- changes without concrete defect are rolled back
- SPECULATIVE items (M5) without user response default to REVERT -- no silent acceptance of model-generated additions

---

## Definition of Done

- [ ] Scope detected (primary + affected + dependency skills)
- [ ] Phase 2 automated checks executed for all skills in scope
- [ ] D1-D9 dimensions reviewed across all skills
- [ ] M1-M5 intent evaluated for primary skills
- [ ] Fixable findings auto-fixed via Edit
- [ ] Report generated with PASS/PASS with CONCERNS/FAIL verdict

---

**Version:** 1.0.0
**Last Updated:** 2026-03-13
