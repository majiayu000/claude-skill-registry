---
name: memory-management
description: 'Persist SEO/GEO campaign context across Claude sessions with automatic hot-list, active work, and archive tiers. 项目记忆/跨会话'
version: "6.0.0"
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
when_to_use: "Use when reviewing, archiving, or cleaning up campaign memory. Also when the user asks to check saved findings, manage hot cache, or archive old data."
argument-hint: "[review|archive|cleanup]"
metadata:
  author: aaron-he-zhu
  version: "6.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - project-memory
    - context-management
    - campaign-tracking
    - session-context
    - hot-cache
    - 项目记忆
    - プロジェクト記憶
    - 프로젝트메모리
    - memoria-proyecto
  triggers:
    # EN-formal
    - "remember project context"
    - "save SEO data"
    - "track campaign progress"
    - "store keyword data"
    - "manage project memory"
    - "project context"
    # EN-casual
    - "remember this for next time"
    - "save my keyword data"
    - "keep track of this campaign"
    - "what did we decide last time"
    - "what do we know so far"
    - "project status"
    # EN-question
    - "how to save project progress"
    # ZH-pro
    - "项目记忆管理"
    - "SEO数据保存"
    - "跨会话记忆"
    # ZH-casual
    - "保存进度"
    - "上次说了什么"
    - "记住这个"
    # JA
    - "プロジェクト記憶"
    - "SEOデータ保存"
    # KO
    - "프로젝트 메모리"
    - "데이터 저장"
    # ES
    - "memoria del proyecto"
    - "guardar progreso"
    # PT
    - "memória do projeto"
---

# Memory Management

