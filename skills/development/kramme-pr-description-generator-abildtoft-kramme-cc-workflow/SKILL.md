---
name: kramme:pr-description-generator
description: Generate comprehensive Pull Request descriptions by analyzing git changes, commit history, Linear issues, and code structure for both GitLab and GitHub
---

# PR Description Generator

## Instructions

### When to Use This Skill

**Use this skill when:**

- You're ready to create a Pull Request
- You want a well-structured, comprehensive description for your changes
- You need to document what changed, why it changed, and how to test it
- You want to analyze multiple sources (git diff, commits, Linear issues) to create complete context

**When NOT to use this skill:**

- The PR already has a description and you just need to update it
- You're creating a draft PR that doesn't need a full description yet
- The changes are trivial (typo fixes, formatting) and don't warrant detailed documentation

### Context

High-quality PR descriptions are essential for:

- Code reviewers to understand the context and intent of changes
- Future developers investigating the history of a feature
- Product/project managers tracking feature delivery
- Creating an audit trail of technical decisions

This skill automates the process of gathering context from multiple sources (git history, Linear issues, code changes) and generating a structured, comprehensive description following best practices for Pull Requests.

### Guideline Keywords

When used, these keywords indicate the strength and requirement level of guidelines:

- **ALWAYS** — Mandatory requirement, exceptions are very rare and must be explicitly approved
- **NEVER** — Strong prohibition, exceptions are very rare and must be explicitly approved
- **PREFER** — Strong recommendation, exceptions allowed with justification
- **CAN** — Optional, developer's discretion
- **NOTE** — Context, rationale, or clarification
- **EXAMPLE** — Illustrative example

Strictness hierarchy: ALWAYS/NEVER > PREFER > CAN > NOTE/EXAMPLE

## Workflow

### Phase 1: Platform Detection

**ALWAYS** detect which platform is being used:

1. Check git remote URL:

   ```bash
   git remote get-url origin
   ```

   - Contains `gitlab.com` or `consensusaps` → GitLab
   - Contains `github.com` → GitHub

2. **ALWAYS** verify you have access to the appropriate tools:

   - GitLab: GitLab MCP server tools (`mcp__gitlab__*`)
   - GitHub: `gh` CLI tools via Bash

3. **ALWAYS** confirm the current branch:

   ```bash
   git branch --show-current
   ```

4. **ALWAYS** detect and identify the base/target branch dynamically:
   ```bash
   BASE_BRANCH=$(git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's@^refs/remotes/origin/@@')
   [ -z "$BASE_BRANCH" ] && BASE_BRANCH=$(git branch -r | grep -E 'origin/(main|master)$' | head -1 | sed 's@.*origin/@@')
   echo "Base branch: $BASE_BRANCH"
   ```
   - **NOTE**: This detects `main`, `master`, or any custom default branch
   - **CAN** ask user if unclear or override needed

### Phase 2: Context Gathering

**ALWAYS** gather comprehensive context from all available sources.

**IMPORTANT**: Use `origin/$BASE_BRANCH` for all comparisons to ensure you compare against the remote's state, not a potentially stale local branch.

**IMPORTANT**: Spec files and conversation history are for YOUR analysis only to understand implementation decisions. The final PR description should ONLY reference Linear issues as the source of original requirements, since reviewers have access to Linear but not to spec files or conversation history.

#### 2.1 Git Changes Analysis

1. **ALWAYS** get the diff between current branch and base branch:

   ```bash
   git diff origin/$BASE_BRANCH...HEAD
   ```

   - **NOTE**: Use three dots (`...`) to compare from merge base
   - **NOTE**: Use `origin/` prefix to compare against remote state

2. **ALWAYS** get the list of changed files with stats:

   ```bash
   git diff origin/$BASE_BRANCH...HEAD --stat
   ```

3. **ALWAYS** categorize changed files by area:

   - **Frontend**: Files under `Connect/ng-app-monolith/`
   - **Backend**: Files under `Connect/Connect.Api/`, `Connect/Connect.Core/`, etc.
   - **Tests**: Files matching `*.spec.ts`, `*.test.ts`, or under `tests/` directories
   - **Migrations**: Files under `Connect/Connect.Api/Migrations/`
   - **Documentation**: `*.md` files
   - **Configuration**: `*.json`, `*.config.*`, `*.yml` files

4. **CAN** use GitLab/GitHub tools to get branch diffs if available:
   - GitLab: `mcp__gitlab__get_branch_diffs`
   - GitHub: `gh pr diff` (if PR already exists)

#### 2.2 Commit History Analysis

1. **ALWAYS** get commit history for the current branch:

   ```bash
   git log origin/$BASE_BRANCH..HEAD --oneline
   ```

2. **ALWAYS** get detailed commit messages:

   ```bash
   git log origin/$BASE_BRANCH..HEAD --format="%h %s%n%b%n"
   ```

