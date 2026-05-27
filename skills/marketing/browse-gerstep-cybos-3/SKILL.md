---
name: browse
description: Discover trending topics and content ideas from social feeds for post creation. Use when scanning Twitter timeline or finding content inspiration.
---

# Browse Skill

Discover trending topics and content ideas from social feeds for post creation.

## Capabilities

- **Twitter Feed Scan**: Browse home timeline for high-engagement topics
- **Topic Discovery**: Identify trends relevant to cyber.Fund's focus areas
- **Content Ideas**: Generate post angles from discovered topics

## Workflows

- `workflows/twitter-feed.md`: **PRIMARY** - Scan Twitter timeline for topics

## Tools Used

- `mcp__claude-in-chrome__*`: Browser automation for Twitter access
- `mcp__claude-in-chrome__navigate`: Navigate to feeds
- `mcp__claude-in-chrome__read_page`: Extract feed content
- `mcp__claude-in-chrome__computer`: Scroll, screenshot, interact

## Output Format

Returns structured topic list with:
- Topic title and summary
- Engagement signals (likes, views, retweets)
- Suggested angle for your voice
- Key sources/accounts

## Topic Filters

Focus on content relevant to:
1. AI/ML infrastructure and tools
2. Crypto/Web3 developments
3. Robotics and automation
4. VC/investment patterns
5. Futurism and tech predictions

## Usage

```
/cyber-browse twitter        # Scan Twitter home timeline
/cyber-browse twitter --save # Scan and save topics to file
```

## Output Location

- Topics: `~/CybosVault/private/content/ideas/MMDD-browse-YY.md`

## Integration with Content

Browse output feeds directly into:
- `/cyber-tweet` - Pick topic and generate post
- `/cyber-essay` - Expand topic into long-form
- Research workflows - Deep dive on discovered topic
