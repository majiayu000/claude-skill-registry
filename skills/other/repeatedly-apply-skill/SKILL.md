---
name: repeatedly-apply-skill
user-invocable: false
skill_api_version: 1
hexagonal_role: supporting
metadata:
  tier: execution
description: "Use when applying a skill repeatedly with progressive deepening for iterative improvement."
practices:
- pragmatic-programmer
---
# Repeatedly Apply Skill

Orchestrate N passes of any skill against a target. Each pass is delegated
to a fresh subagent with a unique mission derived from the skill itself.

## Architecture: Orchestrator + Subagents

**You are the ORCHESTRATOR.** You do NOT apply the skill yourself.
You delegate each pass to a subagent via the `Agent` tool. This solves:

- **Laziness**: Each subagent is fresh — no accumulated fatigue
- **Context**: Each subagent gets full context window for its one mission
- **Verification**: YOU verify the subagent's work after each pass
- **Compaction**: The progress file tells you where to resume

## Step 0: Plan the Missions

**Before pass 1**, read the target skill's SKILL.md (or understand the
slash command's purpose). Then generate N missions that are specific to
THAT skill. Do not use generic missions.

**Example for `ui-polish`:**
1. Layout hierarchy and spacing  2. Color palette and contrast
3. Typography scale and weight  4. Interactive states (hover, focus, active, disabled)
5. Micro-animations and transitions  6. Empty/loading/error states
7. Responsive breakpoints  8. Dark mode consistency
9. Visual rhythm and alignment  10. Final screenshot comparison

**Example for `ubs` (bug scanner):**
1. Null/undefined paths  2. Error handling gaps
3. Race conditions and async  4. Input validation boundaries
5. Security (injection, auth)  6. Resource leaks (connections, listeners)
7. Type safety holes  8. Logic errors
9. Edge cases (empty, max, negative)  10. Cross-cutting concerns

**Example for `tui-glamorous`:**
1. Layout structure and flex  2. Color scheme and theming
3. Keyboard navigation  4. Focus management and state machines
5. Dynamic content rendering  6. Responsive terminal sizing
7. Animation and transitions  8. Accessibility (screen readers)
9. Performance under load  10. Visual polish and sparklines

**The missions MUST come from the skill's domain, not from a generic
template.** Read the skill, understand its concerns, then subdivide
those concerns into N passes.

## Step 0b: Create the Progress File

Write `.skill-loop-progress.md` in the project root (NOT /tmp/):

```markdown
# Skill Loop Progress
# Skill: [name]
# Target: [path]
# Total Passes: [N]
# Started: [ISO timestamp]

## Status: IN PROGRESS — Pass 1 of N

## Missions
1. [Mission 1 name]: [one-line description]
2. [Mission 2 name]: [one-line description]
...
N. [Mission N name]: [one-line description]

## Completed Passes
(none yet)
```

**This file is the SINGLE SOURCE OF TRUTH.** After compaction, read it
first. It contains everything needed to resume.

## Step 1-N: The Delegation Loop

**CRITICAL: Passes are STRICTLY SERIAL.** Each pass MUST complete and be
verified before the next one starts. NEVER launch multiple passes in
parallel — each pass builds on the previous one's changes. If you launch
pass 3 before pass 2's changes are committed, pass 3 will operate on
stale code and produce wrong or conflicting results. One subagent at a
time. Wait for it to return. Verify. Commit. Then launch the next.

For each pass K from 1 to N:

### 1. Launch a Subagent (ONE at a time — wait for completion)

