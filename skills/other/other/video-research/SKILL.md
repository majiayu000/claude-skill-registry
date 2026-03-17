---
name: video-research
description: Research topics and gather content for video production
allowed-tools:
  - mcp__claude-in-chrome__*
  - WebSearch
  - WebFetch
  - Read
  - Write
  - Bash
---

# Video Research Skill

Research and gather content for video production.

## Research Workflow

```
Topic → Source Discovery → Content Gathering → Asset Collection → Script Outline
```

## Step 1: Source Discovery

### Find Primary Sources

```
1. WebSearch for the topic + recent news
2. Look for official announcements, blog posts, demos
3. Find social media discussions (X, Reddit, HN)
4. Identify key people/accounts talking about topic
```

### Source Types to Look For

| Source Type | Value | Example |
|-------------|-------|---------|
| Official announcement | Primary facts | Company blog post |
| Demo video | Visual content | YouTube demo |
| Expert commentary | Analysis/opinion | Industry analyst tweet |
| Community discussion | Reactions/context | Reddit/HN threads |
| Documentation | Technical details | GitHub README |

## Step 2: Content Gathering

### For Each Source, Extract:

```markdown
## Source: {Title}
URL: {url}
Type: {announcement/demo/commentary/discussion}

### Key Facts
- Fact 1
- Fact 2
- Fact 3

### Notable Quotes
> "Quote that could be used in video"

### Visual Assets
- Screenshot 1: {description} [timestamp if video]
- Screenshot 2: {description}

### Related Links
- Link 1
- Link 2
```

## Step 3: Asset Collection

### Download Video Clips

```bash
# Download specific portion of YouTube video
yt-dlp --download-sections "*0:30-1:00" \
  -o "assets/downloads/clip_%(title)s.%(ext)s" \
  "{VIDEO_URL}"

# Download full video for later editing
yt-dlp -f "bestvideo[height<=1080]+bestaudio" \
  -o "assets/downloads/%(title)s.%(ext)s" \
  "{VIDEO_URL}"
```

### Capture Screenshots

```
1. Use mcp__claude-in-chrome__computer with action: "screenshot"
2. Save to assets/downloads/screenshot_{topic}_{n}.png
3. Note what each screenshot shows for later reference
```

## Step 4: Research Output Template

```markdown
# Video Research: {Topic}

## Overview
{1-2 sentence summary of the topic}

## Story Arc
1. Hook: {what grabs attention}
2. Context: {background viewers need}
3. Main content: {the meat of the story}
4. Implications: {why it matters}
5. Call to action: {what viewers should do}

## Key Facts
1. {Most important fact}
2. {Second most important}
3. {Third}

## Sources
| Source | Type | URL | Key Content |
|--------|------|-----|-------------|
| {name} | {type} | {url} | {what it provides} |

## Visual Assets Collected
| File | Description | Suggested Use |
|------|-------------|---------------|
| clip1.mp4 | Demo footage | Main section |
| screenshot1.png | UI screenshot | Explanation |

## Suggested Script Outline
### Intro (0:00-0:15)
{hook and topic introduction}

### Section 1 (0:15-0:45)
{first main point}

### Section 2 (0:45-1:15)
{second main point}

### Outro (1:15-1:30)
{conclusion and CTA}
```

## Research Best Practices

1. **Start broad, then narrow**: Get overview before diving deep
2. **Verify facts**: Cross-reference important claims
3. **Note sources**: Always track where info came from
4. **Capture context**: Understand why something matters
5. **Think visually**: Note what will look good on video
6. **Consider audience**: What do they already know?
