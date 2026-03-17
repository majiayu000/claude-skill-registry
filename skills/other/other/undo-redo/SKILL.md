---
name: undo-redo
description: Use the undo_redo tool to rewind or reapply buffered file changes or inspect diffs without UI navigation. Use when you need to adjust or verify changes in the current session history.
---

# Undo/Redo (LLM Tool)

## When to use

- You need to roll back or reapply buffered filesystem changes without asking the user to navigate the session tree.
- You need a diff for a specific file across conversation leaves.
- You need a list of all buffered diffs.

## Tool actions

`undo_redo` supports the following actions:

- `undo`: move to the previous leaf and restore files.
- `redo`: move to the next leaf and restore files.
- `list_diffs`: list all buffered diffs across leaves.
- `diff`: show a diff for a specific file.
  - `path` is required.
  - `leafId` is optional (defaults to the current leaf).

### Examples

```json
{"action":"undo"}
```

```json
{"action":"redo"}
```

```json
{"action":"list_diffs"}
```

```json
{"action":"diff","path":"src/index.ts"}
```

```json
{"action":"diff","leafId":"abcd1234","path":"README.md"}
```

## Important behavior difference vs commands

The tool does not trigger UI navigation and does not rebuild the current turn context. This keeps the current KV cache intact and avoids editor/tree updates. The new leaf and restored files will be applied for the next user prompt when pi rebuilds context. If the user wants immediate UI navigation and context replay, instruct them to use `/undo` or `/redo` instead.
