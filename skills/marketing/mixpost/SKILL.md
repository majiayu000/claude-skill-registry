---
name: mixpost
description: Mixpost is a self-hosted social media management software that helps you schedule and manage your social media content across multiple platforms including Facebook, Twitter/X, Instagram, LinkedIn, Pinterest, TikTok, YouTube, Mastodon, Google Business Profile, Threads, Bluesky, and more.
homepage: https://mixpost.app
metadata: {"openclaw":{"emoji":"🗓️","primaryEnv":"MIXPOST_ACCESS_TOKEN","requires":{"env":["MIXPOST_URL","MIXPOST_ACCESS_TOKEN","MIXPOST_WORKSPACE_UUID"]}}}
---

# Mixpost Skill

Mixpost is a self-hosted social media management software that helps you schedule and manage your social media content across multiple platforms including Facebook, Twitter/X, Instagram, LinkedIn, Pinterest, TikTok, YouTube, Mastodon, Google Business Profile, Threads, Bluesky, and more.

## Setup

1. Navigate to your Mixpost dashboard
2. Click on **Access Tokens** from the user menu
3. Click **Create** to generate a new token
4. Get your workspace UUID: Go to **Social Accounts** page, click the **3 dots menu** on any account, and copy the workspace UUID
5. Set environment variables:
   ```bash
   export MIXPOST_URL="https://your-mixpost-instance.com/mixpost"
   export MIXPOST_ACCESS_TOKEN="your-access-token"
   export MIXPOST_WORKSPACE_UUID="your-workspace-uuid"
   ```

## Test Connection

```bash
curl -X GET "$MIXPOST_URL/api/ping" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## Accounts

### Get all accounts

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/accounts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Get a specific account

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/accounts/:accountUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## Media

### Get all media

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media?limit=50" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Get a specific media file

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media/:mediaUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Upload media (form-data)

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json" \
  -F "file=@/path/to/your/file.png"
```

### Update media

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media/:mediaUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "alt_text": "Alternative text for accessibility"
  }'
```

### Delete media

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/media" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "items": ["media-id-1", "media-id-2"]
  }'
```

---

## Tags

### Get all tags

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Get a specific tag

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Create a tag

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Marketing",
    "hex_color": "#FF5733"
  }'
```

### Update a tag

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Updated Tag Name",
    "hex_color": "#00FF00"
  }'
```

### Delete a tag

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/tags/:tagUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

---

## Posts

### Get all posts

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts?limit=50&status=scheduled&page=1" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

**Query Parameters:**
- `limit` (number, default: 50): Results per page
- `status`: `draft`, `scheduled`, `published`, `failed`, `needs_approval`, `trash`
- `keyword` (string): Search posts by content
- `accounts` (array): Filter by account IDs
- `tags` (array): Filter by tag names
- `page` (number): Page number for pagination

### Get a specific post

```bash
curl -X GET "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Create a post

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "schedule": true,
    "date": "2024-12-25",
    "time": "10:00",
    "timezone": "America/New_York",
    "accounts": [1, 2],
    "tags": [1],
    "versions": [
      {
        "account_id": 0,
        "is_original": true,
        "content": [
          {
            "body": "Hello from Mixpost API!",
            "media": [1, 2],
            "url": "https://example.com"
          }
        ],
        "options": {}
      }
    ]
  }'
```

**Post Options:**
- `schedule`: Set to `true` to schedule for specific date/time
- `schedule_now`: Set to `true` to publish immediately
- `queue`: Set to `true` to add to publishing queue
- If none are set, post is saved as draft

**Platform-specific options:**
```json
{
  "options": {
    "facebook_page": {
      "type": "post" // post, reel, story
    },
    "instagram": {
      "type": "post" // post, reel, story
    },
    "linkedin": {
      "visibility": "PUBLIC" // PUBLIC, CONNECTIONS
    },
    "mastodon": {
      "sensitive": false // boolean
    },
    "pinterest": {
      "link": null, // null | string
      "title": "", // string
      "boards": {
        "account-1": "971672010430333260" // The key `account-*` is the ID of your Pinterest account
      }
    },
    "youtube": {
      "title": null, // null | string
      "status": "public" // public, private, unlisted
    },
    "gbp": { // Google Business Profile
      "type": "post", // post, offer, event
      "button": "NONE", // NONE, BOOK, ORDER, SHOP, LEARN_MORE, SIGN_UP, CALL
      "button_link": "", // Leave empty if button is NONE or CALL
      "offer_has_details": false, // Only applies if type is offer
      "coupon_code": "", // Only applies if type is offer and offer_has_details is true
      "offer_link": "", // Only applies if type is offer and offer_has_details is true
      "terms": "", // Only applies if type is offer and offer_has_details is true
      "event_title": "", // Only applies if type is event or offer
      "start_date": null, // null | string - Only applies if type is event or offer
      "end_date": null, // null | string - Only applies if type is event or offer
      "event_has_time": false, // Only applies if type is event
      "start_time": "09:00", // Only applies if type is event and event_has_time is true
      "end_time": "17:00" // Only applies if type is event and event_has_time is true
    },
    "tiktok": {
      "privacy_level": {
        "account-2": "PUBLIC_TO_EVERYONE" // PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, SELF_ONLY - The key `account-*` is the ID of your TikTok account
      },
      "allow_comments": {
        "account-2": true // boolean
      },
      "allow_duet": {
        "account-2": false // boolean
      },
      "allow_stitch": {
        "account-2": false // boolean
      },
      "content_disclosure": {
        "account-2": false // boolean
      },
      "brand_organic_toggle": {
        "account-2": false // boolean
      },
      "brand_content_toggle": {
        "account-2": false // boolean
      }
    }
  }
}
```

### Update a post

```bash
curl -X PUT "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "content": "Updated post content",
    "schedule_at": "2024-12-25T10:00:00Z",
    "media": ["url1", "url2"],
    "tags": ["tag1", "tag2"],
    "account_ids": ["id1", "id2"]
  }'
```

### Delete a post

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "trash": false,
    "delete_mode": "app_only"
  }'
```

**Delete modes:**
- `app_only`: Delete only from the app (default)
- `app_and_social`: Delete from both app and social media
- `social_only`: Delete only from social media platforms

### Delete multiple posts

```bash
curl -X DELETE "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "posts": ["post-uuid-1", "post-uuid-2"],
    "trash": false,
    "delete_mode": "app_only"
  }'
```

### Schedule a post

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/schedule/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "postNow": false
  }'
```

### Add post to queue

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/add-to-queue/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```

### Approve a post

```bash
curl -X POST "$MIXPOST_URL/api/$MIXPOST_WORKSPACE_UUID/posts/approve/:postUuid" \
  -H "Authorization: Bearer $MIXPOST_ACCESS_TOKEN" \
  -H "Accept: application/json"
```
