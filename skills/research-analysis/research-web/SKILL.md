---
name: research-web
description: 'Deep web research with parallel investigators, multi-wave exploration, and structured synthesis. Spawns multiple web-researcher agents to explore different facets of a topic simultaneously, launches additional waves when gaps are identified, then synthesizes findings. Use when asked to research, investigate, compare options, find best practices, or gather comprehensive information from the web.\n\nThoroughness: quick for factual lookups | medium for focused topics | thorough for comparisons/evaluations (waves continue while critical gaps remain) | very-thorough for comprehensive research (waves continue until satisficed). Auto-selects if not specified.'
context: fork
---

**Research request**: $ARGUMENTS

# Thoroughness Level

**FIRST**: Determine thoroughness before researching. Parse from natural language (e.g., "quick lookup", "thorough research", "comprehensive analysis") or auto-select based on query characteristics.

**Auto-selection logic**:
- Single fact/definition/date → quick
- Focused question about one topic → medium
- Comparison, evaluation, or "best" questions → thorough
- "comprehensive"/"all options"/"complete analysis"/"deep dive" → very-thorough

**Explicit user preference**: If user explicitly specifies a thoroughness level (e.g., "do a quick lookup", "thorough research on X"), honor that request regardless of other triggers in the query.

**Trigger conflicts (auto-selection only)**: When auto-selecting and query contains triggers from multiple levels, use the highest level indicated (very-thorough > thorough > medium > quick).

| Level | Agents/Wave | Wave Policy | Behavior | Triggers |
|-------|-------------|-------------|----------|----------|
| **quick** | 1 | Single wave | Single web-researcher, no orchestration file, direct answer | "what is", "when did", factual lookups, definitions |
| **medium** | 1-2 | Single wave | Orchestration file, focused research on 1-2 angles | specific how-to, single technology, focused question |
| **thorough** | 2-4 | Continue while critical gaps remain | Full logging, parallel agents, cross-reference, follow-up waves for critical gaps | "compare", "best options", "evaluate", "pros and cons" |
| **very-thorough** | 4-6 | Continue until comprehensive OR diminishing returns | Multi-wave research until all significant gaps addressed or new waves stop yielding value | "comprehensive", "complete analysis", "all alternatives", "deep dive" |

**Multi-wave research**: For thorough and very-thorough levels, research continues in waves until satisficing criteria are met. Each wave can spawn new investigators to address gaps, conflicts, or newly discovered areas from previous waves. There is no hard maximum - waves continue as long as they're productive and gaps remain at the triggering threshold.

**Ambiguous queries**: If thoroughness cannot be determined AND the query is complex (involves comparison, evaluation, or multiple facets), ask the user:

```
I can research this at different depths:
- **medium**: Focused research on core aspects (~3-5 min)
- **thorough**: Multi-angle investigation with cross-referencing (~8-12 min)
- **very-thorough**: Comprehensive analysis covering all facets (~15-20 min)

Which level would you prefer? (Or I can auto-select based on your query)
```

State: `**Thoroughness**: [level] — [reason]` then proceed.

---

# Deep Web Research Skill

Orchestrate parallel web researchers to comprehensively investigate a topic through iterative waves, then synthesize findings into actionable intelligence.

**Loop**: Determine thoroughness → Decompose topic → Launch Wave 1 → Collect findings → Evaluate gaps → [If gaps significant AND waves remaining: Launch next wave → Collect → Evaluate → Repeat] → Synthesize → Output

**Orchestration file**: `/tmp/research-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md` - external memory for tracking multi-wave research progress and synthesis.

---

# Satisficing Criteria

Research continues in waves until satisficing criteria are met for the given thoroughness level.

## Wave Continuation by Level

| Level | Continue When | Stop When (Satisficed) |
|-------|---------------|------------------------|
| quick | N/A | Always single wave |
| medium | N/A | Always single wave |
| thorough | Critical gaps remain AND previous wave was productive AND ≤50% source overlap with prior waves | No critical gaps OR diminishing returns OR >50% source overlap |
| very-thorough | Significant gaps remain AND previous wave was productive AND ≤50% source overlap with prior waves | Comprehensive coverage (no significant gaps) OR diminishing returns OR >50% source overlap |

