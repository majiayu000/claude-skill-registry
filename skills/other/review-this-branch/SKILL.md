---
name: review-this-branch
description: "{{ 𝛀𝛀𝛀 }} Assess branch readiness for PR submission"
model: opus
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Bash(git:*)"]
---

Assess whether this branch is ready to be submitted as a reviewable pull request.

## Analysis Steps

1. Identify the base branch (usually `main`) and list all commits since diverging
2. Review the full diff for:
   - Incomplete work (half-implemented features, placeholder logic)
   - Obvious bugs or unhandled edge cases
   - Code quality issues that would block a reviewer
3. Check commit history:
   - Conventional commit compliance (`type(scope): description`)
   - Logical atomicity — each commit should represent one coherent change
   - No WIP, fixup, or junk commits that should have been cleaned up
4. Check branch name against naming conventions:
   - Format: `<prefix>/<short-description>` (lowercase, hyphens, imperative)
   - Valid prefixes: `feat`, `fix`, `enhance`, `refactor`, `types`, `perf`, `styles`, `layout`, `docs`, `test`, `deps`, `config`, `build`, `agents`, `chore`, `ci`, `deploy`, `spike`, `experiment`, `wip`, `hotfix`
   - Breaking change branches should use `<prefix>/breaking-<description>`
5. Scan for anti-patterns:
   - Debugging artefacts (`console.log`, commented-out code)
   - Unresolved conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
   - `TODO` / `FIXME` comments introduced in this branch
   - Diff size >500 lines (flag for possible split)
6. Detect breaking changes:
   - Removed or renamed exports, functions, types, or components
   - Changed function signatures (required parameters added/reordered)
   - Modified return types in a widening direction
   - Database schema changes (columns removed/renamed, constraints changed)
   - HTTP API changes (routes, methods, request/response shapes)
   - New required environment variables
   - Changed component props (removed, renamed, type-changed, newly required)

## Output Format

### Verdict
One of: **Ready** | **Needs Work** | **Blocked**

### Branch Health
- Branch name compliance
- Commit message quality
- Commit atomicity

### Code Quality Flags
Specific issues found, with file and line references where possible. Omit this section if none found.

### Breaking Changes
Any detected breaking changes with context. Flag format:
> ⚠️ Breaking change — consider `feat!:` or `BREAKING CHANGE:` footer

Omit this section if none found.

### Recommended Next Steps
Ordered list — blockers first, then improvements, then nice-to-haves.

---

If the verdict is **Ready**, offer to run `/git:pull-request` immediately.
