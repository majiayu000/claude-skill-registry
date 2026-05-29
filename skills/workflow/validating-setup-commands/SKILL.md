---
name: validating-setup-commands
description: Use before creating worktrees or executing tasks - validates that CLAUDE.md defines required setup commands (install, optional postinstall) and provides clear error messages with examples if missing
---

# Validating Setup Commands

## Overview

**Worktrees require dependency installation before tasks can execute.** Projects MUST define setup commands in CLAUDE.md.

This skill validates setup commands exist BEFORE creating worktrees, preventing cryptic failures later.

## When to Use

Use this skill when:
- Creating new worktrees (spec, execute commands)
- Before executing tasks that need dependencies
- Any time you need to verify project setup is documented

**Use early:** Validate during setup phase, not during task execution.

## Why This Matters

**Without validation:**
- Worktrees get created
- Tasks start executing
- Fail with "command not found" errors
- User debugging nightmare: "Why is npm/pytest/cargo missing?"

**With validation:**
- Missing commands detected immediately
- Clear error with exact CLAUDE.md section to add
- User fixes once, all worktrees work

## The Validation Process

**Announce:** "Validating CLAUDE.md setup commands before creating worktrees."

### Step 1: Check File Exists

```bash
# Get repo root
REPO_ROOT=$(git rev-parse --show-toplevel)

# Check if CLAUDE.md exists
if [ ! -f "$REPO_ROOT/CLAUDE.md" ]; then
  echo "❌ Error: CLAUDE.md not found in repository root"
  echo ""
  echo "Spectacular requires CLAUDE.md to define setup commands."
  echo "See: https://docs.claude.com/claude-code"
  exit 1
fi
```

**Why fail fast:** No CLAUDE.md = no command configuration. Stop before creating any worktrees.

### Step 2: Parse Setup Section

```bash
# Parse CLAUDE.md for setup section
INSTALL_CMD=$(grep -A 10 "^### Setup" "$REPO_ROOT/CLAUDE.md" | grep "^- \*\*install\*\*:" | sed 's/.*: `\(.*\)`.*/\1/')

if [ -z "$INSTALL_CMD" ]; then
  echo "❌ Error: Setup commands not defined in CLAUDE.md"
  echo ""
  echo "Worktrees require dependency installation before tasks can execute."
  echo ""
  echo "Add this section to CLAUDE.md:"
  echo ""
  echo "## Development Commands"
  echo ""
  echo "### Setup"
  echo "- **install**: \`npm install\`  (or your package manager)"
  echo "- **postinstall**: \`npx prisma generate\`  (optional - any codegen)"
  echo ""
  echo "Example for different package managers:"
  echo "- Node.js: npm install, pnpm install, yarn, or bun install"
  echo "- Python: pip install -r requirements.txt"
  echo "- Rust: cargo build"
  echo "- Go: go mod download"
  echo ""
  echo "See: https://docs.claude.com/claude-code"
  echo ""
  echo "Execution stopped. Add setup commands to CLAUDE.md and retry."
  exit 1
fi

# Extract postinstall command (optional)
POSTINSTALL_CMD=$(grep -A 10 "^### Setup" "$REPO_ROOT/CLAUDE.md" | grep "^- \*\*postinstall\*\*:" | sed 's/.*: `\(.*\)`.*/\1/')
```

**Parsing logic:**
- Look for `### Setup` header
- Extract `**install**:` command (required)
- Extract `**postinstall**:` command (optional)
- Use sed to extract command from backticks

### Step 3: Report Success

```bash
# Report detected commands
echo "✅ Setup commands found in CLAUDE.md"
echo "   install: $INSTALL_CMD"
if [ -n "$POSTINSTALL_CMD" ]; then
  echo "   postinstall: $POSTINSTALL_CMD"
fi
```

**Store for later use:**
- Return `INSTALL_CMD` to caller
- Return `POSTINSTALL_CMD` (may be empty)
- Caller uses these in worktree dependency installation

