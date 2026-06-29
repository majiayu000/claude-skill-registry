---
name: content-reviewer
description: 'Use when the user asks to "review this influencer content" or "check if this post meets brand guidelines"; produces a structured review (brand alignment, message accuracy, compliance, quality, technical specs), an approve/revise/reject decision, and a constructive feedback message for the creator. Not for drafting the brief that sets the criteria — use brief-generator; not for the partnership agreement — use contract-helper.'
version: "10.0.1"
license: Apache-2.0
compatibility: "Claude Code and compatible agent-skill hosts"
homepage: "https://github.com/aaron-he-zhu/aaron-marketing-skills"
when_to_use: "Activate when the user has an influencer content submission (draft post, video, image, caption) and needs a gate decision before it goes live. Triggers include reviewing content against a brief, checking FTC/disclosure compliance, scoring creative quality, building a review checklist, or writing revision feedback for a creator. Use after the brief exists and before the content is published or amplified."
argument-hint: "<content submission or link> [platform] [campaign]"
metadata:
  author: aaron-he-zhu
  version: "10.0.1"
  family: influencer-marketing
  impact-phase: Activate
---

# Content Reviewer

This skill helps you systematically review influencer content submissions to ensure they meet brand guidelines, campaign objectives, and legal requirements before going live.

## Quick Start

Shortest invocation:

```
Review this influencer content submission: [content description/link]
```

Common scenario — gate a submission against a campaign brief:

```
Check if this TikTok post meets our brand guidelines for [campaign], then give me an approve/revise/reject decision and feedback I can send the creator
```

## Skill Contract

- **Reads**: the content submission (link, description, caption, media notes), the campaign brief and key messages, brand guidelines, disclosure/FTC requirements, platform technical specs, and any prior review notes in `memory/influencer/content-reviewer/`.
- **Writes**: a review record at `memory/influencer/content-reviewer/YYYY-MM-DD-<topic>.md` containing category scores, the gate decision, and the feedback message.
- **Promotes**: durable facts (final approval status, recurring compliance gaps, creator-specific notes) to `memory/hot-cache.md`.
- **Done when**:
  1. Every must-pass category (brand alignment, message accuracy, compliance, technical specs) has an explicit pass/fail with evidence.
  2. A single decision is recorded — APPROVED, APPROVED WITH MINOR CHANGES, REVISIONS REQUIRED, or REJECTED.
  3. A constructive feedback message for the creator exists (when changes are needed).
- **Primary next skill**: [contract-helper](../../activate/contract-helper/SKILL.md)

### Handoff Summary

> Emit the standard shape from [skill-contract.md §Handoff Summary Format](../../references/skill-contract.md).

## Data Sources

This family needs no live integrations (Tier 1). The skill works end to end from inputs you provide: paste the content link or description, the brief, brand guidelines, and platform specs, and it produces the review.

Optional connectors can speed up evidence gathering where available:

- `~~social platform analytics` — pull native post specs, engagement signals, and platform disclosure flags (e.g. "Paid partnership" label).
- `~~influencer database` — load the creator's history, prior submissions, and past compliance flags.
- `~~CRM` — link the review back to the deal, campaign owner, and approval chain.
- `~~compliance reference` — current FTC / platform disclosure rules for the relevant market.

With no connector configured, ask the user for the missing inputs and proceed. See [CONNECTORS.md](../../CONNECTORS.md) for the keyless data recipes.

## Instructions

When a user requests content review:

1. **Establish Review Criteria**

   ```markdown
   ### Review Framework
   
   **Campaign**: [name]
   **Influencer**: @[handle]
   **Platform**: [platform]
   **Content Type**: [format]
   **Brief Reference**: [link to brief]
   
   ### Review Categories
   
   | Category | Weight | Pass Threshold |
   |----------|--------|----------------|
   | Brand Alignment | [%] | Must pass |
   | Message Accuracy | [%] | Must pass |
   | Compliance | [%] | Must pass |
   | Creative Quality | [%] | 80%+ |
   | Technical Specs | [%] | Must pass |
   ```

