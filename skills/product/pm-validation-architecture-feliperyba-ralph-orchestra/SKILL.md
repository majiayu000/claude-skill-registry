---
name: pm-validation-architecture
description: Detect and validate client-authoritative vs server-authoritative architecture gaps
category: validation
---

# Architecture Validation Skill

> "Server-authoritative code must have specific validation markers. If markers are missing, code is likely client-authoritative."

## When to Use This Skill

Use during **retrospective synthesis** when analyzing why multiplayer features may not be truly server-authoritative.

## Critical Detection Pattern

**Retrospective 2026-01-22 Finding**: Tasks marked `serverAuthoritative: true` had 100% client-side implementation.

**Detection Pattern**:
1. Task marked as `serverAuthoritative: true`
2. Code review shows client calculates state directly
3. Server only logs input, doesn't process
4. TODO comments exist in server code (e.g., "TODO: Forward to ECS")

## Architecture Validation Checklist

For each task marked `serverAuthoritative: true`:

### Step 1: Check Client Code

```bash
# Search for direct state manipulation (anti-pattern)
grep -r "velocity.x = " src/components/game/player/
grep -r "position.x += " src/components/game/player/
grep -r "rigidBody.setVelocity" src/components/game/

# These indicate CLIENT-SIDE physics (not server-authoritative)
```

**What to look for**:

| Pattern | Indicates | Correct Pattern |
|---------|-----------|-----------------|
| `rigidBody.setVelocity()` | Client-authoritative | `networkManager.send({ type: 'input', ... })` |
| `position.x += input.x` | Client-authoritative | Server applies velocity |
| `if (hit) spawnDecal()` | Client-authoritative | Server confirms hit, then spawn |
| `score += 10` | Client-authoritative | Server calculates score |

### Step 2: Check Server Code

```bash
# Search for actual input processing (good pattern)
grep -A 10 "onMessage" server/rooms/GameRoom.ts

# Look for TODO comments (warning sign)
grep -r "TODO" server/rooms/GameRoom.ts
```

**What to look for**:

| Pattern | Indicates | Correct Pattern |
|---------|-----------|-----------------|
| `console.log(data)` only | Server not processing | Input validation + simulation |
| `TODO: Forward to ECS` | Incomplete implementation | ECS integration complete |
| Empty message handler | Server ignores client | Handler processes input |

### Step 3: Check Message Flow

```typescript
// CORRECT: Server-authoritative message flow
// Client (PlayerController.tsx)
networkManager.send({
  type: 'player_input',
  input: { forward, backward, left, right, jump },
  sequence: inputSequence++
});

// Server (GameRoom.ts)
onMessage(client, data) {
  if (data.type === 'player_input') {
    const input = data.input;

    // VALIDATE
    if (!validateInput(input, player)) return;

    // PROCESS
    const velocity = calculateVelocity(input);
    player.x += velocity.x * dt;
    player.z += velocity.z * dt;

    // BROADCAST
    this.broadcast({
      type: 'player_state',
      sessionId: client.sessionId,
      position: { x: player.x, z: player.z }
    });
  }
}
```

## Detection: Code Review Commands

```bash
# Check if movement is client-authoritative
rg "rigidBody\.velocity|setVelocity|setLinvel" src/components/game/player/

# Check if shooting is client-authoritative
rg "spawnProjectile|createProjectile" src/components/game/weapons/

# Check for TODO comments indicating incomplete server implementation
rg "TODO.*server|TODO.*ECS" server/
```

## Architecture Gap Detection Matrix

| Feature | Client Code | Server Code | Gap |
|---------|-------------|-------------|-----|
| **Movement** | PlayerController.tsx:520-678 (direct velocity) | GameRoom.ts:265-282 (log only) | ✗ Client-authoritative |
| **Shooting** | PaintGun.tsx:208-394 (spawn projectile) | GameRoom.ts:287-299 (broadcast only) | ✗ Client-authoritative |
| **Score** | HUD.tsx (local calculation) | No server score tracking | ✗ Client-authoritative |

## PRD Update Pattern

When architecture gaps are detected, update PRD:

```json
{
  "id": "iter4-002",
  "serverAuthoritative": false,
  "revalidationRequired": true,
  "notes": "CODE REVIEW 2026-01-22: Currently 100% client-side. Needs validate-001 to implement server-authoritative movement."
}
```

Create new validation tasks:

