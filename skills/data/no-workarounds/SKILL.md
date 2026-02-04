---
name: no-workarounds
description: |
  Prevents manual workarounds when building tools. Use when: (1) developing CLI tools,
  (2) building automation features, (3) implementing install/deploy commands. Blocks
  progress if Claude manually does what the tool should do instead of fixing the tool.
category: development
---

# No Manual Workarounds

When developing a tool, CLI, or automation feature, you MUST NOT manually work around failures.

## Core Principle

If you're building a tool that automates X, and X fails, you fix the tool - you don't manually do X.

Manual workarounds:
1. Hide bugs that users will encounter
2. Create false confidence that the feature works
3. Waste the user's time when they discover it's broken
4. Defeat the entire purpose of building automation

## Blocking Condition

If the tool/feature you're building doesn't work:

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
| "It's faster to do it manually" | You're building the tool to save time later. Manual = tool is broken. | Fix the tool |
| "Just this once" | That's what you said last time. And the time before. | Fix the tool |
| "I need to make progress" | Progress = working tool, not completed task via workaround | Fix the tool |
| "The tool is mostly working" | "Mostly working" means broken for some cases | Fix the tool |
| "I'll fix it later" | Later never comes. The bug is hidden now. | Fix the tool NOW |
| "The user needs the result" | The user needs a WORKING TOOL, not a one-time result | Fix the tool |
| "It's a minor issue" | Minor issues compound into major broken tools | Fix the tool |
| "It's a one-time migration" | The tool will be used for MANY projects. Build the feature. | Fix the tool |
| "Migration cleanup" | Same as above. If it's a common operation, automate it. | Fix the tool |
| "The plan said to do it manually" | Plans can be wrong. The principle is: automate, don't workaround. | Fix the tool |

## Detection Signals

Watch for these patterns that indicate workaround behavior:

1. **Tool fails, then doing the action manually**
   - `skills install` fails → manually copying SKILL.md
   - Build command fails → running individual commands

2. **Skipping the tool entirely**
   - "Let me just..." followed by manual file operations
   - Using `cp`, `mv`, `curl` when a wrapper exists

3. **Partial tool usage**
   - Using the tool for easy cases, manual for hard ones
   - "The tool doesn't handle this case, so I'll..."

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

## Chained Skills (MUST FOLLOW)

When no-workarounds is activated AND you're fixing a bug in the tool:

1. **tdd ALSO APPLIES** - Write regression tests FIRST (RED phase)
2. The fix to the tool MUST be test-driven
3. Do NOT patch code without regression tests

| Situation | Skills That Apply | Workflow |
|-----------|-------------------|----------|
| Tool fails, need to fix bug | no-workarounds + tdd | RED → GREEN → REFACTOR → Verify |
| Tool works, adding feature | no-workarounds + dogfood-skills | Build feature → Run scan → Verify |
| Tool fails, not fixing | BLOCKED (must fix) | Stop and fix the tool |

**Example of chained workflow:**

```
> skills install svelte-runes from svelte-claude-skills
Error: Skill "svelte5-runes" not found

BLOCKED: FIX THE TOOL (no-workarounds)
BLOCKED: PHASE 1 - RED REQUIRED (tdd)

Chained workflow:
1. Write test that reproduces "skill not found" error
2. Run test, confirm it fails
3. Fix the skill name mapping in curated-sources.ts
4. Run test, confirm it passes
5. Run the actual install command, verify it works
```

## Integration with Other Skills

This skill complements:
- **dogfood-skills**: Use the tools you build
- **tdd**: Write tests before fixing (RED → GREEN → REFACTOR)

Together they enforce: Test → Fix → Use → Verify

## Self-Check

Before completing any tool development task, ask:

1. Did I run the tool I was building?
2. Did it succeed without manual intervention?
3. If it failed, did I fix the tool (not work around it)?

If any answer is "no", you are **BLOCKED: FIX THE TOOL**.
