---
name: cleaning-project
description: Scans the codebase for unused files, dead code, and common junk patterns. Always performs a "Dry Run" first to list candidates for deletion and requires explicit user confirmation.
---

# Project Cleaner & Janitor

## When to use this skill
- When the user explicitly asks to "clean up unused files" or "delete dead code".
- Post-refactoring, to remove old implementations.
- When the project feels "bloated" with temporary files.

## Workflow

### 1. The Scan (Dry Run)
**Do not delete anything yet.**
1.  **Junk Pattern Scan**: Look for common temporary/system files:
    - `.DS_Store`, `Thumbs.db`, `.log` files (root), `.tmp` files.
    - **Empty Directories**: Find folders with no content.
2.  **Orphan File Scan (Static Analysis)**:
    - Identify all source files (ts, js, dart, py).
    - Checks if each file is imported by *at least one* other file in the project.
    - *Exclusion*: Ignore "entry points" (e.g., `main.tsx`, `page.tsx`, `index.js`, `app.py`) as they are rarely imported but essential.
3.  **Dead Code Scan**:
    - Identify exported functions/constants that are never imported.
    - *Note*: This is complex to do perfectly with regex. If using a language server (LSP) is possible, use it. Otherwise, rely on reliable grep/ripgrep searches.

### 2. The Report
Present the findings to the user in a clear list:
```markdown
### 🧹 Cleaning Report
**Junk Files (Safe to delete):**
- `.DS_Store`
- `npm-debug.log`

**Orphan Files (No imports found):**
- `src/components/OldButton.tsx` (CAUTION: Is this an entry point?)
- `utils/unused_helper.js`

**Empty Folders:**
- `src/features/old_feature/`
```

### 3. The Confirmation
Ask: *"Do you want me to proceed with deleting the Junk Files? What about the Orphan Files?"*

### 4. The Action
Only after receiving "Yes" or specific instructions (e.g., "Delete junk, keep orphans"):
1.  Run the deletion commands.
2.  (Optional) If it was dead code removal within a file, edit the file to remove the unused block.

## Instructions

### Tools to Use
- **`find`**: For empty directories (`find . -type d -empty`).
- **`fd` / `find`**: For pattern matching junk files.
- **`grep` / `ripgrep`**: For checking imports.
    - *Heuristic*: To check if `OldButton.tsx` is used, search for `OldButton` string in the whole `src/` directory. If count is 1 (the definition itself), it's likely unused.

### Safety Rules
1.  **Never delete `node_modules/`, `.git/`, `.next/`, `build/`** manually. (Use standard clean commands for those).
2.  **Always respect `.gitignore`**.
3.  **Backup Strategy**: If the user is unsure, offer to move files to a `_deprecated/` folder instead of permanent deletion.

## Self-Correction Checklist
1.  "Did I assume this file is unused just because I didn't see an import?" -> Check if it's a Next.js Page (`page.tsx`) or API route. THESE ARE NEVER IMPORTED. **Whitelist them.**
2.  "Am I about to delete a configuration file?" -> Whitelist `*.config.js`, `Dockerfile`, `.env*`.
