---
name: gh-pr
description: Create, update, and comment on GitHub pull requests with focus on material impact, safety, and human reviewability
---

# GitHub PR Communication Skill

Use this skill for creating, updating, or commenting on GitHub pull requests. Focus on material impact, safe operations, and respecting busy reviewers.

## When to Use This Skill

- Creating PRs from feature branches
- Updating PR descriptions after significant changes
- Adding comments to communicate with reviewers
- Any PR communication task

## Announcement

Always announce at start:

```
"I'm using the gh-pr skill to <create|update|comment on> the pull request."
```

## Core Principles

1. **Safety first:** All PR bodies written to `.scratch/pr-bodies/` before use with `gh --body-file`
2. **Material impact:** Focus on why changes matter, not metrics or file counts
3. **Smart merge:** Detect manual edits, only update when changes are material
4. **Human-friendly:** Concise, warm tone; assume busy reviewer
5. **Flexible workflow:** Explicit commands when clear, smart routing when ambiguous

## File Structure

```
.scratch/pr-bodies/
  drafts/
    <slugified-title>.md          # Draft body before PR creation
  <pr-number>/
    metadata.json                  # PR metadata and state
    <timestamp>-body.md           # Timestamped snapshots of generated bodies
    <timestamp>-comment.md        # Comment drafts
```

### Metadata Schema

```json
{
  "pr_number": 123,
  "branch": "feature/add-skill",
  "base": "main",
  "title": "Add spotlight exclusion skill",
  "created_at": "2025-11-07T10:30:00Z",
  "last_generated_hash": "abc123def456",
  "last_updated_at": "2025-11-07T16:45:30Z",
  "manual_edits_detected": false
}
```

## Trigger Patterns

### Explicit Triggers (Always Honored)

- **"create a PR"** / **"open a PR"** → Create flow
- **"update the PR body/description"** → Update body flow
- **"comment on the PR"** / **"add a PR comment"** → Comment flow

### Ambiguous Triggers (Smart Routing)

**"update the PR":**

- No PR exists → Error: "No PR found for this branch. Did you mean to create one?"
- PR exists, no reviews → Update body
- PR exists, has reviews → Ask: "This PR has reviews. Update body or add comment?"

**"communicate the changes":**

- PR exists, no reviews yet → Update body
- PR exists, has reviews → Add comment (generates notifications)

## Operation Flows

### 1. Create PR

```
☐ Check if PR already exists
  - gh pr view --json number 2>/dev/null
  - If exists → error or route to update

☐ Gather information
  - Commits: git log <base>..HEAD
  - Check for PR template (.github/pull_request_template.md, etc.)
  - Check for CONTRIBUTING.md
  - Analyze commit messages and diffs

☐ Generate PR content
  - Title: from branch name or first commit (imperative mood, <72 chars)
  - Body:
    * Follow template structure if exists
    * Summary: 2-4 bullets of material impact
    * Test plan: if non-obvious
    * NO H1 heading (GitHub shows title separately)
    * NO metrics (# tests, # files, etc.)
    * Concise, warm tone

☐ Draft review
  - Write to .scratch/pr-bodies/drafts/<slug>.md
  - Show draft to user: "Here's the draft PR. Does this look good?"
  - Allow edits before creating

☐ Create PR
  - gh pr create --title "..." --body-file .scratch/pr-bodies/drafts/<slug>.md
  - Capture PR number from output

☐ Archive and track
  - mkdir -p .scratch/pr-bodies/<number>/
  - mv draft to <number>/<timestamp>-body.md
  - Write metadata.json with hash of generated body
  - rm .scratch/pr-bodies/drafts/<slug>.md
```

### 2. Update PR Body

```
☐ Verify PR exists
  - gh pr view --json number,body,title,state
  - Load metadata.json if exists
  - Check state (error if closed/merged unless user confirms)

☐ Detect manual edits
  - Hash current body: echo "$body" | shasum -a 256
  - Compare to last_generated_hash in metadata
  - If differs:
    * Compute diff: diff <(echo "$last_generated") <(echo "$current")
    * Analyze: whitespace-only vs content changes
    * If material: show diff, ask "Overwrite manual edits, merge, or cancel?"

☐ Check for material changes
  - Re-analyze full commit range: <base>..HEAD
  - Compare to previous analysis
  - If no material change:
    * "The current PR description is still accurate."
    * Skip update unless user forces

☐ Generate updated body
  - Follow same content guidelines as create
  - Re-analyze all commits in range

☐ Draft review
  - Write to .scratch/pr-bodies/<number>/<timestamp>-body.md
  - Show diff: current vs proposed
  - "Here's what would change. Look good?"

☐ Update PR
  - gh pr edit <number> --body-file <file>
  - Update metadata.json (hash, timestamp, manual_edits_detected)
```

### 3. Add PR Comment

