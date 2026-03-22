---
name: git-version-control
description: Git commit standards, branch strategy, and LLM-assisted development workflows. Use when making commits, managing branches, or working in high-velocity LLM-assisted development contexts. Covers atomic commits, conventional commits, branching strategies (trunk-based, GitHub flow), merge vs rebase decisions, and recovery patterns.
---

# Git Version Control

<skill_scope skill="git-version-control">
**Related skills:**
- `software-engineer` — Design principles that inform commit granularity
- `test-driven-development` — Test-commit cycles and when to commit during TDD

This skill covers Git commit standards, branch strategy, and LLM-assisted development workflows. It emphasizes atomic commits, meaningful commit messages, and high-frequency integration.
</skill_scope>

## Core Philosophy

<core_philosophy>
**"Commit Often, Perfect Later, Publish Once"** — Seth Robertson

**Integration frequency is the most powerful determinant of branching success.** Elite teams integrate multiple times daily. "If it hurts, do it more often." — Martin Fowler

**Revertability principle**: Commits should represent meaningful units of work that could be reverted independently without breaking the system.
</core_philosophy>

## Commit Practices

<atomic_commits>
**Atomic commit decision:** "If you can describe what you did in a short sentence and it makes sense, commit."

**When larger commits are acceptable:** Initial prototyping (squash before review), closely coupled changes, when over-granularity loses context.

**Time guideline:** 30-60 min ideal, max 4 hours. See `<commit_triggers>` for event-based commit points.
</atomic_commits>

### Commit Triggers

<commit_triggers>
**Commits are responses to completion events, not scheduled activities.**

Commit discipline isn't about remembering to commit—it's about recognizing completion signals.

<observable_completion_events>
#### Observable Completion Events

| Event | Action | Rationale |
|-------|--------|-----------|
| Tests pass after a change | Commit | Green is a save point |
| Build succeeds after a change | Commit | Working state confirmed |
| Linter/type checker passes | Commit | Code meets standards |
| Todo item marked complete | Commit | Logical unit finished |
| User confirms functionality | Commit | Acceptance achieved |
| Configuration value tweaked | Commit | Discrete, working change |

**Key insight:** Passing tests/builds are commit signals, not just validation. Green means save your progress.
</observable_completion_events>

<transition_points>
#### Transition Points

| Transition | Action | Rationale |
|------------|--------|-----------|
| Before starting different task | Commit current work | Clean separation |
| Before risky/experimental change | Commit as checkpoint | Safe rollback point |
| After reverting failed approach | Commit clean state | Document decision |
| Before context window compaction | Commit all work | Preserve across sessions |
</transition_points>

<conversational_cues>
#### LLM-Assisted Conversational Cues

In LLM-assisted development, user messages signal completion:

| User Says | Likely Meaning | Action |
|-----------|----------------|--------|
| "That works", "looks good", "perfect" | Acceptance | Commit |
| "Done", "ship it", "let's move on" | Task complete | Commit |
| "Now let's work on..." | Topic change | Commit previous work first |
| "Can you also..." | Scope expansion | Consider committing current state |

**Anti-pattern:** Batching multiple unrelated changes because "I'll commit later." Each completion event deserves its own commit.
</conversational_cues>
</commit_triggers>

### Branch Discipline

<branch_discipline>
Before committing, verify you're on the appropriate branch:

| Situation | Action |
|-----------|--------|
| On main, multi-commit work expected | Create feature branch first |
| On main, single quick-fix commit | Acceptable to commit directly |
| On feature branch | Commit freely |
| Unsure how many commits needed | Create feature branch (safer default) |

**LLM-assisted pattern:** When starting work that might need multiple commits, proactively create a feature branch before the first commit. Ask the user if uncertain about scope.

<merge_strategy>
**Merge strategy for completed branches:**

| Branch State | Recommended Merge | Rationale |
|--------------|-------------------|-----------|
| 1-2 clean commits | ff-merge or rebase-merge | Preserves meaningful history |
| 3-5 commits | Consider squash-merge | Balance history vs. noise |
| >5 commits | Strongly prefer squash-merge | Collapse implementation noise |
| Messy/WIP commits | Squash-merge | Hide the sausage-making |

**Squash preference:** Feature branches with more than 3-5 commits should generally be squash-merged. The intermediate commits represent implementation exploration, not meaningful history. Mainline should tell the story of *what* changed, not *how you figured it out*.
</merge_strategy>
</branch_discipline>

