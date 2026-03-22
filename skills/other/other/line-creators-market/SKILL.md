---
name: line-creators-market
description: Comprehensive reference for LINE Creators Market — sticker character design (static, animated, custom, message, big, popup, effect stickers), emoji series planning, theme creation, technical specifications, review guidelines, submission workflow, revenue model, AI usage declaration, and market strategies for Japan, Taiwan, Thailand, and global audiences. This skill should be used when the user asks to "design a LINE sticker character", "plan an emoji series", "create a LINE theme", "check sticker submission specs", "understand review guidelines", "optimize sticker SEO", "plan market strategy for LINE stickers", "calculate creator revenue", or mentions LINE stickers, LINE emoji, LINE themes, Creators Market, sticker submission, sticker review, sticker pricing, sticker rejection, APNG animated stickers, creator revenue sharing, LINE Sticker Premium, LINE Sticker Maker, custom stickers, message stickers, big stickers, popup stickers, effect stickers, or AI-generated stickers. Always use this skill whenever the user mentions LINE stickers, LINE emoji, LINE themes, sticker creation, or LINE Creators Market, even if they don't explicitly say "Creators Market".
---

# LINE Creators Market

Reference for creating, submitting, and selling LINE stickers, emoji, and themes on Creators Market.

**Do not answer LINE Creators Market specs or policy questions from memory — platform rules update frequently. Always consult the references below.**

## Workflow

### Character Design Consultation
1. Clarify user goals: sticker / emoji / theme? Target market?
2. Load [references/style-guide.md](references/style-guide.md) to match style direction
3. Reference [references/experts.md](references/experts.md) for successful case studies
4. Check [references/sticker-specs.md](references/sticker-specs.md) for technical feasibility
5. Use output templates to provide structured proposals

### Technical Spec Queries
1. Load [references/sticker-specs.md](references/sticker-specs.md)
2. Answer specific spec questions, citing official data
3. Flag common spec mistakes

### Market Strategy Planning
1. Confirm target market (Japan / Taiwan / Thailand / Global)
2. Load [references/market-tips.md](references/market-tips.md) for market-specific playbook
3. Combine with [references/experts.md](references/experts.md) success stories
4. Provide concrete, actionable plans

### Submission & Review
1. Load [references/creators-market-guide.md](references/creators-market-guide.md)
2. Guide user through the submission process
3. Run quality checklist for final confirmation

## Creative Framework

Before starting creation, clarify three key questions:

### 1. Character Positioning
- **Emotional connection**: What emotion or personality does the character represent? Healing, funny, sarcastic, cute?
- **Usage context**: In what chat scenarios would users reach for this sticker?
- **Memorability**: One feature that makes the character memorable (round face, distinctive eyes, signature pose)

### 2. Market Positioning
- **Target market**: Japan (healing), Taiwan (local slang), Thailand (humor), Global (universal expressions)
- **Competitive analysis**: Strengths and weaknesses of similar stickers? How to differentiate?
- **Pricing strategy**: Paid vs free (ad-supported, promotional)

### 3. Series Planning
- **Extensibility**: Can the character support multiple sticker sets? Is there a storyline?
- **Character family**: Can supporting characters or a world be developed?
- **Cross-media**: Potential for animation, merchandise licensing?

## Output Templates

### Character Proposal Format
```
Character Name:
Core Personality: (one-sentence description)
Visual Features: (appearance, color palette, signature pose)
Target Audience:
Target Market:
Usage Scenarios: (top 3-5 chat situations where users would use this)
Differentiation: (what sets it apart from existing competitors)
Extension Potential: (series expansion, cross-media possibilities)
```

### Sticker Set Planning Format
```
Type: Sticker / Emoji / Theme
Quantity:
Essential Expressions: (greeting, thanks, apology, OK, NG...)
Signature Expressions: (character-specific poses, catchphrases)
Recommended Price:
Launch Timing:
```

## Quality Checklist

- [ ] Character is clearly recognizable at thumbnail size (96x74 px)
- [ ] Expression variety covers common chat scenarios
- [ ] All image dimensions are even numbers
- [ ] File sizes within limits (sticker < 1MB, animated < 1MB, emoji < 1MB, animated emoji < 300KB)
- [ ] Background fully transparent with ~10px margin on all sides
- [ ] No copyrighted elements (brand logos, other creators' characters)
- [ ] No ads, announcements, or dates embedded in images
- [ ] Title and description are compelling and SEO-friendly
- [ ] Multi-language descriptions are accurate (title <= 40 chars, description <= 160 chars)
- [ ] Tags set (max 9 per sticker/emoji) for auto-suggest functionality
- [ ] AI usage declaration accurately set if AI was used in creation
- [ ] Previewed in simulator for chat room appearance

## Reference Index

| File | Topic |
|------|-------|
| [sticker-specs.md](references/sticker-specs.md) | Full technical specs for stickers, animated stickers, emoji, and themes |
| [style-guide.md](references/style-guide.md) | Five creative style guides and design principles |
| [experts.md](references/experts.md) | Top global creator database and success strategies |
| [market-tips.md](references/market-tips.md) | Market-specific playbooks, pricing, SEO, and promotion |
| [creators-market-guide.md](references/creators-market-guide.md) | Creators Market platform operations, review rules, and revenue model |
| [theme-specs.md](references/theme-specs.md) | Theme design best practices, color coordination, readability tips |

## Language-Aware Links

All Creators Market URLs use `https://creator.line.me/{lang}/...`. Match `{lang}` to the user's language (see [creators-market-guide.md](references/creators-market-guide.md) for the full mapping). Default to `en` if uncertain.

## Tools

- **LINE Sticker Maker**: [iOS](https://itunes.apple.com/jp/app/line/id1239684967) | [Android](https://play.google.com/store/apps/details?id=com.linecorp.usersticker) | [Info](https://creator.line.me/{lang}/stickermaker/) — mobile sticker creation from photos/videos
- **Sticker Simulator**: Preview stickers in chat room context before submission (in Creators Market web dashboard)
- **Photoshop Template**: Official PSD template for theme creation (CS6+)
- **LINE STORE Search**: [LINE Sticker Maker](https://store.line.me/search/sticker/en?q=LINE+Sticker+Maker) — browse existing LINE Sticker Maker creations
