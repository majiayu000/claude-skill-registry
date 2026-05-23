---
name: writing-brainstorm
description: This skill should be used when the user asks to "find something to write about", "brainstorm topics", "what should I write about", "find writing ideas", "gather sources for", "pull references on", or needs help discovering topics from their reading highlights. Leverages Readwise MCP to surface patterns and gather references.
---

# Writing Brainstorm

Generate writing topics and gather references from Readwise highlights.

## When to Use

Invoke this skill for:
- Discovering what to write about from reading patterns
- Gathering sources and references for a known topic
- Finding thematic connections across highlights
- Building an outline with supporting quotes

## Prerequisites

This skill requires the Readwise MCP server. The plugin auto-configures it, but the `READWISE_TOKEN` environment variable must be set.

**Setup (if MCP not working):**
1. Get API token from https://readwise.io/access_token
2. Set environment variable: `export READWISE_TOKEN=your_token`
3. Verify: `claude mcp list` should show `readwise`

## Critical: Sub-Agent Pattern for Readwise Searches

**NEVER call `search_readwise_highlights` directly from the main chat.** Raw search results return 50-100+ highlights, polluting context and degrading conversation quality.

**ALWAYS use parallel sub-agents** (one per search theme) to:
1. Execute the search
2. Filter and deduplicate results
3. Return a condensed summary

### Sub-Agent Pattern

For a topic with N distinct themes, launch N parallel sub-agents using the Task tool:

```
Task(
  subagent_type="general-purpose",
  model="haiku",  # Fast and cheap for filtering
  prompt="""Search Readwise for highlights about **[THEME]**.

Use `mcp__readwise__search_readwise_highlights` with:
- vector_search_term: "[semantic search terms]"
- full_text_queries: [{"field_name": "highlight_plaintext", "search_term": "[keyword]"}]

Return ONLY:
- Top 3 most relevant sources (title, author)
- Top 3 quotes worth citing (with source attribution)
- 1-2 sentence theme summary"""
)
```

### Example: Law Review on Private Equity Access

Launch 5 parallel agents:
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

1. **Fetch tag landscape**
   - Use `get_tags` to see all topic clusters
   - Present tags grouped by frequency/recency

2. **Analyze recent reading**
   - Use `get_recent_content` to fetch recent highlights
   - Identify recurring themes, authors, or concepts

3. **Semantic pattern detection**
   - Examine highlights for cross-cutting themes
   - Look for: tensions, debates, unanswered questions, surprising connections

4. **Present topic candidates**
   - For each potential topic, show:
     - Theme description
     - Supporting highlights (2-3 examples)
     - Relevant tags
     - Potential angle or thesis

### Gathering Mode (Progressive Workflow)

When user has a topic ("gather sources on X"), follow this **human-in-the-loop** workflow:

#### Phase 1: Clarify Intent

**BEFORE any search**, use `AskUserQuestion` to understand:

```
AskUserQuestion(questions=[
  {
    "question": "What's your primary angle or thesis for this piece?",
    "header": "Angle",
    "options": [
      {"label": "Critique existing framework", "description": "Argue current approach is flawed"},
      {"label": "Propose reform", "description": "Offer specific policy changes"},
      {"label": "Comparative analysis", "description": "Compare approaches across jurisdictions"},
      {"label": "Empirical analysis", "description": "Present data-driven findings"}
    ],
    "multiSelect": false
  },
  {
    "question": "Who is your target audience?",
    "header": "Audience",
    "options": [
      {"label": "Law review", "description": "Academic legal audience"},
      {"label": "Practitioners", "description": "Lawyers, regulators, compliance"},
      {"label": "Policy makers", "description": "Legislators, agency staff"},
      {"label": "General educated", "description": "Informed non-specialists"}
    ],
    "multiSelect": false
  }
])
```

#### Phase 2: Search Sources

1. **Decompose into themes** based on clarified intent
   - Break the topic into 3-6 distinct search themes
   - Each theme becomes a parallel sub-agent search

2. **Launch parallel sub-agents**
   - Use the Task tool with `model="haiku"` for each theme
   - Run all searches in a single message (parallel execution)
   - See "Sub-Agent Pattern" section above

3. **Synthesize results**
   - Deduplicate sources across agent responses
   - Identify the strongest quotes from each theme
   - Note gaps (themes with few/no highlights)

#### Phase 3: Draft Outline → `OUTLINE.md`

Save the outline to a file for iteration:

```markdown
# OUTLINE.md

## Working Title
[Title]

## Thesis
[One-sentence claim]

## Target Audience
[From Phase 1]

## Structure
### I. Introduction
### II. [Section]
### III. [Section]
...

## Key Sources
[Deduplicated from Phase 2]

## Open Questions
[Gaps to address]
```

