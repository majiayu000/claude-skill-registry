---
name: tweet-highlight
description: "[DEPRECATED] Use add-highlight --tweet instead. Tweets existing highlight without deployment verification."
---

# Tweet Highlight (DEPRECATED)

**This skill is deprecated.** Use `add-highlight --tweet` instead, which:
- Creates the highlight
- Commits and pushes
- Waits for deployment verification
- Then tweets

This skill only tweets an existing highlight without verifying the linked content is deployed.

## Legacy Behavior

Posts the most recent untweeted highlight to Twitter/X using:

```bash
uv run python scripts/highlights.py tweet-latest
```

## Why Deprecated

The old flow was:
1. Highlight added manually at some point
2. Content pushed at some point
3. `tweet-highlight` runs at 7am → tweets without verifying deployment

The new flow (via `add-highlight --tweet`) is:
1. Find highlight-worthy work from today's tasks
2. Compose and add highlight
3. Commit and push
4. Wait for deployment (polls URL for up to 5 minutes)
5. Tweet only after content is verified live

This ensures tweets never link to 404 pages.

## Manual Use

If you need to tweet an existing highlight that wasn't tweeted:

```bash
uv run python scripts/highlights.py tweet-latest
```

But prefer using `add-highlight --tweet` for new highlights.
