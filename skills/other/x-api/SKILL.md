---
name: x-api
description: "Post tweets, build threads, upload media via the X API."
user-invocable: false
agent: python-general-engineer
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
routing:
  triggers:
    - post to X
    - post tweet
    - tweet this
    - build thread
    - post thread
    - twitter thread
    - x api
    - upload media to X
    - read timeline
    - search X
    - search twitter
    - publish to X
    - publish to twitter
  pairs_with:
    - content-engine
  complexity: Medium
  category: content-publishing
---

# X API Skill

## Overview

This skill orchestrates OAuth-authenticated, rate-limit-aware X/Twitter API interactions through a deterministic Python script (`scripts/x-api-poster.py`). The workflow implements a 4-phase pipeline with an explicit confirmation gate (Phase 2) to prevent accidental public posts.

**Core principles**:
- Always validate credentials and content before any network call
- The confirm gate is mechanically enforced by the script (refuses write ops without `--confirmed`)
- Credentials flow from environment variables only; the operator never configures auth mode
- Rate limits are surfaced immediately if remaining capacity drops below 10

---

## Instructions

### Phase 1: VALIDATE

**Goal**: Confirm credentials, content, and dependencies before any network call.

**Step 1: Check credentials**

Test credential presence by running a dry-run credential check:

```bash
python3 $HOME/.claude/scripts/x-api-poster.py post --dry-run --text "ping"
```

This confirms all required environment variables are set: `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`, `X_ACCESS_SECRET`, `X_BEARER_TOKEN`.
- For read-only operations (timeline, search), only `X_BEARER_TOKEN` is required
- For write operations (post, thread), all five are required
- If any required variables are missing, the script exits with a clear error; surface it to the user and stop
- **Important**: Never pass credentials as command arguments or store in files — always read from environment

**Step 2: Validate content length**

The script enforces a 280-character limit per tweet. Before posting, validate your content length:

For a single tweet:
```bash
python3 $HOME/.claude/scripts/x-api-poster.py post --dry-run --text "your tweet text here"
```

For a thread:
```bash
python3 $HOME/.claude/scripts/x-api-poster.py thread --dry-run --texts "part 1" "part 2" "part 3"
```

If `--dry-run` reports a length error, ask the user to shorten the text or approve auto-segmentation into a thread.

**Gate**: Dry run exits 0, content length validates, credentials confirmed present. Proceed only when gate passes.

---

### Phase 2: CONFIRM

**Goal**: Show the user exactly what will be posted and require explicit approval before writing.

This gate is mandatory because X posts are public and irreversible. Present a content preview in this format:

```
CONTENT PREVIEW
================
Tweet 1/1:
  "Your tweet text here"
  Characters: 42/280

Action: POST single tweet

Approve? [yes/no]
```

For a thread:
```
CONTENT PREVIEW
================
Tweet 1/3:
  "First part text"
Tweet 2/3:
  "Second part text"
Tweet 3/3:
  "Third part text"

Action: POST thread (3 tweets, chained replies)

Approve? [yes/no]
```

**Wait for explicit user approval.** The words "yes", "approve", "go ahead", "post it", or equivalent typed in the current conversation turn constitute approval. Do not infer approval from context or prior conversation turns. Do not pass `--confirmed` before the user provides explicit typed approval.

**Gate**: User has typed an explicit approval in this conversation turn. Proceed only when gate passes.

---

### Phase 3: POST

**Goal**: Execute the write operation and capture tweet IDs.

Only proceed once Phase 2 approval is confirmed. Pass the `--confirmed` flag when the user approves in this turn.

**Single tweet:**
```bash
python3 $HOME/.claude/scripts/x-api-poster.py post \
  --confirmed \
  --text "your tweet text here"
```

**Thread:**
```bash
python3 $HOME/.claude/scripts/x-api-poster.py thread \
  --confirmed \
  --texts "part 1" "part 2" "part 3"
```

**Tweet with media:**
```bash
python3 $HOME/.claude/scripts/x-api-poster.py post \
  --confirmed \
  --text "your tweet text here" \
  --media /absolute/path/to/image.jpg
```

