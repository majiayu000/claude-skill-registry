---
name: review-ai-writing
description: Detect AI-generated writing patterns in developer text — docs, docstrings, commit messages, PR descriptions, and code comments. Use when reviewing any text artifact for authenticity and clarity.
disable-model-invocation: true
autoContext:
  whenUserAsks:
    - ai writing
    - ai-generated
    - sounds like ai
    - writing quality
    - humanize-beagle
    - robotic writing
    - chatgpt
dependencies:
  - docs-style
---

# Review AI Writing

Detect AI-generated writing patterns across developer text artifacts using parallel subagents.

## Usage

```text
/beagle-docs:review-ai-writing [--all] [--category <name>] [path]
```

**Flags:**
- `--all` - Scan entire codebase (default: changed files from main)
- `--category <name>` - Only check specific category: `content|vocabulary|formatting|communication|filler|code_docs`
- Path: Target directory (default: current working directory)

## Instructions

### 1. Parse Arguments

Extract flags from `$ARGUMENTS`:
- `--all` - Full codebase scan
- `--category <name>` - Filter to specific category
- Path - Target directory

### 2. Load Skills

Load required skills:

```text
Skill(skill: "beagle-docs:review-ai-writing")
Skill(skill: "beagle-core:review-verification-protocol")
```

### 3. Determine Scope

```bash
# Default: changed files from main
git diff --name-only $(git merge-base HEAD main)..HEAD

# If --all flag: scan all text artifacts
find . -type f \( -name "*.md" -o -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.rb" -o -name "*.swift" -o -name "*.kt" -o -name "*.ex" -o -name "*.exs" \) ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/vendor/*" ! -path "*/__pycache__/*" ! -path "*/dist/*" ! -path "*/build/*"
```

If no files found, exit with: "No files to scan. Check your branch has changes or use --all."

### 4. Check for Existing LLM Artifacts Review

```bash
# Check if llm-artifacts review exists to avoid double-flagging
if [ -f .beagle/llm-artifacts-review.json ]; then
  echo "Found existing llm-artifacts review — will skip overlapping findings"
fi
```

Parse existing findings from `.beagle/llm-artifacts-review.json` if present. When consolidating, skip any finding where both the file:line and pattern type match an existing llm-artifacts finding (specifically `verbose_comment` and `over_documentation` types).

### 5. Classify Files by Type

Partition files into three groups:

| Group | File Types | Patterns to Check |
|-------|-----------|-------------------|
| **Prose** | `*.md` | All 6 categories |
| **Code Docs** | `*.py`, `*.ts`, `*.tsx`, `*.js`, `*.jsx`, `*.go`, `*.rs`, `*.java`, `*.rb`, `*.swift`, `*.kt`, `*.ex`, `*.exs` | vocabulary, communication, filler, code_docs |
| **Git** | Commit messages, PR descriptions | content, vocabulary, communication, filler |

For Git artifacts, collect recent commits:

```bash
# Commits on current branch not in main
git log --format="%H %s" $(git merge-base HEAD main)..HEAD
```

### 6. Spawn Parallel Subagents

If total items >= 4, spawn up to 3 subagents via `Task` tool. If `--category` is set, spawn a single agent for that category only.

#### Subagent 1: Prose Agent

**Scope:** Markdown files only
**Check:** All 6 pattern categories
**Instructions:**
1. Load `beagle-docs:review-ai-writing` skill
2. Read each markdown file
3. Scan for all pattern categories
4. Apply false positive checks from the skill
5. Return findings in the structured format

#### Subagent 2: Code Docs Agent

**Scope:** Source code files
**Check:** vocabulary, communication, filler, code_docs categories
**Instructions:**
1. Load `beagle-docs:review-ai-writing` skill
2. Extract docstrings and comments from each file
3. Scan for applicable pattern categories
4. Skip code itself — only check text in comments and docstrings
5. Return findings in the structured format

#### Subagent 3: Git Agent

**Scope:** Commit messages and PR descriptions
**Check:** content, vocabulary, communication, filler categories
**Instructions:**
1. Load `beagle-docs:review-ai-writing` skill
2. Read commit messages from the branch
3. If on a PR branch, read the PR description via `gh pr view --json body`
4. Scan for applicable pattern categories
5. Use synthetic paths: `git:commit:<sha>` with line 0, `git:pr:<number>` with line 0
6. Return findings in the structured format

