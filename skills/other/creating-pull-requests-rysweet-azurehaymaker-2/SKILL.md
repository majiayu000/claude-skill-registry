---
name: "Creating Pull Requests"
description: "Creates high-quality pull requests with comprehensive descriptions, test plans, and context. Activates when user wants to create PR, says 'ready to merge', or has completed feature work. Analyzes commits and changes to generate meaningful PR descriptions."
allowed-tools: ["Bash", "Read", "Grep", "Glob"]
---

# Creating Pull Requests

You are activating pull request creation capabilities. Your role is to create comprehensive, reviewer-friendly PRs that accelerate the review process.

## When to Activate

This skill activates when:

- User says "create PR", "make pull request"
- User says "ready to merge" or "ready for review"
- Feature work is complete and tests pass
- User asks about PR best practices
- Significant changes are ready to share

## PR Philosophy

### Why Quality PRs Matter

- **Faster Reviews**: Clear context = quick approval
- **Better Feedback**: Reviewers understand intent
- **Knowledge Sharing**: PRs document decisions
- **Future Reference**: PRs are searchable history
- **Team Culture**: Quality PRs encourage quality code

### PR Best Practices

1. **Small & Focused**: One thing per PR
2. **Clear Context**: Why this change matters
3. **Test Coverage**: Prove it works
4. **Reviewer Friendly**: Easy to review
5. **Self-Review First**: Catch obvious issues

## PR Creation Process

### 1. Analyze Changes

Understand what's being submitted:

```bash
# Check current branch and status
git status
git branch --show-current

# See all commits since divergence from base branch
git log main..HEAD --oneline

# View full diff from base branch
git diff main...HEAD

# Check for staged/unstaged changes
git diff HEAD
git diff --staged
```

**Key Questions**:

- What feature/fix does this implement?
- What's the scope of changes?
- Are there related commits?
- Is everything committed?

### 2. Verify Quality

Ensure PR is ready:

```bash
# Run tests
npm test  # or pytest, cargo test, etc.

# Run linting
npm run lint  # or ruff check, cargo clippy, etc.

# Check builds
npm run build  # if applicable
```

**Pre-flight Checklist**:

- [ ] All tests pass
- [ ] Linting passes
- [ ] No unintended changes
- [ ] No debug code/comments
- [ ] No secrets/credentials
- [ ] Branch is up to date with main

### 3. Craft PR Description

Create comprehensive description:

```markdown
## Summary

[2-3 sentences describing what this PR does and why]

## Changes

- [Key change 1]
- [Key change 2]
- [Key change 3]

## Motivation

[Why this change is needed. Link to issue if applicable.]

## Implementation Details

[Any non-obvious decisions or tradeoffs]

## Testing

- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed
- [ ] Edge cases covered

## Screenshots/Videos

[If UI changes, include before/after screenshots]

## Breaking Changes

[If any, describe and provide migration guide]

## Rollout Plan

[For significant changes: how will this be deployed?]

## Related

- Fixes #[issue number]
- Related to #[issue number]
- Depends on #[pr number]
```

### 4. Create PR

Push and create:

```bash
# Push to remote (with tracking if needed)
git push -u origin feature-branch

# Create PR with gh CLI
gh pr create \
  --title "Clear, descriptive title" \
  --body "$(cat <<'EOF'
[PR description from step 3]
EOF
)"
```

### 5. Self-Review

Review your own PR first:

- Read the diff as if you're the reviewer
- Check for embarrassing mistakes
- Ensure all changes are intentional
- Add comments explaining complex parts

## PR Title Guidelines

### Format

```
<type>: <short description>
```

**Types**:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `refactor:` Code restructuring (no behavior change)
- `perf:` Performance improvement
- `test:` Adding/fixing tests
- `chore:` Maintenance tasks

**Examples**:

- ✅ `feat: Add user authentication with JWT`
- ✅ `fix: Resolve race condition in cache invalidation`
- ✅ `refactor: Extract payment logic into separate module`
- ❌ `Update stuff` (vague)
- ❌ `WIP` (not ready for review)
- ❌ `Fix bug` (which bug?)

### Good Titles

- **Descriptive**: What changed, not just where
- **Concise**: 50-72 characters
- **Action-oriented**: Start with verb
- **Specific**: Enough context to understand

## PR Description Template

### Comprehensive Template

