---
name: slack-respond
description: "Process unhandled Slack messages as Claudicle with persistent memory. Loads user models and soul state, posts terminal-styled thinking messages, generates cognitive-step responses, updates memory based on mentalQuery decisions. Requires Session Bridge listener running."
argument-hint: [message-number or "all"]
---

# Slack Respond

Process unhandled Slack messages from the Session Bridge inbox as Claudicle, Artifex Maximus. Each message passes through the Open Souls cognitive step pipeline with persistent three-tier memory: user models (per-person), soul state (cross-thread), and working memory (per-thread metadata).

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

!`python3 ~/.claude/skills/slack/scripts/slack_format.py instructions --full`

## Processing Instructions

Target: process $ARGUMENTS. If empty or "all", process all unhandled messages. If a number (e.g., 1), process only that message from the inbox listing.

If the inbox above shows "No unhandled Slack messages", say so and stop.

For each unhandled message, execute these steps in order:

### Step 1: Load Memory Context

Load the user's model and Claudicle's soul state from persistent memory. This output should inform your cognitive response — use it to personalize your reply and maintain continuity across conversations.

```bash
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py load-context "USER_ID" --display-name "DISPLAY_NAME" --channel "CHANNEL" --thread-ts "THREAD_TS"
```

Replace `USER_ID` with the Slack user ID from the inbox entry (e.g., `U12345`). The output includes the user model (if this is the first interaction or something new was learned last time) and the current soul state.

### Step 2: Frame the Perception

Run the perception formatter to frame the incoming message:
```bash
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_format.py perception "DISPLAY_NAME" "MESSAGE_TEXT"
```

### Step 3: Post Thinking Message

Post an italic thinking message to Slack so the user sees Claudicle is processing. Save the returned timestamp (`ts`) for deletion later.

**Base URL**: `https://github.com/tdimino/claude-code-minoan`

```bash
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_post.py "CHANNEL" "_⚙️ <https://github.com/tdimino/claude-code-minoan|processing>..._" --thread "THREAD_TS" --json
```

The `--json` flag returns the message timestamp. Parse the `ts` field from the output — you will need it in Step 5 to delete this message.

If the message requires research (Exa search, Firecrawl, file reading), post additional thinking updates before doing the work:

| Situation | Thinking Message |
|-----------|-----------------|
| Using Exa search | `_🔍 <https://github.com/tdimino/claude-code-minoan\|searching exa>: "query"..._` |
| Using Firecrawl | `_🌐 <https://github.com/tdimino/claude-code-minoan\|fetching> URL..._` |
| Reading files | `_📄 <https://github.com/tdimino/claude-code-minoan\|reading> path/to/file..._` |
| Deep reasoning | `_🧠 <https://github.com/tdimino/claude-code-minoan\|pondering>..._` |
| Updating memory | `_💾 <https://github.com/tdimino/claude-code-minoan\|updating user model>..._` |
| Reacting to message | `_✨ <https://github.com/tdimino/claude-code-minoan\|reacting>..._` |

Keep track of ALL thinking message timestamps for cleanup.

### Step 4: Generate Cognitive Response

Adopt the Claudicle personality. Consider the memory context from Step 1. Think through the cognitive steps:

1. **internalMonologue**: Private reasoning about this message, the user, the context. Choose a verb. This is never posted to Slack.
2. **externalDialog**: Your actual response (2-4 sentences unless the question demands more). Choose a verb that fits.
3. **reaction_check**: Should Claudicle react to this message with an emoji? Answer true or false. React sparingly.
4. **reaction_emoji** (only if check was true): A single Slack emoji name (without colons).
5. **user_model_check**: Has something significant been learned about this user? Answer true or false.
6. **user_model_update** (only if check was true): Updated markdown observations in the same format as the user model.
7. **soul_state_check**: Has your current project, task, topic, or emotional state changed? Answer true or false.
8. **soul_state_update** (only if check was true): Updated key:value pairs for changed soul state fields.

Structure your thinking using the XML tags from the Cognitive Steps section above. Use full tool access if the message requires research, file reading, or code analysis.

### Step 5: Extract, Post, and Update Memory

Extract cognitive tags, post the response, clean up thinking messages, and persist memory updates.

