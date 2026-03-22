---
name: claude-cost-optimization
description: Comprehensive cost tracking and optimization for production Claude deployments. Covers Admin API usage tracking, efficiency measurement, ROI calculation, optimization patterns (caching, batching, model selection, context editing, effort parameter), and cost prediction. Use when tracking costs, optimizing token usage, measuring efficiency, calculating ROI, reducing production expenses, or implementing cost-effective Claude integrations.
---

# Claude Cost Optimization

## Overview

Cost optimization is critical for production Claude deployments. A single inefficiently-designed agent can cost hundreds or thousands of dollars monthly, while optimized implementations cost 10-90% less for identical functionality. This skill provides a comprehensive workflow for measuring, analyzing, and optimizing token costs.

**Why This Matters**:
- Token costs are your largest Claude expense
- Small improvements compound over millions of API calls
- Context optimization alone saves 60-90% on long conversations
- Model + effort selection can reduce costs 5-10x for specific tasks

**Key Savings Available**:
- Effort parameter: 20-70% token reduction (same model, different reasoning depth)
- Context editing: 60-90% reduction on long conversations
- Tool optimization: 37-85% reduction with advanced tool patterns
- Prompt caching: 90% reduction on repeated content
- Model selection: 2-5x cost difference between models

## When to Use This Skill

Use claude-cost-optimization when you need to:

- **Track Token Costs**: Understand exactly what your Claude implementation costs
- **Identify Expensive Patterns**: Find which operations consume the most tokens
- **Measure ROI**: Calculate the business value of your Claude integration
- **Optimize for Production**: Reduce costs before deploying expensive agents
- **Analyze Cost Drivers**: Break down costs by model, feature, endpoint, or time period
- **Plan Budget**: Forecast future costs based on growth projections
- **Implement Optimizations**: Apply proven techniques (caching, batching, context editing)
- **Set Alerts**: Monitor costs and get notified of anomalies or budget overruns

## 5-Step Optimization Workflow

### Step 1: Measure Baseline Usage

Establish your current cost baseline before optimization.

**What to Measure**:
```
- Total monthly tokens (input + output)
- Cost breakdown by model
- Top 10 most expensive operations
- Average tokens per request
- Peak usage times and patterns
```

**How to Measure** (using Admin API):
```python
from anthropic import Anthropic

client = Anthropic()

# Get monthly usage
response = client.beta.admin.usage_metrics.list(
    limit=30,
    sort_by="date",
)

total_input_tokens = sum(m.input_tokens for m in response.data)
total_output_tokens = sum(m.output_tokens for m in response.data)
total_cost = (total_input_tokens * 0.000005) + (total_output_tokens * 0.000025)
print(f"Monthly cost: ${total_cost:.2f}")
```

**Where to Start**: See references/usage-tracking.md for detailed Admin API integration

### Step 2: Analyze Cost Drivers

Understand where your costs actually come from.

**Identify Expensive Patterns**:
1. Which operations use the most tokens?
2. Which models cost the most?
3. Are you using caching effectively?
4. Are context windows growing unnecessarily?
5. Are you making redundant API calls?

**Create Cost Breakdown** (example):
```
Agent reasoning loops: 45% of costs
File analysis: 25% of costs
Web search: 15% of costs
Classification tasks: 10% of costs
Other: 5% of costs
```

**Key Metrics to Calculate**:
- Cost per transaction
- Tokens per transaction
- Cost per business outcome
- Cost trend (week-over-week)

### Step 3: Apply Optimizations

Apply targeted optimizations to your biggest cost drivers.

**Effort Parameter** (if using Opus 4.5):
- Complex reasoning: high effort (default)
- Balanced tasks: medium effort (20-40% savings)
- Simple classification: low effort (50-70% savings)

**Context Editing** (for long conversations):
- Automatic tool result clearing (saves 60-90%)
- Client-side compaction (saves automatic summarization)
- Memory tool integration (enables infinite conversations)

**Tool Optimization** (for large tool sets):
- Tool search with deferred loading (supports 10K+ tools)
- Programmatic calling (37% token reduction on data processing)
- Tool examples (improve accuracy 72% → 90%)

