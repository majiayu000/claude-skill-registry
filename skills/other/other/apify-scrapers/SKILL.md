---
name: apify-scrapers
description: Social media and web scraping using Apify actors. Use this skill when scraping Twitter/X tweets, Reddit posts, LinkedIn posts, Instagram profiles/posts/reels, Facebook pages/posts/groups, TikTok videos, YouTube content, Google Maps businesses/reviews, contact enrichment (emails/phones from websites), or when auto-detecting URL type to scrape. Triggers on requests to scrape social media, get trending posts, extract business info, find contact details, or extract content from social URLs.
---

# Apify Scrapers

## Overview

Scrape content from major social platforms using Apify actors. Each platform has optimized settings for cost and quality.

## Quick Decision Tree

```
What do you want to scrape?
│
├── Social Media Posts
│   ├── Twitter/X → references/twitter.md
│   │   └── Script: scripts/scrape_twitter_ai_trends.py
│   │
│   ├── Reddit → references/reddit.md
│   │   └── Script: scripts/scrape_reddit_ai_tech.py
│   │
│   ├── LinkedIn → references/linkedin.md
│   │   └── Script: scripts/scrape_linkedin_posts.py
│   │
│   ├── Instagram → references/instagram.md
│   │   └── Script: scripts/scrape_instagram.py
│   │   └── Modes: profile, posts, hashtag, reels, comments
│   │
│   ├── Facebook → references/facebook.md
│   │   └── Script: scripts/scrape_facebook.py
│   │   └── Modes: page, posts, reviews, groups, marketplace
│   │
│   ├── TikTok → references/multi-platform.md
│   │   └── Script: scripts/scrape_multi_platform.py
│   │
│   └── YouTube → references/multi-platform.md
│       └── Script: scripts/scrape_multi_platform.py
│
├── Business/Places
│   ├── Google Maps businesses → references/google-maps.md
│   │   └── Script: scripts/scrape_google_maps.py
│   │   └── Modes: search, place, reviews
│   │
│   └── Contact info from websites → references/contact-enrichment.md
│       └── Script: scripts/scrape_contact_info.py
│       └── Extract: emails, phone numbers, social profiles
│
├── Auto-detect URL type → references/url-detect.md
│   └── Script: scripts/scrape_content_by_url.py
│
├── Trend Analysis (NEW)
│   └── Enriched trend analysis → workflows/trend-analysis.md
│       └── Script: scripts/analyze_trends.py
│       └── Features: velocity scoring, lifecycle staging, opportunity scoring
│
└── Workflows (multi-step)
    ├── Lead generation → workflows/lead-generation.md
    ├── Influencer discovery → workflows/influencer-discovery.md
    ├── Competitor analysis → workflows/competitor-intel.md
    ├── Trend analysis → workflows/trend-analysis.md
    └── Competitor Ads Intelligence (NEW) → workflows/competitor-ads.md
        └── Script: scripts/scrape_competitor_ads.py
        └── Platforms: Facebook Ads Library, Google Ads Transparency
        └── Features: Spend estimates, creative analysis, benchmarking
```

## Environment Setup

```bash
# Required in .env
APIFY_TOKEN=apify_api_xxxxx
```

Get your API key: https://console.apify.com/account/integrations

## Common Usage Patterns

### Scrape Twitter Trends
```bash
python scripts/scrape_twitter_ai_trends.py --query "AI agents" --max-tweets 50
```

### Scrape Reddit Discussions
```bash
python scripts/scrape_reddit_ai_tech.py --subreddits "MachineLearning,LocalLLaMA" --max-posts 100
```

### Scrape LinkedIn Author
```bash
python scripts/scrape_linkedin_posts.py author "https://linkedin.com/in/username" --max-posts 30
```

### Auto-detect and Scrape URL
```bash
python scripts/scrape_content_by_url.py "https://x.com/user/status/123456"
```

### Scrape Instagram Profile
```bash
python scripts/scrape_instagram.py profile "https://instagram.com/username" --max-posts 20
```

### Scrape Instagram Hashtag
```bash
python scripts/scrape_instagram.py hashtag "#artificialintelligence" --max-posts 50
```

### Scrape Instagram Reels
```bash
python scripts/scrape_instagram.py reels "https://instagram.com/username" --max-reels 30
```

### Scrape Facebook Page
```bash
python scripts/scrape_facebook.py page "https://facebook.com/pagename" --max-posts 50
```

### Scrape Facebook Reviews
```bash
python scripts/scrape_facebook.py reviews "https://facebook.com/pagename" --max-reviews 100
```

### Scrape Facebook Marketplace
```bash
python scripts/scrape_facebook.py marketplace "laptops in san francisco" --max-items 30
```

### Scrape Google Maps Businesses
```bash
python scripts/scrape_google_maps.py search "AI consulting firms in New York" --max-results 50
```

