<!-- SOURCE-OF-TRUTH: shared/templates/agents_md_template.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# {{PROJECT_NAME}}

{{PROJECT_DESCRIPTION}}

<!-- SCOPE: Canonical machine-facing entry point with repo map, critical rules, command overview, and links to detailed documentation ONLY. -->
<!-- DOC_KIND: index -->
<!-- DOC_ROLE: canonical -->
<!-- READ_WHEN: Start here when you need the project map, local rules, or the next canonical document. -->
<!-- SKIP_WHEN: Skip when you already know the exact target document or code area. -->
<!-- PRIMARY_SOURCES: AGENTS.md, docs/README.md -->

## Quick Navigation

| Need | Read |
|------|------|
| Documentation map | [docs/README.md](docs/README.md) |
| Standards | [docs/documentation_standards.md](docs/documentation_standards.md) |
| Principles | [docs/principles.md](docs/principles.md) |


## Agent Entry

- Purpose: Canonical repo map and routing layer for agents.
- Read when: You need the project overview, local rules, or the next canonical doc.
- Skip when: You already know the exact file or document to inspect.
- Canonical: Yes.
- Read next: `docs/README.md`, then the relevant canonical doc for the task.
- Primary sources: `AGENTS.md`, `docs/README.md`.

## Critical Rules

| Category | Rule | When to Apply |
|----------|------|---------------|
| Documentation | Read the relevant canonical doc before editing a domain | Before making non-trivial changes |
| Navigation | Respect `SCOPE` and `Agent Entry` in each document | Before reading deep content |
| Task Management | Follow the provider in `.hex-skills/environment_state.json` | For all task operations |
| Language | Keep project code and documentation in English | For all written project artifacts |
| Research | Prefer configured official documentation sources | Before stack-specific decisions |

<!-- Optional Workflow Principles shard. When ENABLE_WORKFLOW_PRINCIPLES=true, replace the next line with the full content of references/templates/agents_md_workflow_principles.md. When false, leave the line as-is and it will be stripped from the rendered output. -->
{{WORKFLOW_PRINCIPLES_BLOCK}}

## Development Commands

| Task | Windows | Bash |
|------|---------|------|
| Install dependencies | {{INSTALL_WINDOWS}} | {{INSTALL_BASH}} |
| Run tests | {{TEST_WINDOWS}} | {{TEST_BASH}} |
| Start dev server | {{DEV_WINDOWS}} | {{DEV_BASH}} |
| Build | {{BUILD_WINDOWS}} | {{BUILD_BASH}} |
| Lint or format | {{LINT_WINDOWS}} | {{LINT_BASH}} |

## Maintenance

**Update Triggers:**
- When root navigation or canonical document links change
- When core commands change
- When critical project rules change

**Verification:**
- [ ] Links resolve
- [ ] Commands match current project setup
- [ ] Canonical docs listed here still exist

**Last Updated:** {{DATE}}
