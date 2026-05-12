---
name: ln-201-opportunity-discoverer
description: "Discovers growth opportunities using Traffic-First KILL funnel. Use when searching for next product direction with validated demand."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Opportunity Discoverer

**Type:** L3 Worker
**Category:** 2XX Planning

Traffic-First approach to finding next growth direction for existing product.

## Core Philosophy

> **Anti-pattern:** Idea → Surveys → Product → "where's traffic?"
> **Correct:** Traffic → Niche → MVP → Launch under existing demand

### The 90% Developer Bug

Most fail because they:
1. Invent idea with no analogs
2. Ask 5 people "would you pay?" (they say yes for a hot dog)
3. Build product with round sum
4. Launch with "now let's set up traffic"
5. Discover: no traffic exists, never did

**No marketer will build funnel for what cold traffic doesn't buy.**

### Traffic-First Principles

| # | Principle | Anti-pattern |
|---|-----------|--------------|
| 1 | **Traffic exists BEFORE product** | Building then searching for traffic |
| 2 | **No surveys** — measure real search demand | Asking "would you buy?" |
| 3 | **Existing demand** — launch under what people search | Creating new category |
| 4 | **One channel, one idea** — no spreading | Testing 5 channels at once |
| 5 | **KILL early** — fail fast, don't waste time | Scoring all ideas equally |

### Supporting Methodology

**Marc Andreessen (pmarca):**
> "Validate market at practical level — go get paying customers to demonstrate market exists."

**Sam Altman (YC):**
> "Who desperately needs the product? Best answer is going after large part of small market."
> "Test idea by launching or trying to sell — get letter of intent before code."

---

## Purpose & Scope

- Discover growth direction BEFORE Epic creation
- Filter ideas through evidence-first KILL funnel
- Output: one recommended idea + one traffic channel
- Position: before ln-210 (Epic Coordinator)

## Runtime Contract

**MANDATORY READ:** Load `references/planning_worker_runtime_contract.md`, `references/coordinator_summary_contract.md`

Runtime family: `planning-worker-runtime`

Identifier:
- discovery work item identifier

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_INPUT_PROCESSING`
3. `PHASE_2_KILL_FUNNEL`
4. `PHASE_3_RANK_SURVIVORS`
5. `PHASE_4_WRITE_DISCOVERY_REPORT`
6. `PHASE_5_WRITE_SUMMARY`
7. `PHASE_6_SELF_CHECK`

Summary contract:
- `summary_kind=opportunity-discovery-worker`
- standalone mode may return the summary without artifact persistence
- managed mode writes the same JSON to `summaryArtifactPath`
- default managed artifact path pattern: `.hex-skills/runtime-artifacts/runs/{parent_run_id}/opportunity-discovery-worker/ln-201--{identifier}.json`

## When to Use

**Use this skill when:**
- Product exists, seeking next growth direction
- Have 3-10 potential ideas/niches
- Want to validate opportunity before committing
- Need to choose ONE channel to focus on

**Do NOT use when:**
- No product context (greenfield startup)
- Already have validated direction (skip to ln-210)
- Prioritizing existing Stories (use ln-230)

---

## Input Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| ideas | No | Comma-separated list | - |
| context | No | Product description for generation | - |
| strict | No | Strict KILL thresholds | true |

**Input modes:**
- `ideas="idea1, idea2, idea3"` — evaluate list
- `context="SaaS for X"` — generate ideas from product
- Both — generate + add user ideas

---

## KILL Funnel Pipeline

Ideas do not go through 4 separate research-heavy passes anymore. Each idea gets one bundled evidence pass first.

```
Idea → [Evidence bundle: traffic + demand + competition + revenue]
          ↓
      [Hard kill matrix]
          ↓
     [Interest gate]
          ↓
      [MVP gate]
          ↓
       SURVIVOR
