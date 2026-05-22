---
name: bluesky
description: Read from and post to Bluesky social network using the AT Protocol. Use this skill when the user wants to interact with Bluesky including posting text/images/links, replying to posts, reading their timeline, searching posts, viewing profiles, following/unfollowing users, checking notifications, or viewing reply threads. All scripts use PEP 723 inline metadata for dependencies and run via `uv run`. Requires BLUESKY_HANDLE and BLUESKY_PASSWORD environment variables.
---

# Skill Overview

This skill provides access to the Bluesky social network via a set of Python scripts.

## Identify Yourself in Each Post

When posting to BlueSky, always start the post with a brief statement saying who you are and that you are using the user's BlueSky account.  Something short like: `This is [AI name] posting using [user name]'s account.` is good, but feel free to vary it.  Replace `[AI name]` with your name and `[user name]` with the user's BlueSky full name or first name for brevity.

## Prerequisites

**Tool Dependency**:
- `uv` - The scripts in this skill require the [uv](https://docs.astral.sh/uv/) package manager/runner. Most cloud-based AI agents have `uv` pre-installed (or they can install it). Local agents should install it via `curl -LsSf https://astral.sh/uv/install.sh | sh` or see the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/).

**Environment Variables** (must be set before running any script):
- `BLUESKY_HANDLE` - The user's Bluesky handle (e.g., `username.bsky.social`)
- `BLUESKY_PASSWORD` - The user's Bluesky password

**Important**: The user should configure a BlueSky App Password (create in Settings > App Passwords) instead of using their main account password. App Passwords can be revoked individually if compromised.

## Network Access

**Important**: The scripts in this skill require network access to the following domains:

- `bsky.social`
- `bsky.network`
- `*.bsky.network`
- `public.api.bsky.app`

If you (the AI agent) have network restrictions, the user may need to whitelist the above domains in the agent's settings for this skill to function. This is known to be necessary with Claude, and may be necessary with others.

## Available Scripts

All scripts include PEP 723 inline metadata declaring their dependencies. Just run with `uv run` — no manual dependency installation or `--with` flags needed.

### Post to Bluesky (`scripts/post.py`)

Create posts with text, images, or link cards. URLs in the text are automatically detected and made clickable (supports `https://...`, `http://...`, `www....`, and bare domain URLs like `github.com/user/repo`).

```bash
# Simple text post
uv run scripts/post.py --text "Hello, Bluesky!"

# Post with image
uv run scripts/post.py --text "Check this out" --image photo.jpg

# Post with multiple images (up to 4)
uv run scripts/post.py --text "Photos" --image a.jpg --image b.jpg

# Post with image and alt text
uv run scripts/post.py --text "My cat" --image cat.jpg --alt "Orange cat sleeping"

# Post with link card
uv run scripts/post.py --text "Read this" \
    --link-url "https://example.com" \
    --link-title "Article Title" \
    --link-description "Description text"
```

### View Replies (`scripts/replies.py`)

Fetch and display the reply thread for a specific post.

```bash
# View replies using a web URL (most common)
uv run scripts/replies.py https://bsky.app/profile/someone.bsky.social/post/abc123

# View replies using an AT Protocol URI
uv run scripts/replies.py "at://did:plc:xxx/app.bsky.feed.post/abc123"

# Limit reply depth (e.g., only direct replies)
uv run scripts/replies.py --depth 1 https://bsky.app/profile/someone/post/abc123

# Output as JSON for processing
uv run scripts/replies.py --json https://bsky.app/profile/someone/post/abc123

# Skip parent posts, show only target post and its replies
uv run scripts/replies.py --no-parents https://bsky.app/profile/someone/post/abc123
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `post` | Post identifier: either a `bsky.app` URL or an AT Protocol URI (required) |
| `--depth`, `-d` | Maximum depth of replies to fetch (default: no limit) |
| `--json`, `-j` | Output as JSON instead of human-readable format |
| `--no-parents` | Don't show parent posts (only target post and replies) |

### Post a Reply (`scripts/reply.py`)

Reply to an existing Bluesky post. The script automatically handles AT Protocol threading (root and parent references). URLs in the reply text are automatically detected and made clickable.

```bash
# Reply to a post using its web URL
uv run scripts/reply.py --to https://bsky.app/profile/someone.bsky.social/post/abc123 \
    --text "Great post!"

