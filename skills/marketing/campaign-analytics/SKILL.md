---
name: campaign-analytics
description: Generic marketing campaign performance analysis patterns. Use when tracking ad spend, calculating ROI, optimizing budgets, or analyzing multi-channel performance. Framework for project-specific implementations.
---

# Campaign Analytics Framework

Generic patterns for marketing campaign analysis and optimization across any platform.

## When to Use

- Tracking advertising spend and performance
- Calculating ROI, ROAS, CAC metrics
- Multi-channel attribution analysis
- Budget allocation optimization
- Campaign performance reporting

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project
- Reference this framework with `extends: "marketing-intelligence-framework/campaign-analytics"`
- Add platform-specific credentials via skill.config.json

## Core Concepts

### Key Metrics

| Metric | Formula | Good Target |
|--------|---------|-------------|
| **ROAS** | Revenue ÷ Ad Spend | >3.0 |
| **CAC** | Ad Spend ÷ New Customers | < LTV/3 |
| **CPC** | Ad Spend ÷ Clicks | Varies by industry |
| **CTR** | Clicks ÷ Impressions | >2% |
| **Conversion Rate** | Conversions ÷ Clicks | >3% |
| **LTV** | Avg Order Value × Repeat Rate × Lifespan | 3× CAC |

### Multi-Channel Attribution

```
Customer Journey:
Google Ads → Website Visit → Remarketing (Facebook) → WhatsApp Contact → Sale

Attribution Models:
- Last Click: Facebook gets 100% credit
- First Click: Google Ads gets 100% credit
- Linear: Each touchpoint gets 25% credit
- Time Decay: Recent touchpoints weighted higher
- Position-Based: First and last get 40% each, middle gets 20%
```

## Implementation Patterns

### 1. Data Collection Structure

```typescript
// Generic campaign data structure
export interface CampaignData {
  platform: 'google_ads' | 'facebook_ads' | 'instagram_ads' | 'linkedin_ads' | string;
  campaign_id: string;
  campaign_name: string;
  date: string; // YYYY-MM-DD
  metrics: {
    impressions: number;
    clicks: number;
    spend: number; // in your currency
    conversions: number;
    revenue: number;
  };
  metadata?: {
    campaign_type?: string;
    targeting?: any;
    creative_id?: string;
  };
}

// Aggregated metrics
export interface AggregatedMetrics extends CampaignData {
  calculated: {
    ctr: number;          // clicks / impressions
    cpc: number;          // spend / clicks
    cpa: number;          // spend / conversions
    roas: number;         // revenue / spend
    conversion_rate: number; // conversions / clicks
  };
}
```

### 2. Google Ads Integration

```typescript
import { GoogleAdsApi } from 'google-ads-api';

export class GoogleAdsAnalytics {
  private client: GoogleAdsApi;

  constructor(
    customerId: string,
    developerToken: string,
    keyFile: string
  ) {
    this.client = new GoogleAdsApi({
      client_id: process.env.GOOGLE_ADS_CLIENT_ID!,
      client_secret: process.env.GOOGLE_ADS_CLIENT_SECRET!,
      developer_token: developerToken
    });
  }

  async getCampaignPerformance(
    startDate: string,
    endDate: string
  ): Promise<CampaignData[]> {
    const customer = this.client.Customer({
      customer_id: this.customerId,
      refresh_token: process.env.GOOGLE_ADS_REFRESH_TOKEN!
    });

    const campaigns = await customer.query(`
      SELECT
        campaign.id,
        campaign.name,
        segments.date,
        metrics.impressions,
        metrics.clicks,
        metrics.cost_micros,
        metrics.conversions,
        metrics.conversions_value
      FROM campaign
      WHERE segments.date BETWEEN '${startDate}' AND '${endDate}'
        AND campaign.status = 'ENABLED'
      ORDER BY segments.date DESC
    `);

    return campaigns.map(c => ({
      platform: 'google_ads',
      campaign_id: c.campaign.id,
      campaign_name: c.campaign.name,
      date: c.segments.date,
      metrics: {
        impressions: c.metrics.impressions,
        clicks: c.metrics.clicks,
        spend: c.metrics.cost_micros / 1_000_000, // Convert micros to currency
        conversions: c.metrics.conversions,
        revenue: c.metrics.conversions_value || 0
      }
    }));
  }

  async pauseLowPerformingCampaigns(roasThreshold: number = 1.0): Promise<void> {
    // Get recent performance
    const campaigns = await this.getCampaignPerformance(
      getDateDaysAgo(30),
      getDateToday()
    );

    // Calculate ROAS per campaign
    const aggregated = aggregateByCampaign(campaigns);

    for (const [campaignId, data] of Object.entries(aggregated)) {
      const roas = data.revenue / data.spend;

      if (roas < roasThreshold && data.spend > 100) {
        console.log(`Pausing campaign ${campaignId} (ROAS: ${roas.toFixed(2)})`);
        await this.pauseCampaign(campaignId);
      }
    }
  }
}
```

