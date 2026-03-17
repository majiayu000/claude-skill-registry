---
description: Templates for creating well-structured GitHub issues for bugs, features, and tasks
disable-model-invocation: false
---

# GitHub Issue Templates

Comprehensive templates for creating different types of GitHub issues. Use these templates to ensure consistency and completeness when creating issues.

---

## Bug Report Template

Use this template when reporting bugs, errors, or unexpected behavior.

```markdown
## Description

Brief, clear description of the bug in 1-2 sentences.

## Steps to Reproduce

1. Go to [specific page or action]
2. Click on [button/link]
3. Enter [specific data]
4. Observe the error

## Expected Behavior

What should happen when following the steps above.

## Actual Behavior

What actually happens. Include error messages, stack traces, or screenshots.

## Environment

- **Browser/OS**: Chrome 120 / macOS 14.2
- **Version/Branch**: v2.1.0 / main
- **Environment**: Production / Staging / Local

## Reproduction Rate

- [ ] Always (100%)
- [ ] Frequently (>50%)
- [ ] Sometimes (<50%)
- [ ] Rare (<10%)

## Screenshots/Logs

[Attach screenshots, error logs, or console output if applicable]

## Additional Context

- When did this start happening?
- Does it affect all users or specific users?
- Any recent changes that might be related?
- Workarounds discovered?

## Impact Assessment

- **Users Affected**: All / Subset / Single user
- **Severity**: Critical / High / Medium / Low
- **Business Impact**: [Describe impact on business operations]

## Suggested Priority

- [ ] P1 - Critical (blocks core functionality, affects all users)
- [ ] P2 - High (significant impact but has workaround)
- [ ] P3 - Normal (minor impact, can be scheduled)
```

### Example Bug Report

```markdown
## Description

Users cannot log in with SSO authentication, receiving "Invalid OAuth state" error.

## Steps to Reproduce

1. Navigate to https://app.example.com/login
2. Click "Login with SSO"
3. Enter corporate email
4. Redirected to error page with "Invalid OAuth state"

## Expected Behavior

User should be authenticated and redirected to dashboard.

## Actual Behavior

Error page displays "Invalid OAuth state parameter" and user cannot proceed.

## Environment

- **Browser/OS**: All browsers / All OS
- **Version/Branch**: v2.3.1 / production
- **Environment**: Production

## Reproduction Rate

- [x] Always (100%)

## Screenshots/Logs

```
Error: OAuth state mismatch
  at validateState (auth.js:45)
  at processCallback (oauth.js:123)
```

## Additional Context

- Started after deployment at 2:00 PM UTC today
- Affects ALL users attempting SSO login
- Username/password login still works
- Related to PR #123 which updated OAuth library

## Impact Assessment

- **Users Affected**: All SSO users (~80% of user base)
- **Severity**: Critical
- **Business Impact**: Users cannot access application, blocking all work

## Suggested Priority

- [x] P1 - Critical (blocks core functionality, affects all users)
```

---

## Feature Request Template

Use this template when proposing new features or enhancements.

```markdown
## Feature Description

Clear, concise description of the proposed feature in 1-2 sentences.

## Problem Statement

What problem does this feature solve? Who experiences this problem?

## Proposed Solution

Detailed description of how the feature should work:

- User interaction flow
- UI/UX considerations
- Technical approach (high-level)

## Acceptance Criteria

- [ ] User can [specific action]
- [ ] System responds with [expected behavior]
- [ ] Edge case [X] is handled properly
- [ ] Feature works on [platforms/browsers]

## User Stories

**As a** [type of user]
**I want** [goal/desire]
**So that** [benefit/value]

## Alternatives Considered

What other approaches were considered and why were they rejected?

## Dependencies

- Requires [feature/component]
- Blocks [other feature]
- Depends on [external service/library]

## Success Metrics

How will we measure if this feature is successful?

- [ ] [Metric 1]
- [ ] [Metric 2]

## Priority Suggestion

- [ ] P1 - Critical (essential for launch/key business need)
- [ ] P2 - High (important enhancement with clear value)
- [ ] P3 - Normal (nice-to-have improvement)

## Additional Context

- Mockups or wireframes
- User research or feedback
- Competitive analysis
- Technical considerations
```

### Example Feature Request

