---
name: github-pr-review
description: Comprehensive GitHub PR review with inline suggestions, approval/rejection criteria, and technology-agnostic checklists. Triggers when reviewing PRs, analyzing code changes, or when user requests PR review. ALWAYS approve or request changes after review.
---

# GitHub PR Review with Suggested Changes

## Skill Purpose

This skill enables comprehensive GitHub pull request reviews with **actionable suggested changes** that developers can apply directly through GitHub's web UI using the "Commit suggestion" button.

**Key Features:**
- Code review with comprehensive checklists (security, quality, performance)
- Inline suggested changes using ````suggestion` blocks
- **Approval decision logic** (APPROVE / REQUEST_CHANGES / COMMENT)
- GitHub API integration for programmatic review comments
- Batch suggestion support for efficient fixes
- Integration with tech-specific skills (Unity, React Native, etc.)

## ⚠️ CRITICAL: Always Approve or Request Changes

**After every PR review, you MUST submit a review decision:**

```bash
# Approve (no critical/high issues)
gh pr review $PR --repo $REPO --approve --body "..."

# Request changes (critical/high issues found)
gh pr review $PR --repo $REPO --request-changes --body "..."

# Comment only (medium issues, can merge)
gh pr review $PR --repo $REPO --comment --body "..."
```

**See:** [Approval Criteria](references/approval-criteria.md) for decision tree.

## When This Skill Triggers

**Automatically triggers when:**
- User asks to "review PR" or "review pull request"
- User provides a GitHub PR URL for review
- User asks to "check PR" or "analyze PR changes"
- User requests code review with suggestions
- User asks "help review this PR"

**Manual trigger:**
- User explicitly invokes the skill with `/github-pr-review`

## Quick Reference

### GitHub Suggested Changes Syntax

```markdown
Add nullable directive at the top of the file.

\`\`\`suggestion
#nullable enable

namespace YourNamespace
\`\`\`
```

**Result:** Shows a "Commit suggestion" button in GitHub UI that applies the change when clicked.

## How It Works

### Step 1: Fetch PR Details

```bash
# Get PR information
gh pr view <PR_NUMBER> --repo <OWNER/REPO> --json title,body,files,commits

# Get PR diff
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>
```

### Step 2: Analyze Code Changes

- Review against coding standards (e.g., `theone-unity-standards`)
- Identify issues by severity (Critical, Important, Suggestions)
- Categorize issues by file and line number

### Step 3: Create Inline Suggestions

**Use GitHub API to add inline comments with suggestions:**

```bash
# Get latest commit ID
COMMIT_ID=$(gh pr view <PR> --repo <REPO> --json commits --jq '.commits[-1].oid')

# Add inline suggestion comment
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments \
  -f body="<suggestion text with \`\`\`suggestion block>" \
  -f commit_id="$COMMIT_ID" \
  -f path="<file_path>" \
  -F position=<line_number>
```

### Step 4: Add Summary Comment

Add a general comment explaining:
- Number of suggestions added
- How to apply suggestions (individual or batch)
- What issues will be resolved

## Suggestion Types

### 1. Single-Line Suggestions

```markdown
Fix access modifier.

\`\`\`suggestion
public sealed class MyClass
\`\`\`
```

### 2. Multi-Line Suggestions

```markdown
Add nullable directive and fix class.

\`\`\`suggestion
#nullable enable

namespace MyNamespace
{
    public sealed class MyClass
    {
        // class body
    }
}
\`\`\`
```

### 3. Complete File Replacements

For major refactoring, provide complete fixed file in expandable section:

```markdown
<details>
<summary>Click to expand: Complete fixed file</summary>

\`\`\`csharp
// entire file content
\`\`\`
</details>
```

## Best Practices

### ✅ DO:

1. **Use inline suggestions for fixable issues**
   - Syntax errors, formatting issues
   - Missing keywords, modifiers
   - Simple refactoring

2. **Add suggestions at correct line positions**
   - Use `gh pr diff` to find exact line numbers
   - Use `position` parameter (diff position, not file line number)

3. **Group related changes**
   - Combine related fixes in one suggestion block
   - Example: Add `#nullable enable` + `sealed` keyword together

4. **Provide context**
   - Explain WHY the change is needed
   - Reference coding standards or best practices

5. **Use batch suggestions for multiple fixes**
   - Tell developer about "Add suggestion to batch" option
   - Allows applying all suggestions in one commit

