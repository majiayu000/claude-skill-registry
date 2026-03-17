---
name: mechanics-check
description: Audit SENTINEL game data integrity. Validates regions, jobs, vehicles, and favors against schema enums.
allowed-tools: Bash, Read, Glob, Grep
user-invocable: true
proactive: false
---

# Mechanics Integrity Check

Validate SENTINEL game data consistency to catch bugs before they surface during play.

## When to Use

- After modifying `regions.json`, job templates, or favor costs
- Before committing game data changes
- When adding new factions, regions, or mission types
- After updating schema enums
- Periodic health checks on game data

## How to Run

### Quick Check (Recommended)

Run the validation script directly:

```bash
python C:/dev/SENTINEL/sentinel-agent/scripts/check_mechanics.py
```

### JSON Output (for CI/automation)

```bash
python C:/dev/SENTINEL/sentinel-agent/scripts/check_mechanics.py --json
```

### Present Results

Format the output as an actionable checklist:

```markdown
## Mechanics Health Report

### Status: [HEALTHY | NEEDS ATTENTION | BROKEN]

### Issues Found
- [ ] Issue 1 (ERROR) — must fix
- [ ] Issue 2 (WARNING) — should investigate
- [ ] Issue 3 (INFO) — informational

### Recommendations
- ...
```

## What It Checks

### Regions (`data/regions.json`)
- All 11 Region enum values have entries
- `primary_faction` and `contested_by` reference valid faction IDs
- `adjacent` lists contain valid region IDs
- Adjacency is bidirectional (if A→B then B→A)

### Jobs (`data/jobs/*.json`)
- `faction` matches FactionName enum (display names)
- `type` matches MissionType enum
- `region` (if present) matches Region enum
- `opposing_factions` contain valid faction names
- `requires_vehicle_tags` exist in at least one vehicle
- `requires_vehicle_type` matches actual vehicle types

### Vehicles (`tui_commands.py` VEHICLE_DATA)
- All job-required tags exist in at least one vehicle
- Reports orphan tags (defined but not used by any job) as INFO

### Favors (`systems/favors.py`)
- All FavorType values have costs defined
- All Disposition levels have favor mappings and cost modifiers

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| ERROR | Breaks game functionality | Must fix |
| WARNING | Inconsistency that may work | Should investigate |
| INFO | Suggestion or design note | Optional |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed (HEALTHY) |
| 1 | Warnings only (NEEDS ATTENTION) |
| 2 | Errors found (BROKEN) |

## Tips

- Run after any `schema.py` changes that add/remove enum values
- The check is read-only — it never modifies files
- JSON output can be filtered with jq:
  ```bash
  python check_mechanics.py --json | jq '.issues[] | select(.severity == "error")'
  ```
- Orphan vehicle tags (INFO) are not bugs — they're future-proofing for jobs not yet written

## Data Sources

| Data | Location |
|------|----------|
| Schema enums | `src/state/schema.py` |
| Regions | `data/regions.json` |
| Jobs | `data/jobs/*.json` |
| Vehicles | `src/interface/tui_commands.py` |
| Favors | `src/systems/favors.py` |
