---
name: create-review
description: Bootstrap a local AI review pipeline and generate a paste-ready review prompt for any reviewer agent. Use after creating a handoff or when ready to get an AI code review.
author: chalk
version: "1.1.0"
metadata-version: "3"
allowed-tools: Bash, Read, Glob, Grep, Write
argument-hint: "[reviewer-name] e.g. codex, gemini, gpt4, claude — optional, used for labeling only"
read-only: false
destructive: false
idempotent: false
open-world: true
user-invocable: true
tags: review, code-quality, pipeline
capabilities: review.bootstrap, review.prompt.create
activation-intents: create review, start review, generate review prompt
activation-events: user-prompt
activation-artifacts: .chalk/reviews/**
risk-level: medium
---

# Create Review

Bootstrap the review pipeline and generate a paste-ready review prompt for any AI reviewer.

## Step 1: Determine the reviewer and session

**Reviewer:** If the user provided `$ARGUMENTS`, sanitize it to a safe kebab-case string (lowercase, strip any characters that aren't alphanumeric or hyphens, collapse multiple hyphens) and use that as the reviewer name (e.g. `codex`, `gemini`, `gpt4`, `claude`). If no argument, use `generic`.

**Session:** Detect from context:
1. If `.chalk/reviews/` exists, check for the most recent session directory
2. Otherwise, infer from the current branch name (kebab-case)
3. If on `main`/`master`, ask the user

Store as `{reviewer}` and `{session}`.

## Step 2: Bootstrap the review pipeline

Check if `.chalk/reviews/scripts/pack.sh` exists. If not, bootstrap the full pipeline:

```sh
mkdir -p .chalk/reviews/scripts .chalk/reviews/templates .chalk/reviews/sessions
```

### Create `.chalk/reviews/scripts/pack.sh`

This script generates a review context pack from git state:

```sh
#!/usr/bin/env bash
set -euo pipefail

BASE_REF="${1:-origin/main}"
SESSION="${2:-adhoc}"
OUTPUT_PATH="${3:-.chalk/reviews/sessions/${SESSION}/pack.md}"

# Resolve base ref
if ! git rev-parse --verify "$BASE_REF" >/dev/null 2>&1; then
  for candidate in main origin/main master origin/master; do
    if git rev-parse --verify "$candidate" >/dev/null 2>&1; then
      BASE_REF="$candidate"
      break
    fi
  done
fi

MERGE_BASE="$(git merge-base HEAD "$BASE_REF" 2>/dev/null || echo "")"
if [ -z "$MERGE_BASE" ]; then
  MERGE_BASE="$(git rev-list --max-parents=0 HEAD | tail -n 1)"
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"

{
  echo "# Review Pack"
  echo
  echo "- Session: \`$SESSION\`"
  echo "- Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
  echo "- Base ref: \`$BASE_REF\`"
  echo "- Merge base: \`${MERGE_BASE:0:12}\`"
  echo "- Head: \`$(git rev-parse --short HEAD)\`"
  echo
  echo "## Diff Stat"
  echo '```'
  git diff --stat "$MERGE_BASE"..HEAD 2>/dev/null || echo "(no committed diff)"
  echo '```'
  echo
  echo "## Changed Files"
  CHANGED="$(git diff --name-only "$MERGE_BASE"..HEAD 2>/dev/null || true)"
  if [ -n "$CHANGED" ]; then
    echo "$CHANGED" | while IFS= read -r f; do [ -n "$f" ] && echo "- $f"; done
  else
    echo "- (none)"
  fi
  echo
  echo "## Commit Log"
  echo '```'
  git log --oneline "$MERGE_BASE"..HEAD 2>/dev/null || echo "(no commits ahead of base)"
  echo '```'
  echo
  echo "## Working Tree Status"
  echo '```'
  git status --short
  echo '```'
} > "$OUTPUT_PATH"

echo "PACK_PATH=$OUTPUT_PATH"
```

### Create `.chalk/reviews/scripts/render-prompt.sh`

This script combines pack + handoff + reviewer template into a prompt:

```sh
#!/usr/bin/env bash
set -euo pipefail

REVIEWER="${1:?Usage: render-prompt.sh <reviewer> [pack-path] [handoff-path] [output-path]}"
PACK_PATH="${2:-}"
HANDOFF_PATH="${3:-}"
OUTPUT_PATH="${4:-}"
SESSION="${5:-}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

REVIEWER_TITLE="$(echo "$REVIEWER" | awk '{print toupper(substr($0,1,1)) substr($0,2)}')"

if [ -z "$SESSION" ] && [ -f "$ROOT_DIR/.current-session" ]; then
  SESSION="$(cat "$ROOT_DIR/.current-session")"
fi
SESSION="${SESSION:-adhoc}"

[ -z "$PACK_PATH" ] && PACK_PATH="$ROOT_DIR/sessions/$SESSION/pack.md"
[ -z "$HANDOFF_PATH" ] && HANDOFF_PATH="$ROOT_DIR/sessions/$SESSION/handoff.md"
[ -z "$OUTPUT_PATH" ] && OUTPUT_PATH="$ROOT_DIR/sessions/$SESSION/${REVIEWER}.prompt.md"

if [ ! -f "$PACK_PATH" ]; then
  echo "Pack not found at $PACK_PATH. Run pack.sh first." >&2
  exit 1
fi

mkdir -p "$(dirname "$OUTPUT_PATH")"

{
  echo "# $REVIEWER_TITLE Review Request"
  echo

  # Use the universal reviewer template
  TEMPLATE="$ROOT_DIR/templates/reviewer.template.md"
  if [ -f "$TEMPLATE" ]; then
    cat "$TEMPLATE"
  fi

  echo
  echo "---"
  echo
  echo "## Review Pack"
  cat "$PACK_PATH"

  if [ -f "$HANDOFF_PATH" ]; then
    echo
    echo "---"
    echo
    echo "## Handoff"
    cat "$HANDOFF_PATH"
  fi
} > "$OUTPUT_PATH"

echo "PROMPT_PATH=$OUTPUT_PATH"
```

### Create `.chalk/reviews/scripts/copy-prompt.sh`

```sh
#!/usr/bin/env bash
set -euo pipefail

REVIEWER="${1:?Usage: copy-prompt.sh <reviewer> [pack] [handoff] [output] [session]}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

OUTPUT="$(bash "$SCRIPT_DIR/render-prompt.sh" "$@")"
echo "$OUTPUT"

PROMPT_PATH="$(echo "$OUTPUT" | sed -n 's/^PROMPT_PATH=//p' | head -1)"
if [ -z "$PROMPT_PATH" ] || [ ! -f "$PROMPT_PATH" ]; then
  echo "Could not resolve prompt path." >&2
  exit 1
fi

COPIED=0
if command -v pbcopy >/dev/null 2>&1; then
  pbcopy < "$PROMPT_PATH" && COPIED=1 && echo "CLIPBOARD=pbcopy"
elif command -v xclip >/dev/null 2>&1; then
  xclip -selection clipboard < "$PROMPT_PATH" && COPIED=1 && echo "CLIPBOARD=xclip"
elif command -v wl-copy >/dev/null 2>&1; then
  wl-copy < "$PROMPT_PATH" && COPIED=1 && echo "CLIPBOARD=wl-copy"
fi

if [ "$COPIED" -eq 0 ]; then
  echo "CLIPBOARD=none (copy manually from $PROMPT_PATH)"
fi
```

### Create `.chalk/reviews/templates/reviewer.template.md`

Only create if it does not already exist (preserve user customizations):

```markdown
You are acting as an independent code reviewer.

Primary objective:
- Find real defects and risks in changed lines only.
- Prioritize actionable, high-signal output over style commentary.
- Report defects and risks, not style preferences.

Output format (required):

1. `## Verdict`
   - `Block merge: yes|no`
   - `Blocking findings: P0=<n>, P1=<n>`
   - If no P0/P1 findings, include exact text: `No blocking findings`.

2. `## Findings`
   - Use a markdown table with columns:
     - `ID` (R-001, R-002, ...)
     - `Severity` (P0 = critical | P1 = high | P2 = medium | P3 = low)
     - `Category` (Security | Correctness | Performance | Reliability | Testing)
     - `File:Line`
     - `Issue` — concise summary
     - `Failure mode` — what breaks and when
     - `Suggested fix` — actionable next step
     - `Confidence` (0.00–1.00)

3. `## Testing Gaps`
   - List missing tests that could hide regressions.

4. `## Open Questions`
   - Only unresolved assumptions that affect correctness.

Rules:
- Review changed lines only.
- Focus on correctness, security, reliability, and regression risk.
- Do not comment on formatting, import ordering, or trivial naming.
- Do not suggest broad refactors unless required for correctness.
- Keep recommendations patch-oriented and specific to the failure mode.
- If no blocking issues exist, explicitly state: `No blocking findings`.
```

### Make scripts executable

```sh
chmod +x .chalk/reviews/scripts/pack.sh .chalk/reviews/scripts/render-prompt.sh .chalk/reviews/scripts/copy-prompt.sh
```

### Create `.chalk/reviews/PIPELINE.md`

Write a brief usage guide explaining the pipeline, available scripts, and how to add custom reviewer templates. Refresh this on every run.

## Step 3: Resolve the base branch

1. `git merge-base main HEAD` → if it works, use it
2. Try `origin/main`, then `master`, `origin/master`
3. Store as `{base}`

## Step 4: Check for a handoff

Look for `.chalk/reviews/sessions/{session}/handoff.md`. If it exists, it will be included in the prompt. If not, warn the user that no handoff was found and suggest running `/create-handoff` first, but continue anyway.

## Step 5: Generate the review pack

```sh
bash .chalk/reviews/scripts/pack.sh "{base}" "{session}" ".chalk/reviews/sessions/{session}/pack.md"
```

## Step 6: Generate the review prompt

```sh
bash .chalk/reviews/scripts/render-prompt.sh "{reviewer}" \
  ".chalk/reviews/sessions/{session}/pack.md" \
  ".chalk/reviews/sessions/{session}/handoff.md" \
  ".chalk/reviews/sessions/{session}/{reviewer}.prompt.md" \
  "{session}"
```

## Step 7: Copy to clipboard

```sh
bash .chalk/reviews/scripts/copy-prompt.sh "{reviewer}" \
  ".chalk/reviews/sessions/{session}/pack.md" \
  ".chalk/reviews/sessions/{session}/handoff.md" \
  ".chalk/reviews/sessions/{session}/{reviewer}.prompt.md" \
  "{session}"
```

## Step 8: Report to the user

Show:
- The prompt file path
- Whether it was copied to clipboard
- Suggest: paste the prompt into any AI model (Codex, Gemini, GPT, Claude, etc.)
- To run multiple reviews: run the skill again with a different reviewer name for labeling (e.g. `/create-review gemini`)

Also mention:
- The reviewer template at `.chalk/reviews/templates/reviewer.template.md` can be customized
- Each run with a different reviewer name creates a separate prompt file in the session directory

## Step 9: Save current session

Write the session name to `.chalk/reviews/.current-session` so subsequent runs can pick it up.

## Rules

- Only create template files if they don't already exist — preserve user customizations
- Always refresh scripts (pack.sh, render-prompt.sh, copy-prompt.sh) to latest version
- Always refresh PIPELINE.md to latest version
- Do NOT modify any source code
- If no git changes exist ahead of base, warn the user but still generate (they may have local uncommitted work)
