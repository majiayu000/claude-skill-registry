---
name: ln-230-story-prioritizer
description: "RICE-scores Stories with market research and generates prioritization table. Use when Stories need business priority ranking for sprint planning."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

# Story Prioritizer

**Type:** L3 Worker
**Category:** 2XX Planning

Evaluate Stories using RICE scoring with market research. Generate consolidated prioritization table for Epic.

## Purpose & Scope

- Prioritize Stories AFTER ln-220 creates them
- Research market size and competition per Story
- Calculate RICE score for each Story
- Generate prioritization table (P0/P1/P2/P3)
- Output: docs/market/[epic-slug]/prioritization.md

## When to Use

**Use this skill when:**
- Stories created by ln-220, need business prioritization
- Planning sprint with limited capacity (which Stories first?)
- Stakeholder review requires data-driven priorities
- Evaluating feature ROI before implementation

**Do NOT use when:**
- Epic has no Stories yet (run ln-220 first)
- Stories are purely technical (infrastructure, refactoring)
- Prioritization already exists in docs/market/

**Who calls this skill:**
- **ln-200-scope-decomposer** Phase 4 (optional, sequential per Epic)
- **User (manual)** - standalone after ln-220-story-coordinator

---

## Input Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| epic | Yes | Epic ID or "Epic N" format | - |
| stories | No | Specific Story IDs to prioritize | All in Epic |
| depth | No | Research depth (quick/standard/deep) | "standard" |

**depth options:**
- `quick` - 2-3 min/Story, 1 WebSearch per type
- `standard` - 5-7 min/Story, 2-3 WebSearches per type
- `deep` - 8-10 min/Story, comprehensive research

---

## Output Structure

```
docs/market/[epic-slug]/
└── prioritization.md    # Consolidated table + RICE details + sources
```

**Table columns (from user requirements):**

| Priority | Customer Problem | Feature | Solution | Rationale | Impact | Market | Sources | Competition |
|----------|------------------|---------|----------|-----------|--------|--------|---------|-------------|
| P0 | User pain point | Story title | Technical approach | Why important | Business impact | $XB | [Link] | Blue 1-3 / Red 4-5 |

---

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `epicId` | Yes | args, kanban, user | Epic to process |

**Resolution:** Epic Resolution Chain.
**Status filter:** Active (planned/started)

## Tools Config

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider

## Research Tools

| Tool | Purpose | Example Query |
|------|---------|---------------|
| **WebSearch** | Market size, competitors | "[domain] market size {current_year}" |
| **mcp__Ref** | Industry reports | "[domain] market analysis report" |
| **Task provider** | Load Stories | IF linear: list_issues / ELSE: Glob story.md |
| **Glob** | Check existing | "docs/market/[epic]/*" |

---

## Workflow

### Phase 1: Discovery (2 min)

**Objective:** Validate input and prepare context.

**Process:**

1. **Resolve epicId:** Run Epic Resolution Chain per guide.

2. **Load Epic details:**
   - **IF task_provider == "linear":** `get_project(query=epicId)`
   - **ELSE IF task_provider == "github":** `gh issue view {epicId} -R {REPO} --json number,title,body`
   - **ELSE:** `Read("docs/tasks/epics/epic-{N}-*/epic.md")`
   - Extract: Epic ID, title, description

3. **Auto-discover configuration:**
   - Read `docs/tasks/kanban_board.md` for Team ID
   - Slugify Epic title for output path

4. **Check existing prioritization:**
   ```
   Glob: docs/market/[epic-slug]/prioritization.md
   ```
   - If exists: Ask "Update existing or create new?"
   - If new: Continue

5. **Create output directory:**
   ```bash
   mkdir -p docs/market/[epic-slug]/
   ```

**Output:** Epic metadata, output path, existing check result

---

### Phase 2: Load Stories Metadata (3 min)

**Objective:** Build Story queue with metadata only (token efficiency).

**Process:**

1. **Query Stories from Epic:**
   **IF task_provider == "linear":**
   ```
   list_issues(project=Epic.id, label="user-story")
   ```
   **ELSE IF task_provider == "github":**
   ```
   gh api /repos/{O}/{R}/issues/{epic_num}/sub_issues --jq '.[].number'
   → for each: gh issue view {num} -R {REPO} --json number,title,state,labels
   → filter: label "user-story"
   ```
   **ELSE (file mode):**
   ```
   Glob("docs/tasks/epics/epic-{N}-*/stories/*/story.md")
   ```

2. **Extract metadata only:**
   - Story ID, title, status
   - **DO NOT** load full descriptions yet

3. **Filter Stories:**
   - Exclude: Done, Cancelled, Archived
   - Include: Backlog, Todo, In Progress

4. **Build processing queue:**
   - Order by: existing priority (if any), then by ID
   - Count: N Stories to process

**Output:** Story queue (ID + title), ~50 tokens/Story

---

### Phase 3: Story-by-Story Analysis Loop (5-10 min/Story)

**Objective:** For EACH Story: load description, research, score RICE.

