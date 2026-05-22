---
name: supabase-debugger
description: This skill should be used when debugging, monitoring, or optimizing Supabase applications. Triggers on Supabase connection issues, RLS policy problems, authentication failures, slow queries, realtime subscription bugs, memory leaks, and database schema validation. Provides real-time inspection, error tracking, performance analysis, and systematic debugging workflows for local and cloud Supabase environments.
---

# Supabase Debugger

Debug, monitor, and optimize Supabase applications with systematic troubleshooting workflows and real-time analysis.

## Overview

This skill enables comprehensive debugging of Supabase applications covering:
- **Authentication**: Session monitoring, token inspection, MFA tracking
- **Database**: Query analysis, RLS policy validation, connection pooling
- **Realtime**: Subscription monitoring, latency testing, payload analysis
- **Performance**: Memory tracking, slow query detection, optimization recommendations

## When to Use This Skill

Activate this skill when encountering:
- "Connection refused" or database connectivity issues
- Authentication token expired/invalid errors
- RLS policy violations or permission denied errors
- Slow queries or page load performance issues
- Realtime messages not delivering
- Memory usage growing unexpectedly
- Schema validation errors (missing columns, constraints)
- Pre-deployment verification needs

## Workflow Decision Tree

```
Issue Type?
├── Connection Issues → Workflow 1: Connection Diagnostics
├── Auth Problems → Workflow 2: Authentication Debugging
├── Slow Performance → Workflow 3: Query Optimization
├── Realtime Issues → Workflow 4: Subscription Debugging
├── Memory Leaks → Workflow 5: Memory Investigation
├── RLS Violations → Workflow 6: Policy Validation
├── Pre-Deploy Check → Workflow 7: Production Readiness
├── Data Resurrection → Workflow 8: localStorage Fallback Audit
└── Production API Issues → Workflow 9: Production Debugging (Cloudflare + Caddy)
```

## Workflow 1: Connection Diagnostics

When encountering "Connection refused" or database connectivity issues:

### Step 1: Verify Infrastructure

```bash
# Check if Docker is running
docker ps

# Check Supabase services status
npx supabase status
```

### Step 2: Test Database Connection

```bash
# Test PostgreSQL connection directly
psql "postgresql://postgres:postgres@localhost:5432/postgres" -c "SELECT 1"

# Check connection from application
curl http://localhost:54321/rest/v1/ -H "apikey: YOUR_ANON_KEY"
```

### Step 3: Analyze Connection Pool

```sql
-- Check active connections
SELECT count(*), state, wait_event_type
FROM pg_stat_activity
GROUP BY state, wait_event_type;

-- Check max connections
SHOW max_connections;
```

### Step 4: Common Fixes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Connection refused | Docker not running | `docker-compose up -d` |
| Too many connections | Pool exhausted | Implement connection pooling |
| Timeout | Network issue | Check firewall, increase timeout |

## Workflow 2: Authentication Debugging

When users report login failures or token issues:

### Step 1: Inspect Token

```javascript
// Decode JWT token (in browser console)
const token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...';
const payload = JSON.parse(atob(token.split('.')[1]));
console.log({
  userId: payload.sub,
  email: payload.email,
  role: payload.role,
  expiresAt: new Date(payload.exp * 1000),
  isExpired: Date.now() > payload.exp * 1000
});
```

### Step 2: Check Auth Configuration

```sql
-- Check auth.users table
SELECT id, email, created_at, last_sign_in_at, confirmed_at
FROM auth.users
WHERE email = 'user@example.com';

-- Check auth settings
SELECT * FROM auth.config;
```

### Step 3: Monitor Auth Events

```javascript
// Set up auth state listener
supabase.auth.onAuthStateChange((event, session) => {
  console.log('Auth event:', event);
  console.log('Session:', session);
});
```

### Step 4: Token Refresh Implementation

```javascript
// Implement token refresh before expiration
const { data, error } = await supabase.auth.refreshSession();
if (error) {
  console.error('Refresh failed:', error.message);
  // Handle by redirecting to login
}
```

## Workflow 3: Query Optimization

When experiencing slow page loads or database performance issues:

### Step 1: Enable Query Logging

```sql
-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- View slow queries
SELECT
  query,
  calls,
  total_time / calls as avg_time_ms,
  rows
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY total_time DESC
LIMIT 20;
```

### Step 2: Analyze Specific Query

