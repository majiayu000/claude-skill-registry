---
name: supabase-api
description: Supabase JavaScript client API and REST API usage. Use when integrating Supabase, setting up clients, or using REST endpoints directly.
---

# Supabase API Skill

JavaScript client and REST API reference.

## Installation

```bash
npm install @supabase/supabase-js
```

## Client Initialization

### Browser Client

```javascript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(
  'https://your-project.supabase.co',
  'your-anon-key'
)
```

### With TypeScript Types

```typescript
import { createClient } from '@supabase/supabase-js'
import { Database } from './database.types'

const supabase = createClient<Database>(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)
```

### Server Client (Service Role)

```javascript
const supabaseAdmin = createClient(
  process.env.SUPABASE_URL,
  process.env.SUPABASE_SERVICE_ROLE_KEY,
  {
    auth: {
      autoRefreshToken: false,
      persistSession: false
    }
  }
)
```

### Custom Options

```javascript
const supabase = createClient(url, key, {
  auth: {
    persistSession: true,
    autoRefreshToken: true,
    storage: localStorage,
    storageKey: 'supabase-auth'
  },
  global: {
    headers: { 'x-custom-header': 'value' }
  },
  db: {
    schema: 'public'
  },
  realtime: {
    params: {
      eventsPerSecond: 10
    }
  }
})
```

## REST API Direct

### API URL Format

```
https://<project-ref>.supabase.co/rest/v1/<table>
```

### Headers

```javascript
const headers = {
  'apikey': 'your-anon-key',
  'Authorization': 'Bearer your-anon-key',
  'Content-Type': 'application/json',
  'Prefer': 'return=representation'  // Return data after mutation
}
```

### Select (GET)

```bash
# All rows
curl 'https://xxx.supabase.co/rest/v1/users' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY"

# Specific columns
curl 'https://xxx.supabase.co/rest/v1/users?select=id,name,email' \
  -H "apikey: $SUPABASE_KEY"

# With filter
curl 'https://xxx.supabase.co/rest/v1/users?status=eq.active' \
  -H "apikey: $SUPABASE_KEY"

# With pagination (query params)
curl 'https://xxx.supabase.co/rest/v1/users?limit=10&offset=0' \
  -H "apikey: $SUPABASE_KEY"

# With pagination (Range header - alternative)
curl 'https://xxx.supabase.co/rest/v1/users' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Range: 0-9"

# With ordering
curl 'https://xxx.supabase.co/rest/v1/users?order=created_at.desc' \
  -H "apikey: $SUPABASE_KEY"

# Get count with results
curl 'https://xxx.supabase.co/rest/v1/users?select=*' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Prefer: count=exact"
```

### Insert (POST)

```bash
curl -X POST 'https://xxx.supabase.co/rest/v1/users' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "John", "email": "john@example.com"}'
```

### Update (PATCH)

```bash
curl -X PATCH 'https://xxx.supabase.co/rest/v1/users?id=eq.123' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d '{"name": "John Doe"}'
```

### Upsert (POST with Resolution)

```bash
curl -X POST 'https://xxx.supabase.co/rest/v1/users' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation,resolution=merge-duplicates" \
  -d '{"id": 123, "name": "John"}'
```

### Delete (DELETE)

```bash
curl -X DELETE 'https://xxx.supabase.co/rest/v1/users?id=eq.123' \
  -H "apikey: $SUPABASE_KEY" \
  -H "Authorization: Bearer $SUPABASE_KEY"
```

## Filter Operators (REST)

| Operator | Example |
|----------|---------|
| `eq` | `?status=eq.active` |
| `neq` | `?status=neq.deleted` |
| `gt` | `?age=gt.18` |
| `gte` | `?age=gte.21` |
| `lt` | `?price=lt.100` |
| `lte` | `?price=lte.50` |
| `like` | `?name=like.*John*` |
| `ilike` | `?name=ilike.*john*` |
| `is` | `?deleted_at=is.null` |
| `in` | `?status=in.(active,pending)` |
| `cs` | `?tags=cs.{sports,news}` (contains) |
| `cd` | `?tags=cd.{a,b,c}` (contained by) |
| `or` | `?or=(status.eq.active,status.eq.pending)` |
| `and` | `?and=(status.eq.active,verified.eq.true)` |

## JavaScript Client Quick Reference

### Database Operations

```javascript
// Select
const { data, error } = await supabase.from('table').select('*')

// Select with filter
const { data } = await supabase.from('table').select('*').eq('id', 1)

// Insert
const { data } = await supabase.from('table').insert({ col: 'value' }).select()

// Update
const { data } = await supabase.from('table').update({ col: 'new' }).eq('id', 1)

// Upsert
const { data } = await supabase.from('table').upsert({ id: 1, col: 'value' })

// Delete
const { error } = await supabase.from('table').delete().eq('id', 1)

// RPC (function call)
const { data } = await supabase.rpc('function_name', { param: 'value' })
```

### Auth Operations

```javascript
// Sign up
await supabase.auth.signUp({ email, password })

// Sign in
await supabase.auth.signInWithPassword({ email, password })

// Sign out
await supabase.auth.signOut()

// Get user
const { data: { user } } = await supabase.auth.getUser()

// Get session
const { data: { session } } = await supabase.auth.getSession()

// Auth state listener
supabase.auth.onAuthStateChange((event, session) => { })
```

### Storage Operations

```javascript
// Upload
await supabase.storage.from('bucket').upload('path', file)

// Download
const { data } = await supabase.storage.from('bucket').download('path')

// Get public URL
const { data } = supabase.storage.from('bucket').getPublicUrl('path')

// Get signed URL
const { data } = await supabase.storage.from('bucket').createSignedUrl('path', 3600)

// Delete
await supabase.storage.from('bucket').remove(['path'])

// List
const { data } = await supabase.storage.from('bucket').list('folder')
```

### Realtime Operations

```javascript
// Subscribe to database changes
const channel = supabase
  .channel('changes')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, callback)
  .subscribe()

// Broadcast
channel.send({ type: 'broadcast', event: 'message', payload: data })

// Presence
await channel.track({ user_id: '123' })
const state = channel.presenceState()

// Unsubscribe
await supabase.removeChannel(channel)
```

### Edge Functions

```javascript
const { data, error } = await supabase.functions.invoke('function-name', {
  body: { key: 'value' }
})
```

## Error Handling

```javascript
const { data, error } = await supabase.from('users').select('*')

if (error) {
  console.error('Error code:', error.code)
  console.error('Error message:', error.message)
  console.error('Error details:', error.details)
  console.error('Error hint:', error.hint)
  return
}

// data is safe to use
console.log(data)
```

### Common Error Codes

| Code | Description |
|------|-------------|
| `PGRST116` | No rows returned (single expected) |
| `PGRST301` | Multiple rows returned (single expected) |
| `23505` | Unique constraint violation |
| `23503` | Foreign key violation |
| `42501` | RLS policy violation |
| `42P01` | Table doesn't exist |

## TypeScript Types

### Generate Types

```bash
supabase gen types typescript --local > database.types.ts
```

### Type Helpers

```typescript
import { Database } from './database.types'

// Table row type
type User = Database['public']['Tables']['users']['Row']

// Insert type
type NewUser = Database['public']['Tables']['users']['Insert']

// Update type
type UpdateUser = Database['public']['Tables']['users']['Update']

// Query result type
import { QueryData } from '@supabase/supabase-js'

const usersQuery = supabase.from('users').select('id, name, posts(title)')
type UsersWithPosts = QueryData<typeof usersQuery>
```

## References

- [client-patterns.md](references/client-patterns.md) - Common client patterns
