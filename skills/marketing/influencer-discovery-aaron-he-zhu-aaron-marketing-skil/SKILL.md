---
name: influencer-discovery
description: 'Use when the user asks to "find influencers", "build an influencer list", or "discover creators in [niche]"; produces a multi-platform candidate pool, per-influencer profiles with audience and engagement metrics, authenticity red-flag screening, and a tiered shortlist with fit scores. Not for scoring or ranking a known shortlist — use fit-scorer.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate when building an influencer roster from scratch, expanding into a new platform or niche, replacing churned partners, finding micro and nano creators at scale, identifying which influencers a competitor partners with, or standing up an always-on discovery pipeline. The user names a niche, platform, follower band, or brand and wants a list of candidate creators to evaluate."
argument-hint: "<brand or niche> [platform] [follower-range]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Map
---

# Influencer Discovery

This skill helps you find the right influencers for your brand by searching across platforms, analyzing content and audience fit, and building curated lists of potential partners. It adapts traditional lead research methodology to the influencer marketing context.

## Quick Start

Shortest invocation:

```
Find 20 influencers in [niche] for [brand/product]
```

Common scenario:

```
Find influencers who:
- Are in the [niche] space
- Have 50K-200K followers
- Post primarily on TikTok and Instagram
- Are based in [location]
- Have engagement rates above 4%
- Have worked with brands similar to [brand]
```

## Skill Contract

- **Reads**: brand/product, niche or category, target platforms, follower range, engagement floor, location/language, audience demographics, exclusions; prior `entity-optimizer` brand profile and any `audience-analyzer` output if present in memory.
- **Writes**: discovery results to `memory/influencer/influencer-discovery/YYYY-MM-DD-<topic>.md` — search criteria, candidate pool stats, per-influencer profiles, tiered shortlist with fit scores.
- **Promotes**: durable facts (top-tier handles, confirmed niche/platform mix, competitor-saturated creators) to `memory/hot-cache.md`.
- **Done when**:
  - A candidate pool exists with at least the requested count screened past follower, engagement, and brand-safety filters.
  - Each shortlisted influencer has a profile with metrics, audience read, and a preliminary fit score.
  - A tiered shortlist (must-reach / strong / consider) is compiled with next-step pointers.
- **Primary next skill**: [fit-scorer](../../map/fit-scorer/SKILL.md) — score and rank the discovered candidates with weighted criteria.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family has no live integrations required (Tier 1): the skill works with only the inputs the user provides. Ask the user for niche, platforms, follower band, engagement floor, location, and exclusions, then reason over what they supply plus any public handles they share.

Where a tool *could* sharpen results, use `~~` connector placeholders:

- `~~influencer database` — bulk discovery, follower/engagement metrics, audience demographics.
- `~~social platform analytics` — native creator-marketplace data, trending sounds, related accounts.
- `~~CRM` — import the shortlist and dedupe against existing partners.
- `~~audience overlap` — estimate creator-audience vs. brand-audience match.

See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category and the opt-in MCP layer. None are required — every step degrades to user-supplied inputs.

## Instructions

When a user requests influencer discovery:

1. **Define Search Criteria**

   ```markdown
   ### Discovery Parameters
   
   **Brand/Product**: [name]
   **Campaign Goal**: [awareness/consideration/conversion]
   **Budget Range**: [budget implications for influencer tier]
   
   **Search Criteria**:
   
   | Parameter | Requirement | Priority |
   |-----------|-------------|----------|
   | Niche/Category | [niche] | Required |
   | Platform(s) | [platforms] | Required |
   | Follower Range | [min-max] | Required |
   | Engagement Rate | [minimum %] | Required |
   | Location | [regions] | [Required/Preferred] |
   | Language | [languages] | [Required/Preferred] |
   | Content Type | [video/photo/etc.] | Preferred |
   | Posting Frequency | [minimum] | Preferred |
   | Audience Demographics | [age/gender/interests] | Preferred |
   | Brand Safety | [requirements] | Required |
   
   **Nice-to-Have**:
   - [Additional preference 1]
   - [Additional preference 2]
   
   **Exclusions**:
   - [Competitor partnerships]
   - [Content types to avoid]
   - [Other exclusions]
   ```