```sql
-- Explain analyze a slow query
EXPLAIN (ANALYZE, BUFFERS, FORMAT TEXT)
SELECT * FROM tasks WHERE user_id = 'uuid-here';
```

### Step 3: Index Recommendations

```sql
-- Find missing indexes on foreign keys
SELECT
  tc.table_name,
  kcu.column_name,
  'CREATE INDEX idx_' || tc.table_name || '_' || kcu.column_name
    || ' ON ' || tc.table_name || '(' || kcu.column_name || ');' as suggested_index
FROM information_schema.table_constraints tc
JOIN information_schema.key_column_usage kcu
  ON tc.constraint_name = kcu.constraint_name
WHERE tc.constraint_type = 'FOREIGN KEY'
AND NOT EXISTS (
  SELECT 1 FROM pg_indexes
  WHERE tablename = tc.table_name
  AND indexdef LIKE '%' || kcu.column_name || '%'
);
```

### Step 4: Query Optimization Patterns

```javascript
// BEFORE: Slow query
const { data } = await supabase
  .from('users')
  .select('*')
  .limit(100);

// AFTER: Optimized query
const { data } = await supabase
  .from('users')
  .select('id, name, email')  // Specific columns
  .order('created_at', { ascending: false })
  .limit(100);
```

## Workflow 4: Subscription Debugging

When realtime messages are not delivering:

### Step 1: Verify Realtime Status

```javascript
// Check subscription state
const channel = supabase.channel('test');
channel.on('system', {}, (payload) => {
  console.log('System event:', payload);
}).subscribe((status) => {
  console.log('Subscription status:', status);
});
```

### Step 2: Test Channel Connectivity

```javascript
// Simple broadcast test
const channel = supabase.channel('test-channel');

channel
  .on('broadcast', { event: 'test' }, (payload) => {
    console.log('Received:', payload);
  })
  .subscribe(async (status) => {
    if (status === 'SUBSCRIBED') {
      await channel.send({
        type: 'broadcast',
        event: 'test',
        payload: { message: 'hello', timestamp: Date.now() }
      });
    }
  });
```

### Step 3: Check Database Triggers

```sql
-- Verify realtime is enabled on table
SELECT * FROM pg_publication_tables
WHERE pubname = 'supabase_realtime';

-- Enable realtime for a table
ALTER PUBLICATION supabase_realtime ADD TABLE your_table;
```

### Step 4: Common Realtime Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No messages | Table not in publication | Add to supabase_realtime publication |
| Dropped messages | Payload > 1MB | Reduce payload size with select() |
| Stale connection | No heartbeat | Implement reconnection logic |
| Filter not working | Syntax error | Use `eq.` prefix: `filter: 'id=eq.123'` |

## Workflow 5: Memory Investigation

When memory usage grows without cleanup:

### Step 1: Track Memory Delta

```javascript
// Browser memory tracking
const initialMemory = performance.memory?.usedJSHeapSize || 0;
setInterval(() => {
  const currentMemory = performance.memory?.usedJSHeapSize || 0;
  const delta = currentMemory - initialMemory;
  console.log(`Memory delta: ${(delta / 1024 / 1024).toFixed(2)} MB`);
}, 5000);
```

### Step 2: Audit Subscriptions

```javascript
// List all active channels
const channels = supabase.getChannels();
console.log('Active channels:', channels.length);
channels.forEach(ch => {
  console.log(`- ${ch.topic}: ${ch.state}`);
});
```

### Step 3: Proper Cleanup Pattern

```javascript
// React/Vue cleanup pattern
useEffect(() => {
  const channel = supabase
    .channel('my-channel')
    .on('postgres_changes',
      { event: '*', schema: 'public', table: 'tasks' },
      handleChange
    )
    .subscribe();

  // CRITICAL: Cleanup on unmount
  return () => {
    supabase.removeChannel(channel);
  };
}, []);
```

### Step 4: Database Connection Cleanup

```javascript
// Implement connection pooling
const supabase = createClient(url, key, {
  db: {
    schema: 'public',
  },
  realtime: {
    params: {
      eventsPerSecond: 10,  // Rate limit
    },
  },
});
```

## Workflow 6: RLS Policy Validation

When encountering permission denied errors:

### Step 1: Check Current Policies

```sql
-- View all policies on a table
SELECT
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
FROM pg_policies
WHERE tablename = 'your_table';
```

### Step 2: Test Policy as User

```sql
-- Temporarily switch to user role and test
SET ROLE authenticated;
SET request.jwt.claim.sub = 'user-uuid-here';

SELECT * FROM your_table;  -- Test SELECT
INSERT INTO your_table (col) VALUES ('test');  -- Test INSERT

RESET ROLE;
```

