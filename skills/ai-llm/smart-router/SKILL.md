---
name: smart-router
description: Multi-tier LLM routing for cost optimization in the BidDeed.AI ecosystem. Routes tasks to appropriate model tier based on complexity, achieving 90% FREE tier processing. Use when making API calls, selecting models, implementing chat interfaces, or optimizing AI costs. Tiers: FREE (gemini-2.5-flash 1M context), ULTRA_CHEAP (deepseek-v3.2), CHEAP, STANDARD, PREMIUM (claude-sonnet-4), ULTRA (claude-opus-4.5).
---

# Smart Router V5

Multi-tier LLM routing achieving 90% FREE tier processing through intelligent task classification.

## Model Tiers

| Tier | Model | Context | Cost | Use Case |
|------|-------|---------|------|----------|
| FREE | gemini-2.5-flash | 1M tokens | $0 | Default, chat, summarization |
| ULTRA_CHEAP | deepseek-v3.2 | 128K | ~$0.28/1M | Simple analysis, formatting |
| CHEAP | gemini-1.5-pro | 2M | ~$1.25/1M | Long document analysis |
| STANDARD | claude-haiku-4.5 | 200K | ~$2.50/1M | Quick reasoning |
| PREMIUM | claude-sonnet-4 | 200K | ~$15/1M | Complex analysis |
| ULTRA | claude-opus-4.5 | 200K | ~$75/1M | Architecture, critical decisions |

## Routing Logic

```python
def route_task(task: dict) -> str:
    """Route task to appropriate model tier."""
    
    complexity = task.get('complexity', 'medium')
    requires_reasoning = task.get('reasoning', False)
    token_count = task.get('estimated_tokens', 0)
    critical = task.get('critical', False)
    
    # ULTRA tier - reserved for critical decisions
    if critical or task.get('type') == 'architecture':
        return 'ULTRA'
    
    # FREE tier - default for most tasks
    if complexity == 'low' and not requires_reasoning:
        return 'FREE'
    
    # ULTRA_CHEAP - simple but needs better than free
    if complexity == 'low' and requires_reasoning:
        return 'ULTRA_CHEAP'
    
    # CHEAP - long context needed
    if token_count > 100_000:
        return 'CHEAP'
    
    # STANDARD - moderate reasoning
    if complexity == 'medium':
        return 'STANDARD'
    
    # PREMIUM - complex analysis
    return 'PREMIUM'
```

## Task Classification

### FREE Tier Tasks (Target: 90%)
- Chat/conversation
- Simple Q&A
- Text summarization
- Format conversion
- Basic extraction

### ULTRA_CHEAP Tasks
- Structured data parsing
- Simple code generation
- Template filling
- Translation

### PREMIUM/ULTRA Tasks
- Lien priority analysis (legal reasoning)
- Architecture decisions
- Complex debugging
- ML model evaluation

## Configuration

```javascript
// Cloudflare Worker environment
const ROUTER_CONFIG = {
  FREE: {
    model: 'gemini-2.5-flash',
    apiKey: env.GOOGLE_API_KEY,
    projectId: '171223116958',
    maxTokens: 1_000_000
  },
  ULTRA_CHEAP: {
    model: 'deepseek-v3.2',
    endpoint: 'https://api.deepseek.com/v1/chat/completions',
    apiKey: env.DEEPSEEK_API_KEY
  },
  PREMIUM: {
    model: 'claude-sonnet-4-20250514',
    apiKey: env.ANTHROPIC_API_KEY
  }
};
```

## Cost Tracking

Log every API call to Supabase `daily_metrics`:

```sql
INSERT INTO daily_metrics (date, tier, calls, tokens, cost_usd)
VALUES (CURRENT_DATE, 'FREE', 1, 5000, 0.00);
```

## Integration Points

- Chat apps: `brevard-bidder-landing.pages.dev/chat`
- Life OS: `life-os-aiy.pages.dev/chat`
- GitHub Actions: Use PREMIUM for pipeline tasks
- API endpoints: Route via Cloudflare Worker

## Cost Optimization Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| FREE tier % | 90% | `free_calls / total_calls` |
| Avg cost/call | <$0.01 | `total_cost / total_calls` |
| Monthly spend | <$100 | Sum of all tiers |
| Paid tier savings | 25% | vs. STANDARD-only baseline |

