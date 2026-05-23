---
name: agent-cost-optimizer
description: Real-time cost tracking, budget enforcement, and ROI measurement for AI agent operations. Track token usage, predict costs, enforce budget caps ($50-70/month typical), optimize model selection, cache results, measure cost-to-value. Use when tracking AI costs, preventing budget overruns, optimizing spend, measuring ROI, or ensuring cost-effective AI operations.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Agent Cost Optimizer

## Overview

agent-cost-optimizer provides comprehensive cost tracking, budget enforcement, and ROI measurement for AI agent operations.

**Purpose**: Control and optimize AI spending while maximizing value delivered

**Pattern**: Task-based (7 operations for cost management)

**Key Innovation**: Real-time cost tracking with automatic budget enforcement and cost-effective fallbacks

**Industry Context** (2025):
- Average AI spending: **$85,521/month** (36% YoY increase)
- Only **50% of organizations can measure AI ROI**
- IT teams struggle with hidden costs

**Solution**: Comprehensive cost management from tracking to optimization

---

## When to Use

Use agent-cost-optimizer when:

- Tracking AI costs across skills
- Preventing budget overruns
- Measuring ROI (cost vs. value delivered)
- Optimizing model selection (Opus vs. Sonnet vs. Haiku)
- Planning AI budgets
- Cost-effective development
- Enterprise cost accountability

---

## Prerequisites

### Required
- AI API access (Anthropic, OpenAI, Google)
- Cost tracking capability (API usage data)

### Optional
- Paid.ai or AgentOps integration (advanced cost tracking)
- Prometheus/Grafana (cost visualization)
- Budget approval workflow

---

## Cost Operations

### Operation 1: Track Token Usage

**Purpose**: Monitor token consumption per skill invocation

**Process**:

1. **Initialize Tracking**:
   ```json
   {
     "tracking_id": "track_20250126_1200",
     "skill": "multi-ai-verification",
     "started_at": "2025-01-26T12:00:00Z",
     "tokens": {
       "prompt": 0,
       "completion": 0,
       "total": 0
     },
     "cost": {
       "amount_usd": 0.00,
       "model": "claude-sonnet-4-5"
     }
   }
   ```

2. **Track During Execution**:
   ```typescript
   // After each AI call
   trackTokens({
     prompt_tokens: response.usage.input_tokens,
     completion_tokens: response.usage.output_tokens,
     model: 'claude-sonnet-4-5'
   });

   // Update running totals
   ```

3. **Finalize Tracking**:
   ```json
   {
     "tracking_id": "track_20250126_1200",
     "skill": "multi-ai-verification",
     "completed_at": "2025-01-26T12:45:00Z",
     "duration_minutes": 45,
     "tokens": {
       "prompt": 15234,
       "completion": 8932,
       "total": 24166
     },
     "cost": {
       "amount_usd": 0.073,
       "model": "claude-sonnet-4-5",
       "rate": "$3 per million tokens"
     }
   }
   ```

4. **Save to Cost Log**:
   ```bash
   # Append to daily cost log
   cat tracking.json >> .cost-tracking/$(date +%Y-%m-%d).json
   ```

**Outputs**:
- Token usage per invocation
- Cost per invocation
- Model used
- Daily/monthly aggregates

**Validation**:
- [ ] Tracking initialized
- [ ] Tokens counted accurately
- [ ] Cost calculated correctly
- [ ] Logs saved

**Time Estimate**: Automatic (integrated into skills)

---

### Operation 2: Calculate Costs

**Purpose**: Compute accurate costs based on provider pricing

**Pricing** (2025 rates):

**Anthropic** (Claude):
| Model | Input (per MTok) | Output (per MTok) |
|-------|------------------|-------------------|
| Claude Opus 4.5 | $15 | $75 |
| Claude Sonnet 4.5 | $3 | $15 |
| Claude Haiku 4.5 | $0.80 | $4 |

**OpenAI** (Codex):
| Model | Input | Output |
|-------|-------|--------|
| GPT-5.1-codex | $5 | $15 |
| o3 | $10 | $40 |
| o4-mini | $1.50 | $6 |

**Google** (Gemini):
| Model | Input | Output |
|-------|-------|--------|
| Gemini 2.5 Pro | $1.25 | $5 |
| Gemini 2.5 Flash | $0.15 | $0.60 |

**Process**:

