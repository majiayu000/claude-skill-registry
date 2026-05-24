---
name: geo-research
description: Perform comprehensive geopolitical research using GDELT data sources and specialized analysis agents. Routes queries to appropriate workflows (conflict analysis, sanctions research, actor mapping, narrative analysis) using the diffusion research loop pattern with parallel workers and iterative gap detection. Use when researching armed conflicts, sanctions regimes, international relations, actor networks, or media coverage of geopolitical events.
---

<objective>
Execute comprehensive geopolitical research by:
1. Clarifying the research question and identifying the appropriate analysis type
2. Routing to specialized workflows (conflict, sanctions, actors, narrative)
3. Deploying parallel specialist agents with GDELT MCP tools
4. Synthesizing findings with structured geopolitical output
5. Iterating with gap detection until coverage is sufficient
6. Producing a final report with GDELT data citations and source URLs
</objective>

<essential_principles>
## Geopolitical Research Design

This skill implements the diffusion research pattern specialized for geopolitical intelligence:

### 1. Topic-Based Routing

Route queries to the appropriate analysis type:

| Query Signals | Route To | Primary Agent |
|---------------|----------|---------------|
| Conflict, war, violence, military, escalation | Conflict Analysis | `conflict-analyst` |
| Sanctions, embargo, OFAC, trade restrictions | Sanctions Research | `sanctions-researcher` |
| Relations between X and Y, alliances, networks | Actor Analysis | `actor-mapper` |
| Coverage, perception, media, sentiment, narrative | Narrative Analysis | `sentiment-tracker` + `trend-analyst` |
| General/unclear | Multi-Agent | Route based on brief refinement |

### 2. GDELT-First Research

Always start with structured GDELT data before web sources:
- Events data provides quantitative foundation
- GKG provides entity/theme context
- Tone data quantifies sentiment
- Web sources fill gaps and provide qualitative depth

### 3. Worker Isolation with Domain Expertise

Each specialist agent receives ONLY their focus area:
- Conflict analysts see conflict queries + CAMEO codes
- Sanctions researchers see economic sanctions queries
- Actor mappers see relationship queries
- This prevents cross-contamination of analysis frames

### 4. Geopolitical Gap Detection

Use `gap-detector-geo` for specialized coverage evaluation across:
- Temporal dimensions (historical, current, future)
- Actor completeness (all stakeholders represented)
- Data source diversity (events, GKG, news, official sources)
- Perspective balance (multiple viewpoints)
</essential_principles>

<available_components>
## MCP Tools (GDELT Server)

| Tool | Purpose | Key Use Cases |
|------|---------|---------------|
| `gdelt_events` | CAMEO-coded event queries | Conflict tracking, bilateral events, Goldstein scale analysis |
| `gdelt_gkg` | Global Knowledge Graph | Entity extraction, theme analysis, tone data |
| `gdelt_actors` | Actor relationship mapping | Bilateral relationships, actor profiles |
| `gdelt_trends` | Coverage trends over time | Volume tracking, tone trajectories |
| `gdelt_doc` | Full-text article search | Qualitative sources, specific article retrieval |
| `gdelt_cameo_lookup` | CAMEO code meanings | Decode event types, explain Goldstein scores |

## Specialist Agents

| Agent | Expertise | When to Deploy |
|-------|-----------|----------------|
| `geopolitical-research:conflict-analyst` | Armed conflict, escalation, military dynamics | Conflict events, violence patterns, actor fighting |
| `geopolitical-research:sanctions-researcher` | Sanctions regimes, trade restrictions, enforcement | Economic measures, OFAC/EU designations, evasion |
| `geopolitical-research:actor-mapper` | Relationship networks, alliance structures | Actor relationships, power dynamics, coalitions |
| `geopolitical-research:sentiment-tracker` | Media sentiment, narrative frames | Coverage tone, polarization, source bias |
| `geopolitical-research:trend-analyst` | Temporal patterns, coverage evolution | Trend analysis, early warning, forecasting |
| `geopolitical-research:gap-detector-geo` | Coverage evaluation | After each research round (DO NOT use for research) |
</available_components>

<algorithm>
## The Geopolitical Research Loop