### Step 3: Common RLS Patterns

```sql
-- Users can only see their own data
CREATE POLICY "Users see own data"
ON tasks FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own data
CREATE POLICY "Users create own data"
ON tasks FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own data
CREATE POLICY "Users update own data"
ON tasks FOR UPDATE
USING (auth.uid() = user_id)
WITH CHECK (auth.uid() = user_id);
```

### Step 4: Debug Silent RLS Failures

```javascript
// Check if operation succeeded
const { data, error, count } = await supabase
  .from('tasks')
  .insert({ title: 'Test' })
  .select()
  .single();

if (error) {
  console.error('Insert error:', error);
} else if (!data) {
  console.warn('RLS may have silently blocked the operation');
} else {
  console.log('Success:', data);
}
```

## Workflow 7: Production Readiness Check

Pre-deployment validation checklist:

### Step 1: Database Health

```sql
-- Check for missing indexes
SELECT
  relname as table,
  seq_scan,
  idx_scan,
  n_tup_ins + n_tup_upd + n_tup_del as writes
FROM pg_stat_user_tables
WHERE seq_scan > idx_scan * 10
AND seq_scan > 1000;

-- Check table sizes
SELECT
  relname as table,
  pg_size_pretty(pg_total_relation_size(relid)) as size
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC;
```

### Step 2: RLS Coverage

```sql
-- Check all tables have RLS enabled
SELECT
  schemaname,
  tablename,
  rowsecurity
FROM pg_tables
WHERE schemaname = 'public';

-- Verify each table has policies
SELECT
  t.tablename,
  COUNT(p.policyname) as policy_count
FROM pg_tables t
LEFT JOIN pg_policies p ON t.tablename = p.tablename
WHERE t.schemaname = 'public'
GROUP BY t.tablename
HAVING COUNT(p.policyname) = 0;
```

### Step 3: Performance Baseline

```sql
-- Capture slow query baseline
SELECT
  query,
  calls,
  mean_time,
  max_time
FROM pg_stat_statements
WHERE mean_time > 100
ORDER BY mean_time DESC
LIMIT 10;
```

### Step 4: Deployment Checklist

- [ ] All migrations tested locally
- [ ] RLS policies on all public tables
- [ ] Indexes on frequently queried columns
- [ ] No hardcoded credentials
- [ ] Connection pooling configured
- [ ] Error handling implemented
- [ ] Subscription cleanup verified
- [ ] Rate limiting configured

## Workflow 8: localStorage Fallback Audit

When deleted data reappears after page refresh, or Supabase data conflicts with cached data:

### Step 1: Identify All localStorage Keys

```bash
# Scan codebase for all localStorage usage
grep -roh "localStorage\.\(get\|set\|remove\)Item(['\"][^'\"]*['\"]" src/ \
  --include="*.ts" --include="*.vue" | \
  sed "s/localStorage\.\(get\|set\|remove\)Item(['\"]//g" | \
  sed "s/['\"]//g" | sort -u
```

### Step 2: Check for Dangerous Fallback Patterns

**DANGER PATTERN**: Loading from localStorage when Supabase returns empty

```typescript
// ❌ BAD: Resurrects deleted data
const loadedGroups = await fetchGroups()  // Returns [] (all deleted)
if (loadedGroups.length === 0) {
  const localGroups = loadFromLocalStorage()  // Has OLD deleted groups!
  _rawGroups.value = localGroups  // RESURRECTS DELETED DATA
}

// ✅ GOOD: Supabase is source of truth
const loadedGroups = await fetchGroups()
_rawGroups.value = loadedGroups  // Empty means empty
```

### Step 3: FlowState localStorage Inventory

| Key | File | Risk Level | Notes |
|-----|------|------------|-------|
| `flowstate-guest-groups` | canvas.ts | **FIXED** | Was resurrecting deleted groups |
| `flow-state-golden-backup` | useBackupSystem.ts | **HIGH** | Never expires, can restore old data |
| `flowstate-offline-queue` | offlineQueue.ts | **MEDIUM** | No TTL, infinite retry |
| `flow-state-resolution-rules` | userResolutionRules.ts | **MEDIUM** | Could affect conflict resolution |
| `canvas-viewport` | canvas.ts | **MEDIUM** | Loaded before Supabase ready |
| `flow-state-filters` | taskPersistence.ts | **MEDIUM** | Stale filters show wrong view |
| `flow-state-backup-history` | useBackupSystem.ts | **MEDIUM** | Old backups persist indefinitely |
| `flowstate-canvas-locks` | canvasStateLock.ts | **LOW** | Has 7s TTL |
| `flowstate-canvas-has-initial-fit` | canvasUi.ts | **LOW** | Has 5min TTL |

