<!-- SOURCE-OF-TRUTH: shared/templates/agents_md_workflow_principles.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

<!-- Opt-in shard. Inserted into agents_md_template.md at {{WORKFLOW_PRINCIPLES_BLOCK}} when ENABLE_WORKFLOW_PRINCIPLES=true. Universal workflow rules only — anything harness-specific, project-specific, or path-scoped goes elsewhere. See references/agent_instructions_writing_guide.md for rationale. -->

## Workflow Principles

**Plan first.** For any task with 3+ steps or architectural impact, produce a written plan before implementing. If something goes sideways during execution, STOP and re-plan rather than patch forward.

**Verify before "done".** Never mark a task complete without evidence: diffs against main where relevant, passing tests, logs showing the new behavior. Ask yourself: "would a staff engineer approve this in review?"

**Demand elegance, not over-engineering.** For non-trivial changes, pause and ask "is there a more elegant approach?" If a fix feels hacky, rewrite it with what you now know. For simple fixes, skip this — don't invent complexity.

**Core principles.** Simplicity first · find root causes, no temporary patches · minimize blast radius, change only what's necessary.
