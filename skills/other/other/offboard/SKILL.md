---
name: offboard
description: Walk through the Designer/Developer wrap-up checklist for offboarding a client engagement — conversationally, one item at a time.
disable-model-invocation: true
---

## Behavior

Walk through each wrap-up item below as a conversation. Go one item at a time. For each item:

1. Explain what needs to happen and why.
2. If you can assist directly (scan code, check branches, grep for secrets), do it right then.
3. Ask whether the item applies, whether it's done, or whether they need help.
4. Move on when they confirm.

Skip items that clearly don't apply based on what you've already learned (e.g., skip Figma items if there's no design work). If you're unsure, ask.

---

## Checklist

### 1. Transfer codebase ownership to the client

Check who owns the repo. Ask whether the client has admin access and whether any transfer is needed.

### 2. Upload files to client-accessible storage

Ask whether all project files (documents, assets, exports) have been uploaded to Basecamp, Drive, or whatever file storage the client uses.

### 3. Figma file transfer

Ask whether this engagement involved design work. If yes:

- Have Figma files been transferred to the client's organization, or exported as `.fig` files and sent?
- Does your team have a copy of the files?
- Have client members been removed as editors from your Figma team? (Viewers are fine — they don't count toward billing.)

If no design work, skip this entirely.

### 4. Archive Slack or other chat rooms

Ask which shared channels or chat rooms exist and whether they should be archived.

### 5. Clean up project management tools

Ask about Trello, Switchboard, or other project management tools. Should boards be archived or closed?

### 6. Transfer password manager entries

Ask whether any credentials are stored in your team's password manager that need to be transferred to the client's vault.

### 7. Delete sensitive user data from machines

Scan the local project directory for potential sensitive data:

- Grep for common patterns: API keys, tokens, passwords, `.env` files, credential files, database dumps, SSH keys.
- Check for `.env`, `.env.local`, `.env.production`, or similar files.
- Check for any database dumps or seed files with real user data.

Report what you find. Ask whether there's anything else on their machine that needs to be cleaned up.

### 8. Remove remote RSA keys on machines

Ask whether they added any SSH keys to client servers or services that should be removed.

### 9. Return client equipment

Ask whether they have any client equipment (laptops, hardware) to return.

### 10. Archive the retrospective

Ask whether the project retrospective has been documented and stored somewhere the team can reference it.

### 11. Archive design artifacts

Ask whether screenshots and other design artifacts have been saved somewhere accessible to the team. Skip if no design work.

### 12. Remind client to rotate credentials

This is important — any credentials or API keys the client shared should be rotated after offboarding.

Ask whether they've reminded the client to change credentials and API keys that were shared during the engagement.

### 13. Tidy up Google Docs

Ask whether project-related Google Docs have been organized into a folder and made accessible at the organization level.

### 14. Book knowledge transfer session

Ask whether a knowledge transfer session has been scheduled to walk the client through all resources, the codebase, and anything they'll need to maintain going forward.

If the codebase is in the current working directory, offer to help prepare — check the README, look at open branches, scan for TODOs, and identify areas that might need a walkthrough.

---

## Tone

Calm, professional, thorough. You're a colleague helping them make sure nothing falls through the cracks. Don't rush — each item matters. But don't over-explain items they've already handled.
