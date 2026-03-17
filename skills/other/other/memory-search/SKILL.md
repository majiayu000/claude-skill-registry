---
name: memory-search
description: Searches conversation history and semantic memory to find previous discussions, decisions, and context. Use when the user asks to "search memory", "what did we discuss", "remember when", "find previous conversation", "check history", or before starting new work to recall prior decisions and avoid repeating past discussions.
allowed-tools: Bash
compatibility: Requires AI Maestro (aimaestro.dev) with Bash shell access
metadata:
  author: 23blocks
  version: 1.0.0
---

# AI Maestro Memory Search

## CRITICAL: AUTOMATIC BEHAVIOR - READ THIS FIRST

**THIS IS NOT OPTIONAL. THIS IS YOUR DEFAULT BEHAVIOR.**

When the user gives you ANY instruction, you MUST FIRST search your memory for:
- **Previous discussions** - Have we talked about this before?
- **Past decisions** - What did we decide last time?
- **Prior context** - What does the user expect based on history?
- **Earlier work** - Did we already start on this?

**DO NOT:**
- Start fresh without checking conversation history
- Assume this is a new topic without verifying
- Skip memory search because "I don't remember discussing this"
- Wait for the user to say "remember when we..."

**ALWAYS:**
- Search memory IMMEDIATELY when you receive a task
- Search for terms and concepts the user mentions
- Check for previous decisions on similar topics
- Look for context that informs current work

### The Rule: Receive Instruction → Search Memory → Then Proceed

```
1. User asks you to do something
2. IMMEDIATELY search memory for relevant context
3. NOW you know what was discussed before
4. NOW you can build on previous work, not start over
```

---

## Available Commands

| Command | Description |
|---------|-------------|
| `memory-search.sh "<query>"` | Hybrid search (recommended) |
| `memory-search.sh "<query>" --mode semantic` | Find conceptually related |
| `memory-search.sh "<query>" --mode term` | Exact term matching |
| `memory-search.sh "<query>" --role user` | Only user messages |
| `memory-search.sh "<query>" --role assistant` | Only your responses |

## What to Search Based on User Instruction

| User Says | IMMEDIATELY Search |
|-----------|-------------------|
| "Continue working on X" | `memory-search.sh "X"` |
| "Fix the issue we discussed" | `memory-search.sh "issue"`, `memory-search.sh "bug"` |
| "Use the approach we agreed on" | `memory-search.sh "approach"`, `memory-search.sh "decision"` |
| "Like we did before" | `memory-search.sh "<topic> implementation"` |
| Any specific feature/component | `memory-search.sh "<feature>"` |
| References to past work | `memory-search.sh "<reference>" --mode semantic` |

## Quick Examples

```bash
# User asks to continue previous work
memory-search.sh "authentication"
memory-search.sh "last session"

# User mentions a component we discussed
memory-search.sh "PaymentService" --mode term

# Find what the user previously asked for
memory-search.sh "user request" --role user

# Find your previous solutions
memory-search.sh "implementation" --role assistant

# Conceptual search for related discussions
memory-search.sh "error handling patterns" --mode semantic
```

## Search Modes

| Mode | Use When |
|------|----------|
| `hybrid` (default) | General search, best for most cases |
| `semantic` | Looking for related concepts, different wording |
| `term` | Looking for exact function/class names |
| `symbol` | Looking for code symbols mentioned |

### Symbol Mode Examples

The `symbol` mode is optimized for finding code symbols (function names, class names, variable names) mentioned in past conversations. Unlike `term` mode which does exact text matching, `symbol` mode understands code identifiers and matches them across different contexts.

```bash
# Find discussions where a specific function was mentioned
memory-search.sh "processPayment" --mode symbol

# Find conversations about a class
memory-search.sh "AuthenticationService" --mode symbol

# Find references to a variable or constant
memory-search.sh "MAX_RETRY_COUNT" --mode symbol
```

**When to use `symbol` vs `term`:**
- Use `--mode symbol` when searching for code identifiers (functions, classes, variables)
- Use `--mode term` when searching for exact phrases or non-code text

## Why This Matters

Without searching memory first, you will:
- Repeat explanations the user already heard
- Contradict previous decisions
- Miss context that changes the approach
- Start over instead of continuing

**Memory search takes 1 second. Frustrating the user is much worse.**

## Combining with Doc Search

For complete context, use BOTH:
```bash
# User asks about creating a new feature
memory-search.sh "feature"       # What did we discuss?
docs-search.sh "feature"         # What do docs say?
```

## Helper Scripts

This skill relies on an internal helper script that provides shared utility functions:

- **`memory-helper.sh`** - Sourced by the `memory-*.sh` tool scripts. Provides memory-specific API functions (`memory_query`, `init_memory`) and initialization logic. Located alongside the tool scripts in `~/.local/bin/` (installed) or `plugin/src/scripts/` (source). If tool scripts fail with "common.sh not found", re-run the installer (`./install-memory-tools.sh`).

## Error Handling

If no results found, that's valuable information too:
"No previous discussions found about X - this appears to be a new topic. Let me search the documentation..."

Then search docs as fallback.

**Script not found:**
- Check PATH: `which memory-search.sh`
- Verify scripts installed: `ls -la ~/.local/bin/memory-*.sh`
- Scripts are installed to `~/.local/bin/` which should be in your PATH

## Installation

If commands are not found:
```bash
./install-memory-tools.sh
```

This installs scripts to `~/.local/bin/`.