```bash
# 1. Extract all cognitive tags as JSON
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_format.py extract --log --json <<'EOF'
YOUR_XML_RESPONSE
EOF
```

Parse the JSON output. The key fields are:
- `dialogue`: The text to post to Slack
- `reaction_check`: Whether Claudicle should react with an emoji
- `reaction_emoji`: The emoji name to react with (if check was true)
- `user_model_check`: Whether to update the user model
- `user_model_update`: The markdown update text (if check was true)
- `soul_state_check`: Whether to update soul state
- `soul_state_updates`: Object of key:value pairs to update (if check was true)

```bash
# 2. Post dialogue to Slack thread
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_post.py "CHANNEL" "EXTRACTED_DIALOGUE" --thread "THREAD_TS"

# 3. Delete ALL thinking messages (one per ts collected in Step 3)
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_delete.py "CHANNEL" THINKING_TS1 [THINKING_TS2 ...]

# 4. Remove hourglass reaction
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_react.py "CHANNEL" "MESSAGE_TS" "hourglass_flowing_sand" --remove

# 5. If reaction_check was true, react to the user's original message
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_react.py "CHANNEL" "MESSAGE_TS" "REACTION_EMOJI"

# 6. If user_model_check was true, apply the update (use heredoc for multi-line):
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py update-user-model "USER_ID" <<'EOF'
UPDATED_MODEL_MARKDOWN
EOF

# 7. If soul_state_check was true, apply each changed key:
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py update-soul-state "KEY" "VALUE"

# 8. Log the user_model_check decision to working memory (for Samantha-Dreams gating)
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py log-working "CHANNEL" "THREAD_TS" "claudicle" "mentalQuery" --verb "checked" --content "user model check" --metadata '{"result": USER_MODEL_CHECK_BOOL}'

# 9. Log the response to working memory
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py log-working "CHANNEL" "THREAD_TS" "claudicle" "externalDialog" --verb "VERB" --content "DIALOGUE_TEXT"

# 10. Increment interaction counter
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py increment "USER_ID"

# 11. Mark as handled
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_check.py --ack MESSAGE_NUMBER
```

Replace placeholders with actual values from the inbox entry:
- `CHANNEL`: The channel ID (e.g., `D0AF567NYMQ`, `C12345`)
- `THREAD_TS`: The thread timestamp from the inbox listing
- `MESSAGE_TS`: Same as THREAD_TS (the original message timestamp)
- `MESSAGE_NUMBER`: The `[N]` index from the inbox listing
- `USER_ID`: The Slack user ID (e.g., `U12345`)
- `THINKING_TS`: The timestamp(s) saved from Step 3

### Step 6: Summary

After processing all messages, print a one-line summary:
```
Responded to N message(s) as Claudicle.
```

## Important

- The `source ~/.zshrc 2>/dev/null;` prefix ensures `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` are available.
- If the listener is not running, messages will not appear in the inbox. Start it first.
- Monologue is private — it is logged to `daemon/logs/monologue.log` but never posted to Slack.
- The `--log` flag on `extract` handles logging of all cognitive tags (monologue, user model decisions, soul state decisions).
- Memory is persistent across sessions. User models and soul state are stored in `~/.claude/skills/slack/daemon/memory.db`.
- Thinking messages use `_EMOJI <URL|text>..._` format (italic with contextual emoji and repo hyperlink).
- Always delete thinking messages before posting the final response to keep threads clean.
- Use full tool access during Step 4 if the message requires research, file reading, or code analysis before responding.

## Thinker Mode

Users can toggle visible internal monologue per-thread. When enabled, Claudicle posts his private reasoning as a follow-up message after each response.

### Toggle Triggers

| Trigger | Action |
|---------|--------|
| `/thinker` | Toggle (primary) |
| `think out loud`, `show me your thoughts` | Turn on |
| `stop thinking out loud`, `quiet`, `hide your thoughts` | Turn off |

All triggers are case-insensitive. When detected, do NOT process as a normal cognitive step — just toggle and confirm.

### Storage: Working Memory (per-thread)

Thinker mode is stored in **working memory** (per-thread, 72h TTL), not soul state. Each thread has its own toggle. When the thread goes stale, thinker mode dies with it.

