---
name: supabase-audit-realtime
description: Test Supabase Realtime WebSocket channels for unauthorized subscriptions and data exposure.
---

# Realtime Channel Audit

> 🔴 **CRITICAL: PROGRESSIVE FILE UPDATES REQUIRED**
>
> You MUST write to context files **AS YOU GO**, not just at the end.
> - Write to `.sb-pentest-context.json` **IMMEDIATELY after each channel tested**
> - Log to `.sb-pentest-audit.log` **BEFORE and AFTER each subscription test**
> - **DO NOT** wait until the skill completes to update files
> - If the skill crashes or is interrupted, all prior findings must already be saved
>
> **This is not optional. Failure to write progressively is a critical error.**

This skill tests Supabase Realtime WebSocket channels for security issues.

## When to Use This Skill

- To check if Realtime channels are properly secured
- To detect unauthorized data streaming
- When Realtime is used for sensitive data
- As part of comprehensive security audit

## Prerequisites

- Supabase URL and anon key available
- Detection completed

## Understanding Supabase Realtime

Supabase Realtime enables:

```
wss://[project].supabase.co/realtime/v1/websocket
```

| Feature | Description |
|---------|-------------|
| Postgres Changes | Stream database changes |
| Broadcast | Pub/sub messaging |
| Presence | User presence tracking |

## Security Model

Realtime respects RLS policies:
- ✅ If RLS blocks SELECT, Realtime won't stream
- ❌ If RLS allows SELECT, Realtime streams data
- ⚠️ Broadcast channels can be subscribed without RLS

## Tests Performed

| Test | Purpose |
|------|---------|
| Channel enumeration | Find open channels |
| Postgres Changes | Test table streaming |
| Broadcast | Test pub/sub access |
| Presence | Test presence channel access |

## Usage

### Basic Realtime Audit

```
Audit Realtime channels on my Supabase project
```

### Test Specific Feature

```
Test if Postgres Changes streams sensitive data
```

## Output Format

