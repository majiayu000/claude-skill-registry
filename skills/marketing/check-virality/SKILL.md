---
name: check-virality
description: |
  Audit viral growth: social sharing, OG images, referrals, distribution.
  Outputs structured findings. Use log-virality-issues to create issues.
  Invoke for: shareability audit, referral review, distribution analysis.
---

# /check-virality

Audit viral growth infrastructure. Output findings as structured report.

## What This Does

1. Check social metadata (OG tags, Twitter cards)
2. Check dynamic OG image generation
3. Check share mechanics
4. Check referral system
5. Check distribution readiness
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-virality-issues` to create GitHub issues or `/fix-virality` to fix.

## Process

### 1. Social Metadata Check

```bash
# OG tags present?
grep -rE "og:title|og:description|og:image" --include="*.tsx" --include="*.ts" app/ src/ pages/ 2>/dev/null | head -5

# Twitter cards?
grep -rE "twitter:card|twitter:title|twitter:image" --include="*.tsx" --include="*.ts" app/ src/ pages/ 2>/dev/null | head -5

# Root metadata?
grep -q "generateMetadata\|metadata.*:" app/layout.tsx 2>/dev/null && echo "✓ Root metadata" || echo "✗ Root metadata missing"
```

### 2. Dynamic OG Images Check

```bash
# OG image endpoint?
[ -f "app/api/og/route.tsx" ] || [ -d "pages/api/og" ] && echo "✓ OG image endpoint" || echo "✗ OG image endpoint"

# Using @vercel/og?
grep -q "@vercel/og" package.json 2>/dev/null && echo "✓ @vercel/og installed" || echo "✗ @vercel/og not installed"

# Dynamic images per content type?
grep -rE "generateMetadata.*images" --include="*.tsx" app/ 2>/dev/null | head -5
```

### 3. Share Mechanics Check

```bash
# Share components?
grep -rE "share|Share|navigator\.share" --include="*.tsx" --include="*.ts" components/ src/ 2>/dev/null | head -5

# Shareable URLs?
grep -rE "shareUrl|shareLink|getShareUrl|clipboard\.writeText" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5

# Web Share API?
grep -q "navigator.share" components/**/*.tsx 2>/dev/null && echo "✓ Web Share API" || echo "✗ Web Share API"
```

### 4. Referral System Check

```bash
# Referral codes?
grep -rE "referral|invite|inviteCode|refCode" --include="*.tsx" --include="*.ts" --include="*.sql" . 2>/dev/null | grep -v node_modules | head -5

# Attribution tracking?
grep -rE "utm_|referrer|attribution" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v node_modules | head -5

# Referral tracking in database?
grep -rE "referral|invitation" --include="*.ts" convex/ schema/ prisma/ 2>/dev/null | head -5
```

### 5. Distribution Readiness Check

```bash
# Launch assets?
[ -f "public/product-hunt-logo.png" ] || [ -d "public/launch" ] && echo "✓ Launch assets" || echo "✗ Launch assets"

# Press kit?
[ -d "public/press" ] || [ -d "public/media" ] && echo "✓ Press kit" || echo "✗ Press kit"

# Changelog page?
[ -f "app/changelog/page.tsx" ] || [ -f "pages/changelog.tsx" ] && echo "✓ Changelog page" || echo "✗ Changelog page"

# Social proof?
grep -rE "testimonial|review|rating" --include="*.tsx" . 2>/dev/null | grep -v node_modules | head -3
```

### 6. Viral Loop Analysis

Check for viral loop patterns:
- Creation → Share prompts
- Achievement → Share cards
- Invitation → Reward system
- Content → Watermarks/branding

## Output Format

```markdown
## Virality Audit

### P0: Critical (Invisible Online)
- No OG tags - Links look broken when shared
- No root metadata configured

### P1: Essential (Every Product)
- No dynamic OG images - All shares look the same
- No share button/mechanism
- No Twitter card configuration
- metadataBase not set (og images won't work)

### P2: Important (Growth)
- No referral system
- No attribution (UTM) tracking
- No share prompts at key moments
- No Web Share API (mobile native share)

### P3: Launch Readiness
- No changelog page
- No press kit
- No launch assets
- No testimonials/social proof

## Current Status
- OG metadata: Missing
- Dynamic OG images: Not configured
- Share mechanics: None
- Referral system: None
- Distribution: Not ready

## Summary
- P0: 2 | P1: 4 | P2: 4 | P3: 4
- Recommendation: Add root metadata and OG image endpoint first
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No OG tags | P0 |
| No root metadata | P0 |
| No dynamic OG images | P1 |
| No share mechanics | P1 |
| No Twitter cards | P1 |
| No referral system | P2 |
| No UTM tracking | P2 |
| No share prompts | P2 |
| Launch assets missing | P3 |
| No changelog | P3 |

## Related

- `/log-virality-issues` - Create GitHub issues from findings
- `/fix-virality` - Fix virality gaps
- `/virality` - Full viral growth workflow
- `/launch-strategy` - Product launch planning