<conventional_commits>
**Style preference:** Use full keywords (`feature:` not `feat:`). Imperative mood. Subject ≤50 chars, body wraps at 72, explain WHY.

**Imperative mood test:** Subject line should complete the sentence "If applied, this commit will _____."[^beams] Examples: "Add caching for API responses" ✓, "Added caching" ✗, "Adds caching" ✗.

**Content principles:**
- **Delta, not journey** — Describe what changed, not how you discovered what to change. The debugging process doesn't belong in the permanent record.
- **Neutral framing** — Avoid judgmental language about prior state ("fix broken", "remove wrong", "correct mistake"). Prefer neutral verbs: "update", "change", "revise".
- **Outcome, not process** — Don't document how you verified, tested, or arrived at the change. The commit message records *what*, not *how you figured it out*.
- **Let the diff speak** — Implementation details belong in the diff. The message explains intent and scope; the diff shows specifics.

**Anti-pattern:** "Fix incorrect attribution that cited Apple docs when the quote was actually from a community blog post" — this documents the debugging journey, uses judgmental framing, and includes detail the diff already shows.

**Better:** "Update source attributions" — neutral, outcome-focused, appropriate abstraction level.
</conventional_commits>

<fixup_workflow>
```bash
git commit --fixup=<sha>           # Creates "fixup! Original message"
git rebase --autosquash origin/main # Squashes fixups automatically
git config --global rebase.autosquash true
```
</fixup_workflow>

## Branching Strategies

<branching_decision>
| Context | Strategy | Integration |
|---------|----------|-------------|
| Single production version, strong CI/CD | Trunk-Based | Multiple times daily |
| Continuous deployment, web apps | GitHub Flow | Daily+ |
| Multiple production versions | Git Flow | Per release |

**Trunk-based:** Short-lived branches (<24h), feature flags for incomplete work.

**Branch naming:** `<category>/<ticket-id>-<description>` (e.g., `feature/PROJ-4521-add-oauth`)
</branching_decision>

<merge_vs_rebase>
**Rebase:** Private branches, linear history, working alone.
**Merge:** Public/shared branches, preserve collaboration history, audit trails.

**GOLDEN RULE:** Never rebase commits others may have based work on.

**Force push safety:** After rebasing a personal branch, use `--force-with-lease` instead of `--force`. It fails if someone else pushed, preventing you from overwriting their work.
```bash
git push --force-with-lease  # Safe
git push --force             # Dangerous
```

**CRITICAL: NEVER force push to main/master branches.** Even with `--force-with-lease`, force pushing to primary branches can destroy team history, break CI/CD pipelines, and cause widespread disruption. If this is ever requested, warn about the consequences first.
</merge_vs_rebase>

<interactive_limitations>
**LLM-assisted context limitation:** Interactive git commands (`git rebase -i`, `git add -i`, `git add -p`) require terminal interaction and are unavailable in LLM-assisted contexts. Use alternatives:
- Instead of `git rebase -i`: Use `--autosquash` with fixup commits
- Instead of `git add -i`: Use explicit `git add <file>` commands
- Instead of `git add -p`: Stage specific files, or use GUI tools
</interactive_limitations>

## LLM-Assisted Development Patterns

### Checkpoint Commits

<llm_checkpoints>
Lightweight savepoints before LLM modifications without commit overhead.

