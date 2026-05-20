---
name: reddit-insights
description: |
  Search and analyze Reddit content using semantic AI search via reddit-insights.com MCP server.
  Use when you need to: (1) Find user pain points and frustrations for product ideas, (2) Discover niche markets or underserved needs, (3) Research what people really think about products/topics, (4) Find content inspiration from real discussions, (5) Analyze sentiment and trends on Reddit, (6) Validate business ideas with real user feedback.
  Triggers: reddit search, find pain points, market research, user feedback, what do people think about, reddit trends, niche discovery, product validation.
---

# Reddit Insights MCP

Semantic search across millions of Reddit posts. Unlike keyword search, this understands intent and meaning.

## Why This vs ChatGPT?

**Problem with ChatGPT:** It has no real-time Reddit access. It can't search current discussions, can't filter by engagement, and can't show you what people are saying RIGHT NOW about your topic.

**This skill provides:**
1. **Live semantic search** - Searches millions of Reddit posts with AI-powered intent matching (not just keywords)
2. **Engagement filtering** - Sort by upvotes/comments to find validated pain points
3. **Sentiment analysis** - Automatically tags posts as Discussion/Q&A/Story/News
4. **Relevance scoring** - Shows 0-1 match score so you know which results matter
5. **Subreddit intelligence** - Browse communities, see trending topics, get recent posts
6. **Direct links** - Every result includes Reddit URL for full context

**You can replicate this** by manually browsing Reddit, searching multiple subreddits, reading hundreds of posts, taking notes, and synthesizing patterns. Takes 1-2 hours per research query. This skill does it in 15-20 seconds.

## Setup

### 1. Get API Key (free tier available)
1. Sign up at https://reddit-insights.com
2. Go to Settings → API
3. Copy your API key

### 2. Install MCP Server

**For Claude Desktop** - add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx",
      "args": ["-y", "reddit-insights-mcp"],
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**For Clawdbot** - add to `config/mcporter.json`:
```json
{
  "mcpServers": {
    "reddit-insights": {
      "command": "npx reddit-insights-mcp",
      "env": {
        "REDDIT_INSIGHTS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Verify installation:**
```bash
mcporter list reddit-insights
```

## Available Tools

| Tool | Purpose | Key Params |
|------|---------|------------|
| `reddit_search` | Semantic search across posts | `query` (natural language), `limit` (1-100) |
| `reddit_list_subreddits` | Browse available subreddits | `page`, `limit`, `search` |
| `reddit_get_subreddit` | Get subreddit details + recent posts | `subreddit` (without r/) |
| `reddit_get_trends` | Get trending topics | `filter` (latest/today/week/month), `category` |

## Performance Notes

- **Response time:** 12-25 seconds (varies by query complexity)
  - Simple queries: ~12-15s
  - Complex semantic queries: ~17-20s
  - Heavy load periods: up to 25s
- **Best results:** Specific products, emotional language, comparison questions
- **Weaker results:** Abstract concepts, non-English queries, generic business terms
- **Sweet spot:** Questions a real person would ask on Reddit

## Best Use Cases (Tested)

| Use Case | Effectiveness | Why |
|----------|--------------|-----|
| Product comparisons (A vs B) | ⭐⭐⭐⭐⭐ | Reddit loves debates |
| Tool/app recommendations | ⭐⭐⭐⭐⭐ | High-intent discussions |
| Side hustle/money topics | ⭐⭐⭐⭐⭐ | Engaged communities |
| Pain point discovery | ⭐⭐⭐⭐ | Emotional posts rank well |
| Health questions | ⭐⭐⭐⭐ | Active health subreddits |
| Technical how-to | ⭐⭐⭐ | Better to search specific subreddits |
| Abstract market research | ⭐⭐ | Too vague for semantic search |
| Non-English queries | ⭐ | Reddit is English-dominant |

## Query Strategies (Tested with Real Data)

### ✅ Excellent Queries (relevance 0.70+)

**Product Comparisons** (best results!):
```
"Notion vs Obsidian for note taking which one should I use"
→ Relevance: 0.72-0.81 | Found: Detailed comparison discussions, user experiences

