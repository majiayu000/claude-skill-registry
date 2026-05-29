---
name: lokalise-cost-tuning
description: |
  Optimize Lokalise costs through plan selection, usage monitoring, and efficiency.
  Use when analyzing Lokalise billing, reducing costs,
  or implementing usage monitoring and budget alerts.
  Trigger with phrases like "lokalise cost", "lokalise billing",
  "reduce lokalise costs", "lokalise pricing", "lokalise budget".
allowed-tools: Read, Grep
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Lokalise Cost Tuning

## Overview
Optimize Lokalise costs through smart plan selection, usage monitoring, and efficient workflows.

## Prerequisites
- Access to Lokalise billing dashboard
- Understanding of current usage patterns
- Database for usage tracking (optional)
- Alerting system configured (optional)

## Lokalise Pricing Overview

### Plans (2025)
| Plan | Price | Included | Best For |
|------|-------|----------|----------|
| Free | $0 | 1 project, 500 keys | Personal/testing |
| Essential | $120/mo | Unlimited projects, 2K keys/project | Small teams |
| Pro | $400/mo | Unlimited keys, OTA, Figma | Growing teams |
| Enterprise | Custom | SSO, dedicated support, SLA | Large organizations |

### Key Cost Factors
- Number of translation keys
- Number of target languages
- Machine translation usage
- Professional translation orders
- OTA bandwidth (mobile apps)

## Instructions

### Step 1: Analyze Current Usage
```typescript
import { LokaliseApi } from "@lokalise/node-api";

async function analyzeUsage(): Promise<UsageReport> {
  const client = new LokaliseApi({
    apiKey: process.env.LOKALISE_API_TOKEN!,
  });

  const projects = await client.projects().list();
  const usage: UsageReport = {
    totalProjects: projects.items.length,
    totalKeys: 0,
    totalLanguages: 0,
    projectDetails: [],
  };

  for (const project of projects.items) {
    const stats = project.statistics;

    usage.totalKeys += stats.keys_total;
    usage.totalLanguages += stats.languages;

    usage.projectDetails.push({
      name: project.name,
      projectId: project.project_id,
      keys: stats.keys_total,
      languages: stats.languages,
      baseWords: stats.base_words,
      progress: stats.progress_total,
    });
  }

  return usage;
}

interface UsageReport {
  totalProjects: number;
  totalKeys: number;
  totalLanguages: number;
  projectDetails: Array<{
    name: string;
    projectId: string;
    keys: number;
    languages: number;
    baseWords: number;
    progress: number;
  }>;
}
```

### Step 2: Identify Cost Optimization Opportunities
```typescript
function analyzeOptimizations(usage: UsageReport): Recommendation[] {
  const recommendations: Recommendation[] = [];

  // Check for unused projects
  for (const project of usage.projectDetails) {
    if (project.keys < 10) {
      recommendations.push({
        type: "unused_project",
        severity: "low",
        message: `Project "${project.name}" has only ${project.keys} keys. Consider archiving.`,
        potentialSavings: "Reduce clutter, potential plan downgrade",
      });
    }

    // Check for duplicate/similar keys
    if (project.keys > 1000) {
      recommendations.push({
        type: "key_audit",
        severity: "medium",
        message: `Project "${project.name}" has ${project.keys} keys. Review for duplicates.`,
        potentialSavings: "5-15% key reduction typical",
      });
    }

    // Check for low-progress languages
    if (project.progress < 50 && project.languages > 3) {
      recommendations.push({
        type: "unused_languages",
        severity: "medium",
        message: `Project "${project.name}" has ${project.languages} languages at ${project.progress}% progress.`,
        potentialSavings: "Remove unused target languages",
      });
    }
  }

  // Plan recommendation
  if (usage.totalKeys < 2000 && usage.totalProjects <= 3) {
    recommendations.push({
      type: "plan_downgrade",
      severity: "high",
      message: "Current usage fits Essential plan",
      potentialSavings: "Potential $280/mo savings vs Pro",
    });
  }

  return recommendations;
}
```

