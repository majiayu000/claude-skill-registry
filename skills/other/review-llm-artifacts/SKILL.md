---
name: review-llm-artifacts
description: Detects common LLM coding agent artifacts by spawning four parallel subagents over the project or changed files. Scans files changed since main by default; use --all for full-project scan. Triggers on LLM cruft cleanup, agent-generated code review, dead code sweeps, test-quality passes, or when the user asks to scan the whole repo.
disable-model-invocation: true
---

# LLM Artifacts Review

Detect common artifacts left behind by LLM coding agents: over-abstraction, dead code, DRY violations in tests, verbose comments, and defensive overkill.

## Hard gates (sequence)

Advance only when each **pass condition** is objectively true (prevents “review complete” without artifacts):

| Gate | Pass condition |
|------|----------------|
| **G1 — Scope** | File list is non-empty *or* you exit with exactly the Step 1 message; `scope` is set to `all` or `changed`. |
| **G2 — Four categories** | Tests, dead code, abstraction, and style are each reviewed (four `Task` runs when Step 3 applies, or four sequential passes covering the same categories). **Stop** if any category did not complete; do not write JSON or a summary that implies a full pass. |
| **G3 — JSON before summary** | `.beagle/llm-artifacts-review.json` exists and is valid JSON **before** Step 6 markdown. |
| **G4 — Integrity** | Step 7 checks pass before treating the run as complete. |

## Arguments

Parse `$ARGUMENTS` for flags and optional path:

| Flag | Effect |
|------|--------|
| *(default)* | **Changed-files scope** — only files changed since `git merge-base HEAD main` (PR-style scope) |
| `--all` | Full project scan — all matching source files under the target path |
| `--parallel` | Force parallel execution (default when 4+ files in scope) |
| Path | Root directory to scan (default: current working directory) |

## Step 1: Determine Scope

**A. Changed files only (default):**

Resolve the base ref explicitly and fail loudly if none exists — **do not** wrap the `git merge-base` call in `|| true`, which would silently swallow a missing `main`/`master` ref and report "no files to scan" on repos that only have `origin/main` or use `master`. If no base ref is found, suggest the user pass `--all` instead of silently falling back.

```bash
BASE=$(for ref in main origin/main master origin/master; do
         git rev-parse --verify "$ref" >/dev/null 2>&1 && { echo "$ref"; break; }
       done)
if [ -z "$BASE" ]; then
  echo "error: no main/master ref found (checked main, origin/main, master, origin/master). Pass --all for a full-project scan." >&2
  exit 1
fi
MERGE_BASE=$(git merge-base HEAD "$BASE") || {
  echo "error: git merge-base HEAD $BASE failed." >&2
  exit 1
}
git diff --name-only "$MERGE_BASE..HEAD" | grep -E '\.(py|ts|tsx|js|jsx|go|rs|java|rb|swift|kt)$' || true
```

(The trailing `|| true` on the `grep` is intentional — zero source-file matches is a legitimate empty-scope result, distinct from a failed base-ref resolution.)

**B. Full project (`--all`):**

From `TARGET` (default `.`), list source files and **prune** excluded dependency/build trees so `find` never descends into them. `! -path "*/foo/*"` only filters the output; `find` still walks the tree (minutes of wasted I/O on large `node_modules`, `target`, etc.). Use `-prune` instead:

```bash
find "$TARGET" \
  \( -type d \( \
       -name node_modules -o -name .git -o -name vendor -o -name __pycache__ \
    -o -name .venv        -o -name venv -o -name dist   -o -name build \
    -o -name target       -o -name .next -o -name coverage -o -name .turbo \
  \) -prune \) -o \
  \( -type f \( \
       -name "*.py" -o -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
    -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o -name "*.rb" \
    -o -name "*.swift" -o -name "*.kt" \
  \) -print \)
```

**Large repos:** The `--all` path can produce huge file lists. If file count exceeds **400**, warn and suggest narrowing: pass a subdirectory as `TARGET`, or drop `--all` to fall back to the default changed-files scope. Still proceed unless the user explicitly cancels. (This warning does **not** fire on the default changed-files scope, which is already bounded by the PR diff.)

If no files are found, exit with:

`No files to scan. Check the path, branch, or pass --all for a full-project scan.`

Set `scope` in the report: `"all"` for `--all`, `"changed"` for the default changed-files scope.

## Step 2: Detect Languages

Extract unique file extensions from the file list:

```bash
echo "$FILES" | sed 's/.*\.//' | sort -u
```

Map extensions to language names for the report:
- `.py` -> Python
- `.ts`, `.tsx` -> TypeScript
- `.js`, `.jsx` -> JavaScript
- `.go` -> Go
- `.rs` -> Rust
- `.java` -> Java
- `.rb` -> Ruby
- `.swift` -> Swift
- `.kt` -> Kotlin

## Step 3: Spawn Parallel Subagents

If file count >= 4 OR `--parallel` flag is set, spawn 4 subagents via `Task` tool.

Each subagent MUST:
1. Load the skill: `Skill(skill: "beagle-core:llm-artifacts-detection")`
2. Review only its assigned category
3. Return findings in the structured format below

### Subagent 1: Tests Agent

**Focus:** Testing anti-patterns from LLM generation

