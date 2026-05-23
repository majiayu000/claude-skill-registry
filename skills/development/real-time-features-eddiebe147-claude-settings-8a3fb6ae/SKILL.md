---
name: real-time-features
description: Expert guide for real-time features using Supabase Realtime, WebSockets, live updates, presence, and collaborative features. Use when building chat, live updates, or collaborative apps.
---

# Real-Time Features Skill

## Overview

This skill helps you implement real-time features in your Next.js application. From live data updates to collaborative editing, this covers everything you need for interactive, real-time experiences.

## Supabase Realtime

### Setup
```typescript
// lib/supabase/client.ts
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### Real-Time Subscriptions

**Subscribe to Table Changes:**
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function RealtimeMessages() {
  const [messages, setMessages] = useState<Message[]>([])
  const supabase = createClient()

  useEffect(() => {
    // Fetch initial data
    supabase
      .from('messages')
      .select('*')
      .order('created_at', { ascending: true })
      .then(({ data }) => setMessages(data || []))

    // Subscribe to new messages
    const channel = supabase
      .channel('messages')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
        },
        (payload) => {
          setMessages((prev) => [...prev, payload.new as Message])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  return (
    <div>
      {messages.map((msg) => (
        <div key={msg.id}>{msg.content}</div>
      ))}
    </div>
  )
}
```

**Subscribe to All Events:**
```typescript
const channel = supabase
  .channel('messages-all')
  .on(
    'postgres_changes',
    {
      event: '*', // INSERT, UPDATE, DELETE
      schema: 'public',
      table: 'messages',
    },
    (payload) => {
      if (payload.eventType === 'INSERT') {
        setMessages((prev) => [...prev, payload.new as Message])
      }
      if (payload.eventType === 'UPDATE') {
        setMessages((prev) =>
          prev.map((msg) =>
            msg.id === payload.new.id ? (payload.new as Message) : msg
          )
        )
      }
      if (payload.eventType === 'DELETE') {
        setMessages((prev) =>
          prev.filter((msg) => msg.id !== payload.old.id)
        )
      }
    }
  )
  .subscribe()
```

**Filter Subscriptions:**
```typescript
// Only listen to messages in a specific room
const channel = supabase
  .channel(`room:${roomId}`)
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: `room_id=eq.${roomId}`,
    },
    (payload) => {
      setMessages((prev) => [...prev, payload.new as Message])
    }
  )
  .subscribe()
```

## Custom Realtime Hook

```typescript
// hooks/use-realtime-subscription.ts
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { RealtimeChannel } from '@supabase/supabase-js'

type UseRealtimeOptions<T> = {
  table: string
  filter?: string
  event?: 'INSERT' | 'UPDATE' | 'DELETE' | '*'
  onInsert?: (record: T) => void
  onUpdate?: (record: T) => void
  onDelete?: (record: T) => void
}

export function useRealtimeSubscription<T>({
  table,
  filter,
  event = '*',
  onInsert,
  onUpdate,
  onDelete,
}: UseRealtimeOptions<T>) {
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase
      .channel(`${table}-changes`)
      .on(
        'postgres_changes',
        {
          event,
          schema: 'public',
          table,
          filter,
        },
        (payload) => {
          if (payload.eventType === 'INSERT' && onInsert) {
            onInsert(payload.new as T)
          }
          if (payload.eventType === 'UPDATE' && onUpdate) {
            onUpdate(payload.new as T)
          }
          if (payload.eventType === 'DELETE' && onDelete) {
            onDelete(payload.old as T)
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [table, filter, event, onInsert, onUpdate, onDelete, supabase])
}

// Usage
function Chat({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([])

  useRealtimeSubscription<Message>({
    table: 'messages',
    filter: `room_id=eq.${roomId}`,
    event: '*',
    onInsert: (msg) => setMessages((prev) => [...prev, msg]),
    onUpdate: (msg) =>
      setMessages((prev) =>
        prev.map((m) => (m.id === msg.id ? msg : m))
      ),
    onDelete: (msg) =>
      setMessages((prev) => prev.filter((m) => m.id !== msg.id)),
  })

  return <div>{/* Render messages */}</div>
}
```

## Presence (Who's Online)

### Track User Presence
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type PresenceState = {
  [key: string]: {
    user_id: string
    username: string
    online_at: string
  }[]
}

export function usePresence(roomId: string) {
  const [onlineUsers, setOnlineUsers] = useState<PresenceState>({})
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel(`room:${roomId}`)

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState<PresenceState>()
        setOnlineUsers(state)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          // Get current user
          const {
            data: { user },
          } = await supabase.auth.getUser()

          if (user) {
            // Track presence
            await channel.track({
              user_id: user.id,
              username: user.email,
              online_at: new Date().toISOString(),
            })
          }
        }
      })

    return () => {
      channel.untrack()
      supabase.removeChannel(channel)
    }
  }, [roomId, supabase])

  return onlineUsers
}

