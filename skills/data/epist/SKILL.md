---
name: epist
description: Epistemological tracking system for managing facts, conclusions, and provenance chains with Git integrity and semantic search. Integrates with Quarto for visual provenance analysis. Use when analyzing data from multiple sources, conducting research, working with metrics/surveys, making data-driven conclusions, or tracking complex findings. Triggers on data analysis (analyze data, metrics, survey, research, findings, insights), conclusions (conclude, recommend, decide, infer), quantitative work (percentage, trend, correlation, statistic), source attribution (according to, based on, from source), or any epistemological tracking. Skip for trivial calculations.
---
# Epist - Epistemological Tracking System Skill

You are an epistemological tracking specialist using `epist`, a CLI tool that helps track facts, conclusions, and their provenance using Git for integrity and Lancer for semantic search. **EPIST now integrates directly with Quarto** for visual epistemological analysis.

## What is epist?

`epist` is a powerful tool for:
- **Fact tracking**: Record facts with proper provenance (sources, dates, context)
- **Conclusion management**: Track conclusions derived from facts
- **Provenance tracing**: Understand dependency chains and staleness
- **Semantic search**: Find facts and conclusions using vector search
- **Git-backed integrity**: Version control for epistemological claims
- **MCP server**: Integration with Claude and other AI tools
- **Quarto integration**: Visual provenance analysis with `/think` command

## Core Capabilities

1. **Add facts**: Record factual claims with provenance
2. **Add conclusions**: Create conclusions based on facts
3. **Search**: Semantic search across facts and conclusions
4. **Trace**: Follow provenance chains and check staleness
5. **List**: Browse all facts and conclusions
6. **Remove**: Delete facts or conclusions
7. **MCP**: Run as Model Context Protocol server
8. **Quarto integration**: Visual epistemological analysis with `/think` command

## Quick Start

### Initialize Knowledge Base

```bash
# Initialize new epist knowledge base
epist init

# This creates:
# - .epist/ directory with SQLite database
# - Git repository for version control
# - LanceDB vector embeddings for search
```

### Adding Facts

```bash
# Add a fact interactively (opens editor)
epist add fact

# Example fact structure:
# ---
# title: Q4 2024 Team Autonomy Score
# source: Team Survey Results
# source_url: https://example.com/survey/q4-2024
# date: 2024-12-15
# tags: [metrics, autonomy, team-alpha]
# ---
# 
# Team Alpha's autonomy score in Q4 2024 was 78%, down from 85% in Q3.
# This represents a 7 percentage point decrease quarter-over-quarter.
```

### Adding Conclusions

```bash
# Add a conclusion based on facts
epist add conclusion

# Example conclusion structure:
# ---
# title: Team Alpha Needs Autonomy Intervention
# based_on:
#   - facts/metrics/q4_autonomy.md
#   - facts/interviews/team_lead_feedback.md
# confidence: high
# tags: [recommendations, team-alpha]
# ---
# 
# Based on declining autonomy scores and team lead feedback, Team Alpha
# requires immediate intervention to restore autonomy levels.
```

### Searching

```bash
# Search all facts and conclusions
epist search "team autonomy problems"

# Search only facts
epist search "deployment issues" --type fact --limit 5

# Search only conclusions
epist search "recommendations" --type conclusion

# JSON output for scripting
epist search "metrics" --format json
```

### Tracing Provenance

```bash
# Trace dependency chain for a conclusion
epist trace conclusions/team-alpha/recommendation.md

# Shows:
# - All facts the conclusion depends on
# - Staleness indicators (if facts are outdated)
# - Full dependency tree
```

### Listing

```bash
# List all facts and conclusions
epist list

# List only facts
epist list --type fact

# List only conclusions
epist list --type conclusion

# JSON output
epist list --format json
```

## Command Reference

### `epist init`
Initialize a new epistemological knowledge base.

**What it creates:**
- `.epist/` directory with SQLite database
- Git repository for version control
- LanceDB vector store for semantic search

```bash
epist init
```

### `epist add fact`
Add a new fact with provenance information.

**Interactive mode** (opens editor):
```bash
epist add fact
```

