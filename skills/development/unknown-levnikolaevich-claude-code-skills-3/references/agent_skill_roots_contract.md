<!-- SOURCE-OF-TRUTH: shared/references/agent_skill_roots_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Agent Skill Roots Contract

Shared contract for active skill discovery roots versus cache roots across supported agents.

Use this contract when a skill:
- audits agent setup health
- repairs marketplace/plugin alignment
- diagnoses duplicate skills
- writes Codex skill-root metadata into environment state

## Rules

- Discovery roots may contain only active install surfaces and system skills.
- Cache snapshots must never live under a discovery root.
- Duplicate detection is by skill directory name under the discovery root.
- A discovery violation is any cache path, stale snapshot, or foreign install location exposed inside the discovery root.

## Root Model by Agent

| Agent | Discovery Root | Active Install Surface | Cache Root | Discovery Rule |
|-------|----------------|------------------------|------------|----------------|
| Claude Code | `~/.claude/plugins/marketplaces/{marketplace}` | Active marketplace/plugin install under `marketplaces/` | `~/.claude/plugins/cache/{marketplace}/{family}/{snapshot}` | Cache is not an active install surface |
| Codex CLI | `~/.codex/skills` | `.system` plus `marketplaces/{marketplace}` under the Codex root | `~/.codex/skill-cache/{marketplace}` or another path outside `~/.codex/skills` | Cache under `~/.codex/skills/cache/**` is invalid |

## Codex-Specific Rules

- `~/.codex/skills` is the Codex discovery root. Do not map this root to `~/.claude/plugins` or any other foreign plugin tree.
- `~/.codex/skills/marketplaces/{marketplace}` is the active marketplace surface. Use one active copy per marketplace.
- `~/.codex/skills/known_marketplaces.json` must point `installLocation` to the Codex active install surface, not to `~/.claude/plugins/...`.
- `~/.codex/skills/cache/**` is a discovery violation even if the cache was created by a previous alignment run.
- If duplicate skill names remain after cache relocation and install-location repair, treat the Codex mapping as drifted and not healthy.

## Environment State Fields

Record Codex skill-root health under `agents.codex`:
- `active_skill_roots`
- `cache_roots`
- `duplicate_skill_names`
- `discovery_violation`

## Verification Checklist

- Codex discovery root contains no `cache/**`
- Active marketplace path exists under `~/.codex/skills/marketplaces/...`
- `known_marketplaces.json` points to the active Codex install path
- Duplicate skill-name scan under `~/.codex/skills` returns only active copies
