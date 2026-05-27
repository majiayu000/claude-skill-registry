---
name: dk-loop-audit
description: "Audit whether an AI agent can autonomously close the loop on problems in a given area — from discovering a symptom to verifying a fix — without human intervention. Evaluates documentation, diagnostic tools, commands, logs, and flows for completeness and actionability. Generates a gap-focused report with ratings. Use this skill whenever someone wants to assess debugging readiness, check if docs are agent-sufficient, audit a workflow for autonomous solvability, evaluate operational tooling coverage, or wants to know 'could an agent fix this on its own?' Triggers on: 'loop audit', 'audit this flow', 'is this debuggable', 'agent readiness', 'can an agent solve this', 'autonomous debugging check', or /dk-loop-audit."
argument-hint: "[area/flow/doc to audit, e.g. 'odin exec flow' or 'task failure debugging']"
allowed-tools: Bash, Read, Edit, Write, Task, Grep, Glob
---

# /dk-loop-audit — Autonomous Loop-Closing Readiness Audit

You're auditing whether the tooling, docs, commands, and flows in a given area are sufficient for an AI agent to autonomously solve problems — from first symptom to verified fix — without stopping to ask a human.

This is not a documentation quality check. It's an operational readiness assessment. The question isn't "do docs exist?" but "if an agent hit a wall here at 3am, could it get itself unstuck?"

## Target

<audit_target> $ARGUMENTS </audit_target>

If the target is empty or vague, ask the user:
1. What area or flow should be audited? (e.g., "odin task execution", "taskit API debugging", "reflection quality issues")
2. Is there a specific scenario that prompted this? (a recent failure where an agent got stuck is the best input)

If the user provides a doc path, start there but don't stop there — trace outward to the commands, tools, and flows the doc references.

## The Mental Model

An AI agent closing the loop on a problem goes through six stages. A gap at any stage breaks the chain:

```
DISCOVER → DIAGNOSE → HYPOTHESIZE → FIX → VERIFY → DOCUMENT
   ↓          ↓           ↓          ↓       ↓          ↓
 "Something  "The root   "Changing  "Apply  "Confirm   "Record what
  is wrong"   cause is    X should   the     it works   happened and
              Y because   fix it     change  end-to-    why"
              Z"          because W" itself  end"
```

Each stage needs specific resources. The audit checks whether those resources exist, are discoverable, and are actually usable by an agent (not just by a human who knows where to look).

## Process

### Step 1: Scope the audit

Read the target area's CLAUDE.md, AGENTS.md, and any referenced docs. Build a mental map of:
- What problems can occur here? (error types, failure modes, misconfigurations)
- What tools exist for this area? (diagnostic scripts, CLI commands, log files)
- What docs cover this area? (guides, patterns, solutions)

Don't read everything — scan headings and structure first. Depth comes in Step 2 when you know where to look.

### Step 2: Walk the agent journey

For each stage, evaluate from the perspective of an AI agent that has access to the repo's CLAUDE.md files and tools but no prior tribal knowledge. Use parallel subagents to check multiple stages simultaneously.

**DISCOVER — Can the agent detect that something is wrong?**
- Are error messages actionable? (Do they say what failed, or just "error"?)
- Are logs accessible and parseable? (Where are they? What format? Can an agent tail them?)
- Are there health checks or status commands? (Quick "is this working?" checks)
- Is there monitoring that surfaces problems before a human reports them?

**DIAGNOSE — Can the agent find the root cause?**
- Are diagnostic scripts/commands available? (Not just "look at the code")
- Do diagnostic tools explain what they find? (Auto-detected problems, not just raw data)
- Is the data flow traceable? (Can the agent follow data from input to symptom?)
- Are common failure patterns documented with their signatures?

**HYPOTHESIZE — Can the agent form a theory?**
- Do docs explain the WHY behind design decisions? (Not just what the code does)
- Are edge cases and gotchas documented? (The non-obvious things)
- Are there solution docs from past incidents? (Searchable by symptom)
- Is there enough architectural context to reason about side effects?

**FIX — Can the agent make the change?**
- Are modification commands documented? (Not just read-only inspection)
- Are there guard rails? (Tests that catch regressions, linters, type checks)
- Is the change surface well-bounded? (Can the agent know which files to touch?)
- Are there examples of similar past fixes? (Patterns to follow)

**VERIFY — Can the agent confirm the fix works?**
- Are test commands documented and runnable? (Not just "run the tests")
- Is there a live verification path? (Beyond unit tests — can the agent check end-to-end?)
- Are success criteria defined? (How does "working" look, specifically?)
- Can the agent verify without human eyes? (No "check the UI visually" without tooling)

