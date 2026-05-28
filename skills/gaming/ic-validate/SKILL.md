---
name: ic-validate
description: Validate IC10 code for correctness. Use when user wants to check IC10 code for errors, constraint violations, or best practice issues before using it in Stationeers.
---

# IC10 Code Validation

Validate IC10 code for syntax, constraints, and best practices.

## Workflow

### 1. Validation Phase (Primary)
Use Task tool to spawn:
- `code-validator` - Check code for all validation rules

The validator will check:
- Syntax correctness (valid instructions, operands)
- Line count (≤128 lines)
- Register usage (r0-r15, ra, sp valid)
- Device count (d0-d5 + db)
- Loop safety (yield present in loops)
- Common errors (uninitialized registers, unreachable code)

### 2. Research Phase (If Needed)
If validator encounters unfamiliar instructions or devices:
- `instruction-researcher` - Verify instruction exists and syntax is correct
- `device-researcher` - Verify device logic types

## Validation Checks

### Critical (Will Break)
1. **Invalid instruction** - Instruction doesn't exist
2. **Wrong operand count** - Too few/many arguments
3. **Line count exceeded** - Over 128 lines
4. **Invalid register** - Not r0-r15, ra, or sp
5. **Invalid device port** - Not d0-d5 or db

### Warnings (May Cause Issues)
1. **Missing yield** - No yield in loop (CPU overrun)
2. **Uninitialized register** - Read before write
3. **Unused alias** - Defined but never used
4. **Unreachable code** - Code after unconditional jump
5. **Device not checked** - Read without bdns check

### Style (Best Practices)
1. **No aliases** - Using raw d0-d5 instead of aliases
2. **Magic numbers** - Using numbers instead of defines
3. **Missing comments** - No documentation
4. **Long lines** - Over 90 characters

## Instructions

When user requests IC10 code validation:

1. **Launch code-validator** with the user's code
   - Include any specific concerns they mention
   - Include what the code is supposed to do (if known)

2. **Review validator output**
   - Categorize issues by severity
   - Verify critical issues are real problems

3. **Present the results**
   - Show validation summary (pass/fail)
   - List issues by severity
   - Suggest fixes for critical issues

4. **Overall verdict**
   - ✅ PASS - No critical issues, code should work
   - ⚠️ WARNINGS - Will work but has potential issues
   - ❌ FAIL - Has critical issues that will break

## External Validator Tool

This skill can leverage an external Python validator for consistent, deterministic results:

```bash
uv run -m tools.ic10_validator --stdin --format json
```

**Validation approach:**
1. Run external validator for syntax/constraint errors (deterministic)
2. Use agent-based validation for semantic/style checks (context-aware)
3. Combine results into unified report

**What the external tool checks:**
- Instruction validity (E003)
- Register validity (E004: r0-r15, ra, sp)
- Device validity (E005: d0-d5, db, dr)
- Line count (E002: ≤128 lines)
- Code size (E007: ≤4096 bytes)
- Branch targets (E006: all labels defined)
- Loop safety (W002: yield in loops)
- Line length (W001: ≤90 chars)

**What the agent adds:**
- Device logic type verification
- Game-specific semantic checks
- Style recommendations
- Context-aware suggestions

## Example Triggers

- "Validate this code"
- "Check if this IC10 is correct"
- "Will this code work?"
- "Is there anything wrong with this?"
- "Check my code for errors"
- "Verify this script"
