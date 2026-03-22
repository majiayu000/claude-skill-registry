---
name: SRT Social Summary
description: This skill should be used when the user asks to "generate social media summary from srt", "create platform-specific descriptions", "generate Facebook post from transcript", "create YouTube description from srt", "write Thread post from subtitles", "生成影片介紹", "根據逐字稿生成貼文", or needs to create engaging social media content from SRT subtitle files for Facebook, Thread, or YouTube platforms.
version: 0.1.0
---

# SRT Social Summary Generator

Generate compelling social media summaries from SRT subtitle files, optimized for different platform characteristics to maximize engagement and reach.

## Purpose

This skill analyzes SRT transcript files and generates platform-specific summaries that:
- Capture the core message and key insights
- Match platform-specific best practices (tone, length, format)
- Create emotional resonance with target audiences
- Highlight the value proposition clearly
- Include strategic hashtags for discoverability

## When to Use

Use this skill when:
- Converting video transcripts into social media posts
- Promoting video content across multiple platforms
- Creating platform-optimized descriptions for the same content
- Need to extract key points from lengthy transcripts
- Want to maximize engagement through platform-specific formatting

## Platform Characteristics

### Facebook
- **Tone**: Conversational, community-focused, relatable
- **Length**: 100-250 characters for high engagement (can go longer for storytelling)
- **Format**: Hook in first line, value proposition, call-to-action
- **Hashtags**: 2-3 relevant hashtags (not overused)
- **Goal**: Spark conversation, encourage shares and comments

### Thread (Twitter-like)
- **Tone**: Concise, punchy, thought-provoking
- **Length**: 280 characters max per post (can use thread format for longer content)
- **Format**: Strong hook, key insight, intrigue/question
- **Hashtags**: 1-2 highly relevant hashtags
- **Goal**: Quick attention grab, encourage retweets and replies

### YouTube
- **Tone**: Informative, SEO-friendly, comprehensive
- **Length**: 150-300 words (first 2-3 lines are critical)
- **Format**: Hook + detailed value breakdown + timestamps (if applicable) + CTA
- **Hashtags**: 3-5 strategic hashtags for search
- **Goal**: Improve searchability, set viewer expectations, encourage watch time

## Usage Workflow

### Step 1: Analyze the SRT Content

Read the SRT file to understand:
- Main topic and core message
- Key insights or takeaways (3-5 points)
- Emotional tone (educational, inspirational, entertaining, etc.)
- Target audience signals
- Unique value propositions

Extract the essence without getting lost in filler words or repetition common in spoken content.

### Step 2: Identify Platform Requirements

Ask the user which platform(s) they need:
- Facebook only
- Thread only
- YouTube only
- All three platforms

If not specified, generate for all three platforms by default.

### Step 3: Generate Platform-Specific Summaries

For each platform, create content following these principles:

#### Facebook Summary Structure
```
[Hook - 1 compelling sentence that stops scrolling]

[Value Proposition - What will the audience learn/gain?]

[Key Insights - 2-3 bullet points or short sentences]

[Call-to-Action - Encourage engagement]

#Hashtag1 #Hashtag2 #Hashtag3
```

#### Thread Summary Structure
```
[Punchy Hook - Maximum impact in minimum words]

[Core Insight - The "aha" moment]

[Intrigue/Question - Make them want to watch]

#Hashtag1 #Hashtag2
```

#### YouTube Summary Structure
```
[Strong Hook - First 2 lines appear in search results]

[Detailed Overview - What this video covers]

[Key Topics/Timestamps - If applicable]
🎯 Topic 1
🎯 Topic 2
🎯 Topic 3

[Value Statement - Why watch this]

[Call-to-Action - Like, subscribe, comment]

#Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4 #Hashtag5
```

### Step 4: Craft Strategic Hashtags

Select hashtags based on:
- **Relevance**: Directly related to content
- **Search Volume**: Balance popular and niche tags
- **Competition**: Mix high-traffic and specific tags
- **Trending**: Include timely topics when relevant
- **Branding**: Include brand/creator tags if applicable

Avoid:
- Generic hashtags (#love, #instagood)
- Overused hashtags that drown content
- Irrelevant trending tags
- Too many hashtags (looks spammy)

### Step 5: Output Format

Generate output in this format:

```markdown
# 社群平台摘要

## Facebook
[Facebook content]

---

## Thread
[Thread content]

---

## YouTube
[YouTube content]

---

## 分析說明
- **核心主題**: [Main topic]
- **目標受眾**: [Target audience]
- **情感基調**: [Emotional tone]
- **關鍵賣點**: [Key value propositions]
```

Save the output as `summary.md` in the same directory as the source SRT file.

## Best Practices

### Content Analysis
- Focus on transformation/outcome, not just information
- Identify the "so what?" factor - why should audience care?
- Look for quotable moments or surprising insights
- Consider the audience's pain points and desires

### Writing Hooks
- Use numbers ("3 ways to...", "5 secrets...")
- Ask provocative questions
- Make bold statements
- Create curiosity gaps
- Use power words (discover, revealed, proven, secret)

### Emotional Resonance
- Tap into aspirations (what they want to become)
- Address frustrations (what they want to avoid)
- Create relatability (shared experiences)
- Inspire action (achievable next steps)

### Platform Optimization
- **Facebook**: Prioritize shareability and discussion
- **Thread**: Maximize retweet potential with quotability
- **YouTube**: Optimize for search and watch time

### Hashtag Strategy
- Research platform-specific trending tags
- Use a mix of broad and specific tags
- Include branded hashtags for tracking
- Test and iterate based on performance

## Common Patterns

### Educational Content
- Hook: "Most people don't know..."
- Value: "Learn the [X] framework for [outcome]"
- CTA: "Which tip will you try first?"

### Inspirational Content
- Hook: "What if I told you..."
- Value: "Discover how [person/method] achieved [result]"
- CTA: "Tag someone who needs to hear this"

### Entertainment Content
- Hook: "[Surprising fact or statistic]"
- Value: "Watch as we [interesting activity]"
- CTA: "Drop a 🔥 if you agree"

### Tutorial Content
- Hook: "Stop doing [common mistake]"
- Value: "Here's the right way to [achieve goal]"
- CTA: "Save this for later"

## Additional Resources

### Reference Files

For detailed platform specifications and advanced techniques:
- **`references/platform-specs.md`** - Detailed platform requirements, character limits, and algorithm insights
- **`references/hook-formulas.md`** - Proven hook templates and copywriting formulas
- **`references/hashtag-research.md`** - Hashtag research methodology and tools

## Quality Checklist

Before finalizing summaries:
- [ ] Hook grabs attention in first 5 words
- [ ] Value proposition is crystal clear
- [ ] Content matches platform tone and length
- [ ] Hashtags are relevant and strategic
- [ ] Call-to-action is specific and compelling
- [ ] No jargon or unclear terms
- [ ] Emotional resonance is present
- [ ] Unique angle or insight is highlighted
- [ ] Grammar and formatting are polished

## Example Usage

**User**: "根據這個 SRT 生成影片介紹"

**Process**:
1. Read and analyze the SRT file
2. Extract core message and key insights
3. Identify target audience and tone
4. Generate platform-specific summaries
5. Select strategic hashtags
6. Output formatted markdown file

The result will be engaging, platform-optimized content that drives views and engagement.
