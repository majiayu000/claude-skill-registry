---
name: marketing
description: Create comprehensive marketing content for themes, plugins, and web products. Generates organized folder structure with product descriptions, feature highlights, social media posts, email campaigns, video scripts, sales materials, and brand assets. Use when creating promotional content, announcements, or sales copy.
---

# Marketing Skill for Theme & Plugin Agency

## Writing Style Guidelines

### Tone & Voice (Non-Negotiable)

**Be Human, Not AI:**
- Write like a helpful colleague, not a marketing robot
- Use natural language that sounds like a real person wrote it
- Avoid buzzwords: "revolutionary", "game-changing", "seamless", "leverage", "synergy"
- Skip filler words: "basically", "essentially", "simply", "just"
- No excessive punctuation (!!!) or ALL CAPS for emphasis

**Emoji Policy:**
- Maximum ONE emoji per piece of content (or none)
- Use only when it adds clarity, not decoration
- Prefer text over emoji for important information

**What to Avoid:**
```
❌ "🚀 This REVOLUTIONARY plugin will TRANSFORM your workflow!! 💥"
✅ "This plugin handles form submissions automatically, so you can focus on your actual work."

❌ "Simply leverage our seamless integration to unlock game-changing results!"
✅ "Connect it to your email list in two clicks. New subscribers sync automatically."
```

## Folder Structure

When creating marketing content for a product, create this folder structure:

```
marketing/
├── 01-slides/                    # Visual presentation content
│   ├── product-overview-slides.md
│   ├── feature-breakdown-slides.md
│   ├── use-case-slides.md
│   └── free-vs-pro-comparison.md
├── 02-video-scripts/             # Video content
│   ├── 01-product-overview.md    # 2-3 min explainer
│   ├── 02-installation-setup.md  # Tutorial
│   ├── 03-feature-demos.md       # Feature walkthroughs
│   ├── short-ads.md              # 15s, 30s, 60s scripts
│   └── shot-list-template.md     # Production notes
├── 03-website-copy/              # Website content
│   ├── landing-page.md           # Full landing page
│   ├── features.md               # Feature highlights
│   ├── product-description.md    # Marketplace descriptions
│   ├── faq-content.md            # FAQ section
│   └── feature-pages/            # Individual feature pages
│       └── [feature-name].md
├── 04-email-sequences/           # Email campaigns
│   ├── welcome-sequence.md       # Onboarding emails
│   ├── feature-announcement.md   # New feature emails
│   ├── free-to-pro-upgrade.md    # Upgrade campaigns
│   └── re-engagement.md          # Win-back emails
├── 05-social-media/              # Social content (separate files per platform)
│   ├── twitter-posts.md          # Twitter/X content
│   ├── linkedin-posts.md         # LinkedIn content
│   ├── facebook-posts.md         # Facebook content
│   └── instagram-captions.md     # Instagram content
├── 06-sales-materials/           # Sales enablement
│   ├── one-pager.md              # Quick sales sheet
│   ├── objection-handling.md     # Sales FAQ responses
│   ├── feature-comparison-chart.md # Competitive comparison
│   ├── roi-calculator-content.md # Value justification
│   └── testimonials.md           # Customer quotes
├── 07-brand-assets/              # Brand guidelines
│   ├── persona-profiles.md       # Target customer profiles
│   ├── messaging-guide.md        # Voice and messaging
│   └── seo-keywords.md           # Keywords and meta content
└── README.md                     # Index and quick reference
```

## Instructions

### 1. Always Start with Personas

Before creating content, define 3-5 target personas in `07-brand-assets/persona-profiles.md`:

```markdown
## Persona: [Name]

### Demographics
- Role, Age, Team Size, Industry, Technical Level

### Goals
- What they want to achieve

### Pain Points
- Problems they face (be specific, not generic)

### Why Product Appeals
- Feature-to-benefit mapping

### Key Message
> "One sentence that resonates with this persona"

### Content They Respond To
- Types of content that work
```