// Usage
function ChatRoom({ roomId }: { roomId: string }) {
  const onlineUsers = usePresence(roomId)
  const count = Object.keys(onlineUsers).length

  return (
    <div>
      <p>{count} users online</p>
      {Object.values(onlineUsers).map((presences) =>
        presences.map((presence) => (
          <div key={presence.user_id}>{presence.username}</div>
        ))
      )}
    </div>
  )
}
```

## Broadcast (Send Custom Messages)

### Real-Time Collaboration
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type CursorPosition = {
  x: number
  y: number
  user_id: string
  username: string
}

export function CollaborativeCanvas({ roomId }: { roomId: string }) {
  const [cursors, setCursors] = useState<CursorPosition[]>([])
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel(`canvas:${roomId}`)

    channel
      .on('broadcast', { event: 'cursor-move' }, ({ payload }) => {
        setCursors((prev) => {
          const filtered = prev.filter(
            (c) => c.user_id !== payload.user_id
          )
          return [...filtered, payload as CursorPosition]
        })
      })
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId, supabase])

  const handleMouseMove = async (e: React.MouseEvent) => {
    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (user) {
      supabase.channel(`canvas:${roomId}`).send({
        type: 'broadcast',
        event: 'cursor-move',
        payload: {
          x: e.clientX,
          y: e.clientY,
          user_id: user.id,
          username: user.email,
        },
      })
    }
  }

  return (
    <div onMouseMove={handleMouseMove}>
      {cursors.map((cursor) => (
        <div
          key={cursor.user_id}
          style={{
            position: 'absolute',
            left: cursor.x,
            top: cursor.y,
            width: 10,
            height: 10,
            borderRadius: '50%',
            backgroundColor: 'blue',
            pointerEvents: 'none',
          }}
        >
          <span>{cursor.username}</span>
        </div>
      ))}
    </div>
  )
}
```

## Live Chat Application

### Chat Component
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Message = {
  id: string
  content: string
  user_id: string
  username: string
  created_at: string
}

export function LiveChat({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [typing, setTyping] = useState<Set<string>>(new Set())
  const supabase = createClient()

  useEffect(() => {
    // Fetch initial messages
    supabase
      .from('messages')
      .select('*')
      .eq('room_id', roomId)
      .order('created_at', { ascending: true })
      .then(({ data }) => setMessages(data || []))

    const channel = supabase.channel(`chat:${roomId}`)

    // Listen for new messages
    channel
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        (payload) => {
          setMessages((prev) => [...prev, payload.new as Message])
        }
      )
      // Listen for typing indicators
      .on('broadcast', { event: 'typing' }, ({ payload }) => {
        setTyping((prev) => new Set(prev).add(payload.user_id))
        setTimeout(() => {
          setTyping((prev) => {
            const next = new Set(prev)
            next.delete(payload.user_id)
            return next
          })
        }, 3000)
      })
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId, supabase])

  const sendMessage = async () => {
    if (!newMessage.trim()) return

    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (!user) return

    await supabase.from('messages').insert({
      content: newMessage,
      room_id: roomId,
      user_id: user.id,
      username: user.email,
    })

    setNewMessage('')
  }

  const handleTyping = async () => {
    const {
      data: { user },
    } = await supabase.auth.getUser()

    if (user) {
      supabase.channel(`chat:${roomId}`).send({
        type: 'broadcast',
        event: 'typing',
        payload: { user_id: user.id },
      })
    }
  }

  return (
    <div>
      <div className="h-96 overflow-y-auto">
        {messages.map((msg) => (
          <div key={msg.id}>
            <strong>{msg.username}:</strong> {msg.content}
          </div>
        ))}
      </div>

      {typing.size > 0 && (
        <p className="text-sm text-gray-500">
          {typing.size} {typing.size === 1 ? 'person is' : 'people are'} typing...
        </p>
      )}

      <div className="flex gap-2">
        <input
          value={newMessage}
          onChange={(e) => {
            setNewMessage(e.target.value)
            handleTyping()
          }}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  )
}
```

## Live Notifications

### Notification System
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Notification = {
  id: string
  title: string
  message: string
  read: boolean
  created_at: string
}

export function NotificationBell() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const supabase = createClient()

  useEffect(() => {
    const fetchNotifications = async () => {
      const {
        data: { user },
      } = await supabase.auth.getUser()

      if (!user) return

      const { data } = await supabase
        .from('notifications')
        .select('*')
        .eq('user_id', user.id)
        .order('created_at', { ascending: false })

      setNotifications(data || [])
      setUnreadCount(data?.filter((n) => !n.read).length || 0)
    }

    fetchNotifications()

    const channel = supabase
      .channel('notifications')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'notifications',
        },
        (payload) => {
          setNotifications((prev) => [payload.new as Notification, ...prev])
          setUnreadCount((prev) => prev + 1)

          // Show browser notification
          if ('Notification' in window && Notification.permission === 'granted') {
            new Notification(payload.new.title, {
              body: payload.new.message,
            })
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  const markAsRead = async (id: string) => {
    await supabase
      .from('notifications')
      .update({ read: true })
      .eq('id', id)

    setNotifications((prev) =>
      prev.map((n) => (n.id === id ? { ...n, read: true } : n))
    )
    setUnreadCount((prev) => prev - 1)
  }

  return (
    <div>
      <button className="relative">
        🔔
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white rounded-full w-5 h-5 text-xs">
            {unreadCount}
          </span>
        )}
      </button>

      <div>
        {notifications.map((notification) => (
          <div
            key={notification.id}
            className={notification.read ? 'opacity-50' : ''}
            onClick={() => markAsRead(notification.id)}
          >
            <h4>{notification.title}</h4>
            <p>{notification.message}</p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

## Live Dashboard Updates

### Real-Time Analytics
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Stats = {
  total_users: number
  active_sessions: number
  revenue_today: number
}

export function LiveDashboard() {
  const [stats, setStats] = useState<Stats>({
    total_users: 0,
    active_sessions: 0,
    revenue_today: 0,
  })
  const supabase = createClient()

  useEffect(() => {
    // Fetch initial stats
    const fetchStats = async () => {
      const { data } = await supabase.rpc('get_dashboard_stats')
      setStats(data)
    }

    fetchStats()

    // Listen for relevant table changes
    const channel = supabase
      .channel('dashboard-updates')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'users',
        },
        () => {
          setStats((prev) => ({
            ...prev,
            total_users: prev.total_users + 1,
          }))
        }
      )
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'orders',
        },
        (payload) => {
          setStats((prev) => ({
            ...prev,
            revenue_today: prev.revenue_today + payload.new.amount,
          }))
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  return (
    <div className="grid grid-cols-3 gap-4">
      <div className="p-4 bg-white rounded shadow">
        <h3>Total Users</h3>
        <p className="text-3xl font-bold">{stats.total_users}</p>
      </div>
      <div className="p-4 bg-white rounded shadow">
        <h3>Active Sessions</h3>
        <p className="text-3xl font-bold">{stats.active_sessions}</p>
      </div>
      <div className="p-4 bg-white rounded shadow">
        <h3>Revenue Today</h3>
        <p className="text-3xl font-bold">${stats.revenue_today}</p>
      </div>
    </div>
  )
}
```

