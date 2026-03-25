---
name: memory-management
version: "4.0.0"
description: 'Persist SEO/GEO project context, brand guidelines, and target keywords across sessions so your agent remembers strategy without re-explaining. Use when the user asks to "remember project context", "save SEO data", "track campaign progress", "store keyword data", "manage project memory", "remember this for next time", "save my keyword data", "keep track of this campaign". Manages a two-layer memory system (hot cache + cold storage) with intelligent promotion/demotion.'
license: Apache-2.0
compatibility: "Claude Code ≥1.0, skills.sh marketplace, ClawHub marketplace, Vercel Labs skills ecosystem. No system packages required. Optional: MCP network access for SEO tool integrations."
homepage: "https://github.com/aaron-he-zhu/seo-geo-claude-skills"
metadata:
  author: aaron-he-zhu
  version: "4.0.0"
  geo-relevance: "low"
  tags:
    - seo
    - geo
    - project memory
    - context management
    - campaign tracking
    - data persistence
    - keyword tracking
    - project context
    - context-memory
    - project-memory
    - seo-tracking
    - campaign-tracking
    - session-context
    - hot-cache
    - project-continuity
  triggers:
    - "remember project context"
    - "save SEO data"
    - "track campaign progress"
    - "store keyword data"
    - "manage project memory"
    - "save progress"
    - "project context"
    - "remember this for next time"
    - "save my keyword data"
    - "keep track of this campaign"
---

# Memory Management


