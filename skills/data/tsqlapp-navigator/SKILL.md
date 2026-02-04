---
name: tsqlapp-navigator
description: Navigate and understand TSQL.APP applications through metadata queries. Use when users share TSQL.APP URLs, ask about cards/screens, want to understand available actions/buttons/filters, explore parent-child relationships, or need to locate features in a TSQL.APP application. This skill parses URLs into application state and queries the meta database to explain what the user is seeing and what they can do.
---

# TSQL.APP Navigator

Navigate TSQL.APP applications by querying the metadata database. Parse URLs, discover actions, and explain application state.

## Two-Database Architecture

Every TSQL.APP application = 2 databases:

| Database | Purpose | Contains |
|----------|---------|----------|
| `{app}` | Business data | Tables, views, stored procedures |
| `{app}_proj` | Application definition | Cards, fields, actions, children |

MCP connects to `{app}_proj`. Get business DB name: `SELECT dbo.main_db()`

## URL Pattern

```
https://{domain}/{card}[/{parent_id}/{child_card}]?[ord={field_id}[d]][,{field_id}][&red={filter_name}][&id={record_id}]
```

| Parameter | Example | Meaning |
|-----------|---------|---------|
| `{card}` | `incoming_invoice` | Card name (path) |
| `{parent_id}` | `142338` | Parent record ID (child context) |
| `{child_card}` | `invrow_1` | Child card name |
| `ord` | `18377d` | Sort field ID, `d`=descending |
| `ord` | `32408,30233` | Multi-field sort |
| `red` | `Draft+%2F+Empty` | Active filter (URL encoded) |
| `id` | `142338` | Selected record ID |

## Core Meta Tables

### api_card
```sql
SELECT id, name, tablename, basetable, reducer FROM api_card WHERE name = @card_name
```
- `tablename` = READ (view for display)
- `basetable` = WRITE (table for CRUD)

### api_card_fields
```sql
SELECT id, name, list_order FROM api_card_fields WHERE card_id = @card_id
```
- `id` = field ID used in `ord` URL parameter

### api_card_actions
```sql
SELECT id, name, display_name, action, keycode, group_id, type, disabled
FROM api_card_actions WHERE card_id = @card_id
```
- `action` = `'stored_procedure'` (button) or `'reducer'` (filter)
- `keycode` = keyboard shortcut
- `group_id` = parent sub-menu (NULL = top level)
- `type` = `'list'`, `'form'`, `'list_form'`, `'hidden'`

### api_card_children
```sql
SELECT child, ref, keycode, unbound, reducer, is_hidden, group_id
FROM api_card_children WHERE parent = @card_id
```
- `keycode` = navigation shortcut (e.g., `'Enter'`)
- `ref` = FK column linking parent to child
- `unbound` = `0` (filter by ref) or `1` (custom reducer)

## Action Hierarchy

```
Card
├── Top-level (group_id IS NULL)
│   ├── Buttons (action='stored_procedure')
│   ├── Filters (action='reducer')
│   └── Sub-menus (referenced as group_id)
└── Sub-menu contents (group_id = sub-menu.id)
```

Keyboard sequence: `{submenu_keycode}` → `{action_keycode}`

## Standard Queries

### Parse URL
```sql
-- Card info
SELECT id, name, tablename, basetable FROM api_card WHERE name = @card_name

-- Sort field (from ord parameter)
SELECT name FROM api_card_fields WHERE id = @field_id

-- Filter (from red parameter, URL decoded)
SELECT id, sql FROM api_card_actions 
WHERE card_id = @card_id AND name = @filter_name AND action = 'reducer'
```

### List All Actions with Shortcuts
```sql
SELECT 
    CASE WHEN g.keycode IS NOT NULL 
         THEN CONCAT(g.keycode, ' → ', ISNULL(a.keycode, '-'))
         ELSE ISNULL(a.keycode, '-')
    END as shortcut,
    a.name,
    CASE a.action WHEN 'reducer' THEN 'filter' ELSE 'button' END as type,
    a.disabled
FROM api_card_actions a
LEFT JOIN api_card_actions g ON a.group_id = g.id
WHERE a.card_id = @card_id
ORDER BY COALESCE(a.group_id, 0), a.action_order
```

### List Children with Navigation
```sql
SELECT 
    acc.keycode,
    c.name as child_card,
    acc.ref as link_column,
    CASE acc.unbound WHEN 1 THEN 'custom' ELSE 'bound' END as filter_type
FROM api_card_children acc
JOIN api_card c ON acc.child = c.id
WHERE acc.parent = @card_id AND ISNULL(acc.is_hidden, 0) = 0
ORDER BY acc.keycode
```

### Find What Enter Does
```sql
SELECT c.name as child_card, acc.ref
FROM api_card_children acc
JOIN api_card c ON acc.child = c.id
WHERE acc.parent = @card_id AND acc.keycode = 'Enter'
```

### Predict Next URL (Child Navigation)
```sql
-- Current: /{card}?id={record_id}
-- After Enter: /{card}/{record_id}/{child_card}
SELECT CONCAT('/', @card, '/', @record_id, '/', c.name) as next_url
FROM api_card_children acc
JOIN api_card c ON acc.child = c.id
WHERE acc.parent = @card_id AND acc.keycode = 'Enter'
```

## Response Pattern

When user shares URL:

1. **Parse** - Extract card, parent/child, sort, filter, selection
2. **Query** - Look up card, fields, actions, children in metadata
3. **Explain** - Current view, active filter, selected record
4. **List** - Available actions with keyboard shortcuts
5. **Predict** - What happens on common keys (Enter, etc.)

## Critical Rules

1. **Do NOT guess** - Query metadata for exact values
2. **URL is state** - Every URL is a complete deep link
3. **Metadata is truth** - If it's in the meta tables, it's accurate
4. **Actions have hierarchy** - Check group_id for sub-menus
5. **Children have shortcuts** - Check api_card_children.keycode

## Reference

For detailed architecture and examples, see `references/architecture.md`.
