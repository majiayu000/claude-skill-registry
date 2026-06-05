---
name: x-dm-auto-chat
description: "X (Twitter) DM automated chat end-to-end Skill: scan DM inbox to identify pending-reply conversations, read message history, generate persona-based replies and send; also supports searching users and starting new conversations. Built-in E2E passcode unlock, DM permission filtering, and rate control. Use when user mentions X auto-reply DMs, Twitter DM automated chat, auto-handle unread DMs, reply to X private messages with persona, X DM outreach campaign, batch send DMs to Twitter users, auto-process pending DM replies, Twitter DM bot, automated Twitter outreach, X direct message automation."
---

# X (Twitter) — DM Auto Chat (End-to-End)

> Full X DM automation Skill: inbox scan → conversation read → persona-based reply → send; also supports search-and-outreach. The calling Agent generates reply text based on persona; this Skill handles all mechanical operations.

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Encapsulate "refresh DM list → identify pending replies → read context → reply with persona → send" and "search user → enter chat → send first message" into callable end-to-end capabilities.

## Prerequisites

- Browser is open at X site, logged into X account (`[aria-label="Account menu"]` present)
- The 4-digit DM passcode for the current account is available (required for E2E encryption)
- Caller has prepared a "persona description" (used to generate replies), e.g.:
  - `"You are BrowserAct outreach team. Tone: friendly, concise, professional. Goal: invite creators to collaborate."`
- Optional: list of target user search queries (for outreach scenario)

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

### 2. Open DM Entry + Comprehensive State Check

```
browser-act --session <name> navigate https://x.com/i/chat
browser-act --session <name> wait stable --timeout 15000
browser-act --session <name> eval "$(python scripts/check-page-state.py)"
```

Return format:
```json
{
  "url": "https://x.com/i/chat/pin/recovery?from=%2Fi%2Fchat",
  "logged_in": true,
  "need_passcode": true,
  "on_inbox": false,
  "on_conversation": false,
  "has_panel": false,
  "has_composer": false,
  "inbox_count": 0
}
```

Decision matrix:
- `logged_in: false` → inform user to log in first; wait; retry this step
- `need_passcode: true` → proceed to step 3 below
- `on_inbox: true` and `inbox_count > 0` → ready, enter business flow
- `on_inbox: true` but `inbox_count === 0` → account has no DM conversations; outreach scenario can still proceed, pending-reply scenario has nothing to do

### 3. DM Passcode Unlock (when need_passcode is true)

1. If caller has provided passcode in advance → use it directly; otherwise ask user for 4-digit DM passcode via **AskUserQuestion tool** (do not use plain text prompt — must call AskUserQuestion)
2. `browser-act --session <name> state` — find indexes of 4 `<input maxlength=1 pattern=[0-9]*>` elements (usually 4 consecutive)
3. Enter each digit: `browser-act --session <name> input <idx1> "<d1>"`, `<idx2> "<d2>"`, `<idx3> "<d3>"`, `<idx4> "<d4>"`
   - **Must use `browser-act input` (CDP real keyboard events), cannot use eval to set value** — X ignores non-real keyboard input
4. `browser-act --session <name> wait stable --timeout 10000`
5. Re-run `check-page-state.py`, confirm `need_passcode: false` and `on_inbox: true`
6. 3 consecutive failures still showing `need_passcode: true` → inform user passcode may be wrong; terminate

## Business Flows

> Choose Scenario A, Scenario B, or both. Each scenario is an ordered AI Workflow (not a single JS).

### Scenario A: Scan unread DMs → Persona-based reply

**Flow**: `Scan inbox → Filter unread & latest peer messages → Per-conversation: read context → Generate reply with persona → Send → Next`

**Steps**:

1. **Scan inbox**:
   ```
   browser-act --session <name> eval "$(python scripts/scan-inbox-merged.py)"
   ```
   Returns `items[]`, each containing `conversation_id` / `conversation_url` / `peer_screen_name` / `peer_display_name` / `peer_can_dm` / `latest_message_preview` / `latest_message_from_self` / `unread`, etc.

