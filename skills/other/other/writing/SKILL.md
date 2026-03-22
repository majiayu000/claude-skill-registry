---
name: writing
description: "This skill should be used when the user asks to 'write a paper', 'start a writing project', 'draft an article', 'write about', 'brainstorm writing topics', 'gather sources for a paper', 'what should I write about', or needs the writing workflow entry point for any writing task."
allowed-tools: Read, Grep, Glob, Bash, Skill, TodoWrite
---

# Writing

**Entry point for all writing tasks.** Routes to quick mode or project workflow.

## Shared Enforcement

Load the constraint index for the writing workflow:

!`cat ${CLAUDE_SKILL_DIR}/../../references/writing-common-constraints.md`

**Router loads index only.** Phase skills load specific atomic files relevant to their phase.

## Session Resume Detection

Before starting, check for an existing handoff:

1. Check if `.planning/HANDOFF.md` exists
2. **If found:** Read it and present to user:
   - Show the phase, section in progress, and Next Action
   - Ask: "Resume from handoff, or start fresh?"
   - If resume: skip to the recorded phase
   - If fresh: proceed with mode detection
3. **If not found:** Proceed normally

## Decision Flowchart (This IS the Spec)

```
START
  │
  ├─ Quick edit? ("check this paragraph", inline short text)
  │  YES → Load writing-general/SKILL.md → Apply rules → Return → EXIT
  │
  ├─ Active workflow? (.planning/ACTIVE_WORKFLOW.md exists)
  │  YES → Read ACTIVE_WORKFLOW.md → Resume at current phase → EXIT
  │
  └─ New project
     → Phase 2: Detect Domain, Gather Sources
     → Launch writing-setup
```

If text and flowchart disagree, the flowchart wins.

## Step 1: Detect Mode

**Quick Mode Indicators** (edit text directly, no workflow):
- “Check this paragraph”
- “Edit this text”
- “Review my writing”
- Short text provided inline
- No mention of “project”, “paper”, “article”

→ If quick mode: discover the writing-general skill path via `${CLAUDE_SKILL_DIR}/../../skills/writing-general/SKILL.md`, then `Read()` the output path and apply rules to text.

**Project Mode Indicators** (full workflow):
- “Write a paper on...”
- “Start a law review article”
- “Draft an economics paper”
- Mentions thesis, argument, research

→ If project mode: Continue to Phase 2 below.

## Step 2: Check for Active Workflow

```
if .planning/ACTIVE_WORKFLOW.md exists:
    Read(“.planning/ACTIVE_WORKFLOW.md”)
    Read(“.planning/PRECIS.md”)
    Read(“.planning/OUTLINE.md”)
    → Resume at current phase with appropriate domain skill
else:
    → Continue to Phase 3 (new project setup)
```

---

## Project Mode Workflow

Creates PRECIS.md (thesis, audience, claims) and OUTLINE.md (structure), then hands off to domain-specific writing skill.

## Project Structure

Writing projects should follow this standardized structure:

```
project-name/
├── .planning/
│   ├── ACTIVE_WORKFLOW.md      # Workflow state (auto-created)
│   ├── PRECIS.md               # Thesis, audience, claims, counterarguments
│   └── OUTLINE.md              # Master document structure
├── outlines/                    # Detailed section/part outlines
│   ├── Part I (Outline).md
│   ├── Part II (Outline).md
│   └── ...
├── drafts/                      # Prose drafts (expanded from outlines)
│   ├── Part I (Draft).md
│   ├── Part II (Draft).md
│   └── ...
├── references/                  # Source materials, notes
│   ├── sources.md               # Bibliography / source list
│   └── [topic-notes].md         # Research notes by topic
└── scratch/                     # Working files (gitignored)
    └── brainstorm-notes.md
```

### Directory Purposes

| Directory | Purpose | Tracked in Git |
|-----------|---------|----------------|
| `.planning/` | Workflow state + high-level docs (PRECIS, OUTLINE) | Yes |
| `outlines/` | Detailed outlines per section/part | Yes |
| `drafts/` | Prose versions of outlines | Yes |
| `references/` | Sources, research notes | Yes |
| `scratch/` | Temporary working files | No |