"why I switched from Salesforce to HubSpot honest experience"  
→ Relevance: 0.70-0.73 | Found: Migration stories, feature comparisons
```

**Side Hustle/Money Topics:**
```
"side hustle ideas that actually make money not scams"
→ Relevance: 0.70-0.77 | Found: Real experiences, specific suggestions
```

**Niche App Research:**
```
"daily horoscope apps which one is accurate and why"
→ Relevance: 0.67-0.72 | Found: App recommendations, feature requests
```

### ✅ Good Queries (relevance 0.60-0.69)

**Pain Point Discovery:**
```
"I hate my current CRM it is so frustrating"
→ Relevance: 0.60-0.64 | Found: Specific CRM complaints, feature wishlists

"cant sleep at night tried everything what actually works"
→ Relevance: 0.60-0.63 | Found: Sleep remedies discussions, medical advice seeking
```

**Tool Evaluation:**
```
"AI tools that actually save time not just hype"
→ Relevance: 0.64-0.65 | Found: Real productivity gains, tool recommendations
```

### ❌ Weak Queries (avoid these patterns)

**Too Abstract:**
```
"business opportunity growth potential"
→ Relevance: 0.52-0.58 | Returns unrelated generic posts
```

**Non-English:**
```
"学习编程最好的方法" (Chinese)
→ Relevance: 0.45-0.51 | Reddit is English-dominant, poor cross-lingual results
```

### Query Formula Cheat Sheet

| Goal | Pattern | Relevance |
|------|---------|-----------|
| Compare products | "[Product A] vs [Product B] which should I use" | 0.70-0.81 |
| Find switchers | "why I switched from [A] to [B]" | 0.70-0.73 |
| Money/hustle topics | "[topic] that actually [works/makes money] not [scam/hype]" | 0.70-0.77 |
| App recommendations | "[category] apps which one is [accurate/best] and why" | 0.67-0.72 |
| Pain points | "I hate my current [tool] it is so [frustrating/slow]" | 0.60-0.64 |
| Solutions seeking | "[problem] tried everything what actually works" | 0.60-0.63 |

## Response Fields

Each result includes:
- `title`, `content` - Post text
- `subreddit` - Source community  
- `upvotes`, `comments` - Engagement metrics
- `relevance` (0-1) - Semantic match score (0.5+ is good, 0.6+ is strong)
- `sentiment` - Discussion/Q&A/Story Sharing/Original Content/News
- `url` - Direct Reddit link

**Example response:**
```json
{
  "id": "1oecf5e",
  "title": "Trying to solve the productivity stack problem",
  "content": "The perfect productivity app doesn't exist. No single app can do everything well, so we use a stack of apps. But this creates another problem: multi app fragmentation...",
  "subreddit": "productivityapps",
  "upvotes": 1,
  "comments": 0,
  "relevance": 0.631,
  "sentiment": "Discussion",
  "url": "https://reddit.com/r/productivityapps/comments/1oecf5e"
}
```

## Real Case Study

**User:** SaaS founder validating a new project management tool idea

**Challenge:** Needed to understand real frustrations with existing PM tools (Asana, Monday, ClickUp) to find positioning angle.

**Research Query:**
```
reddit_search("I hate my project management tool it's so frustrating for remote teams", limit=50)
```

**What They Found (in 18 seconds):**
- **42 posts** with 0.60+ relevance
- **Top pain points** (mentioned 15+ times):
  - "Too complicated for simple projects"
  - "Mobile app is terrible"
  - "Hard to see the big picture"
  - "Notifications are overwhelming"
  - "Pricing jumps too fast with team size"

**Most upvoted insight** (+347 upvotes, r/startups):
> "We switched from Monday to a Notion template because Monday felt like learning a new language just to assign a task. Sometimes simple beats powerful."

**Positioning Decision:**
Built messaging around: **"Project management that feels like a shared doc, not enterprise software."**

**Product Changes Made:**
- Simplified onboarding (3 clicks to first task vs 15-step wizard)
- Mobile-first design (every feature tested on phone first)
- Flat pricing ($8/user, no tiers)
- Big-picture dashboard view (Gantt hidden by default)

**Results (6 months post-launch):**
- 2,400 paying users
- 78% came from "Reddit research-informed" messaging
- 4.7/5 rating on G2 with reviews saying "finally, PM without the bloat"
- Founder quote: "That one Reddit search saved us from building features nobody wanted."

## Tips

1. **Natural language works best** - Ask questions like a human would
2. **Include context** - "for small business" or "as a developer" improves results
3. **Combine emotion words** - "frustrated", "love", "hate", "wish" find stronger opinions
4. **Filter by engagement** - High upvotes/comments = validated pain points
5. **Check multiple subreddits** - Same topic discussed differently in r/startups vs r/smallbusiness
6. **Use comparison queries** - "X vs Y" consistently returns high-relevance results
7. **Search for stories** - "why I switched" and "honest experience" reveal real user journeys

## Example Workflows

**Find SaaS opportunity:**
1. `reddit_search`: "frustrated with project management tools for remote teams"
2. Filter results with high engagement (20+ upvotes or 10+ comments)
3. Identify recurring complaints → product opportunity
4. Export top 10 posts to analyze language patterns for messaging

**Validate idea:**
1. `reddit_search`: "[your product category] recommendations"
2. See what alternatives people mention
3. Note gaps in existing solutions
4. Check `reddit_get_subreddit` for relevant communities to monitor

**Content research:**
1. `reddit_get_subreddit`: Get posts from target community
2. `reddit_search`: Find specific questions/discussions with high engagement
3. Create content answering real user questions (with examples from Reddit)
4. Post back to Reddit (with value, not spam)

**Competitive intelligence:**
1. `reddit_search`: "[competitor name] experience"
2. `reddit_search`: "switched from [competitor] to [other]"
3. Extract feature complaints and praise
4. Build comparison matrix based on real feedback

## Pro Tips

**For Product Research:**
- Search for "I wish [category] had..." to find feature requests
- Filter by comments (not just upvotes) to find discussion-heavy threads
- Look for posts from 30-90 days ago (recent but with accumulated discussion)

**For Content Ideas:**
- Search your topic + "explained" or "guide"
- Check what questions have 0-2 replies (content gaps!)
- Save high-upvote posts and create better answers

**For Market Validation:**
- Run the same search monthly to track sentiment trends
- Compare subreddit sizes (r/notion has 180K vs r/obsidianmd 90K)
- Watch for "migration posts" ("leaving X for Y") as early signals

## Quality Indicators

A good Reddit Insights search has:
- [ ] Relevance scores mostly 0.60+ (strong semantic match)
- [ ] Results from 3+ different subreddits (diverse perspectives)
- [ ] Mix of high engagement (100+ upvotes) and niche discussions
- [ ] Clear patterns across multiple posts (not one-off opinions)
- [ ] Recent posts (<90 days) mixed with classic threads

## Common Mistakes to Avoid

❌ **Being too generic** - "marketing tips" returns weak results; "B2B cold email that actually works" is better
❌ **Ignoring engagement metrics** - A post with 2 upvotes is one person's opinion; 200+ upvotes is validated
❌ **Taking single posts as truth** - Look for patterns across 5-10 posts minimum
❌ **Forgetting to check sentiment** - A "Discussion" post is different from a "Q&A" (check the field!)
❌ **Not visiting actual threads** - The semantic summary is great, but top comments often have gold

---

**Built on semantic AI search (not keyword matching).**
**Find what people REALLY think. Not what marketing says they think.**