### ❌ DON'T:

1. **Don't suggest changes for non-fixable issues**
   - Architectural problems requiring discussion
   - Design pattern changes
   - Use regular comments for these

2. **Don't create overlapping suggestions**
   - Each suggestion should apply cleanly
   - Avoid suggesting same lines multiple times

3. **Don't suggest changes without explanation**
   - Always include WHY the change is needed
   - Link to relevant documentation or standards

## GitHub API Position Calculation

**Important:** The `position` parameter is the **diff position**, not the file line number.

```bash
# Get diff to see positions
gh pr diff <PR_NUMBER> --repo <OWNER/REPO>

# Position starts at 1 for first changed line
# Increments for each line in the diff (context + changes)
```

**Example:**
```diff
@@ -0,0 +1,10 @@
+namespace MyNamespace    # position: 1
+{                        # position: 2
+    public class Foo     # position: 3
+    {                    # position: 4
```

## Common Review Patterns

### Pattern 1: Missing Nullable Directive

**Issue:** Missing `#nullable enable`
**Location:** Line 1 (before namespace)
**Position:** Usually 1

```markdown
Add \`#nullable enable\` directive at the top of the file.

\`\`\`suggestion
#nullable enable

namespace YourNamespace
\`\`\`
```

### Pattern 2: Missing Sealed Keyword

**Issue:** Class should be `sealed`
**Location:** Class declaration line
**Position:** Find in diff

```markdown
Add \`sealed\` keyword to prevent inheritance.

\`\`\`suggestion
    public sealed class YourClass
\`\`\`
```

### Pattern 3: Fields to Properties

**Issue:** Public fields instead of properties
**Location:** Field declaration lines
**Position:** Find in diff

```markdown
Convert field to property with getter.

\`\`\`suggestion
        public Dictionary<string, int> MyProperty { get; } = new();
\`\`\`
```

### Pattern 4: Remove Region Comments

**Issue:** Using `#region` / `#endregion`
**Location:** Region block
**Position:** Find in diff

```markdown
Remove \`#region\` comments - code should be self-organizing.

\`\`\`suggestion
        private readonly UserDataManager userDataManager;

        public MyController(UserDataManager userDataManager)
        {
            this.userDataManager = userDataManager;
        }
\`\`\`
```

## Complete Workflow Example

```bash
# 1. Get PR details
PR_NUMBER=984
REPO="The1Studio/TheOneFeature"
COMMIT_ID=$(gh pr view $PR_NUMBER --repo $REPO --json commits --jq '.commits[-1].oid')

# 2. Review code (use theone-unity-standards skill)
# ... analyze code against standards ...

# 3. Add suggestion for file1
gh api \
  --method POST \
  -H "Accept: application/vnd.github+json" \
  /repos/$REPO/pulls/$PR_NUMBER/comments \
  -f body="Add \`#nullable enable\` directive.

\`\`\`suggestion
#nullable enable

namespace MyNamespace
\`\`\`" \
  -f commit_id="$COMMIT_ID" \
  -f path="path/to/file1.cs" \
  -F position=1

# 4. Add suggestion for file2
# ... repeat for each issue ...

# 5. Add summary comment
gh pr comment $PR_NUMBER --repo $REPO --body "## ✅ Suggestions Ready

I've added 6 inline suggestions. Go to Files Changed tab and click 'Commit suggestion' on each, or use 'Add suggestion to batch' to apply all at once."
```

## Integration with Other Skills

**Works best with:**
- `theone-unity-standards` - For Unity C# code reviews
- `theone-react-native-standards` - For React Native reviews
- `theone-cocos-standards` - For Cocos reviews
- `code-review` - For internal review practices (receiving feedback)
- `docs-seeker` - For finding latest library documentation

**Example workflow:**
1. User provides PR URL
2. Apply general checklists ([Review Checklists](references/review-checklists.md))
3. Trigger tech-specific skill (e.g., `theone-unity-standards`) for detailed analysis
4. Create inline suggestions using `github-pr-review`
5. Submit review decision (APPROVE/REQUEST_CHANGES) per [Approval Criteria](references/approval-criteria.md)
6. Developer applies suggestions via GitHub UI

## Review Process

### Step 0: Apply Review Checklists

Before diving into code, run through technology-agnostic checklists:

**See:** [Review Checklists](references/review-checklists.md)

