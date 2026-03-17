---
name: last30days
description: Research any topic across Reddit, X, and web from the last 30 days. Get current trends, real community sentiment, and actionable insights in 7 minutes vs 2 hours manual research.
version: 2.0.0
author: theflohart
tags: [research, trends, reddit, twitter, competitive-intel, content-research]
---

# /last30days Research Skill

**Real-time intelligence engine:** Find what's working RIGHT NOW, not last quarter.

Scans Reddit, X, and web for the last 30 days, identifies patterns, extracts community insights, and delivers actionable intelligence with copy-paste-ready prompts.

## Why This vs ChatGPT?

**Problem with "research [topic]":** ChatGPT's training data is months/years old. It gives you general knowledge, not current signals.

**Problem with Perplexity:** Searches web but misses Reddit threads and X conversations where real practitioners share what's actually working.

**This skill provides:**
1. **30-day freshness filter** - Only pulls recent content (not 2023 blog posts)
2. **Multi-platform synthesis** - Combines Reddit (detailed discussions), X (real-time signals), and web (articles) in one pass
3. **Pattern detection** - Highlights themes mentioned 3+ times across sources
4. **Sentiment analysis** - Shows community vibe (hype, skepticism, frustration)
5. **Ready-to-use outputs** - Copy-paste prompts and action ideas, not just summaries

**You can replicate this** by manually searching Reddit, X, and Brave Search with date filters, reading 30+ sources, identifying patterns, and synthesizing insights. Takes 2+ hours. This skill does it in 7 minutes.

## When to Use

**Perfect for:**
- **Trend discovery** - "What's hot in AI agents right now?"
- **Strategy validation** - "What content marketing tactics are working in 2026?"
- **Competitive intel** - "What are developers saying about Cursor vs Copilot?"
- **Product research** - "What do users love/hate about Notion?"
- **Prompt research** - "What Claude prompting techniques are trending?"
- **Community sentiment** - "How do marketers feel about AI tools?"

**Not ideal for:**
- Historical research (use regular search)
- Academic/scientific papers (use Google Scholar)
- Non-English topics (limited coverage)
- Topics with zero online discussion

## Required Setup

This skill orchestrates multiple tools. Verify you have:

```bash
# 1. Brave Search API (for web_search)
# Already configured in OpenClaw by default

# 2. Bird CLI (for X/Twitter search)
source ~/.openclaw/credentials/bird.env && bird search "test" -n 1
# If this fails, install bird CLI first

# 3. Reddit Insights (optional but recommended)
# If you have reddit-insights MCP server configured, skill will use it
# Otherwise falls back to Reddit web search via Brave
```

**Quick verification:**
```bash
/last30days --check-setup
```

Should return:
- ✅ Brave Search: Available
- ✅ Bird CLI: Available
- ✅ Reddit Insights: Available (or "Using web search fallback")

## Workflow

### Step 1: Web Search (Freshness Filter = Past Month)
```
web_search: "[topic] 2026" + freshness=pm
web_search: "[topic] strategies trends current"
web_search: "[topic] what's working"
```

**Purpose:** Get recent articles, blog posts, tools

### Step 2: Reddit Search
**If reddit-insights MCP configured:**
```
reddit_search: "[topic] discussions techniques"
reddit_get_trends: "[subreddit]"
```

**Otherwise:**
```
web_search: "[topic] site:reddit.com" + freshness=pm
web_search: "[topic] reddit.com/r/[relevant_sub]"
```

**Purpose:** Find detailed discussions, practitioner insights, "what's actually working" threads

### Step 3: X/Twitter Search
```
bird search "[topic]" -n 10
bird search "[topic] 2026" -n 10
bird search "[topic] best practices" -n 10
```

**Purpose:** Real-time signals, expert takes, trending threads

### Step 4: Deep Dive on Top Sources (Optional)
For the 2-3 most relevant links:
```
web_fetch: [article URL]
```

**Purpose:** Extract specific tactics, quotes, data points

### Step 5: Synthesize & Package
1. **Identify patterns** - What appears 3+ times across sources?
2. **Extract key quotes** - Most upvoted Reddit comments, retweeted takes
3. **Assess sentiment** - Hype, adoption, skepticism, frustration?
4. **Create ready-to-use outputs** - Prompts, action ideas, copy-paste tactics

## Output Template

