---
name: social-media-automation
description: >
  Multi-platform social media automation patterns for Facebook, Instagram, and Twitter (X)
  with MCP server templates, API integration examples, platform-specific constraints, and
  coordinated posting workflows. Includes draft generation with character limits, image
  requirements, rate limit handling, and human approval gates. Use when: (1) building
  multi-platform social media automation, (2) implementing Facebook/Instagram/Twitter API
  integrations, (3) creating coordinated cross-platform posting, (4) handling platform-specific
  constraints (character limits, media requirements), (5) extending Gold tier with Phase 2B
  social media features.
---

# Social Media Automation

## Multi-Platform Architecture

```
Company_Handbook.md → Social Media Generator
                             ↓
          ┌──────────────────┼──────────────────┐
          ↓                  ↓                  ↓
    Facebook Draft    Instagram Draft    Twitter Draft
          ↓                  ↓                  ↓
    Pending_Approval/  Pending_Approval/  Pending_Approval/
      Social/            Social/            Social/
        Facebook/          Instagram/         Twitter/
          ↓                  ↓                  ↓
    [Human approval for each platform separately]
          ↓                  ↓                  ↓
    Facebook MCP       Instagram MCP      Twitter MCP
    (Graph API)        (Basic Display)    (API v2)
```

---

## Facebook Integration

### Facebook MCP Server

```python
# mcp_servers/facebook_mcp/server.py
import requests
import json
import sys

def create_post(message: str, access_token: str, page_id: str) -> dict:
    """Post to Facebook Page via Graph API"""
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

    params = {
        "message": message,
        "access_token": access_token
    }

    try:
        response = requests.post(url, params=params, timeout=30)
        data = response.json()

        if response.status_code == 200:
            return {
                "post_id": data['id'],
                "post_url": f"https://www.facebook.com/{data['id']}"
            }
        elif response.status_code == 429:
            raise Exception("RATE_LIMITED: Facebook API rate limit")
        else:
            raise Exception(f"FACEBOOK_API_ERROR: {data.get('error', {}).get('message')}")

    except requests.exceptions.Timeout:
        raise Exception("NETWORK_ERROR: Facebook API timeout")

def read_feed(access_token: str, page_id: str, limit: int = 10) -> dict:
    """Read recent posts from Facebook Page"""
    url = f"https://graph.facebook.com/v18.0/{page_id}/feed"

    params = {
        "fields": "id,message,created_time,reactions.summary(true)",
        "limit": limit,
        "access_token": access_token
    }

    response = requests.get(url, params=params)
    return response.json()
```

**Config:**
```json
// mcp_servers/facebook_mcp/config.json
{
  "FACEBOOK_APP_ID": "your-app-id",
  "FACEBOOK_APP_SECRET": "your-app-secret",
  "FACEBOOK_ACCESS_TOKEN": "page-access-token",
  "FACEBOOK_PAGE_ID": "your-page-id"
}
```

**Character Limit:** 63,206 characters

---

## Instagram Integration

### Instagram MCP Server

```python
# mcp_servers/instagram_mcp/server.py
import requests
import json
import base64

def create_post(image_url: str, caption: str, access_token: str, user_id: str) -> dict:
    """Create Instagram post via Basic Display API"""

    # Step 1: Create media container
    container_url = f"https://graph.instagram.com/v18.0/{user_id}/media"
    container_params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": access_token
    }

    container_response = requests.post(container_url, params=container_params)
    container_data = container_response.json()

    if 'id' not in container_data:
        raise Exception(f"Instagram container creation failed: {container_data}")

    container_id = container_data['id']

    # Step 2: Publish media container
    publish_url = f"https://graph.instagram.com/v18.0/{user_id}/media_publish"
    publish_params = {
        "creation_id": container_id,
        "access_token": access_token
    }

    publish_response = requests.post(publish_url, params=publish_params)
    publish_data = publish_response.json()

    if 'id' not in publish_data:
        raise Exception(f"Instagram publish failed: {publish_data}")

    return {
        "post_id": publish_data['id'],
        "post_url": f"https://www.instagram.com/p/{publish_data['id']}/"
    }

def create_story(image_url: str, access_token: str, user_id: str) -> dict:
    """Create Instagram story"""
    url = f"https://graph.instagram.com/v18.0/{user_id}/media"

    params = {
        "image_url": image_url,
        "media_type": "STORIES",
        "access_token": access_token
    }

    # Similar two-step process: create container, then publish
    # ...
```

**Requirements:**
- Image required for posts
- Supported formats: JPEG, PNG
- Aspect ratio: 1:1 (square), 4:5 (portrait), 1.91:1 (landscape)
- Caption max: 2,200 characters

---

## Twitter (X) Integration

### Twitter MCP Server

