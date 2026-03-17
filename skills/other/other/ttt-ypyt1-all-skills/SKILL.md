---
name: ttt
description: Manage TinyTalkingTodos lists and items via the ttt CLI
metadata: {"openclaw": {"emoji": "✅", "requires": {"bins": ["ttt"]}, "homepage": "https://tinytalkingtodos.com"}}
---

# TinyTalkingTodos CLI

Use `ttt` to manage todo lists and items from the command line. The CLI syncs with TinyTalkingTodos in real-time.

## Installation

```bash
npm install -g @ojschwa/ttt-cli
```

Or install locally for development:

```bash
cd /path/to/talking-todo/ttt-cli
npm install
npm run build
npm link
```

Verify with `ttt --help`.

## Authentication

Before using the CLI, the user must be authenticated:

```bash
# Check auth status
ttt auth status

# Login via browser (opens OAuth flow)
ttt auth login

# Logout
ttt auth logout

# Export credentials as env vars (for scripts)
ttt auth export
```

## List Management

### List all lists

```bash
ttt list ls
```

Output (compact, token-efficient):
```
Today [2/5]
Groceries [0/3]
Work Tasks [1/4]
```

For structured data:
```bash
ttt list ls --json
```

### Get list details

```bash
ttt list get "Groceries"
# or by ID
ttt list get list-abc123
```

### Create a new list

```bash
ttt list create "Weekend Plans"
ttt list create "Shopping" --icon "🛒" --color "#FF6B6B"
```

Options:
- `--color <hex>` - Background color
- `--icon <emoji>` - List icon
- `--type <type>` - List type

### Update a list

```bash
ttt list update "Groceries" --name "Shopping List"
ttt list update "Shopping List" --icon "🛒" --color "#00FF00"
```

Options:
- `--name <name>` - New list name
- `--color <hex>` - Background color
- `--icon <emoji>` - List icon
- `--type <type>` - List type

### Delete a list

```bash
ttt list delete "Old List"
ttt list rm "Old List"  # alias

# Force delete even if list has todos
ttt list delete "Old List" --force
```

## Todo Operations

### List todos in a list

```bash
ttt todo ls --list "Groceries"
```

Output (compact):
```
Groceries [1/4]
✓ Milk id:todo-abc123
○ Bread id:todo-def456
○ Eggs id:todo-ghi789
○ Butter id:todo-jkl012
```

For JSON output:
```bash
ttt todo ls --list "Groceries" --json
```

### Add a todo

Basic:
```bash
ttt todo add "Buy avocados" --list "Groceries"
```

With options:
```bash
ttt todo add "Doctor appointment" --list "Health" \
  --date 2026-02-15 \
  --time 14:30 \
  --notes "Bring insurance card"

ttt todo add "Try new pasta place" --list "Restaurants" \
  --url "https://example.com/restaurant" \
  --street-address "123 Main St" \
  --rating 4

ttt todo add "Tomatoes" --list "Groceries" \
  --amount 2.50 \
  --category "Produce" \
  --emoji "🍅"
```

All `--list` options:
| Option | Description | Example |
|--------|-------------|---------|
| `--notes <text>` | Additional notes | `--notes "organic preferred"` |
| `--date <YYYY-MM-DD>` | Due date | `--date 2026-02-15` |
| `--time <HH:MM>` | Due time | `--time 14:30` |
| `--url <url>` | Associated URL | `--url "https://..."` |
| `--emoji <emoji>` | Item emoji | `--emoji "🎉"` |
| `--email <email>` | Associated email | `--email "contact@..."` |
| `--street-address <addr>` | Location | `--street-address "123 Main"` |
| `--number <n>` | Numeric value | `--number 5` |
| `--amount <n>` | Amount/price | `--amount 12.99` |
| `--rating <1-5>` | Star rating | `--rating 4` |
| `--type <A-E>` | Item type | `--type A` |
| `--category <name>` | Category | `--category "Urgent"` |

### Mark a todo as done

```bash
ttt todo done todo-abc123
```

The todo ID is shown in the compact output format after `id:`.

### Mark a todo as not done

```bash
ttt todo undone todo-abc123
```

