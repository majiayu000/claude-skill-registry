---
name: ru-review
description: Review GitHub issues and PRs across repositories using the ru CLI tool. Use when asked to review issues, PRs, or run ru review. CRITICAL - never stash or discard user changes; commit them first if needed.
---

# ru review - GitHub Issues/PRs Review Process

## Overview

The `ru` (Repo Updater) CLI has a built-in `ru review` command that reviews GitHub issues and PRs across all configured repositories using Claude. It includes the project's contribution policy automatically.

## ⚠️ CRITICAL RULES - NEVER VIOLATE THESE ⚠️

### 1. NEVER Stash User Changes
If repositories have uncommitted changes, **NEVER use `git stash`**. This risks losing user work and is extremely dangerous. Stashed changes can be difficult to recover, especially untracked files which require `git show stash@{0}^3:path` to extract.

### 2. NEVER Modify Working Tree State Without Permission
Do not run `git checkout`, `git reset`, `git clean`, or any command that modifies uncommitted changes without explicit user permission.

### 3. Commit Changes First (The Correct Approach)
If repos have uncommitted changes and the user wants to proceed with review, **commit the changes first**. Use this exact approach:

```
Now, based on your knowledge of the project, commit all changed files now in a series of logically connected groupings with super detailed commit messages for each and then push. Take your time to do it right. Don't edit the code at all. Don't commit obviously ephemeral files. Use ultrathink.
```

**How to group commits logically:**
- Group by feature/subsystem (e.g., all sync-related files together)
- Group by type of change (e.g., all test files together if they test one feature)
- Keep config/infrastructure changes separate from feature changes
- Use clear commit message format: `feat(scope): description` or `fix(scope): description`

**Skip ephemeral files (do NOT commit):**
- `target/`, `target_*/` - Rust build directories
- `node_modules/`, `web/node_modules/` - npm packages
- `*.pyc`, `__pycache__/` - Python bytecode
- `playwright-report/`, `test-results/` - Test artifacts
- `.coverage`, `htmlcov/` - Coverage reports
- `*.log` files

### 4. Skip Dirty Repos - ru Handles This
The `ru review` command automatically skips repositories with uncommitted changes. This is the correct behavior. Let it skip them rather than trying to force them clean.

## Decision Tree: Handling Dirty Repos

```
Found uncommitted changes in repos?
├── User wants to proceed with ru review?
│   ├── YES → Ask: "Should I commit these changes first?"
│   │   ├── User says YES → Commit with logical groupings, push, then run ru review
│   │   └── User says NO → Let ru skip those repos, review clean repos only
│   └── NO → Stop, let user handle their changes
└── No uncommitted changes → Run ru review normally
```

## How ru review Works

### Discovery Phase
```bash
ru review --dry-run  # See what issues/PRs exist without starting sessions
```

### Plan Mode (Default)
```bash
ru review --plan  # Generate review plans, no mutations
```

### Apply Mode
```bash
ru review --apply  # Execute approved plans from previous --plan run
```

### Key Options
- `--mode=local` - Use local Claude instead of ntm
- `--max-repos=N` - Limit number of repos to review
- `--repos=PATTERN` - Filter repos by pattern (regex)
- `--skip-days=N` - Skip repos reviewed within N days
- `--parallel=N` - Concurrent review sessions (default: 4)
- `--push` - Allow pushing changes (with --apply)

## ⚠️ ABSOLUTE RULE: WE DO NOT MERGE PRs - EVER ⚠️

**WE. DO. NOT. MERGE.**

We don't allow PRs or outside contributions to any of these projects as a matter of policy. Here is the policy disclosed to users:

> *About Contributions:* Please don't take this the wrong way, but I do not accept outside contributions for any of my projects. I simply don't have the mental bandwidth to review anything, and it's my name on the thing, so I'm responsible for any problems it causes; thus, the risk-reward is highly asymmetric from my perspective. I'd also have to worry about other "stakeholders," which seems unwise for tools I mostly make for myself for free. Feel free to submit issues, and even PRs if you want to illustrate a proposed fix, but know I won't merge them directly. Instead, I'll have Claude or Codex review submissions via `gh` and independently decide whether and how to address them. Bug reports in particular are welcome. Sorry if this offends, but I want to avoid wasted time and hurt feelings. I understand this isn't in sync with the prevailing open-source ethos that seeks community contributions, but it's the only way I can move at this velocity and keep my sanity.

### What This Means In Practice

1. **NEVER run `gh pr merge`** - Not ever. Not for any reason.
2. **NEVER recommend merging a PR** - Don't even suggest it.
3. **PRs are for INSPIRATION ONLY** - You can look at them to see if they contain good ideas.
4. **Even good ideas need approval** - Check with the user first before integrating even ideas from PRs, as they could take the project in an unwanted direction or introduce scope creep.
5. **Implement fixes YOURSELF** - If a PR or issue identifies a real problem, write your own fix from scratch after independent verification.

### Independent Verification Protocol

When reviewing issues and PRs:
1. **Do NOT trust user reports** - They may be wrong, outdated, or misguided.
2. **Do NOT trust proposed fixes** - They may introduce bugs, security issues, or scope creep.
3. **Check dates** - Many issues may already be fixed by subsequent commits.
4. **Verify against actual code** - Read the current codebase, not what the user claims.
5. **Test empirically** - Run the code, check behavior, verify claims.
6. **Use official documentation** - Not user interpretations.
7. **Write your own implementation** - Even if inspired by a PR, the code must come from your own understanding.

### After Review Actions

