---
name: reddit-product-viability
description: Scrape and analyze Reddit for real user signals about product viability, pain severity, willingness to pay, and competitor saturation. Validate product ideas before building by systematically analyzing discussions, complaints, feature requests, and purchasing behavior across relevant subreddits. Integrates with Firecrawl for scraping, Supabase for storage, and Superset for trend visualization.
---

# Reddit Product Viability Research

## When to Use This Skill

Use this skill when you need to:
- **Validate product ideas** before investing development time
- **Assess market demand** through real user conversations
- **Identify pain points** and severity across target segments
- **Evaluate willingness to pay** based on user discussions
- **Analyze competitor saturation** and gaps in solutions
- **Discover feature requests** and unmet needs
- **Monitor product-market fit signals** over time
- **Research SaaS alternative opportunities** (like SAP Concur, Ariba alternatives)

## Core Capabilities

### Product Viability Validation Framework

Systematically evaluate four critical dimensions:

1. **Real Demand Signals**
   - Volume of discussions about the problem
   - Frequency of complaints and pain points
   - Emotional intensity in user posts
   - Problem persistence over time

2. **Pain Severity Assessment**
   - Impact on users' work/life
   - Workarounds currently being used
   - Time/money currently wasted
   - Urgency of need for solution

3. **Willingness to Pay**
   - Current spending on alternatives
   - Budget discussions and constraints
   - "Shut up and take my money" signals
   - Pricing tolerance indicators

4. **Competitor Saturation**
   - Existing solutions mentioned
   - User satisfaction with alternatives
   - Gap analysis (unfulfilled needs)
   - Market positioning opportunities

### Technical Implementation

- **Reddit API + Firecrawl** - Scrape subreddits, threads, comments
- **Supabase Storage** - Store posts with deduplication
- **NLP Analysis** - Sentiment, entity extraction, topic modeling
- **Superset Dashboards** - Visualize trends and insights
- **Notion Integration** - Track validation findings
- **Scheduled Monitoring** - Daily/weekly trend analysis

## Prerequisites

### Required Access
- Reddit API key (free tier: 100 requests/minute)
- Firecrawl API key (self-hosted or paid)
- Supabase project with pgvector
- Superset instance for visualization

### Optional Integrations
- OpenAI API for GPT-4 analysis
- Perplexity API for research enhancement
- Notion for findings documentation

### Python Dependencies
```python
praw  # Reddit API wrapper
firecrawl-py
supabase-py
pandas
numpy
transformers  # For sentiment analysis
```

## Implementation Patterns

### Product Validation Prompt Template

```markdown
✅ Product Viability — Reddit Insight Prompt

Goal: Validate real demand, pain severity, willingness to pay, and competitor 
saturation for [PRODUCT_IDEA].

Scrape and analyze Reddit for real user signals about the following product idea:

**Product Idea:** [Your product concept]

**Target Subreddits:**
- r/[relevant_sub1]
- r/[relevant_sub2]
- r/[relevant_sub3]

**Analysis Timeframe:** Past [6/12/24] months

**Key Questions to Answer:**

1. **Real Demand:**
   - How many users discuss this problem?
   - How often does it come up?
   - What triggers discussions about it?
   - Is the problem persistent or seasonal?

2. **Pain Severity:**
   - What impact does the problem have?
   - What workarounds are users trying?
   - How much time/money is being wasted?
   - What's the urgency level?

3. **Willingness to Pay:**
   - What are users currently spending on alternatives?
   - What's their budget range?
   - Are there "shut up and take my money" signals?
   - What pricing would be acceptable?

4. **Competitor Saturation:**
   - Which solutions are mentioned?
   - What are users' complaints about alternatives?
   - What gaps exist in current solutions?
   - Where's the market positioning opportunity?

**Output Format:**
- Quantitative metrics (post volume, sentiment scores)
- Qualitative insights (user quotes, pain points)
- Competitor analysis matrix
- Recommended next steps
- Risk factors and red flags
```

### Reddit Scraping Script