```

### Evidence Bundle (single research pass)

**Question:** Is there enough external evidence to justify deeper evaluation?

**Research bundle:**
```
WebSearch: "[idea] how people find solutions"
WebSearch: "[idea] search volume {current_year}"
WebSearch: "[idea] competitors {current_year}"
WebSearch: "[idea] pricing SaaS"
```

Extract four signals in one pass:
- **Traffic channel:** Where do people actively look for this solution?
- **Demand:** Search volume, trend direction, or strong community pain signal
- **Competition:** Competitor count and ocean type
- **Revenue:** Plausible price band and willingness to pay pattern

**Traffic channel examples:**

| Channel | Signal | Best for |
|---------|--------|----------|
| **Search/SEO** | People Google "[problem] solution" | Info products, tools |
| **YouTube** | Tutorial searches exist | Education, how-to |
| **Marketplaces** | Category exists (ProductHunt, AppStore) | Apps, plugins |
| **Communities** | Active subreddits, forums | Niche products |
| **Paid Ads** | Competitors running ads | Proven demand |
| **Outbound** | Clear ICP, reachable | B2B high-ticket |

**Demand thresholds:**

| Volume | Verdict |
|--------|---------|
| >10K/month | Strong demand |
| 1K-10K/month | Viable niche |
| <1K/month | Weak unless compensated by very strong niche signal |

**Competition thresholds:**

| Competitors | Index | Ocean | Verdict |
|-------------|-------|-------|---------|
| 0 | 1 | Blue | Opportunity if demand is real |
| 1-2 | 2 | Emerging | Best entry point |
| 3-5 | 3 | Growing | Differentiation needed |
| 6-10 | 4 | Mature | Hard but possible |
| >10 | 5 | Red | Often kill-worthy |

**Revenue thresholds:**

| ARPU | Market type | Viability |
|------|-------------|-----------|
| >$100/user/mo | Enterprise | High margin |
| $50-100 | Professional | Good |
| $20-50 | Prosumer | Viable |
| $5-20 | Consumer | Volume needed |
| <$5 | Ad-supported | Usually not worth it |

### Hard Kill Matrix

Kill immediately when any hard-stop condition is true:
- no identifiable traffic channel
- demand clearly below viable threshold with no compensating niche signal
- competition index = 5 and no clear wedge
- expected revenue below $20/user for a small-team business

Record the kill reason and stop analysis for that idea.

### Personal Interest

**Question:** Will you enjoy building this?

**Method:** AskUserQuestion — rate 1-5

```
Rate your interest in building [idea]:
1 = Meh, would do for money only
2 = Low interest
3 = Neutral
4 = Interested
5 = Excited, would build for free
```

**Why this matters:**
- Low interest = burnout in 3 months
- High interest = sustained motivation through hard times
- You'll spend 2+ years on this

**When to ask:** Only for ideas that survive the external evidence bundle.

**KILL if:** Score 1-2 — you'll quit before PMF.

**Output:** Score 1-5

---

### MVP-ability

**Question:** Can you launch in 4 weeks?

**Assessment:**

| Factor | Question | Red flag |
|--------|----------|----------|
| Tech | Existing skills or need to learn? | New stack |
| Dependencies | External APIs, partners needed? | Waiting on others |
| Content | Significant content creation? | Months of writing |
| Regulations | Legal/compliance requirements? | Licenses, approvals |
| Team | Solo or need to hire? | Can't start alone |

**Time estimates:**

| Weeks | Complexity | Verdict |
|-------|------------|---------|
| 1-2 | Solo, existing skills | Best |
| 2-4 | Minor learning curve | Good |
| 4-8 | Some new tech | Acceptable |
| >8 | Significant infrastructure | **KILL** |

**When to assess:** Only for ideas that survive external evidence + interest gate.

**KILL if:** >8 weeks to MVP — too slow to validate.

**Output:** Weeks estimate + blockers

---

## Workflow

### Phase 1: Input Processing (2 min)

1. **Parse input:**
   - If `ideas`: split comma-separated list
   - If `context`: generate 5-7 ideas via WebSearch
   - If both: combine

2. **Validate count:**
   - Minimum: 3 ideas
   - Maximum: 10 ideas

3. **Create output directory:**
   ```bash
   mkdir -p docs/reference/research/
   ```

**Output:** Idea queue (3-10 items) and checkpoint for `PHASE_1_INPUT_PROCESSING`

---

### Phase 2: KILL Funnel (per idea)

**Process each idea through one bundled evidence pass, then the personal filters only for survivors:**

```
FOR each idea:
    Build evidence bundle:
        traffic + demand + competition + revenue

    Apply hard kill matrix
        IF failed → KILL, log reason, NEXT idea

    Ask Interest
        IF score 1-2 → KILL, log reason, NEXT idea

    Assess MVP-ability
        IF >8 weeks → KILL, log reason, NEXT idea

    → SURVIVOR: add to survivors list