3. **ALWAYS** analyze commits to understand:
   - The narrative/journey of the implementation
   - Key technical decisions mentioned in commit bodies
   - Any referenced issues or tickets

#### 2.3 Linear Issue Context

1. **ALWAYS** check if branch name contains a Linear issue ID:

   - Pattern: `{initials}/{team-issue-id}-{description}`
   - **Known team abbreviations**: WAN, HEA, MEL, POT, FIR, FEG
   - **EXAMPLE**: `mab/wan-521-ensure-that-platform-picker-page-is-only-shown-if-the-user`
   - Extract issue ID: `wan-521` → `WAN-521` (uppercase)
   - **EXAMPLE**: `jd/hea-123-fix-header-bug` → Extract: `HEA-123`
   - **EXAMPLE**: `ab/mel-456-add-new-feature` → Extract: `MEL-456`

2. **ALWAYS** attempt to fetch Linear issue details if issue ID found:

   ```
   mcp__linear__get_issue with issue ID
   ```

3. **ALWAYS** include in context:

   - Issue title
   - Issue description
   - Issue state
   - Related project/labels

4. **ALWAYS** compare implementation against Linear issue description:

   - Check if the actual changes align with what was described in the issue
   - **ALWAYS** note any significant divergences from the original issue scope
   - **ALWAYS** identify if features were added/removed compared to issue description
   - **ALWAYS** note if approach differs from what was requested in the issue
   - **EXAMPLE**: Issue asked for A, but implementation delivers A + B, or implements A differently

5. **CAN** check commit messages for Linear issue references:
   - Pattern: `{TEAM}-{number}` where TEAM is one of: WAN, HEA, MEL, POT, FIR, FEG
   - **EXAMPLE**: `WAN-123`, `Fixes HEA-456`, `Related to MEL-789`

#### 2.4 Code Structure Analysis

1. **ALWAYS** analyze the scope of changes:

   - Frontend-only: Only files under `ng-app-monolith/`
   - Backend-only: Only files under `Connect/` (excluding `ng-app-monolith/`)
   - Full-stack: Changes in both areas
   - Tests-only: Only test files modified
   - Documentation-only: Only `.md` files modified

2. **ALWAYS** identify change characteristics:

   - **New feature**: New files created, new functionality added
   - **Bug fix**: Primarily modifications to existing files, issue mentions "bug" or "fix"
   - **Refactor**: Code reorganization without behavior change
   - **Chore**: Config, dependencies, tooling updates

3. **ALWAYS** check for breaking changes indicators:
   - Database migrations created
   - API endpoint signature changes (parameter changes, return type changes)
   - Public interface/contract changes
   - Configuration schema changes
   - Environment variable additions/removals

#### 2.5 Conversation History and Specification Files Analysis

**ALWAYS** check for implementation decisions and context from the development process:

1. **Specification Files** (commonly created by structured-implementation-workflow Skill):

   - **ALWAYS** search for these files in the repository root or feature directories:
     - `SPEC.md` - Main specification document
     - `LOG.md` - Implementation log/journal
     - `OPEN_ISSUES.md` - Known issues and decisions
     - `IMPLEMENTATION.md` - Implementation notes

   ```bash
   # Search for specification files
   find . -maxdepth 3 -name "SPEC.md" -o -name "LOG.md" -o -name "OPEN_ISSUES.md" -o -name "IMPLEMENTATION.md"
   ```

2. **Read specification files if found**:

   - Extract key technical decisions made during implementation
   - Identify scope changes or refinements
   - Note any deviations from original plan with rationale
   - **ALWAYS** capture divergences from Linear issue description with explanation
   - Capture important constraints or limitations
   - Look for reviewer-relevant context (performance considerations, security implications, etc.)

3. **Review conversation history**:

   - **ALWAYS** scan the current conversation for:
     - Architecture or design decisions discussed with the user
     - Trade-offs explicitly considered (e.g., "chose approach A over B because...")
     - Scope clarifications or boundary decisions
     - **Divergences from Linear issue with reasoning** (e.g., "Changed from X to Y because...")
     - Performance, security, or scalability considerations
     - Known limitations or future work mentioned
     - Any "why" explanations that would help reviewers understand the approach