```python
# reddit_viability_scraper.py
import praw
from firecrawl import FirecrawlApp
from supabase import create_client
from datetime import datetime, timedelta
import pandas as pd
from transformers import pipeline

class RedditViabilityAnalyzer:
    def __init__(self, supabase_url, supabase_key, reddit_client_id, reddit_secret):
        # Initialize Reddit client
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_secret,
            user_agent='ProductViabilityBot/1.0'
        )
        
        # Initialize Supabase
        self.supabase = create_client(supabase_url, supabase_key)
        
        # Initialize sentiment analyzer
        self.sentiment_analyzer = pipeline("sentiment-analysis")
    
    def scrape_subreddit(self, subreddit_name, keywords, timeframe_months=6):
        """
        Scrape subreddit for product validation signals
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []
        
        # Calculate timeframe
        cutoff_date = datetime.now() - timedelta(days=timeframe_months * 30)
        
        # Search for keywords
        for keyword in keywords:
            results = subreddit.search(
                keyword,
                sort='relevance',
                time_filter='year',
                limit=100
            )
            
            for post in results:
                if datetime.fromtimestamp(post.created_utc) >= cutoff_date:
                    # Extract post data
                    post_data = {
                        'id': post.id,
                        'title': post.title,
                        'text': post.selftext,
                        'score': post.score,
                        'num_comments': post.num_comments,
                        'created_utc': post.created_utc,
                        'url': post.url,
                        'subreddit': subreddit_name,
                        'keyword': keyword,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # Get top comments
                    post.comments.replace_more(limit=0)
                    comments = []
                    for comment in post.comments.list()[:10]:  # Top 10 comments
                        comments.append({
                            'text': comment.body,
                            'score': comment.score,
                            'created_utc': comment.created_utc
                        })
                    
                    post_data['comments'] = comments
                    posts.append(post_data)
        
        return posts
    
    def analyze_demand_signals(self, posts):
        """
        Analyze volume, frequency, and intensity of demand signals
        """
        df = pd.DataFrame(posts)
        
        analysis = {
            'total_posts': len(df),
            'avg_score': df['score'].mean(),
            'avg_comments': df['num_comments'].mean(),
            'total_engagement': df['score'].sum() + df['num_comments'].sum(),
            'posts_per_month': len(df) / 6,  # Assuming 6 month timeframe
            'top_posts': df.nlargest(5, 'score')[['title', 'score', 'url']].to_dict('records')
        }
        
        return analysis
    
    def analyze_pain_severity(self, posts):
        """
        Analyze pain points and their severity
        """
        pain_indicators = [
            'frustrated', 'annoying', 'waste of time', 'terrible',
            'awful', 'nightmare', 'ridiculous', 'broken', 'useless'
        ]
        
        high_pain_posts = []
        for post in posts:
            text = f"{post['title']} {post['text']}".lower()
            pain_score = sum(1 for indicator in pain_indicators if indicator in text)
            
            if pain_score > 0:
                high_pain_posts.append({
                    'title': post['title'],
                    'pain_score': pain_score,
                    'score': post['score'],
                    'url': post['url']
                })
        
        high_pain_posts.sort(key=lambda x: x['pain_score'], reverse=True)
        
        return {
            'high_pain_posts_count': len(high_pain_posts),
            'avg_pain_score': sum(p['pain_score'] for p in high_pain_posts) / len(high_pain_posts) if high_pain_posts else 0,
            'top_pain_posts': high_pain_posts[:10]
        }
    
    def analyze_willingness_to_pay(self, posts):
        """
        Analyze pricing discussions and budget indicators
        """
        price_keywords = [
            'price', 'cost', 'expensive', 'cheap', 'free', 'subscription',
            'monthly', 'yearly', 'budget', 'afford', 'worth', 'pay'
        ]
        
        pricing_posts = []
        for post in posts:
            text = f"{post['title']} {post['text']}".lower()
            if any(keyword in text for keyword in price_keywords):
                pricing_posts.append({
                    'title': post['title'],
                    'text': post['text'],
                    'url': post['url'],
                    'score': post['score']
                })
        
        return {
            'pricing_discussion_count': len(pricing_posts),
            'pricing_posts': pricing_posts[:10]
        }
    
    def analyze_competitor_saturation(self, posts):
        """
        Identify competitors and satisfaction levels
        """
        # This would need to be customized per use case
        competitors = {}
        
        for post in posts:
            text = f"{post['title']} {post['text']}".lower()
            
            # Extract competitor mentions (simplified)
            # In practice, use NER or custom extraction
            for comment in post.get('comments', []):
                # Analyze satisfaction with mentioned tools
                sentiment = self.sentiment_analyzer(comment['text'][:512])[0]
                
                # Track competitor mentions and sentiment
                # (Simplified - would need more sophisticated NER)
        
        return competitors
    
    def store_in_supabase(self, posts, analysis):
        """
        Store posts and analysis in Supabase
        """
        # Store raw posts
        for post in posts:
            self.supabase.table('reddit_posts').upsert({
                'post_id': post['id'],
                'title': post['title'],
                'text': post['text'],
                'score': post['score'],
                'num_comments': post['num_comments'],
                'created_at': datetime.fromtimestamp(post['created_utc']).isoformat(),
                'url': post['url'],
                'subreddit': post['subreddit'],
                'keyword': post['keyword'],
                'scraped_at': post['scraped_at']
            }).execute()
        
        # Store analysis summary
        self.supabase.table('viability_analysis').insert({
            'analyzed_at': datetime.now().isoformat(),
            'demand_signals': analysis['demand'],
            'pain_severity': analysis['pain'],
            'pricing_insights': analysis['pricing'],
            'competitor_analysis': analysis['competitors']
        }).execute()
    
    def generate_report(self, analysis):
        """
        Generate human-readable viability report
        """
        report = f"""
# Product Viability Analysis Report

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 1. Demand Signals ✅

- **Total Posts Analyzed:** {analysis['demand']['total_posts']}
- **Average Engagement:** {analysis['demand']['avg_score']:.1f} upvotes per post
- **Discussion Frequency:** {analysis['demand']['posts_per_month']:.1f} posts/month
- **Total Community Engagement:** {analysis['demand']['total_engagement']} interactions

**Top Discussions:**
"""
        for post in analysis['demand']['top_posts'][:3]:
            report += f"\n- [{post['title']}]({post['url']}) ({post['score']} upvotes)"
        
        report += f"""

## 2. Pain Severity 🔥

- **High-Pain Posts:** {analysis['pain']['high_pain_posts_count']}
- **Average Pain Score:** {analysis['pain']['avg_pain_score']:.2f}/10

**Most Painful Issues:**
"""
        for post in analysis['pain']['top_pain_posts'][:3]:
            report += f"\n- [{post['title']}]({post['url']}) (Pain: {post['pain_score']}, Score: {post['score']})"
        
        report += f"""

## 3. Willingness to Pay 💰

- **Pricing Discussions:** {analysis['pricing']['pricing_discussion_count']} posts mention pricing

## 4. Competitor Analysis 🎯

(Detailed competitor breakdown would go here)

## Recommendations

Based on the analysis:

1. **Market Validation:** {'STRONG' if analysis['demand']['total_posts'] > 50 else 'WEAK'}
2. **Pain Point Severity:** {'HIGH' if analysis['pain']['high_pain_posts_count'] > 10 else 'MODERATE'}
3. **Suggested Next Steps:**
   - Interview top posters for deeper insights
   - Build MVP focusing on highest pain points
   - Test pricing with {analysis['demand']['total_posts'] // 10} potential users

## Risk Factors ⚠️

- Monitor for seasonal trends
- Validate across multiple subreddits
- Consider demographic biases in Reddit userbase
"""
        
        return report

# Usage
analyzer = RedditViabilityAnalyzer(
    supabase_url=os.getenv('SUPABASE_URL'),
    supabase_key=os.getenv('SUPABASE_KEY'),
    reddit_client_id=os.getenv('REDDIT_CLIENT_ID'),
    reddit_secret=os.getenv('REDDIT_SECRET')
)

# Scrape relevant subreddits
posts = analyzer.scrape_subreddit(
    'EntrepreneurRideAlong',
    keywords=['expense management', 'travel expenses', 'receipts', 'reimbursement'],
    timeframe_months=6
)

# Analyze viability
analysis = {
    'demand': analyzer.analyze_demand_signals(posts),
    'pain': analyzer.analyze_pain_severity(posts),
    'pricing': analyzer.analyze_willingness_to_pay(posts),
    'competitors': analyzer.analyze_competitor_saturation(posts)
}

# Store and report
analyzer.store_in_supabase(posts, analysis)
report = analyzer.generate_report(analysis)

print(report)
```

