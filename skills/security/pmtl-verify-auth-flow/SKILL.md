---
name: pmtl-verify-auth-flow
description: PMTL_VN auth verification skill. Use when touching register, login, logout, forgot-password, reset-password, profile, session cookies, proxy auth guards, or OAuth callbacks so auth behavior is verified instead of assumed.
---

# PMTL Verify Auth Flow

## Purpose

Verify PMTL auth behavior through the current `apps/web + apps/api + apps/admin` architecture so session, cookie, and protected-route changes are tested instead of assumed.

## Use When

- Touching register, login, logout, forgot-password, reset-password, verify-email, profile, or session behavior.
- Changing proxy/request-boundary logic that can affect browser auth.
- Reviewing auth regressions across member/admin protected surfaces.

## Required Inputs

- touched auth surface or route
- whether the change affects browser cookies, proxy behavior, or role guards
- any current helper/runtime constraints that limit runnable verification

## Expected Output

- Evidence that the changed auth path still works or a clearly scoped failure report.
- No success claim based only on reading code when a runnable auth check exists.

## Execution Approach

1. Start from the changed auth surface: browser flow, protected route, cookie path, or admin/member split.
2. Run the auth helper lane first when it can exercise the path quickly.
3. Read current design owners for auth/session rules before trusting helper output.
4. Supplement helper output with targeted manual checks when the helper does not cover the changed path deeply enough.

## What to verify

- API/web health before auth checks.
- Register or verify-email flow when touched.
- Login and session token issuance.
- Logout and logout-all semantics when touched.
- `GET /api/auth/me`.
- Forgot/reset password flow when touched.
- Profile or protected-route behavior when the change touches those paths.
- Member/admin boundary when role or guard logic changed.
- Cookie or proxy behavior when the bug is session-related.

## Script

Primary entrypoint: `py infra/tools/codex_actions.py auth-flow`

Compatibility wrapper: `scripts/run_auth_flow_check.py`

```bash
py infra/tools/codex_actions.py auth-flow
```

## Verification

- Treat the helper as a fast lane, not a proof that every auth branch is covered.
- Confirm at least one protected read path and one auth mutation path when auth behavior changed materially.
- If cookies, refresh, or proxy behavior changed, verify browser-auth assumptions against PMTL security and request-boundary docs.
- If helper output is legacy-biased or incomplete for the touched path, say so and add targeted checks.

## Quality Criteria

- Verification covers the actual touched auth behavior, not just a generic smoke pass.
- Findings distinguish auth logic failure from proxy/cookie transport failure.
- Admin/member guard differences are not collapsed into one “protected route” claim.

## Edge Cases

- Current helper is a convenience wrapper around the repo smoke lane; it is useful but not a complete auth matrix.
- Refresh/session rotation, CSRF, and proxy/cookie regressions may need targeted checks beyond the helper output.
- Legacy references to old CMS-era paths are not authoritative for the current architecture.

## Read when needed

- `design/baseline/security.md`
- `design/01-identity/contracts.md`
- `design/01-identity/use-cases/manage-auth-session.md`
- `design/tracking/api-route-inventory.md`
- `apps/web/src/proxy.ts`

## Pair with

- `pmtl-production-baseline` for runtime/security boundary changes.
- `pmtl-verify-quality-gate` after meaningful code changes.
