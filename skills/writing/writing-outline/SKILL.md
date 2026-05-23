---
name: writing-outline
description: Internal skill for creating detailed section outlines. Called by /writing workflow after PRECIS and master OUTLINE are complete.
user-invocable: false
disable-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/writing-suggest-verify.py"
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/writing-claim-id-guard.py"
---

# Writing Outline

Create a detailed outline for a specific section/part before drafting prose. This is Level 3 of the progressive expansion workflow.

## Progressive Expansion Context

```
.planning/PRECIS.md          # Level 1: Thesis, claims, audience
       ↓
.planning/OUTLINE.md         # Level 2: Master structure (sections, goals)
       ↓
outlines/Part I.md         # Level 3: THIS STEP - Detailed section outline
       ↓
drafts/Part I.md           # Level 4: Prose expansion
```

**Never skip to prose drafting without a detailed outline first.**

## Shared Enforcement

Read the constraint index: `${CLAUDE_PLUGIN_ROOT}/references/writing-common-constraints.md`

Then load these phase-specific files:

**Constraints:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progressive-expansion-hierarchy.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/flowchart-authority.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/no-pause-between-phases.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/progress-gating.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/topic-change-protocol.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/drive-aligned-default.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/context-monitoring.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/deviation-rules.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/claim-id-traceability.md`

**Conventions:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/gate-function-standard.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/artifact-review-gates.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/phase-summary-frontmatter.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/checkpoint-type-classification.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/autonomous-phase-chaining.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/iteration-topology.md`

## Outline Flowchart (This IS the Spec)

```
START (PRECIS + master OUTLINE exist)
  │
  ├─ Step 1: Load context (PRECIS, OUTLINE, ACTIVE_WORKFLOW)
  │
  ├─ Step 2: Select section (user choice or next unoutlined)
  │
  ├─ Step 3: Gather structure/depth preferences
  │
  ├─ Step 4: Create detailed outline
  │  └─ For each subsection: POINT + EVIDENCE + LOGIC
  │     Opening → Body (subsections with transitions) → Closing
  │
  ├─ Step 5: Cross-reference with PRECIS claims
  │  └─ Verify: advances claim, within scope, thesis thread
  │
  ├─ Step 6: Update ACTIVE_WORKFLOW.md
  │
  └─ More sections remaining?
     ├─ YES → Loop to Step 2 (NO pause, NO "should I continue?")
     └─ NO → GATE: Every OUTLINE section has outlines/ file?
            ├─ NO → Report missing, loop back
            └─ YES → Outline Review Gate
                     └─ Dispatch writing-outline-reviewer subagent
                        ├─ APPROVED → IMMEDIATELY load writing-draft (no pause)
                        └─ ISSUES_FOUND → fix outlines → re-dispatch (max 5)
```

If text and flowchart disagree, the flowchart wins.

<EXTREMELY-IMPORTANT>
## The Iron Law of Outline Before Prose

**NO PROSE WITHOUT OUTLINE. Never skip to prose drafting without a detailed outline in `outlines/` first. This is not negotiable.**

If you find yourself writing prose without a matching outline file:
1. STOP immediately
2. DELETE the prose
3. Create the outline first
4. THEN draft

Thin outlines produce thin drafts. Each outline must have POINT, EVIDENCE, and LOGIC for every subsection.
</EXTREMELY-IMPORTANT>

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Thin outlines let us get to drafting faster" | The draft has no structure to expand. Every section wanders. You redraft from scratch. Your speed produced chaos and rework. | **Anti-helpful** |
| **Competence** | "I know this topic well enough to skip detail" | Without mapped evidence, the draft section makes unsupported assertions. Without planned transitions, the argument fragments. Your confidence was incompetence. | **Incompetent** |
| **Honesty** | "The outline covers the main points" | You listed topics without POINT, EVIDENCE, or LOGIC. The user drafts from a skeleton — every section is improvised and needs rewriting. | **Anti-helpful** |

## Session Resume Detection

Before starting, check for an existing handoff:

1. Check if `.planning/HANDOFF.md` exists
2. **If found:** Read it and present to user:
   - Show the phase, section in progress, and Next Action
   - Ask: "Resume from handoff, or start fresh?"
   - If resume: skip to the recorded section
   - If fresh: proceed normally
3. **If not found:** Proceed normally

## Process

### Step 1: Load Context

```
Read(".planning/ACTIVE_WORKFLOW.md")
Read(".planning/PRECIS.md")
Read(".planning/OUTLINE.md")
```

If master OUTLINE.md is missing, run writing-brainstorm first.

### Step 2: Select Section

If not specified by user, present available sections:

```
AskUserQuestion(questions=[
  {
    "question": "Which section should I outline in detail?",
    "header": "Section",
    "options": [
      {"label": "Part I / Introduction", "description": "Hook, thesis, roadmap"},
      {"label": "Part II / Background", "description": "Context and precedents"},
      {"label": "Part III / Argument", "description": "Main claims and evidence"},
      {"label": "Part IV / Counterarguments", "description": "Objections and responses"}
    ],
    "multiSelect": false
  }
])
```

### Step 3: Gather Section Details

For the selected section, ask clarifying questions:

```
AskUserQuestion(questions=[
  {
    "question": "How should this section be structured?",
    "header": "Structure",
    "options": [
      {"label": "Chronological", "description": "Events/developments in time order"},
      {"label": "Thematic", "description": "Grouped by topic or concept"},
      {"label": "Problem-Solution", "description": "Issue then resolution"},
      {"label": "Comparative", "description": "Side-by-side analysis"}
    ],
    "multiSelect": false
  },
  {
    "question": "What level of detail do you want?",
    "header": "Depth",
    "options": [
      {"label": "Paragraph-level", "description": "One bullet per paragraph"},
      {"label": "Sentence-level", "description": "Key sentences mapped out"},
      {"label": "Full skeleton", "description": "Nearly complete argument structure"}
    ],
    "multiSelect": false
  }
])
```

### Step 4: Create Detailed Outline

Create directory if needed and write the detailed outline:

```bash
mkdir -p outlines
```

Write to `outlines/[Section Name] (Outline).md`:

```markdown
# [Section Name] - Detailed Outline

## Section Goal
[From master OUTLINE.md - what this section accomplishes]

## Claim Supported
[Which claim from PRECIS.md this section advances]

## Structure: [Chronological/Thematic/Problem-Solution/Comparative]

---

## Opening

**Lead sentence**: [Draft or TBD]
**Context needed**: [What reader must know]
**Transition from previous**: [How we got here]

---

## Body

### Subsection A: [Name]

**Point**: [Main argument of this subsection]
**Evidence**:
  - [Source 1]: "[key quote or fact]"
  - [Source 2]: "[key quote or fact]"
**Logic**: [How evidence supports point]
**Transition**: [Bridge to next subsection]

### Subsection B: [Name]

**Point**: [Main argument]
**Evidence**:
  - [Source]: "[key quote or fact]"
**Logic**: [How evidence supports point]
**Anticipated objection**: [If applicable]
  - Response: [How to address]
**Transition**: [Bridge to next]

### Subsection C: [Name]

[Continue pattern...]

---

## Closing

**Section summary**: [One sentence recap]
**Bridge to next section**: [How this leads to what follows]
**Thesis thread**: [How this connects to main thesis from PRECIS]

---

## Sources Used in This Section
- [Source 1] - used for [what]
- [Source 2] - used for [what]

## Open Questions
- [Anything unresolved before drafting]

## Estimated Length
[Paragraph count or word count target]
```

### Step 5: Cross-Reference with PRECIS

Verify the detailed outline against PRECIS.md:

- [ ] Advances at least one claim from PRECIS
- [ ] Addresses relevant counterarguments (if applicable)
- [ ] Stays within IN scope
- [ ] Avoids OUT scope items
- [ ] Maintains thesis thread

Report any misalignments.

### Step 6: Update Workflow State

Update `.planning/ACTIVE_WORKFLOW.md`:

```yaml
phase: outline
current_section: [section name]
outlines_complete:
  - [list of completed outlines]
```

### Step 7: Continue or Proceed

After completing a section outline, IMMEDIATELY start the next section. Do NOT:
- Ask "should I continue?"
- Summarize what you just outlined
- Wait for confirmation

**Pausing between section outlines is procrastination disguised as courtesy.**

When ALL sections from OUTLINE.md have detailed outlines in `outlines/`, proceed to the draft phase.

---

## Deviation Rules (Outline Phase)

When outlining reveals unplanned issues, follow the deviation rules from `constraints/deviation-rules.md`:

- **R1 (Factual):** Source contradicts a PRECIS claim → auto-fix: note the contradiction, adjust the outline point
- **R2 (Evidence):** No source found for an outline point → auto-fix: flag as evidence gap, search for sources
- **R3 (Structural):** Section doesn't fit the argument flow → auto-fix: reorder subsections
- **R4 (Restructuring):** Entire PRECIS claim needs revision based on outlining → **STOP**, present to user, may require returning to writing-setup

Track deviations per section outline. Each section summary should include: **Deviations:** N auto-fixed (R1: X, R2: Y, R3: Z). **R4 escalations:** [list or "none"].