### 3. Facebook/Meta Ads Integration

```typescript
import { FacebookAdsApi } from 'facebook-nodejs-business-sdk';

export class MetaAdsAnalytics {
  private api: FacebookAdsApi;

  constructor(accessToken: string) {
    this.api = FacebookAdsApi.init(accessToken);
  }

  async getCampaignPerformance(
    adAccountId: string,
    startDate: string,
    endDate: string
  ): Promise<CampaignData[]> {
    const account = new AdAccount(`act_${adAccountId}`);

    const campaigns = await account.getCampaigns([
      'id',
      'name',
      'insights.time_range({"since":"' + startDate + '","until":"' + endDate + '"}).fields(impressions,clicks,spend,actions,action_values)'
    ]);

    return campaigns.map(campaign => {
      const insights = campaign.insights?.data?.[0];
      const conversions = this.extractConversions(insights?.actions);
      const revenue = this.extractRevenue(insights?.action_values);

      return {
        platform: 'facebook_ads',
        campaign_id: campaign.id,
        campaign_name: campaign.name,
        date: startDate, // Aggregate date range
        metrics: {
          impressions: parseInt(insights?.impressions || '0'),
          clicks: parseInt(insights?.clicks || '0'),
          spend: parseFloat(insights?.spend || '0'),
          conversions,
          revenue
        }
      };
    });
  }

  private extractConversions(actions: any[]): number {
    const leadActions = actions?.find(a =>
      a.action_type === 'lead' ||
      a.action_type === 'purchase' ||
      a.action_type === 'complete_registration'
    );
    return parseInt(leadActions?.value || '0');
  }

  private extractRevenue(actionValues: any[]): number {
    const purchaseValue = actionValues?.find(a =>
      a.action_type === 'purchase' ||
      a.action_type === 'omni_purchase'
    );
    return parseFloat(purchaseValue?.value || '0');
  }
}
```

### 4. Multi-Channel Aggregation