### Step 3: Implement Usage Monitoring
```typescript
interface UsageMetrics {
  date: Date;
  keysCreated: number;
  keysDeleted: number;
  translationsUpdated: number;
  mtCharacters: number;  // Machine translation
  apiCalls: number;
}

class LokaliseUsageMonitor {
  private metrics: UsageMetrics[] = [];

  trackApiCall(operation: string, details?: any) {
    // Track API usage
    console.log({
      timestamp: new Date().toISOString(),
      operation,
      details,
    });
  }

  async getMonthlyReport(): Promise<MonthlyReport> {
    const client = new LokaliseApi({
      apiKey: process.env.LOKALISE_API_TOKEN!,
    });

    const projects = await client.projects().list();

    let totalKeys = 0;
    let totalMTCharacters = 0;

    for (const project of projects.items) {
      totalKeys += project.statistics.keys_total;
      // Note: MT usage requires checking orders/billing API
    }

    return {
      month: new Date().toISOString().slice(0, 7),
      totalKeys,
      estimatedCost: this.estimateCost(totalKeys),
    };
  }

  private estimateCost(keys: number): number {
    // Simplified estimation based on plan tiers
    if (keys <= 500) return 0;  // Free tier
    if (keys <= 2000) return 120;  // Essential
    return 400;  // Pro
  }
}
```

### Step 4: Clean Up Unused Resources
```typescript
async function cleanupUnusedKeys(projectId: string, dryRun = true) {
  const client = new LokaliseApi({
    apiKey: process.env.LOKALISE_API_TOKEN!,
  });

  // Find archived keys
  const archivedKeys = await client.keys().list({
    project_id: projectId,
    filter_archived: "include",
    limit: 500,
  });

  const toDelete = archivedKeys.items.filter(k => k.is_archived);
  console.log(`Found ${toDelete.length} archived keys`);

  if (dryRun) {
    console.log("DRY RUN - would delete:", toDelete.map(k => k.key_name.web));
    return { deleted: 0, archived: toDelete.length };
  }

  // Actually delete
  for (const key of toDelete) {
    await client.keys().delete(key.key_id, { project_id: projectId });
  }

  return { deleted: toDelete.length };
}

async function removeUnusedLanguages(projectId: string, threshold = 10) {
  const client = new LokaliseApi({
    apiKey: process.env.LOKALISE_API_TOKEN!,
  });

  const languages = await client.languages().list({ project_id: projectId });

  const unused = languages.items.filter(
    lang => (lang.statistics?.progress ?? 0) < threshold && !lang.is_default
  );

  console.log(`Languages below ${threshold}% progress:`,
    unused.map(l => `${l.lang_name} (${l.statistics?.progress}%)`));

  // Don't auto-delete - just report
  return unused;
}
```

## Output
- Usage analysis complete
- Cost optimization recommendations
- Usage monitoring implemented
- Cleanup scripts for unused resources

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Unexpected charges | Untracked MT usage | Monitor orders API |
| Key limit exceeded | Organic growth | Archive or delete unused |
| Overage fees | Wrong plan | Upgrade before hitting limits |
| Budget exceeded | No monitoring | Set up usage alerts |

## Examples

### Quick Usage Check
```typescript
const report = await analyzeUsage();
console.log(`Total Projects: ${report.totalProjects}`);
console.log(`Total Keys: ${report.totalKeys}`);
console.log(`Estimated Plan: ${report.totalKeys < 500 ? 'Free' : report.totalKeys < 2000 ? 'Essential' : 'Pro'}`);
```

### Machine Translation Cost Estimate
```typescript
// Lokalise MT pricing varies by provider and language pair
function estimateMTCost(
  characters: number,
  provider: "google" | "deepl" | "amazon" = "google"
): number {
  const rates: Record<string, number> = {
    google: 0.02,  // $20 per million characters
    deepl: 0.025,  // $25 per million characters
    amazon: 0.015, // $15 per million characters
  };

  return (characters / 1_000_000) * rates[provider];
}
```

### Budget Alert Script
```typescript
async function checkBudget(budgetKeys: number): Promise<boolean> {
  const usage = await analyzeUsage();

  if (usage.totalKeys > budgetKeys * 0.9) {
    console.warn(`WARNING: Approaching key limit (${usage.totalKeys}/${budgetKeys})`);

    // Send alert
    await sendSlackAlert({
      channel: "#billing",
      text: `Lokalise key usage at ${Math.round((usage.totalKeys / budgetKeys) * 100)}%`,
    });

    return false;
  }

  return true;
}
```

### Cost Comparison Report
```markdown
## Lokalise Cost Analysis

### Current Usage
- Projects: 5
- Total Keys: 3,500
- Languages: 8

### Current Plan: Pro ($400/mo)

### Recommendations
1. Archive 2 unused projects (-500 keys)
2. Remove 3 low-progress languages
3. Delete 200 archived keys
4. **Potential: Essential plan at $120/mo**

### Annual Savings: $3,360
```

## Resources
- [Lokalise Pricing](https://lokalise.com/pricing)
- [Lokalise Billing FAQ](https://docs.lokalise.com/en/articles/1400477-billing)

## Next Steps
For architecture patterns, see `lokalise-reference-architecture`.