**Media constraints**: Images must be <= 5 MB (JPG, PNG, GIF); videos must be <= 512 MB (MP4). Media upload is a two-step process; if either step fails, no orphaned media is left behind. Confirm the file exists and is in a supported format before posting.

Watch output for:
- `[tweet-posted] id=... url=...` — success line per tweet; contains canonical URL (https://x.com/i/web/status/{id})
- `[rate-limit-warning] remaining=N reset=EPOCH` — surface to user immediately if present
- Any `ERROR:` line — surface verbatim and stop

**OAuth mode is automatic**: Read operations use Bearer token only; write operations require full OAuth 1.0a. The script selects the mode based on operation type — do not override it.

**Gate**: Script exits 0, at least one `[tweet-posted]` line in output. Proceed only when gate passes.

---

### Phase 4: REPORT

**Goal**: Return tweet URLs, IDs, and engagement baseline to the user.

**Step 1: Collect tweet IDs from Phase 3 output**

Parse all `[tweet-posted] id=... url=...` lines from the script output.

**Step 2: Read engagement baseline (optional)**

For each posted tweet, you may optionally read initial engagement metrics via:
```bash
python3 $HOME/.claude/scripts/x-api-poster.py read-timeline --user-id me --max-results 5
```

**Engagement metrics have propagation delay**: X API metrics take time to populate. Reading `public_metrics` immediately after posting with 0 impressions is expected behavior, not failure. Report metrics as baseline at post time and note they will grow asynchronously.

**Step 3: Report to user**

Provide:
- Tweet URL(s) as clickable links
- Tweet ID(s) for reference
- Thread structure if applicable (N tweets, root ID)
- Any rate limit warnings encountered
- Engagement baseline if collected (impressions, likes, retweets at T+0), with a note about async growth

---

## Error Handling

### Error: "Missing required environment variable: X_API_KEY"
Cause: One or more credential env vars not set in the shell
Solution:
1. Verify all five variables are exported: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET, X_BEARER_TOKEN
2. For read-only operations, only X_BEARER_TOKEN is required
3. For write operations, all five are required
4. Never pass credentials as command arguments or store in files

### Error: "Tweet text exceeds 280 characters"
Cause: A single tweet segment is too long
Solution:
1. Shorten the text manually
2. Or approve auto-segmentation into a thread — the skill will split on sentence boundaries

### Error: "Write operation requires --confirmed flag"
Cause: Script invoked without confirmation (should not happen if Phase 2 gate was followed)
Solution: Return to Phase 2, present the confirm gate, and obtain explicit user approval

### Error: "403 Forbidden" or "401 Unauthorized"
Cause: Credentials are invalid, expired, or lack the required permissions
Solution:
1. Verify the X developer app has Read and Write permissions enabled
2. Regenerate access tokens after changing app permissions
3. Confirm the app is attached to a Project in the X developer portal

### Error: "429 Too Many Requests" or rate limit exhaustion
Cause: API rate limit window exhausted
Solution:
1. Check x-rate-limit-reset timestamp in the warning output
2. Wait until the reset epoch before retrying
3. X API rate limits are per-15-minute window — a thread of N tweets consumes N requests

### Error: "Media upload failed at step 1" or "Media upload failed at step 2"
Cause: Media upload is a two-step process; failure at either step leaves no orphaned media
Solution:
1. Confirm media file exists and is a supported format (JPG, PNG, GIF, MP4)
2. Check file size: images <= 5 MB, videos <= 512 MB
3. Re-run the post command; the script does not partially attach media on failure

---

## References

- `$HOME/.claude/scripts/x-api-poster.py`: Backing script (exit codes: 0=success, 1=missing credentials, 2=content validation failed, 3=API error, 4=write attempted without --confirmed)
- X API v2 documentation: https://developer.twitter.com/en/docs/twitter-api
- X media upload (v1.1): https://developer.twitter.com/en/docs/twitter-api/v1/media/upload-media/api-reference/post-media-upload
