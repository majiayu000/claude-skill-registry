---
name: git-strategy-advisor
description: >-
  Use when deciding git workflow strategy for planned or completed work.
  Recommends branch creation vs direct commit, branch naming, push timing,
  and PR creation based on change scope and type.
---

# Git Strategy Advisor

Analyzes work context (planned or completed) and recommends an appropriate git workflow strategy. Produces four decisions -- branch strategy, branch naming, push timing, and PR creation -- as structured YAML output with confidence calibration and rationale.

This skill is **advisory only**. It reads git state but never modifies it. The caller or user executes the recommended actions.

## When to Use This Skill

- Before starting work (pre-work mode): to determine branch strategy before making changes
- After completing work (post-work mode): to determine push/PR strategy based on actual changes
- Standalone: when you want git advice for the current repository state
- When a calling orchestrator needs git strategy recommendations via Task tool
- When unsure whether to branch, push, or create a PR

## When NOT to Use This Skill

- Executing git commands (this skill advises; it does not modify the repository)
- Commit message generation (deferred to v2)
- PR description generation (deferred to v2)
- Complex branching strategies (mono-repos, release branches, gitflow)
- Conflict resolution
- Repository initialization or setup
- Re-invoking orchestrator or pipeline skills from within this skill (this skill is a leaf node; it reads git state and returns recommendations but never delegates work to other skills or orchestrators)

## Workflow Overview

Three sequential phases, each building on the previous:

```
Phase 1: Context Analysis    -->  Determine mode, check git state, validate context
Phase 2: Work Classification -->  Extract metrics, classify scope and work type
Phase 3: Strategy Recommendation --> Apply decision matrix, check consistency, format output
```

**Tools used**: Bash (for git commands in post-work mode), Read (for decision-matrix.md), Write (for output file)

**Output**: Structured YAML recommendation (written to file AND returned in response)

---

## Phase 1: Context Analysis

Determine invocation mode, run pre-flight checks, and validate context sufficiency.

### 1.1 Mode Detection

Use this priority-based detection cascade:

1. **Explicit mode signal** (highest priority): If context contains `mode: pre-work` or `mode: post-work`, use that mode directly.
2. **Structured data signal**: If context contains `git status` porcelain output (patterns: `M  path`, `?? path`, `A  path`) or `git diff` headers (`+++ b/`, `--- a/`), use post-work mode.
3. **Keyword heuristic** (lowest priority): Count pre-work signals ("plan", "about to", "will", "estimated", "going to", "planning to", "intend to") vs post-work signals ("completed", "finished", "done", "implemented", "changed", "modified", "just made"). Use mode with more signals. Tie = post-work.
4. **Default**: post-work (analyze current git state).

**Confidence adjustment**:
- Explicit signal or unambiguous structured data: no penalty.
- Keyword heuristic with unclear winner: degrade confidence one level.
- Default fallback (no signals): confidence starts at "low" with note in summary.

**Caller guidance**: Callers SHOULD include explicit `mode: pre-work` or `mode: post-work` for reliable behavior.

### 1.2 Pre-flight Check: Git Repository

Run `git rev-parse --is-inside-work-tree 2>/dev/null`:

- If exit code != 0 (not a git repo):
  - **Pre-work mode**: Produce recommendation with defaults (create-feature-branch, stay-local, no-pr-needed), confidence = "low", summary includes "Consider initializing git with `git init`."
  - **Post-work mode**: Return structured output with confidence = "none", summary = "Post-work analysis requires a git repository."

### 1.3 Pre-flight Check: Git State

Before extracting metrics, detect special states:

- **Detached HEAD**: `git branch --show-current` returns empty. Set current_branch = "DETACHED", is_on_main = false. Force branch.action = "create-feature-branch" with rationale about preserving work.
- **Merge in progress**: `test -f .git/MERGE_HEAD`. Return advisory: "Complete or abort the merge before requesting strategy advice." All strategy fields = null, confidence = "none".
- **Rebase in progress**: `test -d .git/rebase-merge || test -d .git/rebase-apply`. Return advisory: "Complete or abort the rebase before requesting strategy advice." All strategy fields = null, confidence = "none".