1. 🔒 Security checklist (secrets, injection, auth)
2. ✅ Correctness checklist (logic, state, API)
3. 🧪 Testing checklist (coverage, quality)
4. 🧹 Quality checklist (structure, DRY)
5. ⚡ Performance checklist (queries, memory)
6. 📚 Documentation checklist

## Troubleshooting

### Issue: "404 Not Found" when creating suggestion

**Cause:** Wrong `position` value
**Fix:** Verify position in diff output

```bash
gh pr diff <PR> --repo <REPO> | less
# Count lines from @@ hunk header
```

### Issue: Suggestion doesn't show "Commit suggestion" button

**Cause:** Invalid ````suggestion` syntax
**Fix:** Ensure proper markdown formatting:
- Three backticks
- Word "suggestion" (lowercase)
- Proper code indentation inside block

### Issue: Suggestion applies but breaks code

**Cause:** Incorrect indentation or incomplete context
**Fix:**
- Match existing file indentation exactly
- Include enough context lines
- Test suggestion locally first

## Summary

This skill automates comprehensive GitHub PR reviews with actionable suggestions:

1. ✅ Applies technology-agnostic review checklists
2. ✅ Fetches PR details and diff
3. ✅ Analyzes code against standards (general + tech-specific)
4. ✅ Creates inline suggestions with ````suggestion` blocks
5. ✅ Uses GitHub API for programmatic comments
6. ✅ **Submits review decision (APPROVE/REQUEST_CHANGES)**
7. ✅ Enables one-click fixes via GitHub UI

**Result:** Faster, more efficient PR reviews with instant applicability AND clear approval status.

## Skill References

| Reference | Purpose |
|-----------|---------|
| [Approval Criteria](references/approval-criteria.md) | Decision tree for APPROVE/REQUEST_CHANGES |
| [Review Checklists](references/review-checklists.md) | Technology-agnostic security, quality, performance checklists |
| [API Reference](references/api-reference.md) | GitHub API commands and examples |
| [Workflow Examples](references/workflow-examples.md) | Complete review workflow examples |

## ClaudeAssistant Automated Review Service

For **The1Studio** repositories, you can trigger automated PR reviews via webhook:

### Triggering Automated Review

```bash
# Simply comment on any PR:
/review

# The webhook will:
# 1. Fetch PR files and diffs
# 2. Run Claude Code review with inline suggestions
# 3. Post review with "Apply suggestion" buttons
```

### How It Works

```
┌──────────────────────────────────────────────────────────────┐
│  GitHub PR Comment "/review"                                  │
│            ↓                                                  │
│  Webhook → github-review-service (port 16300)                │
│            ↓                                                  │
│  Fetch PR files → Generate prompt with diffs                 │
│            ↓                                                  │
│  claude-service (port 16304) → Claude Code analysis          │
│            ↓                                                  │
│  Post inline comments with ```suggestion blocks              │
│            ↓                                                  │
│  GitHub shows "Apply suggestion" button on each comment      │
└──────────────────────────────────────────────────────────────┘
```

### Inline Suggestions Format

The service generates suggestions in GitHub's format:

```markdown
🔵 **Suggestion**

Add `sealed` keyword to prevent inheritance.

\`\`\`suggestion
public sealed class MyClass
\`\`\`

**Category:** CodeQuality
```

**Result:** Users see "Apply suggestion" button and can commit fixes with one click.

### Service Architecture

| Service | Port | Purpose |
|---------|------|---------|
| github-review-service | 16300 | Webhook handler, review orchestration |
| claude-service | 16304 | Claude Code API gateway |
| postgres | 16305 | Review history storage |
| dashboard | 16302 | Monitoring UI |

### Deduplication

- Reviews are deduplicated by commit SHA
- Same commit won't be reviewed twice
- Merged PRs can trigger but may skip if already reviewed

### Manual API Trigger

```bash
# If webhook not working, trigger via API:
curl -X POST http://localhost:16300/api/review \
  -H "Content-Type: application/json" \
  -d '{
    "owner": "The1Studio",
    "repo": "YourRepo",
    "prNumber": 123,
    "installationId": 95277005
  }'
```

## External References

- [GitHub Suggested Changes](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request)
- [GitHub API - PR Review Comments](https://docs.github.com/en/rest/pulls/comments)
- [TheOne Studio Standards](../theone-unity-standards/SKILL.md)
- [ClaudeAssistant Repository](https://github.com/The1Studio/ClaudeAssistant)
