---
name: git-best-practices
description: Generate comprehensive, detailed git commit messages following best practices with problem explanations for fixes and complete change lists for features. Use when committing changes, writing commit messages, or when user mentions git commit, staging changes, or version control.
version: 1.0.0
---

# Git Best Practices - Comprehensive Commit Messages

Generate detailed, professional commit messages that provide complete context about changes.

## Critical First Step: Always Verify Changes

Before generating any commit message, ALWAYS run these commands in order:

1. **Check repository status:**
```bash
git status
```

2. **View staged changes in detail:**
```bash
git diff --staged
```

3. **Check recent commit history:**
```bash
git log --oneline -5
```

4. **View last commit details:**
```bash
git show HEAD
```

5. **If needed, check specific file changes:**
```bash
git diff HEAD <filename>
```

NEVER generate a commit message without analyzing actual changes first.

## Commit Message Structure

### Header Format (Required)

```
type(scope): Brief description of main change
```

**Components:**
- **type**: Type of change (see types below)
- **scope**: Component/module/feature affected
- **description**: Clear, imperative mood, max 72 characters

### Body Format (Required - NOT Optional)

Always include comprehensive body with:
1. What changed (detailed list)
2. Why it changed (for fixes: what was the problem?)
3. How it works (technical implementation)
4. Impact on system/users

**NEVER create commit messages with just the header. Body is mandatory.**

## Commit Types

- **feat**: New feature or functionality
- **fix**: Bug fix or problem resolution
- **refactor**: Code restructuring without behavior change
- **docs**: Documentation changes
- **style**: Code formatting, whitespace, semicolons
- **test**: Adding or updating tests
- **chore**: Build process, dependencies, tooling
- **perf**: Performance improvements

## Detailed Requirements by Type

### FOR FIXES/BUGS (Critical)

Must include:

1. **Problem Description**
   - What was broken or not working
   - When/how the issue occurred
   - Impact on users/system

2. **Root Cause**
   - Why the problem existed
   - What was causing the issue

3. **Solution Approach**
   - How you fixed it
   - Why this approach was chosen

4. **Changes Made**
   - Detailed bullet list of modifications
   - Functions/files affected
   - Logic changes explained

5. **Verification**
   - Why this fixes the issue
   - What behavior is now correct

**Example Fix Format:**

```
fix(daily-limits): compare date portion only for reset detection

Problem:
Daily usage reset logic was comparing full timestamp strings including
time components, causing false mismatches when comparing dates across
different storage formats (with/without timezone info).

Root Cause:
Timestamps stored in different formats (YYYY-MM-DD vs YYYY-MM-DD HH:MM:SS)
were being compared as strings, causing date equality checks to fail even
when dates were actually the same day.

Solution:
Refactor to extract and compare only the date portion (YYYY-MM-DD) from
timestamps instead of full datetime strings.

Changes:
- Extract first 10 characters from lastResetDate and today strings
- Apply comparison logic to date portions in getDailyUsageFromCounter
- Apply same logic to incrementDailyUsage function
- Add clarifying comments about handling format variations

Verification:
This ensures consistent daily reset behavior regardless of timestamp
format variations and prevents false mismatches when comparing dates
across different storage formats.
```

### FOR FEATURES (Comprehensive)

Must include:

1. **New Functionality Overview**
   - What new capability is added
   - Purpose and use case

2. **Detailed Component List**
   - All new files/components created
   - API endpoints with descriptions
   - UI components with purpose
   - Database changes
   - Type/interface updates

3. **Implementation Details**
   - How components interact
   - Key technical decisions
   - Configuration changes

4. **Integration Points**
   - What existing code is affected
   - Dependencies added
   - Breaking changes if any

5. **Status/Next Steps**
   - What's complete
   - What's ready for integration
   - Future work needed

**Example Feature Format:**

```
feat(subscriptions): Add Phase 2 API endpoints for test subscriptions

New Functionality:
Complete backend API infrastructure for test subscription system allowing
whitelisted users to activate mock subscriptions without payment.

API Endpoints Created:
- GET /api/subscription/whitelist/check
  - Check if user is whitelisted for test subscriptions
  - Returns whitelist status and entry details
  - Respects ENABLE_TEST_SUBSCRIPTIONS feature flag
  - Returns 403 if feature disabled

- POST /api/subscription/mock-checkout
  - Create mock checkout session for whitelisted users
  - Validates whitelist access before proceeding
  - Returns session details and expiration timestamp
  - Simulates payment flow without actual charges

- POST /api/subscription/activate
  - Activate subscription after mock payment completion
  - Creates billing history record with mock payment details
  - Updates user subscription document in Firestore
  - Sends activation notification to user
  - Tracks upgrades from previous subscription plans
  - Handles plan switching logic

- GET /api/subscription/billing-history
  - Retrieve complete user billing history
  - Calculate total amount spent across all subscriptions
  - Get next billing date based on current plan
  - Optional: Include billing statistics and analytics

Type Updates:
- Extended BillingHistory interface to allow additional metadata fields
- Added MockCheckoutSession type for test subscription flow
- Updated SubscriptionStatus enum with test plan states

Configuration:
- ENABLE_TEST_SUBSCRIPTIONS flag controls feature availability
- Whitelist stored in Firestore collection: subscription_whitelist
- Mock payment expiration set to 24 hours

Phase 2 Status:
Core subscription APIs complete and ready for UI integration. Frontend
can now implement subscription selection, checkout flow, and billing
history display.
```

