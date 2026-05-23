---
name: generate-story-bank
description: Generate interview-ready stories using HPARL format (Hook, Principles, Action, Results, Learnings). Transforms achievements into compelling narratives for behavioral interviews.
---

# Generate Story Bank

<purpose>
Transform achievements into interview-ready stories using the HPARL framework — designed to be more engaging than STAR for senior PM interviews.
</purpose>

<when_to_activate>
Activate when:
- User wants to prepare for behavioral interviews
- User says "generate stories", "story bank", "interview prep"
- Transforming achievements into HPARL format
- Building the 10-15 story bank recommended for senior interviews

**Trigger phrases:** "story bank", "interview prep", "behavioral stories", "HPARL", "interview stories"
</when_to_activate>

## HPARL vs STAR

| STAR | HPARL | Why HPARL Wins |
|------|-------|----------------|
| Situation | **Hook** | Promises the answer, creates curiosity |
| (missing) | **Principles** | Shows your thinking, not just actions |
| Task + Action | **Action** | What you specifically did (use "I") |
| Result | **Results** | Quantified outcomes (multiple if possible) |
| (missing) | **Learnings** | Shows growth mindset, self-awareness |

**The key insight**: STAR tells what happened. HPARL shows how you think.

---

## The HPARL Format

### 1. Hook (10-15 seconds)
Promise the interviewer you'll answer their question AND make them want to listen.

**Bad hook**: "At Anchorage, I worked on ETH staking infrastructure."
**Good hook**: "I'll tell you about the time we had $2B in staked ETH and I had to ensure we never lost a single dollar to slashing — while shipping 8 new protocols in parallel."

**Formula**: Stakes + constraint + tease of outcome

### 2. Principles (30 seconds)
Your philosophy or approach that guided the work. This is where you show judgment.

**Example**: "My principle with infrastructure products is that reliability is the feature — users don't notice when things work, they only notice when things break. So I always over-invest in redundancy before we need it, not after we've had an incident."

**Formula**: "I believe..." or "My approach to X is..." + why

### 3. Action (60-90 seconds)
What YOU specifically did. Use "I", not "we". Be concrete.

**Structure**:
- First, I...
- Then, I...
- The key decision was...

**Include**:
- Concrete actions you took
- Decisions you made (and why)
- Trade-offs you navigated
- How you worked with others (but your role)

### 4. Results (30 seconds)
Quantified outcomes. Multiple metrics if possible.

**Structure**:
```
Primary metric: [X outcome]
Secondary metric: [Y outcome]
Business impact: [What it meant for the company]
```

**Example**: "Zero slashing events across 18 months. Galaxy, Grayscale, and other institutions trusted us with their staking. We grew from $X to $Y in staked assets."

### 5. Learnings (15-30 seconds)
What you took away. Shows self-awareness and growth mindset.

**Formula**: "The counterintuitive insight was..." or "What I learned was..."

**Example**: "The counterintuitive insight was that slower deployments meant faster growth. Institutions needed to see months of perfect operation before committing significant capital. Velocity isn't always the right metric."

---

## Story Bank Target

You need **10-15 stories** that cover different behavioral question types:

| Category | # Stories | Question Types |
|----------|-----------|----------------|
| Leadership | 2-3 | "Tell me about a time you led...", "Describe a difficult team situation" |
| Conflict/Influence | 2-3 | "Tell me about a disagreement...", "How do you handle pushback?" |
| Failure/Learning | 2-3 | "Tell me about a mistake...", "What would you do differently?" |
| Technical Challenge | 2-3 | "Describe a complex technical problem...", "How do you make trade-offs?" |
| Impact/Achievement | 2-3 | "What's your biggest accomplishment?", "Tell me about something you built" |
| Ambiguity/Prioritization | 2-3 | "How do you handle competing priorities?", "Tell me about unclear requirements" |

---

## Generation Process

### Step 1: Select Achievement

**First, check competency coverage** to understand what stories you need:
```bash
npm run check:coverage
```

This shows which of the 7 PM bundles are covered vs gaps. Target stories that fill gaps.

**Search for achievements by theme:**
```bash
# Find leadership stories
npm run search:evidence -- --terms "led,managed,cross-functional,team"

# Find technical stories
npm run search:evidence -- --terms "architecture,api,system,infrastructure"

# Find impact/growth stories
npm run search:evidence -- --terms "revenue,growth,launched,shipped"
```

**Or list all achievements:**
```bash
ls content/knowledge/achievements/
```

Choose achievements that:
- Have strong quantified outcomes
- Demonstrate judgment (decisions, trade-offs)
- Show your personal contribution
- Cover different story categories
- **Fill gaps identified by check:coverage**

### Step 2: Transform to HPARL

For each achievement, generate:

```yaml
# content/knowledge/stories/{achievement-id}.hparl.yaml
id: "{achievement-id}-hparl"
sourceAchievement: "{achievement-id}"
format: "HPARL"
lastUpdated: "YYYY-MM-DD"

# ───────────────────────────────────────────────────────────────
# THE STORY
# ───────────────────────────────────────────────────────────────
hook: |
  [10-15 second attention grabber with stakes and constraint]

principles: |
  [Your philosophy/approach that guided this work]

action:
  - "[First concrete action you took]"
  - "[Second action - key decision point]"
  - "[Third action - how you worked with others]"
  - "[Fourth action - trade-off you navigated]"

results:
  - metric: "[Primary outcome]"
    context: "[Why this matters]"
  - metric: "[Secondary outcome]"
    context: "[Business impact]"

learnings: |
  [The counterintuitive insight or what you'd do differently]

# ───────────────────────────────────────────────────────────────
# INTERVIEW MAPPING
# ───────────────────────────────────────────────────────────────
goodFor:
  - "[Question type 1 this answers well]"
  - "[Question type 2]"
  - "[Question type 3]"

categories:
  - leadership          # Which category bucket
  - technical-challenge

# ───────────────────────────────────────────────────────────────
# PRACTICE NOTES
# ───────────────────────────────────────────────────────────────
timing:
  hook: "15s"
  principles: "30s"
  action: "90s"
  results: "30s"
  learnings: "15s"
  total: "3 minutes"

practiceNotes: |
  [Personal notes on what to emphasize, what to skip, common follow-ups]
```

