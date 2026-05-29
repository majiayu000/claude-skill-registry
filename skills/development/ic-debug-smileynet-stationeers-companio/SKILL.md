---
name: ic-debug
description: Debug and fix IC10 code issues. Use when user has IC10 code that isn't working, has errors, or behaves unexpectedly in Stationeers.
---

# IC10 Code Debugging

Find and fix issues in IC10 code.

## Workflow

### 1. Debug Phase (Primary)
Use Task tool to spawn:
- `code-debugger` - Analyze issues AND provide fixes

The debugger will:
- Identify all issues in the code
- Explain root causes
- Provide corrected code for each issue
- Give the complete fixed code

### 2. Research Phase (If Needed)
If debugger needs more context about devices or syntax:
- `instruction-researcher` - Verify correct IC10 syntax
- `device-researcher` - Verify correct logic types for devices

These can run in parallel with the debugger if the problem description mentions specific devices or instructions.

## Common IC10 Issues

### Fatal Errors (Script Stops)
1. **Missing yield** - CPU overrun, must have yield in loops
2. **Line limit exceeded** - Over 128 lines won't compile
3. **Invalid instruction** - Typo or wrong syntax
4. **Device not connected** - Reading from empty port

### Logic Errors (Wrong Behavior)
1. **Inverted comparison** - Using sgt instead of slt
2. **Wrong device port** - d0-d5 mismatch with wiring
3. **Incorrect logic type** - Wrong property name
4. **Uninitialized registers** - Using before setting
5. **Missing device check** - No bdns before read

### Performance Issues
1. **No yield in fast loop** - Updates too slowly
2. **Redundant operations** - Reading same value repeatedly
3. **Unnecessary complexity** - Over-engineered solution

## Instructions

When user reports IC10 code issues:

1. **Launch code-debugger** with the user's code
   - Include the problem description
   - Include any error messages they reported
   - Include what behavior they expected

2. **Review debugger output**
   - Verify fixes make sense
   - Check that all issues are addressed

3. **Present the solution**
   - Show what was wrong
   - Show the corrected code
   - Explain briefly why it works now

4. **If multiple issues**
   - List issues by severity (Critical > High > Medium > Low)
   - Provide all fixes together in final corrected code

## Parallel Research

If the problem involves specific devices or unclear syntax, launch research agents in parallel with the debugger:

```
User: "My arc furnace won't activate"
→ Launch code-debugger + device-researcher (for Arc Furnace)

User: "Getting error on my lb instruction"
→ Launch code-debugger + instruction-researcher (for lb syntax)
```

## Example Triggers

- "My code isn't working"
- "This script has an error"
- "Why isn't this working?"
- "Help me fix this"
- "Debug this code"
- "The IC keeps stopping"
- "Getting CPU overrun"
- "My [device] isn't responding"
