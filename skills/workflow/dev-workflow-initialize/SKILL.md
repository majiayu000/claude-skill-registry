---
name: dev-workflow-initialize
description: Start working on a Jira ticket or GitHub issue by fetching details and creating a git branch in a new worktree. Use when the user wants to start a ticket, begin work on a Jira issue, a GitHub issue, or create a branch. For unticketed work, use placeholder RETIRE-1908.
---

# Start Ticket or Issue

Start working on a Jira ticket or GitHub issue by fetching its details and creating a feature branch in a new worktree based on origin/main. Requirements can come from **Jira** (e.g. RETIRE-123), **GitHub** (e.g. owner/repo#1 or issue URL), or **unticketed** (placeholder RETIRE-1908). For source rules and branch naming see [sources.md](sources.md).

## Placeholder Ticket (Unticketed Work)

When the user is working on an **unticketed task** (no Jira ticket yet), use this placeholder:

- **RETIRE-1908** — Use when starting a branch or worktree for work that doesn’t have a ticket. Fetch this ticket for branch naming and worktree setup; the summary/description may be generic. You can still derive a branch name from what the user is doing (e.g. "RETIRE-1908-add-settings-screen") or use the ticket summary if it’s descriptive.

If the user says they’re working on something without a ticket, unticketed work, or similar, use RETIRE-1908 and optionally ask for a short description to build the branch name.

## Workflow

### Step 1: Get Ticket or Issue

If the user hasn't provided a ticket or issue, **ALWAYS use the AskQuestion tool:**

- Title: "Which Ticket or Issue?"
- Question: "What would you like to start from?"
- Options:
  - id: "jira", label: "Jira ticket (e.g., RETIRE-123)"
  - id: "github", label: "GitHub issue (URL or owner/repo#N)"
  - id: "unticketed", label: "Unticketed work (use RETIRE-1908)"

Based on the response:

- "jira" → Ask for the Jira ticket number (e.g. RETIRE-123)
- "github" → Ask for the GitHub issue URL or owner/repo#N (or #N if current repo)
- "unticketed" → Use **RETIRE-1908** and optionally ask for a brief description for the branch name

If the user already provided a GitHub issue URL or owner/repo#N, treat as GitHub and parse it; no need to ask.

### Step 2: Fetch Details

**Jira:** Use the `jira-expert` subagent to fetch the ticket by key. Present: key, type, status, priority; summary; description (condensed); sprint/epic if available.

**GitHub:** Fetch the issue: from URL parse owner/repo and number, then `gh issue view N --repo owner/repo --json title,body,state,number`; or for #N in current repo use `gh issue view N --json title,body,state,number`. If `gh` fails or is unavailable, try `mcp_web_fetch` with the issue URL (public repos only). Present: number, title, state; body (condensed).

### Step 3: Generate Branch Name

Generate a kebab-case summary from the title/summary (lowercase, spaces/special chars → hyphens, no consecutive hyphens, 3-5 words).

- **Jira:** `[TICKET_KEY]-[kebab-case-summary]` (e.g. RETIRE-123-add-user-authentication)
- **GitHub:** `issue-[N]-[kebab-case-summary]` (e.g. issue-1-add-auth-flow)
- **Unticketed:** `RETIRE-1908-[kebab-case-summary]`

### Step 4: Determine Worktree Paths

- `[MAIN_WORKTREE]` = current workspace root (e.g., `/Users/timmy.garrabrant/Developer/mobile-app`)
- `[PROJECT_NAME]` = basename of main worktree (e.g., `mobile-app`)
- `[BRANCH_NAME]` = generated branch name from Step 3
- `[NEW_WORKTREE]` = `../[PROJECT_NAME]-[BRANCH_NAME]`

### Step 5: Check Prerequisites

```bash
# Check for existing branch
git branch --list [BRANCH_NAME]

# Check for existing worktree
git worktree list | grep [BRANCH_NAME]
```

If branch or worktree exists, **ALWAYS use the AskQuestion tool:**

- Title: "Branch/Worktree Already Exists"
- Question: "A branch or worktree named [BRANCH_NAME] already exists. How would you like to proceed?"
- Options:
  - id: "switch", label: "Switch to existing worktree"
  - id: "suffix", label: "Create with suffix (e.g., [BRANCH_NAME]-2)"
  - id: "abort", label: "Abort"

Based on the response:

- "switch" → Navigate to existing worktree
- "suffix" → Create new worktree with numeric suffix
- "abort" → Stop the workflow

### Step 6: Create Worktree with New Branch

Always base the new branch on origin/main:

```bash
git fetch origin main
git worktree add [NEW_WORKTREE] -b [BRANCH_NAME] origin/main
```

### Step 7: Copy Required Files

Copy .env from the main worktree:

```bash
cp [MAIN_WORKTREE]/.env [NEW_WORKTREE]/.env
```

### Step 8: Trust Mise Configuration

Trust the mise configuration in the new worktree to avoid permission errors:

```bash
cd [NEW_WORKTREE]
mise trust
```

This prevents the "Config files are not trusted" error when mise tools are invoked.

### Step 9: Install Dependencies

```bash
cd [NEW_WORKTREE]
npm install
```

Monitor progress - this takes several minutes.

### Step 10: Report Success

```
Started [TICKET_OR_ISSUE_REF]: "[Summary]"

Worktree created!
Branch: [BRANCH_NAME]
Location: [NEW_WORKTREE]
Based on: origin/main

Files copied: .env
Mise config: trusted
Dependencies: installed
```

### Step 11: Open in Cursor

**ALWAYS use the AskQuestion tool:**

- Title: "Open in Cursor?"
- Question: "Worktree created successfully at [NEW_WORKTREE]. Would you like me to open it in a new Cursor window?"
- Options:
  - id: "open", label: "Yes, open it"
  - id: "skip", label: "No, I'll open it manually"

Based on the response:

- "open" → Run `cursor [NEW_WORKTREE]`
- "skip" → Continue to next step

### Step 12: Prompt to Start Work

**ALWAYS use the AskQuestion tool:**

- Title: "Start Implementation?"
- Question: "Would you like me to start working on this ticket now?"
- Options:
  - id: "start", label: "Yes, start implementing"
  - id: "stop", label: "No, I'll do it myself"

Based on the response:

- "start" → Begin analyzing the codebase and implementing the requirements from the ticket description
- "stop" → End the workflow

## Error Handling

- **Ticket or issue not found**: Report the error and ask for a valid Jira key or GitHub issue URL/number
- **Branch exists**: Ask if user wants to switch to existing worktree or create with suffix
- **Worktree exists**: Ask to remove/recreate or use existing
- **Missing .env in main worktree**: Warn user that .env is missing from main worktree and must be created manually
- **mise trust fails**: Warn about the failure but continue with installation (mise trust is not critical)
- **npm install fails**: Show error, suggest `rm -rf node_modules && npm install`
- **Dirty working directory**: Warn user about uncommitted changes (though worktrees are isolated, this is informational)

## Cleanup

When done with a ticket:

```bash
# Remove worktree
git worktree remove [NEW_WORKTREE]

# Delete branch if merged
git branch -d [BRANCH_NAME]
```
