---
name: commit
description: Generate Conventional Commits-compliant messages (feat/fix/docs/chore) in Korean and English. Use when you need to create a well-structured commit message for staged changes.
allowed-tools: Bash(git status:*), Bash(git diff:*), Bash(git log:*), Bash(git branch:*), Read, Grep, Write
disable-model-invocation: true
---

# Conventional Commits Message Generator

Generates commit messages following [Conventional Commits v1.0.0](https://www.conventionalcommits.org/) specification in both Korean and English. **Choose one version for your commit.**

## Repository State Analysis

- Git status: !`git status --porcelain`
- Current branch: !`git branch --show-current`
- Staged changes: !`git diff --cached --stat`
- Unstaged changes: !`git diff --stat`
- Recent commits: !`git log --oneline -10`

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

## Commit Message Format Guidelines

**Core Principle: Root Cause → Rationale → Implementation**

Commit messages document decision **history**, not just code changes. Every non-trivial commit body MUST answer:

1. **WHY-Problem**: Why did this problem exist? (root cause, not symptoms)
2. **WHY-Solution**: Why this solution? (decision rationale, alternatives considered)
3. **HOW**: How was it resolved? (implementation summary)

### Complexity-Based Formats

#### Very Simple Changes (No WHY needed)

```
type: brief description
```

#### Simple Changes (Minimal WHY)

```
type: problem description

Root cause in one sentence.
Why this solution was chosen (if non-obvious).
```

#### Standard Changes

```
type: problem description

Description of the problem that occurred
(Brief reproduction steps if applicable)

Root cause explanation and why this solution approach was chosen

fix #N
```

## Output Format

The command will provide:

1. Analysis of the staged changes (or all changes if nothing is staged)
2. **Creates commit_message.md file** containing both Korean and English versions
3. Copy your preferred version from the file

## Important Notes

- This command ONLY generates commit messages - it never performs actual commits
- **commit_message.md file contains both versions** - choose the one you prefer
- **Focus on root cause and rationale** - don't just list changes
- Branch issue numbers (e.g., develop/32) will automatically append "fix #N"
- Copy message from generated file and manually execute `git commit`
- **Spec compliance**: All messages MUST follow Conventional Commits format

## Execution Instructions

### Phase 1: Discover WHY (before analyzing diff)

1. Check current conversation for problem/solution discussion
2. Extract context from branch name, file names, test descriptions
3. Read changed files to find comments, function names, or test descriptions that signal intent

### Phase 2: Analyze WHAT (git analysis)

4. Run git commands to see staged changes (or all if none staged)
5. Analyze file patterns and suggest appropriate commit type
6. Match changes to problem context from Phase 1

### Phase 3: Generate Message

7. Determine if scope is needed (e.g., `fix(api):`, `feat(ui):`)
8. Draft commit message following format
9. Choose format complexity based on change scope

### Phase 4: Self-Verification

10. Self-check: "Does this message tell me something git diff doesn't?"
11. If not, revise to add root cause or decision rationale

### Output

12. Generate both Korean and English versions
13. Write to `commit_message.md`
14. Present suggested type with reasoning
