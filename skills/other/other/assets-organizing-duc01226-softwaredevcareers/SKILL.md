---
name: assets-organizing
description: Organize all outputs from slash commands and subagents in assets/ directory by topics, date format, and slugs.
---

# Assets Organizing

Standardize asset output locations, naming conventions, and directory structures for all marketing outputs.

## When to Use

Use this skill when:
- Creating content that needs file output (articles, videos, designs)
- Generating AI assets (images, storyboards, scripts)
- Organizing existing assets
- Determining output paths for new content types

## Quick Reference

### Output Paths

| Asset Type | Path | Naming |
|------------|------|--------|
| Articles | `assets/articles/{date}-{slug}/` | `{slug}.md` + `images/{date}-{slug}/` |
| Storyboards | `assets/storyboards/{date}-{slug}/` | `storyboard.md` + `scene-{N}-*.png` |
| Videos | `assets/videos/{date}-{slug}/` | `master.mp4` + `scene-{N}.mp4` |
| Transcripts | `assets/transcripts/` | `{slug}.md` |
| Writing Styles | `assets/writing-styles/` | `{slug}.md` |
| Banners | `assets/banners/{campaign}/` | `{variant}-{size}.{ext}` |
| Designs | `assets/designs/{project}/` | `{type}-{variant}.{ext}` |
| Infographics | `assets/infographics/` | `{date}-{slug}.{ext}` |
| Logos | `assets/logos/` | `{name}-{variant}.{ext}` |
| Social Posts | `assets/posts/{platform}/` | `{date}-{slug}.{ext}` |
| Generated | `assets/generated/{type}/` | `{date}-{slug}.{ext}` |
| **Reports** | | |
| Analytics | `assets/reports/analytics/` | `{date}-{report-type}.md` |
| SEO | `assets/reports/seo/` | `{date}-{audit-type}.md` |
| Social | `assets/reports/social/` | `{date}-{platform}-{report-type}.md` |
| Campaign | `assets/reports/campaigns/` | `{date}-{campaign}-{report-type}.md` |
| Performance | `assets/reports/performance/` | `{date}-{channel}-report.md` |
| Ads | `assets/reports/ads/` | `{date}-{platform}-report.md` |
| Email | `assets/reports/email/` | `{date}-{campaign}-report.md` |
| Funnel | `assets/reports/funnels/` | `{date}-{funnel}-analysis.md` |
| Content | `assets/reports/content/` | `{date}-{content-type}-audit.md` |
| **Text Content** | | |
| Copy | `assets/copy/{type}/` | `{date}-{slug}.md` |
| Ad Copy | `assets/copy/ads/` | `{date}-{campaign}-{variant}.md` |
| Email Copy | `assets/copy/emails/` | `{date}-{sequence}-{slug}.md` |
| Landing Pages | `assets/copy/landing-pages/` | `{slug}.md` |
| Headlines | `assets/copy/headlines/` | `{date}-{topic}.md` |
| Scripts | `assets/scripts/{type}/` | `{slug}.md` |
| **Campaigns** | | |
| Campaign Briefs | `assets/campaigns/{date}-{slug}/briefs/` | `{type}-brief.md` |
| Campaign Creatives | `assets/campaigns/{date}-{slug}/creatives/` | `{channel}-{variant}.{ext}` |
| Campaign Reports | `assets/campaigns/{date}-{slug}/reports/` | `{date}-{report-type}.md` |
| Campaign Assets | `assets/campaigns/{date}-{slug}/assets/` | `{type}-{name}.{ext}` |
| **Sales** | | |
| Pitches | `assets/sales/pitches/` | `{date}-{industry}-{persona}.md` |
| Proposals | `assets/sales/proposals/` | `{date}-{client}-proposal.md` |
| Case Studies | `assets/sales/case-studies/` | `{date}-{client}-{outcome}.md` |
| Battlecards | `assets/sales/battlecards/` | `{competitor}.md` |
| **SEO** | | |
| SEO Audits | `assets/seo/audits/` | `{date}-{domain}-audit.md` |
| Keyword Research | `assets/seo/keywords/` | `{date}-{topic}-keywords.md` |
| Schema Markup | `assets/seo/schemas/` | `{page}-schema.json` |
| **Funnels** | | |
| Funnel Designs | `assets/funnels/designs/` | `{date}-{slug}-funnel.md` |
| Funnel Audits | `assets/funnels/audits/` | `{date}-{funnel}-audit.md` |
| A/B Tests | `assets/funnels/tests/` | `{date}-{test-name}.md` |
| **Leads** | | |
| Scoring Models | `assets/leads/scoring-models/` | `{date}-{model-name}.md` |
| Segments | `assets/leads/segments/` | `{segment-name}.md` |
| ICP Profiles | `assets/leads/icp-profiles/` | `{persona}.md` |
| **Community** | | |
| Response Templates | `assets/community/templates/` | `{situation}.md` |
| FAQs | `assets/community/faqs/` | `{topic}.md` |
| Moderation Guides | `assets/community/moderation/` | `{policy}.md` |
| **Retention** | | |
| Retention Campaigns | `assets/retention/campaigns/` | `{date}-{campaign}.md` |
| Health Scoring | `assets/retention/scoring-models/` | `{date}-{model}.md` |
| Intervention Playbooks | `assets/retention/playbooks/` | `{segment}.md` |
| **Attraction** | | |
| Landing Page Content | `assets/attraction/landing-pages/` | `{slug}.md` |
| Lead Magnets | `assets/attraction/lead-magnets/` | `{slug}.md` |
| pSEO Templates | `assets/attraction/pseo-templates/` | `{template-name}.md` |
| Content Briefs | `assets/attraction/content-briefs/` | `{date}-{topic}.md` |
| **Diagnostics** | | |
| Campaign Audits | `assets/diagnostics/campaign-audits/` | `{date}-{campaign}.md` |
| Content Reviews | `assets/diagnostics/content-reviews/` | `{date}-{content}.md` |

