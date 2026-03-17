---
name: service-layer-architecture
model: standard
description: Controller-service-query layered API architecture with data enrichment and parallel fetching. Use when building REST APIs or GraphQL resolvers with clean separation of concerns. Triggers on API architecture, service layer, controller pattern, data enrichment, REST API.
---

# Service Layer Architecture

Clean, performant API layers with proper separation of concerns and parallel data fetching.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install service-layer-architecture
```


---

## When to Use

- Building REST APIs with complex data aggregation
- GraphQL resolvers needing data from multiple sources
- Any API where responses combine data from multiple queries
- Systems needing testable, maintainable code

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│  Controllers   │  HTTP handling, validation        │
├─────────────────────────────────────────────────────┤
│  Services      │  Business logic, data enrichment  │
├─────────────────────────────────────────────────────┤
│  Queries       │  Database access, raw data fetch  │
└─────────────────────────────────────────────────────┘
```

---

## Layer 1: Controllers (HTTP Only)

```typescript
// controllers/Entity.ts
import { getEntity, getEntities } from "../services/Entity";

const router = new Router();

router.get("/entity/:entityId", async (ctx) => {
  const { entityId } = ctx.params;

  if (!entityId) {
    ctx.status = 400;
    ctx.body = { error: "Invalid entity ID" };
    return;
  }

  const entity = await getEntity(entityId);
  
  if (!entity) {
    ctx.status = 404;
    ctx.body = { error: "Entity not found" };
    return;
  }
  
  ctx.status = 200;
  ctx.body = entity;
});
```

---

## Layer 2: Services (Business Logic)

```typescript
// services/Entity.ts
import { queries } from "@common";

export const getEntityData = async (entity: RawEntity): Promise<EnrichedEntity> => {
  // Parallel fetch all related data
  const [metadata, score, activity, location] = await Promise.all([
    queries.getMetadata(),
    queries.getLatestScore(entity.id),
    queries.getActivity(entity.id),
    queries.getLocation(entity.slotId),
  ]);

  // Transform and combine
  return {
    ...entity,
    bonded: entity.bonded / Math.pow(10, metadata.decimals),
    total: score?.total ?? 0,
    location: location?.city,
    activity: {
      activeCount: activity?.active?.length ?? 0,
      inactiveCount: activity?.inactive?.length ?? 0,
    },
  };
};

export const getEntity = async (entityId: string): Promise<EnrichedEntity | null> => {
  const entity = await queries.getEntityById(entityId);
  if (!entity) return null;
  return getEntityData(entity);
};

export const getEntities = async (): Promise<EnrichedEntity[]> => {
  const all = await queries.allEntities();
  const enriched = await Promise.all(all.map(getEntityData));
  return enriched.sort((a, b) => b.total - a.total);
};
```

---

## Layer 3: Queries (Database Access)

```typescript
// queries/Entities.ts
import { EntityModel } from "../models";

export const allEntities = async () => {
  return EntityModel.find({}).lean();  // Always use .lean()
};

export const getEntityById = async (id: string) => {
  return EntityModel.findOne({ id }).lean();
};

export const validEntities = async () => {
  return EntityModel.find({ valid: true }).lean();
};
```

---

## Parallel Data Fetching

```typescript
// BAD: Sequential (slow)
const metadata = await queries.getMetadata();
const score = await queries.getScore(id);
const location = await queries.getLocation(id);
// Time: sum of all queries

// GOOD: Parallel (fast)
const [metadata, score, location] = await Promise.all([
  queries.getMetadata(),
  queries.getScore(id),
  queries.getLocation(id),
]);
// Time: max of all queries
```

---

## Layer Responsibilities

| Task | Layer |
|------|-------|
| Parse request params | Controller |
| Validate input | Controller |
| Set HTTP status | Controller |
| Combine multiple queries | Service |
| Transform data | Service |
| Sort/filter results | Service |
| Run database query | Query |

---

## Related Skills

- **Related:** [postgres-job-queue](../postgres-job-queue/) — Background job processing
- **Related:** [realtime/websocket-hub-patterns](../../realtime/websocket-hub-patterns/) — Real-time updates from services

---

## NEVER Do

- **NEVER put database queries in controllers** — Violates separation
- **NEVER put HTTP concerns in services** — Services must be reusable
- **NEVER fetch related data sequentially** — Use Promise.all
- **NEVER skip .lean() on read queries** — 5-10x faster
- **NEVER expose raw database errors** — Transform to user-friendly messages
