---
name: qa-multiplayer-testing
description: E2E multiplayer testing using Playwright API with multi-client browser contexts. Validates server-authoritative patterns, state synchronization, and anti-cheat measures. Use when testing multiplayer features.
category: validation
---

# Multiplayer Testing with E2E Tests

> "Server-authoritative code must be validated with actual server connections using E2E tests."

## When to Use This Skill

Use for **EVERY task** marked with `serverAuthoritative: true` or `multiplayerTested: true`.

## Core Principle: Write Multi-Client E2E Tests

**✅ CORRECT APPROACH:**

```typescript
// Write E2E test with multiple browser contexts - YES!
test('server-authoritative movement sync', async ({ browser }) => {
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  // Test multi-client behavior
  await page1.goto('http://localhost:3000'); // E2E tests use baseURL from playwright.config.ts
  await page2.goto('http://localhost:3000');

  // Verify state sync...
});
```

**❌ DO NOT USE:**

```typescript
// Interactive MCP - NO!
mcp__playwright__browser_navigate('http://localhost:3000');
mcp__playwright__browser_tabs({ action: 'new' });
```

## Critical Architecture Principle

**Single-browser testing is INSUFFICIENT for multiplayer validation.**

You must verify in E2E tests:

- Server receives input from clients
- Server validates and processes input
- Server broadcasts state to all clients
- All clients see synchronized state

## Quick Start: Multi-Client Test Pattern

```typescript
// tests/e2e/multiplayer-suite.spec.ts
import { test, expect } from '@playwright/test';

test('server-authoritative movement sync', async ({ browser }) => {
  // Create 2 separate browser contexts (simulate 2 players)
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();

  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  try {
    // Both connect to same server room
    await page1.goto('http://localhost:3000?room=test_room');
    await page2.goto('http://localhost:3000?room=test_room');

    // Wait for connection
    await page1.waitForFunction(() => (window as any).isConnected?.() === true);
    await page2.waitForFunction(() => (window as any).isConnected?.() === true);

    // Player 1 moves (WASD input)
    await page1.click('canvas');
    await page1.keyboard.down('KeyW');
    await page1.waitForTimeout(500);
    await page1.keyboard.up('KeyW');

    // Wait for server sync
    await page1.waitForTimeout(200);

    // Player 2 should see Player 1's new position
    const player1PosOnPage2 = await page2.evaluate(() => {
      return (window as any).getRemotePlayerPosition?.('player1');
    });

    expect(player1PosOnPage2.z).toBeLessThan(0); // Moved forward
  } finally {
    await context1.close();
    await context2.close();
  }
});
```

## Test Categories

| Category         | What to Validate                                        |
| ---------------- | ------------------------------------------------------- |
| Connection       | Multiple clients connect to same room                   |
| State Sync       | All clients see same server state                       |
| Movement         | Client input → Server validate → All clients see result |
| Shooting         | Client fires → Server validates → All clients see paint |
| Spawning         | Server assigns spawn → All clients see same location    |
| Tamper Detection | Server rejects invalid inputs                           |
| Latency          | Client prediction + server reconciliation               |

## Server Management

**⚠️ CRITICAL: Use `shared-lifecycle` skill for server management.**

### Server Detection (Before Multiplayer E2E Tests)

**⚠️ IMPORTANT: Playwright's `webServer` config manages servers for E2E tests automatically.**

Multiplayer tests require both frontend (port 3000) and backend (Colyseus port 2567) servers.

When running `npm run test:e2e`, Playwright automatically starts:
- `npm run dev` (port 3000) with `reuseExistingServer: !process.env.CI`
- `npm run server` (port 2567) with `reuseExistingServer: false`

**DO NOT manually start servers for E2E tests.**

### Server Check Pattern

```bash
# Check if dev server is running (port 3000)
netstat -an | grep :3000 || lsof -i :3000

# Check if Colyseus server is running (port 2567)
netstat -an | grep :2567 || lsof -i :2567

# Alternative: Try curl to detect Vite
curl -s http://localhost:3000 | grep -q "vite" && echo "DEV_RUNNING" || echo "DEV_NOT_RUNNING"

# Check Colyseus WebSocket server
curl -s http://localhost:2567 || echo "COLYSEUS_NOT_RUNNING"
```