### 2. Product Descriptions

Lead with benefits, not features:

```
❌ "Includes auto-moderation feature"
✅ "Stop spam automatically — so you can focus on growing your community"
```

**Power words to use wisely:** effortless, powerful, stunning, instant, automatic
**Words to avoid:** revolutionary, game-changing, seamless, leverage, synergy, cutting-edge

### 3. Feature Highlights

Transform every feature into a benefit using:
- "so you can..."
- "which means..."

```markdown
**What It Does:**
[Feature description - plain language]

**The Benefit:**
[Outcome] — so you can [user benefit].

**Why It Matters:**
- [Feature detail], which means [benefit]
- [Feature detail], so you can [benefit]
```

### 4. Screenshots & Visuals

**Requirements:**
- Use real screenshots from local development environment
- Show actual product UI, not mockups
- Annotate with arrows or highlights for clarity
- Crop to relevant area (no full-screen captures)
- Ensure no sensitive data visible
- Use consistent browser/window size

**Before creating visual content, ask:**
> "Do you have a local development setup where we can capture real screenshots? I'll need access to take authentic product images."

### 5. Video Scripts

Structure for each video:
```markdown
## Video Details
- Title, Duration, Purpose, Tone, Target

## Script

### INTRO (0:00 - 0:XX)
**VISUAL:** [Description]
**NARRATOR:** "[Script - conversational, not salesy]"
**ON-SCREEN TEXT:** "[Text overlay]"

### [SECTION NAME] (X:XX - X:XX)
...

## Production Notes
- Visual style
- Music suggestions (upbeat but not overwhelming)
- Screenshots needed (from local dev environment)
```

### 6. Social Media (Separate Files Per Platform)

**Twitter/X:** (`twitter-posts.md`)
- Hook in first line
- 1-2 key benefits
- One emoji maximum (or none)
- Thread format for longer content

**LinkedIn:** (`linkedin-posts.md`)
- Professional tone
- Problem → Solution format
- Statistics and proof points
- No emoji or one maximum

**Facebook:** (`facebook-posts.md`)
- Community-focused
- Storytelling approach
- Engagement questions

**Instagram:** (`instagram-captions.md`)
- Visual-first (describe image needed)
- Short, punchy captions
- Carousel/Reel ideas included

### 7. Email Campaigns

Structure each email file with multiple templates:
- Subject line variations (A/B test)
- Full email body (human tone, not salesy)
- CTA options (clear, action-oriented)

### 8. Sales Materials

**One-Pager:** Print-ready summary with:
- Problem/Solution (lead with the problem they feel)
- Key features (3-5 max)
- Results/Stats (real numbers when possible)
- Pricing
- CTA

**Objection Handling:** For each objection:
- Understand (clarifying questions)
- Acknowledge (validate concern genuinely)
- Address (provide information)
- Confirm (check if resolved)

### 9. Pricing Messaging

Always include accurate pricing from product page:
```markdown
| License | Price | Sites |
|---------|-------|-------|
| Single | $XX/yr | 1 site |
| 5 License | $XX/yr | 5 sites |
| Developer | $XX/yr | Unlimited |
```

## Quality Checklist

Before completing, verify:

### Content Quality
- [ ] Personas defined
- [ ] All folders created
- [ ] Pricing accurate
- [ ] Benefits (not just features)
- [ ] "so you can..." language used
- [ ] Social media split by platform
- [ ] Objection handling complete
- [ ] README index updated

### Tone Check
- [ ] Human tone (not robotic/AI-sounding)
- [ ] No excessive emojis (max 1 per piece)
- [ ] No buzzwords (revolutionary, seamless, etc.)
- [ ] No filler words (basically, simply, etc.)
- [ ] Reads like a helpful colleague wrote it
- [ ] Direct and respectful of reader's time

### Visual Content
- [ ] Screenshots requested from local dev environment
- [ ] No stock photos where real product images should be
- [ ] All visuals annotated clearly
- [ ] No sensitive data visible
