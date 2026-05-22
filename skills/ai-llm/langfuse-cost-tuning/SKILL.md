---
name: langfuse-cost-tuning
description: |
  Monitor and optimize LLM costs using Langfuse analytics and dashboards.
  Use when tracking LLM spending, identifying cost anomalies,
  or implementing cost controls for AI applications.
  Trigger with phrases like "langfuse costs", "LLM spending",
  "track AI costs", "langfuse token usage", "optimize LLM budget".
allowed-tools: Read, Write, Edit
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Langfuse Cost Tuning

## Overview
Track, analyze, and optimize LLM costs using Langfuse observability data.

## Prerequisites
- Langfuse tracing with token usage
- Understanding of LLM pricing models
- Access to Langfuse analytics dashboard

## LLM Cost Reference

| Model | Input (per 1M) | Output (per 1M) |
|-------|----------------|-----------------|
| GPT-4 Turbo | $10.00 | $30.00 |
| GPT-4o | $5.00 | $15.00 |
| GPT-4o-mini | $0.15 | $0.60 |
| GPT-3.5 Turbo | $0.50 | $1.50 |
| Claude 3 Opus | $15.00 | $75.00 |
| Claude 3 Sonnet | $3.00 | $15.00 |
| Claude 3 Haiku | $0.25 | $1.25 |

## Instructions

### Step 1: Track Token Usage in Generations

```typescript
import { Langfuse } from "langfuse";

const langfuse = new Langfuse();

// Model pricing configuration
const MODEL_PRICING: Record<
  string,
  { input: number; output: number }
> = {
  "gpt-4-turbo": { input: 10.0, output: 30.0 },
  "gpt-4o": { input: 5.0, output: 15.0 },
  "gpt-4o-mini": { input: 0.15, output: 0.6 },
  "gpt-3.5-turbo": { input: 0.5, output: 1.5 },
  "claude-3-opus": { input: 15.0, output: 75.0 },
  "claude-3-sonnet": { input: 3.0, output: 15.0 },
  "claude-3-haiku": { input: 0.25, output: 1.25 },
};

function calculateCost(
  model: string,
  promptTokens: number,
  completionTokens: number
): number {
  const pricing = MODEL_PRICING[model] || { input: 0, output: 0 };
  const inputCost = (promptTokens / 1_000_000) * pricing.input;
  const outputCost = (completionTokens / 1_000_000) * pricing.output;
  return inputCost + outputCost;
}

// Track with cost metadata
async function tracedLLMCall(
  trace: ReturnType<typeof langfuse.trace>,
  model: string,
  messages: any[]
) {
  const generation = trace.generation({
    name: "llm-call",
    model,
    input: messages,
  });

  const response = await openai.chat.completions.create({
    model,
    messages,
  });

  const usage = response.usage!;
  const cost = calculateCost(model, usage.prompt_tokens, usage.completion_tokens);

  generation.end({
    output: response.choices[0].message,
    usage: {
      promptTokens: usage.prompt_tokens,
      completionTokens: usage.completion_tokens,
      totalTokens: usage.total_tokens,
    },
    metadata: {
      cost_usd: cost,
      model_version: model,
    },
  });

  return response;
}
```

### Step 2: Create Cost Dashboard Queries

```typescript
// Fetch cost data from Langfuse
async function getCostAnalytics(days: number = 30) {
  const langfuse = new Langfuse();

  const fromDate = new Date();
  fromDate.setDate(fromDate.getDate() - days);

  const generations = await langfuse.fetchGenerations({
    fromTimestamp: fromDate,
  });

  // Aggregate costs
  const costByModel: Record<string, number> = {};
  const costByDay: Record<string, number> = {};
  const tokensByModel: Record<string, { prompt: number; completion: number }> = {};

  for (const gen of generations.data) {
    const model = gen.model || "unknown";
    const date = new Date(gen.startTime).toISOString().split("T")[0];

    // Get cost from metadata or calculate
    const cost = gen.metadata?.cost_usd || calculateCost(
      model,
      gen.usage?.promptTokens || 0,
      gen.usage?.completionTokens || 0
    );

    // Aggregate by model
    costByModel[model] = (costByModel[model] || 0) + cost;

    // Aggregate by day
    costByDay[date] = (costByDay[date] || 0) + cost;

    // Token usage by model
    if (!tokensByModel[model]) {
      tokensByModel[model] = { prompt: 0, completion: 0 };
    }
    tokensByModel[model].prompt += gen.usage?.promptTokens || 0;
    tokensByModel[model].completion += gen.usage?.completionTokens || 0;
  }

  return {
    totalCost: Object.values(costByModel).reduce((a, b) => a + b, 0),
    costByModel,
    costByDay,
    tokensByModel,
    generationCount: generations.data.length,
  };
}
```

