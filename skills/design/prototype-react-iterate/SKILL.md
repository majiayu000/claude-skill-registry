---
name: prototype-react-iterate
description: A closed-loop system for evolving UI designs using AI personas as users.
---

---
name: prototype-react-iterate
description: >
  Generate and iterate on React/Tailwind/ShadCN prototypes with Persona-driven feedback loops.
  Creates multiple variants, serves them, uses VLM to simulate user feedback based on
  Persona traits (Federated Taxonomy), and iterates on the code.
allowed-tools: [Bash, Read, Write, Connect, Browser]
triggers:
  - prototype react
  - create ui
  - design ui
  - generate interface
  - iterate design
  - persona review ui
metadata:
  short-description: Persona-driven React/ShadCN prototyping lab
  author: "Horus"
  version: "0.1.0"

provides:
  - prototype-react-iterate
composes: [, task-monitor]
---

# Prototype React Iterate

A closed-loop system for evolving UI designs using AI personas as users.

## Workflow

1.  **Create**: Scaffolds a Next.js + ShadCN app with `N` variants (A, B, C...).
2.  **Serve**: Runs the app (dev server).
3.  **Simulate**: Uses a Persona (e.g., "Embry") + VLM to "look" at the UI and provide feedback.
    -   Feedback is grounded in Persona traits (Bio/Bridge Attributes).
    -   Output: `ANNOTATIONS.jsonl` (coordinates + comments).
4.  **Iterate**: Applies feedback to the code using an LLM patcher.
5.  **Loop**: Repeats until Persona satisfaction threshold is met.

## Quick Start

```bash
cd .pi/skills/prototype-react-iterate

# 1. Create 3 variants for a prompt
./run.sh create "Cyberpunk dashboard for controlling a drone swarm" --variants 3

# 2. Run the loop (Serve -> Simulate -> Iterate)
./run.sh loop "Cyberpunk dashboard" --persona "Embry" --max-cycles 3
```

## Commands

### `create`
Scaffold new variants.
```bash
./run.sh create "PROMPT" [--variants N] [--out DIR]
```

### `simulate`
Run a VLM session where a Persona critiques the UI.
```bash
./run.sh simulate --url http://localhost:3000 --persona "Embry" --out outputs/run-01/variants/A
```

### `iterate`
Apply feedback from `ANNOTATIONS.jsonl` to the code.
```bash
./run.sh iterate --dir outputs/run-01/variants/A
```