2. **Conduct Search**

   ```markdown
   ## Search Strategy
   
   ### Primary Search Methods
   
   1. **Hashtag Research**
      - Core hashtags: #[hashtag1], #[hashtag2]
      - Niche hashtags: #[hashtag3], #[hashtag4]
      - Brand-adjacent: #[hashtag5]
   
   2. **Similar Accounts**
      - Starting from: @[known influencer]
      - Platform suggestions: "Similar to" features
   
   3. **Competitor Mentions**
      - Check tagged posts on [competitor accounts]
      - Monitor #[competitor hashtags]
   
   4. **Platform-Specific Discovery**
      - TikTok: Creator Marketplace, trending sounds
      - Instagram: Explore page, Reels
      - YouTube: Related channels, collaboration networks
   
   5. **Tool Queries** (if available)
      - [Platform]: [search query]
   ```

3. **Initial Screening**

   ```markdown
   ## Initial Candidate Pool
   
   **Total Candidates Found**: [number]
   **After Initial Screening**: [number]
   
   ### Screening Criteria Applied
   
   | Criterion | Filter | Eliminated |
   |-----------|--------|------------|
   | Follower range | [range] | [#] |
   | Engagement rate | >[%] | [#] |
   | Recent activity | <[days] | [#] |
   | Content relevance | [criteria] | [#] |
   | Brand safety | [criteria] | [#] |
   
   ### Red Flags Identified
   
   - [#] accounts with suspected fake followers
   - [#] accounts with controversial content
   - [#] accounts with competitor exclusivity
   - [#] accounts inactive >30 days
   ```

4. **Build Influencer Profiles**

   For each qualified influencer:

   ```markdown
   ---
   
   ## Influencer #[X]: @[handle]
   
   ### Basic Information
   
   | Attribute | Details |
   |-----------|---------|
   | **Name** | [name] |
   | **Handle** | @[handle] |
   | **Platform** | [primary platform] |
   | **Other Platforms** | [other handles] |
   | **Location** | [city, country] |
   | **Language** | [primary language] |
   | **Niche** | [category] |
   
   ### Metrics
   
   | Platform | Followers | Engagement Rate | Avg. Views |
   |----------|-----------|-----------------|------------|
   | [Platform 1] | [count] | [%] | [views] |
   | [Platform 2] | [count] | [%] | [views] |
   
   **Growth Trend**: [growing/stable/declining] ([%] last 90 days)
   
   ### Audience Analysis
   
   | Demographic | Breakdown | Notes |
   |-------------|-----------|-------|
   | Gender | [%F / %M] | |
   | Age | [primary age range] | |
   | Location | [top countries/cities] | |
   | Interests | [categories] | |
   
   **Audience Quality Score**: [X/10]
   - Real followers estimate: [%]
   - Audience-brand overlap: [High/Medium/Low]
   
   ### Content Analysis
   
   **Content Style**:
   - Primary format: [format]
   - Posting frequency: [X posts/week]
   - Aesthetic: [description]
   - Tone: [description]
   
   **Top Performing Content**:
   1. [Content 1]: [engagement]
   2. [Content 2]: [engagement]
   3. [Content 3]: [engagement]
   
   **Brand Fit Assessment**:
   - Visual alignment: [High/Medium/Low]
   - Value alignment: [High/Medium/Low]
   - Audience alignment: [High/Medium/Low]
   
   ### Partnership History
   
   **Past Brand Partnerships**:
   | Brand | Date | Content Type | Est. Performance |
   |-------|------|--------------|------------------|
   | [brand 1] | [date] | [type] | [performance] |
   | [brand 2] | [date] | [type] | [performance] |
   
   **Competitor Partnerships**: [Yes/No - details]
   
   ### Contact Information
   
   - **Email**: [if public]
   - **Agency/Manager**: [if applicable]
   - **Contact Method**: [best approach]
   
   ### Fit Score Summary
   
   | Factor | Score (1-5) |
   |--------|-------------|
   | Audience match | [score] |
   | Content quality | [score] |
   | Brand alignment | [score] |
   | Engagement quality | [score] |
   | Authenticity | [score] |
   | **Total** | **[X/25]** |
   
   **Recommendation**: ⭐ [Highly Recommended / Recommended / Consider / Pass]
   
   **Why They're a Good Fit**:
   [2-3 sentences explaining the fit]
   
   **Potential Concerns**:
   - [Concern 1 if any]
   
   ---
   ```

