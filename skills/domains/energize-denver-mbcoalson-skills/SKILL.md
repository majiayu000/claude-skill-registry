---
name: energize-denver
description: Use when working with Denver's Energize Denver Article XIV building performance regulations. Provides compliance requirements, pathways, deadlines, penalties, MAI production efficiency metrics, benchmarking rules, and performance targets for commercial and multifamily buildings in Denver. Use when the user mentions Energize Denver, Denver Article XIV, MAI buildings, compliance pathways, performance targets, or Denver building performance requirements.
---

# Energize Denver Article XIV Compliance Reference

Authoritative reference for Denver's High-Performance Existing Buildings Program (Article XIV) compliance requirements, pathways, deadlines, and penalties.

## When to Use This Skill

Invoke this skill when working with:
- **Energize Denver compliance questions** - Requirements, deadlines, penalties
- **Denver Article XIV regulations** - Building performance policy details
- **MAI buildings** - Manufacturing, Agricultural, Industrial compliance pathways
- **Performance targets** - Baseline calculations, interim/final targets (2024/2027/2030)
- **Compliance pathways** - Whole-building EUI, production efficiency, prescriptive paths
- **Benchmarking requirements** - Annual submission rules, Energy Star Portfolio Manager
- **Penalty calculations** - Rates, shortfall calculations, enforcement
- **Timeline extensions** - Application process, valid reasons, requirements
- **Alternate compliance options** - Timing adjustments, target modifications

## What This Skill Provides

**Regulatory Knowledge**:
- Complete Article XIV requirements by building size and type
- MAI production efficiency pathway (detailed guidance)
- Performance target calculation methods
- Penalty rates and enforcement procedures
- Deadline and milestone tracking
- Alternate compliance application requirements

**Decision Support**:
- Pathway selection criteria (EUI vs production efficiency vs prescriptive)
- Compliance vs penalty cost analysis
- Timeline extension eligibility assessment

## What This Skill Does NOT Cover

- ❌ Pricing or scoping Energize Denver services → Use **writing-proposals** skill
- ❌ General proposal development → Use **writing-proposals** skill
- ❌ Non-Denver building performance programs
- ❌ Technical energy modeling or audit procedures

## Quick Reference

### Building Categories

**25,000+ sf (Non-MAI)**:
- Annual benchmarking (due June 1)
- Performance targets: 2024, 2027, 2030
- Baseline: Typically 2019 EUI
- Compliance metric: 30% EUI reduction by 2030

**25,000+ sf (MAI Buildings)**:
- Two pathway options: Prescriptive or Performance
- Performance metrics: 30% EUI reduction OR 30% production efficiency OR 52.9 EUI OR ENERGY STAR 75
- First performance year: 2026
- Application deadline: December 31, 2025

**5,000-24,999 sf**:
- LED lighting OR 20% solar by deadline
- Deadlines: Dec 31, 2025/2026/2027 (by size tier)

### Key Deadlines

| Date | Requirement |
|------|-------------|
| **June 1 (annual)** | Benchmarking submission (25k+ sf) |
| **December 31, 2025** | MAI ACO application deadline |
| **December 31, 2025** | Small buildings 15k-25k sf LED/solar |
| **December 31, 2026** | Small buildings 10k-15k sf LED/solar |
| **December 31, 2027** | Small buildings 5k-10k sf LED/solar |
| **June 1, 2025** | Demonstrate 2024 target compliance |
| **June 1, 2028** | Demonstrate 2027 target compliance |
| **June 1, 2031** | Demonstrate 2030 target compliance |

### Penalty Rates (Updated April 2025)

**Standard Commercial Buildings (25,000+ sf)**:
- $0.15/kBtu - Buildings on standard updated timeline
- $0.23/kBtu - Buildings opted into 2028/2032 timeline
- $0.35/kBtu - Buildings granted timeline extensions
- +$0.10/kBtu surcharge - Extensions requested after target year ends

**MAI Buildings**: Same rates apply to production efficiency shortfalls

## How to Use This Skill

### Answer Regulatory Questions

When the user asks about Energize Denver requirements:

1. **Identify the question type**:
   - Building applicability and exclusions?
   - Compliance pathway selection?
   - Performance target calculation?
   - Penalty calculation?
   - Deadline or milestone?
   - Application requirements?

2. **Consult the detailed requirements**:
   - See [./article-xiv-requirements.md](./article-xiv-requirements.md) for complete regulatory reference

3. **Provide specific, actionable answers**:
   - Cite specific sections and requirements
   - Include deadlines, formulas, and rates
   - Explain implications and decision criteria