```typescript
function calculateCost(usage, model) {
  const pricing = {
    'claude-sonnet-4-5': { input: 3, output: 15 },
    'claude-haiku-4-5': { input: 0.80, output: 4 },
    'claude-opus-4-5': { input: 15, output: 75 },
    // ... more models
  };

  const rates = pricing[model];
  const inputCost = (usage.prompt_tokens / 1_000_000) * rates.input;
  const outputCost = (usage.completion_tokens / 1_000_000) * rates.output;

  return {
    input_cost: inputCost,
    output_cost: outputCost,
    total_cost: inputCost + outputCost,
    currency: 'USD'
  };
}
```

**Outputs**:
- Accurate cost per invocation
- Model-specific pricing
- Input vs. output cost breakdown

---

### Operation 3: Enforce Budget Caps

**Purpose**: Prevent exceeding monthly budget limits

**Process**:

1. **Set Budget**:
   ```json
   {
     "monthly_budget_usd": 100,
     "skill_budgets": {
       "multi-ai-verification": 70,
       "multi-ai-research": 20,
       "multi-ai-testing": 10
     },
     "alert_thresholds": {
       "warning": 0.80,
       "critical": 0.95
     }
   }
   ```

2. **Check Before Operation**:
   ```typescript
   async function checkBudget(skill, estimated_cost) {
     const usage = getCurrentMonthUsage();
     const remaining = budget.monthly_budget_usd - usage.total_cost;

     if (estimated_cost > remaining) {
       return {
         allowed: false,
         reason: `Budget exceeded: $${usage.total_cost}/$${budget.monthly_budget_usd}`,
         overage: estimated_cost - remaining
       };
     }

     if (usage.total_cost / budget.monthly_budget_usd > 0.80) {
       return {
         allowed: true,
         warning: `80% of monthly budget used ($${usage.total_cost}/$${budget.monthly_budget_usd})`
       };
     }

     return { allowed: true };
   }
   ```

3. **Enforce**:
   ```typescript
   const budgetCheck = await checkBudget('multi-ai-verification', 0.50);

   if (!budgetCheck.allowed) {
     console.log(`❌ Budget exceeded: ${budgetCheck.reason}`);
     console.log(`Options:`);
     console.log(`  1. Use cheaper model (Sonnet → Haiku)`);
     console.log(`  2. Skip optional verification layers`);
     console.log(`  3. Request budget increase`);
     return;
   }

   if (budgetCheck.warning) {
     console.log(`⚠️ ${budgetCheck.warning}`);
   }

   // Proceed with operation
   ```

**Outputs**:
- Budget status checked
- Operations blocked if over budget
- Warnings at 80%
- Cost-effective alternatives suggested

---

### Operation 4: Optimize Model Selection

**Purpose**: Choose cost-effective model for each task

**Decision Matrix**:

| Task Type | Recommended Model | Cost | Rationale |
|-----------|-------------------|------|-----------|
| **Simple verification** (Layer 1-2) | Haiku | $ | Rules-based, fast, cheap |
| **Code generation** | Sonnet | $$ | Balanced quality/cost |
| **Complex reasoning** (architecture) | Opus | $$$ | Best quality, worth premium |
| **LLM-as-judge** | Sonnet or external model | $$ | Good judgment, reasonable cost |
| **Test generation** | Sonnet | $$ | Comprehensive coverage needed |
| **Research** | Sonnet/Haiku mix | $-$$ | Haiku for search, Sonnet for synthesis |

**Auto-Optimization**:
```typescript
function selectModel(task_type, criticality, budget_remaining) {
  // Critical + budget OK → Use Opus
  if (criticality === 'critical' && budget_remaining > 20) {
    return 'claude-opus-4-5';
  }

  // Standard → Use Sonnet
  if (criticality === 'standard') {
    return 'claude-sonnet-4-5';
  }

  // Budget low or simple task → Use Haiku
  if (budget_remaining < 5 || task_type === 'simple') {
    return 'claude-haiku-4-5';
  }

  return 'claude-sonnet-4-5'; // Default
}
```

**Outputs**:
- Optimal model selected
- Cost minimized
- Quality maintained

---

### Operation 5: Cost-Effective Caching

**Purpose**: Avoid re-computing identical operations

**Process**:

1. **Cache Key Generation**:
   ```typescript
   function generateCacheKey(operation, inputs) {
     // Hash inputs to create unique key
     const content_hash = crypto
       .createHash('sha256')
       .update(JSON.stringify(inputs))
       .digest('hex');

     return `${operation}_${content_hash}`;
   }
   ```