2. **Brand Alignment Review**

   ```markdown
   ## Brand Alignment Review
   
   ### Visual Brand Check
   
   | Element | Guideline | Content | Status |
   |---------|-----------|---------|--------|
   | Tone | [expected] | [observed] | ✅/⚠️/❌ |
   | Aesthetic | [expected] | [observed] | ✅/⚠️/❌ |
   | Quality level | [expected] | [observed] | ✅/⚠️/❌ |
   | Brand representation | [expected] | [observed] | ✅/⚠️/❌ |
   
   ### Brand Safety Check
   
   | Risk Area | Check | Status | Notes |
   |-----------|-------|--------|-------|
   | Controversial topics | [details] | ✅/❌ | [notes] |
   | Competitor mentions | [details] | ✅/❌ | [notes] |
   | Inappropriate content | [details] | ✅/❌ | [notes] |
   | Sensitive contexts | [details] | ✅/❌ | [notes] |
   | Background elements | [details] | ✅/❌ | [notes] |
   
   ### Value Alignment
   
   | Brand Value | Reflected in Content? | Notes |
   |-------------|-----------------------|-------|
   | [Value 1] | ✅/⚠️/❌ | [how/why not] |
   | [Value 2] | ✅/⚠️/❌ | [how/why not] |
   
   **Brand Alignment Score**: [X/10]
   **Status**: ✅ Pass / ⚠️ Minor Issues / ❌ Fail
   
   **Notes**: [Overall assessment]
   ```

3. **Message Accuracy Review**

   ```markdown
   ## Message Accuracy Review
   
   ### Key Message Check
   
   | Required Message | Present? | How Communicated | Accuracy |
   |------------------|----------|------------------|----------|
   | [Message 1] | ✅/❌ | [how] | ✅/⚠️/❌ |
   | [Message 2] | ✅/❌ | [how] | ✅/⚠️/❌ |
   | [Message 3] | ✅/❌ | [how] | ✅/⚠️/❌ |
   
   ### Talking Points Check
   
   | Talking Point | Included | Notes |
   |---------------|----------|-------|
   | [Point 1] | ✅/❌ | [notes] |
   | [Point 2] | ✅/❌ | [notes] |
   | [Point 3] | ✅/❌ | [notes] |
   
   ### Prohibited Claims Check
   
   | Prohibited Content | Present? | Issue |
   |--------------------|----------|-------|
   | False claims | ✅/❌ | [if present] |
   | Competitor disparagement | ✅/❌ | [if present] |
   | Unsubstantiated claims | ✅/❌ | [if present] |
   | [Industry-specific] | ✅/❌ | [if present] |
   
   ### Call-to-Action Check
   
   | CTA Requirement | Status | Notes |
   |-----------------|--------|-------|
   | CTA present | ✅/❌ | |
   | Correct CTA | ✅/❌ | Expected: [X], Actual: [Y] |
   | Clear and compelling | ✅/⚠️/❌ | |
   
   **Message Accuracy Score**: [X/10]
   **Status**: ✅ Pass / ⚠️ Minor Issues / ❌ Fail
   ```

