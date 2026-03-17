# brand-compliance

Unified brand compliance validation across visual, verbal, and legal dimensions.

## Triggers

- "brand review"
- "check brand compliance"
- "validate against brand guidelines"
- "brand audit"
- "is this on-brand"

## Purpose

This skill provides comprehensive brand compliance validation by:
- Checking visual identity (colors, logos, typography)
- Validating verbal identity (tone, voice, terminology)
- Verifying claims and legal requirements
- Ensuring accessibility compliance
- Generating actionable compliance reports

## Behavior

When triggered, this skill:

1. **Loads brand guidelines**:
   - Visual identity from `.aiwg/marketing/brand/`
   - Voice profile from voice-framework
   - Legal requirements from compliance config

2. **Analyzes visual elements**:
   - Color palette compliance
   - Logo usage correctness
   - Typography standards
   - Layout and spacing

3. **Validates verbal content**:
   - Tone consistency with brand voice
   - Terminology correctness
   - Messaging alignment
   - Tagline usage

4. **Checks legal compliance**:
   - Claims substantiation
   - Required disclosures
   - Trademark usage
   - Privacy statements

5. **Validates accessibility**:
   - WCAG 2.1 AA standards
   - Color contrast ratios
   - Alt text presence
   - Readable font sizes

6. **Generates compliance report**:
   - Pass/fail per criterion
   - Issue severity ratings
   - Specific corrections needed
   - Overall compliance score

## Validation Dimensions

### Visual Identity

```yaml
visual_checks:
  colors:
    - primary_colors_only: Verify only brand colors used
    - color_ratios: Check 60-30-10 rule
    - contrast_compliance: WCAG AA contrast

  logo:
    - correct_version: Right logo variant for context
    - clear_space: Minimum padding around logo
    - no_modifications: Logo not altered
    - proper_placement: Correct position

  typography:
    - approved_fonts: Only brand typefaces
    - hierarchy: Proper heading structure
    - minimum_sizes: Legible font sizes
    - line_spacing: Adequate line height

  imagery:
    - style_consistency: Matches brand aesthetic
    - quality_standards: Resolution requirements
    - diversity_representation: Inclusive imagery
```

### Verbal Identity

```yaml
verbal_checks:
  tone:
    - voice_consistency: Matches brand voice profile
    - formality_level: Appropriate for channel
    - personality_traits: Brand personality evident

  terminology:
    - approved_terms: Using brand glossary
    - product_names: Correct product naming
    - banned_phrases: No prohibited language

  messaging:
    - value_prop_alignment: Core messages present
    - tagline_usage: Correct tagline application
    - call_to_action: On-brand CTAs

  grammar:
    - style_guide: AP/Chicago/Brand style
    - capitalization: Title case rules
    - punctuation: Consistent punctuation
```

### Legal Compliance

```yaml
legal_checks:
  claims:
    - substantiation: Claims have evidence
    - comparative: Fair comparison rules
    - testimonials: Proper disclaimers

  disclosures:
    - required_statements: Mandatory disclosures
    - placement: Visible disclosure location
    - font_size: Legible disclosure text

  trademarks:
    - proper_symbols: ® and ™ usage
    - third_party: Licensed usage
    - no_infringement: No trademark violations

  privacy:
    - data_collection: Privacy notice present
    - consent: Opt-in mechanisms
    - cookies: Cookie notice if applicable
```

### Accessibility

```yaml
accessibility_checks:
  wcag:
    - contrast_ratio: Minimum 4.5:1 text, 3:1 UI
    - text_alternatives: Alt text for images
    - keyboard_navigation: Focusable elements
    - readable_text: No text in images

  inclusive:
    - plain_language: Readable content
    - color_independence: Info not color-only
    - responsive: Mobile accessible
```

## Compliance Report Format

