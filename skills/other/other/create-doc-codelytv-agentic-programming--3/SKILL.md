---
name: create-doc
description: Create or improve documentation based on the current conversation. Use this when a plan has been created and changes were requested because it didn’t follow the repository’s conventions.
---

Based on the current conversation, create new or improve existing documentation files inside the `docs/` folder.

## Steps

1. Identify conventions, patterns, or decisions discussed in the conversation that should be documented.
2. Check if a relevant doc already exists in `docs/` (organized by area: `backend/`, `frontend/`, `database/`, etc.).
   - If it exists, improve it while preserving the required structure.
   - If it does not exist, create a new file in the appropriate subfolder.
3. Read `docs/documentation-guidelines.md` and follow its structure exactly. Every document MUST include these sections in order:
```
# 🎯 Name of the convention

## 💡 Convention
## 🏆 Benefits
## 👀 Examples (with ✅ Good and ❌ Bad subsections)
## 🧐 Real world examples
## 🔗 Related agreements
```

4. Ask the user to confirm the target file path before writing.
5. Update the AGENTS.md index with the new doc.

## Rules

- Each convention goes in its own standalone Markdown file — never bundle multiple conventions into one doc.
- Place files in the correct area subfolder (`backend/`, `frontend/`, `database/`, `testing/`, etc.).
- Include concrete good and bad examples with code blocks when applicable.
- Link to real files in the codebase that follow the convention in the "Real world examples" section.
