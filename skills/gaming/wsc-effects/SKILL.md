---
name: wsc-effects
description: Apply chronicle event effects to world state. Use when events need to modify entities (battles change force strength, treaties change relationships, deaths remove agents). This is the core simulation engine.
allowed-tools: Read, Write, Bash, Glob
---

# WSC Effects System

The effects system applies chronicle events to world state. When an event is emitted, its effects are applied deterministically to modify entity attributes.

## How It Works

```
Event Emitted → Effects Handler → Entity Updates
     ↓              ↓                   ↓
  battle.resolved → applyBattleEffects → force.strength reduced
```

## Commands

### Apply Effects for an Event

```bash
# Apply effects for a specific event
npx tsx .claude/skills/wsc-effects/scripts/apply.ts evt_10492

# Apply effects for all pending events
npx tsx .claude/skills/wsc-effects/scripts/apply.ts --pending

# Dry run (show what would change)
npx tsx .claude/skills/wsc-effects/scripts/apply.ts evt_10492 --dry-run
```

### List Effect Handlers

```bash
npx tsx .claude/skills/wsc-effects/scripts/apply.ts --list-handlers
```

## Effect Handlers

Each event type has a handler that knows how to apply its effects:

### Conflict Events

| Event Type | Effects |
|------------|---------|
| `battle.resolved` | Reduces force strength based on losses |
| `conflict.started` | Sets presence states to "at_war" |
| `conflict.ended` | Clears conflict states |
| `asset.captured` | Changes holding ownership |

### Influence Events

| Event Type | Effects |
|------------|---------|
| `influence.changed` | Modifies presence influence value |
| `control.changed` | Updates presence control status |

### Agent Events

| Event Type | Effects |
|------------|---------|
| `agent.killed` | Sets agent status to "dead" |
| `agent.promoted` | Updates agent role |
| `agent.defected` | Changes agent affiliation |
| `agent.wounded` | Reduces agent stats temporarily |

### Governance Events

| Event Type | Effects |
|------------|---------|
| `treaty.signed` | Creates relationship between polities |
| `election.held` | May change polity government |

### Settlement Events

| Event Type | Effects |
|------------|---------|
| `infrastructure.completed` | Adds infrastructure to site |
| `unrest.spike` | Increases site unrest value |

## Effect Application Rules

1. **Idempotency**: Effects are designed to be safely re-applied
2. **Validation**: Effects check entity exists before modifying
3. **Bounds**: Numeric values are clamped to valid ranges (0-1 for normalized)
4. **Logging**: All changes are logged for debugging

## Example: Battle Effects

For event `battle.resolved`:

```json
{
  "id": "evt_10492",
  "type": "battle.resolved",
  "who": ["force.7th_fleet", "force.raiders"],
  "data": {
    "outcome": "raider_victory",
    "losses": {
      "7th_fleet": { "strength_before": 0.75, "strength_after": 0.50 },
      "raiders": { "strength_before": 0.25, "strength_after": 0.20 }
    }
  }
}
```

Effects applied:
- `force.7th_fleet.attrs.strength` → 0.50
- `force.raiders.attrs.strength` → 0.20

## Adding New Handlers

Handlers are defined in `scripts/handlers.ts`. To add a new handler:

```typescript
export const handlers: EffectHandlers = {
  'my_event.type': (event, world) => {
    // Find relevant entities
    const entity = world.getEntity(event.who[0]);

    // Apply changes
    entity.attrs.value = event.data.newValue;

    // Save
    world.saveEntity(entity);

    return { modified: [entity.id] };
  },
};
```

## Integration

The effects system is typically called automatically by the orchestrator after events are emitted:

1. Agent emits event via `wsc-chronicle`
2. Orchestrator calls `wsc-effects` to apply
3. Entities are updated
4. Next tick proceeds