Use `gh` to respond on behalf of the owner:
- **Close issues** that are already fixed or invalid
- **Comment on issues** to acknowledge valid bugs (then fix them yourself)
- **Comment on PRs** to thank contributors but explain the no-merge policy
- **Close PRs** after extracting any useful information (if applicable)

## Coordinating with Other Agents

When multiple agents are reviewing repos simultaneously:

1. **Use alphabetical ordering** - One agent works forward (A→Z), another works reverse (Z→A)
2. **Check which repos are already in progress** - Look for uncommitted changes or lock files
3. **Skip repos being worked on** - Don't try to review a repo another agent is actively modifying

Example: If another agent is working on `beads_viewer`, start from `xf` and work backwards through `wasm_cmaes`, `ultrasearch`, etc.

## Typical Workflow

1. **Check what needs review**
   ```bash
   ru review --dry-run
   ```

2. **Start plan-mode review**
   ```bash
   ru review --plan --mode=local
   ```

3. **If repos have uncommitted changes:**
   - Let ru skip them automatically
   - OR ask user if they want to commit changes first
   - NEVER stash or discard changes

4. **After review plans are approved:**
   ```bash
   ru review --apply --push
   ```

## Troubleshooting

### "Repository has uncommitted changes"
This is normal and expected. Options:
- Let ru skip those repos (recommended)
- Ask user to commit their changes first
- Wait for other agents to finish their work

### "Failed to prepare worktrees"
This often means some repos were skipped due to uncommitted changes but others succeeded. The review will still run on the successfully prepared repos.

### Checkpoint Issues
If you see "Invalid JSON, refusing to write checkpoint":
```bash
rm -f ~/.local/state/ru/review/review-checkpoint.json
```

## What NOT to Do

- ❌ `git stash` - NEVER stash user changes
- ❌ `git checkout -- .` - NEVER discard changes
- ❌ `git reset --hard` - NEVER reset working tree
- ❌ `git clean -fd` - NEVER clean untracked files
- ❌ Shell loops to iterate repos - ru handles iteration internally
- ❌ Direct `gh` commands for bulk operations - use ru's orchestration

## What TO Do

- ✅ Use `ru review --dry-run` to discover work items
- ✅ Let ru skip repos with uncommitted changes
- ✅ Ask user before modifying their working tree state
- ✅ Commit changes (with user permission) before review if needed
- ✅ Use `--mode=local` if ntm has issues
- ✅ Work in reverse alphabetical order when coordinating with other agents

## Emergency: Recovering from Accidental Stash

If someone accidentally stashed changes, here's how to recover:

### Tracked Files (Easy)
```bash
git stash pop  # Restore tracked changes
```

### Untracked Files (Harder - requires extraction)
Untracked files in a stash are stored in the third parent commit. To recover:

```bash
# List untracked files in stash
git show stash@{0}^3 --name-only

# Extract a specific untracked file
git show stash@{0}^3:path/to/file.rs > path/to/file.rs
```

### If Stash Was Dropped
```bash
# Find dangling stash commits
git fsck --unreachable | grep commit

# For each commit, check if it's your stash
git show <commit-hash>

# Recover if found
git stash apply <commit-hash>
```

## Example: Complete Review Session

```bash
# 1. Discovery - see what needs review
ru review --dry-run

# 2. Check for dirty repos
for repo in /data/projects/*/; do
  (cd "$repo" && [ -n "$(git status --porcelain)" ] && echo "$repo has changes")
done

# 3. If dirty repos exist, commit them first (with user permission)
# Use logical groupings, detailed messages, push each repo

# 4. Run the review
ru review --plan --mode=local

# 5. After plans approved
ru review --apply --push
```

## Review Response Guidelines

When reviewing issues and PRs, remember:
- **Verify independently** - Don't trust submitted code blindly
- **Check actual behavior** - Run tests, verify against docs
- **Use gh commands** to respond on behalf of the user
- **Close issues** that are resolved or invalid
- **Request clarification** if issue is unclear

## ⚠️ IMPORTANT: Check Twitter Before Responding on Behalf of Jeffrey

When the repo owner is **Jeffrey Emanuel** (GitHub: `Dicklesworthstone`, X/Twitter: `@doodlestein`), you MUST check his recent Twitter posts before giving advice or making statements in his name on topics he may have publicly discussed.

### Why This Matters
Jeffrey has public opinions on many technical topics. Responses on his behalf should be consistent with his stated positions. Checking Twitter ensures you don't contradict something he's already said publicly.

### How to Check Twitter
Use the `xf` tool to search his Twitter archive:

```bash
# Search for relevant tweets on a topic
xf search "contribution policy" --limit 10

# Search for opinions on specific tech
xf search "local LLM" --limit 10

# Search recent tweets (within last N days)
xf search "openrouter" --since "90 days ago" --limit 10
```

The Twitter data is indexed at `/data/projects/my_twitter_data` and accessible via `xf`.

### When to Check
- Before responding to feature requests (check if he's discussed the feature)
- Before explaining project philosophy (check his stated positions)
- Before declining/accepting approaches (check if he's opined on similar)
- Before discussing tools, frameworks, or tech choices

### Example Workflow
```bash
# User asks about OpenRouter support
xf search "openrouter" --limit 5

# User asks about contribution policy
xf search "contribution" --limit 5
xf search "pull request" --limit 5

# User asks about local models
xf search "local model" --limit 5
xf search "ollama" --limit 5
```

If you find relevant tweets, incorporate his stated position into your response. If no relevant tweets exist, proceed with your best judgment based on project context.