**Fact template:**
```markdown
---
title: [Required] Descriptive title
source: [Required] Where this came from
source_url: [Optional] Link to source
date: [Required] YYYY-MM-DD
tags: [Optional] [tag1, tag2]
confidence: [Optional] low|medium|high
---

[Required] The actual factual claim or data.
Can be multiple paragraphs.
```

**Flags:**
- None currently - always interactive

### `epist add conclusion`
Add a conclusion derived from facts.

**Interactive mode** (opens editor):
```bash
epist add conclusion
```

**Conclusion template:**
```markdown
---
title: [Required] Descriptive title
based_on: [Required] List of fact paths
  - facts/path/to/fact1.md
  - facts/path/to/fact2.md
confidence: [Optional] low|medium|high
tags: [Optional] [tag1, tag2]
---

[Required] The conclusion or inference drawn from the facts.
Explain the reasoning connecting the facts to this conclusion.
```

**Flags:**
- None currently - always interactive

### `epist search <query>`
Semantic search using LanceDB vector embeddings.

```bash
# Search all
epist search "team autonomy"

# Search only facts
epist search "metrics" --type fact

# Limit results
epist search "deployment" --limit 5

# JSON output
epist search "issues" --format json
```

**Flags:**
- `--type <type>` - Filter by type: `fact`, `conclusion`, `all` (default: `all`)
- `--limit <n>` - Maximum results (default: 10)
- `--format <fmt>` - Output format: `table`, `json`, `paths` (default: `table`)

**Output formats:**
- `table` - Human-readable table with title, type, tags, preview
- `json` - Structured JSON for scripting
- `paths` - Just file paths (one per line)

### `epist trace <path>`
Trace provenance chain and check staleness.

```bash
# Trace a conclusion
epist trace conclusions/team-alpha/recommendation.md

# Trace a fact
epist trace facts/metrics/q4_autonomy.md
```

**Shows:**
- Full dependency tree
- Staleness warnings (if dependencies changed)
- Missing dependencies (if files deleted)

**Flags:**
- None currently

### `epist list`
List all facts and conclusions.

```bash
# List all
epist list

# List only facts
epist list --type fact

# List only conclusions
epist list --type conclusion

# JSON output
epist list --format json
```

**Flags:**
- `--type <type>` - Filter by type: `fact`, `conclusion`, `all` (default: `all`)
- `--format <fmt>` - Output format: `table`, `json` (default: `table`)

### `epist get <path>`
Get full details of a fact or conclusion.

```bash
# Get fact details
epist get facts/metrics/q4_autonomy.md

# Get conclusion details
epist get conclusions/team-alpha/recommendation.md
```

**Shows:**
- Full metadata (YAML frontmatter)
- Complete content
- File path and timestamps

**Flags:**
- None currently

### `epist remove <path>`
Remove a fact or conclusion from the knowledge base.

```bash
# Remove a fact
epist remove facts/metrics/outdated_data.md

# Remove a conclusion
epist remove conclusions/obsolete/old_recommendation.md
```

**Warning:** This is destructive and removes from Git history.

**Flags:**
- None currently - always prompts for confirmation

### `epist destroy`
Completely destroy the knowledge base (DESTRUCTIVE).

```bash
epist destroy
```

**Warning:** This removes:
- `.epist/` directory
- All facts and conclusions
- Git history
- Vector embeddings

**Flags:**
- None currently - always prompts for confirmation

### `epist mcp`
MCP (Model Context Protocol) server commands.

```bash
# Start MCP server
epist mcp start

# MCP server provides tools for:
# - Searching facts and conclusions
# - Getting fact/conclusion details
# - Adding new facts (future)
# - Adding new conclusions (future)
```

**Use in Claude Desktop:**
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "epist": {
      "command": "epist",
      "args": ["mcp", "start"]
    }
  }
}
```

## Workflows

### Workflow 1: Recording Research Findings

```bash
# Initialize if not done
epist init

# Add facts from research
epist add fact
# Title: "Team Alpha Q4 Autonomy Score"
# Source: "Team Survey"
# Date: 2024-12-15
# Content: "Team Alpha autonomy: 78% (down from 85%)"

