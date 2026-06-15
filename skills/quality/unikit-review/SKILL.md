---
name: unikit-review
description: Reviews {{engine_name}} {{engine_code_language}} code against project coding rules, design principles, and framework-specific conventions. Supports four modes — staged changes, PR, commit history, and individual files. Use when reviewing {{engine_name}} code, checking code quality, reviewing staged changes, PRs, commit ranges, or when the user asks to review scripts or check for coding violations. Also triggers on "review code", "check code", "code review", "review PR", "review staged", "review commits", or any review request for {{engine_name}} {{engine_code_language}} scripts.
argument-hint: "[script.cs ... | @folder ... | PR number | branch/commit/tag | empty]"
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash(find *)
  - Bash(wc *)
  - Bash(git *)
  - Bash(gh *)
  - AskUserQuestion
---

# {{engine_name}} Code Reviewer

Analyze {{engine_code_language}} code against the project's coding rules and produce a structured review report.

## Language Awareness — BLOCKING PRE-REQUISITE

**BEFORE producing ANY output**, silently read `.unikit/system/LANGUAGE_RULES.md`
and apply its rules to ALL subsequent output.
If the file is missing or unreadable, fall back to English.
Do not produce any user-facing output until language rules are loaded.
Do not announce, confirm, or mention the language setting.

## Step 1: Load rules

Read (they always apply):
- `.unikit/ARCHITECTURE.md` — module boundaries, dependency rules
- `.unikit/ROADMAP.md` (if present) — milestone alignment

Read `.unikit/memory/RULES_INDEX.md`. Load rules:
- **RULES.md**: ALWAYS read `.unikit/RULES.md` first (highest priority)
- **Core**: read the Core table. For EACH row where Required By = `all` or contains `{{self_name}}` — read that file from `.unikit/memory/core/` using the Read tool. Do NOT skip any matching row. Always re-read at skill start, never rely on prior conversation cache
- **Stack**: load dynamically when the current task or context matches "Load When" column, or when a need arises during work

Read `.unikit/skill-context/{{self_name}}/SKILL.md` if it exists — project-level overrides that win over this SKILL.md when conflicting.

## Step 2: Route argument and get code

### Routing chain

1. **Empty** → Staged mode
2. **Digits / `#N` / PR URL** (e.g. `123`, `#42`, `https://github.com/.../pull/123`) → PR mode. Extract number from URL if needed
3. **Starts with `@`** → File mode (folder). Strip `@`, glob `<path>/**/*.cs`
4. **Contains `.cs`** → File mode (explicit files)
5. **Other** → `git rev-parse --verify <arg>`:
   - Valid → Commits mode
   - Invalid → `AskUserQuestion` (staged / cancel / corrected ref)

> `@` disambiguates folder paths from git refs with `/`.

### Staged mode

1. `git diff --cached` → if empty, `git diff` → if empty, inform and **stop**
2. Extract changed `.cs` files, read full content for stack rule detection

### PR mode

1. `gh pr view <N> --json title,body,baseRefName,headRefName,files`
2. `gh pr diff <N>`
3. Extract changed `.cs` files, read full content for stack rule detection

### Commits mode

1. Validate ref via `git rev-parse --verify`. Invalid → ask user
2. `git log --oneline --reverse <ref>..HEAD` → if empty, inform and **stop**
3. If >20 commits → `AskUserQuestion` (all / last 20 / cancel)
4. `git diff --name-only <ref>..HEAD -- '*.cs'` → read full content for stack rule detection
5. For each commit: `git show <hash> --stat` and `git show <hash>`

### File mode

- `.cs` args: locate via `Glob`/`find`. Name without path → search entire project
- `@folder` args: `Glob <folder>/**/*.cs`. No results → report error, continue with others
- Read full content of all found files for stack rule detection

## Step 3: Load stack rules

Now that target code is available, scan it for framework markers from the **Stack** section of `RULES_INDEX.md`. Each entry lists which keywords/types indicate relevance ("Load When" column). Load only matching rule files. If no markers match — skip stack rules entirely.

## Step 4: Analyze

Apply **all loaded rules** (core + stack + project + ARCHITECTURE.md) uniformly, regardless of mode.

