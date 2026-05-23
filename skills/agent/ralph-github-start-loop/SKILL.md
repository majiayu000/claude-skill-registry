---
name: ralph-github-start-loop
description: Runs autonomous loop fetching stories from GitHub Issues. Implements and closes issues as done. Triggers on "loop through my PRDs", "work on my issues", "start the autonomous loop", "implement my PRDs", or requests to work through GitHub issues autonomously.
disable-model-invocation: true
argument-hint: "[--all] [iterations] [prd-search]"
---

# Loop GitHub Issues

Run the autonomous loop to execute features from GitHub Issues.

## Usage

```
/loop-github-issues              # Interactive: shows available PRDs and asks which to run
/loop-github-issues --all        # Run all available PRDs (no prompt)
/loop-github-issues auth-flow    # Run PRDs matching search term
/loop-github-issues 25           # Run with 25 iterations per PRD
/loop-github-issues --all 25     # Run all PRDs with 25 iterations each
```

When running non-interactively (background mode), `--all` is auto-enabled.

## Prerequisites

- `gh` CLI authenticated
- PRD issues created via `/ralph-github-create-issues` (reads from `.claude/plans/` or `prds/`)

**Note:** Assume gh extensions are installed. Do NOT try to install them.

## Process

1. Check prerequisites (`gh auth status`)
2. Run the script directly - it handles PRD selection and filtering:

```bash
~/.claude/skills/loop-github-issues/loop-github-issues.sh [iterations] [prd-search-term] [--all]
```

Use `run_in_background: true` to prevent timeout.

**Monitoring progress:**
- Local status: `cat /tmp/ralph-status-{repo}-{prd-number}.txt`
- GitHub: Comments are posted to the PRD issue as stories complete

**Important**: Don't list PRDs separately before running - the script shows available PRDs (excluding those with open PRs) and handles selection.

### What It Does

1. Lists open PRD issues (identified by `prd` label) that don't already have open PRs
2. Prompts user to select which PRD(s) to work on (or auto-selects in background mode)
3. For each selected PRD:
   - Assigns issue to current user (shows as in progress)
   - Creates git worktree at `../{repo}-{feature}/`
   - For each iteration:
     - Passes all open sub-issues to the agent
     - Agent picks the logical next story based on dependencies
     - Implements the story
     - Commits: `feat: Story Title (closes #XXX)`
     - Closes sub-issue with link to commit
   - When all sub-issues closed, creates PR (parent PRD closes on merge)
   - Cleans up worktree

### Differences from `/ralph`

| Aspect | `/ralph` (JSON) | `/loop-github-issues` (GitHub) |
|--------|-----------------|--------------------------|
| Story source | `prds/*.json` | GitHub Issues |
| Status tracking | `passes: true/false` | Issue open/closed |
| Dependencies | `dependsOn` array | Native GitHub blocking |
| Completion | Update JSON | Close issue |
| PRD done | All stories pass | All sub-issues closed |

### Dependencies

Ralph-issues checks GitHub's native blocking relationships. PRDs with open blocking issues are skipped.

The script queries the `blockedBy` field via GraphQL to determine if a PRD is ready to start.

## Issue Conventions

### Finding PRD Issues

```bash
gh issue list --label prd --state open --json number,title,body
```

### Finding Story Sub-Issues

Uses the `gh-sub-issue` extension:
```bash
gh sub-issue list <parent-number> --state open --json number,title,body
```

### Closing Issues

On story completion:
```bash
gh issue close 101 --comment "Implemented in https://github.com/owner/repo/commit/abc123"
```

Parent PRD issues close automatically when the PR is merged (via `Closes #XX` in PR body).

## Branch Naming

Uses conventional prefixes parsed from the PRD issue body:
- `feature/<name>` for enhancements
- `bugfix/<name>` for bug fixes

## Notes

- Run multiple Ralph instances in parallel on independent PRDs (separate terminals)
- Each works in its own worktree, no conflicts
- Commits include `closes #XXX` to auto-close issues on merge