2. **Check Cache Before Operation**:
   ```typescript
   const cacheKey = generateCacheKey('verify_code', {
     files: ['src/auth.ts'],
     file_hashes: {'src/auth.ts': 'abc123'}
   });

   const cached = readCache(cacheKey);

   if (cached && !isExpired(cached, 24)) {
     // Use cached result
     console.log('📦 Using cached verification result');
     return cached.result;
   }

   // Cache miss → run verification
   const result = await runVerification();

   // Save to cache
   saveCache(cacheKey, result, ttl: 24 hours);
   ```

3. **Cache Structure**:
   ```json
   {
     "cache_key": "verify_code_abc123def456",
     "created_at": "2025-01-26T12:00:00Z",
     "expires_at": "2025-01-27T12:00:00Z",
     "inputs": {
       "files": ["src/auth.ts"],
       "file_hashes": {"src/auth.ts": "abc123"}
     },
     "result": {
       "quality_score": 92,
       "layers_passed": 5,
       "issues": []
     },
     "cost_saved": 0.073
   }
   ```

**Outputs**:
- 90% reduction in re-verification costs
- Instant results for unchanged code
- Cache hit/miss tracking

**Validation**:
- [ ] Cache key correctly identifies identical operations
- [ ] File changes invalidate cache
- [ ] Expired cache not used
- [ ] Cost savings tracked

---

### Operation 6: Measure ROI

**Purpose**: Calculate return on investment for AI spending

**Process**:

1. **Track Time Saved**:
   ```json
   {
     "task": "Implement user authentication",
     "without_ai": {
       "estimated_hours": 40,
       "developer_rate": 100,
       "total_cost": 4000
     },
     "with_ai": {
       "actual_hours": 11.3,
       "developer_rate": 100,
       "developer_cost": 1130,
       "ai_cost": 2.50,
       "total_cost": 1132.50
     },
     "roi": {
       "time_saved_hours": 28.7,
       "cost_saved": 2867.50,
       "roi_percentage": 253,
       "payback_period_hours": 0.025
     }
   }
   ```

2. **Calculate ROI**:
   ```typescript
   function calculateROI(task) {
     const time_saved = task.without_ai.estimated_hours - task.with_ai.actual_hours;
     const cost_saved = task.without_ai.total_cost - task.with_ai.total_cost;
     const roi_percentage = (cost_saved / task.with_ai.ai_cost) * 100;

     return {
       time_saved_hours: time_saved,
       cost_saved_usd: cost_saved,
       roi_percentage: roi_percentage,
       payback_period: task.with_ai.ai_cost / (task.without_ai.developer_rate * (time_saved / 40)) // weeks
     };
   }
   ```

3. **Monthly ROI Report**:
   ```markdown
   # Monthly ROI Report - January 2025

   ## AI Spending
   - Total AI costs: $87.50
   - Breakdown:
     - multi-ai-verification: $62.30 (71%)
     - multi-ai-research: $18.40 (21%)
     - multi-ai-testing: $6.80 (8%)

   ## Time Savings
   - Tasks completed: 8
   - Total hours saved: 156 hours
   - Average savings per task: 19.5 hours

   ## Cost Savings
   - Developer cost avoided: $15,600 (156h × $100/h)
   - AI costs: $87.50
   - Net savings: $15,512.50

   ## ROI
   - ROI: 17,728% ($177 saved per $1 spent)
   - Payback period: 0.03 weeks (immediate)
   - Value multiplier: 178x

   ## Recommendations
   - ✅ Current spending highly cost-effective
   - Continue using AI for all qualifying tasks
   - Consider increasing budget (high ROI)
   ```

**Outputs**:
- Comprehensive ROI analysis
- Time and cost savings quantified
- Monthly reports
- Business justification for AI spending

---

### Operation 7: Predict Costs

**Purpose**: Estimate costs before starting expensive operations

**Process**:

1. **Historical Data**:
   ```json
   {
     "operation": "multi-ai-verification",
     "mode": "all_5_layers",
     "historical_costs": [
       {"date": "2025-01-15", "tokens": 24166, "cost": 0.073},
       {"date": "2025-01-18", "tokens": 21893, "cost": 0.066},
       {"date": "2025-01-20", "tokens": 26543, "cost": 0.080}
     ],
     "avg_cost": 0.073,
     "std_dev": 0.007
   }
   ```

