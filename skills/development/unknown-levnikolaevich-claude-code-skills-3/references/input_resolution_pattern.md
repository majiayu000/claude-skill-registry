<!-- SOURCE-OF-TRUTH: shared/references/input_resolution_pattern.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Input Resolution Pattern

Hard contract for resolving Epic, Story, and Task identifiers when a skill is invoked without complete args.

## Core Rule

Explicit args always win. Auto-detection is only a fallback and must not silently choose from multiple candidates.

## Resolution Chain

For each entity type:

1. **Args:** use the first explicit `epicId`, `storyId`, or `taskId`.
2. **Git branch:** parse current branch name.
3. **Recent commits:** parse `git log --oneline -5`.
4. **Changed files:** match staged/unstaged paths against task docs only if branch/commit produced nothing.
5. **Kanban/provider:** list candidates using the skill's status filter.
6. **Ask user:** required when there are zero or multiple safe candidates.

## ID Patterns

| Pattern | Entity |
|---|---|
| `{TEAM_KEY}-{N}` | Linear issue |
| `US{NNN}` | file-mode Story |
| `T{NNN}` | file-mode Task |
| `epic-{N}` or `Epic-{N}` | file-mode Epic |

## Candidate Rules

- A single candidate from args or exact git ID is safe.
- A single status-filtered kanban candidate may be suggested, but the user must confirm before mutation.
- Multiple candidates must be shown as choices grouped by parent entity.
- A changed-file match is advisory unless exactly one task doc references the changed files.

## Required Evidence

Record the source of the resolved ID in the summary or checkpoint:

```json
{
  "resolved_id": "T003",
  "entity_type": "task",
  "source": "args|branch|commit|changed_files|kanban|user",
  "confidence": "exact|suggested|confirmed"
}
```

## Ask Shape

Use concise choices:
- Story: `US001: User Login` with Epic/status in description.
- Task: `T001: DB Schema` with Story/status in description.
- Epic: `Epic 1: Authentication` with status in description.

**Version:** 1.1.0
**Last Updated:** 2026-03-06