### 1.4 Insufficient Context Handling

If pre-work mode detected but context lacks actionable detail (no file paths, no scope keywords, no numeric estimates):

- **Standalone invocation**: Ask user for more context (what files, how many, what type of change).
- **Orchestrator invocation** (via Task tool): Return conservative defaults: scope = "minor", work_type = "mixed", confidence = "low", summary includes "Insufficient context for accurate recommendation. Consider re-invoking in post-work mode."

---

## Phase 2: Work Classification

Extract metrics, detect primary branch, classify scope and work type.

### 2.1 Primary Branch Detection

Use this detection chain (first success wins):

1. `git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@'`
2. `git branch --list main master develop trunk | head -1 | tr -d '* '`
3. `git config init.defaultBranch`
4. Default to "main"

Store as `context.primary_branch`. Set `context.is_on_main` by comparing current branch to primary branch.

### 2.2 Remote Detection

Check `git remote -v` for output. Set `context.has_remote` to true if any remote is configured.

### 2.3 Metrics Extraction

**Post-work mode**:

First check for changes:
- Run `git status --porcelain` to detect uncommitted changes.
- If empty (clean working tree):
  - Check staged changes: `git diff --staged --stat`
  - Check unpushed commits: `git log @{upstream}..HEAD --oneline 2>/dev/null` or `git log origin/{primary_branch}..HEAD --oneline 2>/dev/null`
  - If unpushed commits exist: Use `git diff --stat origin/{primary_branch}..HEAD` for metrics. Note: "Analysis based on N unpushed commits."
  - If nothing: scope = "trivial", summary = "No uncommitted or unpushed changes detected."

For uncommitted changes, use `git diff --numstat HEAD` to capture BOTH staged and unstaged changes:
- Files changed: count lines of output
- Lines changed: sum of additions + deletions
- Directories spanned: count distinct first path components from changed file paths
- Binary files: count separately (shown as `-` in numstat), note in warnings if present

If HEAD does not exist (empty repo), treat all files from `git status --porcelain` as new additions with confidence = "medium".

**Pre-work mode**:
- Estimate from task description keywords and file/directory mentions.
- If caller provides explicit estimates, use those directly.

### 2.4 Scope Classification

Apply the threshold table and aggregation algorithm from `references/decision-matrix.md`:

1. Evaluate each metric independently against the threshold table.
2. Take the MAXIMUM scope level across all three metrics.
3. **Single-metric exception**: If only one metric is elevated and the other two are at trivial, downgrade by one level and set confidence to "medium".

See `references/decision-matrix.md` for the complete threshold table and worked examples.

### 2.5 Work Type Classification

Apply the majority rule from `references/decision-matrix.md`:

1. Classify each file by extension using the extension mapping.
2. Count files per type.
3. If ALL files belong to one type: use that type.
4. If >= 80%: use that type (note minority in warnings).
5. If no type reaches 80%: classify as "mixed".
6. Skill type override: requires >50% skill-path files.
7. Unrecognized extensions: classify as "code" (conservative default).

---

## Phase 3: Strategy Recommendation

Apply decision matrix, check consistency, calibrate confidence, and format output.

### 3.1 Decision Matrix Application

Read `references/decision-matrix.md` and apply the four decision tables based on Phase 2 classification:

1. **Branch Strategy**: Based on scope, work type, and whether on primary branch.
2. **Branch Naming**: Based on work type with keyword overrides for fix/refactor.
3. **Push Strategy**: Based on scope and remote availability.
4. **PR Strategy**: Based on scope and work type.

**Defaults for uncovered combinations**:

| Decision | Default Action | Rationale |
|----------|---------------|-----------|
| Branch | create-feature-branch | Conservative: isolates changes |
| Push | push-after-review | Moderate: backs up work |
| PR | consider-pr | Advisory: lets caller decide |
| Naming | feature/{description} | Generic: works for all types |

### 3.2 Branch Name Generation

Format: `{type}/{brief-description}`

Prefix selection:
- Check for keyword overrides first: "fix/bug/patch/repair" -> `fix/`, "refactor/restructure/reorganize/cleanup" -> `refactor/`
- Fall back to work-type mapping: code -> `feature/`, documentation -> `docs/`, configuration -> `config/`, skill -> `skill/`, mixed -> `feature/`

Name generation:
1. Extract 2-4 keywords from task description.
2. Join with hyphens, lowercase.
3. Truncate at last complete word within 40 characters (never cut mid-word).

### 3.3 Post-Decision Consistency Check

After computing all four decisions independently, apply the five consistency override rules from `references/decision-matrix.md` in order. Log any overrides in the `warnings` array with code "CONSISTENCY_OVERRIDE".

### 3.4 Rationale Quality

Rationale strings follow the situation-implication-action pattern:
- **Situation** (what metrics show): "3 files, 120 lines across 2 directories"
- **Implication** (what this means): "moderate scope change on main branch"
- **Action** (what to do): "create a feature branch to isolate changes"

Example: `"3 files, 120 lines across 2 directories (moderate scope) on main -- feature branch isolates risk and enables PR review."`

For major scope, include: "Consider breaking this into smaller PRs for better review quality (research shows review effectiveness drops significantly above 200 lines)."

### 3.5 Confidence Calibration

Start at "high" and degrade based on conditions:

| Condition | Degradation |
|-----------|-------------|
| Pre-work mode (description only, no git data) | -1 level (start at "medium") |
| Missing `git diff` output (git status only) | -1 level |
| Scope at threshold boundary (aggregation exception triggered) | -1 level |
| Mode detection via keyword heuristic (unclear winner) | -1 level |
| Work type "mixed" (no dominant type) | no degradation |
| Default fallback mode (no signals) | set to "low" |
| Git not initialized | set to "low" (pre-work) or "none" (post-work) |
| Special git state (detached HEAD) | set to "medium" |
| Special git state (merge/rebase in progress) | set to "none" |

Maximum: "high". Minimum: "low" (or "none" for error states). Any 2 degradation conditions = "low".

### 3.6 Output Formatting

**For standalone invocation**, present human-readable summary followed by full YAML:

```
Git Strategy Recommendation
---
Based on your changes (3 files, 120 lines across 2 directories):

  Branch: Create feature branch `feature/add-validation-logic`
  Push:   Push after self-review
  PR:     Create a pull request

  Confidence: High
  Rationale: Moderate code changes on main branch warrant isolation
             and peer review.

Full recommendation written to: /tmp/git-strategy-recommendation.yaml
```

**For orchestrator invocation** (via Task tool), return YAML in the response text AND write to file.

### 3.7 Output File Handling

1. If caller specifies output path: attempt to write there. If parent directory missing or write fails, fall back to `/tmp/git-strategy-recommendation.yaml`.
2. Always return full recommendation in Task tool response text (dual delivery).
3. Log warning with code "OUTPUT_FALLBACK" if fallback path was used.

---

## Output Schema

