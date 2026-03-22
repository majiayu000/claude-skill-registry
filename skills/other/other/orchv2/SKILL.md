---
name: orchv2
description: Context-Aware Agentic Orchestrator that analyzes product context (budget, channel, maturity, timeline, team), recommends optimal execution scenarios, and generates budget-optimized campaign plans with 6 pre-built scenario templates.
---

# OrchV2 - Context-Aware Agentic Orchestrator

This skill is the **meta-orchestrator** that intelligently routes product launches through optimal execution paths based on business context detection.

## When to Use

Invoke this skill when:
- User says: "create a campaign plan", "what's the best approach", "recommend marketing strategy"
- User provides product details and asks for execution guidance
- User needs budget-optimized scenario recommendations
- User asks: "what will this cost?", "how long will this take?", "what do I need?"
- Beginning any multi-skill orchestration workflow
- Any skill needs to query execution context (recursive invocation)

## When NOT to Use

- User already knows exact skills to run (use direct skill invocation)
- Single-skill execution tasks
- User wants to manually control every step without recommendations

---

## What OrchV2 Does

### 1. Analyzes Product Context
Detects **6 business dimensions**:
- **Budget Tier**: bootstrapped (<$5K), lean ($5-20K), standard ($20-100K), premium (>$100K)
- **Launch Channel**: Kickstarter, Indiegogo, DTC, SaaS, Enterprise
- **Brand Maturity**: pre-launch, launch-ready, growth, established  
- **Timeline Urgency**: rushed (<2wks), standard (2-8wks), thorough (>8wks)
- **Team Size**: solo (1 person), small (2-5), agency (>5)
- **Content Depth**: minimal, standard, maximum

### 2. Recommends Scenarios  
Generates ranked list of **6 pre-built scenarios**:
1. 🏗️ **Brand Genesis** - Foundation-building ($4K, 1-2 days, 8 skills)
2. 🎯 **Crowdfunding Lean** - Budget Kickstarter ($12.5K, 2-3 days, 12 skills)
3. 🚀 **Crowdfunding Full** - Premium campaign ($28K, 4-5 days, 20 skills)
4. 🛒 **Bootstrapped DTC** - Organic launch ($8K, 1-2 days, 9 skills)
5. 🏢 **Enterprise GTM** - B2B SaaS ($45K, 5-7 days, 12 skills)
6. ⚙️ **Custom Hybrid** - Pick & choose with smart recommendations

### 3. Generates Execution Plans
For selected scenario:
- Ordered list of skills to execute
- Cost estimates (tokens + USD)
- Timeline projections (days)
- Deliverables breakdown (included/excluded)
- Platform-specific constraints

### 4. Optimizes for Budget
- Substitutes lean variants when over-budget
- Recommends upgrades when under-budget
- Explains cost-benefit tradeoffs
- Shows ROI estimates

---

## Input Variables

### Required
- `[PRODUCT]` - One of:
  - Path to `product.md` file
  - Inline product description with brand name, category, description, audience

### Optional (Auto-Detected)
- `[BUDGET_AMOUNT]` - USD budget available
- `[LAUNCH_CHANNEL]` - kickstarter|indiegogo|dtc|saas|enterprise
- `[TIMELINE_WEEKS]` - Weeks until launch
- `[TEAM_COUNT]` - Number of people on team
- `[STAGE]` - pre-launch|launch-ready|growth|established

### Output Preferences
- `[OUTPUT_FORMAT]` - recommendations|plan|comparison (default: recommendations)
- `[SCENARIO_ID]` - Specific scenario to use (optional, auto-recommends if missing)
- `[LIMIT]` - Number of scenarios to return (default: 3)

---

## The Protocol (4 Phases)

### Phase 1: Context Detection (Steps 1-3)

**Step 1: Parse Product Input**
- Extract: brand name, category, positioning
- Identify product type: hardware, digital, service, physical goods
- Parse specifications if provided
- Extract target audience segments

**Step 2: Detect Launch Context** (if not explicit)

Budget Tier Detection:
```
IF budget_amount provided:
  < $5K → bootstrapped
  $5-20K → lean
  $20-100K → standard
  > $100K → premium
ELSE IF product_price available:
  < $50 → bootstrapped
  $50-200 → lean
  $200-500 → standard
  > $500 → premium
ELSE IF team_count available:
  1 person → bootstrapped
  2-5 people → lean/standard
  > 5 people → premium
ELSE:
  default: standard
```

