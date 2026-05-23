---
name: notes-processor
description: |
  Process and organize notes.md using the LNO (Leverage/Neutral/Overhead) framework for systematic task prioritization.
  Use when: (1) adding action items to notes.md, (2) organizing daily tasks, (3) categorizing work by ROI potential,
  (4) carrying forward incomplete tasks to new date sections, (5) routing initiative-specific notes,
  (6) user requests "update notes" or "process my notes", or (7) synchronizing action items from CLAUDE.md files to daily tracking.
  Applies Shreyas Doshi's ROI-based prioritization framework to maintain strategic focus in daily execution.
allowed-tools: [Read, Edit, Write]
---

# Notes Processor Skill

**Version**: 1.0.0
**Last Updated**: January 27, 2026

## Purpose

Systematically organize daily notes using the LNO framework to maintain strategic focus and ensure high-leverage work gets appropriate priority. This skill transforms ad-hoc note-taking into a strategic prioritization system that surfaces ROI-based work categorization.

## Invocation

**Trigger phrases**:
- "add action items to notes.md"
- "update my notes"
- "process notes"
- "categorize these tasks"
- "organize my daily tasks"
- "sync action items from [initiative]"

**Usage**:
```
Invoked by agents (initiative-tracker, meeting-notes-router) or directly when user requests notes organization
```

## Framework: LNO Prioritization

### Core Philosophy

**The Problem**: Not all work is equal. PMs often treat all tasks as equally important, leading to strategic work being crowded out by tactical firefighting.

**The Solution**: Shreyas Doshi's LNO framework categorizes work by ROI potential:

- **🟢 Leverage (L)**: 10x-100x ROI potential
  - Strategic initiatives, experiments, research
  - Documentation systems, templates, automation
  - Work that compounds over time
  - *Example*: "Design experiment to test new onboarding flow"

- **🟡 Neutral (N)**: 1x ROI (equal effort to return)
  - Regular meetings, standard project work
  - Planning, coordination, reviews
  - Necessary but not amplifying
  - *Example*: "Weekly sync with engineering team"

- **🔴 Overhead (O)**: <1x ROI (necessary but low return)
  - Administrative work, required responses
  - Urgent fixes, firefighting
  - Work that must be done but doesn't move strategic goals
  - *Example*: "Respond to expense report request"

### Why This Matters

**Customer Value**: By surfacing high-leverage work, PMs spend more time on initiatives that compound customer value rather than reacting to daily noise.

**Trade-off**: Requires discipline to categorize honestly. Accepting that not all work is strategic enables better resource allocation.

**Outcome**: Over time, ratio of L:N:O work shifts toward leverage, driving disproportionate impact.

## Execution Protocol

### Phase 1: UNDERSTAND - Read Current State

**CRITICAL**: Always read notes.md before modifying.

1. Read `notes.md` to understand current structure
2. Identify current date section (format: `# Jan 27:` or `# Jan 27 (Completed):`)
3. Check for:
   - Unformatted content at top of file
   - Processing Queue items
   - Incomplete tasks in previous date sections
   - Tasks missing LNO categorization

### Phase 2: CATEGORIZE - Apply LNO Framework

For each task or note item:

**Step 1: Identify Task Type**
- Action item with clear deliverable?
- Meeting/coordination?
- Administrative/reactive work?
- Strategic/experimental work?

**Step 2: Assess ROI Potential**
Ask: "If I complete this, what's the multiplier effect?"
- >10x return? → Leverage
- ~1x return? → Neutral
- <1x return but necessary? → Overhead

**Step 3: Apply Classification**
Use keyword hints to guide categorization:

**Leverage indicators**: "strategic", "experiment", "optimize", "automate", "research", "design", "framework", "template"
**Neutral indicators**: "meeting", "sync", "update", "coordinate", "plan", "review"
**Overhead indicators**: "respond", "urgent", "required", "send message", "fix bug", "admin"

**Step 4: Validate Against Framework**
- Am I being honest about ROI or inflating importance?
- Would Shreyas Doshi agree with this categorization?
- Does this serve strategic outcomes or just feel busy?

### Phase 3: STRUCTURE - Organize in notes.md

**Current Date Section Format**:
```markdown
# Jan 27:

## 🟢 Leverage (L)
- [ ] **[L]** High-leverage task description *(Created: Jan 20)*

## 🟡 Neutral (N)
- [ ] **[N]** Standard task description *(Created: Jan 27)*

## 🔴 Overhead (O)
- [ ] **[O]** Administrative task description *(Created: Jan 27)*
```

