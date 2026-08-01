---
name: contract-checker
description: Validates contract JSON Schemas and fixtures, fails fast on breaking
  format issues.
---

# Contract Checker Skill

## Inputs
- JSON fixtures in `skills/contract-checker/fixtures/`.
- Command and decision JSON schemas in `contracts/schemas/`.

## Outputs
- Validation report printed to stdout.
- Non-zero exit status when fixtures do not match schemas.

## Steps
1. Load command and decision schemas.
2. Validate each fixture against the correct schema.
3. Treat `invalid_*.json` fixtures as expected failures.
4. Emit a summary and exit with status 1 if expectations are not met.

## Definition of Done (DoD)
- All fixtures validate against their expected schema outcome.
- Invalid fixtures fail validation as expected.
- Script exits cleanly with status 0 when expectations are met.
