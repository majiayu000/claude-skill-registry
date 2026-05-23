---
name: paw-review-critic
description: Critically assesses generated review comments for usefulness, accuracy, and appropriateness, adding assessment sections.
---

# PAW Review Critic Skill

Critically assess generated review comments to help reviewers make informed decisions about what feedback to include, modify, or skip.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Prerequisites

Verify `ReviewComments.md` exists in `.paw/reviews/<identifier>/`.

Also verify access to all supporting artifacts:
- `ReviewContext.md` (PR metadata)
- `CodeResearch.md` (baseline understanding)
- `DerivedSpec.md` (PR intent)
- `ImpactAnalysis.md` (system-wide effects)
- `GapAnalysis.md` (categorized findings)

If ReviewComments.md is missing, report blocked status—Feedback Generation must complete first.

## Core Responsibilities

- Read and understand all generated review comments
- Critically evaluate each comment's usefulness and accuracy
- Consider alternative perspectives and trade-offs
- Add assessment sections to ReviewComments.md
- Provide recommendations (Include, Modify, Skip) with justification
- Help reviewer make informed decisions about feedback quality

## Process Steps

### Step 1: Read All Review Comments

Understand the complete feedback landscape:

**Load ReviewComments.md:**
- Read all inline comments
- Read all thread comments
- Read questions for author
- Understand summary comment framing

**Load Supporting Context:**
- Review GapAnalysis.md findings that generated each comment
- Reference CodeResearch.md for baseline patterns
- Check ImpactAnalysis.md for system-wide context
- Understand DerivedSpec.md intent

**Identify Relationships:**
- Note batched findings (multiple locations in one comment)
- Identify linked comments (related but separate)
- Understand categorization (Must/Should/Could)

### Step 2: Critical Assessment

For each review comment, evaluate multiple dimensions:

#### Usefulness Evaluation

Ask: "Does this comment truly improve code quality? Is it actionable?"

**High Usefulness:**
- Fixes actual bug with clear failure mode
- Prevents production issue (security, data loss, crash)
- Improves maintainability significantly with concrete benefits
- Adds essential test coverage for risky code
- Addresses critical design flaw

**Medium Usefulness:**
- Improves code quality (clarity, consistency)
- Adds useful tests for non-critical paths
- Enhances error handling for edge cases
- Improves documentation for complex code
- Suggests better patterns with clear advantages

**Low Usefulness:**
- Stylistic preference without concrete benefit
- Minimal impact on quality or maintainability
- Already addressed elsewhere in PR or codebase
- Over-engineering for current requirements
- Bikeshedding (arguing about trivial details)

#### Accuracy Validation

Ask: "Are evidence references correct? Is the diagnosis sound?"

**Verify:**
- File:line references point to actual code
- Diagnosis matches actual code behavior (not misread)
- Baseline pattern comparison is fair and relevant
- Impact assessment is realistic (not exaggerated)
- Best practice citation is appropriate for context
- Code suggestion would actually fix the issue

**Flag if:**
- Evidence references are incorrect or outdated
- Diagnosis misunderstands code intent
- Baseline pattern cited isn't actually analogous
- Impact is speculative without concrete evidence
- Suggestion would introduce new problems

#### Alternative Perspective Exploration

Ask: "What might the initial reviewer have missed? Are there valid reasons for the current approach?"

**Consider:**
- Project-specific context not captured in artifacts
- Time/complexity trade-offs for suggested change
- Intentional design decisions with valid rationale
- Performance/readability trade-offs
- Technical debt consciously accepted
- Platform/framework limitations

**Identify:**
- Cases where current approach might be deliberate
- Situations where "better" is subjective
- Comments that are too prescriptive vs exploratory
- Recommendations that conflict with other constraints

#### Trade-off Analysis

Ask: "Are there valid reasons to do it the current way? What are the costs of changing?"

**Evaluate:**
- Effort required vs benefit gained
- Risk introduced by change (new bugs, regressions)
- Complexity added by "better" solution
- Consistency with rest of codebase vs ideal pattern
- Timing (now vs later with more information)

