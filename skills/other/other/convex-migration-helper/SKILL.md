---
name: convex-migration-helper
description: Plan and implement safe Convex schema and data migrations, especially when changing existing fields, relationships, or required data.
version: 1.0.0
metadata:
  author: agentforge
  source: get-convex/convex-agent-plugins@f104efb49a787a1ef4a6c84df496d58800ce334a
---

# Convex Migration Helper

Use this when a schema change affects existing rows or when data shape must be transformed.

## Migration defaults

- Prefer additive changes first.
- Add required fields as optional, backfill, then tighten.
- Use internal functions for migration work.
- Keep the app running during the migration whenever possible.

## When this skill is needed

- Required fields are being introduced.
- Field types are changing.
- Nested data is being split into relational tables.
- Existing indexes or lookup paths are changing in ways that require backfills.

## What to check

- Is a dual-read or dual-write period needed?
- Can the migration run in batches?
- Does the schema need a temporary compatibility state?
- Are there existing functions that assume the old shape?
