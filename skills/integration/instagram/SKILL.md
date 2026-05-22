---
name: instagram
description: Instagram Graph API integration via curl. Use this skill to fetch and publish Instagram media.
vm0_secrets:
  - INSTAGRAM_ACCESS_TOKEN
vm0_vars:
  - INSTAGRAM_BUSINESS_ACCOUNT_ID
---

# Instagram API (Graph API)

Use the Instagram Graph API by directly executing `curl` commands to **read and publish Instagram content**.

> Official docs: `https://developers.facebook.com/docs/instagram-api`

---

## When to Use

Use this skill when you need to:

- **Fetch recent media (photos / videos / Reels)** from an account
- **Get detailed information** about a specific media item (caption, type, link, time, etc.)
- **Search recent media by hashtag**
- **Publish image posts via API** (with caption)

---

## Prerequisites

1. You must have an **Instagram Business / Creator account** linked to a **Facebook Page**
2. Create an app in Facebook Developers and enable **Instagram Basic Display / Instagram Graph API** permissions
3. Obtain:
  - `INSTAGRAM_ACCESS_TOKEN`: a long-lived user access token
  - `INSTAGRAM_BUSINESS_ACCOUNT_ID`: your Instagram Business account ID

Set the environment variables, for example:

```bash
export INSTAGRAM_ACCESS_TOKEN="EAAG..."
export INSTAGRAM_BUSINESS_ACCOUNT_ID="1784140xxxxxxx"
```

These examples use Graph API version `v21.0`. You can replace this with the latest version if needed.

### Required permissions (scopes)

Depending on which endpoints you use, make sure your app has requested and been approved for (at least):

- `instagram_basic`
- `pages_show_list`
- `instagram_content_publish` (for publishing media)
- `instagram_manage_insights` and related permissions (for insights / some hashtag use cases)

---


> **Important:** When using `$VAR` in a command that pipes to another command, wrap the command containing `$VAR` in `bash -c '...'`. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.example.com" -H "Authorization: Bearer $API_KEY"' | jq '.'
> ```

## How to Use

All examples below assume you have already set:

```bash
INSTAGRAM_ACCESS_TOKEN
INSTAGRAM_BUSINESS_ACCOUNT_ID
```

### 1. Fetch recent media for the account

Fetch the most recent media (photos / videos / Reels) for the account:

```bash
bash -c 'curl -s -X GET "https://graph.facebook.com/v21.0/${INSTAGRAM_BUSINESS_ACCOUNT_ID}/media?fields=id,caption,media_type,media_url,permalink,timestamp" --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

**Notes:**

- Each item in the returned JSON represents a media object
- Common fields:
  - `id`: media ID (used for details / insights later)
  - `caption`: caption text
  - `media_type`: `IMAGE` / `VIDEO` / `CAROUSEL_ALBUM`
  - `media_url`: direct URL to the media
  - `permalink`: Instagram permalink
  - `timestamp`: creation time

---

### 2. Get details for a single media

If you already have a media `id`, you can fetch more complete information. Replace `<your-media-id>` with the `id` field from the "Get User Media" response (section 1 above):

```bash
bash -c 'curl -s -X GET "https://graph.facebook.com/v21.0/<your-media-id>?fields=id,caption,media_type,media_url,permalink,thumbnail_url,timestamp,username" --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

---

### 3. Search media by hashtag

> Note: hashtag search requires proper business use cases and permissions as defined by Facebook/Instagram. Refer to the official docs.

This usually involves two steps:

#### 3.1 Get the hashtag ID

Replace `<hashtag-name>` with any hashtag name you want to search for (without the # symbol), e.g., "travel", "food", "photography":

```bash
bash -c 'curl -s -X GET "https://graph.facebook.com/v21.0/ig_hashtag_search?user_id=${INSTAGRAM_BUSINESS_ACCOUNT_ID}&q=<hashtag-name>" --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

Note the `id` field in the returned JSON for use in the next step.

#### 3.2 Fetch recent media for the hashtag

Replace `<hashtag-id>` with the `id` field from the "Search Hashtag" response (section 3.1 above):

```bash
bash -c 'curl -s -X GET "https://graph.facebook.com/v21.0/<hashtag-id>/recent_media?user_id=${INSTAGRAM_BUSINESS_ACCOUNT_ID}&fields=id,caption,media_type,media_url,permalink,timestamp" --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

---

### 4. Publish an image post

Publishing an image post via the Graph API usually requires **two steps**:

1. **Create a media container**
2. **Publish the container to the feed**

#### 4.1 Create a media container

Write the request data to `/tmp/request.json`:

```json
{
  "image_url": "https://example.com/image.jpg",
  "caption": "Hello from Instagram API 👋"
}
```

Replace `https://example.com/image.jpg` with any publicly accessible image URL and update the caption text as needed.

```bash
bash -c 'curl -s -X POST "https://graph.facebook.com/v21.0/${INSTAGRAM_BUSINESS_ACCOUNT_ID}/media" -H "Content-Type: application/json" -d @/tmp/request.json --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

The response will contain an `id` (media container ID), for example:

```json
{
  "id": "1790xxxxxxxxxxxx"
}
```

Note this ID for use in the next step.

#### 4.2 Publish the media container to the feed

Write the request data to `/tmp/request.json`:

```json
{
  "creation_id": "<your-creation-id>"
}
```

Replace `<your-creation-id>` with the `id` field from the "Create Media Container" response (section 4.1 above):

```bash
bash -c 'curl -s -X POST "https://graph.facebook.com/v21.0/${INSTAGRAM_BUSINESS_ACCOUNT_ID}/media_publish" -H "Content-Type: application/json" -d @/tmp/request.json --header "Authorization: Bearer ${INSTAGRAM_ACCESS_TOKEN}"'
```

If successful, the response will contain the final media `id`:

```json
{
  "id": "1791yyyyyyyyyyyy"
}
```

You can then use the "Get details for a single media" command to fetch its `permalink`.

---

### 5. Common errors and troubleshooting

1. **Permissions / OAuth errors**

  - Typical error message: `(#10) Application does not have permission for this action`
  - Check:
  - Whether the app has been reviewed / approved
  - Whether the required Instagram permissions are enabled
  - Whether `INSTAGRAM_ACCESS_TOKEN` is a valid long-lived token

2. **Unsupported account type**

  - Most Graph API features require **Business / Creator** accounts
  - Make sure the Instagram account type is correct and linked to a Facebook Page

3. **Rate limits**
  - Too many requests in a short period may hit rate limits; add delays for bulk operations

---

## Guidelines

1. **Do not log tokens**: `INSTAGRAM_ACCESS_TOKEN` is sensitive; avoid printing it in logs or chat transcripts
2. **Validate curl commands in a test environment first**: confirm flows before wiring them into automation / agents
3. **Keep API version up to date**: periodically check Facebook docs and update the `v21.0` version in URLs to the latest
4. **Use placeholder text for IDs**: all examples use placeholder text like `<your-media-id>` instead of shell variables in URLs to avoid dependencies and make examples self-contained