4. **Capture important decisions and divergences**:
   - **ALWAYS** include significant decisions in the Technical Details section
   - **ALWAYS** document any divergences from the Linear issue description with clear rationale
   - **PREFER** explaining "why" over just "what" for non-obvious choices
   - **EXAMPLE**: "Used debouncing instead of throttling because platform data changes infrequently and we want to avoid unnecessary API calls"
   - **EXAMPLE**: "Linear issue requested email notifications, but implemented push notifications instead after discovering email delivery was unreliable in testing"
   - **NEVER** include trivial decisions or over-explain obvious choices
   - **IMPORTANT**: Spec files (SPEC.md, LOG.md, etc.) and conversation history are for YOUR analysis only
   - **NEVER** reference spec files or conversation history in the PR description (reviewers don't have access to them)
   - **ALWAYS** reference only Linear issues as the source of original requirements when documenting divergences

### Phase 2.5: Analysis and Clarification

**ALWAYS** pause after gathering context and before generating the description:

1. **Present initial analysis**:

   - Summarize what you've found:
     - Change type (feature, bug fix, refactor, etc.)
     - Scope (frontend-only, backend-only, full-stack)
     - Key technical decisions identified
     - **Any divergences from Linear issue description**
     - Any breaking changes detected

2. **Ask clarification questions**:

   - **ALWAYS** ask the user if there's anything specific they want emphasized
   - **ALWAYS** ask if there are any concerns or considerations reviewers should know about
   - **CAN** ask about:
     - Specific areas that need more detailed explanation
     - Known limitations or trade-offs to document
     - Performance or security implications to highlight
     - Future work or follow-up tasks to mention

3. **Example clarification prompt**:

   ```
   I've analyzed the changes and identified this as a [type] that [brief summary].

   Key decisions I found:
   - [Decision 1]
   - [Decision 2]

   Divergences from Linear issue (if any):
   - [Divergence 1 and why]
   - [Divergence 2 and why]

   Before generating the description:
   - Is there anything specific you'd like me to emphasize or explain in detail?
   - Are there any concerns, limitations, or trade-offs reviewers should be aware of?
   - Should I highlight any particular aspects of the implementation?
   - Should I explain any divergences from the original Linear issue in more detail?
   ```

4. **Wait for user response** before proceeding to Phase 3

### Phase 3: Description Generation

**ALWAYS** generate a structured PR title and description.

#### 3.0 Title Generation

Generate a PR title using [Conventional Commits](https://www.conventionalcommits.org/) format: `<type>(<scope>): <description>`

**NOTE**: Check the project's CLAUDE.md for any project-specific conventional commit rules.

**Types** (based on Phase 2.4 analysis):

| `feat` | `fix` | `refactor` | `docs` | `test` | `build`/`ci` | `chore` | `perf` | `style` | `revert` |

**Rules**:
- **Scope**: Optional. Use component/module name, lowercase, hyphenated (e.g., `auth`, `platform-picker`). Omit if changes span multiple areas.
- **Description**: Imperative mood ("add", not "added"), specific, under 50 chars. Total title under 72 chars. No trailing period.

**Examples**: `feat(auth): add OAuth2 support` · `fix: resolve null pointer in user lookup` · `refactor(api): extract validation utilities`

#### 3.1 Summary Section

**ALWAYS** include:

1. **What changed** (1-2 sentences, high-level, user/business-focused)

   - **PREFER** non-technical language when possible
   - **EXAMPLE**: "Added ability for users to export their survey results to PDF format"

2. **Why it changed** (1-2 sentences, business context)

   - Pull from Linear issue description if available
   - **EXAMPLE**: "Users requested this feature to share results with stakeholders who don't have system access"

3. **Link to Linear issue** (if available):

   - **ALWAYS** use a "magic word" + issue ID for automatic linking
   - **Magic words**: `Fixes`, `Closes`, `Resolves` (marks issue as done when PR merges)
   - **Alternative**: `Related to`, `Refs`, `References` (links without auto-closing)
   - **CAN** use either issue ID or full Linear URL

   **Format options:**
   ```markdown
   Fixes WAN-521
   ```
   or
   ```markdown
   Closes https://linear.app/consensusaps/issue/WAN-521/title
   ```
   or (for related but not closing):
   ```markdown
   Related to WAN-521
   ```

   - **PREFER** `Fixes` or `Closes` when the PR completes the work for the issue
   - **PREFER** `Related to` when the PR is partial work or tangentially related

**EXAMPLE Summary:**

```markdown
## Summary

Added a platform picker guard that automatically skips the platform selection page if a user only has access to one platform. This improves the user experience by reducing unnecessary navigation steps.

This change addresses user feedback that the platform picker was unnecessary for single-platform users, causing confusion and extra clicks.

Fixes WAN-521
```

#### 3.2 Technical Details Section

**ALWAYS** include:

1. **Implementation approach** (2-4 sentences):

   - Key architectural decisions
   - Design patterns used
   - Why this approach was chosen over alternatives
   - **If applicable**: Divergences from Linear issue description with clear rationale

2. **Scope changes** (if implementation diverged from Linear issue):

   - **ONLY document divergences from Linear issue(s)** - this is the only source reviewers have access to
   - **NEVER** reference spec files (SPEC.md, LOG.md, etc.) or conversation history - reviewers cannot see these
   - **What changed**: Clear description of how implementation differs from Linear issue
   - **Why it changed**: Rationale for the divergence (discovered during implementation, technical constraints, better approach found, etc.)
   - **EXAMPLE**: "Linear issue WAN-123 requested feature X, but implemented X + Y because Y was required to make X work correctly in production"
   - **EXAMPLE**: "Linear issue requested server-side rendering approach, but changed to client-side due to performance testing results showing 40% better load times"
   - **WRONG**: "As discussed in SPEC.md, we changed the approach..." (reviewers can't see SPEC.md)
   - **WRONG**: "Based on our conversation, we decided..." (reviewers can't see conversation history)

3. **Changes by area**:

   **Frontend Changes** (if applicable):

   - List key components/services modified or created
   - State management changes (ComponentStore, etc.)
   - Routing/navigation changes
   - UI/UX changes

   **Backend Changes** (if applicable):

   - API endpoints added/modified
   - Service/repository changes
   - Business logic updates
   - Database changes

   **Database Migrations** (if applicable):

   - Migration name and purpose
   - Schema changes (tables, columns, indices)
   - Data migrations (if any)

   **Test Coverage** (if applicable):

   - New tests added
   - Test coverage areas

3. **Files changed summary**:
   - Group by category (Frontend, Backend, Tests, etc.)
   - **PREFER** listing only the most significant files (not every file)
   - **EXAMPLE**:
     ```markdown
     **Key Files:**

     - Frontend:
       - `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.ts` - New guard implementation
       - `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.spec.ts` - Guard tests
     - Backend:
       - `Connect/Connect.Api/Controllers/PlatformController.cs` - Added user platform count endpoint
     ```

**EXAMPLE Technical Details:**

```markdown
## Technical Details

### Implementation Approach

Implemented a new Angular route guard (`PlatformPickerRedirectGuard`) that checks the user's platform count before allowing navigation to the platform picker page. If the user has only one platform, the guard automatically redirects to the appropriate destination.

The implementation uses NgRx ComponentStore for reactive state management and integrates with the existing platform service to fetch user platform data.

### Scope Changes

The Linear issue originally requested only redirecting single-platform users. During implementation, added a 2-second timeout with graceful fallback to prevent indefinite loading states when the platform API is slow or unresponsive. This was added after discovering edge cases during testing where network latency could leave users on a blank screen.

### Changes by Area

**Frontend:**

- Created `PlatformPickerRedirectGuard` implementing Angular `CanActivate` interface
- Added `PlatformPickerRedirectStore` for managing guard state
- Integrated guard into platform picker route configuration
- Added comprehensive unit tests for guard logic

**Backend:**

- Added `GET /api/platforms/count` endpoint to retrieve user platform count
- Updated `PlatformService` to support count queries
- Added caching for platform count to improve performance

**Tests:**

- 15 new unit tests for guard behavior
- 3 integration tests for the new API endpoint
- E2E tests for single-platform and multi-platform user flows

**Key Files:**

- Frontend:
  - `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.ts`
  - `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.spec.ts`
  - `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.store.ts`
- Backend:
  - `Connect/Connect.Api/Controllers/PlatformController.cs`
  - `Connect/Connect.Core/Services/PlatformService.cs`
```

#### 3.3 Test Plan Section

**ALWAYS** include actionable testing steps:

1. **Setup steps** (if needed):

   - Environment configuration
   - Test data requirements
   - User permissions needed

2. **Test scenarios** (organized by priority):

   - **Happy path**: Normal expected flow
   - **Edge cases**: Boundary conditions
   - **Error cases**: What happens when things go wrong

3. **Verification points**:
   - Expected outcomes for each scenario
   - What to check in the UI, database, logs, etc.

**PREFER** using a checklist format for clarity:

**EXAMPLE Test Plan:**

```markdown
## Test Plan

### Prerequisites

- User account with multiple platforms (for multi-platform testing)
- User account with single platform (for auto-redirect testing)

### Test Scenarios

**Scenario 1: Single-platform user**

- [ ] Log in as a user with only one platform
- [ ] Navigate to a route that would normally show platform picker
- [ ] Verify user is automatically redirected past the platform picker
- [ ] Verify the correct platform is pre-selected

**Scenario 2: Multi-platform user**

- [ ] Log in as a user with multiple platforms
- [ ] Navigate to platform picker route
- [ ] Verify platform picker page is displayed
- [ ] Verify all user's platforms are shown

**Scenario 3: Platform count API error**

- [ ] Simulate API error (network failure or 500 response)
- [ ] Verify user is still able to access platform picker
- [ ] Verify error is handled gracefully (no crash)

**Scenario 4: First-time user (no platforms)**

- [ ] Log in as a new user with no platforms
- [ ] Verify appropriate message/redirect to onboarding
```

#### 3.4 Breaking Changes Section

**ALWAYS** include this section if any of the following are true:

- Database migrations that require downtime
- API endpoint signatures changed (parameters, return types)
- Configuration changes (environment variables, app settings)
- Dependency version upgrades with breaking changes
- Public interface/contract changes

**If no breaking changes**, use:

```markdown
## Breaking Changes

None
```

**If breaking changes exist**, include:

1. **What breaks**:

   - Clear description of what is no longer compatible

2. **Why it's breaking**:

   - Rationale for the breaking change

3. **Migration path**:

   - Step-by-step instructions for adapting to the change

4. **Impact assessment**:
   - What systems/components are affected
   - Estimated effort to adapt

**EXAMPLE Breaking Changes:**

````markdown
## Breaking Changes

### API Endpoint Signature Change

**What changed:**
The `GET /api/platforms` endpoint now requires a `userId` query parameter. Previously, it inferred the user from the authentication context.

**Why:**
This change enables admin users to query platforms for other users, which is required for the new admin dashboard feature.

**Migration:**

- **Frontend clients**: Update API calls to include `userId` parameter

  ```typescript
  // Before
  this.http.get("/api/platforms");

  // After
  this.http.get("/api/platforms", { params: { userId: currentUserId } });
  ```
````

- **External integrations**: Add `userId` to query string in API requests

**Impact:**

- All frontend components calling this endpoint (5 locations identified)
- External API consumers (audit-log-service, analytics service)
- Estimated migration effort: 2-4 hours

### Database Migration

**What changed:**
New `platform_access_count` column added to `users` table with NOT NULL constraint.

**Migration:**
Run migration before deploying new application version:

```bash
dotnet ef database update -c ConnectContext
```

**Downtime:**
~5 minutes (backfill operation for existing users)

````

#### 3.5 Screenshots and Videos Section

**ALWAYS** include a placeholder section for visual aids:

```markdown
## Screenshots / Videos

<!-- Add screenshots or videos here to help reviewers visualize the changes -->
<!-- Consider including: -->
<!-- - Before/after UI comparisons -->
<!-- - New features in action -->
<!-- - Error states or edge cases -->
<!-- - Mobile/responsive views -->
```

**NOTE**: This is a placeholder section for the PR creator to populate with relevant visuals

### Phase 4: Output Formatting

**ALWAYS** format the output as clean Markdown:

1. **ALWAYS** use proper heading hierarchy (##, ###)
2. **ALWAYS** use code blocks with language hints for code snippets
3. **ALWAYS** use bullet points and numbered lists for readability
4. **PREFER** using tables for structured data (if applicable)
5. **NEVER** include meta-commentary or placeholders like `[TODO]` or `[Fill this in]`
6. **NEVER** include AI attribution or badges such as:
   - `🤖 Generated with [Claude Code](https://claude.ai/code)`
   - `Generated with Claude Code`
   - `Co-Authored-By: Claude` or similar
   - Any mention of AI assistance in the description

**ALWAYS** present the final PR title and description in a clear, copy-paste-ready format:

```markdown
Here is your generated PR:

**Title:** `<type>(<scope>): <description>`

---

[DESCRIPTION CONTENT HERE]

---
```

**NOTE**: The title is formatted with backticks for easy copying. The description follows the standard markdown format.

6. **ALWAYS** ask if the description should be saved to a markdown file:

   - After presenting the description, ask: "Would you like me to save this description to a markdown file?"
   - If yes, save to a file named `PR_DESCRIPTION.md` in the repository root
   - Confirm the file location after saving

### Phase 5: Final Checklist

**ALWAYS** verify before presenting the PR:

- [ ] **Title** follows conventional commit format (`<type>(<scope>): <description>`)
- [ ] **Title** uses correct type (feat, fix, refactor, docs, test, chore, etc.)
- [ ] **Title** is concise (under 72 characters total)
- [ ] **Title** uses imperative mood ("add", not "added")
- [ ] Summary clearly explains what and why (objective tone, no excessive praise)
- [ ] Linear issue is linked with appropriate magic word (Fixes/Closes vs. Related to)
- [ ] Technical details cover implementation approach and key decisions from conversation/spec files
- [ ] **Divergences from Linear issue are documented with clear rationale** (if applicable)
- [ ] Changes are categorized by area (Frontend/Backend/Tests)
- [ ] Key files are listed (not line counts)
- [ ] Test plan includes actionable scenarios
- [ ] Breaking changes are documented (or marked as "None")
- [ ] Screenshots/Videos placeholder section is included
- [ ] Markdown is properly formatted
- [ ] No placeholders or TODOs in the output (except Screenshots section)
- [ ] Description is ready to copy-paste
- [ ] No listing of the amount of lines changed
- [ ] No AI attribution or "Generated with Claude Code" badges included
- [ ] Asked user if they want to save to markdown file

## Best Practices

### Context Gathering

- **ALWAYS** detect the base branch dynamically using `git symbolic-ref refs/remotes/origin/HEAD`
- **ALWAYS** use `git diff origin/$BASE_BRANCH...HEAD` (three dots, `origin/` prefix) to compare from merge base against the remote's state
- **NEVER** use local branch names like `main` or `master` directly - always use `origin/` prefix to avoid comparing against stale local branches
- **ALWAYS** look at both commit messages and code changes - they tell different stories
- **NEVER** skip Linear issue lookup if the branch name contains an issue ID
- **PREFER** using MCP tools (GitLab/Linear) over bash commands when available for richer data

### Writing Style

- **ALWAYS** write in present tense ("Adds feature" not "Added feature")
- **ALWAYS** be specific and concrete ("Added Redis caching for user queries" not "Improved performance")
- **NEVER** use vague terms like "various changes" or "miscellaneous updates"
- **PREFER** active voice over passive voice ("The guard redirects users" not "Users are redirected by the guard")
- **ALWAYS** maintain a professional, objective tone - let the changes speak for themselves
- **NEVER** use excessive praise or superlatives ("amazing", "excellent", "great improvement")
- **NEVER** argue for why changes are good - describe what was done and why, without advocacy
- **PREFER** factual descriptions over persuasive language
   - **NEVER** write sentences like "This brilliant solution elegantly solves the performance problem"
   - **ALWAYS** write sentences like "Reduces query time by caching frequently accessed data"
- **NEVER** make up statistics or performance claims without evidence

### Technical Details

- **ALWAYS** explain **why** decisions were made, not just **what** changed
- **PREFER** including relevant code snippets for complex changes
- **NEVER** list every single file - focus on the most significant ones
- **NEVER** list the amount of lines changed - it's not useful information, clutters the description and is often quickly made incorrect by subsequent commits
- **CAN** reference existing patterns in AGENTS.md when explaining implementation choices

### Test Plans

- **ALWAYS** make test scenarios actionable (steps anyone can follow)
- **PREFER** checklist format for test scenarios
- **NEVER** write "test thoroughly" without specific scenarios
- **ALWAYS** include edge cases and error scenarios, not just happy paths

## Anti-Patterns

### Title Anti-Patterns

| ❌ Wrong | ✅ Correct | Issue |
|----------|-----------|-------|
| `Update platform picker` | `feat(platform-picker): add redirect` | Missing type |
| `feat(auth): fixed login bug` | `feat(auth): fix login bug` | Past tense |
| `fix: bug fix` | `fix(checkout): resolve race condition` | Vague |
| `feat(user-auth-service): add comprehensive OAuth2...` | `feat(auth): add OAuth2 support` | Too long |

---

### ❌ WRONG: Vague Summary

```markdown
## Summary

Updated the platform picker functionality to work better.
```

### ✅ CORRECT: Specific Summary

```markdown
## Summary

Added automatic redirect logic that skips the platform picker page when a user has access to only one platform, reducing unnecessary navigation steps.

Fixes WAN-521
```

---

### ❌ WRONG: List of Files Without Context

```markdown
## Changes

- file1.ts
- file2.cs
- file3.spec.ts
- file4.html
- file5.scss
```

### ✅ CORRECT: Categorized Changes with Purpose

```markdown
## Technical Details

**Frontend:**

- `platform-picker-redirect.guard.ts` - New guard that checks platform count and redirects single-platform users
- `platform-picker-redirect.store.ts` - ComponentStore for managing guard state
- `platform-picker-redirect.guard.spec.ts` - Comprehensive unit tests

**Backend:**

- `PlatformController.cs` - Added `/api/platforms/count` endpoint
```

---

### ❌ WRONG: No Test Plan

```markdown
## Test Plan

Test all the changes manually.
```

### ✅ CORRECT: Actionable Test Scenarios

```markdown
## Test Plan

**Scenario 1: Single-platform user**

- [ ] Log in as a user with only one platform
- [ ] Navigate to `/platform-picker`
- [ ] Verify automatic redirect to dashboard
- [ ] Verify correct platform is pre-selected

**Scenario 2: Multi-platform user**

- [ ] Log in as a user with 2+ platforms
- [ ] Navigate to `/platform-picker`
- [ ] Verify platform picker page displays
- [ ] Verify all platforms are listed
```

---

### ❌ WRONG: Overly Enthusiastic Tone

```markdown
## Summary

This amazing implementation brilliantly solves the platform picker problem! We've created
an excellent solution that elegantly handles all edge cases. This is a huge improvement
that will dramatically enhance user experience!

## Technical Details

The implementation is beautifully architected using cutting-edge patterns. The guard is
incredibly efficient and handles everything perfectly. This is truly exceptional work!
```

### ✅ CORRECT: Professional, Objective Tone

```markdown
## Summary

Added automatic redirect logic to skip the platform picker page when users have access
to exactly one platform, eliminating an unnecessary navigation step.

Fixes WAN-521

## Technical Details

### Implementation Approach

Implemented a route guard that checks platform count before navigation. When a user has
exactly one platform, the guard redirects directly to that platform instead of showing
the picker page.
```

---

### ❌ WRONG: Hidden Breaking Changes

```markdown
## Technical Details

Changed the API endpoint signature.
```

### ✅ CORRECT: Explicit Breaking Changes Section

````markdown
## Breaking Changes

### API Endpoint Signature Change

**What changed:**
`GET /api/platforms` now requires `userId` query parameter.

**Migration:**
Update all API calls:

```typescript
// Before
this.http.get("/api/platforms");

// After
this.http.get("/api/platforms", { params: { userId } });
```
````

**Impact:**

- 5 frontend components
- 2 external services (audit-log, analytics)

````

---

### ❌ WRONG: AI Attribution in Description

```markdown
## Summary

Added the new feature to improve user experience.

🤖 Generated with [Claude Code](https://claude.ai/code)
```

### ✅ CORRECT: Clean Description Without Attribution

```markdown
## Summary

Added the new feature to improve user experience.
```

## Examples

### Example 1: Frontend-Only Feature

**Input:**
- Branch: `mab/wan-521-auto-skip-platform-picker`
- Changed files: 3 frontend files (guard, store, tests)
- Commits: 4 commits with incremental implementation
- Linear issue: WAN-521 (feature request)

**Generated PR:**
```markdown
Here is your generated PR:

**Title:** `feat(platform-picker): add automatic redirect for single-platform users`

---

## Summary

Added automatic redirect logic that skips the platform picker page when users have access to only one platform. This eliminates an unnecessary navigation step and improves user experience for single-platform users.

This addresses user feedback that the platform picker was confusing for users who only had one platform available.

Fixes WAN-521

## Technical Details

### Implementation Approach

Created a new Angular route guard (`PlatformPickerRedirectGuard`) that queries the user's platform count and conditionally redirects based on the result. The guard integrates with the existing platform service and uses NgRx ComponentStore for reactive state management.

### Changes by Area

**Frontend:**
- Implemented `PlatformPickerRedirectGuard` using Angular `CanActivate` interface
- Created `PlatformPickerRedirectStore` for managing platform count state
- Integrated guard into platform picker route configuration
- Added 12 unit tests covering all guard scenarios

**Key Files:**
- `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.ts` - Guard implementation
- `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.store.ts` - State management
- `libs/connect/shared/platform-picker/data-access/src/lib/platform-picker-redirect.guard.spec.ts` - Tests

## Test Plan

**Scenario 1: Single-platform user**
- [ ] Log in with user account that has only one platform
- [ ] Navigate to any route that would trigger platform picker
- [ ] Verify automatic redirect past platform picker
- [ ] Verify correct platform is pre-selected in destination

**Scenario 2: Multi-platform user**
- [ ] Log in with user account that has multiple platforms
- [ ] Navigate to platform picker route
- [ ] Verify platform picker page displays normally
- [ ] Verify all platforms are shown in the picker

**Scenario 3: Error handling**
- [ ] Simulate platform service error (disconnect network)
- [ ] Verify graceful fallback (show picker anyway)
- [ ] Verify no crashes or console errors

## Breaking Changes

None

## Screenshots / Videos

<!-- Add screenshots or videos here to help reviewers visualize the changes -->
<!-- Consider including: -->
<!-- - Before/after UI comparisons -->
<!-- - New features in action -->
<!-- - Error states or edge cases -->
<!-- - Mobile/responsive views -->
````

### Example 2: Full-Stack Feature with Database Migration

**Input:**

- Branch: `feature/add-user-preferences-api`
- Changed files: Backend controller, service, migration + Frontend service, component
- Database migration: Add `user_preferences` table
- Linear issue: CON-789

**Generated PR:**

````markdown
Here is your generated PR:

**Title:** `feat(preferences): add user preferences storage and API`

---

## Summary

Added user preferences storage and API endpoints to enable users to save and retrieve their application settings (theme, notification preferences, default views). This provides a foundation for future personalization features.

Related to CON-789

## Technical Details

### Implementation Approach

Implemented a new `user_preferences` table to store JSON preference data, with API endpoints for CRUD operations. The frontend uses a new preferences service that caches user preferences and syncs changes to the backend.

Database migration adds the preferences table with appropriate indexing and foreign key constraints.

### Changes by Area

**Backend:**

- `PreferencesController.cs` - New REST endpoints for preferences CRUD
- `UserPreferencesService.cs` - Business logic for preference management
- `UserPreference.cs` - Entity model
- `20250122_AddUserPreferences.cs` - Database migration

**Frontend:**

- `user-preferences.service.ts` - Service for managing user preferences with local caching
- `preferences.component.ts` - UI for editing preferences
- API client updates for new endpoints

**Database Migration:**

- Added `user_preferences` table with columns: `id`, `user_id`, `preferences_json`, `created_at`, `updated_at`
- Added index on `user_id` for query performance
- Foreign key constraint to `users` table

**Tests:**

- 8 unit tests for backend service
- 6 integration tests for API endpoints
- 10 frontend component tests

**Key Files:**

- Backend:
  - `Connect/Connect.Api/Controllers/PreferencesController.cs`
  - `Connect/Connect.Core/Services/UserPreferencesService.cs`
  - `Connect/Connect.Api/Migrations/20250122_AddUserPreferences.cs`
- Frontend:
  - `libs/connect/shared/preferences/data-access/src/lib/user-preferences.service.ts`
  - `libs/connect/shared/preferences/feature/src/lib/preferences.component.ts`

## Test Plan

### Prerequisites

- Database migration applied
- User account for testing

### Test Scenarios

**Scenario 1: Create preferences (first time)**

- [ ] Log in as user with no preferences
- [ ] Navigate to preferences page
- [ ] Change theme to "dark"
- [ ] Enable email notifications
- [ ] Click "Save"
- [ ] Verify success message
- [ ] Reload page and verify preferences persisted

**Scenario 2: Update existing preferences**

- [ ] Log in as user with existing preferences
- [ ] Change notification settings
- [ ] Click "Save"
- [ ] Verify preferences updated in database
- [ ] Verify UI reflects changes immediately

**Scenario 3: API validation**

- [ ] Send invalid JSON to preferences API
- [ ] Verify 400 Bad Request response
- [ ] Verify helpful error message

**Scenario 4: Cross-user isolation**

- [ ] Create preferences for User A
- [ ] Log in as User B
- [ ] Verify User B cannot see User A's preferences
- [ ] Verify User B can create own preferences

## Breaking Changes

### Database Migration Required

**What changed:**
New `user_preferences` table added to database schema.

**Migration:**
Run the following migration before deploying:

```bash
dotnet ef database update -c ConnectContext
```
````

**Downtime:**
~1 minute (table creation, no data backfill needed)

**Rollback:**
If rollback is needed:

```bash
dotnet ef migrations remove -c ConnectContext
```

## Screenshots / Videos

<!-- Add screenshots or videos here to help reviewers visualize the changes -->
<!-- Consider including: -->
<!-- - Before/after UI comparisons -->
<!-- - New features in action -->
<!-- - Error states or edge cases -->
<!-- - Mobile/responsive views -->
```

## Reference Files

**ALWAYS** refer to these files for context:

- `AGENTS.md` - Authoritative development guidelines for this codebase
- `CLAUDE.md` - AI-specific instructions, including GitLab vs GitHub guidance
- Existing PR descriptions in the repository for style reference

## Platform-Specific Notes

### GitLab

- **PREFER** using GitLab MCP server tools when available:
  - `mcp__gitlab__get_branch_diffs` for diff analysis
  - `mcp__gitlab__list_commits` for commit history
  - `mcp__gitlab__get_merge_request` if PR already exists
- **ALWAYS** link Linear issues using magic words for automatic linking:
  - **Magic words that auto-close**: `Fixes`, `Closes`, `Resolves` (use when PR completes the issue)
  - **Magic words that link only**: `Related to`, `Refs`, `References` (use for partial/related work)
  - **Format**: `{magic word} {TEAM}-{number}` or `{magic word} {full Linear URL}`
  - **EXAMPLE**: `Fixes WAN-123`, `Closes HEA-456`, `Related to MEL-789`
  - **NOTE**: Team abbreviations: WAN, HEA, MEL, POT, FIR, FEG

### GitHub

- **PREFER** using `gh` CLI via Bash for GitHub operations
- **ALWAYS** link issues using: `Fixes #123` or `Closes #123` or `Related to #123`

## Notes

- **NOTE**: This skill generates the description text only - it does NOT create the PR
- **NOTE**: After generation, review the description and adjust as needed before using it
- **NOTE**: The skill follows Connect project conventions (AGENTS.md) but may need customization for other projects
- **NOTE**: If Linear issue lookup fails, continue anyway and note the issue ID in the summary without detailed context
- **NOTE**: Spec files (SPEC.md, LOG.md, OPEN_ISSUES.md, etc.) and conversation history are for context gathering ONLY
  - Use them to understand what happened during implementation
  - **NEVER** reference them in the PR description - reviewers don't have access to them
  - Only reference Linear issues when documenting divergences or original requirements
  - **WRONG**: "As mentioned in LOG.md..." or "Based on our earlier discussion..."
  - **RIGHT**: "Linear issue WAN-123 requested X, but implemented Y because..."
```