```
PHASE 0: QUERY REFINEMENT (Interactive)
├── 0.1 Parse geopolitical query
├── 0.2 Identify primary analysis type (conflict/sanctions/actors/narrative)
├── 0.3 Generate DRAFT research brief
├── 0.4 Present brief to user via AskUserQuestion
│   ├── "Is this the right analysis type?"
│   ├── "Are these dimensions correct?"
│   ├── "What temporal scope?"
│   └── "Any specific actors to focus on?"
├── 0.5 Refine brief based on feedback
└── 0.6 Confirm and proceed

PHASE 1: INITIALIZATION
├── 1.1 Finalize research brief with:
│   ├── Primary analysis type
│   ├── Geographic scope
│   ├── Temporal scope
│   ├── Key actors to track
│   └── Specific questions to answer
├── 1.2 Select specialist agents for deployment
└── 1.3 Generate initial speculative assessment

PHASE 2: DIFFUSION LOOP (max 3 iterations)
├── 2.1 SPAWN SPECIALIST WORKERS
│   ├── Deploy 2-4 specialist agents in PARALLEL
│   ├── Each agent receives focused brief + GDELT tool access
│   └── Wait for all to complete
│
├── 2.2 SYNTHESIZE
│   ├── Merge findings by dimension
│   ├── Cross-reference GDELT data with web sources
│   ├── Resolve contradictions (note if unresolvable)
│   └── Structure with proper citations
│
├── 2.3 GAP DETECTION
│   ├── Launch gap-detector-geo with: query, brief, draft
│   ├── Evaluate across weighted dimensions:
│   │   ├── Core (3x): Temporal, Actor, Data Source
│   │   ├── Supporting (2x): Quantification, Geographic, Perspective
│   │   └── Contextual (1x): Precedents, Expert Sources, Timeline
│   └── Decision: CONTINUE (gaps found) or COMPLETE
│
└── 2.4 ITERATE or EXIT
    ├── If CONTINUE: spawn workers for specific gaps
    └── If COMPLETE: proceed to final report

PHASE 3: FINAL REPORT
├── 3.1 Structure findings by analysis type
├── 3.2 Include all quantitative GDELT data
├── 3.3 Compile sources (GDELT queries + URLs)
└── 3.4 Add executive summary and confidence assessment
```
</algorithm>

<intake>
What geopolitical topic would you like me to research?

I can provide comprehensive analysis using GDELT's event database and specialized agents for:

**Conflict Analysis**
- Armed conflict dynamics and escalation patterns
- Actor relationships in conflict zones
- Third-party involvement (mediators, suppliers, allies)

**Sanctions Research**
- Active sanctions regimes and recent designations
- Economic impact assessment
- Enforcement actions and evasion patterns

**Actor Analysis**
- Relationship networks between countries/actors
- Alliance structures and power dynamics
- Bilateral relationship trends

**Narrative Analysis**
- Media sentiment across source countries
- Coverage trends and inflection points
- Polarization and narrative framing

**Example queries:**
- "What is the current state of the Russia-Ukraine conflict and who are the key third-party actors?"
- "How effective have semiconductor sanctions on China been?"
- "Map the relationship network around the Gulf Cooperation Council"
- "How is Western vs BRICS media covering the Israel-Palestine situation?"
</intake>

<execution_guide>
## Phase 0: Query Refinement

After receiving the query, classify and validate with the user.

### Step 1: Classify Query Type

Analyze the query to determine primary analysis type:

```markdown
## Query Classification

**Your Query:** [Original query]

**Detected Type:** [Conflict / Sanctions / Actor / Narrative / Multi-Dimensional]

**Reasoning:** [Why this classification]

**Proposed Focus:**
- Geographic scope: [Countries/regions]
- Temporal scope: [Time period]
- Key actors: [Primary actors to track]
```

### Step 2: Generate Draft Brief

```markdown
## Draft Research Brief

**Query:** [User's question]
**Analysis Type:** [Primary type]

**Core Dimensions:**
1. [Dimension 1] - [Why it matters for this analysis]
2. [Dimension 2] - [Why it matters]
3. [Dimension 3] - [Why it matters]

**Key Questions:**
- [Question 1] (Core)
- [Question 2] (Core)
- [Question 3] (Supporting)

**Specialist Agents to Deploy:**
1. [Agent 1] for [Focus area]
2. [Agent 2] for [Focus area]
3. [Agent 3] for [Focus area]
```

### Step 3: Validate with User

