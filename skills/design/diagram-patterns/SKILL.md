---
name: diagram-patterns
description: Decision guidance for selecting the right diagram type and tool. Provides patterns for common visualization scenarios, tool comparison, and best practices.
allowed-tools: Read, Glob, Grep, Skill, AskUserQuestion
---

# Diagram Selection & Patterns

## Interactive Diagram Selection

Use AskUserQuestion to understand requirements and recommend the optimal diagram type and tool:

```yaml
# Question 1: Primary Purpose (MCP: CLI best practices - scope selection)
question: "What are you trying to visualize?"
header: "Purpose"
options:
  - label: "System Architecture (Recommended)"
    description: "Components, services, containers, deployment"
  - label: "Process/Workflow"
    description: "Steps, decisions, activities, state transitions"
  - label: "Data Structures"
    description: "Classes, entities, relationships, schemas"
  - label: "Interactions"
    description: "Sequence of calls, messages, API flows"

# Question 2: Tool Constraints (MCP: CLI best practices - output format)
question: "Do you have tool or platform constraints?"
header: "Tool"
options:
  - label: "GitHub/GitLab Markdown (Recommended)"
    description: "Use Mermaid - native rendering, no setup"
  - label: "Maximum Customization"
    description: "Use PlantUML - more styling, sprites, icons"
  - label: "Enterprise Architecture"
    description: "Use PlantUML - C4, ArchiMate support"
  - label: "No Preference"
    description: "I'll recommend based on diagram type"
```

Use these responses to apply the decision tree and recommend the appropriate diagram type and tool.

## Overview

This skill helps you choose the right diagram type and tool for your visualization needs. Use this when you need to decide:

1. **Which diagram type** best represents your information
2. **Which tool** (Mermaid or PlantUML) to use
3. **How to structure** the diagram for clarity

---

## Diagram Type Decision Tree

```text
START
  |
  +-- Interactions over time? --> SEQUENCE DIAGRAM
  |
  +-- Object/class structure? --> CLASS DIAGRAM
  |
  +-- Database schema? --> ER DIAGRAM
  |
  +-- State transitions? --> STATE DIAGRAM
  |
  +-- Process/workflow? --> FLOWCHART or ACTIVITY DIAGRAM
  |
  +-- System architecture?
  |     |
  |     +-- High-level context? --> C4 CONTEXT
  |     +-- Containers/services? --> C4 CONTAINER or COMPONENT
  |     +-- Infrastructure? --> DEPLOYMENT DIAGRAM
  |
  +-- Project timeline? --> GANTT CHART
  |
  +-- Git branching? --> GIT GRAPH (Mermaid only)
  |
  +-- Hierarchical ideas? --> MINDMAP (PlantUML only)
  |
  +-- Data structure? --> JSON DIAGRAM (PlantUML only)
```

---

## Tool Selection Guide

### Quick Decision Matrix

| Need | Recommended Tool | Reason |
| --- | --- | --- |
| GitHub/GitLab rendering | **Mermaid** | Native support |
| Complex C4 models | **PlantUML** | Mature, better rendering |
| Simple sequence/class | **Mermaid** | Simpler syntax |
| MindMaps | **PlantUML** | Only option |
| JSON visualization | **PlantUML** | Only option |
| GitGraph | **Mermaid** | Only option |
| ER diagrams | **Mermaid** | Better default rendering |
| State diagrams | **Mermaid** | Cleaner output |
| Maximum customization | **PlantUML** | More styling options |
| Zero setup | **Mermaid** | Browser-based |
| Enterprise architecture | **PlantUML** | Better ArchiMate, C4 |

### Detailed Comparison

| Feature | Mermaid | PlantUML |
| --- | --- | --- |
| **Setup** | None (browser) | Java + GraphViz |
| **Markdown integration** | Native (GitHub, GitLab) | Requires image embedding |
| **Learning curve** | Gentle | Steeper |
| **Customization** | Limited | Extensive |
| **C4 support** | Experimental | Mature |
| **Diagram types** | ~10 | 15+ |
| **JSON/MindMap** | No | Yes |
| **GitGraph** | Yes | No |

### When to Choose Mermaid

- Documentation that lives in GitHub/GitLab repos
- Quick diagrams that need no setup
- Teams with mixed technical backgrounds
- Simple to moderately complex diagrams

### When to Choose PlantUML

- Complex enterprise architecture (C4, ArchiMate)
- Maximum control over appearance
- Specialized diagrams (MindMap, JSON, WBS)
- Need for sprites/icons

---

## Quick Reference: Choosing Diagram Type

| Question | If Yes, Use |
| --- | --- |
| Showing message flow between systems? | Sequence |
| Modeling OOP classes and relationships? | Class |
| Documenting database tables? | ER |
| Showing valid state transitions? | State |
| Depicting a process or algorithm? | Flowchart |
| High-level system overview? | C4 Context |
| Service/container architecture? | C4 Container |
| Timeline or schedule? | Gantt |
| Git branching strategy? | Git Graph |
| Brainstorming hierarchy? | MindMap |

---

## References

For detailed patterns and examples, see:

| Reference | Content | When to Load |
| --- | --- | --- |
| [sequence-class-patterns.md](references/sequence-class-patterns.md) | API flows, auth, async, domain models, repositories | Creating sequence/class diagrams |
| [er-state-flow-patterns.md](references/er-state-flow-patterns.md) | Blog/e-commerce schemas, order lifecycle, decision trees | Creating ER/state/flow diagrams |
| [c4-patterns.md](references/c4-patterns.md) | C4 context/container, tool recommendations | Creating architecture diagrams |
| [best-practices.md](references/best-practices.md) | General guidelines, diagram tips, anti-patterns | Improving diagram quality |

---

## Delegation

For detailed syntax reference:

- **Mermaid syntax**: Invoke `visualization:mermaid-syntax` skill
- **PlantUML syntax**: Invoke `visualization:plantuml-syntax` skill

---

## Test Scenarios

### Scenario 1: Choosing a diagram type

**Query:** "What diagram should I use to show API request flow?"

**Expected:** Skill activates, recommends sequence diagram, provides tool comparison

### Scenario 2: Tool selection

**Query:** "Should I use Mermaid or PlantUML for C4 diagrams?"

**Expected:** Skill activates, recommends PlantUML for complex C4, Mermaid for simple context

### Scenario 3: Pattern lookup

**Query:** "Show me an authentication sequence diagram pattern"

**Expected:** Skill activates, directs to sequence-class-patterns.md reference

---

**Last Updated:** 2025-12-28

## Version History

- **v1.1.0** (2025-12-28): Refactored to progressive disclosure - extracted patterns to references/
- **v1.0.0** (2025-12-26): Initial release
