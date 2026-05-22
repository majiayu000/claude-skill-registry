---
name: social-media-generator
description: This skill should be used when the user requests social media content creation for Twitter, Instagram, LinkedIn, or Facebook. It generates platform-optimized posts and saves them in an organized folder structure with meaningful filenames based on event details.
---

# Social Media Generator

## Overview

This skill enables creation of platform-optimized social media content for Twitter, Instagram, LinkedIn, and Facebook. It automatically generates posts tailored to each platform's best practices and saves them in an organized directory structure.

## When to Use This Skill

Use this skill when the user requests:
- Creation of social media posts for multiple platforms
- Content generation for specific events, announcements, or campaigns
- Platform-specific content optimization
- Organized storage of social media content

## Core Workflow

### Step 1: Gather Information

Collect the following details from the user (ask if not provided):
- Event/content name
- Date and time (format: DD-MM-YYYY-HHMM)
- Main message or announcement
- Target audience
- Key details to include
- Call-to-action
- Any specific hashtags or mentions
- Brand voice/tone preferences

### Step 2: Generate Platform-Specific Content

Create content for each platform using the templates in `assets/`:

**Twitter** (`assets/twitter_template.md`)
- Keep under 280 characters
- Concise and punchy
- 1-3 relevant hashtags
- Clear call-to-action
- Consider emojis for engagement

**Instagram** (`assets/instagram_template.md`)
- Engaging caption with hook in first line
- More detailed description
- 5-15 relevant hashtags
- Visual-focused messaging
- Line breaks for readability
- Encourage engagement

**LinkedIn** (`assets/linkedin_template.md`)
- Professional and informative tone
- Value-driven content
- Industry insights or takeaways
- 3-5 professional hashtags
- Bullet points for key information
- Discussion-prompting questions

**Facebook** (`assets/facebook_template.md`)
- Conversational and engaging
- Keep concise (under 250 chars for best engagement)
- 2-3 relevant hashtags
- Visual-focused
- Encourage comments and shares
- Include event details if applicable

### Step 3: Create Organized File Structure

Create the following directory structure in the project:

```
social-media/
├── twitter/
│   └── event-name-DD-MM-YYYY-HHMM.md
├── instagram/
│   └── event-name-DD-MM-YYYY-HHMM.md
├── linkedin/
│   └── event-name-DD-MM-YYYY-HHMM.md
└── facebook/
    └── event-name-DD-MM-YYYY-HHMM.md
```

**Filename Format:** `event-name-DD-MM-YYYY-HHMM.md`
- Use lowercase with hyphens for spaces
- Include date in format: day-month-year-time
- Example: `product-launch-15-03-2025-1400.md`

### Step 4: Write Content to Files

For each platform:
1. Generate platform-optimized content based on the templates
2. Create the platform-specific subdirectory if it doesn't exist
3. Write the content to the appropriately named markdown file
4. Include metadata at the bottom (platform, date, character count)

### Step 5: Review and Confirm

After generating all posts:
1. Provide a summary of created files
2. Highlight key points for each platform
3. Note any character count warnings
4. Offer to make revisions if needed

## Content Optimization Guidelines

### Character Limits
- Twitter: 280 characters
- Instagram: 2,200 characters (but concise is better)
- LinkedIn: 3,000 characters
- Facebook: Unlimited (but under 250 for best engagement)

### Hashtag Strategy
- Twitter: 1-3 focused hashtags
- Instagram: 5-15 relevant hashtags
- LinkedIn: 3-5 professional hashtags
- Facebook: 2-3 hashtags

### Tone Adaptation
- Twitter: Casual, conversational, timely
- Instagram: Visual-first, engaging, lifestyle-focused
- LinkedIn: Professional, insightful, value-driven
- Facebook: Friendly, community-focused, conversational

### Call-to-Action Best Practices
- Make it clear and specific
- Use action verbs
- Create urgency when appropriate
- Match platform conventions

## Example Usage

**User Request:**
"Create social media posts for our product launch event on March 15, 2025 at 2 PM. The product is an AI-powered productivity tool called TaskFlow."

**Execution:**
1. Gather additional details (key features, target audience, website link)
2. Generate four platform-specific posts
3. Create directory structure: `social-media/twitter/`, `social-media/instagram/`, etc.
4. Write files: `taskflow-launch-15-03-2025-1400.md` in each platform folder
5. Provide summary with file locations and key points

## Assets

This skill includes template files in the `assets/` directory:
- `twitter_template.md` - Twitter post structure and best practices
- `instagram_template.md` - Instagram caption format and guidelines
- `linkedin_template.md` - LinkedIn post structure and professional tone guide
- `facebook_template.md` - Facebook post format and engagement tips

These templates serve as reference for platform-specific requirements and best practices when generating content.