**Example Feature with UI Components:**

```
feat(dating): require profile picture for discovery features

Problem Solved:
Users without profile pictures were able to access dating features,
creating poor user experience and reducing match quality.

Implementation:
- Create DatingRequiresProfileModal component
  - Modal blocks users without profile pictures from dating features
  - Cannot be dismissed (no close button or backdrop click)
  - Follows AfterDark gradient styling pattern
  - Mobile-responsive design using existing imageUrl field

- Add auto-detection on /discover page
  - useEffect hook checks for imageUrl on page load
  - Automatically shows modal if profile picture missing
  - Prevents interaction with dating features until resolved

- Two user options in modal:
  1. Add profile picture - Redirects to /settings/profile
  2. Go back - Returns to previous page

Backend Validation (Double Security):
- Update /api/swipe/like endpoint
  - Validates imageUrl exists before processing like
  - Returns 400 error if profile picture missing

- Update /api/swipe/spark endpoint
  - Validates imageUrl exists before processing spark
  - Returns 400 error if profile picture missing

- Update /api/swipe/pass endpoint
  - Validates imageUrl exists before processing pass
  - Returns 400 error if profile picture missing

Security Approach:
Frontend modal provides immediate user feedback, backend validation
ensures no API calls can bypass the requirement even if frontend is
modified or bypassed.

Feature Scope:
- Only blocks dating/swipe-related features
- Other app features remain fully accessible
- User can navigate away and return to other sections

Exports:
- Export modal from components/modals/index.ts barrel file
- Added to modal registry for centralized management

Impact:
Ensures all dating feature users have profile pictures, improving
match quality and user experience in discovery features.
```

## Formatting Rules

### Structure Requirements

1. **Header Line:**
   - Max 72 characters
   - Lowercase type and scope
   - Imperative mood ("add" not "added")
   - No period at end

2. **Body Content:**
   - Blank line after header (required)
   - Max 72 characters per line
   - Use bullet points (- or *) for lists
   - Blank line between sections
   - Group related changes under headings

3. **Sections to Include:**
   - Problem/Purpose (for fixes/features)
   - Changes/Implementation (detailed list)
   - Impact/Verification (what this accomplishes)

### List Formatting

**Good:**
```
Changes:
- Create new UserProfile component
  - Add profile image upload
  - Add bio text editor
  - Add interests selection
- Update API endpoint /api/profile
  - Add image validation
  - Add bio character limit
```

**Bad:**
```
Changes:
- updated profile stuff
- fixed api
```

## Workflow Process

### Step 1: Verify Repository State

```bash
git status
```

Check:
- What files are staged
- What files are modified but unstaged
- Any untracked files

### Step 2: Review Staged Changes

```bash
git diff --staged
```

Analyze:
- Exact lines changed
- Functions modified
- New code added
- Code removed

### Step 3: Check Context

```bash
git log --oneline -5
git show HEAD
```

Understand:
- Recent commits in this branch
- Related changes
- Commit message patterns

### Step 4: Categorize Changes

Group changes by:
- File/component affected
- Type of change (API, UI, logic, config)
- Related functionality
- Dependencies

### Step 5: Generate Commit Message

Create comprehensive message including:
- Accurate type and scope from diff
- All changes observed in git diff
- Problem explanation (for fixes)
- Complete feature list (for features)
- Technical implementation details
- Impact and verification

### Step 6: Validate Message

Before finalizing, verify:
- [ ] All changed files are mentioned
- [ ] All new functionality is listed
- [ ] Problem is explained (for fixes)
- [ ] Technical details are included
- [ ] Message is comprehensive enough to review later
- [ ] No vague descriptions like "fix bug" or "update code"

## Validation Rules

### REJECT Messages That:

- ❌ Lack detailed body (header only)
- ❌ Use vague descriptions ("fix bug", "update code")
- ❌ Don't explain the problem (for fixes)
- ❌ Don't list all changes (for features)
- ❌ Missing technical details
- ❌ Can't be understood without reading code
- ❌ Don't match git diff output

### REQUIRE Messages To:

- ✅ Include comprehensive body
- ✅ Explain what and why
- ✅ List all changes in detail
- ✅ For fixes: Problem + Root Cause + Solution + Changes
- ✅ For features: Overview + Components + Implementation + Impact
- ✅ Match actual changes in git diff
- ✅ Be detailed enough for code review
- ✅ Provide complete context

## Templates

### Fix Template