**Task Format Rules**:
- Checkbox states:
  - `[ ]` for incomplete (not started)
  - `[>]` for in progress
  - `[~]` for blocked/waiting
  - `[-]` for cancelled/no longer needed
  - `[X]` or `[x]` for completed
- Label: `**[L]**`, `**[N]**`, or `**[O]**`
- Creation date: `*(Created: [date])*` in abbreviated format (e.g., "Jan 27")
- Completion date (when finished): `*(Completed: [date])*`
- Cancellation date (when cancelled): `*(Cancelled: [date])*` with brief reason

### Phase 4: DATE TRANSITIONS - Carry Forward Logic

**When creating new date section:**

**CRITICAL RULE**: Only carry forward active incomplete tasks `[ ]` and blocked tasks `[~]`. Never carry forward completed `[X]`, cancelled `[-]`, or in-progress `[>]` tasks from previous days.

**Carryforward Protocol**:
```
For each task in previous date section:
  IF checkbox is [ ] (not started):
    IF has *(Created: [date])*:
      → Preserve *(Created: [date])* exactly as is
    ELSE:
      → Add *(Created: [previous-date])*
    → Copy to new date section
  ELSE IF checkbox is [~] (blocked/waiting):
    → Carry forward (still active, waiting on external factors)
    → Preserve creation date
  ELSE IF checkbox is [X] or [x] (completed):
    → Skip (done successfully, leave in original date section)
  ELSE IF checkbox is [-] (cancelled/no longer needed):
    → Skip (done by cancellation, leave in original date section)
  ELSE IF checkbox is [>] (in progress from yesterday):
    → Reset to [ ] and carry forward (new day, new start)
    → Preserve creation date
```

**Why This Matters**: Preserving creation dates shows task age, helping identify:
- Tasks lingering too long (need to be broken down or escalated)
- Patterns of what gets delayed
- True cycle time for work

**Mark Previous Section Complete**:
```markdown
# Jan 26 (Completed):
```

### Phase 5: ROUTE - Initiative-Specific Content

**When notes reference specific initiatives**, route to initiative CLAUDE.md:

**Detection Keywords** (examples, dynamically discover actual initiatives):

**Routing Protocol**:
1. Identify initiative-specific content (meetings, decisions, insights)
2. Extract relevant notes
3. Append to initiative's RunningNotes.md with date header
4. Log routing in notes.md "✅ Processed Notes" section

**Why Route**: Initiatives need context persistence. Daily notes are ephemeral; initiative files are durable memory.

### Phase 6: COMPLETION & CANCELLATION TRACKING

**When task changes from incomplete to complete**:
1. Change checkbox: `[ ]` → `[X]`
2. Add completion timestamp: `*(Completed: Jan 27)*`
3. Leave task in original date section (do NOT move)

**Format**:
```markdown
- [X] **[L]** Completed task description *(Created: Jan 20)* *(Completed: Jan 27)*
```

**When task becomes cancelled/no longer needed**:
1. Change checkbox: `[ ]` → `[-]`
2. Add cancellation timestamp: `*(Cancelled: Jan 27)*`
3. Add brief reason inline or as sub-bullet
4. Leave task in original date section (do NOT move)

**Format**:
```markdown
- [-] **[L]** Cancelled task description *(Created: Jan 20)* *(Cancelled: Jan 27)*
  - Reason: Superseded by new unified approach
```

**Why Track Cancellations**:
- Documents strategic pivots and evolution of thinking
- Shows what was considered but not pursued (learning)
- Explains why effort wasn't invested (useful for retrospectives)
- Transparency about changing priorities

**Cancelled tasks behave like completed tasks**: They stay in their original date section and do NOT carry forward to future dates.

### Phase 7: METADATA UPDATE

Update "Last Updated" timestamp at bottom of notes.md:
```markdown
---
**Last Updated**: 2026-01-27 14:30
```

## Integration with Initiative Tracker

When invoked by initiative-tracker or meeting-notes-router:

**Input**: List of action items with context
```
Action Items:
- [Owner: Khushal] Follow up with design team on wireframes
- [Owner: Khushal] Draft experiment brief for onboarding test
- Context: From meeting about FCC Beta launch
```

**Processing**:
1. Categorize each using LNO framework
2. Add to current date section in notes.md
3. Preserve context (note source/meeting if relevant)
4. Apply proper formatting with creation date

**Output**: Confirmation of items added with LNO classification

## Quality Gates

Before completing any notes processing:

- [ ] **Read First**: Did I read current notes.md state before modifying?
- [ ] **LNO Categorization**: Are all tasks properly categorized by ROI potential?
- [ ] **Honest Assessment**: Am I being truthful about leverage vs inflating importance?
- [ ] **Carryforward Accuracy**: Did I ONLY carry forward incomplete tasks?
- [ ] **Creation Dates Preserved**: Are original creation dates maintained on carried-forward tasks?
- [ ] **Completion Timestamps**: Are completion dates added to all finished tasks?
- [ ] **Initiative Routing**: Did I route initiative-specific content appropriately?
- [ ] **Metadata Updated**: Is the "Last Updated" timestamp current?
- [ ] **Strategic Alignment**: Does this organization serve the user's strategic priorities?

## Integration with Shannon

This skill embodies Shannon's core philosophy:

### Framework-Driven Thinking
- LNO framework provides systematic approach to prioritization
- Every task categorization is a trade-off decision
- Framework reveals patterns: too much overhead? Need more leverage work.

### Shreyas Doshi Quality Standards
- **Customer-centric logic**: Leverage work directly serves customer value creation
- **Explicit trade-offs**: Accepting honest categorization over optimistic inflation
- **Outcome-focused**: LNO ratio shifts toward leverage drive real impact
- **Framework application**: Every task gets systematic ROI assessment

### Quality Standards Reference
See `.claude/reference/quality-framework.md` for full Shannon quality gates.

### First Principles
- Not all work is equal (fundamental truth)
- Time is finite resource requiring allocation strategy
- Strategic work gets crowded out without explicit prioritization
- Honest categorization enables better resource allocation

## Success Criteria

This skill succeeds when:

1. ✅ All tasks in notes.md have clear LNO categorization
2. ✅ Categorization reflects honest ROI assessment, not wishful thinking
3. ✅ Date transitions preserve task history (creation dates maintained)
4. ✅ Completed tasks stay in original date sections with completion timestamps
5. ✅ Initiative-specific content routed to appropriate CLAUDE.md files
6. ✅ User can scan notes.md and immediately see leverage vs overhead ratio
7. ✅ Over time, user's work shifts toward more leverage activities
8. ✅ Strategic work is visible and not buried in tactical noise

## Anti-Patterns to Avoid

❌ **False Leverage**: Categorizing everything as [L] to feel productive
- *Reality check*: Most work is Neutral or Overhead. True Leverage is rare.

❌ **Category Inflation**: "This meeting is strategic" when it's coordination
- *Fix*: Be brutally honest. Coordination = Neutral, even if important.

❌ **Carrying Forward Completed/Cancelled Tasks**: Pollutes new date sections
- *Fix*: Completed `[X]` and cancelled `[-]` tasks stay in their original date forever.
- Both represent "done" - just in different ways (success vs obsolescence)

❌ **Losing Task History**: Updating creation dates when carrying forward
- *Fix*: Preserve original `*(Created: [date])*` to track task age.

❌ **Skipping Categorization**: Adding tasks without LNO labels
- *Fix*: Every task gets a category. No exceptions.

❌ **Processing Without Reading**: Modifying notes.md without understanding current state
- *Fix*: Always read first. Context matters.

## Reference Materials

For detailed implementation rules, see:
- **LNO Framework Deep Dive**: `.claude/reference/lno-framework.md` (if exists)
- **Notes Structure Rules**: Original notes-processor agent for granular formatting rules
- **Quality Framework**: `.claude/reference/quality-framework.md`

## Error Handling

### Missing Date Section
If current date section doesn't exist:
- Create it with proper LNO structure
- Carry forward incomplete tasks from previous date
- Mark previous section as "(Completed)"

### Ambiguous Categorization
If task ROI is unclear:
- Default to Neutral [N]
- Add note: "*(Category uncertain - review)*"
- User can recategorize later

### Initiative Routing Uncertainty
If initiative mentioned but no matching folder found:
- List discovered initiatives
- Ask user which to route to, or skip routing

### Invalid Task Format
If existing task lacks proper format:
- Apply format corrections
- Preserve task content
- Add missing elements (creation date, LNO label)

## Continuous Improvement

**Over time, this skill enables**:
- Pattern recognition: Am I drowning in overhead?
- Strategic shifts: Consciously increase leverage work percentage
- Honest assessment: Seeing true work composition
- Prioritization: When overloaded, drop overhead first, protect leverage

**This is the point**: Notes organization isn't admin work. It's strategic resource allocation made visible.
