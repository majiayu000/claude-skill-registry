---
name: generate-social-graphic
description: Generate social media graphics using the jocko-imagery MCP server
user-invocable: true
---

You are helping the marketing team generate social media graphics for Jocko Fuel.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+jocko-imagery` to load the jocko-imagery MCP tools. All tools below are prefixed with `mcp__jocko-imagery__` (e.g., `mcp__jocko-imagery__generate_image`).

Follow these steps:

### Step 1: Define the Content

Ask the user for:
- **Platform** — Instagram (feed/story/reel cover), Facebook, Twitter/X, LinkedIn, TikTok
- **Content type** — product announcement, promotion/sale, motivational quote, educational, event
- **Key message** — the main text or headline to feature
- **Product(s)** — which products to include (if any)

### Step 2: Configure Design Parameters

Based on the platform, set format:
- **Instagram feed**: 1080x1080 (1:1) or 1080x1350 (4:5)
- **Instagram story**: 1080x1920 (9:16)
- **Facebook**: 1200x630 (landscape)
- **Twitter/X**: 1600x900 (16:9)
- **LinkedIn**: 1200x627 (landscape)
- **TikTok cover**: 1080x1920 (9:16)

Discuss style:
- **Visual style** — bold/graphic, photographic, minimalist, branded template
- **Color scheme** — brand primary (black/red), brand secondary, seasonal, custom
- **Text overlay** — headline placement, font style, readability

### Step 3: Generate the Graphic

Use the appropriate `mcp__jocko-imagery__` tool to generate the social graphic with:
- Platform-specific dimensions
- Content and style parameters
- Jocko Fuel brand guidelines (bold typography, clean layout)

### Step 4: Review and Iterate

Present the generated graphic to the user. Offer:
- **Approve** — graphic is ready to post
- **Adjust** — modify text, layout, or style and regenerate
- **Adapt** — create versions for additional platforms from the same concept

### Error Handling

- If MCP tools are unavailable, inform the user that the jocko-imagery server may need reconnection
- If text rendering is poor, suggest reducing text length or simplifying the layout
- If the graphic doesn't match brand standards, adjust color scheme and typography
