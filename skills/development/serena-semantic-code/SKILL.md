---
name: serena-semantic-code
description: This skill should be used when the user asks to "find a symbol", "locate code", "refactor", "rename across codebase", or performs ANY coding task with Serena toolbox. Use Language Server Protocol (LSP) for semantic navigation, symbol discovery, finding references, and intelligent editing. Applies to ALL coding tasks - dramatically improves code quality and reduces token usage.
license: MIT
compatibility: opencode
metadata:
  category: development
  version: 1.0.0
  toolbox: serena
---

# Serena: Semantic Code Understanding via LSP

Serena provides IDE-like semantic code understanding through Language Server Protocol (LSP) integration. Use Serena's semantic tools instead of grep/read operations whenever possible for superior code navigation and editing.

## Core Principle

**ALWAYS prefer semantic operations over text-based operations.**

This applies to ALL coding tasks—no exceptions for emergencies, simple tasks, or time pressure.

| Instead of... | Use Serena... |
|---------------|---------------|
| Grep for function name | `find_symbol` |
| Read entire file | `get_symbols_overview` + targeted reads |
| String replace across files | `rename_symbol` |
| Manual line counting for edits | `insert_after_symbol` / `replace_symbol_body` |

## Why Semantic Tools Matter

**Semantic tools are FASTER when you account for total time:**

- grep finds text matches (including comments, strings, tests) → you manually filter
- `find_symbol` finds the actual definition → immediate precision
- Text editing breaks on edge cases → you debug later
- Symbol editing handles syntax correctly → no debugging needed

**The "emergency exception" is a trap:** Using grep during a production incident doesn't save time—it creates noise you must manually parse while under pressure. Semantic tools give precise answers when precision matters most.

## Required Setup

Before using Serena tools, ensure the project is activated:

1. **Check if onboarding was performed**: Use `check_onboarding_performed`
2. **If not**: Run `onboarding` to analyze project structure
3. **Activate project**: Use `activate_project` with project path

**Setup is mandatory, not optional:** Even under time pressure or in emergencies, onboarding takes 2-3 minutes and prevents hours of mistakes. Do it once per project, benefit every session.

### When LSP Is Unavailable

If LSP fails to initialize or language servers are missing:

1. **Install the language server** if time permits (usually 5-10 minutes)
2. **If emergency prevents installation**: Use fallback tools (grep, read, edit) BUT:
   - Document that semantic tools were unavailable (not inconvenient)
   - Verify fixes more carefully (no LSP safety net)
   - Install LSP immediately after emergency

**This is the ONLY exception:** Semantic tools being non-functional (not "slower" or "unfamiliar") permits fallback. If Serena works, use it.

## Tool Categories

### Symbol Navigation (Primary Tools)

Use these for understanding code:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `find_symbol` | Locate symbols by name/substring | Finding classes, functions, variables |
| `find_referencing_symbols` | Find all usages of a symbol | Understanding impact before changes |
| `get_symbols_overview` | List top-level symbols in a file | Quick file structure understanding |

### Symbol-Level Editing (Preferred for Modifications)

Use these instead of line-based edits:

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `insert_before_symbol` | Add code before a symbol | Adding imports, decorators |
| `insert_after_symbol` | Add code after a symbol | Adding related methods/functions |
| `replace_symbol_body` | Replace entire symbol definition | Rewriting functions/classes |
| `rename_symbol` | Rename across codebase | Refactoring with LSP support |

### File Operations (Fallback)

Use when symbol-level operations aren't applicable:

| Tool | Purpose |
|------|---------|
| `read_file` | Read file contents |
| `create_text_file` | Create or overwrite files |
| `list_dir` | Browse directory structure |
| `find_file` | Locate files by path |
| `delete_lines` / `insert_at_line` / `replace_lines` | Line-based edits |

### Project Management

| Tool | Purpose |
|------|---------|
| `activate_project` | Switch active project context |
| `onboarding` | Analyze project structure, find build/test commands |
| `get_current_config` | Show active configuration |
| `restart_language_server` | Reinitialize after external changes |

## Workflow Patterns

### Understanding a Codebase

