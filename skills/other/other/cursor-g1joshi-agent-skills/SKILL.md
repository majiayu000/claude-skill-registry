---
name: cursor
description: Cursor AI-powered code editor with chat. Use for AI-assisted coding.
---

# Cursor

Cursor is a fork of VS Code customized for AI. It pioneered **Tab-to-Complete** (Copilot++) and **Composer** (Multi-file edits). In 2025, it is the leading "AI Native" editor.

## When to Use

- **Heavy AI Usage**: If you copy-paste to ChatGPT 50 times a day, use Cursor.
- **Legacy Refactoring**: "Rewrite this entire legacy class to use React Hooks" works across multiple files.
- **Speed**: The "Shadow Workspace" indexing makes AI answers aware of full context instantly.

## Core Concepts

### Composer (Cmd+I)

A floating window that can edit multiple files simultaneously. "Add a `verified` field to the User model and update all call sites."

### Tab (Copilot++)

Predicts your next _cursor movement_, not just text. It feels like mind-reading.

### Indexing

Cursor locally indexes your code (embeddings) so the LLM knows about function definitions in other files without you opening them.

## Best Practices (2025)

**Do**:

- **Use Rules**: Add a `.cursorrules` file to repo root to instruct the AI (e.g., "Always use Tailwind", "No try/catch blocks").
- **Import VS Code Extensions**: It takes 1 click to migrate everything from VS Code.
- **Review Diffs**: Cursor applies changes fast. Always review the diff (`Cmd+Shift+P` -> Accept).

**Don't**:

- **Don't sleep on Model Toggle**: Switch between `claude-3.5-sonnet` (Coding) and `gpt-4o` (Reasoning) depending on task.

## References

- [Cursor Documentation](https://docs.cursor.com/)