Channel Detection:
```
Scan for keywords in category/messaging:
  "kickstarter", "crowdfunding", "backer" → kickstarter
  "indiegogo" → indiegogo
  "shopify", "dtc", "ecommerce" → dtc
  "saas", "subscription", "platform" → saas
  "enterprise", "b2b" → enterprise

IF hardware/wearable/gadget:
  default: kickstarter
ELSE IF software/app:
  default: saas
ELSE:
  default: dtc
```

Maturity Detection:
```
IF has_existing_brand=false AND has_existing_content=false:
  → pre-launch
ELSE IF has_existing_brand=true AND has_existing_content=false:
  → launch-ready
ELSE IF has_existing_brand=true AND has_existing_content=true:
  IF target_regions > 2:
    → established
  ELSE:
    → growth
```

Timeline Detection:
```
IF timeline_weeks < 2:
  → rushed
ELSE IF timeline_weeks <= 8:
  → standard
ELSE:
  → thorough

Fallback from budget:
  bootstrapped → rushed
  premium → thorough
  else → standard
```

Team Size Detection:
```
IF team_count = 1:
  → solo
ELSE IF team_count <= 5:
  → small
ELSE:
  → agency

Fallback from budget:
  bootstrapped → solo
  premium → agency
  else → small
```

**Step 3: Explain Detection Logic**
For each dimension, state:
- Detected value
- Reasoning (which heuristic triggered)
- Confidence level: high (explicit data), medium (inferred), low (default)

**Validation Gate 1:**
- All 6 dimensions must have a value (even if default)
- Flag any low-confidence detections
- Suggest user confirm if >2 dimensions are low-confidence

---

### Phase 2: Scenario Matching (Steps 4-6)

**Step 4: Score All Scenarios** (0-100% match)

Scoring Algorithm:
```
match_score = 0

# Budget alignment (50% weight)
IF budget_tier == scenario.best_for_budget:
  match_score += 50
ELSE IF abs(budget_tier_index - scenario_budget_index) == 1:
  match_score += 25  # Adjacent tier
ELSE:
  match_score += 0

# Channel alignment (30% weight)
IF channel IN scenario.best_for_channels:
  match_score += 30
ELSE IF scenario.best_for_channels is empty:
  match_score += 15  # Universal scenario
ELSE:
  match_score += 0

# Maturity alignment (20% weight)
IF maturity IN scenario.best_for_maturity:
  match_score += 20
ELSE IF scenario.best_for_maturity is empty:
  match_score += 10  # Universal scenario
ELSE:
  match_score += 0

# Return final score (0-100)
```

**Step 5: Generate Pros/Cons** for each scenario

Pros Logic:
```
IF match_score >= 80:
  + "Perfect match for your context"
IF budget matches:
  + "Budget aligned ($X,XXX)"
IF channel matches:
  + "Optimized for {channel}"
IF timeline fits:
  + "Timeline matches urgency ({timeline})"
IF features comprehensive:
  + "Complete asset package"
```

Cons Logic:
```
IF budget over:
  - "Would exceed budget by ${over_amount}"
IF budget under significantly:
  - "Under-utilizes budget (room for upgrades)"
IF wrong channel:
  - "Better suited for {other_channels}"
IF assumes assets user doesn't have:
  - "Assumes existing {missing_asset}"
IF excludes desired features:
  - "Excludes {feature}"
```

**Step 6: Rank by Score** (descending)
- Sort scenarios by match_score
- Take top N (default 3)
- Mark highest score as "RECOMMENDED"

**Validation Gate 2:**
- At least 1 scenario must score >50%
- If no good match, recommend "custom-hybrid" with explanation
- If top 3 scores are very close (<10% apart), flag as "multiple good options"

---

### Phase 3: Cost Estimation (Steps 7-8)

**Step 7: Calculate Costs for Top Scenarios**

For each scenario:
```python
total_tokens = 0
total_usd = 0
skill_breakdown = []

FOR each skill_id IN scenario.skill_ids:
  skill = registry.get_skill(skill_id)
  
  # Base token estimate
  base_tokens = skill.metadata.estimated_tokens
  
  # Apply depth multiplier
  depth_multipliers = {
    "surface": 0.5,
    "focused": 1.0,
    "comprehensive": 1.5,
    "exhaustive": 2.5
  }
  depth_mult = depth_multipliers[scenario.execution_context.depth_level]
  
  # Apply format overhead
  format_overhead = {
    "minimal": 500,
    "standard": 1500,
    "maximum": 3000
  }
  format_add = format_overhead[scenario.execution_context.output_format]
  
  # Calculate
  skill_tokens = int(base_tokens * depth_mult + format_add)
  skill_usd = int(skill_tokens * 0.25)  # $0.25 per 1K tokens
  
  total_tokens += skill_tokens
  total_usd += skill_usd
  
  skill_breakdown.append({
    "skill_id": skill_id,
    "skill_name": skill.name,
    "tokens": skill_tokens,
    "usd": skill_usd
  })

scenario.estimated_tokens = total_tokens
scenario.estimated_cost_usd = total_usd
scenario.cost_breakdown = skill_breakdown
```

