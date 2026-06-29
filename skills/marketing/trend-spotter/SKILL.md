---
name: trend-spotter
description: 'Use when the user asks to "find trending topics", "what trends should my brand jump on", or "time a campaign around a cultural moment"; produces a ranked trend report with brand-fit scores, format calls (rising/peak/declining), a cultural calendar, and go/skip recommendations. Not for finding the creators to run those trends — use influencer-discovery.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Use when planning campaign timing and themes, deciding whether to join a hashtag, sound, or challenge, scouting trending content formats on a platform, mapping upcoming cultural moments to lead times, or checking which trends competitors have adopted or missed. Auto-activate when the request is about what is trending, what to post around, or when to act."
argument-hint: "<brand or industry> [platform] [time horizon]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Insight
---

# Trend Spotter

This skill helps you identify and capitalize on trends that matter to your audience. It monitors social conversations, emerging topics, viral content formats, and cultural moments to inform influencer campaign timing and content strategy.

## Quick Start

Shortest invocation:

```
What trends are relevant for [brand/industry] right now?
```

Common scenario — analyze one specific trend before committing:

```
Should [brand] participate in [trend/challenge]? Score the brand fit and give a go/skip call.
```

## Skill Contract

- **Reads**: brand/industry, target platforms, audience, geographic focus, time horizon, content categories; prior audience and niche findings from `memory/influencer/` if present.
- **Writes**: a trend report (ranked trends, brand-fit scores, format calls, cultural calendar, go/skip recommendations) to `memory/influencer/trend-spotter/YYYY-MM-DD-<topic>.md`.
- **Promotes**: durable facts (top trends to act on now, trends to avoid, next review date) to `memory/hot-cache.md`.
- **Done when**:
  1. Each candidate trend has a brand-fit score and a go / caution / skip call.
  2. The report names the top 3 trends to act on now plus a watch list and an avoid list.
  3. Action items carry a timing window and a content-format recommendation.
- **Primary next skill**: [influencer-discovery](../../map/influencer-discovery/SKILL.md) — find the creators who can execute the chosen trends.

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This skill works with no live integrations (Tier 1): ask the user for the brand, platforms, audience, and time horizon, then reason from those inputs. Where a tool would sharpen the read, use a `~~` connector placeholder:

- `~~social platform analytics` — trending hashtags, sounds, and view counts per platform.
- `~~trend database` — emerging topics, challenge participation, and growth rates.
- `~~social listening` — cultural conversations and sentiment around a topic.
- `~~competitor tracking` — which trends rival brands have adopted and how they performed.

No connector is required to produce a useful report. See [CONNECTORS.md](../../CONNECTORS.md) for the free/keyless recipe per category.

## Instructions

When a user requests trend analysis:

1. **Define Trend Parameters**

   ```markdown
   ### Trend Analysis Parameters

   **Brand/Industry**: [name]
   **Target Platforms**: [platforms]
   **Target Audience**: [audience description]
   **Geographic Focus**: [regions]
   **Time Horizon**: [immediate/this month/this quarter]
   **Content Categories**: [relevant categories]
   ```

2. **Identify Current Trends**

   ```markdown
   ## Current Trends

   ### Trending Topics

   | Topic | Platform | Volume | Relevance | Lifespan |
   |-------|----------|--------|-----------|----------|
   | [Topic 1] | [platform] | High/Med/Low | ⭐⭐⭐⭐⭐ | [days/weeks] |
   | [Topic 2] | [platform] | High/Med/Low | ⭐⭐⭐⭐ | [days/weeks] |
   | [Topic 3] | [platform] | High/Med/Low | ⭐⭐⭐ | [days/weeks] |

   ### Trending Hashtags

   | Hashtag | Platform | Posts | Growth | Brand Fit |
   |---------|----------|-------|--------|-----------|
   | #[hashtag1] | [platform] | [volume] | +[%] | ✅/⚠️/❌ |
   | #[hashtag2] | [platform] | [volume] | +[%] | ✅/⚠️/❌ |

   ### Trending Audio/Sounds

   | Sound | Platform | Uses | Origin | Brand Safe |
   |-------|----------|------|--------|------------|
   | [sound 1] | TikTok | [count] | [source] | ✅/⚠️/❌ |
   | [sound 2] | Reels | [count] | [source] | ✅/⚠️/❌ |

   ### Trending Challenges

   | Challenge | Platforms | Participation | Difficulty | Risk |
   |-----------|-----------|---------------|------------|------|
   | [challenge 1] | [platforms] | [level] | [easy/medium/hard] | [risk level] |
   ```