2. **Predict Before Operation**:
   ```typescript
   const prediction = predictCost('multi-ai-verification', {
     mode: 'all_5_layers',
     code_size_lines: 850
   });

   console.log(`💰 Estimated cost: $${prediction.estimated_cost} ± $${prediction.std_dev}`);
   console.log(`   Range: $${prediction.min_cost} - $${prediction.max_cost}`);
   console.log(`   Confidence: ${prediction.confidence}%`);

   // Check budget
   if (prediction.estimated_cost > budget_remaining) {
     console.log(`⚠️ Estimated cost exceeds remaining budget`);
     console.log(`Options:`);
     console.log(`  1. Use Haiku (estimated: $${prediction.estimated_cost * 0.27})`);
     console.log(`  2. Skip Layer 5 (save ~60%: $${prediction.estimated_cost * 0.4})`);
     console.log(`  3. Increase budget`);
   }
   ```

**Outputs**:
- Cost predictions with confidence intervals
- Budget impact assessment
- Cost-effective alternatives suggested

---

## Cost Optimization Strategies

### Strategy 1: Model Selection

**Baseline** (All Sonnet): $100/month

**Optimized** (Smart selection):
- Layer 1-2: Haiku ($20)
- Layer 3-4: Sonnet ($40)
- Layer 5: Sonnet ($30)
- **Total**: $90/month (10% savings)

**Aggressive** (Maximum savings):
- Layer 1-2: Haiku ($20)
- Layer 3-4: Haiku ($15)
- Layer 5: Sonnet ($30)
- **Total**: $65/month (35% savings)

**Trade-off**: Some quality reduction at Layers 3-4

---

### Strategy 2: Caching

**Without Caching**: Re-verify same code multiple times

**With Caching** (24-hour TTL):
- First verification: $0.073
- Same code next 24h: $0 (cache hit)
- **Savings**: 90% on unchanged code

**Implementation**:
```typescript
const cacheKey = hash(files_to_verify);
const cached = getCache(cacheKey);

if (cached && !isExpired(cached, 24)) {
  return cached.result; // $0 cost
}

const result = await verify(); // $0.073 cost
saveCache(cacheKey, result);
```

---

### Strategy 3: Ensemble Optimization

**Baseline** (Always 5-agent ensemble):
- 5 agents × $0.073 = $0.365 per verification

**Optimized** (Conditional ensemble):
- Critical features: 5 agents ($0.365)
- Standard features: 3 agents ($0.219)
- Simple changes: 1 agent ($0.073)
- **Average savings**: 60%

**Decision Logic**:
```typescript
function shouldUseEnsemble(criticality, code_size, budget) {
  if (criticality === 'critical') return 5;
  if (criticality === 'high' && budget > 20) return 3;
  return 1; // Single agent
}
```

---

### Strategy 4: Layer Skipping

**Full Verification** (All 5 layers): ~$0.073

**Fast-Track** (Layers 1-2 only):
- Rules + Functional only
- ~$0.015 (80% savings)
- Use for: minor changes, docs, config

**Decision**:
```typescript
if (lines_changed < 50 && files_changed.every(f => !isCritical(f))) {
  // Fast-track: Layers 1-2 only
  mode = 'fast_track';
  estimated_cost = 0.015;
} else {
  // Full verification
  mode = 'standard';
  estimated_cost = 0.073;
}
```

---

## Budget Management

### Monthly Budget Planning

**Sample Budget** ($100/month):
```json
{
  "monthly_budget_usd": 100,
  "allocation": {
    "multi-ai-verification": {
      "budget": 70,
      "rationale": "Most expensive (LLM-as-judge)"
    },
    "multi-ai-research": {
      "budget": 20,
      "rationale": "Occasional use, tri-AI"
    },
    "multi-ai-testing": {
      "budget": 10,
      "rationale": "Mostly automated"
    },
    "buffer": 10
  },
  "assumptions": {
    "features_per_month": 8,
    "verifications_per_feature": 1.5,
    "research_per_month": 2
  }
}
```

### Budget Tracking

**Daily**:
```bash
# Check today's spending
cat .cost-tracking/$(date +%Y-%m-%d).json | jq '[.[] | .cost.amount_usd] | add'

# Output: $3.45 today
```

**Monthly**:
```bash
# Check month-to-date
cat .cost-tracking/2025-01-*.json | jq '[.[] | .cost.amount_usd] | add'

# Output: $67.80 this month (68% of budget)
```

