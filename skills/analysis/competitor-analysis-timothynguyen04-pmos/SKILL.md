---
name: competitor-analysis
description: Deep competitive analysis + ongoing monitoring. Checks user research for competitor mentions, sales notes, existing analysis. Integrates with retention-analysis and user-research-synthesis.
disable-model-invocation: false
user-invocable: true
---

# /competitor-analysis - Strategic Competitive Intelligence

Two modes: **Deep Analysis** (comprehensive one-time research) + **Ongoing Monitoring** (weekly/monthly tracking)

## Quick Start

1. Name the competitor(s) you want to analyze
2. Choose mode: **Deep Analysis** (full research) or **Ongoing Monitoring** (monthly check-in)
3. I check your workspace first -- user research, meeting notes, churn data, past analysis
4. I show what we already know, identify gaps, then fill gaps with web research
5. I deliver a strategic report with defensive, offensive, and innovative plays

**Example:** "Analyze Competitor X -- we're losing enterprise deals to them"

**Output:** `outputs/research-synthesis/competitor-analysis-[name]-[date].md`

**Time:** Deep Analysis: 2-4 hours | Monitoring: 30 min/month

## Context Routing Logic (Internal - for Claude)

**Automatic Context Checks:**
When this skill is invoked, immediately check:

| Source | Files/Folders | Search Terms | What to Extract |
|--------|---------------|--------------|-----------------|
| User Research | `context-library/research/*.md` | competitor name, "switched to", "chose", "vs [competitor]", "competitor" | Customer quotes, pain points, feature comparisons |
| Existing Analysis | `context-library/research/competitive-*.md` | competitor name | Past findings, dates, trends, avoid duplication |
| Meeting Notes | `context-library/meetings/*.md` | competitor name, "lost deal", "churn", sales, CS | Sales losses, CS feedback, win/loss patterns |
| PRDs | `context-library/prds/*.md` | competitor name, "competitive", "positioning" | Feature decisions, positioning rationale |
| Strategy | `context-library/strategy/*.md` | competitor name, "positioning", "differentiation" | Strategic context, counter-positioning |
| Metrics | `context-library/metrics/*.md` | "churn", "retention", competitor name | Churn to competitors, competitive benchmarks |

**Context Priority:**
1. Internal context FIRST (user research, meetings, PRDs)
2. Analytics MCP SECOND (if connected - query churn cohorts)
3. Web search LAST (only for gaps not covered by internal intel)

**Cross-Skill Links:**
- If churn mentioned → Link to `retention-analysis`
- If user feedback → Link to `user-research-synthesis`
- If positioning mentioned → Link to `write-prod-strategy`

---

## Step 0: Understanding What We Already Know

Before diving into research, let me check what competitive intelligence already exists in your workspace...

**Checking:**
- `context-library/research/` for user interviews mentioning competitors
- `context-library/research/competitive-*.md` for past competitive analysis
- `context-library/meetings/` for sales/CS notes with competitive intel
- `context-library/prds/` for competitive positioning decisions
- `context-library/strategy/` for strategic context
- `context-library/metrics/` for churn data

**[If analytics MCP connected]:** "Let me also query [Amplitude/Mixpanel] for churn patterns and competitor-related data."

**Based on what I find, I'll show you:**

### Internal Intelligence Summary

**From User Research:**
- [List interviews mentioning competitors with quotes]
- Example: "Found 4 interviews mentioning Competitor X: 'We switched because...'"

**From Sales/CS Meetings:**
- [List competitive losses and patterns]
- Example: "3 sales calls lost to Competitor Y in Enterprise segment"

**From Existing Analysis:**
- [Reference past competitive analysis]
- Example: "Last analyzed Competitor X on 2024-08-15 (6 months ago). Key finding: [summary]"

**From PRDs:**
- [Features built in response to competitors]
- Example: "PRD-2024-03 added Feature Z to match Competitor positioning"

**From Strategy Docs:**
- [Strategic positioning context]
- Example: "Your strategy positions you as [X] vs competitors who are [Y]"

**From Metrics/Analytics:**
- [Churn data, if available]
- Example: "20% of churned customers mentioned Competitor X as reason"

### Gaps in Knowledge

Based on internal context, we **don't yet know:**
- [Gap 1]: Recent product updates from Competitor X
- [Gap 2]: Current pricing model for Competitor Y
- [Gap 3]: Distribution channels for Competitor Z

**Should I fill these gaps with web research, or do you want to provide additional context first?**

---

## Step 1: Choose Your Analysis Mode

Based on your objective and existing context:

### Deep Analysis Mode

**Use when:**
- Entering a new market or launching major feature
- Significant shift in competitive landscape
- Need to inform strategic decision (roadmap, pricing, positioning)
- Preparing for funding/board presentation
- Haven't done competitive research in 6+ months