```json
{
  "id": "validate-001",
  "title": "Server-Authoritative Movement Implementation",
  "description": "Refactor movement to be server-authoritative...",
  "acceptanceCriteria": [
    "Client sends input state via NetworkManager (not velocity)",
    "Server receives input messages in GameRoom",
    "Server validates input (speed limits, jump cooldowns)",
    "Server calculates velocity server-side",
    "TODO at GameRoom.ts:273 resolved"
  ]
}
```

## Red Flags for Client-Authoritative Code

| Symptom | Check | Result |
|---------|-------|--------|
| TODO comments in GameRoom.ts | `rg "TODO" server/rooms/GameRoom.ts` | Found: "TODO: Forward to player entity in ECS" |
| Direct physics manipulation on client | `rg "setVelocity\|velocity\.x\s*=" src/` | Found: Client controls physics |
| No input validation on server | Check `onMessage` handlers | Found: Only console.log |
| Server doesn't calculate state | Check server update loop | Found: MovementSystem.ts only syncs |

## Validation Script

```typescript
// scripts/validate-server-authoritative.ts
import { readFileSync } from 'fs';
import { globSync } from 'glob';

interface ValidationResult {
  taskId: string;
  feature: string;
  clientAuthoritative: boolean;
  issues: string[];
}

function validateServerAuthoritative(taskId: string): ValidationResult {
  const issues: string[] = [];
  let clientAuthoritative = false;

  // Check client code for direct state manipulation
  const clientFiles = globSync(`src/components/game/**/*.tsx`);
  for (const file of clientFiles) {
    const content = readFileSync(file, 'utf-8');

    if (content.includes('rigidBody.setVelocity') ||
        content.includes('velocity.x =') ||
        content.includes('position.x +=')) {
      issues.push(`${file}: Direct state manipulation detected`);
      clientAuthoritative = true;
    }
  }

  // Check server code for input processing
  const serverFiles = globSync(`server/**/*.ts`);
  for (const file of serverFiles) {
    const content = readFileSync(file, 'utf-8');

    if (content.includes('TODO')) {
      issues.push(`${file}: TODO comment indicates incomplete implementation`);
      clientAuthoritative = true;
    }

    if (content.includes('console.log') && !content.includes('validate')) {
      issues.push(`${file}: Input logged but not validated`);
      clientAuthoritative = true;
    }
  }

  return {
    taskId,
    feature: taskId,
    clientAuthoritative,
    issues
  };
}
```

## Decision Framework

| Question | Yes → | No → |
|----------|-------|------|
| Client sends input (WASD, aim)? | Continue | ❌ Not server-authoritative |
| Server validates input? | Continue | ❌ Client-authoritative |
| Server calculates state? | Continue | ❌ Client-authoritative |
| Server broadcasts state? | Continue | ❌ Client-authoritative |
| Server rejects invalid input? | ✓ Server-authoritative | ⚠ Partial |

## Retrospective Questions for Architecture Validation

During retrospective, ask Developer:

1. **Does client send input or state?**
   - Input (WASD, aim) → ✓ Correct
   - State (position, velocity) → ✗ Client-authoritative

2. **Does server validate input?**
   - Yes (speed limits, cooldowns) → ✓ Correct
   - No (accepts all input) → ✗ Not server-authoritative

3. **Does server calculate game state?**
   - Yes (physics, collisions) → ✓ Correct
   - No (client calculates) → ✗ Client-authoritative

4. **Are there TODO comments in server code?**
   - Yes → ⚠ Incomplete implementation
   - No → ✓ Likely complete

## Anti-Patterns

❌ **DON'T:**

- Trust PRD `serverAuthoritative: true` without code review
- Assume server code processes input without checking
- Skip checking for TODO comments
- Ignore client-side direct state manipulation

✅ **DO:**

- Code review every `serverAuthoritative: true` task
- Check client code for direct state changes
- Check server code for actual input processing
- Look for TODO comments as warning signs
- Create validation tasks when gaps found

## Skill Improvement

After detecting architecture gaps:

1. **Update this skill** with new detection patterns
2. **Add code examples** from actual project
3. **Create validation tasks** in PRD
4. **Update Developer skill** with server-authoritative patterns

## Reference

- [dev-multiplayer-colyseus-server](../dev-multiplayer-colyseus-server/SKILL.md) — Server-authoritative implementation
- [pm-retrospective-facilitation](../pm-retrospective-facilitation/SKILL.md) — When to use this detection
- [qa-multiplayer-testing](../qa-multiplayer-testing/SKILL.md) — Testing server authority
