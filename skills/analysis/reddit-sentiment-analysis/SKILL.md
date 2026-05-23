---
name: reddit-sentiment-analysis
description: Conduct comprehensive sentiment analysis of Reddit discussions for any product, brand, company, or topic. Analyzes what people like, dislike, and wish were different with structured output summaries.
---

# Reddit Sentiment Analysis Skill

## Purpose

This skill enables systematic sentiment analysis of Reddit discussions to understand community opinions, preferences, and desires about products, brands, games, companies, or any topic. It produces actionable insights about what people like, what they criticize, and what improvements they wish for.

## When to Use This Skill

Use this skill when you need to:
- Analyze community sentiment about games, products, or brands
- Understand what features/aspects users appreciate
- Identify common complaints and pain points
- Discover what improvements or changes users desire
- Generate competitive intelligence from community discussions
- Track sentiment trends over time for a topic
- Make data-driven product decisions based on user feedback

## Prerequisites

This skill requires the Reddit MCP server to be configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["mcp-server-reddit"]
    }
  }
}
```

## Core Workflow

### Phase 1: Target Identification and Data Collection

**1. Define Analysis Target**
   - Identify the product/brand/game/topic to analyze
   - Determine relevant subreddits (e.g., r/gaming, r/Games, product-specific subs)
   - Set time frame (recent posts, top posts from month/year)
   - Define scope (how many posts/comments to analyze)

**2. Collect Reddit Data**
   - Use `mcp__reddit__get_subreddit_hot_posts` for trending discussions
   - Use `mcp__reddit__get_subreddit_top_posts` for highly-rated content
   - Use `mcp__reddit__get_post_content` for detailed post + comments
   - Collect minimum 10-20 posts for meaningful analysis
   - Include both posts and top-level comments

### Phase 2: Sentiment Classification

**3. Analyze Each Discussion**

For each post and comment, classify sentiment into:

**POSITIVE Signals:**
- Explicit praise: "I love...", "amazing", "best", "fantastic"
- Recommendations: "highly recommend", "must-try", "worth it"
- Emotional positivity: "fun", "enjoyable", "satisfying", "addicting"
- Problem solutions: "finally fixed", "works great now"
- Comparative praise: "better than X", "superior to"

**NEGATIVE Signals:**
- Explicit criticism: "hate", "terrible", "worst", "awful"
- Disappointment: "let down", "expected more", "overhyped"
- Problems: "broken", "doesn't work", "buggy", "crashes"
- Frustration: "annoying", "frustrating", "ridiculous"
- Regret: "waste of money", "not worth it", "refunded"

**NEUTRAL Signals:**
- Questions without sentiment
- Factual statements
- Technical discussions
- Requests for information

**WISH/DESIRE Signals:**
- "I wish...", "they should...", "would be better if..."
- "needs more...", "lacking...", "missing..."
- "hope they add...", "waiting for..."
- Feature requests and suggestions

### Phase 3: Entity and Aspect Extraction

**4. Identify Specific Aspects Mentioned**

Extract what specifically is being discussed:
- **Features**: gameplay mechanics, UI/UX, specific capabilities
- **Performance**: speed, stability, optimization, bugs
- **Content**: story, levels, variety, depth
- **Value**: pricing, monetization, cost-benefit
- **Support**: customer service, updates, community engagement
- **Comparisons**: versus competitors, previous versions

### Phase 4: Aggregation and Summarization

**5. Create Structured Summary**

Generate output in this format:

```markdown
# Sentiment Analysis: [Topic/Product Name]

**Analysis Period**: [Date Range]
**Subreddits Analyzed**: [List]
**Posts Analyzed**: [Number]
**Comments Analyzed**: [Number]

## Overall Sentiment Score
- Positive: X%
- Negative: Y%
- Neutral: Z%
- Mixed: W%

## What People LIKE
1. **[Aspect/Feature Name]** (mentioned X times, Y% positive)
   - Representative quotes: "[quote 1]", "[quote 2]"
   - Common themes: [summary]

2. **[Another Aspect]** (...)
   - Representative quotes: ...
   - Common themes: ...

[Continue for top 5-7 positive aspects]

## What People DISLIKE
1. **[Problem/Issue Name]** (mentioned X times, Y% negative)
   - Representative quotes: "[quote 1]", "[quote 2]"
   - Common complaints: [summary]
   - Severity: [Low/Medium/High based on frequency and intensity]

