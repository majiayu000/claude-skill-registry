---
name: writing-setup
description: Internal skill for creating PRECIS.md, OUTLINE.md, and ACTIVE_WORKFLOW.md. Called after brainstorm sources are gathered.
user-invocable: false
disable-model-invocation: true
hooks:
  PostToolUse:
    - matcher: "Write"
      hooks:
        - type: command
          command: "python3 ${CLAUDE_PLUGIN_ROOT}/hooks/writing-precis-guard.py"
---

# Writing Setup

Create the project foundation: PRECIS.md (thesis, audience, claims), OUTLINE.md (document structure), and ACTIVE_WORKFLOW.md (state tracking).

**Prerequisites:** Brainstorm complete. User has confirmed topic, angle, and audience.

## Session Resume Detection

Before starting, check for an existing handoff:

1. Check if `.planning/HANDOFF.md` exists
2. **If found:** Read it and present to user:
   - Show the phase, section in progress, and Next Action
   - Ask: "Resume from handoff, or start fresh?"
   - If resume: skip to the recorded step
   - If fresh: proceed normally
3. **If not found:** Proceed normally

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
- Read `${CLAUDE_PLUGIN_ROOT}/references/constraints/claim-id-traceability.md`

**Conventions:**
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/gate-function-standard.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/artifact-review-gates.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/phase-summary-frontmatter.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/checkpoint-type-classification.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/autonomous-phase-chaining.md`
- Read `${CLAUDE_PLUGIN_ROOT}/references/conventions/iteration-topology.md`

## Setup Flowchart (This IS the Spec)

```
START (brainstorm confirmed)
  │
  ├─ Step 1: Create project directories
  │  └─ mkdir outlines/ drafts/ references/ scratch/ .planning/
  │
  ├─ Step 2: Interview → Create PRECIS.md
  │  ├─ Ask thesis question
  │  ├─ Ask counterargument question
  │  └─ Write .planning/PRECIS.md (thesis, claims, audience, scope)
  │
  ├─ Step 2b: PRECIS Review Gate
  │  └─ Dispatch writing-precis-reviewer subagent
  │     ├─ APPROVED → proceed to Step 3
  │     └─ ISSUES_FOUND → fix PRECIS.md → re-dispatch (max 5)
  │
  ├─ Step 3: Create OUTLINE.md
  │  └─ Map sections → claims from PRECIS
  │     Each section has: Goal, Claim, Key Points, Transition
  │
  ├─ Step 4: Detect domain (legal/econ/general)
  │
  ├─ Step 5: Create ACTIVE_WORKFLOW.md
  │
  └─ GATE: All 3 files exist with required content?
     ├─ NO → Report missing content, fix before proceeding
     └─ YES → IMMEDIATELY load writing-outline (no pause)
```

If text and flowchart disagree, the flowchart wins.

<EXTREMELY-IMPORTANT>
## The Iron Law of Progressive Expansion

**NO OUTLINE WITHOUT PRECIS. NO DRAFTING WITHOUT OUTLINE. This is not negotiable.**

The levels are:
1. PRECIS.md (thesis, claims, audience)
2. OUTLINE.md (structure mapped to claims)
3. Section outlines in outlines/ (detailed per-section)
4. Prose drafts in drafts/ (expanded from outlines)

Skipping levels produces incoherent documents. Each level expands the previous.
</EXTREMELY-IMPORTANT>

## Step 1: Create Project Structure

```bash
mkdir -p outlines drafts references scratch .planning
echo "scratch/" >> .gitignore
```

## Step 2: Create PRECIS.md

### Interview for PRECIS

Use `AskUserQuestion` to gather remaining details:

```
AskUserQuestion(questions=[
  {
    "question": "What is your thesis in one sentence?",
    "header": "Thesis",
    "options": [
      {"label": "I have a thesis", "description": "I will type it"},
      {"label": "Help me find it", "description": "Synthesize from sources"},
      {"label": "Critique: X is wrong", "description": "Argue against existing view"},
      {"label": "Propose: X should change", "description": "Recommend reform"}
    ],
    "multiSelect": false
  },
  {
    "question": "What is the strongest objection to your thesis?",
    "header": "Counter",
    "options": [
      {"label": "I know it", "description": "I will describe the objection"},
      {"label": "Find from sources", "description": "What do critics say?"},
      {"label": "Steel-man for me", "description": "Generate the best counter"}
    ],
    "multiSelect": false
  }
])
```

### PRECIS.md Template

Write to `.planning/PRECIS.md`:

```markdown
# Precis: [Working Title]

## Thesis
[One sentence - the core argument]

## Audience
[From earlier interview - who is reading, what they know/believe]

## Purpose
[What reader should think/do/believe after reading]

## Hook
[Concrete problem, controversy, or question that opens the piece - draft or TBD]

## Key Claims
- **CLAIM-01**: [Claim 1] → supports thesis by...
- **CLAIM-02**: [Claim 2] → supports thesis by...
- **CLAIM-03**: [Claim 3] → supports thesis by...

## Counterarguments to Address
1. **[Objection]**: [description]
   - Response: [how we will address it]
   - Section: [where it appears]

## Scope
### In
- [What we cover]

### Out
- [What we explicitly exclude and why]

## Domain
[legal | econ | general] → determines which writing skill to use
```

## Step 2b: PRECIS Review Gate

After writing PRECIS.md, dispatch the precis reviewer BEFORE creating the outline. Do NOT skip this step.

Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-precis-reviewer/SKILL.md` and follow its instructions.

Follow the reviewer skill instructions: dispatch the subagent, handle APPROVED/ISSUES_FOUND, fix and re-review up to 5 times. Only proceed to Step 3 when the reviewer returns APPROVED.

## Step 3: Create OUTLINE.md

