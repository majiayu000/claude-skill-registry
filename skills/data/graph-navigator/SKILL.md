# graph-navigator

Navigate and manipulate the semantic knowledge graph for the SDLC Agêntico corpus.

## Overview

The `graph-navigator` skill provides tools for:
- Building and maintaining the semantic graph from corpus documents
- Navigating relationships between decisions, learnings, patterns, and concepts
- Extracting concepts from documents automatically
- Generating visualizations (Mermaid, DOT)
- Finding paths and transitive relationships

## Version

**v1.4.0** - Initial release with semantic graph support

## Scripts

### graph_manager.py

CRUD operations on the semantic graph.

```bash
# Add a node
python3 .claude/skills/graph-navigator/scripts/graph_manager.py add \
    --id ADR-015 \
    --type Decision \
    --title "Use Redis for caching"

# Add an edge (relationship)
python3 .claude/skills/graph-navigator/scripts/graph_manager.py edge \
    --source ADR-015 \
    --relation dependsOn \
    --target ADR-001

# Get neighbors (1 hop)
python3 .claude/skills/graph-navigator/scripts/graph_manager.py neighbors ADR-001

# Get neighbors (2 hops, outgoing only)
python3 .claude/skills/graph-navigator/scripts/graph_manager.py neighbors ADR-001 \
    --hops 2 \
    --direction outgoing

# Find shortest path between nodes
python3 .claude/skills/graph-navigator/scripts/graph_manager.py path ADR-001 ADR-010

# Get transitive closure (all dependencies)
python3 .claude/skills/graph-navigator/scripts/graph_manager.py closure ADR-001 \
    --relation dependsOn

# Show graph statistics
python3 .claude/skills/graph-navigator/scripts/graph_manager.py stats

# Validate graph integrity
python3 .claude/skills/graph-navigator/scripts/graph_manager.py validate

# List nodes
python3 .claude/skills/graph-navigator/scripts/graph_manager.py list --type Decision
```

### graph_builder.py

Build the graph from corpus YAML files.

```bash
# Full rebuild
python3 .claude/skills/graph-navigator/scripts/graph_builder.py

# Rebuild with relation inference (finds related nodes by shared concepts)
python3 .claude/skills/graph-navigator/scripts/graph_builder.py --infer

# Dry run (show stats without saving)
python3 .claude/skills/graph-navigator/scripts/graph_builder.py --dry-run

# Incremental update for single file
python3 .claude/skills/graph-navigator/scripts/graph_builder.py \
    --incremental .project/corpus/nodes/decisions/adr-015.yml
```

### concept_extractor.py

Extract concepts from corpus documents.

```bash
# Show extracted concepts as JSON
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py --output json

# Save concepts as YAML files
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py --output save

# Filter by minimum confidence
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py \
    --min-confidence 0.5

# Show extraction statistics
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py --output stats

# Extract from single file
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py \
    --file .project/corpus/nodes/decisions/adr-001.yml
```

### graph_visualizer.py

Generate visualizations from the graph.

```bash
# Generate Mermaid diagram
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py --format mermaid

# Generate DOT format (for Graphviz)
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py --format dot

# Filter by node type
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py \
    --format mermaid \
    --type Decision

# Filter by phase
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py \
    --format mermaid \
    --phase 3

# Generate subgraph around a node
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py \
    --format mermaid \
    --center ADR-001 \
    --hops 2

# Show graph metrics
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py --metrics

# Save to file
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py \
    --format mermaid \
    --output graph.md
```

## Semantic Relations

| Relation | Description | Example |
|----------|-------------|---------|
| `supersedes` | Replaces previous decision | ADR-002 supersedes ADR-001 |
| `implements` | Implements a pattern | ADR-005 implements PATTERN-cqrs |
| `addresses` | Addresses a requirement | ADR-003 addresses REQ-security |
| `causedBy` | Learning caused by incident | LEARNING-001 causedBy INC-001 |
| `relatedTo` | Generic relation (bidirectional) | ADR-001 relatedTo ADR-002 |
| `dependsOn` | Depends on another decision | ADR-005 dependsOn ADR-001 |
| `usedIn` | Used in SDLC phase | ADR-001 usedIn phase-3 |
| `isA` | Concept hierarchy | postgresql isA relational-database |
| `partOf` | Part-of relation | auth-service partOf api-layer |

## Node Types

| Type | Prefix | Description |
|------|--------|-------------|
| `Decision` | ADR- | Architecture Decision Record |
| `Learning` | LEARNING- | Lesson learned from incidents/retros |
| `Pattern` | PATTERN- | Design or implementation pattern |
| `Concept` | CONCEPT- | Extracted concept from documents |

## Files Generated

| File | Description |
|------|-------------|
| `.project/corpus/graph.json` | Main graph with nodes and edges |
| `.project/corpus/adjacency.json` | Adjacency index for fast traversal |
| `.project/corpus/index.yml` | Text search index |
| `.project/corpus/nodes/concepts/*.yml` | Extracted concept nodes |

## Integration with Other Skills

### rag-query

The `hybrid_search.py` script uses the graph for expanded search:

```bash
python3 .claude/skills/rag-query/scripts/hybrid_search.py "database" --mode hybrid
```

Results include:
- Direct text matches
- Graph-expanded related nodes
- Combined relevance scores

### memory-manager

When saving decisions/learnings, the graph can be updated incrementally:

```bash
# After saving a new ADR
python3 .claude/skills/graph-navigator/scripts/graph_builder.py \
    --incremental .project/corpus/nodes/decisions/adr-new.yml
```

### gate-evaluator

The `graph-integrity` gate validates:
- Graph file exists and is valid
- No orphan edges
- Consistent adjacency
- Minimum coverage thresholds

## Usage Examples

### Impact Analysis

Find all decisions affected by changing ADR-001:

```bash
python3 .claude/skills/graph-navigator/scripts/graph_manager.py neighbors ADR-001 \
    --hops 3 \
    --direction incoming
```

### Decision Chain

Find the path from a feature decision to its dependencies:

```bash
python3 .claude/skills/graph-navigator/scripts/graph_manager.py path ADR-010 ADR-001
```

### Knowledge Map

Generate a visual map of architecture decisions:

```bash
python3 .claude/skills/graph-navigator/scripts/graph_visualizer.py \
    --format mermaid \
    --type Decision \
    --output docs/architecture-graph.md
```

### Concept Discovery

Extract and review concepts before adding to graph:

```bash
python3 .claude/skills/graph-navigator/scripts/concept_extractor.py \
    --output json \
    --min-confidence 0.6 \
    --top 20
```

## Allowed Tools

- Read
- Write
- Glob
- Bash

## Dependencies

**None** - Uses only Python standard library + PyYAML (already installed)

## Agents Using This Skill

| Agent | Usage |
|-------|-------|
| `system-architect` | Impact analysis, decision chains |
| `domain-researcher` | Knowledge mapping, concept discovery |
| `rag-curator` | Graph maintenance, corpus organization |
| `adr-author` | Finding related decisions |