```
AskUserQuestion(
  questions: [
    {
      header: "Analysis Type",
      question: "Is this the right type of analysis for your question?",
      options: [
        { label: "Yes, proceed", description: "This analysis type fits my needs" },
        { label: "Focus on conflict", description: "I want conflict/escalation analysis" },
        { label: "Focus on sanctions", description: "I want economic sanctions analysis" },
        { label: "Focus on relationships", description: "I want actor network mapping" },
        { label: "Focus on coverage", description: "I want media/sentiment analysis" }
      ],
      multiSelect: false
    },
    {
      header: "Temporal Scope",
      question: "What time period should I focus on?",
      options: [
        { label: "Recent (30 days)", description: "Current developments and immediate context" },
        { label: "Medium (90 days)", description: "Recent quarter with trend context" },
        { label: "Extended (1 year)", description: "Full year for pattern analysis" },
        { label: "Historical (2+ years)", description: "Deep historical analysis" }
      ],
      multiSelect: false
    },
    {
      header: "Depth",
      question: "What level of depth do you need?",
      options: [
        { label: "Quick overview", description: "Key facts, 1 iteration, ~3 min" },
        { label: "Standard (Recommended)", description: "Thorough coverage, 2-3 iterations, ~7 min" },
        { label: "Exhaustive", description: "Maximum depth, all angles, ~12 min" }
      ],
      multiSelect: false
    }
  ]
)
```

### Step 4: Refine Based on Feedback

- Adjust analysis type if user redirects
- Modify temporal scope
- Update specialist agent selection
- Proceed to Phase 1 once confirmed

---

## Phase 1: Spawn Specialist Workers

Deploy agents in parallel based on analysis type:

### Conflict Analysis Workers

```
Task(
  subagent_type: "geopolitical-research:conflict-analyst",
  prompt: "Analyze conflict dynamics for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Active conflicts and CAMEO event patterns
- Goldstein scale trends (escalation/de-escalation)
- Key belligerents and their recent actions
- Third-party actor involvement

Use GDELT MCP tools: gdelt_events, gdelt_actors, gdelt_gkg
Return structured findings with GDELT data citations.",
  description: "Conflict analysis: [topic]"
)
```

### Sanctions Research Workers

```
Task(
  subagent_type: "geopolitical-research:sanctions-researcher",
  prompt: "Research sanctions for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Active sanctions regimes and recent designations
- Economic impact indicators
- Enforcement actions and violations
- Evasion patterns detected

Use GDELT MCP tools: gdelt_gkg, gdelt_doc, gdelt_trends
Cross-reference with official sources (OFAC, EU).
Return findings with quantitative data.",
  description: "Sanctions research: [topic]"
)
```

### Actor Mapping Workers

```
Task(
  subagent_type: "geopolitical-research:actor-mapper",
  prompt: "Map actor relationships for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Key actors and their types (state, non-state, IGO, etc.)
- Bilateral relationship patterns (Goldstein averages)
- Alliance structures and coalitions
- Relationship trends over time

Use GDELT MCP tools: gdelt_events, gdelt_actors
Return network analysis with relationship metrics.",
  description: "Actor mapping: [topic]"
)
```

### Narrative Analysis Workers

```
Task(
  subagent_type: "geopolitical-research:sentiment-tracker",
  prompt: "Analyze media sentiment for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Overall tone and polarity
- Sentiment by source country/region
- Narrative themes detected
- Media coverage disparities

Use GDELT MCP tools: gdelt_gkg, gdelt_doc
Return quantified sentiment analysis.",
  description: "Sentiment analysis: [topic]"
)

Task(
  subagent_type: "geopolitical-research:trend-analyst",
  prompt: "Analyze coverage trends for: [TOPIC]

Context: [Research brief excerpt]

Focus on:
- Coverage volume timeline
- Key inflection points
- Historical pattern comparison
- Early warning indicators

Use GDELT MCP tools: gdelt_trends, gdelt_events
Return trend analysis with forecasting.",
  description: "Trend analysis: [topic]"
)
```

**CRITICAL**: Spawn ALL relevant workers in a SINGLE message for parallel execution.

---

## Phase 2: Synthesis and Gap Detection

### Synthesize Findings

After workers return, merge into structured draft:

```markdown
## Research Draft: [Topic] (Iteration N)

### Executive Summary
[Key findings in 2-3 sentences]

### [Section by Analysis Type]

#### [Dimension 1]
[Synthesized content with GDELT data]

**GDELT Data:**
- Events: [Summary of event query results]
- Tone: [Sentiment metrics]
- Actors: [Relationship data]

**Sources:**
- [1] GDELT Events Query: [parameters]
- [2] [URL from worker]

[Repeat for each dimension]

### Current Gaps
[Note obvious gaps before formal detection]
```

### Gap Detection

Spawn the geopolitical gap detector:

