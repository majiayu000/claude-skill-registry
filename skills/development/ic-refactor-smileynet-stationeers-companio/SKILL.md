---
name: ic-refactor
description: Refactor IC10 code for clarity and structure. Use when user wants to reorganize code, apply design patterns, improve naming, or make code more maintainable without changing functionality.
---

# IC10 Code Refactoring

Restructure IC10 code for better clarity, organization, and maintainability.

## When to Use

This skill is for **restructuring** code, not optimizing it:

| User Request | Use This Skill? |
|-------------|-----------------|
| "Refactor this code" | ✅ Yes |
| "Make this more readable" | ✅ Yes |
| "Reorganize this script" | ✅ Yes |
| "Apply state machine pattern" | ✅ Yes |
| "Extract constants" | ✅ Yes |
| "Reduce line count" | ❌ Use ic-optimize |
| "Make this faster" | ❌ Use ic-optimize |
| "Fix this bug" | ❌ Use ic-debug |

## Workflow

### 1. Analysis Phase
Use Task tool to spawn in parallel:
- `code-analyzer` - Understand current structure and identify issues
- `pattern-finder` - Find applicable patterns from examples

### 2. Refactoring Phase
Use Task tool to spawn:
- `code-refactorer` - Apply refactoring with analysis context

Provide the refactorer with:
- Original code
- Analysis results
- User's specific requests (if any)
- Applicable patterns found

### 3. Documentation Phase (Optional)
If code needs documentation after refactoring:
- `code-documenter` - Add/update comments and headers

## Refactoring Types

### Structure Refactoring
- Organize code into clear sections (aliases, constants, main loop)
- Add section headers with comments
- Group related operations together

### Naming Refactoring
- Replace d0-d5 with meaningful aliases
- Replace r0-r15 with descriptive names where appropriate
- Extract magic numbers to named defines

### Pattern Application
- State machine for multi-phase processes
- Hysteresis for threshold control
- PID for smooth control loops
- Subroutines for repeated logic

### Code Clarity
- Split complex conditions into steps
- Add intermediate variables for clarity
- Improve comment quality

## Instructions

When user requests IC10 refactoring:

1. **Identify refactoring type**
   - Is it structure, naming, pattern, or general cleanup?
   - Note any specific user requests

2. **Launch analysis agents** (parallel)
   - code-analyzer: Current structure assessment
   - pattern-finder: Applicable patterns

3. **Launch refactorer** with context
   - Include analysis results
   - Specify user's focus areas
   - Request explanation of changes

4. **Present results**
   - Show before/after comparison
   - Explain each change made
   - Highlight patterns applied

5. **Offer documentation** if needed
   - Ask if user wants additional comments
   - Can run code-documenter as follow-up

## Example Triggers

- "Refactor this for clarity"
- "Reorganize this code"
- "Make this more readable"
- "Apply state machine pattern"
- "Extract constants from this"
- "Improve the structure"
- "Clean up this script"
- "Add proper aliases"
- "Convert to hysteresis pattern"

## Key Principles

1. **Never change functionality** - Refactoring preserves behavior
2. **Clarity over brevity** - May add lines for readability
3. **Meaningful names** - All aliases should be descriptive
4. **Pattern where appropriate** - Don't force patterns unnecessarily
5. **Explain changes** - User should understand what changed and why