epist add fact
# Title: "Team Lead Interview: Autonomy Concerns"
# Source: "Interview with Jane Doe"
# Date: 2024-12-18
# Content: "Lead reports increased micromanagement..."

# Create conclusion
epist add conclusion
# Title: "Team Alpha Autonomy Intervention Needed"
# Based on: facts/q4_autonomy.md, facts/lead_interview.md
# Content: "Declining autonomy requires intervention..."
```

### Workflow 2: Searching for Context

```bash
# Search for autonomy-related facts
epist search "autonomy problems" --type fact

# Find all conclusions about a team
epist search "team alpha" --type conclusion

# Get full details of a finding
epist get facts/metrics/q4_autonomy.md
```

### Workflow 3: Checking Provenance

```bash
# Before using a conclusion, check its provenance
epist trace conclusions/team-alpha/intervention.md

# Output shows:
# ✓ Conclusion: Team Alpha Autonomy Intervention Needed
#   └─ ✓ Fact: Q4 Autonomy Score (2024-12-15)
#   └─ ⚠ Fact: Team Lead Interview (outdated: 60 days old)
```

### Workflow 4: Updating Facts

```bash
# When new data arrives
epist add fact
# Title: "Team Alpha Q1 2025 Autonomy Score"
# Source: "Team Survey"
# Date: 2025-03-15
# Content: "Team Alpha autonomy: 82% (up from 78%)"

# Trace dependent conclusions to see what's affected
epist search "team alpha" --type conclusion
epist trace conclusions/team-alpha/intervention.md

# Update conclusions if needed
epist add conclusion
# (Reference both old and new facts)
```

### Workflow 5: Data Analysis with Epistemological Rigor

When conducting data analysis from multiple sources, use epist to maintain provenance and prevent misinterpretation:

```bash
# Initialize knowledge base if not done
epist init

# Step 1: Record data sources as facts
epist add fact
# ---
# title: Q4 2024 Team Survey Results - Autonomy
# source: Employee Survey Platform
# source_url: https://surveys.company.com/q4-2024/results
# date: 2024-12-20
# tags: [metrics, autonomy, q4-2024, survey]
# ---
# 
# Survey question: "I have autonomy in my work"
# Overall company score: 18%
# Response rate: 87% (1,200 employees)
# Note: This is a newly added question, no historical baseline

epist add fact
# ---
# title: HR Analytics - Autonomy Metric Definition
# source: HR Analytics Documentation
# source_url: https://docs.company.com/hr/metrics#autonomy
# date: 2024-01-15
# tags: [documentation, metrics, autonomy, definitions]
# ---
# 
# Autonomy metric measured at DEPARTMENT level, not team level.
# Aggregation: Average of all department scores weighted by headcount.
# Department defined as: Direct reports to VP or higher.

epist add fact
# ---
# title: Team Lead Interview - Alpha Team Autonomy Concerns
# source: 1:1 Interview with Jane Doe (Team Alpha Lead)
# date: 2024-12-18
# tags: [qualitative, autonomy, team-alpha, interview]
# confidence: medium
# ---
# 
# "Our team feels micromanaged lately. Every decision requires approval
# from the VP level, which slows us down significantly."
# Context: Team Alpha is part of Engineering department (120 people).

# Step 2: Analyze and identify potential issues
# (During analysis, you notice 18% seems wrong given the interview feedback)

# Step 3: Record conclusion with provenance
epist add conclusion
# ---
# title: Survey Data May Misrepresent Team-Level Autonomy
# based_on:
#   - facts/survey_results_q4_autonomy.md
#   - facts/hr_metrics_autonomy_definition.md
#   - facts/interview_team_alpha_lead.md
# confidence: high
# tags: [analysis, autonomy, methodology]
# ---
# 
# The 18% autonomy score likely conflates department-level and team-level
# autonomy. The metric definition specifies DEPARTMENT level (VP reports),
# but the survey question asks about individual autonomy.
# 
# Team Alpha's interview feedback suggests high frustration with autonomy,
# but they're grouped with 119 other engineers in the same department.
# If most of the department has autonomy but Team Alpha doesn't, the
# department average masks the team-specific problem.
# 
# RECOMMENDATION: Re-analyze survey data at team level, not department level.
# Request engineering to break down the 18% by individual teams.