```
Task(
  subagent_type: "geopolitical-research:gap-detector-geo",
  prompt: "Evaluate geopolitical research coverage:

ORIGINAL QUERY:
[Query]

RESEARCH BRIEF:
[Brief]

CURRENT FINDINGS:
[Draft]

ITERATION: [N]

Assess coverage across:
- Core dimensions (3x weight): Temporal, Actor, Data Source
- Supporting dimensions (2x weight): Quantification, Geographic, Perspective
- Contextual dimensions (1x weight): Precedents, Expert Sources, Timeline

Provide weighted coverage score and specific gaps for follow-up.",
  description: "Evaluate geopolitical coverage"
)
```

### Iteration Decision

**CONTINUE** if:
- Weighted Coverage < 70%
- Major actor/stakeholder missing
- Critical temporal dimension uncovered
- Quantitative claims without GDELT data

**COMPLETE** if:
- Weighted Coverage >= 70%
- All major actors represented
- Key claims have GDELT citations
- No critical gaps identified

**Maximum 3 iterations** to prevent infinite loops.

---

## Phase 3: Final Report

Structure based on primary analysis type:

### Conflict Analysis Report

```markdown
# Geopolitical Research Report: [Title]

**Analysis Type:** Conflict Analysis
**Date:** [Timestamp]
**Coverage Score:** [X%]
**Confidence Level:** [High/Medium/Low]

---

## Executive Summary

[3-5 bullet points of key findings]

---

## Conflict Overview

### Active Conflicts

| Conflict | CAMEO Codes | Avg Goldstein | Trend | Intensity |
|----------|-------------|---------------|-------|-----------|
| [Name] | [Codes] | [Score] | [Direction] | [Level] |

### Key Actors

**Belligerents:**
[Actor profiles with CAMEO codes and recent actions]

**Third-Party Actors:**
[Mediators, suppliers, allies with their roles]

---

## Escalation/De-escalation Assessment

**Indicators Observed:**
- [Indicator 1]: [Status]
- [Indicator 2]: [Status]

**Current Trajectory:** [Assessment]

---

## Key Events Timeline

| Date | Event | Actors | CAMEO | Goldstein | Source |
|------|-------|--------|-------|-----------|--------|
| [Date] | [Description] | [Actors] | [Code] | [Score] | [Source] |

---

## Quantitative Metrics

**GDELT Event Statistics:**
- Total events analyzed: [N]
- Date range: [Range]
- Goldstein scale distribution: [Stats]
- Quad class breakdown: [Stats]

---

## Analysis and Implications

[Cross-cutting insights, patterns, risks]

---

## Confidence Assessment

- **Data Quality:** [Assessment]
- **Coverage Completeness:** [Assessment]
- **Analytical Confidence:** [Assessment]

---

## Sources

**GDELT Queries:**
1. [Query description and parameters]
2. [Query description and parameters]

**News/Expert Sources:**
1. [Title](URL) - [What it contributed]
2. [Title](URL) - [What it contributed]

---
*Research conducted using GDELT geopolitical analysis with [N] specialist agents over [M] iterations.*
```

### Sanctions Research Report

Use similar structure with sections for:
- Active Sanctions Regimes (table)
- Recent Designations/Removals
- Economic Impact Indicators (with data)
- Enforcement Actions
- Evasion Patterns Detected

### Actor Analysis Report

Use similar structure with sections for:
- Actor Profiles (table)
- Relationship Matrix (with Goldstein scores)
- Network Visualization Data (JSON)
- Relationship Trends
- Power Dynamics Analysis

### Narrative Analysis Report

Use similar structure with sections for:
- Sentiment by Region/Source (table)
- Sentiment Timeline
- Narrative Themes Detected
- Coverage Disparities
- Trend Forecast
</execution_guide>

<routing_logic>
## Query Routing Decision Tree

```
START: Parse user query
│
├── Contains: war, conflict, fighting, violence, military, attack,
│   escalation, ceasefire, troops, combat, weapons?
│   └── YES → CONFLICT ANALYSIS
│       ├── Primary: conflict-analyst
│       ├── Supporting: actor-mapper (for actor relationships)
│       └── GDELT focus: gdelt_events (CAMEO 14-20), gdelt_actors
│
├── Contains: sanctions, embargo, OFAC, trade restrictions, asset freeze,
│   designation, tariffs, export controls, enforcement?
│   └── YES → SANCTIONS RESEARCH
│       ├── Primary: sanctions-researcher
│       ├── Supporting: trend-analyst (for impact trends)
│       └── GDELT focus: gdelt_gkg (TAX_SANCTIONS), gdelt_doc
│
├── Contains: relationship, alliance, network, between X and Y,
│   bilateral, coalition, partnership, rivalry?
│   └── YES → ACTOR ANALYSIS
│       ├── Primary: actor-mapper
│       ├── Supporting: trend-analyst (for relationship trends)
│       └── GDELT focus: gdelt_actors, gdelt_events
│
├── Contains: media, coverage, sentiment, narrative, perception,
│   portrayal, tone, how is X reported, bias?
│   └── YES → NARRATIVE ANALYSIS
│       ├── Primary: sentiment-tracker
│       ├── Secondary: trend-analyst
│       └── GDELT focus: gdelt_gkg (tone), gdelt_trends
│
└── UNCLEAR or MULTI-DIMENSIONAL
    └── Ask user to clarify OR deploy multiple analysis types
        ├── Use AskUserQuestion to determine primary focus
        └── If truly multi-dimensional, run parallel workflows
```