### Progressive Expansion Workflow

Writing proceeds through levels of detail:

```
.planning/PRECIS.md          # Level 1: Thesis, claims, audience
       ↓
.planning/OUTLINE.md         # Level 2: Master structure (sections, goals)
       ↓
outlines/Part I.md         # Level 3: Detailed section outline (bullets, sources)
       ↓
drafts/Part I.md           # Level 4: Prose expansion
```

**Each level expands the previous.** Don’t skip levels:
- PRECIS before OUTLINE
- Master OUTLINE before section outlines
- Section outline before drafting prose

### File Naming Convention

For multi-part documents:
- Section outlines: `outlines/Part I (Outline).md`
- Prose drafts: `drafts/Part I (Draft).md`

For single documents:
- Master outline in `.planning/OUTLINE.md` is sufficient
- Draft: `drafts/draft.md` or `drafts/[title].md`

### Creating Project Structure

When starting a new writing project, create the directories:

```bash
mkdir -p outlines drafts references scratch .planning
echo “scratch/” >> .gitignore
```

## Writing Workflow Overview

```
/writing (entry point)
    │
    └── skills/writing/ (this skill)
            │ Mode detect, source gathering, topic exploration
            │ GATE: Sources gathered, domain detected
            │
            └── skills/writing-setup/ (project foundation)
                    │ PRECIS.md, OUTLINE.md, ACTIVE_WORKFLOW.md
                    │ GATE: All three files exist with required content
                    │
                    └── skills/writing-outline/ (per section)
                            │ outlines/[Section] (Outline).md
                            │ GATE: Outline cross-references PRECIS claims
                            │
                            └── skills/writing-draft/ (per section)
                                    │ Domain skill loaded (legal/econ/general)
                                    │ drafts/[Section] (Draft).md
                                    │ GATE: All sections drafted with depth
                                    │
                                    └── /writing-review (diagnose → REVIEW.md)
                                            │ Hierarchical review: section → transition → document
                                            │ .planning/REVIEW.md
                                            │ GATE: All sections reviewed, all levels complete
                                            │
                                            └── /writing-revise (fix from REVIEW.md + complete)
```

## When to Use

Invoke this skill for:
- Discovering what to write about from reading patterns
- Gathering sources and references for a known topic
- Finding thematic connections across highlights
- Building an outline with supporting quotes

## Prerequisites

Source searching is handled by the **librarian agent** (`workflows:librarian`), which routes through NLM first, then Readwise via opencode. You do NOT need direct Readwise MCP access.

## Critical: ALL Source Searches Go Through Librarian

<EXTREMELY-IMPORTANT>
**NEVER call Readwise MCP tools directly. NEVER spawn general-purpose agents for searches.**

ALL source gathering MUST go through the librarian agent, which enforces:
1. Check NLM first (curated knowledge)
2. Readwise via opencode (context-safe, 1M window)
3. Structured output (sources, quotes, synthesis)

**If you're about to call `mcp__readwise__*` or spawn a `general-purpose` agent for search, STOP.**
</EXTREMELY-IMPORTANT>

<EXTREMELY-IMPORTANT>
## The Iron Law of Clarifying Intent

**NO SEARCH WITHOUT CLARIFYING INTENT FIRST. This is not negotiable.**

In Gathering Mode, you MUST use `AskUserQuestion` to understand angle and audience BEFORE launching any librarian searches. Searching without intent produces scattered results that don't serve an argument.

If you find yourself about to search before the user has confirmed their angle:
1. STOP immediately
2. Ask the clarifying questions (Phase 1)
3. THEN decompose into search themes
4. THEN launch parallel librarian agents

**Searching before clarifying is like outlining before having a thesis.** You'll gather sources for a topic, not an argument. The sources won't support any specific claim because you don't have one yet.
</EXTREMELY-IMPORTANT>

