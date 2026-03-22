---
name: manage
description: This skill should be used when the user asks to "manage email", "bulk email", "move emails", "flag emails", "archive emails", "unflag emails", or wants to perform batch operations. Handles flag, unflag, move, and archive for multiple emails at once.
triggers:
  - manage email
  - bulk email
  - move emails
  - flag emails
  - archive emails
  - unflag emails
---

# /email:manage - Bulk Email Management

Perform batch operations on multiple emails: flag, unflag, move, archive.

## Usage

```
/email:manage flag 1,2,5          # Flag specific email IDs
/email:manage unflag 3,7          # Remove flags from emails
/email:manage move 1,2,3 Archive  # Move emails to Archive
/email:manage archive 4,5,6       # Shortcut for move to Archive
/email:manage move all-unread Spam  # Move all unread to Spam
```

## When Invoked

1. Parse the action and target list:
   - **Actions**: `flag`, `unflag`, `move`, `archive`
   - **Targets**: comma-separated IDs (e.g., `1,2,5`) or `all-unread`
   - **Destination**: required for `move` and `archive` (defaults to `Archive`)
2. If targeting more than 5 emails, show confirmation gate:
   ```
   ⚠️ This will move 12 emails to Archive. Continue? (yes/no)
   ```
3. Execute operations in sequence, showing progress:
   ```
   [1/7] Flagging email #1...
   [2/7] Flagging email #2...
   ...
   ```
4. Display summary when complete

## Safety Rules

- Require explicit confirmation for operations on more than 5 emails
- Always show what will happen before executing bulk moves
- Never delete emails — only move to Trash (user can recover)
- If `all-unread` is used, first call `list_emails` to count and show the scope

## MCP Tools Used

- `flag_email` — for flag/unflag operations (action: `add` or `remove`, flags: `["Flagged"]`)
- `move_email` — for move/archive operations
- `list_emails` — to resolve `all-unread` targets
- `search_emails` — to resolve filter-based targets

## Output Format

```
✅ Bulk operation complete

Action: Move to Archive
Emails processed: 7/7
  [1] alice@co — Meeting tomorrow → Archive ✓
  [2] bob@co — PR review needed → Archive ✓
  [3] team@co — Weekly standup → Archive ✓
  [4] hr@co — Benefits update → Archive ✓
  [5] news@co — Tech digest → Archive ✓
  [6] ci@co — Build passed → Archive ✓
  [7] github@co — Issue closed → Archive ✓

→ "Undo" to move these back to INBOX
→ "/email:inbox" to check remaining emails
```
