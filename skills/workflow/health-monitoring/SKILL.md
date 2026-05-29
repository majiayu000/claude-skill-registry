---
name: health-monitoring
description: Generic health check and data freshness monitoring patterns for marketing intelligence systems. Use when validating connectivity to data sources, checking data staleness, or ensuring system reliability. Framework for project-specific implementations.
---

# Health Monitoring Framework

Generic patterns for system health checks, connectivity validation, and data freshness monitoring across marketing data sources.

## When to Use

- Validate connectivity to all marketing data sources
- Check data freshness (when was data last updated?)
- Monitor system health before critical operations
- Alert when data becomes stale
- Verify API credentials and permissions
- Detect silent failures in data pipelines

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project (e.g., `/landing/.claude/skills/marketing-health-check`)
- Reference this framework with `extends: "marketing-intelligence-framework/health-monitoring"`
- Add project-specific data sources and freshness thresholds

## Core Concepts

### Health Check Workflow

```
1. Test connectivity → Can we reach each system?
2. Validate credentials → Are API keys/tokens valid?
3. Fetch recent data → Get latest records
4. Check freshness → Compare timestamp to threshold
5. Aggregate status → Overall system health
6. Report results → Display summary or alert
```

### Health Status Levels

| Status | Meaning | Action |
|--------|---------|--------|
| **healthy** | All systems operational | No action needed |
| **degraded** | Some systems have issues | Monitor closely |
| **critical** | Major system failures | Immediate attention |

### Data Freshness Thresholds

| Data Source | Acceptable Lag | Critical Lag |
|-------------|----------------|--------------|
| **Real-time (Supabase leads)** | < 1 hour | > 24 hours |
| **Daily batch (orders)** | < 24 hours | > 48 hours |
| **Advertising APIs** | < 24 hours | > 48 hours |
| **Analytics (GSC, GTM)** | < 24 hours | > 72 hours |

## Implementation Patterns

### 1. Health Check Result Structure

```typescript
interface HealthCheckResult {
  timestamp: string;
  systems: {
    [systemName: string]: {
      status: 'connected' | 'failed' | 'degraded';
      error?: string;
      metadata?: Record<string, unknown>;
    };
  };
  dataFreshness: {
    [dataSource: string]: {
      lastUpdated: string;
      ageHours: number;
      isStale: boolean;
    };
  };
  overallStatus: 'healthy' | 'degraded' | 'critical';
}
```

### 2. Check Database Connectivity

```typescript
async function checkSupabase(): Promise<{
  status: 'connected' | 'failed';
  metadata?: any;
  error?: string;
}> {
  try {
    const supabase = createClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.SUPABASE_SERVICE_ROLE_KEY!
    );

    // Test connection by fetching 1 record
    const { data, error } = await supabase
      .from('leads')
      .select('id, created_at')
      .limit(1);

    if (error) {
      return {
        status: 'failed',
        error: error.message
      };
    }

    return {
      status: 'connected',
      metadata: {
        recordCount: data?.length || 0,
        latestRecord: data?.[0]?.created_at
      }
    };
  } catch (error) {
    return {
      status: 'failed',
      error: (error as Error).message
    };
  }
}
```

### 3. Check API Connectivity (Airtable example)

```typescript
import Airtable from 'airtable';

async function checkAirtable(): Promise<{
  status: 'connected' | 'failed';
  metadata?: any;
  error?: string;
}> {
  try {
    const apiKey = process.env.AIRTABLE_API_KEY;
    const baseId = process.env.AIRTABLE_BASE_ID;

    if (!apiKey || !baseId) {
      return {
        status: 'failed',
        error: 'Missing AIRTABLE_API_KEY or AIRTABLE_BASE_ID'
      };
    }

    const base = new Airtable({ apiKey }).base(baseId);

    // Test connection
    const records = await base('Orders')
      .select({ maxRecords: 1 })
      .firstPage();

    return {
      status: 'connected',
      metadata: {
        baseId,
        testRecordId: records[0]?.id
      }
    };
  } catch (error) {
    return {
      status: 'failed',
      error: (error as Error).message
    };
  }
}
```

### 4. Check Data Freshness

```typescript
function checkDataFreshness(
  lastUpdated: string,
  thresholdHours: number
): {
  lastUpdated: string;
  ageHours: number;
  isStale: boolean;
} {
  const now = new Date();
  const updated = new Date(lastUpdated);
  const ageMs = now.getTime() - updated.getTime();
  const ageHours = ageMs / (1000 * 60 * 60);

  return {
    lastUpdated,
    ageHours: Math.round(ageHours * 10) / 10,
    isStale: ageHours > thresholdHours
  };
}

// Example usage
async function checkLeadDataFreshness() {
  const supabase = createClient(/* ... */);

  const { data } = await supabase
    .from('leads')
    .select('created_at')
    .order('created_at', { ascending: false })
    .limit(1);

  if (!data || data.length === 0) {
    return { isStale: true, ageHours: Infinity };
  }

  return checkDataFreshness(data[0].created_at, 1); // 1 hour threshold
}
```

### 5. Comprehensive Health Check