### Librarian Search Pattern

For a topic with N distinct themes, launch N parallel librarian agents:

```
Task(
  subagent_type="workflows:librarian",
  prompt="""Search for highlights and sources about **[THEME]**.

Check NLM notebooks first, then search Readwise.

Return ONLY:
- Top 3 most relevant sources (title, author)
- Top 3 quotes worth citing (with source attribution)
- 1-2 sentence theme summary"""
)
```

### Example: Law Review on Private Equity Access

Launch 5 parallel librarian agents:
1. "private equity retail investors democratization"
2. "accredited investor definition regulation"
3. "401k retirement private markets"
4. "interval fund tender offer evergreen"
5. "investor protection paternalism securities"

Each returns ~100 words instead of ~5000 words of raw highlights.

---

## Two Modes

### Discovery Mode

When user wants to find topics ("what should I write about?"):

1. **Survey knowledge base**
   - Dispatch librarian: "List NLM notebooks and summarize what topics are covered"
   - Dispatch librarian: "What are the most common tags and recent reading themes in Readwise?"

2. **Analyze patterns**
   - From librarian results, identify recurring themes, authors, or concepts
   - Look for: tensions, debates, unanswered questions, surprising connections

3. **Present topic candidates**
   - For each potential topic, show:
     - Theme description
     - Supporting highlights (2-3 examples)
     - Relevant tags
     - Potential angle or thesis

### Gathering Mode (Progressive Workflow)

When user has a topic (“gather sources on X”), follow this **human-in-the-loop** workflow:

#### Phase 1: Clarify Intent

**BEFORE any search**, use `AskUserQuestion` to understand:

```
AskUserQuestion(questions=[
  {
    “question”: “What’s your primary angle or thesis for this piece?”,
    “header”: “Angle”,
    “options”: [
      {“label”: “Critique existing framework”, “description”: “Argue current approach is flawed”},
      {“label”: “Propose reform”, “description”: “Offer specific policy changes”},
      {“label”: “Comparative analysis”, “description”: “Compare approaches across jurisdictions”},
      {“label”: “Empirical analysis”, “description”: “Present data-driven findings”}
    ],
    “multiSelect”: false
  },
  {
    “question”: “Who is your target audience?”,
    “header”: “Audience”,
    “options”: [
      {“label”: “Law review”, “description”: “Academic legal audience”},
      {“label”: “Practitioners”, “description”: “Lawyers, regulators, compliance”},
      {“label”: “Policy makers”, “description”: “Legislators, agency staff”},
      {“label”: “General educated”, “description”: “Informed non-specialists”}
    ],
    “multiSelect”: false
  }
])
```

#### Phase 2: Search Sources

1. **Decompose into themes** based on clarified intent
   - Break the topic into 3-6 distinct search themes
   - Each theme becomes a parallel sub-agent search

2. **Launch parallel librarian agents**
   - Use the Task tool with `subagent_type="workflows:librarian"` for each theme
   - Run all searches in a single message (parallel execution)
   - See "Librarian Search Pattern" section above

3. **Synthesize results**
   - Deduplicate sources across agent responses
   - Identify the strongest quotes from each theme
   - Note gaps (themes with few/no highlights)

#### Phase 3: Synthesize and Present

Present a summary of findings to the user for confirmation:
- **Topic and angle** confirmed
- **Key themes** identified (3-6)
- **Source coverage** - strong/weak areas noted
- **Domain detected** (legal/econ/general)

**Ask for feedback** before proceeding to project setup.

The actual OUTLINE.md and PRECIS.md creation happens in the next phase (writing-setup), not here. Brainstorm's job is to gather and synthesize, not to create project artifacts.

## Output Format

Present brainstorm results as a summary:

```markdown
# [Topic Title]

## Thesis/Angle
[One-sentence framing]

## Key Sources
- **[Source 1]** by [Author]
  - “[Highlight quote]”
  - Relevant to: [subtopic]

## Outline
### [Subtopic 1]
- Point A (Source 1, Source 3)
- Point B (Source 2)

### [Subtopic 2]
...

## Open Questions
- [Questions highlights don’t answer]

## Next Steps
- Suggested writing skill: /writing-[domain]
```