### Step 3: Implement Cost Alerts

```typescript
interface CostAlert {
  type: "daily" | "hourly" | "per-request";
  threshold: number;
  action: "warn" | "block" | "notify";
}

const COST_ALERTS: CostAlert[] = [
  { type: "daily", threshold: 100, action: "warn" },
  { type: "daily", threshold: 500, action: "notify" },
  { type: "per-request", threshold: 1, action: "warn" },
];

class CostMonitor {
  private hourlySpend: Map<string, number> = new Map();
  private dailySpend: Map<string, number> = new Map();

  trackCost(cost: number) {
    const hourKey = new Date().toISOString().slice(0, 13);
    const dayKey = new Date().toISOString().slice(0, 10);

    this.hourlySpend.set(
      hourKey,
      (this.hourlySpend.get(hourKey) || 0) + cost
    );
    this.dailySpend.set(
      dayKey,
      (this.dailySpend.get(dayKey) || 0) + cost
    );

    this.checkAlerts(cost);
  }

  private checkAlerts(requestCost: number) {
    const dayKey = new Date().toISOString().slice(0, 10);
    const dailyTotal = this.dailySpend.get(dayKey) || 0;

    for (const alert of COST_ALERTS) {
      let currentValue: number;

      switch (alert.type) {
        case "daily":
          currentValue = dailyTotal;
          break;
        case "per-request":
          currentValue = requestCost;
          break;
        default:
          continue;
      }

      if (currentValue >= alert.threshold) {
        this.triggerAlert(alert, currentValue);
      }
    }
  }

  private triggerAlert(alert: CostAlert, value: number) {
    const message = `Cost alert: ${alert.type} spend $${value.toFixed(2)} exceeded threshold $${alert.threshold}`;

    switch (alert.action) {
      case "warn":
        console.warn(message);
        break;
      case "notify":
        this.sendNotification(message);
        break;
      case "block":
        throw new Error(`Request blocked: ${message}`);
    }
  }

  private async sendNotification(message: string) {
    // Send to Slack, PagerDuty, etc.
    await fetch(process.env.SLACK_WEBHOOK_URL!, {
      method: "POST",
      body: JSON.stringify({ text: message }),
    });
  }

  getStats() {
    const dayKey = new Date().toISOString().slice(0, 10);
    return {
      dailySpend: this.dailySpend.get(dayKey) || 0,
      dailyBudgetRemaining: 100 - (this.dailySpend.get(dayKey) || 0),
    };
  }
}

const costMonitor = new CostMonitor();
```

### Step 4: Implement Cost Optimization Strategies

```typescript
// Model selection based on task complexity
interface ModelSelector {
  selectModel(task: string, inputLength: number): string;
}

class CostOptimizedModelSelector implements ModelSelector {
  selectModel(task: string, inputLength: number): string {
    // Simple tasks -> cheaper model
    const simpleTasks = ["summarize", "classify", "extract"];
    if (simpleTasks.some((t) => task.toLowerCase().includes(t))) {
      return "gpt-4o-mini";
    }

    // Short inputs -> cheaper model
    if (inputLength < 500) {
      return "gpt-4o-mini";
    }

    // Complex tasks -> more capable model
    const complexTasks = ["analyze", "reason", "code", "math"];
    if (complexTasks.some((t) => task.toLowerCase().includes(t))) {
      return "gpt-4o";
    }

    // Default to mid-tier
    return "gpt-4o-mini";
  }
}

// Prompt optimization to reduce tokens
function optimizePrompt(prompt: string): string {
  // Remove excessive whitespace
  let optimized = prompt.replace(/\s+/g, " ").trim();

  // Remove redundant instructions
  optimized = optimized.replace(/please |kindly |could you /gi, "");

  return optimized;
}

// Caching for repeated queries
const responseCache = new Map<string, { response: string; timestamp: Date }>();

async function cachedLLMCall(
  prompt: string,
  model: string,
  ttlMs: number = 3600000
): Promise<string> {
  const cacheKey = `${model}:${prompt}`;
  const cached = responseCache.get(cacheKey);

  if (cached && Date.now() - cached.timestamp.getTime() < ttlMs) {
    console.log("Cache hit - saved API call");
    return cached.response;
  }

  const response = await callLLM(prompt, model);
  responseCache.set(cacheKey, { response, timestamp: new Date() });

  return response;
}
```

