---
name: trello-manager
description: Manage Trello boards, lists, and cards. Use this skill when the user wants to view, create, or update their Trello tasks, boards, or project status.
---

# Trello Manager

Interact with Trello via `python3 scripts/trello_api.py <command> [args]`.

## Commands

| Command | Args | Description |
|---------|------|-------------|
| `list_boards` | - | Show all boards |
| `create_board` | `<name> [desc]` | Create board |
| `list_lists` | `<board_id>` | Show lists in board |
| `create_list` | `<board_id> <name>` | Create list |
| `update_list` | `<list_id> <name>` | Rename list |
| `list_cards` | `<list_id>` | Show cards in list |
| `get_card` | `<card_id>` | Get card details |
| `create_card` | `<list_id> <name> [desc]` | Create card |
| `move_card` | `<card_id> <list_id>` | Move card to list |
| `delete_card` | `<card_id>` | Delete card |
| `update_card_desc` | `<card_id> <desc>` | Update description |
| `list_labels` | `<board_id>` | Show board labels |
| `create_label` | `<board_id> <name> <color>` | Create label |
| `add_label` | `<card_id> <label_id>` | Add label to card |
| `remove_label` | `<card_id> <label_id>` | Remove label |
| `create_checklist` | `<card_id> [name]` | Add checklist |
| `add_checkitem` | `<checklist_id> <name>` | Add checklist item |
| `list_checklists` | `<card_id>` | Show checklists with items |
| `complete_checkitem` | `<card_id> <checklist_id> <item_id>` | Mark item complete |
| `uncomplete_checkitem` | `<card_id> <checklist_id> <item_id>` | Mark item incomplete |

## Workflow

1. Start with `list_boards` to get board IDs
2. Use `list_lists <board_id>` to get list IDs
3. Use `list_cards <list_id>` or `create_card` as needed

## Adding Cards with Checklists

When creating cards that need checklists (e.g., recipes with shopping lists):

1. Create the card: `create_card <list_id> "Card Name" "Description"`
2. Create a checklist: `create_checklist <card_id> "Checklist Name"`
3. Add items: `add_checkitem <checklist_id> "Item name"`

Example (recipe card):
```bash
# Create recipe card
python3 scripts/trello_api.py create_card <list_id> "Recipe Name" "Ingredients and steps..."
# Add shopping list checklist
python3 scripts/trello_api.py create_checklist <card_id> "Shopping List"
# Add ingredients as checklist items
python3 scripts/trello_api.py add_checkitem <checklist_id> "Ingredient 1"
python3 scripts/trello_api.py add_checkitem <checklist_id> "Ingredient 2"
```

## Output Format

All output is optimized for minimal context:
- Lists show: `Name [id]` per line
- Cards show: `Name [id] - description_preview`
- Labels show: `Name [id] (color)`
- Checklists show items with `[x]` or `[ ]` status
- Mutations return: `Action message: new_id`

## Notes

- Requires `TRELLO_API_KEY` and `TRELLO_API_TOKEN` in environment
- IDs are always shown in `[brackets]` for easy extraction