**Critical:** Process Stories ONE BY ONE for token efficiency!

#### Per-Story Steps:

##### Step 3.1: Load Story Description

**IF task_provider == "linear":**
```
get_issue(id=storyId, includeRelations=false)
```

**ELSE IF task_provider == "github":**
```
gh issue view {storyId} -R {REPO} --json number,title,body,state,labels
```

**ELSE (file mode):**
```
Read("docs/tasks/epics/epic-{N}-*/stories/us{NNN}-*/story.md")
```

**Extract from Story:**
- **Feature:** Story title
- **Customer Problem:** From "So that [value]" + Context section
- **Solution:** From Technical Notes (implementation approach)
- **Rationale:** From AC + Success Criteria

##### Step 3.2: Research Market Size

**WebSearch queries (based on depth):**
```
"[customer problem domain] market size TAM {current_year}"
"[feature type] industry market forecast"
```

**mcp__Ref query:**
```
"[domain] market analysis Gartner Statista"
```

**Extract:**
- Market size: $XB (with unit: B=Billion, M=Million)
- Growth rate: X% CAGR
- Sources: URL + date

**Confidence mapping:**
- Industry report (Gartner, Statista) → Confidence 0.9-1.0
- News article → Confidence 0.7-0.8
- Blog/Forum → Confidence 0.5-0.6

##### Step 3.3: Research Competition

**WebSearch queries:**
```
"[feature] competitors alternatives {current_year}"
"[solution approach] market leaders"
```

**Count competitors and classify:**

| Competitors Found | Competition Index | Ocean Type |
|-------------------|-------------------|------------|
| 0 | 1 | Blue Ocean |
| 1-2 | 2 | Emerging |
| 3-5 | 3 | Growing |
| 6-10 | 4 | Mature |
| >10 | 5 | Red Ocean |

##### Step 3.4: Calculate RICE Score

```
RICE = (Reach x Impact x Confidence) / Effort
```

**Reach (1-10):** Users affected per quarter
| Score | Users | Indicators |
|-------|-------|------------|
| 1-2 | <500 | Niche, single persona |
| 3-4 | 500-2K | Department-level |
| 5-6 | 2K-5K | Organization-wide |
| 7-8 | 5K-10K | Multi-org |
| 9-10 | >10K | Platform-wide |

**Impact (0.25-3.0):** Business value
| Score | Level | Indicators |
|-------|-------|------------|
| 0.25 | Minimal | Nice-to-have |
| 0.5 | Low | QoL improvement |
| 1.0 | Medium | Efficiency gain |
| 2.0 | High | Revenue driver |
| 3.0 | Massive | Strategic differentiator |

**Confidence (0.5-1.0):** Data quality (from Step 3.2)

**Data Confidence Assessment:**

For each RICE factor, assess data confidence level:

| Confidence | Criteria | Score Modifier |
|------------|----------|----------------|
| HIGH | Multiple authoritative sources (Gartner, Statista, SEC filings) | Factor used as-is |
| MEDIUM | 1-2 sources, mixed quality (blog + report) | Factor ±25% range shown |
| LOW | No sources, team estimate only | Factor ±50% range shown |

**Output:** Show confidence per factor in prioritization table + RICE range (optimistic/pessimistic) to make uncertainty explicit.

**Effort (1-10):** Person-months
| Score | Time | Story Indicators |
|-------|------|------------------|
| 1-2 | <2 weeks | 3 AC, simple CRUD |
| 3-4 | 2-4 weeks | 4 AC, integration |
| 5-6 | 1-2 months | 5 AC, complex logic |
| 7-8 | 2-3 months | External dependencies |
| 9-10 | 3+ months | New infrastructure |

##### Step 3.5: Determine Priority

| Priority | RICE Threshold | Competition Override |
|----------|----------------|---------------------|
| P0 (Critical) | >= 30 | OR Competition = 1 (Blue Ocean monopoly) |
| P1 (High) | >= 15 | OR Competition <= 2 (Emerging market) |
| P2 (Medium) | >= 5 | - |
| P3 (Low) | < 5 | Competition = 5 (Red Ocean) forces P3 |

##### Step 3.6: Store and Clear

- Append row to in-memory results table
- Clear Story description from context
- Move to next Story in queue

**Output per Story:** Complete row for prioritization table

---

### Phase 4: Generate Prioritization Table (5 min)

**Objective:** Create consolidated markdown output.

**Process:**

1. **Sort results:**
   - Primary: Priority (P0 → P3)
   - Secondary: RICE score (descending)

2. **Generate markdown:**
   - Use template from references/prioritization_template.md
   - Fill: Priority Summary, Main Table, RICE Details, Sources

3. **Save file:**
   ```
   Write: docs/market/[epic-slug]/prioritization.md
   ```

**Output:** Saved prioritization.md

---

### Phase 5: Summary & Next Steps (1 min)

**Objective:** Display results and recommendations.

