---
name: Session Checker
description: Check if Interstellio/NebularStack client sessions are active. Analyzes CDR records to determine connection status, session history, and terminate causes.
version: 1.0.0
dependencies: lib/interstellio/client.ts
---

# Session Checker

A skill for checking if CircleTel customer PPPoE/RADIUS sessions are active using the Interstellio (NebularStack) Telemetry API. Analyzes CDR (Call Detail Records) to determine real-time connection status.

## When This Skill Activates

This skill automatically activates when you:
- Need to check if a customer's internet session is active
- Want to view session history for a subscriber
- Debug connection issues or troubleshoot "not connected" complaints
- Analyze session patterns and terminate causes
- Check PPPoE connection status

**Keywords**: session active, session status, connection status, PPPoE session, check session, CDR records, subscriber online, is connected, client session, terminate cause

## Core Concepts

### Session States

| State | terminate_cause | Meaning |
|-------|-----------------|---------|
| **Active** | `null` | Session is currently connected |
| **Disconnected** | `Lost-Carrier` | Connection lost (modem/router issue) |
| **User Ended** | `User-Request` | User initiated disconnect |
| **Idle Timeout** | `Idle-Timeout` | Session timed out due to inactivity |
| **Session Timeout** | `Session-Timeout` | Max session duration reached |
| **Admin Disconnect** | `Admin-Reset` | Administratively disconnected |
| **Port Error** | `Port-Error` | NAS/BNG port issue |
| **NAS Error** | `NAS-Error` | Network access server error |

### CDR Record Fields

| Field | Description |
|-------|-------------|
| `id` | Unique session identifier |
| `start_time` | When session started (ISO 8601) |
| `update_time` | Last accounting update |
| `username` | PPPoE username (e.g., `customer@circletel.co.za`) |
| `calling_station_id` | Customer's IP address assigned by BRAS |
| `called_station_id` | BRAS/BNG IP address |
| `nas_ip_address` | NAS that authenticated the session |
| `duration` | Session duration in seconds |
| `terminate_cause` | Why session ended (null if active) |

## Quick Check Methods

### Method 1: Using the Interstellio Client (Programmatic)

```typescript
import { getInterstellioClient } from '@/lib/interstellio'

// Set token first (get from Interstellio dashboard or auth)
const client = getInterstellioClient()
client.setToken(process.env.INTERSTELLIO_API_TOKEN!, 'circletel.co.za')

// Quick check - just returns true/false
const isActive = await client.isSessionActive('subscriber-uuid-here')
console.log('Session active:', isActive)

// Detailed analysis
const analysis = await client.analyzeSessionStatus('subscriber-uuid-here')
console.log('Analysis:', {
  isActive: analysis.isActive,
  lastSession: analysis.lastSession?.username,
  sessionsToday: analysis.totalSessionsToday,
  terminateCauses: analysis.terminateCauses
})

// Get raw CDR records for custom analysis
const records = await client.getCDRRecords('subscriber-uuid', {
  start_time: '2025-12-19T00:00:00+02:00',
  end_time: '2025-12-19T23:59:59+02:00'
})
```

### Method 2: Using PowerShell (Quick CLI Check)

```powershell
# Run the session checker script
powershell -File .claude/skills/session-checker/check-session.ps1 -SubscriberId "23ffee86-dbe9-11f0-9102-61ef2f83e8d9"
```

### Method 3: Direct API Call (cURL/PowerShell)

```powershell
$headers = @{
    "X-Auth-Token" = $env:INTERSTELLIO_API_TOKEN
    "X-Tenant-ID" = "circletel.co.za"
    "X-Domain" = "circletel.co.za"
    "X-Timezone" = "Africa/Johannesburg"
    "Content-Type" = "application/json"
}

$body = @{
    start_time = (Get-Date).Date.ToString("yyyy-MM-ddT00:00:00+02:00")
    end_time = (Get-Date).ToString("yyyy-MM-ddTHH:mm:ss+02:00")
} | ConvertTo-Json

$response = Invoke-RestMethod `
    -Uri "https://telemetry-za.nebularstack.com/v1/subscriber/{subscriber_id}/cdr/records" `
    -Method POST `
    -Headers $headers `
    -Body $body

# Check if session is active
if ($response.terminate_cause -eq $null) {
    Write-Host "Session is ACTIVE" -ForegroundColor Green
    Write-Host "Username: $($response.username)"
    Write-Host "Connected since: $($response.start_time)"
    Write-Host "Duration: $([math]::Round($response.duration / 60, 1)) minutes"
} else {
    Write-Host "Session is DISCONNECTED" -ForegroundColor Red
    Write-Host "Last terminate cause: $($response.terminate_cause)"
}
```

## Finding Subscriber IDs

### From Supabase (CircleTel Database)

