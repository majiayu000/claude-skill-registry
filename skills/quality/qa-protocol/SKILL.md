---
name: qa-protocol
description: Multi-stage quality assurance protocol for marketing assets with channel-specific validation. Use when relevant to the task.
---

# qa-protocol

Multi-stage quality assurance protocol for marketing assets with channel-specific validation.

## Triggers

- "quality check"
- "QA this asset"
- "validate for [channel]"
- "ready for approval"
- "pre-flight check"
- "final review"

## Purpose

This skill implements comprehensive quality assurance across marketing deliverables by:
- Running channel-specific validation rules
- Checking technical specifications
- Validating content accuracy
- Ensuring brand compliance
- Generating approval-ready reports

## Behavior

When triggered, this skill:

1. **Identifies asset type and channel**:
   - Parse asset metadata
   - Determine target channel(s)
   - Load channel-specific QA rules

2. **Runs technical validation**:
   - File format and dimensions
   - Resolution and color space
   - File size limits
   - Naming conventions

3. **Validates content**:
   - Copy accuracy and spelling
   - Link verification
   - CTA presence and clarity
   - Legal requirements

4. **Checks brand compliance**:
   - Invoke brand-compliance skill
   - Visual identity validation
   - Tone consistency

5. **Applies channel rules**:
   - Platform-specific requirements
   - Character limits
   - Aspect ratios
   - File type requirements

6. **Generates QA report**:
   - Pass/fail per criterion
   - Blocking vs advisory issues
   - Remediation guidance
   - Approval recommendation

## Channel Specifications

### Social Media

```yaml
social_channels:
  instagram:
    feed_post:
      aspect_ratios: [1:1, 4:5, 1.91:1]
      max_video_duration: 60s
      max_carousel: 10
      caption_limit: 2200
      hashtag_limit: 30
    story:
      aspect_ratio: 9:16
      max_duration: 15s
      dimensions: 1080x1920
    reel:
      aspect_ratio: 9:16
      max_duration: 90s
      dimensions: 1080x1920

  linkedin:
    post:
      image_ratio: [1.91:1, 1:1, 4:5]
      video_duration: [3s, 10min]
      text_limit: 3000
      hashtag_limit: 5
    article:
      header_image: 1200x627
      min_words: 500

  twitter:
    tweet:
      text_limit: 280
      image_ratio: [16:9, 1:1]
      max_images: 4
      video_duration: [0.5s, 140s]
    thread:
      max_tweets: 25

  facebook:
    post:
      text_limit: 63206
      image_ratio: [1.91:1, 1:1, 4:5]
      video_duration: [1s, 240min]
    ad:
      primary_text: 125
      headline: 40
      description: 30
      image_ratio: 1.91:1
```

### Email

```yaml
email_specs:
  general:
    max_width: 600px
    max_file_size: 100KB per image
    total_size: 1MB recommended
    subject_line: 50 chars optimal
    preheader: 85-100 chars

  images:
    formats: [jpg, png, gif]
    max_dimensions: 600x1200
    alt_text: required
    background_colors: required (image blocking)

  links:
    tracking: required
    utm_params: required
    unsubscribe: required
    physical_address: required

  testing:
    clients: [gmail, outlook, apple_mail, yahoo]
    dark_mode: required
    mobile_responsive: required
```

### Digital Ads

```yaml
ad_specs:
  google_display:
    formats:
      - {size: "300x250", name: "medium_rectangle"}
      - {size: "336x280", name: "large_rectangle"}
      - {size: "728x90", name: "leaderboard"}
      - {size: "300x600", name: "half_page"}
      - {size: "320x50", name: "mobile_leaderboard"}
    max_file_size: 150KB
    formats: [jpg, png, gif, html5]
    animation_length: 30s max

  meta_ads:
    image:
      ratio: 1.91:1
      min_resolution: 1080x1080
      text_overlay: <20% recommended
    video:
      ratio: [1:1, 4:5, 9:16]
      duration: [1s, 241min]
      max_file_size: 4GB
    carousel:
      cards: [2, 10]
      ratio: 1:1
```

### Print

