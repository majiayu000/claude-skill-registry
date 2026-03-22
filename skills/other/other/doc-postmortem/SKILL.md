---
version: 1.0.0
name: doc-postmortem
description: >
  Generate a blameless post-mortem from template. Use when the user says "write a post-mortem",
  "incident report", "what went wrong", "document the outage", or after a production incident.
disable-model-invocation: false
user-invocable: true
argument-hint: "[incident title or date]"
---

# Generate Post-Mortem

## Path Resolution

1. Read `workflow.json` in the project root
2. If it exists and `docsRepo` is `"."`: this IS the docs repo — use local paths
3. If it exists and `docsRepo` is a repo name: resolve via `pwsh .claude/skills/tool-worktree/scripts/resolve-repo.ps1 <docsRepo>` to get the docs root path. Templates at `<resolved>/templates/`, output to `<resolved>/postmortems/`
4. If no `workflow.json`: templates at `templates/`, output to `docs/postmortems/`

## Instructions

1. **Resolve paths** (see Path Resolution above)
2. **Read the template** at `<templates>/postmortem.md`
2. **Gather incident details**:
   - What happened? When?
   - What was the impact? (users, revenue, SLA)
   - What was the timeline? (detection → response → resolution)
   - What was the root cause?
3. **Generate the post-mortem** following blameless principles:
   - **Focus on systems, not people** — "the deploy pipeline didn't catch X" not "Bob forgot to check X"
   - **Be specific about impact** — numbers, not adjectives
   - **Timeline must be precise** — include timestamps
   - **Action items must be actionable** — assigned owner, due date, clear definition of done
4. **Save** to `<output>/[date]-[slug].md`

## Blameless Principles

- Use passive voice or system-focused language for failures
- "What went well" section is mandatory — acknowledge good response
- "Where we got lucky" exposes hidden risks
- Action items should prevent recurrence, improve detection, AND improve response

## Quality Checklist

- [ ] Summary is 2-3 sentences (scannable)
- [ ] Impact has concrete numbers
- [ ] Timeline has timestamps (not "then... later...")
- [ ] Root cause is technical and specific
- [ ] Contributing factors are listed (root cause is never the only factor)
- [ ] Detection section identifies the gap
- [ ] Action items have owners and due dates
- [ ] At least one action each for: prevent, detect, respond
- [ ] "Where we got lucky" section is filled in
- [ ] Tone is blameless throughout

## Tips

- Write the timeline first — it structures everything else
- The "where we got lucky" section is often the most valuable
- Every post-mortem should update at least one runbook
- Link to monitoring dashboards and log queries for evidence
