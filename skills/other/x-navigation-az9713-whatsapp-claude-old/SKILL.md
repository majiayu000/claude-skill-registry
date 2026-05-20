---
name: x-navigation
description: Navigate X (Twitter) to browse, search, and interact with content
allowed-tools:
  - mcp__claude-in-chrome__*
  - Read
  - Write
---

# X Navigation Skill

Navigate and interact with X (Twitter) using browser automation.

## Prerequisites

- Chrome extension connected (`/chrome` command)
- Logged into X in the browser

## Core Navigation Patterns

### 1. Go to X Homepage

```
1. Use mcp__claude-in-chrome__navigate to go to https://x.com
2. Wait for page to load (use mcp__claude-in-chrome__computer with action: "wait")
3. Take screenshot to verify page loaded
```

### 2. Search for Content

```
1. Navigate to https://x.com/search
2. Use mcp__claude-in-chrome__find to locate the search input
3. Use mcp__claude-in-chrome__form_input to enter search query
4. Press Enter to submit search
5. Wait for results to load
```

### 3. Go to User Profile

```
1. Navigate to https://x.com/{username}
2. Wait for profile to load
3. Verify profile loaded by checking for user's name/handle
```

### 4. Scroll Through Feed

```
1. Use mcp__claude-in-chrome__computer with action: "scroll" and scroll_direction: "down"
2. Take screenshot after scrolling
3. Repeat as needed to gather more content
```

### 5. Click on a Tweet

```
1. Use mcp__claude-in-chrome__find to locate the tweet
2. Click on the tweet to open detail view
3. Wait for replies and engagement data to load
```

## Reading Page Content

### Extract Tweet Text

```
1. Use mcp__claude-in-chrome__read_page to get page accessibility tree
2. Look for article elements containing tweet content
3. Extract text, author, timestamp, and engagement metrics
```

### Extract Profile Information

```
1. Navigate to profile page
2. Use mcp__claude-in-chrome__read_page
3. Extract: name, handle, bio, follower/following counts, pinned tweet
```

## Common Selectors and Patterns

| Element | Find Query |
|---------|------------|
| Search box | "search input" or "search bar" |
| Tweet compose | "compose tweet button" or "What's happening" |
| Like button | "like button" |
| Retweet button | "retweet button" |
| Reply button | "reply button" |
| Follow button | "follow button" |

## Error Handling

- If page doesn't load, wait 2-3 seconds and retry
- If element not found, try scrolling to reveal it
- If login required, inform user to log in manually
- If rate limited, wait and retry or inform user

## Best Practices

1. Always take screenshots to verify actions
2. Wait after navigation for dynamic content to load
3. Scroll slowly to allow content to render
4. Extract data incrementally to avoid missing content
5. Respect rate limits and avoid rapid repeated actions