```typescript
async function performHealthCheck(): Promise<HealthCheckResult> {
  const result: HealthCheckResult = {
    timestamp: new Date().toISOString(),
    systems: {},
    dataFreshness: {},
    overallStatus: 'healthy'
  };

  // Check all systems in parallel
  const [supabaseHealth, airtableHealth, googleAdsHealth, metaAdsHealth] = await Promise.all([
    checkSupabase(),
    checkAirtable(),
    checkGoogleAds(),
    checkMetaAds()
  ]);

  result.systems.supabase = supabaseHealth;
  result.systems.airtable = airtableHealth;
  result.systems.google_ads = googleAdsHealth;
  result.systems.meta_ads = metaAdsHealth;

  // Check data freshness
  const [leadsFreshness, ordersFreshness, adSpendFreshness] = await Promise.all([
    checkLeadDataFreshness(),
    checkOrderDataFreshness(),
    checkAdSpendDataFreshness()
  ]);

  result.dataFreshness.leads = leadsFreshness;
  result.dataFreshness.orders = ordersFreshness;
  result.dataFreshness.ad_spend = adSpendFreshness;

  // Determine overall status
  const failedSystems = Object.values(result.systems).filter(s => s.status === 'failed').length;
  const staleData = Object.values(result.dataFreshness).filter(d => d.isStale).length;

  if (failedSystems > 0 || staleData > 1) {
    result.overallStatus = 'critical';
  } else if (failedSystems > 0 || staleData > 0) {
    result.overallStatus = 'degraded';
  }

  return result;
}
```

### 6. Health Check Display

```typescript
function displayHealthCheck(result: HealthCheckResult): void {
  console.log('🟣 System Health Check\n');
  console.log('═'.repeat(60));
  console.log(`Timestamp: ${result.timestamp}`);
  console.log(`Overall Status: ${getStatusEmoji(result.overallStatus)} ${result.overallStatus.toUpperCase()}\n`);

  // Display system connectivity
  console.log('📡 System Connectivity:');
  Object.entries(result.systems).forEach(([name, health]) => {
    const emoji = health.status === 'connected' ? '✅' : '❌';
    console.log(`  ${emoji} ${name}: ${health.status}`);
    if (health.error) {
      console.log(`     Error: ${health.error}`);
    }
  });

  // Display data freshness
  console.log('\n🕐 Data Freshness:');
  Object.entries(result.dataFreshness).forEach(([source, freshness]) => {
    const emoji = freshness.isStale ? '⚠️' : '✅';
    console.log(`  ${emoji} ${source}: ${freshness.ageHours}h ago ${freshness.isStale ? '(STALE)' : ''}`);
  });

  console.log('═'.repeat(60));
}

function getStatusEmoji(status: string): string {
  switch (status) {
    case 'healthy': return '✅';
    case 'degraded': return '⚠️';
    case 'critical': return '🚨';
    default: return 'ℹ️';
  }
}
```

### 7. Automated Health Monitoring

```typescript
// Run health checks on schedule
async function scheduledHealthCheck() {
  const result = await performHealthCheck();

  // Alert on critical status
  if (result.overallStatus === 'critical') {
    await sendSlackAlert({
      level: 'CRITICAL',
      message: 'System health check failed',
      details: result
    });
  }

  // Log for historical tracking
  await logHealthCheck(result);

  return result;
}

// Store health check results for trend analysis
async function logHealthCheck(result: HealthCheckResult): Promise<void> {
  const supabase = createClient(/* ... */);

  await supabase.from('health_check_logs').insert({
    timestamp: result.timestamp,
    overall_status: result.overallStatus,
    systems_status: result.systems,
    data_freshness: result.dataFreshness
  });
}
```

## Reusability Patterns

### Framework Level (75% reusable)
```typescript
// Generic health check pattern works for any data source
export async function checkDataSource(
  fetchFn: () => Promise<any>,
  sourceName: string
): Promise<{ status: 'connected' | 'failed'; error?: string }> {
  try {
    await fetchFn();
    return { status: 'connected' };
  } catch (error) {
    return { status: 'failed', error: (error as Error).message };
  }
}
```

### Implementation Level (project-specific)
```typescript
// MyArmy-specific data sources and thresholds
const DATA_SOURCES = {
  supabase_leads: { threshold: 1 },  // 1 hour
  airtable_orders: { threshold: 24 }, // 24 hours
  google_ads: { threshold: 24 },
  meta_ads: { threshold: 24 }
};
```

## Alert Triggers

### When to Alert

✅ **DO alert when:**
- Any system fails connectivity test
- Data is stale beyond critical threshold
- Overall status becomes 'critical'
- Multiple degraded systems simultaneously

❌ **DON'T alert when:**
- Known maintenance windows
- Temporary API rate limits (retry first)
- Single data source slightly stale (< critical threshold)

## Common Pitfalls

❌ **Timeout Issues**: Always set reasonable timeouts for API calls
❌ **Rate Limiting**: Space out health checks to avoid hitting API limits
❌ **False Positives**: Account for timezone differences in timestamps
❌ **Missing Error Handling**: Always catch and log errors
❌ **Noisy Alerts**: Don't alert on temporary transient failures

## Related Frameworks

- **advertising-performance**: Requires healthy data sources for accurate analysis
- **budget-optimization**: Depends on fresh data for budget decisions

## Example Project Implementation

See `/landing/.claude/skills/marketing-health-check/` for MyArmy-specific implementation using this framework.