**DOCUMENT — Can the agent record what happened?**
- Is there a documentation workflow? (Where to put learnings, what format)
- Are there templates for incident docs? (Solution docs, RCA reports)
- Is the compounding mechanism discoverable? (Would an agent know to use /dk-compound?)

### Step 3: Rate each stage

For each of the six stages, assign a readiness level:

- **GREEN** — Agent can handle this autonomously. Tools exist, are documented, and are discoverable.
- **YELLOW** — Agent can probably handle this but might waste time or miss things. Partial tooling, unclear docs, or undiscoverable resources.
- **RED** — Agent will get stuck here. Missing tools, no docs, or requires human knowledge that isn't written down.

The rating is about the *weakest realistic scenario*, not the happy path. If the diagnostic script works great for task failures but there's no way to debug harness timeouts, the DIAGNOSE stage is YELLOW (not GREEN just because one path works).

### Step 4: Identify the critical gaps

For each YELLOW and RED stage, identify the specific gaps. A gap is:
- Something an agent would need but can't find
- Something that exists but isn't discoverable (buried in code, not in docs)
- Something that requires human judgment that could be codified
- Something that works for one scenario but not others in the same area

Prioritize gaps by impact: which ones would block the agent most often?

## Output

### Create the report

Write to `docs/loop_audits/<area-slug>-<date>.md`:

```markdown
# Loop Audit: [Area Name]

**Audited**: [date]
**Target**: [what was audited]
**Trigger**: [what prompted this audit, if known]

## Readiness Summary

| Stage | Rating | Key Gap |
|-------|--------|---------|
| Discover | GREEN/YELLOW/RED | [one-line gap or "—"] |
| Diagnose | GREEN/YELLOW/RED | [one-line gap or "—"] |
| Hypothesize | GREEN/YELLOW/RED | [one-line gap or "—"] |
| Fix | GREEN/YELLOW/RED | [one-line gap or "—"] |
| Verify | GREEN/YELLOW/RED | [one-line gap or "—"] |
| Document | GREEN/YELLOW/RED | [one-line gap or "—"] |

**Overall**: [RED/YELLOW/GREEN — the weakest stage determines the overall rating]

## Gaps (ranked by agent-blocking impact)

### GAP-1: [Short title]
**Stage**: [which stage this blocks]
**Impact**: [what happens when an agent hits this — be specific]
**What exists**: [what's already there, briefly]
**What's missing**: [the specific gap]
**Suggested fix**: [concrete action — a doc to write, a script to add, a command to document]
**Effort**: [small/medium/large]

### GAP-2: ...
[repeat for each gap, ranked by impact]

## What Works Well
[2-3 sentences max. Not a list of everything that's fine — just notable strengths that other areas should learn from. Skip this section entirely if nothing stands out.]

## Recommendations
[Ordered list of the top 3-5 actions that would most improve autonomous solvability. Each should be concrete enough to act on without further clarification.]
```

### Report principles

The report is the product. It should be:

- **Gap-focused**: Don't catalog what works. An agent that reads this report should immediately know what's broken and what to do about it. Strengths get at most 2-3 sentences — only if they're worth replicating elsewhere.
- **Specific**: "Docs are insufficient" is not a finding. "There's no way to diagnose harness timeout failures — task_inspect.py shows task metadata but doesn't surface the harness subprocess stderr, which is where timeout errors appear" is a finding.
- **Actionable**: Every gap must have a suggested fix that someone could execute without asking follow-up questions.
- **Honest about severity**: If an area is genuinely well-covered, say so with a GREEN and move on. Don't manufacture gaps to justify the audit. An all-GREEN report with "no significant gaps found" is a valid and useful outcome.

### Print summary

After writing the report, print to conversation:
- The readiness summary table
- The top 3 gaps with their suggested fixes
- The report file path

Don't paste the entire report — the user can read the file.

## Edge Cases

**What if the target is too broad?** (e.g., "audit everything") — Pick the area with the most recent failures or the most complex flow. Audit that deeply rather than auditing everything shallowly. Suggest follow-up audits for other areas.

**What if the target is already well-covered?** — That's a valid finding. Write a short report confirming GREEN across stages, note any minor improvements, and move on. Don't inflate minor issues.

**What if the audit reveals a gap you can fix right now?** — Don't fix it. The audit's job is to produce the report. Fixing gaps is a separate task that the user should prioritize. Mention "this could be fixed now" in the effort field if it's truly trivial.
