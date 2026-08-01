---
name: fixtures-generator
description: Generates valid and invalid JSON fixtures for CommandDTO and DecisionDTO
  based on current contract schemas.
---

# Fixtures Generator Skill

## Inputs
- Optional output directory (defaults to `skills/fixtures-generator/fixtures/`).
- Core graph sample command generator.

## Outputs
- Generated fixture JSON files.
- Updated documentation snippet in README between markers.

## Steps
1. Generate sample command and decision payloads.
2. Write fixtures to the output directory.
3. Update README content between documentation markers.
4. Report the generated fixture locations.

## Definition of Done (DoD)
- Fixtures are written to disk in the expected location.
- README markers are updated with the latest fixture summary.
- Script exits with status 0 when generation completes.
