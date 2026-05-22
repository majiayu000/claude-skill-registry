---
name: advertising-performance
description: Generic multi-channel advertising performance analysis patterns for Google Ads and Meta Ads. Use when monitoring CAC, ROAS, spend, and conversions across platforms. Framework for project-specific implementations.
---

# Advertising Performance Framework

Generic patterns for multi-channel advertising performance monitoring and optimization.

## When to Use

- Monitor daily ad spend and conversions
- Calculate CAC (Customer Acquisition Cost) and ROAS (Return on Ad Spend)
- Compare performance across Google Ads and Meta Ads
- Generate performance alerts when metrics exceed thresholds
- Track campaign effectiveness over time

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project (e.g., `/landing/.claude/skills/google-ads-performance`)
- Reference this framework with `extends: "marketing-intelligence-framework/advertising-performance"`
- Add project-specific thresholds via skill.config.json

## Core Concepts

### Key Metrics

| Metric | Formula | Good Target | Critical Threshold |
|--------|---------|-------------|-------------------|
| **CAC** | Spend ÷ Conversions | Platform-specific | 2x target |
| **ROAS** | Revenue ÷ Spend | 3x+ for most businesses | <2x needs review |
| **CTR** | Clicks ÷ Impressions | 2-5% | <1% poor |
| **CPC** | Spend ÷ Clicks | Industry-specific | Trending up = issue |

### Performance Analysis Workflow

```
1. Fetch daily performance → Google Ads + Meta Ads APIs
2. Normalize currency → Convert all to CHF/USD/EUR
3. Calculate metrics → CAC, ROAS, blended performance
4. Check thresholds → Compare against targets
5. Generate alerts → CRITICAL/WARNING/INFO levels
6. Take action → Pause campaigns, adjust budgets, optimize
```

## Implementation Patterns

### 1. Setup Multi-Platform Tracking

```typescript
import {
  MARKETING_THRESHOLDS,
  calculateCAC,
  calculateROAS,
  analyzePlatformPerformance,
  type PlatformPerformance
} from '@/app/lib/marketing';

// Define platform-specific thresholds
const thresholds = {
  google_ads: {
    cac: { target: 15.0, warning: 18.0, critical: 20.0 },
    roas: { target: 3.0, minimum: 2.0 }
  },
  meta_ads: {
    cac: { target: 5.0, warning: 8.0, critical: 12.0 },
    roas: { target: 8.0, minimum: 5.0 }
  }
};
```

### 2. Fetch Platform Performance

```typescript
// Google Ads example
async function fetchGoogleAdsPerformance(date: string): Promise<PlatformPerformance> {
  const client = new GoogleAdsClient({
    customer_id: process.env.GOOGLE_ADS_CUSTOMER_ID!
  });

  const response = await client.query(`
    SELECT
      metrics.cost_micros,
      metrics.conversions,
      metrics.clicks,
      metrics.impressions
    FROM campaign
    WHERE segments.date = '${date}'
  `);

  const spend = response.cost_micros / 1_000_000;
  const conversions = response.conversions;

  return {
    date,
    spend_chf: spend,
    conversions,
    cac: calculateCAC(spend, conversions),
    roas: 0, // Calculate if revenue data available
    clicks: response.clicks,
    impressions: response.impressions
  };
}

// Meta Ads example
async function fetchMetaAdsPerformance(date: string): Promise<PlatformPerformance> {
  const api = FacebookAdsApi.init(process.env.FACEBOOK_ACCESS_TOKEN!);
  const account = new AdAccount(process.env.FACEBOOK_AD_ACCOUNT_ID!);

  const insights = await account.getInsights([
    'spend',
    'actions',
    'clicks',
    'impressions'
  ], {
    time_range: { since: date, until: date }
  });

  const spend = parseFloat(insights[0].spend);
  const conversions = insights[0].actions?.find(a => a.action_type === 'purchase')?.value || 0;

  return {
    date,
    spend_chf: spend,
    conversions: parseInt(conversions),
    cac: calculateCAC(spend, parseInt(conversions)),
    roas: 0,
    clicks: parseInt(insights[0].clicks),
    impressions: parseInt(insights[0].impressions)
  };
}
```

