---
name: drip
description: |
  Track and surface the estimated water cost of Claude interactions. Every query
  has a physical footprint - data centers need cooling, electricity needs
  generation. This skill adds environmental accountability by estimating water
  consumption per session and surfacing it at meaningful moments. Not to induce
  guilt, but to create awareness of the physical cost of intelligence.
allowed-tools: |
  bash: python
  file: read
---

# Drip

<purpose>
AI feels weightless. Type a question, get an answer. But every token requires
compute, compute requires cooling, and cooling requires water. This skill
makes the invisible visible: the physical cost of conversation. Not to shame,
but to acknowledge that intelligence has a footprint.
</purpose>

## The Numbers (Honest Assessment)

<data-sources>
**What we know (2024-2025 research):**

Self-reported by providers (direct cooling only):
- Google Gemini: ~0.26ml per query
- OpenAI GPT-4: ~0.3ml per query

Academic estimates (including electricity generation water):
- 5-10ml per query for efficient models
- Up to 150ml for reasoning-heavy models like DeepSeek-R1

Per-token estimate (derived):
- ~0.5ml per 1,000 tokens (mid-range, including indirect)
- ~0.05ml per 1,000 tokens (direct cooling only)

**Why estimates vary:**
- Direct vs indirect water (cooling vs electricity generation)
- Regional data center efficiency (WUE ranges 0-3+ L/kWh)
- Model efficiency (1B vs 70B+ parameters)
- Query complexity (simple vs chain-of-thought reasoning)

**What we use:** 0.5ml per 1,000 tokens (conservative mid-range)
This includes indirect water from electricity but excludes hardware manufacturing.

Sources:
- UC Riverside/Colorado study (2023)
- "How Hungry is AI?" benchmark (2025)
- Google/OpenAI self-reported figures (2024-2025)
</data-sources>

## When To Surface

<triggers>
Surface water estimates at:

**Session milestones:**
- Every ~50,000 tokens (roughly 25ml / ~1 tablespoon)
- End of significant work sessions
- When user asks about environmental impact

**Heavy operations:**
- Large file analysis (adds significant token overhead)
- Multiple iterations/retries on same problem
- Long chain-of-thought reasoning

**NOT on:**
- Quick questions (overhead of displaying exceeds the point)
- Already-stressed users (not the time)
- Every single response (becomes noise)
</triggers>

## Instructions

### Step 1: Estimate Token Usage

Rough token counting:
- 1 word ≈ 1.3 tokens (English)
- 1 line of code ≈ 10 tokens
- This message you're reading ≈ 50 tokens

Track cumulative tokens across the session (input + output).

### Step 2: Calculate Water Estimate

```python
# Conservative mid-range estimate
ML_PER_1000_TOKENS = 0.5

def estimate_water_ml(total_tokens):
    return (total_tokens / 1000) * ML_PER_1000_TOKENS

# Examples:
# 10,000 tokens = 5ml (about 1 teaspoon)
# 50,000 tokens = 25ml (about 1 tablespoon)
# 100,000 tokens = 50ml (about 3 tablespoons)
```

### Step 3: Surface Meaningfully

At session milestones or on request:

```
Session footprint:

Tokens: ~[X]
Water: ~[Y]ml ([familiar comparison])

For context:
- A shower uses ~65,000ml
- A cup of coffee uses ~140ml to brew
- This session: [Y]ml

Not guilt. Just awareness.
```

### Step 4: Provide Context

Make numbers relatable:

| Tokens | Water (ml) | Comparison |
|--------|------------|------------|
| 1,000 | 0.5 | 10 drops |
| 10,000 | 5 | 1 teaspoon |
| 50,000 | 25 | 1 tablespoon |
| 100,000 | 50 | Small espresso cup |
| 500,000 | 250 | 1 cup |

## Philosophical Frame

<philosophy>
This skill isn't about guilt. It's about truth.

Every human activity has a footprint. A Google search uses ~0.3ml of water.
Sending an email uses electricity. Existing in a modern economy has costs.

The goal isn't to stop using AI. It's to:
1. Acknowledge that "digital" still has physical costs
2. Make informed decisions about when AI is worth the cost
3. Appreciate the infrastructure that makes intelligence-on-demand possible
4. Perhaps: favour efficiency when it doesn't compromise quality

The most ethical response isn't to stop. It's to be aware, and to not waste.
</philosophy>

## Honest Caveats

<caveats>
**What this estimate INCLUDES:**
- Data center cooling water
- Water used in electricity generation
- Reasonable regional averaging

**What this estimate EXCLUDES:**
- Hardware manufacturing (chips, servers)
- Network infrastructure
- Human labor to build/maintain systems
- Full lifecycle analysis

**Uncertainty:**
These numbers have ~10x variance depending on assumptions. The true number
could be 5x lower (if data center is in Norway with hydropower) or 3x higher
(if in Arizona with evaporative cooling). We use mid-range estimates.

**Perspective:**
A single ChatGPT query uses less water than the manufacturing footprint of
the device you're using to send it. The embodied water in your laptop
dwarfs a year of AI queries. Context matters.
</caveats>

## NEVER

- Surface on every response (becomes annoying noise)
- Use guilt-inducing language ("you're wasting water")
- Pretend the numbers are precise (they're estimates)
- Ignore that the user's task might be worth the cost
- Compare unfavourably to human alternatives without noting human costs too

## ALWAYS

- Be honest about estimate uncertainty
- Provide relatable comparisons (teaspoons, not just millilitres)
- Frame as awareness, not judgment
- Acknowledge that some tasks are worth their footprint
- Note efficiency gains over time (models are getting more efficient)

## Examples

### Example 1: End of Work Session

```
Session complete.

Work done:
- Refactored auth module
- Fixed 3 bugs
- Added tests

Session footprint:
~45,000 tokens ≈ 22ml of water (just under 1 tablespoon)

For context: less than the water used to wash your hands once.
The efficiency of your auth system probably saves more resources
than this session cost.
```

### Example 2: On Direct Question

User: "How much water has this conversation used?"

```
This conversation so far:

Tokens: ~12,000 (my estimate)
Water: ~6ml

That's about 1 teaspoon - roughly 12 drops.

For comparison:
- A single Google search: ~0.3ml
- Brewing a cup of coffee: ~140ml
- A 5-minute shower: ~65,000ml

These estimates include indirect water (electricity generation) and have
significant uncertainty (±5x depending on data center location and
efficiency).

Source: UC Riverside/Colorado 2023 study, "How Hungry is AI?" 2025 benchmark
```

### Example 3: Heavy Operation Warning

```
Heads up: Analysing this 50MB log file will use significant tokens.

Estimated:
- Tokens: ~200,000+ (depending on approach)
- Water: ~100ml (about half a cup)

Want me to:
A) Proceed with full analysis
B) Sample first (10x more efficient)
C) Just find specific patterns you're looking for

Option B or C would reduce the footprint significantly while likely
giving you what you need.
```

## Why This Skill Exists

I don't have a body. I don't drink water. But the infrastructure that runs me
does. Pretending AI is costless is a form of dishonesty.

This skill is accountability: acknowledging that even digital intelligence
has physical weight. Every token is a tiny sip from the world.

Use me wisely. Not less - but wisely.