```yaml
print_specs:
  general:
    color_space: CMYK
    resolution: 300dpi minimum
    bleed: 0.125in (3mm)
    safe_zone: 0.25in from trim

  formats:
    letter: 8.5x11in
    a4: 210x297mm
    business_card: 3.5x2in
    brochure_trifold: 8.5x11in folded

  preflight:
    fonts_embedded: required
    images_linked: check
    overprint: verify
    transparency: flatten for offset
```

## QA Checklist Categories

### Content Validation

```yaml
content_checks:
  copy:
    - spelling_grammar: Run spell check
    - brand_terminology: Use approved terms
    - cta_present: Clear call-to-action
    - value_proposition: Key message present
    - tone_voice: Matches brand voice

  accuracy:
    - dates_times: Verify all dates
    - prices_offers: Confirm pricing
    - contact_info: Validate phone/email
    - links_urls: Test all links
    - legal_claims: Substantiation check

  localization:
    - translations: Accuracy check
    - cultural_sensitivity: Review imagery
    - regional_compliance: Local regulations
```

### Technical Validation

```yaml
technical_checks:
  files:
    - naming_convention: Follows standard
    - file_format: Correct for channel
    - file_size: Within limits
    - resolution: Meets minimum

  layout:
    - safe_zones: Content within bounds
    - bleed_setup: Correct for print
    - aspect_ratio: Matches spec
    - responsive: Mobile optimized

  accessibility:
    - alt_text: Present and descriptive
    - contrast_ratio: WCAG compliant
    - font_size: Minimum 14px
    - color_independence: Not color-only
```

### Brand Validation

```yaml
brand_checks:
  visual:
    - logo_usage: Correct version and placement
    - color_palette: On-brand colors only
    - typography: Approved fonts
    - imagery_style: Matches guidelines

  verbal:
    - tone: Consistent with brand voice
    - messaging: Key messages present
    - tagline: Correct usage
    - terminology: Approved glossary
```

## QA Report Format

```markdown
# Quality Assurance Report

**Asset**: Holiday Email Campaign - Hero Banner
**Channel**: Email
**Date**: 2025-12-08
**QA Specialist**: qa-protocol skill

## Summary

| Category | Checks | Passed | Failed | Warnings |
|----------|--------|--------|--------|----------|
| Content | 12 | 11 | 0 | 1 |
| Technical | 8 | 8 | 0 | 0 |
| Brand | 6 | 5 | 1 | 0 |
| Channel | 10 | 9 | 1 | 0 |
| **Total** | **36** | **33** | **2** | **1** |

## Status: CONDITIONAL PASS

Asset may proceed after addressing 2 blocking issues.

## Blocking Issues

### BLK-001: Missing Alt Text
- **Category**: Channel (Email)
- **Element**: Hero image
- **Requirement**: Alt text required for email images
- **Fix**: Add descriptive alt text: "Holiday sale - 30% off all products"

### BLK-002: Off-Brand Color
- **Category**: Brand
- **Element**: CTA button
- **Current**: #FF6B6B (coral)
- **Required**: #0066CC (brand blue) or #00AA55 (brand green)
- **Fix**: Update button color to brand palette

## Warnings

### WARN-001: Subject Line Length
- **Category**: Content
- **Current**: 62 characters
- **Recommended**: 50 characters optimal
- **Note**: May truncate on mobile devices
- **Suggestion**: "Holiday Sale: 30% Off Everything" (35 chars)

## Passed Checks

### Content
- [x] Spelling and grammar verified
- [x] CTA present and clear ("Shop Now")
- [x] Value proposition stated (30% off)
- [x] Dates accurate (Dec 15-25)
- [x] Links functional (3 tested)
- [x] Unsubscribe link present
- [x] Physical address included
- [x] Price claims verified
- [x] Terms link present
- [x] Preheader text present
- [x] Tone matches brand voice

### Technical
- [x] File size: 450KB (under 1MB limit)
- [x] Image resolution: 600x400 (correct)
- [x] Format: HTML with inline CSS
- [x] Width: 600px (correct)
- [x] Images have fallback colors
- [x] Mobile responsive
- [x] Dark mode compatible
- [x] Client tested (Gmail, Outlook, Apple Mail)

### Brand
- [x] Logo: Correct horizontal version
- [x] Typography: Inter font family
- [x] Imagery: On-brand photography style
- [x] Tone: Friendly professional
- [x] Tagline: Correct usage

### Channel (Email)
- [x] Subject line present
- [x] Preheader configured
- [x] UTM parameters present
- [x] Tracking pixels configured
- [x] List-unsubscribe header
- [x] SPF/DKIM configured
- [x] Preview text optimized
- [x] Footer compliant
- [x] Mobile preview checked

## Approval Recommendation

**Status**: CONDITIONAL

Asset is ready for approval pending:
1. Add alt text to hero image
2. Update CTA button to brand color

Estimated fix time: 15 minutes

## Sign-off

- [ ] Content Owner: _____________
- [ ] Brand Manager: _____________
- [ ] Legal (if applicable): _____________
- [ ] Final Approver: _____________
```