> **[SEO & GEO Skills Library](https://github.com/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · [ClawHub](https://clawhub.ai/u/aaron-he-zhu) · [skills.sh](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)
> **System Mode**: This cross-cutting skill is part of the protocol layer and follows the shared [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md) and [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md).

This skill implements a three-tier memory system (HOT/WARM/COLD) for SEO and GEO projects. HOT memory (80 lines max) loads automatically every session via the SessionStart hook. WARM memory loads on demand per skill. COLD memory is archived data queried only when explicitly requested. The skill manages the full lifecycle: capture, promote, demote, and archive.

**System role**: Campaign Memory Loop. It defines how project context is captured, promoted, archived, and handed off across sessions. It is the sole executor of WARM-to-COLD archival and the aggregator for cross-skill project status queries.

## When This Must Trigger

Use this whenever project state should survive the current session — even if the user doesn't use memory terminology:

- User says "remember this", "save this", "keep track of this"
- User asks "what did we decide", "what do we know", "project status"
- Setting up memory structure for a new SEO project
- After completing audits, ranking checks, or performance reports (Stop hook reminds automatically)
- When project context needs updating (new keywords, competitors, priorities)
- When you need to look up historical data or project-specific terminology
- After 30+ days of work to clean up and archive stale data
- When open-loops.md has items older than 7 days (SessionStart hook reminds automatically)

## What This Skill Does

1. **HOT Cache Management**: Maintains `memory/hot-cache.md` (80 lines max) — loaded automatically every session by SessionStart hook
2. **WARM Storage**: Organizes dated findings in `memory/` subdirectories — loaded on demand by relevant skills
3. **COLD Archive**: Moves stale data (90+ days unreferenced) to `memory/archive/` with date prefix
4. **Promotion**: Elevates frequently-referenced findings from WARM to HOT (3+ refs in 7 days, or 2+ skill refs)
5. **Demotion**: Moves unreferenced HOT items to WARM (30 days), WARM to COLD (90 days)
6. **Cross-Skill Aggregation**: When user asks "what do we know", aggregates from all `memory/` subdirectories
7. **Open Loop Tracking**: Maintains `memory/open-loops.md`, reminds user of stale items via SessionStart hook

## Quick Start

Start with one of these prompts. Finish with a hot-cache update plan and a handoff summary using the repository format in [Skill Contract](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/skill-contract.md).

### Initialize Memory Structure

```
Set up SEO memory for [project name]
```

```
Initialize memory structure for a new [industry] website optimization project
```

### Update After Analysis

```
Update memory after ranking check for [keyword group]
```

```
Refresh hot cache with latest competitor analysis findings
```

### Query Stored Context

```
What are our hero keywords?
```

```
Show me the last ranking update date for [keyword category]
```

```
Look up our primary competitors and their domain authority
```

### Promotion and Demotion

```
Promote [keyword] to hot cache
```

```
Archive stale data that hasn't been referenced in 30+ days
```

### Glossary Management

```
Add [term] to project glossary: [definition]
```

```
What does [internal jargon] mean in this project?
```

## Skill Contract

**Expected output**: a memory update plan, hot-cache changes, and a short handoff summary.

- **Reads**: current campaign facts, new findings from other skills, approved decisions, and the shared [State Model](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/state-model.md).
- **Writes**: updates to `memory/hot-cache.md`, `memory/open-loops.md`, `memory/decisions.md`, and related `memory/` folders. Also manages WARM-to-COLD archival in `memory/archive/`.
- **Promotes**: durable strategy, blockers, terminology, entity candidates, and major deltas. Applies temperature lifecycle rules: promote to HOT on high reference frequency, demote on staleness.
- **Next handoff**: use the `Next Best Skill` below when the project memory baseline is ready for active work.

### Temperature Lifecycle Rules

| Condition | Action |
|-----------|--------|
| Finding referenced by 2+ skills within 7 days | Promote WARM → HOT (extract ≤3 line summary) |
| Finding referenced 3+ times within 7 days | Promote WARM → HOT |
| HOT item unreferenced for 30 days | Demote HOT → WARM (remove from hot-cache.md, keep source file) |
| WARM file unreferenced for 90 days | Demote WARM → COLD (move to `memory/archive/YYYY-MM-DD-filename.md`) |

### Hook Integration

This skill's behavior is reinforced by the library's prompt-based hooks:
- **SessionStart**: loads `memory/hot-cache.md`, reminds of stale open loops
- **Stop**: prompts to save session findings, auto-saves veto issues to hot-cache

## Data Sources

> See [CONNECTORS.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/CONNECTORS.md) for tool category placeholders.

**With ~~SEO tool + ~~analytics + ~~search console connected:**
Automatically populate memory from historical data: keyword rankings over time, competitor domain authority changes, traffic metrics, conversion data, backlink profile evolution. The skill will fetch current rankings, alert on significant changes, and update both hot cache and cold storage.

**With manual data only:**
Ask the user to provide:
1. Current target keywords with priority levels
2. Primary competitors (3-5 domains)
3. Key performance metrics and last update date
4. Active campaigns and their status
5. Any project-specific terminology or abbreviations

Proceed with memory structure creation using provided data. Note in CLAUDE.md which data requires manual updates vs. automated refresh.

## Instructions

When a user requests SEO memory management:

### 1. Initialize Memory Structure

For new projects, create the following structure:

```markdown
## Directory Structure

project-root/
├── CLAUDE.md                           # HOT tier (80 lines max)
└── memory/
    ├── decisions.md                    # Major strategic choices
    ├── open-loops.md                   # Unresolved blockers and follow-ups
    ├── glossary.md                     # Project terminology
    ├── entities/
    │   └── [entity-name].md           # Canonical entity profiles
    ├── research/
    │   ├── keywords/                  # Hero, secondary, and opportunity sets
    │   ├── competitors/               # Competitor overviews and dated analyses
    │   ├── serp/                      # SERP snapshots and notes
    │   └── content-gaps/              # Gap summaries and topic opportunities
    ├── content/
    │   ├── briefs/                    # Content briefs and approved angles
    │   ├── calendar/                  # Active and archived campaign plans
    │   └── published/                 # Dated shipped-content summaries
    ├── audits/
    │   ├── content/                   # Content audits
    │   ├── domain/                    # Domain authority (CITE) audits
    │   ├── technical/                 # Technical SEO audits
    │   └── internal-linking/          # Link architecture audits
    └── monitoring/
        ├── alerts/                    # Alert history and thresholds
        ├── rank-history/              # Dated ranking snapshots / CSV exports
        ├── reports/                   # Monthly, quarterly, campaign reports
        └── snapshots/                 # Dated hot-cache snapshots
```

> **Templates**: See [references/hot-cache-template.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/hot-cache-template.md) for the complete CLAUDE.md hot cache template and [references/glossary-template.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/glossary-template.md) for the project glossary template.

### 4. Context Lookup Flow

When a user references something unclear, follow this lookup sequence:

**Step 1: Check CLAUDE.md (Hot Cache)**
- Is it in active keywords?
- Is it in primary competitors?
- Is it in current priorities or campaigns?

**Step 2: Check memory/glossary.md**
- Is it defined as project terminology?
- Is it a custom segment or shorthand?

**Step 3: Check Cold Storage**
- Search memory/research/keywords/ for historical keyword context
- Search memory/research/competitors/ for past analyses
- Search memory/monitoring/reports/ for archived mentions

**Step 4: Ask User**
- If not found in any layer, ask for clarification
- Log the new term in glossary if it's project-specific

Example lookup:

```markdown
User: "Update rankings for our hero KWs"

Step 1: Check CLAUDE.md → Found "Hero Keywords (Priority 1)" section
Step 2: Extract keyword list from hot cache
Step 3: Execute ranking check
Step 4: Update both CLAUDE.md and memory/monitoring/rank-history/YYYY-MM-DD-ranks.csv
```

### 5. Promotion & Demotion Logic

> **Reference**: See [references/promotion-demotion-rules.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/promotion-demotion-rules.md) for detailed promotion/demotion triggers (keywords, competitors, metrics, campaigns) and the action procedures for each.

### 6. Update Triggers, Archive Management & Cross-Skill Integration

> **Reference**: See [references/update-triggers-integration.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/update-triggers-integration.md) for the complete update procedures after ranking checks, competitor analyses, audits, and reports; monthly/quarterly archive routines; and integration points with all 8 connected skills (keyword-research, rank-tracker, competitor-analysis, content-gap-analysis, seo-content-writer, content-quality-auditor, domain-authority-auditor).

### Memory Hygiene Checks

When invoked for review or cleanup:

1. **Line count check**: Count lines in `memory/hot-cache.md`. If >80, list oldest entries for archival.
2. **Byte check**: If hot-cache exceeds 25KB, warn and recommend trimming long entries.
3. **Staleness scan**: List memory files older than 30 days that have not been referenced. Recommend archival for files >90 days.
4. **Frontmatter audit**: Check that all memory files (except hot-cache.md) have `name`, `description`, and `type` in their frontmatter. Report any missing fields.

### Save Results

After delivering any memory update or aggregation to the user, ask:

> "Save these results for future sessions?"

If yes, write a dated summary to the appropriate `memory/` path using filename `YYYY-MM-DD-<topic>.md` containing:
- One-line verdict or headline finding
- Top 3-5 actionable items
- Open loops or blockers
- Source data references

If any veto-level issue was found (CORE-EEAT T04, C01, R10 or CITE T03, T05, T09), also append a one-liner to `memory/hot-cache.md` without asking.

## Validation Checkpoints

### Structure Validation
- [ ] memory/hot-cache.md exists and is under 80 lines
- [ ] memory/ directory structure matches the shared state model
- [ ] glossary.md exists and is populated with project basics
- [ ] All historical data files include timestamps in filename or metadata

### Content Validation
- [ ] CLAUDE.md "Last Updated" date is current
- [ ] Every keyword in hot cache has current rank, target rank, and status
- [ ] Every competitor has domain authority and position assessment
- [ ] Every active campaign has status percentage and expected completion date
- [ ] Key Metrics Snapshot shows "Previous" values for comparison

### Lookup Validation
- [ ] Test lookup flow: reference a term → verify it finds it in correct layer
- [ ] Test promotion: manually promote item → verify it appears in CLAUDE.md
- [ ] Test demotion: manually archive item → verify removed from CLAUDE.md
- [ ] Glossary contains all custom segments and shorthand used in CLAUDE.md

### Update Validation
- [ ] After ranking check, `memory/monitoring/rank-history/` has a dated snapshot or export
- [ ] After competitor analysis, `memory/research/competitors/` has a dated file
- [ ] After audit, top action items appear in CLAUDE.md priorities
- [ ] After monthly report, metrics snapshot reflects new data

## Examples

> **Reference**: See [references/examples.md](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/cross-cutting/memory-management/references/examples.md) for three complete examples: (1) updating hero keyword rankings with memory refresh, (2) glossary lookup flow, and (3) initializing memory for a new e-commerce project.

## Advanced Features

### Smart Context Loading

```
Load full context for [campaign name]
```

Retrieves hot cache + all cold storage files related to campaign.

### Memory Health Check

```
Run memory health check
```

Audits memory structure: finds orphaned files, missing timestamps, stale hot cache items, broken references.

### Bulk Promotion/Demotion

```
Promote all keywords ranking in top 10 to hot cache
```

```
Demote all completed campaigns from Q3 2024
```

### Memory Snapshot

```
Create memory snapshot for [date/milestone]
```

Takes point-in-time copy of entire memory structure for major milestones (site launches, algorithm updates, etc.).

### Cross-Project Memory

```
Compare memory with [other project name]
```

Identifies keyword overlaps, competitor intersections, and strategy similarities across multiple projects.

## Practical Limitations

- **Concurrent access**: If multiple Claude sessions update memory simultaneously, later writes may overwrite earlier ones. Mitigate by using timestamped filenames for audit reports rather than overwriting a single file.
- **Cold storage retrieval**: Files in `memory/` subdirectories are only loaded when explicitly requested. They do not appear in Claude's context automatically. The hot cache (`CLAUDE.md`) is the primary cross-session mechanism.
- **CLAUDE.md size**: The HOT cache should stay concise (80 lines max). If it grows too large, archive older metrics to cold storage.
- **Data freshness**: Memory reflects the last time each skill was run. Stale data (>90 days) should be flagged for refresh.

## Tips for Success

1. **Keep hot cache lean** - memory/hot-cache.md should never exceed 80 lines. If it grows larger, aggressively demote.
2. **Date everything** - Every file in cold storage should have YYYY-MM-DD in filename or prominent metadata.
3. **Update after every significant action** - Don't let memory drift from reality. Update immediately after ranking checks, audits, or reports.
4. **Use glossary liberally** - If you find yourself explaining a term twice, add it to glossary.
5. **Review hot cache weekly** - Quick scan to ensure everything there is still relevant and active.
6. **Automate where possible** - If ~~SEO tool or ~~search console connected, write dated exports into `memory/monitoring/rank-history/`.
7. **Archive aggressively** - Better to have data in cold storage and not need it than clutter hot cache.
8. **Link between layers** - CLAUDE.md should always reference where detailed data lives ("Full data: memory/research/keywords/").
9. **Timestamp changes** - When updating CLAUDE.md, always update "Last Updated" date.
10. **Use memory for continuity** - If you switch between different analysis sessions, memory ensures nothing is forgotten.

## Reference Materials

- [CORE-EEAT Content Benchmark](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/core-eeat-benchmark.md) — Content quality scoring stored in memory
- [CITE Domain Rating](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/references/cite-domain-rating.md) — Domain authority scoring stored in memory

## Next Best Skill

- **Primary**: [keyword-research](https://github.com/aaron-he-zhu/seo-geo-claude-skills/blob/main/research/keyword-research/SKILL.md) — seed or refresh campaign strategy with current demand signals.
