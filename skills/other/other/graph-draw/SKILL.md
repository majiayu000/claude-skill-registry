---
name: excalidraw-free
description: Create Excalidraw diagrams. USE WHEN user specifically asks for Excalidraw. WORKFLOWS - mind-maps, swimlane, process-flow.
---

# Excalidraw Free Skill

Create professional Excalidraw diagrams with Claude. Mind maps, swimlanes, and process flows with arrows that actually connect.

---

## What's Included

| Diagram Type | Use For | Workflow |
|--------------|---------|----------|
| **Mind Maps** | Brainstorming, book summaries, topic exploration | [workflows/mind-maps.md](workflows/mind-maps.md) |
| **Swimlanes** | Multi-role processes, who does what, handoffs | [workflows/swimlane.md](workflows/swimlane.md) |
| **Process Flows** | Step-by-step procedures, SOPs, decision flows | [workflows/process-flow.md](workflows/process-flow.md) |

---

## How It Works

1. **You describe** what you want to visualize
2. **Claude identifies** the right diagram type
3. **Claude analyzes** the content and plans the layout
4. **Claude generates** the `.excalidraw` file with proper formatting

---

## Quick Start

Tell Claude what you want to visualize:

- "Create a mind map for my content strategy"
- "Map out my client onboarding process as a swimlane"
- "Show my sales funnel as a process flow"
- "Visualize the steps in my morning routine"

Claude will ask clarifying questions if needed, then generate the diagram.

---

## Workflow Routing

**Step 1: Identify diagram type from user request**

| User Says | Diagram Type | LOAD THIS WORKFLOW |
|-----------|--------------|---------------------|
| "mind map", "brainstorm", "ideas", "branches", "book summary" | Mind Map | **READ: [workflows/mind-maps.md](workflows/mind-maps.md)** |
| "swimlane", "who does what", "roles", "handoff", "multi-person" | Swimlane | **READ: [workflows/swimlane.md](workflows/swimlane.md)** |
| "process", "steps", "flow", "procedure", "SOP", "workflow" | Process Flow | **READ: [workflows/process-flow.md](workflows/process-flow.md)** |
| Other/unclear | Ask user | Clarify before proceeding |

**Step 2: Load core references (ALWAYS)**

Before generating ANY diagram, also READ these files:
1. **[references/json-format.md](references/json-format.md)** - Required for proper JSON structure
2. **[references/colors.md](references/colors.md)** - Color palettes

**Step 3: Follow the workflow**

Each workflow file contains:
- Layout rules and positioning
- Element templates
- Color schemes
- Example outputs

---

## References (Load Before Generating)

| Reference | Purpose |
|-----------|---------|
| [references/json-format.md](references/json-format.md) | JSON structure, shapes, arrows, binding rules |
| [references/colors.md](references/colors.md) | Color palettes for professional diagrams |

**CRITICAL:** Always load `json-format.md` before generating ANY Excalidraw file. It contains the bidirectional binding rules that make arrows connect properly.

---

## Example Prompts

### Mind Maps
- "Create a mind map for the book Atomic Habits"
- "Map out my business goals for this year"
- "Visualize the topics I want to cover in my course"

### Swimlanes
- "Show my content creation workflow (me, AI, editor)"
- "Map the customer journey from lead to client"
- "Create a swimlane for our hiring process"

### Process Flows
- "Show the steps in my morning routine"
- "Create a flowchart for handling customer complaints"
- "Map my sales process from first contact to close"

---

## Output

Claude saves diagrams as `.excalidraw` files.

**Naming convention:**
- `[topic]-mindmap.excalidraw`
- `[process]-swimlane.excalidraw`
- `[process]-flow.excalidraw`

**To open:**
1. Go to [excalidraw.com](https://excalidraw.com)
2. Click menu → "Open"
3. Select the `.excalidraw` file

---

## Skill Structure

```
excalidraw-free/
├── SKILL.md (this file)
├── workflows/
│   ├── mind-maps.md      ← Radial diagrams
│   ├── swimlane.md       ← Multi-role processes
│   └── process-flow.md   ← Sequential steps
└── references/
    ├── json-format.md    ← JSON structure + binding rules
    └── colors.md         ← Color palettes
```

---

## Tips

1. **Keep it simple** - Start with 4-8 elements, add more if needed
2. **Use colors meaningfully** - Different colors for different categories
3. **Check the output** - Open in Excalidraw to verify arrows connect

---

## Want More?

This free skill covers the fundamentals. For advanced business visualization:

**Business X-Ray Workshop** includes:
- The interview process (what questions to ask)
- Advanced diagram types (bowtie, decision trees, sequences)
- Business architecture methodology
- How to identify what to visualize

*The skill makes diagrams. The workshop teaches you how to think.*

---

*Free Excalidraw skill by Rashid*