### Step 5: Generate Cost Reports

```typescript
async function generateCostReport(period: "daily" | "weekly" | "monthly") {
  const days = period === "daily" ? 1 : period === "weekly" ? 7 : 30;
  const analytics = await getCostAnalytics(days);

  const report = `
# LLM Cost Report - ${period.charAt(0).toUpperCase() + period.slice(1)}
Generated: ${new Date().toISOString()}

## Summary
- Total Cost: $${analytics.totalCost.toFixed(2)}
- Total Generations: ${analytics.generationCount}
- Average Cost per Generation: $${(analytics.totalCost / analytics.generationCount).toFixed(4)}

## Cost by Model
${Object.entries(analytics.costByModel)
  .sort(([, a], [, b]) => b - a)
  .map(([model, cost]) => `- ${model}: $${cost.toFixed(2)}`)
  .join("\n")}

## Token Usage by Model
${Object.entries(analytics.tokensByModel)
  .map(
    ([model, tokens]) =>
      `- ${model}: ${tokens.prompt.toLocaleString()} prompt, ${tokens.completion.toLocaleString()} completion`
  )
  .join("\n")}

## Recommendations
${generateRecommendations(analytics)}
`;

  return report;
}

function generateRecommendations(analytics: any): string {
  const recommendations: string[] = [];

  // Check for expensive model overuse
  const gpt4Cost = analytics.costByModel["gpt-4-turbo"] || 0;
  const totalCost = analytics.totalCost;

  if (gpt4Cost > totalCost * 0.5) {
    recommendations.push(
      "- Consider using GPT-4o or GPT-4o-mini for simpler tasks to reduce costs"
    );
  }

  // Check for high output token ratio
  for (const [model, tokens] of Object.entries(analytics.tokensByModel)) {
    const { prompt, completion } = tokens as any;
    if (completion > prompt * 2) {
      recommendations.push(
        `- ${model}: High output ratio. Consider limiting max_tokens or response length`
      );
    }
  }

  return recommendations.length > 0
    ? recommendations.join("\n")
    : "- No immediate optimization opportunities identified";
}
```

## Output
- Token usage tracking in generations
- Cost analytics dashboard
- Real-time cost alerts
- Model selection optimization
- Caching and prompt optimization
- Automated cost reports

## Cost Optimization Strategies

| Strategy | Potential Savings | Implementation Effort |
|----------|-------------------|----------------------|
| Model downgrade | 50-90% | Low |
| Prompt optimization | 10-30% | Low |
| Response caching | 20-60% | Medium |
| Batch processing | 10-20% | Medium |
| Sampling | Variable | Medium |

## Error Handling
| Issue | Cause | Solution |
|-------|-------|----------|
| Missing usage data | SDK not capturing | Verify generation.end() includes usage |
| Inaccurate costs | Wrong pricing | Update MODEL_PRICING regularly |
| Budget exceeded | No alerts | Implement cost alerts |
| Report failures | API limits | Add pagination to fetchGenerations |

## Resources
- [Langfuse Analytics](https://langfuse.com/docs/analytics)
- [OpenAI Pricing](https://openai.com/pricing)
- [Anthropic Pricing](https://www.anthropic.com/pricing)

## Next Steps
For reference architecture, see `langfuse-reference-architecture`.