### Naming Conventions

Load: `references/naming-conventions.md`

### Directory Structure Rules

Load: `references/directory-structure.md`

### Asset Type Details

Load: `references/asset-types.md`

## Core Rules

1. **Always use kebab-case** for slugs and filenames
2. **Date prefix** for time-sensitive assets: `{YYMMDD}` or `{YYMMDD-HHmm}`
3. **Self-contained folders** for multi-file assets (articles, videos, storyboards)
4. **Flat files** for single-file assets (transcripts, writing-styles)
5. **Platform subfolders** for platform-specific content

## Date Format

Use `$CK_PLAN_DATE_FORMAT` env var or default to `YYMMDD-HHmm`.

```bash
# PowerShell
Get-Date -UFormat "%y%m%d-%H%M"

# Bash
date +%y%m%d-%H%M
```

## Pre-Output Checklist

Before writing any asset:
1. Determine asset type → get base path
2. Generate slug from topic/title
3. Check if folder/file exists (avoid overwrite)
4. Create directory structure if needed
5. Output all related files together

## Integration Points

This skill integrates with:
- `/video:create` - Video assets
- `/video:storyboard:create` - Storyboard assets
- `/content/blog` - Article assets
- `/campaign` commands - Campaign assets
- `content-creator` agent - Various content
- `ui-ux-designer` agent - Design assets
- `copywriter` agent - Copy assets
- `email-wizard` agent - Email copy
- `social-media-manager` agent - Social posts
- `campaign-manager` agent - Campaign assets
- `sale-enabler` agent - Sales assets
- `seo-specialist` agent - SEO assets
- `/seo` commands - SEO audits
- `funnel-architect` agent - Funnel assets
- `lead-qualifier` agent - Lead assets
- `community-manager` agent - Community assets
- `continuity-specialist` agent - Retention assets
- `attraction-specialist` agent - Attraction assets
- `campaign-debugger` agent - Diagnostic reports
- `content-reviewer` agent - Review reports
- `analytics` skill - Analytics reports
- `seo-optimization` skill - SEO reports
- `social-media` skill - Social reports
- `campaign-management` skill - Campaign reports
- `ads-management` skill - Ads reports
- `email-marketing` skill - Email reports
