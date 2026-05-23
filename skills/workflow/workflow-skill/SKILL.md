---
name: [workflow-name]
description: [End-to-end workflow description]. Use when [full workflow trigger], or when user asks to "[action phrase]".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# [Workflow Name]

Complete workflow for [end goal].

## Workflow Overview

```
[Step 1] → [Step 2] → [Step 3] → [Complete]
```

## When to Use

- Beginning [project phase]
- When user requests "[natural language trigger]"
- For [specific scenario]

## Prerequisites

Before starting:
- [ ] [Requirement 1]
- [ ] [Requirement 2]
- [ ] [Requirement 3]

## Complete Workflow

### Phase 1: [Name]

**Goal**: [What this phase achieves]

**Steps**:
1. **[Action]** - Run:
   ```bash
   # Command
   ```
   Expected output: ...

2. **[Action]** - Check:
   ```bash
   # Verification
   ```
   Should see: ...

3. **[Action]** - Proceed to Phase 2

### Phase 2: [Name]

**Goal**: [What this phase achieves]

**Steps**:
1. ...
2. ...

### Phase 3: [Name]

**Goal**: [What this phase achieves]

**Steps**:
1. ...
2. ...

## Validation

After completion, verify:
```bash
# Check 1
# Check 2
# Check 3
```

All checks should ✅ pass.

## Rollback

If something goes wrong:

1. **Stop current process**:
   ```bash
   # Stop command
   ```

2. **Restore previous state**:
   ```bash
   # Rollback command
   ```

3. **Verify rollback**:
   ```bash
   # Verification
   ```

## Files Modified

This workflow touches:
- `[file1]` - [how modified]
- `[file2]` - [how modified]

## Success Criteria

✅ Workflow complete when:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Common Issues

See [Troubleshooting](#troubleshooting) section.

## Automation

To automate this workflow:
```bash
# Script or command
```

## Related Workflows

- `[related-workflow-1]` - Run before this
- `[related-workflow-2]` - Run after this

## Version History

- v1.0.0 (YYYY-MM-DD): Initial workflow
