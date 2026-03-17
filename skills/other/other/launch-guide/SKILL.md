---
name: launch-guide
description: Guide the complete product launch process across Product Hunt, social media, blogs, and other platforms. Use when preparing a launch, filling out Product Hunt submission forms, planning screenshots and visual assets, writing taglines, or coordinating multi-platform launch day execution.
category: business
license: MIT
---

# Launch Guide

End-to-end product launch execution guide covering platform submissions, visual
asset preparation, copywriting, and launch day coordination.

## When to Use

- Preparing a Product Hunt submission (name, tagline, description, tags, first
  comment)
- Planning what screenshots to take and how to annotate them
- Writing launch copy for blogs, social media, and email
- Coordinating a multi-platform launch day
- Creating a launch checklist and timeline

## Phase 1: Gather Launch Information

Ask the user for all required launch details using this structured intake:

### Required Fields

| Field             | Constraints                   | Example                           |
| ----------------- | ----------------------------- | --------------------------------- |
| **Product name**  | 12-40 characters              | "Kellog Engine"                   |
| **Tagline**       | Up to 60 characters, required | "Build games 10x faster with ECS" |
| **Description**   | Up to 500 characters          | What's new or different           |
| **Launch tags**   | 1-3 tags, required            | AI, Developer Tools, Open Source  |
| **Links**         | Product URL + store links     | App Store, Steam, web app         |
| **X account**     | x.com/ handle                 | x.com/kellog_engine               |
| **Open source?**  | Yes/No                        | Yes                               |
| **First comment** | Essential for engagement      | See template below                |

### Additional Context to Gather

- Target audience and ideal user persona
- Top 3 differentiators vs. existing products
- Pricing model (free, freemium, paid)
- Demo URL, video, or live playground
- Launch date and timezone
- Any existing landing page or repo

## Phase 2: Product Hunt Submission

### Filling Out the Form

**Name** (12-40 chars): Use the actual product name. Short, memorable, no
tagline in the name field.

**Tagline** (up to 60 chars): One sentence that communicates the core benefit.
Formula: `[Action verb] + [outcome] + [differentiator]`

Tagline examples:

- "Ship games faster with a Bevy-inspired ECS engine for Zig"
- "AI-powered code review that catches bugs before your team does"
- "Turn screenshots into annotated tutorials in seconds"

**Links**: Add all relevant links:

- Primary product URL (required)
- App Store / Google Play / Steam / Amazon links
- GitHub repo (if open source)

**Description** (up to 500 chars): Answer: "What's new or different compared to
existing products? Which features make it stand out?"

Structure: `[Problem] → [Solution] → [Key differentiator] → [Who it's for]`

**Launch tags**: Select up to 3 tags that match the product category. Pick the
most specific tags available. Broad tags like "Productivity" have more
competition.

**First comment**: Post immediately upon launch. This is essential to start the
discussion. See
[references/first-comment-templates.md](references/first-comment-templates.md).

### Gallery Assets (Product Hunt)

Product Hunt allows up to 8 images/videos. Recommended gallery order:

1. **Hero image**: Product in action, clean UI, main value prop as text overlay
2. **Problem/solution**: Before/after or pain point → resolution
3. **Key feature 1**: Annotated screenshot with callouts
4. **Key feature 2**: Annotated screenshot with callouts
5. **Key feature 3**: Annotated screenshot with callouts
6. **Demo GIF or video**: 30-60 second walkthrough
7. **Social proof**: Testimonials, metrics, logos
8. **Pricing or CTA**: How to get started

## Phase 3: Screenshot and Visual Asset Strategy

### What Screenshots to Take

Capture these categories:

**Hero shots**: Clean, full-screen product UI showing the main value. Remove
distracting browser chrome. Use a clean desktop wallpaper if showing desktop
app.

**Feature highlights**: One screenshot per key feature. Show the feature in use,
not just a settings panel. Include realistic data, not lorem ipsum.

**Workflow sequences**: 3-4 screenshots showing a complete task from start to
finish. Number them or add step labels.

**Before/after**: Side-by-side comparison showing the problem state and the
solution state.

**Results/output**: Show what the user gets — the report, the generated code,
the final design, the dashboard with real metrics.

### Screenshot Best Practices

- Use 1270x760px or 2x (2540x1520px) for Product Hunt
- Clean up notifications, bookmarks bar, messy tabs before capture
- Use realistic data — fake data looks fake
- Consistent window size and zoom level across all shots
- Light mode preferred for readability (unless product is dark-themed)