**Output format:**
```
## Prioritization Complete

**Epic:** [Epic N - Name]
**Stories analyzed:** X
**Time elapsed:** Y minutes

### Priority Distribution:
- P0 (Critical): X Stories - Implement ASAP
- P1 (High): X Stories - Next sprint
- P2 (Medium): X Stories - Backlog
- P3 (Low): X Stories - Consider deferring

### Top 3 Priorities:
1. [Story Title] - RICE: X, Market: $XB, Competition: Blue/Red

### Saved to:
docs/market/[epic-slug]/prioritization.md

### Next Steps:
1. Review table with stakeholders
2. Run ln-300 for P0/P1 Stories first
3. Consider cutting P3 Stories
```

---

## Time-Box Constraints

| Depth | Per-Story | Total (10 Stories) |
|-------|-----------|-------------------|
| quick | 2-3 min | 20-30 min |
| standard | 5-7 min | 50-70 min |
| deep | 8-10 min | 80-100 min |

**Time management rules:**
- If Story exceeds time budget: Skip deep research, use estimates (Confidence 0.5)
- If total exceeds budget: Switch to "quick" depth for remaining Stories
- Parallel WebSearch where possible (market + competition)

---

## Token Efficiency

**Loading pattern:**
- Phase 2: Metadata only (~50 tokens/Story)
- Phase 3: Full description ONE BY ONE (~3,000-5,000 tokens/Story)
- After each Story: Clear description, keep only result row (~100 tokens)

**Memory management:**
- Sequential processing (not parallel)
- Maximum context: 1 Story description at a time
- Results accumulate as compact table rows

---

## Integration with Ecosystem

**Position in workflow:**
```
ln-210 (Scope → Epics)
     ↓
ln-220 (Epic → Stories)
     ↓
ln-230 (RICE per Story → prioritization table) ← THIS SKILL
     ↓
ln-300 (Story → Tasks)
```

**Dependencies:**
- WebSearch, mcp__Ref (market research)
- Task provider: Linear MCP or file mode (load Epic, Stories)
- Glob, Write, Bash (file operations)

**Downstream usage:**
- Sprint planning uses P0/P1 to select Stories
- ln-300 processes Stories in priority order
- Stakeholders review before implementation

---

## Critical Rules

1. **Source all data** - Every Market number needs source + date
2. **Prefer recent data** - last 2 years, warn if older
3. **Cross-reference** - 2+ sources for Market size (reduce error)
4. **Time-box strictly** - Skip depth for speed if needed
5. **Confidence levels** - Mark High/Medium/Low for estimates
6. **No speculation** - Only sourced claims, note "[No data]" gaps
7. **One Story at a time** - Token efficiency critical
8. **Preserve language** - If user asks in Russian, respond in Russian

---

## Definition of Done

- [ ] Epic validated (Linear or file mode)
- [ ] All Stories loaded (metadata, then descriptions per-Story)
- [ ] Market research completed (2+ sources per Story)
- [ ] RICE score calculated for each Story
- [ ] Competition index assigned (1-5)
- [ ] Priority assigned (P0/P1/P2/P3)
- [ ] Table sorted by Priority + RICE
- [ ] File saved to docs/market/[epic-slug]/prioritization.md
- [ ] Summary with top priorities and next steps
- [ ] Total time within budget

---

## Example Usage

**Basic usage:**
```
ln-230-story-prioritizer epic="Epic 7"
```

**With parameters:**
```
ln-230-story-prioritizer epic="Epic 7: Translation API" depth="deep"
```

**Specific Stories:**
```
ln-230-story-prioritizer epic="Epic 7" stories="US001,US002,US003"
```

**Example output (docs/market/translation-api/prioritization.md):**

| Priority | Customer Problem | Feature | Solution | Rationale | Impact | Market | Sources | Competition |
|----------|------------------|---------|----------|-----------|--------|--------|---------|-------------|
| P0 | "Repeat translations cost GPU" | Translation Memory | Redis cache, 5ms lookup | 70-90% GPU cost reduction | High | $2B+ | [M&M](link) | 3 |
| P0 | "Can't translate PDF" | PDF Support | PDF parsing + layout | Enterprise blocker | High | $10B+ | [Eden](link) | 5 |
| P1 | "Need video subtitles" | SRT/VTT Support | Timing preservation | Blue Ocean opportunity | Medium | $5.7B | [GMI](link) | 2 |

---

## Phase 6: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `planning-coordinator`. Run after all phases complete. Output to chat using the `planning-coordinator` format.

## Reference Files

- **MANDATORY READ:** `shared/references/environment_state_contract.md`
- **MANDATORY READ:** `shared/references/storage_mode_detection.md`
- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

| File | Purpose |
|------|---------|
| [prioritization_template.md](references/prioritization_template.md) | Output markdown template |
| [rice_scoring_guide.md](references/rice_scoring_guide.md) | RICE factor scales and examples |
| [research_queries.md](references/research_queries.md) | WebSearch query templates by domain |
| [competition_index.md](references/competition_index.md) | Blue/Red Ocean classification rules |

---

**Version:** 2.0.0
**Last Updated:** 2026-04-05
