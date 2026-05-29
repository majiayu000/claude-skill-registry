---
name: ai-review
description: >-
  Get AI code review from a second model (Gemini/OpenAI) mid-session via CLI.
  Use when asked to review code, get a second opinion, check quality, or verify
  implementation — especially in unfamiliar stacks.
  Triggers on /ai-review, "review this", "get a second opinion",
  "check with another model".
globs: []
license: MIT
metadata:
  author: eins78
  repo: https://github.com/eins78/skills
  version: "0.0.3"
compatibility: Claude Code, Cursor
---

# AI Code Review

Request code reviews from a second AI model mid-session via CLI.

## Prerequisites

- `gemini` CLI installed (run `${CLAUDE_SKILL_DIR}/scripts/install-dependencies.sh`)
- Auth: either `GEMINI_API_KEY` env var (recommended — see "Paid API" below) or Google Account OAuth (`gemini` interactively once)
- Optional: `codex` CLI for OpenAI reviews: `brew install codex`

## CRITICAL: Never Skip Reviews

**Quality over speed.** When a review is requested, you MUST wait for the result. Do NOT:
- Skip the review because of rate limits or timeouts
- Proceed without the review and say "we can review later"
- Substitute your own review instead of calling the external model

The `gemini` CLI handles rate limit retries automatically. If the script exits with a timeout (exit code 2), ask your human partner for help — do not silently continue.

## Rate Limits (Free Tier — Google Account Auth)

| Metric | Limit |
|---|---|
| Requests per minute | 60 RPM |
| Requests per day | 1,000 RPD |
| **Capacity (tokens/time)** | **Very low — the real bottleneck** |
| Model | Auto-selected by Google (upgrades over time) |
| Cost | $0 |

**Important:** The RPM/RPD limits are rarely the issue. Google also enforces a **capacity quota** (total tokens processed per rolling time window) that is much more restrictive. Large review payloads (code + auto-context) can exhaust this quota in just a few requests, triggering a `TerminalQuotaError` with a multi-hour reset (typically 1-3 hours). This is especially tight on newer auto-selected models (e.g., Gemini 2.5 Pro).

**To reduce quota pressure:**
- Use `--no-context` for small/focused reviews to cut token usage
- Split large reviews into smaller chunks
- Use a paid API key to avoid capacity limits entirely (see below)

The CLI retries automatically on per-minute rate limit hits (resets in seconds). The capacity quota does NOT retry — it requires waiting for the reset window. The script has a 1-hour timeout — if exceeded, it aborts and you should ask the user for help.

## Paid API (Recommended for Regular Use)

The free tier's capacity quota makes it impractical for more than a few reviews per session. A paid API key removes this bottleneck at minimal cost.

### Setup

