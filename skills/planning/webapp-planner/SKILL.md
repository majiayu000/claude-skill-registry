---
name: webapp-planner
description: Desktop web app planning skill for vague customer requirements. Use when (1) customers describe requirements vaguely ("I want something like..."), (2) planning HTML + Tailwind + vanilla JS web apps, (3) creating ASCII wireframes from descriptions, (4) generating technical specifications without backend, (5) creating project roadmaps with prioritization. Triggers include phrases like "make me an app", "build a web app", "I need a tool for...", or any unclear feature requests that need clarification.
---

# Web App Planner

A comprehensive planning system that transforms vague customer requirements into detailed specifications for desktop web apps using **HTML + Tailwind CSS + vanilla JavaScript** with **no backend** (LocalStorage + IndexedDB only).

## Quick Start

This skill orchestrates 7 specialized agents to create complete project specifications:

1. **interviewer** - Extract requirements through persistent questioning
2. **ui-sketcher** - Generate ASCII wireframes
3. **documentation-writer** - Create specs with UX philosophy
4. **tech-researcher** - Research localbase patterns and repository architecture
5. **mermaid-designer** - Create flowcharts using ai-diagrams-toolkit patterns
6. **interactive-designer** - Design Tailwind animations and micro-interactions
7. **planner** - Structure phases, priorities, and development roadmap

## Workflow

```
Customer Request (vague)
         ↓
   [Interviewer] ← Persistent questioning until requirements clear
         ↓
   [UI Sketcher] → ASCII wireframes with Tailwind hints
         ↓
   [Documentation Writer] → Markdown spec with UX philosophy (Norman/Nielsen)
         ↓
   [Tech Researcher] → localbase patterns, repository architecture
         ↓
   [Mermaid Designer] → Flowcharts (ai-diagrams-toolkit style)
         ↓
   [Interactive Designer] → Tailwind animations, micro-interactions
         ↓
   [Planner] → MoSCoW/RICE priorities, WBS, phases
         ↓
   Final Output: Complete Markdown specification
```

## Agent Delegation

### When to Use Each Agent

| Agent | Trigger | Output |
|-------|---------|--------|
| `interviewer` | Vague requirements, unclear scope | Clarified requirements document |
| `ui-sketcher` | "Show me the layout", feature description | ASCII wireframe with annotations |
| `documentation-writer` | After wireframe complete | Markdown spec with UX rationale |
| `tech-researcher` | Data storage questions, API patterns | localbase guide, repository patterns |
| `mermaid-designer` | "Show me the flow", process description | Mermaid diagrams |
| `interactive-designer` | "Make it interactive", animation needs | Tailwind animation code |
| `planner` | "What should we build first?", prioritization | Roadmap with phases |

### Delegation Pattern

```
1. TASK: [Specific atomic goal]
2. EXPECTED OUTCOME: [Concrete deliverables]
3. REQUIRED SKILLS: [Agent name]
4. REQUIRED TOOLS: [Tool whitelist]
5. MUST DO: [Exhaustive requirements]
6. MUST NOT DO: [Forbidden actions]
7. CONTEXT: [File paths, patterns, constraints]
```

## References

Load based on current task:

| Task | Reference |
|------|-----------|
| Overall process | `references/workflow.md` |
| Customer interviews | `references/interview-patterns.md` |
| ASCII wireframes | `references/ascii-art-guide.md` |
| Data persistence | `references/localbase-guide.md` |
| UX documentation | `references/ux-philosophy.md` |
| Flowcharts | `references/mermaid-patterns.md` |
| Animations | `references/tailwind-animations.md` |
| Prioritization | `references/planning-methods.md` |

## Tech Stack Constraints

This skill targets **desktop web apps** with:

- **Frontend**: HTML + Tailwind CSS + vanilla JavaScript
- **Storage**: LocalStorage (settings) + IndexedDB via localbase (data)
- **No Backend**: All logic runs client-side
- **No File System API**: Browser storage only

## Output Format

Final deliverable is a **Markdown file** containing:

1. Project overview and goals
2. User personas and scenarios
3. Feature list with MoSCoW priorities
4. ASCII wireframes with UX annotations
5. Data model (localbase collections)
6. User flow diagrams (Mermaid)
7. Animation specifications
8. Development phases and milestones

See `assets/planning-template.md` for the complete template.