## Domain Detection

After gathering sources, detect the topic domain and load the appropriate skill:

| Domain Indicators | Style | Skill to Load |
|-------------------|-------|---------------|
| Legal cases, statutes, law reviews, constitutional | legal | `skills/writing-legal/SKILL.md` |
| Economics, markets, policy, data, empirical | econ | `skills/writing-econ/SKILL.md` |
| General/other | general | `skills/writing-general/SKILL.md` |

Domain-specific enforcement rules are applied during the **draft phase** (writing-draft skill), not during brainstorm. Brainstorm only detects the domain; enforcement happens later.

## Source Access Quick Reference

| Need | Action |
|------|--------|
| Survey topic landscape | Dispatch librarian: "What topics are in my NLM notebooks and Readwise tags?" |
| Find highlights by keyword | Dispatch librarian: "Search for highlights about [topic]" |
| Get book/article highlights | Dispatch librarian: "Get highlights from [title] and summarize" |
| Full document text | Dispatch librarian: "Fetch full text of articles tagged [tag]" |

## Workflow Examples

### Discovery Mode Example

**User:** “I want to write something but don’t know what”

**Process:**
1. Fetch tags → find clusters like “antitrust”, “market-power”, “regulation”
2. Get recent highlights → notice many from economics sources
3. Analyze → tension between “consumer welfare” and “market structure” keeps appearing
4. Present → “Potential topic: The consumer welfare standard debate. You have 12 highlights across 4 sources discussing this tension. Angle: Why market structure matters beyond prices.”
5. Domain detection → Economics sources detected → econ style will apply during drafting

### Gathering Mode Example (Progressive)

**User:** “Let’s brainstorm a law review article about retail access to private equity”

**Process:**
1. **Clarify** → AskUserQuestion: angle (critique/reform/comparative), audience (law review/practitioners)
2. **User responds** → “Critique existing framework, law review audience”
3. **Decompose** → 5 themes: PE retail access, accredited investor, 401(k) access, fund structures, investor protection
4. **Search** → Launch 5 parallel librarian agents
5. **Synthesize** → Dedupe sources, extract best quotes, note gaps
6. **Present** → "Here are the themes and sources. Confirm topic and angle?"
7. **User confirms** → "Yes, critique framework. Add comparative section on EU ELTIF."
8. **Handoff** → Proceed to writing-setup for PRECIS.md and OUTLINE.md creation

---

## Agent Team Pattern: Parallel Source Gathering

For topics with many research themes, launch parallel librarian agents that each own a research angle:

```
# Launch 3 librarian agents in a SINGLE message (parallel)
Task(subagent_type="workflows:librarian", prompt="Search for sources SUPPORTING the thesis: [thesis]. Return top quotes and sources.")
Task(subagent_type="workflows:librarian", prompt="Search for sources OPPOSING the thesis: [thesis]. Steel-man the counterarguments.")
Task(subagent_type="workflows:librarian", prompt="Search for empirical evidence and data related to: [thesis]. Focus on numbers and findings.")
```

This produces better-grounded brainstorming than sequential searches because parallel agents find contradictions you'd otherwise miss.

---

## Gate: Exit Brainstorm

Before proceeding to project setup:

1. **IDENTIFY**: What file-based evidence proves brainstorm is complete?
   - Sources gathered: librarian sub-agent results returned with real quotes and source attributions
   - Domain detected: indicators from source material (not guessed from topic name)
   - User confirmation: AskUserQuestion response confirming topic, angle, and audience
2. **RUN**: Verify file-based artifacts exist:
   - At least one librarian sub-agent returned structured results (sources + quotes)
   - OR (discovery mode) topic candidates were presented with supporting highlights
   - AskUserQuestion was used to confirm angle and audience (not just conversation flow)