```markdown
# Brand Compliance Report

**Asset**: Summer Campaign Hero Banner
**Date**: 2025-12-08
**Reviewer**: brand-compliance skill

## Summary

| Dimension | Score | Status |
|-----------|-------|--------|
| Visual Identity | 95% | ✅ Pass |
| Verbal Identity | 88% | ⚠️ Minor Issues |
| Legal Compliance | 100% | ✅ Pass |
| Accessibility | 75% | ⚠️ Needs Attention |
| **Overall** | **90%** | **Conditional Pass** |

## Visual Identity

### ✅ Colors
- Primary blue (#0066CC) used correctly
- Secondary green (#00AA55) in accent areas
- No off-brand colors detected

### ✅ Logo
- Correct horizontal logo version
- Clear space maintained (1x height)
- No modifications to logo

### ⚠️ Typography
- **Issue**: Body text uses Arial instead of Inter
- **Severity**: Medium
- **Fix**: Replace Arial with Inter Regular

## Verbal Identity

### ✅ Tone
- Voice consistent with "Friendly Professional" profile
- Appropriate formality for social media channel

### ⚠️ Terminology
- **Issue**: "Best-in-class" used (prohibited phrase)
- **Severity**: High
- **Fix**: Replace with specific benefit statement

### ✅ Messaging
- Value proposition clearly stated
- CTA "Start Free Trial" is on-brand

## Legal Compliance

### ✅ Claims
- All claims substantiated
- No comparative claims

### ✅ Disclosures
- Trademark symbols present
- Terms link visible

## Accessibility

### ⚠️ Contrast
- **Issue**: White text on light blue (3.2:1 ratio)
- **Severity**: High
- **Fix**: Darken background or use darker text
- **Standard**: WCAG AA requires 4.5:1

### ❌ Alt Text
- **Issue**: Hero image missing alt text
- **Severity**: High
- **Fix**: Add descriptive alt text

## Required Corrections

| Priority | Issue | Location | Fix |
|----------|-------|----------|-----|
| High | Low contrast | Hero text | Darken background |
| High | Missing alt text | Hero image | Add alt attribute |
| High | Banned phrase | Body copy | Replace "best-in-class" |
| Medium | Wrong font | Body text | Use Inter, not Arial |

## Approval Status

**Status**: CONDITIONAL APPROVAL

Asset may proceed after addressing:
- [ ] High-priority accessibility issues
- [ ] Banned phrase removal

Re-review recommended after corrections.
```

## Usage Examples

### Full Brand Review

```
User: "Brand review for the new landing page"

Skill validates:
1. Visual: colors, logo, typography
2. Verbal: tone, terms, messaging
3. Legal: claims, disclosures, trademarks
4. Accessibility: contrast, alt text

Output:
"Brand Compliance: 90% (Conditional Pass)

Issues Found:
- High: Low contrast ratio (3.2:1, need 4.5:1)
- High: Missing alt text on 2 images
- Medium: Body font incorrect

Report: .aiwg/marketing/reviews/brand-landing-page.md"
```

### Quick Tone Check

```
User: "Is this copy on-brand?"

Skill analyzes:
- Voice consistency
- Terminology
- Messaging alignment

Output:
"Tone Analysis: ✅ On-brand

Voice: Friendly Professional (matches profile)
Terminology: All approved terms
Messaging: Value prop present

One suggestion: CTA could be more action-oriented"
```

### Legal Review Focus

```
User: "Check claims compliance"

Skill validates:
- Claim substantiation
- Comparative statements
- Required disclosures

Output:
"Claims Compliance: ⚠️ Issues Found

- Claim 'fastest in industry' needs substantiation
- Missing source citation for statistics
- Disclosure font too small (8pt, need 10pt)"
```

## Integration

This skill uses:
- `parallel-dispatch`: Launch Brand Guardian + Legal + Accessibility
- `voice-framework`: Load brand voice profile for tone validation
- `project-awareness`: Find brand guidelines location

## Agent Orchestration

```yaml
agents:
  visual_review:
    agent: brand-guardian
    focus: Visual identity validation

  verbal_review:
    agent: brand-guardian
    focus: Verbal identity and tone

  legal_review:
    agent: legal-reviewer
    focus: Claims, disclosures, trademarks

  accessibility_review:
    agent: accessibility-checker
    focus: WCAG compliance, inclusive design

  quality_check:
    agent: quality-controller
    focus: Technical specs, rendering
```

## Configuration

### Brand Guidelines Location

```yaml
brand_config:
  guidelines_dir: .aiwg/marketing/brand/
  voice_profile: .aiwg/voices/brand-voice.yaml
  color_palette: brand/colors.yaml
  typography: brand/typography.yaml
  logo_specs: brand/logo-usage.md
  terminology: brand/glossary.yaml
  banned_phrases: brand/banned-phrases.yaml
```

### Severity Thresholds

```yaml
severity:
  blocking:
    - trademark_violation
    - missing_required_disclosure
    - wcag_level_a_failure

  high:
    - banned_phrase
    - contrast_below_aa
    - missing_alt_text
    - wrong_logo_version

  medium:
    - wrong_font
    - color_off_palette
    - tone_inconsistency

  low:
    - minor_spacing
    - style_preference
```

## Output Locations

- Compliance report: `.aiwg/marketing/reviews/brand-{asset}-{date}.md`
- Issue tracker: `.aiwg/marketing/reviews/brand-issues.json`
- Approval records: `.aiwg/marketing/approvals/`

## References

- Brand guidelines: .aiwg/marketing/brand/
- Voice profiles: voice-framework addon
- WCAG guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- Templates: templates/governance/brand-compliance-checklist.md