**What I'll do:**
1. **Internal Intelligence First** - Synthesize what we already know
2. **Gap Analysis** - Identify missing information
3. **Web Research** - Fill gaps with public data (websites, pricing, reviews)
4. **SWOT Analysis** - Per competitor
5. **Positioning Map** - Visual 2x2 showing market space
6. **Strategic Recommendations** - Roadmap, pricing, GTM implications

**Time:** 2-4 hours (depending on number of competitors)

**Output:** Comprehensive report saved to `outputs/research-synthesis/competitor-analysis-[date].md`

### Ongoing Monitoring Mode

**Use when:**
- You already have baseline competitive analysis
- Want to track competitor moves over time
- Need regular intel updates (monthly check-ins)

**What I'll do:**
1. **Monthly Check-in** - Search competitor mentions in user feedback
2. **Feature Tracking** - Monitor features appearing in customer requests
3. **Win/Loss Trends** - Track patterns via sales team
4. **Update Matrix** - Keep feature comparison current
5. **Alert on Major Moves** - Flag significant changes

**Time:** 30 minutes/month

**Output:** Updates saved to `outputs/research-synthesis/competitive-intel-[month].md`

---

## Deep Analysis Mode: PM-Specific Questions

Instead of generic "Who are your competitors?", I'll ask:

### Question 1: Competitive Context
**"Which competitors appear most frequently in your user research or churn interviews?"**

This tells me who actually threatens your business (not just who you think competes with you).

### Question 2: Customer Segment
**"Where do competitors win with your target customer segment?"**

Focus on specific segments, not broad "they have more features."

Examples:
- "Competitor X dominates with enterprise IT buyers because..."
- "SMB customers choose Competitor Y because..."

### Question 3: Churn Reasons
**"What do churned customers say about why they picked competitors?"**

Pull from actual customer interviews, not assumptions.

### Question 4: Distribution Advantage
**"Where does Competitor X have stronger distribution/presence?"**

Examples:
- Geographic presence
- Channel partnerships
- Integration ecosystem
- Community/network effects

### Question 5: Lost Segments
**"What customer segments are you losing to specific competitors?"**

Be specific: "Enterprise healthcare" not "big companies"

---

## Deep Analysis Framework

Once I understand the competitive landscape from internal intel + your answers:

### Phase 1: Synthesize Internal Intelligence (15 min)

I'll create a report showing:

**What We Already Know:**
- User quotes about competitors
- Sales losses and why
- Features we built to compete
- Strategic positioning decisions
- Churn patterns

**What We Don't Know:**
- [Gaps requiring web research]

### Phase 2: Gather Missing Intelligence (60-90 min)

For each gap, I'll guide you through:

#### Public Data Collection
- Website positioning analysis
- Pricing page breakdown
- Product trial/demo walkthrough
- Marketing messaging audit

#### Customer Intelligence
- G2/Capterra review synthesis
- Reddit/Twitter sentiment analysis
- App store feedback patterns

