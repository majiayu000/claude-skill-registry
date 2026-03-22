---
name: wolverine__guide
description: "Wolverine guide covering all HTTP write operations: CREATE (POST / start event stream), UPDATE (PUT or PATCH / append event), and DELETE (soft-delete / tombstone event). Use for any Wolverine command handler or HTTP endpoint task."
---

Use this skill for all Wolverine write-side operations in the ApiService — commands, events, and HTTP endpoint handlers.

## Task Routing

Read only the sub-file for your task:

| Task | Read |
|------|------|
| Add a `POST` endpoint to create a new resource (starts a new event stream) | [`operations.md`](operations.md) — Create section |
| Add a `PUT` or `PATCH` endpoint to modify an existing resource (appends event) | [`operations.md`](operations.md) — Update section |
| Add a `DELETE` endpoint to remove or archive a resource (soft delete) | [`operations.md`](operations.md) — Delete section |
| Understand or review Wolverine durability/configuration settings | [`configuration.md`](configuration.md) |

## Related Skills

- [`/marten__guide`](../marten__guide/SKILL.md) — Aggregates, projections, and query endpoints