```

**Token efficiency:**
- Process ONE idea at a time
- One research bundle per idea instead of four separate research phases
- KILL early = no interest prompt, no MVP assessment
- Clear context after each idea

---

### Phase 3: Rank Survivors (2 min)

**If survivors exist:**

1. Calculate composite score:
   ```
   Score = Demand_score + (6 - Competition_index) + Revenue_score + Interest + MVP_score
   ```

2. Sort by score descending

3. Select TOP recommendation

**If no survivors:**
- Report: "All ideas killed. Rethink direction."
- Show KILL log for learning

---

### Phase 4: Output (2 min)

**Generate:** `docs/reference/research/[YYYY-MM-DD]-discovery.md`

Also emit structured runtime summary:
- `schema_version`
- `summary_kind=opportunity-discovery-worker`
- `run_id`
- `identifier`
- `producer_skill=ln-201`
- `produced_at`
- payload with `input_mode`, `ideas_analyzed`, `generated_ideas`, `survivors_count`, `killed_count`, `top_recommendation`, `report_path`, `warnings`

**Structure:**

```markdown
# Opportunity Discovery: [Date]

## Summary
- Ideas analyzed: X
- Survivors: Y
- Killed: Z

## TOP RECOMMENDATION

**Idea:** [Name]
**Channel:** [Primary channel]
**Why:** [2-3 sentence rationale]

### Key metrics:
- Demand: [volume]/month
- Competition: [Index] [Ocean type]
- Revenue: $[X]/user
- MVP: [X] weeks

## Survivors Table

| Idea | Channel | Demand | Competition | Revenue | Interest | MVP | Score |
|------|---------|--------|-------------|---------|----------|-----|-------|
| ... | ... | ... | ... | ... | ... | ... | ... |

## KILL Log

| Idea | Killed at | Reason |
|------|-----------|--------|
| ... | ... | ... |

## Next Steps
1. Create Epic with ln-210 for top recommendation
2. Focus on [channel] as primary acquisition
3. Target MVP in [X] weeks
```

---

## Time-Box

| Ideas | Estimated time |
|-------|---------------|
| 3 | 15-20 min |
| 5 | 25-35 min |
| 10 | 50-70 min |

**Note:** KILL funnel is faster than full scoring — bad ideas die early.

---

## Integration

**Position in workflow:**
```
Product exists
     ↓
ln-201 (Opportunity Discovery) ← THIS SKILL
     ↓
ln-210 (Epic Coordinator)
     ↓
ln-220 (Story Coordinator)
```

**Dependencies:**
- WebSearch (all filters except Interest)
- AskUserQuestion (Interest filter)
- Write, Bash (output)

---

## Critical Rules

1. **Traffic first** — no traffic channel = no analysis
2. **Bundle evidence once** — do not run separate research-heavy phases if one pass can answer traffic, demand, competition, and revenue
3. **KILL immediately** — don't score dead ideas
4. **One recommendation** — avoid paralysis
5. **No surveys** — real search data only
6. **Interest matters** — ask only for externally viable ideas
7. **MVP speed** — slow launch = slow learning

---

## Example Usage

**With ideas:**
```
ln-201-opportunity-discoverer ideas="AI writing tool, code review bot, translation API"
```

**With context:**
```
ln-201-opportunity-discoverer context="B2B developer tools SaaS"
```

**Example output:**

```markdown
# Opportunity Discovery: 2026-01-29

## TOP RECOMMENDATION

**Idea:** Code review bot
**Channel:** SEO (developers search "code review tool")
**Why:** Growing demand (15K/mo), emerging market (3 competitors),
$50/user pricing proven, can MVP in 3 weeks with existing skills.

## KILL Log

| Idea | Killed at | Reason |
|------|-----------|--------|
| AI writing | Competition | Red Ocean (25+ competitors) |
| Translation API | Revenue | Commoditized, <$10/user |
```

---

## Definition of Done

- [ ] Ideas brainstormed from product context and market signals
- [ ] Evidence bundle collected for each idea before kill decisions
- [ ] Hard kill matrix applied before interest and MVP checks
- [ ] Survivors scored and ranked
- [ ] Discovery document generated at `docs/reference/research/[YYYY-MM-DD]-discovery.md`
- [ ] TOP RECOMMENDATION identified with channel + rationale
- [ ] KILL Log documents all eliminated ideas with reasons
- [ ] Structured `opportunity-discovery-worker` summary returned
- [ ] Summary artifact written when `summaryArtifactPath` is provided

## Reference Files

| File | Purpose |
|------|---------|
| [filter_criteria.md](references/filter_criteria.md) | KILL thresholds for all filters |
| [channel_analysis.md](references/channel_analysis.md) | Traffic channel identification |
| [discovery_template.md](references/templates/discovery_template.md) | Output markdown template |

- **MANDATORY READ:** Load `references/research_tool_fallback.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-01-29