**Balance:**
- Perfect vs good enough for current context
- Immediate needs vs future flexibility
- Code purity vs pragmatic delivery

### Step 3: Add Assessment Sections

Append assessment after each comment's rationale in ReviewComments.md:

**Assessment Structure:**
```markdown
**Assessment:**
- **Usefulness**: <High|Medium|Low> - <justification>
- **Accuracy**: <validation of evidence and diagnosis>
- **Alternative Perspective**: <other valid interpretations or approaches>
- **Trade-offs**: <reasons current approach might be acceptable>
- **Recommendation**: <Include as-is | Modify to... | Skip because...>
```

**CRITICAL - Where Assessments Go:**

| Add to ReviewComments.md | DO NOT Post Externally |
|-------------------------|------------------------|
| Append assessment sections after rationale | No GitHub posting |
| Keep assessments local to reviewer's workspace | Not visible to PR author |
| Use assessments to inform reviewer's decisions | No external platform posting |

**Why**: Assessments help the reviewer decide what feedback to give, but showing this internal evaluation process to the PR author would be confusing and potentially counterproductive.

**Example Assessment:**

```markdown
### File: `auth.ts` | Lines: 45-50

**Type**: Must
**Category**: Safety

Missing null check before accessing user.profile could cause runtime error.

**Suggestion:**
```typescript
if (user?.profile) {
  return user.profile.name;
}
return 'Anonymous';
```

**Rationale:**
- **Evidence**: `auth.ts:45` shows direct access to user.profile.name
- **Baseline Pattern**: Similar code in `auth.ts:120` uses null checks for user objects
- **Impact**: Null pointer exception if user profile not loaded
- **Best Practice**: Defensive programming - validate before access

**Assessment:**
- **Usefulness**: High - Prevents actual runtime crash. User profile loading is conditional based on auth provider, so null case is realistic.
- **Accuracy**: Evidence confirmed. auth.ts:45 does access user.profile.name without check. Baseline pattern at auth.ts:120 does use optional chaining for similar access.
- **Alternative Perspective**: Could argue that profile should always exist if user is authenticated, but auth provider variance makes this risky assumption.
- **Trade-offs**: Minimal cost to add check. No downside to defensive code here.
- **Recommendation**: Include as-is. Clear safety improvement with concrete failure mode.

**Posted**: ✓ Pending review comment ID: <id>
```

### Recommendation Guidelines

**Include as-is:**
- High usefulness + accurate diagnosis + no major alternatives
- Clear benefit with minimal cost
- Addresses concrete issue with evidence
- Aligns with codebase patterns
- Reviewer confident in recommendation

**Modify to...:**
- Core issue is valid but suggestion needs adjustment
- Tone could be more/less direct
- Could be batched with related comment
- Suggestion is too prescriptive vs suggesting exploration
- Evidence is correct but impact overstated

**Skip because...:**
- Low usefulness (stylistic preference, minimal impact)
- Inaccurate diagnosis or evidence
- Valid alternative explanation exists
- Already addressed elsewhere
- Cost outweighs benefit
- Not appropriate for this review cycle

## Assessment Guidelines

### Usefulness Calibration

**Avoid Grade Inflation:**
- Not every suggestion is "High" usefulness
- Style preferences are typically "Low" even if correct
- Medium is appropriate for incremental improvements

**Focus on Impact:**
- What actually breaks vs what could theoretically be better?
- User-facing impact vs internal code cleanliness?
- Maintainability boost that saves real time vs theoretical elegance?

**Consider Context:**
- Is this a critical production system or experimental prototype?
- Is this a hot path or rarely-executed edge case?
- Is this public API or internal implementation?

### Accuracy Rigor

**Verify Evidence:**
- Check that file:line references are current (not stale)
- Confirm code behavior matches description
- Validate that baseline pattern is truly analogous

**Challenge Assumptions:**
- Is the "problem" actually problematic in this context?
- Could the current code be intentionally designed this way?
- Is the suggestion actually an improvement or just different?

