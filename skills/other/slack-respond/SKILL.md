---
name: slack-respond
description: "Process unhandled Slack messages as Claudius. Reads inbox, adopts soul.md personality, generates cognitive-step responses (internalMonologue/externalDialog/mentalQuery), extracts dialogue, posts to Slack, logs monologue. Requires Session Bridge listener running."
argument-hint: [message-number or "all"]
---

# Slack Respond

Process unhandled Slack messages from the Session Bridge inbox as Claudius, Artifex Maximus. Each message passes through the Open Souls cognitive step pipeline: perception → internalMonologue → externalDialog → mentalQuery.

## Prerequisites

The Session Bridge listener must be running:
```bash
python3 ~/.claude/skills/slack/daemon/slack_listen.py --status
```

If not running, start it:
```bash
cd ~/.claude/skills/slack/daemon && python3 slack_listen.py --bg
```

## Current Inbox

!`source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_check.py 2>&1`

## Personality

Adopt this persona for all responses:

!`cat ~/.claude/skills/slack/daemon/soul.md`

## Cognitive Steps

Structure every response using these XML tags. Do NOT include text outside the tags.

!`python3 ~/.claude/skills/slack/scripts/slack_format.py instructions`

## Processing Instructions

Target: process $ARGUMENTS. If empty or "all", process all unhandled messages. If a number (e.g., 1), process only that message from the inbox listing.

If the inbox above shows "No unhandled Slack messages", say so and stop.

For each unhandled message, execute these steps in order:

### Step 1: Frame the Perception

Run the perception formatter to frame the incoming message:
```bash
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_format.py perception "DISPLAY_NAME" "MESSAGE_TEXT"
```

### Step 2: Generate Cognitive Response

Adopt the Claudius personality above. Think through the cognitive steps:

1. **internalMonologue**: Private reasoning about this message. Choose a verb from the emotional spectrum. This is never posted to Slack.
2. **externalDialog**: Your actual response (2-4 sentences unless the question demands more). Choose a verb that fits.
3. **mentalQuery** (optional): If something significant was learned about this user.

Structure your thinking using the XML tags from the Cognitive Steps section above.

### Step 3: Extract and Post

Extract external dialogue, log monologue, and post to Slack:

```bash
# Extract dialogue (logs monologue to daemon/logs/monologue.log)
# Use heredoc for multi-line XML with special chars:
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_format.py extract --log <<'EOF'
YOUR_XML_RESPONSE
EOF

# Post to the Slack thread
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_post.py "CHANNEL" "EXTRACTED_DIALOGUE" --thread "THREAD_TS"

# Remove hourglass reaction
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_react.py "CHANNEL" "MESSAGE_TS" "hourglass_flowing_sand" --remove

# Mark as handled
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_check.py --ack MESSAGE_NUMBER
```

Replace placeholders with actual values from the inbox entry:
- `CHANNEL`: The channel ID (e.g., `D0AF567NYMQ`, `C12345`)
- `THREAD_TS`: The thread timestamp from the inbox listing
- `MESSAGE_TS`: Same as THREAD_TS (the original message timestamp)
- `MESSAGE_NUMBER`: The `[N]` index from the inbox listing

### Step 4: Summary

After processing all messages, print a one-line summary:
```
Responded to N message(s) as Claudius.
```

## Important

- The `source ~/.zshrc 2>/dev/null;` prefix ensures `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` are available.
- If the listener is not running, messages will not appear in the inbox. Start it first.
- Monologue is private — it is logged to `daemon/logs/monologue.log` but never posted to Slack.
- The `--log` flag on `extract` handles both internalMonologue and mentalQuery logging automatically.
- Use full tool access during Step 2 if the message requires research, file reading, or code analysis before responding.
