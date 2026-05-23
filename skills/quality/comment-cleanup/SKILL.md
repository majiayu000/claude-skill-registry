---
name: comment-cleanup
description: "Clean up code comments. Use when: improving comment quality, removing redundant comments. Triggers on: 'clean up comments', 'comment cleanup'."
allowed-tools: Read, Edit, Glob, Grep
disable-model-invocation: true
argument-hint: <file_path>
---

# Comment Cleanup

I'll analyze and improve the documentation in the specified file following strategic documentation principles.

## Target File

$ARGUMENTS

## Documentation Philosophy

### Core Principles

1. **Self-documenting code first** - Improve naming and structure before adding comments
2. **Comments capture design intent** - Document WHY, not WHAT (when WHAT is obvious)
3. **Reduce cognitive load** - Make implicit knowledge explicit
4. **Eliminate redundancy** - Never restate what code already makes clear

### What Makes GOOD Comments

- **Design decisions** - Why this approach over alternatives
- **Non-obvious behavior** - Complex logic that isn't immediately clear
- **Interface contracts** - What a function/module does, parameters, returns
- **Important context** - Background information needed to understand
- **Gotchas and edge cases** - Subtle behaviors that could cause issues
- **Dependencies** - How components relate to each other

### What to AVOID

- Redundant comments restating obvious code
- Comments duplicating well-named variables/functions
- Implementation details that are self-evident
- Comments that would become outdated easily

## Analysis Process

1. **Read the file** to understand its purpose and structure
2. **Identify naming improvements** that could make code more self-documenting
3. **Find complex logic** that needs explanation
4. **Locate design decisions** that should be documented
5. **Remove harmful comments** that add noise or are outdated
6. **Add strategic comments** where they reduce cognitive load

## Execution

I will:

1. First read and analyze the target file
2. Suggest and apply naming improvements if needed
3. Remove redundant or misleading comments
4. Add comments only where they:
   - Explain non-obvious behavior
   - Document design decisions
   - Clarify complex algorithms
   - Provide essential interface documentation
5. Ensure all changes follow the "campsite rule" - leave code cleaner than found

The goal is **minimal, high-value documentation** - make code so clear it needs few comments, then add comments only where they capture essential information not expressible in code.
