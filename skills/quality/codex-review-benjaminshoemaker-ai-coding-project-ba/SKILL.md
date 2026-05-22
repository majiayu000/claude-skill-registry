---
name: codex-review
description: Have OpenAI Codex review the current branch with documentation research. Use for second-opinion code reviews or when you want cross-AI verification.
argument-hint: "[focus] [--upstream FILE] [--research TOPICS] [--base BRANCH] [--model MODEL]"
allowed-tools: Bash, Read, Glob, Grep
---

# Codex Review

Invoke OpenAI's Codex CLI to review the current branch, with instructions to research relevant documentation before reviewing.

## When to Use

- You want a second opinion on your implementation
- You want cross-verification between different AI models
- The implementation uses tools/libraries where current docs would help
- You've completed a feature and want thorough review before merging
- `/phase-checkpoint` invokes this for cross-model review (Step 4)

## Prerequisites

- Codex CLI installed (`codex --version` works)
- Valid OpenAI authentication (`codex login` completed)
- On a feature branch with commits to review

## Arguments

| Argument | Example | Description |
|----------|---------|-------------|
| `focus` | `security` | Focus review on specific area |
| `--upstream FILE` | `--upstream PRODUCT_SPEC.md` | Check that code preserves requirements from upstream doc |
| `--research TOPICS` | `--research "Supabase, NextAuth"` | Explicit technologies for Codex to research |
| `--base BRANCH` | `--base develop` | Compare against different base branch |
| `--model MODEL` | `--model gpt-5.2-codex` | Use specific Codex model |

## Workflow

Copy this checklist and track progress:

```
Codex Review Progress:
- [ ] Step 1: Verify Codex CLI available
- [ ] Step 2: Gather branch context
- [ ] Step 3: Generate review prompt
- [ ] Step 4: Invoke Codex
- [ ] Step 5: Present results
```

## Step 1: Verify Codex CLI

### Check if Running Inside Codex

```bash
# Codex sets CODEX_SANDBOX when running
if [ -n "$CODEX_SANDBOX" ]; then
  echo "RUNNING_IN_CODEX"
fi
```

**If running inside Codex CLI:**
```
CODEX REVIEW: SKIPPED
=====================
Reason: Already running inside Codex CLI.

Cross-model verification requires a different model.
Continuing without cross-model verification.
```

Return early. Do NOT block the parent workflow.

### Check Codex CLI Installed

```bash
codex --version
```

If not installed:
```
Codex CLI is not installed or not in PATH.

Install: https://github.com/openai/codex
Then run: codex login
```

### Check Authentication

```bash
codex login status
```

If not authenticated:
```
Codex authentication failed. Run:
  codex login
```

**If ANY pre-flight check fails:** Report the specific failure and STOP.
Do NOT attempt alternative commands or workarounds. Return status: `skipped`.

### Read Configuration

Read `.claude/settings.local.json` for settings:

```bash
# Read config
CODE_MODEL=$(jq -r '.codexReview.codeModel // "gpt-5.3-codex"' .claude/settings.local.json 2>/dev/null || echo "gpt-5.3-codex")
TIMEOUT_MINS=$(jq -r '.codexReview.reviewTimeoutMinutes // 20' .claude/settings.local.json 2>/dev/null || echo "20")
```

If `codexReview.enabled` is explicitly `false`, skip with message.

### Select Model

Priority order: `--model` flag > config > default (`gpt-5.3-codex`)

```bash
# 1. Explicit --model flag always wins
if [ -n "$EXPLICIT_MODEL" ]; then
  CODEX_MODEL="$EXPLICIT_MODEL"
# 2. Use configured code model
else
  CODEX_MODEL="$CODE_MODEL"
fi
```

**Note:** For reviewing non-code documents (specs, plans), use `/codex-consult` instead.

## Step 2: Gather Branch Context

Collect information about the current branch:

```bash
# Current branch name
git branch --show-current

# Commits on this branch (vs main or specified base)
BASE_BRANCH="${BASE:-main}"
git log --oneline $BASE_BRANCH..HEAD 2>/dev/null || git log --oneline -10

# Changed files summary
git diff $BASE_BRANCH...HEAD --stat 2>/dev/null || git diff HEAD~5 --stat

# Get the merge base
git merge-base $BASE_BRANCH HEAD 2>/dev/null
```

**Auto-detect research topics** from changed files if `--research` not provided:
- Check `package.json` for dependencies
- Look at import statements in changed files
- Identify frameworks (Next.js, React, etc.)

## Step 3: Generate Review Prompt

See [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) for the full prompt structure.

Key sections:
1. **Pre-Review Research** — Technologies Codex should research
2. **Review Context** — Branch, commits, changed files
3. **Upstream Context** (if `--upstream` provided) — Requirements to preserve
4. **Review Instructions** — What to check, output format

## Step 4: Invoke Codex

See [CODEX_INVOCATION.md](CODEX_INVOCATION.md) for detailed command building.