**Git aliases** (adapted from Nathan Orick's checkpoint pattern[^orick]):
```bash
[alias]
checkpoint = "!f() { git add -A && git commit --no-verify -m \"SAVEPOINT\"; git tag \"checkpoint/$(date +%Y_%m_%d_%H_%M_%S)\"; git reset HEAD~1 --mixed; }; f"
listCheckpoints = tag -l "checkpoint/*"
loadCheckpoint = "!f() { git reset --hard checkpoint/$1 && git reset HEAD~1 --mixed; }; f"
deleteCheckpoint = "!f() { git tag -d checkpoint/$1; }; f"
```

**Workflow:**
```bash
git checkpoint                              # Before LLM changes
git listCheckpoints                         # View savepoints
git loadCheckpoint 2024_11_15_13_25_55      # Restore if bad
```
</llm_checkpoints>

### Commit Frequency by Context

<commit_frequency>
| Context | Frequency | Granularity |
|---------|-----------|-------------|
| Solo prototyping | Very high | Very fine |
| Team feature dev | Hourly | Atomic units |
| Pre-review cleanup | Once | Squashed |
| LLM-generated code | High → Low | Fine → Squashed |
</commit_frequency>

### Generate-Test-Commit-or-Revert

<generate_test_commit>
1. **CHECKPOINT** before LLM generates code
2. **TEST** — run tests, build, verify
3. **DECIDE** — pass → **commit immediately**; fail → restore checkpoint
4. **REVIEW** — PR before merge

**Key insight:** AI excels at generating plausible-looking but subtly incorrect code. Time saved by being careless will dwarf the mess you'll face later.

**If LLM fails 3+ times,** break it down further — abstraction level too high.
</generate_test_commit>

### Context Management

<context_management>
```bash
git diff --no-pager --no-color HEAD^  # Full diff for review
git diff -U0                          # No context (fewer tokens)
git diff --cached                     # Staged changes only
```
</context_management>

## Recovery Patterns

<recovery_triggers>
**Reflog** — Recover from rebases, resets, amends. Local only, 90 days default.
```bash
git reflog
git reset --hard HEAD@{5}
git reset --hard main@{2.hours.ago}
```

**Rerere** — Auto-resolve repeated conflicts. Enable: `git config --global rerere.enabled true`

**Bisect** — O(log n) regression hunting.
```bash
git bisect start && git bisect bad HEAD && git bisect good v1.0
git bisect run make test  # Automated
```
</recovery_triggers>

## Tool Selection

<stash_branch_worktree>
| Tool | Use When |
|------|----------|
| Stash | Very temporary, same day |
| Branch | >few hours, need sharing |
| Worktree | Parallel work, multi-agent |

**Multi-agent worktrees:**
```bash
git worktree add ../agent-1-workspace feature-auth
git worktree add ../agent-2-workspace feature-payment
```
</stash_branch_worktree>

## Anti-Patterns

<anti_patterns>
**Commit Anti-Patterns:**
- **Broken code on main**: Every commit on main should pass tests and build. Use feature branches or feature flags.
- **Giant mixed-concern commits**: Mixing refactoring with features makes review and revert impossible. Separate concerns.
- **Meaningless messages**: "fix", "update", "WIP" provide no context. Explain WHY, not just WHAT.
- **Committing secrets**: API keys, credentials, private keys. Use `.gitignore`, git-secrets, or pre-commit hooks.

**Branch Anti-Patterns:**
- **Long-lived branches (>1 week)**: Merge conflicts compound exponentially. Integrate frequently.
- **Rebasing public branches**: Rewrites shared history. Use merge for shared branches.
- **No feature flags on trunk**: Incomplete features on main without flags block releases.
- **Force pushing to main/master**: Destroys team history. Never do this.

**LLM-Assisted Anti-Patterns:**
- **"Vibe coding" without review**: LLM output requires human verification before commit.
- **No checkpoints before LLM changes**: Always checkpoint before LLM modifications for easy rollback.
- **Context drift from large windows**: Long conversations lose context. Break into smaller tasks.
</anti_patterns>

## Common Mistakes by Background

<common_mistakes>
### From SVN/Perforce Users
- Treating branches as expensive (they're cheap in Git—use them freely)
- Expecting central locking (Git is distributed—conflicts resolve at merge)
- Not pulling before push (always `git pull --rebase` before pushing)
- Expecting linear history without effort (requires disciplined rebasing)

### From Solo Developers
- Not considering rebase vs merge implications (matters when collaborating)
- Treating main as scratch space (use feature branches even when solo)
- Giant commits because "only I use this" (future you will regret it)
- No commit message discipline (you'll forget why in 6 months)

### From GUI-Only Users
- Not understanding what commands the GUI executes (learn the underlying operations)
- Panic when something goes wrong (reflog saves almost everything)
- Not leveraging command-line power for scripting and automation
</common_mistakes>

## Resources

<resources>
**Official:**
- [Git Documentation](https://git-scm.com/docs)
- [Pro Git Book](https://git-scm.com/book/en/v2)

**Patterns:**
- [Martin Fowler: Branching Patterns](https://martinfowler.com/articles/branching-patterns.html)
- [ConventionalCommits.org](https://www.conventionalcommits.org/en/v1.0.0/)
- [Nathan Orick: Git Checkpoints](https://nathanorick.com/git-checkpoints/)
</resources>

## Sources

<sources>
[^beams]: Chris Beams. 2014. How to Write a Git Commit Message. https://cbea.ms/git-commit/

[^orick]: Nathan Orick. Git Checkpoints. https://nathanorick.com/git-checkpoints/
</sources>
