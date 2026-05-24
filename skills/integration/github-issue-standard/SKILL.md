---
name: github-issue-standard
description: Mandatory format standard for ALL GitHub issues created by SpecWeave with checkable acceptance criteria and proper metadata. Use when creating GitHub issues, formatting issue content, or ensuring consistent issue structure. Covers user stories, epics, features, and increments.
---

# GitHub Issue Standard - Universal Format

**CRITICAL**: This is the **MANDATORY** format for ALL GitHub issues created by SpecWeave, whether for:
- User stories (individual us-*.md files)
- Epics/Features (FS-* folders)
- Increments (0001-* folders)
- Specs (spec-*.md files)

## Issue Title Format (MANDATORY)

### ✅ ONLY Allowed Title Formats

```
[FS-XXX][US-YYY] User Story Title    ← STANDARD (User Stories)
[FS-XXX] Feature Title               ← Rare (Feature-level only)
```

**Examples**:
- ✅ `[FS-059][US-003] Hook Optimization (P0)`
- ✅ `[FS-054][US-001] Fix Reopen Desync Bug (P0)`
- ✅ `[FS-048] Smart Pagination Feature`

### ❌ PROHIBITED Title Formats (NEVER USE)

```
[BUG] Title                          ← WRONG! Bug is a LABEL, not title prefix
[HOTFIX] Title                       ← WRONG! Hotfix is a LABEL
[FEATURE] Title                      ← WRONG! Feature is a LABEL
[DOCS] Title                         ← WRONG! Docs is a LABEL
[Increment XXXX] Title               ← DEPRECATED! Old format
```

**Why?** Type-based prefixes like `[BUG]` break traceability:
- Cannot link to Feature Spec (FS-XXX)
- Cannot link to User Story (US-YYY)
- Violates SpecWeave's data flow: `Increment → Living Docs → GitHub`

**What to do instead?**
1. Link work to a Feature (FS-XXX) in living docs
2. Create User Story (US-YYY) under that feature
3. Use GitHub **labels** for categorization: `bug`, `enhancement`, `hotfix`

### Validation

The GitHub client (`github-client-v2.ts`) enforces this:
- Rejects titles starting with `[BUG]`, `[HOTFIX]`, `[FEATURE]`, etc.
- Rejects deprecated `[Increment XXXX]` format
- Only allows `[FS-XXX][US-YYY]` or `[FS-XXX]` formats

---

## The Standard Format

### ✅ Required Elements

Every GitHub issue MUST include:

1. **Checkable Acceptance Criteria**
   - Use GitHub task checkbox format: `- [x]` or `- [ ]`
   - Include AC ID, description, priority, and testable flag
   - Example: `- [x] **AC-US4-01**: Description (P1, testable)`

2. **Checkable Tasks**
   - Link to increment tasks.md with GitHub URLs (not relative paths)
   - Use GitHub task checkbox format
   - Example: `- [x] [T-008: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-008-title)`

3. **Working GitHub URLs** (v5.0.0+ - NO _features folder)
   - Feature links: `https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031`
   - User story links: `https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031/us-004-*.md`
   - Task links: `https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#task-anchor`
   - Increment links: `https://github.com/owner/repo/tree/develop/.specweave/increments/0031`

   **Note**: Feature ID is DERIVED from increment (0031 → FS-031)

