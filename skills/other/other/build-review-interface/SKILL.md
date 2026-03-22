---
name: build-review-interface
description: Build a custom web interface for trace annotation and review. Use when users need a bespoke review surface for their workflow.
---

# Build Review Interface

Use this skill to design and implement a stack-agnostic custom trace review web UI.

## Interactive Q&A protocol (mandatory)

<HARD-GATE>
BEFORE the first scoping question, search for a structured question tool (e.g., `AskUserQuestion` or similar interactive widget) and load it. Use that tool for EVERY scoping question. Fall back to plain-text lettered options ONLY if no such tool exists in the environment.
</HARD-GATE>

Start with custom web UI scoping questions.

Rules:
- Ask one question at a time.
- Use the structured question tool for every question. Structure each with a short header, 2-4 options with labels and descriptions, and place the recommended option first. Do not add "(Recommended)" or similar annotations to option labels.
- Ask one follow-up when requirements are ambiguous.

Example question:

```
What should the primary annotation action set be in v1?
A) Pass / Fail only
B) Pass / Fail + free-text notes
C) Pass / Fail + notes + Defer
D) Custom label set
```

## Custom UI workflow

1. Define annotation contract:
   - pass/fail controls
   - free-text notes
   - defer action
   - autosave behavior
2. Define data source and persistence:
   - JSON/CSV input or API-backed source
   - CSV/JSON/SQLite output for labels
3. Build trace review views:
   - render markdown as markdown
   - syntax highlight code
   - pretty-print JSON
   - collapse low-value verbose sections
4. Add navigation and productivity controls:
   - next/previous
   - position and progress counters
   - keyboard shortcuts
5. Validate end to end:
   - functional checks
   - data persistence checks
   - Playwright verification for core annotation loop

## Design checklist

- Consistent layout and terminology across traces
- Pass/fail actions visually distinct
- Full trace visible or expandable
- Autosave on primary actions
- Keyboard shortcuts for frequent actions
- Trace-level annotation as default

## Guardrails

- Keep technology guidance stack-agnostic unless the user asks for a specific stack.
   - Review the existing codebase to determine if any existing stack is available and offer that as an option.
- Keep sampling logic separate from UI implementation.
