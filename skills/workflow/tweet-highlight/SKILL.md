---
name: tweet-highlight
description: Tweet the most recent untweeted highlight. Scheduled for 7am UTC daily.
---

# Tweet Highlight

Posts the most recent highlight to Twitter/X. This is a scheduled task that runs at 7am UTC daily.

## When to Use

- Automatically invoked by `/evolve` when scheduled (7am UTC, once per day)
- Manual invocation: `/tweet-highlight`

## Instructions

### 1. Check for Recent Highlight

Read the highlights file and find the most recent entry:

```bash
uv run python scripts/highlights.py list --limit 1
```

If no highlights exist or the most recent was already tweeted today, skip silently.

### 2. Check Last Tweet Time

Read `obsidian/workflow/evolution-state.yaml` and check `last_runs.tweet-highlight`.

If already tweeted today (same UTC date), skip to avoid duplicate tweets.

### 3. Post the Tweet

Use the highlights CLI to tweet the most recent highlight:

```bash
uv run python scripts/highlights.py tweet-latest
```

This will:
- Get the most recent highlight
- Format it for Twitter (description + link URL)
- Post via Twitter API
- Return success/failure status

### 4. Update State

After successful tweet, update `last_runs.tweet-highlight` in evolution-state.yaml to the current timestamp.

## Important

- **Max 1 tweet per day** - enforced by checking last_runs timestamp
- **Only runs at/after 7am UTC** - enforced by scheduled_hours constraint
- **Requires Twitter credentials** - if not configured, logs warning and skips
- **Non-blocking** - Twitter failures don't affect other tasks
