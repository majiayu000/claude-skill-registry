---
name: paw-review-feedback
description: Transforms gap analysis findings into structured review comments with comprehensive rationale. Handles both initial draft generation and critique response iteration.
---

# PAW Review Feedback Skill

Transform gap analysis findings into structured review comments with comprehensive rationale sections that cite evidence, baseline patterns, impact, and best practices.

> **Reference**: Follow Core Review Principles from `paw-review-workflow` skill.

## Prerequisites

Verify these artifacts exist in `.paw/reviews/<identifier>/`:
- `ReviewContext.md` (PR metadata and parameters)
- `CodeResearch.md` (baseline codebase understanding)
- `DerivedSpec.md` (what the PR is trying to achieve)
- `ImpactAnalysis.md` (system-wide impact assessment)
- `GapAnalysis.md` (categorized findings with evidence)
- `CrossRepoAnalysis.md` (optional—only for multi-repo reviews)

If any required artifact is missing, report blocked status—earlier stages must complete first.

**Multi-repo detection**: Check if `CrossRepoAnalysis.md` exists. If present, incorporate cross-repo gaps into comment generation.

## Core Responsibilities

- Batch related findings into coherent comments (One Issue, One Comment principle)
- Transform findings into clear, actionable review comments
- Generate comprehensive rationale sections citing evidence, baseline patterns, impact, and best practices
- Create `ReviewComments.md` with all comments, rationale, and metadata
- **Critique Response Mode**: Update comments based on critic assessment, marking each with `**Final**:` status
- Enable tone adjustment while preserving evidence and IDs

**Note**: GitHub posting is handled by the `paw-review-github` skill after critique iteration completes.

## Process Steps

### Step 1: Batch Related Findings (One Issue, One Comment)

Group findings that share the same root cause:

**Batching Criteria:**
- Same underlying issue manifesting in multiple locations
- Related error handling gaps across a module
- Consistent pattern violations throughout changed files
- Missing tests for related functionality

**Batching Approach:**
- Create single comment referencing multiple file:line locations, OR
- Create linked comments (note relationship in comment text)
- Avoid scattering feedback for one logical issue across multiple disconnected comments

**Examples:**
- Multiple null checks missing in same class → One comment listing all locations
- Architectural concern spanning 3 files → One thread comment discussing the pattern
- Missing tests for several related methods → One comment about test coverage gap

### Step 1.5: Incorporate Cross-Repository Correlation Findings (Multi-Repo Only)

**Condition**: Only if `CrossRepoAnalysis.md` exists in the artifact directory.

When `CrossRepoAnalysis.md` is present, add cross-repo gaps to the findings list:

**Load Cross-Repo Gaps:**
1. Read `CrossRepoAnalysis.md` → extract "Cross-Repository Gaps" section
2. For each gap, create a finding entry with:
   - Severity from gap (Must/Should/Could)
   - Evidence from gap's file:line references
   - Cross-reference notation from the gap's related PR

**Cross-Repo Finding Format:**
```markdown
**Type**: Must (from CrossRepoAnalysis.md)
**Category**: Cross-Repository Coordination
**Files**: [repo-b/src/api/client.ts:8](repo-b/src/api/client.ts#L8)
**Issue**: Missing consumer update for `lastLogin` field
**Evidence**: 
  - Added in repo-a: [repo-a/src/types/user.ts:22](repo-a/src/types/user.ts#L22)
  - Missing in repo-b: [repo-b/src/api/client.ts](repo-b/src/api/client.ts)
**Cross-Reference**: (Cross-repo: see repo-a#123 for interface change)
```

**Routing Cross-Repo Comments:**
- Post cross-repo findings to the PR that needs to make the change
- Include cross-reference notation: `(Cross-repo: see owner/other-repo#NNN for [context])`
- Note deployment order in comment if relevant from CrossRepoAnalysis.md

### Step 2: Build Comment Objects

For each finding or batched group of findings, create structured comment:

**Required Fields:**
- **Type**: `inline` (line-specific) or `thread` (file/concept-level)
- **File(s) and line range(s)**: Specific locations from GapAnalysis.md
- **Severity**: Must/Should/Could (from GapAnalysis categorization)
- **Category**: Correctness, Safety, Testing, Maintainability, Performance, etc.
- **Description**: Clear, specific explanation of the issue
- **Suggestion**: Code example or recommended approach
- **Rationale**: (generated in next step)

**Inline vs Thread Determination:**

Use **Inline** for:
- Issue specific to particular lines of code
- Logic error in a function
- Missing check at a specific location
- Performance issue in a specific loop
- Test gap for a specific method

Use **Thread** for:
- Architectural concern across >3 files
- Missing integration tests spanning components
- Consistent pattern violation throughout the PR
- Cross-cutting concerns (logging, error handling approach)
- General discussion about design decisions