3. **Analyze Content Format Trends**

   ```markdown
   ## Trending Content Formats

   ### Video Formats

   | Format | Platform | Performance | Example | Adoption |
   |--------|----------|-------------|---------|----------|
   | [Format 1] | [platform] | [engagement] | [example] | Rising/Peak/Declining |
   | [Format 2] | [platform] | [engagement] | [example] | Rising/Peak/Declining |

   **Hot Formats Right Now**:

   1. **[Format Name]**
      - What it is: [description]
      - Why it works: [explanation]
      - Best for: [use cases]
      - How to adapt: [brand approach]
      - Example: [link or description]

   2. **[Format Name]**
      - What it is: [description]
      - Why it works: [explanation]
      - Best for: [use cases]
      - How to adapt: [brand approach]

   ### Emerging Formats to Watch

   | Format | Platform | Status | When to Adopt |
   |--------|----------|--------|---------------|
   | [format] | [platform] | Early adopter phase | Now for first-mover advantage |
   | [format] | [platform] | Growing | Next 2-4 weeks |

   ### Declining Formats to Avoid

   | Format | Platform | Why Declining | Alternative |
   |--------|----------|---------------|-------------|
   | [format] | [platform] | [reason] | [alternative] |
   ```

4. **Track Cultural Moments**

   ```markdown
   ## Cultural Calendar & Moments

   ### Upcoming Cultural Moments

   | Event/Moment | Date | Relevance | Lead Time | Opportunity |
   |--------------|------|-----------|-----------|-------------|
   | [Event 1] | [date] | ⭐⭐⭐⭐⭐ | [weeks needed] | [opportunity description] |
   | [Event 2] | [date] | ⭐⭐⭐⭐ | [weeks needed] | [opportunity description] |
   | [Event 3] | [date] | ⭐⭐⭐ | [weeks needed] | [opportunity description] |

   ### Cultural Conversations

   **Active Conversations to Join**:

   | Conversation | Platforms | Sentiment | Brand Angle |
   |--------------|-----------|-----------|-------------|
   | [topic] | [platforms] | Positive/Mixed/Negative | [how to participate] |

   **Conversations to Avoid**:

   | Topic | Risk Level | Why Avoid |
   |-------|------------|-----------|
   | [topic] | High | [reason] |

   ### Seasonal Opportunities

   | Season/Period | Themes | Content Ideas | Influencer Angle |
   |---------------|--------|---------------|------------------|
   | [period] | [themes] | [ideas] | [approach] |
   ```

5. **Assess Trend Relevance**

   ```markdown
   ## Trend Relevance Assessment

   ### Trend: [Name]

   **Overview**:
   - What: [description]
   - Origin: [where it started]
   - Current Status: [rising/peaking/declining]
   - Platform: [primary platforms]
   - Audience: [who's participating]

   **Brand Fit Analysis**:

   | Factor | Score | Notes |
   |--------|-------|-------|
   | Audience alignment | [1-5] | [explanation] |
   | Brand value fit | [1-5] | [explanation] |
   | Content adaptability | [1-5] | [explanation] |
   | Risk level | [1-5] | [explanation] |
   | Timing window | [1-5] | [explanation] |
   | **Total Score** | [X/25] | |

   **Recommendation**: ✅ Participate / ⚠️ Proceed with caution / ❌ Skip

   **If Participating**:
   - Best approach: [how to adapt]
   - Timing: [when to post]
   - Influencer type: [who should create]
   - Risk mitigation: [how to stay safe]

   **If Skipping**:
   - Reason: [why not]
   - Alternative: [what to do instead]
   ```

6. **Monitor Competitor Trend Adoption**

   ```markdown
   ## Competitor Trend Activity

   ### Competitor Trend Adoption

   | Competitor | Recent Trends Adopted | Performance | Learnings |
   |------------|----------------------|-------------|-----------|
   | [Comp 1] | [trends] | [results if known] | [what to learn] |
   | [Comp 2] | [trends] | [results if known] | [what to learn] |

   ### Gap Analysis

   **Trends competitors are missing**:
   - [Trend 1]: [opportunity for you]
   - [Trend 2]: [opportunity for you]

   **Trends competitors are overusing**:
   - [Trend 1]: [saturation level]

   ### Best Practices from Competitors

   | Competitor | What They Did Well | How to Apply |
   |------------|-------------------|--------------|
   | [comp] | [execution] | [your approach] |
   ```

