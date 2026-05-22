---
name: social-playbook-skill
description: Design and generate complete social media playbooks (scripts, visuals, captions, hooks, thumbnails, transitions) for Synthex clients across YouTube, TikTok, Instagram, Facebook, LinkedIn, and Shorts/Reels. Use when planning multi-platform campaigns or content systems.
allowed-tools: Read, Write, Search
---

# Social Playbook Skill

## Purpose
Create fully structured, implementation-ready social media playbooks that Synthex can execute autonomously for each client, including video ideas, scripts, thumbnails, captions, posting cadence, and visual styles.

## Data & Files to Use
- Database tables (once created):
  - `social_playbooks`
  - `social_assets`
- Visual & animation modules:
  - `src/lib/visual/animations/*`
  - `src/components/visual/*`
- Any existing marketing/offer docs in `docs/marketing/` and `docs/offers/`.

## What This Skill Should Produce
For each playbook:
1. **Campaign Overview**
   - Goal (lead gen, authority, launch, nurture)
   - Primary persona (trade, agency, consultant, etc.)
   - Platforms (YouTube, TikTok, IG, LinkedIn, Facebook)

2. **Video & Post Concepts**
   - 10–30 ideas with:
     - Title
     - 3–5 second hook
     - 30–180 second script outline
     - Suggested B-roll or screen capture ideas
     - Thumbnail concept + text overlay

3. **Platform-Specific Mappings**
   - How each idea becomes:
     - YT long
     - YT Short
     - TikTok
     - IG Reel + carousel
     - LinkedIn post

4. **Scheduling & Cadence**
   - Weekly posting map
   - Recommended time windows

5. **Storage Format**
   - Structured for DB insertion into `social_playbooks` and `social_assets`.

## When to Use
- New client onboarding
- Launching a new feature or product
- Creating a content library for agencies/trades with no visual ideas

## Constraints & Quality
- No-fluff, results-driven content
- Match the brand tone (practical, straight-talking, no hype)
- Prioritize trades, agencies, and real small businesses
