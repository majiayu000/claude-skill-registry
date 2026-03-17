---
name: posting-instagram
description: |
  Post content to Instagram using Meta Graph API.
  Use when publishing Instagram posts, managing media, getting insights,
  or optimizing hashtags. Requires Instagram Business Account.
  NOT when posting to Facebook (use posting-facebook instead).
---

# Instagram Poster Skill

Automated Instagram posting via Meta Graph API.

## Quick Start

```bash
# Post with image
python scripts/run.py --post "Caption here" --image "https://example.com/image.jpg" --hashtags "business,automation"

# Get insights
python scripts/run.py --insights --days 7

# Verify setup
python scripts/verify.py
```

## Setup

### 1. Requirements

- Instagram Business Account (connected to Facebook Page)
- Facebook Page with Admin access

### 2. Get Credentials

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an App
3. Add "Instagram" product
4. Generate access token with permissions:
   - `instagram_basic`
   - `instagram_content_publish`
   - `pages_read_engagement`
5. Get your Instagram Business Account ID

### 3. Configure Environment

Add to `.env`:
```
META_ACCESS_TOKEN=your_access_token_here
INSTAGRAM_ACCOUNT_ID=your_instagram_account_id_here
GRAPH_API_VERSION=v18.0
```

## Features

### Posting
- Image posts with captions
- Hashtag optimization (up to 30)
- Approval workflow (default)
- Rate limiting (25 posts/day, 5/hour)

### Analytics
- Engagement metrics
- Reach and impressions
- Follower growth
- Best performing content

## Hashtag Strategy

- **Instagram:** Use 20-30 relevant hashtags
- Mix of popular and niche tags
- Industry-specific tags
- Trending tags when relevant

## Approval Workflow

Posts create files in `Vault/Pending_Approval/`:
- Review caption and image
- Edit hashtags as needed
- Move to `Vault/Approved/` to publish

## Rate Limits

- **Daily:** 25 posts
- **Hourly:** 5 posts

## Verification

Run: `python scripts/verify.py`

Expected: `✓ posting-instagram valid`

## References

- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api)
- [Content Publishing](https://developers.facebook.com/docs/instagram-api/guides/content-publishing)
