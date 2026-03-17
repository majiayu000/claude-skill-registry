---
name: "supabase-realtime-specialist"
description: "Implement Supabase Realtime subscriptions for live data updates; use when building real-time features like live notifications, collaborative editing, presence detection, or live data feeds"
version: "1.0.0"
---

# Supabase Realtime Specialist

## Supabase Project Reference

| Environment | Project ID | URL |
|-------------|-----------|-----|
| **Production** | `csjruhqyqzzqxnfeyiaf` | `https://csjruhqyqzzqxnfeyiaf.supabase.co` |
| **Staging** | `hxpcknyqswetsqmqmeep` | `https://hxpcknyqswetsqmqmeep.supabase.co` |

**For database credentials and deployment**: See `.claude/skills/production-database-query/SKILL.md`

## Overview

Supabase Realtime enables live data updates without polling. This skill covers:
- **Realtime subscriptions** to database changes
- **Presence tracking** (who's online)
- **Collaborative features** (live editing)
- **Live notifications** (instant alerts)

---

## 🟢 Quick Start

### Enable Realtime on a Table

```sql
-- In Supabase SQL Editor
BEGIN;

-- Realtime must be enabled on tables you want to subscribe to
ALTER PUBLICATION supabase_realtime ADD TABLE events;
ALTER PUBLICATION supabase_realtime ADD TABLE users;

COMMIT;
```

### Subscribe to Changes in Client Component

```typescript
'use client'
import { useEffect, useState } from 'react'
import { useSupabaseClient } from '@kit/supabase/hooks/use-supabase'

export function LiveEventsList() {
  const [events, setEvents] = useState<Event[]>([])
  const supabase = useSupabaseClient()

  useEffect(() => {
    // Fetch initial data
    const fetchEvents = async () => {
      const { data } = await supabase
        .from('events')
        .select()

      setEvents(data || [])
    }

    fetchEvents()

    // Subscribe to changes
    const channel = supabase
      .channel('events')
      .on(
        'postgres_changes',
        { event: '*', schema: 'public', table: 'events' },
        (payload) => {
          // payload.eventType = 'INSERT' | 'UPDATE' | 'DELETE'
          // payload.new = new record (INSERT, UPDATE)
          // payload.old = old record (UPDATE, DELETE)

          if (payload.eventType === 'INSERT') {
            setEvents(prev => [payload.new as Event, ...prev])
          } else if (payload.eventType === 'UPDATE') {
            setEvents(prev =>
              prev.map(e =>
                e.id === payload.new.id ? payload.new : e
              )
            )
          } else if (payload.eventType === 'DELETE') {
            setEvents(prev => prev.filter(e => e.id !== payload.old.id))
          }
        }
      )
      .subscribe()

    // Cleanup
    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  return (
    <div>
      <h2>Live Events ({events.length})</h2>
      {events.map(event => (
        <EventCard key={event.id} event={event} />
      ))}
    </div>
  )
}
```

---

## 📡 Realtime Subscriptions

### Type 1: Row Changes (INSERT, UPDATE, DELETE)

```typescript
// Subscribe to any changes on 'events' table
const channel = supabase
  .channel('events')
  .on(
    'postgres_changes',
    {
      event: '*', // 'INSERT' | 'UPDATE' | 'DELETE' | '*'
      schema: 'public',
      table: 'events',
    },
    (payload) => {
      console.log('Change:', payload.eventType, payload.new || payload.old)
    }
  )
  .subscribe()

// Cleanup
supabase.removeChannel(channel)
```

### Type 2: Broadcast Messages

```typescript
// Send custom messages (not database changes)
const channel = supabase.channel('notifications')

// Send message
channel.send({
  type: 'broadcast',
  event: 'user_action',
  payload: { userId: 123, action: 'liked_post' },
})

// Listen to messages
channel.on('broadcast', { event: 'user_action' }, (payload) => {
  console.log('User action:', payload.payload)
})

channel.subscribe()
```

### Type 3: Presence (Who's Online)

```typescript
'use client'
import { useEffect, useState } from 'react'
import { useSupabaseClient } from '@kit/supabase/hooks/use-supabase'
import { useUser } from '@kit/supabase/hooks/use-user'

export function OnlineUsers() {
  const [onlineUsers, setOnlineUsers] = useState<User[]>([])
  const supabase = useSupabaseClient()
  const user = useUser()

  useEffect(() => {
    if (!user) return

    const channel = supabase.channel('presence')

    channel.on('presence', { event: 'sync' }, () => {
      // Get all users in channel
      const users = channel.presenceState()
      const userList = Object.values(users).flat() as User[]
      setOnlineUsers(userList)
    })

    channel.on('presence', { event: 'join' }, (payload) => {
      // New user joined
      const newUser = payload.newPresences[0]
      setOnlineUsers(prev => [...prev, newUser])
    })

    channel.on('presence', { event: 'leave' }, (payload) => {
      // User left
      const leftUser = payload.leftPresences[0]
      setOnlineUsers(prev =>
        prev.filter(u => u.id !== leftUser.id)
      )
    })

    // Subscribe this user
    channel.subscribe(async (status) => {
      if (status === 'SUBSCRIBED') {
        await channel.track({
          id: user.id,
          email: user.email,
          lastSeen: new Date(),
        })
      }
    })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase, user])

  return (
    <div>
      <h3>Online Users ({onlineUsers.length})</h3>
      {onlineUsers.map(u => (
        <div key={u.id}>{u.email} 🟢 Online</div>
      ))}
    </div>
  )
}
```

---

## 🎯 Real-World Examples

### Example 1: Live Feed (Like Twitter)

```typescript
'use client'
import { useEffect, useState } from 'react'
import { useSupabaseClient } from '@kit/supabase/hooks/use-supabase'

export function LiveFeed() {
  const [posts, setPosts] = useState<Post[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const supabase = useSupabaseClient()

  useEffect(() => {
    let isMounted = true

    const setupRealtime = async () => {
      // Fetch initial posts
      const { data: initialPosts } = await supabase
        .from('posts')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(50)

      if (isMounted) {
        setPosts(initialPosts || [])
        setIsLoading(false)
      }

      // Subscribe to new posts
      const channel = supabase
        .channel('posts')
        .on(
          'postgres_changes',
          { event: 'INSERT', schema: 'public', table: 'posts' },
          (payload) => {
            if (isMounted) {
              // New post inserted
              setPosts(prev => [payload.new as Post, ...prev])
            }
          }
        )
        .on(
          'postgres_changes',
          { event: 'UPDATE', schema: 'public', table: 'posts' },
          (payload) => {
            if (isMounted) {
              // Post updated (likes, comments count, etc.)
              setPosts(prev =>
                prev.map(p => (p.id === payload.new.id ? payload.new : p))
              )
            }
          }
        )
        .subscribe()

      return () => {
        supabase.removeChannel(channel)
      }
    }

    setupRealtime()

    return () => {
      isMounted = false
    }
  }, [supabase])

  return (
    <div>
      {isLoading ? (
        <div>Loading posts...</div>
      ) : (
        posts.map(post => (
          <PostCard key={post.id} post={post} />
        ))
      )}
    </div>
  )
}
```

### Example 2: Collaborative Editing (Live Cursor)

```typescript
'use client'
import { useEffect, useState } from 'react'
import { useSupabaseClient } from '@kit/supabase/hooks/use-supabase'
import { useUser } from '@kit/supabase/hooks/use-user'

export function CollaborativeEditor({ documentId }: { documentId: string }) {
  const [content, setContent] = useState('')
  const [remoteCursors, setRemoteCursors] = useState<Cursor[]>([])
  const supabase = useSupabaseClient()
  const user = useUser()

  useEffect(() => {
    if (!user) return

    const channel = supabase
      .channel(`editor-${documentId}`, {
        config: { broadcast: { self: true } },
      })

    // Listen to document changes
    channel.on(
      'postgres_changes',
      {
        event: 'UPDATE',
        schema: 'public',
        table: 'documents',
        filter: `id=eq.${documentId}`,
      },
      (payload) => {
        setContent(payload.new.content)
      }
    )

    // Listen to cursor positions
    channel.on('broadcast', { event: 'cursor' }, (payload) => {
      setRemoteCursors(prev => [
        ...prev.filter(c => c.userId !== payload.payload.userId),
        payload.payload,
      ])
    })

    channel.subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase, documentId, user])

  const handleContentChange = async (newContent: string) => {
    setContent(newContent)

    // Update database
    await supabase
      .from('documents')
      .update({ content: newContent })
      .eq('id', documentId)
  }

  const handleMouseMove = (e: MouseEvent) => {
    // Broadcast cursor position
    const channel = supabase.channel(`editor-${documentId}`)
    channel.send({
      type: 'broadcast',
      event: 'cursor',
      payload: {
        userId: user?.id,
        x: e.clientX,
        y: e.clientY,
        userName: user?.email,
      },
    })
  }

  return (
    <div onMouseMove={handleMouseMove}>
      <textarea
        value={content}
        onChange={e => handleContentChange(e.target.value)}
        placeholder="Start typing..."
      />

      {/* Show remote cursors */}
      {remoteCursors.map(cursor => (
        <div
          key={cursor.userId}
          style={{
            position: 'absolute',
            left: `${cursor.x}px`,
            top: `${cursor.y}px`,
            pointerEvents: 'none',
          }}
        >
          <div className="text-xs bg-blue-500 text-white px-2 py-1 rounded">
            {cursor.userName}
          </div>
        </div>
      ))}
    </div>
  )
}
```

### Example 3: Live Notifications

```typescript
'use client'
import { useEffect } from 'react'
import { useSupabaseClient } from '@kit/supabase/hooks/use-supabase'
import { useUser } from '@kit/supabase/hooks/use-user'
import { useToast } from '@kit/ui/use-toast'

export function NotificationListener() {
  const supabase = useSupabaseClient()
  const user = useUser()
  const { toast } = useToast()

  useEffect(() => {
    if (!user) return

    const channel = supabase
      .channel(`notifications-${user.id}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'notifications',
          filter: `user_id=eq.${user.id}`,
        },
        (payload) => {
          const notification = payload.new as Notification
          toast({
            title: notification.title,
            description: notification.message,
            duration: 5000,
          })
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase, user, toast])

  return null // This component just listens
}
```

---

## ⚠️ Important: RLS and Realtime

### Problem

By default, RLS policies do NOT apply to Realtime subscriptions!

### Solution 1: Use `@supabase` JWT for Auth

```typescript
// Supabase client with JWT auth
const channel = supabase
  .channel('events', {
    config: {
      broadcast: { ack: true },
      presence: { key: user.id },
    },
  })
  .subscribe()
