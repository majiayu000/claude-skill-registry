---
name: post-mortem
description: 'Comprehensive post-implementation validation. Combines retro (learnings), vibe (code validation), security scanning (Talos), and knowledge extraction into a single unified workflow. Triggers: "post-mortem", "validate completion", "final check", "wrap up epic", "close out", "what did we learn".'
---

# Post-Mortem Skill

> **Quick Ref:** Full validation + knowledge extraction. Output: `.agents/retros/*.md` + `.agents/learnings/*.md` + Gate 4 decision.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Validate, learn, and feed knowledge back into the flywheel.

## Execution Steps

Given `/post-mortem [epic-id]`:

### Step 1: Identify What Was Completed

**If epic ID provided:** Use it directly.

**If no epic ID:** Find recently completed work:
```bash
bd list --status closed --since "7 days ago" 2>/dev/null | head -5
```

Or check recent git activity:
```bash
git log --oneline --since="24 hours ago" | head -10
```

### Step 1a: Pre-flight Check - Work Exists

**Verify there is work to post-mortem:**

```bash
# Count recent commits
git log --oneline --since="7 days ago" 2>/dev/null | wc -l
```

**If 0 commits found and no epic ID provided:**
```
STOP and return error:
  "No work found to post-mortem. Either:
   - Provide epic ID: /post-mortem <epic-id>
   - Or complete some work first"
```

Do NOT run post-mortem on empty work - this produces misleading "all clear" reports.

### Step 2: Run Code Validation (Inline - No Nesting)

**Read changed files and validate directly:**

```bash
# Get recent changes
git diff --name-only HEAD~5 2>/dev/null | head -20
```

Read each changed file with the Read tool, then apply the 8 vibe aspects:
1. Semantic - code matches docs?
2. Security - vulnerabilities?
3. Quality - dead code, smells?
4. Architecture - layer violations?
5. Complexity - too complex?
6. Performance - issues?
7. Slop - AI hallucinations?
8. Accessibility - issues?

Record findings with file:line citations.

### Step 2a: Early Exit on CRITICAL

**If inline validation found CRITICAL issues:**

```
STOP IMMEDIATELY. Do NOT dispatch the swarm.

Report to user:
  "CRITICAL issues found in inline validation. Fix before continuing post-mortem."

  Findings:
  - <file:line> - <critical issue>

  Action: Fix these issues, then re-run /post-mortem
```

**CRITICAL issues block Gate 4.** There's no point running a 6-agent swarm to extract learnings from broken code.

### Step 3: Dispatch Post-Mortem Validation Swarm

**Launch ALL SIX agents in parallel (single message, 6 Task tool calls):**

```
Tool: Task (ALL 6 IN PARALLEL)
Parameters:
  subagent_type: "agentops:plan-compliance-expert"
  model: "haiku"
  description: "Plan compliance check"
  prompt: |
    Compare implementation to original plan for: <epic-id>

    Files: .agents/plans/*.md, recent git commits

    Check: Did we build what we said we'd build?
    Return: Deviation percentage and missed items.

Tool: Task
Parameters:
  subagent_type: "agentops:goal-achievement-expert"
  model: "haiku"
  description: "Goal achievement check"
  prompt: |
    Validate user problem was solved for: <epic-id>

    Check: Beyond plan compliance - did we actually solve the problem?
    Return: Goal achievement assessment and value delivered.

Tool: Task
Parameters:
  subagent_type: "agentops:ratchet-validator"
  model: "haiku"
  description: "Ratchet chain validation"
  prompt: |
    Verify ratchet gates are locked for: <epic-id>

    Check all gates: Research → Pre-mortem → Plan → Implement → Vibe
    Return: Gate status and any regression risks.

Tool: Task
Parameters:
  subagent_type: "agentops:flywheel-feeder"
  model: "haiku"
  description: "Knowledge extraction (learnings + provenance)"
  prompt: |
    Extract ALL learnings from this completed work with full provenance.

    Files: .agents/research/*.md, .agents/plans/*.md, .agents/vibe/*.md, git log
    Session ID: <current-session-id>

    Extract:
    - Technical patterns worth repeating
    - Anti-patterns to avoid
    - Process improvements
    - Decisions and rationale
    - Gotchas and edge cases

    Return structured learnings with:
    - ID (L1, L2...)
    - Category (technical, process, architecture)
    - Confidence (high, medium, low)
    - Source file:line citation

Tool: Task
Parameters:
  subagent_type: "agentops:security-expert"
  model: "haiku"
  description: "Security validation"
  prompt: |
    Security review of completed work for: <epic-id>

    Review recent commits for:
    - Hardcoded secrets
    - SQL injection
    - XSS vulnerabilities
    - Auth/authz issues
    - OWASP Top 10

    Return findings with severity and file:line.

Tool: Task
Parameters:
  subagent_type: "agentops:code-quality-expert"
  model: "haiku"
  description: "Code quality check"
  prompt: |
    Code quality review for: <epic-id>

    Check: Complexity, maintainability, test coverage, documentation.
    Return: Quality assessment with specific issues.
```

