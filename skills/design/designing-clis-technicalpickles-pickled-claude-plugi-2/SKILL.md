---
name: designing-clis
description: Use when building, improving, or reviewing command-line interfaces for better user experience - before implementing commands/output/errors, when users report confusion or frustration, or when CLI feels hard to use - provides UX principles, visual design techniques, and practical patterns for creating discoverable, delightful CLIs
---

# Designing CLIs

## Overview

Modern CLIs are conversations between human and machine. Great CLIs feel discoverable, responsive, and forgiving. Poor CLIs leave users guessing, waiting, and frustrated.

**Core principle:** Every CLI interaction should answer: "What happened? What can I do? What's next?"

## When to Use

**Building:**
- Creating new CLI commands or tools
- Designing output format, error messages, progress indicators
- Planning CLI architecture (flags, subcommands, interaction model)

**Improving:**
- Enhancing existing CLI user experience
- Adding features to existing commands
- Making CLI "less confusing" or "easier to use"

**Reviewing:**
- Auditing CLI code for UX issues
- Responding to user complaints about difficulty
- Troubleshooting discoverability problems

## Quick Decision Framework

| Working On | Read This |
|------------|-----------|
| New CLI under time pressure | practical-patterns.md (Priority Checklist) |
| Adding to existing CLI | practical-patterns.md (Working with Existing CLIs) |
| Fixing "confusing" CLI | practical-patterns.md (CLI UX Audit Checklist) |
| Command structure, flags | ux-principles.md (Familiarity, Discoverability) |
| Output formatting | visual-techniques.md (Layout, Spacing, Color) |
| Error messages, help text | practical-patterns.md (Error Message Patterns) |
| Overall architecture | ux-principles.md (complete overview) |

## The Six UX Principles

1. **Familiarity** - Use known conventions (--help, --version, verb-noun)
2. **Discoverability** - Guide users (help text, prompts, examples)
3. **Feedback** - Show what's happening (progress, confirmations, state)
4. **Clarity** - Structure output (spacing, alignment, hierarchy)
5. **Flow** - Minimize friction (shortcuts, defaults, scriptability)
6. **Forgiveness** - Handle errors gracefully (clear messages, suggestions, safety)

See ux-principles.md for detailed guidance and examples.

## The Five Visual Techniques

1. **Color** - Semantic meaning (green=success, red=error, yellow=warning)
2. **Spacing** - Visual grouping (blank lines, indentation, alignment)
3. **Layout** - Structured regions (panels, blocks, persistent areas)
4. **Symbols** - Fast signifiers (✓ ✗ ⚠ →, checkboxes, progress indicators)
5. **Structured Feedback** - Narrative output (phases, lists, visible progress)

See visual-techniques.md for implementation patterns.

## Common Mistakes

❌ **Silent operations** - No feedback during slow operations
✅ Show progress, confirmations, or at minimum "Working..."

❌ **Cryptic errors without guidance** - "Error: invalid input"
✅ Explain what's wrong, what's valid, how to fix: "Error: Invalid environment 'production'. Valid: dev, staging, prod"

❌ **No --help text** - Forces users to read docs or source
✅ Every command supports --help with usage and examples

❌ **Wrong exit codes** - Always returns 0, breaks scripting
✅ 0 for success, 1 for errors

❌ **Color-only information** - Inaccessible without color support
✅ Always pair color with text/symbols, support --no-color

❌ **Walls of unstructured text** - Dense output hard to scan
✅ Use spacing, alignment, hierarchy to structure information

## Priority Under Time Pressure

When building CLI urgently, include these first (high impact, low effort):

1. **--help flag** (2 minutes) - Include usage, examples, common flags
2. **Exit codes** (1 minute) - 0=success, 1=error, enables CI/CD
3. **Clear errors** (5 minutes) - What happened + what's valid + how to fix
4. **Progress feedback** (3 minutes) - Show activity during slow operations

Skip initially (lower priority):
- Color schemes (polish, not function)
- Advanced formatting (tables, columns)
- Multiple output formats (JSON, YAML, etc.)

## Cross-References

**Detailed guidance:**
- practical-patterns.md - Checklists, templates, decision trees
- ux-principles.md - Principles with real-world examples
- visual-techniques.md - Implementation patterns for terminal output
- reading-list.md - Sources and deeper learning

**Research materials:**
- research/ - Original blog-style documentation and analysis