```
═══════════════════════════════════════════════════════════
 REALTIME CHANNEL AUDIT
═══════════════════════════════════════════════════════════

 Project: abc123def.supabase.co
 Endpoint: wss://abc123def.supabase.co/realtime/v1/websocket

 ─────────────────────────────────────────────────────────
 Connection Test
 ─────────────────────────────────────────────────────────

 WebSocket Connection: ✅ Established
 Authentication: Anon key accepted
 Protocol: Phoenix channels

 ─────────────────────────────────────────────────────────
 Postgres Changes Test
 ─────────────────────────────────────────────────────────

 Subscribing to table changes with anon key...

 Table: users
 ├── Subscribe: ✅ Subscribed
 ├── INSERT events: 🔴 P0 - RECEIVING ALL NEW USERS
 ├── UPDATE events: 🔴 P0 - RECEIVING ALL UPDATES
 └── DELETE events: 🔴 P0 - RECEIVING ALL DELETES

 Sample Event Received:
 ```json
 {
   "type": "INSERT",
   "table": "users",
   "record": {
     "id": "550e8400-e29b-...",
     "email": "newuser@example.com",  ← PII STREAMING!
     "name": "New User",
     "created_at": "2025-01-31T10:00:00Z"
   }
 }
 ```

 Finding: 🔴 P0 - User data streaming without authentication!
          RLS may not be properly configured for Realtime.

 Table: orders
 ├── Subscribe: ✅ Subscribed
 ├── INSERT events: ❌ Not receiving (RLS working)
 ├── UPDATE events: ❌ Not receiving (RLS working)
 └── DELETE events: ❌ Not receiving (RLS working)

 Assessment: ✅ Orders table properly protected.

 Table: posts
 ├── Subscribe: ✅ Subscribed
 ├── INSERT events: ✅ Receiving published only
 ├── UPDATE events: ✅ Receiving published only
 └── DELETE events: ✅ Receiving published only

 Assessment: ✅ Posts streaming respects RLS (published only).

 ─────────────────────────────────────────────────────────
 Broadcast Channel Test
 ─────────────────────────────────────────────────────────

 Attempting to subscribe to common channel names...

 Channel: room:lobby
 ├── Subscribe: ✅ Success
 ├── Messages: Receiving broadcasts
 └── Assessment: ℹ️ Open channel (may be intentional)

 Channel: admin
 ├── Subscribe: ✅ Success ← Should this be public?
 ├── Messages: Receiving admin notifications
 └── Assessment: 🟠 P1 - Admin channel publicly accessible

 Channel: notifications
 ├── Subscribe: ✅ Success
 ├── Messages: Receiving user notifications for ALL users!
 └── Assessment: 🔴 P0 - User notifications exposed

 Sample Notification:
 ```json
 {
   "user_id": "123...",
   "type": "payment_received",
   "amount": 150.00,
   "from": "customer@example.com"
 }
 ```

 ─────────────────────────────────────────────────────────
 Presence Test
 ─────────────────────────────────────────────────────────

 Channel: online-users
 ├── Subscribe: ✅ Success
 ├── Presence List: Receiving all online users
 └── Users Online: 47

 Sample Presence Data:
 ```json
 {
   "user_id": "550e8400-...",
   "email": "user@example.com",
   "status": "online",
   "last_seen": "2025-01-31T14:00:00Z"
 }
 ```

 Assessment: 🟠 P1 - User presence data exposed
             Consider if email/user_id should be visible.

 ─────────────────────────────────────────────────────────
 Summary
 ─────────────────────────────────────────────────────────

 Postgres Changes:
 ├── 🔴 P0: users table streaming all data
 ├── ✅ PASS: orders table protected by RLS
 └── ✅ PASS: posts table correctly filtered

 Broadcast:
 ├── 🔴 P0: notifications channel exposing user data
 ├── 🟠 P1: admin channel publicly accessible
 └── ℹ️ INFO: lobby channel open (review if intended)

 Presence:
 └── 🟠 P1: online-users exposing user details

 Critical Findings: 2
 High Findings: 2

 ═══════════════════════════════════════════════════════════
 Recommendations
 ═══════════════════════════════════════════════════════════

 1. FIX USERS TABLE RLS
    Ensure RLS applies to Realtime:
    ```sql
    ALTER TABLE users ENABLE ROW LEVEL SECURITY;

    CREATE POLICY "Users see only themselves"
      ON users FOR SELECT
      USING (auth.uid() = id);
    ```

 2. SECURE BROADCAST CHANNELS
    Use Realtime Authorization:
    ```javascript
    // Require auth for sensitive channels
    const channel = supabase.channel('admin', {
      config: {
        broadcast: { ack: true },
        presence: { key: userId }
      }
    })

    // Server-side: validate channel access
    // Use RLS on realtime.channels table
    ```

 3. LIMIT PRESENCE DATA
    Only share necessary information:
    ```javascript
    channel.track({
      online_at: new Date().toISOString()
      // Don't include email, user_id unless needed
    })
    ```

═══════════════════════════════════════════════════════════
```

## Realtime Security Model

### Postgres Changes + RLS

```sql
-- This RLS policy applies to Realtime too
CREATE POLICY "Users see own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

-- With this policy:
-- - API SELECT: Only own data
-- - Realtime: Only own data changes
```

### Broadcast Security

```sql
-- Realtime authorization (Supabase extension)
-- Add policies to realtime.channels virtual table

-- Only authenticated users can join
CREATE POLICY "Authenticated users join channels"
  ON realtime.channels FOR SELECT
  USING (auth.role() = 'authenticated');

-- Or restrict specific channels
CREATE POLICY "Admin channel for admins"
  ON realtime.channels FOR SELECT
  USING (
    name != 'admin' OR
    (SELECT is_admin FROM profiles WHERE id = auth.uid())
  );
```

## Context Output

```json
{
  "realtime_audit": {
    "timestamp": "2025-01-31T14:00:00Z",
    "connection": "established",
    "postgres_changes": {
      "users": {
        "subscribed": true,
        "receiving_events": true,
        "severity": "P0",
        "finding": "All user data streaming without RLS"
      },
      "orders": {
        "subscribed": true,
        "receiving_events": false,
        "severity": null,
        "finding": "Properly protected by RLS"
      }
    },
    "broadcast": {
      "notifications": {
        "accessible": true,
        "severity": "P0",
        "finding": "User notifications exposed"
      },
      "admin": {
        "accessible": true,
        "severity": "P1",
        "finding": "Admin channel publicly accessible"
      }
    },
    "presence": {
      "online-users": {
        "accessible": true,
        "severity": "P1",
        "users_visible": 47,
        "finding": "User presence data exposed"
      }
    }
  }
}
```

