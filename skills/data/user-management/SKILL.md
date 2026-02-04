---
name: clix-user-management
display-name: User Management
short-description: User management setup
description: Implements Clix user identification and user properties (setUserId,
  removeUserId, setUserProperty/setUserProperties,
  removeUserProperty/removeUserProperties) with safe schemas, logout best
  practices, and campaign-ready personalization/audience usage. Use when the
  user mentions login/logout, userId, user properties, personalization, audience
  targeting or when the user types `clix-user-management`.
user-invocable: true
---

# Clix User Management

Use this skill to help developers implement **Clix user identification** and
**user properties** so campaigns can use `user.*` variables and audience
filters, and so user identity is consistent across devices and sessions.

## What the official docs guarantee (high-signal)

- **Anonymous vs identified**: if no user ID is set, Clix treats the user as
  anonymous; setting a user ID converts the anonymous user into an identified
  user and links prior activity.
- **Logout**: **do not** call `setUserId(null)` on logout; handle logout in app
  logic only; when a different user logs in, call `setUserId(newUserId)` to
  switch.
- **User properties**: values are strings, numbers, or booleans; user operations
  can throw—handle errors.

## MCP-first (source of truth)

If Clix MCP tools are available, treat them as the **source of truth**:

- `clix-mcp-server:search_docs` for conceptual behavior and logout guidance
- `clix-mcp-server:search_sdk` for exact SDK signatures per platform

If MCP tools are not available, use the bundled references:

- Contract + pitfalls → `references/user-management-contract.md`
- Logout + switching rules → `references/logout-and-switching.md`
- Property schema + PII → `references/property-schema.md`
- Implementation patterns → `references/implementation-patterns.md`
- Personalization + audience mapping →
  `references/personalization-and-audience.md`
- Debugging checklist → `references/debugging.md`

## Workflow (copy + check off)

```
User management progress:
- [ ] 1) Confirm platform(s) and auth model (anonymous browsing? login? shared devices?)
- [ ] 2) Propose user plan (when setUserId/removeUserId, properties, logout policy)
- [ ] 3) Validate plan (PII, property types, logout rules)
- [ ] 4) Implement (platform-correct calls + error handling)
- [ ] 5) Verify (switching works, properties appear, campaigns can target/personalize)
```

## 1) Confirm the minimum inputs

Ask only what’s needed:

- **Platform**: iOS / Android / React Native / Flutter
- **Auth events**: where login success and logout happen in code
- **User identifier**: what stable ID to use (prefer internal user id, not
  email)
- **PII policy**: what must never be stored as user properties
- **Campaign goals**: personalization, audience filters, or both

## 2) Propose a “User Plan” (before touching code)

Return a compact table:

- **user_id source**: where it comes from (auth response, local db)
- **setUserId timing**: exact point (after login success / token saved)
- **logout behavior**: explicitly “no call to setUserId(null)”
- **properties**: key + type, required vs optional
- **purpose**: personalization / audience / analytics

## 3) Validate the plan (fast feedback loop)

Create `user-plan.json` in `.clix/` (recommended) or project root.

**For agents**: locate `scripts/validate-user-plan.sh` in the installed skill
directory and run:

```bash
# From project root:
bash <skill-dir>/scripts/validate-user-plan.sh .clix/user-plan.json
# Or if in root:
bash <skill-dir>/scripts/validate-user-plan.sh user-plan.json
```

If validation fails: fix the plan first, then implement.

## 4) Implement (platform-correct)

Use MCP to fetch the exact signatures per platform, then:

- Place `setUserId(...)` **after** login/signup is confirmed.
- On logout: **do nothing with Clix** (no `setUserId(null)`).
- When switching users: call `setUserId(newUserId)` after the new login
  succeeds.
- Set user properties only from controlled sources; avoid free-text/PII.
- Always handle errors (async calls can throw).

## 5) Verify

- Identity:
  - Anonymous flow works without calling `setUserId`
  - After login, `setUserId` is called once and stable
  - Switching accounts updates the active profile
- Properties:
  - Properties are primitives (string/number/boolean) and consistent
  - Campaign audiences can filter on them
  - Messages can use `user.*` personalization
