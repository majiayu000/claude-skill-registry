---
name: mr-test-cases
description: Generate test cases for Merge Request changes. Analyzes diff between MR branch and develop, identifies affected areas (components, utilities, API calls, styling), and generates prioritized test cases. Use when reviewing MRs, planning QA testing, or before merging to ensure proper test coverage. Supports GitLab MR URLs or local branch comparison.
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - WebFetch
  - Task
---

# MR Test Cases Generator

Generate test cases based on code changes in a Merge Request.

## Features

- **Automatic diff analysis** - compares MR branch with develop
- **Smart categorization** - identifies affected areas (UI, API, utils, etc.)
- **Prioritized test cases** - P0 (critical) to P4 (low priority)
- **GitLab integration** - can fetch MR details from GitLab API
- **Markdown output** - ready to copy to MR description or test plan

## Workflow

### Step 1: Get MR Information

Ask user for one of:
1. **GitLab MR URL** - e.g., `https://gitlab.syncad.com/hive/denser/-/merge_requests/123`
2. **MR number** - e.g., `!123` or `123`
3. **Branch name** - e.g., `feature/my-branch` (will compare with develop)
4. **Current branch** - use current git branch (default)

### Step 2: Fetch Branch Information

**Option A: From GitLab API (if MR number provided)**
```bash
# Get MR details
glab api "projects/hive%2Fdenser/merge_requests/123" | jq '{source_branch, target_branch, title, description}'

# Get MR changes
glab api "projects/hive%2Fdenser/merge_requests/123/changes" | jq '.changes[] | {old_path, new_path}'
```

**Option B: From local git (if branch name provided)**
```bash
# Get current branch
git branch --show-current

# Get commits between develop and branch
git log develop..HEAD --oneline

# Get changed files
git diff develop...HEAD --stat

# Get detailed diff
git diff develop...HEAD
```

### Step 3: Analyze Changes

For each changed file, identify:

1. **File type and location**:
   - `apps/blog/` - Blog application
   - `apps/wallet/` - Wallet application
   - `packages/ui/` - Shared UI components
   - `packages/transaction/` - Blockchain transactions
   - `packages/smart-signer/` - Authentication

2. **Change type**:
   - New file - needs full testing
   - Modified file - focus on changed functions
   - Deleted file - check for broken references
   - Renamed file - check imports

3. **Affected area** (see references/area-mapping.md):
   - Components (UI changes)
   - Hooks (state/logic changes)
   - Utils/helpers (calculation changes)
   - API calls (data fetching changes)
   - Types (interface changes)
   - Styles (visual changes)
   - Tests (test changes)

### Step 4: Generate Test Cases

Use the following template for each test case:

```markdown
| ID | Priority | Area | Test Case | Description |
|----|----------|------|-----------|-------------|
| TC-XX | P0-P4 | Area | Test name | What to verify |
```

**Priority Guidelines**:
- **P0 (Critical)**: Financial calculations, authentication, data integrity
- **P1 (High)**: Core functionality, API integrations, user-facing features
- **P2 (Medium)**: UI components, tooltips, secondary features
- **P3 (Low)**: Navigation, styling, minor enhancements
- **P4 (Minimal)**: Documentation, refactoring without behavior change

### Step 5: Output Format

Generate a structured markdown document:

```markdown
## Test Cases for MR !{number}: {title}

**Branch**: `{source_branch}` → `{target_branch}`
**Changed files**: {count}
**Affected areas**: {list}

---

### Summary of Changes

{Brief description of what changed}

---

### Test Cases

#### P0 - Critical Tests
| ID | Area | Test Case | Description |
|----|------|-----------|-------------|
| TC-01 | ... | ... | ... |

#### P1 - High Priority Tests
...

#### P2 - Medium Priority Tests
...

#### P3 - Low Priority Tests
...

#### P4 - Minimal Priority Tests
...

---

### Recommended Test Approach

1. **Manual testing**: {list of manual checks}
2. **Automated tests**: {existing tests to run}
3. **Regression areas**: {areas that might be affected}

---

### Commands to Run

```bash
# Run related e2e tests
pnpm --filter @hive/blog test:e2e