### Scrape Google Maps Reviews
```bash
python scripts/scrape_google_maps.py reviews "ChIJN1t_tDeuEmsRUsoyG83frY4" --max-reviews 100
```

### Extract Contact Info from Websites
```bash
python scripts/scrape_contact_info.py "https://example.com" --depth 2
```

### Bulk Contact Enrichment
```bash
python scripts/scrape_contact_info.py --urls-file companies.txt --output contacts.json
```

### Scrape Competitor Ads (Single Competitor)
```bash
python scripts/scrape_competitor_ads.py "Nike" --platforms facebook google --country US --days 30
```

### Compare Multiple Competitors' Ads
```bash
python scripts/scrape_competitor_ads.py "Nike" "Adidas" "Puma" --compare --output comparison.json
```

### Discover Advertisers by Keyword
```bash
python scripts/scrape_competitor_ads.py --search "running shoes" --country US --max-ads 200
```

### Filter Competitor Ads by Media Type
```bash
python scripts/scrape_competitor_ads.py "Netflix" "Disney+" --platforms facebook --media-types video --days 7
```

### Analyze Trends (NEW)
```bash
# Analyze specific topic with enrichments
python scripts/analyze_trends.py "artificial intelligence" --sources google instagram tiktok --days 90

# Discover trending topics in category
python scripts/analyze_trends.py --category technology --discover --top 50

# Compare multiple trends
python scripts/analyze_trends.py "AI" "blockchain" "metaverse" --compare

# Export HTML trend report
python scripts/analyze_trends.py "sustainable fashion" --format html --output trend_report.html
```

## Cost Estimates

| Platform | Actor | Cost per Item |
|----------|-------|---------------|
| Twitter | kaitoeasyapi/twitter-x-data-tweet-scraper | ~$0.00025 |
| Reddit | trudax/reddit-scraper | ~$0.001-0.005 |
| LinkedIn | harvestapi/linkedin-post-search | ~$0.01-0.05 |
| YouTube | streamers/youtube-scraper | ~$0.01-0.05 |
| TikTok | clockworks/tiktok-scraper | ~$0.005 |
| Instagram (profile) | apify/instagram-profile-scraper | ~$0.005 |
| Instagram (posts) | apify/instagram-post-scraper | ~$0.002-0.005 |
| Instagram (hashtag) | apify/instagram-hashtag-scraper | ~$0.002-0.005 |
| Instagram (reels) | apify/instagram-reel-scraper | ~$0.005-0.01 |
| Instagram (comments) | apify/instagram-comment-scraper | ~$0.001-0.003 |
| Facebook (page) | apify/facebook-pages-scraper | ~$0.005-0.01 |
| Facebook (posts) | apify/facebook-posts-scraper | ~$0.003-0.005 |
| Facebook (reviews) | apify/facebook-reviews-scraper | ~$0.002-0.005 |
| Facebook (groups) | apify/facebook-groups-scraper | ~$0.005-0.01 |
| Facebook (marketplace) | apify/facebook-marketplace-scraper | ~$0.005-0.01 |
| Google Maps (search) | compass/crawler-google-places | ~$0.01-0.02 |
| Google Maps (place) | compass/google-maps-business-scraper | ~$0.01 |
| Google Maps (reviews) | compass/google-maps-reviews-scraper | ~$0.003-0.005 |
| Contact Enrichment | lukaskrivka/contact-info-scraper | ~$0.01-0.03 |
| Google Trends | apify/google-trends-scraper | ~$0.01 |
| Trend Analysis (multi) | Multiple actors | ~$0.50-1.50/run |
| Facebook Ads Library | apify/facebook-ads-scraper | ~$0.75/1K ads |
| Facebook Ads (alt) | curious_coder/facebook-ads-library-scraper | ~$0.50/1K ads |
| Google Ads Transparency | lexis-solutions/google-ads-scraper | ~$1.00/1K ads |
| Google Ads (alt) | xtech/google-ad-transparency-scraper | ~$0.80/1K ads |

## Output Location

All scraped data saves to `.tmp/` with timestamped filenames:
- `.tmp/twitter_ai_trends_YYYYMMDD.json`
- `.tmp/reddit_ai_tech_YYYYMMDD.json`
- `.tmp/linkedin_posts_YYYYMMDD_HHMMSS.json`

## Security Notes

### Credential Handling
- Store `APIFY_TOKEN` in `.env` file (never commit to git)
- Rotate API tokens periodically via Apify Console
- Never log or print API tokens in script output
- Use environment variables, not hardcoded values

### Data Privacy
- Scraped data contains only publicly available content
- Social media posts may include PII (names, handles, profile info)
- Data is stored locally in `.tmp/` directory
- No data is retained by Apify after actor run completes
- Consider data minimization - only scrape what you need

### Access Scopes
- Apify tokens have full account access (no granular scopes)
- Use separate Apify accounts for different projects if needed
- Monitor usage via Apify Console dashboard