### Step 3: Validate Coverage

After generating stories, check coverage:

```yaml
storyBankCoverage:
  leadership:
    count: 3
    stories: ["eth-staking-hparl", "l2-integrations-hparl", "team-conflict-hparl"]
  conflict:
    count: 2
    stories: ["stakeholder-alignment-hparl", "technical-pushback-hparl"]
  failure:
    count: 2
    stories: ["launch-delay-hparl", "wrong-architecture-hparl"]
  technical:
    count: 3
    stories: ["eth-staking-hparl", "ankr-api-hparl", "xbox-blockchain-hparl"]
  impact:
    count: 3
    stories: ["ankr-15x-hparl", "eth-staking-hparl", "xbox-blockchain-hparl"]
  ambiguity:
    count: 2
    stories: ["forte-pivot-hparl", "mempools-startup-hparl"]

  totalStories: 12
  gaps: []  # Categories with <2 stories
  recommendation: "Coverage looks good. Consider adding 1 more failure story."
```

---

## Example Transformation

### Source Achievement (STAR format)
```yaml
id: eth-staking-zero-slashing
headline: "Zero slashing events across $2B+ in staked ETH"
situation: |
  Anchorage needed ETF-grade staking infrastructure...
task: |
  Lead validator architecture and client partnerships...
action: |
  Designed multi-cloud failover, built compliance dashboard...
result: |
  Zero slashing, Galaxy/Grayscale onboarded, $2B staked...
```

### Generated HPARL Story
```yaml
id: eth-staking-zero-slashing-hparl
sourceAchievement: eth-staking-zero-slashing
format: HPARL

hook: |
  I'll tell you about the time we had $2B in staked ETH across
  institutional clients like Galaxy and Grayscale, and I had to
  ensure we never lost a single dollar to slashing while shipping
  8 new protocol integrations in parallel.

principles: |
  My principle with infrastructure products is that reliability IS
  the feature. Users don't notice when things work perfectly—they
  only notice when things break. So I always over-invest in
  redundancy before we need it, not after an incident forces us to.

action:
  - "I designed a validator orchestration system across 3 cloud providers with automated failover—if AWS went down, we'd be on GCP in under 30 seconds"
  - "I built a compliance dashboard for institutional clients so they could see real-time attestation health, which became a key sales differentiator"
  - "I partnered with our security team to implement multi-sig key management that satisfied SOC2 requirements while maintaining operational speed"
  - "The hardest trade-off was choosing reliability over velocity—I pushed back on rushing new protocol launches until our monitoring was bulletproof"

results:
  - metric: "Zero slashing events"
    context: "across 18 months of operation with $2B+ staked"
  - metric: "Galaxy, Grayscale, and 5 other institutions"
    context: "trusted us with their ETH staking"
  - metric: "8 new protocols integrated"
    context: "while maintaining zero-incident track record"

learnings: |
  The counterintuitive insight was that slower deployments meant
  faster growth. Institutions needed to see months of perfect
  operation before committing significant capital. What looked
  like over-engineering to internal stakeholders was actually
  the fastest path to enterprise trust.

goodFor:
  - "Tell me about a time you built something reliable"
  - "How do you handle pressure to ship faster?"
  - "Describe a technical leadership challenge"
  - "Tell me about working with enterprise clients"

categories:
  - technical-challenge
  - leadership
  - impact

timing:
  total: "2.5-3 minutes"
```

---

## Quality Checklist

Before marking a story complete:

- [ ] Hook creates genuine curiosity (stakes + constraint + tease)
- [ ] Principles show YOUR thinking, not generic PM advice
- [ ] Actions use "I" not "we" — your specific contribution is clear
- [ ] Results have at least 2 quantified metrics
- [ ] Learnings show self-awareness (what you'd do differently OR counterintuitive insight)
- [ ] Story maps to at least 2 question types
- [ ] Total timing is 2-3 minutes when spoken
- [ ] You could defend every claim in a follow-up question

---

## File Locations

| File | Purpose |
|------|---------|
| `content/knowledge/achievements/*.yaml` | Source achievements (STAR format) |
| `content/knowledge/stories/*.hparl.yaml` | Interview-ready stories (HPARL format) |
| `content/knowledge/stories/_template.yaml` | Original story template |
| `content/knowledge/stories/_template.hparl.yaml` | HPARL story template |

---

## Commands

```bash
# ═══════════════════════════════════════════════════════════════
# STEP 1: Check what competencies need stories
# ═══════════════════════════════════════════════════════════════
npm run check:coverage           # Show gaps in 7 PM bundles
npm run check:coverage -- --json # JSON output for processing

# ═══════════════════════════════════════════════════════════════
# STEP 2: Search for relevant achievements
# ═══════════════════════════════════════════════════════════════
npm run search:evidence -- --terms "leadership,cross-functional"
npm run search:evidence -- --terms "technical,architecture,api"
npm run search:evidence -- --terms "revenue,growth,impact"

# ═══════════════════════════════════════════════════════════════
# STEP 3: List source files
# ═══════════════════════════════════════════════════════════════
ls content/knowledge/achievements/
ls content/knowledge/stories/*.hparl.yaml
```