```markdown
# 🔍 /last30days: [TOPIC]
*Research compiled: [DATE]*  
*Sources analyzed: [NUMBER] (Reddit threads, X posts, articles)*  
*Time period: Last 30 days*

---

## 🔥 Top Patterns Discovered

### 1. [Pattern Name]
**Mentioned: X times across [platforms]**

[Description of the pattern + why it matters]

**Key evidence:**
- Reddit (r/[sub]): "[Quote from highly upvoted comment]"
- X: "[Quote from popular thread]"
- Article ([Source]): "[Key insight]"

---

### 2. [Pattern Name]
[Continue same format...]

---

## 📊 Reddit Sentiment Breakdown

| Subreddit | Discussion Volume | Sentiment | Key Insight |
|-----------|-------------------|-----------|-------------|
| r/[sub] | [# threads] | 🟢 Positive / 🟡 Mixed / 🔴 Skeptical | [One-liner takeaway] |

**Top upvoted insights:**
1. "[Quote]" — u/[username] (+234 upvotes)
2. "[Quote]" — u/[username] (+189 upvotes)

---

## 🐦 X/Twitter Signal Analysis

**Trending themes:**
- [Theme 1] - [# mentions]
- [Theme 2] - [# mentions]

**Notable voices:**
- [@handle]: "[Key take]"
- [@handle]: "[Key take]"

**Engagement patterns:**
[What types of posts are getting traction?]

---

## 📈 Web Article Highlights

**Most shared articles:**
1. "[Article Title]" — [Source] — [Key insight]
2. "[Article Title]" — [Source] — [Key insight]

**Common recommendations across articles:**
- [Tactic 1]
- [Tactic 2]
- [Tactic 3]

---

## 🎯 Copy-Paste Prompt

**Based on current community best practices:**

```
[Ready-to-use prompt incorporating the patterns discovered]

Context: [Relevant context from research]
Task: [Clear task]
Style: [Tone/voice based on research]
Constraints: [Any patterns to avoid based on research]
```

**Why this works:** [Brief explanation based on research findings]

---

## 💡 Action Ideas

**Immediate opportunities based on this research:**

1. **[Opportunity 1]**
   - What: [Specific action]
   - Why: [Evidence from research]
   - How: [Implementation steps]

2. **[Opportunity 2]**
   [Continue format...]

---

## 📌 Source List

**Reddit Threads:**
- [Thread title] - r/[sub] - [URL]

**X Threads:**
- [@handle] - [Tweet] - [URL]

**Articles:**
- [Title] - [Source] - [URL]

---

*Research complete. [X] sources analyzed in [Y] minutes.*
```

## Real Examples

### Example 1: Prompt Research

**Query:** `/last30days Claude prompting best practices`

**Abbreviated Output:**
```markdown
# 🔍 /last30days: Claude Prompting Best Practices

## Top Patterns Discovered

### 1. XML Tags for Structure (12 mentions)
Reddit and X both emphasize using XML tags for complex prompts:
- Reddit: "XML tags changed my Claude workflow. <context> and <task> make responses 3× more accurate."
- X: "@anthropicAI's own docs now recommend XML. It's the meta."

### 2. Examples Over Instructions (9 mentions)  
"Show, don't tell" — Provide 2-3 examples instead of long instructions.

### 3. Chain of Thought Explicit (7 mentions)
Add "Think step-by-step before answering" dramatically improves reasoning.

## Copy-Paste Prompt

<context>
[Your context here]
</context>

<task>
[Your task here]
</task>

<examples>
Example 1: [Show desired output style]
Example 2: [Show edge case handling]
</examples>

Think step-by-step before providing your final answer.
```

---

### Example 2: Competitive Intel

**Query:** `/last30days Notion vs Obsidian 2026`

**Abbreviated Output:**
```markdown
## Top Patterns

### 1. "Notion for Teams, Obsidian for Individuals" (18 mentions)
Strong consensus: Notion wins for collaboration, Obsidian wins for personal PKM.

### 2. Performance Complaints About Notion (11 mentions)
"Notion is slow with 1000+ pages" — recurring pain point

## Reddit Sentiment

| Subreddit | Sentiment | Key Insight |
|-----------|-----------|-------------|
| r/Notion | 🟡 Mixed | Love features, frustrated by speed |
| r/ObsidianMD | 🟢 Positive | Passionate community, local-first advocates |

## Action Ideas

**If building a PKM tool:**
1. Positioning: "Notion speed + Obsidian power" opportunity
2. Target: Teams frustrated by Notion slowness
3. Messaging: "Collaboration without the lag"
```

---

### Example 3: Content Strategy

