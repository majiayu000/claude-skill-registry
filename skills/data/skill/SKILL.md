---
name: uni-cli
description: |
  Unified CLI for AI agents. Pattern: uni <service> <command>.
  Services: WhatsApp, Telegram, Google Suite (Calendar, Gmail, Drive, Sheets, Docs, Slides, Forms, Meet, Tasks, Contacts),
  Slack, Notion, Linear, Todoist, web search (Exa), research (arXiv, Reddit, HN, Wikipedia), utilities (weather, stocks, currency, QR, URL shortener).
  Run `uni list` for all services, `uni <service> --help` for commands.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# uni CLI

Universal CLI wrapping 25+ services. One command pattern for everything.

## Pattern

```bash
uni <service> <command> [args] [--options]
```

## Discovery

```bash
uni list                    # All services
uni <service> --help        # Commands for a service
uni doctor                  # Health check
```

## Services

| Category | Services |
|----------|----------|
| Messaging | `wa`, `telegram` |
| Google | `gcal`, `gmail`, `gdrive`, `gsheets`, `gdocs`, `gslides`, `gforms`, `gmeet`, `gtasks`, `gcontacts` |
| Productivity | `slack`, `notion`, `linear`, `todoist` |
| Research | `exa`, `arxiv`, `reddit`, `hn`, `wiki` |
| Utilities | `weather`, `stocks`, `currency`, `qrcode`, `shorturl` |
| Meta | `ask`, `run`, `flow`, `plugins`, `config`, `alias`, `history` |

## Quick Examples

```bash
# Messaging
uni wa send me "hello"                  # WhatsApp to self
uni telegram send me "test"             # Telegram to saved messages

# Google
uni gcal list                           # Today's calendar
uni gmail list --unread                 # Unread emails
uni gtasks add "Buy groceries"          # Add task

# Productivity
uni slack send "#general" "update"      # Slack message
uni linear issues                       # Linear issues
uni todoist tasks                       # Todoist tasks

# Research
uni exa search "AI agents 2025"         # Web search
uni arxiv search "transformers"         # Academic papers
uni hn top                              # Hacker News

# Utilities
uni weather "NYC"                       # Weather
uni stocks AAPL                         # Stock price
uni currency 100 usd to eur             # Convert currency
```

## Multi-Command

```bash
uni run "cmd1" "cmd2"                   # Sequential
uni run -p "cmd1" "cmd2"                # Parallel
uni run "cmd1 && cmd2"                  # Conditional (on success)
uni run "cmd1 | cmd2"                   # Pipe output
```

## Natural Language

```bash
uni ask "show my calendar tomorrow"     # Translates to uni command
uni ask -i                              # Interactive mode
```

## Output

- Default: Human-readable
- `--json`: Machine-readable JSON

## Service Details

For detailed commands, see:
- [Messaging (WA, Telegram)](services/messaging.md)
- [Google Suite](services/google.md)
- [Research (Exa, arXiv, Reddit, HN, Wiki)](services/research.md)
- [Productivity (Slack, Notion, Linear, Todoist)](services/productivity.md)
- [Utilities (Weather, Stocks, Currency, QR, URL)](services/utilities.md)

## See Also

- [REFERENCE.md](REFERENCE.md) - Auto-generated full command reference
- [PATTERNS.md](PATTERNS.md) - Common workflow patterns
