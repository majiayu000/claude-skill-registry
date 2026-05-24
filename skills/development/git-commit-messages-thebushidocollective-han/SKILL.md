---
name: git-storytelling-commit-messages
description: Use when writing commit messages that clearly communicate changes and tell the story of development. Helps create informative, well-structured commit messages that serve as documentation.
allowed-tools:
  - Bash
  - Read
---

# Git Storytelling - Commit Messages

This skill guides you in crafting commit messages that are clear, informative, and tell the story of your development process. Good commit messages are documentation that lives with your code.

## Core Principles

### The Purpose of Commit Messages

Commit messages serve multiple audiences and purposes:

- **Future developers** (including yourself) understanding why changes were made
- **Code reviewers** evaluating the intent and scope of changes
- **Project managers** tracking progress and understanding what was delivered
- **Automated tools** generating changelogs and release notes
- **Git tools** like blame, log, and bisect for debugging

### The Three-Part Structure

Effective commit messages follow a consistent structure:

1. **Subject Line**: Brief summary (50 characters or less)
2. **Body** (optional): Detailed explanation of what and why
3. **Footer** (optional): Issue references, breaking changes, co-authors

### The Subject Line Format

```
<type>: <description>

Examples:
feat: add user authentication system
fix: resolve race condition in payment processing
docs: update API documentation for v2 endpoints
```

## Commit Message Anatomy

### Subject Line Rules

**DO:**

- Start with a type prefix (feat, fix, docs, etc.)
- Use imperative mood ("add" not "added" or "adds")
- Keep it under 50 characters
- Don't end with a period
- Capitalize the first letter after the colon
- Be specific and descriptive

**DON'T:**