### 7. Consolidate Findings

Wait for all subagents to complete, then:

1. Merge all findings into a single list
2. Remove duplicates (same file:line and type)
3. Remove findings that overlap with `.beagle/llm-artifacts-review.json`
4. Assign unique IDs (1, 2, 3...)
5. Group by category for display

### 8. Write JSON Report

Create `.beagle` directory if it doesn't exist:

```bash
mkdir -p .beagle
```

Write findings to `.beagle/ai-writing-review.json`:

```json
{
  "version": "1.0.0",
  "created_at": "2025-01-15T10:30:00Z",
  "git_head": "abc1234",
  "scope": "changed",
  "files_scanned": 12,
  "commits_scanned": 5,
  "findings": [
    {
      "id": 1,
      "category": "vocabulary",
      "type": "ai_vocabulary_high",
      "file": "README.md",
      "line": 15,
      "original_text": "This library leverages cutting-edge algorithms to facilitate seamless data processing.",
      "description": "High-signal AI vocabulary: leverage, cutting-edge, facilitate, seamless",
      "suggestion": "This library uses streaming algorithms for fast data processing.",
      "risk": "Low",
      "fix_safety": "Safe",
      "fix_action": "rewrite"
    },
    {
      "id": 2,
      "category": "code_docs",
      "type": "tautological_docstring",
      "file": "src/auth.py",
      "line": 42,
      "original_text": "\"\"\"Get the user by ID.\"\"\"",
      "description": "Docstring restates function name get_user_by_id without adding value",
      "suggestion": "\"\"\"Raises UserNotFound if ID doesn't exist.\"\"\"",
      "risk": "Medium",
      "fix_safety": "Needs review",
      "fix_action": "rewrite"
    },
    {
      "id": 3,
      "category": "communication",
      "type": "chat_leak",
      "file": "git:commit:abc1234",
      "line": 0,
      "original_text": "Certainly! Here's the updated authentication flow",
      "description": "Chat leak in commit message: starts with 'Certainly! Here's'",
      "suggestion": "Update authentication flow",
      "risk": "Low",
      "fix_safety": "Safe",
      "fix_action": "rewrite"
    }
  ],
  "summary": {
    "total": 3,
    "by_category": {
      "vocabulary": 1,
      "code_docs": 1,
      "communication": 1
    },
    "by_risk": {
      "Low": 2,
      "Medium": 1
    },
    "by_fix_safety": {
      "Safe": 2,
      "Needs review": 1
    }
  }
}
```

### 9. Display Summary

```markdown
## AI Writing Review

**Scope:** Changed files from main
**Files scanned:** 12 | **Commits scanned:** 5

### Findings by Category

#### Vocabulary (1 issue)

1. [README.md:15] **AI vocabulary** (Low, Safe)
   - High-signal AI vocabulary: leverage, cutting-edge, facilitate, seamless
   - Suggestion: Rewrite with simple words

#### Code Docs (1 issue)

2. [src/auth.py:42] **Tautological docstring** (Medium, Needs review)
   - Docstring restates function name without adding value
   - Suggestion: Add meaningful information or delete

#### Communication (1 issue)

3. [git:commit:abc1234:0] **Chat leak** (Low, Safe)
   - Commit message starts with "Certainly! Here's"
   - Suggestion: Rewrite as imperative commit message

### Summary Table

| Category | Safe | Needs Review | Total |
|----------|------|--------------|-------|
| Vocabulary | 1 | 0 | 1 |
| Code Docs | 0 | 1 | 1 |
| Communication | 1 | 0 | 1 |
| **Total** | **2** | **1** | **3** |

### Next Steps

- Run `/beagle-docs:humanize-beagle` to apply fixes
- Run `/beagle-docs:humanize-beagle --dry-run` to preview changes first
- Review the JSON report at `.beagle/ai-writing-review.json`
```

### 10. Verification

Before completing, all of the following must **pass** (objective checks):