```sql
-- Find subscriber by customer email
SELECT
    cs.interstellio_subscriber_id,
    cs.radius_username,
    c.email,
    c.first_name,
    c.last_name
FROM customer_services cs
JOIN customers c ON cs.customer_id = c.id
WHERE c.email = 'customer@example.com';

-- Find subscriber by account number
SELECT
    cs.interstellio_subscriber_id,
    cs.radius_username,
    cs.status
FROM customer_services cs
JOIN customers c ON cs.customer_id = c.id
WHERE c.account_number = 'CT-2025-00001';
```

### From Interstellio API

```typescript
// Search by username
const subscribers = await client.listSubscribers({
  username: 'customer@circletel.co.za'
})
const subscriberId = subscribers.payload[0]?.id
```

## Common Troubleshooting Scenarios

### Scenario 1: Customer Reports "No Internet"

1. **Check session status**:
   ```typescript
   const analysis = await client.analyzeSessionStatus(subscriberId)
   ```

2. **Interpret results**:
   - `isActive: true` → Session is up, issue is elsewhere (DNS, routing, etc.)
   - `isActive: false` with `Lost-Carrier` → Customer's router lost connection
   - `isActive: false` with `Session-Timeout` → Session expired, needs reconnect

3. **Check session history** for patterns:
   ```typescript
   // Multiple Lost-Carrier in short time = unstable line
   if (analysis.terminateCauses['Lost-Carrier'] > 5) {
     console.log('Line appears unstable - recommend technician check')
   }
   ```

### Scenario 2: Checking Before Service Activation

```typescript
// Ensure no orphaned sessions before provisioning
const existingSessions = await client.listSessions(subscriberId)
if (existingSessions.payload.length > 0) {
  // Disconnect existing sessions first
  await client.disconnectAllSessions(subscriberId)
}
```

### Scenario 3: Usage Monitoring Dashboard

```typescript
// Get today's session stats for dashboard
const analysis = await client.analyzeSessionStatus(subscriberId)

const dashboardData = {
  connectionStatus: analysis.isActive ? 'Online' : 'Offline',
  currentSessionDuration: analysis.lastSession?.duration || 0,
  reconnectsToday: analysis.terminateCauses['Lost-Carrier'] || 0,
  totalOnlineTime: analysis.totalDurationSeconds
}
```

## API Reference

### Endpoint

```
POST https://telemetry-za.nebularstack.com/v1/subscriber/{subscriber_id}/cdr/records
```

### Required Headers

| Header | Value |
|--------|-------|
| `X-Auth-Token` | JWT from Interstellio identity service |
| `X-Tenant-ID` | `circletel.co.za` |
| `X-Domain` | `circletel.co.za` |
| `X-Timezone` | `Africa/Johannesburg` |
| `Content-Type` | `application/json` |

### Request Body

```json
{
  "start_time": "2025-12-19T00:00:00+02:00",
  "end_time": "2025-12-19T23:59:59+02:00"
}
```

**Note**: Maximum query window is 32 days.

### Response Example

```json
{
  "id": "4d81f126-dcd1-11f0-9e13-a59eec990c99::2025-12-01",
  "start_time": "2025-12-19T13:53:15.000+02:00",
  "update_time": "2025-12-19T14:20:50.132+02:00",
  "acct_unique_id": "4d81f126-dcd1-11f0-9e13-a59eec990c99",
  "username": "customer@circletel.co.za",
  "calling_station_id": "100.125.57.136",
  "called_station_id": "100.127.1.229",
  "nas_ip_address": "41.198.130.3",
  "client_ip_address": "13.247.40.35",
  "duration": 1655,
  "terminate_cause": "Lost-Carrier"
}
```

## Environment Variables Required

```env
INTERSTELLIO_API_TOKEN=your_jwt_token_here
INTERSTELLIO_TENANT_ID=circletel.co.za
INTERSTELLIO_DOMAIN=circletel.co.za
```

## Related Files

| File | Purpose |
|------|---------|
| `lib/interstellio/client.ts` | Interstellio API client |
| `lib/interstellio/types.ts` | TypeScript types including CDR records |
| `docs/api/INTERSTELLIO_API.md` | Full API documentation |
| `.claude/skills/session-checker/check-session.ps1` | PowerShell quick-check script |

## Best Practices

1. **Always check session status before disconnecting** - Don't blindly disconnect active sessions
2. **Use timezone-aware dates** - Always include `+02:00` for South Africa
3. **Handle empty results** - API may return empty if no sessions in time window
4. **Cache tokens** - Interstellio tokens are valid for 12 months
5. **Monitor terminate causes** - High `Lost-Carrier` counts indicate line issues

---

**Version**: 1.0.0
**Last Updated**: 2025-12-20
**Maintained By**: CircleTel Development Team
**API Source**: https://docs.interstellio.io/
