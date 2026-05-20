---
name: websocket-streaming
description: Implements real-time bidirectional communication between DAG execution engines and visualization dashboards via WebSocket. Covers connection management, typed event protocols, reconnection
  with backoff, and React hook integration. Activate on "WebSocket", "real-time updates", "live streaming", "execution events", "state streaming", "push notifications". NOT for HTTP REST APIs, server-sent
  events (SSE), or general networking.
allowed-tools: Read,Write,Edit,Bash
metadata:
  category: DevOps & Site Reliability
  tags:
  - websocket
  - streaming
  - real-time-updates
  - live-streaming
  pairs-with:
  - skill: reactflow-expert
    reason: WebSocket connections deliver live DAG state updates to ReactFlow visualization dashboards
  - skill: real-time-collaboration-engine
    reason: WebSocket transport powers the real-time communication layer for collaborative editing
  - skill: llm-streaming-response-handler
    reason: WebSocket is an alternative transport to SSE for bidirectional LLM streaming
---

# WebSocket Streaming

Real-time bidirectional communication between DAG execution engines and dashboards. Typed event protocols, connection management, and React hook integration.

---

## When to Use

✅ **Use for**:
- Streaming DAG node state changes to a visualization dashboard
- Sending human gate decisions from dashboard to execution engine
- Live cost ticker and progress updates during execution
- Bi-directional communication (not just server → client)

❌ **NOT for**:
- One-way server → client updates (consider SSE, simpler)
- REST API design (use `api-architect`)
- Polling-based status checks (WebSocket replaces polling)

---

## Event Protocol

### Server → Client Events

```typescript
type ServerEvent =
  | { type: 'node_state'; node_id: string; status: NodeStatus; output?: any; metrics?: NodeMetrics }
  | { type: 'edge_active'; from: string; to: string }
  | { type: 'dag_mutated'; mutation: DAGMutation }
  | { type: 'cost_update'; spent: number; budget: number; remaining: number }
  | { type: 'execution_complete'; results: Record<string, any> }
  | { type: 'human_gate_waiting'; node_id: string; presentation: GatePresentation }
  | { type: 'error'; node_id?: string; message: string };
```

### Client → Server Events

```typescript
type ClientEvent =
  | { type: 'human_decision'; node_id: string; decision: 'approve' | 'reject' | 'modify'; feedback?: string }
  | { type: 'pause_execution' }
  | { type: 'resume_execution' }
  | { type: 'cancel_execution' };
```

---

## React Hook: useDAGStream

```typescript
import { useEffect, useRef, useCallback } from 'react';

export function useDAGStream(dagId: string, store: DAGStore) {
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectAttempt = useRef(0);

  const connect = useCallback(() => {
    const ws = new WebSocket(`/api/dags/${dagId}/stream`);

    ws.onopen = () => { reconnectAttempt.current = 0; };

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data) as ServerEvent;
      switch (msg.type) {
        case 'node_state':
          store.updateNodeData(msg.node_id, {
            status: msg.status, output: msg.output, metrics: msg.metrics,
          });
          break;
        case 'cost_update':
          store.setCostState({ spent: msg.spent, budget: msg.budget });
          break;
        case 'dag_mutated':
          store.applyMutation(msg.mutation);
          break;
        case 'execution_complete':
          store.setExecutionComplete(msg.results);
          break;
      }
    };

    ws.onclose = () => {
      // Reconnect with exponential backoff (max 30s)
      const delay = Math.min(1000 * 2 ** reconnectAttempt.current, 30000);
      reconnectAttempt.current++;
      setTimeout(connect, delay);
    };

    wsRef.current = ws;
  }, [dagId, store]);

  useEffect(() => { connect(); return () => wsRef.current?.close(); }, [connect]);

  // Send client events
  const send = useCallback((event: ClientEvent) => {
    wsRef.current?.send(JSON.stringify(event));
  }, []);

  return { send };
}
```

---

## Server Implementation (Node.js)

```typescript
import { WebSocketServer } from 'ws';

const wss = new WebSocketServer({ noServer: true });

// Per-DAG rooms
const rooms = new Map<string, Set<WebSocket>>();

function broadcast(dagId: string, event: ServerEvent) {
  const clients = rooms.get(dagId);
  if (!clients) return;
  const msg = JSON.stringify(event);
  for (const ws of clients) {
    if (ws.readyState === ws.OPEN) ws.send(msg);
  }
}

// Usage in execution engine:
function onNodeComplete(dagId: string, nodeId: string, result: any) {
  broadcast(dagId, {
    type: 'node_state',
    node_id: nodeId,
    status: 'completed',
    output: result.output,
    metrics: result.metrics,
  });
}
```

---

## Anti-Patterns

### No Reconnection Logic
**Wrong**: WebSocket closes and the dashboard shows stale data forever.
**Right**: Exponential backoff reconnection (1s, 2s, 4s, 8s... max 30s). Resync state on reconnect.

### Sending Full State on Every Event
**Wrong**: Broadcasting the entire DAG state on every node update.
**Right**: Send only the delta: which node changed, to what status. The client applies the update to its local store.

### No Typed Protocol
**Wrong**: Sending untyped JSON objects and parsing with `any`.
**Right**: Define `ServerEvent` and `ClientEvent` union types. Exhaustive switch on `msg.type`.