```python
# mcp_servers/twitter_mcp/server.py
import requests
import json
from requests_oauthlib import OAuth1

def create_tweet(text: str, api_key: str, api_secret: str,
                  access_token: str, access_secret: str) -> dict:
    """Post tweet via Twitter API v2"""

    # Twitter API v2 requires OAuth 1.0a
    auth = OAuth1(api_key, api_secret, access_token, access_secret)

    url = "https://api.twitter.com/2/tweets"
    payload = {"text": text}

    try:
        response = requests.post(url, auth=auth, json=payload, timeout=30)
        data = response.json()

        if response.status_code == 201:
            tweet_id = data['data']['id']
            return {
                "tweet_id": tweet_id,
                "tweet_url": f"https://twitter.com/i/web/status/{tweet_id}"
            }
        elif response.status_code == 429:
            raise Exception("RATE_LIMITED: Twitter API rate limit (wait 15 min)")
        else:
            raise Exception(f"TWITTER_API_ERROR: {data.get('errors', [{}])[0].get('message')}")

    except requests.exceptions.Timeout:
        raise Exception("NETWORK_ERROR: Twitter API timeout")

def read_mentions(api_key: str, api_secret: str, access_token: str,
                   access_secret: str, max_results: int = 10) -> dict:
    """Read recent mentions"""
    auth = OAuth1(api_key, api_secret, access_token, access_secret)
    url = f"https://api.twitter.com/2/users/me/mentions"

    params = {
        "max_results": max_results,
        "tweet.fields": "created_at,author_id,conversation_id"
    }

    response = requests.get(url, auth=auth, params=params)
    return response.json()
```

**Character Limit:** 280 characters (strict enforcement)

---

## Multi-Platform Draft Generator

### Coordinated Content Creation

```python
# scripts/social_media_generator.py
from agent_skills.draft_generator import (
    generate_facebook_post,
    generate_instagram_post,
    generate_twitter_tweet
)

def generate_coordinated_posts():
    """Generate drafts for all 3 platforms with aligned messaging"""

    # Read business context
    handbook = parse_markdown_file('vault/Company_Handbook.md')
    social_strategy = extract_social_media_strategy(handbook)

    # Generate core message
    core_message = generate_core_message(social_strategy)

    # Platform-specific adaptations
    drafts = {
        "facebook": generate_facebook_post(core_message, max_chars=63206),
        "instagram": generate_instagram_post(core_message, requires_image=True),
        "twitter": generate_twitter_tweet(core_message, max_chars=280)
    }

    # Save to respective folders
    for platform, draft in drafts.items():
        save_draft(draft, f"vault/Pending_Approval/Social/{platform.title()}/")

    print(f"✅ Created {len(drafts)} coordinated social media drafts")
```

### Platform-Specific Generators

```python
# agent_skills/draft_generator.py (extensions)

def generate_facebook_post(core_message: str, max_chars: int = 63206) -> dict:
    """Generate Facebook post (long-form allowed)"""
    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": f"""Adapt this message for Facebook:

{core_message}

Requirements:
- Longer, more detailed than other platforms
- Conversational and engaging
- Call-to-action for comments/shares
- Max {max_chars} characters
"""
        }]
    )

    content = response.content[0].text
    return {
        "platform": "facebook",
        "action": "create_post",
        "content": content[:max_chars],
        "character_count": len(content),
        "status": "pending_approval"
    }

def generate_instagram_post(core_message: str, requires_image: bool = True) -> dict:
    """Generate Instagram post (requires image)"""
    # Similar Claude API call, optimized for Instagram

    return {
        "platform": "instagram",
        "action": "create_post",
        "content": content[:2200],
        "requires_image": True,
        "image_url": "https://example.com/image.jpg",  # Placeholder
        "status": "pending_approval"
    }

def generate_twitter_tweet(core_message: str, max_chars: int = 280) -> dict:
    """Generate Twitter tweet (280 char limit)"""
    client = Anthropic(api_key=os.getenv('CLAUDE_API_KEY'))

    response = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=500,
        messages=[{
            "role": "user",
            "content": f"""Adapt this message for Twitter (X):

{core_message}

Requirements:
- Concise and punchy
- EXACTLY {max_chars} characters or less
- Can use 1-2 hashtags if relevant
- No emojis unless impactful
"""
        }]
    )

    content = response.content[0].text

    # Auto-truncate at last word if exceeds limit
    if len(content) > max_chars:
        content = content[:max_chars].rsplit(' ', 1)[0]

    return {
        "platform": "twitter",
        "action": "create_tweet",
        "content": content,
        "character_count": len(content),
        "status": "pending_approval"
    }
```

---

## Platform-Specific Validation

```python
def validate_facebook_draft(draft: dict):
    """Validate Facebook post requirements"""
    assert len(draft['content']) <= 63206, "Facebook post too long"
    assert len(draft['content']) > 0, "Facebook post empty"

def validate_instagram_draft(draft: dict):
    """Validate Instagram post requirements"""
    assert len(draft['content']) <= 2200, "Instagram caption too long"
    assert draft.get('requires_image'), "Instagram requires image"
    assert draft.get('image_url'), "Instagram image_url missing"

def validate_twitter_draft(draft: dict):
    """Validate Twitter tweet requirements"""
    assert len(draft['content']) <= 280, "Tweet exceeds 280 characters"
    assert len(draft['content']) > 0, "Tweet empty"
```