## Multi-Dimensional Queries

Some queries require multiple analysis types:

**Example:** "What is the current state of US-China relations?"
- Actor Analysis: Relationship patterns, Goldstein trends
- Sanctions Research: Trade restrictions, tech sanctions
- Narrative Analysis: Media coverage differences

**Approach:**
1. Identify primary type (Actor Analysis in this case)
2. Spawn primary + supporting agents
3. Structure output to integrate all dimensions
</routing_logic>

<mid_research_steering>
## Mid-Research Steering

During the diffusion loop, watch for user steering:

| User Says | Action |
|-----------|--------|
| "Focus more on X" | Add X to next worker batch, prioritize in synthesis |
| "What about sanctions?" | Add sanctions-researcher to next round |
| "Go deeper on actors" | Spawn additional actor-mapper worker |
| "Skip narrative analysis" | Remove sentiment workers, note as out-of-scope |
| "That's enough" | Skip remaining iterations, produce final report |
| "Add country Y" | Update geographic scope, spawn workers for Y |

Use AskUserQuestion if intent is ambiguous:

```
AskUserQuestion(
  questions: [{
    header: "Clarify Focus",
    question: "You mentioned X. Should I...",
    options: [
      { label: "Add dedicated analysis", description: "Spawn specialist worker for X" },
      { label: "Include in current analysis", description: "Cover X within current scope" },
      { label: "Replace current focus", description: "Shift primary focus to X" }
    ],
    multiSelect: false
  }]
)
```
</mid_research_steering>

<output_specifications>
## Output File Location

Save reports to: `research_output/geo/[topic-slug]_[date].md`

Example: `research_output/geo/russia-ukraine-conflict_2024-01-15.md`

## Required Sections (All Reports)

1. **Metadata Header**
   - Query
   - Analysis type
   - Date
   - Iterations
   - Coverage score
   - Confidence level

2. **Executive Summary** (3-5 bullet points)

3. **Type-Specific Content** (varies by analysis type)

4. **Quantitative GDELT Data** (always include raw metrics)

5. **Confidence Assessment**
   - Data quality
   - Coverage completeness
   - Analytical confidence
   - Known limitations

6. **Sources**
   - GDELT queries with parameters
   - News URLs with descriptions
   - Expert/official sources

7. **Methodology Note** (brief)
</output_specifications>

<success_criteria>
## Research Completion Criteria

Research is complete when:

**Data Requirements:**
- All core questions from brief are addressed with GDELT data
- Weighted coverage score >= 70% (from gap-detector-geo)
- Key claims have quantitative GDELT citations
- At least 2 source types used (events, GKG, news)

**Quality Requirements:**
- All major actors/stakeholders represented
- Temporal scope adequately covered (historical + current)
- Contradictions noted and explained
- Confidence levels clearly stated

**Stop Conditions:**
- Maximum 3 iterations reached
- User requests early stop
- Diminishing returns (gap detector shows < 5% improvement potential)

**NOT sufficient for completion:**
- Draft "reads well" subjectively
- Only web sources used (must have GDELT data)
- Single perspective represented
- Missing quantitative data for key claims
</success_criteria>

<quick_start>
## Quick Start

1. User provides geopolitical research query
2. Classify query type (conflict/sanctions/actors/narrative)
3. Generate DRAFT research brief
4. **Use AskUserQuestion to validate type, scope, depth**
5. Refine brief based on feedback
6. Spawn 2-4 specialist agents in parallel
7. Synthesize findings with GDELT data
8. Spawn gap-detector-geo agent
9. If gaps found: spawn targeted workers, repeat
10. If complete: generate final report

**Time expectation:** 3-12 minutes depending on depth and iterations

**Skip refinement:** If user says "just do it" or "quick analysis", proceed with best judgment on the brief.
</quick_start>
