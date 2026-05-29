---
name: activity-logging
description: Follow these patterns when implementing activity emission and audit logging in OptAIC. Use for emitting ActivityEnvelopes on mutations (create, update, delete, execute), designing payloads, and ensuring audit compliance.
---

# Activity Logging Patterns

Guide for implementing audit-compliant activity emission in OptAIC services.

## When to Use

Apply when:
- Implementing service layer methods that mutate state
- Adding new domain resource operations (CRUD)
- Tracking execution events (runs, training, backtests)
- Implementing approval/promotion workflows
- Ensuring audit trail compliance

## Core Rule

> **If it changes state, it MUST emit an activity.**

All mutations must emit activities in the **service layer** (not API handlers or models).

## ActivityEnvelope

```python
ActivityEnvelope(
    tenant_id=UUID,
    actor_principal_id=UUID,
    resource_id=UUID,
    resource_type=str,           # "signal", "dataset", "portfolio"
    action=str,                  # "signal.created", "run.completed"
    visibility=str,              # "private"|"resource"|"scope"|"tenant"
    payload=dict,                # Action-specific data
    delivery_channels=list,      # Where to publish
    correlation_id=UUID          # Links related activities
)
```

## Action Naming

Use pattern: `<resource>.<verb>`

### Core Resource Actions
```
signal.registered    signal.validated     signal.promoted
dataset.created      dataset.previewed    dataset.refresh_started
dataset.refresh_completed dataset.refresh_failed
```

### Pipeline Actions
```
pipeline_def.submitted   pipeline_def.deployed
pipeline_instance.created pipeline.run_started pipeline.run_completed
```

### Experiment Actions
```
experiment.created   experiment.updated
experiment.run_completed experiment.run_failed
expression.evaluated macro.saved
```

### Run Lifecycle Actions
```
run.started          run.completed        run.failed          run.cancelled
backtest.started     backtest.completed   backtest.failed
training.started     training.completed   training.failed
inference.started    inference.completed  inference.failed
optimization.started optimization.completed optimization.failed
monitoring.started   monitoring.completed monitoring.alert
```

### Portfolio Actions
```
portfolio.rebalanced portfolio.constraints_updated
portfolio.weights_computed portfolio.optimization_started
```

### Promotion/Workflow Actions
```
promotion.requested  promotion.approved   promotion.merged    promotion.rejected
guardrails.validated guardrails.blocked   guardrails.warned
```

### Monitoring Actions
```
monitoring.drift_detected    monitoring.performance_alert
monitoring.data_quality_alert monitoring.threshold_breach
```

## Emission Patterns

### Simple Emission
```python
await record_activity_with_outbox(
    session=self.session,
    envelope=ActivityEnvelope(
        action="signal.created",
        actor_principal_id=self.actor_id,
        tenant_id=self.tenant_id,
        resource_id=resource.id,
        resource_type="signal",
        payload={"signal_type": dto.signal_type}
    )
)
```

### Transaction Wrapper
```python
from libs.core.activity import tx_activity

result, activity = await tx_activity(db, envelope, domain_fn)
```

## Payload Guidelines

**Include:** Changed fields, related IDs, computed metrics, status transitions
**Exclude:** Passwords, API keys, large blobs, PII beyond necessity

See [references/payload-examples.md](references/payload-examples.md).

## Correlation IDs

Link related activities in workflows:
```python
correlation_id = uuid4()

# Use same correlation_id throughout workflow
await emit("promotion.requested", correlation_id=correlation_id)
await emit("guardrails.validated", correlation_id=correlation_id)
await emit("promotion.merged", correlation_id=correlation_id)
```

## Real-time Notifications (Outbox Worker)

Activities are processed by the outbox worker which publishes to Centrifugo for real-time WebSocket delivery.

### Notification Types

| Type | Who | Mechanism | Opt-in? |
|------|-----|-----------|---------|
| **Implicit** | Owner + Delegators | Query Resource + RoleBinding | Automatic |
| **Explicit** | Subscribers | Query Subscription table | User opts in |

### Watchers Build Flow

```python
# Outbox worker builds watchers set:
watchers: set[UUID] = set()

# 1. Explicit subscribers (user opt-in)
watchers |= await _subscription_watchers(session, tenant_id, resource_id)

# 2. Resource owner (implicit - auto-notified)
owner_id = await _resource_owner(session, tenant_id, resource_id)
if owner_id:
    watchers.add(owner_id)

# 3. Delegators (owner/delegator roles on resource or ancestors)
watchers |= await _resource_delegators(session, tenant_id, resource_id)

# 4. CRITICAL: Exclude actor (don't notify yourself)
watchers.discard(actor_principal_id)

# 5. Filter by user notification preferences
watchers = await _filter_watchers_by_preference(session, tenant_id, watchers, action)
```

### Notification Preferences

Users configure via `PUT /notifications/preferences`:

| Filter Mode | Actions Notified |
|-------------|------------------|
| `all` | All activity types |
| `mutations` (default) | `resource.created/updated/deleted`, `transfer.*`, `promotion.*` |
| `custom` | User-defined patterns (e.g., `["resource.*", "chat.*"]`) |

```python
# Custom pattern matching uses fnmatch
await client.notifications.update_preferences(
    filter_mode="custom",
    custom_actions=["resource.*", "promotion.*"],
)
```

### Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------------|----------------|------------------|
| Notify actor about own action | Noisy, redundant | Always `watchers.discard(actor_id)` |
| Hardcode notification targets | Inflexible | Build watchers dynamically |
| Skip preference filtering | Users can't control noise | Always filter by preferences |
| Notify without checking roles | Security issue | Use `_resource_delegators()` |

### Subscription API (Explicit Opt-in)

```python
# Subscribe to a resource
await client.subscriptions.create(
    resource_id=folder_id,
    scope="descendants",  # or "resource" for single resource
)

# List subscriptions
subs = await client.subscriptions.list()

# Unsubscribe
await client.subscriptions.revoke(subscription_id)
```

## Reference Files

- [Payload Examples](references/payload-examples.md) - Example payloads by action type
- [Testing Activities](references/testing.md) - How to test activity emission