2. **Filter pending-reply conversations**: from `items`, select conversations meeting all conditions:
   - `unread === true` (has unread) **or** `latest_message_from_self === false` (peer's latest message not yet replied)
   - `peer_can_dm === true` (recipient allows DM)
   - `is_muted !== true` and `is_deleted_by_viewer !== true`
   - Optional caller filters: only reply to specific screen_names, exclude already-replied (use external JSONL ledger)

3. **For each pending-reply conversation** (strictly serial, **random `sleep 8-15` seconds between each**):

   a. **Open conversation**:
      ```
      browser-act --session <name> navigate https://x.com<conversation_url>
      browser-act --session <name> wait stable --timeout 15000
      ```

   b. **If passcode re-triggered** → re-unlock (usually won't re-trigger within same session)

   c. **Read context**:
      ```
      browser-act --session <name> eval "$(python scripts/read-conversation.py)"
      ```
      Returns `messages[]`, each with `direction` (self/peer), `text`, `timestamp_text`, `links`, `images`.

   d. **(Optional) Load full history**: If caller needs longer context, loop:
      ```
      browser-act --session <name> eval "$(python scripts/scroll-load-history.py)"
      ```
      Until `reached_top: true`, then re-read with `read-conversation.py`.

   e. **Generate reply**: **Calling Agent combines persona, message history to generate reply text.** Reply content is entirely the caller's decision; this Skill does not participate in generation. Suggested inputs:
      - Persona prompt (provided by caller)
      - Recent N messages (typically `messages.slice(-6)`)
      - Peer name (`peer_display_name` / `peer_screen_name`) for address
      - Return one string `reply_text`, length < 10,000 characters

   f. **Send reply**:
      1. `browser-act --session <name> eval "$(python scripts/check-composer.py)"` → record `last_message_id`
      2. `browser-act --session <name> state` — find `<textarea placeholder=Message>` index `TA_IDX`
      3. `browser-act --session <name> input <TA_IDX> "<reply_text>"` (**must use CDP real keyboard, cannot use eval**)
      4. `browser-act --session <name> wait --selector '[data-testid="dm-composer-send-button"]' --state attached --timeout 5000`
      5. `browser-act --session <name> eval "document.querySelector('[data-testid=\"dm-composer-send-button\"]').click(); 'clicked'"`
      6. `browser-act --session <name> wait stable --timeout 15000`
      7. Verify: `browser-act --session <name> eval "$(python scripts/verify-sent.py '<reply_text>' --prev-last-id <last_message_id from step f1>)"`
         - `sent: true` and `composer_cleared: true` → success, record result
         - `sent: false` → record failure, **do not retry** (prevents duplicate sends); proceed to next conversation

   g. **Random delay**: `sleep 8-15` seconds (avoid anti-abuse limits)

4. **Batch completion**: Summarize results (success count / failure count / conversation_id per item); return or write to external log file.

### Scenario B: Search users → Start new conversation → Send first message

**Flow**: `Search candidates → Filter sendable → Enter conversation → Generate first message → Send`

**Steps**:

1. **Search target users** (one search per target, **1-2 second interval between searches**):
   ```
   browser-act --session <name> eval "$(python scripts/search-users.py '<search_query>')"
   ```
   Returns `users[]`, each with `user_id` / `name` / `screen_name` / `can_dm` / `can_dm_reason` / verification fields.

2. **Filter users who can receive DMs**:
   - `can_dm === true and !suspended and !protected`
   - `can_dm_reason === "Allowed"`
   - If `screen_name` is already in send history → skip (deduplication)

3. **For each target user** (strictly serial, `sleep 10-20` seconds between each):

   a. **Calculate conversation URL**:
      ```
      browser-act --session <name> eval "$(python scripts/open-conversation-by-user.py '<user_id>')"
      ```
      Returns `conversation_url` (e.g., `/i/chat/{smaller_id}-{larger_id}`).

   b. **Navigate to conversation**:
      ```
      browser-act --session <name> navigate https://x.com<conversation_url>
      browser-act --session <name> wait stable --timeout 15000
      ```

   c. **Handle passcode** (may appear on first DM entry) → unlock

   d. **Verify composer ready**:
      ```
      browser-act --session <name> eval "$(python scripts/check-composer.py)"
      ```
      `composer_ready: true` → record `last_message_id`; `false` → skip this user

   e. **Generate first message**: Calling Agent generates first outreach text `first_text` based on persona + target user info (screen_name / name / verification type). Suggested content:
      - Brief self-introduction (caller identity)
      - Personalized reason for reaching out to this specific user
      - Clear call-to-action
      - Keep length < 500 characters (first messages that are too long are more likely to be flagged as spam)

   f. **Send**: Follow the 7 sub-steps in "Scenario A step 3f", substituting `first_text` for `reply_text`.

   g. **Random delay**: `sleep 10-20` seconds

4. **Batch completion**: Summarize results.

## Capability Components (callable individually)

In addition to the Scenario A / B end-to-end flows, the following components can also be called directly:

### Composite: Inbox scan (API + DOM merged)
`browser-act --session <name> eval "$(python scripts/scan-inbox-merged.py)"`
Returns merged conversation list with peer screen_name + message preview + unread flag.

### API: Fetch inbox from API only (with pagination)
`browser-act --session <name> eval "$(python scripts/fetch-inbox-api.py --cursor-id {cursor_id} --graph-snapshot-id {snap} --limit {N})"`

### DOM: Read current conversation messages
`browser-act --session <name> eval "$(python scripts/read-conversation.py)"`

### DOM: Scroll to load message history
`browser-act --session <name> eval "$(python scripts/scroll-load-history.py)"`

### DOM: Check composer state
`browser-act --session <name> eval "$(python scripts/check-composer.py)"`

### DOM: Verify message was sent
`browser-act --session <name> eval "$(python scripts/verify-sent.py '<expected_text>' --prev-last-id <last_id>)"`

### API: Search X users (with DM permission)
`browser-act --session <name> eval "$(python scripts/search-users.py '<query>')"`

### JS: Calculate conversation URL from user_id
`browser-act --session <name> eval "$(python scripts/open-conversation-by-user.py '<user_id>')"`

### JS: Comprehensive page state check
`browser-act --session <name> eval "$(python scripts/check-page-state.py)"`

## Success Criteria

**End-to-end Scenario A**:
- `sent: true` rate >= 90% for each pending-reply conversation
- Failed conversations have clear reason recorded (wrong passcode, composer unavailable, 429, etc.)

**End-to-end Scenario B**:
- All filtered sendable users enter conversation page (`composer_ready: true`)
- First message `sent: true` rate >= 90%

**Atomic components**: see success criteria in each atomic Skill (scripts in this directory fully reuse the atomic implementations).

## Known Limitations

### X Platform DM Limits (verified through exploration)

- **E2E encryption passcode required**: Must enter 4-digit passcode to unlock DMs; wrong or disconnected passcode loses message history. Passcode input only works via `browser-act input` (CDP real keyboard); eval setting value does not work
- **Message bodies are E2E encrypted**: GraphQL API response message events are base64 T-protocol encrypted binary; plaintext is only readable from the browser's already-unlocked DOM. This Skill must run in an already-logged-in and unlocked browser
- **Peer DM permissions** (`can_dm_reason` enum, observed values): `Allowed` — can send; `InboxClosed` — recipient closed DM; other values (possibly `Blocked`, `NotFollowing`, etc.) treat as cannot send
- **Non-follower DMs go to Message Requests**: First message to a user who doesn't follow you goes to their Message Requests; they must accept before it moves to Primary
- **Send rate (anti-abuse, no official docs)**: Empirical max ~5-10 messages per minute; 8-15 second random delay between messages; exceeding threshold triggers HTTP 429 or UI block
- **Message length cap**: 10,000 characters per message (X official limit)
- **Timestamp precision**: DOM only gives X display format (`"30m"` / `"6:25 PM"` / `"May 8"`); no ISO datetime
- **Attachment messages not covered**: Sending images / GIFs / voice / video / quote tweets not implemented; this Skill handles plain text only

### Additional Skill Limitations

- **Does not participate in reply content generation**: Reply text generation (persona application, context understanding, personalization) is entirely the calling Agent's responsibility; this Skill is the operation layer
- **Does not maintain cross-session state**: Per-run reply history, blocklists, and progress need the caller to record in external files (JSONL)
- **Group conversations**: `peer_*` fields take only the first non-self member; fine-grained replies in group conversations are not supported
- **Message Requests sub-inbox**: Currently only scans Primary inbox; Message Requests are not read; scanning Message Requests requires navigating to a different page — not implemented in this version

## Execution Efficiency

- **Batch processing**: One run processes one batch (N conversations or N target users) then returns; no long-running resident loop — let the caller decide the scheduling cadence
- **Strictly serial**: All DM operations for the same account must be serial — no parallel; parallel operations accelerate anti-abuse triggering
- **No retry on failure**: DM send failures are usually permission / rate / network issues; retrying risks duplicate sends — record uniformly and skip
- **Resume from breakpoint**: Batch tasks use JSONL to record `{target, status, timestamp, error?}` per item; resume from breakpoint on interruption
- **Small-scale validation first**: Before bulk runs, validate the full pipeline with 1-2 items, then scale to full batch
- **Reuse browser session**: Use the same browser-act session (e.g., `--session x-dm`) for the whole batch; passcode unlock and login state persist within the session, no need to re-unlock for each item

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/x-dm-automation-x-dm-auto-chat.memory.md` (working directory is determined by the Agent running the Skill)

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective, a selector changed, a rate threshold discovered); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered, new `can_dm_reason` enum values), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file. Do not record what keywords were used, which conversations were replied to, or how many messages were sent — those are task outputs, not experience.
