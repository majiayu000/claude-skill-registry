---
name: partner-delivery
description: Deliver repeatable MotherDuck architectures across multiple clients. Use when standardizing isolation, provisioning, regional deployment, sharing boundaries, and client-specific exceptions for a consultancy or partner delivery model.
argument-hint: [client-delivery-scenario]
license: MIT
---

# Partner Delivery

Use this skill when a consultancy, implementation partner, or multi-client product team needs a repeatable MotherDuck delivery pattern across several clients.

This is a use-case skill. It orchestrates `connect`, `explore`, `model-data`, `query`, `share-data`, and `create-dive`.

## Start Here: Is a MotherDuck Server Active?

Always determine this first.

- If a **remote MotherDuck MCP server** or **local MotherDuck server** is active, use it.
- If the delivery will run against an existing workspace, ask which client databases or workspaces are already in scope.
- Explore the live setup when available:
  - current client database boundaries
  - regional layout
  - existing service-account or share boundaries
  - reusable schemas vs client-specific schemas

Use that discovery to decide what can be standardized and what must stay client-specific.

If no server is active, ask for representative client patterns and regions before proposing the standard delivery model.

## Use This Skill When

- The user is delivering MotherDuck solutions across multiple clients.
- The user needs region-aware, repeatable architecture.
- The user needs standard provisioning with explicit client exceptions.
- The goal is a reusable delivery pattern, not a one-off single-client implementation.

## Delivery Defaults

- structural isolation over query-time tenant filtering
- one client database or stronger boundary per client
- shared architecture, client-specific schema
- explicit sharing and revocation per client

## Workflow

1. Confirm whether live MotherDuck discovery is available.
2. Classify the client patterns.
3. Inspect the existing regional and database layout if available.
4. Standardize the architecture and provisioning path.
5. Document client-specific exceptions.
6. Produce the handoff assets and validation checks.

When this skill produces a native DuckDB (`md:`) connection, watermark it with `custom_user_agent=agent-skills/1.0.0(harness-<harness>;llm-<llm>)`. If metadata is missing, fall back to `harness-unknown` and `llm-unknown`.

## Output

The output of this skill should be:

- the default multi-client pattern
- the standard provisioning checklist
- the region and isolation posture
- the client-specific exceptions

If the caller explicitly asks for structured JSON, return raw JSON only with no Markdown fences or prose before/after it.
This is mainly for automated tests, regression checks, or downstream tooling that needs a stable machine-readable shape. Normal human-facing use of the skill can stay in prose unless JSON is explicitly requested.

Use this exact top-level shape when JSON is requested:

```json
{
  "summary": {},
  "assumptions": [],
  "implementation_plan": [],
  "validation_plan": [],
  "risks": []
}
```

## References

- `references/PARTNER_DELIVERY_GUIDE.md` -- preserved detailed guidance that used to live in this skill

## Runnable Artifact

- `artifacts/client_delivery_example.py` -- MotherDuck-backed Python example showing one database namespace per client and a simple validation pass across client environments
- `artifacts/client_delivery_example.ts` -- TypeScript companion artifact with the same delivery output contract

Run it with:

```bash
uv run --with duckdb python skills/partner-delivery/artifacts/client_delivery_example.py
```

Run the same artifact against temporary MotherDuck databases:

```bash
MOTHERDUCK_ARTIFACT_USE_MOTHERDUCK=1 \
uv run --with duckdb python skills/partner-delivery/artifacts/client_delivery_example.py
```

Validate the TypeScript companion artifact:

```bash
uv run scripts/test_typescript_artifacts.py
```

## Related Skills

- `connect` -- standardize the connection path
- `explore` -- inspect existing client workspaces and boundaries
- `model-data` -- design client-specific schemas
- `query` -- validate core metrics and data contracts
- `share-data` -- publish governed share boundaries
- `create-dive` -- create repeatable client-facing answer surfaces when needed