### Step 3: Generate Rationale Sections

For EVERY comment, create comprehensive rationale with four components:

**Evidence:**
- File:line references from GapAnalysis.md findings
- Specific code snippets showing the issue
- Concrete examples of the problem

**Baseline Pattern:**
- Reference existing code in the codebase to show how similar situations are handled
- Cite established conventions and patterns from the codebase
- Show consistency/inconsistency with existing code
- **Important**: Do NOT reference CodeResearch.md or other PAW artifacts in comments—cite actual file:line locations instead

**Impact:**
- Explain what could go wrong (for Must items: specific failure modes)
- Describe user/system impact of not addressing
- Note performance, security, or maintainability implications
- Reference impact findings from analysis where applicable
- **Important**: Do NOT reference ImpactAnalysis.md or other PAW artifacts in comments—describe impacts directly

**Best Practice Citation:**
- Reference industry best practices from review-research-notes.md (if available)
- Cite language/framework conventions
- Link to relevant documentation or style guides
- Note security/safety standards

**Example Rationale:**
```markdown
**Rationale:**
- **Evidence**: `auth.ts:45` shows user input passed directly to SQL query without validation
- **Baseline Pattern**: Similar code in `database.ts:120-130` uses parameterized queries
- **Impact**: SQL injection vulnerability allowing unauthorized data access or modification
- **Best Practice**: OWASP Top 10 - Always use parameterized queries for user input
```

### Step 4: Create ReviewComments.md

Generate comprehensive markdown document:

```markdown
---
date: <timestamp>
git_commit: <sha>
branch: <branch>
repository: <repo>
topic: "Review Comments for <PR/Branch>"
tags: [review, comments, feedback]
status: draft
---

# Review Comments for <PR Number or Branch Slug>

**Context**: GitHub PR #X OR Non-GitHub branch feature/...
**Base Branch**: <base>
**Head Branch**: <head>
**Review Date**: <date>
**Reviewer**: <git user>
**Status**: ⏳ Pending critique

## Summary Comment

<Brief, positive opening acknowledging the work and effort>

<Overview of feedback scope and organization>

**Findings**: X Must-address items, Y Should-address items, Z optional suggestions

---

## Inline Comments

### File: `path/to/file.ts` | Lines: 45-50

**Type**: Must
**Category**: Safety

<Clear explanation of the issue>

**Suggestion:**
```typescript
// Proposed fix or approach with code example
```

**Rationale:**
- **Evidence**: `file.ts:45` shows unchecked null access
- **Baseline Pattern**: Similar code in `file.ts:100` uses null checks before accessing properties
- **Impact**: Potential null pointer exception causing crash in production
- **Best Practice**: Defensive programming - validate inputs before use

---

### File: `path/to/another.ts` | Lines: 88

**Type**: Could
**Category**: Performance

<Suggestion for potential optimization>

**Suggestion:**
```typescript
// Optional improvement example
```

**Rationale:**
- **Evidence**: `another.ts:88` shows inefficient pattern
- **Baseline Pattern**: More efficient approach used in `optimized.ts:42`
- **Impact**: Minor performance improvement in non-critical path
- **Best Practice**: Optimization best practice reference

---

## Thread Comments

### File: `path/to/module/` (Overall Architecture)

**Type**: Should
**Category**: Maintainability

<Discussion about broader architectural or design pattern concern>

**Rationale:**
...

---

## Questions for Author

1. <Question about intent or design decision - reference specific file:line>
2. <Clarification needed on edge case handling>
```

**Key Requirements:**
- Summary must be positive and constructive
- Every comment has rationale with all four components
- File:line references for all evidence
- Code examples for non-trivial suggestions

## Critique Response Mode

When ReviewComments.md already contains Assessment sections (from `paw-review-critic`), enter Critique Response Mode to incorporate feedback and finalize comments.

### Detection

- Check if comments have `**Assessment:**` sections
- If assessments exist, this is a second pass to incorporate critique
- Skip to Critique Response Mode steps below

### Process

For each comment with an assessment:

