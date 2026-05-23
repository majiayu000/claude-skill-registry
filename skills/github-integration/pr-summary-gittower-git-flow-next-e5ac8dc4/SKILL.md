---
name: pr-summary
description: Generate a PR summary and write to workflows/ pr_summary.md
allowed-tools: Read, Grep, Glob, Write, Bash
---

# Create PR Summary

Generate a comprehensive pull request summary based on branch changes.

## Instructions

1. **Gather Context**
   - Get current branch name
   - Find workflow folder for this branch
   - Read analysis.md and plan.md if they exist
   - Get associated issue number from branch name or commits

2. **Analyze Changes**
   ```bash
   # All commits on this branch
   git log main...HEAD --oneline

   # Full diff
   git diff main...HEAD --stat

   # Changed files
   git diff main...HEAD --name-only
   ```

3. **Categorize Changes**
   - New features added
   - Bugs fixed
   - Tests added/modified
   - Documentation updates
   - Refactoring

4. **Generate Summary**

   Write to `workflows/<folder>/pr_summary.md`:

   ```markdown
   # PR: <title>

   ## Summary
   <1-3 bullet points describing the key changes>

   ## Related Issues
   - Resolves #<number>
   - Relates to #<number>

   ## Changes

   ### Features
   - <New feature 1>
   - <New feature 2>

   ### Bug Fixes
   - <Fix 1>

   ### Code Changes
   | File | Change Type | Description |
   |------|-------------|-------------|
   | `path/to/file.go` | Modified | <brief description> |
   | `path/to/new.go` | Added | <brief description> |

   ### Tests
   - Added `TestXxx` - <what it tests>
   - Added `TestYyy` - <what it tests>

   ### Documentation
   - Updated `docs/xxx.md` - <what changed>

   ## Implementation Notes
   <Any important technical details reviewers should know>

   ## Test Plan
   Verification steps for reviewers:

   - [ ] Clone branch and build: `go build ./...`
   - [ ] Run tests: `go test ./...`
   - [ ] <Manual verification step 1>
   - [ ] <Manual verification step 2>

   ## Screenshots
   <If applicable - command output examples>

   ## Breaking Changes
   <None, or list breaking changes with migration steps>

   ## Checklist
   - [x] Code follows project guidelines
   - [x] Tests added for new functionality
   - [x] Documentation updated
   - [x] All tests pass
   - [x] No breaking changes (or documented above)
   ```

5. **Create PR Command**

   Also output the `gh pr create` command:

   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   ## Summary
   <summary bullets>

   ## Test Plan
   <test steps>

   ---
   Generated with Claude Code
   EOF
   )"
   ```

6. **Report Completion**
   - Show path to pr_summary.md
   - Show the PR creation command
   - Remind to push branch first if not already pushed

## PR Title Guidelines

- Use imperative mood: "Add feature" not "Added feature"
- Be specific but concise
- Include issue number if applicable: "Add squash merge support (#42)"

## Body Best Practices

- Lead with the most important information
- Keep summary bullets scannable
- Include enough context for reviewers
- Make test plan actionable
- Note any deployment considerations
