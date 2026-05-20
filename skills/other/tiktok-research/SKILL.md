---
name: tiktok-research
description: |
  Research high-performing TikTok videos from tracked accounts using Apify's TikTok Scraper.
  Identifies outlier content, analyzes top 5 videos with AI, and generates reports with actionable hook formulas.

  Use when asked to:
  - Find trending TikTok content in a niche
  - Research what's performing on TikTok
  - Identify high-performing video patterns
  - Analyze competitors' TikTok content
  - Generate content ideas from TikTok trends
  - Run TikTok research
  - Find viral TikToks
  - Analyze hooks and content structure

  Triggers: "tiktok research", "tt research", "find trending tiktoks", "analyze tiktok accounts",
  "what's working on tiktok", "content research tiktok", "tiktok analysis", "tiktok trends"
---

# TikTok Research

Research high-performing TikTok videos, identify outliers, and analyze top video content for hooks and structure.

## Prerequisites

- `APIFY_TOKEN` environment variable or in `.env`
- `apify-client` Python package
- Accounts configured in `.claude/context/tiktok-accounts.md`

Verify setup:
```bash
python3 -c "
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from apify_client import ApifyClient
assert os.environ.get('APIFY_TOKEN'), 'APIFY_TOKEN not set'
" && echo "Prerequisites OK"
```

## Workflow

### 1. Create Run Folder

```bash
RUN_FOLDER="tiktok-research/$(date +%Y-%m-%d_%H%M%S)" && mkdir -p "$RUN_FOLDER" && echo "$RUN_FOLDER"
```

### 2. Fetch Content

```bash
python3 .claude/skills/tiktok-research/scripts/fetch_tiktok.py \
  --days 30 \
  --limit 50 \
  --sorting latest \
  --output {RUN_FOLDER}/raw.json
```

Parameters:
- `--days`: Days back to search (default: 30)
- `--limit`: Max videos per account (default: 50)
- `--sorting`: "latest", "popular", or "oldest" (default: latest)
- `--usernames`: Override accounts file with specific usernames

### 3. Identify Outliers

```bash
python3 .claude/skills/tiktok-research/scripts/analyze_posts.py \
  --input {RUN_FOLDER}/raw.json \
  --output {RUN_FOLDER}/outliers.json \
  --threshold 2.0
```

Output JSON contains:
- `total_videos`: Number of videos analyzed
- `outlier_count`: Number of outliers found
- `topics`: Top hashtags, sounds, and keywords
- `accounts`: List of accounts analyzed
- `outliers`: Array of outlier videos with engagement metrics

### 4. Analyze Top Videos with AI

Read `{RUN_FOLDER}/outliers.json` and analyze the top 5 videos directly.

For each video, extract:
- Hook technique and replicable formula (opening line, why it works)
- Content structure (intro / body / CTA sections)
- Retention techniques
- CTA strategy

Use `OPENAI_API_KEY` if you want to run a script-based analysis. Otherwise Claude Code itself reads the JSON and performs the analysis inline.

### 5. Generate Report

Read `{RUN_FOLDER}/outliers.json` and `{RUN_FOLDER}/video-analysis.json`, then generate `{RUN_FOLDER}/report.md`.

**Report Structure:**

```markdown
# TikTok Research Report

Generated: {date}

## Top Performing Hooks

Ranked by engagement. Use these formulas for your content.

### Hook 1: {technique} - @{username}
- **Opening**: "{opening_line}"
- **Why it works**: {attention_grab}
- **Replicable Formula**: {replicable_formula}
- **Engagement**: {diggCount} likes, {commentCount} comments, {playCount} views
- [Watch Video]({webVideoUrl})

[Repeat for each analyzed video]

## Content Structure Patterns

| Video | Format | Pacing | Key Retention Techniques |
|-------|--------|--------|--------------------------|
| @username | {format} | {pacing} | {techniques} |

## CTA Strategies

| Video | CTA Type | CTA Text | Placement |
|-------|----------|----------|-----------|
| @username | {type} | "{cta_text}" | {placement} |

## All Outliers

| Rank | Username | Likes | Comments | Shares | Views | Engagement Rate |
|------|----------|-------|----------|--------|-------|-----------------|
[List all outliers with metrics and links]

## Trending Topics

### Top Hashtags
[From outliers.json topics.hashtags]

### Top Sounds
[From outliers.json topics.sounds]

### Top Keywords
[From outliers.json topics.keywords]

## Actionable Takeaways

[Synthesize patterns into 4-6 specific recommendations]

## Accounts Analyzed
[List accounts]
```

Focus on actionable insights. The "Top Performing Hooks" section with replicable formulas should be prominent.

## Quick Reference

Full pipeline:
```bash
RUN_FOLDER="tiktok-research/$(date +%Y-%m-%d_%H%M%S)" && mkdir -p "$RUN_FOLDER" && \
python3 .claude/skills/tiktok-research/scripts/fetch_tiktok.py -o "$RUN_FOLDER/raw.json" && \
python3 .claude/skills/tiktok-research/scripts/analyze_posts.py -i "$RUN_FOLDER/raw.json" -o "$RUN_FOLDER/outliers.json"
```

Then read `$RUN_FOLDER/outliers.json`, analyze top 5 videos inline (Step 4), and generate the report.

## Engagement Metrics

**Engagement Score**: `likes + (3 x comments) + (2 x shares) + (2 x saves) + (0.05 x views)`

**Outlier Detection**: Videos with engagement rate > mean + (threshold x std_dev)

**Engagement Rate**: (score / followers) x 100

## TikTok-Specific Fields

- `diggCount`: Likes/hearts
- `shareCount`: Shares
- `playCount`: Video views
- `commentCount`: Comments
- `collectCount`: Saves/bookmarks
- `authorFollowers`: Creator's follower count
- `musicName`: Sound used in video
- `musicOriginal`: Whether sound is original