### E2E Test Path (Standard Multiplayer Validation)

```bash
# Playwright handles both servers via webServer config
npm run test:e2e -- tests/e2e/multiplayer-suite.spec.ts

# NO manual server start needed
# NO manual cleanup needed - Playwright handles it
```

### Manual MCP Validation Path (Only when explicitly needed)

```bash
# Only for manual MCP validation (NOT E2E tests)
# Check ports first
if ! netstat -an | grep :3000; then
  # Start dev server in background
  Bash(command="npm run dev", run_in_background=true)
  # Capture shell_id for cleanup
fi

if ! netstat -an | grep :2567; then
  # Start Colyseus server in background
  Bash(command="npm run server", run_in_background=true)
  # Capture shell_id for cleanup
fi

# After validation completes:
TaskStop(task_id="dev_server_shell_id")  # MANDATORY cleanup
TaskStop(task_id="server_shell_id")      # MANDATORY cleanup
```

Before running multiplayer E2E tests, always check/start the dev server using the patterns from `shared-lifecycle` skill.

**MANDATORY CLEANUP after all tests complete (pass OR fail):**

Use the cleanup patterns from `shared-lifecycle` skill to ensure:

- Dev server is stopped
- Backend server is stopped
- Ports 3000 and 2567 are released
- No orphaned processes remain

## Server Validation Checklist

Before running multiplayer E2E tests, verify server is running:

```bash
# Terminal 1: Start servers
npm run dev:all:sh
# Expected output: "listening on ws://localhost:2567"
# Expected output: "Local: http://localhost:3000"
```

**If server is NOT running, FAIL the validation immediately.**

## Progressive Guide

### Level 1: Multi-Client Connection

```typescript
test('two clients connect to same room', async ({ browser }) => {
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  try {
    // Both connect
    await page1.goto('http://localhost:3000');
    await page2.goto('http://localhost:3000');

    // Verify connection on both
    const connected1 = await page1.evaluate(() => (window as any).gameState?.connected);
    const connected2 = await page2.evaluate(() => (window as any).gameState?.connected);

    expect(connected1).toBe(true);
    expect(connected2).toBe(true);

    // Verify same room
    const room1 = await page1.evaluate(() => (window as any).gameState?.roomId);
    const room2 = await page2.evaluate(() => (window as any).gameState?.roomId);
    expect(room1).toBe(room2);
  } finally {
    await context1.close();
    await context2.close();
  }
});
```

### Level 2: State Synchronization

```typescript
test('movement syncs between clients', async ({ browser }) => {
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  try {
    await page1.goto('http://localhost:3000');
    await page2.goto('http://localhost:3000');

    // Wait for both players to spawn
    await page1.waitForFunction(() => (window as any).gameState?.players?.size >= 2);
    await page2.waitForFunction(() => (window as any).gameState?.players?.size >= 2);

    // Get initial positions
    const initialPos = await page1.evaluate(() => {
      const localId = (window as any).gameState?.localPlayerId;
      return (window as any).gameState?.players?.get(localId)?.position;
    });

    // Player 1 moves forward
    await page1.click('canvas');
    await page1.keyboard.down('KeyW');
    await page1.waitForTimeout(1000); // Move for 1 second
    await page1.keyboard.up('KeyW');

    // Wait for server sync
    await page1.waitForTimeout(200);

    // Verify Player 1 moved locally
    const localPos = await page1.evaluate(() => {
      const localId = (window as any).gameState?.localPlayerId;
      return (window as any).gameState?.players?.get(localId)?.position;
    });

    // Verify Player 2 sees Player 1's new position
    const remotePos = await page2.evaluate(() => {
      const players = (window as any).gameState?.players;
      for (const [id, player] of players?.entries()) {
        if (id !== (window as any).gameState?.localPlayerId) {
          return player.position;
        }
      }
    });

    expect(localPos.z).not.toBe(initialPos.z); // Local player moved
    expect(Math.abs(remotePos.z - localPos.z)).toBeLessThan(1); // Sync within tolerance
  } finally {
    await context1.close();
    await context2.close();
  }
});
```

### Level 3: Server Authority Validation