4. **Compliance Review**

   ```markdown
   ## Compliance Review
   
   ### Disclosure Check
   
   | Requirement | Status | Details |
   |-------------|--------|---------|
   | Disclosure present | ✅/❌ | [type used] |
   | Disclosure visible | ✅/❌ | [placement] |
   | Disclosure clear | ✅/❌ | [assessment] |
   | Disclosure early | ✅/❌ | [timing/placement] |
   
   **Acceptable Disclosures Used**:
   - [ ] #ad
   - [ ] #sponsored
   - [ ] "Paid partnership" feature
   - [ ] Verbal disclosure
   - [ ] Other: [specify]
   
   **Disclosure Issues** (if any):
   - [Issue 1]
   - [Issue 2]
   
   ### Platform-Specific Requirements
   
   | Platform Rule | Status | Notes |
   |---------------|--------|-------|
   | [Rule 1] | ✅/❌ | [notes] |
   | [Rule 2] | ✅/❌ | [notes] |
   
   ### Legal/Regulatory Check
   
   | Requirement | Status | Notes |
   |-------------|--------|-------|
   | FTC compliance | ✅/❌ | |
   | Industry regulations | ✅/❌ | [specific] |
   | Age restrictions | ✅/❌ | [if applicable] |
   | Claims substantiation | ✅/❌ | |
   | Copyright/licensing | ✅/❌ | Music, images, etc. |
   
   ### Required Elements Check
   
   | Element | Required | Present | Status |
   |---------|----------|---------|--------|
   | Brand mention | ✅ | ✅/❌ | ✅/❌ |
   | @[handle] tag | ✅ | ✅/❌ | ✅/❌ |
   | #[hashtag] | ✅ | ✅/❌ | ✅/❌ |
   | Link/URL | ✅/❌ | ✅/❌ | ✅/❌ |
   | Promo code | ✅/❌ | ✅/❌ | ✅/❌ |
   
   **Compliance Score**: [X/10]
   **Status**: ✅ Pass / ❌ Fail (no partial pass for compliance)
   ```

   **C³ ART veto enforcement.** This compliance gate is the C³ **Content** review ([ART](../../references/c3/art-content-benchmark.md)). Two ART items are veto-level — a failure forces the overall decision to **Reject** (never "revise"), and you must cite the veto ID:
   - **T1 · FTC Disclosure** (maps to the Disclosure Check + FTC compliance rows above) — missing or inadequate disclosure on sponsored content → **Reject (T1)**. Regulatory basis: FTC 16 CFR §255 and the 2024 Trade Regulation Rule (16 CFR Part 465). Not legal advice.
   - **T2 · Claim Integrity** (maps to Claims substantiation) — false or unsubstantiated claims → **Reject (T2)**.

5. **Quality Assessment**

   ```markdown
   ## Quality Assessment
   
   ### Production Quality
   
   | Element | Rating | Notes |
   |---------|--------|-------|
   | Video/Image quality | [1-5] | [notes] |
   | Audio quality (if applicable) | [1-5] | [notes] |
   | Lighting | [1-5] | [notes] |
   | Framing/Composition | [1-5] | [notes] |
   | Editing | [1-5] | [notes] |
   
   **Production Score**: [X/25]
   
   ### Content Effectiveness
   
   | Element | Rating | Notes |
   |---------|--------|-------|
   | Hook strength | [1-5] | [notes] |
   | Engagement potential | [1-5] | [notes] |
   | Authenticity | [1-5] | [notes] |
   | Storytelling | [1-5] | [notes] |
   | Persuasiveness | [1-5] | [notes] |
   
   **Effectiveness Score**: [X/25]
   
   ### Platform Optimization
   
   | Element | Optimized? | Notes |
   |---------|------------|-------|
   | Format for platform | ✅/❌ | |
   | Length appropriate | ✅/❌ | [actual vs. optimal] |
   | Native feel | ✅/❌ | |
   | Trend relevance | ✅/⚠️/❌ | |
   
   ### Creative Assessment
   
   | Factor | Assessment |
   |--------|------------|
   | Originality | [1-5] |
   | Brand integration naturalness | [1-5] |
   | Memorability | [1-5] |
   | Share-worthiness | [1-5] |
   
   **Quality Score**: [X/10]
   **Status**: ✅ Pass / ⚠️ Acceptable / ❌ Below Standard
   ```