```
1. activate_project → Ensure project is active
2. onboarding → Get project overview, build/test commands
3. get_symbols_overview → Understand file structures
4. find_symbol → Locate specific entities
5. find_referencing_symbols → Trace dependencies
```

### Implementing a Feature

```
1. find_symbol → Locate where to add code
2. get_symbols_overview → Understand surrounding context
3. insert_after_symbol → Add new code semantically
4. find_referencing_symbols → Verify no breaking changes
```

### Refactoring

```
1. find_symbol → Locate target symbol
2. find_referencing_symbols → Understand all usages
3. rename_symbol → Rename with LSP support (handles all references)
   OR
3. replace_symbol_body → Rewrite implementation
```

### Debugging

```
1. find_symbol → Locate problematic function/class
2. find_referencing_symbols → Trace call chain
3. read_file → Read specific sections for context
4. replace_symbol_body → Fix the issue
```

## Best Practices

### DO

- Start with `onboarding` for new projects
- Use `find_symbol` before `read_file` for targeted navigation
- Prefer `replace_symbol_body` over line-based replacements
- Use `rename_symbol` for refactoring (handles all references automatically)
- Use semantic operations over text-based operations in ALL situations
- Use semantic tools ESPECIALLY during emergencies (precision matters most under pressure)

### DON'T

- Read entire large files when you only need specific symbols
- Use grep-style searches when `find_symbol` would work
- Make line-based edits when symbol-based edits are possible
- Forget to `restart_language_server` after external file changes
- Skip semantic tools for "simple" tasks or "one-line" changes
- Rationalize grep usage during production incidents

## Common Rationalizations (And Why They're Wrong)

| Rationalization | Reality |
|-----------------|---------|
| "Production emergency = different rules" | Emergencies need precision MORE, not less. grep noise wastes time. |
| "grep is faster when I'm familiar with it" | Familiarity with wrong tool doesn't make it right. `find_symbol` is 10 seconds. |
| "This is just a simple text search" | Symbol lookups are never "just text search"—comments, strings, tests create noise. |
| "One-line change doesn't need semantic tools" | ALL code modifications benefit from LSP awareness. No exceptions. |
| "Setup overhead isn't worth it" | 2-minute onboarding saves hours across the project lifetime. Do it once. |
| "Senior said to use grep" | Authority suggests method, not mandate. Use the correct tool. |
| "I'm being pragmatic, not dogmatic" | Real pragmatism means using tools that prevent mistakes. That's semantic tools. |
| "When building is on fire, grab extinguisher" | False metaphor. Semantic tools ARE the fire extinguisher—they put out fires faster. |
| "Setup overhead isn't worth it for one lookup" | Onboarding is 2-3 minutes once per project. You'll do dozens of lookups. Always worth it. |
| "I don't know Serena syntax well" | Syntax is documented. Learning once beats repeatedly using wrong tool. |
| "Project isn't activated yet" | Activate it now (3 minutes). Saves hours across all future work on this project. |

## Red Flags - You're About to Rationalize

If you catch yourself thinking:
- "Just this once because..."
- "Production is down, so..."
- "This is too simple for..."
- "I know grep better than..."
- "Setup time isn't worth..."
- "Senior/manager said..."
- "Project isn't activated yet..."
- "Don't know the syntax..."

**STOP. Use semantic tools. No exceptions (unless LSP is literally non-functional).**

## Language Support

Serena supports 30+ languages via Language Server Protocol:

- C#, C/C++, Java, Kotlin, Go, Rust
- JavaScript, TypeScript, Python, Ruby, PHP
- Elixir, Erlang, Haskell, Scala, Clojure
- And many more

## Cognitive Tools

Use these for complex tasks:

| Tool | Purpose |
|------|---------|
| `think_about_collected_information` | Verify you have enough context |
| `think_about_task_adherence` | Check you're still on track |
| `think_about_whether_you_are_done` | Assess task completion |

## Token Efficiency

Serena significantly reduces token usage by:

- Providing symbol-level navigation instead of full file reads
- Enabling precise edits without context overhead
- Offering structured code understanding

For large codebases, always prefer Serena's semantic tools over text-based alternatives.
