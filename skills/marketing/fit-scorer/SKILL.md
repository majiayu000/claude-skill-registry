---
name: fit-scorer
description: 'Use when the user asks to "score this influencer", "rank these creators for our campaign", or "tell me which influencer is the best fit"; produces weighted fit scores across audience match, content quality, brand alignment, engagement authenticity, and partnership potential, plus a ranked comparison and a go/pass verdict. Not for finding new influencers — use influencer-discovery; not for sending outreach — use outreach-manager.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when a user has a shortlist of influencers and needs an objective, weighted score to prioritize outreach, choose between candidates, justify a selection to stakeholders, set consistent evaluation standards, compare creators across niches or platforms, or build long-term partner tiers. Activates on requests like score @handle for our brand, compare and rank these creators, or which of these is the best fit."
argument-hint: "<brand or campaign> <influencer handle(s)> [campaign goal: awareness|engagement|conversion]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Map
---

# Fit Scorer

This skill helps you objectively evaluate how well an influencer matches your brand by scoring them across multiple dimensions. It turns subjective "gut feel" into data-driven partnership decisions.

## Quick Start

Shortest invocation — score one influencer:

```
Score @[handle] for [brand/campaign] and tell me if they're a good fit
```

Common scenario — compare and rank a shortlist:

```
Compare and rank these influencers for [campaign]:
- @influencer1
- @influencer2
- @influencer3
```

## Skill Contract

- **Reads**: brand/campaign context, target audience definition, campaign goal, and a shortlist of influencer handles (supplied by the user or carried over from `influencer-discovery`). Optional prior audience profiles from `memory/influencer/audience-analyzer/` and competitor partner benchmarks from `memory/influencer/competitor-tracker/`.
- **Writes**: a fit-score report (per-dimension raw scores, weighted totals, verdict, ranked comparison) to `memory/influencer/fit-scorer/YYYY-MM-DD-<topic>.md`.
- **Promotes**: top-ranked handles, final scores, and the go/pass verdict to `memory/hot-cache.md` so downstream skills pick the right targets.
- **Done when**:
  - Every shortlisted influencer has a weighted total score on the 1-5 scale with per-dimension justifications.
  - A ranked comparison and an explicit verdict (Highly Recommended / Recommended / Consider / Pass) exist for each candidate.
  - The report is saved to the family memory path and top picks are promoted to the hot cache.
- **Primary next skill**: [competitor-tracker](../../map/competitor-tracker/SKILL.md) — benchmark your top-scored picks against the creators competitors already partner with.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family needs no live integrations (Tier 1). Fit Scorer works end to end by asking the user for the inputs it scores — handles, audience targets, brand values, and any metrics they have. Where a connector is available it sharpens the numbers, but none is required.

- `~~influencer database` — pull follower counts, audience demographics, and partnership history instead of asking the user to paste them.
- `~~social platform analytics` — engagement rate, comment quality samples, posting cadence, and growth trend for authenticity checks.
- `~~audience intelligence` — real-vs-bot follower estimates and audience overlap with your target.
- `~~CRM` — prior contact, response reputation, and delivery history for the partnership-potential dimension.

With zero integrations, ask the user to supply each value the scoring tables request; the framework and weighting still produce a defensible ranking. See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category.

## Instructions

When a user requests influencer scoring:

1. **Define Scoring Framework**

   ```markdown
   ### Scoring Framework
   
   **Brand/Campaign**: [name]
   **Campaign Goal**: [awareness/consideration/conversion]
   **Target Audience**: [description]
   
   ### Scoring Dimensions
   
   | Dimension | Weight | Description |
   |-----------|--------|-------------|
   | Audience Match | [%] | How well their audience matches target |
   | Content Quality | [%] | Production value and consistency |
   | Brand Alignment | [%] | Values, aesthetic, messaging fit |
   | Engagement Quality | [%] | Authenticity and depth of engagement |
   | Partnership Potential | [%] | Professionalism, history, availability |
   | **Total** | **100%** | |
   
   **Scoring Scale**: 1-5 (1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent)
   ```

   **C³ ACE alignment & veto gate.** This skill is the C³ **Creator** scorer ([ACE](../../references/c3/ace-creator-benchmark.md)). Map the dimensions onto ACE: Audience Match → **A**udience; Engagement Quality → **E**ngagement; and the **Brand Safety** sub-check (below) → **C**redibility (C1). Note: the value/aesthetic/messaging-fit part of Brand Alignment is *creator × brand fit*, which C³ scores in ROI.Orchestration (O1), **not** in ACE — ACE is brand-independent, so keep brand-fit out of the Credibility dimension. Before ranking, screen every creator against the three ACE veto items; any failure is disqualifying → verdict **PASS (do not partner)** AND cap the numeric Final Rating at the Poor / Below-Average band (**≤ 2.9 / 5**, i.e. ACE ≤ 59/100) so the score never contradicts the decline verdict. State the veto ID + evidence:

   | Veto | Item | Fail condition |
   |------|------|----------------|
   | **A2** | Real-Follower Rate | < 70% real followers, or audit refused (follower fraud) |
   | **C1** | Brand Safety | disqualifying content / active scandal |
   | **E2** | Engagement Authenticity | pod / bought engagement (see Engagement Quality below) |