# Step 4: Before sharing analysis, verify provenance
epist trace conclusions/survey_methodology_issue.md
# Output shows:
# ✓ Conclusion: Survey Data May Misrepresent Team-Level Autonomy
#   └─ ✓ Fact: Q4 2024 Survey Results (2024-12-20)
#   └─ ✓ Fact: HR Metrics Definition (2024-01-15)
#   └─ ✓ Fact: Team Lead Interview (2024-12-18)

# Step 5: Search for related analysis when needed
epist search "autonomy methodology" --type conclusion
```

**Why this workflow matters:**
- **Prevents misinterpretation**: Caught that 18% was department-level, not team-level
- **Audit trail**: Can explain your reasoning months later
- **Reproducible**: Others can verify your logic
- **Staleness detection**: Know when facts become outdated
- **Source tracking**: Always know where data came from

**When to use this workflow:**
- Analyzing survey results, metrics, or quantitative data
- Combining multiple data sources (quantitative + qualitative)
- Making recommendations based on data
- Investigating trends or anomalies
- Conducting research spanning multiple sessions

## Best Practices

### Fact Recording

1. **Always include sources**: Every fact needs a `source` field
2. **Date everything**: Use `date` field for temporal tracking
3. **Tag liberally**: Use tags for easy categorization
4. **Link sources**: Add `source_url` when available
5. **Be specific**: Write clear, verifiable facts

### Conclusion Building

1. **Reference facts explicitly**: Use `based_on` to link facts
2. **Explain reasoning**: Show how facts lead to conclusions
3. **Indicate confidence**: Use `confidence` field honestly
4. **Keep atomic**: One conclusion per file
5. **Update regularly**: Revisit when facts change

### Provenance Management

1. **Trace before using**: Always check provenance chains
2. **Watch for staleness**: Update facts when they age
3. **Document assumptions**: Note when facts are incomplete
4. **Version control**: Commit regularly to Git
5. **Review dependencies**: Periodically audit conclusion chains

### Search Strategy

1. **Use semantic search**: Don't rely on exact keywords
2. **Start broad**: Use general queries, then narrow
3. **Filter by type**: Use `--type` to focus search
4. **Check multiple results**: Don't stop at first match
5. **Verify provenance**: Always trace important findings

## Integration with Other Tools

### Git Integration

```bash
# Epist uses Git under the hood
cd .epist/
git log  # View history of changes
git diff  # See what changed
git blame facts/some_fact.md  # See who added/modified
```

### Lancer Integration

```bash
# Epist uses Lancer for vector search
# Search indices are automatically maintained
# No manual lancer commands needed
```

### MCP Integration

```bash
# Use epist with Claude Desktop
epist mcp start

# Or integrate with other MCP clients
# MCP tools available:
# - epist_search: Search facts and conclusions
# - epist_get: Get full details
# - epist_trace: Trace provenance chains
```

### Quarto Integration (RECOMMENDED for Analysis)

**EPIST now integrates directly with Quarto for epistemological analysis and reporting.**

#### Why Quarto + EPIST

**Quarto provides:**
- Visual provenance chains (Mermaid diagrams)
- Publication-quality output (GFM, HTML, PDF, DOCX)
- Mathematical rigor (LaTeX notation)
- Formatted tables and charts (professional presentation)
- Multi-format rendering (archival + collaboration)

**EPIST provides:**
- Persistent fact storage (Git-backed)
- Semantic search (find related facts)
- Provenance tracking (dependency chains)
- Version control (track changes over time)

**Together they enable:**
- Traceable reasoning (facts → analysis → conclusions)
- Reproducible research (code + data + provenance)
- Shareable analysis (Quarto renders to multiple formats)
- Long-term knowledge management (EPIST persists across sessions)

#### Workflow: EPIST → Quarto Analysis

**Step 1: Record facts in EPIST**

```bash
# Record key facts with provenance
epist add fact
# Title: Q4 2024 Sales Data
# Source: sales_database.csv
# Date: 2024-12-31
# 
# Total sales: $2.1M
# YoY growth: 15%
# Top product: Widget X ($450k)
```

**Step 2: Create Quarto analysis document**

Use `/think` command or create `.qmd` file:

```qmd
---
title: "Sales Analysis Q4 2024 with EPIST Provenance"
author: "Analysis Team"
date: "2024-12-31"
format:
  gfm: default
  html:
    theme:
      dark: darkly
      light: flatly
  docx: default