**Step 8: Calculate Budget Utilization**
```
IF user_budget_amount provided:
  utilization = (estimated_cost / user_budget_amount) * 100
  
  IF utilization > 100:
    warning = f"Over budget by {utilization - 100}%"
  ELSE IF utilization < 70:
    suggestion = f"Under budget by {100 - utilization}%. Consider upgrades."
  ELSE:
    status = f"Good fit ({utilization}% of budget)"
```

**Validation Gate 3:**
- Per-skill cost should be 1K-15K tokens (flag if outside)
- Total cost should align with scenario.estimated_cost_usd ±20%
- Budget utilization should be reasonable (50-120%)

---

### Phase 4: Output Generation (Steps 9-12)

**Step 9: Generate Recommendations Output** (if output_format = "recommendations")

Structure:
```markdown
# Scenario Recommendations

## Detected Context
| Dimension | Value | Reasoning |
|-----------|-------|-----------|
| Budget    | lean  | Explicit budget $15K |
| Channel   | kickstarter | Keywords + hardware category |
| ...       | ...   | ... |

## Recommended Scenarios

### #1 - 🎯 Crowdfunding Lean ← RECOMMENDED
**Match Score:** 85%
**Description:** {scenario.description}
**Estimates:** 12 skills | $12,500 | 2-3 days
**Pros:**
- Perfect budget match
- Optimized for Kickstarter
**Cons:**
- Assumes existing brand identity
**Deliverables:** Campaign page, video script, ads, emails...

### #2 - ... (repeat for top 3)

## Next Steps
1. Review recommendations
2. Select scenario
3. Run: `python3 -m orchv2.cli.main plan --scenario <id>`
```

**Step 10: Generate Execution Plan** (if output_format = "plan")

Structure:
```markdown
# Execution Plan: Crowdfunding Lean

## Scenario Overview
{Description, estimates, context}

## Execution Context
| Constraint | Value |
|------------|-------|
| Budget Tier | lean |
| Tone | conversion-focused, urgent |
| Depth | focused |
| ...

## Skills to Execute
1. Buyer Persona
   - Tokens: 5,000 | Cost: $1,250 | Time: ~8 min
   - Dependencies: None
   - Outputs: persona_name, voice_samples, emotional_drivers

2. Competitor Analysis
   - Tokens: 6,000 | Cost: $1,500 | Time: ~10 min
   - Dependencies: None
   - Outputs: market_gaps, verified_anxieties

... (repeat for all 12 skills)

## Cost Breakdown
| Skill | Tokens | USD |
|-------|--------|-----|
| Buyer Persona | 5,000 | $1,250 |
| ... | ... | ... |
| **TOTAL** | **50,000** | **$12,500** |

## How to Execute
```bash
python3 -m orchv2.cli.main run --scenario crowdfunding-lean
```
```

**Step 11: Generate Comparison Table** (if output_format = "comparison")

Structure:
```markdown
# Scenario Comparison

## Side-by-Side
| Metric | Crowdfund Lean | Crowdfund Full | Bootstrap DTC |
|--------|---------------|----------------|---------------|
| Skills | 12 | 20 | 9 |
| Cost | $12,500 | $28,000 | $8,000 |
| Timeline | 2-3 days | 4-5 days | 1-2 days |
| ... | ... | ... | ... |

## Deliverables Matrix
| Deliverable | Lean | Full | DTC |
|-------------|------|------|-----|
| Campaign Page | ✅ | ✅ | ✅ |
| Video Script | ⚡ | ✅ | ❌ |
| ... | ... | ... | ... |

Legend: ✅ Full | ⚡ Lean | ❌ Not included

## Recommendation: Crowdfunding Lean (85% match)
{Reasoning}
```

**Step 12: Generate JSON Metadata Block**