### Compliance Considerations
- **Terms of Service**: Respect each platform's ToS (Twitter, Reddit, LinkedIn)
- **Rate Limiting**: Actors have built-in rate limiting to avoid bans
- **Robots.txt**: Some actors may bypass robots.txt - use responsibly
- **GDPR**: Scraped PII may be subject to GDPR if EU residents
- **Ethical Use**: Only scrape public data; never bypass authentication
- **Proxy Ethics**: Residential proxies should be used ethically

## Troubleshooting

### Common Issues

#### Issue: Actor run failed
**Symptoms:** Script terminates with "Actor run failed" or timeout error
**Cause:** Invalid actor ID, insufficient proxy credits, or actor configuration issue
**Solution:**
- Verify the actor ID is correct in the script
- Check Apify Console for actor run logs
- Ensure proxy settings match actor requirements
- Try running with default proxy settings first

#### Issue: Empty results returned
**Symptoms:** Script completes but returns 0 items
**Cause:** Content blocked by platform, invalid query, or proxy being detected
**Solution:**
- Try a different proxy type (residential vs datacenter)
- Simplify the search query
- Reduce the number of results requested
- Check if the platform is blocking scraping attempts

#### Issue: Rate limited by platform
**Symptoms:** Script fails with 429 errors or "rate limited" messages
**Cause:** Too many requests in a short time period
**Solution:**
- Add delays between requests (actor settings)
- Reduce concurrent requests
- Use proxy rotation
- Wait and retry after a cooldown period

#### Issue: Invalid API token
**Symptoms:** Authentication error or "invalid token" message
**Cause:** Token expired, revoked, or incorrectly set
**Solution:**
- Regenerate API token in Apify Console
- Verify token is correctly set in `.env` file
- Check for leading/trailing whitespace in token
- Ensure `APIFY_TOKEN` environment variable is loaded

#### Issue: Proxy connection errors
**Symptoms:** Connection timeout or proxy errors
**Cause:** Proxy pool exhausted or geo-restriction issues
**Solution:**
- Switch proxy type (basic, residential, or datacenter)
- Verify proxy credit balance in Apify Console
- Try a different proxy country/region
- Disable proxy to test if that's the root cause

## Resources

### Platform References
- **references/twitter.md** - Twitter/X scraping details
- **references/reddit.md** - Reddit scraping with subreddit targeting
- **references/linkedin.md** - LinkedIn post scraping (author or search mode)
- **references/instagram.md** - Instagram profile, posts, hashtag, reels, and comments scraping
- **references/facebook.md** - Facebook page, posts, reviews, groups, and marketplace scraping
- **references/multi-platform.md** - TikTok and YouTube scraping
- **references/url-detect.md** - Auto-detect URL type and scrape

### Business/Places References
- **references/google-maps.md** - Google Maps business search, place details, and reviews
- **references/contact-enrichment.md** - Extract emails, phone numbers, and social profiles from websites

### Workflow References
- **workflows/lead-generation.md** - Multi-step lead generation workflow
- **workflows/influencer-discovery.md** - Find and analyze influencers across platforms
- **workflows/competitor-intel.md** - Competitive intelligence gathering workflow
- **workflows/trend-analysis.md** - Enriched multi-platform trend analysis with scoring

## Integration Patterns

### Scrape and Enrich
**Skills:** apify-scrapers → parallel-research
**Use case:** Scrape social media posts, then enrich with deep research
**Flow:**
1. Scrape Twitter/Reddit for mentions of a topic
2. Extract company names or URLs from posts
3. Use parallel-research to get detailed info on each company

### Scrape and Summarize
**Skills:** apify-scrapers → content-generation
**Use case:** Create newsletter content from social media trends
**Flow:**
1. Scrape trending AI posts from Twitter
2. Pass scraped data to content-generation summarize
3. Generate a formatted newsletter section

### Scrape and Archive
**Skills:** apify-scrapers → google-workspace
**Use case:** Save scraped data to Google Drive for team access
**Flow:**
1. Scrape LinkedIn posts from target accounts
2. Format data as CSV or JSON
3. Upload to Google Drive client folder via google-workspace

### Trend Analysis + Content Strategy
**Skills:** apify-scrapers (trend-analysis) → content-generation
**Use case:** Identify trending topics and create content strategy
**Flow:**
1. Run trend analysis: `python scripts/analyze_trends.py "AI productivity" --sources all`
2. Review lifecycle stage and opportunity score
3. Use content-generation to create content for high-opportunity trends
4. Focus on emerging trends with high velocity scores

### Competitive Trend Monitoring
**Skills:** apify-scrapers (trend-analysis) → parallel-research
**Use case:** Monitor competitor visibility in trending topics
**Flow:**
1. Analyze industry trends: `python scripts/analyze_trends.py --category "your-industry" --discover`
2. Compare your brand vs competitors in those trends
3. Use parallel-research for deep dive on gaps
4. Generate competitive intelligence report