### Supabase Schema

```sql
-- reddit_posts table
CREATE TABLE reddit_posts (
    post_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    text TEXT,
    score INTEGER,
    num_comments INTEGER,
    created_at TIMESTAMPTZ,
    url TEXT,
    subreddit TEXT,
    keyword TEXT,
    scraped_at TIMESTAMPTZ,
    sentiment_score FLOAT,
    pain_score INTEGER,
    created_at_index TIMESTAMPTZ
);

CREATE INDEX idx_reddit_posts_subreddit ON reddit_posts(subreddit);
CREATE INDEX idx_reddit_posts_keyword ON reddit_posts(keyword);
CREATE INDEX idx_reddit_posts_created ON reddit_posts(created_at);

-- viability_analysis table
CREATE TABLE viability_analysis (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    analyzed_at TIMESTAMPTZ DEFAULT NOW(),
    product_idea TEXT,
    demand_signals JSONB,
    pain_severity JSONB,
    pricing_insights JSONB,
    competitor_analysis JSONB,
    recommendation TEXT
);

-- Enable pgvector for semantic search
CREATE EXTENSION IF NOT EXISTS vector;

ALTER TABLE reddit_posts ADD COLUMN embedding vector(1536);

CREATE INDEX ON reddit_posts USING ivfflat (embedding vector_cosine_ops);
```

