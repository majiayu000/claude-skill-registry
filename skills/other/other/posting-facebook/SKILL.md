---
name: posting-facebook
description: |
  Post content to Facebook using Meta Graph API.
  Use when publishing Facebook posts, configuring posting schedule,
  managing post queue, or getting engagement insights.
  NOT when posting to Instagram (use posting-instagram instead).
---

# Facebook Poster Skill

Automated Facebook posting via Meta Graph API.

## Quick Start

```bash
# Post content (requires approval)
python scripts/run.py --post "Your post content here"

# Post with link
python scripts/run.py --post "Check this out!" --link "https://example.com"

# Get insights
python scripts/run.py --insights --days 7

# Verify setup
python scripts/verify.py
```

## Setup

### 1. Get Meta Access Token

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create an App
3. Add "Pages" product
4. Generate access token with permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
5. Get your Facebook Page ID

### 2. Configure Environment

Add to `.env`:
```
META_ACCESS_TOKEN=your_access_token_here
FACEBOOK_PAGE_ID=your_page_id_here
GRAPH_API_VERSION=v18.0
```

## Features

### Posting
- Text posts with optional links
- Approval workflow (default)
- Rate limiting (25 posts/day, 5/hour)
- Audit logging

### Analytics
- Page impressions
- Engagement metrics
- Fan growth
- Post performance

## Approval Workflow

Posts create files in `Vault/Pending_Approval/`:
- Review and edit content
- Move to `Vault/Approved/` to publish
- Or delete to reject

## Rate Limits

- **Daily:** 25 posts
- **Hourly:** 5 posts

Enforced automatically by MCP server.

## Verification

Run: `python scripts/verify.py`

Expected: `✓ posting-facebook valid`

## References

- [Meta Graph API Docs](https://developers.facebook.com/docs/graph-api)
- [Pages API](https://developers.facebook.com/docs/pages/overview)