All outputs must include:
```json
{
  "meta": {
    "orchestrator_version": "2.0.0",
    "product_name": "...",
    "detected_context": {
      "budget_tier": "lean",
      "launch_channel": "kickstarter",
      "maturity_stage": "pre-launch",
      "timeline_urgency": "standard",
      "team_size": "small"
    },
    "generated_at": "2026-01-20T18:30:00Z"
  },
  "recommendations": [
    {
      "rank": 1,
      "scenario_id": "crowdfunding-lean",
      "match_score": 0.85,
      "estimated_cost_usd": 12500,
      "estimated_tokens": 50000,
      "timeline_days": "2-3",
      "skills": ["buyer-persona", "competitor-analysis", ...]
    },
    // ... top 3 scenarios
  ]
}
```

**Validation Gate 4:**
- Output includes all required sections
- JSON is valid and complete
- Cost estimates are present
- Reasoning is clear and actionable

---

## Output Templates

Generate output using one of three templates:

1. **recommendations.md** - Top 3 scenarios with match scores, pros/cons
2. **execution-plan.md** - Detailed plan for selected scenario with cost breakdown
3. **scenario-comparison.md** - Side-by-side table of multiple scenarios

(See `templates/` directory for full templates)

---

## Self-Reference Pattern

OrchV2 can be invoked recursively for context queries:

**Example: Campaign Copy Skill Queries OrchV2**
```
Step 1: campaign-page-copy skill starts execution
Step 2: Skill needs to know: "Am I in lean or premium mode?"
Step 3: Skill invokes: query_orchv2("execution_context")
Step 4: OrchV2 returns:
{
  "budget_tier": "lean",
  "tone": "conversion-focused, urgent",
  "depth_level": "focused",
  "output_format": "standard",
  "token_limit": 5000
}
Step 5: Skill adapts output accordingly
```

**Context Queries Supported:**
- `execution_context` - Returns ExecutionContext object
- `am_i_over_budget(tokens_used)` - Returns boolean + remaining budget
- `what_scenario` - Returns current scenario_id
- `what_quality_bar` - Returns quality_bar setting
- `platform_constraints` - Returns list of platform-specific rules

This creates a **context-aware agent mesh** where any skill can query the orchestrator.

---

## Quality Guardrails

1. **Always explain detection** - Don't just say "lean budget", explain WHY
2. **Surface uncertainty** - Flag low-confidence detections with ⚠️
3. **Provide alternatives** - Show top 3, not just #1
4. **Explain tradeoffs** - Clear pros/cons for each
5. **Cost transparency** - Always show estimates
6. **Validate assumptions** - Ask user to confirm if confidence <medium

---

## Error Handling

| Condition | Action |
|-----------|--------|
| Product data missing | Ask for minimum: brand name + category |
| Context undetectable | Use defaults + flag low confidence |
| No scenario >50% match | Recommend custom-hybrid + explain why |
| Budget too low | Suggest brand-genesis-lean OR increasing budget |
| Skills registry empty | Fallback to V1 orchestrator skill list |

---

## CLI Invocation

```bash
# Context analysis
python3 -m orchv2.cli.main analyze-context --product product.md

# Get recommendations
python3 -m orchv2.cli.main recommend --limit 3

# Generate plan
python3 -m orchv2.cli.main plan --scenario crowdfunding-lean

# Compare scenarios
python3 -m orchv2.cli.main compare --scenarios crowdfunding-lean,crowdfunding-full
```

---

## Python API

```python
from orchv2 import ContextAnalyzer, ScenarioRecommender, SkillsRegistry

# Load product
product = load_product("product.md")

# Analyze context
analyzer = ContextAnalyzer()
context = analyzer.analyze(product)

# Get recommendations
recommender = ScenarioRecommender()
matches = recommender.recommend(product, context, limit=3)

# Generate plan
scenario = recommender.get_scenario(matches[0].scenario_id)
registry = SkillsRegistry()
cost = registry.estimate_total_cost(scenario.skill_ids)

print(f"Recommended: {scenario.name}")
print(f"Cost: ${cost['total_usd']:,}")
```

---

## Integration & Technical Specs

- **ID**: `orchv2`
- **Version**: `2.0.0`
- **Category**: Meta-Orchestration / Strategy
- **Complexity**: High (coordinates 64+ skills)
- **Estimated Tokens**: 2,000-5,000 (orchestration overhead only)
- **Execution Time**: 30-60 seconds (analysis + recommendations)
- **Dependencies**: None (root-level skill)
- **Downstream**: All 64 skills can reference orchv2 for context

---

## Metadata

```json
{
  "skill_id": "orchv2",
  "version": "2.0.0",
  "source": "both",
  "estimated_tokens": 2000,
  "complexity": "high",
  "quality_tier": "premium",
  "can_run_parallel": true,
  "supports_scenarios": ["all"],
  "provides_context": true,
  "recursive_invocation": true
}
```
