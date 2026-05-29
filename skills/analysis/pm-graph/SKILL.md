---
name: pm-graph
description: Visualize the decision graph — show connections between decisions, identify clusters, find central nodes and peripheral orphans, trace the lineage of a specific decision. Text-based graph representation since no visual tool is available. Triggers on "/pm-graph", "/pm-graph [decision]", "show connections", "trace lineage", "decision graph".
user-invocable: true
allowed-tools: Read, Grep, Glob, Bash
context: fork
---

## Runtime Configuration (Step 0)

Read `ops/derivation-manifest.md` for vocabulary.

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse immediately:
- If empty: generate overview graph showing all decisions and their connection counts
- If target is a decision name: generate full lineage trace for that decision
- If "clusters": identify topically clustered decisions
- If "central": find the most-connected decisions (highest graph centrality)

**START NOW.**

---

## Philosophy

**The graph reveals what individual notes cannot: the shape of institutional memory.**

A PM system with 50 decisions and 200 connections between them is fundamentally different from one with 50 decisions and 12 connections. The first has compound institutional memory — you can reason about relationships. The second has an indexed list.

/pm-graph makes the connection density visible. High-connection nodes are architectural load-bearers — changing them has cascade effects. Low-connection nodes are either orphans (structural failure) or genuinely isolated facts (acceptable). Clusters reveal coherent reasoning zones. Bridges between clusters reveal architectural principles that span domains.

This analysis runs without semantic search. It is pure link-extraction — finding `[[wiki-links]]` in notes and mapping them.

---

## Workflow

### Mode 1: Overview Graph

Extract all wiki-links from all decisions and map connection counts:

```bash
# For each decision file, count outgoing links
for f in decisions/*.md; do
  basename=$(basename "$f" .md)
  links=$(rg "\[\[([^\]]+)\]\]" "$f" -o --no-filename | grep -v "register\|index" | wc -l)
  echo "$links $basename"
done | sort -rn | head -30
```

Output: ranked list of decisions by connection count.

### Mode 2: Decision Lineage Trace

For a named decision, trace all connections bidirectionally:

```bash
# Find the decision file
target_file=$(ls decisions/ | grep -i "target-name" | head -1)

# Find all decisions that LINK TO this decision
rg "\[\[$target_file\]\]" decisions/ --include="*.md" -l

# Find all decisions this decision LINKS TO
rg "\[\[([^\]]+)\]\]" "decisions/$target_file" -o --no-filename
```

Repeat recursively for 2 hops to show the extended neighborhood.

### Mode 3: Cluster Detection

Group decisions by their shared register membership and cross-links:

```bash
# For each register, get the decisions it contains
for reg in decisions/*-register.md; do
  echo "=== $(basename $reg) ==="
  rg "\[\[([^\]]+)\]\]" "$reg" -o --no-filename | grep -v "register\|index"
done
```

Decisions that appear in multiple registers are bridge nodes — they connect reasoning zones.

### Mode 4: Central Nodes

High-centrality nodes are decisions referenced by many others. They are the load-bearers.

```bash
# Count how many times each decision is referenced by other decisions
for f in decisions/*.md; do
  basename=$(basename "$f" .md)
  refs=$(rg "\[\[$basename\]\]" decisions/ --include="*.md" -l | wc -l)
  echo "$refs $basename"
done | sort -rn | head -20
```

---

## Output Format

### Overview Mode
```
## Decision Graph Overview — YYYY-MM-DD

### Most Connected Decisions (Top 10)
1. [[validation-block-enforcement]] — 12 connections
2. [[vc-architecture-3phase-redesign]] — 9 connections
3. [[qftest-groovy-casing]] — 7 connections
...

### Most Referenced (Incoming Links)
1. [[sprint-1-security-remediation]] — referenced by 8 decisions
2. [[validation-block-enforcement]] — referenced by 6 decisions
...

### Orphan Decisions (No Connections)
- [[decision-name]] — no incoming or outgoing links

### Graph Density
Total decisions: N
Total connections: N
Average connections per decision: N.N
Bridge nodes (appear in 2+ registers): N

### Observations
- [Pattern: high clustering around QFTest decisions — most tech-facts are interconnected]
- [Pattern: enforcement decisions are well-connected; architectural decisions have fewer links]
- [Gap: sprint records have low outgoing connections — decisions from sprints are not being linked back]
```

### Lineage Mode
```
## Decision Lineage: [[target-decision]]

### The Decision
[Full title and one-line description]

### Upstream (decisions this depends on or was informed by)
- [[decision-a]] — relationship: implements | because: [reason]
- [[decision-b]] — relationship: surfaces | because: [reason]

### Downstream (decisions that reference or were created by this)
- [[decision-c]] — relationship: validates | because: [reason]
- [[decision-d]] — relationship: extends | because: [reason]

### Extended Neighborhood (2 hops)
- Via [[decision-a]]: [[decision-e]], [[decision-f]]
- Via [[decision-c]]: [[decision-g]]

### Lineage Summary
This decision is [central / peripheral / bridge / isolated].
[One sentence on what this position means for PM coordination.]
```
