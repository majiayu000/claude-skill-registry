---
name: social-media
description: Social media content, API integrations, scheduling. X, Facebook, Threads, LinkedIn, YouTube, TikTok. OAuth, rate limits, media uploads, engagement, threads.
license: MIT
version: 2.0.0
---

# Social Media Skill

Content creation, API integrations, and scheduling for X, Facebook, Threads, LinkedIn, YouTube, TikTok.

## When to Use

- Create social media content (posts, threads, carousels)
- Implement API posting automation
- Build scheduling systems
- Handle OAuth authentication flows
- Manage media uploads and rate limits

## Quick Reference

| Platform | Max Length | API | Best Times (UTC) |
|----------|------------|-----|------------------|
| X/Twitter | 280/4000 | v2 OAuth 1.0a | Tue-Fri 9am-12pm |
| LinkedIn | 3000 | REST v2 | Tue-Thu 8-10am |
| Facebook | 63,206 | Graph v20.0 | Mon-Fri 9am-1pm |
| Threads | 500 | Graph v1.0 | Mon-Fri 11am-2pm |
| TikTok | 2000 | v2 | Tue-Thu 7-9pm |
| YouTube | 5000 (desc) | Data v3 | Thu-Sat 2-5pm |

## References

### Content & Strategy
- `references/platform-specs.md` - Platform character limits, formats
- `references/posting-best-practices.md` - Optimal posting strategies
- `references/thread-templates.md` - Thread/carousel templates
- `references/engagement-templates.md` - Engagement reply templates
- `references/hook-writing.md` - Hook formulas for attention

### API Workflows
- `references/x-twitter-workflow.md` - X posting, threads, OAuth 1.0a
- `references/linkedin-workflow.md` - Personal, company pages, PDF carousels
- `references/facebook-workflow.md` - Pages, Reels, scheduling
- `references/threads-workflow.md` - Carousel, reply threads
- `references/tiktok-workflow.md` - Video/photo posting
- `references/youtube-workflow.md` - Video upload, thumbnails
- `references/rate-limits-errors.md` - API limits, retry strategies
- `references/unified-api-services.md` - Ayrshare, Late.dev alternatives

## Scripts

```bash
# Validate post content
node scripts/validate-post-content.js --platform x --content "Your post" --media "img.jpg"
node scripts/validate-post-content.js --platform x --premium --content "Long premium post..."

# Schedule posts with optimal timing
node scripts/schedule-post.js --suggest-time --platforms "x,linkedin,tiktok"
node scripts/schedule-post.js --platforms "x,linkedin" --content "Hello" --time "2026-01-21T10:00:00Z"
```

## Core Workflows

### Content Creation
1. Define platform and goal
2. Write platform-optimized copy (load `posting-best-practices.md`)
3. Create hook using formulas (load `hook-writing.md`)
4. Add visuals, hashtags
5. Schedule optimal time

### Thread Creation
1. Choose type: educational, story, list, how-to
2. Write hook (most important)
3. Outline 5-15 posts
4. End with CTA

### API Posting
1. Authenticate: OAuth 2.0 (most) or OAuth 1.0a (X)
2. Upload media (chunked for large videos)
3. Validate content via `validate-post-content.js`
4. Create post with media IDs
5. Handle errors with exponential backoff

## Environment Variables

```bash
# X (Twitter)
X_API_KEY=
X_API_SECRET=

# LinkedIn
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=

# Facebook/Threads (Meta)
FACEBOOK_APP_ID=
FACEBOOK_APP_SECRET=

# TikTok
TIKTOK_CLIENT_ID=
TIKTOK_CLIENT_SECRET=

# YouTube
YOUTUBE_CLIENT_ID=
YOUTUBE_CLIENT_SECRET=

# Unified APIs
AYRSHARE_API_KEY=
LATE_API_KEY=
```

## Best Practices

1. **Content**: Native content > cross-posted
2. **Timing**: Test posting times for your audience
3. **Engagement**: Respond within 1 hour
4. **Tokens**: Refresh before expiry
5. **Rate Limits**: Exponential backoff (5s, 10s, 20s...)
6. **Media**: Resize images (<4MB), check video duration

## Related Skills

- `video-production` - Video content specs
- `campaign-management` - Multi-platform campaigns
- `copywriting` - High-converting copy

## Agent Integration

**Primary Agents:** social-media-manager, content-creator, community-manager
