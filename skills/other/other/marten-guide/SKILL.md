---
name: marten__guide
description: "Marten guide covering event-sourced aggregates, projections (single-stream, multi-stream, composite, event), and query endpoints (get-by-id, paged list). Use for any Marten modeling or read-side query task."
---

Use this skill for all Marten tasks in the ApiService — aggregates, projections, and query endpoints.

## Task Routing

Read only the sub-file for your task:

| Task | Read |
|------|------|
| Create a new event-sourced aggregate | [`aggregate.md`](aggregate.md) |
| Build a read model from a single aggregate stream | [`projections.md`](projections.md) — Single-stream section |
| Build a read model aggregating multiple streams (dashboards, rollups) | [`projections.md`](projections.md) — Multi-stream section |
| Chain or stage multiple projections for throughput | [`projections.md`](projections.md) — Composite section |
| Emit one document per event (audit log, history, side table) | [`projections.md`](projections.md) — Event projection section |
| Add `GET /resource/{id}` with caching | [`queries.md`](queries.md) — Get-by-ID section |
| Add paged `GET /resource` list with filtering and caching | [`queries.md`](queries.md) — List query section |
| Understand or review Marten/Wolverine greenfield configuration settings | [`configuration.md`](configuration.md) |

## Related Skills

- [`/wolverine__guide`](../wolverine__guide/SKILL.md) — Write-side operations (POST/PUT/DELETE endpoints)

