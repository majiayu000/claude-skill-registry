---
name: denylist-stuck-messages
description: Add message IDs to the relayer denylist. Use after investigating stuck messages with /investigate-stuck-messages, or when you have specific message IDs to denylist.
---

# Denylist Stuck Messages

Add message IDs to the relayer denylist configuration, create a PR, and deploy.

## When to Use

1. **After investigation:**
   - User ran `/investigate-stuck-messages` and wants to denylist the found messages
   - User says "denylist these" or "add these to blacklist"

2. **Direct denylist request:**
   - User provides specific message IDs to denylist
   - User pastes message IDs from explorer or logs

## Input Parameters

```
/denylist-stuck-messages <message_ids> [app_context=NAME] [reason=REASON]
```

| Parameter     | Required | Default                  | Description                                    |
| ------------- | -------- | ------------------------ | ---------------------------------------------- |
| `message_ids` | Yes      | -                        | Space or newline separated message IDs (0x...) |
| `app_context` | No       | Inferred or "Unknown"    | App context name for the comment               |
| `reason`      | No       | "stuck in prepare queue" | Reason for denylisting (for comment)           |
| `environment` | No       | `mainnet3`               | Deployment environment                         |

**Examples:**

```
/denylist-stuck-messages 0xabc123 0xdef456 app_context=USDC/mainnet-cctp-v2-standard
```

```
/denylist-stuck-messages
0xabc123
0xdef456
0x789ghi
```

## Workflow

### Step 1: Parse Message IDs

Extract all message IDs from the input. Valid formats:

- Space-separated: `0xabc 0xdef 0x123`
- Newline-separated
- Comma-separated: `0xabc, 0xdef, 0x123`

Validate each ID:

- Must start with `0x`
- Must be 66 characters (0x + 64 hex chars)

### Step 2: Confirm with User

Use `AskUserQuestion` to confirm:

```
Ready to denylist X messages for [APP_CONTEXT]:

| Message ID |
|------------|
| 0xabc123... |
| 0xdef456... |

Proceed?
```

Options:

1. "Yes, denylist all" (Recommended)
2. "Let me modify the list"
3. "Cancel"

### Step 3: Get User's GitHub Handle

Ask for GitHub handle if not known:

```
What is your GitHub handle for the branch name?
```

### Step 4: Update Blacklist Configuration

Edit `typescript/infra/config/environments/mainnet3/customBlacklist.ts`:

1. Read the current file
2. Add new message IDs to the `blacklistedMessageIds` array
3. Include a comment with:
   - App context name
   - Date (YYYY-MM-DD format)
   - Reason

Example addition:

```typescript
  // [APP_CONTEXT] [REASON] [YYYY-MM-DD]
  '0xabc123...',
  '0xdef456...',
```

Add entries near the end of the array, before the closing bracket.

### Step 5: Create Branch and Pull Request

```bash
# Checkout main and pull latest
git checkout main && git pull origin main

# Create branch
git checkout -b <github_handle>/denylist-<app_context>

# Stage changes
git add typescript/infra/config/environments/mainnet3/customBlacklist.ts

# Commit
git commit -m "chore: denylist <APP_CONTEXT> stuck messages

Added X message IDs to denylist for <APP_CONTEXT> route.
Reason: <REASON>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Push and create PR
git push -u origin HEAD
gh pr create --title "chore: denylist <APP_CONTEXT> stuck messages" --body "$(cat <<'EOF'
## Summary
- Added X message IDs to the relayer denylist
- App context: `<APP_CONTEXT>`
- Reason: <REASON>

## Message IDs
<list of message IDs>

## Test plan
- [ ] Review message IDs are correct
- [ ] Deploy relayer with updated denylist

Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

### Step 6: Output Slack Message

Before asking about deployment, output the Slack message:

```
**Slack Message (copy/paste to #relayer-alerts):**

:no_entry_sign: *Denylist PR created*

App context: `<APP_CONTEXT>`
Messages denylisted: X
Reason: <REASON>

PR: <PR_URL>
```

### Step 7: Ask About Deployment

Use `AskUserQuestion`:

```
PR created. Deploy the relayer now with the updated denylist?
```

Options:

1. "Yes, deploy now" (Recommended)
2. "No, I'll deploy later"

If user confirms, run:

```bash
pnpm --dir typescript/infra exec tsx ./scripts/agents/deploy-agents.ts -e mainnet3 --context hyperlane --role relayer
```

If user skips, output the command for later use.

### Step 8: Update Slack Message After Deploy

If deployed, update the Slack message:

```
:no_entry_sign: *Denylist deployed*

App context: `<APP_CONTEXT>`
Messages denylisted: X
Reason: <REASON>

PR: <PR_URL>
```

## Grouping by Destination

If message IDs are for multiple destinations (from investigation output), group them in the blacklist file:

```typescript
  // [APP_CONTEXT] stuck messages [YYYY-MM-DD]
  // dest: arbitrum
  '0xabc123...',
  '0xdef456...',
  // dest: optimism
  '0x789ghi...',
  '0xjkl012...',
```

## Error Handling

- **Invalid message ID format**: Show which IDs are invalid, ask user to fix
- **Git conflicts**: Pull latest main and retry
- **PR creation fails**: Check gh auth status
- **Deployment fails**: Show error, suggest manual deployment

## Prerequisites

- `gh` CLI authenticated
- Git configured with push access to the repo
- For deployment: `kubectl` configured with mainnet cluster access