1. **JSON file exists and parses:** `.beagle/ai-writing-review.json` is present **or** you exited at Gate 1 with no scan (then no JSON is required).
2. **JSON validity:** If the file exists, `python3 -c "import json; json.load(open('.beagle/ai-writing-review.json'))"` exits 0.
3. **Subagent success:** If you used `Task` subagents, each returned without tool/runtime failure (failed spawn = do not write final JSON as if complete).
4. **Git HEAD captured:** When JSON exists, `git_head` matches `git rev-parse HEAD` (non-empty string).
5. **No double-flagging:** If `.beagle/llm-artifacts-review.json` exists, no finding duplicates its file:line + overlapping type for the skip rules in §4.

```bash
# Verify JSON is valid (when file exists)
python3 -c "import json; json.load(open('.beagle/ai-writing-review.json'))" 2>/dev/null && echo "Valid JSON" || echo "Invalid JSON"
```

If any check fails, report the error and do not proceed.

## Output Format for Each Finding

```text
[FILE:LINE] ISSUE_TITLE
- Category: content | vocabulary | formatting | communication | filler | code_docs
- Type: specific_pattern_name
- Original: "the problematic text"
- Suggestion: "the improved text" or "delete"
- Risk: Low | Medium
- Fix Safety: Safe | Needs review
```

## Rules

- Always load `beagle-docs:review-ai-writing` and `beagle-core:review-verification-protocol` first
- Use `Task` tool for parallel subagents when >= 4 items to scan
- Every finding MUST have file:line reference (use synthetic paths for git artifacts)
- Do not flag false positives listed in the skill
- Do not duplicate findings from `.beagle/llm-artifacts-review.json`
- Create `.beagle` directory if needed
- Write JSON report before displaying summary

## Gates (sequenced pass conditions)

Advance only when each **pass condition** is satisfied using artifacts (paths, exit codes, parseable output)—not an internal “I checked” claim.

1. **Arguments → scope**
   - **Pass:** You can list the concrete paths (or `git:commit:<sha>` / `git:pr:<n>`) you will scan. If that set is empty, emit the “No files to scan…” message and **do not** create `.beagle/ai-writing-review.json`.

2. **Scope → execution**
   - **Pass:** Each of Prose, Code docs, and Git (when in scope) has either completed subagent output **or** equivalent inline work with the same structured fields per finding.

3. **Consolidation → write**
   - **Pass:** Duplicates (same file:line and type) removed; when `.beagle/llm-artifacts-review.json` exists, overlaps with it skipped per §4; `git_head` equals the output of `git rev-parse HEAD` (non-empty).

4. **JSON → summary**
   - **Pass:** `python3 -c "import json; json.load(open('.beagle/ai-writing-review.json'))"` exits 0.

5. **Finding → verification protocol**
   - **Pass:** For each reported issue, you can cite the surrounding paragraph or function you used so the flag is evidence-backed (see `beagle-core:review-verification-protocol`).

## Reference Material

### AI Writing Detection for Developer Text

Detect patterns characteristic of AI-generated text in developer artifacts. These patterns reduce trust, add noise, and obscure meaning.

## Pattern Categories

| Category | Reference | Key Signals |
|----------|-----------|-------------|
| Content | `references/content-patterns.md` | Promotional language, vague authority, formulaic structure, synthetic openers |
| Vocabulary | `references/vocabulary-patterns.md` | AI word tiers, copula avoidance, rhetorical devices, synonym cycling, commit inflation |
| Formatting | `references/formatting-patterns.md` | Boldface overuse, emoji decoration, heading restatement |
| Communication | `references/communication-patterns.md` | Chat leaks, cutoff disclaimers, sycophantic tone, apologetic errors |
| Filler | `references/filler-patterns.md` | Filler phrases, excessive hedging, generic conclusions |
| Code Docs | `references/code-docs-patterns.md` | Tautological docstrings, narrating obvious code, "This noun verbs", exhaustive enumeration |

## Scope

Scan these artifact types:

| Artifact | File Patterns | Notes |
|----------|--------------|-------|
| Markdown docs | `*.md` | READMEs, guides, changelogs |
| Docstrings | `*.py`, `*.ts`, `*.js`, `*.go`, `*.swift`, `*.rs`, `*.java`, `*.kt`, `*.rb`, `*.ex` | Language-specific docstring formats |
| Code comments | Same as docstrings | Inline and block comments |
| Commit messages | `git log` output | Use synthetic path `git:commit:<sha>` |
| PR descriptions | GitHub PR body | Use synthetic path `git:pr:<number>` |

### What NOT to Scan

- Generated code (lock files, compiled output, vendor directories)
- Third-party content (copied license text, vendored docs)
- Code itself (variable names, string literals used programmatically)
- Test fixtures and mock data

## Detection Rules

### High-Confidence Signals (Always Flag)

These patterns are strong indicators of AI-generated text:

1. **Chat leaks** — "Certainly!", "I'd be happy to", "Great question!", "Here's" as sentence opener
2. **Cutoff disclaimers** — "As of my last update", "I cannot guarantee"
3. **High-signal AI vocabulary** — delve, utilize (as "use"), whilst, harnessing, paradigm, synergy
4. **"This noun verbs" in docstrings** — "This function calculates", "This method returns"
5. **Synthetic openers** — "In today's fast-paced", "In the world of"
6. **Sycophantic code comments** — "Excellent approach!", "Great implementation!"

### Medium-Confidence Signals (Flag in Context)

Flag when 2+ appear together or pattern is repeated:

1. **Low-signal AI vocabulary clusters** — 3+ words from the low-signal list in one section
2. **Formulaic structure** — Rigid intro-body-conclusion in a README section
3. **Heading restatement** — First sentence after heading restates the heading
4. **Excessive hedging** — "might potentially", "could possibly", "it seems like it may"
5. **Synonym cycling** — Same concept called different names within one section
6. **Boldface overuse** — More than 30% of sentences contain bold text

### Low-Confidence Signals (Note Only)

Mention but don't flag as issues:

1. **Emoji in technical docs** — May be intentional project style
2. **Filler phrases** — Some are common in human writing too
3. **Generic conclusions** — May be appropriate for summary sections
4. **Commit inflation** — Some teams prefer descriptive commits

## False Positive Warnings

Do NOT flag these as AI-generated:

| Pattern | Why It's Valid |
|---------|----------------|
| "Ensure" in security docs | Standard term for security requirements |
| "Comprehensive" in test coverage discussion | Accurate technical descriptor |
| Formal tone in API reference docs | Expected register for reference material |
| "Leverage" in financial/business domain code | Domain-specific meaning, not AI filler |
| Bold formatting in CLI help text | Standard convention |
| Structured intro paragraphs in RFCs/ADRs | Expected format for these document types |
| "This module provides" in Python `__init__.py` | Idiomatic Python module docstring |
| Rhetorical questions in blog posts | Appropriate for informal content |

## Integration

### With `beagle-core:review-verification-protocol`

Before reporting any finding:

1. Read the surrounding context (full paragraph or function)
2. Confirm the pattern is AI-characteristic, not just formal writing
3. Check if the project has established conventions that match the pattern
4. Verify the suggestion improves clarity without changing meaning

### With `beagle-core:llm-artifacts-detection`

Code-level patterns (tautological docstrings, obvious comments) overlap with `llm-artifacts-detection`'s style criteria. When both skills are loaded:

- `review-ai-writing` focuses on **writing style** (how it reads)
- `llm-artifacts-detection` focuses on **code artifacts** (whether it should exist at all)
- If `.beagle/llm-artifacts-review.json` exists, skip findings already captured there

## Output Format

Report each finding as:

```text
[FILE:LINE] ISSUE_TITLE
- Category: content | vocabulary | formatting | communication | filler | code_docs
- Type: specific_pattern_name
- Original: "the problematic text"
- Suggestion: "the improved text" or "delete"
- Risk: Low | Medium
- Fix Safety: Safe | Needs review
```

### Risk Levels

- **Low** — Filler phrases, obvious comments, emoji. Removing improves clarity with no meaning change.
- **Medium** — Vocabulary swaps, structural changes, docstring rewrites. Meaning could shift if done carelessly.

### Fix Safety

- **Safe** — Mechanical replacement or deletion. No judgment needed.
- **Needs review** — Rewrite requires understanding context. Human should verify the replacement preserves intent.
