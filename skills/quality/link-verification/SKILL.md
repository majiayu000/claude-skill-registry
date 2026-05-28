---
name: link-verification
description: Use during content verification - validates all URLs are accessible and quoted text exists verbatim in sources
allowed-tools: WebFetch, Read
---

# Link Verification

## The Iron Law

**NO DRAFT APPROVAL WITH BROKEN LINKS OR MISMATCHED QUOTES**

Every URL must return 200 OK. Every quote must exist verbatim in its source. No exceptions.

## Purpose

Ensure all content maintains link integrity and quote accuracy by:
- Validating URL accessibility (no 404s, 403s, timeouts)
- Verifying quoted text exists verbatim in sources
- Detecting placeholder links (example.com, TODO, etc.)
- Confirming source attribution accuracy

## When to Use This Skill

Activate automatically when:
- Verifying content before publication
- Draft completion with `content-drafting` workflow
- Explicit verification step with `content-verification` workflow
- User requests link checking
- `citation-compliance` skill invokes this for URL validation

## Validation Requirements

### 1. URL Accessibility

**Requirement**: All URLs must be accessible with successful HTTP response

**Acceptable responses:**
- 200 OK (success)
- 301/302 Redirect (follow to final destination)

**Failure responses:**
- 404 Not Found
- 403 Forbidden
- 500 Internal Server Error
- Timeout (>10 seconds)
- Connection refused
- DNS resolution failure

**Validation process:**
1. Extract all URLs from draft content
2. For each URL:
   - Use WebFetch to request the URL
   - Record response status
   - Follow redirects to final destination
   - Verify final status is 200 OK
3. Report all failures with specific error codes

### 2. Quote Verbatim Verification

**Requirement**: All quoted text must match source content exactly

**Quote formats to detect:**
```markdown
> "Quoted text in blockquote"
"Inline quoted text"[^1]
"Quoted text with attribution" — Author Name
```

**Validation process:**
1. Extract all quoted text from draft
2. Identify source reference for each quote (footnote, inline link, citation ID)
3. Fetch/read the source content
4. Search for exact match in source
5. Flag mismatches (paraphrasing, summarization, missing quotes)

**Pass example:**
```markdown
# Draft
> "Seasonality impacts email engagement by up to 40% during peak periods"
Source: research-source.md

# Source content (research-source.md)
... analysis shows that seasonality impacts email engagement by up to 40% during peak periods such as Black Friday...

✓ Exact match found
```

**Fail example:**
```markdown
# Draft
> "Seasonality significantly affects email performance during holidays"
Source: research-source.md

# Source content (research-source.md)
... seasonality impacts email engagement by up to 40% during peak periods...

✗ Quote not found verbatim (paraphrased)
```

### 3. Placeholder Detection

**Forbidden placeholder patterns:**
- `example.com`, `example.org`
- `TODO`, `FIXME`, `TBD`
- `http://localhost`, `http://127.0.0.1`
- `[insert link]`, `[link here]`
- Broken markdown links: `[text]()` (empty href)

**Validation process:**
1. Scan draft for placeholder patterns
2. Report any matches
3. Fail verification if placeholders present

### 4. Attribution Accuracy

**Requirement**: Source attribution must match actual source metadata

**Validation for citations with attribution:**
```markdown
> "Quote text" — Author Name, Publication Title (2024)
```

**Validation process:**
1. Extract attribution details (author, title, date)
2. Read source metadata
3. Verify author matches
4. Verify title matches
5. Verify date matches (if provided)
6. Flag mismatches

## Validation Process

### 1. Load Draft and Sources

**Read:**
- Draft content: `datasets/marketing/content/{date}_{type}_{slug}/drafts/draft_v{n}.md`
- Citations: `datasets/marketing/content/{date}_{type}_{slug}/citations/sources.json`
- Referenced source files

### 2. Extract URLs and Quotes

**URLs:**
```regex
https?://[^\s\)]+
```

**Quotes:**
```regex
> "([^"]+)"
"([^"]+)"\[[\^\d+]\]
```

### 3. Validate URLs

For each URL:
```
1. WebFetch URL
2. Record status code
3. If 301/302: Follow to final URL and validate
4. If 200 OK: PASS
5. Otherwise: FAIL with error code
```