**No hard maximum**: For thorough and very-thorough, waves continue based on necessity, not arbitrary limits. The satisficing criteria drive when to stop.

**Source overlap**: Percentage of sources in current wave that were also cited in any previous wave. >50% overlap indicates research is cycling through same sources.

## Gap Classification

After each wave, classify identified gaps:

| Gap Type | Definition | Triggers New Wave? |
|----------|------------|-------------------|
| **Critical** | Core question aspect unanswered, major conflicts unresolved, key comparison missing | Yes (thorough, very-thorough) |
| **Significant** | Important facet unexplored, partial answer needs depth, newly discovered area | Yes (very-thorough only) |
| **Minor** | Nice-to-have detail, edge case unclear, tangential info | No - note in limitations |

## Satisficing Evaluation

After Phase 4 (Cross-Reference), evaluate whether to continue:

**Definitions**:
- **Finding**: A distinct piece of information answering part of the research question, with at least one source citation. Multiple sources confirming the same fact count as one finding with higher confidence.
- **Substantive finding**: A finding that provides new information not already established in previous waves. Variations or restatements of known information do not count.
- **High-authority source**: Official documentation, peer-reviewed research, established news outlets (e.g., major tech publications), or sources from recognized domain experts. Company blogs about their own products count as high-authority for factual claims about that product.
- **Independent sources**: Sources with different underlying information origins. Two articles citing the same primary source count as one source. Multiple pages from the same domain count as one source unless they represent different authors/teams with distinct research.
- **High confidence**: Finding corroborated by ≥3 independent sources OR ≥2 high-authority sources.
- **Medium confidence**: Finding corroborated by 2 independent sources OR 1 high-authority source.
- **Low confidence**: Finding from a single non-authoritative source with no corroboration.
- **Medium+ confidence**: Confidence level of Medium or High (i.e., not Low, Contested, or Inconclusive).

**Satisficed when ANY true**:
- All critical gaps addressed (thorough) OR all significant gaps addressed (very-thorough)
- Diminishing returns detected: new wave revealed <2 new substantive findings AND no finding's confidence increased by at least one level AND no new areas discovered
- User explicitly requested stopping or a specific wave count
- Comprehensive coverage achieved: all identified facets addressed with medium+ confidence

**Continue when ALL true**:
- Gaps exist at the triggering threshold:
  - thorough: Critical gaps remain (core question unanswered, major conflicts)
  - very-thorough: Significant gaps remain (important facets unexplored, conflicts, newly discovered areas)
