---
name: commit
description: Generate Conventional Commits-compliant messages (feat/fix/docs/chore) in Korean and English. Use when you need to create a well-structured commit message for staged changes.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Read, Grep, Write
disable-model-invocation: true
---

# Conventional Commits Message Generator

Generates commit messages following [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) specification in both Korean and English. **Choose one version for your commit.**

## Repository State Analysis

- Git status: !git status --porcelain
- Current branch: !git branch --show-current
- Staged changes: !git diff --cached --stat
- Unstaged changes: !git diff --stat
- Recent commits: !git log --oneline -10

## What This Command Does

1. Checks current branch name to detect issue number (e.g., develop/shlee/32 → #32)
2. Checks which files are staged with git status
3. Performs a git diff to understand what changes will be committed
4. Generates commit messages in Conventional Commits format in both Korean and English
5. Adds "fix #N" at the end if branch name ends with a number
6. **Saves to commit_message.md file for easy copying**

## Conventional Commits Format (REQUIRED)

```
<type>[(optional scope)]: <description>

[optional body]

[optional footer: fix #N]
```

### Available Types

Analyze staged changes and suggest the most appropriate type:

| Type         | When to Use                                           | SemVer Impact |
| ------------ | ----------------------------------------------------- | ------------- |
| **feat**     | New feature or capability added                       | MINOR (0.x.0) |
| **fix**      | User-facing bug fix                                   | PATCH (0.0.x) |
| **ifix**     | Internal/infrastructure bug fix (CI, build, deploy)   | PATCH (0.0.x) |
| **perf**     | Performance improvements                              | PATCH         |
| **docs**     | Documentation only changes (README, comments, etc.)   | PATCH         |
| **style**    | Code formatting, missing semicolons (no logic change) | PATCH         |
| **refactor** | Code restructuring without changing behavior          | PATCH         |
| **test**     | Adding or fixing tests                                | PATCH         |
| **chore**    | Build config, dependencies, tooling updates           | PATCH         |
| **ci**       | CI/CD configuration changes                           | PATCH         |

**BREAKING CHANGE**: MUST use both type! format (exclamation mark after type) AND BREAKING CHANGE: footer with migration guide for major version bump.

Example:

```
feat!: change API response format from JSON to MessagePack

Migrated response format to MessagePack binary for 40% packet size reduction.

BREAKING CHANGE: Client code update required
- Install MessagePack library: npm install msgpack5
- Update response parsing: response.json() → msgpack.decode(response.body)
- Update type definitions: API_RESPONSE_FORMAT constant changed
```

### Type Selection Decision Tree

Analyze git diff output and suggest type based on file patterns:

```
Changed Files → Suggested Type

src/**/*.{ts,js,tsx,jsx} + new functions/classes → feat
src/**/*.{ts,js,tsx,jsx} + bug fix → fix
README.md, docs/**, *.md → docs
package.json, pnpm-lock.yaml, .github/** → chore
**/*.test.{ts,js}, **/*.spec.{ts,js} → test
.github/workflows/** → ci
```

If multiple types apply, prioritize: `feat` > `fix` > other types.

### Confusing Cases: fix vs ifix vs chore

**Key distinction**: Does it affect **users** or only **developers/infrastructure**?

| Scenario                                              | Type       | Reason                                       |
| ----------------------------------------------------- | ---------- | -------------------------------------------- |
| Backend GitHub Actions test workflow not running      | `ifix`     | Bug in CI/CD that blocks development         |
| OOM error causing deployment failure                  | `ifix`     | Infrastructure bug blocking release          |
| E2E test flakiness causing false negatives            | `ifix`     | Testing infrastructure bug                   |
| Vite build timeout in production build                | `ifix`     | Build system bug                             |
| API returns 500 error for valid requests              | `fix`      | Users experience error responses             |
| Page loading speed improved from 3s to 0.8s           | `perf`     | Users directly feel the improvement          |
| App crashes when accessing profile page               | `fix`      | Users experience crash                       |
| Internal database query optimization (no user impact) | `refactor` | Code improvement, no measurable user benefit |
| Dependency security patch (CVE fix)                   | `chore`    | Build/tooling update (not a bug fix)         |
| Upgrading React version for new features              | `chore`    | Dependency update (not a bug fix)            |

**Decision flowchart:**

```
Is it a bug (something broken)?
├─ NO → Use chore/refactor/docs/etc
└─ YES → Does it affect end users?
    ├─ YES → fix (user-facing bug)
    └─ NO → ifix (infrastructure/developer bug)
```

**Examples:**

- ✅ `fix: login button not responding` (user problem)
- ✅ `ifix: Docker build failing due to missing environment variable` (infra bug)
- ✅ `ifix: Prisma migration script syntax error` (developer tooling bug)
- ❌ ~~`fix: null pointer exception in ItemService`~~ → Use `fix: app crashes when viewing items` (user perspective)

## Commit Message Format Guidelines

**Core Principle: Root Cause → Rationale → Implementation**

Commit messages document decision **history**, not just code changes. Every non-trivial commit body MUST answer:

1. **WHY-Problem**: Why did this problem exist? (root cause, not symptoms)
2. **WHY-Solution**: Why this solution? (decision rationale, alternatives considered)
3. **HOW**: How was it resolved? (implementation summary)

This is **historical documentation** for future maintainers, NOT a changelog entry.

**Title Writing Principle: Prioritize user-facing problems**

- ❌ "Fix empty login form submission error" (code perspective)
- ✅ "Fix login button not responding to clicks" (user perspective)
- ❌ "Handle null pointer exception" (technical perspective)
- ✅ "Fix app crash when accessing profile page" (user perspective)

### Anti-Patterns to Avoid

❌ **Change Lists (just narrating the diff)**:

```
fix: improve performance

- Added database index
- Implemented caching
- Optimized query
```

✅ **Root Cause + Rationale**:

```
fix: checkout page timing out under load

Sequential API calls to payment/inventory/shipping services caused cascading timeouts when any single service exceeded 3s threshold.

Switched to Promise.all() for parallel execution, reducing total wait time from 9s worst-case to 3s.
Rejected queue-based approach due to real-time inventory accuracy requirements.
```

❌ **Symptom Description Only**:

```
fix: users seeing error on profile page

Profile page crashed with null reference error.
Added null check to prevent crash.
```

✅ **Root Cause Analysis**:

```
fix: users seeing error on profile page

Profile API returns null for avatar_url when S3 object doesn't exist, but frontend assumed non-null contract based on outdated API docs.

Added null coalescing with default avatar rather than fixing API to maintain backwards compatibility with mobile app v1.x still in use.
```

❌ **Implementation Details Without Context**:

```
refactor: migrate to Redux Toolkit

Replaced all Redux boilerplate with Redux Toolkit.
Reduced code by 40%.
```

✅ **Decision Rationale**:

```
refactor: migrate to Redux Toolkit

Manual Redux pattern required 5 files per feature (actions, types, reducer, selectors, middleware) making new feature development take 2+ days just for state scaffolding.

Adopted Redux Toolkit to reduce boilerplate while maintaining Redux DevTools compatibility.
Rejected Zustand/Jotai because existing 200+ components deeply coupled to Redux patterns.
```

### Complexity-Based Formats

Keep it simple and concise. Use appropriate format based on complexity:

#### Very Simple Changes (No WHY needed)

Use ONLY for trivial changes where root cause is obvious:

```
type: brief description
```

**Example:**

```
docs: fix typo in README
```

#### Simple Changes (Minimal WHY)

For changes where root cause is straightforward but solution choice matters:

```
type: problem description

Root cause in one sentence.
Why this solution was chosen (if non-obvious).
```

**Example:**

```
fix: login button not responding with empty fields

Empty form validation Promise never rejected in error path, causing UI to freeze waiting for resolution.

Added explicit error handling to validation chain.
```

**For multiple changes/reasons, use list format:**

```
refactor: backend architect agent role redefinition

- Changed focus from API design to system structure design
- Modified to concentrate on domain modeling, layered architecture, and modularization strategy
```

#### Standard Changes

```
type: problem description

Description of the problem that occurred
(Brief reproduction steps if applicable)

Root cause explanation and why this solution approach was chosen

fix #N
```

**Example:**

```
fix: user list page failing to load

User list page showed continuous loading spinner with 1000+ users
(Reproduction: User List > View All click)

user_created_at column lacked index, causing full table scan on 1000+ record sorts with 30+ second query times.

Chose composite index + Redis caching over pagination because 8 existing UI screens depend on full dataset for client-side filtering.
Pagination would require frontend changes across all screens.

fix #32
```

#### Complex Changes (rarely needed)

```
type: problem description

Problem:
- Specific problem description
- Root cause analysis

Solution:
- Approach taken and why that method was chosen over alternatives
- Trade-offs and constraints that influenced the decision

fix #N
```

**Example:**

```
fix: users being logged out after service updates

Problem:
- All users forced to log out with each new deployment
- In-memory session storage lost on pod restart during rolling updates
- No session persistence mechanism across K8s instances

Solution:
- Chose Redis over sticky sessions because load balancer doesn't support session affinity in current infrastructure
- Added JWT refresh tokens for automatic re-authentication
- Rejected database session storage due to 200ms latency vs 5ms Redis

fix #48
```

**Important formatting rules:**

- First line (title): `type: clearly express the user-facing problem`
- description must start with lowercase, no period at end, use imperative mood
- Prefer user perspective > code/technical perspective when possible
- Except for very simple cases, don't just list changes - explain with sentences
- Include root cause and decision rationale when explaining solutions
- Keep descriptions concise - avoid verbose explanations
- If branch name ends with number (e.g., develop/32, develop/shlee/32), add "fix #N" at the end
- **When multiple changes/reasons exist, use bullet points (-) for better readability**
- **Never break sentences mid-way** - keep each sentence on a single line. Line breaks only after sentence ends

### Articulating "Why This Solution"

Good rationale mentions alternatives and trade-offs:

**Decision Framework:**

1. What other solutions were considered?
2. Why were they rejected?
3. What constraints drove the final choice?

**Examples:**

- ❌ Weak: "Used Redis for caching"
- ✅ Strong: "Chose Redis over in-memory cache because multiple API instances need shared cache state"

- ❌ Weak: "Refactored to use composition"
- ✅ Strong: "Switched from inheritance to composition because adding features required modifying 7 parent classes"

- ❌ Weak: "Fixed by adding validation"
- ✅ Strong: "Added input validation at API layer rather than database constraints to return user-friendly error messages"

**Common Trade-off Categories:**

- Performance vs maintainability
- Backwards compatibility vs clean design
- Quick fix vs structural refactor
- Client-side vs server-side solution
- Library dependency vs custom implementation

## Output Format

The command will provide:

1. Analysis of the staged changes (or all changes if nothing is staged)
2. **Creates commit_message.md file** containing both Korean and English versions
3. Copy your preferred version from the file

## Important Notes

- This command ONLY generates commit messages - it never performs actual commits
- **commit_message.md file contains both versions** - choose the one you prefer
- **Focus on root cause and rationale** - don't just list changes
- Explain solutions with **why you chose this approach over alternatives**
- Keep messages concise - don't over-explain what's obvious from the code
- Branch issue numbers (e.g., develop/32) will automatically append "fix #N"
- Copy message from generated file and manually execute `git commit`
- **Spec compliance**: All messages MUST follow Conventional Commits format
- **Type is mandatory**: No type = invalid commit for semantic-release
- **Case sensitivity**: Types must be lowercase (except `BREAKING CHANGE`)

## Execution Instructions for Claude

### Phase 1: Discover WHY (before analyzing diff)

1. Check current conversation for problem/solution discussion
2. Extract context from branch name, file names, test descriptions
3. Read changed files to find comments, function names, or test descriptions that signal intent
4. If context insufficient and changes are non-trivial, consider what problem the code is solving

### Phase 2: Analyze WHAT (git analysis)

5. Run git commands to see staged changes (or all if none staged)
6. Analyze file patterns and suggest appropriate commit type
7. Match changes to problem context from Phase 1

### Phase 3: Generate Message

8. Determine if scope is needed (e.g., `fix(api):`, `feat(ui):`)
9. Draft commit message following format:
   - Title: `<type>[(scope)]: <user-facing description>`
   - Body: MANDATORY three-step analysis (unless "Very Simple")
     a) Identify root cause: What underlying issue caused this problem?
     b) Explain solution rationale: Why this approach vs alternatives?
     c) Summarize implementation: How was it resolved?
   - Footer: Auto-add `fix #N` if branch name ends with number
10. Choose format complexity based on change scope (very simple/simple/standard/complex)

### Phase 4: Self-Verification

11. Self-check: "Does this message tell me something git diff doesn't?"
12. If not, revise to add root cause or decision rationale
13. Verify the message would help a developer 6 months from now understand WHY

### Output

14. Generate both Korean and English versions
15. Write to `commit_message.md`
16. Present suggested type with reasoning

**Context-aware analysis**: Balance token cost with message quality:

- Use `git log --oneline -5` to check commit style consistency
- Read only files with significant changes (avoid trivial whitespace changes)
- If changed files contain tests, read test descriptions for intent signals
- Look for TODO/FIXME comments near changes that explain intent
- Invest tokens in understanding WHY - a quality commit message beats a quick one
