---
name: trello-cli
description: 'Trello board, list and card management via CLI. Activate when user mentions
  "Trello" - examples: "Show my Trello tasks", "Add card to Trello", "Move on Trello",
  "Trello board", "List Trello", "Trello'
---

---
name: trello-cli
description: Trello board, list and card management via CLI. Activate when user mentions "Trello" - examples: "Show my Trello tasks", "Add card to Trello", "Move on Trello", "Trello board", "List Trello", "Trello cards".
---

# Trello CLI

Manage Trello boards, lists, and cards using the `trello-cli` command.

## Important Rules

1. **Only activate when "Trello" is mentioned** - Do not interfere with Notion, Jira, or other tools
2. **Check JSON output after each command** - `ok: true` means success, `ok: false` means error
3. **Follow the workflow**: First find board ID, then list ID, then perform card operations

## Quick Reference

### Board & List

```bash
trello-cli --get-boards                              # List all boards
trello-cli --get-lists <board-id>                    # Get lists in board
```

### Cards

```bash
trello-cli --get-all-cards <board-id>                # All cards in board
trello-cli --create-card <list-id> "<name>"          # Create card
trello-cli --create-card <list-id> "<name>" --desc "<desc>" --due "2025-01-15"
trello-cli --update-card <card-id> --name "<name>" --desc "<desc>"
trello-cli --move-card <card-id> <list-id>           # Move card
trello-cli --delete-card <card-id>                   # Delete card
trello-cli --get-comments <card-id>                  # Get comments
trello-cli --add-comment <card-id> "<text>"          # Add comment
```

### Attachments

```bash
trello-cli --list-attachments <card-id>              # List attachments
trello-cli --upload-attachment <card-id> <file-path> [--name "<name>"]
trello-cli --attach-url <card-id> <url> [--name "<name>"]
trello-cli --delete-attachment <card-id> <attach-id>
```

**Note:** Downloading attachments is not supported - Trello's download API requires browser authentication. Use `--attach-url` to link attachments between cards.

## Typical Workflows

### List All Tasks
```bash
trello-cli --get-boards           # → Get board ID
trello-cli --get-all-cards <id>   # → See all cards
```

### Add New Task
```bash
trello-cli --get-boards           # → Get board ID
trello-cli --get-lists <id>       # → Find "To Do" or "Backlog" list ID
trello-cli --create-card <list-id> "<task-name>"
```

### Move to Done
```bash
trello-cli --get-lists <board-id> # → Find "Done" list ID
trello-cli --move-card <card-id> <done-list-id>
```

## When Uncertain

If you encounter an error or don't know how to proceed:

```bash
trello-cli --help
```

For detailed command reference, see [REFERENCE.md](REFERENCE.md).

## Example Scenarios

**User:** "Show my Trello tasks"
→ Run `--get-boards`, then `--get-all-cards <board-id>`

**User:** "Add a new task to Trello"
→ Run `--get-boards`, `--get-lists`, then `--create-card`

**User:** "Move the card to Done on Trello"
→ Run `--get-lists` to find Done ID, then `--move-card`

**User:** "Update the Trello card description"
→ Run `--update-card <card-id> --desc "<new-desc>"`

**User:** "Upload this file to the Trello card"
→ Run `--upload-attachment <card-id> "<file-path>"`

**User:** "Link an attachment to another Trello card"
→ Run `--list-attachments <source-card-id>` to get the URL, then `--attach-url <target-card-id> <url>`