**Prompt Caching** (for repeated content):
- Cache system prompts (90% cost reduction on cached portion)
- Cache repeated files/documents
- Cache tool definitions

**Model Selection**:
- Opus 4.5: $5/M input, $25/M output (complex tasks)
- Sonnet 4.5: (see references for pricing)
- Haiku 4.5: (see references for pricing)

### Step 4: Track Improvements

Monitor cost reductions and efficiency gains after optimizations.

**Metrics to Track**:
- Cost per transaction (before vs after)
- Total token reduction percentage
- Quality impact (did results improve or worsen?)
- Implementation difficulty and time

**Measurement Period**: Track for 1-2 weeks per optimization to see impact

**Example Impact**:
```
Optimization: Client-side compaction on long research tasks
Before: 450K tokens/request, $11.25 cost
After:  180K tokens/request, $4.50 cost
Savings: 60% cost reduction
```

### Step 5: Report ROI

Calculate business value of your optimizations.

**ROI Calculation**:
```
Monthly Savings = (Daily Cost × 30) - (Optimized Cost × 30)
Implementation Hours = Time to implement optimizations
Cost per Hour = $100-300 (your eng cost)
Payback Period = (Implementation Hours × Cost per Hour) / Monthly Savings
```

**ROI Example**:
```
Monthly savings: $500/month
Implementation: 8 hours
Cost per hour: $150
Implementation cost: $1,200
Payback period: 2.4 months
First year ROI: 400%
```

## Quick Start - Usage Tracking

Get started with Admin API cost tracking in 5 minutes:

```python
import anthropic
from datetime import datetime, timedelta

client = anthropic.Anthropic()

def get_monthly_costs():
    """Get current month's token costs"""

    # Get usage for last 30 days
    now = datetime.now()
    thirty_days_ago = now - timedelta(days=30)

    response = client.beta.admin.usage_metrics.list(
        limit=30,
        sort_by="date",
    )

    total_input = sum(m.input_tokens for m in response.data)
    total_output = sum(m.output_tokens for m in response.data)

    # Opus 4.5 pricing: $5/M input, $25/M output
    input_cost = total_input * 0.000005
    output_cost = total_output * 0.000025
    total_cost = input_cost + output_cost

    print(f"Last 30 days:")
    print(f"  Input tokens: {total_input:,}")
    print(f"  Output tokens: {total_output:,}")
    print(f"  Input cost: ${input_cost:.2f}")
    print(f"  Output cost: ${output_cost:.2f}")
    print(f"  Total cost: ${total_cost:.2f}")

    return {
        "input_tokens": total_input,
        "output_tokens": total_output,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost
    }

# Run the function
costs = get_monthly_costs()
```

## Quick Start - ROI Calculation

Calculate the business value of your Claude implementation:

```python
def calculate_roi(
    monthly_cost: float,
    monthly_transactions: int,
    cost_before_claude: float = None,
    quality_improvement: float = 1.0
) -> dict:
    """Calculate ROI metrics for Claude implementation"""

    cost_per_transaction = monthly_cost / monthly_transactions

    metrics = {
        "monthly_cost": monthly_cost,
        "monthly_transactions": monthly_transactions,
        "cost_per_transaction": cost_per_transaction,
    }

    # If you had costs before Claude (manual process, previous tool, etc)
    if cost_before_claude:
        savings = cost_before_claude - monthly_cost
        roi_percentage = (savings / cost_before_claude) * 100
        metrics["previous_cost"] = cost_before_claude
        metrics["monthly_savings"] = savings
        metrics["roi_percentage"] = roi_percentage

    # Account for quality improvements
    effective_cost = monthly_cost / quality_improvement
    metrics["quality_adjusted_cost"] = effective_cost

    return metrics

# Example: Research agent replacing manual research
result = calculate_roi(
    monthly_cost=500,          # Claude costs
    monthly_transactions=1000,  # Requests processed
    cost_before_claude=3000,   # Manual research was $3k/month
    quality_improvement=1.5    # Claude results are 50% better
)

print(f"Cost per transaction: ${result['cost_per_transaction']:.4f}")
print(f"Monthly savings: ${result['monthly_savings']:.2f}")
print(f"ROI: {result['roi_percentage']:.0f}%")
```