#### Strategic Signals
- LinkedIn hiring patterns (what they're building)
- Funding announcements
- Partnership deals
- Executive changes

### Phase 3: Synthesize with Frameworks (30 min)

#### SWOT Analysis (Per Competitor)

```markdown
## Competitor: [Name]

### Strengths
- [What they do exceptionally well]
- [Their sustainable advantages]
- **Example from your data:** "User Interview 2024-08-15: 'Their onboarding is 10x faster'"

### Weaknesses
- [Where they consistently fall short]
- [Common customer complaints]
- **Example from your data:** "G2 reviews: 70% mention poor customer support"

### Opportunities (for us)
- [Gaps we can exploit]
- **Example:** "30% of their users want Feature X but they don't offer it"

### Threats (from them)
- [What they could do to hurt us]
- **Example:** "Partnership with Salesforce could lock us out of enterprise"
```

#### Positioning Map

I'll create a 2x2 visualization:

```
Complexity (Simple → Enterprise)
        │
  You  │         Competitor A
        │
────────┼────────────  Price (Low → High)
        │
  Comp B│    Competitor C
        │

Your opportunity: [Identify white space]
```

#### Feature Comparison Matrix

```markdown
| Feature | Your Product | Comp A | Comp B | Analysis |
|---------|--------------|--------|--------|----------|
| [Core Feature 1] | ✅ | ✅ | ✅ | Table stakes |
| [Your Advantage] | ✅ | ⚠️ Limited | ❌ | Differentiator |
| [Gap] | ❌ | ✅ | ✅ | Consider building |

**Legend:**
- ✅ Full support
- ⚠️ Limited/beta
- ❌ Not available
```

### Phase 4: Strategic Recommendations (30 min)

I'll categorize insights into 3 buckets:

#### 🛡️ Defensive Plays (Close Critical Gaps)

```markdown
**Feature:** [What to build]
**Why:** Competitor has it, customers expect it, blocking deals
**User Story:** "As a [user], I want [feature] so that [outcome]"
**Priority:** High
**Effort:** [Estimate]
**Link to PRD:** [If exists]
```

#### ⚔️ Offensive Plays (Attack Weaknesses)

```markdown
**Opportunity:** [Competitor weakness from customer complaints]
**Our Advantage:** [How we can do it better]
**Impact:** [Market share we can capture]
**Evidence:** [Quote from user research or reviews]
```

#### 🚀 Innovative Plays (Create New Market Space)

```markdown
**Gap:** [What no competitor is doing]
**Hypothesis:** [Why customers would care]
**Risk:** [Why no one else has done this]
**Validation Plan:** [How to test before building]
```

### Phase 5: Positioning & Pricing Guidance (15 min)

#### Value Proposition Framework

```markdown
**For:** [Target customer]
**Who:** [Their pain or need]
**Our product is a:** [Category]
**That:** [Key benefit]
**Unlike:** [Main competitor]
**We:** [Key differentiator]
```

#### Pricing Recommendations

Based on competitive benchmarks:
- Market pricing range
- Where you're positioned
- Opportunity for price increase or new tier

---

## Ongoing Monitoring Mode: Setup

Instead of complex Make.com automation, I'll help you set up:

### Monthly Competitive Check-in (30 min/month)

**Week 1 of Month:**

1. **Search User Feedback**
   - Review latest interviews for competitor mentions
   - Check support tickets for "switching to" mentions
   - Scan feature requests citing competitors

2. **Sales Team Intel**
   - Ask: "Which competitors came up this month?"
   - Review win/loss log
   - Track deal-loss reasons

3. **Web Monitoring**
   - Check competitor blogs for product updates
   - Scan LinkedIn for major hires
   - Google Alerts for funding/partnership news

4. **Update Tracking**
   - Update feature comparison matrix
   - Note pricing changes
   - Log significant moves

**Output Format:**

```markdown
# Competitive Intel: [Month YYYY]

## Summary
- [1-2 sentence summary of significant changes]

## Competitor Updates

### Competitor A
- **Product:** [New features or changes]
- **Pricing:** [Any changes]
- **Strategic Moves:** [Partnerships, funding, hires]
- **Customer Mentions:** [Quotes from your research]

### Competitor B
[Same structure]

## Implications for Our Roadmap
- **Defensive:** [Gaps we need to close]
- **Offensive:** [Weaknesses we can exploit]
- **Monitoring:** [Things to watch]

## Action Items
- [ ] [Action 1 with owner]
- [ ] [Action 2 with owner]
```

Save to: `outputs/research-synthesis/competitive-intel-[month].md`

### Optional: Google Alerts Setup

I can help you set up:
- Competitor name + "funding"
- Competitor name + "acquires"
- Competitor name + "announces"
- Competitor name + "launches"

---

## Output Integration

### Where Files Go

**Deep Analysis:**
- Active work: `outputs/research-synthesis/competitor-analysis-[name]-[date].md`
- When finalized: Move to `context-library/research/` for future reference

**Ongoing Monitoring:**
- Save directly to: `outputs/research-synthesis/competitive-intel-[month].md`

### Link to Other Work

After completing analysis:
- **Reference in PRDs** - "Based on competitive analysis [link], we're positioning as..."
- **Update strategy docs** - "Competitive landscape has shifted: [insight]"
- **Create battlecards** - Use findings for sales team (via `/slack-message`)
- **Inform roadmap** - Link specific competitor threats to roadmap priorities

### Cross-Skill Integration

**Feeds into:**
- `/prd-draft` - Auto-populate "Market Context" and "Alternatives Considered"
- `/write-prod-strategy` - Inform competitive positioning and differentiation
- `/retention-analysis` - Understand churn to competitors
- `/user-research-synthesis` - Reference competitive mentions in interviews

**Pulls from:**
- `/user-research-synthesis` - Uses existing research themes
- `/retention-analysis` - Churn patterns and reasons
- `/feature-results` - Which features helped us compete

---

## Web Research Methodology

When performing competitive research to fill gaps not covered by internal intel, follow this systematic approach:

### Research Steps (in order)

1. **Check company website** for recent announcements, pricing changes, and feature updates. Look at their homepage messaging, pricing page, changelog/release notes, and blog.

2. **Search for recent product updates.** Query: "[competitor] product updates [current quarter]" and "[competitor] new features [current year]". Focus on the last 90 days for freshness.

3. **Check G2/Capterra for recent reviews** mentioning new features. Sort by "most recent" and look for patterns in what users praise or complain about. Extract specific quotes.

4. **Search LinkedIn for competitor PM/engineering job postings.** Job postings reveal strategic direction -- if they are hiring ML engineers, they are building AI features. If they are hiring enterprise sales reps, they are moving upmarket. Query: "[competitor] site:linkedin.com/jobs"

5. **Check their changelog/blog for release notes.** Most SaaS companies publish release notes. This gives you a timeline of what they shipped and how fast they are moving.

6. **Search for funding, partnerships, and acquisitions.** Query: "[competitor] funding [current year]" or "[competitor] partnership". These signals indicate where they are investing.

### Source Documentation

For every competitive claim, document the source with a date:

```markdown
**Claim:** Competitor X launched AI-powered search in Q4 2025
**Source:** Competitor X blog post (https://example.com/blog/ai-search)
**Date verified:** 2026-02-05
**Confidence:** High (primary source)
```

**Confidence levels:**
- **High** -- Primary source (company website, official announcement, direct product trial)
- **Medium** -- Secondary source (G2 review, news article, LinkedIn post)
- **Low** -- Third-party speculation (analyst report, Reddit thread, rumor)

Always prefer high-confidence sources. Flag low-confidence claims explicitly so the PM can decide how much weight to give them.

---

## Common Mistakes to Avoid

### Mistake 1: Jumping to Web Research First
**Bad:** Immediately Googling competitors without checking internal intel
**Good:** Starting with "What do our churned customers say?" from actual interviews

### ❌ Mistake 2: Feature List Without Strategy
**Bad:** "Competitor A has 47 features, we have 35"
**Good:** "Competitor A's complexity is their weakness—30% of reviews complain about onboarding. Our opportunity is simplicity."

### ❌ Mistake 3: Ignoring Indirect Competitors
**Bad:** Only tracking direct competitors
**Good:** Watching for adjacent players who could pivot (like Figma launching FigJam to compete with Miro)

### ❌ Mistake 4: Static Document
**Bad:** Beautiful analysis that lives in a deck, never updated
**Good:** Living document feeding into monthly roadmap discussions

### ❌ Mistake 5: Missing Internal Intel
**Bad:** Only using public data
**Good:** Creating feedback loops with sales/CS teams who hear competitor intel daily

---

## Pro Tips

### 1. Focus on "Why" Not Just "What"

Don't just list features. Understand:
- Why customers choose each competitor (pull from interviews)
- Why they churn from each competitor (pull from churn analysis)
- Why certain features matter more than others (pull from user research)

### 2. Track Signals, Not Just Facts

**Facts:** "Competitor raised $50M Series C"
**Signals:** "With $50M, they'll likely expand to enterprise (based on hiring pattern) and build mobile app (top feature request in their reviews)"

### 3. Use Jobs-to-be-Done Lens

**Bad:** "We need video calling because Competitor has it"
**Good:** "Users hire products to collaborate async across timezones. Video calling is one solution, but async video or threaded conversations might be better for our segment."

### 4. Make It Visual

Create positioning maps, feature matrices, and timelines. Visuals make patterns obvious and are easier to share with stakeholders.

### 5. Balance Your Competitive Response

- 60% Defensive (close critical gaps)
- 30% Offensive (attack their weaknesses)
- 10% Innovative (create new market space)

Don't spend all your time playing catch-up.

---

**Remember:** The best competitive analysis isn't the most comprehensive—it's the one that shows what you *already know internally*, identifies the real gaps, and drives clear decisions about what to build next.

## Output Quality Self-Check

Before delivering a competitive analysis, verify:

- [ ] **Internal intel checked first** -- User research, meetings, PRDs, strategy, and metrics were searched before web research
- [ ] **Gaps identified explicitly** -- Report clearly separates "what we know" from "what we researched externally"
- [ ] **Sources documented with dates** -- Every competitive claim has a source, URL (if applicable), and date verified
- [ ] **Confidence levels assigned** -- Claims marked as High, Medium, or Low confidence
- [ ] **SWOT is specific, not generic** -- Strengths/weaknesses reference actual data (user quotes, review excerpts, feature comparisons), not vague statements
- [ ] **Positioning map included** -- Visual 2x2 showing where competitors sit relative to your product
- [ ] **Feature comparison is strategic** -- Not just a checklist; includes analysis of what matters to your customers
- [ ] **Recommendations are actionable** -- Defensive, offensive, and innovative plays are specific enough to inform roadmap decisions
- [ ] **Cross-skill links included** -- References to relevant retention-analysis, user-research-synthesis, or strategy docs where appropriate

If any check fails, fix it before delivering. The best competitive analysis drives clear decisions, not just awareness.

---

**This skill automatically checks your workspace first, references related skills, and only suggests web research for actual gaps. It works like a real PM connecting dots across research, meetings, and metrics.**