**Ask for feedback** on the outline before proceeding.

#### Phase 4: Section Deep-Dive

For each major section, use `AskUserQuestion` to refine:

```
AskUserQuestion(questions=[
  {
    "question": "For Section II (Background), what level of detail do you need?",
    "header": "Depth",
    "options": [
      {"label": "Brief context", "description": "1-2 paragraphs, assume reader familiarity"},
      {"label": "Full background", "description": "Comprehensive treatment for general reader"},
      {"label": "Synthesis only", "description": "Synthesize precedents without detailed summaries"}
    ],
    "multiSelect": false
  }
])
```

Create `SECTION-II-OUTLINE.md` with:
- Section thesis/purpose
- Key arguments in order
- Supporting sources mapped to arguments
- Anticipated counterarguments

Repeat for each section, getting human feedback before moving to prose.

## Output Format

Produce a markdown outline:

```markdown
# [Topic Title]

## Thesis/Angle
[One-sentence framing]

## Key Sources
- **[Source 1]** by [Author]
  - "[Highlight quote]"
  - Relevant to: [subtopic]

## Outline
### [Subtopic 1]
- Point A (Source 1, Source 3)
- Point B (Source 2)

### [Subtopic 2]
...

## Open Questions
- [Questions highlights don't answer]

## Next Steps
- Suggested writing skill: /writing-[domain]
```

## Domain Detection

After gathering sources, detect the topic domain and suggest the appropriate writing skill:

| Domain Indicators | Suggested Skill |
|-------------------|-----------------|
| Legal cases, statutes, law reviews, constitutional | `/writing-legal` (Volokh) |
| Economics, markets, policy, data, empirical | `/writing-econ` (McCloskey) |
| General/other | `/writing` (Strunk & White) |

## Readwise MCP Tools

Primary tools for brainstorming:

| Tool | Use Case | Direct Call OK? |
|------|----------|-----------------|
| `get_tags` | Survey topic landscape | ✅ Yes |
| `get_recent_content` | See current reading themes | ✅ Yes |
| `search_readwise_highlights` | Find highlights by keyword | ❌ **Sub-agent only** |
| `get_highlights` | Retrieve with filters | ⚠️ Use caution (can be large) |
| `get_books` | Browse source library | ✅ Yes |

**Why sub-agents for search?** A single search can return 50-100 highlights (~5000+ tokens). Multiple searches compound this. Sub-agents filter to essentials before returning to main context.

## File Output Convention

Save brainstorming artifacts to the project's `docs/` or `scratch/` directory:

```
project/
├── docs/
│   └── writing/
│       ├── OUTLINE.md              # Main article outline
│       ├── SECTION-I-OUTLINE.md    # Introduction details
│       ├── SECTION-II-OUTLINE.md   # Background details
│       └── ...
└── scratch/
    └── brainstorm-notes.md         # Working notes (gitignored)
```

## Workflow Examples

### Discovery Mode Example

**User:** "I want to write something but don't know what"

**Process:**
1. Fetch tags → find clusters like "antitrust", "market-power", "regulation"
2. Get recent highlights → notice many from economics sources
3. Analyze → tension between "consumer welfare" and "market structure" keeps appearing
4. Present → "Potential topic: The consumer welfare standard debate. You have 12 highlights across 4 sources discussing this tension. Angle: Why market structure matters beyond prices."
5. Domain detection → Economics sources detected → "Use `/writing-econ` for drafting"

### Gathering Mode Example (Progressive)

**User:** "Let's brainstorm a law review article about retail access to private equity"

**Process:**
1. **Clarify** → AskUserQuestion: angle (critique/reform/comparative), audience (law review/practitioners)
2. **User responds** → "Critique existing framework, law review audience"
3. **Decompose** → 5 themes: PE retail access, accredited investor, 401(k) access, fund structures, investor protection
4. **Search** → Launch 5 parallel Haiku sub-agents
5. **Synthesize** → Dedupe sources, extract best quotes, note gaps
6. **Save** → Write `docs/writing/OUTLINE.md`
7. **Feedback** → "Here's the outline. Any sections to add/remove/reorder?"
8. **User responds** → "Add comparative section on EU ELTIF"
9. **Deep-dive** → AskUserQuestion per section, create `SECTION-II-OUTLINE.md`
10. **Handoff** → "Outline complete. Use `/writing-legal` to draft."

## Integration

After brainstorming:
- `/writing` - General prose drafting
- `/writing-econ` - Economics/finance articles
- `/writing-legal` - Law review articles
- `/ai-anti-patterns` - Check for AI writing indicators
