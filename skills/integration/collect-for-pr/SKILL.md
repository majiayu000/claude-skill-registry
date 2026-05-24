---
name: collect-for-pr
description: Collect pending worktree commits into a PR for review. Use this skill when subdirectory worktrees have accumulated 4-7+ commits that should be batched together and submitted for review. Invoked with /collect-for-pr or automatically when monitoring worktree status.
---

# Collect Commits for PR

You are a coordinator agent that gathers matched function commits from subdirectory worktrees into PRs for review. Your job is to batch commits efficiently and create well-organized pull requests.

## When to Use This Skill

Use `/collect-for-pr` when:
- Subdirectory worktrees have accumulated commits ready for review
- You want to batch 4-7+ commits into a single PR (flexible threshold)
- After a decomp session to collect completed work

## Workflow

### Step 1: Check Worktree Status

```bash
melee-agent worktree list --commits
```

This shows all subdirectory worktrees with their pending commits. Look for:
- **Pending commits**: How many commits are waiting on each worktree
- **Total across worktrees**: Whether there's enough work to batch

**Automatic limits:**
The collect command now automatically limits PRs to **7 function match commits** by default.
Fix-up commits (build fixes, header updates, etc.) don't count toward this limit.

- Use `--max-functions N` to adjust the limit
- Use `--no-limit` to collect all pending commits
- Deferred commits remain on worktree branches for the next PR

### Step 2: Dry Run First

Always preview what will be collected. The `--source-dir` parameter is required:

```bash
melee-agent worktree collect --source-dir lb --dry-run
```

This shows:
- Which commits will be cherry-picked from that subdirectory
- Total commit count

**Review the output for:**
- Build fix commits that should go together with function matches
- Logical groupings within the subdirectory

### Step 3: Collect and Create PR

If the dry run looks good, collect and create the PR:

```bash
melee-agent worktree collect --source-dir lb --create-pr
```

This will:
1. Create a new branch from `upstream/master` (named `batch/lb-YYYYMMDD`)
2. Cherry-pick pending commits from the specified subdirectory
3. Push the branch to origin
4. Create a GitHub PR with organized commit listing
5. Reset pending commit counts in the database

**Custom branch name (optional):**
```bash
melee-agent worktree collect --source-dir lb --create-pr --branch "batch/lb-module-cleanup"
```

### Step 4: Handle Conflicts

If cherry-picks fail:
- The command aborts the cherry-pick automatically
- Failed commits are listed with error details
- Successful commits are still collected

**For failed commits:**
1. Note which subdirectories have conflicts
2. The commits remain on their subdirectory branches
3. They can be collected in a future PR after resolving

### Step 5: Monitor PR and Fix Issues

After creating the PR, use the feedback command to monitor for issues:

```bash
# Get all PR feedback in one call
melee-agent pr feedback https://github.com/doldecomp/melee/pull/XXXX

# JSON output for automated processing
melee-agent pr feedback https://github.com/doldecomp/melee/pull/XXXX --json
```

This command consolidates:
- **CI check status** - Pass/fail with parsed error messages (compile errors, linker errors)
- **Review comments** - Both inline and PR-level comments from reviewers
- **decomp-dev report** - Regressions and improvements detected by the bot
- **Action items** - Generated list of what needs to be fixed

**If issues are found:**
1. Fix the issues on the appropriate subdirectory worktree
2. Push fix commits to the PR branch
3. Re-run `melee-agent pr feedback` to verify fixes

### Step 6: Post-PR Cleanup

After the PR is merged, clean up empty worktrees:

```bash
melee-agent worktree prune --dry-run  # Preview
melee-agent worktree prune            # Execute
```

## Decision Framework

### Should I Create a PR Now?

Each subdirectory worktree is collected separately. Consider each subdirectory independently:

| Situation | Recommendation |
|-----------|----------------|
| 5-7 function matches in a subdirectory | Yes, good batch size (default limit) |
| 8+ function matches | Run collect (it will auto-limit to 7, defer the rest) |
| 2-4 function matches but work has stopped | Yes, ship what's ready |
| 1-2 function matches with active work ongoing | Wait for more |
| Many fix-up commits | Include them - they don't count toward limit |

**Note:** The `--max-functions` limit only counts function match commits. Fix-up commits
(build fixes, header updates, signature changes) are always included and don't count.

### PR Timing

- **End of work session**: Collect all completed work
- **Before switching focus**: Don't leave commits unbatched
- **Module completion**: When finishing a focused module push
- **CI keeps up**: Don't create multiple PRs faster than CI can process

## What the Commands Do

### `worktree list`
Shows all subdirectory worktrees with status:
- Commits pending (ahead of upstream/master)
- Lock status
- Last activity time
- Uncommitted changes (work in progress)

### `worktree collect --source-dir <subdir>`
Cherry-picks commits from a specific subdirectory branch:
- Requires `--source-dir` to specify which subdirectory to collect
- Creates new branch from upstream/master (named `batch/<subdir>-YYYYMMDD`)
- Cherry-picks commits from that subdirectory
- Tracks success/failure per commit
- Optionally creates GitHub PR with `--create-pr`

### `worktree prune`
Removes worktrees with no pending commits:
- Only removes fully merged worktrees
- Use `--force` to remove with uncommitted changes
- Use `--max-age N` to only prune old worktrees