filters:
  - auto-dark
---

## Facts Observed

```{python}
#| echo: false
from IPython.display import Markdown

# Reference EPIST facts
Markdown("""
- **Total Sales**: $2.1M (Source: EPIST fact `sales_q4_total.md`)
- **YoY Growth**: 15% (Source: EPIST fact `sales_growth_yoy.md`)
- **Top Product**: Widget X at $450k (Source: EPIST fact `top_product_q4.md`)

All facts stored in EPIST knowledge base with full provenance.
""")
```

## Analysis

```{python}
#| echo: false
import matplotlib.pyplot as plt

# Visualization
sales_data = [1.5, 1.7, 1.9, 2.1]  # Q1-Q4
quarters = ['Q1', 'Q2', 'Q3', 'Q4']

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(quarters, sales_data, marker='o', linewidth=2, color='#2E86AB')
ax.set_title('Quarterly Sales Growth 2024', fontsize=14, fontweight='bold')
ax.set_ylabel('Sales ($M)')
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

## Provenance Chain

```{mermaid}
flowchart LR
    F1[Fact: Sales $2.1M] --> C1[Conclusion: Strong Q4]
    F2[Fact: YoY Growth 15%] --> C1
    F3[Fact: Widget X Top] --> C2[Conclusion: Focus on Widgets]
    C1 --> R[Recommendation: Increase inventory]
```

## Conclusion

```{python}
#| echo: false
Markdown("""
Q4 2024 exceeded targets with $2.1M in sales (15% YoY growth).

**Confidence**: High (based on 3 verified facts in EPIST)

**Provenance**: All claims traceable to EPIST facts with source attribution.
""")
```
```

**Step 3: Render Quarto document**

```bash
quarto render sales_analysis.qmd --to gfm      # Markdown (archival)
quarto render sales_analysis.qmd --to html     # HTML (viewing)
quarto render sales_analysis.qmd --to docx     # DOCX (Google Docs)
```

**Step 4: Record conclusions in EPIST**

```bash
# Add analysis conclusions back to EPIST
epist add conclusion
# Title: Q4 2024 Sales Analysis - Strong Performance
# Based on:
#   - facts/sales_q4_total.md
#   - facts/sales_growth_yoy.md
#   - facts/top_product_q4.md
# Source: sales_analysis.qmd
# Date: 2024-12-31
# Confidence: high
# 
# Q4 2024 exceeded targets with strong 15% YoY growth.
# Widget X dominates product mix at $450k (21% of total).
# Recommend increasing inventory for Q1 2025.
```

#### Using `/think` Command with EPIST

**The `/think` command integrates EPIST automatically:**

```bash
/think What caused the sales spike in Q4?
```

**LLM will:**
1. Search EPIST for relevant facts (`epist search "sales Q4"`)
2. Create Quarto document with full reasoning chain
3. Include Mermaid diagrams showing fact→conclusion provenance
4. Render to GFM, HTML, DOCX
5. Optionally save conclusions back to EPIST

**Template structure includes:**
- Facts Observed (from EPIST search)
- Hypotheses (multiple alternatives)
- Analysis (with charts, LaTeX math)
- Provenance Flow (Mermaid diagram)
- Conclusion (with EPIST reference)
- Recommendations (actionable)

#### Querying EPIST from Quarto

**Use Python to query EPIST directly:**

```python
import subprocess
import json

# Search EPIST for facts
result = subprocess.run(
    ['epist', 'search', 'sales Q4', '--format', 'json'],
    capture_output=True, text=True
)
facts = json.loads(result.stdout)

# Use facts in analysis
for fact in facts:
    print(f"- {fact['title']} (Source: {fact['source']})")
```

#### Best Practices: Quarto + EPIST