- Use vague terms like "update stuff" or "fix things"
- Include file names unless necessary
- Describe HOW you did it (that's what the code shows)
- Use past tense
- Be too generic

### Body Guidelines

The body should explain:

- **What** changed (briefly, the code shows details)
- **Why** the change was needed
- **Any side effects** or implications
- **Alternatives** considered
- **Context** that isn't obvious from the code

Format:

- Wrap at 72 characters per line
- Use bullet points for multiple items
- Separate from subject with a blank line
- Use proper paragraphs for complex explanations

### Footer Elements

```
Refs: #123, #456
Closes: #789
Breaking Change: API endpoint /users now requires authentication
Co-Authored-By: Jane Doe <jane@example.com>

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Commit Types

### feat: New Features

Use when adding new functionality or capabilities.

```
feat: add password reset functionality

Implement password reset flow with email verification:
- Generate secure reset tokens
- Send reset emails with expiration
- Validate tokens before allowing password change
- Log password reset events for security audit

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### fix: Bug Fixes

Use when correcting defects or unexpected behavior.

```
fix: prevent duplicate order submission

Add client-side debouncing and server-side idempotency check
to prevent users from accidentally submitting the same order
multiple times when clicking quickly.

Closes: #234

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### docs: Documentation

Use for documentation-only changes.

```
docs: add architecture decision record for database choice

Document why we chose PostgreSQL over MongoDB for our
primary datastore, including performance benchmarks and
team expertise considerations.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### refactor: Code Restructuring

Use when improving code without changing behavior.

```
refactor: extract authentication logic into middleware

Move authentication checks from individual route handlers
into reusable middleware to reduce duplication and improve
maintainability.

No functional changes to authentication behavior.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### test: Testing Changes

Use when adding or modifying tests.

```
test: add integration tests for payment flow

Add end-to-end tests covering:
- Successful payment processing
- Failed payment handling
- Refund processing
- Webhook event handling

Improves test coverage from 65% to 82%.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### perf: Performance Improvements

Use for changes that improve performance.

```
perf: optimize database query in user dashboard

Replace N+1 query pattern with single JOIN query, reducing
dashboard load time from 2.3s to 0.4s for users with 100+
items.

Added database index on user_id and created_at columns.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### style: Formatting Changes

Use for whitespace, formatting, missing semicolons, etc.

```
style: format code with prettier

Apply prettier formatting across all TypeScript files
to maintain consistent code style. No functional changes.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### chore: Maintenance Tasks

Use for routine tasks, dependency updates, build changes.

```
chore: upgrade dependencies to latest stable versions

Update all npm packages to resolve security vulnerabilities:
- express: 4.17.1 -> 4.18.2
- axios: 0.21.1 -> 1.4.0
- jest: 27.0.6 -> 29.5.0

All tests passing after upgrade.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Code Examples

### Example 1: Feature with Context

```
feat: implement webhook signature verification

Add HMAC-SHA256 signature verification for incoming webhooks
to ensure requests are authentic and haven't been tampered with.

Implementation details:
- Validate signature from X-Webhook-Signature header
- Use timing-safe comparison to prevent timing attacks
- Return 401 for invalid signatures
- Log suspicious webhook attempts

Security measure required before production launch.

Refs: #567

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 2: Fix with Root Cause

```
fix: resolve memory leak in event listener cleanup

Event listeners were being added on component mount but not
removed on unmount, causing memory to accumulate and browser
to slow down after multiple navigation cycles.

Root cause: Missing cleanup function in useEffect hook.

Solution: Return cleanup function that removes all event
listeners when component unmounts.

This bug affected users who navigated the app extensively
without refreshing, particularly noticeable after 10+ page
transitions.

Closes: #892

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 3: Refactor with Motivation

```
refactor: replace callback hell with async/await

Convert nested callback-based error handling to async/await
pattern for improved readability and maintainability.

Before: 5 levels of nested callbacks
After: Linear async/await flow

Benefits:
- Easier to understand error handling
- Reduced cognitive load when reading code
- Simpler to add new steps to the flow
- Better stack traces for debugging

No behavior changes, all existing tests pass.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 4: Breaking Change

```
feat: migrate to v2 API with breaking changes

Update API client to use v2 endpoints with improved
error handling and response format.

BREAKING CHANGE: Response format has changed
- Old: { data: {...}, status: "ok" }
- New: { result: {...}, success: true }

Migration guide:
1. Update response handlers to use 'result' instead of 'data'
2. Check 'success' boolean instead of status string
3. Error responses now include 'error.code' field

All internal services updated. Third-party integrators
will need to update their code.

Refs: #1001

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 5: Performance Optimization

```
perf: implement Redis caching for frequently accessed data

Add Redis cache layer for user profile data that changes
infrequently but is accessed on every request.

Metrics:
- Cache hit rate: 94% after 1 hour of traffic
- Average response time: 450ms -> 45ms
- Database load: Reduced by 80%

Cache invalidation strategy:
- Expire after 1 hour
- Invalidate on profile update
- Fallback to database on cache miss

Configuration via REDIS_URL environment variable.

Refs: #445

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 6: Security Fix

```
fix: sanitize user input to prevent XSS attacks

Escape HTML entities in user-generated content before
rendering to prevent cross-site scripting attacks.

Vulnerability: User could inject <script> tags in profile
bio field, which would execute in other users' browsers.

Fix: Use DOMPurify library to sanitize all user input
before storing and rendering.

Affected fields:
- User profile bio
- Comment content
- Custom status messages

Security severity: High
No known exploitation in production.

Closes: #778

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 7: Configuration Change

```
chore: configure automatic dependency updates

Set up Dependabot to automatically check for and create
PRs for dependency updates on a weekly schedule.

Configuration:
- Check npm dependencies weekly
- Auto-merge patch updates after tests pass
- Require manual review for minor/major updates
- Group updates by dependency type

This will help us stay current with security patches
and reduce manual maintenance burden.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Example 8: Revert

```
revert: roll back Redis caching implementation

Revert "perf: implement Redis caching for frequently accessed data"

Rolling back due to cache invalidation bugs causing stale
data to be served to users. The caching strategy needs to be
redesigned to properly handle all update scenarios.

Issues discovered:
- Partial profile updates don't invalidate cache
- Race condition between cache write and DB write
- Cache stampede under high load

Will re-implement with fixes in follow-up PR.

Refs: #445

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## When to Use This Skill

Use this skill when:

- Writing commit messages for any code change
- Creating commits during development workflow
- Preparing commits for code review
- Contributing to open source projects
- Working on team projects with shared git history
- Documenting important technical decisions
- Creating release notes or changelogs
- Using git bisect to debug issues
- Teaching others about git best practices
- Establishing team git conventions

## Best Practices

1. **Write the commit message before committing** - Thinking about the message helps clarify what you're committing

2. **Use the imperative mood** - "Add feature" not "Added feature" or "Adds feature"

3. **Separate subject from body with blank line** - Required by many git tools

4. **Limit subject line to 50 characters** - Forces you to be concise and thoughtful

5. **Wrap body at 72 characters** - Keeps messages readable in various tools

6. **Explain the why, not the what** - Code shows what changed, message explains why

7. **Reference issues and PRs** - Creates traceability between code and requirements

8. **Use conventional commit format** - Enables automated changelog generation

9. **Include breaking changes in footer** - Critical for semantic versioning

10. **Mention side effects** - Alert others to non-obvious consequences

11. **List co-authors when pairing** - Give credit where due

12. **Be specific about scope** - "fix: resolve login bug" not "fix: bug in auth"

13. **Describe the problem solved** - Not just the solution implemented

14. **Include relevant metrics** - Performance improvements, test coverage, etc.

15. **Use consistent terminology** - Match terms used in codebase and documentation

## Common Pitfalls

1. **Vague subject lines** - "fix bug" tells us nothing useful

2. **Including too much detail in subject** - Save details for the body

3. **Using past tense** - "Fixed bug" instead of "fix bug"

4. **Missing body explanation** - Non-obvious changes need context

5. **Writing for yourself only** - Remember others will read this

6. **Describing implementation instead of intent** - Focus on the why

7. **Forgetting to reference issues** - Breaks traceability

8. **Inconsistent commit types** - Mix of feat/feature/add makes history messy

9. **No blank line between subject and body** - Breaks formatting in many tools

10. **Subject line ends with period** - Unnecessary and wastes character limit

11. **Writing essay-length commit messages** - Be concise but complete

12. **Not updating commit message when amending** - Old message may no longer be accurate

13. **Generic messages like "updates" or "changes"** - These provide zero value

14. **Putting file names in subject** - Usually obvious from the diff

15. **Missing breaking change warnings** - Can break downstream consumers

## Resources

### Git Documentation

- [Git Commit Guidelines](https://git-scm.com/book/en/v2/Distributed-Git-Contributing-to-a-Project)
- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [Angular Commit Message Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)

### Tools

- `git commit` - Standard commit command
- `git commit --amend` - Modify the last commit message
- `git log --oneline` - View abbreviated commit history
- `git log --format=fuller` - See complete commit information
- `git show <commit>` - View full commit details
- `git rebase -i` - Edit historical commit messages

### Checking Your Messages

```bash
# View recent commit messages
git log --oneline -10

# See full commit message with diff
git show HEAD

# Check if subject line is too long
git log --format="%h %s" | awk 'length($0) > 52 { print }'

# View all commit messages from current branch
git log main..HEAD --format="%B"

# See commits by author
git log --author="Your Name" --format="%h %s"
```

### Message Templates

Create a commit message template:

```bash
# Create template file
cat > ~/.gitmessage << EOF
# <type>: <subject>

# <body>

# <footer>

# Type can be:
#    feat     (new feature)
#    fix      (bug fix)
#    refactor (refactoring code)
#    style    (formatting, missing semicolons, etc)
#    test     (adding missing tests)
#    docs     (changes to documentation)
#    chore    (updating build tasks, dependencies, etc)
#    perf     (performance improvement)
EOF

# Configure git to use template
git config --global commit.template ~/.gitmessage
```

### Pre-commit Hooks

Enforce message format with commit-msg hook:

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore|perf):"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "Error: Commit message must start with type prefix"
    echo "Example: feat: add new feature"
    exit 1
fi

# Check subject line length
subject=$(echo "$commit_msg" | head -n1)
if [ ${#subject} -gt 50 ]; then
    echo "Warning: Subject line exceeds 50 characters"
    echo "Length: ${#subject}"
fi

exit 0
```

### Related Skills

- **git-storytelling-commit-strategy**: When to commit and how often
- **git-storytelling-branch-strategy**: Managing branches for clear development narratives
- **code-reviewer**: How good commit messages improve code review

## Advanced Patterns

### Multi-Component Changes

When a change affects multiple components:

```
feat: add user notification system

Implement real-time notifications across the application:

Backend changes:
- Add WebSocket server for push notifications
- Create notification storage in database
- Implement notification API endpoints

Frontend changes:
- Add notification bell icon to header
- Create notification panel component
- Connect to WebSocket for live updates

Changes span both client and server to deliver complete
notification feature.

Refs: #234, #235, #236

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Bug Fix with Test

When fixing a bug, include test information:

```
fix: handle null values in date formatting

The date formatter would throw exception when passed null,
causing the entire page to crash.

Fix: Add null check and return empty string for null dates.

Test: Added unit test to verify null handling and edge cases
for undefined, empty string, and invalid date formats.

Before: Application crashed on null dates
After: Gracefully handles all invalid date inputs

Closes: #567

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

### Dependency Update with Migration Notes

```
chore: upgrade React 17 to React 18

Update React to version 18 for improved concurrent rendering
and automatic batching features.

Migration steps performed:
1. Updated react and react-dom to 18.2.0
2. Replaced ReactDOM.render with createRoot
3. Updated test configuration for new rendering API
4. Verified all components work with new concurrent features

Breaking changes addressed:
- Updated enzyme to React 18 compatible version
- Replaced deprecated lifecycle methods
- Fixed tests that relied on synchronous rendering

All tests passing, no visual regressions detected.

Refs: #789

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Conclusion

Well-crafted commit messages are an investment in your project's future. They serve as documentation, aid in debugging, facilitate code review, and tell the story of how your software evolved. By following these guidelines and making thoughtful commit messages a habit, you'll create a git history that is valuable, searchable, and maintainable.

Remember: Your commit messages are documentation that lives with your code forever. Make them count.