```markdown
# [Feature/Fix Name]

## Summary

[1-2 paragraph overview of what this PR does and why it matters]

## Problem

[What problem does this solve? What was broken/missing?]

## Solution

[High-level approach taken. Why this approach?]

## Changes

### Added

- [New feature 1]
- [New feature 2]

### Changed

- [Modified behavior 1]
- [Modified behavior 2]

### Removed

- [Deleted code/feature]

### Fixed

- [Bug fix 1]
- [Bug fix 2]

## Implementation Details

### Key Decisions

1. **[Decision 1]**: [Why this choice?]
2. **[Decision 2]**: [Tradeoffs considered]

### Tradeoffs

- **Chose X over Y because**: [Reasoning]
- **Accepted limitation**: [What and why]

### Alternative Approaches Considered

- **Approach A**: [Why not chosen]
- **Approach B**: [Why not chosen]

## Testing

### Test Coverage

- Unit tests: [X% or list of tests]
- Integration tests: [Description]
- Manual testing: [What was tested]

### Test Plan for Reviewers

1. [Step 1]
2. [Step 2]
3. [Expected result]

### Edge Cases Tested

- [ ] Empty input
- [ ] Large input
- [ ] Concurrent requests
- [ ] Error conditions

## Performance Impact

- Memory: [Impact]
- CPU: [Impact]
- Network: [Impact]
- Database: [Query count changes]

## Security Considerations

- [ ] No sensitive data logged
- [ ] Input validation added
- [ ] Authentication/authorization checked
- [ ] No new security vulnerabilities

## Breaking Changes

[If any, list them with migration guide]

**Migration Guide**:
```

// Before
oldMethod();

// After
newMethod();

```

## Deployment Notes

- [ ] Database migrations needed
- [ ] Configuration changes required
- [ ] Dependencies updated
- [ ] Feature flags to toggle

## Screenshots

[For UI changes]

**Before**:
[Screenshot]

**After**:
[Screenshot]

## Checklist

- [ ] Tests pass locally
- [ ] Linting passes
- [ ] Documentation updated
- [ ] No console.log/print statements
- [ ] No commented-out code
- [ ] Self-reviewed the diff
- [ ] Breaking changes documented

## Related

- Closes #[issue]
- Related to #[issue/pr]
- Blocks #[issue/pr]
- Blocked by #[issue/pr]

---

Generated with Claude Code
```

### Minimal Template (Small PRs)

```markdown
## Summary

[Brief description of changes]

## Changes

- [Change 1]
- [Change 2]

## Testing

- [ ] Tests added/updated
- [ ] Manually tested

## Related

- Fixes #[issue]

---

Generated with Claude Code
```

## Size Guidelines

### Ideal PR Sizes

- **Small** (< 200 lines): Easy to review, fast approval
- **Medium** (200-500 lines): Manageable, good context
- **Large** (500-1000 lines): Needs extra effort to review
- **Too Large** (> 1000 lines): Consider splitting

### When to Split PRs

Split if:

- Multiple unrelated changes
- Can be deployed independently
- Large refactor + feature addition
- Different reviewers needed for different parts

**Example Split**:

```
Original: "Rewrite authentication and add OAuth"

Split into:
1. PR: Refactor existing auth to be more modular
2. PR: Add OAuth support on top of refactored auth
```

## Review Considerations

### Make It Easy to Review

**Add Comments to Complex Code**:

```python
def complex_algorithm(data):
    # Review note: Using binary search here because data is pre-sorted
    # from database query (see line 45). Time complexity: O(log n)
    result = binary_search(data, target)
    return result
```

**Break Into Reviewable Commits**:

```bash
# Good commit structure
git log --oneline
abc123 Add user authentication endpoint
def456 Add JWT token generation
ghi789 Add password hashing
jkl012 Add authentication middleware
```

**Highlight Important Changes**:

```markdown
## Areas Needing Special Attention

1. **Line 145-160**: Changed cache invalidation logic
   - Please verify timeout values are correct
2. **Line 230**: SQL query modified
   - Please check for N+1 query issues
```

### Respond to Feedback

When reviewer comments:

- Respond to all feedback
- Thank them for catching issues
- Explain decisions if they ask
- Mark resolved conversations
- Push fixes quickly

## Integration Points

### Invokes

- **Git Commands**: Via Bash tool
- **gh CLI**: For PR creation
- **Code Analysis**: To understand changes

### Escalates To

- **Reviewing Code Skill**: For self-review
- **Testing Code Skill**: To ensure tests exist

### References

- **PR Examples**: `Examples/GoodPRs/`
- **Team Guidelines**: Project-specific PR standards

## Example Workflow

````
User: "I'm done with the shopping cart feature. Can you create a PR?"

Creating Pull Requests Skill:

Let me analyze your changes and create a comprehensive PR.

## Analyzing Changes

Checking branch status...
Current branch: feature/shopping-cart
Commits since main: 8 commits
Files changed: 12 files
Lines changed: +450, -120

Running pre-flight checks...
✓ All tests pass (45 tests, 0 failures)
✓ Linting passes
✓ Branch up to date with main

## Change Analysis