1. Get a key from [Google AI Studio](https://aistudio.google.com/apikey)
2. **Enable billing** on the associated Google Cloud project — without billing, the API key still uses free-tier capacity limits (the same bottleneck as OAuth). In AI Studio: Settings → Billing, or in the [Google Cloud Console](https://console.cloud.google.com/billing).
3. **Configure the gemini CLI** to use API key auth:
   ```bash
   # Set auth type in gemini settings (~/.gemini/settings.json)
   # Run gemini interactively once — it will prompt to select auth method.
   # Choose "Gemini API Key" when prompted.
   ```
4. Set the environment variable:
   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```
   Add this to your shell profile so new shells pick it up. If you're in an already-running session (e.g., Claude Code), you'll need to source the file or restart the session.
5. Verify it works: `gemini -p "hello"` — should respond without OAuth prompts or quota errors.

### Cost Estimate (Gemini 2.5 Pro)

| | Tokens | Cost |
|---|---|---|
| Input per review (context + diff) | ~8-12K | ~$0.01-0.015 |
| Output per review | ~1-2K | ~$0.01-0.02 |
| **Total per review** | | **~$0.02-0.04** |

| Usage level | Reviews/month | Est. cost |
|---|---|---|
| Light (few/week) | ~20 | ~$0.50 |
| Moderate (few/day) | ~60 | ~$1.50 |
| Heavy (many/day) | ~150 | ~$4.00 |

### Tracking Usage

- **AI Studio** → Dashboard → Usage tab (requests, tokens, costs)
- **Google Cloud Console** → APIs & Services → Dashboard → "Generative Language API"
- **Billing Reports** → group by SKU for per-model breakdown
- **Tip:** Create multiple keys in the same project to separate ai-review usage from interactive gemini CLI use

## How to Use

### Step 1: Determine What to Review

Choose based on context:

| Situation | What to send |
|---|---|
| Just wrote code | The specific files changed |
| Mid-feature | `git diff` (unstaged changes) |
| Before commit | `git diff --cached` (staged changes) |
| Branch review | `git diff main...HEAD` |
| Specific concern | Single file or function |

### Step 2: Run the Review

Use the review script at `${CLAUDE_SKILL_DIR}/scripts/review.sh` — this path resolves to the skill's own directory regardless of the current working directory. **Never use `./scripts/review.sh`** (that's relative to CWD and will fail in other repos). **Never pipe code directly to `gemini` or `codex`** — always use the review script.

```bash
# Review unstaged changes (default)
${CLAUDE_SKILL_DIR}/scripts/review.sh

# Review staged changes
${CLAUDE_SKILL_DIR}/scripts/review.sh --staged

# Review specific files
${CLAUDE_SKILL_DIR}/scripts/review.sh path/to/file1.swift path/to/file2.swift

# Review branch diff vs main
${CLAUDE_SKILL_DIR}/scripts/review.sh --branch

# Review branch vs remote (when working on main directly)
REVIEW_BASE_BRANCH=origin/main ${CLAUDE_SKILL_DIR}/scripts/review.sh --branch

# Add extra context string for better reviews
${CLAUDE_SKILL_DIR}/scripts/review.sh --context "SwiftUI app, iOS 18+, Swift 6" path/to/file.swift

# Review with a specific plan file
${CLAUDE_SKILL_DIR}/scripts/review.sh --plan PLAN.md path/to/file.swift

# Skip auto-context (only send the code/diff)
${CLAUDE_SKILL_DIR}/scripts/review.sh --no-context --staged
```

### Step 3: Act on Feedback

After receiving the review:
1. Address any ERROR-severity issues immediately
2. Consider WARNING items — fix unless there's a good reason not to
3. INFO items are suggestions — use judgment
4. If the review raises questions you're unsure about, discuss with the user

### Handling Failures

| Exit code | Meaning | Action |
|---|---|---|
| 0 | Success | Act on review feedback |
| 1 | No code to review / bad args | Check arguments |
| 2 | Timeout (>1 hour blocked) | **Ask user for help** — do not skip the review |

## Auto-Context

The review script automatically prepends project context to every review so the reviewer understands conventions, architecture, and intent. No manual "Code Review Context" section needed in CLAUDE.md.

**Included automatically** (in order):

1. **Implementation plan** — first found of: `--plan` flag, `PLAN.md` at repo root, most recent `.claude/plans/*.md`
2. **Project instructions** — first found of: `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` at repo root
3. **File tree** — repo structure at depth 3

Use `--no-context` to skip this (e.g., for very large payloads).

The `--context` flag adds an additional inline context string on top of the auto-context.

## Provider Configuration

Default provider is `gemini`. Override per-session:

```bash
# Use OpenAI instead
REVIEW_PROVIDER=codex ${CLAUDE_SKILL_DIR}/scripts/review.sh
```

## Important Notes

- Reviews are advisory — the second model may have false positives
- Large diffs (>50KB) may be truncated. Split into smaller reviews if needed.
- The review model runs in prompt mode (`-p`) and cannot browse the repo. Project context is auto-included to compensate — see "Auto-Context" above.