**Timeout:** 3 minutes per agent. If <80% return, report INCOMPLETE and do NOT proceed to synthesis.

### Step 3a: Apply Conflict Resolution

**Wait for agents, then synthesize:**
1. Check quorum (80% must return = 5/6 minimum)
2. Apply severity escalation (if ANY agent reports CRITICAL → final is CRITICAL)
3. Deduplicate findings by file:line (±5 lines tolerance)
4. Compute weighted grade per `.agents/specs/conflict-resolution-algorithm.md` Step 4
5. Track agreement per finding (e.g., "3/6 agents found this")

**Grade Computation:**
```
WEIGHTS = {CRITICAL: 10, HIGH: 5, MEDIUM: 2, LOW: 1}
total_weight = sum(WEIGHTS[f.severity] for f in findings)

Grade A: 0 critical, weight 0-5
Grade B: 0 critical, weight 6-15
Grade C: 0 critical, weight 16-30
Grade D: 1+ critical OR weight 31+
Grade F: Multiple critical, weight 50+
```

**If quorum not met:** Report as INCOMPLETE, do NOT proceed to Gate 4.

### Step 4: Request Human Approval (Gate 4)

**USE AskUserQuestion tool - The Key Decision:**

```
Tool: AskUserQuestion
Parameters:
  questions:
    - question: "Post-mortem complete. Grade: <grade>. Is this output good enough to TEMPER?"
      header: "Gate 4"
      options:
        - label: "TEMPER & STORE"
          description: "Output is good - lock learnings and index for future"
        - label: "ITERATE"
          description: "Not satisfied - back to the forge for another round"
      multiSelect: false
```

**If ITERATE:** Return control to user for another round of research/plan/implement.

**If TEMPER & STORE:** Proceed to index the knowledge.

### Step 5: Index Knowledge (if ao available)

```bash
# Forge learnings from this session
ao forge transcript 2>/dev/null

# Index all artifacts for future discovery
ao pool add .agents/research/*.md .agents/learnings/*.md .agents/patterns/*.md 2>/dev/null

# Mark artifacts as TEMPERED (validated, locked)
ao ratchet lock .agents/retros/YYYY-MM-DD-post-mortem-*.md 2>/dev/null
```

If ao CLI not available, knowledge is still captured in `.agents/` files for manual discovery.

### Step 6: Write Post-Mortem Report

**Write to:** `.agents/retros/YYYY-MM-DD-post-mortem-<topic>.md`

```markdown
# Post-Mortem: <Topic/Epic>

**Date:** YYYY-MM-DD
**Epic:** <epic-id or description>
**Duration:** <how long the work took>

## Summary
<What was built and outcome>

## Vibe Results
**Grade:** <overall grade from vibe>
**Findings:**
- CRITICAL: <count>
- HIGH: <count>
- MEDIUM: <count>

<Key issues if any>

## What Went Well
- <thing 1>
- <thing 2>

## What Could Be Improved
- <improvement 1>
- <improvement 2>

## Learnings Extracted
<Link to learnings created by /retro>

## Follow-up Issues
<Any issues created from vibe findings>

## Recommendations for Next Time
- <recommendation 1>
- <recommendation 2>
```

### Step 7: Create Follow-up Issues (if needed)

If vibe found HIGH or MEDIUM issues that weren't fixed:
```bash
bd create --title "Address <finding>" --body "<details>" --label "tech-debt"
```

### Step 8: Report to User

Tell the user:
1. Post-mortem report location
2. Vibe grade and key findings
3. Learnings extracted
4. Follow-up issues created (if any)
5. Gate 4 decision (TEMPERED or ITERATE)
6. The knowledge has been indexed for future sessions (if TEMPERED)

## The Flywheel Effect

Post-mortem closes the knowledge loop:

```
Implementation → POST-MORTEM → Knowledge → Next Research
                    │
                    ├── .agents/retros/     (locked)
                    ├── .agents/learnings/  (locked)
                    └── ao forge index      (searchable)
```

Future `/research` calls will find this knowledge automatically.

## Key Rules

- **Always run vibe** - validate the code quality
- **Always run retro** - extract learnings
- **Fix CRITICAL issues** - don't close with critical problems
- **Index knowledge** - make it discoverable
- **Write the report** - always produce `.agents/retros/` artifact

## Without ao CLI

If ao CLI not available:
1. Skip the indexing step
2. Knowledge is still captured in `.agents/` files
3. Future sessions find it via file search