```
fix(scope): Brief description of what was fixed

Problem:
[Describe what was broken, when it occurred, impact on users]

Root Cause:
[Explain why the problem existed, what was causing it]

Solution:
[Describe the approach taken to fix it]

Changes:
- [Detailed list of modifications]
- [Functions/files affected]
- [Logic changes explained]

Verification:
[Why this fixes the issue, what behavior is now correct]
```

### Feature Template

```
feat(scope): Brief description of new feature

Overview:
[What new capability is added, purpose and use case]

Components Created:
- [Component/file name]
  - [Description of what it does]
  - [Key functionality]
  - [Integration points]

API Endpoints:
- [METHOD] [path]
  - [What it does]
  - [Parameters/validation]
  - [Response format]

Implementation Details:
- [Technical decisions]
- [How components interact]
- [Configuration changes]

Impact:
[What this enables, what's ready for next phase]
```

### Refactor Template

```
refactor(scope): Brief description of refactoring

Purpose:
[Why refactoring was needed]

Changes:
- [List all structural changes]
- [Functions renamed/moved]
- [Code organization improvements]

Benefits:
[Improved maintainability, performance, readability]

Verification:
[Behavior unchanged, tests still pass]
```

## Examples from Real Commits

### Example 1: Subscription Feature

```
feat(subscriptions): Add Phase 2 API endpoints for test subscriptions

API Endpoints Created:
- GET /api/subscription/whitelist/check
  - Check if user is whitelisted
  - Returns whitelist status and entry details
  - Respects ENABLE_TEST_SUBSCRIPTIONS flag

- POST /api/subscription/mock-checkout
  - Create mock checkout session
  - Validates whitelist access
  - Returns session details and expiration

- POST /api/subscription/activate
  - Activate subscription after mock payment
  - Creates billing history record
  - Updates user subscription document
  - Sends activation notification
  - Tracks upgrades from previous plans

- GET /api/subscription/billing-history
  - Retrieve user billing history
  - Calculate total spent
  - Get next billing date
  - Optional billing statistics

Type Updates:
- Allow additional metadata fields in BillingHistory

Phase 2 complete: Core subscription APIs ready for UI integration
```

### Example 2: Date Comparison Fix

```
fix(daily-limits): compare date portion only for reset detection

Refactor daily usage reset logic to extract and compare only the date
portion (YYYY-MM-DD) from timestamps instead of full datetime strings.

Changes:
- Extract first 10 characters from lastResetDate and today strings
- Apply comparison logic to date portions in getDailyUsageFromCounter
- Apply same logic to incrementDailyUsage function
- Add clarifying comments about handling format variations

This ensures consistent daily reset behavior regardless of timestamp
format variations (e.g., with/without time component, timezone info)
and prevents false mismatches when comparing dates across different
storage formats.
```

### Example 3: Profile Picture Requirement

```
feat(dating): require profile picture for discovery features

- Create DatingRequiresProfileModal to block users without profile pictures
- Add auto-detection on /discover page with useEffect hook
- Modal shows when user lacks imageUrl, cannot be dismissed
- Two options: Add profile picture (redirects to settings) or Go back
- Update API endpoints with backend validation:
  * /api/swipe/like - validates imageUrl before processing
  * /api/swipe/spark - validates imageUrl before processing
  * /api/swipe/pass - validates imageUrl before processing
- Returns 400 error if profile picture missing (double security)
- Only blocks dating/swipe features, other features accessible
- Mobile compatible: uses existing imageUrl field
- Follows AfterDark gradient styling pattern
- Non-dismissible modal (no close button/backdrop click)
- Export modal from components/modals/index.ts barrel
```

## Integration with Commit Command

This skill works seamlessly with C:\Users\NATH\.claude\commands\commit.md

When user requests commit message:
1. Run git commands to verify changes
2. Analyze all staged files
3. Generate comprehensive message following patterns above
4. Validate message meets all requirements
5. Present for user review

## Key Principles

1. **Verification First**: Always check git diff before writing
2. **Comprehensive Detail**: Include all changes, no exceptions
3. **Problem Context**: For fixes, explain what was wrong
4. **Complete Lists**: For features, list all components
5. **Technical Depth**: Explain how things work
6. **Future Reference**: Message should be reviewable months later
7. **Accuracy**: Message must match actual git diff output

## Quality Checklist

Before finalizing any commit message:

- [ ] Ran git status to check staged files
- [ ] Ran git diff --staged to see exact changes
- [ ] Ran git log to check recent history
- [ ] Type and scope are accurate
- [ ] All changed files are mentioned
- [ ] Problem is explained (for fixes)
- [ ] All new functionality listed (for features)
- [ ] Technical implementation detailed
- [ ] Impact/verification included
- [ ] Message is comprehensive and detailed
- [ ] Future reviewers can understand without code
- [ ] No vague or generic descriptions
- [ ] Follows formatting rules (72 chars, bullets, sections)

Remember: A good commit message tells the complete story of what changed, why it changed, and how it works. It should be detailed enough that someone reviewing it months later can understand the change without reading the code.
