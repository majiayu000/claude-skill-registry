---
version: 1.0.0
name: doc-runbook
description: >
  Generate an operational runbook from template. Use when the user says "write a runbook",
  "create an ops guide", "incident response procedure", "how to handle [X] in production",
  or "document the on-call procedure for".
disable-model-invocation: false
user-invocable: true
argument-hint: "[operation or incident type]"
---

# Generate Runbook

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/runbooks/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/runbooks/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/runbook.md`
2. **Understand the operation/incident**:
   - What triggers this runbook? (Alert, symptom, scheduled task)
   - What services are involved?
   - What access/permissions are needed?
3. **Generate the runbook** with emphasis on:
   - **Concrete commands**: Every diagnosis and resolution step should have copy-pasteable commands
   - **Decision tree**: Clear "if X then Y" logic for diagnosis
   - **Escalation path**: When and how to escalate
   - **Verification**: How to confirm the issue is resolved
4. **Save** to `<output>/[slug].md`

## Quality Checklist

- [ ] Every diagnosis step has a concrete command or dashboard link
- [ ] Common causes are ordered by likelihood (most likely first)
- [ ] Resolution steps are copy-pasteable (not abstract instructions)
- [ ] Rollback procedure is included
- [ ] Escalation criteria are specific (time-based or condition-based)
- [ ] Verification steps confirm the fix worked
- [ ] Prerequisites list required access and tools

## Tips

- Write for someone who's been paged at 3 AM — be explicit, don't assume context
- Include actual commands, not descriptions of commands
- Order diagnosis steps by likelihood to minimize mean time to resolution
- Link to monitoring dashboards and log queries
- Update runbooks after every incident (add what was learned)