2. **Score Audience Match**

   ```markdown
   ## Audience Match Score
   
   **Influencer**: @[handle]
   
   ### Target vs. Actual Comparison
   
   | Attribute | Target | Influencer's Audience | Match |
   |-----------|--------|----------------------|-------|
   | Age | [target] | [actual] | ✅/⚠️/❌ |
   | Gender | [target] | [actual] | ✅/⚠️/❌ |
   | Location | [target] | [actual] | ✅/⚠️/❌ |
   | Interests | [target] | [actual] | ✅/⚠️/❌ |
   | Income/Purchasing | [target] | [actual] | ✅/⚠️/❌ |
   
   ### Audience Quality Assessment
   
   | Metric | Value | Assessment |
   |--------|-------|------------|
   | Real follower % | [%] | [Good/Concerning] |
   | Active follower % | [%] | [Good/Concerning] |
   | Bot/spam % | [%] | [Good/Concerning] |
   | Audience growth | [trend] | [Organic/Suspicious] |
   
   ### Audience Match Score: [X/5]
   
   **Justification**: [explanation]
   
   **Weighted Score**: [X] × [weight%] = [weighted points]
   ```

3. **Score Content Quality**

   ```markdown
   ## Content Quality Score
   
   **Influencer**: @[handle]
   
   ### Production Quality
   
   | Factor | Rating | Notes |
   |--------|--------|-------|
   | Visual quality | [1-5] | [notes] |
   | Audio quality (if video) | [1-5] | [notes] |
   | Editing skill | [1-5] | [notes] |
   | Creativity | [1-5] | [notes] |
   | Consistency | [1-5] | [notes] |
   
   ### Content Analysis
   
   **Posting Frequency**: [X posts/week]
   **Content Mix**: [types and %]
   **Caption Quality**: [assessment]
   **Hashtag Strategy**: [assessment]
   
   ### Best Content Examples
   
   1. **[Content 1]**: [why it's good]
   2. **[Content 2]**: [why it's good]
   
   ### Content Concerns
   
   - [Concern 1 if any]
   - [Concern 2 if any]
   
   ### Content Quality Score: [X/5]
   
   **Justification**: [explanation]
   
   **Weighted Score**: [X] × [weight%] = [weighted points]
   ```

4. **Score Brand Alignment**

   ```markdown
   ## Brand Alignment Score
   
   **Influencer**: @[handle]
   
   ### Value Alignment
   
   | Brand Value | Influencer Alignment | Evidence |
   |-------------|---------------------|----------|
   | [Value 1] | ✅/⚠️/❌ | [example from content] |
   | [Value 2] | ✅/⚠️/❌ | [example from content] |
   | [Value 3] | ✅/⚠️/❌ | [example from content] |
   
   ### Aesthetic Alignment
   
   | Element | Brand Style | Influencer Style | Match |
   |---------|-------------|------------------|-------|
   | Colors | [brand] | [influencer] | [%] |
   | Tone | [brand] | [influencer] | [%] |
   | Visual style | [brand] | [influencer] | [%] |
   
   ### Messaging Fit
   
   - **Voice compatibility**: [assessment]
   - **Topic relevance**: [assessment]
   - **Audience overlap**: [assessment]
   
   ### Brand Safety Check
   
   | Risk Category | Assessment | Notes |
   |---------------|------------|-------|
   | Political content | [Low/Medium/High] | [notes] |
   | Controversial opinions | [Low/Medium/High] | [notes] |
   | Competitor mentions | [Low/Medium/High] | [notes] |
   | Adult content | [Low/Medium/High] | [notes] |
   | Legal/regulatory | [Low/Medium/High] | [notes] |
   
   **Overall Brand Safety**: [Safe/Proceed with caution/Risk]
   
   ### Brand Alignment Score: [X/5]
   
   **Justification**: [explanation]
   
   **Weighted Score**: [X] × [weight%] = [weighted points]
   ```