3. **READ**: Check the evidence:
   - Source results contain specific titles, authors, and quoted text (not summaries from training data)
   - Domain indicators come from actual source material characteristics
4. **VERIFY**: All three conditions met: (a) real sources gathered, (b) user confirmed via AskUserQuestion, (c) domain detected from evidence
5. **CLAIM**: Only if steps 1-4 pass, proceed to writing-setup

**"User seemed to agree" is not confirmation. AskUserQuestion response or explicit typed confirmation is confirmation.** Inferring agreement from silence or topic continuation is rubber-stamping the gate.

## Rationalization Table

| Excuse | Reality | Do Instead |
|---|---|---|
| "I already know enough about this topic" | Your training data is not research | Search for real sources |
| "One search is enough" | One search finds one perspective | Decompose into 3-6 parallel searches |
| "The user seems impatient, skip the interview" | Wrong objectives waste more time than questions | Ask the clarifying questions |
| "I'll gather more sources later" | Later never comes; you'll draft with what you have | Gather sources now |
| "This topic is straightforward" | "Straightforward" means you haven't thought deeply enough | Find the complexity |

**Skipping source gathering is NOT HELPFUL — the user publishes unsupported claims that reviewers reject.** Your training knowledge is not research. Your recall is not citation.

## Why Skipping Hurts the Thing You Care About Most

| Your Drive | Why You Skip | What Actually Happens | The Drive You Failed |
|------------|--------------|----------------------|---------------------|
| **Helpfulness** | "Getting to drafting fast helps the user see progress" | The draft has no evidence. Every claim is an assertion. The user submits and reviewers reject for lack of sources. Your speed destroyed their credibility. | **Anti-helpful** |
| **Competence** | "I already know enough about this topic to skip research" | You searched nothing. The paper misses the 3 most relevant recent sources. A librarian search would have found them in 2 minutes. Your expertise was ignorance. | **Incompetent** |
| **Efficiency** | "The user interview wastes time — I can infer the angle" | You inferred wrong. The paper argues critique when the user wanted reform. You rewrote from scratch. The 5-minute interview would have saved 2 hours. | **Anti-efficient** |
| **Approval** | "The user seems eager to start writing" | You skipped clarification to please them. The draft argues the wrong thesis. The user now questions whether you understand their work at all. You lost trust. | **Lost approval** |
| **Honesty** | "I cited from memory — I know these sources" | Your training data citations are wrong or outdated. The user submits fabricated sources — their credibility is destroyed. | **Anti-helpful** |

## Red Flags - STOP If You Catch Yourself:

| Action | Why Wrong | Do Instead |
|---|---|---|
| Jumping to PRECIS creation without source gathering | PRECIS without sources = thin argument | Gather sources first |
| Skipping the user interview about angle/audience | You'll brainstorm for the wrong audience | Ask the clarifying questions |
| Running a single search instead of parallel librarian agents | Single search misses themes | Decompose into 3-6 parallel librarian searches |
| Calling Readwise MCP tools directly | Violates librarian Iron Law, pollutes context | Always dispatch workflows:librarian |
| Detecting domain without checking source indicators | Wrong domain = wrong style enforcement later | Check the domain detection table |
| Moving to setup before user confirms the topic | User approval is the gate | Present findings, get confirmation |

## Next Phase

<EXTREMELY-IMPORTANT>
### No Pause Between Brainstorm and Setup

**After the user confirms topic and sources are gathered, IMMEDIATELY proceed to writing-setup. Do NOT ask "should I continue?" or "ready to proceed?" or any variant.**

The gate passed. The user confirmed. Asking permission to continue is procrastination disguised as courtesy. Load the next skill and execute it.
</EXTREMELY-IMPORTANT>

After brainstorm is complete, proceed to project setup:

Read `${CLAUDE_SKILL_DIR}/../../skills/writing-setup/SKILL.md` and follow its instructions.

Then follow its instructions immediately to create PRECIS.md, OUTLINE.md, and ACTIVE_WORKFLOW.md.