- Previous wave was productive (≥2 new substantive findings OR ≥1 finding's confidence increased by at least one level OR new areas discovered)
- Research is still yielding value (≤50% of sources in this wave were cited in previous waves)

## Wave Planning

When continuing to a new wave:
1. Identify specific gaps to address (from Cross-Reference Analysis)
2. Design targeted research prompts for each gap
3. Assign 1-3 agents per wave (focused investigation)
4. Update orchestration file with wave number and assignments
5. Launch agents and collect findings
6. Return to gap evaluation

**Topic-slug format**: Extract 2-4 key terms (nouns and adjectives that identify the topic; exclude articles, prepositions, and generic words like "best", "options", "analysis"), lowercase, replace spaces with hyphens. Example: "best real-time database options 2025" → `real-time-database-options`

**Timestamp format**: `YYYYMMDD-HHMMSS`. Obtain via `date +%Y%m%d-%H%M%S`.

## Phase 1: Initial Setup (skip for quick)

### 1.1 Get timestamp & create todo list

Run two commands:
- `date +%Y%m%d-%H%M%S` → for filename timestamp (e.g., `20260112-060615`)
- `date '+%Y-%m-%d %H:%M:%S'` → for human-readable "Started" field (e.g., `2026-01-12 06:06:15`)

Todos = **research areas to investigate + write-to-log operations**, not fixed steps. Each research todo represents a distinct angle or facet. List expands as decomposition reveals new areas. Write-to-log todos ensure external memory stays current.

**Starter todos** (seeds - list grows during decomposition):

```
- [ ] Create orchestration file; done when file created
- [ ] Topic decomposition→log; done when all facets identified
- [ ] (expand: research facets as decomposition reveals)
- [ ] Launch Wave 1 agents; done when all agents spawned
- [ ] Collect Wave 1 findings→log; done when all agents returned
- [ ] Cross-reference findings→log; done when agreements/conflicts mapped
- [ ] Evaluate gaps→log; done when gaps classified
- [ ] (expand: Wave 2+ if continuing)
- [ ] Refresh: read full orchestration file
- [ ] Synthesize→final output; done when all findings integrated + sourced
```

**Critical todos** (never skip):
- `→log` after EACH phase/agent completion
- `Refresh:` ALWAYS before synthesis

**Expansion pattern**: As decomposition reveals facets, add research todos:
```
- [x] Create orchestration file; file created
- [x] Topic decomposition→log; 4 facets identified
- [ ] Research: real-time database landscape 2025; done when options cataloged
- [ ] Research: performance benchmarks; done when latency/throughput data found
- [ ] Research: conflict resolution strategies; done when CRDT/OT patterns documented
- [ ] Research: production case studies; done when 3+ cases collected
- [ ] Launch Wave 1 agents (4 parallel); done when all agents spawned
- [ ] Collect Agent 1→log; done when findings written
- [ ] Collect Agent 2→log; done when findings written
- [ ] Collect Agent 3→log; done when findings written
- [ ] Collect Agent 4→log; done when findings written
- [ ] Cross-reference→log; done when agreements/conflicts mapped
- [ ] Evaluate gaps→log; done when gaps classified
- [ ] (expand: Wave 2 if continuing)
- [ ] Refresh: read full orchestration file
- [ ] Synthesize→final output; done when all findings integrated + sourced
```

### 1.2 Create orchestration file (skip for quick)

Path: `/tmp/research-orchestration-{topic-slug}-{YYYYMMDD-HHMMSS}.md`

```markdown
# Web Research Orchestration: {topic}
Timestamp: {YYYYMMDD-HHMMSS}
Started: {YYYY-MM-DD HH:MM:SS}
Thoroughness: {level}
Wave Policy: {single wave | continue while critical gaps | continue until comprehensive}

## Research Question
{Clear statement of what needs to be researched}

## Topic Decomposition
- Core question: {main thing to answer}
- Facets to investigate: (populated in Phase 2)
- Expected researcher count: {based on thoroughness level}

## Wave Tracking
| Wave | Agents | Focus | Status | New Findings | Decision |
|------|--------|-------|--------|--------------|----------|
| 1 | {count} | Initial investigation | Pending | - | - |

## Research Assignments
(populated in Phase 2)

## Agent Status
(updated as agents complete)

## Collected Findings
(populated as agents return)

## Cross-Reference Analysis
(populated after each wave)

## Gap Evaluation
(populated after each wave - drives continuation decisions)

## Synthesis Notes
(populated in final phase)
```

## Phase 2: Topic Decomposition & Agent Assignment

### 2.1 Decompose the research topic into ORTHOGONAL facets

Before launching agents, analyze the query to identify **non-overlapping** research angles. Each agent should have a distinct domain with clear boundaries.

1. **Core question**: What is the fundamental thing being asked?
2. **Facets**: What distinct aspects need investigation? Ensure minimal overlap:
   - Technical aspects (how it works, implementation details)
   - Comparison aspects (alternatives, competitors, trade-offs)
   - Practical aspects (real-world usage, adoption, case studies)
   - Current state (recent developments, 2025 updates)
   - Limitations/concerns (drawbacks, issues, criticisms)

3. **Orthogonality check**: Before assigning agents, verify:
   - Each facet covers a distinct domain
   - No two facets would naturally search the same queries
   - Boundaries are clear enough to state explicitly

**Bad decomposition** (overlapping):
- Agent 1: "Research Firebase"
- Agent 2: "Research real-time databases" ← Firebase is a real-time database, overlap!

**Good decomposition** (orthogonal):
- Agent 1: "Research Firebase specifically - features, pricing, limits"
- Agent 2: "Research non-Firebase alternatives: Supabase, Convex, PlanetScale"

### 2.2 Plan agent assignments with explicit boundaries

| Facet | Research Focus | Explicitly EXCLUDE |
|-------|----------------|-------------------|
| {facet 1} | "{what to research}" | "{what other agents cover}" |
| {facet 2} | "{what to research}" | "{what other agents cover}" |

**Agent count by level**:
- medium: 1-2 agents (core + one related angle)
- thorough: 2-4 agents (core + alternatives + practical + concerns)
- very-thorough: 4-6 agents (comprehensive coverage of all facets)

**If decomposition reveals more facets than agent count allows**:
- Prioritize facets by: (1) directly answers core question, (2) enables comparison if requested, (3) addresses user-specified concerns
- Combine related facets into single agent assignments where orthogonality allows
- Schedule remaining facets for Wave 2 if initial wave is productive

**Orthogonality strategies**:
- By entity: Agent 1 = Product A, Agent 2 = Product B (not both "products")
- By dimension: Agent 1 = Performance, Agent 2 = Pricing, Agent 3 = Security
- By time: Agent 1 = Current state, Agent 2 = Historical evolution
- By perspective: Agent 1 = Official docs, Agent 2 = Community experience

### 2.3 Expand todos for each research area

Add a todo for each planned agent assignment:

```
- [x] Topic decomposition & research planning
- [ ] Research: {facet 1 description}
- [ ] Research: {facet 2 description}
- [ ] Research: {facet 3 description}
- [ ] ...
- [ ] Collect and cross-reference findings
- [ ] Synthesize final output
```

### 2.4 Update orchestration file

After decomposition, update the file:

```markdown
## Topic Decomposition
- Core question: {main question}
- Facets identified:
  1. {facet 1}: {why this angle matters}
  2. {facet 2}: {why this angle matters}
  ...

## Research Assignments
| Agent | Facet | Prompt | Status |
|-------|-------|--------|--------|
| 1 | {facet} | "{prompt}" | Pending |
| 2 | {facet} | "{prompt}" | Pending |
...
```

## Phase 3: Launch Parallel Researchers

### 3.1 Launch web-researcher agents

Use Task tool with `subagent_type: "vibe-workflow:web-researcher"` for each research angle. **Launch agents in parallel** (single message with multiple Task tool calls) to maximize efficiency.

**Wave 1 prompt template** (broad exploration with boundaries):
```
{Specific research question for this facet}

YOUR ASSIGNED SCOPE:
- Focus areas: {specific aspect 1}, {specific aspect 2}, {specific aspect 3}
- This is YOUR domain - go deep on these topics

DO NOT RESEARCH (other agents cover these):
- {facet assigned to Agent 2}
- {facet assigned to Agent 3}
- {etc.}

Current date context: {YYYY-MM-DD} - prioritize recent sources.

---
Research context:
- Wave: 1 (initial investigation)
- Mode: Broad exploration within your assigned scope
- Stay within your boundaries - other agents handle the excluded areas
- Report any gaps or conflicts you discover for potential follow-up waves
```

**Wave 2+ prompt template** (gap-filling):
```
{Specific gap or conflict to resolve}

Context from previous waves:
- Previous findings: {summary of relevant findings from earlier waves}
- Gap being addressed: {specific gap - e.g., "Sources conflict on X" or "Y aspect unexplored"}
- What we already know: {established facts from Wave 1}

YOUR ASSIGNED SCOPE:
- Focus narrowly on: {targeted aspect 1}, {targeted aspect 2}
- This gap was identified because: {why previous research was insufficient}

DO NOT RESEARCH:
- Topics already well-covered in Wave 1 (don't repeat)
- {areas other Wave 2 agents are handling}

Current date context: {YYYY-MM-DD} - prioritize recent sources.

---
Research context:
- Wave: {N} (gap-filling)
- Mode: Targeted investigation - focus narrowly on the gap above
- Build on previous findings, don't repeat broad exploration
- Flag if this gap cannot be resolved (conflicting authoritative sources, no data available, etc.)
```

**Batching rules**:
- thorough: Launch all 2-4 agents in a single parallel batch
- very-thorough: Launch in batches of 3-4 agents; for 5 agents use 3+2, for 6 agents use 3+3 (avoid overwhelming context)
- Wave 2+: Launch 1-3 focused agents per wave

### 3.2 Update orchestration file after each agent completes

After EACH agent returns, immediately update:

```markdown
## Agent Status
| Agent | Facet | Status | Key Finding |
|-------|-------|--------|-------------|
| 1 | {facet} | Complete | {1-sentence summary} |
| 2 | {facet} | Complete | {1-sentence summary} |
...

## Collected Findings

### Agent 1: {facet}
**Confidence**: {High/Medium/Low/Contested/Inconclusive}
**Sources**: {count}

{Paste key findings from agent - preserve source citations}
{If Contested: note the conflicting positions}
{If Inconclusive: note what couldn't be determined}

### Agent 2: {facet}
...
```

### 3.3 Handle agent failures

If an agent times out or returns incomplete results:
1. Note the gap in orchestration file
2. Decide based on facet criticality:
   - **Retry** (narrower prompt) if: facet covers a Critical gap for the research question, OR facet is explicitly required by the research question for comparison/evaluation (e.g., query asks to compare X and Y, and facet covers X or Y), OR user explicitly requested this facet
   - **Mark as gap** (don't retry) if: facet covers a Significant or Minor gap, OR other agents partially covered the topic, OR research can synthesize without this facet
3. Never block synthesis for a single failed agent - proceed with available findings and note the limitation
4. If ALL agents in a wave fail:
   - For Wave 1: Retry with simpler decomposition (fewer agents, broader prompts)
   - For Wave 2+: Mark gaps as unresolvable, proceed to synthesis with prior wave findings
   - Always note the systemic failure in Gaps & Limitations

## Phase 4: Collect, Cross-Reference & Evaluate Gaps

### 4.1 Mark collection todo in_progress

### 4.2 Analyze findings across agents

Look for:
- **Agreements**: Where do multiple agents reach similar conclusions?
- **Conflicts**: Where do findings contradict? (includes agent-reported "Contested" findings)
- **Inconclusive**: Areas where agents couldn't determine answers
- **Gaps**: What wasn't covered by any agent?
- **Surprises**: Unexpected findings that warrant highlighting

**Handling agent confidence levels**:
- **High/Medium/Low**: Standard confidence - use for cross-referencing
- **Contested**: Agent found high-authority sources that directly contradict each other - treat as a conflict requiring resolution or presentation of both positions
- **Inconclusive**: Agent couldn't find agreement among sources - may warrant follow-up wave with different search angles

### 4.3 Update orchestration file with cross-reference

```markdown
## Cross-Reference Analysis

### Agreements (High Confidence)
- {Finding}: Supported by agents {1, 3, 4}
- {Finding}: Confirmed across {count} sources

### Conflicts (Requires Judgment)
- {Topic}: Agent 1 says X, Agent 3 says Y
  - Resolution: {which to trust and why, or present both}
- {Topic}: Agent 2 reported as Contested - {Position A} vs {Position B}
  - Resolution: {present both with supporting sources, or identify which is more authoritative}

### Inconclusive Areas
- {Topic}: Agent {N} couldn't determine - {reason}
  - Action: {follow-up wave with different angles, or note as limitation}

### Gaps Identified
- {What wasn't answered}
- {Areas needing more research}

### Key Insights
- {Synthesis observation 1}
- {Synthesis observation 2}
```

### 4.4 Evaluate gaps and decide next wave (skip for quick/medium)

**For thorough and very-thorough levels**, classify each gap:

```markdown
## Gap Evaluation (Wave {N})

### Critical Gaps (triggers thorough/very-thorough continuation)
- [ ] {Gap}: {Why critical - core question aspect unanswered}
- [ ] {Gap}: {Why critical - major conflict unresolved}

### Significant Gaps (triggers very-thorough continuation)
- [ ] {Gap}: {Why significant - important facet unexplored}
- [ ] {Gap}: {Why significant - partial answer needs depth}
- [ ] {Gap}: {Why significant - newly discovered area worth exploring}

### Minor Gaps (note in limitations, don't pursue)
- {Gap}: {Why minor - nice-to-have detail}

### Wave Productivity Assessment
- New substantive findings this wave: {count}
- Confidence improvements: {which areas improved}
- New areas discovered: {list or "none"}
- Diminishing returns signals: {yes/no - explain}

### Wave Decision
- Current wave: {N}
- Thoroughness level: {level}
- Wave policy: {single wave | continue while critical gaps | continue until comprehensive}
- Critical gaps remaining: {count}
- Significant gaps remaining: {count}
- Was this wave productive? {yes/no - ≥2 findings OR confidence improved OR new areas}
- **Decision**: {CONTINUE to Wave N+1 | SATISFICED - proceed to synthesis}
- **Reason**: {explain based on satisficing criteria - what gaps remain or why comprehensive}
```

### 4.5 Wave Decision Logic

**If SATISFICED** (any of these true):
- Level is quick or medium → Proceed to Phase 5
- No critical gaps (thorough) or no significant gaps (very-thorough) → Proceed to Phase 5
- Diminishing returns: previous wave yielded <2 new substantive findings AND no finding's confidence increased by at least one level AND no new areas discovered → Proceed to Phase 5
- Comprehensive coverage achieved: all identified facets addressed with medium+ confidence → Proceed to Phase 5
- User explicitly requested stopping

**If CONTINUE** (all of these true):
- Gaps exist at triggering threshold:
  - thorough: Critical gaps remain
  - very-thorough: Significant gaps remain
- Previous wave was productive (≥2 new substantive findings OR ≥1 finding's confidence increased by at least one level OR new areas discovered)
- Not cycling through same sources (≤50% of sources in this wave were cited in previous waves)

### 4.6 Launch Next Wave (if continuing)

When continuing to a new wave:

1. **Update Wave Tracking table** in orchestration file:
```markdown
## Wave Tracking
| Wave | Agents | Focus | Status | New Findings |
|------|--------|-------|--------|--------------|
| 1 | 4 | Initial investigation | Complete | 12 findings |
| 2 | 2 | Gap-filling: {focus areas} | In Progress | - |
```

2. **Add wave-specific todos**:
```
- [ ] Wave 2: Investigate {critical gap 1}
- [ ] Wave 2: Resolve conflict on {topic}
- [ ] Wave 2: Deep-dive {significant gap}
```

3. **Design targeted prompts** for gaps:
   - Be specific: "Resolve conflict between X and Y regarding Z"
   - Include context: "Previous research found A, but need clarification on B"
   - Narrower scope than Wave 1 agents

4. **Launch 1-3 agents** for this wave (focused investigation)
   - Use Task tool with `subagent_type: "vibe-workflow:web-researcher"`
   - Prompts reference specific gaps, not broad topics

5. **Collect findings** and return to 4.2 (cross-reference including new findings)

### 4.7 Mark collection todo complete (when proceeding to synthesis)

## Phase 5: Synthesize & Output

### 5.1 Refresh context (MANDATORY - never skip)

**CRITICAL**: Read the FULL orchestration file using the Read tool to restore ALL findings, cross-references, gap evaluations, and wave tracking into context.

**Why this matters**: By this point, findings from multiple agents across potentially multiple waves have been written to the orchestration file. Context degradation means these details may have faded. Reading the full file immediately before synthesis brings all findings into recent context where attention is strongest.

**Todo must show**:
```
- [x] Refresh context: read full orchestration file  ← Must be marked complete before synthesis
- [ ] Synthesize final output
```

**Verification**: After reading, you should have access to:
- All collected findings from every agent
- Cross-reference analysis (agreements, conflicts, inconclusive)
- Gap evaluations from each wave
- Wave tracking with decisions
- All source citations

### 5.2 Mark synthesis todo in_progress

### 5.3 Generate comprehensive output

**Only after completing 5.1** - synthesize ALL agent findings into a cohesive answer. Include:

```markdown
## Research Findings: {Topic}

**Thoroughness**: {level} | **Waves**: {count} | **Researchers**: {total across waves} | **Total Sources**: {aggregate}
**Overall Confidence**: High/Medium/Low (based on agreement and source quality)
**Satisficing**: {reason research concluded - e.g., "All significant gaps addressed" or "Diminishing returns after Wave 3"}

### Executive Summary
{4-8 sentences synthesizing the key takeaway. What does the user need to know?}

### Detailed Findings

#### {Major Finding Area 1}
{Synthesized insights with inline source citations from multiple agents}

#### {Major Finding Area 2}
{...}

### Comparison/Evaluation (if applicable)
| Option | Pros | Cons | Best For |
|--------|------|------|----------|
| {opt 1} | {from agents} | {from agents} | {synthesis} |
| {opt 2} | {from agents} | {from agents} | {synthesis} |

### Recommendations
{Based on synthesized evidence - what should the user consider/do?}

### Confidence Notes
- **High confidence**: {findings with strong multi-source agreement}
- **Medium confidence**: {findings with some support}
- **Contested**: {where high-authority sources directly contradicted - present both positions}
- **Inconclusive**: {where agents couldn't determine answers despite searching}
- **Low confidence**: {single source or weak agreement}

### Research Progression (for multi-wave)
| Wave | Focus | Agents | Key Contribution |
|------|-------|--------|------------------|
| 1 | Initial investigation | {N} | {what this wave established} |
| 2 | {Gap focus} | {N} | {what this wave resolved} |
| ... | ... | ... | ... |

### Gaps & Limitations
- {What couldn't be definitively answered despite multi-wave investigation}
- {Areas where more research would help}
- {Potential biases in available sources}
- {Gaps intentionally not pursued (minor priority)}

### Source Summary
| Source | Authority | Date | Used For | Wave |
|--------|-----------|------|----------|------|
| {url} | High/Med | {date} | {finding} | 1 |
...

---
Orchestration file: {path}
Research completed: {timestamp}
```

### 5.4 Mark all todos complete

## Quick Mode Flow

For quick (single-fact) queries, skip orchestration:

1. State: `**Thoroughness**: quick — [reason]`
2. Launch single web-researcher agent: `Task("vibe-workflow:web-researcher", "{query}")`
3. Return agent's findings directly (no synthesis overhead)

## Key Principles

| Principle | Rule |
|-----------|------|
| Thoroughness first | Determine level before any research |
| Todos with write-to-log | Each collection gets a todo, followed by a write-to-orchestration-file todo |
| Write after each phase | Write to orchestration file after EACH phase/agent |
| Parallel execution | Launch multiple agents simultaneously when possible |
| Cross-reference | Compare findings across agents before synthesizing |
| Gap evaluation | Classify gaps after each wave (critical/significant/minor) |
| Wave iteration | Continue waves until satisficed OR diminishing returns |
| **Context refresh** | **Read full orchestration file BEFORE synthesis - non-negotiable** |
| Source preservation | Maintain citations through synthesis |
| Gap honesty | Explicitly state what couldn't be answered despite multi-wave effort |

**Log Pattern Summary**:
1. Create orchestration file at start
2. Add write-to-log todos after each collection phase
3. Write to it after EVERY step (decomposition, agent findings, cross-reference, gap evaluation)
4. "Refresh context: read full orchestration file" todo before synthesis
5. Read FULL file before synthesis (restores all context)

## Never Do

- Launch agents without determining thoroughness level
- Skip write-to-log todos (every collection must be followed by a write todo)
- Proceed to next phase without writing findings to orchestration file
- Synthesize without completing "Refresh context: read full orchestration file" todo first
- Skip orchestration file updates after agent completions
- Present synthesized findings without source citations
- Ignore conflicts between agent findings (especially "Contested" findings)
- Skip gap evaluation for thorough/very-thorough levels
- Continue waves when diminishing returns detected (wasted effort)
- Stop prematurely when critical gaps remain (thorough) or significant gaps remain (very-thorough) and waves are still productive

## Example: Technology Comparison

Query: "Compare the best real-time databases for a collaborative app in 2025"

**Thoroughness**: thorough — comparison query requiring multi-angle investigation

**Decomposition**:
- Facet 1: Real-time database landscape 2025 (what options exist)
- Facet 2: Performance and scalability comparisons
- Facet 3: Collaborative app requirements (conflict resolution, sync)
- Facet 4: Production experiences and case studies

**Agents launched** (parallel):
1. "Real-time database options 2025: Firebase, Supabase, Convex, others. Current market landscape."
2. "Real-time database performance benchmarks and scalability. Latency, throughput, concurrent users."
3. "Conflict resolution and sync strategies for collaborative apps. CRDTs, OT, last-write-wins."
4. "Production case studies using real-time databases. Companies, scale, lessons learned."

**Output**: Synthesized comparison table with recommendations based on use case, backed by cross-referenced sources from all four agents.

## Example: Multi-Wave Comprehensive Research

Query: "Give me a comprehensive analysis of all the AI coding assistant options in 2025"

**Thoroughness**: very-thorough — "comprehensive analysis" + "all options" triggers maximum depth

### Wave 1: Initial Investigation
**Decomposition** (6 orthogonal facets):
- Facet 1: Market landscape - what tools exist (names only, no features/pricing)
- Facet 2: Feature comparison - autocomplete, chat, agents, IDE support (no pricing)
- Facet 3: Pricing and licensing - costs, tiers, enterprise deals (no features)
- Facet 4: Enterprise/security - compliance, SOC2, on-prem (no general features)
- Facet 5: Developer sentiment - reviews, community feedback (no official docs)
- Facet 6: Recent news - announcements, launches, acquisitions (no evergreen content)

**Agents launched with explicit boundaries** (parallel batch of 4, then 2):
1. "AI coding assistant market landscape 2025. YOUR SCOPE: List all tools (Copilot, Cursor, Claude Code, Codeium, etc). DO NOT RESEARCH: features, pricing, reviews."
2. "AI coding assistant features 2025. YOUR SCOPE: autocomplete, chat, agentic capabilities, IDE support. DO NOT RESEARCH: pricing, enterprise security, user reviews."
3. "AI coding assistant pricing 2025. YOUR SCOPE: subscription costs, usage-based models, free tiers. DO NOT RESEARCH: features, security compliance."
4. "Enterprise AI coding assistant compliance 2025. YOUR SCOPE: SOC2, HIPAA, on-premise, data residency. DO NOT RESEARCH: general features, consumer pricing."
5. "AI coding assistant developer sentiment 2025. YOUR SCOPE: Reddit, HN, Twitter discussions, community feedback. DO NOT RESEARCH: official documentation, pricing pages."
6. "AI coding assistant news 2025. YOUR SCOPE: recent announcements, launches, acquisitions since Jan 2025. DO NOT RESEARCH: established features, pricing."

**Gap Evaluation (Wave 1)**:
- Critical gaps: None (all facets had substantial findings)
- Significant gaps:
  - Conflict: Sources disagree on which tool has best agentic capabilities
  - Partial answer: Enterprise pricing not fully detailed for all options
  - New discovery: Several sources mention "AI code review" as emerging category
- Minor gaps: Specific latency benchmarks, rare IDE integrations

**Wave Decision**: CONTINUE — 3 significant gaps remain, Wave 1 was productive (18 findings), research still yielding new information

### Wave 2: Gap-Filling
**Focus**: Resolve agentic capabilities conflict, deepen enterprise pricing, explore AI code review

**Agents launched** (3 focused):
1. "Compare agentic capabilities: Cursor Composer vs Claude Code vs GitHub Copilot Workspace 2025"
2. "Enterprise AI coding assistant pricing 2025: Copilot Business, Cursor Teams, volume discounts"
3. "AI code review tools 2025: CodeRabbit, Sourcery, Codacy AI. Emerging category analysis."

**Gap Evaluation (Wave 2)**:
- Critical gaps: None
- Significant gaps: None remaining (conflict resolved, enterprise pricing clarified)
- Minor gaps: Some niche tools not fully covered

**Wave Decision**: SATISFICED — No significant gaps remaining, 2 waves complete

### Output Summary
**Thoroughness**: very-thorough | **Waves**: 2 | **Researchers**: 9 | **Sources**: 34
**Satisficing**: All significant gaps addressed — comprehensive coverage achieved
