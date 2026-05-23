---
name: code-change-summarizer
description: "Generates clear and structured pull request descriptions from code changes. Use when Claude needs to: (1) Create PR descriptions from git diffs or code changes, (2) Summarize what changed and why, (3) Document breaking changes with migration guides, (4) Add technical details and design decisions, (5) Provide testing instructions, (6) Enhance descriptions with security, performance, and architecture notes, (7) Document dependency changes. Takes code changes as input, outputs comprehensive PR description in Markdown."
---

# Code Change Summarizer

Generate clear, structured pull request descriptions from code changes.

## Workflow

### 1. Analyze Code Changes

**Gather code changes:**
- Git diff output
- Modified files list
- Commit messages
- Related issue numbers

**Understand the changes:**
- Read through all modified files
- Identify what changed (added/modified/removed/fixed)
- Understand the purpose of changes
- Note any patterns or themes

**Categorize changes:**
- **Feature additions:** New functionality
- **Bug fixes:** Issue resolutions
- **Refactoring:** Code improvements without behavior changes
- **Documentation:** Doc updates
- **Tests:** Test additions or modifications
- **Dependencies:** Package updates
- **Configuration:** Config or build changes

### 2. Create Initial Summary

**Write a clear title:**

Format: `[Type] Brief description (max 72 characters)`

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `refactor:` Code refactoring
- `docs:` Documentation
- `test:` Tests
- `chore:` Maintenance
- `perf:` Performance
- `style:` Code style
- `ci:` CI/CD
- `build:` Build system

**Examples:**
- `feat: Add user authentication with OAuth2`
- `fix: Resolve memory leak in data processor`
- `refactor: Simplify error handling logic`

**Write summary paragraph:**
- 2-3 sentences
- Explain what and why
- Use active voice
- Be concise and clear

**Example:**
```
This PR adds OAuth2 authentication to the user login system. The change
improves security by using industry-standard authentication and enables
single sign-on with external providers.
```

### 3. Document Changes

**List changes by category:**

**Added:**
- New features or functionality
- New files or components
- New API endpoints

**Modified:**
- Changed behavior or implementation
- Updated configuration
- Refactored code

**Removed:**
- Deprecated features
- Deleted files
- Removed dependencies

**Fixed:**
- Bug fixes
- Issue resolutions
- Error corrections

**Example:**
```markdown
## Changes

### Added
- OAuth2 authentication flow
- User session management
- Login/logout endpoints

### Modified
- User model to include OAuth tokens
- Authentication middleware
- Database schema

### Fixed
- Session timeout not working correctly
- Memory leak in token refresh
```

### 4. Identify Breaking Changes

**Check for breaking changes:**
- API signature changes
- Removed functionality
- Changed behavior
- Configuration changes
- Database schema changes
- Dependency updates with breaking changes

**Document each breaking change:**

**Format:**
```markdown
## Breaking Changes

⚠️ **[Breaking change description]**

**Impact:** [Who/what is affected]

**Migration Guide:**
1. [Step 1]
2. [Step 2]

**Before:**
```[language]
// Old code
```

**After:**
```[language]
// New code
```
```

**Example:**
```markdown
## Breaking Changes

⚠️ **Authentication endpoint signature changed**

**Impact:** All API clients must update their authentication calls.

**Migration Guide:**
1. Update authentication endpoint from `/auth/login` to `/auth/oauth/login`
2. Include `provider` parameter in request body
3. Handle new response format with OAuth tokens

**Before:**
```javascript
POST /auth/login
{ "username": "user", "password": "pass" }
```

**After:**
```javascript
POST /auth/oauth/login
{ "username": "user", "password": "pass", "provider": "google" }
```
```

### 5. Add Technical Details

**Explain implementation approach:**
- High-level technical approach
- Key algorithms or patterns used
- Important implementation details

**Document design decisions:**
- Why this approach was chosen
- Alternatives considered
- Trade-offs made

**Note architecture changes:**
- New components or modules
- Changed relationships
- Updated data flow

**Example:**
```markdown
## Technical Details

### Implementation Approach
Implemented OAuth2 using the Authorization Code flow with PKCE for enhanced
security. The authentication flow is handled by a new `AuthService` that
manages token exchange and refresh.

### Key Design Decisions
- **OAuth2 over SAML:** Chose OAuth2 for better mobile support and simpler
  implementation
- **PKCE extension:** Added PKCE to protect against authorization code
  interception attacks
- **Token storage:** Store refresh tokens in secure HTTP-only cookies

### Architecture Changes
- Added new `AuthService` layer between controllers and OAuth provider
- Introduced `TokenManager` for token lifecycle management
- Updated database schema to store OAuth provider information
```