Use the `Agent` tool. The prompt MUST include:
- The skill name or slash command to apply
- The mission name and focus for this pass
- The target files/directory
- What was already done in prior passes (so it doesn't repeat)

```
Agent prompt template:

Apply the skill [SKILL_NAME] to [TARGET].

MISSION for this pass: [Mission K name] — [description].
Focus EXCLUSIVELY on [mission focus]. Do not fix issues outside
this mission's scope — other passes will handle those.

Prior passes already addressed:
[list of completed mission names and key changes]

After making changes, report:
1. What files you changed and why
2. What issues you found in this mission's scope
3. What you checked but found already correct
```

### 2. Verify the Subagent's Work

After the subagent returns, YOU (the orchestrator) verify:

```bash
git diff --stat
```

Check that:
- Changes exist (the subagent actually did work)
- Changes are in the target files (not random other files)
- Changes align with the mission focus (not off-topic)

**If the subagent claims "nothing found" but you suspect laziness:**
Re-launch with a more specific prompt targeting 2-3 concrete things
within the mission's scope. One retry is allowed per pass.

### 3. Commit the Pass

```bash
git add [target-files] && git commit -m "skill-loop pass K/N: [mission name]"
```

Committing after each pass enables easy rollback and provides proof.

### 4. Update the Progress File

Append to `.skill-loop-progress.md`:

```markdown
### Pass K — [Mission Name] — [timestamp]
- Files changed: [list]
- Changes: [brief summary from subagent report]
- Commit: [short hash]
- Verdict: PRODUCTIVE / ZERO-CHANGE / RETRY-NEEDED
```

Update the status line: `## Status: IN PROGRESS — Pass K+1 of N`

### 5. Check Stop Conditions

| Condition | Required Evidence | Action |
|-----------|------------------|--------|
| Two consecutive ZERO-CHANGE passes | Two git diffs with no changes | Stop — convergence |
| Thrashing | Same lines flipping back and forth | Stop — conflicting criteria |
| Pass cap reached | K == N | Stop — complete |
| User-specified quality target met | Tests pass, lint clean, etc. | Stop — goal reached |

No other stop conditions are valid. Proceed to pass K+1.

## Compaction Recovery Protocol

If context compacts mid-loop:

1. Read `.skill-loop-progress.md` from the project root
2. Note which pass you're on (the Status line)
3. Note completed missions (don't repeat them)
4. Resume from the next uncompleted pass
5. Continue the delegation loop as normal

## Anti-Laziness Rules

1. **The orchestrator does NOT apply the skill.** Delegate to subagents.
   This prevents laziness accumulation across passes.

2. **Each subagent gets ONE mission.** Do not batch multiple missions
   into one subagent — each gets a focused, achievable task.

3. **STRICTLY SERIAL execution.** NEVER launch multiple subagents in
   parallel. Each pass changes the code; the next pass must see those
   changes. Launch one → wait → verify → commit → then launch the next.

4. **No hollow passes.** If a subagent reports "nothing found," its
   report must name 3+ specific things it checked and why they were
   correct. Otherwise, retry with a more targeted prompt.

5. **Later passes are MORE valuable.** The user already knows pass 1
   finds obvious things. They're requesting 10 passes because passes
   5-10 find what passes 1-4 miss. Treat later missions with MORE
   scrutiny, not less.

6. **The progress file is authoritative.** If it says you're on pass 6,
   you're on pass 6. Don't re-derive state from memory.

## Summary Report (After Loop Completes)

```
## Improvement Loop: [skill] × [K passes]

| Pass | Mission | Files | Key Changes | Commit |
|------|---------|-------|-------------|--------|
| 1 | [name] | 4 | [summary] | abc123 |
| 2 | [name] | 3 | [summary] | def456 |
| ... | ... | ... | ... | ... |

Stopped at pass K/N: [reason + evidence]
Total files modified: N | Total commits: N
```

## Fallback: No Subagents Available

If Agent tool is unavailable, apply the skill yourself but:
- Still create the progress file
- Still follow one-mission-per-pass (shift your analytical lens)
- Still run `git diff --stat` after every pass
- Still commit after every pass
- If you catch yourself rushing later passes, STOP and re-read
  the current mission's focus description before continuing

## Skills That Loop Well

`ui-polish`, `simplify`, `ubs`, `tui-glamorous`,
`react-best-practices`, `ux-audit`, `interactive-visualization-creator`,
`de-slopify`, `multi-pass-bug-hunting`, `codebase-audit`
