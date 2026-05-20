---
name: meta:write-docs
description: Guidelines and patterns for writing Kagenti documentation
---

# Write Documentation

## Table of Contents

- [When to Use](#when-to-use)
- [Document Structure](#document-structure)
- [Formatting Rules](#formatting-rules)
- [Diagrams](#diagrams)
- [Tables](#tables)
- [Code Blocks](#code-blocks)
- [Cross-References](#cross-references)
- [Checklist](#checklist)
- [Template](#template)

## When to Use

- Creating new documentation under `docs/`
- Writing design documents, guides, or reference material
- Updating existing docs with new sections

## Document Structure

Every document follows this skeleton:

```markdown
# Title

Brief one-paragraph description of what this document covers and who it is for.

## Table of Contents

- [Section One](#section-one)
- [Section Two](#section-two)
  - [Subsection](#subsection)

---

## Section One

Content here.

---

## Section Two

### Subsection

Content here.
```

**Rules:**

1. Single `#` title at the top
2. One-paragraph overview immediately after the title
3. TOC with anchor links for documents over 50 lines
4. `---` horizontal rules between major sections
5. Keep explanations concise - prefer bullets and tables over prose
6. Use `###` subsections to break up long sections

## Formatting Rules

### Text

- **Bold** for key terms, component names, and emphasis
- `inline code` for commands, file paths, variable names, API endpoints
- *Italic* for introducing new terminology (first use only)
- Blockquotes for callouts:

```markdown
> **Note:** Additional context that supplements the main text.

> **Warning:** Something that can cause problems if ignored.

> **Prerequisite:** Something required before proceeding.
```

### Lists

- Bullet lists (`-`) for unordered items
- Numbered lists (`1.`) for sequential steps or ranked items
- Keep list items concise (1-2 lines)
- Nest at most 2 levels deep

### Expandable Sections

Use `<details>` for optional or advanced content:

```markdown
<details>
<summary>Advanced: Custom collector configuration</summary>

Content that most readers can skip.

</details>
```

## Diagrams

### Mermaid (for flows and relationships)

Use Mermaid for process flows, state machines, and component relationships.
Wrap in ` ```mermaid ` code fences:

```markdown
` ` `mermaid
flowchart LR
    A[Source] --> B[Processor]
    B --> C[Exporter]
` ` `
```

**Mermaid patterns:**

| Type | Use Case | Directive |
|------|----------|-----------|
| `flowchart LR` | Left-to-right process flows | Data pipelines, request flows |
| `flowchart TB` | Top-to-bottom hierarchies | Component trees, deployment order |
| `sequenceDiagram` | Request/response interactions | API calls, auth flows |
| `stateDiagram-v2` | Lifecycle states | Pod states, build stages |
| `graph TB` with `subgraph` | Grouped components | Architecture with namespaces |

**Style tips:**

- Use `subgraph` to group related components (e.g., by namespace or cluster)
- Add labels on edges: `A -->|"OTLP gRPC"| B`
- Keep node labels short (3-4 words max)
- Use `:::className` for visual distinction when needed

### ASCII Art (for architecture layouts)

Use ASCII art for spatial layouts showing where components live physically
(clusters, namespaces, nodes). Wrap in ` ```text ` or ` ```shell `:

```text
+----------------------------+
|    Management Cluster      |
|  +--------+  +---------+  |
|  | Prom   |  | Alerts  |  |
|  +---^----+  +----^----+  |
+------|-----------|---------+
       |           |
+------|-----------|---------+
|    Hosted Cluster          |
|  +--------+  +---------+  |
|  | OTEL   |  | Agents  |  |
|  +--------+  +---------+  |
+----------------------------+
```

**ASCII art rules:**

- Use `+`, `-`, `|` for borders (not Unicode box-drawing characters in code blocks)
- Use `^`, `v`, `<`, `>` for directional arrows
- Align columns for readability
- Label every box
- Keep width under 80 characters

### When to use which

| Scenario | Use |
|----------|-----|
| Data flows, pipelines | Mermaid `flowchart` |
| API interactions | Mermaid `sequenceDiagram` |
| Cluster/namespace layouts | ASCII art |
| Component lifecycle | Mermaid `stateDiagram` |
| Decision trees | Mermaid `flowchart` with conditions |

## Tables

Use tables for structured reference data. Keep column count to 3-5:

```markdown
| Component | Purpose | Namespace |
|-----------|---------|-----------|
| OTEL Collector | Telemetry pipeline | `kagenti-system` |
| TempoStack | Trace storage | `tempo-system` |
```

**Table rules:**

- Header row always present
- Left-align text, right-align numbers
- Use `inline code` for technical values
- Keep cell content to 1 line when possible

## Code Blocks

### Commands

Always specify language. Use `bash` for shell commands:

````markdown
```bash
kubectl get pods -n kagenti-system
```
````

### YAML/JSON manifests

Include just the relevant fields, not entire manifests. Add a comment
at the top identifying the resource:

````markdown
```yaml
# charts/kagenti/templates/observability/collector.yaml
apiVersion: opentelemetry.io/v1beta1
kind: OpenTelemetryCollector
metadata:
  name: kagenti-collector
spec:
  mode: daemonset
```
````

### Expected output

Show expected output after commands when it aids understanding:

````markdown
```bash
kubectl get tempostacks -n tempo-system
```

```text
NAME            AGE   STATUS
kagenti-tempo   5m    Ready
```
````

## Cross-References

- Link to other docs with relative paths: `[Components](../components.md)`
- Link to source files: `[check-capacity.sh](../../.github/scripts/hypershift/ci/slots/check-capacity.sh)`
- Link to external references at the bottom in a `## References` section
- Use descriptive link text, not "click here"

## Checklist

Before committing documentation:

- [ ] Title and one-paragraph overview present
- [ ] TOC with working anchor links (if >50 lines)
- [ ] Sections separated by `---`
- [ ] Code blocks have language tags
- [ ] Diagrams render correctly (Mermaid syntax valid, ASCII aligned)
- [ ] Tables have header rows
- [ ] Cross-references use relative paths
- [ ] No broken links
- [ ] Concise - no unnecessary prose

## Template

```markdown
# Document Title

Brief description of what this document covers and its audience.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)
- [References](#references)

---

## Overview

Context and goals in 2-3 sentences.

---

## Architecture

` ` `mermaid
flowchart LR
    A[Component A] -->|protocol| B[Component B]
` ` `

---

## Configuration

### Component Name

` ` `yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: example
` ` `

| Parameter | Default | Description |
|-----------|---------|-------------|
| `key` | `value` | What it does |

---

## Troubleshooting

### Problem: Description

**Symptom**: What you observe
**Cause**: Why it happens
**Fix**: How to resolve

---

## References

- [External Doc](https://example.com)
- [Related Internal Doc](../related.md)
```

## Related Skills

- `skills:write` - Template for creating skills (different from docs)