```yaml
git_strategy_recommendation:
  version: "1.0"
  timestamp: "2026-02-07T10:30:00Z"
  mode: "pre-work" | "post-work"
  confidence: "high" | "medium" | "low" | "none"

  analysis:
    files_changed: 3
    lines_changed: 120
    directories_spanned: 2
    work_type: "code"
    scope: "moderate"

  context:
    current_branch: "main"
    primary_branch: "main"
    is_on_main: true
    has_remote: true

  strategy:
    branch:
      action: "create-feature-branch"
      suggested_name: "feature/add-validation-logic"
      rationale: "3 files, 120 lines across 2 dirs (moderate) on main -- feature branch isolates risk."
    push:
      action: "push-now"
      rationale: "Moderate scope with remote configured -- push to back up work and enable collaboration."
    pr:
      action: "create-pr"
      rationale: "Moderate scope warrants peer review via pull request."

  warnings: []
    # Example entries:
    # - code: "SCOPE_BOUNDARY"
    #   message: "Metrics conflict on scope. Used highest (moderate)."
    # - code: "CONSISTENCY_OVERRIDE"
    #   message: "PR strategy overridden: direct-commit does not use PRs."
    # - code: "GIT_NOT_INITIALIZED"
    #   message: "Git repository not found. Defaults used."

  summary: "Create feature branch `feature/add-validation-logic`, push to remote, and open a PR for review."
```

---

## Error Handling

Errors do NOT abort the pipeline. Phase 3 receives partial data with warnings. The `confidence` field reflects cumulative error severity.

| Phase | Failure | Behavior | Output |
|-------|---------|----------|--------|
| Phase 1 | `git rev-parse` fails (not a repo) | Mode-specific defaults | confidence: "low"/"none" |
| Phase 2 | `git diff` fails but `git status` works | Use file count only | confidence: "medium", warning added |
| Phase 2 | Both git commands fail | Return defaults | confidence: "low", warning added |
| Phase 2 | Empty context (no description, no git data) | Ask user (standalone) or conservative defaults (orchestrator) | confidence: "low" |
| Phase 3 | No matching decision matrix row | Use default actions | confidence: "low", warning added |
| Phase 3 | Scope classification ambiguous | Classify as higher scope | confidence: "medium" |

---

## Integration Notes

### State Management

This skill uses in-context state only. No intermediate files, no session directory, no resume capability. If interrupted, re-invoke. The skill is idempotent.

### Ecosystem Alignment

- **with programming-pm Phase 6**: programming-pm may optionally invoke git-strategy-advisor in post-work mode before its existing branching logic. The advisor may recommend direct-commit for trivial changes or confirm the existing branch-on-main behavior for larger changes. programming-pm's existing Phase 6 logic takes precedence unconditionally; the advisor's recommendation is presented as an informational note.
- **with programming-pm branch naming**: programming-pm uses `{type}/{task-id}-{description}`. git-strategy-advisor uses `{type}/{description}` (no task ID available). If caller provides task ID, include it in the description.
- **with skill-editor Phase 4**: skill-editor may optionally invoke git-strategy-advisor in post-work mode before committing. The advisor may recommend branching for skill changes depending on scope. skill-editor's existing commit logic takes precedence unconditionally; the advisor's recommendation is presented as an informational note.
- **with other orchestrators**: technical-pm, lit-pm, scientific-analysis-architect, and research-pipeline may invoke git-strategy-advisor in post-work mode after completing their workflows to get git recommendations for the produced files.

**Maintenance note**: git-strategy-advisor integration sections exist in 6 orchestrator SKILL.md files (programming-pm, skill-editor, technical-pm, lit-pm, scientific-analysis-architect, research-pipeline). When modifying the integration pattern in any single orchestrator, check all 6 for consistency.

### Invocation Patterns

- **Pattern A** (Orchestrator pre-work): Task tool with `mode: pre-work` and task description. See `examples/pre-work-invocation.md`.
- **Pattern B** (Orchestrator post-work): Task tool with `mode: post-work` and git state. See `examples/post-work-invocation.md`.
- **Pattern C** (Standalone): User asks for git advice directly. Skill reads current git state via Bash.
- **Pattern D** (Bookend): Pre-work invocation at start, post-work re-evaluation at end. Post-work is authoritative.

### Archival Compliance

When writing output files, this skill:
- Uses descriptive filenames (`git-strategy-recommendation.yaml`)
- Includes version and timestamp in the output schema
- Follows the dual-delivery pattern (file + response text) for traceability
