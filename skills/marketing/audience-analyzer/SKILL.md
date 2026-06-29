---
name: audience-analyzer
description: 'Use when the user asks to "analyze my target audience" or "build an audience profile for influencer targeting"; produces demographic/psychographic profiles, platform-priority matrices, named personas, and influencer-selection criteria. Not for finding specific creators — use influencer-discovery; not for niche community deep-dives — use niche-researcher.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Run at the start of an influencer program or when entering a new audience segment. Use when the user wants to understand who their customer is, where that customer spends time online, which creators they trust, and what influencer-selection criteria follow from that. Also use to diagnose why a prior campaign underperformed or to build personas for a creative brief. Works from a brand or product name alone, or from supplied customer data."
argument-hint: "<brand or product> [category] [geographic focus]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Insight
---

# Audience Analyzer

This skill helps you deeply understand your target audience before selecting influencers. It analyzes demographics, behaviors, content preferences, and platform habits to ensure influencer partnerships reach the right people.

## Quick Start

Shortest invocation:

```
Analyze the target audience for [brand/product/category]
```

Common scenario — build a profile from your own data:

```
Here's our customer data: [data]. Build an audience profile for influencer targeting.
```

## Skill Contract

- **Reads**: brand or product name, category, geographic focus, price point, campaign objective, and any supplied customer data (surveys, social insights, sales records). Prior `niche-researcher` or `trend-spotter` output if present in the hot cache.
- **Writes**: an audience analysis to `memory/influencer/audience-analyzer/YYYY-MM-DD-<topic>.md` — demographic + psychographic profiles, behavioral map, platform-priority matrix, content preferences, influencer-affinity table, named persona, and a must-have/nice-to-have influencer-selection criteria set.
- **Promotes**: durable facts (target age range, priority platforms, ideal influencer profile, persona name) to `memory/hot-cache.md` so downstream skills inherit them.
- **Done when**:
  1. Primary and secondary audiences are profiled across demographics, psychographics, and behavior with stated confidence levels.
  2. A platform-priority matrix and a named persona exist.
  3. An influencer-selection criteria set (must-have, nice-to-have, red flags) is written and ready to hand to discovery.
- **Primary next skill**: [niche-researcher](../../insight/niche-researcher/SKILL.md) — deepen specific communities the persona belongs to before scoring creators.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family is Tier 1 — every step works with no live integration. Ask the user for inputs (brand, category, geography, price point, objective, any customer data) and reason from those. When a connector is available it sharpens the profile but is never required:

- `~~influencer database` — validate which creator tiers and categories the audience actually follows.
- `~~social platform analytics` — confirm platform usage, active times, and engagement style instead of estimating.
- `~~CRM` / `~~customer survey data` — replace assumed demographics and psychographics with first-party facts.
- `~~web analytics` — corroborate the decision journey and discovery method.

Lead with what the user gives you; mark every inferred attribute with a confidence level so unsupported guesses are visible. Connector recipes (free/keyless options included) are in [CONNECTORS.md](../../CONNECTORS.md).

## Instructions

When a user requests audience analysis:

1. **Gather Context**

   ```markdown
   ### Analysis Parameters
   
   **Brand/Product**: [name]
   **Category**: [industry/vertical]
   **Current Customer Base**: [description if available]
   **Geographic Focus**: [regions/countries]
   **Price Point**: [budget/mid/premium]
   **Campaign Objective**: [awareness/consideration/conversion]
   ```

2. **Analyze Demographics**

   ```markdown
   ## Demographic Profile
   
   ### Primary Audience
   
   | Attribute | Profile | Confidence |
   |-----------|---------|------------|
   | Age Range | [X-Y years] | High/Med/Low |
   | Gender | [distribution] | High/Med/Low |
   | Location | [primary markets] | High/Med/Low |
   | Income | [range] | High/Med/Low |
   | Education | [level] | High/Med/Low |
   | Occupation | [types] | High/Med/Low |
   | Family Status | [single/married/parents] | High/Med/Low |
   
   ### Secondary Audience
   
   | Attribute | Profile | Notes |
   |-----------|---------|-------|
   | [attributes] | [values] | [notes] |
   
   ### Demographic Insights
   
   **Key Findings**:
   1. [Insight about age/generation]
   2. [Insight about location/culture]
   3. [Insight about life stage]
   
   **Implications for Influencer Selection**:
   - Look for influencers aged [range] who resonate with [demographic]
   - Prioritize creators in [locations/markets]
   - Consider [family/lifestyle] focused content creators
   ```

