---
name: content-style
description: Use when drafting marketing content - enforces grade-8 readability, no em dashes, word count bands, and skimmable structure
---

# Content Style

## The Iron Laws

**1. NO EM DASHES. EVER.**

Not "—", not "–", not "--". Use periods, commas, or split into separate sentences.

**2. GRADE-8 READABILITY OR FAIL.**

Short sentences, simple words, clear structure. No academic jargon. No corporate bloat.

**3. WORD COUNT BANDS ARE MANDATORY.**

- Blog posts: 1000-1500 words
- Case studies: 500-800 words
- Internal docs: 600-1200 words

With `--strict` flag: ±10% tolerance only.

## Purpose

Ensure all marketing content maintains:
- Accessible, skimmable writing (grade-8 readability)
- Clean punctuation (no em dashes)
- Appropriate length for content type
- Bold key phrases for scanability
- Logical section structure with clear subheadings

## When to Use This Skill

Activate automatically when:
- Drafting blog posts, case studies, or documentation
- Verifying content before publication
- User explicitly requests style checking
- Content workflows invoke this quality gate
- `--strict` flag is set (enforces tighter word count tolerance)

## Style Requirements

### 1. Readability: Grade-8 Target

**Characteristics of grade-8 readability:**
- Average sentence length: 15-20 words
- Simple, common vocabulary
- Active voice preferred over passive
- One idea per sentence
- Short paragraphs (2-4 sentences)

**Pass examples:**
```
✓ "Seasonal demand fluctuates. Plan your campaigns accordingly."
✓ "Customers prefer personalized emails. Use segmentation to deliver relevant content."
✓ "Most users churn before their first send. Reduce onboarding friction to improve retention."
```

**Fail examples:**
```
✗ "The implementation of sophisticated segmentation methodologies facilitates enhanced personalization paradigms." (Grade 16+, corporate jargon)
✗ "Leveraging cutting-edge AI-driven predictive analytics enables stakeholders to optimize engagement metrics." (Grade 18+, buzzword soup)
```

**Validation method:**
- Use readability formulas (Flesch-Kincaid, Gunning Fog)
- Target: Grade 7-9 (acceptable range)
- Flag: Grade 10+ (requires simplification)

### 2. Punctuation: Zero Em Dashes

**Forbidden characters:**
- `—` (em dash)
- `–` (en dash used as em dash)
- `--` (double hyphen as em dash substitute)

**Acceptable alternatives:**
```
✗ "Email campaigns—when executed correctly—drive significant revenue."
✓ "Email campaigns drive significant revenue when executed correctly."

✗ "Three factors matter: personalization, timing—and relevance."
✓ "Three factors matter: personalization, timing, and relevance."

✗ "Users want simplicity—but most platforms overcomplicate setup."
✓ "Users want simplicity. Most platforms overcomplicate setup."
✓ "Users want simplicity, but most platforms overcomplicate setup."
```

**Validation method:**
- Scan entire draft for `—`, `–`, `--`
- Report exact line/location of violations
- Block completion until all removed

### 3. Word Count Bands

**Default bands:**
| Content Type | Minimum | Maximum | Strict (±10%) |
|--------------|---------|---------|---------------|
| Blog post | 1000 | 1500 | 900-1650 |
| Case study | 500 | 800 | 450-880 |
| Internal docs | 600 | 1200 | 540-1320 |

**Validation method:**
1. Count words in draft (exclude YAML frontmatter, footnotes)
2. Determine content type from intent.yaml or metadata
3. Apply appropriate band
4. If `--strict` flag: enforce ±10% tolerance
5. If outside band: FAIL with specific overage/underage

**Reporting:**
```
Blog post: 1847 words (target 1000-1500)
✗ FAIL: 347 words over maximum
Required action: Cut 347+ words or split into multiple pieces
```

### 4. Skimmable Structure

**Required elements:**
- Clear H1 (title)
- Descriptive H2s (section headings)
- Optional H3s (subsection headings)
- Bold key phrases (2-5 per section)
- Short paragraphs (2-4 sentences)
- Bulleted or numbered lists where appropriate

**Pass example:**
```markdown
# How to Plan Seasonal Email Campaigns

## Identify High-Demand Periods

Most ecommerce brands see **predictable demand spikes** during holidays and seasonal events. Analyze your historical data to find patterns.

Key periods to consider:
- Black Friday / Cyber Monday
- Valentine's Day (for gifting brands)
- Back-to-school (August-September)

## Align Campaign Timing

Launch campaigns **2-3 weeks before peak demand**. This gives customers time to browse, compare, and purchase.
```