```markdown
## Feature Description

Add dark mode theme option to the application dashboard and user interface.

## Problem Statement

Users working in low-light environments or during evening hours find the bright interface uncomfortable and experience eye strain. Multiple users have requested a dark mode option in feedback surveys.

## Proposed Solution

Implement a theme toggle in user settings:

1. Add theme selector in user preferences (Settings > Appearance)
2. Offer "Light", "Dark", and "Auto (system)" options
3. Persist user preference to database
4. Apply theme across all dashboard components
5. Use CSS variables for easy theme switching

## Acceptance Criteria

- [ ] User can toggle between light and dark mode in settings
- [ ] User can select "Auto" to follow system theme
- [ ] Theme preference is saved per user account
- [ ] Theme persists across sessions and devices
- [ ] All dashboard components support both themes
- [ ] Text remains readable in both themes (WCAG AA contrast)
- [ ] Theme applies immediately without page refresh

## User Stories

**As a** dashboard user
**I want** to switch to dark mode
**So that** I can work comfortably in low-light environments without eye strain

## Alternatives Considered

1. **Single dark mode only**: Rejected - some users prefer light mode
2. **Browser extension**: Rejected - requires external dependency
3. **Time-based auto-switch**: Rejected - too complex for MVP

## Dependencies

- CSS variable system (already implemented)
- User preferences API (needs enhancement)
- Component library updates (all components must support theming)

## Success Metrics

- [ ] 30%+ of users enable dark mode within first month
- [ ] Reduced complaints about interface brightness
- [ ] Positive feedback in user surveys

## Priority Suggestion

- [ ] P1 - Critical
- [x] P2 - High (frequently requested feature with clear user value)
- [ ] P3 - Normal

## Additional Context

- Figma mockups: [link]
- User survey results: 67% requested dark mode
- Similar feature in competitor products
```

---

## Task Template

Use this template for development tasks, technical work, or non-user-facing improvements.

```markdown
## Objective

What needs to be accomplished? Be specific and actionable.

## Context

Why is this task needed? What's the background or motivation?

## Requirements

Detailed list of what must be completed:

- [ ] Requirement 1
- [ ] Requirement 2
- [ ] Requirement 3

## Technical Approach

High-level technical plan or considerations:

1. [Step or component 1]
2. [Step or component 2]
3. [Step or component 3]

## Files/Components Affected

- `path/to/file1.js`
- `path/to/file2.py`
- `component/Module`

## Testing Requirements

- [ ] Unit tests for [component]
- [ ] Integration tests for [workflow]
- [ ] Manual testing of [scenario]
- [ ] Performance testing if applicable

## Documentation Requirements

- [ ] Update README
- [ ] Update API docs
- [ ] Add inline code comments
- [ ] Update changelog

## Dependencies

- Requires completion of #[issue-number]
- Blocked by [external factor]
- Depends on [library/service]

## Definition of Done

- [ ] Implementation complete and tested
- [ ] Code reviewed and approved
- [ ] Tests added and passing
- [ ] Documentation updated
- [ ] No regressions introduced
- [ ] Deployed to staging/production

## Priority

- [ ] P1 - Critical (blocking other work)
- [ ] P2 - High (important technical improvement)
- [ ] P3 - Normal (standard development work)

## Estimated Effort

[Small / Medium / Large] or [hours/days estimate]
```

### Example Task

```markdown
## Objective

Refactor authentication middleware to support multiple OAuth providers (GitHub, Google, Microsoft).

## Context

Currently auth middleware only supports GitHub OAuth. New enterprise customers require Google and Microsoft SSO support. The existing implementation is tightly coupled to GitHub, making it difficult to extend.

## Requirements

- [ ] Abstract OAuth provider interface
- [ ] Implement provider-specific adapters for GitHub, Google, Microsoft
- [ ] Update configuration to support multiple providers
- [ ] Maintain backward compatibility with existing GitHub auth
- [ ] Add provider selection to login UI

## Technical Approach

1. Create `OAuthProvider` interface with standard methods
2. Extract GitHub-specific code into `GitHubProvider` adapter
3. Implement `GoogleProvider` and `MicrosoftProvider` adapters
4. Update middleware to route to appropriate provider based on config
5. Add provider selection dropdown to login page
6. Update user model to store provider type

## Files/Components Affected

- `src/middleware/auth.js` - Main refactoring
- `src/providers/github.js` - New file
- `src/providers/google.js` - New file
- `src/providers/microsoft.js` - New file
- `src/config/oauth.js` - Configuration updates
- `src/components/LoginForm.jsx` - UI updates
- `src/models/User.js` - Schema updates

## Testing Requirements

- [ ] Unit tests for each provider adapter
- [ ] Integration tests for full auth flow with each provider
- [ ] Test backward compatibility with existing GitHub users
- [ ] Test provider switching for users
- [ ] Manual testing of UI provider selection

## Documentation Requirements

- [ ] Update README with OAuth configuration examples
- [ ] Document provider interface in code
- [ ] Add setup guide for each OAuth provider
- [ ] Update environment variable documentation

## Dependencies

- OAuth credentials for Google and Microsoft (in progress)
- No blocking dependencies

## Definition of Done

- [ ] All three providers implemented and tested
- [ ] Existing GitHub auth continues to work
- [ ] Tests added for all providers (100% coverage)
- [ ] Code reviewed and approved
- [ ] Documentation complete
- [ ] Deployed to staging for QA testing
- [ ] No performance regressions

## Priority

- [ ] P1 - Critical
- [x] P2 - High (important for enterprise customer contracts)
- [ ] P3 - Normal

## Estimated Effort

Large (3-5 days)
```