**Check Suggestions:**
- Would the proposed fix actually work?
- Would it introduce new issues (performance, complexity)?
- Is it compatible with the framework/platform?

### Alternative Perspective Depth

**Steelman, Don't Strawman:**
- Present the strongest case for the current approach
- Consider legitimate trade-offs, not just defend poor code
- Acknowledge when criticism is valid but timing might be wrong

**Common Valid Alternatives:**
- "Premature optimization" - current simple approach sufficient for now
- "Technical debt acknowledged" - team aware, will address later
- "Platform limitation" - workaround necessary given constraints
- "Readability trade-off" - more explicit code despite verbosity

### Trade-off Realism

**Quantify When Possible:**
- "Would require refactoring 5 files" vs "simple one-line fix"
- "Adds 10% performance overhead" vs "negligible impact"
- "Increases complexity from 3 conditionals to 8" vs "simplifies logic"

**Acknowledge Uncertainty:**
- "Unknown if this path is hot enough to matter"
- "Unclear if this pattern will generalize to future cases"
- "Would need profiling to confirm performance impact"

## Guardrails

**Advisory Only:**
- Assessments help reviewer decide, don't make final decisions
- Reviewer can override any recommendation
- Purpose is to inform, not to dictate

**Critical Thinking:**
- Question assumptions in generated comments
- Consider alternative interpretations
- Don't rubber-stamp every comment as useful

**Local Only:**
- NEVER post assessments to GitHub or external platforms
- Assessments remain in ReviewComments.md only
- Internal decision-making tool, not external communication

**Respectful Tone:**
- Assessment is about comment quality, not personal critique
- Focus on improving feedback, not judging the Feedback Generation skill
- Acknowledge when comments are well-crafted

**Context-Aware:**
- Reference all available artifacts for complete picture
- Consider project-specific patterns from CodeResearch.md
- Understand PR intent from DerivedSpec.md
- Factor in system-wide impacts from ImpactAnalysis.md

**Balanced Perspective:**
- Don't be reflexively negative or positive
- Some comments will be excellent, others questionable
- Honest assessment serves reviewer and PR author best

## Iteration Summary

After adding assessments to all comments, append an Iteration Summary section to ReviewComments.md:

```markdown
---

## Iteration Summary

### Comments to Update (Based on Critique)

| Original Comment | Recommendation | Update Guidance |
|------------------|----------------|-----------------|
| File: auth.ts L45-50 | Modify | Soften tone; acknowledge valid alternative |
| File: api.ts L88 | Skip | Stylistic preference, not actionable |
| File: db.ts L120 | Include as-is | High value, accurate |

### Counts
- **Comments to Include as-is**: X
- **Comments to Modify**: Y  
- **Comments to Skip**: Z (will not post to GitHub, retained in ReviewComments.md)

### Notes for Feedback Response
[Any specific guidance for the feedback skill when updating comments]
```

**Skip Clarification**: Comments marked "Skip" remain in ReviewComments.md for documentation but will NOT be posted to GitHub by `paw-review-github`. The reviewer can override by changing the recommendation before the feedback response pass.

## Validation Checklist

Before completing, verify:

- [ ] Assessment added for every inline comment
- [ ] Assessment added for every thread comment
- [ ] All assessments have all five components (Usefulness, Accuracy, Alternative Perspective, Trade-offs, Recommendation)
- [ ] Usefulness ratings calibrated (not inflated)
- [ ] Evidence validation performed (file:line references checked)
- [ ] Alternative perspectives genuinely considered
- [ ] Trade-offs realistically evaluated
- [ ] Recommendations actionable and justified
- [ ] Assessments remain in ReviewComments.md (NOT posted externally)
- [ ] Iteration Summary section appended with counts table
- [ ] Tone is respectful and constructive

## Completion Response

```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/ReviewComments.md (assessments added)
Status: Success

Iteration Summary:
- Include as-is: N comments
- Modify: M comments (with update guidance in assessments)
- Skip: K comments (retained in artifact, will not post to GitHub)

Next: Run paw-review-feedback in Critique Response Mode to finalize comments with **Final**: markers.
