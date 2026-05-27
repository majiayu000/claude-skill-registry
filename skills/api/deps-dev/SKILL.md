---
name: deps-dev
description: "deps.dev API v3 package metadata lookup. Covers version discovery, default/latest version, URL encoding. Keywords: deps.dev, api.deps.dev, package versions."
version: "3"
release_date: "2026-02-01"
---

# deps.dev (Skill Router)

This file is intentionally **introductory**.

Open the right note under `references/` based on what you need.

## Start here (fast)

- Need the latest/default version of a known package? Read: `references/latest-version.md`.
- Handling huge version lists or truncated responses? Read: `references/large-responses.md`.
- Not sure how to format/normalize package names per ecosystem? Read: `references/naming-and-encoding.md`.
- Need endpoint shapes and fields to parse? Read: `references/api.md`.

## Primary recipe (one request)

Goal: given `{system, packageName}`, return the default/latest version.

- Call **GetPackage**: `GET https://api.deps.dev/v3/systems/{SYSTEM}/packages/{PACKAGE}`
- Parse `versions[]` and select the item with `isDefault=true`.

If `isDefault` is missing for all versions, **stop** and ask for an explicit selection rule (e.g., include pre-releases or not) instead of guessing.

## Critical prohibitions

- Do not guess the “latest” version by string sorting.
- Do not output placeholder or “approximate” versions; always wait for API data.
- Do not parse large JSON via `grep` or manual truncation; use a JSON parser (jq/Python/Node).
- Do not silently fall back when `isDefault` is missing; ask for the desired rule.
- Do not paste large verbatim chunks from docs; summarize.
- Do not assume auth or rate limits; treat them as unspecified unless you have evidence.

## Links

- Docs: https://docs.deps.dev/api/v3/
- API base: https://api.deps.dev/v3/