## Expected CLAUDE.md Format

The skill expects this exact format:

```markdown
## Development Commands

### Setup
- **install**: `npm install`
- **postinstall**: `npx prisma generate`  (optional)
```

**Format requirements:**
- Section header: `### Setup` (exactly)
- Install line: `- **install**: `command`` (required)
- Postinstall line: `- **postinstall**: `command`` (optional)
- Commands must be in backticks

**Multi-language examples:**

```markdown
### Setup
- **install**: `npm install`           # Node.js
- **install**: `pip install -r requirements.txt`  # Python
- **install**: `cargo build`           # Rust
- **install**: `go mod download`       # Go
- **install**: `bundle install`        # Ruby
```

## Error Messages

### Error 1: CLAUDE.md Not Found

```
❌ Error: CLAUDE.md not found in repository root

Spectacular requires CLAUDE.md to define setup commands.
See: https://docs.claude.com/claude-code
```

**User action:** Create CLAUDE.md in repository root.

### Error 2: Setup Commands Missing

```
❌ Error: Setup commands not defined in CLAUDE.md

Worktrees require dependency installation before tasks can execute.

Add this section to CLAUDE.md:

## Development Commands

### Setup
- **install**: `npm install`  (or your package manager)
- **postinstall**: `npx prisma generate`  (optional - any codegen)

Example for different package managers:
- Node.js: npm install, pnpm install, yarn, or bun install
- Python: pip install -r requirements.txt
- Rust: cargo build
- Go: go mod download

See: https://docs.claude.com/claude-code

Execution stopped. Add setup commands to CLAUDE.md and retry.
```

**User action:** Add Setup section with at least `install` command.

## Integration Pattern

**How commands use this skill:**

```bash
# In execute.md or spec.md:

# Step 1.5: Validate Setup Commands
# Use validating-setup-commands skill to extract and verify
INSTALL_CMD=$(validate_setup_commands_install)
POSTINSTALL_CMD=$(validate_setup_commands_postinstall)

# Step 3: Create worktrees
git worktree add .worktrees/{runid}-task-1

# Step 4: Install dependencies using validated commands
cd .worktrees/{runid}-task-1
$INSTALL_CMD
if [ -n "$POSTINSTALL_CMD" ]; then
  $POSTINSTALL_CMD
fi
```

**Reusable across:**
- `/spectacular:spec` - Validates before creating main worktree
- `/spectacular:execute` - Validates before creating task worktrees
- Future commands that create worktrees

## Common Mistakes

### Mistake 1: Running Validation Too Late

**Wrong:** Create worktrees, then validate
**Right:** Validate BEFORE creating ANY worktrees

**Why:** Failed validation after worktrees exist leaves orphaned directories.

### Mistake 2: Not Providing Examples

**Wrong:** "Error: Add setup commands"
**Right:** "Error: Add setup commands. Here's the exact format: [example]"

**Why:** Users need to know WHAT to add and WHERE.

### Mistake 3: Requiring Postinstall

**Wrong:** Fail if postinstall missing
**Right:** Postinstall is optional (codegen only needed in some projects)

**Why:** Not all projects have codegen (Prisma, GraphQL, etc.).

## Quick Reference

**Validation sequence:**
1. Check CLAUDE.md exists (exit if missing)
2. Parse for `### Setup` section
3. Extract `install` command (exit if missing)
4. Extract `postinstall` command (optional)
5. Report success and return commands

**Exit points:**
- Missing CLAUDE.md → Error with creation instructions
- Missing setup section → Error with exact format example
- Success → Return INSTALL_CMD and POSTINSTALL_CMD

**Format validated:**
- `### Setup` header
- `- **install**: `command``
- `- **postinstall**: `command`` (optional)

## The Bottom Line

**Validate setup commands BEFORE creating worktrees.**

Early validation with clear error messages prevents confusing failures during task execution.

The skill provides users with exact examples of what to add, making fixes easy.