7. **Generate Trend Report**

   ```markdown
   # Trend Report: [Brand/Industry]

   **Report Date**: [date]
   **Time Horizon**: [period covered]

   ## Executive Summary

   **Top 3 Trends to Act On Now**:
   1. [Trend 1]: [why and how]
   2. [Trend 2]: [why and how]
   3. [Trend 3]: [why and how]

   **Trends to Watch**:
   - [Trend]: [when it might peak]

   **Trends to Avoid**:
   - [Trend]: [why]

   ## Priority Action Items

   ### Immediate (This Week)

   1. **[Trend/Opportunity]**
      - Action: [specific action]
      - Influencer approach: [type of creator]
      - Content format: [format]
      - Hashtags: [relevant hashtags]

   ### Short-term (This Month)

   1. **[Trend/Opportunity]**
      - Action: [specific action]
      - Timeline: [when to execute]

   ### Plan Ahead (This Quarter)

   | Opportunity | Timing | Prep Needed | Budget Consideration |
   |-------------|--------|-------------|---------------------|
   | [opportunity] | [date] | [weeks] | [notes] |

   ## Content Format Recommendations

   | Platform | Hot Formats | Content Ideas |
   |----------|-------------|---------------|
   | TikTok | [formats] | [ideas] |
   | Instagram | [formats] | [ideas] |
   | YouTube | [formats] | [ideas] |

   ## Hashtag Strategy

   **Trending to use**:
   - #[hashtag] - [context]
   - #[hashtag] - [context]

   **Brand + Trend combinations**:
   - #[brand] + #[trend] = [combination]

   ## Risk Assessment

   | Trend | Risk Level | Mitigation |
   |-------|------------|------------|
   | [trend] | [level] | [how to stay safe] |

   ## Next Steps

   1. Brief influencers on [top trend]
   2. Create content calendar incorporating [cultural moments]
   3. Monitor [emerging trends] for right timing
   4. Review trend report again on [date]
   ```

## When to Use This Skill

- Planning campaign timing and themes
- Identifying trending content formats to incorporate
- Finding viral moments to capitalize on
- Discovering emerging hashtags and challenges
- Understanding cultural conversations relevant to your brand
- Staying ahead of competitor trend adoption

## What This Skill Does

1. **Trend Identification**: Spots emerging trends across platforms
2. **Relevance Assessment**: Evaluates trend fit for your brand
3. **Timing Analysis**: Determines optimal moment to act
4. **Format Discovery**: Identifies trending content formats
5. **Cultural Monitoring**: Tracks cultural moments and conversations
6. **Competitor Tracking**: Monitors competitor trend adoption

## Example

**User**: "What TikTok trends should a fitness brand run right now?"

**Output**:

```markdown
# TikTok Fitness Trends Report

## Top Trends to Act On Now

### 1. "Hot Girl Walk" Evolution
- **What**: Walking content with self-improvement audio
- **Volume**: 2.3B views on related hashtags
- **Status**: Still growing, evolved into multiple variations
- **Brand Fit**: ⭐⭐⭐⭐⭐ Strong for fitness apparel/supplements
- **How to Use**: Partner with lifestyle influencers for "walk with me" content featuring products

### 2. "75 Hard" / Challenge Content
- **What**: Fitness challenge documentation
- **Volume**: 1.8B views
- **Status**: Evergreen, consistent interest
- **Brand Fit**: ⭐⭐⭐⭐ Good for supplements, programs
- **How to Use**: Sponsor influencers doing challenges, provide products as part of their journey

### 3. GRWM (Get Ready With Me) Workout Edition
- **What**: Pre-workout routines showing products used
- **Volume**: Rising trend
- **Status**: Early growth phase - first mover advantage
- **Brand Fit**: ⭐⭐⭐⭐⭐ Strong for all fitness products
- **How to Use**: Brief creators on "GRWM: Gym Edition" showing outfit + supplements + routine

## Content Format Recommendation

Best performing format: 15-30 second videos with:
- Hook in first 2 seconds
- Trending audio
- Text overlay
- Quick cuts

## Hashtags to Use
- #FitTok (42B views)
- #GymTok (18B views)
- #[Your product category specific]

## Action: Brief your influencers this week on GRWM Gym Edition content
```

## Tips for Success

1. **Act fast but thoughtfully** - Trends move quickly, but brand safety matters
2. **Adapt, don't copy** - Put your brand's spin on trends
3. **Consider timing** - Early is better, but not too early
4. **Monitor continuously** - Set up regular trend reviews
5. **Know when to skip** - Not every trend is for every brand

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — HOT/WARM/COLD memory tiers and save paths.
- [CONNECTORS.md](../../CONNECTORS.md) — free/keyless data recipe per connector category.
- C3 benchmark scoring at [references/c3/scoring-architecture.md](../../references/c3/scoring-architecture.md) — for grading trend-driven creative output downstream.
- Siblings in the Insight phase: [audience-analyzer](../audience-analyzer/SKILL.md), [niche-researcher](../niche-researcher/SKILL.md).

## Next Best Skill

- **Primary**: [influencer-discovery](../../map/influencer-discovery/SKILL.md) — turn the chosen trends into a shortlist of creators who can execute them.
- **Alternate**: [audience-analyzer](../audience-analyzer/SKILL.md) — confirm which trends actually resonate with your audience before committing.
- **Alternate**: [niche-researcher](../niche-researcher/SKILL.md) — dig into niche-specific trend pockets the broad scan missed.

Termination: keep a visited-set of skills invoked this session. If the primary next skill was already run this turn, stop and report the chain complete rather than re-invoking. Max handoff depth is 3; once reached, summarize and return control to the user.
