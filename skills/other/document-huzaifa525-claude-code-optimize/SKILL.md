---
name: document
description: Use when the user wants to add documentation, JSDoc, docstrings, or API docs to existing code.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Bash
argument-hint: "[file or directory]"
---

Document: **$ARGUMENTS**

## Steps

1. **Detect the language and doc style**
   - Check existing docs in the codebase for style
   - TypeScript/JavaScript → JSDoc or TSDoc
   - Python → Google-style docstrings
   - Go → godoc comments
   - Rust → `///` doc comments
   - Match whatever style already exists

2. **Read the code** thoroughly — understand every function, class, and type

3. **Add documentation for:**

   | Element | What to Document |
   |---------|-----------------|
   | Functions | Purpose, params, return value, throws, example |
   | Classes | Purpose, usage pattern |
   | Interfaces/Types | What it represents, field descriptions |
   | Constants | Why this value |
   | Complex logic | Step-by-step explanation |
   | Module/File | Top-level description of what this file does |

4. **Rules**
   - Document the WHY, not the WHAT (code already shows what)
   - Keep descriptions concise — one line if possible
   - Include `@example` for non-obvious usage
   - Don't document getters/setters or trivial functions
   - Match existing doc style in the codebase exactly

5. **Verify** — ensure no code was accidentally changed
   ```
   git diff --stat
   ```

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
