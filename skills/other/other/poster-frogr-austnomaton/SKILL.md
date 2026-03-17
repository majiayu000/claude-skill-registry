---
name: poster
description: Post content to X and Moltbook
user_invocable: true
---

# Poster Skill

## Purpose
Publish content to social platforms:
- Moltbook posts
- X/Twitter posts and threads
- Cross-platform publishing

## Invocation
```
/poster [platform] [content] [options]
```

### Arguments
- `platform`: moltbook, x, or all
- `content` (optional): Content to post (or will be prompted)
- `--thread`: Create a thread instead of single post
- `--schedule [time]`: Schedule for later
- `--draft`: Save as draft without posting

### Examples
```
/poster moltbook "Just shipped a new feature"
/poster x --thread                    # Start thread workflow
/poster all "Cross-platform post"     # Post everywhere
```

## Platforms

### Moltbook
- API Key required (in .env)
- Supports longer posts
- Markdown formatting
- Community engagement

### X/Twitter
- OAuth credentials required (in .env)
- 280 character limit
- Thread support
- Media attachments

## Workflow

1. **Prepare** content (validate length, format)
2. **Check** against content-log.md (no duplicates)
3. **Load** appropriate personality (poster.md)
4. **Review** content for quality
5. **Post** to specified platform(s)
6. **Log** to content-log.md
7. **Notify** if configured
8. **Update** metrics

## Content Guidelines

### Loaded from `personality/poster.md`:
- Poaster energy but not mean
- Funny observations
- Hot takes that are good
- Lowercase acceptable
- Emoji sparingly

### Quality Checks
- [ ] Not too similar to recent posts
- [ ] Appropriate for platform
- [ ] Aligns with personality
- [ ] Not cringe
- [ ] Adds value

## API Integration

### Moltbook API
```python
# POST to Moltbook
import requests
import os

response = requests.post(
    "https://api.moltbook.com/v1/posts",
    headers={"Authorization": f"Bearer {os.environ['MOLTBOOK_API_KEY']}"},
    json={"content": content}
)
```

### X API
```python
# Uses tweepy or similar library
# Requires OAuth 1.0a authentication
# See X Developer docs for details
```

## Logging

Every post logged to `memory/content-log.md`:
```markdown
### [DATE] [PLATFORM] post
**Content**: The actual content
**Link**: https://moltbook.com/post/123
**Performance**: TBD (updated later)
```

## Safety

- Rate limiting enforced
- Duplicate detection
- No auto-posting without review (configurable)
- Follows platform ToS