---

## Documentation Update Template

Use this template for documentation improvements or additions.

```markdown
## Documentation Need

What documentation is missing or needs improvement?

## Target Audience

Who will use this documentation?
- [ ] End users
- [ ] Developers
- [ ] DevOps/Operations
- [ ] Contributors

## Scope

What should be documented:

- [ ] Topic 1
- [ ] Topic 2
- [ ] Topic 3

## Existing Documentation

What documentation already exists that relates to this?

## Proposed Changes

What should be added, updated, or removed:

1. [Change 1]
2. [Change 2]
3. [Change 3]

## Success Criteria

- [ ] Documentation is clear and accurate
- [ ] Examples are provided
- [ ] Common issues are addressed
- [ ] Links are functional

## Priority

- [ ] P1 - Critical (blocking users/developers)
- [ ] P2 - High (frequently needed info)
- [ ] P3 - Normal (nice-to-have)
```

---

## Quick Command to Create Issue

Use these commands with the templates above:

```bash
# Interactive issue creation (will prompt for all fields)
gh issue create

# Create from template (save template to file first)
gh issue create --body-file bug-report.md --title "Issue title" --label "P1,bug"

# Quick bug report
gh issue create \
  --title "Brief bug description" \
  --body "$(cat <<'EOF'
## Description
[Bug description]

## Steps to Reproduce
1. Step 1
2. Step 2

## Expected vs Actual
Expected: [...]
Actual: [...]
EOF
)" \
  --label "P1,bug"
```

---

## Template Selection Guide

| Issue Type               | Template to Use          | Labels to Add        |
|--------------------------|--------------------------|----------------------|
| Bug or error             | Bug Report               | `bug`, `P1/P2/P3`    |
| New feature              | Feature Request          | `enhancement`, `P2/P3` |
| Technical work           | Task                     | `task`, `P2/P3`      |
| Performance issue        | Bug Report               | `bug`, `performance` |
| Security vulnerability   | Bug Report (urgent)      | `security`, `P1`     |
| Documentation gap        | Documentation Update     | `documentation`, `P3` |
| Refactoring              | Task                     | `refactor`, `P3`     |
| Technical debt           | Task                     | `tech-debt`, `P3`    |

---

## Best Practices

### When Creating Issues

1. **Choose the right template** for the issue type
2. **Fill in all sections** - don't leave blanks
3. **Be specific and actionable** in descriptions
4. **Assign priority** based on impact and urgency
5. **Add relevant labels** beyond just priority
6. **Link related issues** and PRs
7. **Include reproduction steps** for bugs
8. **Define acceptance criteria** for features

### Template Customization

These templates can be customized per repository:
- Save templates to `.github/ISSUE_TEMPLATE/` directory
- GitHub will show them in the issue creation UI
- Customize sections based on team needs
- Add repository-specific fields

---

## Using Templates with Guided Commands

The `/gh-create-issue` command will help you use these templates interactively:

```bash
# Use guided workflow
/gh-create-issue

# The command will:
# 1. Ask for issue type (bug/feature/task)
# 2. Load appropriate template
# 3. Guide you through filling it out
# 4. Create the issue with proper labels and priority
```

---

## Golden Rules

1. **Always use a template** - ensures completeness
2. **Always assign priority** - P1/P2/P3
3. **Be thorough** - complete all sections
4. **Be specific** - actionable details
5. **Think about the reader** - they may have no context

---

## Related Skills

- Use `github-issues-quick-reference` skill for gh CLI commands
- Use `/gh-create-issue` for guided issue creation
- Use `/gh-triage` for prioritizing existing issues
