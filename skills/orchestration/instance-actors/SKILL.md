---
name: instance-actors
description: Managing instance actor orchestrations for PostgreSQL health monitoring. Use when debugging stale actors, restarting actors, or troubleshooting health check issues.
---

# Instance Actor Management

## Overview
Instance actors are detached Duroxide orchestrations that run continuously to monitor PostgreSQL instance health. They can become orphaned or stale.

## Actor Lifecycle

1. **Created**: When instance is created, `create_instance` orchestration spawns an actor
2. **Running**: Actor loops forever: check health → update CMS → timer → continue-as-new
3. **Cancelled**: When instance is deleted, actor is cancelled via `cancel_instance()`

## Detecting Problems

### Stale Actor (running but not working)
- `last_health_check` > 5 minutes old
- Actor may be stuck, timer broken, or worker not processing

### Missing Actor
- `instance_actor_orchestration_id` is NULL
- Or orchestration doesn't exist in duroxide state

### Zombie Actor (in DB but not processing)
- Status shows "Running" but no health updates
- Often caused by server crash or DB migration

## API Endpoints

```bash
# Start new actor
curl -X POST /api/instances/:name/actor/start

# Restart actor (cancel + start new)
curl -X POST /api/instances/:name/actor/restart

# Cancel actor
curl -X POST /api/instances/:name/actor/cancel
```

## Duroxide Client Usage

```rust
// Cancel an actor
client.cancel_instance(&actor_id, "User requested cancellation").await?;

// Check if actor exists
match client.get_instance_info(&actor_id).await {
    Ok(info) => println!("Status: {}", info.status),
    Err(_) => println!("Actor not found"),
}

// Start new actor (detached)
client.start_orchestration(
    &new_actor_id,
    orchestrations::INSTANCE_ACTOR,
    serde_json::to_string(&input)?,
).await?;
```

## Recovery Procedures

### Restart All Stale Actors
```sql
-- Find instances with stale health
SELECT user_name, k8s_name, last_health_check, instance_actor_orchestration_id
FROM toygres_cms.instances
WHERE state = 'running'
  AND (last_health_check IS NULL OR last_health_check < NOW() - INTERVAL '5 minutes');
```

Then use the UI or API to restart each actor.

### After Database Migration
If duroxide state wasn't migrated, all actors are orphaned:
1. List all running instances
2. For each, call `/api/instances/:name/actor/start`
