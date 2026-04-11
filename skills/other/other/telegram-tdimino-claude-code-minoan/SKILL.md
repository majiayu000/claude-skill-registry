---
name: telegram
description: Send, read, and respond to Telegram messages as Claudicle via the @claudicle_bot Bot API. Use this skill when sending Telegram messages (text, Markdown, inline keyboards), building approval gates with tappable buttons, checking the shared inbox for unhandled Telegram messages, answering callback queries, managing Telegram memory context, or checking bot and listener status. Five purpose-built scripts (send, check, status, callback, memory) wrap the python-telegram-bot v22 polling adapter at ~/.claudicle/adapters/telegram/ with REST-based senders (no asyncio). Pairs with /telegram-respond for the cognitive pipeline and with mazkir-callback-watcher.py for the Mazkir approval gate.
---

# Telegram

Send, read, and respond to Telegram messages through a Claudicle Telegram bot.
This skill is the thin Claude-facing layer over the `python-telegram-bot` v22
polling adapter at `~/.claudicle/adapters/telegram/`. Send scripts use REST
directly (via `requests`), not asyncio, so they work reliably inside any
subprocess or skill invocation.

## Portability

This skill is machine-agnostic. It depends only on:

- The Claudicle adapter directory at `~/.claudicle/adapters/telegram/` (set up
  by the [Claudicle framework](https://github.com/tdimino/claudicle) / the
  `claude-code-minoan` distribution).
- A Telegram bot token in `~/.config/env/secrets.env`.
- Python 3.9+ for the REST-based send/status/callback scripts; Python 3.10+
  for the listener.

All paths resolve from `Path.home()`. No machine-specific hardcoded paths.
The Mazkir integration and the launchd deployment notes below are concrete
examples of how one operator (Tom) runs the skill — they describe a pattern,
not a requirement. The skill is fully usable without any of that.

## When to Use This Skill

- Send a Telegram message (text, Markdown, HTML, reply threading)
- Build an approval gate with inline keyboard buttons (tap-to-approve/reject flows)
- Check the shared inbox for unhandled Telegram messages
- Read pending callback queries from tapped buttons
- Answer a callback query (clear the spinner, show a toast to the user)
- Check bot identity and listener health before debugging a failed send
- Load Telegram memory context (working memory, user models, soul state)
- Launch the full cognitive pipeline on unhandled messages via `/telegram-respond`

## Prerequisites

- `TELEGRAM_BOT_TOKEN` in `~/.config/env/secrets.env`
- `pip install --break-system-packages requests` (send/status/callback scripts)
- `pip install --break-system-packages python-telegram-bot` (only for the listener)
- **Python 3.10+** for the listener. Python 3.9 has an asyncio event loop bug
  that breaks `CallbackQueryHandler` in `python-telegram-bot` v22. On macOS
  the listener must use `/opt/homebrew/bin/python3` (Homebrew Python 3.14),
  not `/usr/bin/python3` (system 3.9). The skill's `telegram_send.py`,
  `telegram_status.py`, and `telegram_callback.py` use REST instead and work
  on any Python 3.9+.
- A bot created via [@BotFather](https://t.me/BotFather). Tom's instance runs
  `@claudicle_bot` (ID: 8646522411); yours will differ.
- Your Telegram user ID for DMs, or a group/channel chat ID. Find your own
  user ID by DM'ing [@userinfobot](https://t.me/userinfobot).

## Quick Start

Replace `<CHAT_ID>` with your Telegram chat or user ID.

```bash
# Send a message
python3 ~/.claude/skills/telegram/scripts/telegram_send.py <CHAT_ID> "Hello from Claudicle!"

# Markdown formatting
python3 ~/.claude/skills/telegram/scripts/telegram_send.py <CHAT_ID> "*bold* _italic_" --parse-mode Markdown

# Inline keyboard (approval gate)
python3 ~/.claude/skills/telegram/scripts/telegram_send.py <CHAT_ID> "Approve dispatch?" \
  --buttons '[["Approve|approve_day42","Reject|reject_day42"]]'

# Read incoming messages
python3 ~/.claude/skills/telegram/scripts/telegram_check.py

# Read pending button taps
python3 ~/.claude/skills/telegram/scripts/telegram_callback.py --prefix approve:

# Check bot + listener health
python3 ~/.claude/skills/telegram/scripts/telegram_status.py

# Run the full cognitive pipeline on unhandled messages
/telegram-respond
```

## Available Scripts

### `telegram_send.py` — Send Messages

REST-based sender. Supports parse_mode, reply threading, stdin, silent mode,
and inline keyboards. Long messages auto-split on newline boundaries; the
keyboard attaches to the final chunk so the tap target lands on the most
recent message.

```bash
python3 telegram_send.py CHAT_ID "text" [OPTIONS]
```

| Flag | Description |
|------|-------------|
| `--reply-to MSG_ID` | Reply to a specific message (thread in groups) |
| `--parse-mode MODE` | `Markdown`, `MarkdownV2`, or `HTML` |
| `--buttons JSON` | Inline keyboard as JSON (see format below) |
| `--stdin` | Read message text from stdin |
| `--silent` | Send without notification sound |

**Button format**: a list of rows, each row a list of `"Label|callback_data"`
strings. To emit a URL button instead of a callback button, use
`"Label|url:https://..."`.

```bash
# Two buttons on one row
--buttons '[["Approve|approve_day42","Reject|reject_day42"]]'

# Two rows, one button each (stacked)
--buttons '[["Option A|opt_a"],["Option B|opt_b"]]'

# URL button mixed with callback
--buttons '[["View|url:https://example.com","Dismiss|dismiss"]]'
```

On success, prints one message_id per line to stdout so callers can capture
them for later editing or referencing.

**Parse mode fallback**: if Telegram rejects the formatting (e.g., unescaped
special chars in Markdown), the script retries once as plain text and prints
a warning to stderr rather than failing the send.

### `telegram_check.py` — Read Inbox

Reads `~/.claudicle/daemon/inbox.jsonl`, filtered to `telegram:*` channels.
Same shape as the SMS and Slack check scripts.

```bash
python3 telegram_check.py                    # Unhandled messages
python3 telegram_check.py --all              # Include handled
python3 telegram_check.py --limit 5          # Last N
python3 telegram_check.py --mark-read TS     # Mark one handled
python3 telegram_check.py --mark-all-read    # Mark all telegram entries handled
```

### `telegram_callback.py` — Callback Query Reader

Reads `entry_type: "telegram_callback"` entries from the same inbox. These
are written by the listener's `CallbackQueryHandler` whenever a user taps
an inline keyboard button. Supports prefix filtering (useful for namespacing
approval flows), marking handled, and answering the callback to clear the
spinner.

```bash
# All pending button taps
python3 telegram_callback.py

# Only a specific namespace
python3 telegram_callback.py --prefix "approve:"

# Clear the Telegram spinner on a specific tap
python3 telegram_callback.py --answer QUERY_ID "Received — processing."

# Mark handled so it stops showing up
python3 telegram_callback.py --mark-read 1775828391.0
```

Telegram expects `answerCallbackQuery` to be called within about 30 seconds
of the tap, or the query expires and the spinner sticks. Call `--answer`
promptly after detecting the tap, even if the actual work happens later.

### `telegram_status.py` — Bot and Listener Health

Checks three things in one run: the bot is reachable via `getMe`, the
listener process is alive (PID file + `kill -0`), and the inbox is being
written to. Exits `0` only when everything is healthy.

```bash
python3 telegram_status.py          # Human-readable
python3 telegram_status.py --json   # For scripts
```

Exit codes: `0` = all good, `1` = bot OK but listener down, `2` = bot
unreachable (token missing or network error).

### `telegram_memory.py` — Memory Context CLI

Thin wrapper over `~/.claudicle/adapters/shared/claudicle_memory.py`.
Gives Claude access to working memory, user models, and soul state for
Telegram channels. Used by the `/telegram-respond` pipeline.

```bash
python3 telegram_memory.py load-context <CHAT_ID>
python3 telegram_memory.py user-model tg:<USER_ID>
python3 telegram_memory.py soul-state
```

## Listener Management

The listener lives in the existing Claudicle adapter, not in this skill:

```bash
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --bg      # Start background
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --status  # Check
python3 ~/.claudicle/adapters/telegram/telegram_listen.py --stop    # Stop
```

### Optional: Running the Listener Persistently

On macOS the listener can be kept alive by launchd. The Claudicle
distribution ships a template plist and startup script; point them at the
listener in `~/.claudicle/adapters/telegram/telegram_listen.py`. On Linux
use systemd-user or your preferred process supervisor.

Two constraints matter regardless of platform:

- The Python interpreter must be 3.10+. On macOS with Homebrew that means
  `/opt/homebrew/bin/python3`, not `/usr/bin/python3` (which is 3.9 on
  recent releases and has an asyncio event loop bug that breaks
  `CallbackQueryHandler`, producing `Task attached to different loop`).
- `drop_pending_updates=False` in `app.run_polling()` so button taps during
  listener restarts aren't lost.

### Verifying the Listener Has Callback Support

The listener needs `CallbackQueryHandler` to capture inline keyboard taps.
Check with:

```bash
grep CallbackQueryHandler ~/.claudicle/adapters/telegram/telegram_listen.py
```

If missing, the Claudicle repo provides an idempotent patch script that
adds the handler, the registration, and the `drop_pending_updates` flip.

## Cognitive Pipeline

`/telegram-respond` processes unhandled Telegram messages through the
Claudicle cognitive pipeline: internal monologue, user model check/update,
soul state check/update, external response. See
`~/.claude/commands/telegram-respond.md`.

For fully autonomous response (no Claude Code session required), the
unified `~/.claudicle/daemon/adapters/inbox_watcher.py` handles `telegram:*`
channels alongside Slack and SMS. Deploying it is a separate task — its
launchd plist template needs instantiation with real paths.

## Mazkir Approval Gate Integration

The worldwarwatcher Mazkir pipeline uses this skill's sender for its
Telegram dispatches:

1. **Producer** (`mazkir-producer.sh`) writes a proposal bundle to
   `~/.claudicle/mazkir-staging/pending/run-xxx/` and calls
   `telegram_send.py` with `--buttons` showing [Approve] and [Reject].
2. **Listener** catches the tap and writes a `telegram_callback` entry to
   `inbox.jsonl`.
3. **Watcher** (`mazkir-callback-watcher.py`) tails the inbox, moves the
   bundle to `approved/` on approve, and spawns `mazkir-merger.sh`.

The skill's `telegram_callback.py` is useful for ad-hoc inspection of the
callback stream and for namespaces other than Mazkir. It does not
replace `mazkir-callback-watcher.py`, which owns the Mazkir state machine.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `TELEGRAM_BOT_TOKEN` | — | Bot token from @BotFather |
| `CLAUDICLE_TELEGRAM_ALLOWED_CHATS` | — | Comma-separated group chat IDs (empty = all groups) |
| `CLAUDICLE_TELEGRAM_RESPOND_TO_DMS` | `true` | Respond to private messages |
| `CLAUDICLE_TELEGRAM_RESPOND_TO_MENTIONS` | `true` | Respond to @mentions in groups |

**Env var naming drift to watch for**: the current listener reads
`CLAUDICLE_TELEGRAM_ALLOWED_CHATS` for access control, not
`CLAUDICLE_TELEGRAM_ALLOWED_USERS`. If an older startup script in your
Claudicle setup exports `ALLOWED_USERS`, it's a no-op — only `_CHATS` is
enforced. Low impact since the bot token is private, but worth knowing when
debugging DM allowlisting.

## Architecture

```
Claude Code session
  ├─ telegram_send.py      (REST POST, parse_mode, inline keyboards, stdin)
  ├─ telegram_check.py     (read telegram:* entries from inbox.jsonl)
  ├─ telegram_callback.py  (read telegram_callback entries, answerCallbackQuery)
  ├─ telegram_status.py    (getMe + listener PID + inbox count)
  ├─ telegram_memory.py    (3-tier memory CLI wrapper)
  └─ /telegram-respond     (cognitive pipeline command)
                 ↓
~/.claudicle/adapters/telegram/
  ├─ telegram_listen.py    (python-telegram-bot polling + CallbackQueryHandler)
  ├─ telegram_post.py      (legacy asyncio sender — superseded by telegram_send.py)
  └─ _telegram_utils.py    (split_message, channel helpers)
                 ↓
~/.claudicle/daemon/
  ├─ inbox.jsonl                        (shared SMS/Slack/Telegram inbox)
  └─ adapters/inbox_watcher.py          (autonomous responder, channel-agnostic)
```

## Channel and ID Conventions

- **Channel format**: `telegram:{chat_id}` (e.g., `telegram:123456789` for a DM, `telegram:-100123456789` for a supergroup)
- **User model key**: `tg:{user_id}` (e.g., `tg:123456789`)
- **Callback data conventions**: keep under 64 bytes (Telegram hard limit).
  Two common patterns:
  - `{action}:{run_id}` — e.g., `approve:run-2026-04-10T14Z-a4f3`
  - `{namespace}_{action}` — e.g., `mazkir_approve`, `deploy_rollback`
- **Message limit**: 4096 chars per message; `split_message` handles longer
  text by breaking on newlines.

## Security

- Never commit `TELEGRAM_BOT_TOKEN` to git. It lives in
  `~/.config/env/secrets.env` (chmod 600).
- DM access is nominally allowlist-based via
  `CLAUDICLE_TELEGRAM_ALLOWED_CHATS`, but see the env var drift note above.
- User-provided text is sanitized for XML tags before the cognitive pipeline
  processes it. `WebFetch` is removed from allowed tools in the daemon-mode
  subprocess to reduce attack surface.
- Callback queries are scoped to the bot's messages, but `callback_data` is
  untrusted input — always validate it against an expected namespace before
  acting on it.

## Troubleshooting

**Send works but buttons don't appear.** Check that `--buttons` JSON parses
and that each button contains exactly one `|` separator.

**Button tap doesn't land in inbox.jsonl.** Check the listener is running
(`telegram_status.py`) and that it has `CallbackQueryHandler` registered
(`grep CallbackQueryHandler ~/.claudicle/adapters/telegram/telegram_listen.py`).
If missing, run the worldwarwatcher `patch-telegram-listener.py`.

**`Task attached to different loop` error on tap.** Listener is running on
Python 3.9. Switch `start-telegram-listener.sh` to `/opt/homebrew/bin/python3`.

**`Query is too old` error when answering callbacks.** Answer within ~30
seconds of the tap. If delayed work is needed, answer immediately with a
holding message ("Received — processing.") and update later via
`editMessageText`.

**Parse mode errors (`can't parse entities`).** The send script auto-retries
as plain text and logs a warning. If it's important that formatting stick,
escape the special characters for the chosen parse mode (MarkdownV2 is the
strictest).
