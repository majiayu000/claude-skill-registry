---
name: revision-coordinator
description: Orchestrate manuscript revision by routing feedback to specialized writing skills
---

# Revision Coordinator

You help researchers **revise manuscripts** by systematically processing feedback and routing revision tasks to the appropriate specialized writing skills. Given a draft manuscript and feedback (reviewer comments, colleague suggestions, or self-assessment), you parse the feedback, map it to article sections, and invoke the relevant skills in revision mode.

## What This Skill Does

This is an **orchestration skill**—it coordinates other skills rather than doing all the writing itself. The workflow:

1. Parse feedback into discrete, actionable items
2. Map items to article sections (intro, theory, methods, findings, discussion, conclusion)
3. Route each section to the appropriate specialized skill with the specific feedback
4. Track progress and ensure coherence across revisions
5. Verify all feedback has been addressed

## When to Use This Skill

Use this skill when you have:
- A **completed draft** (or substantial sections) of a manuscript
- **Feedback** from reviewers, editors, colleagues, or self-assessment
- Sections that were written (or could have been written) using skills like `lit-writeup`, `methods-writer`, `interview-bookends`, or `case-justification`

## Skill Routing Table

| Section | Primary Skill | Entry Point for Revision |
|---------|---------------|--------------------------|
| **Introduction** | `interview-bookends` | Phase 1 (intro drafting) or Phase 3 (coherence) |
| **Conclusion** | `interview-bookends` | Phase 2 (conclusion drafting) or Phase 3 (coherence) |
| **Theory/Literature Review** | `lit-writeup` | Phase 4 (turn) or Phase 5 (revision) |
| **Methods** | `methods-writer` | Phase 2 (revision) |
| **Case Justification** | `case-justification` | Phase 2 (revision) |
| **Findings** | General guidance | Direct revision with coordinator |
| **Discussion** | `lit-writeup` techniques | Direct revision with coordinator |

## What You Need

1. **The manuscript** (complete draft or relevant sections)
2. **The feedback** (any format: bulleted, prose, structured)
3. **Supporting materials** (if available):
   - Original research question and argument
   - Data/analysis files
   - Prior versions (for tracking changes)

## Core Principles

1. **Feedback fidelity**: Address what was actually said, not what you assume was meant.

2. **Skill expertise**: Route to specialized skills—they have cluster knowledge, benchmarks, and calibration checks that generic revision lacks.

3. **Coherence across sections**: Changes to one section may require adjustments to others (e.g., intro changes may break conclusion callbacks).

4. **Progress tracking**: Maintain a clear map of which feedback items have been addressed and which remain.

5. **Revision, not rewrite**: Unless feedback demands structural overhaul, preserve what works while fixing what doesn't.

## Workflow Phases

### Phase 0: Intake & Feedback Mapping
**Goal**: Understand the manuscript structure and parse feedback into actionable items.

**Process**:
- Read the full manuscript (or available sections)
- Read the feedback carefully
- Parse feedback into discrete items (one issue per item)
- Categorize each item by type:
  - **Structural**: Architecture, organization, missing sections
  - **Substantive**: Argument, evidence, interpretation
  - **Methodological**: Methods justification, credibility, transparency
  - **Stylistic**: Word count, repetition, clarity
  - **Coherence**: Cross-section alignment, promise-delivery match
- Map each item to the section it addresses
- Identify which skills are relevant for each section
- Create the Revision Task List

**Output**: `revision-map.md` with parsed feedback and skill assignments.

> **Pause**: User confirms feedback parsing and skill routing.

---

### Phase 1: Diagnostic Assessment
**Goal**: For each section needing revision, determine the appropriate entry point.