From commits, this PR:
1. Adds shopping cart state management
2. Implements add/remove/update cart items
3. Adds cart persistence to localStorage
4. Creates cart UI components
5. Adds cart item quantity limits
6. Implements cart total calculation
7. Adds unit tests for cart logic
8. Updates integration tests

## Generated PR

Title: `feat: Add shopping cart functionality`

Description:
```markdown
# Shopping Cart Feature

## Summary

Implements a complete shopping cart system allowing users to add, remove,
and update product quantities. Cart persists across sessions using localStorage
and includes real-time total calculation with quantity limits.

## Changes

### Added
- Cart state management with Redux
- Cart UI components (CartIcon, CartDrawer, CartItem)
- localStorage persistence
- Cart item quantity limits (max 10 per item)
- Real-time total calculation
- Unit tests for cart logic (15 tests)

### Changed
- Product list components now include "Add to Cart" button
- Navigation header includes cart icon with item count

## Implementation Details

### Key Decisions

1. **localStorage for persistence**: Chose over cookies due to size limits.
   Cart can hold up to 50 items without exceeding localStorage quota.

2. **Redux for state management**: Considered React Context but Redux provides
   better debugging with DevTools and easier testing.

3. **Quantity limit of 10**: Based on product specs to prevent bulk orders
   through cart UI (bulk order form coming in separate PR).

### Tradeoffs

- **localStorage**: Simple but not synchronized across tabs. Users opening
  multiple tabs may see inconsistent cart state. Will address in future
  iteration with BroadcastChannel API.

## Testing

### Test Coverage
- Unit tests: 15 tests covering all cart operations
- Integration tests: Cart workflow from add to checkout
- Manual testing: Tested on Chrome, Firefox, Safari

### Test Plan for Reviewers
1. Add product to cart from product list
2. Open cart drawer (icon in header)
3. Increase/decrease quantities
4. Remove items
5. Refresh page - cart persists
6. Add >10 of same item - see error message

### Edge Cases Tested
- [ ] Empty cart behavior
- [ ] Maximum quantity limit
- [ ] localStorage quota exceeded
- [ ] Invalid product IDs
- [ ] Concurrent modifications

## Performance Impact

- Memory: +2KB bundle size (cart components)
- No additional network requests (localStorage only)
- Cart calculations are O(n) where n = cart items (typically < 20)

## Security Considerations

- [ ] Cart contents stored client-side only (no sensitive data)
- [ ] Product prices verified server-side at checkout
- [ ] Quantity limits enforced both client and server

## Screenshots

**Cart Icon with Badge**:
[Screenshot showing cart icon with item count]

**Cart Drawer**:
[Screenshot of open cart with items]

**Quantity Limit Error**:
[Screenshot showing error when exceeding limit]

## Checklist

- [x] Tests pass locally
- [x] Linting passes
- [x] Components documented
- [x] No console.log statements
- [x] Self-reviewed the diff

## Related

- Implements #234 (Shopping Cart Feature)
- Blocks #250 (Checkout Flow) - needs cart to exist first

---

Generated with Claude Code
````

## Next Steps

Ready to create this PR? I'll:

1. Push branch to remote
2. Create PR with description above
3. Add appropriate labels
4. Request reviewers (if specified)

Proceed?

```

## Quality Checklist

Before creating PR:
- [ ] Changes are committed
- [ ] Tests pass
- [ ] Linting passes
- [ ] Branch is up to date with main
- [ ] Description is comprehensive
- [ ] Title is clear and follows convention
- [ ] Test plan is included
- [ ] Screenshots added (if UI changes)
- [ ] Breaking changes documented (if any)
- [ ] Self-reviewed the diff

## Common Mistakes to Avoid

### 1. Vague Descriptions
❌ "Fixed bug"
✅ "Fixed race condition in cache invalidation causing stale data"

### 2. Too Large
❌ 2000+ line PR with refactor + features + fixes
✅ Split into multiple focused PRs

### 3. No Context
❌ Just code diff, no explanation
✅ Explain what, why, how, and tradeoffs

### 4. Not Self-Reviewing
❌ Submit immediately after coding
✅ Review your own diff first, catch obvious issues

### 5. Missing Tests
❌ "Works on my machine"
✅ Tests prove it works, reviewers can verify

### 6. No Screenshots
❌ UI changes with no visual proof
✅ Before/after screenshots show impact

## Success Criteria

Good PR:
- Reviewer understands it without asking questions
- Review happens in < 24 hours
- Minimal back-and-forth
- Approved without major changes
- Teaches reviewer something
- Future developers can understand decisions

## Related Capabilities

- **Skill**: "Reviewing Code" for self-review
- **Skill**: "Testing Code" to ensure test coverage
- **Tool**: `gh` CLI for GitHub integration
- **Documentation**: Team-specific PR guidelines

---

Remember: Your PR is communication. Make it easy for reviewers to say yes.
```
