---
name: technical-writing
description: Writes technical blog posts about features being built. Triggers when user asks to write about development progress, implementations, or project updates.
---

# Technical Writing Skill

## Overview

Create technical blog posts about features you're building. This skill analyzes your codebase to understand implementations, then structures clear, engaging content that balances technical detail with readability while avoiding AI-sounding language.

## Process

### Phase 1: Research and Planning

**1.1 Load Writing Guides (REQUIRED - Load First)**

Before any other work, load the following:

1. **Writing Rules** (from `WRITING_ANTI_PATTERNS_PATH` env var, or fall back to `references/anti-patterns.md`) - Comprehensive lists of AI-sounding words, phrases, and patterns to avoid. This is the foundation - what NOT to sound like.

2. **Writing Style Guide** (from `WRITING_STYLE_GUIDE_PATH` env var, or fall back to `references/style-guide.md`) - Personal writing voice, tone, structure, and signature moves. This is the voice layer - what TO sound like.

**PRIORITY RULE**: When guides conflict, anti-patterns win. Avoiding AI patterns always takes precedence over stylistic choices.

**1.2 Fetch WordPress Taxonomy (if configured)**

If `WORDPRESS_URL`, `WORDPRESS_USERNAME`, and `WORDPRESS_APP_PASSWORD` env vars are set, fetch available categories and tags before writing so frontmatter uses existing taxonomy:

```bash
curl -s -u "$WORDPRESS_USERNAME:$WORDPRESS_APP_PASSWORD" \
  "$WORDPRESS_URL/wp-json/wp/v2/categories?per_page=100" | python3 -c "import sys,json; [print(c['name']) for c in json.load(sys.stdin)]"

curl -s -u "$WORDPRESS_USERNAME:$WORDPRESS_APP_PASSWORD" \
  "$WORDPRESS_URL/wp-json/wp/v2/tags?per_page=100" | python3 -c "import sys,json; [print(t['name']) for t in json.load(sys.stdin)]"
```

Use these when choosing `category` and `tags` in frontmatter. Prefer existing values. Skip this step if WordPress env vars are not set.

**1.3 Understand What Was Built**


Investigate the codebase to understand the feature:

- Ask which feature or changes they want to write about
- Use git to check recent commits if relevant (skip if not a git repo): `git log --oneline -10`
- Read relevant code files to understand implementation
- Identify key technical decisions, architecture, and interesting details
- Note any challenges solved or clever solutions

**1.4 Plan the Structure**

Plan what to cover in the post. Use these as a guide, not a rigid template:

- **Opening**: Start with an engaging hook or context for what you built
- **Overview**: Brief explanation of the feature (2-3 sentences)
- **Problem/Value**: Why this matters or what problem it solves
- **Technical Details**: How it works with code snippets
  - Key implementation details
  - Interesting technical decisions
  - Architecture or design patterns used
- **Challenges**: What was tricky and how you solved it (if relevant)
- **Future**: Next steps or related features (if relevant)
- **Tech Stack**: Technologies used (can be woven into the narrative or listed)

The actual headings, structure, and flow should feel natural to the specific post - not formulaic.

### Phase 2: Writing

**2.1 Draft Creation**

Create the blog post applying BOTH guides you loaded in Phase 1. After drafting, re-read the post against the anti-patterns guide and fix any violations before saving.

**Code Snippets:**
- Keep snippets short (5-15 lines)

**Target length**: Match length to complexity. Default short.
- Simple idea, announcement, or single concept: 400-600 words
- Moderate technical walkthrough: 600-900 words
- Deep architectural dive or multi-part explanation: 900-1200 words

Err on the side of shorter. If the post can be said in 500 words, don't stretch it to 800. Cut filler, merge thin sections, and stop when the point is made.

**2.2 Save the Draft**

Save the completed blog post to the drafts directory (create the folder if missing).

**To find the save path**, run: `echo $WRITING_DRAFTS_PATH`
- If the output is non-empty, save there
- If empty, fall back to `.drafts/` in the current project

**File naming convention:**
- Format: `YYYY-MM-DD-slug.md`
- Slugs should be short, memorable, and easy to type — two words max
- Capture the core concept of the post, not necessarily the title
- Think "what would I type after the domain name?"
- Examples: `2025-12-29-ralph.md` (post: "How I Got Ralph to Ship Overnight"), `2026-01-10-listen.md` (post: "Giving my blog a voice"), `2025-11-15-choosing-open.md` (post: "WordPress Almost Didn't Happen" — about choosing open source)

**Frontmatter (REQUIRED):**

Every draft must start with YAML frontmatter containing `title` and `url`:

```yaml
---
title: How I got Ralph to ship overnight
url: /ralph
category: Development
tags:
  - AI
  - Shipping
---
```

- `title` — the post title (do NOT repeat as an H1 in the body). Titles should be short (3-7 words), evocative, and leave room for curiosity. Don't explain the whole post — hint at it. Think newspaper headline, not description.
  - Good: "Giving my blog a voice", "WordPress Almost Didn't Happen", "Planning Out Loud"
  - Bad: "I built a skill that writes blog posts from my codebase" (too long, explains everything)
- `url` — the permalink path, matching the filename slug (e.g. `/ralph`, `/listen`, `/choosing-open`)
- `category` — WordPress category (use an existing one from Phase 1.2 when available)
- `tags` — WordPress tags (prefer existing ones from Phase 1.2)

### Phase 3: Publishing (Optional)

**3.1 WordPress Publishing**

If the user wants to publish to WordPress, load **WordPress Publishing Guide** (`references/wordpress-publishing.md`) for complete setup and publishing instructions.

The guide covers:
- Environment setup and credentials
- Python dependencies installation
- Publishing commands and workflow
- Smart update tracking (no duplicate posts)
- Troubleshooting common issues

Quick summary:
- First time: Creates new WordPress draft
- Subsequent: Updates existing draft (no duplicates)
- Always saves as draft (never auto-publishes)
- Returns post URL and edit URL

## Output Format

After creating and saving the blog post, provide:

1. **Saved Location**: Path where the post was saved
2. **Post Title**: The final title used
3. **Key Files Referenced**: List of files mentioned with line numbers
4. **Word Count**: Approximate length

## Example Interaction

**User**: "Help me write about the voice planning feature"

**Response**:
```
Let me investigate the voice planning implementation to write about it.

[Phase 1: Loads anti-patterns + style guide, fetches WP taxonomy, reads code]

[Phase 2: Creates and saves blog post applying both guides]

Blog post saved to: .drafts/2025-12-29-planning-aloud.md

Title: "Planning Out Loud"

Key Files Referenced:
- src/components/voice-session.tsx:78 (voice session initialization)
- src/app/api/webhook/route.ts:40 (webhook signature validation)
- src/lib/claude.ts:88 (Claude tool calling)

Word Count: ~550 words
```

## Environment Variables

Configure in Claude Code settings (`~/.claude/settings.json`) under the `env` key:

```json
{
  "env": {
    "WRITING_STYLE_GUIDE_PATH": "/path/to/style-guide.md",
    "WRITING_ANTI_PATTERNS_PATH": "/path/to/anti-patterns.md",
    "WRITING_DRAFTS_PATH": "/path/to/drafts",
    "WORDPRESS_URL": "https://yourblog.com",
    "WORDPRESS_USERNAME": "your_username",
    "WORDPRESS_APP_PASSWORD": "xxxx xxxx xxxx xxxx",
    "WRITING_TITLE_CASE_STYLE": "title",
    "WRITING_HEADING_CASE_STYLE": "sentence"
  }
}
```

| Variable | Required | Description |
|----------|----------|-------------|
| `WRITING_STYLE_GUIDE_PATH` | No | Path to shared writing style guide. Loaded in Phase 1.1 |
| `WRITING_ANTI_PATTERNS_PATH` | No | Path to shared anti-patterns. Overrides `references/anti-patterns.md` |
| `WRITING_DRAFTS_PATH` | No | Where to save drafts. Falls back to `.drafts/` in current project |
| `WORDPRESS_URL` | For publishing | WordPress site URL (include `https://`) |
| `WORDPRESS_USERNAME` | For publishing | WordPress account username |
| `WORDPRESS_APP_PASSWORD` | For publishing | Application password (not regular password) |
| `WRITING_TITLE_CASE_STYLE` | No | `"sentence"` (default) or `"title"` |
| `WRITING_HEADING_CASE_STYLE` | No | `"sentence"` (default) or `"title"` |

## Tips for Best Results

1. **Be specific about scope**: "Write about the webhook security implementation" is better than "write about webhooks"
2. **Mention target audience**: "For developers familiar with Next.js" vs "For non-technical readers"
3. **Specify length preference**: "Quick 500-word update" vs "Detailed deep-dive"
4. **Share context**: "This is part 2 in a series" or "First post about this project"
5. **Request revisions**: After the draft, ask to expand sections, simplify explanations, or adjust tone

## Advanced: Series Posts

For multi-part series:
- Start with "Help me outline a 3-part series about [topic]"
- Each post should build on previous ones
- Include "Previously" and "Next up" sections
- Keep consistent structure across posts
