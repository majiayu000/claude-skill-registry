---
name: realtime-react-hooks
model: standard
description: React hooks for real-time data with SSE, WebSocket, and SWR integration. Covers connection management, reconnection logic, and optimistic updates. Use when building React apps with real-time features. Triggers on SSE hook, WebSocket hook, real-time React, useEventSource, live updates.
---

# Real-Time React Hooks

Production patterns for real-time data in React applications using SSE, WebSocket, and SWR.


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install realtime-react-hooks
```


---

## When to Use

- React apps needing live data updates
- Dashboards with real-time metrics
- Chat interfaces, notifications
- Any UI that should update without refresh

---

## Pattern 1: SSE Hook

```typescript
import { useEffect, useRef, useState, useCallback } from 'react';

interface UseSSEOptions<T> {
  url: string;
  onMessage?: (data: T) => void;
  onError?: (error: Event) => void;
  enabled?: boolean;
}

export function useSSE<T>({
  url,
  onMessage,
  onError,
  enabled = true,
}: UseSSEOptions<T>) {
  const [data, setData] = useState<T | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    if (!enabled) return;

    const eventSource = new EventSource(url);
    eventSourceRef.current = eventSource;

    eventSource.onopen = () => {
      setIsConnected(true);
    };

    eventSource.onmessage = (event) => {
      try {
        const parsed = JSON.parse(event.data) as T;
        setData(parsed);
        onMessage?.(parsed);
      } catch (e) {
        console.error('SSE parse error:', e);
      }
    };

    eventSource.onerror = (error) => {
      setIsConnected(false);
      onError?.(error);
    };

    return () => {
      eventSource.close();
      eventSourceRef.current = null;
    };
  }, [url, enabled]);

  const close = useCallback(() => {
    eventSourceRef.current?.close();
    setIsConnected(false);
  }, []);

  return { data, isConnected, close };
}
```

---

## Pattern 2: WebSocket Hook with Reconnection

```typescript
interface UseWebSocketOptions {
  url: string;
  onMessage?: (data: unknown) => void;
  reconnect?: boolean;
  maxRetries?: number;
}

export function useWebSocket({
  url,
  onMessage,
  reconnect = true,
  maxRetries = 5,
}: UseWebSocketOptions) {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const retriesRef = useRef(0);

  const connect = useCallback(() => {
    const ws = new WebSocket(url);
    wsRef.current = ws;

    ws.onopen = () => {
      setIsConnected(true);
      retriesRef.current = 0;
    };

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        onMessage?.(data);
      } catch {
        onMessage?.(event.data);
      }
    };

    ws.onclose = () => {
      setIsConnected(false);
      if (reconnect && retriesRef.current < maxRetries) {
        retriesRef.current++;
        const delay = Math.min(1000 * 2 ** retriesRef.current, 30000);
        setTimeout(connect, delay);
      }
    };

    ws.onerror = () => {
      ws.close();
    };
  }, [url, onMessage, reconnect, maxRetries]);

  useEffect(() => {
    connect();
    return () => wsRef.current?.close();
  }, [connect]);

  const send = useCallback((data: unknown) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify(data));
    }
  }, []);

  return { isConnected, send };
}
```

---

## Pattern 3: SWR with Real-Time Updates

```typescript
import useSWR from 'swr';
import { useEffect } from 'react';

export function useRealtimeData<T>(
  key: string,
  fetcher: () => Promise<T>
) {
  const { data, mutate, ...rest } = useSWR(key, fetcher);

  // Subscribe to real-time updates
  useEffect(() => {
    const eventSource = new EventSource(`/api/events/${key}`);

    eventSource.onmessage = (event) => {
      const update = JSON.parse(event.data);
      
      // Optimistically update cache
      mutate((current) => {
        if (!current) return update;
        return { ...current, ...update };
      }, false); // false = don't revalidate
    };

    return () => eventSource.close();
  }, [key, mutate]);

  return { data, mutate, ...rest };
}
```

---

## Pattern 4: Subscription Hook

```typescript
interface UseSubscriptionOptions {
  channels: string[];
  onEvent: (channel: string, data: unknown) => void;
}

export function useSubscription({ channels, onEvent }: UseSubscriptionOptions) {
  const { send, isConnected } = useWebSocket({
    url: '/api/ws',
    onMessage: (msg: any) => {
      if (msg.type === 'event') {
        onEvent(msg.channel, msg.data);
      }
    },
  });

  useEffect(() => {
    if (!isConnected) return;

    // Subscribe to channels
    channels.forEach((channel) => {
      send({ type: 'subscribe', channel });
    });

    return () => {
      channels.forEach((channel) => {
        send({ type: 'unsubscribe', channel });
      });
    };
  }, [channels, isConnected, send]);

  return { isConnected };
}
```

---

## Pattern 5: Connection Status Indicator

```tsx
export function ConnectionStatus({ isConnected }: { isConnected: boolean }) {
  return (
    <div className="flex items-center gap-2">
      <span
        className={cn(
          'size-2 rounded-full',
          isConnected ? 'bg-success animate-pulse' : 'bg-destructive'
        )}
      />
      <span className="text-xs text-muted-foreground">
        {isConnected ? 'Live' : 'Disconnected'}
      </span>
    </div>
  );
}
```

---

## Related Skills

- **Meta-skill:** [ai/skills/meta/realtime-dashboard/](../../meta/realtime-dashboard/) — Complete realtime dashboard guide
- [resilient-connections](../resilient-connections/) — Retry logic
- [design-systems/animated-financial-display](../../design-systems/animated-financial-display/) — Number animations

---

## NEVER Do

- **NEVER forget cleanup** — Always close connections on unmount
- **NEVER reconnect infinitely** — Use max retries with exponential backoff
- **NEVER parse without try/catch** — Server might send malformed data
- **NEVER mutate and revalidate** — Use `mutate(data, false)` for optimistic updates
- **NEVER ignore connection state** — Show users when they're disconnected

---

## Quick Reference

```typescript
// SSE
const { data, isConnected } = useSSE({ url: '/api/events' });

// WebSocket
const { isConnected, send } = useWebSocket({
  url: 'wss://api.example.com/ws',
  onMessage: (data) => console.log(data),
});

// SWR + Real-time
const { data } = useRealtimeData('metrics', fetchMetrics);

// Subscriptions
useSubscription({
  channels: ['user:123', 'global'],
  onEvent: (channel, data) => updateState(channel, data),
});
```
