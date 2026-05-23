---
name: bird-cli
description: Read-only usage of the bird CLI for X/Twitter accounts (timelines, mentions, and analysis). Trigger when asked to inspect whoami, timelines, mentions, replies, search, or reporting tasks without account mutations.
---

# Bird CLI

## Safety Policy (Hard Rules)

This skill is **read-only** with respect to X/Twitter account state.

- Never use commands that publish or mutate account state.
- If a request asks for posting or account mutations, refuse that part and offer a read-only alternative.

### CRITICAL: bird's default subcommand is `tweet` (PUBLISH)
- Running `bird <any-text>` without a subcommand will PUBLISH that text as a tweet
- To READ a tweet, ALWAYS use `bird read <id-or-url>` — never just `bird <id>`
- This is the #1 source of accidental tweets. Triple-check every bird command.

### Forbidden Commands (never run)

- `bird tweet`
- `bird reply`
- `bird follow`
- `bird unfollow`
- `bird unbookmark`

### Allowed Commands (query/inspection only)

- `bird whoami`
- `bird check`
- `bird read`
- `bird replies`
- `bird thread`
- `bird search`
- `bird mentions`
- `bird bookmarks`
- `bird likes`
- `bird home`
- `bird following`
- `bird followers`
- `bird lists`
- `bird list-timeline`
- `bird about`
- `bird user-tweets`
- `bird news` / `bird trending`
- `bird query-ids` (including `--fresh`)
- NEVER run `bird <id-or-url>` without a subcommand — bird's default subcommand is `tweet` (publish), NOT `read`. Always use `bird read <id-or-url>` explicitly.

## Quick Start

- Prefer explicit cookie source and browser profile to avoid Safari auto-detection.
- If multiple accounts exist, pass `--chrome-profile` and `--username` explicitly.
- Defaults can be set in `~/.config/skills/config.json` under `bird` (`chrome_profile`, `username`).

## Task: List unanswered mentions (most recent first)

- Run `scripts/unanswered_mentions.py` with the target profile.
- If auto-detection fails, pass `--username`.
- The script checks `bird replies <tweet>` for a reply authored by the target username (heuristic).

Examples:

```bash
python scripts/unanswered_mentions.py --cookie-source chrome --chrome-profile "<Profile>" --json-out /tmp/bird-unanswered.json --numbered
```

```bash
python scripts/unanswered_mentions.py --cookie-source chrome --chrome-profile "<Profile>" --show-text --limit 10
```

Output format:

```
<createdAt> | @author | https://x.com/<author>/status/<id>
```

## Resources

- `scripts/unanswered_mentions.py`: lists unanswered mentions in descending date order.
- `scripts/daily_brief.py`: daily brief of AI/dev news + home candidates.

## Task: Daily brief (AI + dev)

Run:

```bash
python scripts/daily_brief.py
```

Defaults: AI news + Home following, prints 5 news items and 10 home candidates.

Optional flags:

```bash
python scripts/daily_brief.py --news-count 5 --home-results 10
python scripts/daily_brief.py --allow-for-you   # use For You instead of Following
python scripts/daily_brief.py --json-out /tmp/bird-daily.json
```
- `scripts/ignore_mentions.py`: mark mention IDs as ignored so they stop appearing.