**Fail example:**
```markdown
# Seasonal Email Strategy

The implementation of seasonal email campaign strategies requires comprehensive analysis of historical demand patterns, customer behavior analytics, and competitive landscape assessment. Organizations should leverage data-driven insights to optimize timing, messaging, and segmentation approaches across multiple touchpoints and channels to maximize engagement and conversion outcomes.
```

### 5. Soft Raleon Integration

**Guideline**: Single-line Raleon mention (≈1x per piece)

**Pass examples:**
```
✓ "Raleon automates this segmentation based on real-time behavior data."
✓ "Tools like Raleon learn these patterns and adjust send times automatically."
```

**Fail examples:**
```
✗ "Raleon is the best, most advanced, industry-leading platform for email marketing that outperforms all competitors and delivers unmatched results." (Over-selling, superlatives)
✗ [Multiple Raleon mentions throughout] (Too promotional)
```

## Validation Process

### 1. Load Draft

Read draft from:
- `datasets/marketing/content/{date}_{type}_{slug}/drafts/draft_v{n}.md`
- In-memory draft content

### 2. Apply Style Checks

Run all checks in parallel:

**Em Dash Scan:**
```bash
grep -n '—\|–\|--' draft.md
```
Report line numbers and context.

**Word Count:**
```bash
# Exclude YAML frontmatter and footnotes
wc -w draft.md
```
Compare to band for content type.

**Readability:**
- Calculate Flesch-Kincaid Grade Level
- Calculate Gunning Fog Index
- Average the two scores
- Compare to target (7-9)

**Structure Check:**
- Verify H1 exists (exactly one)
- Count H2s (minimum 3 for blogs, 2 for case studies)
- Verify bold usage (at least 1 per major section)
- Check paragraph length (flag paragraphs >6 sentences)

### 3. Generate Report

**If all pass:**
```markdown
# Content Style Validation: PASS

✓ No em dashes detected
✓ Word count: 1247 (target 1000-1500)
✓ Readability: Grade 8.2 (Flesch-Kincaid 8.1, Gunning Fog 8.3)
✓ Structure: Clear H1, 5 H2s, appropriate bold usage
✓ Raleon integration: 1 mention (appropriate)

**Status**: Ready for publication
```

**If any fail:**
```markdown
# Content Style Validation: FAIL

✗ Em dashes detected:
  - Line 42: "Email campaigns—when executed correctly—drive revenue"
  - Line 87: "Three factors matter: personalization, timing—and relevance"

✗ Word count: 1847 (target 1000-1500)
  - 347 words over maximum
  - Requires cutting or splitting

✗ Readability: Grade 11.4 (target 7-9)
  - Average sentence length: 28 words (target 15-20)
  - Requires simplification

**Required fixes**:
1. Remove/replace 2 em dashes
2. Cut 350+ words
3. Simplify sentences (reduce avg length to <20 words)

**Status**: NEEDS_FIX
```

### 4. Block or Approve

**If PASS:**
- Draft can proceed to snippets or publication
- Style validation complete

**If FAIL:**
- Draft blocked from next step
- Workflow status set to "NEEDS_FIX"
- Must address violations before resuming

## Integration with Workflows

### Content Pipeline Integration

**Invoked by:**
- `content-drafting` workflow (before marking draft complete)
- `content-verification` workflow (explicit style check)

**Blocking behavior:**
- If style check fails → draft cannot proceed
- Workflow paused until fixes applied
- User must address violations

### Strict Mode (`--strict` flag)

**When enabled:**
- Word count tolerance reduced to ±10%
- Readability target narrowed to Grade 7.5-8.5
- Paragraph length maximum reduced to 4 sentences
- All violations become blocking (no warnings)

## Success Criteria

Style validation passes when:
- Zero em dashes in draft
- Word count within band (or strict tolerance)
- Readability grade 7-9
- Clear H1/H2 structure
- Appropriate bold usage for skimmability
- Single soft Raleon mention

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Em dashes present | Replace with periods, commas, or split sentences |
| Word count over | Cut content or split into multiple pieces |
| Readability too high (Grade 12+) | Simplify sentences, use common words |
| Missing H2 structure | Add section headings every 200-300 words |
| Long paragraphs (>6 sentences) | Break into shorter paragraphs |
| Over-selling Raleon | Single soft mention, no superlatives |

## Related Skills

- **citation-compliance**: Validates source integrity (separate concern)
- **content-drafting**: Invokes this quality gate before completion
- **content-verification**: Explicit style validation step

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "One em dash won't hurt" | Zero tolerance. Remove it. |
| "This topic requires complex language" | Grade-8 or fail. Simplify. |
| "It's only 50 words over" | Bands exist for a reason. Cut it. |
| "Readers will understand long sentences" | Keep sentences <20 words average. |
| "We can fix style in editing" | Fix now or block workflow. |
