---
name: instagram-api
description: Instagram Graph API entegrasyonu. Use when publishing content, fetching insights, or working with Instagram media.
---

# Instagram Graph API

**Version:** v21.0 | **Base:** `https://graph.instagram.com/v21.0`

## Quick Reference

| Action | Endpoint | Method |
|--------|----------|--------|
| Create Container | `/{user_id}/media` | POST |
| Publish | `/{user_id}/media_publish` | POST |
| Check Status | `/{container_id}` | GET |
| Get Insights | `/{media_id}/insights` | GET |

## Two-Phase Publishing

```
1. Create Container → container_id
2. (Video only) Poll until FINISHED
3. Publish Container → post_id
```

## Publishing Functions

```python
from app.instagram_helper import (
    post_photo_to_instagram,
    post_video_to_instagram,
    post_carousel_to_instagram
)

# Image
result = await post_photo_to_instagram(image_url, caption)

# Reels
result = await post_video_to_instagram(video_url, caption)

# Carousel (2-10 images)
result = await post_carousel_to_instagram(image_urls, caption)
```

## Video Requirements

| Spec | Value |
|------|-------|
| Resolution | 720x1280 (9:16) |
| Codec | H.264 video, AAC audio |
| FPS | 30 |
| Max | 90 seconds |

```python
# Auto-convert
from app.instagram_helper import convert_video_for_instagram
result = await convert_video_for_instagram(input_path)
# Returns: {success, output_path, converted, file_size_mb}
```

## Insights

```python
from app.insights_helper import get_instagram_media_insights

insights = await get_instagram_media_insights(media_id)
# Returns: {plays, reach, saves, shares, likes, comments, engagement_rate}
```

**Reels metrics:** plays, reach, saved, shares, comments, likes
**Image metrics:** impressions, reach, saved

## Rate Limiting

- Container creation: 2s delay
- Video polling: 10s interval, max 30 attempts
- Insights fetch: 0.3s delay between calls

## Environment Variables

```bash
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_USER_ID=...
INSTAGRAM_BUSINESS_ID=...  # Optional
```

## Return Format

```python
# Success
{"success": True, "id": "17901234567890123", "platform": "instagram"}

# Error
{"success": False, "error": "Error message"}
```

## Common Errors

| Error | Solution |
|-------|----------|
| OAuthException | Token expired - refresh |
| MediaTypeNotSupported | Wrong format - convert |
| RateLimitError | Too many calls - add delay |

## Deep Links

- `app/instagram_helper.py` - Publishing
- `app/insights_helper.py` - Metrics
- `app/cloudinary_helper.py` - Video CDN