# Reply using an AT Protocol URI
uv run scripts/reply.py --to "at://did:plc:xxx/app.bsky.feed.post/abc123" \
    --text "I agree with this!"

# Short form arguments
uv run scripts/reply.py -p https://bsky.app/profile/someone/post/abc123 -t "Thanks!"
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `--to`, `-p` | Post to reply to: either a `bsky.app` URL or an AT Protocol URI (required) |
| `--text`, `-t` | The reply text content, max 300 characters (required) |

**How it works:** The script fetches the target post's thread to determine:
1. The **parent** (the post you're replying to)
2. The **root** (the original post that started the thread)

Both references are required by AT Protocol to maintain proper thread structure.

### Read Timeline (`scripts/read_timeline.py`)

View posts from accounts the user follows.

```bash
# Default (25 posts)
uv run scripts/read_timeline.py

# More posts
uv run scripts/read_timeline.py --limit 50

# JSON output
uv run scripts/read_timeline.py --json

# Paginate
uv run scripts/read_timeline.py --cursor "cursor_string"
```

### Search Posts (`scripts/search.py`)

Find posts by keywords or hashtags.

```bash
# Keyword search
uv run scripts/search.py "python programming"

# Hashtag search
uv run scripts/search.py "#machinelearning"

# More results with auto-pagination
uv run scripts/search.py "topic" --limit 100 --all

# JSON output
uv run scripts/search.py "query" --json
```

### View Profiles (`scripts/profile.py`)

View profile information for any user.

```bash
# The user's profile
uv run scripts/profile.py

# Another user
uv run scripts/profile.py someone.bsky.social

# JSON output
uv run scripts/profile.py --json
```

### Follow/Unfollow (`scripts/follow.py`)

Manage the user's social connections.

```bash
# Follow a user
uv run scripts/follow.py someone.bsky.social

# Unfollow a user
uv run scripts/follow.py --unfollow someone.bsky.social

# List who the user follows
uv run scripts/follow.py --list

# List the user's followers
uv run scripts/follow.py --list --followers

# List another user's follows
uv run scripts/follow.py --list someone.bsky.social
```

### Notifications (`scripts/notifications.py`)

View and manage the user's notifications.

```bash
# View notifications
uv run scripts/notifications.py

# More notifications
uv run scripts/notifications.py --limit 50

# Just show unread count
uv run scripts/notifications.py --count

# Mark all as read
uv run scripts/notifications.py --mark-read

# JSON output
uv run scripts/notifications.py --json
```

## Common Patterns

### Setting Credentials

```bash
# Set for current session
export BLUESKY_HANDLE="username.bsky.social"
export BLUESKY_PASSWORD="app-password"

# Or inline with command
BLUESKY_HANDLE="username.bsky.social" BLUESKY_PASSWORD="pass" uv run scripts/post.py --text "Hello"
```

### JSON Output for Processing

All scripts support `--json` for machine-readable output:

```bash
# Get timeline as JSON and extract first post
uv run scripts/read_timeline.py --json | jq '.posts[0]'

# Search and count results
uv run scripts/search.py "topic" --json | jq '.count'
```

### Pagination

Scripts that return lists support cursor-based pagination. Use this to scroll through the user's
timeline and other sequences of posts:

```bash
# First page
uv run scripts/read_timeline.py --json > page1.json

# Get cursor from response, then fetch next page
CURSOR=$(jq -r '.cursor' page1.json)
uv run scripts/read_timeline.py --cursor "$CURSOR" --json > page2.json
```

## Key Concepts

- **Handle**: The user's username (e.g., `user.bsky.social`)
- **DID**: Decentralized Identifier—permanent unique ID (handles can change, DIDs don't)
- **URI**: Resource identifier for posts/records (format: `at://did/collection/rkey`)
- **CID**: Content hash identifier for specific versions of records
- **App Password**: Revocable credential for API access (recommended over main password)

## Error Handling

Scripts exit with non-zero status on errors. Common issues:
- Missing credentials: Set `BLUESKY_HANDLE` and `BLUESKY_PASSWORD`
- Invalid handle: Verify the handle exists on Bluesky
- Rate limits: The API has rate limits; space out bulk operations
- Image format: Only JPEG, PNG, and WebP are supported
- Network blocked: Ensure required domains are whitelisted (see [Network Access](#network-access))