2. **[Another Issue]** (...)
   - Representative quotes: ...
   - Common complaints: ...
   - Severity: ...

[Continue for top 5-7 negative aspects]

## What People WISH FOR
1. **[Feature/Improvement Request]** (mentioned X times)
   - Representative quotes: "[quote 1]", "[quote 2]"
   - Common requests: [summary]
   - Urgency: [Low/Medium/High based on frequency and intensity]

2. **[Another Request]** (...)
   - Representative quotes: ...
   - Common requests: ...
   - Urgency: ...

[Continue for top 5-7 requests]

## Key Insights
- [Insight 1: Major finding about sentiment patterns]
- [Insight 2: Surprising or notable trend]
- [Insight 3: Competitive advantages/disadvantages]
- [Insight 4: Recommended actions based on sentiment]

## Trending Topics
- [Topic 1]: [Brief description of emerging discussion]
- [Topic 2]: [Brief description]

## Competitor Mentions
- [Competitor 1]: [Sentiment when mentioned, context]
- [Competitor 2]: [Sentiment when mentioned, context]
```

## Implementation Protocol

### Step 1: Create Todo List
```javascript
TodoWrite([
  "Identify target subreddits for analysis",
  "Collect hot posts from subreddit(s)",
  "Collect top posts from time period",
  "Fetch detailed post content and comments",
  "Classify sentiment for each post/comment",
  "Extract aspects and entities mentioned",
  "Aggregate positive sentiment patterns",
  "Aggregate negative sentiment patterns",
  "Aggregate wish/desire patterns",
  "Calculate sentiment percentages",
  "Generate structured summary report"
])
```

### Step 2: Parallel Data Collection

**CRITICAL**: Batch all Reddit API calls in a single message:

```javascript
[Single Message - All Data Collection]:
  mcp__reddit__get_subreddit_hot_posts({subreddit_name: "gaming", limit: 20})
  mcp__reddit__get_subreddit_top_posts({subreddit_name: "gaming", time: "month", limit: 20})
  mcp__reddit__get_subreddit_hot_posts({subreddit_name: "Games", limit: 20})
  mcp__reddit__get_subreddit_top_posts({subreddit_name: "Games", time: "month", limit: 20})
```

### Step 3: Parallel Comment Analysis

For each relevant post ID, fetch details in parallel:

```javascript
[Single Message - All Post Details]:
  mcp__reddit__get_post_content({post_id: "abc123", comment_depth: 3, comment_limit: 20})
  mcp__reddit__get_post_content({post_id: "def456", comment_depth: 3, comment_limit: 20})
  mcp__reddit__get_post_content({post_id: "ghi789", comment_depth: 3, comment_limit: 20})
  // ... up to 10-20 posts in parallel
```

### Step 4: Sentiment Analysis Engine

For each piece of content (post title, post body, comment):

1. **Tokenize and normalize text**
   - Convert to lowercase
   - Remove URLs, special characters
   - Identify key phrases

2. **Apply sentiment scoring**
   ```javascript
   function analyzeSentiment(text) {
     const positive_score = countMatches(text, POSITIVE_KEYWORDS);
     const negative_score = countMatches(text, NEGATIVE_KEYWORDS);
     const wish_score = countMatches(text, WISH_KEYWORDS);

     return {
       sentiment: determineOverallSentiment(positive_score, negative_score),
       confidence: calculateConfidence(positive_score, negative_score),
       wishes: wish_score > 0,
       aspects: extractAspects(text)
     };
   }
   ```

3. **Extract context and aspects**
   - What noun/feature is being discussed?
   - What adjectives describe it?
   - What verbs indicate action/desire?

### Step 5: Generate Report

Save the structured summary to `/docs/reddit-sentiment-analysis-[topic]-[date].md`

## Configuration Options

### Basic Analysis (Quick)
- Subreddits: 1-2
- Posts: 10-20
- Comments per post: 10-15
- Time: ~5 minutes

### Comprehensive Analysis (Deep)
- Subreddits: 3-5
- Posts: 40-60
- Comments per post: 20-30
- Time: ~15 minutes

### Competitive Analysis (Wide)
- Subreddits: 5-10 (including competitor subs)
- Posts: 60-100
- Comments per post: 15-20
- Time: ~20 minutes

## Example Usage

### Example 1: Gaming Sentiment Analysis

```
User: "Analyze Reddit sentiment about Elden Ring"