### Pathway Selection Guidance

When helping users choose compliance pathways:

**For MAI Buildings**, evaluate:
- Production growth expectations
- Production metric clarity and measurability
- Availability of historical production data (2018-2022)
- Process load percentage vs HVAC/lighting
- See [./article-xiv-requirements.md](./article-xiv-requirements.md) → "Production Efficiency Pathway - Detailed Requirements"

**For Standard Commercial Buildings**, evaluate:
- Current EUI vs performance targets
- Feasibility of operational improvements
- Capital improvement budget
- Renewable energy options
- Timeline flexibility needs

### Penalty Calculations

When calculating potential penalties:

1. **Determine shortfall**: Target kBtu reduction - Actual kBtu reduction
2. **Identify penalty rate**: Based on timeline status (see rates above)
3. **Calculate penalty**: Shortfall (kBtu) × Penalty Rate ($/kBtu)
4. **Consider timeline**: Multi-year penalties for ongoing non-compliance

Example from requirements document:
```
Building on 2028/2032 timeline:
  Shortfall: 20,000 kBtu
  Rate: $0.23/kBtu
  Penalty: $4,600
```

### Timeline Extensions

When users ask about timeline extensions:

**Valid Reasons** (from Article XIV):
- End-of-life equipment replacement planning
- Major renovations in progress
- Whole-building electrification projects
- District steam system limitations
- Energy service capacity constraints (requires Xcel documentation)
- Innovative projects causing delays

**Application Requirements**:
- ASHRAE Level II audit
- Detailed compliance plan (CASR template)
- Financing strategy
- Specific measures with timelines

**Important**: Applying after target year ends triggers +$0.10/kBtu surcharge

See [./article-xiv-requirements.md](./article-xiv-requirements.md) → "Timeline Extensions for MAI Buildings" (also applicable to standard buildings)

## Cross-References to Other Skills

**When pricing or scoping Energize Denver services**, use the **writing-proposals** skill:
- ASHRAE Level 1/2/3 audit pricing
- Benchmarking service scoping
- Compliance pathway consulting pricing
- Proposal generation and formatting

**Example collaborative workflow**:
- User: "Create Energize Denver MAI proposal for print shop"
- **energize-denver** (this skill): Identify MAI pathway requirements, production efficiency metric selection, Dec 31 deadline
- **writing-proposals**: Price ASHRAE Level II audit, structure scope of work, generate proposal document

## Complete Regulatory Reference

For comprehensive Article XIV details, see:
- [./article-xiv-requirements.md](./article-xiv-requirements.md)

This file contains:
- Detailed applicability and exclusions
- Complete building category requirements (25k+ sf, 5k-25k sf)
- MAI production efficiency pathway (comprehensive guidance)
- Baseline establishment and target calculations
- Compliance demonstration procedures
- Alternate compliance options and applications
- Enforcement and penalty details
- Timeline extensions and application requirements
- CASR contact information and resources

## External Resources

- [Energize Denver Official Site](https://energizedenver.org/)
- [CASR Building Performance Requirements](https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Climate-Action-Sustainability-and-Resiliency)
- [Denver Municipal Code Article XIV](https://library.municode.com/co/denver/codes/code_of_ordinances?nodeId=TITIIREMUCO_CH10BUCO_ARTXIVHIPEEBU)
- [Energy Star Portfolio Manager](https://www.energystar.gov/buildings/benchmark)

## Known Gaps and Limitations

When consulting [./article-xiv-requirements.md](./article-xiv-requirements.md), note the "Known Gaps and Limitations" section identifies:
- Pre-approved production metrics by industry (not published by CASR)
- Product mix change handling for production efficiency
- Metric change procedures after ACO approval
- MAI ACO application review timelines

**For these questions**, recommend direct CASR contact: energizedenver@denvergov.org

## Important Notes

**This skill provides regulatory guidance only**. It does not:
- Price services (use **writing-proposals** skill)
- Provide detailed engineering analysis
- Substitute for legal counsel
- Replace official CASR guidance

**Always verify**:
- Current penalty rates with CASR (rates updated April 2025)
- Application deadlines and requirements
- Specific building applicability before providing advice

**Data quality matters**:
- Production efficiency requires measured data (estimated data not explicitly allowed)
- Weather normalization required for energy data
- Complete calendar year coverage required (no partial-year data)


## Saving Next Steps

When energize-denver work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "energize-denver" \
  --content "## Priority Tasks
1. Review Energize Denver compliance requirements
2. Calculate MAI production efficiency targets
3. Determine applicable compliance pathway"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`