```typescript
export class MultiChannelAnalytics {
  constructor(
    private googleAds: GoogleAdsAnalytics,
    private metaAds: MetaAdsAnalytics
  ) {}

  async getConsolidatedPerformance(
    startDate: string,
    endDate: string
  ): Promise<Record<string, AggregatedMetrics>> {
    // Fetch from all platforms
    const [googleData, metaData] = await Promise.all([
      this.googleAds.getCampaignPerformance(startDate, endDate),
      this.metaAds.getCampaignPerformance(metaAccountId, startDate, endDate)
    ]);

    // Combine all data
    const allData = [...googleData, ...metaData];

    // Aggregate by platform
    const byPlatform: Record<string, AggregatedMetrics> = {};

    allData.forEach(campaign => {
      if (!byPlatform[campaign.platform]) {
        byPlatform[campaign.platform] = {
          platform: campaign.platform,
          campaign_id: 'all',
          campaign_name: 'All Campaigns',
          date: `${startDate}_${endDate}`,
          metrics: {
            impressions: 0,
            clicks: 0,
            spend: 0,
            conversions: 0,
            revenue: 0
          },
          calculated: {
            ctr: 0,
            cpc: 0,
            cpa: 0,
            roas: 0,
            conversion_rate: 0
          }
        };
      }

      const platform = byPlatform[campaign.platform];
      platform.metrics.impressions += campaign.metrics.impressions;
      platform.metrics.clicks += campaign.metrics.clicks;
      platform.metrics.spend += campaign.metrics.spend;
      platform.metrics.conversions += campaign.metrics.conversions;
      platform.metrics.revenue += campaign.metrics.revenue;
    });

    // Calculate derived metrics
    Object.values(byPlatform).forEach(platform => {
      const m = platform.metrics;
      platform.calculated = {
        ctr: (m.clicks / m.impressions) * 100,
        cpc: m.spend / m.clicks,
        cpa: m.spend / m.conversions,
        roas: m.revenue / m.spend,
        conversion_rate: (m.conversions / m.clicks) * 100
      };
    });

    return byPlatform;
  }

  async generateReport(startDate: string, endDate: string): Promise<string> {
    const data = await this.getConsolidatedPerformance(startDate, endDate);

    let report = `# Marketing Performance Report\n`;
    report += `Period: ${startDate} to ${endDate}\n\n`;

    Object.entries(data).forEach(([platform, metrics]) => {
      report += `## ${platform.toUpperCase()}\n`;
      report += `- Spend: $${metrics.metrics.spend.toFixed(2)}\n`;
      report += `- Revenue: $${metrics.metrics.revenue.toFixed(2)}\n`;
      report += `- ROAS: ${metrics.calculated.roas.toFixed(2)}x\n`;
      report += `- Conversions: ${metrics.metrics.conversions}\n`;
      report += `- CPA: $${metrics.calculated.cpa.toFixed(2)}\n`;
      report += `- CTR: ${metrics.calculated.ctr.toFixed(2)}%\n\n`;
    });

    // Overall summary
    const totalSpend = Object.values(data).reduce((sum, m) => sum + m.metrics.spend, 0);
    const totalRevenue = Object.values(data).reduce((sum, m) => sum + m.metrics.revenue, 0);
    const overallROAS = totalRevenue / totalSpend;

    report += `## OVERALL\n`;
    report += `- Total Spend: $${totalSpend.toFixed(2)}\n`;
    report += `- Total Revenue: $${totalRevenue.toFixed(2)}\n`;
    report += `- Overall ROAS: ${overallROAS.toFixed(2)}x\n`;

    return report;
  }
}
```

## Budget Optimization Patterns

### Dynamic Budget Allocation

```typescript
interface BudgetAllocation {
  platform: string;
  current_budget: number;
  recommended_budget: number;
  reason: string;
}

export async function optimizeBudgetAllocation(
  totalBudget: number,
  historicalData: AggregatedMetrics[]
): Promise<BudgetAllocation[]> {
  // Calculate ROAS efficiency by platform
  const platformROAS = historicalData.map(p => ({
    platform: p.platform,
    roas: p.calculated.roas,
    spend: p.metrics.spend
  }));

  // Sort by ROAS
  platformROAS.sort((a, b) => b.roas - a.roas);

  // Allocate budget proportionally to ROAS
  const totalROAS = platformROAS.reduce((sum, p) => sum + p.roas, 0);

  return platformROAS.map(p => ({
    platform: p.platform,
    current_budget: p.spend,
    recommended_budget: (p.roas / totalROAS) * totalBudget,
    reason: `ROAS: ${p.roas.toFixed(2)}x - ${p.roas > 3 ? 'High performer' : 'Underperformer'}`
  }));
}