For each file or diff hunk, check:
- **Rule violations** — every loaded rule against the code
- **Architecture alignment** — boundary/dependency violations (e.g. `Modules/ → Game/` forbidden)
- **Roadmap linkage** — for `feat`/`fix`/`perf` work, missing ROADMAP.md milestone link (suggestion only)
- **Removed code** (diff modes) — broken contracts, dangling references

**Commits mode only** — additionally per commit:
- **Message accuracy** — does the message match the actual changes?
- **Atomicity** — single logical unit, or mixed concerns?

### Severity scale

- 🔴 **Critical** — must fix (crashes, silent failures, memory leaks, data corruption)
- 🟡 **Warning** — likely to cause bugs under specific conditions
- 🟠 **Medium** — performance, code smell, maintainability
- 🟢 **Suggestion** — quality improvement

Record exact line numbers (or commit hash + file:line for diff modes) and relevant code snippets.

### General checklist

Always run these checks in addition to project rules. If a finding from the checklist contradicts a loaded project/core/stack rule or ARCHITECTURE.md (i.e. the code follows project conventions) — **suppress the finding**, it is not an issue.

**Correctness:**
- [ ] Logic errors or bugs
- [ ] Edge cases handling
- [ ] Null/undefined checks
- [ ] Error handling completeness
- [ ] Type safety

**Performance:**
- [ ] Memory leaks
- [ ] Inefficient algorithms
- [ ] N+1 query problems

**Best Practices:**
- [ ] Code duplication
- [ ] Dead code
- [ ] Magic numbers/strings
- [ ] Proper naming conventions
- [ ] SOLID principles
- [ ] DRY principle

**Testing:**
- [ ] Test coverage for new code
- [ ] Edge cases tested
- [ ] Mocking appropriateness

## Step 5: Output

All modes use the same report structure. Mode-specific sections are marked below.

```markdown
## Code Review Summary

<!-- PR mode only: -->
**PR:** #[number] — [title]
**Base:** [baseRefName] ← **Head:** [headRefName]
<!-- Commits mode only: -->
**Range:** `<ref>..HEAD`
**Commits Reviewed:** [count]

**Files Reviewed:** [count]
**Risk Level:** 🟢 Low / 🟡 Medium / 🔴 High
**Stack rules loaded:** [list or "none"]

<!-- Commits mode only: -->
### Per-Commit Notes
#### `<short-hash>` — <commit message>
- **Atomicity:** ✅ Good / ⚠️ Mixed concerns
- **Message accuracy:** ✅ Matches / ⚠️ Misleading
- **Issues:** [findings with severity markers, or "None"]

### Findings

| # | Severity | Location | Rule | Issue | Fix |
|---|----------|----------|------|-------|-----|
| 1 | 🔴/🟡/🟠/🟢 | file:L42 | Rule ref | What's wrong | How to fix |

### Code Fixes

<!-- For 🔴 and 🟡 findings, show: -->
**#1 — [issue title]** (`file:L42`)
​```csharp
// ❌ Current
<problematic code>

// ✅ Fixed
<corrected code>
​```

### Questions
[Ambiguous code or design decisions that need clarification from the author]

### Summary

- **Critical:** [count] | **Warning:** [count] | **Medium:** [count] | **Suggestion:** [count]
- **Top issues:** 3 most impactful to fix first
- **Positive notes:** Good patterns observed
```

## Guidelines

- Be precise: exact line numbers and code references
- Be actionable: every finding includes a concrete fix
- Be complete: check ALL loaded rules
- No false positives: if uncertain, mark "Potential — verify manually"
- Clean code → say so, don't invent issues
- Read-only: do NOT modify any files
- Be constructive: explain "why", acknowledge good code

## Examples

`/unikit-review` — review staged changes
`/unikit-review PlayerController.cs` — review specific file
`/unikit-review @Assets/Scripts/Player` — review folder recursively
`/unikit-review @Assets/Scripts/Player @Assets/Modules/Wallets` — review multiple folders
`/unikit-review 123` or `/unikit-review #42` — review PR by number
`/unikit-review https://github.com/org/repo/pull/123` — review PR by URL
`/unikit-review master` — review commits vs master
`/unikit-review v1.0.0` — review commits vs tag
`/unikit-review feature/day-loop` — review commits vs branch

> **Tip:** Context is heavy after review. Consider `/clear` or `/compact` before continuing.