**Projection**:
```typescript
// Project end-of-month
const days_elapsed = 26;
const days_in_month = 31;
const current_spend = 67.80;

const projected = (current_spend / days_elapsed) * days_in_month;
// = $81.14 projected (within budget ✅)
```

---

## Cost Alerting

### Alert Levels

**80% Budget** (Warning):
```markdown
⚠️  BUDGET ALERT: 80% Used

**Current**: $80.00 / $100.00 (80%)
**Remaining**: $20.00
**Days left**: 5

**Projected EOMs**: $93.75 (within budget)

**Recommendations**:
- Monitor spending closely
- Use Haiku for simple tasks
- Cache aggressively
- Skip optional layers where safe
```

**95% Budget** (Critical):
```markdown
🚨 CRITICAL: 95% Budget Used

**Current**: $95.00 / $100.00 (95%)
**Remaining**: $5.00
**Days left**: 5

**Projected EOM**: $110 (OVER BUDGET)

**Actions Required**:
1. Pause non-critical verifications
2. Use Haiku exclusively
3. Request budget increase OR
4. Defer work to next month

**Auto-throttling**: Enabled
- Only critical operations allowed
- All optional layers disabled
- Ensemble verification disabled
```

**Budget Exceeded**:
```markdown
❌ BUDGET EXCEEDED

**Current**: $102.50 / $100.00 (102.5%)
**Overage**: $2.50

**Operations BLOCKED** until:
1. Budget increased OR
2. Next month (resets automatically)

**Emergency Override**: Requires approval
```

---

## ROI Calculation Framework

### Value Metrics

**Quantifiable Value**:
- Time saved (hours)
- Cost saved (developer time avoided)
- Quality improvement (fewer bugs in production)
- Faster time-to-market (days)

**Formula**:
```
ROI = ((Value Delivered - AI Costs) / AI Costs) × 100%
```

**Example**:
```
Feature without AI: 40 hours × $100/hour = $4,000
Feature with AI: 11.3 hours × $100/hour + $2.50 AI = $1,132.50

Value Delivered = $4,000 - $1,130 = $2,870
AI Costs = $2.50
ROI = ($2,870 / $2.50) × 100% = 114,800%
```

### Monthly Reporting

**Template**:
```markdown
# AI ROI Report - January 2025

## Summary
- **AI Spending**: $87.50
- **Value Delivered**: $15,600 (156 hours saved × $100/hour)
- **ROI**: 17,728%
- **Payback**: Immediate

## Details

### Features Delivered (8)
1. User authentication - 11.3h (was 40h), ROI: 114,800%
2. Payment integration - 8.5h (was 32h), ROI: 108,235%
[... more ...]

### Cost Breakdown
- Verification: $62.30 (71%) - Highest cost, highest value
- Research: $18.40 (21%) - Occasional, high impact
- Testing: $6.80 (8%) - Mostly automated, low cost

### Savings
- Time: 156 hours saved
- Cost: $15,512.50 net savings
- Quality: 4 bugs prevented (saved ~20 hours)

### Recommendations
- ✅ ROI is excellent (17,728%)
- Consider increasing budget (high returns)
- Current spending optimal
```

---

## Quick Reference

### Cost Operations

| Operation | Purpose | Time | Automation |
|-----------|---------|------|------------|
| **Track** | Monitor token usage | Automatic | 100% |
| **Calculate** | Compute costs | Automatic | 100% |
| **Enforce** | Budget caps | Automatic | 100% |
| **Optimize** | Model selection | Semi-auto | 70% |
| **Cache** | Avoid re-compute | Automatic | 100% |
| **Measure ROI** | Value analysis | Manual | 30% |
| **Predict** | Cost estimation | Automatic | 90% |

### Cost Optimization Strategies

| Strategy | Savings | Trade-off | Recommended For |
|----------|---------|-----------|-----------------|
| **Model selection** | 10-35% | Some quality loss | All features |
| **Caching** | 90% | Stale results risk | Unchanged code |
| **Ensemble optimization** | 60% | Lower confidence | Non-critical |
| **Layer skipping** | 80% | Less thorough | Minor changes |

### Budget Thresholds

- **< 80%**: Normal operation
- **80-95%**: Warning, optimize
- **95-100%**: Critical, throttle
- **> 100%**: Block operations

---

**agent-cost-optimizer ensures cost-effective AI operations through real-time tracking, budget enforcement, model optimization, and ROI measurement - preventing budget overruns while maximizing value delivered.**

For cost reports, see examples/. For optimization strategies, see Cost Optimization Strategies section.
