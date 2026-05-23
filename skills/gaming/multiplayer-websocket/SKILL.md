---
name: multiplayer-websocket
description: Manages WebSocket-based real-time multiplayer in Tokyo Sounds. Use when modifying multiplayer sync, useMultiplayer hook, multiplayer-server, message protocol, or adding features that broadcast or receive player state over WebSocket.
---

# Multiplayer WebSocket (Tokyo Sounds)

This project uses a **standalone WebSocket server** plus a **React hook** for real-time multiplayer. The server runs separately (e.g. `npx tsx multiplayer-server.ts` on port 3001). The client connects via `useMultiplayer`, sends position/rotation updates (throttled), and receives a list of nearby players to render.

## Architecture at a Glance

| Layer                           | Role                                                                                                                            |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **multiplayer-server.ts**       | Node.js `ws` server: join/update/leave, 500m visibility, 50ms broadcast, 10s stale cleanup                                      |
| **src/types/multiplayer.ts**    | Shared ClientMessage / ServerMessage and PlayerState types                                                                      |
| **src/hooks/useMultiplayer.ts** | Connect on mount, send join/update/leave, handle welcome/players/playerLeft, throttle updates (50ms), silent reconnect every 5s |
| **Pages / MultiplayerManager**  | Call `useMultiplayer`, pass `nearbyPlayers` to `OtherPlayers`, call `sendUpdate` from position/rotation callbacks or `useFrame` |

## When to Use This Skill

- Changing WebSocket URL (e.g. env `NEXT_PUBLIC_MULTIPLAYER_URL`), port, or ws/wss.
- Adding or changing message types (extend `ClientMessage` / `ServerMessage` in `src/types/multiplayer.ts` and both server and hook).
- Adjusting throttle/broadcast intervals (`CLIENT_UPDATE_INTERVAL_MS`, `BROADCAST_INTERVAL_MS`, `RECONNECT_INTERVAL_MS`, `STALE_PLAYER_TIMEOUT_MS`).
- Fixing connection lifecycle, reconnection, or cleanup in `useMultiplayer`.
- Adding server-side logic (visibility radius, auth, rooms) in `multiplayer-server.ts`.

## Conventions

- **Refs for socket and timers**: Hook keeps `WebSocket` in a ref; cleanup on unmount clears reconnect timeout and closes socket.
- **Mounted guard**: Use `mountedRef.current` before `setState` after async (onopen/onclose) to avoid updates after unmount.
- **Throttle on client**: `sendUpdate` only sends when `Date.now() - lastUpdateTimeRef >= CLIENT_UPDATE_INTERVAL_MS` (50ms).
- **URL**: In browser, use `ws://` or `wss://` to match page protocol; from HTTPS use `wss://` (mixed content otherwise).

## Quick Reference

- Message protocol and example code: see [reference.md](reference.md).
- Server entry: `multiplayer-server.ts`; client entry: `src/hooks/useMultiplayer.ts` and `src/types/multiplayer.ts`.
