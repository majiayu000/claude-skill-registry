---
name: swarm
description: >-
  Dispatch a swarm using any orchestration pattern. Routes to the
  appropriate pattern-specific skill based on the selected preset.
---

# Swarm Dispatcher

## Overview

Route swarm requests to the appropriate pattern skill. Read the
preset config, determine the pattern, and follow the corresponding
skill.

## Goal Slug Generation

When pattern skills create team names, they use the format
`swarm-{pattern}-{goal-slug}-{timestamp}`. Generate the goal slug
from the user's goal description

- Lowercase only
- Replace spaces and special characters with hyphens
- Remove all characters except `a-z`, `0-9`, and `-`
- Collapse consecutive hyphens into one
- Truncate to 30 characters maximum
- Strip leading and trailing hyphens
- **Abort if empty**: if the slug is empty after all transformations
  (e.g., goal was all special characters), abort with: "Could not
  generate a valid team name from the provided goal."

Examples

- "PR review" → `pr-review`
- "Security audit of auth module" → `security-audit-of-auth-module`
- "Fix the OAuth2/OIDC integration!!!" → `fix-the-oauth2-oidc-integrat`

Pass the goal slug through to the pattern skill along with the
goal, target, and preset.

## Stale Worktree Cleanup

Before starting any swarm, check for leftover worktrees from
previous sessions

```bash
git worktree list
```

If worktrees exist that are not associated with the current session
(stale branches from crashed or abandoned swarms), offer the user
two options

1. **Remove stale worktrees**: `git worktree remove <path>` for each stale
   entry. This reclaims disk space but the branches persist and can still be
   merged
2. **Keep them**: the user may want to inspect or recover work

Only worktrees whose branch names match the `swarm-*` naming
convention should be flagged. Non-swarm worktrees are outside
this plugin's scope.

## Steps

1. **Identify goal and target** from the user's request. If unclear,
   ask

2. **Read roles config** from
   `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml`

3. **Select preset or roles** using the same priority as v1. When resolving
   roles, check for inline definitions in the preset first (entries with a
   `name` and `prompt` field), then fall back to global role names in the
   `roles:` section

   - User specifies a preset name -> use it
   - User specifies individual role names -> use those (fan-out)
   - User describes what they want -> match to preset/roles
   - Default for "review" -> `pr-review` preset

4. **Validate config** — check the resolved preset and roles for
   structural problems before routing to a pattern skill. Abort or
   warn as indicated

   ### Required role fields

   Every role referenced by the preset (whether global or inline)
   must have

   - `prompt` — non-empty. An inline role missing `prompt` means the
     agent would be spawned with no instructions. **Abort**
   - `subagent_type` — must be one of `Explore` or `general-purpose`.
     Missing or unrecognized values (typos like `Explorer`) cause
     opaque spawn failures. **Abort**

   ### Isolation consistency

   If a role specifies `isolation: worktree` but its `subagent_type`
   is not `general-purpose`, **warn** that `subagent_type` will be
   overridden to `general-purpose` at spawn time (worktree isolation
   requires write access). This is not an error — pattern skills
   handle the override — but the role definition is internally
   inconsistent and should be fixed.

   ### Numeric fields

   `worker_count` (swarm) and `approach_count` (speculative) must be
   positive integers when present. Non-numeric values, zero, or
   negative values are invalid. **Abort**

   ### Topology-pattern agreement

   The preset's declared `pattern` must match the topology keys
   present in the preset config:

   | Pattern       | Expected keys                 | Unexpected keys               |
   |---------------|-------------------------------|-------------------------------|
   | `fan-out`     | `roles`                       | `stages`, `nodes`             |
   | `pipeline`    | `stages` or `nodes`           | bare `roles`                  |
   | `task-graph`  | `nodes`                       | `stages` without `depends_on` |
   | `map-reduce`  | `map_role`, `reduce_role`     | `roles`, `stages`             |
   | `speculative` | `approach_role`, `judge_role` | `roles`, `stages`             |
   | `swarm`       | `worker_role`                 | `roles`, `stages`             |

   If unexpected keys are present, **warn** that the declared pattern
   may not match the intended topology. Ask the user to confirm.

   ### Watchdog prerequisite

   If the preset has `watchdog: true`, verify that the `monitor` role
   exists in the global `roles:` section. If missing, **abort** —
   the watchdog cannot be spawned without a role definition.

   ### Deprecated preset completeness

   If the preset has `deprecated: true` but no `successor` field,
   **warn** that no replacement can be suggested. The user can still
   proceed.

   ### Reserved names

   If any role name in the preset matches `monitor` or `judge`,
   **warn** that these names have special behavior in hooks
   (exemption from quality gates, speculative gate branching). Using
   them as regular specialist names will cause incorrect gate logic.

5. **Determine pattern** from the selected preset's `pattern` field.
   If absent, default to `fan-out`. If the preset has
   `deprecated: true`, warn the user and suggest the `successor`
   preset instead. Proceed only if the user confirms

6. **Route to pattern skill** — read and follow the corresponding
   skill

   | Pattern               | Skill               |
   |-----------------------|---------------------|
   | `fan-out` (or absent) | `swarm-fan-out`     |
   | `swarm`               | `swarm-swarm`       |
   | `pipeline`            | `swarm-pipeline`    |
   | `task-graph`          | `swarm-pipeline`    |
   | `map-reduce`          | `swarm-map-reduce`  |
   | `speculative`         | `swarm-speculative` |

   Read the skill file and follow its checklist from step 1.
   Pass through: goal, target, selected roles/preset, and any
   user context.

7. **Watchdog modifier** — if the preset has `watchdog: true`, the lead
   must spawn a monitor agent immediately after creating the team (the
   pattern skill's "Create Team" step). Spawn it BEFORE spawning any
   specialist/worker agents.

   Use the `monitor` role from
   `$CLAUDE_PLUGIN_ROOT/config/swarm-roles.yaml`.

   Read `monitor_cron_interval_seconds` from
   `$CLAUDE_PLUGIN_ROOT/.claude-plugin/settings.json` (default: 60).
   Include the resolved interval in the monitor's spawn prompt.

   - `name`: `monitor`
   - `subagent_type`: from the monitor role config (typically `Explore`)
   - `run_in_background`: `true`
   - `prompt`:
     - Identity: "Your name is monitor. You are part of team {team_name}."
     - Immediately send a "Monitoring started" message to the team lead
       via SendMessage (this satisfies the idle hook gate)
     - Call CronCreate with:
       - `intervalSeconds`: {monitor_cron_interval_seconds} (read from
         `$CLAUDE_PLUGIN_ROOT/.claude-plugin/settings.json`, default 60)
       - `prompt`: "Check TaskList for anomalies: tasks stuck in_progress,
         idle workers without findings, failed or blocked tasks. Send a
         SendMessage alert to the team lead for each anomaly found. Do not
         intervene directly — report only."
     - Do not intervene directly — report to the lead

   The monitor does not get its own task — it observes and reports.
   Include the monitor in shutdown (send `shutdown_request` to it).

   Pattern skills do NOT spawn the monitor. This section is the single
   source of truth for monitor spawning.
