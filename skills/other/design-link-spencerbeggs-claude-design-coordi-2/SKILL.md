---
name: design-link
description: Generate cross-reference graph showing relationships between design documents. Use when visualizing doc dependencies, finding related docs, or understanding documentation structure.
allowed-tools: Read, Glob, Bash
context: fork
agent: design-doc-agent
---

# Design Documentation Cross-Reference Graph

Generates visual graphs and reports showing relationships between design
documents based on their frontmatter references and content links.

## Overview

This skill analyzes design documentation to discover and visualize
relationships between documents. It identifies orphaned docs, circular
dependencies, cross-module references, and provides recommendations for
improving documentation connectivity.

## Quick Start

**Full graph:**

```bash
/design-link
```

**Module-specific:**

```bash
/design-link effect-type-registry
```

**Find orphans:**

```bash
/design-link --orphans
```

**JSON output:**

```bash
/design-link --format=json
```

## Parameters

### Optional

- `module`: Limit to specific module (default: all)
- `format`: Output format (mermaid, text, json) (default: mermaid)
- `filter`: Filter by relationship type (related, dependencies, content-links)
- `orphans`: Show only orphaned docs (default: false)

## Workflow

High-level graph generation process:

1. **Parse parameters** to determine scope and output format
2. **Load design.config.json** to identify target modules
3. **Find all design documents** using Glob
4. **Parse references** from frontmatter (related, dependencies) and content
   links
5. **Build graph** with nodes (documents) and edges (references)
6. **Analyze graph** for orphans, circular dependencies, isolated clusters
7. **Generate output** in requested format (Mermaid, text, or JSON)
8. **Provide recommendations** for improving documentation connectivity

For detailed implementation steps, see supporting documentation below.

## Supporting Documentation

When you need detailed information, load the appropriate supporting file:

### For Detailed Workflow

See [instructions.md](instructions.md) for:

- Complete step-by-step graph generation workflow
- Reference extraction from frontmatter and content
- Graph building algorithm (nodes, edges, validation)
- Analysis algorithms (orphans, cycles, clusters)
- Output generation for each format
- Recommendation strategies
- Advanced features (metrics, subgraphs, impact analysis)

**Load when:** Generating graphs or need implementation details

### For Graph Algorithms

See [graph-algorithms.md](graph-algorithms.md) for:

- Graph structure (nodes, edges)
- Orphan detection algorithm
- Circular dependency detection
- Connected components analysis
- Bidirectional and one-way detection
- Cross-module analysis
- Metrics calculation

**Load when:** Need algorithm details or implementing custom analysis

### For Output Formats

See [output-formats.md](output-formats.md) for:

- Mermaid diagram generation (syntax, styling, legends)
- Text report structure and sections
- JSON schema and format
- Format selection guidelines

**Load when:** Generating output or need format specifications

### For Usage Examples

See [examples.md](examples.md) for:

- Full graph for all modules
- Orphaned docs report
- Dependency graph only
- Module-specific graph
- Cross-module references
- Bidirectional vs one-way analysis
- Error scenarios (no docs, broken references)

**Load when:** User needs examples or clarification

## Error Handling

### No Design Docs Found

```text
INFO: No design documents found in {module}

This is normal for new modules. Run /design-init to create your first
design doc.
```

### Broken References

```text
WARNING: Broken references detected in {doc}
- {broken-path-1}
- {broken-path-2}

Fix: Remove reference from frontmatter or create the missing document
```

## Integration

Works well with:

- `/design-review` - Review docs flagged as orphaned
- `/design-update` - Add missing cross-references
- `/design-validate` - Ensure references are valid
- `/design-search` - Find related docs to add references

## Success Criteria

A successful link analysis:

- ✅ All design docs discovered
- ✅ All references extracted (frontmatter + content)
- ✅ Graph built correctly
- ✅ Orphans identified
- ✅ Circular dependencies detected
- ✅ Clear visualization generated
- ✅ Actionable recommendations provided