## Pricing Overview

**Current Claude Model Pricing** (as of November 2025):

| Model | Input | Output | Best For |
|-------|-------|--------|----------|
| Opus 4.5 | $5/M | $25/M | Complex reasoning, agents, coding |
| Sonnet 4.5 | $3/M | $15/M | Balanced performance/cost |
| Haiku 4.5 | $0.80/M | $4/M | Simple tasks, high volume |

**Cost Impact of Optimization Techniques**:

| Technique | Savings | Implementation Difficulty |
|-----------|---------|--------------------------|
| Effort parameter (medium) | 20-40% | Easy (add 2 lines) |
| Effort parameter (low) | 50-70% | Easy (add 2 lines) |
| Context editing | 60-90% | Medium (requires setup) |
| Tool optimization | 37-85% | Medium (architecture change) |
| Prompt caching | 90% | Hard (infrastructure) |
| Model selection | 50-75% | Hard (architecture change) |

**Example Cost Comparison** (1M transactions/month):

```
Scenario: Classification task

Opus 4.5, high effort:
- Input: 50M tokens @ $5/M = $250
- Output: 10M tokens @ $25/M = $250
- Total: $500/month

Opus 4.5, low effort:
- Input: 50M tokens @ $5/M = $250
- Output: 5M tokens @ $25/M = $125
- Total: $375/month (25% savings)

Haiku 4.5, high effort:
- Input: 50M tokens @ $0.80/M = $40
- Output: 10M tokens @ $4/M = $40
- Total: $80/month (84% savings)
```

## Optimization Decision Tree

```
START: Have high costs?
  ↓
  Q1: Do you know what's causing the costs?
    NO → Go to Step 2: Analyze Cost Drivers
    YES → Q2: Have you tried effort parameter (Opus 4.5)?
            NO → Apply effort parameter (medium/low)
                 Expect 20-70% savings, 2-4 hours implementation
            YES → Q3: Do you have long conversations (>50K tokens)?
                    NO → Q4: Do you have 10+ tools in your agents?
                            NO → Q5: Can you cache repeated content?
                                    YES → Implement prompt caching
                                          Expect 90% savings on cached
                                    NO → Consider model selection
                                         Expect 2-5x cost reduction
                            YES → Implement tool search + deferred loading
                                  Expect 85% context savings
                    YES → Implement context editing
                          Expect 60-90% savings on long tasks
```

## Common Optimization Scenarios

### Scenario 1: Reducing Agent Costs 50%

**Before**:
- Opus 4.5 with high effort
- Long reasoning loops
- All 20+ tools always loaded
- Monthly cost: $2,000

**Optimizations** (in order of impact):
1. **Effort Parameter**: Switch to medium effort → 30% savings ($600)
2. **Tool Optimization**: Use tool search + deferred loading → 20% savings ($400)
3. **Context Editing**: Clear old tool results → 10% savings ($200)
4. **Total**: 60% cost reduction to $800/month

**Timeline**: 20-30 hours implementation

### Scenario 2: Reducing Classification Costs 80%

**Before**:
- Opus 4.5 high effort (overkill for classification)
- Simple yes/no decisions
- Monthly cost: $1,000

**Optimizations**:
1. **Model Selection**: Switch to Haiku 4.5 → 80% savings ($800)
2. **Effort Parameter**: Use low effort → Additional 20% on Haiku
3. **Prompt Caching**: Cache classification rules → 90% savings on cache
4. **Total**: 85% cost reduction to $150/month

**Timeline**: 5-10 hours implementation

## Related Skills

For deeper dives into specific optimization areas, see:

- **claude-opus-4-5-guide**: Effort parameter trade-offs and Opus 4.5 capabilities
- **claude-context-management**: Context editing strategies (60-90% savings on long conversations)
- **claude-advanced-tool-use**: Tool optimization patterns (37-85% efficiency gains)
- **anthropic-expert**: Admin API reference and prompt caching basics

For complete optimization strategies, cost prediction models, and ROI measurement frameworks, see references/ directory.