## Common Realtime Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| All data streaming | RLS not enabled/configured | Enable and configure RLS |
| Broadcast open | No channel authorization | Add channel policies |
| Presence exposed | Too much data tracked | Minimize tracked data |

## Remediation Examples

### Secure Table Streaming

```sql
-- Ensure RLS is enabled
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy for authenticated users only
CREATE POLICY "Users see own profile" ON users
  FOR SELECT
  USING (auth.uid() = id);

-- Realtime will now only stream changes for the authenticated user's row
```

### Secure Broadcast Channels

```javascript
// Client: Check access before subscribing
const { data: canAccess } = await supabase
  .from('channel_access')
  .select('*')
  .eq('channel', 'admin')
  .eq('user_id', userId)
  .single();

if (canAccess) {
  const channel = supabase.channel('admin');
  channel.subscribe();
}
```

### Minimal Presence Data

```javascript
// Before (too much data)
channel.track({
  user_id: userId,
  email: email,
  name: fullName,
  avatar: avatarUrl
});

// After (minimal data)
channel.track({
  online_at: new Date().toISOString()
  // User details fetched separately if needed
});
```

## MANDATORY: Progressive Context File Updates

⚠️ **This skill MUST update tracking files PROGRESSIVELY during execution, NOT just at the end.**

### Critical Rule: Write As You Go

**DO NOT** batch all writes at the end. Instead:

1. **Before testing each channel** → Log the action to `.sb-pentest-audit.log`
2. **After each data exposure found** → Immediately update `.sb-pentest-context.json`
3. **After each subscription test** → Log the result immediately

This ensures that if the skill is interrupted, crashes, or times out, all findings up to that point are preserved.

### Required Actions (Progressive)

1. **Update `.sb-pentest-context.json`** with results:
   ```json
   {
     "realtime_audit": {
       "timestamp": "...",
       "connection": "established",
       "postgres_changes": { ... },
       "broadcast": { ... },
       "presence": { ... }
     }
   }
   ```

2. **Log to `.sb-pentest-audit.log`**:
   ```
   [TIMESTAMP] [supabase-audit-realtime] [START] Auditing Realtime channels
   [TIMESTAMP] [supabase-audit-realtime] [FINDING] P0: users table streaming all data
   [TIMESTAMP] [supabase-audit-realtime] [CONTEXT_UPDATED] .sb-pentest-context.json updated
   ```

3. **If files don't exist**, create them before writing.

**FAILURE TO UPDATE CONTEXT FILES IS NOT ACCEPTABLE.**

## MANDATORY: Evidence Collection

📁 **Evidence Directory:** `.sb-pentest-evidence/06-realtime-audit/`

### Evidence Files to Create

| File | Content |
|------|---------|
| `websocket-connection.json` | WebSocket connection test |
| `postgres-changes/[table].json` | Table subscription results |
| `broadcast-channels/[channel].json` | Broadcast channel access |
| `presence-data/[channel].json` | Presence data exposure |

### Evidence Format

```json
{
  "evidence_id": "RT-001",
  "timestamp": "2025-01-31T11:05:00Z",
  "category": "realtime-audit",
  "type": "postgres_changes",
  "severity": "P0",

  "table": "users",

  "subscription_test": {
    "channel": "realtime:public:users",
    "subscribed": true,
    "events_received": true
  },

  "sample_event": {
    "type": "INSERT",
    "table": "users",
    "record": {
      "id": "[REDACTED]",
      "email": "[REDACTED]@example.com",
      "name": "[REDACTED]"
    },
    "redacted": true
  },

  "impact": {
    "pii_streaming": true,
    "affected_columns": ["email", "name"],
    "rls_bypass": true
  },

  "websocket_url": "wss://abc123def.supabase.co/realtime/v1/websocket",

  "reproduction_code": "const channel = supabase.channel('realtime:public:users').on('postgres_changes', { event: '*', schema: 'public', table: 'users' }, (payload) => console.log(payload)).subscribe()"
}
```

## Related Skills

- `supabase-audit-rls` — RLS affects Realtime
- `supabase-audit-tables-read` — API access is related
- `supabase-report` — Include in final report