Structure the argument with sections mapped to claims from PRECIS.md.

### OUTLINE.md Template

```markdown
# Outline: [Title from PRECIS]

## Structure

### I. Introduction
- **Goal**: Hook reader, state thesis, roadmap
- **Hook**: [from PRECIS or TBD]
- **Thesis**: [from PRECIS]
- **Claims preview**: [list from PRECIS]

### II. [Section Name]
- **Goal**: [what this section accomplishes]
- **Implements**: [CLAIM-01, CLAIM-02, etc. from PRECIS]
- **Key points**:
  - Point A (sources: ...)
  - Point B (sources: ...)
- **Transition to next**: [how it leads to Section III]

### III. [Section Name]
- **Goal**: [what this section accomplishes]
- **Implements**: [CLAIM-XX from PRECIS]
- **Key points**:
  - [points with sources]

### IV. Counterarguments
- **Goal**: Address objections from PRECIS
- **Objection 1**: [from PRECIS] → Response
- **Objection 2**: [from PRECIS] → Response

### V. Conclusion
- **Goal**: Restate thesis with earned authority
- **Implications**: What follows from this argument
- **Future questions**: What remains unresolved

## Key Sources
[Deduplicated from search phase]

## Open Questions
[Gaps to address before drafting]
```

## Step 4: Domain Detection

Detect domain from sources and topic:

| Domain Indicators | Style | Skill |
|---|---|---|
| Legal cases, statutes, law reviews, constitutional | legal | writing-legal |
| Economics, markets, policy, data, empirical | econ | writing-econ |
| General/other | general | writing-general |

## Step 5: Create ACTIVE_WORKFLOW.md

Create `.planning/ACTIVE_WORKFLOW.md` to track workflow state:

```yaml
---
workflow: writing
style: [legal|econ|general]
phase: outline
project_root: [current directory]
precis: .planning/PRECIS.md
outline: .planning/OUTLINE.md
current_part: [if multi-part document]
edits_since_verify: 0
verify_threshold: 10
skill_stack:
  - writing
  - writing-[domain]
---
```

## Step 6: Announce Handoff

```
Writing project initialized.

Project: [directory name]
Style: [legal/econ/general]
Phase: outline

Files created:
- .planning/PRECIS.md (thesis, audience, claims)
- .planning/OUTLINE.md (structure)
- .planning/ACTIVE_WORKFLOW.md (workflow state)

Next: Create detailed section outlines.
```

---

## Gate: Exit Setup

Before proceeding to outline phase (see `conventions/gate-function-standard.md` for the full 6-step gate including SUMMARY):

1. **IDENTIFY**: What proves setup is complete?
   - `.planning/PRECIS.md` exists with thesis, claims, audience
   - `.planning/OUTLINE.md` exists with sections mapped to claims
   - `.planning/ACTIVE_WORKFLOW.md` exists with style and phase
2. **RUN**: Read each file
3. **READ**: Check content
   - PRECIS has non-empty Thesis, Key Claims, Audience, Domain
   - OUTLINE has sections with Goals and Claim references
   - ACTIVE_WORKFLOW has `workflow: writing` and valid `style:`
4. **VERIFY**: All three files exist and contain required content
5. **CLAIM**: Only if steps 1-4 pass, proceed to outline phase

## Rationalization Table

| Excuse | Reality | Do Instead |
|---|---|---|
| "I'll refine the thesis during drafting" | Unrefined thesis = unfocused draft = complete rewrite | Nail the thesis now |
| "Three claims is plenty" | Check if three is earned or arbitrary | Justify each claim's necessity |
| "The scope section isn't important" | Unbounded scope produces unbounded documents | Define IN and OUT explicitly |
| "I already know the structure" | You're guessing from similar papers, not this one | Derive structure from THIS thesis and claims |
| "The outline doesn't need transitions planned yet" | Transitions ARE the argument's logic | Plan transitions now or the draft will be fragments |
| "I can add counterarguments later" | Counterarguments shape the thesis itself | Confront objections before finalizing claims |

**Skipping PRECIS verification is NOT HELPFUL — the user builds an entire document on a vague thesis that collapses under scrutiny.** A vague thesis is not a thesis. Placeholder claims are not claims.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Getting to drafting fast helps the user see progress" | The draft has no foundation. Every section wanders from the thesis. You rewrite the entire document. Your speed created 3x the work. | **Anti-helpful** |
| **Competence** | "I can hold the thesis in my head, no need for detailed PRECIS" | Without written claims, sections drift. Without scope boundaries, the document sprawls. Your mental model was incomplete — the PRECIS would have caught it. | **Incompetent** |
| **Honesty** | "The PRECIS is complete enough" | You wrote a vague thesis and placeholder claims. The user drafts an entire document on a shaky foundation — every section wanders. | **Anti-helpful** |

## Red Flags - STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Creating OUTLINE before PRECIS | Structure without thesis = incoherent | Write PRECIS first |
| Skipping the thesis interview | You'll write a document without an argument | Ask the thesis questions |
| Setting domain without checking source indicators | Wrong domain = wrong style rules loaded later | Check the domain detection table |
| Creating ACTIVE_WORKFLOW without PRECIS and OUTLINE | Workflow state without foundation is meaningless | Create artifacts first |
| Rushing through PRECIS to get to drafting | Thin PRECIS → thin argument → high rework | Invest time in PRECIS now |

## Next Phase

After setup is complete, IMMEDIATELY proceed to the outline phase. Do NOT pause to ask the user. Do NOT summarize what you just created. Load the next skill and continue:

Read `${CLAUDE_PLUGIN_ROOT}/skills/writing-outline/SKILL.md` and follow its instructions.

Then follow its instructions immediately to create detailed section outlines.