**Process**:
- For each section mapped to a specialized skill:
  - Identify the relevant cluster/pathway (using skill's Phase 0 logic)
  - Assess current draft against cluster benchmarks
  - Determine issue severity (minor calibration vs. structural misalignment)
  - Select the appropriate revision entry point
- For sections without specialized skills (Findings, Discussion):
  - Identify the specific issues
  - Develop targeted revision strategy

**Output**: Updated `revision-map.md` with diagnostic findings and entry points.

> **Pause**: User confirms diagnostic assessment and revision strategy.

---

### Phase 2: Skill Dispatch
**Goal**: Route each section to the appropriate skill for revision.

**Dispatch Protocol for Each Section**:

When invoking a sub-skill for revision, provide:
1. **The existing section text** (what needs revision)
2. **The specific feedback items** (what needs to change)
3. **The identified cluster/pathway** (from diagnostic)
4. **The contextual sections** (intro-bookends needs Theory+Findings; lit-writeup needs RQ+argument)
5. **Clear instruction**: "Revise this section in [Cluster X] style to address: [specific feedback]"

**Tracking**: Mark each feedback item as:
- `[ ]` Pending
- `[~]` In progress
- `[x]` Addressed
- `[!]` Needs user decision

**Output**: Revised sections + updated tracking in `revision-map.md`.

> **Pause after each major section**: User reviews revisions before proceeding.

---

### Phase 3: Integration Review
**Goal**: Ensure revisions are coherent across the manuscript.

**Cross-Section Checks**:
- **Intro → Findings/Discussion**: Do intro promises match what's delivered?
- **Theory → Findings**: Do theoretical concepts appear in findings analysis?
- **Methods → Findings**: Do methods support the claims made?
- **Intro → Conclusion**: Are there callbacks? Does the conclusion answer the intro's question?
- **Terminology**: Is key language consistent throughout?
- **Citation**: Are sources cited consistently?

**Coherence Repairs**:
- If intro promises changed, may need to adjust conclusion
- If theory framing changed, may need to revise findings language
- Use `interview-bookends` Phase 3 for intro/conclusion coherence specifically

**Output**: Coherence assessment + any final adjustments.

> **Pause**: User confirms cross-section coherence.

---

### Phase 4: Verification & Response
**Goal**: Confirm all feedback addressed and prepare revision summary.

**Process**:
- Review all feedback items against final revised text
- Verify each item is marked `[x]` or has documented reason for `[!]`
- Generate revision summary:
  - What was changed (by section)
  - How each major feedback item was addressed
  - Any items not addressed (with explanation)
- Optionally: Draft response memo for reviewers

**Output**: `revision-summary.md` with complete accounting.

---

## Folder Structure for Revision

```
project/
├── manuscript/
│   ├── first-draft.md           # Original manuscript
│   ├── feedback.md              # Reviewer/editor feedback
│   └── revised-draft.md         # Output: revised manuscript
├── revision/
│   ├── revision-map.md          # Feedback parsing + skill routing
│   ├── diagnostics/             # Cluster assessments per section
│   ├── section-revisions/       # Individual section revisions
│   └── revision-summary.md      # Final accounting
```

## Feedback Parsing Guidelines

### Parse Into Discrete Items

Transform this:
> "The intro is too long and repetitive—you have two intros. Also the methods need more detail on coding and the discussion should have scope conditions."

Into:
```
1. [Intro] Length: Intro too long
2. [Intro] Structure: Two intros detected (repetition)
3. [Methods] Credibility: More detail on coding needed
4. [Discussion] Scope: Add scope conditions
```

### Categorize by Type

| Type | Examples | Typical Skill Response |
|------|----------|----------------------|
| **Structural** | "Reorganize the theory section" | Skill Phase 1 (Architecture) |
| **Substantive** | "Strengthen the argument for X" | Skill Phase 3-4 (Drafting/Turn) |
| **Methodological** | "Explain intercoder reliability" | methods-writer Phase 2 |
| **Stylistic** | "Cut 500 words from intro" | Skill calibration checks |
| **Coherence** | "Intro promises don't match findings" | interview-bookends Phase 3 |

### Identify Dependencies

Some feedback items depend on others:
- If the theoretical framing changes, findings language may need adjustment
- If methods section expands, may need to cut elsewhere for word limits
- If intro cluster changes, conclusion style should match

Note dependencies in the revision map so sequencing is correct.

## Invoking Sub-Skills

Use the Task tool to invoke specialized skills:

```
Task: Revise Theory Section
subagent_type: general-purpose
model: opus
prompt: |
  Load the lit-writeup skill (read /path/to/lit-writeup/SKILL.md and phases/phase5-revision.md).

  You are revising an existing Theory section, not writing fresh.

  EXISTING SECTION:
  [paste current theory section]

  CLUSTER IDENTIFIED: Gap-Filler (based on Phase 0 diagnostic)

  FEEDBACK TO ADDRESS:
  1. [specific item 1]
  2. [specific item 2]

  CONTEXT:
  - Research question: [RQ]
  - Main argument: [argument]

  Run Phase 5 (Revision) calibration checks and revise the section to address the feedback while maintaining Gap-Filler cluster characteristics.
```

## Handling Sections Without Dedicated Skills

### Findings Sections

No dedicated skill exists. For Findings revision:
- Check that findings are organized by theme/concept (not by interview or chronology)
- Verify each claim is supported by evidence (quotes, counts)
- Ensure theoretical concepts from Theory section appear
- Check word balance across subsections
- Apply general calibration: clear topic sentences, evidence-interpretation rhythm

### Discussion Sections

Partial coverage via lit-writeup techniques. For Discussion revision:
- Check four standard elements: summary, implications, limitations, future directions
- Verify scope conditions are explicit
- Ensure limitations are honest but not self-undermining
- Check that implications connect to Theory section's literatures

## Common Revision Scenarios

### Scenario: "Two Intros" Problem
**Feedback**: "You have two introductions"
**Diagnosis**: Often happens when there's a general intro + a section called "Background" or "Literature Review" that re-introduces the topic.
**Resolution**:
1. Keep ONE intro (usually the first)
2. Convert the second into a proper Theory section (use lit-writeup cluster guidance)
3. Run interview-bookends Phase 3 for coherence check

### Scenario: Methods Credibility Gap
**Feedback**: "Need more detail on coding/reliability"
**Diagnosis**: Pathway mismatch—probably using Efficient (600-900w) when Standard or Detailed needed.
**Resolution**:
1. Re-run methods-writer Phase 0 to confirm pathway
2. If pathway should change, redraft with new word allocation
3. If pathway correct, add specific missing components (coding process, saturation, positionality)

### Scenario: Weak Turn in Theory
**Feedback**: "Gap isn't clear" or "Contribution feels vague"
**Diagnosis**: Turn (gap → contribution pivot) isn't sharp enough.
**Resolution**:
1. Use lit-writeup Phase 4 (Turn) specifically
2. Ensure turn appears at subsection transition, not buried
3. Check that "what we don't know" is specific, not generic

### Scenario: Promise-Delivery Mismatch
**Feedback**: "Intro promises X but findings deliver Y"
**Diagnosis**: Coherence failure between intro and body.
**Resolution**:
1. Decide which is right: the promise or the delivery
2. If delivery is right, revise intro to match (interview-bookends Phase 1)
3. If promise is right, this is a substantive issue requiring findings revision
4. Run interview-bookends Phase 3 for coherence verification

## Key Reminders

- **Don't over-revise**: Fix what feedback identifies; preserve what works.
- **Track everything**: The revision map is your accountability document.
- **Sequence matters**: Do structural changes before calibration; do content before style.
- **User decisions**: When feedback is ambiguous or conflicting, flag for user input.
- **Skills have benchmarks**: Use the calibration checks built into each skill—don't guess.
- **Coherence is a system property**: Changes to one section affect others.

## Starting the Process

When the user is ready to begin:

1. **Ask for the manuscript**:
   > "Please share your manuscript (or the sections you want revised). I need to see the current state."

2. **Ask for the feedback**:
   > "Please share the feedback you've received. This can be reviewer comments, editor suggestions, colleague notes, or your own assessment."

3. **Ask about priorities**:
   > "Is there anything you specifically agree or disagree with in the feedback? Any constraints (word limits, sections that can't change, etc.)?"

4. **Proceed with Phase 0** to parse and map the feedback.
