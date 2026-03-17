---
name: pm-retrospect
description: Challenge PM system assumptions against accumulated evidence. Triages observations and tensions from sprint coordination, detects patterns in team performance and enforcement failures, generates proposals for system improvement. The PM learning loop. Triggers on "/pm-retrospect", "review observations", "what have I learned", "challenge assumptions", "run retrospective".
user-invocable: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, AskUserQuestion
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` and `ops/methodology/` for current system self-knowledge.
Read `ops/config.yaml` for observation/tension thresholds.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

- If empty: run full retrospective (drift check + all phases)
- If "triage": triage pending observations and tensions only
- If "patterns": analyze existing evidence for patterns without triage
- If "drift": run drift check only

**START NOW.**

---

## Philosophy

**The PM system is not sacred. Evidence beats assumptions.**

Every enforcement rule in CLAUDE.md, every methodology in self/methodology.md, every assumption about team performance was a hypothesis. Observations in ops/observations/ capture friction from actual coordination work. Tensions in ops/tensions/ capture unresolved conflicts between decisions or approaches.

/pm-retrospect first triages these individually — some become decision notes, some become methodology updates, some get archived — then compares remaining evidence against what the system assumes.

The QF-8 Phase 3 failure (3 teams deployed without validation blocks) was caught by this loop. The correction (embed validation block at Step 1 of every prompt) was implemented through /pm-retrospect.

---

## Phase 0: Drift Check

Rule Zero: ops/methodology/ is the canonical specification of how PM coordination operates. Before triaging, check whether the system has drifted from what methodology says it should do.

Read all notes in ops/methodology/. For each operational directive:

| Directive | Check |
|-----------|-------|
| "Always use Skill tool for team deployments" | Is this being followed? Any raw Task agent uses documented? |
| "Embed validation block in every agent prompt" | Did recent sprints follow this? |
| "Reject deliverables missing citations" | Were deliverables accepted without validation? |
| "Deploy validation gate after implementation teams" | Was this step followed in recent sprints? |

If drift detected: create a tension note in ops/tensions/ naming the directive vs the observed behavior.

## Phase 1: Triage Observations

Read all notes in ops/observations/ with `status: pending`.

For each observation, decide:

| Decision | When | Action |
|----------|------|--------|
| PROMOTE | Pattern is durable enough to be a decision | Create decision note in decisions/ |
| IMPLEMENT | Observation reveals a process change needed | Update CLAUDE.md or self/methodology.md immediately |
| ARCHIVE | One-off event, not a pattern | Update observation status to "archived" |
| KEEP PENDING | Need more evidence | Leave pending, add context |

**What to promote from PM observations:**

- "Team X consistently misses Y" → team-patterns decision note
- "Validation block was missing from N of N sprints" → enforcement decision note
- "Issue QF-1A recurred after supposed fix" → issue lifecycle decision note

## Phase 2: Triage Tensions

Read all notes in ops/tensions/ with `status: pending`.

For each tension, decide:

| Decision | When | Action |
|----------|------|--------|
| RESOLVE | Clear answer exists | Promote winning decision, update losing decision to superseded |
| DISSOLVE | Both were correct for different contexts | Add scope conditions to both decisions |
| ESCALATE | Human judgment required | Document as open question for next sprint planning |
| KEEP PENDING | More evidence needed | Leave pending |

## Phase 3: Pattern Detection

After triage, analyze remaining evidence and promoted decisions for patterns:

**PM-specific patterns to look for:**

- Do any teams consistently miss the same type of validation?
- Do issues of a certain type keep recurring after supposed fixes?
- Are architectural decisions being made without proper documentation?
- Is there a category of tech facts that keeps being rediscovered?
- Is the health trajectory improving or stalling across sprints?

## Phase 4: Proposals

Generate concrete proposals for system changes based on pattern evidence. Each proposal:
- Names the pattern with evidence (N occurrences across N sprints)
- States the proposed change (specific CLAUDE.md section, methodology update, new template field)
- Requires human approval before implementation

**Output proposals as:**
```
## Proposal: [what to change]

Pattern: [what was observed, N occurrences]
Evidence: [list of observations/tensions/decisions that support this]
Proposed change: [specific text to add/modify/remove]
Expected outcome: [what improves]
Risk: [what could go wrong]

APPROVE? (yes/modify/reject)
```

## Phase 5: Implementation (with approval)

After human approves proposals:
1. Update CLAUDE.md if context file changes needed
2. Update self/methodology.md if coordination methodology changes
3. Create new decision notes if new decisions articulated
4. Update ops/methodology/ with retrospective findings

## Output Format

```
## Retrospective Complete

### Drift Check
- Directives checked: N
- Drift detected: [none / details]

### Observations Triaged
- Promoted: N → decisions/
- Implemented: N → CLAUDE.md/methodology.md updates
- Archived: N
- Kept pending: N

### Tensions Resolved
- Resolved: N
- Dissolved: N
- Escalated: N

### Patterns Detected
[Pattern 1: description with evidence count]
[Pattern 2: ...]

### Proposals
[Pending human approval — see proposals above]
```

---

## Critical Constraints

- NEVER auto-implement proposals. Always present for human approval first.
- Personality never contradicts methodology. Even warm, collegial communication enforces the same quality gates.
- The PM system exists to serve the project, not to be perfected. If retrospective takes more than 20% of coordination time, the PM system has become productivity porn.
