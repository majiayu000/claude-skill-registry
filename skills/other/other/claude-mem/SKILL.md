---
name: claude-mem
description: Orchestrator-driven planning and execution workflow. Use when coordinating Claude memory-backed planning, make-plan/do flows, or preserving execution context across multi-step work.
---

# Claude Mem

Use this skill when a task needs the local `claude-mem` planning and execution prompts packaged under this directory.

## Resources

- `make-plan.md` — planning prompt for turning a request into an executable work plan.
- `do.md` — execution prompt for carrying out the current plan while preserving context.

Read the relevant resource only when the user explicitly asks for a `claude-mem` flow or when a task already depends on these prompt files.