5. **Compile Discovery List**

   ```markdown
   # Influencer Discovery Results
   
   **Search Date**: [date]
   **Brand/Campaign**: [name]
   **Criteria Used**: [summary]
   
   ## Summary Statistics
   
   | Metric | Count |
   |--------|-------|
   | Total Candidates Reviewed | [#] |
   | Passed Initial Screening | [#] |
   | Highly Recommended | [#] |
   | Recommended | [#] |
   | To Consider | [#] |
   
   ### By Platform
   
   | Platform | Count | Avg Followers | Avg ER |
   |----------|-------|---------------|--------|
   | Instagram | [#] | [avg] | [%] |
   | TikTok | [#] | [avg] | [%] |
   | YouTube | [#] | [avg] | [%] |
   
   ### By Tier
   
   | Tier | Follower Range | Count | Est. Cost Range |
   |------|----------------|-------|-----------------|
   | Mega | 1M+ | [#] | [range] |
   | Macro | 100K-1M | [#] | [range] |
   | Micro | 10K-100K | [#] | [range] |
   | Nano | <10K | [#] | [range] |
   
   ## Top Recommendations
   
   ### Tier 1: Must Reach Out
   
   | Rank | Handle | Platform | Followers | ER | Fit Score | Why |
   |------|--------|----------|-----------|----|-----------| ----|
   | 1 | @[handle] | [platform] | [count] | [%] | [X/25] | [brief reason] |
   | 2 | @[handle] | [platform] | [count] | [%] | [X/25] | [brief reason] |
   | 3 | @[handle] | [platform] | [count] | [%] | [X/25] | [brief reason] |
   
   ### Tier 2: Strong Candidates
   
   | Handle | Platform | Followers | ER | Fit Score | Notes |
   |--------|----------|-----------|----|-----------| ------|
   | @[handle] | [platform] | [count] | [%] | [X/25] | [notes] |
   
   ### Tier 3: Worth Considering
   
   | Handle | Platform | Followers | ER | Fit Score | Notes |
   |--------|----------|-----------|----|-----------| ------|
   | @[handle] | [platform] | [count] | [%] | [X/25] | [notes] |
   
   ## Influencer Mix Recommendation
   
   For a balanced campaign, consider:
   
   | Tier | Recommended # | Role | Budget % |
   |------|---------------|------|----------|
   | Macro | [#] | Reach & credibility | [%] |
   | Micro | [#] | Engagement & trust | [%] |
   | Nano | [#] | Authenticity & UGC | [%] |
   
   ## Next Steps
   
   1. Review top recommendations with [fit-scorer](../../map/fit-scorer/SKILL.md)
   2. Develop outreach strategy with [outreach-manager](../../activate/outreach-manager/SKILL.md)
   3. Create campaign briefs with [brief-generator](../../plan/brief-generator/SKILL.md)
   
   ## Export Options
   
   - [ ] Export to CSV for CRM import
   - [ ] Create outreach tracking sheet
   - [ ] Generate brief templates for top picks
   ```

6. **Provide Additional Insights**

   ```markdown
   ## Discovery Insights
   
   ### Niche Observations
   
   **Content Trends**:
   - Most successful content type: [type]
   - Trending topics: [topics]
   - Underutilized angles: [opportunities]
   
   **Competitive Picture**:
   - Brands most active: [brands]
   - Influencers oversaturated: [who to avoid]
   - Untapped opportunities: [gaps]
   
   ### Recommendations for Future Searches
   
   - Consider expanding to: [adjacent niches]
   - Platform opportunity: [underutilized platform]
   - Timing: [when to search again]
   ```