### Step 4: Audit Checklist

For each localStorage key that stores user data:

- [ ] **Source of Truth**: Is Supabase the authoritative source for authenticated users?
- [ ] **Fallback Behavior**: Does empty from Supabase mean empty locally?
- [ ] **TTL/Expiration**: Does cached data expire?
- [ ] **Version/Schema**: Is there schema validation on load?
- [ ] **Guest Mode Cleanup**: Is key in `GUEST_EPHEMERAL_KEYS` list?

### Step 5: Common Fixes

| Issue | Symptom | Fix |
|-------|---------|-----|
| Deleted data reappears | Groups/tasks come back after refresh | Remove localStorage fallback for authenticated users |
| Stale viewport | Canvas position wrong after login | Defer viewport load until after Supabase fetch |
| Old backup restores deleted items | Restore brings back items user deleted | Add timestamp/version to backups, validate on restore |
| Offline queue replays old ops | Operations re-applied on reconnect | Add TTL to queued operations, validate target exists |

### Step 6: Verify Fix

```javascript
// In browser console after fix:
// 1. Create some groups
// 2. Delete all groups
// 3. Refresh page
// 4. Check groups are still gone:
console.log('Groups after refresh:',
  JSON.parse(localStorage.getItem('flowstate-guest-groups') || '[]').length,
  'local,',
  // Check Pinia store
  useCanvasStore().groups.length,
  'in store'
);
```

### Step 7: Prevention Pattern

```typescript
// src/stores/canvas.ts - CORRECT PATTERN
const loadFromDatabase = async () => {
  const authStore = useAuthStore()

  // Guest mode: start empty (ephemeral)
  if (!authStore.isAuthenticated) {
    _rawGroups.value = []
    return
  }

  // Authenticated: Supabase is SINGLE source of truth
  const loadedGroups = await fetchGroups()
  _rawGroups.value = loadedGroups  // Empty = empty, no fallback!

  // Log for debugging
  if (loadedGroups.length === 0) {
    console.log('📭 [SUPABASE] No groups (all deleted or none created)')
  }
}
```

## Workflow 9: Production API Debugging (Cloudflare + Caddy)

When Supabase API works locally but fails in production behind Cloudflare and Caddy:

### Step 1: Identify the Issue Layer

| Works | Fails | Likely Layer |
|-------|-------|--------------|
| curl to API | Browser | CORS or Cloudflare cache |
| Firefox | Chrome | Cloudflare + preload scanner |
| Local | Production | Caddy or Cloudflare config |
| REST | Realtime | WebSocket proxy config |

### Step 2: Test Each Layer

```bash
# 1. Test Cloudflare → Origin (bypass CF cache)
curl -sI --resolve "api.example.com:443:YOUR_VPS_IP" \
  "https://api.example.com/rest/v1/tasks" \
  -H "apikey: YOUR_ANON_KEY"

# 2. Test via Cloudflare
curl -sI "https://api.example.com/rest/v1/tasks" \
  -H "apikey: YOUR_ANON_KEY" | grep -iE "cf-cache|content-type"

# 3. Test CORS preflight
curl -X OPTIONS "https://api.example.com/rest/v1/tasks" \
  -H "Origin: https://example.com" \
  -H "Access-Control-Request-Method: GET" \
  -I

# 4. Test WebSocket upgrade
curl -sI "https://api.example.com/realtime/v1/websocket" \
  -H "Upgrade: websocket" \
  -H "Connection: Upgrade"
```

### Step 3: Common Production Issues

| Issue | Symptom | Fix |
|-------|---------|-----|
| CORS blocked | Browser console shows CORS error | Add `Access-Control-Allow-*` headers in Caddy |
| WebSocket fails | Realtime subscriptions don't work | Add `header_up Upgrade/Connection` in Caddy |
| 403 on OPTIONS | Preflight rejected | Add OPTIONS handler before proxy |
| MIME type error | Cloudflare serves wrong content | Add `Vary: Accept` header (see SOP-032) |
| 502 Bad Gateway | Upstream not responding | Check Kong/Supabase containers |

