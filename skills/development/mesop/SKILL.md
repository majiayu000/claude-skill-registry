---
name: mesop
description: Build Python-native web apps with Mesop. Triggers when users want to build, debug, or deploy Mesop applications, including AI chat interfaces, internal tools, and ML demos.
---

# Mesop

Use this skill to build, debug, and deploy **Mesop** applications. Mesop is a Python-native UI framework that enables developers to build web apps without writing frontend code (HTML/CSS/JS).

## Quick Triage

- Use this skill for **pure Python** web UIs, especially for AI/ML demos and internal tools.
- **Do NOT** use this skill if the user specifically requests a different Python framework (Streamlit, Gradio, Solara) unless they are asking for a comparison or migration.
- **Do NOT** use this skill for general Flask/FastAPI backend development unless it's specifically about mounting a Mesop app.

## Workflow

1.  **Setup**: Install `mesop` and create `main.py`.
2.  **Define Page**: Use `@me.page(path="/")` to define the entry point.
3.  **Define State**: Create a `@me.stateclass` to hold session state (must be serializable).
4.  **Create Components**: Build the UI tree using `me.box`, `me.text`, `me.input`, etc.
5.  **Handle Events**: Write event handler functions (regular or generator) to update state.
6.  **Style**: Apply styles using `me.Style` (flexbox/grid) for layout and appearance.
7.  **Deploy**: Deploy to Cloud Run, Docker, or Hugging Face Spaces.

## Essential Patterns

### Standard Import
Always use the standard alias:
```python
import mesop as me
import mesop.labs as mel # For labs components like chat
```

### State Management
State is session-scoped and must be serializable.
```python
@me.stateclass
class State:
  count: int = 0
  input_value: str = "" # Immutable default
  # items: list[str] = field(default_factory=list) # Mutable default pattern
```
**Accessing State:** `state = me.state(State)` inside components or event handlers.

### Event Handlers
- **Regular**: Run to completion, then update UI.
- **Generator**: `yield` to stream UI updates (e.g., loading states, LLM streaming). **MUST** yield at the end.
- **Async**: Use `async def` and `await` for concurrent operations.

### Component Composition
Use `with` blocks for content components (parents):
```python
with me.box(style=me.Style(display="flex")):
  me.text("Child 1")
  me.button("Child 2")
```

### Key Usage
Use `key` to identify components for:
- Resetting state (change key to re-render)
- Focus management (`me.focus_component`)
- Scroll targeting (`me.scroll_into_view`)
- Reusing event handlers (access `e.key`)

## Common Pitfalls

- **Closure Variables**: Do NOT rely on closure variables in event handlers; they may be stale. Use `key` or state instead.
- **Input Race Conditions**: Avoid setting `value` on inputs unless necessary. Use `on_blur` instead of `on_input` for performance, or track "initial" vs "current" value if bidirectional binding is needed.
- **Mutable Defaults**: Never use mutable types (list, dict) as default values in `@me.stateclass`. Use `dataclasses.field(default_factory=...)`.
- **Global State**: Global variables are shared across ALL users. Use `@me.stateclass` for per-session state.

## Reference Map

- **Core Patterns**: `references/core-patterns.md` (State, Events, Streaming, Navigation)
- **Components**: `references/components-reference.md` (API reference for all components)
- **Styling & Layouts**: `references/styling-and-layouts.md` (CSS-in-Python, Flexbox, Grid, Theming)
- **Deployment**: `references/deployment-and-config.md` (Cloud Run, Docker, Config, Security)
- **Web Components**: `references/web-components.md` (Custom JS integration, Lit)
