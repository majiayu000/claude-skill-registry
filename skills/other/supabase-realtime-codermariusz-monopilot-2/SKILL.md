---
name: supabase-realtime
description: Apply when implementing real-time features: live updates, presence, broadcast messages, or database change subscriptions.
---

## When to Use

Apply when implementing real-time features: live updates, presence, broadcast messages, or database change subscriptions.

## Patterns

### Pattern 1: Database Changes Subscription
```typescript
// Source: https://supabase.com/docs/guides/realtime
import { useEffect } from 'react';
import { supabase } from '@/lib/supabase';

function useRealtimeMessages(roomId: string) {
  const [messages, setMessages] = useState<Message[]>([]);

  useEffect(() => {
    // Initial fetch
    supabase.from('messages').select('*').eq('room_id', roomId)
      .then(({ data }) => setMessages(data || []));

    // Subscribe to changes
    const channel = supabase
      .channel(`room:${roomId}`)
      .on('postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'messages', filter: `room_id=eq.${roomId}` },
        (payload) => setMessages((prev) => [...prev, payload.new as Message])
      )
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, [roomId]);

  return messages;
}
```

### Pattern 2: Presence (Who's Online)
```typescript
// Source: https://supabase.com/docs/guides/realtime/presence
const [onlineUsers, setOnlineUsers] = useState<User[]>([]);

useEffect(() => {
  const channel = supabase.channel('online-users');

  channel
    .on('presence', { event: 'sync' }, () => {
      const state = channel.presenceState();
      const users = Object.values(state).flat() as User[];
      setOnlineUsers(users);
    })
    .subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        await channel.track({ user_id: currentUser.id, name: currentUser.name });
      }
    });

  return () => { supabase.removeChannel(channel); };
}, [currentUser]);
```

### Pattern 3: Broadcast (Client-to-Client)
```typescript
// Source: https://supabase.com/docs/guides/realtime/broadcast
const channel = supabase.channel('cursor-positions');

// Send cursor position
const sendCursor = (x: number, y: number) => {
  channel.send({
    type: 'broadcast',
    event: 'cursor',
    payload: { x, y, userId: currentUser.id },
  });
};

// Receive cursor positions
channel
  .on('broadcast', { event: 'cursor' }, ({ payload }) => {
    setCursors((prev) => ({ ...prev, [payload.userId]: payload }));
  })
  .subscribe();
```

### Pattern 4: All Change Events
```typescript
// Source: https://supabase.com/docs/reference/javascript/subscribe
const channel = supabase
  .channel('table-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      if (payload.eventType === 'INSERT') handleInsert(payload.new);
      if (payload.eventType === 'UPDATE') handleUpdate(payload.new);
      if (payload.eventType === 'DELETE') handleDelete(payload.old);
    }
  )
  .subscribe();
```

## Anti-Patterns

- **No cleanup** - Always `removeChannel` on unmount
- **Subscribing to entire table** - Use filters to limit data
- **No error handling** - Handle subscription errors
- **Missing RLS** - Realtime respects RLS policies

## Verification Checklist

- [ ] Channel cleanup in useEffect return
- [ ] Filters applied to subscriptions
- [ ] Initial data fetched before subscribe
- [ ] RLS policies allow realtime access
- [ ] Error state handling for subscription failures