### 6. Document Dependencies

**List dependency changes:**

**Added dependencies:**
- Package name and version
- Why it was added
- What it's used for

**Updated dependencies:**
- Old version → New version
- Why it was updated
- Any breaking changes

**Removed dependencies:**
- Package name
- Why it was removed
- What replaced it (if anything)

**Example:**
```markdown
## Dependencies

### Added
- `passport@0.6.0` - OAuth2 authentication library
- `passport-google-oauth20@2.0.0` - Google OAuth2 strategy

### Updated
- `express@4.17.1` → `express@4.18.2` - Security patches and bug fixes
- `jsonwebtoken@8.5.1` → `jsonwebtoken@9.0.0` - Updated for Node 18 support

### Removed
- `bcrypt@5.0.1` - Replaced by OAuth2, no longer needed for password hashing
```

### 7. Provide Testing Instructions

**Write step-by-step testing guide:**

**Format:**
```markdown
## Testing

### How to Test
1. [Setup step]
2. [Action to perform]
3. [Expected result]
4. [Edge case to verify]

### Test Coverage
- Added [X] unit tests
- Added [Y] integration tests
- Current coverage: [Z]%

### Manual Testing Checklist
- [ ] Test scenario 1
- [ ] Test scenario 2
- [ ] Test edge case 1
```

**Example:**
```markdown
## Testing

### How to Test
1. Start the application: `npm start`
2. Navigate to `/login`
3. Click "Sign in with Google"
4. Complete OAuth flow in popup
5. Verify you're redirected back and logged in
6. Check that session persists after page refresh

### Test Coverage
- Added 15 unit tests for AuthService
- Added 8 integration tests for OAuth flow
- Current coverage: 87% (up from 82%)

### Manual Testing Checklist
- [ ] Google OAuth login works
- [ ] Session persists across page refreshes
- [ ] Logout clears session correctly
- [ ] Token refresh works when token expires
- [ ] Error handling for failed OAuth
```

### 8. Enhance with Context

**Add security considerations:**
- Security improvements made
- Security implications
- Vulnerabilities addressed
- Security review status

**Add performance impact:**
- Expected performance changes
- Benchmark results
- Optimization details
- Resource usage changes

**Add architecture notes:**
- Architectural patterns used
- System design changes
- Integration points
- Scalability considerations

**Example:**
```markdown
## Security Considerations

### Improvements
- ✅ Implemented PKCE to prevent authorization code interception
- ✅ Store refresh tokens in HTTP-only cookies to prevent XSS
- ✅ Added rate limiting on authentication endpoints
- ✅ Validate OAuth state parameter to prevent CSRF

### Security Review
- [ ] Security team review pending
- [ ] Penetration testing scheduled

## Performance Impact

### Expected Changes
- Login time: ~500ms (OAuth redirect adds latency)
- Token validation: <10ms (cached in memory)
- Database queries: +2 per login (OAuth token storage)

### Optimizations
- Implemented token caching to reduce database hits
- Added connection pooling for OAuth provider requests

## Architecture Notes

### Patterns Used
- **Strategy Pattern:** Different OAuth providers (Google, GitHub, etc.)
- **Factory Pattern:** Token creation and validation
- **Middleware Pattern:** Authentication checks

### Integration Points
- Integrates with existing User model
- Hooks into session management middleware
- Compatible with existing authorization system
```

### 9. Add Documentation Notes

**List documentation updates:**
```markdown
## Documentation

- [ ] Updated README with OAuth setup instructions
- [ ] Added API documentation for new endpoints
- [ ] Updated environment variables guide
- [ ] Added OAuth provider configuration guide
- [ ] Updated changelog
```

### 10. Link Related Issues

**Reference related issues:**
```markdown
## Related Issues

Closes #123
Fixes #456
Related to #789
```

### 11. Review and Refine

**Review the PR description:**
- Is the summary clear?
- Are all changes documented?
- Are breaking changes highlighted?
- Are testing instructions complete?
- Is context sufficient?

**Refine for clarity:**
- Remove unnecessary details
- Add missing information
- Improve wording
- Fix formatting

**Verify completeness:**
- All sections filled out
- No placeholders left
- Links work
- Code examples correct

## Output Format

Generate a complete PR description in Markdown:

```markdown
# [Type] Brief description

## Summary
[2-3 sentence overview]

## Changes

### Added
- [Item 1]
- [Item 2]

### Modified
- [Item 1]

### Fixed
- [Item 1]

## Breaking Changes
[If any, with migration guide]

## Technical Details

### Implementation Approach
[Explanation]

### Key Design Decisions
- [Decision 1]
- [Decision 2]

### Architecture Changes
[Description]

## Dependencies

### Added
- [Package] - [Reason]

### Updated
- [Package] - [Reason]

## Testing

### How to Test
1. [Step 1]
2. [Step 2]

### Test Coverage
- [Details]

### Manual Testing Checklist
- [ ] [Item 1]
- [ ] [Item 2]

## Security Considerations
[Details]

## Performance Impact
[Details]

## Architecture Notes
[Details]

## Documentation
- [ ] [Item 1]
- [ ] [Item 2]

## Related Issues
Closes #[number]

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
```

See [pr-templates.md](references/pr-templates.md) for detailed templates.

## Best Practices

### Summary
- Keep it concise (2-3 sentences)
- Explain what and why
- Use active voice
- Be specific

### Changes
- Group by type (Added/Modified/Removed/Fixed)
- Be specific but concise
- Use bullet points
- Link to related issues

### Breaking Changes
- Clearly mark with ⚠️
- Provide migration guide
- Show before/after examples
- Explain impact

### Technical Details
- Explain approach
- Document decisions
- Note architecture changes
- Keep it relevant

### Testing
- Provide clear instructions
- Include expected results
- List edge cases
- Note coverage changes

### Context
- Add security notes
- Note performance impact
- Explain architecture changes
- Document dependencies

## Common Scenarios

### Scenario 1: Feature Addition

**Input:** Code adding user authentication

**Output:**
```markdown
# feat: Add user authentication with OAuth2

## Summary
This PR implements OAuth2 authentication for user login. Users can now
sign in using their Google or GitHub accounts, improving security and
user experience.

## Changes

### Added
- OAuth2 authentication flow
- Google and GitHub OAuth providers
- User session management
- Login/logout endpoints

### Modified
- User model to include OAuth tokens
- Database schema for OAuth data

## Testing

### How to Test
1. Start app: `npm start`
2. Navigate to `/login`
3. Click "Sign in with Google"
4. Complete OAuth flow
5. Verify successful login

### Test Coverage
- Added 15 unit tests
- Added 8 integration tests
- Coverage: 87%
```

### Scenario 2: Bug Fix

**Input:** Code fixing memory leak

**Output:**
```markdown
# fix: Resolve memory leak in data processor

## Summary
This PR fixes a memory leak in the data processor that was causing
memory usage to grow unbounded during long-running operations.

## Changes

### Fixed
- Memory leak in DataProcessor.process()
- Improper cleanup of event listeners
- Unclosed database connections

## Technical Details

### Root Cause
Event listeners were not being removed after processing completed,
causing references to processed data to remain in memory.

### Solution
- Added proper cleanup in finally block
- Implemented connection pooling
- Added memory monitoring

## Testing

### How to Test
1. Run long-running process: `npm run process-large-dataset`
2. Monitor memory usage
3. Verify memory stays stable

Fixes #456
```

### Scenario 3: Refactoring

**Input:** Code refactoring error handling

**Output:**
```markdown
# refactor: Simplify error handling logic

## Summary
This PR refactors error handling across the application to use a
consistent pattern, improving maintainability and reducing code
duplication.

## Changes

### Modified
- Centralized error handling in ErrorHandler class
- Updated all controllers to use new error handling
- Simplified error response format

### Removed
- Duplicate error handling code in controllers
- Inconsistent error response formats

## Technical Details

### Implementation Approach
Introduced a centralized ErrorHandler class that provides consistent
error handling and response formatting across all endpoints.

### Benefits
- Reduced code duplication by 40%
- Consistent error responses
- Easier to maintain and extend

## Testing

### Behavior Verification
All existing tests pass, confirming no behavior changes.

### Test Coverage
- Updated 25 existing tests
- Coverage maintained at 85%
```

## Troubleshooting

### Issue: Not enough context in code changes

**Solution:**
- Ask for commit messages
- Request related issue descriptions
- Check for comments in code
- Ask user for context

### Issue: Unclear what changed

**Solution:**
- Review git diff carefully
- Look for patterns in changes
- Check file names for clues
- Ask user for clarification

### Issue: Can't determine breaking changes

**Solution:**
- Look for API signature changes
- Check for removed functionality
- Review dependency updates
- Ask user if unsure

### Issue: Missing testing information

**Solution:**
- Suggest basic testing steps
- Recommend test coverage goals
- Provide testing checklist template
- Ask user for specific test scenarios