## Optimistic Updates

### Instant UI Updates
```typescript
'use client'
import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function TodoList() {
  const [todos, setTodos] = useState<Todo[]>([])
  const supabase = createClient()

  const addTodo = async (text: string) => {
    // Optimistic update - update UI immediately
    const tempId = crypto.randomUUID()
    const optimisticTodo = {
      id: tempId,
      text,
      done: false,
      created_at: new Date().toISOString(),
    }

    setTodos((prev) => [...prev, optimisticTodo])

    try {
      // Insert to database
      const { data, error } = await supabase
        .from('todos')
        .insert({ text, done: false })
        .select()
        .single()

      if (error) throw error

      // Replace temp todo with real one
      setTodos((prev) =>
        prev.map((todo) => (todo.id === tempId ? data : todo))
      )
    } catch (error) {
      // Rollback on error
      setTodos((prev) => prev.filter((todo) => todo.id !== tempId))
      console.error('Failed to add todo:', error)
    }
  }

  return <div>{/* Render todos */}</div>
}
```

## Connection Status

### Track Connection State
```typescript
'use client'
import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

export function ConnectionStatus() {
  const [isConnected, setIsConnected] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel('connection-test')

    channel
      .on('system', { event: 'online' }, () => setIsConnected(true))
      .on('system', { event: 'offline' }, () => setIsConnected(false))
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [supabase])

  if (!isConnected) {
    return (
      <div className="bg-red-500 text-white p-2 text-center">
        ⚠️ Connection lost. Reconnecting...
      </div>
    )
  }

  return null
}
```

## Best Practices Checklist

- [ ] Clean up subscriptions on unmount
- [ ] Handle connection errors gracefully
- [ ] Implement optimistic updates for better UX
- [ ] Use presence for online status
- [ ] Implement typing indicators in chat
- [ ] Show connection status to users
- [ ] Rate limit broadcast messages
- [ ] Use filters to reduce unnecessary updates
- [ ] Implement reconnection logic
- [ ] Handle duplicate messages
- [ ] Use channels efficiently
- [ ] Test with slow/offline connections
- [ ] Implement message queuing for offline
- [ ] Monitor realtime usage/costs

## When to Use This Skill

Invoke this skill when:
- Building chat applications
- Implementing live notifications
- Creating collaborative features
- Adding presence/online status
- Building real-time dashboards
- Implementing live updates
- Creating multiplayer features
- Debugging realtime connections
- Optimizing realtime performance
- Implementing typing indicators