**IMPORTANT — Execution Rules:**
- Execute synchronously. NEVER use `run_in_background` for Codex invocations.
- If this command fails, report the exit code and return `status: error`.
  Do NOT retry with different flags or subcommands.
- Use the Bash tool's `timeout` parameter set to `TIMEOUT_MINS * 60 * 1000` (ms)
  instead of the shell `timeout` command or `run_in_background`.

### Safety Guard (prevent accidental commits)

Before invoking Codex, protect the working tree:

```bash
# Record current HEAD so we can detect if Codex makes commits
HEAD_BEFORE=$(git rev-parse HEAD)
```

**Note:** Do NOT stash uncommitted changes — stash/pop triggers file-system events
that confuse IDE watchers, hot-reload, and other processes. The HEAD check alone is sufficient.

### Invoke Codex

```bash
OUTPUT_FILE="/tmp/codex-review-output-$(date +%s).txt"

# Build model flag
MODEL_FLAG=""
if [ -n "$CODEX_MODEL" ]; then
  MODEL_FLAG="--model $CODEX_MODEL"
fi

# Execute (use Bash tool's timeout parameter for timeout — NOT shell `timeout`)
cat {prompt_file} | codex exec \
  --sandbox danger-full-access \
  -c 'approval_policy="never"' \
  -c 'features.search=true' \
  $MODEL_FLAG \
  -o $OUTPUT_FILE \
  -
EXIT_CODE=$?
```

### Post-Invocation Safety Check

```bash
# Check if Codex made any commits
HEAD_AFTER=$(git rev-parse HEAD)
if [ "$HEAD_BEFORE" != "$HEAD_AFTER" ]; then
  echo "WARNING: Codex made commits during review. Reverting to pre-review state."
  git reset --hard "$HEAD_BEFORE"
fi
```

**Flags explained:**
- `--sandbox danger-full-access`: Enables network access for documentation research
- `-c 'approval_policy="never"'`: Non-interactive execution
- `-c 'features.search=true'`: Enable web search for documentation research
- `-o $OUTPUT_FILE`: Write final response to file for reliable parsing
- `-`: Read prompt from stdin

**Important:** Do NOT use `2>&1` — Codex streams progress to stderr and final output to stdout. Merging them corrupts the parseable response.

## Step 5: Present Results

Parse and present the Codex output. See [EVALUATION_PRACTICES.md](EVALUATION_PRACTICES.md) for severity classification.

### Output Format (User-Facing)

```
CODEX REVIEW COMPLETE
=====================
Branch: feature/add-auth
Reviewed by: Codex ({model})
Status: PASS WITH NOTES

Critical Issues: None

Recommendations:
1. [src/auth/handler.ts:45] Consider adding rate limiting
   → Suggestion: Use express-rate-limit middleware

2. [src/auth/session.ts:12] Session expiry not explicitly configured
   → Suggestion: Add explicit maxAge to session config

Positive Findings:
- Good separation of concerns in auth module
- Proper error handling for OAuth failures

{If --upstream provided}
Context Preservation: ✓ All 5 items from PRODUCT_SPEC.md preserved
{/If}
```

### Output Format (Programmatic — for /phase-checkpoint)

When invoked by another skill, return structured data:

```json
{
  "status": "pass | pass_with_notes | needs_attention | error | skipped",
  "critical_issues": [],
  "recommendations": [],
  "positive_findings": [],
  "context_preservation": {
    "checked": true,
    "all_preserved": true,
    "missing_items": []
  }
}
```

## Error Handling

| Failure | Action |
|---------|--------|
| Codex CLI not found | Report and stop |
| Authentication failed | Suggest `codex login` |
| No commits on branch | Report nothing to review |
| Codex times out | Return partial output if available |
| Output is malformed | Attempt best-effort parsing: extract any text between known markers (e.g., "Critical Issues:", "Recommendations:"). If no structure found, return the raw output as a single recommendation with status `pass_with_notes` and note "Codex output could not be parsed — raw response included" |

## Configuration

Read from `.claude/settings.local.json`:

```json
{
  "codexReview": {
    "enabled": true,
    "codeModel": "gpt-5.3-codex",
    "reviewTimeoutMinutes": 20
  }
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `enabled` | `true` | Set to `false` to disable Codex review |
| `codeModel` | `"gpt-5.3-codex"` | Model for code review tasks |
| `reviewTimeoutMinutes` | `20` | Max time for review invocations |

For document consultation (specs, plans), see `/codex-consult` which uses `codexConsult` config.
For task execution via Codex, see `/phase-start --codex` which uses `codexReview.taskTimeoutMinutes`.

**For CI/headless environments:** Set `CODEX_API_KEY` environment variable for authentication without interactive login.

## Examples

**Basic review:**
```
/codex-review
```

**Focus on security:**
```
/codex-review security
```

**Verify against upstream spec:**
```
/codex-review --upstream PRODUCT_SPEC.md
```

**Explicit research topics:**
```
/codex-review --research "Supabase Auth, Next.js App Router"
```

**Different base branch and model:**
```
/codex-review --base develop --model gpt-5.2-codex
```