3. **Profile Psychographics**

   ```markdown
   ## Psychographic Profile
   
   ### Values & Beliefs
   
   | Value | Importance | How It Manifests |
   |-------|------------|------------------|
   | [Value 1] | High | [Behavior/preference] |
   | [Value 2] | High | [Behavior/preference] |
   | [Value 3] | Medium | [Behavior/preference] |
   
   ### Interests & Hobbies
   
   **Primary Interests** (directly related to product):
   - [Interest 1] - [relevance]
   - [Interest 2] - [relevance]
   
   **Adjacent Interests** (lifestyle/cultural):
   - [Interest 1] - [connection to brand]
   - [Interest 2] - [connection to brand]
   
   ### Lifestyle Characteristics
   
   **Daily Life**:
   - Morning routine: [description]
   - Work/life balance: [description]
   - Leisure time: [how they spend it]
   - Social habits: [description]
   
   **Aspiration Profile**:
   - Who they aspire to be: [description]
   - Brands they admire: [brands]
   - Lifestyle they want: [description]
   
   ### Personality Traits
   
   | Trait | Level | Impact on Content |
   |-------|-------|-------------------|
   | [Trait 1] | High/Med/Low | [How to appeal] |
   | [Trait 2] | High/Med/Low | [How to appeal] |
   
   **Implications for Influencer Selection**:
   - Partner with creators who embody [values]
   - Content should reflect [lifestyle aspirations]
   - Avoid influencers who [misaligned traits]
   ```

4. **Map Behavioral Patterns**

   ```markdown
   ## Behavioral Analysis
   
   ### Purchase Behavior
   
   **Decision Journey**:
   
   | Stage | Duration | Key Activities | Influencer Role |
   |-------|----------|----------------|-----------------|
   | Awareness | [time] | [activities] | [how influencers help] |
   | Consideration | [time] | [activities] | [how influencers help] |
   | Decision | [time] | [activities] | [how influencers help] |
   | Post-Purchase | [time] | [activities] | [how influencers help] |
   
   **Purchase Triggers**:
   - [Trigger 1]: [description]
   - [Trigger 2]: [description]
   - [Trigger 3]: [description]
   
   **Purchase Barriers**:
   - [Barrier 1]: [how to overcome]
   - [Barrier 2]: [how to overcome]
   
   ### Content Consumption
   
   **Daily Media Diet**:
   
   | Time | Activity | Platforms | Content Type |
   |------|----------|-----------|--------------|
   | Morning | [activity] | [platforms] | [content] |
   | Commute | [activity] | [platforms] | [content] |
   | Lunch | [activity] | [platforms] | [content] |
   | Evening | [activity] | [platforms] | [content] |
   | Weekend | [activity] | [platforms] | [content] |
   
   **Content Engagement Patterns**:
   - Most active time: [days/times]
   - Average session length: [duration]
   - Engagement style: [passive viewer/active commenter/sharer]
   - Discovery method: [algorithm/search/recommendations]
   
   ### Social Behavior
   
   **How They Interact with Influencers**:
   - Follow count: [typical range]
   - Engagement level: [lurker/occasional/active]
   - Trust in recommendations: [low/medium/high]
   - UGC creation: [never/occasionally/frequently]
   ```

5. **Analyze Platform Preferences**

   ```markdown
   ## Platform Analysis
   
   ### Platform Priority Matrix
   
   | Platform | Usage Level | Primary Purpose | Best Content Type |
   |----------|-------------|-----------------|-------------------|
   | Instagram | High/Med/Low | [purpose] | [format] |
   | TikTok | High/Med/Low | [purpose] | [format] |
   | YouTube | High/Med/Low | [purpose] | [format] |
   | Twitter/X | High/Med/Low | [purpose] | [format] |
   | LinkedIn | High/Med/Low | [purpose] | [format] |
   | Pinterest | High/Med/Low | [purpose] | [format] |
   | Twitch | High/Med/Low | [purpose] | [format] |
   
   ### Primary Platform Deep-Dive: [Platform]
   
   **Usage Patterns**:
   - Time spent: [hours/day]
   - Sessions: [frequency]
   - Primary activities: [discovery/entertainment/shopping/social]
   
   **Content Preferences**:
   - Preferred format: [Stories/Reels/Feed/etc.]
   - Content length: [preference]
   - Audio: [sound on/off]
   
   **Influencer Relationship**:
   - Influencer types followed: [mega/macro/micro/nano]
   - Categories: [lifestyle/comedy/educational/etc.]
   - Trust level: [how much they trust platform recommendations]
   
   ### Platform Recommendation
   
   **Prioritize these platforms**:
   1. [Platform 1]: [reason] - [% of budget recommended]
   2. [Platform 2]: [reason] - [% of budget recommended]
   3. [Platform 3]: [reason] - [% of budget recommended]
   
   **Avoid or deprioritize**:
   - [Platform]: [reason]
   ```