```

### Solution 2: Add Realtime-Specific RLS

```sql
-- RLS policy for Realtime (in addition to regular SELECT)
CREATE POLICY "realtime_users_can_see_own_events"
  ON events
  FOR SELECT
  TO authenticated
  USING (auth.uid() = user_id);

-- Enable realtime for this policy
ALTER POLICY "realtime_users_can_see_own_events"
  ON events
  USING (auth.uid() = user_id);
```

### Solution 3: Manual Filtering

```typescript
// Filter on client side (less efficient but safe)
const channel = supabase
  .channel('events')
  .on('postgres_changes', { event: '*', table: 'events' }, (payload) => {
    // Only process if user has access
    if (payload.new?.user_id === user?.id) {
      // Process update
    }
  })
  .subscribe()
```

---

## 🔧 Performance Optimization

### Problem 1: Too Many Subscriptions

❌ **WRONG**:
```typescript
// Creates new subscription on every render
const { data } = useQuery(() =>
  supabase.channel('events').on(...).subscribe()
)
```

✅ **RIGHT**: Use useEffect with cleanup
```typescript
useEffect(() => {
  const channel = supabase.channel('events').on(...).subscribe()
  return () => supabase.removeChannel(channel)
}, [])
```

### Problem 2: Channel Name Collision

❌ **WRONG**:
```typescript
// Multiple components create channel 'events' → conflict
const channel1 = supabase.channel('events')
const channel2 = supabase.channel('events') // Overwrites channel1
```

✅ **RIGHT**: Use unique channel names
```typescript
const channel = supabase.channel(`events-${userId}`)
```

### Problem 3: Memory Leaks

❌ **WRONG**: No cleanup
```typescript
useEffect(() => {
  supabase.channel('events').subscribe()
  // No cleanup - subscription never stops
}, [])
```

✅ **RIGHT**: Always cleanup
```typescript
useEffect(() => {
  const channel = supabase.channel('events').subscribe()
  return () => supabase.removeChannel(channel)
}, [])
```

---

## 📋 Checklist: Setting Up Realtime

- [ ] Enable Realtime on tables in Supabase (SQL: `ALTER PUBLICATION`)
- [ ] Import `useSupabaseClient` from `@kit/supabase/hooks`
- [ ] Create subscription in `useEffect` (not in render)
- [ ] Handle all payload types (INSERT, UPDATE, DELETE)
- [ ] Cleanup subscription on unmount
- [ ] Use unique channel names
- [ ] Test RLS policies with Realtime
- [ ] Handle connection loss gracefully
- [ ] Consider performance impact (many subscriptions?)

---

## 🚨 Debugging Realtime Issues

### Issue 1: Updates Not Appearing

**Check**:
1. Is Realtime enabled on the table?
   ```sql
   SELECT * FROM pg_publication_tables WHERE pubname = 'supabase_realtime';
   ```

2. Is the user authenticated?
   ```typescript
   const { data: { user } } = await supabase.auth.getUser()
   console.log('User:', user)
   ```

3. Is the filter correct?
   ```typescript
   // Check filter matches actual changes
   event: 'INSERT', // or UPDATE, DELETE, '*'
   schema: 'public', // correct schema?
   table: 'events', // correct table?
   ```

### Issue 2: RLS Blocking Realtime

**Check**:
1. Does user have SELECT permission on table?
2. Test with admin client first:
   ```typescript
   const adminClient = createClient(URL, ADMIN_KEY)
   // This bypasses RLS - if it works, RLS is the issue
   ```

### Issue 3: Too Many Messages

**Solution**: Add filters
```typescript
.on(
  'postgres_changes',
  {
    event: 'UPDATE',
    schema: 'public',
    table: 'events',
    filter: `user_id=eq.${userId}`, // Only this user's events
  },
  (payload) => { }
)
```

---

## 💡 Best Practices

1. **Always cleanup subscriptions** (prevents memory leaks)
2. **Filter early** (reduce message volume)
3. **Use unique channel names** (prevent collisions)
4. **Handle RLS carefully** (Realtime bypasses RLS by default)
5. **Test with multiple clients** (ensure real-time is working)
6. **Monitor bandwidth** (each message costs data)
7. **Handle disconnections** (fallback to polling)
8. **Use broadcast for non-DB messages** (presence, cursors)

---

## 📚 See Also

- [Supabase Realtime Docs](https://supabase.com/docs/guides/realtime)
- [Row Level Security](../../docs/04-DATABASE.md#row-level-security)
- [Supabase Auth Wrappers](../../lib/auth-wrappers.ts)
- [useSupabaseClient Hook](../../packages/@kit/supabase/hooks/use-supabase.ts)