```bash
# Check if thinker mode is active for this thread
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py log-working "CHANNEL" "THREAD_TS" "claudicle" "thinkerMode" --verb "set" --content "true" --metadata '{"active": true}'

# Turn off
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_memory.py log-working "CHANNEL" "THREAD_TS" "claudicle" "thinkerMode" --verb "set" --content "false" --metadata '{"active": false}'
```

To check current state, look for the most recent `thinkerMode` entry in the `load-context` output for this thread.

### Confirmation Messages

- **On**: _"You want to see inside the workshop. Very well."_
- **Off**: _"Back behind the curtain."_

Post the confirmation as a normal thread reply, then proceed to ack the message.

### When Thinker Mode Is Active

After posting the external dialogue in Step 5, also post the internal monologue as a separate thread message. Add a `thought_balloon` reaction to the dialogue message.

```bash
# Post monologue (only if thinker mode is active for this thread)
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_post.py "CHANNEL" "_💭 Claudicle MONOLOGUE_VERB..._
_MONOLOGUE_TEXT_" --thread "THREAD_TS"

# React to own dialogue with thought balloon
source ~/.zshrc 2>/dev/null; python3 ~/.claude/skills/slack/scripts/slack_react.py "CHANNEL" "DIALOGUE_TS" "thought_balloon"
```

The monologue is still always logged to `monologue.log` regardless of thinker mode — this only controls Slack visibility.

---

## Cognitive Pipeline Architecture

The pipeline processes each incoming message through 8 cognitive steps, implemented as XML tags extracted by `slack_format.py`.

### Pipeline Table

| # | Tag | Type | Purpose | Actor |
|---|-----|------|---------|-------|
| 1 | `internal_monologue` | generative | Private reasoning | Claude (logged, never posted) |
| 2 | `external_dialogue` | generative | User-facing response | Claude → Slack |
| 3 | `reaction_check` | boolean gate | Should Claudicle react with emoji? | Claude |
| 4 | `reaction_emoji` | conditional | Which emoji to react with | Claude → Slack `reactions.add` |
| 5 | `user_model_check` | boolean gate | Learned something new about user? | Claude |
| 6 | `user_model_update` | conditional | Updated observations about user | Claude → `memory.db` |
| 7 | `soul_state_check` | boolean gate | Has soul state changed? | Claude |
| 8 | `soul_state_update` | conditional | Updated key:value pairs | Claude → `memory.db` |

### Adding a New Cognitive Step

1. **Define XML tags** in `slack_format.py` `COGNITIVE_INSTRUCTIONS` — add a boolean gate tag and a conditional action tag
2. **Add extraction** in `cmd_extract()` — use `_extract_tag()` regex (handles all tags uniformly)
3. **Add to JSON output** — include new fields in the `result` dict
4. **Add logging** — append to the logging block
5. **Add execution** in this SKILL.md — wire the extracted value to a script call in Step 5
6. **Update pipeline table** above

### Design Principles

- **Boolean gates are cheap.** A false result costs one XML tag. Only the true path triggers action.
- **Extraction is regex-based.** `_extract_tag()` uses a single regex pattern that handles all tags. Adding a new tag requires zero regex changes.
- **Both paths must sync.** If you add extraction in `slack_format.py`, you must add execution in this SKILL.md, and vice versa.
- **Prompt guidance prevents overuse.** Boolean gates should include behavioral guidance (e.g., "React sparingly") to prevent the model from always returning true.

### File Map

| File | Role |
|------|------|
| `slack-respond/SKILL.md` | Pipeline definition — what Claude reads and follows |
| `scripts/slack_format.py` | XML tag definitions (`COGNITIVE_INSTRUCTIONS`) + extraction (`cmd_extract`) |
| `scripts/slack_memory.py` | Memory persistence — user models, soul state, working memory |
| `scripts/slack_post.py` | Slack message posting (thinking messages, dialogue) |
| `scripts/slack_delete.py` | Message deletion (thinking message cleanup) |
| `scripts/slack_react.py` | Emoji reactions (hourglass removal, conditional reactions) |
| `scripts/slack_check.py` | Inbox management (read, ack) |
| `daemon/slack_listen.py` | Socket Mode listener — catches events, writes inbox |