### Superset Dashboard SQL

```sql
-- Demand Trend Over Time
SELECT
    DATE_TRUNC('month', created_at) AS month,
    COUNT(*) AS post_count,
    AVG(score) AS avg_score,
    SUM(num_comments) AS total_comments
FROM reddit_posts
WHERE subreddit IN ('EntrepreneurRideAlong', 'SaaS', 'startups')
GROUP BY 1
ORDER BY 1 DESC;

-- Pain Severity Distribution
SELECT
    CASE
        WHEN pain_score >= 5 THEN 'High Pain'
        WHEN pain_score >= 3 THEN 'Moderate Pain'
        ELSE 'Low Pain'
    END AS pain_level,
    COUNT(*) AS post_count,
    AVG(score) AS avg_engagement
FROM reddit_posts
WHERE pain_score > 0
GROUP BY 1;

-- Keyword Performance
SELECT
    keyword,
    COUNT(*) AS mentions,
    AVG(score) AS avg_score,
    SUM(num_comments) AS total_discussion
FROM reddit_posts
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

-- Competitor Mentions
-- (Would need NER processing first)
SELECT
    competitor_name,
    sentiment_category,
    COUNT(*) AS mentions
FROM competitor_mentions
GROUP BY 1, 2;
```

## Integration Points

### With Firecrawl
```python
# Use Firecrawl for JavaScript-heavy Reddit pages
from firecrawl import FirecrawlApp

app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Crawl subreddit
result = app.crawl_url(
    'https://www.reddit.com/r/EntrepreneurRideAlong/search?q=expense+management',
    params={'scrapeOptions': {'formats': ['markdown', 'html']}}
)
```

### With Notion Tracking
```python
# Log findings to Notion
from notion_client import Client

notion = Client(auth=os.getenv('NOTION_TOKEN'))

notion.pages.create(
    parent={"database_id": VALIDATION_DB_ID},
    properties={
        "Product Idea": {"title": [{"text": {"content": "Travel Expense Management"}}]},
        "Demand Score": {"number": analysis['demand']['total_posts']},
        "Pain Severity": {"select": {"name": "High"}},
        "Status": {"select": {"name": "Validated"}}
    }
)
```

### With Superset Visualization
Auto-generate dashboard showing:
- Demand trends over time
- Pain severity heatmap
- Competitor mention frequency
- Sentiment distribution
- Top keywords and topics

## Output Formats

### Viability Score Card
```
Product Viability Assessment: Travel & Expense Management

Demand Signal:        ████████░░ 8/10 (85 relevant posts/month)
Pain Severity:        █████████░ 9/10 (High pain indicators)
Willingness to Pay:   ██████░░░░ 6/10 (Budget discussions present)
Market Opportunity:   ████████░░ 8/10 (Gaps in current solutions)

OVERALL VIABILITY:    ████████░░ 8.2/10 ✅ PROCEED WITH MVP

Recommendation: Strong validation signals. Build MVP focused on receipt
OCR and policy validation - highest pain points identified.
```