---

## Approval Workflow

### Platform-Specific Handlers

```python
# agent_skills/approval_watcher.py (social media handlers)

def handle_facebook_approval(draft_path: str):
    """Send Facebook post after approval"""
    draft = parse_draft_file(draft_path)

    result = call_mcp_tool("facebook-mcp", "create_post", {
        "message": draft['content'],
        "access_token": os.getenv('FACEBOOK_ACCESS_TOKEN'),
        "page_id": os.getenv('FACEBOOK_PAGE_ID')
    })

    log_mcp_action("facebook-mcp", "create_post", "success", draft_path)

def handle_instagram_approval(draft_path: str):
    """Send Instagram post after approval"""
    draft = parse_draft_file(draft_path)

    result = call_mcp_tool("instagram-mcp", "create_post", {
        "image_url": draft['image_url'],
        "caption": draft['content'],
        "access_token": os.getenv('INSTAGRAM_ACCESS_TOKEN'),
        "user_id": os.getenv('INSTAGRAM_USER_ID')
    })

    log_mcp_action("instagram-mcp", "create_post", "success", draft_path)

def handle_twitter_approval(draft_path: str):
    """Send Twitter tweet after approval"""
    draft = parse_draft_file(draft_path)

    result = call_mcp_tool("twitter-mcp", "create_tweet", {
        "text": draft['content'],
        "api_key": os.getenv('TWITTER_API_KEY'),
        "api_secret": os.getenv('TWITTER_API_SECRET'),
        "access_token": os.getenv('TWITTER_ACCESS_TOKEN'),
        "access_secret": os.getenv('TWITTER_ACCESS_SECRET')
    })

    log_mcp_action("twitter-mcp", "create_tweet", "success", draft_path)
```

---

## Rate Limit Handling

| Platform | Rate Limit | Recovery Strategy |
|----------|-----------|-------------------|
| **Facebook** | 200 calls/hour | Retry after 60 min |
| **Instagram** | 200 calls/hour | Retry after 60 min |
| **Twitter** | 300 tweets/3 hours | Retry after 15 min |

```python
def handle_rate_limit(platform: str, draft_path: str):
    """Platform-specific rate limit retry"""
    retry_delays = {
        "facebook": 60,  # minutes
        "instagram": 60,
        "twitter": 15
    }

    update_draft_status(draft_path, "rate_limited_retry")
    schedule_retry(draft_path, delay_minutes=retry_delays[platform])
```

---

## Testing

```python
# tests/integration/test_multi_platform_workflow.py
def test_coordinated_posting():
    """Test multi-platform coordinated posting"""

    # Generate coordinated drafts
    generate_coordinated_posts()

    # Verify all 3 drafts created
    assert os.path.exists('vault/Pending_Approval/Social/Facebook/')
    assert os.path.exists('vault/Pending_Approval/Social/Instagram/')
    assert os.path.exists('vault/Pending_Approval/Social/Twitter/')

    # Mock all 3 APIs
    with patch('requests.post') as mock_fb, \
         patch('requests.post') as mock_ig, \
         patch('requests.post') as mock_tw:

        # Approve all drafts
        # ... trigger approval handlers

        # Verify all posted
        assert mock_fb.called
        assert mock_ig.called
        assert mock_tw.called
```

---

## Configuration

```bash
# .env
# Facebook
FACEBOOK_APP_ID=your-app-id
FACEBOOK_APP_SECRET=your-secret
FACEBOOK_ACCESS_TOKEN=page-token
FACEBOOK_PAGE_ID=your-page-id

# Instagram
INSTAGRAM_APP_ID=your-app-id
INSTAGRAM_APP_SECRET=your-secret
INSTAGRAM_ACCESS_TOKEN=user-token
INSTAGRAM_USER_ID=your-user-id

# Twitter
TWITTER_API_KEY=your-api-key
TWITTER_API_SECRET=your-api-secret
TWITTER_ACCESS_TOKEN=user-token
TWITTER_ACCESS_SECRET=user-secret
TWITTER_BEARER_TOKEN=your-bearer-token
```

---

## Troubleshooting

| Issue | Platform | Solution |
|-------|----------|----------|
| **Token expired** | All | Regenerate OAuth tokens via Developer Portal |
| **Image required** | Instagram | Add image_url to draft before approval |
| **Tweet too long** | Twitter | Auto-truncation at 280 chars (last word) |
| **Rate limited** | All | Automatic retry with platform-specific delay |

---

## Key Files

- `scripts/social_media_generator.py` - Multi-platform generator
- `mcp_servers/facebook_mcp/server.py` - Facebook Graph API
- `mcp_servers/instagram_mcp/server.py` - Instagram Basic Display API
- `mcp_servers/twitter_mcp/server.py` - Twitter API v2
- `vault/Pending_Approval/Social/{Facebook,Instagram,Twitter}/` - Platform-specific queues

---

**Note:** This skill provides templates and patterns for Phase 2B social media integration. Implement Facebook/Instagram/Twitter MCPs following these patterns for full Gold tier+ functionality.
