---
name: niche-researcher
description: 'Use when the user asks to "research a niche community", "deep-dive a subculture", or "find micro-niches for a brand"; produces a community map, culture decode (language, norms, taboos), key-voice tiers, content ecosystem, brand-fit score, and a phased entry strategy. Not for finding specific creators to contract — use influencer-discovery.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Entering a new market or category, understanding a subculture before partnering with creators, identifying micro-communities within a broad audience, finding underserved niches with high engagement, or avoiding cultural missteps in an unfamiliar community. Activate before any creator outreach in a specialized space so the brand learns the language, norms, and taboos first."
argument-hint: "<niche or community> [parent category] [brand or product]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Insight
---

# Niche Researcher

This skill helps you understand specific niche communities before engaging with influencers in that space. It analyzes community culture, identifies key voices, maps content ecosystems, and reveals the unwritten rules that determine authentic engagement.

## Quick Start

Shortest invocation:

```
Research the [niche] community and identify opportunities for [brand]
```

Common scenario:

```
Deep-dive into [subculture] — who are the key voices, what content works,
and would [brand] be a good fit? Flag the cultural risks.
```

## Skill Contract

- **Reads**: niche/community name, parent category, brand or product, research goal (awareness/partnership/entry), platforms to focus on. Optional prior artifacts from `audience-analyzer` or `trend-spotter` in `memory/influencer/`.
- **Writes**: a niche research dossier (community map, culture decode, voice tiers, content ecosystem, brand-fit score, entry strategy) saved to `memory/influencer/niche-researcher/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable facts — niche name, brand-fit verdict, top 3 key voices, hard red lines/taboos — to `memory/hot-cache.md`.
- **Done when**:
  - The community is mapped (size, platforms, sub-niches) and its culture decoded (language, norms, taboos).
  - Key voices are tiered and a brand-fit score (out of 25) with a Strong/Moderate/Weak/Poor verdict is recorded.
  - A phased entry strategy and explicit red lines are written to the dossier.
- **Primary next skill**: [trend-spotter](../../insight/trend-spotter/SKILL.md) — surface what is moving inside the niche you just mapped.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family has no live integrations required (Tier 1). The skill works with nothing connected: ask the user for the niche name, parent category, brand, and target platforms, then build the dossier from what they provide plus what you can observe.

Optional connectors that deepen the research where available:

- `~~influencer database` — pull follower counts, growth rates, and past brand partnerships for the voice tiers.
- `~~social platform analytics` — measure engagement rates, hashtag volume, and content-format performance inside the niche.
- `~~social listening` — sample real community language, recurring topics, and sentiment toward brands.
- `~~CRM` — check whether the brand already has relationships with creators in the space.

See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category. None are required; absence just means you ask the user for those inputs instead.

## Instructions

When a user requests niche research:

1. **Define the Niche**

   ```markdown
   ### Niche Research Parameters
   
   **Niche/Community**: [name]
   **Parent Category**: [broader category]
   **Brand/Product**: [what's being promoted]
   **Research Goal**: [awareness/partnership/entry strategy]
   **Platforms to Focus**: [platforms]
   ```

2. **Map the Community**

   ```markdown
   ## Community Overview
   
   ### Niche Profile
   
   **Name**: [community name/identifier]
   **Size Estimate**: [community size]
   **Growth Trend**: [growing/stable/declining]
   **Primary Platforms**: [where they gather]
   **Secondary Platforms**: [other presence]
   
   ### Community Demographics
   
   | Attribute | Profile | Notes |
   |-----------|---------|-------|
   | Age range | [range] | [notes] |
   | Gender split | [%] | [notes] |
   | Location | [regions] | [notes] |
   | Income | [range] | [notes] |
   | Occupation | [typical jobs] | [notes] |
   
   ### Community Psychographics
   
   **Core Identity**:
   - How they describe themselves: "[self-description]"
   - What unites them: [shared passion/belief/activity]
   - What they're against: [opposition identity]
   
   **Values Hierarchy**:
   1. [Top value]: [why it matters]
   2. [Second value]: [why it matters]
   3. [Third value]: [why it matters]
   
   ### Sub-communities
   
   | Sub-niche | Size | Focus | Key Difference |
   |-----------|------|-------|----------------|
   | [sub 1] | [size] | [focus] | [how it differs] |
   | [sub 2] | [size] | [focus] | [how it differs] |
   ```

3. **Analyze Community Culture**

   ```markdown
   ## Cultural Analysis
   
   ### Language & Terminology
   
   **Key Terms to Know**:
   
   | Term | Meaning | Usage Context |
   |------|---------|---------------|
   | [term 1] | [meaning] | [how/when used] |
   | [term 2] | [meaning] | [how/when used] |
   | [term 3] | [meaning] | [how/when used] |
   
   **Insider Language Examples**:
   - "[phrase]" = [translation]
   - "[phrase]" = [translation]
   
   **Language to Avoid**:
   - "[term]" - [why it's problematic]
   - "[term]" - [why it's problematic]
   
   ### Community Norms
   
   **Unwritten Rules**:
   
   1. **[Rule 1]**: [explanation]
      - Do: [example]
      - Don't: [example]
   
   2. **[Rule 2]**: [explanation]
      - Do: [example]
      - Don't: [example]
   
   ### Status & Credibility
   
   **How credibility is earned**:
   - [Factor 1]: [explanation]
   - [Factor 2]: [explanation]
   - [Factor 3]: [explanation]
   
   **Status markers**:
   - [Marker 1]: [what it signals]
   - [Marker 2]: [what it signals]
   
   ### Content Culture
   
   **Celebrated content types**:
   - [Type 1]: [why it's valued]
   - [Type 2]: [why it's valued]
   
   **Content taboos**:
   - [Taboo 1]: [why it's rejected]
   - [Taboo 2]: [why it's rejected]
   
   ### Brand Attitudes
   
   **How community views brands**:
   - General attitude: [positive/neutral/skeptical/hostile]
   - Brands that succeeded: [examples and why]
   - Brands that failed: [examples and why]
   
   **What earns brand acceptance**:
   - [Factor 1]
   - [Factor 2]
   
   **What triggers rejection**:
   - [Factor 1]
   - [Factor 2]
   ```

4. **Identify Key Voices**

   ```markdown
   ## Key Community Voices
   
   ### Tier 1: Community Leaders
   
   These are the most influential voices who shape community opinion.
   
   | Creator | Platform | Followers | Why They Matter |
   |---------|----------|-----------|-----------------|
   | @[handle1] | [platform] | [count] | [influence description] |
   | @[handle2] | [platform] | [count] | [influence description] |
   
   **Deep Dive: [Top Creator]**
   
   - **Handle**: @[handle]
   - **Platforms**: [platforms]
   - **Content focus**: [topics]
   - **Engagement rate**: [%]
   - **Community standing**: [description]
   - **Brand history**: [past partnerships]
   - **Partnership potential**: [assessment]
   
   ### Tier 2: Rising Stars
   
   Emerging voices gaining influence rapidly.
   
   | Creator | Platform | Followers | Growth Rate | Specialty |
   |---------|----------|-----------|-------------|-----------|
   | @[handle] | [platform] | [count] | [% growth] | [focus] |
   
   ### Tier 3: Micro-Voices
   
   Smaller but highly trusted within specific sub-niches.
   
   | Creator | Sub-niche | Followers | Engagement | Value |
   |---------|-----------|-----------|------------|-------|
   | @[handle] | [niche] | [count] | [rate] | [what they offer] |
   
   ### Voice Map
   
   ```
   Community Influence Structure:
   
   [Leader 1] ─────┐
                   ├──── Core Community
   [Leader 2] ─────┤
                   │
   [Rising 1] ─────┼──── Growing Segment
   [Rising 2] ─────┤
                   │
   [Micro voices] ─┴──── Niche Segments
   ```
   
   ### Collaboration Networks
   
   **Who collaborates with whom**:
   - [Creator A] often works with [Creator B]
   - [Group/collective] includes: [members]
   - Cross-platform presence: [who's on multiple platforms]
   ```

5. **Map Content Ecosystem**

   ```markdown
   ## Content Ecosystem
   
   ### Top Performing Content Types
   
   | Content Type | Platform | Avg Engagement | Example |
   |--------------|----------|----------------|---------|
   | [type 1] | [platform] | [rate] | [example] |
   | [type 2] | [platform] | [rate] | [example] |
   | [type 3] | [platform] | [rate] | [example] |
   
   ### Content Themes
   
   **Evergreen topics** (always relevant):
   - [Topic 1]: [why it resonates]
   - [Topic 2]: [why it resonates]
   
   **Trending topics** (current):
   - [Topic 1]: [current conversation]
   - [Topic 2]: [current conversation]
   
   **Controversial topics** (handle carefully):
   - [Topic 1]: [different perspectives]
   
   ### Content Formats
   
   **High Performance**:
   | Format | Platform | Why It Works | Brand Application |
   |--------|----------|--------------|-------------------|
   | [format] | [platform] | [reason] | [how brand can use] |
   
   **Declining/Saturated**:
   - [Format]: [why it's declining]
   
   ### Hashtags & Discovery
   
   **Community hashtags**:
   | Hashtag | Volume | Community Meaning |
   |---------|--------|-------------------|
   | #[tag1] | [posts] | [significance] |
   | #[tag2] | [posts] | [significance] |
   
   **Discovery pathways**:
   - How content spreads: [mechanism]
   - Cross-posting patterns: [platforms]
   - Algorithm factors: [what gets boosted]
   ```

6. **Assess Opportunities & Risks**

   ```markdown
   ## Opportunity Assessment
   
   ### Market Opportunity
   
   | Factor | Assessment | Notes |
   |--------|------------|-------|
   | Community size | [size] | [growing/stable/shrinking] |
   | Brand saturation | [low/medium/high] | [competitor presence] |
   | Purchase intent | [low/medium/high] | [buying behavior] |
   | Price sensitivity | [low/medium/high] | [spending patterns] |
   | Engagement quality | [low/medium/high] | [interaction depth] |
   
   ### Brand Fit Score
   
   | Factor | Score (1-5) | Explanation |
   |--------|-------------|-------------|
   | Value alignment | [score] | [explanation] |
   | Audience overlap | [score] | [explanation] |
   | Product relevance | [score] | [explanation] |
   | Content fit | [score] | [explanation] |
   | Price point fit | [score] | [explanation] |
   | **Total** | [X/25] | |
   
   **Fit Assessment**: [Strong/Moderate/Weak/Poor]
   
   ### Risk Assessment
   
   | Risk | Likelihood | Impact | Mitigation |
   |------|------------|--------|------------|
   | [Risk 1] | High/Med/Low | High/Med/Low | [how to mitigate] |
   | [Risk 2] | High/Med/Low | High/Med/Low | [how to mitigate] |
   | [Risk 3] | High/Med/Low | High/Med/Low | [how to mitigate] |
   
   **Cultural Sensitivities**:
   - [Sensitivity 1]: [how to navigate]
   - [Sensitivity 2]: [how to navigate]
   
   ### Competitive Map
   
   | Competitor | Niche Presence | Strategy | Performance |
   |------------|----------------|----------|-------------|
   | [comp 1] | [level] | [approach] | [results] |
   | [comp 2] | [level] | [approach] | [results] |
   
   **White Space Opportunities**:
   - [Opportunity 1]: [description]
   - [Opportunity 2]: [description]
   ```

7. **Generate Entry Strategy**

   ```markdown
   ## Niche Entry Strategy
   
   ### Recommended Approach
   
   **Strategy Type**: [Immersion/Partnership/Sponsorship/Content]
   
   **Rationale**: [why this approach]
   
   ### Phase 1: Listen & Learn (Weeks 1-2)
   
   - Follow key voices: [list]
   - Monitor conversations: [topics]
   - Note language patterns: [terminology]
   - Identify content gaps: [opportunities]
   
   ### Phase 2: Soft Entry (Weeks 3-4)
   
   - Initial creator partnerships: [recommended creators]
   - Content approach: [format and style]
   - Community touchpoints: [where to engage]
   
   ### Phase 3: Active Engagement (Month 2+)
   
   - Expanded creator roster: [additional partners]
   - Community participation: [how to contribute]
   - Content cadence: [frequency]
   
   ### Creator Partnership Recommendations
   
   **Must-Partner (High priority)**:
   | Creator | Platform | Why | Approach |
   |---------|----------|-----|----------|
   | @[handle] | [platform] | [reason] | [how to approach] |
   
   **Should-Consider (Medium priority)**:
   | Creator | Platform | Why | Approach |
   |---------|----------|-----|----------|
   | @[handle] | [platform] | [reason] | [how to approach] |
   
   ### Content Strategy
   
   **Themes to emphasize**:
   - [Theme 1]: [content angle]
   - [Theme 2]: [content angle]
   
   **Formats to use**:
   - [Format 1]: [why it works here]
   - [Format 2]: [why it works here]
   
   **Avoid**:
   - [Content type]: [why it won't work]
   
   ### Success Metrics
   
   | Metric | Target | Timeline |
   |--------|--------|----------|
   | [metric 1] | [target] | [when] |
   | [metric 2] | [target] | [when] |
   
   ### Red Lines
   
   Things that would damage brand reputation in this community:
   - [Red line 1]
   - [Red line 2]
   ```

## When to Use This Skill

- Entering a new market or category
- Understanding a subculture before partnering with creators
- Identifying micro-communities within larger audiences
- Finding underserved niches with high engagement
- Avoiding cultural missteps in unfamiliar communities
- Discovering emerging niche categories

## What This Skill Does

1. **Community Mapping**: Identifies and profiles niche communities
2. **Culture Analysis**: Understands values, language, and norms
3. **Voice Identification**: Finds key influencers and thought leaders
4. **Content Ecosystem**: Maps what content performs in the niche
5. **Opportunity Assessment**: Evaluates brand fit and potential
6. **Risk Identification**: Flags cultural sensitivities and taboos

## Example

**User**: "Research the #BookTok community for a publishing brand"

**Output**: [Comprehensive niche research on BookTok including community culture, key voices like @aikitwokki, content types that perform (book reviews, reading vlogs, shelfies), language ("booktok made me buy it"), and strategic recommendations for publisher partnerships]

## Tips for Success

1. **Spend time observing** - Don't rush into partnerships
2. **Learn the language** - Authenticity requires fluency
3. **Respect the culture** - Every community has sacred cows
4. **Start with respected voices** - Credibility transfers
5. **Add value, don't extract** - Communities reject exploitation

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — temperature memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipe per connector category.
- Sibling Insight skills: [audience-analyzer](../audience-analyzer/SKILL.md), [trend-spotter](../trend-spotter/SKILL.md).
- Downstream Map skills: [influencer-discovery](../../map/influencer-discovery/SKILL.md), [fit-scorer](../../map/fit-scorer/SKILL.md).

## Next Best Skill

**Primary**: [trend-spotter](../../insight/trend-spotter/SKILL.md) — surface what is currently moving inside the niche you mapped, so partnerships ride live momentum.

**Alternates (same Insight family)**:
- [audience-analyzer](../audience-analyzer/SKILL.md) — widen from one niche to the broader audience picture when the brand needs cross-community reach.
- [influencer-discovery](../../map/influencer-discovery/SKILL.md) — once the niche and voice tiers are set, find and shortlist specific creators to contract.

**Termination note** (visited-set + depth): if any candidate skill has already been invoked this session, stop and report chain-complete instead of re-running it. Cap the handoff chain at depth 3; beyond that, summarize and hand back to the user.

## Related Skills

- [audience-analyzer](../audience-analyzer/SKILL.md) - Broader audience understanding
- [trend-spotter](../trend-spotter/SKILL.md) - Trends within niches
- [influencer-discovery](../../map/influencer-discovery/SKILL.md) - Find niche influencers
- [fit-scorer](../../map/fit-scorer/SKILL.md) - Evaluate niche influencer fit
