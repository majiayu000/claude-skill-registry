---
name: things-week-ahead-digest
description: Summarize Things todos and recommend next actions using recent activity across projects, areas, and checklist-like notes, plus a week/weekend-ahead preview. Use when asked for Things planning digests, productivity check-ins, weekly previews, or automation that turns Things data into concise priorities.
---

# Things Week Ahead Digest

Build a repeatable Things planning digest with four sections:
- Snapshot
- Recently Active
- Week/Weekend Ahead
- Suggestions

## Inputs

Collect data with Things MCP tools:
1. `things_read_areas`
2. `things_read_projects` with `status="open"`
3. `things_read_todos` with `status="open"` (set `limit` high enough for a full view, usually 300-500)
4. `things_read_todos` with `status="completed"` and `completed_after=<today-7d>`
5. Optional: `things_read_todo` for top candidate tasks (`include_notes=true`) when notes/checklist signals are needed

If any call fails because of permissions, report the missing permission and continue with the best available subset.

## Workflow

1. Build urgency buckets from open todos:
- overdue: `deadline < today`
- due soon: `deadline <= today + 3 days`
- week/weekend ahead: `deadline` between today and `today + 4 days`
2. Score recent activity by project and area using:
- recent completions (last 7 days)
- open tasks
- due soon / overdue counts
- checklist-like hints from notes (`- [ ]`, `- [x]`, multiline bullet blocks)
3. Identify top active projects/areas from the score.
4. Generate 3-5 concrete suggestions:
- one next action for top projects
- one risk/triage action for overdue work
- one planning action for weekend or Monday readiness when relevant
5. Format with the template in `references/output-format.md`.

Keep tone concise and operational. Prefer verbs and specific task titles over generic advice.

## Scripts

Use `scripts/build_digest.py` when deterministic scoring/formatting is preferred (automation, repeatability, large datasets).

```bash
python3 scripts/build_digest.py \
  --areas areas.json \
  --projects projects.json \
  --open-todos open_todos.json \
  --recent-done recent_done.json
```

The script reads JSON exported from Things MCP responses and prints Markdown digest output.

## Automation Templates

Use `$things-week-ahead-digest` inside automation prompts so Codex reliably loads this workflow.

For ready-to-fill Codex App and Codex CLI (`codex exec`) templates, including Things MCP fallback guidance, placeholders, and customization knobs, use:
- `references/automation-prompts.md`

## References

- Scoring and suggestion rules: `references/suggestion-rules.md`
- Output shape and section template: `references/output-format.md`
- Automation prompt templates: `references/automation-prompts.md`
