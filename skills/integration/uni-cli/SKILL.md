---
name: uni-cli
description: |
  uni CLI overview and meta commands. Use for general uni questions, multi-command execution (uni run), saved flows, natural language (uni ask), plugins, config, aliases, history.
  For specific services, use their dedicated skills (uni-wa, uni-telegram, uni-google, etc.)
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# uni CLI

Universal CLI wrapping 25+ services into one interface.

## Pattern

```bash
uni <service> <command> [args] [--options]
uni list                    # All services
uni <service> --help        # Service commands
uni doctor                  # Health check
```

## Multi-Command (run)

```bash
uni run "gcal list" "gtasks list"       # Sequential
uni run -p "cmd1" "cmd2" "cmd3"         # Parallel
uni run --dry-run "cmd1" "cmd2"         # Preview
uni run "wa send me hello{1..5}"        # Brace expansion
uni run --file batch.txt                # From file
uni run --retry 3 "flaky-cmd"           # Retry
uni run "cmd1 && cmd2"                  # On success
uni run "cmd1 || cmd2"                  # On failure
uni run "cmd1 | cmd2"                   # Pipe output
```

## Natural Language (ask)

```bash
uni ask "show my calendar tomorrow"
uni ask "search for React tutorials"
uni ask -i                              # Interactive
uni ask "query" --dry-run               # Preview
uni ask providers                       # List LLM providers
uni ask models --provider anthropic     # List models
```

## Saved Flows

```bash
uni flow add standup "gcal list" "gtasks list"
uni flow list
uni flow run standup
uni standup                             # Shorthand
uni flow remove standup
```

## Plugins

```bash
uni plugins list                        # Installed
uni plugins available                   # Official
uni plugins search google               # Search npm
uni plugins install gkeep               # Install
uni plugins uninstall gkeep             # Remove
uni plugins update                      # Update all
```

## Config

```bash
uni config show                         # All config
uni config get global.color             # Get value
uni config set global.color false       # Set value
uni config edit                         # Open editor
uni config path                         # Config path
```

## Aliases

```bash
uni alias add inbox "gmail list --unread"
uni alias list
uni alias remove inbox
uni inbox                               # Use alias
```

## History

```bash
uni history                             # Recent
uni history --limit 50
uni history --search "gcal"
uni history run 42                      # Re-run #42
uni history clear
```

## Output

- Default: Human-readable
- `--json`: Machine-readable JSON
