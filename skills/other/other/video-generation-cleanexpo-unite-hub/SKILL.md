---
name: video-generation-skill
description: Design video concepts, scripts, shotlists, transitions, and editing notes for VEO, Gemini, and Nano Banana-based pipelines. Use when turning a marketing idea into concrete video assets.
allowed-tools: Read, Write
---

# Video Generation Skill

## Purpose
Translate marketing goals and decision moments into concrete video plans that can be executed by external tools (VEO, Gemini, Nano Banana 2, etc.).

## Outputs
Per video:
- Hook (first 3–5 seconds)
- Full script / outline
- Suggested B-roll and overlay text
- Scene-by-scene breakdown
- Transitions and on-screen prompts
- Thumbnail concept and text

## Video Types

### Short-Form (15-60 seconds)
- TikTok
- Instagram Reels
- YouTube Shorts
- Facebook Reels

**Structure:**
1. Hook (0-3s): Pattern interrupt
2. Problem (3-10s): Identify pain
3. Solution (10-45s): Show the fix
4. CTA (45-60s): What to do next

### Long-Form (2-10 minutes)
- YouTube
- LinkedIn Video
- Website embeds

**Structure:**
1. Hook (0-15s)
2. Introduction (15-30s)
3. Main content (30s-8m)
4. Summary (8-9m)
5. CTA (9-10m)

## Platform Guidelines

### YouTube
- Thumbnail: 1280x720, high contrast, max 3 words
- Title: 40-60 chars, keyword-first
- Description: First 150 chars are preview

### TikTok
- Vertical 9:16
- Native captions required
- Trending sounds boost reach

### Instagram
- Square or vertical
- Auto-captions on
- Cross-post to Facebook

### LinkedIn
- Professional tone
- Captions essential (most watch muted)
- Value-first approach

## Usage
- Called by SocialPlaybookAgent or VisualExperienceAgent
- Use routes and components already defined in Synthex for embedding video demos
- Store concepts in `social_assets` table with `asset_type='video'`