```typescript
test('server validates input (anti-cheat)', async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  // Expose game internals for testing
  const networkManager = await page.evaluate(() => (window as any).networkManager);

  // Attempt to send impossible input (speed hack)
  // This should be REJECTED by server
  await page.evaluate(() => {
    (window as any).networkManager?.send({
      type: 'player_input',
      input: {
        forward: true,
        speed: 999999, // Impossible speed - server should reject
      },
    });
  });

  // Verify position didn't teleport
  const posBefore = await page.evaluate(() => (window as any).gameState?.localPlayer?.position);
  await page.waitForTimeout(500);
  const posAfter = await page.evaluate(() => (window as any).gameState?.localPlayer?.position);

  // Position should NOT have changed dramatically
  expect(Math.abs(posAfter.x - posBefore.x)).toBeLessThan(5);
});
```

### Level 4: Paint Shooting Validation

```typescript
test('shooting syncs between clients', async ({ browser }) => {
  const context1 = await browser.newContext();
  const context2 = await browser.newContext();
  const page1 = await context1.newPage();
  const page2 = await context2.newPage();

  try {
    await page1.goto('http://localhost:3000');
    await page2.goto('http://localhost:3000');

    await page1.waitForFunction(() => (window as any).gameState?.players?.size >= 2);
    await page2.waitForFunction(() => (window as any).gameState?.players?.size >= 2);

    // Player 1 shoots
    await page1.click('canvas');
    await page1.mouse.click(400, 300); // Center of screen
    await page1.waitForTimeout(100);

    // Both clients should see the paint splat
    const paintCount1 = await page1.evaluate(
      () => (window as any).gameState?.paintSplats?.size || 0
    );
    const paintCount2 = await page2.evaluate(
      () => (window as any).gameState?.paintSplats?.size || 0
    );

    expect(paintCount1).toBeGreaterThan(0);
    expect(paintCount1).toBe(paintCount2); // Same count on both clients
  } finally {
    await context1.close();
    await context2.close();
  }
});
```

### Level 5: Network Latency Simulation

```typescript
test('client prediction works with latency', async ({ browser, context }) => {
  // Simulate high latency
  await context.route('**/*', async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 200)); // 200ms delay
    route.continue();
  });

  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  // Client should still feel responsive (prediction)
  // Even with 200ms latency, input should feel immediate
  await page.click('canvas');

  const posBefore = await page.evaluate(() => (window as any).gameState?.localPlayer?.position);
  await page.keyboard.down('KeyW');
  await page.waitForTimeout(100);
  await page.keyboard.up('KeyW');

  const predictedPos = await page.evaluate(() => (window as any).gameState?.localPlayer?.position);

  // Local prediction should have applied
  expect(predictedPos.z).toBeLessThan(posBefore.z);
});
```

## Using Page Objects for Multiplayer Tests

For cleaner tests, use the MultiplayerPage object:

```typescript
import { test, expect } from '@playwright/test';
import { MultiplayerPage } from '@/pages/multiplayer.page';

test('multiplayer state sync with page objects', async ({ browser }) => {
  const multiplayerPage = new MultiplayerPage(null); // page not needed for setup
  const players = await multiplayerPage.setupMultiPlayerTest(browser, 2);

  try {
    await multiplayerPage.connectPlayersToGame(players);
    expect(await multiplayerPage.verifyAllConnected(players)).toBe(true);

    // Player 1 moves
    await players[0].page.click('canvas');
    await players[0].page.keyboard.down('KeyW');
    await players[0].page.waitForTimeout(500);
    await players[0].page.keyboard.up('KeyW');

    // Verify sync
    const synced = await multiplayerPage.verifyStateSync(players);
    expect(synced).toBe(true);
  } finally {
    await multiplayerPage.cleanupPlayers(players);
  }
});
```

## Server-Side Integration Tests

Create server tests alongside client tests:

```typescript
// server/tests/integration/room.test.ts
import { describe, it, expect, beforeEach } from 'vitest';
import { GameRoom } from '../rooms/GameRoom';
import { Client, Room } from 'colyseus';

describe('GameRoom Server Authority', () => {
  let room: GameRoom;

  beforeEach(() => {
    room = new GameRoom();
    room.onCreate({});
  });

  it('validates player input speed', () => {
    const mockClient = { sessionId: 'test-player' } as Client;
    room.onJoin(mockClient);

    const player = room.state.players.get('test-player');

    // Send input with impossible speed
    room.onMessage(mockClient, {
      type: 'player_input',
      input: { speed: 9999 },
    });

    // Position should NOT have changed dramatically
    expect(player.x).toBeCloseTo(0, 0); // Still near spawn
  });

  it('validates shooting cooldown', () => {
    const mockClient = { sessionId: 'test-player' } as Client;
    room.onJoin(mockClient);

    const player = room.state.players.get('test-player');
    player.lastShotTime = Date.now();

    // Try to shoot again immediately (should be rejected)
    room.onMessage(mockClient, {
      type: 'shoot',
      aim: { x: 1, y: 0, z: 0 },
    });

    // No projectile should have been created
    expect(room.projectiles?.length || 0).toBe(0);
  });
});
```

## Tamper Detection Tests

Verify server rejects client manipulation attempts:

```typescript
test('server rejects position hacks', async ({ browser }) => {
  const page = await browser.newPage();
  await page.goto('http://localhost:3000');

  const posBefore = await page.evaluate(() => {
    return (window as any).gameState?.localPlayer?.position;
  });

  // Try to directly manipulate local position (client-side hack simulation)
  await page.evaluate(() => {
    const localId = (window as any).gameState?.localPlayerId;
    (window as any).gameState.players.get(localId).position = { x: 9999, y: 0, z: 9999 };
  });

  // Wait for server correction
  await page.waitForTimeout(500);

  // Server should have overridden the hacked position
  const posAfter = await page.evaluate(() => {
    return (window as any).gameState?.localPlayer?.position;
  });

  expect(posAfter.x).not.toBe(9999); // Server corrected it
  expect(Math.abs(posAfter.x - posBefore.x)).toBeLessThan(10); // Still near original
});
```

## Testing Checklist

For each multiplayer validation:

- [ ] Server running (`npm run dev:all:sh`)
- [ ] 2+ browser contexts created in test
- [ ] All clients connect to same room
- [ ] Client input sends to server (not local state)
- [ ] Server validates input (check logs)
- [ ] Server broadcasts state updates
- [ ] All clients see synchronized state
- [ ] Tamper attempts are rejected
- [ ] No console errors on any client
- [ ] No server errors in terminal
- [ ] Cleanup: contexts closed in finally block

## Common Mistakes

| ❌ Wrong                    | ✅ Right                                   |
| --------------------------- | ------------------------------------------ |
| Test with 1 browser context | Test with 2+ contexts (multi-client)       |
| Don't check server logs     | Verify server receives and processes input |
| Assume state syncs          | Assert state values match across clients   |
| Test local state only       | Test REMOTE player state from other client |
| Ignore server validation    | Test that invalid inputs are rejected      |
| Don't cleanup contexts      | Always close contexts in finally block     |

## Anti-Patterns

❌ **DON'T:**

- Test multiplayer features with only 1 browser
- Skip checking server logs
- Assume state sync without assertions
- Test only local player state
- Skip tamper detection tests
- Use Playwright MCP for multiplayer testing

✅ **DO:**

- Always test with 2+ browser contexts
- Monitor server logs for input processing
- Assert state synchronization explicitly
- Test remote player state from other client's perspective
- Include tamper detection tests
- Write E2E tests as persistent artifacts
- Always cleanup contexts in finally blocks

## Validation Failure Criteria

**FAIL the validation if:**

- Server is not running
- Clients cannot connect to same room
- State does not sync between clients within 500ms
- Server logs show no input processing
- Invalid inputs are not rejected
- Console errors on any client
- Server crashes or throws errors

## Running Multiplayer Tests

```bash
# Run all multiplayer tests
npm run test:e2e -- tests/e2e/multiplayer-suite.spec.ts

# Run specific test
npm run test:e2e -- -g "server-authoritative movement sync"

# Run in headed mode to see both browsers
npm run test:e2e -- --headed

# Run with debug mode
npm run test:e2e -- --debug
```

## References

- **[qa-e2e-test-creation/SKILL.md](../qa-e2e-test-creation/SKILL.md)** - Full E2E test patterns
- [tests/pages/multiplayer.page.ts](tests/pages/multiplayer.page.ts) - Multiplayer page object
- [Colyseus Testing Guide](https://docs.colyseus.io/colyseus/server/testing/) — Server-side testing