5. **Score Engagement Quality**

   ```markdown
   ## Engagement Quality Score
   
   **Influencer**: @[handle]
   
   ### Engagement Metrics
   
   | Platform | Followers | Eng. Rate | Industry Avg | vs. Avg |
   |----------|-----------|-----------|--------------|---------|
   | [Platform 1] | [count] | [%] | [%] | [+/-] |
   | [Platform 2] | [count] | [%] | [%] | [+/-] |
   
   ### Engagement Authenticity
   
   | Indicator | Assessment | Evidence |
   |-----------|------------|----------|
   | Comment quality | [1-5] | [sample comments] |
   | Comment diversity | [1-5] | [unique commenters] |
   | Like/comment ratio | [ratio] | [normal/abnormal] |
   | Engagement timing | [pattern] | [organic/suspicious] |
   | Follower engagement % | [%] | [good/poor] |
   
   ### Engagement Pods/Buying Signs
   
   - [ ] Sudden follower spikes
   - [ ] Engagement from unrelated accounts
   - [ ] Generic/emoji-only comments
   - [ ] Inconsistent engagement patterns
   - [ ] Follower/following ratio red flags
   
   **Authenticity Assessment**: [Authentic/Some concerns/Suspicious]
   
   ### Response & Interaction
   
   - **Responds to comments**: [Yes/Sometimes/Rarely]
   - **Community building**: [Strong/Average/Weak]
   - **Two-way engagement**: [assessment]
   
   ### Engagement Quality Score: [X/5]
   
   **Justification**: [explanation]
   
   **Weighted Score**: [X] × [weight%] = [weighted points]
   ```

6. **Score Partnership Potential**

   ```markdown
   ## Partnership Potential Score
   
   **Influencer**: @[handle]
   
   ### Partnership History
   
   | Brand | Recency | Content Quality | Disclosure | Notes |
   |-------|---------|-----------------|------------|-------|
   | [Brand 1] | [date] | [rating] | [✅/❌] | [notes] |
   | [Brand 2] | [date] | [rating] | [✅/❌] | [notes] |
   
   **Observations**:
   - Partnership frequency: [X per month]
   - Brand category mix: [categories]
   - Competitor partnerships: [details]
   
   ### Professionalism Indicators
   
   | Factor | Assessment | Evidence |
   |--------|------------|----------|
   | Contact availability | [Easy/Moderate/Difficult] | [contact info] |
   | Response reputation | [Responsive/Mixed/Unresponsive] | [if known] |
   | Content delivery | [On time/Variable/Problematic] | [if known] |
   | Creative quality in ads | [Strong/Average/Weak] | [examples] |
   | Disclosure compliance | [Always/Usually/Sometimes] | [examples] |
   
   ### Exclusivity & Availability
   
   - **Category exclusivity**: [Yes/No - details]
   - **Competitor restrictions**: [details]
   - **Upcoming availability**: [if known]
   
   ### Estimated Value
   
   | Metric | Estimate | Notes |
   |--------|----------|-------|
   | Estimated rate | [range] | Based on [followers/engagement] |
   | CPM estimate | [$X] | Industry average: [$X] |
   | Value assessment | [Good/Fair/Premium] | |
   
   ### Partnership Potential Score: [X/5]
   
   **Justification**: [explanation]
   
   **Weighted Score**: [X] × [weight%] = [weighted points]
   ```

7. **Calculate Final Score**

   ```markdown
   ## Final Fit Score
   
   **Influencer**: @[handle]
   
   ### Score Summary
   
   | Dimension | Raw Score | Weight | Weighted Score |
   |-----------|-----------|--------|----------------|
   | Audience Match | [X/5] | [%] | [points] |
   | Content Quality | [X/5] | [%] | [points] |
   | Brand Alignment | [X/5] | [%] | [points] |
   | Engagement Quality | [X/5] | [%] | [points] |
   | Partnership Potential | [X/5] | [%] | [points] |
   | **Total** | | **100%** | **[X/5.00]** |
   
   ### Score Interpretation
   
   | Score Range | Rating | Recommendation |
   |-------------|--------|----------------|
   | 4.5-5.0 | Excellent | Priority partner |
   | 4.0-4.4 | Very Good | Strong candidate |
   | 3.5-3.9 | Good | Worth pursuing |
   | 3.0-3.4 | Average | Consider with caveats |
   | 2.5-2.9 | Below Average | Proceed with caution |
   | <2.5 | Poor | Not recommended |
   
   ### Final Rating: [X/5] - [Rating]
   
   ### Recommendation
   
   **Verdict**: [Highly Recommended / Recommended / Consider / Pass]
   
   **Key Strengths**:
   1. [Strength 1]
   2. [Strength 2]
   3. [Strength 3]
   
   **Key Concerns**:
   1. [Concern 1]
   2. [Concern 2]
   
   **Best Use Case**: [what type of campaign/content]
   
   **Expected Performance**: 
   - Estimated reach: [X]
   - Estimated engagement: [X]
   - Cost estimate: [$X]
   - Projected CPE: [$X]
   ```

