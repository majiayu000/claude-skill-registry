---
name: dogfood
description: Enforces dogfooding for tool projects and prevents manual workarounds.
Use when building CLIs, libraries, or automation that you should use yourself.
Triggers on: feature completion, session end, tool failures.

category: principles
user-invocable: true
---

# Dogfood

When building tools, you MUST use the tools you build. When tools fail, you MUST fix them - never work around them.

## Core Principles

### 1. Use What You Build

If you're building a tool that does X, you must use X yourself. Dogfooding:
1. Reveals bugs and UX issues
2. Builds understanding of user pain points
3. Validates the value proposition
4. Maintains project credibility

### 2. No Manual Workarounds

If you're building a tool that automates X, and X fails, you fix the tool - you don't manually do X.

Manual workarounds:
1. Hide bugs that users will encounter
2. Create false confidence that the feature works
3. Waste the user's time when they discover it's broken
4. Defeat the entire purpose of building automation

## Configuration

Define dogfood commands in CLAUDE.md:

```markdown
## Dogfood

Command: `npm run cli -- scan`
Verify: `npm run cli -- list`
```

If no ## Dogfood section exists, ask the user what command to run.

## Blocking Conditions

### After Completing Any Feature/Bugfix

**BLOCKED: DOGFOODING REQUIRED**

You cannot proceed until you:
1. Run the tool's main command
2. Verify it works as expected
3. Document any issues found

### When Tool Fails

**BLOCKED: FIX THE TOOL**

Do NOT proceed with manual workarounds. Stop and fix the actual implementation.

## What Counts as a Workaround

| Building | Workaround (BLOCKED) | Correct Action |
|----------|---------------------|----------------|
| Install command | Manually copying files | Fix the install logic |
| CLI wrapper | Running raw commands | Fix the CLI code |
| File generator | Writing files by hand | Fix the generator |
| API integration | Calling APIs directly | Fix the integration |
| Build script | Running steps manually | Fix the script |
| Migration tool | Editing DB directly | Fix the migration |

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "I'll test later" | Later never comes | Test NOW |
| "Tests are passing" | Tests != real usage | Run the tool |
| "Just a small change" | Small bugs compound | Still dogfood |
| "It's faster manually" | You're building to save time later | Fix the tool |
| "Just this once" | That's what you said last time | Fix the tool |
| "I need to make progress" | Progress = working tool, not workaround | Fix the tool |
| "The tool is mostly working" | "Mostly working" means broken | Fix the tool |
| "I'll fix it later" | Later never comes. Bug is hidden. | Fix the tool NOW |

## Workflow When Tool Fails

1. **STOP** - Do not proceed with manual alternative
2. **DIAGNOSE** - Why did the tool fail?
   - Read error messages
   - Check logs
   - Trace the code path
3. **FIX** - Implement the fix in the tool's code
4. **VERIFY** - Re-run the tool to confirm it works
5. **CONTINUE** - Only proceed after tool succeeds

## Example: Correct vs Wrong

### Wrong (BLOCKED)

```
> skills install svelte-runes from svelte-claude-skills
Error: Skill "svelte5-runes" not found

Let me manually copy the skill files instead...
[copies files directly]
Done! The skill is now installed.
```

### Correct

```
> skills install svelte-runes from svelte-claude-skills
Error: Skill "svelte5-runes" not found

BLOCKED: FIX THE TOOL

The install command failed. Let me investigate:
1. Check curated-sources.ts - skill name is wrong
2. Fix: change 'svelte5-runes' to 'svelte-runes'
3. Rebuild and re-run the install command
4. Verify it works now
```

## Exceptions (Rare)

Manual intervention is acceptable ONLY when:

1. **Debugging the tool itself** - You need to understand what the tool should do
2. **One-time migration** - Explicitly not building automation (user confirmed)
3. **External tool failure** - The failure is in a dependency you can't fix

Even in exceptions, document why manual intervention was necessary.

## Integration with TDD

When dogfood is activated AND you're fixing a bug in the tool:

1. **tdd ALSO APPLIES** - Write regression tests FIRST (RED phase)
2. The fix to the tool MUST be test-driven
3. Do NOT patch code without regression tests

| Situation | Workflow |
|-----------|----------|
| Tool fails, need to fix bug | RED → GREEN → REFACTOR → Verify |
| Tool works, adding feature | Build feature → Run tool → Verify |
| Tool fails, not fixing | BLOCKED (must fix) |

## Quality Check

Before ending work, verify:
- Did I run the tool I modified?
- Did it succeed without manual intervention?
- If it failed, did I fix the tool (not work around it)?
- Did I document any issues?

If any answer is "no": **BLOCKED**