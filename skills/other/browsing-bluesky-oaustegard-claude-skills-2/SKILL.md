---
name: browsing-bluesky
description: Browse Bluesky content via API and firehose - search posts, fetch user activity, sample trending topics, read feeds and lists, analyze and categorize accounts. Supports authenticated access for personalized feeds. Use for Bluesky research, user monitoring, trend analysis, feed reading, firehose sampling, account categorization.
metadata:
  version: 0.5.1
---

# Browsing Bluesky

Access Bluesky content through public APIs and real-time firehose. Supports optional authentication for personalized feeds. Includes account analysis for categorization.

## Implementation

Add skill directory to path and import:

```python
import sys
sys.path.insert(0, '/path/to/skills/browsing-bluesky')  # or use .claude/skills symlink path
from browsing_bluesky import (
    # Core browsing
    search_posts, get_user_posts, get_profile, get_feed_posts, sample_firehose,
    get_thread, get_quotes, get_likes, get_reposts,
    get_followers, get_following, search_users,
    # Trending
    get_trending, get_trending_topics,
    # Account analysis
    get_all_following, get_all_followers, extract_post_text,
    extract_keywords, analyze_account, analyze_accounts,
    # Authentication utilities
    is_authenticated, get_authenticated_user, clear_session
)
```

## Authentication (Optional)

Authentication enables personalized feeds (like Paper Skygest) that require knowing who's asking.

### Setup

1. Create an app password at Bluesky: **Settings → Privacy and Security → App Passwords**
2. Set environment variables:
   ```bash
   export BSKY_HANDLE="yourhandle.bsky.social"
   export BSKY_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   ```

### Behavior

- **Transparent**: All functions work identically with or without credentials
- **Automatic**: Auth headers are added opportunistically when credentials exist
- **Graceful**: Failed auth silently falls back to public access
- **Secure**: Tokens cached in memory only, never logged or persisted

### Check Auth Status

```python
if is_authenticated():
    print(f"Logged in as: {get_authenticated_user()}")
else:
    print("Using public access")

# Clear session if needed (e.g., switching accounts)
clear_session()
```

## Research Workflows

### Investigate a Topic

Use `search_posts()` with query syntax matching bsky.app advanced search:
- Basic terms: `event sourcing`
- Exact phrases: `"event sourcing"`
- User filter: `from:acairns.co.uk` or use `author=` param
- Date filter: `since:2025-01-01` or use `since=` param
- Hashtags, mentions, domain links: `#python mentions:user domain:github.com`

Combine query syntax with function params for complex searches.

### Monitor a User

1. Fetch profile with `get_profile(handle)` for context (bio, follower count, post count)
2. Get recent posts with `get_user_posts(handle, limit=N)`
3. For topic-specific user content, use `search_posts(query, author=handle)`

### Discover What's Trending

**Recommended workflow** — trending API first, firehose for deep dives:

#### 1. Quick scan with trending topics (~500 tokens)

```python
topics = get_trending_topics(limit=10)
# Returns: {topics: [{topic, display_name, description, link}, ...],
#           suggested: [...]}
```

#### 2. Rich trends with post counts and actors

```python
trends = get_trending(limit=10)
for t in trends:
    print(f"{t['display_name']} — {t['post_count']} posts ({t['status']})")
# Each trend includes: topic, display_name, link, started_at,
#   post_count, status, category, actors
```

#### 3. Targeted exploration of selected trends

```python
posts = search_posts(trend["topic"], limit=25)
```

#### 4. Optional: Firehose for velocity monitoring or long-tail discovery

**Prerequisites**: Install Node.js dependencies once per session:
```bash
cd /home/claude && npm install ws https-proxy-agent 2>/dev/null
```

```python
data = sample_firehose(duration=30)  # Full firehose sample
data = sample_firehose(duration=20, filter="python")  # Filtered sample
```

Returns dict with keys:
- **window**: `{startTime, endTime, durationSeconds}` — sampling time range
- **stats**: `{totalReceived, totalPosts, postsPerSecond, filter, languages}` — volume metrics and language breakdown
- **topWords**: `[[word, count], ...]` — top 50 words (count >= 3)
- **topPhrases**: `[[bigram, count], ...]` — top 30 bigrams (count >= 2)
- **topTrigrams**: `[[trigram, count], ...]` — top 20 trigrams (count >= 2)
- **entities**: `[[entity, count], ...]` — top 25 handles/hashtags (count >= 2)
- **samplePosts**: `[{text, altTexts, hasImages}, ...]` — first 50 matching posts