### Step 4: Correct Caddy API Configuration

```caddyfile
api.example.com {
    tls /etc/caddy/certs/cloudflare-origin.pem /etc/caddy/certs/cloudflare-origin.key

    # Handle CORS preflight FIRST
    @options method OPTIONS
    handle @options {
        header Access-Control-Allow-Origin "*"
        header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, PATCH, OPTIONS"
        header Access-Control-Allow-Headers "*"
        header Access-Control-Expose-Headers "*"
        header Access-Control-Max-Age "86400"
        respond 204
    }

    # Proxy to Supabase Kong
    handle {
        reverse_proxy localhost:8000 {
            # Required headers
            header_up X-Forwarded-Proto https
            header_up X-Forwarded-Host api.example.com

            # WebSocket support
            header_up Upgrade {http.request.header.Upgrade}
            header_up Connection {http.request.header.Connection}
        }

        # CORS headers on responses
        header Access-Control-Allow-Origin "*"
        header Access-Control-Expose-Headers "*"
    }
}
```

### Step 5: Verify Production Auth Flow

```bash
# 1. Get auth token (login)
curl -X POST "https://api.example.com/auth/v1/token?grant_type=password" \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password"}'

# 2. Test authenticated request
curl "https://api.example.com/rest/v1/tasks" \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 3. Check JWT claims
echo "YOUR_ACCESS_TOKEN" | cut -d'.' -f2 | base64 -d 2>/dev/null | jq
```

### Step 6: Debug Realtime in Production

```javascript
// Browser console debug for production realtime
const supabase = createClient('https://api.example.com', 'YOUR_ANON_KEY');

// Enable debug logging
supabase.realtime.setAuth(yourAccessToken);

const channel = supabase
  .channel('debug-channel')
  .on('system', {}, (payload) => {
    console.log('🔌 System event:', payload);
  })
  .on('postgres_changes',
    { event: '*', schema: 'public', table: 'tasks' },
    (payload) => console.log('📬 DB change:', payload)
  )
  .subscribe((status, err) => {
    console.log('📡 Status:', status, err);
  });
```

### Step 7: Production Checklist

- [ ] Caddy handles OPTIONS preflight before proxy
- [ ] WebSocket upgrade headers passed through
- [ ] CORS headers include all required Supabase headers
- [ ] Cloudflare SSL mode is "Full" (not "Flexible")
- [ ] Origin cert is valid and not expired
- [ ] `Vary: Accept` on asset routes (prevents MIME issues)
- [ ] index.html has `no-cache` (prevents stale HTML)

**Related SOPs**:
- `SOP-026-custom-domain-deployment.md` - Full VPS setup
- `SOP-031-cors-configuration.md` - CORS headers
- `SOP-032-cloudflare-cache-mime-prevention.md` - MIME type prevention

---

## Quick Reference Commands

### Database Analysis

```sql
-- Table row counts
SELECT schemaname, relname, n_live_tup
FROM pg_stat_user_tables
ORDER BY n_live_tup DESC;

-- Index usage
SELECT indexrelname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes;

-- Active locks
SELECT * FROM pg_locks WHERE granted = false;

-- Current connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;
```

### Realtime Debugging

```javascript
// Monitor all database changes
supabase
  .channel('db-changes')
  .on('postgres_changes',
    { event: '*', schema: 'public' },
    (payload) => console.log('Change:', payload)
  )
  .subscribe();
```

### Auth Debugging

```javascript
// Get current session
const { data: { session } } = await supabase.auth.getSession();
console.log('Current user:', session?.user);
console.log('Token expires:', new Date(session?.expires_at * 1000));
```

## Troubleshooting Reference

| Error | Cause | Solution |
|-------|-------|----------|
| `PGRST301` | JWT expired | Refresh token before expiration |
| `42501` | RLS violation | Check policy with `pg_policies` |
| `42703` | Column not found | Verify schema matches code |
| `23505` | Unique violation | Handle duplicate key errors |
| `23503` | Foreign key violation | Ensure referenced row exists |
| `57P03` | Cannot connect | Check Supabase is running |
| `REALTIME_SUBSCRIBE_ERROR` | Invalid channel | Check channel name format |

## Resources

For detailed reference documentation, see:
- `references/commands.md` - Complete command reference
- `references/workflows.md` - Extended debugging workflows
- `references/schema-validation.md` - Schema validation queries
- `scripts/check-connection.sh` - Connection diagnostic script
- `scripts/analyze-queries.sql` - Query analysis queries