✅ **DO:**
- Store all source facts in EPIST before analysis
- Reference EPIST fact paths in Quarto documents
- Use Mermaid diagrams to show fact→conclusion chains
- Render Quarto to multiple formats (GFM + HTML + DOCX)
- Save Quarto conclusions back to EPIST
- Use `/think` command for complex epistemological analysis

❌ **DON'T:**
- Skip recording facts in EPIST (makes analysis non-traceable)
- Put raw data in Quarto without EPIST provenance
- Forget to reference source facts in conclusions
- Use only one output format (leverage multi-format rendering)

#### Example: Full EPIST → Quarto → EPIST Cycle

```bash
# 1. Initialize EPIST knowledge base
epist init

# 2. Record facts from multiple sources
epist add fact   # Survey results
epist add fact   # Interview notes
epist add fact   # Metrics data

# 3. Analyze with Quarto using /think
/think Why did team autonomy scores drop in Q4?

# 4. LLM creates Quarto document with:
#    - EPIST fact references
#    - Visual provenance (Mermaid)
#    - Statistical analysis (charts, LaTeX)
#    - Formatted tables (Great Tables)
#    - Multi-format output (GFM, HTML, DOCX)

# 5. Save conclusions back to EPIST
epist add conclusion
# Reference the Quarto analysis as source

# 6. Search for related analysis later
epist search "autonomy analysis" --type conclusion
```

#### Migration from Marimo

**Previous workflow (deprecated):**
- marimo for reactive notebooks
- Manual EPIST integration
- Limited provenance visualization

**New workflow (recommended):**
- Quarto for static analysis with full epistemological chain
- Direct EPIST integration via `/think` command
- Visual provenance with Mermaid diagrams
- Multi-format output (GFM, HTML, DOCX)
- Professional presentation (charts, LaTeX, formatted tables)

**For interactive analysis:**
- Use marimo for exploration during development
- Export to Quarto for final analysis and sharing
- Store facts/conclusions in EPIST for long-term tracking

## Common Use Cases

### Research Projects

Track research findings, sources, and conclusions for long-term projects.

```bash
epist init
# Add facts from papers, interviews, experiments
# Build conclusions based on evidence
# Trace provenance when writing reports
```

### Team Metrics Analysis

Record team metrics and derive insights.

```bash
# Add metric facts (surveys, dashboards, reports)
# Create conclusions about team health
# Track changes over time
# Trace conclusions back to data sources
```

### Decision Making

Document decision-making process with evidence.

```bash
# Record facts about the situation
# Document assumptions and constraints
# Create conclusion with recommendation
# Trace provenance chain for review
```

### Knowledge Management

Build a personal knowledge base with provenance.

```bash
# Add facts from books, articles, experiences
# Create insights and learnings
# Search semantically when needed
# Maintain integrity with Git
```

## Troubleshooting

### Search Returns No Results

```bash
# Check if knowledge base is initialized
epist list

# Verify facts/conclusions exist
ls .epist/

# Rebuild search index (if needed)
# (Future: epist reindex command)
```

### Provenance Trace Shows Staleness

```bash
# Review the stale facts
epist get facts/path/to/stale_fact.md

# Update with new information
epist add fact
# (Create updated version)

# Update dependent conclusions
epist add conclusion
# (Reference new facts)
```

### Git Conflicts

```bash
# If Git conflicts occur in .epist/
cd .epist/
git status
git diff

# Resolve conflicts manually
# Epist stores facts as markdown files
# Standard Git conflict resolution applies
```

## Summary

`epist` provides a systematic way to:
- **Track facts** with proper provenance and sources
- **Build conclusions** based on evidence
- **Search semantically** across your knowledge base
- **Trace provenance** to verify reasoning chains
- **Maintain integrity** using Git version control

**Core workflow:**
1. `epist init` - Initialize knowledge base
2. `epist add fact` - Record factual claims
3. `epist add conclusion` - Derive insights
4. `epist search` - Find relevant information
5. `epist trace` - Verify provenance chains

**Integration:**
- Git for version control and integrity
- Lancer for semantic search
- MCP for AI tool integration

Use `epist` when you need to maintain epistemological rigor in research, analysis, decision-making, or knowledge management.