// Example usage
const allocations = await optimizeBudgetAllocation(10000, historicalData);
/*
[
  {
    platform: 'google_ads',
    current_budget: 6000,
    recommended_budget: 7500, // Increase (high ROAS)
    reason: 'ROAS: 4.2x - High performer'
  },
  {
    platform: 'facebook_ads',
    current_budget: 4000,
    recommended_budget: 2500, // Decrease (low ROAS)
    reason: 'ROAS: 1.8x - Underperformer'
  }
]
*/
```

### Automated Campaign Scaling

```typescript
export async function autoScaleCampaigns(
  analytics: MultiChannelAnalytics,
  scalingRules: {
    highPerformer: { roasThreshold: number; increasePercent: number };
    lowPerformer: { roasThreshold: number; decreasePercent: number };
  }
): Promise<void> {
  const data = await analytics.getConsolidatedPerformance(
    getDateDaysAgo(7),
    getDateToday()
  );

  for (const [platform, metrics] of Object.entries(data)) {
    const roas = metrics.calculated.roas;
    const currentBudget = metrics.metrics.spend / 7; // Daily budget

    if (roas >= scalingRules.highPerformer.roasThreshold) {
      // Scale up
      const newBudget = currentBudget * (1 + scalingRules.highPerformer.increasePercent / 100);
      console.log(`Scaling up ${platform}: $${currentBudget} → $${newBudget} (ROAS: ${roas.toFixed(2)})`);
      await updateCampaignBudget(platform, newBudget);
    } else if (roas <= scalingRules.lowPerformer.roasThreshold) {
      // Scale down
      const newBudget = currentBudget * (1 - scalingRules.lowPerformer.decreasePercent / 100);
      console.log(`Scaling down ${platform}: $${currentBudget} → $${newBudget} (ROAS: ${roas.toFixed(2)})`);
      await updateCampaignBudget(platform, newBudget);
    }
  }
}
```

## Configuration Requirements

**Environment Variables:**
- `GOOGLE_ADS_CUSTOMER_ID` - Google Ads account ID
- `GOOGLE_ADS_DEVELOPER_TOKEN` - Developer token
- `GOOGLE_ADS_CLIENT_ID` - OAuth client ID
- `GOOGLE_ADS_CLIENT_SECRET` - OAuth client secret
- `GOOGLE_ADS_REFRESH_TOKEN` - OAuth refresh token
- `META_ADS_ACCESS_TOKEN` - Facebook/Meta access token
- `META_ADS_ACCOUNT_ID` - Ad account ID

**API Access:**
- Google Ads API enabled
- Meta Marketing API enabled
- Service accounts configured

**Configuration** (skill.config.json):
```json
{
  "configuration": {
    "platforms": {
      "google_ads": {
        "customer_id": "${GOOGLE_ADS_CUSTOMER_ID}",
        "conversion_labels": {
          "lead": "${GOOGLE_ADS_CONVERSION_LABEL_LEAD}",
          "purchase": "${GOOGLE_ADS_CONVERSION_LABEL_PURCHASE}"
        }
      },
      "meta_ads": {
        "account_id": "${META_ADS_ACCOUNT_ID}",
        "pixel_id": "${META_PIXEL_ID}"
      }
    },
    "targets": {
      "min_roas": 2.0,
      "max_cac": 100,
      "target_conversion_rate": 3.0
    }
  }
}
```

## Key Rules

### DO:
- Track all ad spend centrally
- Calculate ROAS at campaign and platform level
- Monitor trends weekly minimum
- Test budget reallocations gradually
- Document significant changes
- Use 30-day windows for performance evaluation

### DON'T:
- Make budget decisions on <7 days data
- Ignore seasonal patterns
- Scale campaigns >50% at once
- Forget to track offline conversions
- Mix currency conversions incorrectly
- Skip attribution analysis

## Resources

- **Google Ads API**: https://developers.google.com/google-ads/api
- **Meta Marketing API**: https://developers.facebook.com/docs/marketing-apis
- **@akson/cortex-analytics**: Unified analytics CLI

## Example Implementations

See project-specific skills that extend this framework:
- `myarmy-skills/campaign-analytics-myarmy` - Swiss market ad performance
- Your implementation here!
