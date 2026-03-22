---
name: convex-realtime
description: Build reactive Convex-backed UI flows with subscriptions, optimistic updates, and pagination-aware data loading.
version: 1.0.0
metadata:
  author: agentforge
  source: waynesutton/convexskills
---

# Convex Realtime

Use this when working on real-time data flows, subscriptions, chat-like interfaces, live dashboards, or optimistic updates.

## Focus areas

- `useQuery` subscription shape and skip behavior.
- mutation-triggered reactive updates.
- optimistic updates where latency matters.
- paginated queries for large lists.

## Repo fit

- This is most relevant to dashboard and chat surfaces backed by Convex.
- Keep real-time guidance aligned with existing thread/message flows rather than inventing a separate agent runtime in Convex.
