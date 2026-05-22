---
name: uni-trello
description: |
  Trello boards, lists, and cards via uni CLI. Use when user wants to manage Trello tasks, create boards, move cards between lists.
  Requires TRELLO_API_KEY and TRELLO_TOKEN.
allowed-tools: Bash(uni:*), Bash(~/.local/bin/uni:*)
---

# Trello (uni)

Manage Trello boards, lists, and cards from the terminal.

## Authentication

```bash
# Set via environment variables
export TRELLO_API_KEY="your_api_key"
export TRELLO_TOKEN="your_token"

# Get credentials from: https://trello.com/app-key
```

## Boards

```bash
uni trello boards                    # List all boards
uni trello boards create "Project"   # Create new board
uni trello boards close <board_id>   # Archive board
```

## Lists

```bash
uni trello lists <board_id>                    # List all lists in board
uni trello lists create <board_id> "To Do"     # Create list
uni trello lists archive <list_id>             # Archive list
```

## Cards

```bash
uni trello cards <board_id>                           # List all cards
uni trello cards create <list_id> "Task name"         # Create card
uni trello cards create <list_id> "Task" -d "Details" # With description
uni trello cards move <card_id> <list_id>             # Move to another list
uni trello cards archive <card_id>                    # Archive card
uni trello cards delete <card_id>                     # Delete permanently
```

## Members

```bash
uni trello members <board_id>        # List board members
```

## Notes

- Board/list/card IDs shown in output as `[xxx]`
- Can use board name instead of ID for some commands
- Cards can have due dates: `--due "2024-12-31"`
