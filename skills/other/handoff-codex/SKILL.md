---
name: handoff-codex
description: Delegate tasks to Codex CLI to save Claude context
user-invocable: true
---

# Handoff to Codex CLI

Delegate tasks to OpenAI Codex CLI to save Claude context.

---

## When to Use Codex

| Use Codex For | Keep in Claude |
|---------------|----------------|
| Simple file edits | Complex reasoning |
| Bulk refactoring | Architecture decisions |
| Code generation from specs | Problem analysis |
| Documentation updates | Multi-step workflows |

---

## Prerequisites

```bash
npm install -g @openai/codex
```

---

## Handoff Process

### 1. Prepare Context
```markdown
## Task for Codex
**Goal**: [What needs to be done]
**Files**: [Which files to modify]
**Details**: [Specific requirements]
```

### 2. Generate Command
```bash
# Single file
codex "Update login function in src/auth.ts to add rate limiting"

# Multiple files
codex "Refactor console.log to logger in src/**/*.ts"
```

### 3. Provide Instructions
- Why Codex is suitable
- Expected changes
- After completion steps

---

## Example

```markdown
## Task: Update All Import Statements

**Command:**
codex "Update all imports from 'lodash' to 'lodash-es' in src/**/*.ts"

**Expected:**
- ~15 files modified
- Each import updated

**After:**
1. Run `npm test`
2. Return if issues arise
```

---

## Benefits

- **Token Savings**: Simple tasks don't consume Claude context
- **Speed**: Fast for straightforward edits
- **Context Preservation**: Keep Claude fresh for complex reasoning
