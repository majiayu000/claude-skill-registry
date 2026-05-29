---
name: ops-darpa
description: >
  Query DARPA programs, opportunities, and BAAs. Searches RSS feeds and Grants.gov API
  for defense research funding opportunities across all DARPA technical offices.
allowed-tools:
  - Bash
  - Read
  - Write
triggers:
  - darpa
  - darpa programs
  - defense research
  - baa
  - broad agency announcement
  - darpa funding
  - i2o
  - mto
  - dso
  - bto
metadata:
  short-description: DARPA programs and funding opportunities
---

# DARPA Operations Skill

Query DARPA (Defense Advanced Research Projects Agency) for:
- **Programs** - Active and completed research programs
- **Opportunities** - BAAs (Broad Agency Announcements) and funding
- **Federal Grants** - Via Grants.gov API for DOD/DARPA opportunities

## Data Sources

| Source | Type | Auth | Updates |
|--------|------|------|---------|
| DARPA RSS | Feed | None | Real-time |
| DARPA Opportunities RSS | Feed | None | Real-time |
| Grants.gov API | REST | None | Daily |

## DARPA Technical Offices

| Office | Code | Focus Area |
|--------|------|------------|
| Information Innovation Office | I2O | AI, cybersecurity, software |
| Microsystems Technology Office | MTO | Hardware, 5G/6G, microsystems |
| Defense Sciences Office | DSO | Foundational science, materials |
| Biological Technologies Office | BTO | Biotechnology, synthetic biology |
| Strategic Technology Office | STO | Strategic systems |
| Tactical Technology Office | TTO | Tactical military systems |

## Quick Start

```bash
# List recent DARPA programs
./run.sh programs

# Filter by office
./run.sh programs --office I2O

# Search opportunities (BAAs)
./run.sh opportunities --keyword "artificial intelligence"

# Search Grants.gov for DARPA funding
./run.sh grants --keyword "cybersecurity"

# Get program details
./run.sh program "AI Cyber Challenge"
```

## Commands

### `programs` - List DARPA Programs

List active and recent DARPA research programs.

```bash
# All recent programs
./run.sh programs

# Filter by technical office
./run.sh programs --office I2O
./run.sh programs --office MTO
./run.sh programs --office DSO

# Search by keyword
./run.sh programs --keyword "quantum"

# Include completed programs
./run.sh programs --include-completed

# Output as JSON
./run.sh programs --json
```

### `opportunities` - DARPA BAAs and Opportunities

Search DARPA funding opportunities from RSS feed.

```bash
# Recent opportunities
./run.sh opportunities

# Filter by office
./run.sh opportunities --office I2O

# Search by keyword
./run.sh opportunities --keyword "machine learning"

# Output as JSON
./run.sh opportunities --json
```

### `grants` - Search Grants.gov

Search federal grant opportunities via Grants.gov API.

```bash
# Search DARPA grants
./run.sh grants --keyword "AI"

# Filter by status
./run.sh grants --keyword "cyber" --status forecasted
./run.sh grants --keyword "cyber" --status posted

# Search all DOD (includes DARPA)
./run.sh grants --keyword "robotics" --agency DOD

# Limit results
./run.sh grants --keyword "quantum" --limit 20

# Output as JSON
./run.sh grants --keyword "5G" --json
```

**Grant statuses:**
- `forecasted` - Upcoming opportunities
- `posted` - Currently accepting applications
- `closed` - No longer accepting
- `archived` - Historical

### `baas` - Office-Wide BAAs

List the standing office-wide BAAs (always open for revolutionary ideas).

```bash
# List all office-wide BAAs
./run.sh baas

# Get specific office BAA
./run.sh baas --office I2O
```

### `feed` - Raw RSS Feed

Get raw RSS feed data for custom processing.

```bash
# Programs feed
./run.sh feed programs

# Opportunities feed
./run.sh feed opportunities

# Output as JSON
./run.sh feed programs --json
```

## Use Cases

### Research Intelligence

```bash
# What is DARPA funding in AI?
./run.sh programs --keyword "artificial intelligence"
./run.sh grants --keyword "AI" --status posted

# Track I2O cybersecurity programs
./run.sh programs --office I2O --keyword "cyber"
```

### Funding Opportunities

```bash
# Find open BAAs for my research area
./run.sh opportunities --keyword "quantum computing"
./run.sh grants --keyword "quantum" --status forecasted
```

### Competitive Intelligence

```bash
# What's DARPA investing in for 2025-2026?
./run.sh programs --include-completed false
./run.sh grants --status forecasted
```

### Technology Scouting

```bash
# Find programs related to specific tech
./run.sh programs --keyword "5G security"
./run.sh programs --keyword "autonomous systems"
```

## Integration with Dogpile

DARPA sources are available in dogpile research:

```bash
# Security research with DARPA context
dogpile search "AI cybersecurity" --preset bleeding_edge

# The preset includes DARPA RSS in sources
```

## RSS Feed URLs

For direct access:
- **Programs/News:** `https://www.darpa.mil/rss.xml`
- **Opportunities:** `https://www.darpa.mil/rss/opportunities.xml`

## Grants.gov API

The skill uses the public Grants.gov Search2 API:
- **Endpoint:** `https://api.grants.gov/v1/api/search2`
- **Method:** POST with JSON body
- **Auth:** None required for search

## Related Resources

- [DARPA Programs](https://www.darpa.mil/research/programs)
- [DARPA Opportunities](https://www.darpa.mil/work-with-us/opportunities)
- [Office-Wide BAAs](https://www.darpa.mil/research/opportunities/baa)
- [Grants.gov](https://www.grants.gov)
- [SAM.gov Opportunities](https://sam.gov) (use ops-sam-gov skill)
