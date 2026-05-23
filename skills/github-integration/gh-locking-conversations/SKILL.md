---
name: gh-locking-conversations
description: Locks or unlocks an issue conversation. Use to manage noise or conclude discussions.
---

# Locking Conversations

## Purpose

Restricts commenting on an issue using the `gh issue lock` command.

## 1. Safety & Verification

- **Reason**: You can specify a reason (off-topic, resolved, etc.).

## 2. Common Workflows

### Workflow: Lock Resolved Issue

Prevents further comments on a finalized discussion.

**Command**:

```bash
gh issue lock <issue-number> --reason resolved
```