- DRY violations (repeated setup code, duplicate assertions)
- Testing library/framework code instead of application logic
- Wrong mock boundaries (mocking too much or too little)
- Overly verbose test names that describe implementation
- Tests that just mirror the implementation

### Subagent 2: Dead Code Agent

**Focus:** Unused or obsolete code

- Unused imports, variables, functions, classes
- TODO/FIXME comments that should have been resolved
- Backwards compatibility code for removed features
- Orphaned test files for deleted code
- Commented-out code blocks
- Feature flags that are always on/off

### Subagent 3: Abstraction Agent

**Focus:** Over-engineering patterns

- Unnecessary abstraction layers (interfaces for single implementations)
- Copy-paste drift (similar code that diverged slightly)
- Over-configuration (configurable things that never change)
- Premature generalization
- Factory/Builder patterns for simple object creation
- Deep inheritance hierarchies

### Subagent 4: Style Agent

**Focus:** Verbose or defensive patterns

- Verbose comments explaining obvious code
- Defensive overkill (null checks on non-nullable values)
- Unnecessary type hints (dynamic languages with obvious types)
- Overly explicit error messages
- Redundant logging
- Self-documenting code with documentation

## Step 4: Consolidate Findings

**Prerequisite:** **G2** satisfied (all four category reviews finished successfully).

Wait for all subagents to complete, then:

1. Merge all findings into a single list
2. Assign unique IDs (1, 2, 3...)
3. Group by category for display

## Step 5: Write JSON Report

Create `.beagle` directory if it doesn't exist:

```bash
mkdir -p .beagle
```

Write findings to `.beagle/llm-artifacts-review.json`:

```json
{
  "version": "1.0.0",
  "created_at": "2024-01-15T10:30:00Z",
  "git_head": "abc1234",
  "scope": "all" | "changed",
  "target": ".",
  "files_scanned": 42,
  "languages": ["Python", "TypeScript", "Go"],
  "findings": [
    {
      "id": 1,
      "category": "tests" | "dead_code" | "abstraction" | "style",
      "type": "dry_violation" | "unused_import" | "over_abstraction" | "verbose_comment" | "...",
      "file": "src/utils/helper.py",
      "line": 42,
      "description": "Repeated setup code in 5 test functions",
      "suggestion": "Extract to a pytest fixture",
      "risk": "Low" | "Medium" | "High",
      "fix_safety": "Safe" | "Needs review",
      "fix_action": "refactor" | "delete" | "simplify" | "extract"
    }
  ],
  "summary": {
    "total": 15,
    "by_category": {
      "tests": 4,
      "dead_code": 5,
      "abstraction": 3,
      "style": 3
    },
    "by_risk": {
      "High": 2,
      "Medium": 8,
      "Low": 5
    },
    "by_fix_safety": {
      "Safe": 10,
      "Needs review": 5
    }
  }
}
```

## Step 6: Display Summary

**Prerequisite:** **G3** satisfied (JSON on disk and parseable).

```markdown
## LLM Artifacts Review

**Scope:** Changed files since merge-base with main | Entire project under `<path>` (when `--all`)
**Files scanned:** 42
**Languages:** Python, TypeScript, Go

### Findings by Category
...
### Summary Table
...
### Next Steps

- Run `/beagle-core:verify-llm-artifacts` to confirm findings and drop false positives before fixing.
- Run `/beagle-core:fix-llm-artifacts` after verification (or to preview safe-only fixes).
- Review the JSON report at `.beagle/llm-artifacts-review.json`
```

## Step 7: Verification (report integrity)

Before completing, verify the review executed correctly:

1. **JSON validity:** Confirm `.beagle/llm-artifacts-review.json` exists and is parseable
2. **Subagent success:** All 4 subagents completed without errors
3. **Git HEAD captured:** The `git_head` field is non-empty in the report
4. **Staleness check:** If a previous report exists, compare stored `git_head` to current HEAD and warn if different

```bash
python3 -c "import json; json.load(open('.beagle/llm-artifacts-review.json'))" 2>/dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"

STORED_HEAD=$(jq -r '.git_head' .beagle/llm-artifacts-review.json 2>/dev/null)
CURRENT_HEAD=$(git rev-parse --short HEAD)
if [ "$STORED_HEAD" != "$CURRENT_HEAD" ]; then
  echo "⚠️ Report was generated on $STORED_HEAD, current HEAD is $CURRENT_HEAD"
fi
```

If any verification fails, report the error and do not proceed.

**Finding-level verification** (precision, not JSON syntax) is a **separate** skill: `/beagle-core:verify-llm-artifacts` — run it before mass deletes or `--fix` on risky items.

## Output Format for Each Finding

```text
[FILE:LINE] **ISSUE_TYPE** (Risk, Fix Safety)
- Description
- Suggestion: Specific fix recommendation
```

## Rules

- Follow **Hard gates** order; do not skip **G3** (JSON before Step 6).
- Always load the `beagle-core:llm-artifacts-detection` skill first
- Use `Task` tool for parallel subagents when >= 4 files
- Every finding MUST have file:line reference
- Categorize risk honestly (don't inflate or deflate)
- Mark fix safety as "Safe" only if change is mechanical and reversible
- Create `.beagle` directory if needed
- Write JSON report before displaying summary
- Default scope is **changed files since merge-base with main**; pass `--all` for a full-project scan
