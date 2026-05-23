---
name: faion-dev-frontend
description: "UI design: brainstorming, prototyping, Storybook. Triggers: ui design, component library."
user-invocable: false
allowed-tools: Read, Write, Edit, Glob, Bash, Task, AskUserQuestion, Skill
---

# UI Design Skill

**Communication: User's language. Code: English.**

## Agents

| Agent | Purpose |
|-------|---------|
| faion-frontend-brainstormer-agent | Generate 3-5 design variants |
| faion-storybook-agent | Setup/maintain Storybook |
| faion-frontend-component-agent | Develop components with stories |

## Workflow

```
Requirements → Brainstorm (3-5 variants) → User selects → Refine → Storybook → Components
```

## Phase 1: Requirements

```python
AskUserQuestion([
    {"question": "Type?", "options": ["Landing", "Dashboard", "Form", "Components"]},
    {"question": "Style?", "options": ["Minimalist", "Bold", "Corporate", "Playful"]},
    {"question": "Tech?", "options": ["HTML/CSS", "React+TS", "Vue", "Next.js"]}
])
```

## Phase 2: Brainstorming

```python
Task(
    subagent_type="faion-frontend-brainstormer-agent",
    prompt=f"""Create 3-5 DISTINCT design variants for: {requirements}
Tech: {tech}, Style: {style}
Each variant: unique aesthetic, working code, rationale"""
)
```

Output: `designs/variant-{N}-{name}/`

## Phase 3: Selection & Refinement

User picks variant → Skill("frontend-design") to refine → iterate until approved

## Phase 4: Storybook

```python
Task(
    subagent_type="faion-storybook-agent",
    prompt=f"Setup Storybook for {project}. Design: {approved_design}"
)
```

## Phase 5: Components

```python
Task(
    subagent_type="faion-frontend-component-agent",
    prompt=f"Develop {component_name} with story file"
)
```

Structure:
```
src/components/{Name}/
├── {Name}.tsx
├── {Name}.stories.tsx
├── {Name}.module.css
└── index.ts
```

## Design Tokens

```typescript
// tokens/
colors = { primary: {...}, semantic: {success, error, warning} }
typography = { fontFamily, fontSize, fontWeight }
spacing = { 0, 1, 2, 4, 8, 16 }
```

## Storybook Commands

- `npm run storybook` — dev server
- `npm run build-storybook` — static build
