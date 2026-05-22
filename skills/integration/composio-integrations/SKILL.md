---
name: integrations
description: Use when connecting Claude to external apps (Slack, GitHub, Gmail, etc.) using the Composio Connect framework.
---

# App Integrations (Composio Connect)

## Overview
This skill enables the Antigravity SDK to interact with 1000+ external applications via the Composio "Connect" protocol. Use it to automate engineering communication, issue tracking, and cross-platform synchronization.

## The /connect Workflow

**USAGE**: Trigger this internally or via `/connect` when a task requires interacting with an external system.

### Core Steps
1. **Identify the App**: Determine which service handles the requirement (e.g., GitHub for issues, Slack for notices).
2. **Authorize (If Needed)**: Use the `connect` tool to initiate OAuth or API key setup.
3. **Execute Action**: Send emails, create tickets, post messages, or update databases.
4. **Verify Result**: Confirm the external state has changed (read back the created issue or sent message).

## Integration Patterns

| Action | Example Command | Intent |
| :--- | :--- | :--- |
| **Email/Slack** | `connect-slack-message --channel #dev --text "Build passed"` | Automated status updates. |
| **Issue Tracking** | `connect-github-create-issue --repo client-repo --title "Bug: Login fails"` | Direct bug reporting from IDE. |
| **Data Sync** | `connect-notion-append-block --page id --content "Phase 2 done"` | Documentation synchronization. |

## Common Integration Mistakes
- **Shadow Executions**: Taking action without notifying the user (always confirm significant external mutations).
- **Hardcoded IDs**: Attempting to use static IDs without first listing/searching for the correct entities.
- **Pollution**: Sending too many automated messages (group notifications into summaries).

## Verification Checklist
- [ ] Correct app and action identified.
- [ ] Authorization status verified.
- [ ] Execution result confirmed (idempotency checked).
- [ ] User notified of external side effects.