6. **Technical Specifications Check**

   ```markdown
   ## Technical Specifications Check
   
   ### Platform Requirements
   
   | Spec | Required | Actual | Status |
   |------|----------|--------|--------|
   | Aspect ratio | [ratio] | [ratio] | ✅/❌ |
   | Resolution | [min] | [actual] | ✅/❌ |
   | Duration | [range] | [actual] | ✅/❌ |
   | File format | [formats] | [format] | ✅/❌ |
   | File size | [max] | [actual] | ✅/❌ |
   
   ### Caption Check
   
   | Element | Requirement | Actual | Status |
   |---------|-------------|--------|--------|
   | Length | [max chars] | [chars] | ✅/❌ |
   | Hashtags | [requirements] | [actual] | ✅/❌ |
   | Tags | [requirements] | [actual] | ✅/❌ |
   | Links | [requirements] | [actual] | ✅/❌ |
   
   **Technical Status**: ✅ Pass / ❌ Fail
   ```

7. **Generate Final Review**

   ```markdown
   # Content Review Summary
   
   ## Submission Details
   
   | Field | Value |
   |-------|-------|
   | Campaign | [name] |
   | Influencer | @[handle] |
   | Content Type | [type] |
   | Submission Date | [date] |
   | Reviewer | [name] |
   | Review Date | [date] |
   
   ## Review Scores
   
   | Category | Score | Status | Weight |
   |----------|-------|--------|--------|
   | Brand Alignment | [X/10] | ✅/⚠️/❌ | [%] |
   | Message Accuracy | [X/10] | ✅/⚠️/❌ | [%] |
   | Compliance | [X/10] | ✅/❌ | [%] |
   | Quality | [X/10] | ✅/⚠️/❌ | [%] |
   | Technical | Pass/Fail | ✅/❌ | - |
   | **Overall** | **[X/10]** | | |
   
   ## Decision
   
   ### ✅ APPROVED
   Content is approved for posting.
   
   OR
   
   ### ⚠️ APPROVED WITH MINOR CHANGES
   Content is conditionally approved pending minor adjustments:
   - [Change 1]
   - [Change 2]
   
   Re-review: Not required / Required
   
   OR
   
   ### 🔄 REVISIONS REQUIRED
   Content requires revisions before approval:
   
   **Must Fix**:
   1. [Critical issue 1]
   2. [Critical issue 2]
   
   **Should Fix**:
   1. [Issue 1]
   2. [Issue 2]
   
   **Nice to Have**:
   1. [Suggestion 1]
   
   Deadline for revised submission: [date]
   
   OR
   
   ### ❌ REJECTED
   Content cannot be approved. Reason:
   - [Critical failure reason]
   
   Next steps: [what to do]
   
   ## Feedback for Influencer
   
   [Constructive feedback message - see below]
   ```

8. **Create Feedback Message**

   ```markdown
   ## Feedback Message for Influencer
   
   ---
   
   Hi [Name]!
   
   Thanks for submitting your content for [Campaign]. We've reviewed it and have some feedback.
   
   ### What We Love ❤️
   
   - [Positive point 1]
   - [Positive point 2]
   - [Positive point 3]
   
   ### Changes Needed 📝
   
   Before we can approve, we need a few adjustments:
   
   **1. [Issue]**
   - What we see: [current state]
   - What we need: [required state]
   - Why: [brief explanation]
   
   **2. [Issue]**
   - What we see: [current state]
   - What we need: [required state]
   
   ### Suggestions (Optional)
   
   These aren't required, but might make the content even stronger:
   - [Suggestion 1]
   - [Suggestion 2]
   
   ### Timeline
   
   Please send the revised content by [date] so we can hit our posting window.
   
   Let me know if you have any questions! Happy to hop on a quick call if that's easier.
   
   Thanks again for your creativity!
   
   Best,
   [Name]
   
   ---
   ```

## Example Review

**User**: "Review this TikTok video submission for our protein powder campaign"

**Output**:

```markdown
# Content Review: @fitnessfiona TikTok

## Quick Summary

| Category | Score | Status |
|----------|-------|--------|
| Brand Alignment | 9/10 | ✅ |
| Message Accuracy | 7/10 | ⚠️ |
| Compliance | 5/10 | ❌ |
| Quality | 9/10 | ✅ |

**Decision**: ❌ REJECTED — **Reject (T1 · FTC Disclosure veto)**

> A missing/inadequate disclosure on sponsored content is the ART **T1 veto** — it forces a Reject, not a revise (FTC 16 CFR §255). The creator must fix the veto item and resubmit; the non-veto items below are required on resubmission.

## Issues Found

### Veto — forces Reject (Compliance)
1. **Missing disclosure** - No #ad or sponsored disclosure visible → **T1 veto → Reject**
   - Fix: Add #ad in caption and/or verbal disclosure in first 3 seconds

2. **Promo code not mentioned** - Brief required promo code "FIONA20"
   - Fix: Add verbal mention and caption inclusion

### Should Fix (Messaging)
1. **Missing key message** - "20g protein per serving" not mentioned
   - Fix: Add this stat when showing the product

## What's Great
- Authentic workout integration
- High production quality
- Engaging hook
- Great product showcase

## Feedback Message
[Generated constructive feedback for influencer]
```

## Review Checklist Template

```markdown
## Quick Review Checklist

### Must-Pass Items
- [ ] Disclosure visible and clear (#ad, #sponsored, etc.)
- [ ] No false/unsubstantiated claims
- [ ] Brand mentioned correctly
- [ ] Required hashtags included
- [ ] No competitor mentions
- [ ] Content is brand-safe

### Quality Check
- [ ] Hook captures attention (first 3 seconds)
- [ ] Audio/video quality acceptable
- [ ] Key messages communicated
- [ ] CTA is clear
- [ ] Authentic feel maintained

### Technical
- [ ] Correct format/dimensions
- [ ] Appropriate length
- [ ] Caption complete
- [ ] Links/codes correct
```

## Tips for Effective Reviews

1. **Be constructive** - Focus on solutions, not just problems
2. **Lead with positives** - Acknowledge what works
3. **Be specific** - "Add #ad to caption" not "fix disclosure"
4. **Explain why** - Help them understand the reasoning
5. **Respect creativity** - Don't over-edit their voice
6. **Be timely** - Quick reviews keep campaigns on track

## Reference Materials

- [skill-contract.md](../../references/skill-contract.md) — shared contract and Handoff Summary format.
- [state-model.md](../../references/state-model.md) — memory tiers and save-path conventions.
- [CONNECTORS.md](../../CONNECTORS.md) — keyless data recipes for the `~~` connector placeholders.
- C³ scoring: [c3-benchmark.md](../../references/c3-benchmark.md) and [c3/art-content-benchmark.md](../../references/c3/art-content-benchmark.md) — the ART Content rubric this review gates on, incl. the T1 (FTC disclosure) and T2 (claim integrity) veto items.
- [brief-generator](../../plan/brief-generator/SKILL.md) — the brief whose criteria this review checks against.
- [contract-helper](../../activate/contract-helper/SKILL.md) — bake content guidelines and approval terms into the agreement.
- [content-amplifier](../../convert/content-amplifier/SKILL.md) — amplify content once approved.
- [performance-analyzer](../../track/performance-analyzer/SKILL.md) — track how approved content performs.

## Next Best Skill

**Primary**: [contract-helper](../../activate/contract-helper/SKILL.md) — once content is approved (or once review feedback exposes a gap the agreement should cover), fold guidelines, usage rights, and approval terms into the partnership contract.

**Alternates** (same Activate family):
- [content-amplifier](../../convert/content-amplifier/SKILL.md) — when content is approved and ready to scale through paid or owned channels.
- [performance-analyzer](../../track/performance-analyzer/SKILL.md) — when the piece is live and you want to measure outcomes.

Termination note (visited-set): if a recommended skill has already been invoked this session, stop and report the chain as complete rather than re-running it. Cap any handoff chain at max-depth 3.
