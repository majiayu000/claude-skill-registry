---
name: ds-brainstorm
description: "This skill should be used when the user asks to 'start data analysis', 'brainstorm analysis approach', 'plan a data project', 'clarify analysis requirements', or as Phase 1 of the /ds workflow."
---

## Contents

- [The Iron Law of DS Brainstorming](#the-iron-law-of-ds-brainstorming)
- [What Brainstorm Does](#what-brainstorm-does)
- [Critical Questions to Ask](#critical-questions-to-ask)
- [Process](#process)
- [Red Flags - STOP If You're About To](#red-flags---stop-if-youre-about-to)
- [Output](#output)

# Brainstorming (Questions Only)

Refine vague analysis requests into clear objectives through Socratic questioning.
**NO data exploration, NO coding** - just questions and objectives.

<EXTREMELY-IMPORTANT>
## The Iron Law of DS Brainstorming

**ASK QUESTIONS BEFORE ANYTHING ELSE. This is not negotiable.**

Before loading data, before exploring, before proposing approaches, you MUST:
1. Ask clarifying questions using AskUserQuestion
2. Understand what the user actually wants to learn
3. Identify data sources and constraints
4. Define success criteria
5. Only THEN propose analysis approaches

**STOP - You're about to load data or explore before asking questions. Don't do this.**
</EXTREMELY-IMPORTANT>

## What Brainstorm Does

| DO | DON'T |
|-------|----------|
| Ask clarifying questions | Load or explore data |
| Understand analysis objectives | Run queries |
| Identify data sources | Profile data (that's /ds-plan) |
| Define success criteria | Create visualizations |
| Ask about constraints | Write analysis code |
| Check if replicating existing analysis | Propose specific methodology |

**Brainstorm answers: WHAT and WHY**
**Plan answers: HOW (data profile + tasks)** (separate skill)

## Critical Questions to Ask

### Data Source Questions
- What data sources are available?
- Where is the data located (files, database, API)?
- What time period does the data cover?
- How frequently is the data updated?

### Objective Questions
- What question are you trying to answer?
- Who is the audience for this analysis?
- What decisions will be made based on results?
- What would a successful outcome look like?

### Constraint Questions
- **Are you replicating an existing analysis?** (Critical for methodology)
- Are there specific methodologies required?
- What is the timeline for this analysis?
- Are there computational resource constraints?

### Output Questions
- What format should results be in (report, dashboard, model)?
- What visualizations are expected?
- How will results be validated?

## Process

### 1. Ask Questions First

Employ `AskUserQuestion` immediately:
- **One question at a time** - never batch
- **Multiple-choice preferred** - easier to answer
- Focus on: objectives, data sources, constraints, replication requirements

### 2. Identify Replication Requirements

**CRITICAL:** Ask early if replicating existing work:

```
AskUserQuestion:
  question: "Are you replicating or extending existing analysis?"
  options:
    - label: "Replicating existing"
      description: "Must match specific methodology/results"
    - label: "Extending existing"
      description: "Building on prior work with modifications"
    - label: "New analysis"
      description: "Fresh analysis, methodology flexible"
```

When replicating:
- Obtain reference to original (paper, code, report)
- Document exact methodology requirements
- Define acceptable deviation from original results

### 3. Propose Approaches

After objectives are clear:
- Propose **2-3 different approaches** with trade-offs
- **Lead with recommendation** (mark as "Recommended")
- Use `AskUserQuestion` for the user to select the preferred approach

### 4. Write Spec Doc

After selecting an approach:
- Write to `.claude/SPEC.md`
- Include: objectives, data sources, success criteria, constraints
- **NO implementation details** - reserve those for /ds-plan

```markdown
# Spec: [Analysis Name]

> **For Claude:** After writing this spec, use `Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-plan/SKILL.md")` for Phase 2.

## Objective
[What question this analysis answers]

## Data Sources
- [Source 1]: [location, format, time period]
- [Source 2]: [location, format, time period]

## Success Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Constraints
- Replication: [yes/no - if yes, reference source]
- Timeline: [deadline]
- Methodology: [required approaches]

## Chosen Approach
[Description of selected approach]

## Rejected Alternatives
- Option B: [why rejected]
- Option C: [why rejected]
```

## Rationalization Table

| Excuse | Reality | Do Instead |
|--------|---------|------------|
| "I already know what analysis is needed" | You're pattern-matching from similar-sounding requests, not understanding THIS one | Ask questions first |
| "The data will tell me what to do" | Data exploration without objectives is aimless — you'll profile everything and answer nothing | Define objectives first |
| "User seems impatient, skip to analysis" | Wrong results from skipped brainstorm waste more time than 3 questions | Ask the questions |
| "The request is clear enough" | Clear to YOU is not clear to the user — your assumptions ≠ their intent | Confirm with AskUserQuestion |
| "I'll refine objectives as I go" | You'll commit to an approach and rationalize the objective to fit | Lock objectives before exploring |

## Red Flags - STOP If You Catch Yourself Doing This:

| Action | Why It's Wrong | Do Instead |
|--------|----------------|------------|
| Loading data | You're exploring before understanding goals | Ask what the user wants to learn |
| Running describe() | You're profiling data when that's for /ds-plan | Finish defining objectives first |
| Proposing specific models | You're jumping to HOW before clarifying WHAT | Define success criteria first |
| Creating task lists | You're planning before objectives are clear | Complete brainstorm first |
| Skipping replication question | You might miss critical methodology constraints | Always ask about replication upfront |

## Output

Declare brainstorm complete when:
- Analysis objectives clearly understood
- Data sources identified
- Success criteria defined
- Constraints documented (especially replication requirements)
- Approach chosen from alternatives
- `.claude/SPEC.md` written
- User confirms ready for data exploration

## Workflow Context

This skill is Phase 1 of the 5-phase `/ds` workflow:

```
┌──────────────┐    ┌──────────┐    ┌──────────────┐    ┌───────────┐    ┌───────────┐
│ ds-brainstorm│───→│ ds-plan  │───→│ ds-implement │───→│ ds-review │───→│ ds-verify │
│  SPEC.md     │    │ PLAN.md  │    │ LEARNINGS.md │    │ APPROVED? │    │ COMPLETE? │
└──────────────┘    └──────────┘    └──────────────┘    └─────┬─────┘    └─────┬─────┘
                                         ↑                    │                │
                                         └── CHANGES REQ'D ───┘                │
                                         ↑                                     │
                                         └──── NEEDS WORK ────────────────────┘
```

1. **Phase 1: ds-brainstorm** (current) - Clarify objectives through Socratic questioning
2. **Phase 2: ds-plan** - Profile data and break analysis into tasks
3. **Phase 3: ds-implement** - Execute analysis tasks with output-first verification
4. **Phase 4: ds-review** - Review methodology, data quality, and statistical validity (max 3 cycles)
5. **Phase 5: ds-verify** - Check reproducibility and obtain user acceptance

## Phase Complete

After completing brainstorm, IMMEDIATELY invoke the next phase:

```bash
# Invoke Phase 2: Data profiling and task breakdown
/ds-plan
```

Or use the Skill tool directly:

```
Read("${CLAUDE_PLUGIN_ROOT}/lib/skills/ds-plan/SKILL.md")
```

**CRITICAL:** Do not skip to analysis implementation. Phase 2 profiles data and breaks down the analysis into discrete, manageable tasks.