6. **Identify Content Preferences**

   ```markdown
   ## Content Preference Analysis
   
   ### Format Preferences
   
   | Format | Preference | Best For | Example |
   |--------|------------|----------|---------|
   | Short video (<60s) | High/Med/Low | [use case] | [example] |
   | Long video (>3min) | High/Med/Low | [use case] | [example] |
   | Static images | High/Med/Low | [use case] | [example] |
   | Carousel posts | High/Med/Low | [use case] | [example] |
   | Stories | High/Med/Low | [use case] | [example] |
   | Live streams | High/Med/Low | [use case] | [example] |
   | Podcasts | High/Med/Low | [use case] | [example] |
   
   ### Content Style Preferences
   
   **Tone that resonates**:
   - [Authentic/polished]
   - [Humorous/serious]
   - [Educational/entertaining]
   - [Aspirational/relatable]
   
   **Visual aesthetics**:
   - [Minimalist/maximalist]
   - [Bright/moody]
   - [Professional/casual]
   - [Trendy/timeless]
   
   **Storytelling preferences**:
   - [Personal stories/product focus]
   - [Problem-solution/lifestyle integration]
   - [Tutorial/review/unboxing]
   
   ### Topics That Engage
   
   | Topic | Interest Level | Content Angle |
   |-------|----------------|---------------|
   | [Topic 1] | High | [angle] |
   | [Topic 2] | High | [angle] |
   | [Topic 3] | Medium | [angle] |
   
   ### Content Red Flags
   
   **Avoid these approaches**:
   - [Approach 1]: [why it fails]
   - [Approach 2]: [why it fails]
   ```

7. **Profile Influencer Affinity**

   ```markdown
   ## Influencer Affinity Analysis
   
   ### Influencer Types They Follow
   
   | Type | Popularity | Trust Level | Example Categories |
   |------|------------|-------------|-------------------|
   | Mega (1M+) | [%] | [level] | [categories] |
   | Macro (100K-1M) | [%] | [level] | [categories] |
   | Micro (10K-100K) | [%] | [level] | [categories] |
   | Nano (<10K) | [%] | [level] | [categories] |
   
   ### Why They Follow Influencers
   
   | Motivation | Strength | Implications |
   |------------|----------|--------------|
   | Entertainment | High/Med/Low | [content strategy] |
   | Education | High/Med/Low | [content strategy] |
   | Aspiration | High/Med/Low | [content strategy] |
   | Deals/Discounts | High/Med/Low | [content strategy] |
   | Community | High/Med/Low | [content strategy] |
   | FOMO | High/Med/Low | [content strategy] |
   
   ### Trust Factors
   
   **What builds credibility**:
   1. [Factor 1]: [explanation]
   2. [Factor 2]: [explanation]
   3. [Factor 3]: [explanation]
   
   **What destroys trust**:
   1. [Factor 1]: [why it fails]
   2. [Factor 2]: [why it fails]
   
   ### Ideal Influencer Profile
   
   Based on audience analysis, ideal influencers should:
   
   - **Be aged**: [range]
   - **Have aesthetic**: [style description]
   - **Create content about**: [topics]
   - **Communicate with**: [tone/style]
   - **Have engagement rate**: [minimum %]
   - **Be on**: [priority platforms]
   - **Avoid**: [red flags]
   ```