### Read Feeds and Lists

`get_feed_posts()` accepts:
- List URLs: `https://bsky.app/profile/austegard.com/lists/3lankcdrlip2f`
- Feed URLs: `https://bsky.app/profile/did:plc:xxx/feed/feedname`
- AT-URIs: `at://did:plc:xxx/app.bsky.graph.list/xyz`

The function extracts the AT-URI from URLs automatically.

### Explore a Thread

Fetch full thread context for a post with parents and replies:

```python
thread = get_thread("https://bsky.app/profile/user/post/xyz", depth=10)
# Returns: {post: {...}, parent: {...}, replies: [...]}
```

### Find Quote Posts

Discover posts that quote a specific post:

```python
quotes = get_quotes("https://bsky.app/profile/user/post/xyz")
for q in quotes:
    print(f"@{q['author_handle']}: {q['text'][:80]}")
```

### Analyze Engagement

Get users who engaged with a post:

```python
likes = get_likes(post_url)
reposts = get_reposts(post_url)

# Accepts both URLs and AT-URIs
likes = get_likes("at://did:plc:.../app.bsky.feed.post/...")
```

### Explore Social Graph

Navigate follower/following relationships:

```python
followers = get_followers("handle.bsky.social")
following = get_following("handle.bsky.social")

# Returns list of actor dicts with handle, display_name, did, description, etc.
```

### Find Users

Search for users by name, handle, or bio:

```python
users = search_users("machine learning researcher")
for u in users:
    print(f"{u['display_name']} (@{u['handle']}): {u['description'][:100]}")
```

## API Endpoint Notes

- **Public AppView**: `https://api.bsky.app/xrpc/` for unauthenticated reads
- **PDS**: `https://bsky.social/xrpc/` for authenticated requests
- **Trending**: `app.bsky.unspecced.getTrends` (rich) and `app.bsky.unspecced.getTrendingTopics` (lightweight)
- **Firehose**: `wss://jetstream1.us-east.bsky.network/subscribe`
- **Endpoint routing** is automatic - authenticated requests go to PDS, public requests go to AppView
- **Rate limits** exist but are generous for read operations

## Return Format

All API functions return structured dicts with:
- `uri`: AT protocol identifier
- `text`: Post content
- `created_at`: ISO timestamp
- `author_handle`: User handle
- `author_name`: Display name
- `likes`, `reposts`, `replies`: Engagement counts
- `links`: Full URLs extracted from post facets (post text truncates URLs with "...")
- `image_alts`: Alt text from embedded images
- `url`: Direct link to post on bsky.app

Profile function returns: `handle`, `display_name`, `description`, `followers`, `following`, `posts`, `did`

## Account Analysis

Analyze accounts for categorization by topic. Fetches profile and posts, extracts keywords, and returns structured data for Claude to categorize.

### Analyze a User's Network

```python
# Analyze accounts you follow
results = analyze_accounts(following="yourhandle.bsky.social", limit=50)

# Analyze your followers
results = analyze_accounts(followers="yourhandle.bsky.social", limit=50)

# Analyze specific handles
results = analyze_accounts(handles=["user1.bsky.social", "user2.bsky.social"])
```

### Single Account Analysis

```python
analysis = analyze_account("user.bsky.social")
# Returns: {handle, display_name, description, keywords, post_count, followers, following}
```

### Keyword Extraction Options

Stopwords parameter filters domain-specific noise:
- `"en"`: English (general purpose, default)
- `"ai"`: AI/ML domain (filters tech boilerplate)
- `"ls"`: Life Sciences (filters research methodology)

```python
results = analyze_accounts(following="handle", stopwords="ai")
```

**Requires**: `extracting-keywords` skill with YAKE venv for keyword extraction.

### Filtering Accounts

```python
results = analyze_accounts(
    following="handle",
    exclude_patterns=["bot", "spam", "promo"]  # Skip accounts matching these
)
```

### Paginated Following/Followers

For large account lists beyond the 100 limit of `get_following`/`get_followers`:

```python
all_following = get_all_following("handle", limit=500)  # Handles pagination
all_followers = get_all_followers("handle", limit=500)
```

### Account Analysis Output

Each analyzed account returns:
```python
{
    "handle": "user.bsky.social",
    "display_name": "User Name",
    "description": "Bio text here",
    "keywords": ["keyword1", "keyword2", "keyword3"],
    "post_count": 20,
    "followers": 1234,
    "following": 567
}
```

Claude uses bio + keywords to categorize accounts by topic without hardcoded rules
