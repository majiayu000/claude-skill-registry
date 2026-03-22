---
name: context-optimization
description: >
  Strategies for managing Claude Code's context window efficiently: token budgeting,
  progressive disclosure, reference files, and using subagents to protect context.
  Use when conversations are getting long, the user mentions context limits, or
  tasks involve reading many files.
---

# Context Optimization

Claude Code's context window is finite. Efficient use of context enables longer sessions, larger refactors, and deeper analysis without hitting limits or losing important earlier information.

## When to Use
- Conversation is approaching context limits (system may compress earlier messages)
- Task requires reading many large files
- User mentions running out of context or losing earlier information
- Planning a large refactoring or multi-file implementation
- Deciding whether to use subagents vs direct tool calls

## Core Patterns

### Token Budgeting

Estimate context costs before reading files:

```
Small file (< 100 lines):   ~500-1000 tokens   -- Read freely
Medium file (100-500 lines): ~1000-5000 tokens  -- Read if needed
Large file (500+ lines):     ~5000+ tokens      -- Use offset/limit or subagent
```

For large files, read only the relevant section:

```
Read:
  file_path: "src/services/auth.ts"
  offset: 150    # Start at line 150
  limit: 50      # Read only 50 lines
```

### Progressive Disclosure

Start with structure, then drill into details:

```
# Step 1: Understand the project structure (cheap)
Glob: "src/**/*.ts"

# Step 2: Find the relevant area (cheap)
Grep: pattern "export function authenticate"

# Step 3: Read only the relevant file (targeted)
Read: "src/middleware/auth.ts"

# Step 4: Read related files only if needed
Read: "src/types/auth.ts"
```

Do not read all source files upfront. Discover what you need, then read it.

### Reference Files Instead of Inline Content

When a file's contents have been read and discussed, refer to it by path and line number instead of quoting large blocks:

```
# EXPENSIVE: Quoting 30 lines of code in your response
"The function at lines 45-75 does X, here is the full code: ..."

# EFFICIENT: Reference by path and line
"The authenticate function at src/middleware/auth.ts:45 handles
token validation. The error branch at line 62 needs updating."
```

### Subagents as Context Firewalls

Use subagents when exploration would consume too much main context:

```
# BAD: Reading 15 files directly into main context
Read: "src/db/users.ts"
Read: "src/db/posts.ts"
Read: "src/db/comments.ts"
... (12 more files)

# GOOD: Delegate to subagent, receive summary only
Agent (Explore):
  prompt: "Read all files in src/db/. For each file, report:
           1. Table/model name
           2. Key query functions
           3. Whether it uses parameterized queries
           Return a concise table with these columns."
```

The subagent reads all 15 files in its own context. The main context receives only the summary table.

### Targeted Grep Before Read

Use Grep to locate exactly what you need before reading entire files:

```
# Step 1: Find where the function is defined
Grep:
  pattern: "export function processPayment"
  output_mode: "content"
  -C: 3

# Step 2: Read only if you need more context around it
Read:
  file_path: "src/services/billing.ts"
  offset: 120
  limit: 40
```

### Context-Sensitive Task Sizing

Match task complexity to remaining context:

High context remaining (early in session):
- Large refactors across multiple files
- Feature implementation spanning many components
- Deep codebase exploration

Low context remaining (late in session):
- Single-file edits
- Independent utility creation
- Simple bug fixes with known location
- Documentation updates

### Avoiding Context Waste

Common context wasters to avoid:

```
# WASTE: Reading a file you will not modify
Read: "package.json"  # Just to "check" — only read if you need specific info

# WASTE: Reading the same file twice
Read: "src/app.ts"  # Read earlier in session
Read: "src/app.ts"  # Reading again because you forgot — check conversation first

# WASTE: Large verbose tool output
Bash: "npm list --all"  # Produces hundreds of lines
# Better: "npm list --depth=0"  # Top-level only

# WASTE: Reading generated files
Read: "dist/bundle.js"  # Generated, not useful
Read: "node_modules/..."  # Never read node_modules
```

## Anti-Patterns

- **Reading everything upfront**: Do not read all project files at the start of a session. Use progressive disclosure — start with structure, drill into specifics.
- **Ignoring offset/limit**: For large files, always use offset and limit to read only the relevant section. Reading a 2000-line file when you need lines 500-520 wastes context.
- **Quoting code back to the user**: The user can see the file. Reference by path:line instead of copying 30 lines into your response.
- **Repeating tool calls**: If you already read a file earlier in the session, do not read it again. Use your conversation history.
- **Using verbose bash output**: Commands like `npm list --all`, `find / -name "*.ts"`, or `git log` without limits dump large amounts of text. Always constrain output with flags or pipes.

## Quick Reference

| Strategy | When | How |
|----------|------|-----|
| Progressive disclosure | Starting exploration | Glob -> Grep -> Read (targeted) |
| Offset/limit | Large files | `offset: N, limit: M` on Read |
| Subagent firewall | Many files to analyze | Agent (Explore) with summary prompt |
| Reference by path | Discussing code | `file.ts:line` instead of quoting |
| Targeted grep | Finding specific code | Grep with context before Read |
| Output constraints | Bash commands | Use `--depth`, `head`, `tail`, flags |

**Rule**: Read only what you need, when you need it. Summarize, do not quote.