### Update a todo

```bash
ttt todo update todo-abc123 --text "New text"
ttt todo update todo-abc123 --category "Urgent" --date 2026-02-15
ttt todo update todo-abc123 --done   # mark as done
ttt todo update todo-abc123 --not-done  # mark as not done
```

Options:
- `--text <text>` - New todo text
- `--notes`, `--date`, `--time`, `--url`, `--emoji`, `--email`, `--street-address`
- `--number`, `--amount`, `--rating`, `--type`, `--category`
- `--done` / `--not-done` - Toggle completion status

### Delete a todo

```bash
ttt todo delete todo-abc123
# or use alias
ttt todo rm todo-abc123
```

### Batch add todos

Add multiple todos at once using JSON:

```bash
ttt todo batch-add --list "Groceries" --items '[
  {"text": "Milk"},
  {"text": "Eggs", "fields": {"category": "Dairy"}},
  {"text": "Bread", "fields": {"amount": 3.50}}
]'
```

Each item requires `text` and optionally `fields` with any todo field.

### Batch update todos

Update multiple todos at once:

```bash
ttt todo batch-update --items '[
  {"id": "todo-abc123", "fields": {"done": true}},
  {"id": "todo-def456", "fields": {"text": "Updated text", "category": "Urgent"}}
]'
```

Each item requires `id` and `fields` with the updates to apply.

## Undo Operations

All mutating operations are recorded and can be undone:

```bash
# Undo the last operation
ttt undo

# Undo the last 3 operations
ttt undo 3

# View undo history
ttt history
ttt history --limit 20
ttt history --json
```

Undo supports: todo add/delete/update, batch-add/update, mark done/undone, list create/update/delete.

## Daemon (Performance)

The daemon keeps a persistent WebSocket connection for faster commands:

```bash
# Start daemon (auto-starts on first command if not running)
ttt daemon start

# Check status
ttt daemon status

# Stop daemon
ttt daemon stop
```

The daemon auto-shuts down after 30 minutes of inactivity.

## Best Practices

1. **Use compact output** (default) when displaying lists to users - it's token-efficient
2. **Use `--json`** when you need to parse data or extract specific fields
3. **Reference lists by name** for readability, or by ID for precision
4. **Check auth status** before operations if you're unsure of login state
5. **Extract todo IDs** from compact output (format: `id:<todo-id>`) for updates
6. **Use batch operations** when adding or updating multiple items - more efficient than individual calls
7. **Use undo** if you make a mistake - `ttt undo` reverts the last operation

## Example Workflows

### Add items to grocery list
```bash
ttt todo add "Milk" --list "Groceries" --category "Dairy"
ttt todo add "Bread" --list "Groceries" --category "Bakery"
ttt todo add "Apples" --list "Groceries" --amount 3.50 --category "Produce"
```

### Check and complete tasks
```bash
# View todos
ttt todo ls --list "Today"

# Mark one done (using ID from output)
ttt todo done todo-xyz789
```

### Create a new list with todos
```bash
ttt list create "Weekend Trip" --icon "🏕️"
ttt todo add "Pack tent" --list "Weekend Trip"
ttt todo add "Check weather" --list "Weekend Trip" --url "https://weather.com"
ttt todo add "Gas up car" --list "Weekend Trip"
```

### Batch add items efficiently
```bash
ttt todo batch-add --list "Party Supplies" --items '[
  {"text": "Balloons", "fields": {"category": "Decorations"}},
  {"text": "Cake", "fields": {"category": "Food", "amount": 45.00}},
  {"text": "Plates", "fields": {"category": "Supplies", "number": 20}},
  {"text": "Candles", "fields": {"category": "Decorations"}}
]'
```

### Mark multiple items done
```bash
ttt todo batch-update --items '[
  {"id": "todo-abc", "fields": {"done": true}},
  {"id": "todo-def", "fields": {"done": true}},
  {"id": "todo-ghi", "fields": {"done": true}}
]'
```

### Undo a mistake
```bash
# Accidentally deleted something? Undo it
ttt undo

# Made several mistakes? Undo multiple
ttt undo 3
```