1. **Preserve Original**: Keep the original comment text intact
2. **Include Critique**: The Assessment section remains as-is
3. **Add Updated Version**: Based on the recommendation:
   - **Include as-is**: Add `**Final**: ✓ Ready for GitHub posting`
   - **Modify**: Add `**Updated Comment:**` section with revised text addressing critique feedback, then `**Final**: ✓ Ready for GitHub posting`
   - **Skip**: Add `**Final**: Skipped per critique - [reason]` (comment remains in artifact but won't post to GitHub)

### Updated Comment Structure

```markdown
### File: `auth.ts` | Lines: 45-50

**Type**: Must
**Category**: Safety

[Original comment text - preserved exactly]

**Suggestion:**
[Original suggestion code]

**Rationale:**
[Original rationale]

**Assessment:**
- **Usefulness**: Medium - [critique justification]
- **Accuracy**: [validation]
- **Alternative Perspective**: [alternatives considered]
- **Trade-offs**: [trade-off analysis]
- **Recommendation**: Modify to soften tone

**Updated Comment:**
[Revised comment text incorporating critique feedback]

**Updated Suggestion:**
[Revised suggestion if needed]

**Final**: ✓ Ready for GitHub posting
```

### Skip Handling

For comments with `Recommendation: Skip`:
- Do NOT remove the comment from ReviewComments.md
- Add `**Final**: Skipped per critique - [reason from assessment]`
- These comments provide documentation but won't be posted to GitHub
- Reviewer can override by changing Final to "✓ Ready for GitHub posting"

### Critique Response Completion

After processing all comments with assessments:
- Update ReviewComments.md status from `draft` to `finalized`
- All comments must have `**Final**:` markers
- Report count of comments: Include as-is, Modified, Skipped

## Tone Adjustment

Support tone adjustments while preserving evidence and IDs:

**Default Tone:**
- Professional and constructive
- Inclusive language: "we", "let's", "this code" (not "you didn't")
- Balanced: acknowledge good work, suggest improvements
- Specific: cite exact locations and evidence

**Tone Adjustment Parameters:**
| Parameter | Low | High |
|-----------|-----|------|
| Directness | More diplomatic | More direct |
| Encouragement | Matter-of-fact | More encouraging |
| Formality | More casual | More formal |
| Conciseness | More explanatory | More concise |

**Adjustment Process:**
1. Accept tone parameters from reviewer
2. Regenerate comment TEXT ONLY (description + suggestion)
3. Preserve: File:line locations, rationale, evidence, categorization
4. Update ReviewComments.md with new text

## Guardrails

**No PAW Artifact References in Comments:**
- NEVER reference PAW artifacts (ReviewContext.md, CodeResearch.md, DerivedSpec.md, ImpactAnalysis.md, GapAnalysis.md, etc.) in comments
- These files are NOT committed to the branch and are NOT accessible to the PR submitter
- Instead: Cite actual codebase files with file:line references
- PAW artifacts are for YOUR internal use and for the reviewer's understanding only

**Rationale Required:**
- EVERY comment must have complete rationale section
- All four components (Evidence, Baseline Pattern, Impact, Best Practice) required
- No suggestions without justification

**Evidence-Based:**
- All recommendations informed by existing codebase patterns
- File:line references for all claims
- Code examples from actual codebase when citing patterns

**Human Control:**
- Reviewer can modify any comment before GitHub posting
- Reviewer can override Skip recommendations
- Final decisions rest with human reviewer

**Comprehensive Coverage:**
- ALL findings from GapAnalysis.md must be transformed into comments
- No cherry-picking or filtering
- Positive observations included in summary
- Questions documented in dedicated section

**One Issue, One Comment:**
- Related findings batched into single coherent comment
- Clear linking when related comments must be separate
- Avoid fragmenting feedback for same root cause

## Validation Checklist

### Initial Pass (Draft Generation)

Before completing initial pass, verify:

- [ ] All GapAnalysis.md findings transformed into comments
- [ ] Related issues batched appropriately (not scattered)
- [ ] Every comment has complete rationale (Evidence, Baseline Pattern, Impact, Best Practice)
- [ ] Code examples included for non-trivial suggestions
- [ ] Inline vs thread distinction applied correctly
- [ ] Summary comment is positive and constructive
- [ ] ReviewComments.md complete with all sections and metadata
- [ ] ReviewComments.md status is `draft`
- [ ] No PAW artifact references in comment text

### Critique Response Pass (Finalization)

Before completing critique response, verify:

- [ ] All comments with Assessment sections processed
- [ ] `**Final**:` marker added to every comment
- [ ] `**Updated Comment:**` added where Recommendation was Modify
- [ ] Skip reasons documented for all skipped comments
- [ ] ReviewComments.md status updated to `finalized`
- [ ] Comment counts accurate: Include as-is, Modified, Skipped

## Completion Response

**Initial Pass (Draft):**
```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/ReviewComments.md
Status: Draft - awaiting critique

Summary:
- Total comments generated: N
- Must: X, Should: Y, Could: Z
- Awaiting paw-review-critic assessment
```

**Critique Response (Finalized):**
```
Activity complete.
Artifact saved: .paw/reviews/<identifier>/ReviewComments.md
Status: Finalized - ready for GitHub posting

Summary:
- Comments ready for posting: X
- Comments modified per critique: Y
- Comments skipped per critique: Z

Next: Run paw-review-github to post finalized comments to GitHub pending review.
