---
name: research
description: Company due diligence, technology deep-dives, market analysis, and topic exploration for cyber•Fund investment decisions, content creation, and personal projects. Supports 3 intensity levels (quick/standard/deep) for speed-quality tradeoffs.
---

# Research Skill

Company due diligence, technology deep-dives, market analysis, and topic exploration for cyber•Fund investment decisions, content creation, and personal projects.

## Capabilities

- **Company Research**: Comprehensive DD on target companies
- **Technology Research**: Deep technical analysis of technologies
- **Market Research**: Market sizing, dynamics, and opportunity assessment
- **Topic Research (Content)**: Ideas, narratives, people for essays/tweets
- **Topic Research (Investment)**: Market dynamics and opportunities for investment thesis

## Research Intensity Levels

- **🔍 Quick** (10-30s): 1 agent
- **🔬 Standard** (2-5m): 2-3 agents [DEFAULT]
- **🔎 Deep** (5-15m): 3-5 agents + quality-reviewer

See `shared/intensity-tiers.md` for full specification.

## Workflow

All research types use **one universal workflow**:
- `workflows/orchestrator.md`

The orchestrator dynamically selects agents based on research type and intensity.

## Agent Selection

See `shared/agent-selection-matrix.md` for full matrix.

| Research Type | Quick | Standard | Deep |
|---------------|-------|----------|------|
| Company DD | company | company + market + financial | +team +quality-reviewer |
| Technology | tech | tech + market | +company +quality-reviewer |
| Market | market | market + financial | +company +quality-reviewer |
| Topic-Content | content | content | +quality-reviewer |
| Topic-Investment | investment | investment + market | +financial +quality-reviewer |

## Agents

**Research agents** (autonomous MCP access):
- `company-researcher`: Business model, product, traction
- `market-researcher`: TAM, dynamics, trends
- `financial-researcher`: Funding, metrics, comparables
- `team-researcher`: Founder backgrounds, team assessment
- `tech-researcher`: Technology deep-dives
- `content-researcher`: Academic papers, social media, first-principles (for content)
- `investment-researcher`: Market dynamics, opportunities, timing (for investment)

**Quality & Synthesis**:
- `quality-reviewer`: Gap analysis, contradiction detection (deep only, max 1 iteration)
- `synthesizer`: Consolidate parallel research outputs

## Common References

- `shared/agent-selection-matrix.md` - Dynamic agent selection
- `shared/investment-lens.md` - cyber•Fund investment philosophy
- `shared/mcp-strategy.md` - MCP tool selection
- `shared/output-standards.md` - Formats and emoji conventions
- `shared/intensity-tiers.md` - 3-tier intensity spec

## Output Locations

All research creates timestamped workspace:

```
~/CybosVault/private/deals/<company>~/CybosVault/private/research/MMDD-<slug>-YY/   # Company
~/CybosVault/private/research/<topic>/MMDD-<slug>-YY/           # Tech/Market/Topic
├── raw/                                     # Agent outputs
└── report.md                                # Final synthesis
```

## Key Principles

1. **Agents do ALL data gathering** - Main session orchestrates, agents make MCP calls
2. **No redundancy** - Each agent makes its own calls autonomously
3. **Dynamic selection** - Agents chosen based on research type + intensity
4. **Quality loop** - Deep mode includes quality-reviewer (max 1 iteration)

## Investment Context

All research applies cyber•Fund's investment philosophy:
- Path to $1B+ revenue (not niche $50M ARR outcomes)
- Defensible moat (data, network effects, hard tech)
- Clear business model (revenue > token speculation)
- Strong founders (high energy, sales DNA, deep expertise)
- Market timing ("why now?")