## Gate: Exit Outline Phase

Before proceeding to draft phase (see `conventions/gate-function-standard.md` for the full 6-step gate including SUMMARY):

1. **IDENTIFY**: What proves outlining is complete?
   - Every section in OUTLINE.md has a corresponding file in `outlines/`
   - Each outline cross-references PRECIS.md claims
2. **RUN**: List files in `outlines/`, compare against sections in OUTLINE.md
3. **READ**: Check each outline has POINT, EVIDENCE, LOGIC for subsections
4. **VERIFY**: All sections have outlines, all outlines reference PRECIS claims
5. **REVIEW**: Dispatch outline reviewer subagent:
   Discover path: `${CLAUDE_PLUGIN_ROOT}/skills/writing-outline-reviewer/SKILL.md`, then `Read()` the output.
   Follow the reviewer skill instructions: dispatch the subagent, handle APPROVED/ISSUES_FOUND, fix and re-review up to 5 times. Only proceed when APPROVED.
6. **CLAIM**: Only if steps 1-5 pass (including reviewer APPROVED), proceed to draft phase

**Skipping the outline verification is NOT HELPFUL — the user drafts from a thin outline and rewrites every section.** You must verify every outline exists and has real structure.

**Proceeding to draft with a thin outline is NOT HELPFUL — every section will wander and require complete redrafting.** The reviewer must confirm depth before drafting begins.

---

## Outline Quality Checklist

Before finalizing each outline, verify:

- [ ] Every subsection has a clear POINT
- [ ] Evidence is specific (quotes, data), not vague ("sources say")
- [ ] Logic connecting evidence to point is explicit
- [ ] Transitions between subsections are planned
- [ ] Section contributes to thesis (not tangential)
- [ ] Anticipated objections are noted where relevant
- [ ] Length estimate is realistic

## Red Flags - STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Creating an outline without reading PRECIS first | Outline won't align with thesis | Read PRECIS.md before every outline |
| Writing a topic list instead of structured outline | Topics ≠ arguments | Add POINT, EVIDENCE, LOGIC for each subsection |
| Skipping the cross-reference with PRECIS | Section may not advance any claim | Check which claim this section serves |
| Stopping after one outline to ask permission | Breaks momentum | Continue to next section immediately |
| Making an outline without sources | Evidence-free outlines produce evidence-free prose | Go back to brainstorm for sources |

## Rationalization Table

| Excuse | Reality | Do Instead |
|---|---|---|
| "The outline is obvious for this structure" | Obvious outlines produce generic papers — the structure should reflect the argument's logic, not a template | Write the outline that THIS argument needs |
| "I'll figure out transitions during drafting" | Transitions ARE the argument's logic; planning them IS the outline's job | Plan every transition now |
| "Three sections is enough" | Check if three is earned by the argument or arbitrary — structure follows claims, not convention | Derive section count from PRECIS claims |
| "I can add supporting points later" | Later means the draft section will be thin and need rewriting — evidence gaps compound | Map evidence to every point now |
| "The PRECIS already covers the structure" | PRECIS is a summary, outline is the blueprint — they serve different purposes | Build the outline as a separate, detailed document |

## Progress Gating

**If 5+ iterations on the same section without meaningful progress, STOP and escalate to the user for scope adjustment.**

Signs you are stuck:
- Rewriting the same subsection structure repeatedly
- Cycling between two structural approaches
- Unable to find evidence for a claimed point after multiple searches
- PRECIS claim doesn't decompose cleanly into this section

When escalating, present:
- What you've tried (briefly)
- Where the section is stuck
- Options: narrow scope, merge with adjacent section, drop the claim, or reframe the argument

**Spinning without progress is anti-helpful.** Recognizing when to ask for guidance is competence, not weakness.

## Common Problems

| Problem | Fix |
|---------|-----|
| Outline is just topic list | Add POINT, EVIDENCE, LOGIC for each |
| No sources mapped | Go back to research or brainstorm |
| Section doesn't advance a claim | Rethink why it exists |
| Too long for one section | Split into multiple sections |
| Transitions missing | Add explicit bridges |

## Next Phase

After all section outlines are complete:

### Outline Review Gate (MANDATORY)

Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-outline-reviewer/SKILL.md` and follow its instructions.

Follow the outline reviewer's instructions:
- If 10+ sections → review in groups of 3-4
- Dispatch reviewer subagent
- If ISSUES_FOUND → fix outlines → re-dispatch (max 5 iterations)
- If APPROVED → proceed to draft phase

**After outline review APPROVED:**

Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-draft/SKILL.md` and follow its instructions.

Then follow its instructions immediately to expand outlines into prose.
