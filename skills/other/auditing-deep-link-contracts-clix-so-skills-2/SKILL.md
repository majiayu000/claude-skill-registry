---
name: auditing-deep-link-contracts
display-name: Auditing Deep Link Contracts
short-description: Deep link contract audit
description: Audits deep link contracts and routing behavior. Use when validating
  supported routes, required parameters, and cold or warm start handling.
user-invocable: true
---

# Auditing Deep Link Contracts

Use this skill to define and audit deep link behavior so links open the correct
screen with correct parameters across cold and warm starts.

## What this skill does

- Defines a deep link contract for supported routes
- Checks required and optional parameters
- Generates cold and warm start test vectors
- Produces a concise audit report with fixes

## Workflow

```
Deep link contract audit progress:

- [ ] 1) Confirm minimum inputs (platforms, routes, entry points)
- [ ] 2) Draft a deep-link contract (JSON)
- [ ] 3) Validate the contract (script)
- [ ] 4) Generate test vectors (script)
- [ ] 5) Audit routing behavior (findings + fixes)
- [ ] 6) Verify fixes (cold and warm start)
```

## 1) Confirm the minimum inputs

Ask only what is needed:

- **Platforms**: iOS, Android, or both
- **Entry points**: push, email, web, in-app, marketing campaigns
- **Routes**: list of deep link routes that must be supported
- **Auth rules**: which routes require login
- **Fallbacks**: where to send users if data is missing

## 2) Draft a deep-link contract

Create `deep-link-contract.json` in `.mobile/` (recommended) or project root.

Recommended location: `.mobile/deep-link-contract.json`

Example:

```json
{
  "base": "myapp://",
  "routes": [
    {
      "name": "order_detail",
      "path": "/orders/{order_id}",
      "required_params": ["order_id"],
      "optional_params": ["ref"],
      "auth_required": true,
      "supported_states": ["cold", "warm"]
    }
  ]
}
```

## 3) Validate the contract

Run:

```bash
bash skills/auditing-deep-link-contracts/scripts/validate-deep-link-contract.sh \
  .mobile/deep-link-contract.json
```

## 4) Generate test vectors

Run:

```bash
bash skills/auditing-deep-link-contracts/scripts/generate-deep-link-test-vectors.sh \
  .mobile/deep-link-contract.json \
  .mobile/deep-link-test-vectors.json
```

## 5) Audit routing behavior

For each test vector, confirm:

- The app opens the expected screen
- Required parameters are present and parsed
- Missing parameters trigger the expected fallback
- Auth-required routes handle logged-out users
- Cold start and warm start behave consistently

## 6) Verify fixes

Re-run the test vectors after changes and confirm all expected behaviors.

## Progressive Disclosure

- **Level 1**: This `SKILL.md`
- **Level 2**: `references/`
- **Level 3**: `examples/` (optional)
- **Level 4**: `scripts/` (execute; do not load)

## References

- `references/deep-link-contract.md`
