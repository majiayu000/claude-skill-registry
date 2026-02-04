---
name: x-posting
description: Compose and publish posts on X (Twitter) with validation
allowed-tools:
  - mcp__claude-in-chrome__*
  - Read
  - Write
---

# X Posting Skill

Compose, validate, and publish posts on X (Twitter).

## Prerequisites

- Chrome extension connected
- Logged into X with posting permissions
- User has explicitly requested posting

## Character Limits

| Content Type | Limit |
|--------------|-------|
| Regular post | 280 characters |
| X Premium | 25,000 characters |
| Reply | 280 characters |
| Quote tweet | 280 characters (+ quoted tweet) |

## Posting Workflows

### 1. Create New Post

```
Steps:
1. Navigate to https://x.com/compose/post or click compose button
2. Use find to locate the compose text area
3. Use form_input to enter the post content
4. Verify character count is within limit
5. Take screenshot for user confirmation
6. If user confirms, click "Post" button
7. Wait for confirmation and capture post URL
```

### 2. Reply to a Tweet

```
Steps:
1. Navigate to the tweet URL
2. Click the reply button
3. Enter reply text in compose area
4. Verify character count
5. Take screenshot for confirmation
6. Click "Reply" to post
```

### 3. Quote Tweet

```
Steps:
1. Navigate to the tweet URL
2. Click retweet button
3. Select "Quote"
4. Enter comment in compose area
5. Verify total character count
6. Take screenshot for confirmation
7. Click "Post" to publish
```

### 4. Create Thread

```
Steps:
1. Start with first tweet in compose
2. Click "+" to add next tweet in thread
3. Repeat for each tweet in thread
4. Take screenshot of full thread preview
5. Click "Post all" to publish thread
```

## Content Validation

### Pre-Post Checklist

```
[ ] Character count within limit
[ ] No broken links (if links included)
[ ] Media attached correctly (if applicable)
[ ] Mentions are correct (@username format)
[ ] Hashtags are relevant and not excessive (max 2-3)
[ ] No sensitive content violations
[ ] Tone matches user's brand/style
```

## Confirmation Flow

**IMPORTANT**: Always confirm with user before posting.

```
1. Compose the post
2. Take screenshot
3. Show user: "Ready to post this? [screenshot]"
4. Wait for explicit "yes" or "post it" confirmation
5. Only then click the Post button
6. Capture and share the posted tweet URL
```

## Best Practices

### Writing Effective Posts

1. **Hook first**: Lead with the most interesting point
2. **Be concise**: Every word should add value
3. **Use threads for long content**: Break into digestible chunks
4. **Add context**: Don't assume readers know the topic
5. **Include CTA**: Ask questions, invite replies

### What to Avoid

- Excessive hashtags (more than 3)
- All caps (reads as shouting)
- Broken links
- Posting too frequently (spam behavior)
- Controversial content without context

## Error Handling

| Error | Solution |
|-------|----------|
| "Something went wrong" | Wait 30 seconds, retry |
| "Over character limit" | Shorten content |
| "Duplicate post" | Modify content slightly |
| "Rate limited" | Wait 15-30 minutes |
| "Account suspended" | Contact X support |