4. **Extracted Priority**
   - Extract from ACs (highest priority wins: P1 > P2 > P3)
   - Show ONLY if priority exists (don't show "undefined")
   - Example: `**Priority**: P1`

5. **NO Project Field**
   - Don't include `**Project**: ...` - not needed for GitHub issues
   - Project is determined by repository context

### ❌ Never Use

- ❌ Relative paths (`../../{project}/FS-031`)
- ❌ Undefined values (`**Priority**: undefined`)
- ❌ Project field in metadata
- ❌ Plain bullet points for ACs (must be checkboxes)
- ❌ Plain bullet points for tasks (must be checkboxes with links)

## Implementation

### UserStoryContentBuilder (✅ REFERENCE IMPLEMENTATION)

**File**: `plugins/specweave-github/lib/user-story-content-builder.ts`

This is the **gold standard** implementation. All other builders must follow this pattern.

**Key features**:
```typescript
// 1. Accept GitHub repo parameter
async buildIssueBody(githubRepo?: string): Promise<string>

// 2. Auto-detect repo from git remote
private async detectGitHubRepo(): Promise<string | null>

// 3. Extract priority from ACs
private extractPriorityFromACs(criteria: AcceptanceCriterion[]): string | null

// 4. Generate GitHub URLs (not relative) - v5.0.0+: No _features folder
const featureUrl = `https://github.com/${repo}/tree/develop/.specweave/docs/internal/specs/${project}/${featureId}`;

// 5. Convert task links to GitHub URLs
if (repo && taskLink.startsWith('../../')) {
  const relativePath = taskLink.replace(/^\.\.\/\.\.\//, '.specweave/');
  taskLink = `https://github.com/${repo}/tree/develop/${relativePath}`;
}
```

### Template

```markdown
**Feature**: [FS-031](https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031)
**Status**: complete
**Priority**: P1

---

## User Story

**As a** user
**I want** feature
**So that** benefit

📄 View full story: [`us-004-name.md`](https://github.com/owner/repo/tree/develop/.specweave/docs/internal/specs/{project}/FS-031/us-004-name.md)

---

## Acceptance Criteria

Progress: 4/6 criteria met (67%)

- [x] **AC-US4-01**: Description (P1, testable)
- [x] **AC-US4-02**: Description (P1, testable)
- [ ] **AC-US4-03**: Description (P2, testable)
- [ ] **AC-US4-04**: Description (P2, testable)

---

## Implementation Tasks

Progress: 3/6 tasks complete (50%)

**Increment**: [0031-name](https://github.com/owner/repo/tree/develop/.specweave/increments/0031-name)

- [x] [T-008: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-008-title)
- [x] [T-009: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-009-title)
- [ ] [T-010: Title](https://github.com/owner/repo/tree/develop/.specweave/increments/0031/tasks.md#t-010-title)

---

🤖 Auto-synced by SpecWeave
```

## Implementation

### Content Builders

All GitHub issue content is generated by these builders:

1. **UserStoryIssueBuilder** (`plugins/specweave-github/lib/user-story-issue-builder.ts`)
   - Creates issues from `us-*.md` files
   - Generates `[FS-XXX][US-YYY] Title` format
   - Extracts ACs and tasks as checkboxes
   - Uses GitHub URLs (not relative paths)

2. **GitHubFeatureSync** (`plugins/specweave-github/lib/github-feature-sync.ts`)
   - Syncs Features as GitHub Milestones
   - Syncs User Stories as GitHub Issues via UserStoryIssueBuilder
   - Universal Hierarchy: Feature → Milestone, User Story → Issue

### Commands

All GitHub sync commands use the Universal Hierarchy:

- `/sw-github:sync` - Sync increments via Feature/UserStory hierarchy
- `/sw-github:create-issue` - Create issue using standard format
- `/sw-github:update-user-story` - Update user story issue

## Validation Checklist

When creating/updating a GitHub issue, verify:

- [ ] Feature link is clickable GitHub URL (not `../../`)
- [ ] User story link is clickable GitHub URL
- [ ] All task links are clickable GitHub URLs
- [ ] ACs are checkable (GitHub checkboxes work in UI)
- [ ] Tasks are checkable (GitHub checkboxes work in UI)
- [ ] Priority shows actual value (P1/P2/P3) or is omitted
- [ ] No "Project: undefined" field
- [ ] Progress percentages are correct
- [ ] Increment link is clickable GitHub URL

## Benefits

- ✅ **Links work**: No more broken relative paths
- ✅ **Checkable**: ACs and tasks can be checked/unchecked in GitHub UI
- ✅ **Clean metadata**: No undefined values cluttering the issue
- ✅ **Consistent**: Same format across all issue types
- ✅ **Traceable**: Direct links to source files in repository

## When to Use

**Always!** This is the ONLY acceptable format for GitHub issues created by SpecWeave.

No exceptions. No shortcuts. Every issue follows this standard.

## Related Files

- **User Story Builder**: `plugins/specweave-github/lib/user-story-issue-builder.ts`
- **Feature Sync**: `plugins/specweave-github/lib/github-feature-sync.ts`
- **Example Issue**: https://github.com/anton-abyzov/specweave/issues/501