### Detailed Findings Report
Generated markdown with:
- Executive summary
- Quantitative metrics
- Qualitative user quotes
- Competitor analysis
- Feature prioritization
- Risk assessment
- Next steps

## Examples

### Example 1: Validate SaaS Alternative Idea

**Prompt:**
```
Validate product viability for "Self-hosted SAP Concur alternative 
for SMBs" by analyzing r/Accounting, r/SmallBusiness, r/Entrepreneur
```

**Output:**
- 127 posts discussing expense management pain
- 89% mention current tools are "too expensive"
- Average pain score: 7.2/10
- Top complaint: Concur pricing ($15K/year)
- Opportunity: Budget-conscious SMBs ($100-500/month pricing)
- Recommendation: STRONG VALIDATION - Build MVP

### Example 2: Feature Prioritization

**Prompt:**
```
Analyze Reddit discussions to prioritize features for expense 
management tool. Focus on r/Accounting over past 12 months.
```

**Output:**
Feature Priority (by mention frequency + pain severity):
1. Receipt OCR (mentioned 89 times, pain: 8/10) ← BUILD FIRST
2. Policy validation (mentioned 67 times, pain: 9/10)
3. Mobile app (mentioned 54 times, pain: 6/10)
4. Multi-currency (mentioned 43 times, pain: 7/10)
5. Integration with QBO (mentioned 38 times, pain: 5/10)

### Example 3: Competitive Intelligence

**Prompt:**
```
Map competitive landscape for travel expense tools by analyzing
user sentiment across r/Accounting, r/BusinessIntelligence
```

**Output:**
Competitor Satisfaction Matrix:
- SAP Concur: 342 mentions, 38% positive, 62% negative
  - Pain: "Too expensive", "Complex setup"
  - Opportunity: SMB market
- Expensify: 178 mentions, 61% positive, 39% negative
  - Pain: "Limited customization"
  - Opportunity: Enterprise features
- Divvy: 89 mentions, 72% positive, 28% negative
  - Strength: Modern UX
  - Gap: Lacks BIR compliance

## Cost Savings

### vs. Paid Research Tools

| Tool | Annual Cost | Self-Hosted Reddit Analysis | Savings |
|------|-------------|----------------------------|---------|
| Gong Insights | $30,000 | $0 (open Reddit API) | $30,000 |
| Wynter | $12,000 | $240 (Firecrawl + compute) | $11,760 |
| UserTesting | $6,000 | $0 (Reddit is free) | $6,000 |

**Total Annual Savings:** $47,760

**Additional Value:**
- Real, unbiased user feedback
- Longitudinal trend analysis
- Competitive intelligence
- Continuous validation (not one-time)

## Best Practices

### Subreddit Selection
✅ **Choose high-signal subreddits:**
- Niche communities (r/Accounting vs. r/business)
- Problem-focused discussions
- Active communities (>10K members)
- Recent activity (posts in last 30 days)

### Keyword Strategy
✅ **Use specific pain language:**
- "frustrated with [tool]"
- "looking for alternative to [competitor]"
- "how do you handle [problem]"
- "anyone else struggling with [pain]"

### Analysis Frequency
✅ **Monthly monitoring for:**
- New trends and pain points
- Competitor mentions and sentiment
- Feature request patterns
- Market opportunity shifts

## Troubleshooting

### Low Post Volume
**Issue:** Only 10 posts found in 6 months  
**Fix:** Expand subreddit list, broaden keywords, increase timeframe

### Reddit API Rate Limits
**Issue:** "429 Too Many Requests"  
**Fix:** Add delays between requests, upgrade to Premium API

### Sentiment Analysis Inaccuracy
**Issue:** Sarcasm misclassified as positive  
**Fix:** Use domain-specific models, manual review of top posts

## License

MIT (Reddit API requires attribution)

## References

- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [PRAW: Python Reddit API Wrapper](https://praw.readthedocs.io/)
- [Product Validation Frameworks](https://www.ycombinator.com/library/6h-how-to-validate-your-idea)
- [Reddit as Market Research Tool](https://www.indiehackers.com/post/using-reddit-for-market-research-a-guide-4e8e3b6f0e)

---

**Validate ideas with real user signals before building. Save months of wasted development on products nobody wants.** 🚀