# Run unit tests (if applicable)
pnpm test

# Run linting
pnpm lint
```
```

## Area Mapping Rules

See [references/area-mapping.md](references/area-mapping.md) for detailed mapping of files to test areas.

### Quick Reference

| File Pattern | Area | Priority Modifier |
|--------------|------|-------------------|
| `**/lib/utils.ts` | Calculations | +1 (higher priority) |
| `**/components/**` | UI | base |
| `**/hooks/**` | Logic | base |
| `**/api/**` | API | +1 |
| `**/*.spec.ts` | Tests | -1 (lower priority) |
| `**/*.test.ts` | Tests | -1 |
| `**/types/**` | Types | -1 |
| `**/*.css` | Styling | -1 |
| `**/locales/**` | i18n | -1 |

## Change Type Analysis

### Function Changes
When a function is modified, check:
- Input parameters changed → test all callers
- Return type changed → test all consumers
- Logic changed → test edge cases
- Error handling changed → test error scenarios

### Component Changes
When a component is modified, check:
- Props changed → test parent components
- State changed → test user interactions
- Rendering changed → visual regression
- Events changed → test handlers

### Hook Changes
When a hook is modified, check:
- Dependencies changed → test re-render behavior
- Return values changed → test consumers
- Side effects changed → test cleanup

### API Changes
When API calls are modified, check:
- Endpoint changed → test connectivity
- Request format changed → test payload
- Response handling changed → test error cases
- Caching changed → test refresh behavior

## Examples

### Example 1: Utility Function Change

**Changed file**: `packages/ui/lib/utils.ts`
**Changed function**: `convertToHP()`

Generated test cases:
| ID | Priority | Area | Test Case | Description |
|----|----------|------|-----------|-------------|
| TC-01 | P0 | Blog - Profile | HP calculation accuracy | Verify HP value matches API calculation |
| TC-02 | P0 | Wallet - Transfers | HP display on transfers | Verify HP shown on wallet page |
| TC-03 | P1 | Blog - Popover | HP in user popover | Verify HP in hover card |

### Example 2: Component Change

**Changed file**: `apps/blog/features/post-rendering/user-popover-card.tsx`

Generated test cases:
| ID | Priority | Area | Test Case | Description |
|----|----------|------|-----------|-------------|
| TC-01 | P2 | Blog - Popover | Popover opens on hover | Hover avatar shows popover |
| TC-02 | P2 | Blog - Popover | Popover data loads | User data appears in popover |
| TC-03 | P3 | Blog - Popover | Popover closes | Popover closes when mouse leaves |

### Example 3: Import Change

**Changed file**: `apps/blog/features/list-of-posts/post-list-item.tsx`
**Change**: Import `accountReputation` from `@hive/ui` instead of local

Generated test cases:
| ID | Priority | Area | Test Case | Description |
|----|----------|------|-----------|-------------|
| TC-01 | P1 | Blog - Posts | Reputation displays | Author reputation shows on post card |
| TC-02 | P2 | Blog - Posts | Reputation values | Check various reputation values (0, negative, high) |

## GitLab API Reference

```bash
# List MRs
glab api "projects/hive%2Fdenser/merge_requests?state=opened"

# Get specific MR
glab api "projects/hive%2Fdenser/merge_requests/123"

# Get MR changes (diff)
glab api "projects/hive%2Fdenser/merge_requests/123/changes"

# Get MR commits
glab api "projects/hive%2Fdenser/merge_requests/123/commits"
```

## Local Git Commands

```bash
# Compare branches
git diff develop...feature-branch

# List changed files
git diff develop...feature-branch --name-only

# Show file stats
git diff develop...feature-branch --stat

# Show specific file diff
git diff develop...feature-branch -- path/to/file.ts

# Get commit messages
git log develop...feature-branch --oneline
```