### 3. Analyze Performance and Generate Alerts

```typescript
import {
  analyzePlatformPerformance,
  analyzeBlendedPerformance,
  formatAlert,
  type DailyPerformance
} from '@/app/lib/marketing';

async function analyzeDaily(date: string) {
  // Fetch from both platforms
  const [googlePerf, metaPerf] = await Promise.all([
    fetchGoogleAdsPerformance(date),
    fetchMetaAdsPerformance(date)
  ]);

  // Analyze each platform
  const googleAlerts = analyzePlatformPerformance(googlePerf, 'google_ads');
  const metaAlerts = analyzePlatformPerformance(metaPerf, 'meta_ads');

  // Analyze blended performance
  const dailyPerf: DailyPerformance = {
    date,
    google_ads: googlePerf,
    meta_ads: metaPerf
  };
  const blendedAlerts = analyzeBlendedPerformance(dailyPerf);

  // Combine all alerts
  const allAlerts = [...googleAlerts, ...metaAlerts, ...blendedAlerts];

  // Display alerts
  allAlerts.forEach(alert => console.log(formatAlert(alert)));

  return allAlerts;
}
```

### 4. Handle Division by Zero

```typescript
// CRITICAL: Always handle zero conversions
function calculateCAC(spend: number, conversions: number): number {
  return conversions > 0 ? spend / conversions : 0; // Return 0, not Infinity
}

function calculateROAS(revenue: number, spend: number): number {
  return spend > 0 ? revenue / spend : 0;
}
```

### 5. Currency Normalization

```typescript
import { convertToCHF } from '@/app/lib/marketing';

// Meta Ads returns USD, normalize to CHF
const spendCHF = convertToCHF(usdSpend, 'USD');

// Google Ads in micros, convert and normalize
const spendCHF = convertToCHF(costMicros / 1_000_000, 'USD');
```

## Reusability Patterns

### Framework Level (90% reusable)
```typescript
// Generic pattern works for ANY advertising platform
export function analyzePlatformPerformance(
  performance: PlatformPerformance,
  platform: 'google_ads' | 'meta_ads'
): PerformanceAlert[] {
  // Applies to any business tracking CAC/ROAS
}
```

### Implementation Level (project-specific)
```typescript
// MyArmy-specific thresholds
const MYARMY_THRESHOLDS = {
  meta_ads: { cac: { target: 3.81 } }, // Based on historical data
  google_ads: { cac: { target: 16.7 } }
};
```

## Alert Handling

### Alert Levels

| Level | Emoji | Action Required | Example |
|-------|-------|-----------------|---------|
| **CRITICAL** | 🚨 | Immediate action | CAC > critical threshold - pause campaigns |
| **WARNING** | ⚠️ | Review needed | CAC > warning threshold - optimize targeting |
| **INFO** | ℹ️ | Informational | CAC approaching target |
| **SUCCESS** | ✅ | No action | CAC below target |

### Automated Actions

```typescript
async function handleCriticalAlert(alert: PerformanceAlert) {
  if (alert.level === 'CRITICAL' && alert.metric === 'CAC') {
    // Pause campaigns immediately
    await pauseCampaigns(alert.platform);

    // Send Slack alert
    await sendSlackAlert({
      level: 'CRITICAL',
      message: alert.message,
      action: alert.action
    });

    // Log for audit trail
    await logAlert(alert);
  }
}
```

## Common Pitfalls

❌ **Division by Zero**: Always check `conversions > 0` before calculating CAC
❌ **Currency Mismatch**: Always normalize to single currency (CHF/USD/EUR)
❌ **Stale Data**: Check data freshness before analysis
❌ **Missing Revenue**: ROAS calculation requires revenue tracking
❌ **Hardcoded Thresholds**: Use centralized config, not hardcoded values

## Related Frameworks

- **budget-optimization**: Budget allocation between platforms
- **health-monitoring**: System health and data freshness checks
- **analytics-framework/gsc-optimization**: SEO performance tracking

## Example Project Implementation

See `/landing/.claude/skills/google-ads-performance/` for MyArmy-specific implementation using this framework.