Agent workflow:
1. Create todos for analysis pipeline
2. Identify subreddits: r/Eldenring, r/gaming, r/Games
3. Collect hot + top posts (parallel): 60 posts total
4. Fetch post details (parallel): 30 most relevant posts
5. Analyze ~500 comments for sentiment
6. Extract aspects: combat, difficulty, exploration, story, performance
7. Generate summary showing:
   - LIKES: Combat system (95%), exploration (92%), art direction (88%)
   - DISLIKES: Performance issues (67%), unclear quest objectives (54%)
   - WISHES: Better quest tracking, PC optimization, more checkpoints
8. Save report to docs/reddit-sentiment-analysis-eldenring-2025-01-26.md
```

### Example 2: Product Brand Analysis

```
User: "What do people think about Tesla on Reddit?"

Agent workflow:
1. Create todos for brand analysis
2. Identify subreddits: r/teslamotors, r/electricvehicles, r/cars
3. Collect discussions mentioning "Tesla" (100 posts)
4. Analyze sentiment across aspects: quality, service, pricing, features
5. Generate brand perception summary:
   - LIKES: Autopilot, acceleration, software updates
   - DISLIKES: Build quality, service wait times, pricing
   - WISHES: Better quality control, more service centers, lower prices
   - Competitive position vs. other EVs
```

## Best Practices

### DO:
- ✅ Analyze multiple subreddits for balanced perspective
- ✅ Include both hot and top posts for recency + quality
- ✅ Read comments, not just post titles (comments have rich sentiment)
- ✅ Provide direct quotes as evidence
- ✅ Quantify sentiment with percentages and counts
- ✅ Organize by aspect/feature, not just positive/negative
- ✅ Save reports to `/docs/` directory
- ✅ Batch all API calls in single messages

### DON'T:
- ❌ Only analyze one subreddit (bias risk)
- ❌ Ignore comment sentiment (posts alone insufficient)
- ❌ Make claims without quote evidence
- ❌ Mix multiple products in one analysis (confusing)
- ❌ Save reports to root directory
- ❌ Make sequential API calls (use parallel batching)

## Advanced Features

### Temporal Sentiment Tracking

Compare sentiment across time periods:
```javascript
[Parallel Time-Based Analysis]:
  get_subreddit_top_posts({time: "week"})
  get_subreddit_top_posts({time: "month"})
  get_subreddit_top_posts({time: "year"})
```

Generate trend report showing sentiment evolution.

### Competitive Benchmarking

Analyze multiple products simultaneously:
```javascript
[Parallel Competitive Analysis]:
  // Collect data for Product A
  // Collect data for Product B
  // Collect data for Product C
```

Generate comparative sentiment matrix.

### Aspect-Specific Deep Dive

Focus on one feature/aspect across all mentions:
```javascript
// Filter all content mentioning "multiplayer" or "co-op"
// Analyze sentiment specifically about that aspect
// Generate aspect-focused report
```

## Output Files

All analysis reports are saved to:
- `/docs/reddit-sentiment-analysis-[topic]-[date].md` - Main report
- `/docs/reddit-raw-data-[topic]-[date].json` - Raw data (optional)

## Integration with Other Skills

This skill works well with:
- **competitive-analysis**: Use sentiment data for market positioning
- **product-roadmap**: Prioritize features based on user wishes
- **market-research**: Combine with other data sources
- **trend-analysis**: Track sentiment changes over time

## Troubleshooting

**Issue**: Not enough posts found
- **Solution**: Expand to more subreddits, increase time range

**Issue**: Sentiment too polarized (all positive or negative)
- **Solution**: Check subreddit bias (fan subs vs. general subs)

**Issue**: Missing key aspects in analysis
- **Solution**: Increase comment depth and limit

**Issue**: Analysis taking too long
- **Solution**: Reduce number of posts, focus on top posts only

## Summary

This skill transforms unstructured Reddit discussions into actionable sentiment insights by:
1. Systematically collecting relevant posts and comments
2. Classifying sentiment with context and evidence
3. Extracting specific aspects and features discussed
4. Aggregating patterns into structured summaries
5. Providing quantified insights with direct quotes
6. Identifying what users like, dislike, and wish for
7. Delivering reports ready for product/business decisions

The output is a comprehensive, evidence-based understanding of community sentiment that can drive product development, marketing strategy, and competitive positioning.