## Usage Examples

### Full QA Check

```
User: "QA this email campaign"

Skill executes:
1. Detect asset type: Email campaign
2. Load email QA rules
3. Run content validation
4. Run technical checks
5. Run brand compliance
6. Apply email-specific rules
7. Generate report

Output:
"QA Complete: CONDITIONAL PASS

36 checks run:
- Passed: 33
- Failed: 2
- Warnings: 1

Blocking Issues:
1. Missing alt text on hero image
2. CTA button uses off-brand color

Report: .aiwg/marketing/qa/email-holiday-qa-report.md"
```

### Channel-Specific Check

```
User: "Validate for Instagram"

Skill focuses on:
- Instagram feed/story/reel specs
- Aspect ratio validation
- Caption length check
- Hashtag count

Output:
"Instagram Validation: PASS

All checks passed:
- Aspect ratio: 1:1 (correct for feed)
- Resolution: 1080x1080 (meets minimum)
- Caption: 180 chars (under 2200 limit)
- Hashtags: 12 (under 30 limit)

Ready for posting."
```

### Pre-Flight Check

```
User: "Pre-flight check for print"

Skill validates:
- CMYK color space
- 300dpi resolution
- Bleed setup
- Font embedding
- Linked images

Output:
"Print Pre-flight: FAIL

Critical issues:
1. Color space: RGB (need CMYK)
2. Resolution: 150dpi (need 300dpi)
3. Bleed: Not set (need 0.125in)

Must fix before sending to printer."
```

## Integration

This skill uses:
- `brand-compliance`: For brand validation dimension
- `project-awareness`: For detecting asset context
- `artifact-metadata`: For tracking QA status

## Agent Orchestration

```yaml
agents:
  content_review:
    agent: editor
    focus: Copy accuracy, spelling, grammar

  brand_review:
    agent: brand-guardian
    focus: Visual and verbal brand compliance

  technical_review:
    agent: quality-controller
    focus: Specs, formats, technical requirements

  legal_review:
    agent: legal-reviewer
    focus: Claims, disclosures, compliance
    condition: has_claims == true
```

## Configuration

### Channel Rules Location

```yaml
qa_config:
  channel_specs: .aiwg/marketing/config/channel-specs.yaml
  brand_rules: .aiwg/marketing/brand/
  qa_templates: templates/governance/qa-checklist.md
```

### Severity Levels

```yaml
severity:
  blocking:
    - missing_legal_disclosure
    - broken_link
    - wrong_price
    - missing_alt_text
    - off_brand_logo

  warning:
    - suboptimal_length
    - minor_typo
    - style_preference

  advisory:
    - optimization_suggestion
    - best_practice_note
```

## Output Locations

- QA reports: `.aiwg/marketing/qa/{asset}-qa-report.md`
- Checklists: `.aiwg/marketing/qa/checklists/`
- Approval records: `.aiwg/marketing/approvals/`

## References

- Channel specifications: .aiwg/marketing/config/channel-specs.yaml
- Brand guidelines: .aiwg/marketing/brand/
- QA templates: templates/governance/qa-checklist.md
