---
name: excalidraw
description: Create professional diagrams and visualizations using Excalidraw JSON format. Specialized for IT architecture diagrams, flowcharts, network topology, system design, microservices, ER diagrams, and state machines. Includes curated color palettes and visual styles. Use when working with .excalidraw files, or when user mentions diagrams, flowcharts, architecture visualization, or drawing. Delegates to subagents to prevent context exhaustion from verbose JSON.
---

# Excalidraw Diagram Skill

Create professional diagrams in Excalidraw JSON format.

## Critical: Subagent Delegation

**Main agents must NEVER read .excalidraw files directly.**

Excalidraw JSON is extremely verbose (4,000 - 22,000+ tokens per file). Always delegate to subagent and request **text summaries**, never raw JSON.

```
Main Agent                          Subagent
    │                                   │
    ├── Provide task description ──────►│
    │                                   ├── Read/parse files
    │                                   ├── Execute operations
    │◄── Receive text summary ──────────┤
```

---

## Component Libraries

Use pre-built components from `libraries/` folder first.

### Library Selection

| Diagram Type | Libraries |
|--------------|-----------|
| AWS | `aws-architecture-icons` |
| Azure | `azure-cloud-services` |
| GCP | `gcp-icons`, `google-icons` |
| System Design | `software-architecture`, `system-design` |
| Microservices | `software-architecture`, `kubernetes-icons` |
| Database/ER | `database`, `uml-er-library` |
| Flowchart | `flow-chart-symbols` |
| Network | `network-topology-icons` |
| DevOps/CI/CD | `devops-icons`, `technology-logos` |
| Wireframe | `basic-ux-wireframing`, `web-kit` |

### Priority Order

1. **Pre-downloaded** → Check `libraries/` folder
2. **Online** → Fetch from [libraries.excalidraw.com](https://libraries.excalidraw.com/)
3. **Custom** → Build from basic shapes (last resort)

See [LIBRARIES.md](LIBRARIES.md) for usage details.

---

## Workflow

### Create Diagram

1. Identify diagram type from user request
2. Select appropriate library and palette
3. Generate JSON with all required properties (see [JSON-SCHEMA.md](JSON-SCHEMA.md))
4. Verify against Quality Checklist

### Modify Diagram

1. Read and parse existing file (via subagent)
2. Apply requested changes
3. Maintain style consistency
4. Return summary of changes

---

## Defaults

| Setting | Default | Notes |
|---------|---------|-------|
| Style | `hand-drawn` | Excalidraw signature look |
| Font | `fontFamily: 1` (Virgil) | Authentic hand-drawn feel |
| Roughness | `1` | Hand-drawn effect |
| Grid | `20px` | Alignment base |

---

## Quality Checklist

Before delivering:

- [ ] Visual hierarchy clear
- [ ] Color follows 60-30-10 rule
- [ ] Text contrast ≥4.5:1 (WCAG AA)
- [ ] Elements aligned to 20px grid
- [ ] Spacing ≥40px between elements
- [ ] All connections clearly directed
- [ ] Key elements labeled
- [ ] Style consistent throughout

---

## Reference Documentation

| Document | Content |
|----------|---------|
| [JSON-SCHEMA.md](JSON-SCHEMA.md) | **Required** - Complete JSON specification |
| [ELEMENTS.md](ELEMENTS.md) | Element types and properties |
| [PALETTES.md](PALETTES.md) | Color palette definitions |
| [STYLES.md](STYLES.md) | Visual style configurations |
| [ICONS.md](ICONS.md) | Hand-drawn icon patterns (fallback) |
| [LIBRARIES.md](LIBRARIES.md) | Component library reference |
| [IT-DIAGRAMS.md](IT-DIAGRAMS.md) | IT architecture templates |
| [TEMPLATES.md](TEMPLATES.md) | General diagram templates |