8. **Generate Audience Persona**

   ```markdown
   ## Audience Persona
   
   ### "[Persona Name]"
   
   **Demographics**:
   - Age: [X]
   - Location: [city/region]
   - Occupation: [job]
   - Income: [range]
   - Family: [status]
   
   **Bio**:
   [2-3 sentence description of who they are]
   
   **A Day in Their Life**:
   [Brief narrative of typical day including media consumption]
   
   **Goals & Challenges**:
   - Goals: [what they want to achieve]
   - Challenges: [what stands in their way]
   - How [product] helps: [connection]
   
   **Media Consumption**:
   - Primary platform: [platform]
   - Content preferences: [types]
   - Influencers they follow: [examples/types]
   - Trust triggers: [what makes them believe]
   
   **Purchase Journey**:
   - Discovery: [how they find products]
   - Research: [how they evaluate]
   - Decision: [what tips them over]
   - Loyalty: [what keeps them]
   
   **Key Quote**:
   > "[A quote this persona might say about the product/category]"
   ```

9. **Summarize Influencer Selection Criteria**

   ```markdown
   # Audience Analysis Summary
   
   ## Key Audience Insights
   
   1. [Most important insight]
   2. [Second insight]
   3. [Third insight]
   
   ## Influencer Selection Criteria
   
   Based on this audience analysis:
   
   ### Must-Have Criteria
   
   | Criterion | Requirement | Reasoning |
   |-----------|-------------|-----------|
   | Audience age | [range] | Matches target demographic |
   | Platform | [platforms] | Where audience is active |
   | Content style | [style] | Resonates with preferences |
   | Engagement rate | [min %] | Indicates active audience |
   | Values alignment | [values] | Matches audience beliefs |
   
   ### Nice-to-Have Criteria
   
   | Criterion | Preference | Reasoning |
   |-----------|------------|-----------|
   | [criterion] | [preference] | [reason] |
   
   ### Red Flags to Avoid
   
   - [Red flag 1]
   - [Red flag 2]
   - [Red flag 3]
   
   ## Recommended Influencer Mix
   
   | Tier | % of Budget | Quantity | Role |
   |------|-------------|----------|------|
   | Mega (1M+) | [%] | [#] | Awareness/credibility |
   | Macro (100K-1M) | [%] | [#] | Reach + engagement |
   | Micro (10K-100K) | [%] | [#] | Trust + conversion |
   | Nano (<10K) | [%] | [#] | Authenticity + UGC |
   
   ## Next Steps
   
   1. Use these criteria in [influencer-discovery](../../map/influencer-discovery/SKILL.md)
   2. Score potential influencers with [fit-scorer](../../map/fit-scorer/SKILL.md)
   3. Develop content strategy based on [content preferences]
   ```

## Example

**User**: "Analyze the target audience for a premium skincare brand targeting millennial women"

**Output**: [Comprehensive audience analysis following the structure above, with specific insights about millennial women's skincare habits, social media behavior, influencer preferences, etc.]

## Tips for Success

1. **Use real data when available** - Customer surveys, social insights, sales data
2. **Don't assume** - Validate hypotheses with research
3. **Consider micro-segments** - Not all customers are the same
4. **Update regularly** - Audiences evolve
5. **Connect to influencer criteria** - Every insight should inform selection

## Reference Materials

- Shared contract and handoff schema: [skill-contract.md](../../references/skill-contract.md)
- Shared state model (memory tiers, save paths): [state-model.md](../../references/state-model.md)
- Connector recipes (free/keyless options): [CONNECTORS.md](../../CONNECTORS.md)
- C3 scoring architecture (downstream creator/fit scoring): [references/c3/scoring-architecture.md](../../references/c3/scoring-architecture.md)
- Sibling Insight skills: [niche-researcher](../../insight/niche-researcher/SKILL.md), [trend-spotter](../../insight/trend-spotter/SKILL.md)
- Downstream Map skills: [influencer-discovery](../../map/influencer-discovery/SKILL.md), [fit-scorer](../../map/fit-scorer/SKILL.md)

## Next Best Skill

**Primary**: [niche-researcher](../../insight/niche-researcher/SKILL.md) — deep-dive the specific communities your persona belongs to before scoring creators.

**Alternates** (same Insight family):
- [trend-spotter](../../insight/trend-spotter/SKILL.md) — surface trends and content angles relevant to this audience.

**Termination**: maintain a visited-set across the session. If a recommended skill has already been invoked this run, stop and report the chain is complete rather than re-entering it. Cap any handoff chain at max-depth 3. Once influencer-selection criteria are written and promoted to the hot cache, the audience phase is terminal — hand off to discovery and stop.
