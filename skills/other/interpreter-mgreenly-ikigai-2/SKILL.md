---
name: patterns/interpreter
description: Interpreter Pattern pattern for C development
---

# Interpreter Pattern

Define a grammar and interpreter for a language. Parse input into AST, evaluate by walking tree. Used for DSLs, expressions, commands.

## ikigai Application

**Slash commands:** Simple interpreter - parse command name and args, dispatch to handler.

**Future DSL possibilities:**
- Query language for conversation search
- Filter expressions for message selection
- Template syntax for prompts

**Current approach:** Slash commands are simple enough that full interpreter isn't needed. Direct string matching suffices.

**When to use:** If command syntax grows complex (flags, subcommands, expressions), consider proper parser with grammar definition.

**ANSI parsing:** Terminal escape sequences are interpreted via state machine, a lightweight interpreter.