8. **For Multiple Influencers - Comparison**

   ```markdown
   # Influencer Comparison Report
   
   **Campaign**: [name]
   **Date**: [date]
   **Influencers Evaluated**: [count]
   
   ## Ranking Summary
   
   | Rank | Influencer | Platform | Followers | Final Score | Rating |
   |------|------------|----------|-----------|-------------|--------|
   | 1 | @[handle] | [platform] | [count] | [X/5] | ⭐⭐⭐⭐⭐ |
   | 2 | @[handle] | [platform] | [count] | [X/5] | ⭐⭐⭐⭐ |
   | 3 | @[handle] | [platform] | [count] | [X/5] | ⭐⭐⭐⭐ |
   
   ## Detailed Comparison
   
   | Dimension | @[handle1] | @[handle2] | @[handle3] |
   |-----------|------------|------------|------------|
   | Audience Match | [X/5] | [X/5] | [X/5] |
   | Content Quality | [X/5] | [X/5] | [X/5] |
   | Brand Alignment | [X/5] | [X/5] | [X/5] |
   | Engagement Quality | [X/5] | [X/5] | [X/5] |
   | Partnership Potential | [X/5] | [X/5] | [X/5] |
   | **Final Score** | **[X/5]** | **[X/5]** | **[X/5]** |
   
   ## Visual Comparison
   
   ```
   Audience Match    |████████░░| |██████░░░░| |████████░░|
   Content Quality   |██████░░░░| |████████░░| |██████░░░░|
   Brand Alignment   |████████░░| |██████░░░░| |████████░░|
   Engagement        |██████░░░░| |████████░░| |████████░░|
   Partnership       |████████░░| |██████░░░░| |██████░░░░|
                      @handle1     @handle2     @handle3
   ```
   
   ## Recommendation
   
   **For this campaign, prioritize**:
   1. **@[handle]** - [reason]
   2. **@[handle]** - [reason]
   
   **Consider combining**:
   - [Influencer A] for [purpose] + [Influencer B] for [purpose]
   
   **Pass on**:
   - @[handle]: [reason]
   ```

## Example

**User**: "Compare these 3 influencers for our sustainable fashion brand: @ecofashionista, @greenwardrobe, @sustainablesarah"

**Output**: [Detailed comparison with scores, leading to clear recommendations with @sustainablesarah ranked #1 due to highest audience match and engagement authenticity]

## Custom Weighting

Adjust weights based on campaign goals:

| Campaign Goal | Audience | Content | Brand | Engagement | Partnership |
|---------------|----------|---------|-------|------------|-------------|
| Awareness | 30% | 25% | 15% | 20% | 10% |
| Engagement | 20% | 20% | 15% | 35% | 10% |
| Conversion | 35% | 15% | 20% | 20% | 10% |
| Brand Building | 20% | 25% | 30% | 15% | 10% |
| Long-term | 25% | 20% | 25% | 15% | 15% |

## Tips for Success

1. **Be consistent** - Use same criteria for all influencers
2. **Gather data** - More data = more accurate scores
3. **Consider context** - Scores are relative to campaign needs
4. **Update regularly** - Influencer quality changes over time
5. **Trust but verify** - Spot-check high scores before outreach

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and handoff summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipe per connector category.
- Scoring rubric: the C³ benchmark — [c3-benchmark.md](../../references/c3-benchmark.md) (CVI rollup), [c3/ace-creator-benchmark.md](../../references/c3/ace-creator-benchmark.md) (the ACE Creator rubric this skill emits, incl. the A2/C1/E2 veto items applied above), and [c3/scoring-architecture.md](../../references/c3/scoring-architecture.md) for weighting and cap methodology.
- Sibling skills: [influencer-discovery](../influencer-discovery/SKILL.md), [competitor-tracker](../competitor-tracker/SKILL.md), [audience-analyzer](../../insight/audience-analyzer/SKILL.md), [outreach-manager](../../activate/outreach-manager/SKILL.md).

## Next Best Skill

**Primary**: [competitor-tracker](../../map/competitor-tracker/SKILL.md) — benchmark your top-scored picks against the creators competitors already work with before you commit budget.

**Alternates** (same Map phase):
- [influencer-discovery](../influencer-discovery/SKILL.md) — if the shortlist is too thin to rank, go back and source more candidates.
- [audience-analyzer](../../insight/audience-analyzer/SKILL.md) — if audience-match scores are uncertain, tighten the target-audience definition first.

**Termination note**: Track a visited-set of skills invoked this session. If the recommended next skill has already run, stop and report the chain complete rather than re-invoking it. Stop after at most 3 hops (max-depth 3) and hand back to the user with the saved report path.

## Related Skills

- [influencer-discovery](../influencer-discovery/SKILL.md) - Find influencers to score
- [competitor-tracker](../competitor-tracker/SKILL.md) - Benchmark against competitor partners
- [audience-analyzer](../../insight/audience-analyzer/SKILL.md) - Define target audience
- [outreach-manager](../../activate/outreach-manager/SKILL.md) - Contact top-scored influencers
