---
name: compound-autolearn-compoundspec
description: Generate a CompoundSpec v2 JSON-only autolearn proposal from git diffstat + existing skills, while respecting strict file-scope constraints.
license: MIT
compatibility: opencode,claude
metadata:
  created_at: "2026-01-30T16:42:50.393Z"
  updated_at: "2026-01-30T16:42:50.393Z"
  version: "1"
---
<!-- BEGIN:compound:skill-managed -->
# Purpose
Turn an autolearn prompt (recent activity + constraints) into a valid CompoundSpec v2 JSON object.

# When To Use
- Prompt says "Background Autolearn" or "learning agent".
- Prompt requires JSON-only output and limits edits to memory/docs artifacts.

# Procedure
- Read the constraints and allowed paths; assume anything else is forbidden.
- If a system reminder indicates read-only / Plan Mode:
  - Do not propose product code changes.
  - Keep proposals strictly within skills/instincts/docs/changelog.
  - Do not propose actions that imply file modifications outside the allowed set.
- Use the git summary (changed_files + diffstat) as evidence for what to learn.
- If the git summary indicates an in-progress merge/conflict state (e.g., diffstat lines labeled "Unmerged <path>"):
  - Treat the diff as incomplete/low-signal.
  - Avoid inferring product behavior changes.
  - Prefer a small instinct/skill update about conflict-state hygiene.
  - If there is no other stable evidence, emit empty skill/instinct changes and set `docs.sync: false`.
- If the diffstat is empty (or there are no meaningful file changes):
  - Do not invent learnings.
  - Emit empty `instincts.create/update` and `skills.create/update`.
  - Set `docs.sync: false`.
  - Use a changelog note that explains the skip (e.g., "Autolearn ran with no diff evidence; skipped memory updates.")

## Evidence hygiene (low-signal diffs)

Treat generated/derived artifacts as low-signal evidence:
- If `services/index.json` changes without corresponding `services/*.md` edits, assume it was refreshed and do not infer new dependency learnings.
- If `.opencode/memory/instincts.json` / `.opencode/memory/INSTINCTS.md` show large rewrites or deletions, assume cleanup and avoid inventing new heuristics from it.
- If changes appear duplicated under both `.claude/skills/` and `.opencode/skills/`, assume a mirror/sync artifact:
  - Do not infer new behavior from the duplication.
  - In CompoundSpec proposals, only target `.opencode/skills/**` (never propose changes to `.claude/skills/**`).
- If the diff is primarily additions/deletions under `src/*.egg-info/`, assume packaging metadata cleanup/regeneration noise and avoid learning anything beyond "egg-info is generated" unless the prompt explicitly states an intentional packaging change.
- If the diffstat shows changes only under `examples/` with no corresponding `src/` or `tests/` changes, treat it as low-signal for durable learnings; emit empty `skills`/`instincts`, set `docs.sync: false`, and use a changelog note explaining the skip.

## Ticket/process-heavy diffs

- If the diff is primarily ticket/process artifacts (e.g. `.tickets/*.md`, `LOOM_ROADMAP.md`, `LOOM_CHANGELOG.md`, `AGENTS.md`) with no corresponding product code changes:
  - Prefer `instincts.update[]` that strengthen workflow heuristics (triage, scoping, read-only constraints).
  - Avoid creating new skills unless a repeated procedural gap is clearly demonstrated.
  - Avoid proposing docs block updates unless a stable always-on principle changed.
  - Do not infer or describe product behavior changes.

## Prefer updates over creation

Prefer:
- `instincts.update[]` to strengthen an existing heuristic
- `skills.update[]` to refine an existing skill
- `skills.create[]` only if there is no close match

## Skill updates

- If updating a skill:
  - Re-emit the entire final managed body (no diffs/snippets).
  - Keep it checklist-like.

## Instinct quality bar

- Keep instincts crisp:
  - Trigger is a concrete situation.
  - Action is a concrete behavior.
  - Confidence is 0.6-0.85 unless repeated evidence.

## Keep proposals small

- Max 3 skills per run.
- Max 8 instinct updates per run.

## Output hygiene

- Output exactly one JSON object.
- Do not wrap in code fences.
- Do not include commentary.
- Use repo-root-relative paths in any markdown content.

# Suggested Minimal Template
- `auto.reason` from prompt (often `session.idle`).
- `auto.sessionID` from prompt.
- `docs.sync: true` if you touched skills/instincts/docs; otherwise `docs.sync: false`.
- `changelog.note` as a single sentence describing the memory delta.
<!-- END:compound:skill-managed -->

## Manual notes

_This section is preserved when the skill is updated. Put human notes, caveats, and exceptions here._
