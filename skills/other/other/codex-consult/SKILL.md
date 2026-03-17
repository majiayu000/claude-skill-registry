---
name: codex-consult
description: Get a second opinion from OpenAI Codex on documents, specs, or plans. Use for cross-AI consultation on any content, not just code diffs.
argument-hint: "[FILE] [question/focus] [--upstream FILE] [--research TOPICS] [--model MODEL]"
allowed-tools: Bash, Read, Glob, Grep
---

# Codex Consult

Invoke OpenAI's Codex CLI to review a document or plan, with instructions to research relevant topics before providing feedback.

## When to Use

- You want a second opinion on a generated spec, plan, or document
- Cross-model consultation on non-code content (specs, plans, configs)
- Generation commands (`/product-spec`, `/technical-spec`, etc.) invoke this automatically
- You want Codex to research current documentation before evaluating content

**For code diff reviews**, use `/codex-review` instead.

## Prerequisites

- Codex CLI installed (`codex --version` works)
- Valid OpenAI authentication (`codex login` completed)

## Arguments

| Argument | Example | Description |
|----------|---------|-------------|
| `FILE` | `PRODUCT_SPEC.md` | Document to consult on (first positional arg) |
| `focus` | `completeness` | Focus consultation on specific area |
| `--upstream FILE` | `--upstream PRODUCT_SPEC.md` | Reference document to check alignment against |
| `--research TOPICS` | `--research "Supabase, NextAuth"` | Explicit technologies for Codex to research |
| `--model MODEL` | `--model gpt-5.2` | Use specific model (overrides config) |

## Workflow

Copy this checklist and track progress:

```
Codex Consult Progress:
- [ ] Step 1: Verify Codex CLI available
- [ ] Step 2: Read document content
- [ ] Step 3: Generate consultation prompt
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
CODEX CONSULT: SKIPPED
======================
Reason: Already running inside Codex CLI.

Cross-model consultation requires a different model.
Continuing without cross-model consultation.
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
# Read model from config (codexConsult with fallback to codexReview)
CONSULT_MODEL=$(jq -r '.codexConsult.researchModel // .codexReview.researchModel // "gpt-5.2"' .claude/settings.local.json 2>/dev/null || echo "gpt-5.2")
TIMEOUT_MINS=$(jq -r '.codexConsult.consultTimeoutMinutes // 20' .claude/settings.local.json 2>/dev/null || echo "20")
```

Check enabled status (fallback chain):

```bash
ENABLED=$(jq -r '.codexConsult.enabled // .codexReview.enabled // true' .claude/settings.local.json 2>/dev/null || echo "true")
```

If `enabled` is explicitly `false`, skip with message.

### Select Model

Priority order: `--model` flag > config > default (`gpt-5.2`)

```bash
# 1. Explicit --model flag always wins
if [ -n "$EXPLICIT_MODEL" ]; then
  CODEX_MODEL="$EXPLICIT_MODEL"
# 2. Use configured model
else
  CODEX_MODEL="$CONSULT_MODEL"
fi
```

## Step 2: Read Document Content

Read the target file specified as the first positional argument:

```bash
# Read the document under review
DOCUMENT_CONTENT=$(cat "$TARGET_FILE")
```

If `--upstream` is provided, also read the reference document:

```bash
UPSTREAM_CONTENT=$(cat "$UPSTREAM_FILE")
```

## Step 3: Generate Consultation Prompt

See [PROMPT_TEMPLATE.md](PROMPT_TEMPLATE.md) for the full prompt structure.

Key sections:
1. **Pre-Consultation Research** — Technologies/topics Codex should research
2. **Document Under Review** — Full content of the target file
3. **Reference Document** (if `--upstream` provided) — Requirements to check against
4. **Focus Area** (if focus provided) — Specific area to concentrate on
5. **Evaluation Criteria** — Completeness, accuracy, feasibility, consistency

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
OUTPUT_FILE="/tmp/codex-consult-output-$(date +%s).txt"

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
  echo "WARNING: Codex made commits during consultation. Reverting to pre-consult state."
  git reset --hard "$HEAD_BEFORE"
fi
```

**Important:** Do NOT use `2>&1` — Codex streams progress to stderr and final output to stdout. Merging them corrupts the parseable response.

## Step 5: Present Results

Parse and present the Codex output.

### Output Format (User-Facing)

```
CODEX CONSULTATION COMPLETE
============================
Document: PRODUCT_SPEC.md
Consulted by: Codex ({model})
Status: PASS WITH NOTES

Issues: None

Suggestions:
1. [Section: User Stories] Consider adding edge case for guest users
   -> Suggestion: Add a user story for unauthenticated access

2. [Section: Data Model] Missing field for soft-delete tracking
   -> Suggestion: Add deleted_at timestamp field

Positive Findings:
- Comprehensive coverage of core user workflows
- Clear acceptance criteria for each feature

{If --upstream provided}
Alignment Check: All 5 requirements from PRODUCT_SPEC.md addressed
{/If}
```

### Output Format (Programmatic — for generation commands)

When invoked by another skill, return structured data:

```json
{
  "status": "pass | pass_with_notes | needs_attention | error | skipped",
  "issues": [],
  "suggestions": [],
  "positive_findings": [],
  "alignment_check": {
    "checked": true,
    "all_addressed": true,
    "missing_items": []
  }
}
```

## Error Handling

| Failure | Action |
|---------|--------|
| Codex CLI not found | Report and stop |
| Authentication failed | Suggest `codex login` |
| Target file not found | Report missing file |
| Codex times out | Return partial output if available |
| Output is malformed | Attempt best-effort parsing |

## Configuration

Read from `.claude/settings.local.json`:

```json
{
  "codexConsult": {
    "enabled": true,
    "researchModel": "gpt-5.2",
    "consultTimeoutMinutes": 20
  }
}
```

| Setting | Default | Fallback | Description |
|---------|---------|----------|-------------|
| `enabled` | `true` | `codexReview.enabled` | Set to `false` to disable consultation |
| `researchModel` | `"gpt-5.2"` | `codexReview.researchModel` | Model for consultation tasks |
| `consultTimeoutMinutes` | `20` | — | Max time for consultation invocations |

Existing `codexReview.researchModel` config continues to work via fallback.

**For CI/headless environments:** Set `CODEX_API_KEY` environment variable for authentication without interactive login.

## Examples

**Review a product spec:**
```
/codex-consult PRODUCT_SPEC.md
```

**Check alignment with upstream:**
```
/codex-consult --upstream PRODUCT_SPEC.md TECHNICAL_SPEC.md
```

**Focus on completeness:**
```
/codex-consult completeness --research "user stories, acceptance criteria" FEATURE_SPEC.md
```

**Specific model:**
```
/codex-consult --model gpt-5.2 EXECUTION_PLAN.md
```