### Annotating Screenshots

Add annotations to guide the viewer's eye:

- **Numbered callouts** (1, 2, 3) pointing to key UI elements
- **Brief labels** (2-5 words) explaining what each callout shows
- **Highlight boxes** around important areas
- **Arrow or pointer** to draw attention to a specific element
- **Text overlay** at top or bottom for context

Tools for annotation: Figma, Cleanshot X, Shottr, Skitch, or browser-based tools
like Markup Hero.

### Creating Annotated Screenshots

Workflow for each screenshot:

1. Take a clean screenshot at proper resolution
2. Open in annotation tool
3. Add a colored highlight box around the key area
4. Add a short text label (e.g., "Real-time collaboration")
5. Optionally add a step number if part of a sequence
6. Export as PNG at 2x resolution
7. Keep consistent annotation style (same colors, fonts, sizes)

## Phase 4: Launch Copy

### Blog Post Structure

```
Title: Introducing [Product] — [Tagline]

## The Problem
[2-3 paragraphs on the pain point]

## Introducing [Product]
[What it does and why it's different]

## Key Features
### [Feature 1]
[Screenshot + explanation]

### [Feature 2]
[Screenshot + explanation]

### [Feature 3]
[Screenshot + explanation]

## How It Works
[Walkthrough with annotated screenshots]

## Get Started
[CTA + links]
```

### Social Media Announcements

**X/Twitter** (single tweet):
`[Emoji] Launching [Product] today on @ProductHunt! [Tagline]. [Link] #LaunchDay`

**X/Twitter** (thread): See the `product-launch-announcement-writer` skill for
full thread templates.

**LinkedIn**: Professional framing. Lead with the problem in your industry.
Include a screenshot. End with a question.

**Email to list**: Subject: "Introducing [Product] — [Benefit]". Keep it
personal. Include one clear CTA.

## Phase 5: Launch Day Execution

### Launch Day Checklist

**Before launch (24-48 hours):**

- [ ] All screenshots taken and annotated
- [ ] Product Hunt submission drafted (schedule if possible)
- [ ] Blog post written and ready to publish
- [ ] Social media posts drafted for all platforms
- [ ] Email drafted and segmented
- [ ] Rally supporters — DM friends, communities, supporters

**Launch morning:**

- [ ] Publish Product Hunt listing (12:01 AM PT for full day visibility)
- [ ] Post first comment immediately
- [ ] Publish blog post
- [ ] Send email blast
- [ ] Post on X/Twitter
- [ ] Post on LinkedIn
- [ ] Post in relevant communities (Slack, Discord, Reddit, HN)

**Throughout the day:**

- [ ] Respond to every Product Hunt comment within 30 minutes
- [ ] Engage with social media replies
- [ ] Share updates and milestones ("We just hit #5 on Product Hunt!")
- [ ] Thank supporters publicly

**After launch (24-48 hours):**

- [ ] Write a thank-you post with results
- [ ] Share learnings and metrics
- [ ] Follow up with new users
- [ ] Plan next launch or feature announcement

### Timing Guidelines

- **Product Hunt**: Launches at 12:01 AM PT. Submit early for full day.
- **X/Twitter**: Best engagement 9-11 AM or 6-8 PM ET
- **LinkedIn**: Tuesday-Thursday, 8-10 AM local time
- **Email**: Tuesday-Thursday, 10 AM recipient's local time
- **Reddit/HN**: Early morning US time (6-9 AM ET)

## Output Format

After gathering all information, produce:

1. **Product Hunt submission** — all form fields filled and ready to paste
2. **Screenshot shot list** — specific screenshots to capture with annotations
3. **Blog post draft** — full launch blog post
4. **Social media posts** — platform-specific announcements
5. **Launch day checklist** — time-sequenced execution plan
6. **First comment draft** — for Product Hunt discussion

For detailed first comment templates and examples, see
[references/first-comment-templates.md](references/first-comment-templates.md).

For the Product Hunt form field reference and tag list, see
[references/product-hunt-form-guide.md](references/product-hunt-form-guide.md).

## Related Skills

- `product-launch-announcement-writer` — detailed announcement copy and platform
  templates
- `community-growth-specialist` — post-launch community engagement
- `lead-research-assistant` — identify influencers and early adopters

## Sources

- [Product Hunt Launch Guide](https://www.producthunt.com/launch)
- [Product Hunt Best Practices](https://blog.producthunt.com/how-to-launch-on-product-hunt)
- [Indie Hackers Launch Strategies](https://www.indiehackers.com/)