> **[SEO & GEO Skills Library](https://github.com/aaron-he-zhu/seo-geo-claude-skills)** · 20 skills for SEO + GEO · [ClawHub](https://clawhub.ai/u/aaron-he-zhu) · [skills.sh](https://skills.sh/aaron-he-zhu/seo-geo-claude-skills)

<details>
<summary>Browse all 20 skills</summary>

**Research** · [keyword-research](../../research/keyword-research/) · [competitor-analysis](../../research/competitor-analysis/) · [serp-analysis](../../research/serp-analysis/) · [content-gap-analysis](../../research/content-gap-analysis/)

**Build** · [seo-content-writer](../../build/seo-content-writer/) · [geo-content-optimizer](../../build/geo-content-optimizer/) · [meta-tags-optimizer](../../build/meta-tags-optimizer/) · [schema-markup-generator](../../build/schema-markup-generator/)

**Optimize** · [on-page-seo-auditor](../../optimize/on-page-seo-auditor/) · [technical-seo-checker](../../optimize/technical-seo-checker/) · [internal-linking-optimizer](../../optimize/internal-linking-optimizer/) · [content-refresher](../../optimize/content-refresher/)

**Monitor** · [rank-tracker](../../monitor/rank-tracker/) · [backlink-analyzer](../../monitor/backlink-analyzer/) · [performance-reporter](../../monitor/performance-reporter/) · [alert-manager](../../monitor/alert-manager/)

**Cross-cutting** · [content-quality-auditor](../content-quality-auditor/) · [domain-authority-auditor](../domain-authority-auditor/) · [entity-optimizer](../entity-optimizer/) · **memory-management**

</details>

This skill implements a two-layer memory system for SEO and GEO projects, maintaining a hot cache for active context and cold storage for detailed historical data. It automatically promotes frequently referenced items and demotes stale data, ensuring optimal context loading and efficient project memory.

## When to Use This Skill

- Setting up memory structure for a new SEO project
- After completing audits, ranking checks, or performance reports
- When starting a new campaign or optimization initiative
- When project context needs updating (new keywords, competitors, priorities)
- When you need to look up historical data or project-specific terminology
- After 30+ days of work to clean up and archive stale data
- When context retrieval feels slow or cluttered

## What This Skill Does

1. **Hot Cache Management**: Maintains CLAUDE.md (~100 lines) with active context that's always loaded
2. **Cold Storage Organization**: Structures detailed archives in memory/ subdirectories
3. **Context Lookup**: Implements efficient lookup flow from hot cache to cold storage
4. **Promotion/Demotion**: Moves items between layers based on reference frequency
5. **Glossary Maintenance**: Manages project-specific terminology and shorthand
6. **Update Triggers**: Refreshes memory after audits, reports, or ranking checks
7. **Archive Management**: Time-stamps and archives old data systematically

## How to Use

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

## Data Sources

> See [CONNECTORS.md](../../CONNECTORS.md) for tool category placeholders.

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
├── CLAUDE.md                           # Hot cache (~100 lines)
└── memory/
    ├── glossary.md                     # Project terminology
    ├── keywords/
    │   ├── hero-keywords.md           # Top priority keywords
    │   ├── secondary-keywords.md      # Medium priority
    │   ├── long-tail-keywords.md      # Long-tail opportunities
    │   └── historical-rankings.csv    # Dated ranking data
    ├── competitors/
    │   ├── primary-competitors.md     # Top 3-5 competitors
    │   ├── [competitor-domain].md     # Individual reports
    │   └── analysis-history/          # Dated analyses
    ├── audits/
    │   ├── technical/                 # Technical SEO audits
    │   ├── content/                   # Content audits
    │   ├── domain/                    # Domain authority (CITE) audits
    │   └── backlink/                  # Backlink audits
    ├── content-calendar/
    │   ├── active-calendar.md         # Current quarter
    │   ├── published-content.md       # Performance tracking
    │   └── archive/                   # Past calendars
    └── reports/
        ├── monthly/                   # Monthly reports
        ├── quarterly/                 # Quarterly reports
        └── campaign/                  # Campaign-specific reports
```

> **Templates**: See [references/hot-cache-template.md](./references/hot-cache-template.md) for the complete CLAUDE.md hot cache template and [references/glossary-template.md](./references/glossary-template.md) for the project glossary template.

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
- Search memory/keywords/ for historical data
- Search memory/competitors/ for past analyses
- Search memory/reports/ for archived mentions

**Step 4: Ask User**
- If not found in any layer, ask for clarification
- Log the new term in glossary if it's project-specific

Example lookup:

```markdown
User: "Update rankings for our hero KWs"

Step 1: Check CLAUDE.md → Found "Hero Keywords (Priority 1)" section
Step 2: Extract keyword list from hot cache
Step 3: Execute ranking check
Step 4: Update both CLAUDE.md and memory/keywords/historical-rankings.csv
```

### 5. Promotion & Demotion Logic

> **Reference**: See [references/promotion-demotion-rules.md](./references/promotion-demotion-rules.md) for detailed promotion/demotion triggers (keywords, competitors, metrics, campaigns) and the action procedures for each.

### 6. Update Triggers, Archive Management & Cross-Skill Integration

> **Reference**: See [references/update-triggers-integration.md](./references/update-triggers-integration.md) for the complete update procedures after ranking checks, competitor analyses, audits, and reports; monthly/quarterly archive routines; and integration points with all 8 connected skills (keyword-research, rank-tracker, competitor-analysis, content-gap-analysis, seo-content-writer, content-quality-auditor, domain-authority-auditor).

## Validation Checkpoints

### Structure Validation
- [ ] CLAUDE.md exists and is under 150 lines (aim for ~100)
- [ ] memory/ directory structure matches template
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
- [ ] After ranking check, historical-rankings.csv has new row with today's date
- [ ] After competitor analysis, analysis-history/ has dated file
- [ ] After audit, top action items appear in CLAUDE.md priorities
- [ ] After monthly report, metrics snapshot reflects new data

## Examples

> **Reference**: See [references/examples.md](./references/examples.md) for three complete examples: (1) updating hero keyword rankings with memory refresh, (2) glossary lookup flow, and (3) initializing memory for a new e-commerce project.

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
- **CLAUDE.md size**: The hot cache should stay concise (<200 lines). If it grows too large, archive older metrics to cold storage.
- **Data freshness**: Memory reflects the last time each skill was run. Stale data (>90 days) should be flagged for refresh.

## Tips for Success

1. **Keep hot cache lean** - CLAUDE.md should never exceed 150 lines. If it grows larger, aggressively demote.
2. **Date everything** - Every file in cold storage should have YYYY-MM-DD in filename or prominent metadata.
3. **Update after every significant action** - Don't let memory drift from reality. Update immediately after ranking checks, audits, or reports.
4. **Use glossary liberally** - If you find yourself explaining a term twice, add it to glossary.
5. **Review hot cache weekly** - Quick scan to ensure everything there is still relevant and active.
6. **Automate where possible** - If ~~SEO tool or ~~search console connected, set up automatic updates to historical-rankings.csv.
7. **Archive aggressively** - Better to have data in cold storage and not need it than clutter hot cache.
8. **Link between layers** - CLAUDE.md should always reference where detailed data lives ("Full data: memory/keywords/").
9. **Timestamp changes** - When updating CLAUDE.md, always update "Last Updated" date.
10. **Use memory for continuity** - If you switch between different analysis sessions, memory ensures nothing is forgotten.

## Reference Materials

- [CORE-EEAT Content Benchmark](../../references/core-eeat-benchmark.md) — Content quality scoring stored in memory
- [CITE Domain Rating](../../references/cite-domain-rating.md) — Domain authority scoring stored in memory

## Related Skills

- [rank-tracker](../../monitor/rank-tracker/) — Provides ranking data to update memory
- [competitor-analysis](../../research/competitor-analysis/) — Generates competitor reports for storage
- [keyword-research](../../research/keyword-research/) — Discovers keywords to add to memory
- [performance-reporter](../../monitor/performance-reporter/) — Creates reports that trigger memory updates
- [content-gap-analysis](../../research/content-gap-analysis/) — Identifies optimization priorities for hot cache
- [seo-content-writer](../../build/seo-content-writer/) — Logs published content to memory calendar
- [content-quality-auditor](../content-quality-auditor/) — Content audit results stored in memory for tracking
- [domain-authority-auditor](../domain-authority-auditor/) — CITE domain audit results stored in memory for tracking
- [entity-optimizer](../entity-optimizer/) — Store entity audit results for tracking over time