## When to Use This Skill

- Building an influencer roster from scratch
- Expanding into new platforms or niches
- Finding replacements for churned influencer partners
- Discovering micro and nano influencers at scale
- Identifying competitors' influencer partners
- Building an always-on influencer pipeline

## What This Skill Does

1. **Multi-Platform Search**: Finds influencers across Instagram, TikTok, YouTube, Twitter, etc.
2. **Criteria Matching**: Filters by niche, follower count, engagement, location
3. **Audience Analysis**: Evaluates if their audience matches your target
4. **Content Assessment**: Reviews content quality and style fit
5. **Authenticity Screening**: Identifies potential red flags
6. **List Building**: Compiles organized, actionable influencer lists

## Example

**User**: "Find 15 micro-influencers (10K-100K followers) in the sustainable fashion space for a new eco-friendly clothing brand"

**Output**:

```markdown
# Influencer Discovery: Sustainable Fashion Micro-Influencers

## Top 5 Recommendations

### 1. @sustainablestyle_sarah
- **Platform**: Instagram (47K) + TikTok (23K)
- **Engagement**: 5.2% IG, 8.1% TikTok
- **Location**: Los Angeles, CA
- **Content**: Outfit styling, brand reviews, thrift hauls
- **Audience**: 78% F, 25-34 primary, US-based
- **Fit Score**: 24/25 ⭐

**Why**: Authentic focus on sustainable fashion since 2019, highly engaged audience that matches target demo exactly, previous successful partnerships with similar eco brands. Known for honest reviews.

**Past Partnerships**: Reformation, ThredUp, Girlfriend Collective

### 2. @eco_emma_style
[... continues with 14 more influencers ...]

## Summary

Found 43 candidates, 15 meet all criteria with fit scores above 18/25.

**Recommended Mix**:
- 5 with higher engagement (>5%) for key content
- 7 mid-tier for volume and variety  
- 3 rising stars for early partnership potential

**Next Steps**: Run through fit-scorer for final ranking, begin outreach to top 5.
```

## Tips for Success

1. **Quality over quantity** - Better to have 10 perfect fits than 100 maybes
2. **Verify authenticity** - Check for fake followers, engagement pods
3. **Review recent content** - Ensure consistent quality and brand safety
4. **Consider past partnerships** - Learn from their collaboration history
5. **Look beyond followers** - Engagement quality matters more
6. **Check all platforms** - Multi-platform creators offer more value
7. **Save for later** - Build a pipeline, not just campaign lists

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipes and opt-in MCP layer.
- C3 benchmark at [references/c3/scoring-architecture.md](../../references/c3/scoring-architecture.md) — scoring framework that fit-scorer applies downstream.
- Siblings in the Map phase: [fit-scorer](../../map/fit-scorer/SKILL.md), [competitor-tracker](../../map/competitor-tracker/SKILL.md).

## Next Best Skill

**Primary**: [fit-scorer](../../map/fit-scorer/SKILL.md) — score and rank the discovered candidates with weighted criteria before outreach.

**Alternates (same IMPACT family)**:
- [competitor-tracker](../../map/competitor-tracker/SKILL.md) — when discovery surfaced competitor-saturated creators and you want to map the competitive field first.
- [audience-analyzer](../../insight/audience-analyzer/SKILL.md) — when the target audience is still fuzzy and criteria need sharpening before a re-search.

**Termination**: Maintain a visited-set. If a skill has already been invoked this session, stop and report chain-complete rather than re-invoking it. Max chain depth is 3 hops from the originating request; stop and summarize when reached.

## Related Skills

- [audience-analyzer](../../insight/audience-analyzer/SKILL.md) - Define who to reach
- [fit-scorer](../../map/fit-scorer/SKILL.md) - Score and rank discovered influencers
- [competitor-tracker](../../map/competitor-tracker/SKILL.md) - Find competitor influencers
- [outreach-manager](../../activate/outreach-manager/SKILL.md) - Contact discovered influencers