**Query:** `/last30days LinkedIn content strategies working 2026`

**Abbreviated Output:**
```markdown
## Top Patterns

### 1. "Teach in Public" Posts Dominate (22 mentions)
Tactical, educational content outperforms thought leadership by 4-5×.

### 2. Carousels Are Fading (14 mentions)
"LinkedIn is deprioritizing carousels" — multiple reports of engagement drops.

### 3. Comment Engagement = Reach (16 mentions)
"Spend 30 min/day commenting on others' posts. Doubled my reach."

## Action Ideas

1. **Shift to educational threads**
   - Format: Problem → Solution (step-by-step) → Result
   - Evidence: Posts using this format getting 3-5× more impressions

2. **Abandon carousel strategy**
   - Data: Engagement down 40-60% since December

3. **Allocate 30 min/day to comments**
   - Tactic: Comment on posts from your ICP 10 min after posting (algorithm boost)
```

## Real Case Study

**User:** B2B SaaS marketer researching content trends quarterly

**Before using skill:**
- Manual research: 2-3 hours per topic
- Visited 20-30 sites, took scattered notes
- Hard to identify patterns across sources
- No systematic approach

**After implementing /last30days:**
- Research time: 7-10 minutes per topic
- Consistent output format (easy to reference later)
- Pattern detection automatic
- Copy-paste prompts immediately usable

**Impact after 3 months:**
- 10 trend reports created (vs 2-3 before)
- Content strategy pivots based on current signals, not guesses
- Team shares research reports across org (became go-to intelligence source)
- Time saved: ~20 hours/month

**Quote:** "I used to spend half a day researching trends, now it's 7 minutes. The pattern detection alone is worth it—I'd miss things reading manually."

## Configuration Options

### Standard Mode (default)
```
/last30days [topic]
```
- Searches web, Reddit, X
- Synthesizes top patterns
- Generates prompts + action ideas

### Deep Dive Mode
```
/last30days [topic] --deep
```
- Fetches and analyzes top 5 articles in full
- More detailed quotes and data points
- Takes 12-15 minutes instead of 7

### Reddit-Only Mode
```
/last30days [topic] --reddit-only
```
- Focuses exclusively on Reddit discussions
- Best for: Community sentiment, practitioner insights

### Quick Brief Mode
```
/last30days [topic] --quick
```
- Top 3 patterns only
- No detailed synthesis
- 3-minute output

## Pro Tips

1. **Use specific topics** - "AI writing tools" better than "AI"
2. **Add context** - "for B2B SaaS" or "for developers" narrows results
3. **Run monthly** - Track trends over time, spot shifts early
4. **Combine with /reddit-insights** - For deeper Reddit analysis
5. **Export to Notion** - Keep a trends database
6. **Share with team** - Intelligence is more valuable when distributed

## Common Use Cases

| Goal | Query Example | Output Value |
|------|---------------|--------------|
| Content ideas | `/last30days AI productivity tools` | Topics getting engagement now |
| Competitive research | `/last30days Superhuman vs Spark email` | User sentiment, pain points |
| Positioning | `/last30days project management frustrations` | Language customers use |
| Product validation | `/last30days AI coding assistant pain points` | Real problems to solve |
| Marketing tactics | `/last30days cold email strategies 2026` | What's working in market |

## Quality Indicators

A good /last30days report has:
- [ ] 3-5 clear patterns (not just random insights)
- [ ] Quotes from actual users (not just article summaries)
- [ ] Sentiment assessment (what's the vibe?)
- [ ] Ready-to-use prompt (copy-paste quality)
- [ ] Specific action ideas (not vague suggestions)
- [ ] Source links for credibility
- [ ] Recency verified (nothing from >30 days)

## Limitations

**This skill does NOT:**
- Access paywalled content (uses public sources only)
- Provide academic-quality research (for speed, not depth)
- Replace domain expertise (synthesizes existing knowledge)
- Guarantee completeness (samples popular discussions)

**Best for:** Fast, directional intelligence. Not dissertation-level research.

## Installation

```bash
# Copy skill to your skills directory
cp -r last30days $HOME/.openclaw/skills/

# Verify dependencies
/last30days --check-setup

# First run
/last30days "your topic here"
```

## Support

Issues or missing sources? Provide:
- Topic searched
- Expected vs actual sources found
- Any error messages
- Your setup verification output

---

**Built to replace 2-hour research sessions with 7-minute intelligence reports.**

**Know what's working RIGHT NOW. Not last quarter. Not last year. Today.**