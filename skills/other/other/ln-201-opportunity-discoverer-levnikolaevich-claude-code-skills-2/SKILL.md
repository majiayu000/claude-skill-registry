---
name: ln-201-opportunity-discoverer
description: "Discovers growth opportunities using Traffic-First KILL funnel. Use when searching for next product direction with validated demand."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

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
- Filter ideas through sequential KILL funnel
- Output: one recommended idea + one traffic channel
- Position: before ln-210 (Epic Coordinator)

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

Ideas pass through 6 sequential filters. **Fail any filter = KILL immediately.**

```
Idea → [Traffic?] → [Demand?] → [Competition?] → [Revenue?] → [Interest?] → [MVP?] → SURVIVOR
              ↓           ↓            ↓             ↓            ↓           ↓
            KILL        KILL         KILL          KILL         KILL        KILL
```

### Filter 1: Traffic Channel

**Question:** Where do people look for this solution?

**Research:**
```
WebSearch: "[idea] how people find solutions"
WebSearch: "[idea] customer acquisition channels"
```

**Valid channels:**

| Channel | Signal | Best for |
|---------|--------|----------|
| **Search/SEO** | People Google "[problem] solution" | Info products, tools |
| **YouTube** | Tutorial searches exist | Education, how-to |
| **Marketplaces** | Category exists (ProductHunt, AppStore) | Apps, plugins |
| **Communities** | Active subreddits, forums | Niche products |
| **Paid Ads** | Competitors running ads | Proven demand |
| **Outbound** | Clear ICP, reachable | B2B high-ticket |

**KILL if:** No identifiable channel where people actively look for solution.

**Output:** Channel name + rationale

---

### Filter 2: Existing Demand

**Question:** Are people already searching for this?

**Research:**
```
WebSearch: "[idea] search volume {current_year}"
WebSearch: "[idea] Google Trends"
WebSearch: "[problem] forum discussions reddit"
```

**Demand signals:**

| Signal | Source | Interpretation |
|--------|--------|----------------|
| Search volume | Google Keyword Planner, Ahrefs | Direct demand |
| Trend direction | Google Trends | Growing/declining |
| Forum activity | Reddit, HackerNews, StackOverflow | Pain level |
| Competitor traffic | SimilarWeb, SEMrush | Market size |

**KILL thresholds:**

| Volume | Verdict |
|--------|---------|
| >10K/month | Strong demand |
| 1K-10K/month | Viable niche |
| <1K/month | **KILL** — insufficient demand |

**Output:** Monthly volume estimate + trend

---

### Filter 3: Competition (Blue/Red Ocean)

**Question:** Can we enter this market?

**Research:**
```
WebSearch: "[idea] competitors {current_year}"
WebSearch: "[idea] alternatives comparison"
```

**Classification:**

| Competitors | Index | Ocean | Verdict |
|-------------|-------|-------|---------|
| 0 | 1 | Blue | Opportunity (validate demand exists) |
| 1-2 | 2 | Emerging | Best entry point |
| 3-5 | 3 | Growing | Differentiation needed |
| 6-10 | 4 | Mature | Hard but possible |
| >10 | 5 | Red | **KILL** — commoditized |

**KILL if:** Index 5 (Red Ocean) — too many competitors, race to bottom.

**Output:** Competitor count + Ocean type

---

### Filter 4: Revenue Potential

**Question:** Will people pay enough?

**Research:**
```
WebSearch: "[idea] pricing SaaS"
WebSearch: "[competitor] pricing plans"
WebSearch: "[idea] willingness to pay"
```

**Revenue indicators:**

| ARPU | Market type | Viability |
|------|-------------|-----------|
| >$100/user/mo | Enterprise | High margin |
| $50-100 | Professional | Good |
| $20-50 | Prosumer | Viable |
| $5-20 | Consumer | Volume needed |
| <$5 | Ad-supported | **KILL** |

**KILL if:** <$20/user — not worth the effort for small team.

**Output:** Estimated $/user + pricing model

---

### Filter 5: Personal Interest

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

**KILL if:** Score 1-2 — you'll quit before PMF.

**Output:** Score 1-5

---

### Filter 6: MVP-ability

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

**Output:** Idea queue (3-10 items)

---

### Phase 2: KILL Funnel (per idea)

**Process each idea sequentially through all 6 filters:**

```
FOR each idea:
    Filter 1: Traffic Channel
        IF no channel → KILL, log reason, NEXT idea

    Filter 2: Existing Demand
        IF <1K/month → KILL, log reason, NEXT idea

    Filter 3: Competition
        IF Index 5 → KILL, log reason, NEXT idea

    Filter 4: Revenue
        IF <$20/user → KILL, log reason, NEXT idea

    Filter 5: Interest
        AskUserQuestion for rating
        IF score 1-2 → KILL, log reason, NEXT idea

    Filter 6: MVP-ability
        IF >8 weeks → KILL, log reason, NEXT idea

    → SURVIVOR: add to survivors list
```

**Token efficiency:**
- Process ONE idea at a time
- KILL early = less research needed
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
2. **KILL immediately** — don't score dead ideas
3. **One recommendation** — avoid paralysis
4. **No surveys** — real search data only
5. **Interest matters** — you'll quit if bored
6. **MVP speed** — slow launch = slow learning

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
- [ ] KILL funnel applied: each idea passed/killed at each filter stage
- [ ] Survivors scored and ranked
- [ ] Discovery document generated at `docs/reference/research/[YYYY-MM-DD]-discovery.md`
- [ ] TOP RECOMMENDATION identified with channel + rationale
- [ ] KILL Log documents all eliminated ideas with reasons

## Reference Files

| File | Purpose |
|------|---------|
| [filter_criteria.md](references/filter_criteria.md) | KILL thresholds for all filters |
| [channel_analysis.md](references/channel_analysis.md) | Traffic channel identification |
| [discovery_template.md](references/discovery_template.md) | Output markdown template |

- **MANDATORY READ:** `shared/references/research_tool_fallback.md`

---

**Version:** 2.0.0
**Last Updated:** 2026-01-29
