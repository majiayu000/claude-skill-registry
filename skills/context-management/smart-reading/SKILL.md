---
name: smart-reading
version: 1.0.0
description: "Use when reading files or command output of unknown size to avoid blind truncation and context loss"
---

# Smart Reading

<ROLE>
Context Preservation Specialist. Reputation depends on never losing critical information to blind truncation.
</ROLE>

## Invariant Principles

1. **No Silent Data Loss** - Blind truncation (`head`, `tail -n`, arbitrary pipes) creates false confidence. Critical errors often appear at end of output.
2. **Size Before Strategy** - Unknown content size requires measurement (`wc -l`) before deciding read approach.
3. **Intent-Driven Delegation** - Subagents read ENTIRE content, return targeted summaries. Specify WHY you need content.
4. **Temp Files Demand Cleanup** - Every capture requires explicit cleanup plan. Use `$$` for collision-free naming.

## Reasoning Schema

<analysis>
Before reading any file or command output:
1. Size known? If not: `wc -l < "$FILE"`
2. ≤200 lines? Read directly
3. >200 AND need exact text? Read with targeted offset/limit
4. >200 AND need understanding? Delegate with explicit intent
5. About to use `head`, `tail -n`, truncating pipe? STOP. Delegate instead.

Before running command with unpredictable output:
6. Capture with `tee` for post-analysis? Or delegate entire command?
7. If capturing: cleanup plan exists?
8. If delegating: intent specified clearly?
</analysis>

<reflection>
After reading:
- Did I truncate blindly? (Forbidden)
- Did I check size before deciding approach?
- For delegation: did I specify WHY I need content?
- For temp files: cleanup planned?
IF YES to first or NO to others: STOP and fix approach.
</reflection>

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| File path or command | Yes | Target to read or execute |
| Intent | Yes | WHY content is needed (editing, understanding, error extraction) |
| Known size | No | Pre-existing knowledge of content length |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| Content or summary | Inline | Full content if small, targeted summary if delegated |
| Cleanup confirmation | Inline | Verification temp files removed (if applicable) |

## Decision Matrix

| Lines | Need Exact Text? | Action |
|-------|------------------|--------|
| ≤200 | Any | Read directly (full file) |
| >200 | Yes (editing) | Read with offset/limit to target section |
| >200 | No (understanding) | Delegate to Explore subagent with intent |

## Command Output Capture

```bash
command 2>&1 | tee /tmp/cmd-$$-output.txt  # Capture with streaming
wc -l < /tmp/cmd-$$-output.txt             # Measure
# Apply decision matrix
rm /tmp/cmd-$$-output.txt                  # ALWAYS cleanup
```

## Delegation Intents

| Intent | Subagent Returns |
|--------|------------------|
| Error extraction | All errors/warnings/failures with context |
| Technical summary | Condensed overview preserving structure |
| Presence check | Does X exist? Where? How? |
| Structure overview | Classes, functions, organization |

## Delegation Template

```
Read [file/output] in full. [INTENT STATEMENT]
Return: [specific deliverables]
Do not truncate. Read entire content before summarizing.
```

## Anti-Patterns

<FORBIDDEN>
- Blind truncation with `head`, `tail -n`, or pipes without size check
- Reading unknown-size files without measuring first
- Delegation without explicit intent statement
- Leaving temp files uncleaned
- Assuming errors appear at start of output
</FORBIDDEN>

### Examples

**Forbidden:**
```bash
pytest tests/ 2>&1 | head -100  # Errors often at end
cat src/large_module.py         # Unknown size
```

**Required:**
```bash
wc -l < src/large_module.py     # Check first: 1847 lines
# Delegate or read targeted section
```

```
Task(Explore): Run pytest tests/ and analyze output. Extract all
failures with full tracebacks. Summarize failure patterns.
```

## When to Use

**Direct Reading**: Small configs, known-small scripts, need exact text for editing, file already in context, verifying specific known lines.

**Delegation**: Test output (failures cluster unpredictably), build logs (errors at end), large files needing understanding not exact text, multiple files to cross-reference, searching unknown scope.

## Self-Check

Before completing:
- [ ] Size checked before reading unknown content
- [ ] No blind truncation used
- [ ] Delegation includes explicit intent if used
- [ ] Temp files cleaned up if created
- [ ] Critical information not lost to truncation

If ANY unchecked: STOP and fix approach.
