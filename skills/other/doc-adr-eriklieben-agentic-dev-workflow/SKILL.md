---
version: 1.0.0
name: doc-adr
description: >
  Generate an Architecture Decision Record from template (MADR format). Use when the user
  says "record this decision", "write an ADR", "document why we chose", or after an RFC
  is accepted.
disable-model-invocation: false
user-invocable: true
argument-hint: "[decision title]"
---

# Generate ADR

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/adr/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/adr/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/adr.md`
3. **Determine the ADR number** by checking existing files in the output directory and incrementing
3. **Gather the decision context**:
   - What was decided?
   - What options were considered?
   - Why was this option chosen?
   - Who was involved in the decision?
4. **Generate the ADR** using MADR format:
   - **Context**: Neutral description of the situation
   - **Decision Drivers**: What factors influenced the decision
   - **Options**: At least 2-3 genuine options with pros and cons
   - **Decision Outcome**: Clear statement of what was chosen and why
   - **Consequences**: Honest positive, negative, and neutral consequences
5. **Save** to `<output>/[number]-[slug].md` (e.g., `<output>/0012-use-event-sourcing.md`)

## Quality Checklist

- [ ] Context is neutral (doesn't pre-argue for the chosen option)
- [ ] At least 3 decision drivers listed
- [ ] At least 2 real options (not strawmen)
- [ ] Each option has both pros and cons
- [ ] Decision outcome includes "because" with clear justification
- [ ] Consequences include at least one negative (every decision has trade-offs)
- [ ] Validation section says how we'll know if this was the right call

## Tips

- ADRs are immutable — if a decision changes, supersede the old ADR with a new one
- Write the context as if explaining to someone who joins the team in 6 months
- Be honest about negative consequences — the point is to document the trade-off, not sell the decision
- Link to the RFC or design doc that led to this decision