### `pr feedback <url>`
Gets all feedback on a PR in one call:
- CI check status with parsed build errors
- Review comments (inline and PR-level)
- decomp-dev bot regression reports
- Generated action items list
- Use `--json` for agent-friendly output

## Example Session

```bash
# Check what's available
melee-agent worktree list --commits
# Output shows:
#   lb:           6 commits (match, match, match, fixup, match, match)
#   ft-chara-ftFox: 2 commits (match, fixup)
#   gr:           2 commits (match, match)

# Preview collection for lb subdirectory
melee-agent worktree collect --source-dir lb --dry-run
# Shows commits from lb that will be cherry-picked
# Classifies each as [match] or [fixup]

# Create the PR for lb
melee-agent worktree collect --source-dir lb --create-pr
# Creates batch/lb-20241230 branch, cherry-picks commits, creates PR
# Returns PR URL: https://github.com/doldecomp/melee/pull/XXXX

# Monitor PR for issues
melee-agent pr feedback https://github.com/doldecomp/melee/pull/XXXX
# Shows CI status, review comments, decomp-dev report, action items

# If CI fails or reviewers request changes, fix and push
# Then re-check:
melee-agent pr feedback https://github.com/doldecomp/melee/pull/XXXX

# After PR merges, clean up
melee-agent worktree prune
```

## PR Quality Checklist

**IMPORTANT**: Before creating a PR, you MUST review ALL commits in the batch against this checklist. These are common issues identified from doldecomp/melee PR reviews:

### Automated Checks (ALL are errors that block commits)

Run `melee-agent hook validate` - ALL issues below will block the commit:

1. **Use `true`/`false` not `TRUE`/`FALSE`**
   - Lowercase boolean literals are required

2. **Float literals need F suffix**
   - Use `1.0F` not `1.0` for f32 values

3. **Hex literals use uppercase**
   - Use `0xABCD` not `0xabcd`

4. **Don't use raw struct accesses/pointer arithmetic**
   - BAD: `*(s32*)((u8*)ptr + 0x10)`
   - GOOD: Use `M2C_FIELD(ptr, 0x10, s32)` or fill in actual struct fields

5. **Don't add unnecessary extern declarations**
   - BAD: `extern UNK_T lbl_804D1234;` at file top
   - GOOD: Include the proper header or create one

6. **Don't rename descriptive symbols to address-based names**
   - BAD: Renaming `ItemStateTable_GShell` → `it_803F5BA8`
   - GOOD: Keep meaningful names

7. **clang-format must pass**
   - Run `git clang-format` before committing

8. **symbols.txt must be updated**
   - New functions need corresponding symbols.txt entries

9. **No implicit function declarations**
   - All functions must have proper prototypes

10. **Header signatures must match implementations**
    - No UNK_RET/UNK_PARAMS mismatches

11. **No local scratch URLs in commits**
    - Commit messages must use production decomp.me URLs
    - Run `melee-agent sync production` before committing to sync scratches
    - Local URLs like `nzxt-discord.local`, `10.200.0.1`, `localhost:8000` will be rejected

### Manual Review Required (not yet automated)

12. **Use `bool` return type for boolean functions**
    - If a function returns 0/1 for false/true, use `bool` not `s32`

13. **Change argument/field types instead of casting**
    - BAD: Adding casts to work around type mismatches
    - GOOD: Change the actual type in the struct or function signature

14. **Keep temporary struct types instead of raw pointer arithmetic**
    - If m2c created a temp struct for field access, keep it

15. **Don't modify unrelated files**
    - If a file shouldn't be in the PR (like `.gitkeep`), revert it

16. **Don't mess with NonMatching/symbols.txt incorrectly**
    - Understand the matching/nonmatching workflow

17. **Always use m2c first**
    - Don't try to one-shot decompile without using m2c
    - m2c output should be the starting point, then cleaned up

### Pre-PR Review Process

Before running `melee-agent worktree collect --create-pr`:

```bash
# 1. Run automated checks
melee-agent hook validate -v

# 2. Review each commit's diff for manual issues
git log upstream/master..HEAD --oneline  # List commits
git show <hash>  # Review each commit

# 3. Search for common issues
grep -r "TRUE\|FALSE" melee/src/  # Boolean literals
grep -rn "0x[0-9a-f]*[a-f]" melee/src/  # Lowercase hex

# 4. If issues found, fix them BEFORE creating PR
# Make fix commits on the subdirectory worktrees
```

## What NOT to Do

1. **Don't create PRs with 1-2 commits** unless work has completely stopped
2. **Don't skip the dry run** on large batches
3. **Don't force-prune worktrees with uncommitted changes** without checking first
4. **Don't create multiple overlapping PRs** - wait for CI on previous PR
5. **Don't ignore cherry-pick failures** - note them for future resolution
6. **Don't skip the quality checklist** - reviewers will request changes

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Branch already exists | Use `--branch` to specify different name |
| Cherry-pick conflict | Commits stay on subdirectory branch for later |
| No pending commits | Nothing to collect - keep working |
| Push failed | Check git remote auth, push manually if needed |
| PR creation failed | Branch is ready, create PR manually via GitHub |

## Integration with Other Skills

- **After `/decomp`**: Commits accumulate on subdirectory worktrees
- **Before `/decomp-fixup`**: Check if fixes should go in same batch
- **Coordination**: Each subdirectory is collected separately, avoiding cross-subdirectory conflicts
