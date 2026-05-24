---
name: slack-context-fetcher
description: Fetches Slack thread content using a Slack bot for ticket context enrichment. Use when tickets reference Slack threads or discussions.
---

# Slack Context Fetcher

Fetches Slack thread content when tickets reference Slack discussions. Assumes `SLACK_BOT_TOKEN` environment variable is set.

## Prerequisites

- `SLACK_BOT_TOKEN` env var set (xoxb-... token)
- Bot added to relevant channels

## Workflow

### 1. Detect Slack References

Parse ticket description for Slack links:

```
Pattern: https://{workspace}.slack.com/archives/{channel_id}/p{timestamp}
Example: https://comfy-org.slack.com/archives/C07ABCD1234/p1234567890123456
```

Extract:

- `channel_id`: C07ABCD1234
- `thread_ts`: 1234567890.123456 (insert decimal before last 6 digits)

### 2. Fetch Thread Content

```bash
CHANNEL="C07ABCD1234"
THREAD_TS="1234567890.123456"

curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/conversations.replies?channel=$CHANNEL&ts=$THREAD_TS" | \
  jq '.messages[] | {user: .user, text: .text, ts: .ts}'
```

### 3. Resolve User Names

```bash
curl -s -H "Authorization: Bearer $SLACK_BOT_TOKEN" \
  "https://slack.com/api/users.info?user=$USER_ID" | \
  jq -r '.user.real_name'
```

### 4. Format for Context

```markdown
## Slack Thread Context

**Thread:** [Link](https://comfy-org.slack.com/archives/C07.../p1234...)
**Participants:** Alice, Bob, Charlie
**Messages:** 12

### Full Thread

**Alice** (2024-01-15 10:30):

> Original message about the issue...

**Bob** (2024-01-15 10:45):

> Response with context...
```

### 5. Save to Run Directory

```bash
echo "$SLACK_CONTEXT" > "$RUN_DIR/slack-context.md"

jq '.slackThreads += [{"url": "...", "fetched": "...", "messages": N}]' \
  "$RUN_DIR/ticket.json" > tmp && mv tmp "$RUN_DIR/ticket.json"
```

## Integration with ticket-intake

During ticket-intake, if Slack URLs detected:

1. Parse channel ID and thread timestamp
2. Fetch thread content
3. Save to slack-context.md
4. Include in research context

## Error Handling

| Error               | Cause              | Resolution            |
| ------------------- | ------------------ | --------------------- |
| `channel_not_found` | Invalid channel ID | Verify URL            |
| `not_in_channel`    | Bot not added      | Add bot to channel    |
| `invalid_auth`      | Bad token          | Check SLACK_BOT_TOKEN |

## Output Artifacts

| File             | Location                            | Description             |
| ---------------- | ----------------------------------- | ----------------------- |
| slack-context.md | `runs/{ticket-id}/slack-context.md` | Thread content          |
| ticket.json      | `runs/{ticket-id}/ticket.json`      | Updated with slack refs |