```
☐ Verify PR exists
  - gh pr view --json number,title,reviews,comments
  - Check for review activity

☐ Determine comment content
  - Analyze recent commits since last update
  - Focus on: what changed and why
  - Common scenarios:
    * Responding to review feedback
    * Noting significant additions after initial review
    * Summarizing a batch of changes

☐ Draft comment
  - Write to .scratch/pr-bodies/<number>/<timestamp>-comment.md
  - Tone: conversational, helpful, concise (3-5 sentences)
  - Structure: "I've updated the PR to address..."
  - Show draft to user

☐ Post comment
  - gh pr comment <number> --body-file <file>
  - Optional: Update metadata.json with comment timestamp
```

## Decision Matrix: Update Body vs Comment

**Prefer UPDATE BODY when:**

- PR has no reviews/comments yet
- User explicitly says "update description/body"
- Material scope change that needs description rewrite

**Prefer COMMENT when:**

- PR has review activity (comments, requested changes)
- User mentions "responding to feedback"
- Batch of changes after initial review
- Want to notify watchers (comments generate notifications, body updates don't)

## Content Guidelines

### PR Title Format

- **Imperative mood:** "Add", "Fix", "Update", "Refactor"
- **Concise:** < 72 characters ideal
- **Capitalize** first word
- **No period** at end
- **Derive from:** Branch name (if semantic) or first commit message

### PR Body Structure

**When PR template exists:**

- Follow template structure exactly
- Fill sections based on commit analysis
- Preserve template comments/instructions

**When no template exists:**

```markdown
## Summary

- Material impact point 1
- Material impact point 2
- Material impact point 3 (if needed)

## Test plan

- How to verify the changes work
- Only if non-obvious or requires manual testing

[Optional sections based on context:]

## Breaking changes

## Migration notes

## Follow-up work
```

### Content Principles

**✅ DO:**

- Focus on material impact: "Enables pattern-based Spotlight exclusions for easier maintenance"
- Be concise yet warm: "This makes it easier to manage exclusions at scale."
- Explain why it matters, what problem it solves
- Include non-obvious testing steps

**❌ DON'T - Common Anti-Patterns:**

**Metrics (unless PR is specifically about them):**
- ❌ "Added 15 tests" → ✅ "Added test coverage for edge cases"
- ❌ "Modified 8 files across 3 modules" → ✅ Say nothing (diff shows this)
- ❌ "Reduced runtime from 2.5s to 1.2s" → ✅ Only if PR is about performance
- ❌ "Added 250 lines of code" → ✅ Never mention line counts
- ❌ "Test coverage increased to 85%" → ✅ Only if PR is about coverage

**Implementation details visible in diff:**
- ❌ "Created new `PatternExpander` class" → ✅ Say nothing (diff shows this)
- ❌ "Refactored into smaller functions" → ✅ Say nothing unless it's the PR's focus
- ❌ "Used async/await pattern" → ✅ Say nothing (implementation detail)
- ❌ "Added error handling" → ✅ Only if error handling is the PR's focus

**Over-explaining/verbose:**
- ❌ "This change significantly improves the developer experience by implementing a novel approach..."
- ✅ "Makes it easier to maintain exclusions at scale"
- ❌ "After careful consideration of multiple approaches, we decided to..."
- ✅ Just describe what it does and why it matters

**Other common mistakes:**
- ❌ Use H1 heading (GitHub shows title separately, causes duplication)
- ❌ List technologies used unless it's a new dependency worth noting
- ❌ Describe file structure changes unless it's an architectural shift
- ❌ Mention "following best practices" (assumed)
- ❌ Say "easy to" or "simple to" (condescending)

**The rule:** If a reviewer can see it in the diff or CI output, don't put it in the PR body unless it's the central focus of the PR.

### Following Repository Guidelines

**Search for PR templates:**

```
- .github/pull_request_template.md
- .github/PULL_REQUEST_TEMPLATE.md
- .github/PULL_REQUEST_TEMPLATE/*.md
```

**Search for CONTRIBUTING.md:**

```
- CONTRIBUTING.md
- .github/CONTRIBUTING.md
- docs/CONTRIBUTING.md
```

**If found:** Extract PR-related guidance (required info, checklists, style) and incorporate into body generation.

### Comment Content Guidelines

**Structure:**

```markdown
I've updated the PR to address the feedback:

- Point about what changed
- Another significant change
- Why these changes were made

[Optional: specific response to review comment if relevant]
```

**Tone:**

- Conversational but professional
- Acknowledge reviewers' input
- Explain reasoning when non-obvious
- Keep brief (3-5 sentences typical)

## Error Handling & Edge Cases

### Safety Checks

**Before creating PR:**

- ✓ Current branch is not main/master
- ✓ Branch has commits ahead of base
- ✓ gh CLI is installed and authenticated
- ✓ User has reviewed draft

**Before updating PR body:**

- ✓ PR exists and is open (warn if closed/merged)
- ✓ Manual edits check complete
- ✓ User has reviewed diff

**Before posting comment:**

- ✓ PR exists
- ✓ Comment is not empty
- ✓ User has reviewed content

### Common Errors

**No PR exists (when updating/commenting):**

```
Error: "No PR found for branch '<branch-name>'.
Would you like to create one?"

Action: Offer to route to create flow
```

**Multiple PRs for branch:**

```
1. gh pr list --head <branch> --state open
2. If exactly 1 open PR → use it
3. If 0 open PRs:
   - Check: gh pr list --head <branch> --state all
   - "No open PR found. Last PR was #123 (closed/merged)."
   - Offer to create new PR
4. If >1 open PR (rare):
   - "Found multiple open PRs: #123, #456. Which one?"
```

**Not on a branch / on main:**

```
Error: "Currently on '<branch>'.
PRs should be created from feature branches, not main/master."

Action: Stop, suggest creating a branch first
```

**gh CLI not available:**

```
Error: "GitHub CLI (gh) not found. Install with: brew install gh"
```

**gh not authenticated:**

```
Error: "GitHub CLI not authenticated. Run: gh auth login"
```

### Edge Cases

**Manual edits detected:**

```
1. Show diff: "The PR body has been manually edited. Here's what changed:"
2. Ask: "Overwrite manual edits, merge, or cancel?"
   - Overwrite: Replace with new generated body
   - Merge: Preserve manually-added sections
   - Cancel: Keep current body
```

**No material changes in update:**

```
"Analyzed commits - no material changes to scope or impact.
The current PR description is still accurate."

Action: Skip update unless user forces
```

**Draft in progress:**

```
"Found existing draft for '<title>'.
Use existing draft, create new, or cancel?"
```

**Scratch directory doesn't exist:**

```
mkdir -p .scratch/pr-bodies/drafts
```

## Change Detection Algorithm

```bash
# 1. Quick hash check
current_hash=$(gh pr view body -q .body < number > --json | shasum -a 256)
last_hash=$(jq -r .last_generated_hash .scratch/pr-bodies/ < number > /metadata.json)

# 2. If hashes match → no changes
if [ "$current_hash" = "$last_hash" ]; then
  echo "No manual edits detected"
  exit 0
fi

# 3. If hashes differ → compute diff
gh pr view body -q .body < number > --json > /tmp/current.md
cat .scratch/pr-bodies/ < number > / < last-timestamp > -body.md > /tmp/last.md
diff -u /tmp/last.md /tmp/current.md

# 4. Analyze diff
# - Whitespace only? → Not material
# - Content changes? → Material, set manual_edits_detected = true
```

## Integration with Other Skills

**working-in-scratch-areas:**

- All drafts go to `.scratch/pr-bodies/`
- Auto-creates directory structure

**git-preferences-and-practices:**

- Respects git workflow preferences
- Works with branch naming conventions

**Repository conventions:**

- Checks for ADRs and references them
- Links to docs/plans if design doc exists

## Example Workflows

### Creating a PR

```
User: "create a PR for this branch"

Claude: "I'm using the gh-pr skill to create the pull request."
[Analyzes commits: 5 commits adding spotlight exclusion patterns]
[Checks for templates: none found]
[Generates draft in .scratch/pr-bodies/drafts/add-spotlight-patterns.md]

Claude: "Here's the draft PR. The summary focuses on the pattern-based
approach and easier maintenance. Does this look good?"

[Shows draft content]

User: "yes"

Claude: [Creates PR #123]
"Created PR #123: Add spotlight exclusion patterns
https://github.com/user/repo/pull/123"
```

### Updating After Changes

```
User: "update the PR"

Claude: "I'm using the gh-pr skill to update the pull request."
[Checks PR #123]
[Hash check: no manual edits]
[Analyzes commits: 3 new commits adding monitoring tools]

Claude: "I've added 3 commits since the PR was created. The scope has
expanded to include monitoring tools. Should I update the description?"

User: "yes"

Claude: [Generates new body]
"Here's what would change in the description:

+ ## Monitoring
+ Includes live monitoring and activity analysis tools

Look good?"

User: "yes"

Claude: [Updates PR]
"Updated PR #123 description"
```

### Adding a Comment

```
User: "comment on the PR about the changes"

Claude: "I'm using the gh-pr skill to comment on the pull request."
[Checks PR #123: has 2 review comments]

Claude: "This PR has review comments. I'll add a comment about the
recent updates. Here's the draft:

---
I've updated the PR to address the feedback:
- Added input validation for pattern file paths
- Improved error messages for invalid patterns
- Updated tests to cover edge cases

The validation now catches malformed patterns before attempting expansion.
---

Look good?"

User: "yes"

Claude: [Posts comment]
"Added comment to PR #123"
```

## File Management

**Keep:**

- metadata.json (permanent record)
- Last 5 timestamped bodies/comments
- Current draft (if in progress)

**Clean up:**

- Completed drafts after PR creation
- Old timestamped files (optional: >30 days)

## Implementation Notes

**Hash algorithm:** Use `shasum -a 256` for consistency

**Timestamp format:** ISO 8601 with hyphens for filenames: `2025-11-07T10-30-00`

**Slugification:** Lowercase, hyphens, strip special chars: "Add Spotlight Skill" → "add-spotlight-skill"

**Base branch detection:**

```bash
# Try to detect from gh pr view first
base=$(gh pr view --json baseRefName -q .baseRefName 2> /dev/null)

# Fall back to common defaults
if [ -z "$base" ]; then
  if git show-ref --verify --quiet refs/heads/main; then
    base="main"
  else
    base="master"
  fi
fi
```
