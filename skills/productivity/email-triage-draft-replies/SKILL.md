---
name: email-triage-draft-replies
description: Review unread email, categorize it, and draft replies (no sending without approval)
---

## What you do

1. Use Gmail MCP to list unread messages (metadata/snippet by default).
2. Categorize messages into:
   - High Priority (needs reply)
   - Low Priority (FYI)
   - Newsletters (archive candidate)
3. For High Priority messages, selectively read full content for the top items only.
4. Draft replies for the High Priority set.
5. If the user wants, create drafts (not send) using Gmail MCP.

## Safety

- Do not send emails.
- Creating drafts is allowed only after approval.
- Never include secrets/tokens.

## Output format

- High Priority (with 1-2 sentence summary each)
- Draft replies (one section per email)
- Suggested archives (newsletters)