### 4. Validate Quotes

For each quote:
```
1. Identify source reference (footnote, inline link, citation ID)
2. Read source content
3. Search for exact quote match
4. If found verbatim: PASS
5. If paraphrased or missing: FAIL
```

### 5. Generate Report

**If all pass:**
```markdown
# Link Verification Report: PASS

## URL Validation
✓ 12 URLs validated successfully
  - https://example.com/article1 (200 OK)
  - https://example.com/article2 (200 OK)
  - [... all URLs listed ...]

## Quote Verification
✓ 8 quotes verified verbatim
  - "Quote 1" → Source: research-file.md (match confirmed)
  - "Quote 2" → Source: https://source.com (match confirmed)
  - [... all quotes listed ...]

## Placeholder Check
✓ No placeholders detected

**Status**: All links and quotes verified
```

**If any fail:**
```markdown
# Link Verification Report: FAIL

## URL Validation
✗ 2 URLs failed:
  - https://broken-link.com/article (404 Not Found)
  - https://timeout-site.com/page (Timeout after 10s)

✓ 10 URLs passed:
  - https://working-link.com/article (200 OK)
  - [... other passing URLs ...]

## Quote Verification
✗ 1 quote mismatch:
  - "Paraphrased quote text"
    - Source: research-file.md
    - Expected: Exact match not found
    - Action: Verify quote accuracy or remove quote marks

✓ 7 quotes verified

## Placeholder Check
✗ 1 placeholder detected:
  - Line 42: "TODO: Add citation here"

**Required fixes**:
1. Fix or remove broken URL: https://broken-link.com/article
2. Fix timeout URL or use archive: https://timeout-site.com/page
3. Verify quote accuracy or remove quote formatting
4. Replace placeholder with actual citation

**Status**: NEEDS_FIX
```

### 6. Block or Approve

**If PASS:**
- All links accessible
- All quotes verified verbatim
- No placeholders present
- Draft can proceed to publication

**If FAIL:**
- Broken links detected
- Quote mismatches found
- Placeholders present
- Workflow status set to "NEEDS_FIX"
- Must address violations before resuming

## Integration with Workflows

### Citation Compliance Integration

**Invoked by:**
- `citation-compliance` quality gate (for URL validation portion)

**Relationship:**
- `citation-compliance` handles overall source integrity
- `link-verification` specializes in URL accessibility and quote accuracy
- Works as sub-skill when needed

### Content Verification Integration

**Invoked by:**
- `content-verification` workflow (explicit verification step)
- `content-drafting` workflow (before marking draft complete)

**Blocking behavior:**
- If link verification fails → draft blocked
- User must fix broken links and mismatched quotes
- Workflow cannot proceed to snippets or publication

## Retry Logic

**For transient failures:**

If URL fails with timeout or 5xx error:
1. Retry once after 3-second delay
2. If second attempt succeeds: PASS
3. If second attempt fails: FAIL (report as unreliable)

**Do not retry:**
- 404 Not Found (permanent)
- 403 Forbidden (permission issue)
- DNS failure (domain issue)

## Success Criteria

Link verification passes when:
- All URLs return 200 OK (or 301/302 to 200 OK)
- All quoted text exists verbatim in sources
- Zero placeholders detected
- All attributions match source metadata
- Verification report shows PASS status

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Ignoring 301 redirects | Follow redirect and verify final destination |
| Accepting paraphrased quotes | Find verbatim match or remove quote formatting |
| Leaving placeholder links | Replace with actual sources |
| Skipping retries for timeouts | Retry once, then report if still failing |
| Not checking attribution accuracy | Verify author/title match source metadata |

## Related Skills

- **citation-compliance**: Invokes this skill for URL validation
- **content-verification**: Uses this skill for explicit verification step
- **source-integrity**: Validates source metadata (complementary concern)

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Link worked yesterday" | Verify every time. No assumptions. |
| "Quote is close enough" | Verbatim or not a quote. |
| "Placeholder is obvious" | Replace with actual source. |
| "One broken link is fine" | Zero tolerance. Fix or fail. |
| "We'll verify later" | Verify now or block workflow. |
