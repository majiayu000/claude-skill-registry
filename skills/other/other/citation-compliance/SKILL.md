---
name: citation-compliance
description: Use when drafting or verifying content requiring source integrity - enforces strategic quoting with inline links and blocks "(source needed)" markers from draft completion
allowed-tools: Read, Grep, WebFetch
---

# Citation Compliance

## The Iron Law

**NO DRAFT COMPLETION WITH "(source needed)" MARKERS**

If any claim lacks a verifiable source, either:
1. Remove the claim entirely, OR
2. Mark "(source needed)" and **immediately fail** the draft with `step="NEEDS_FIX"`

No "fix it later". No "close enough". No exceptions.

## Purpose

Ensure all marketing content, strategy memos, and public-facing documents maintain source integrity through:
- Strategic quoting (not heavy citation)
- Inline links to verifiable sources
- Verbatim quote accuracy
- Research-informed original work

## When to Use This Skill

Activate automatically when:
- Drafting blog posts, case studies, or documentation
- Creating strategy memos or decision documents
- Verifying content before publication
- User explicitly requests citation checking
- Any content workflow invokes this quality gate

## Citation Philosophy

**This is not a research paper.**

- **Strategic quoting**: Include quotes when they add significant value (expert insights, compelling data, case study testimonials)
- **Inline links**: Default to inline links instead of footnotes for source references
- **Research-informed original work**: Write knowledgeably and authoritatively, not as a book report
- **Verbatim accuracy**: When quoting, quotes must match sources exactly

## Validation Rules

### 1. Source Verification

**For every factual claim:**
- Must have a verifiable source (file path, URL, or citation entry)
- Inline link preferred: `[claim text](https://source.com)`
- OR footnote reference: `claim text[^1]` with source in References section
- OR citation ID: `claim text (src_abc123)` with entry in citations/sources.json

### 2. Quote Verification

**For every quoted fragment:**
- Must exist verbatim in the source document
- No paraphrasing presented as quotes
- Proper attribution (author, source, date if applicable)

**Validation Process:**
1. Extract all quoted text from draft
2. For each quote, fetch/read the source
3. Search for exact match in source
4. Confirm quote appears verbatim
5. Flag mismatches immediately

### 3. Link Accessibility

**For every URL:**
- Must be accessible (200 OK response)
- No broken links (404, 403, etc.)
- No placeholder URLs (example.com, TODO, etc.)

**Validation Process:**
1. Extract all URLs from draft
2. Use WebFetch to verify each URL
3. Confirm successful response
4. Flag inaccessible links immediately

### 4. "(source needed)" Detection

**Zero tolerance policy:**
- Scan entire draft for "(source needed)" markers
- If found: STOP immediately
- Set status to `step="NEEDS_FIX"`
- List all instances in verification report
- Do not proceed to next workflow step

## Enforcement Process

### During Drafting

**Before completing any draft:**
1. Scan for "(source needed)" markers
2. If found → fail immediately
3. Validate all inline links
4. Verify all quoted fragments
5. Only mark draft complete if all checks pass

### During Verification

**Explicit verification step:**
1. Load draft and citations/sources.json
2. Extract all source references (links, footnotes, citation IDs)
3. Verify each source is accessible
4. Extract all quoted text
5. Verify quotes exist verbatim in sources
6. Scan for "(source needed)"
7. Generate verification report

### Verification Report Format

```markdown
# Citation Verification Report

## Summary
- Total claims: N
- Verified sources: N
- Broken links: N
- Mismatched quotes: N
- "(source needed)" markers: N
- **Status**: PASS | FAIL

## Verified Citations
✓ [Claim text] → [Source URL/path] (verified)
✓ [Quote text] → [Source] (verbatim match confirmed)

## Failed Citations
✗ [Claim text] → [Source URL] (link broken: 404)
✗ [Quote text] → [Source] (quote not found or mismatched)
✗ [Claim text] → "(source needed)" marker detected

## Required Fixes
1. Fix or remove: [specific claim with broken link]
2. Verify quote accuracy: [specific quote with mismatch]
3. Add source or remove claim: [claim with missing source]
```

## Integration with Workflows

### Content Pipeline Integration

**Invoked by:**
- `content-drafting` workflow (before marking draft complete)
- `content-verification` workflow (explicit verification step)

**Blocking behavior:**
- If citation-compliance fails → draft cannot proceed to snippets
- Workflow status set to "NEEDS_FIX"
- User must address violations before resuming

### Strategy Session Integration

**Invoked by:**
- `strategy-memo` workflow (before finalizing memo)

**Blocking behavior:**
- If citation-compliance fails → memo cannot be finalized
- All claims must be source-backed or removed

## Red Flags

**Immediate violations:**
- Finding "(source needed)" anywhere in draft
- Broken links or inaccessible URLs
- Quoted text that doesn't match source
- Placeholder citations (TODO, FIX, etc.)
- Claims without any source reference

## Success Criteria

Citation compliance is satisfied when:
- Zero "(source needed)" markers in draft
- All URLs accessible (200 OK)
- All quoted text verified verbatim in sources
- Every factual claim has a verifiable source
- Verification report shows PASS status

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Allowing "(source needed)" to proceed | Stop immediately, set NEEDS_FIX |
| Skipping link verification | Validate every URL before completion |
| Accepting paraphrased quotes | Verify verbatim match or remove quote markers |
| "Will fix in next pass" rationalization | Fix now or fail the gate |

## Related Skills

- **link-verification**: Specialized URL validation (invoked by this skill)
- **source-integrity**: Validates citation metadata and checksums
- **content-drafting**: Invokes this quality gate before completion
- **content-verification**: Explicit verification workflow using this skill

## Anti-Rationalization Blocks

Common excuses that are **explicitly rejected**:

| Rationalization | Reality |
|----------------|---------|
| "Just one (source needed) left" | One is too many. Fix it or fail. |
| "I'll add sources in the next pass" | No next pass. Fix now. |
| "The quote is close enough" | Verbatim or not a quote. |
| "Link worked yesterday" | Verify every time. |
| "This is just a draft" | Drafts must pass or be marked NEEDS_FIX. |
