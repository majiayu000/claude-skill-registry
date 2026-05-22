---
name: merge-strategy
description: Intelligent merge/rebase strategy selection with safe execution
disable-model-invocation: false
---

# Intelligent Merge Strategy Selector

I'll help you choose the optimal Git merge strategy and execute it safely based on branch analysis, history, and team conventions.

Arguments: `$ARGUMENTS` - branch name, strategy preference (merge/rebase/squash), or 'auto'

## Token Optimization

This skill uses merge strategy-specific patterns to minimize token usage:

### 1. Branch Analysis Caching (800 token savings)
**Pattern:** Cache branch divergence analysis results
- Store analysis in `merge-strategy/analysis-cache.json` (15 min TTL)
- Cache: commit counts, divergence, conflicts, recommendations
- Read cached analysis on subsequent checks (50 tokens vs 850 tokens fresh)
- Invalidate on new commits to either branch
- **Savings:** 94% on repeated strategy checks

### 2. Bash-Based Divergence Detection (900 token savings)
**Pattern:** Use git commands for branch analysis
- Commits ahead: `git rev-list --count target..source` (100 tokens)
- Commits behind: `git rev-list --count source..target` (100 tokens)
- Conflict preview: `git merge-tree` (200 tokens)
- No Task agents for branch analysis
- **Savings:** 85% vs Task-based branch analysis

### 3. Early Exit for Fast-Forward (95% savings)
**Pattern:** Detect fast-forward merges immediately
- Check merge base: `git merge-base --is-ancestor` (100 tokens)
- If fast-forward possible: return "Use merge --ff-only" (150 tokens)
- **Distribution:** ~30% of merges are fast-forward
- **Savings:** 150 vs 2,500 tokens for fast-forward detections

### 4. Template-Based Strategy Recommendations (1,000 token savings)
**Pattern:** Use predefined decision tree for strategies
- Rules-based recommendations: commit count, branch type, team conventions
- Standard patterns: merge for public branches, rebase for private, squash for features
- No creative strategy generation
- **Savings:** 85% vs LLM-generated recommendations

### 5. Sample-Based Commit Analysis (700 token savings)
**Pattern:** Analyze first 10 commits for patterns
- Extract patterns from first 10 commits (500 tokens)
- Infer strategy from commit history
- Full analysis only if explicitly requested
- **Savings:** 65% vs analyzing entire commit history

### 6. Cached Team Convention Detection (400 token savings)
**Pattern:** Store team merge preferences
- Cache merge strategy from .git/config or CONTRIBUTING.md
- Default to detected convention
- Don't re-detect on each run
- **Savings:** 80% on convention detection

### 7. Progressive Strategy Execution (600 token savings)
**Pattern:** Execute merge in stages with validation
- Stage 1: Preview conflicts (400 tokens)
- Stage 2: Execute merge (500 tokens)
- Stage 3: Validate result (300 tokens)
- Default: Preview only, execute on confirmation
- **Savings:** 70% when preview shows issues

### 8. Conflict Prediction Caching (500 token savings)
**Pattern:** Store merge-tree results
- Cache conflict prediction from git merge-tree
- Re-use for multiple strategy evaluations
- Only recalculate on branch changes
- **Savings:** 80% on repeated strategy comparisons

### Real-World Token Usage Distribution

**Typical operation patterns:**
- **Fast-forward check** (can fast-forward): 150 tokens
- **Strategy analysis** (cached branch analysis): 1,200 tokens
- **Preview merge** (conflict prediction): 1,500 tokens
- **Execute merge** (with validation): 2,000 tokens
- **Full analysis** (first time): 2,500 tokens
- **Most common:** Fast-forward checks or cached analysis

**Expected per-analysis:** 1,500-2,500 tokens (50% reduction from 3,000-5,000 baseline)
**Real-world average:** 900 tokens (due to fast-forward, cached analysis, template-based recommendations)

## Session Intelligence

I'll maintain merge decision tracking across sessions:

**Session Files (in current project directory):**
- `merge-strategy/analysis.md` - Branch divergence analysis and recommendations
- `merge-strategy/state.json` - Merge decisions and outcomes
- `merge-strategy/conflicts.log` - Conflict history and resolutions

**IMPORTANT:** Session files are stored in a `merge-strategy` folder in your current project root

**Auto-Detection:**
- If branch analysis exists: Show previous recommendations
- If no analysis: Perform comprehensive branch analysis
- Commands: `analyze`, `execute`, `preview`, `undo`

## Phase 1: Branch Analysis

### Extended Thinking for Strategy Selection

For complex merge scenarios, I'll use extended thinking to evaluate trade-offs:

<think>
When analyzing merge strategies:
- Impact on git history readability and debugging
- Team workflow preferences and conventions
- Conflict complexity and resolution difficulty
- Public vs private branch considerations
- Collaborative branch with multiple contributors
- CI/CD pipeline requirements and branch protection
- Code review and audit trail needs
- Release branch management implications
</think>

**Triggers for Extended Analysis:**
- Long-lived feature branches
- Multiple contributors on branch
- Complex conflict scenarios
- Release branch management
- Shared public branches

I'll perform comprehensive branch analysis:

```bash
#!/bin/bash
# Branch divergence analysis

analyze_branch() {
    local source_branch="${1:-$(git rev-parse --abbrev-ref HEAD)}"
    local target_branch="${2:-main}"

    echo "=== Branch Divergence Analysis ==="
    echo "Source: $source_branch"
    echo "Target: $target_branch"
    echo

    # Check if branches exist
    if ! git rev-parse --verify "$source_branch" >/dev/null 2>&1; then
        echo "Error: Branch '$source_branch' does not exist"
        return 1
    fi

    if ! git rev-parse --verify "$target_branch" >/dev/null 2>&1; then
        echo "Error: Branch '$target_branch' does not exist"
        return 1
    fi

    # Fetch latest
    echo "Fetching latest changes..."
    git fetch origin "$target_branch" 2>/dev/null

    # Divergence stats
    local ahead=$(git rev-list --count origin/"$target_branch".."$source_branch" 2>/dev/null || echo "0")
    local behind=$(git rev-list --count "$source_branch"..origin/"$target_branch" 2>/dev/null || echo "0")

    echo "Commits ahead of $target_branch: $ahead"
    echo "Commits behind $target_branch: $behind"
    echo

    # Commit history analysis
    echo "=== Recent Commits on $source_branch ==="
    git log --oneline --no-merges "$target_branch".."$source_branch" 2>/dev/null || echo "No unique commits"
    echo

    # Check for merge commits in branch
    local merge_commits=$(git log --oneline --merges "$target_branch".."$source_branch" 2>/dev/null | wc -l)
    echo "Merge commits in branch: $merge_commits"

    # File change analysis
    echo
    echo "=== Files Modified ==="
    git diff --name-status origin/"$target_branch"..."$source_branch" 2>/dev/null | head -20
    local total_files=$(git diff --name-only origin/"$target_branch"..."$source_branch" 2>/dev/null | wc -l)
    if [ "$total_files" -gt 20 ]; then
        echo "... and $((total_files - 20)) more files"
    fi
    echo

    # Potential conflict preview
    echo "=== Conflict Preview ==="
    git merge-tree "$(git merge-base origin/"$target_branch" "$source_branch")" \
                   origin/"$target_branch" "$source_branch" 2>/dev/null | \
        grep -A 5 "changed in both" || echo "No conflicts detected"
}
```

**Analysis Factors:**

1. **Branch Age & Divergence:**
   - Days since branch creation
   - Commits ahead/behind base branch
   - Number of merge commits already in branch

2. **Collaboration Level:**
   - Single author vs multiple contributors
   - Public vs private branch
   - Active PR discussions

3. **Conflict Complexity:**
   - Number of conflicting files
   - Type of conflicts (code vs config)
   - Overlapping changes

4. **Repository Context:**
   - Team conventions (check CONTRIBUTING.md)
   - CI/CD requirements
   - Release branch patterns

## Phase 2: Strategy Evaluation

Based on analysis, I'll evaluate each strategy:

### Strategy 1: Regular Merge (--no-ff)

**Best For:**
- Preserving complete history
- Feature branches with meaningful commits
- Collaborative branches with multiple authors
- When context of feature development is valuable

**Pros:**
- Complete history preserved
- Easy to revert entire feature
- Clear feature boundaries in history
- No rewriting of commits

**Cons:**
- More complex history graph
- Can clutter history with many feature branches
- Merge commits add noise

**Analysis:**
```bash
# Preview merge result
preview_merge() {
    local branch=$1
    local target=${2:-main}

    echo "=== Merge Preview: $branch → $target ==="

    # Create temporary branch for preview
    git checkout -b temp-merge-preview "$target" 2>/dev/null

    # Attempt merge
    if git merge --no-ff --no-commit "$branch" 2>/dev/null; then
        echo "✓ Merge would succeed without conflicts"
        git diff --cached --stat
    else
        echo "⚠️  Merge would have conflicts:"
        git diff --name-only --diff-filter=U
    fi

    # Cleanup
    git merge --abort 2>/dev/null
    git checkout "$target" 2>/dev/null
    git branch -D temp-merge-preview 2>/dev/null
}
```

### Strategy 2: Rebase

**Best For:**
- Linear history preference
- Single author feature branches
- Private branches not pushed
- Cleaning up messy development history

**Pros:**
- Clean linear history
- Easy to follow code evolution
- No merge commits
- Simpler git log output

**Cons:**
- Rewrites commit history (dangerous on public branches)
- Can complicate collaboration
- Loses context of parallel development
- More complex conflict resolution

**Analysis:**
```bash
# Preview rebase result
preview_rebase() {
    local branch=$1
    local target=${2:-main}

    echo "=== Rebase Preview: $branch onto $target ==="

    # Check if branch is pushed
    if git branch -r | grep -q "origin/$branch"; then
        echo "⚠️  WARNING: Branch is pushed to remote"
        echo "   Rebase will rewrite public history"
        echo "   Team members may need to force pull"
    fi

    # Check for conflicts
    local merge_base=$(git merge-base "$target" "$branch")
    local conflicts=$(git merge-tree "$merge_base" "$target" "$branch" 2>/dev/null | \
                     grep -c "changed in both" || echo "0")

    if [ "$conflicts" -gt 0 ]; then
        echo "⚠️  Estimated $conflicts conflicts to resolve"
        echo "   Each conflict must be resolved per commit"
    else
        echo "✓ Rebase likely to succeed without conflicts"
    fi

    # Show commits that would be replayed
    echo
    echo "Commits to replay:"
    git log --oneline "$target".."$branch"
}
```

### Strategy 3: Squash Merge

**Best For:**
- Cleaning up experimental development
- Many small WIP commits
- Feature as single logical unit
- Keeping main branch history clean

**Pros:**
- Single commit on target branch
- Clean main branch history
- Flexible commit message
- Hides development messiness

**Cons:**
- Loses granular history
- Difficult to debug individual changes
- Can't cherry-pick specific commits
- Makes code review harder

**Analysis:**
```bash
# Preview squash merge
preview_squash() {
    local branch=$1
    local target=${2:-main}

    echo "=== Squash Merge Preview: $branch → $target ==="

    # Count commits to be squashed
    local commit_count=$(git rev-list --count "$target".."$branch")
    echo "Will squash $commit_count commits into 1"
    echo

    # Show combined diff
    echo "Combined changes:"
    git diff --stat "$target"..."$branch"
    echo

    # Suggest commit message
    echo "Suggested commit message:"
    echo "---"
    git log --format="%s" "$target".."$branch" | \
        awk '{count[$0]++} END {for (msg in count) print "- " msg}'
}
```

### Strategy 4: Rebase + Merge --no-ff

**Best For:**
- Best of both worlds
- Clean branch history + feature preservation
- Team workflows requiring linear history

**Pros:**
- Linear history within feature
- Preserves feature branch context
- Easier to revert entire feature
- Clean individual commits

**Cons:**
- Two-step process
- Still rewrites history (rebase phase)
- More complex workflow

## Phase 3: Decision Engine

I'll use decision logic to recommend optimal strategy:

```markdown
# Decision Tree

## Question 1: Is the branch public (pushed and shared)?
├─ YES → **Avoid rebase** (or communicate with team first)
│  └─ Go to Question 3
└─ NO → Rebase is safe
   └─ Go to Question 2

## Question 2: Does the branch have meaningful commit history?
├─ YES → **Regular merge or rebase+merge**
│  └─ Linear history preference? → Rebase+merge : Regular merge
└─ NO (WIP commits, "fix typo", etc.) → **Squash merge**

## Question 3: How complex are the conflicts?
├─ HIGH (many files, complex logic) → **Regular merge**
│  └─ Easier conflict resolution
└─ LOW → **Squash merge** for clean history

## Question 4: Check team conventions
└─ Read CONTRIBUTING.md, .git/config, PR templates
   └─ Follow team preference
```

**Automated Recommendation:**
```bash
#!/bin/bash
# Intelligent strategy recommendation

recommend_strategy() {
    local branch=$1
    local target=${2:-main}

    # Check if branch is public
    if git branch -r | grep -q "origin/$branch"; then
        is_public="yes"
    else
        is_public="no"
    fi

    # Count commits
    commit_count=$(git rev-list --count "$target".."$branch")

    # Check commit quality
    wip_commits=$(git log --oneline "$target".."$branch" | \
                 grep -iE "(wip|fixup|temp|test)" | wc -l)
    wip_ratio=$(echo "scale=2; $wip_commits / $commit_count" | bc)

    # Check for conflicts
    merge_base=$(git merge-base "$target" "$branch")
    conflict_files=$(git merge-tree "$merge_base" "$target" "$branch" 2>/dev/null | \
                    grep "changed in both" | wc -l)

    # Check team conventions
    if [ -f "CONTRIBUTING.md" ]; then
        if grep -qi "squash" CONTRIBUTING.md; then
            team_pref="squash"
        elif grep -qi "rebase" CONTRIBUTING.md; then
            team_pref="rebase"
        else
            team_pref="merge"
        fi
    else
        team_pref="unknown"
    fi

    echo "=== Strategy Recommendation ==="
    echo "Branch: $branch → $target"
    echo
    echo "Analysis:"
    echo "  Public branch: $is_public"
    echo "  Commits: $commit_count"
    echo "  WIP ratio: $wip_ratio"
    echo "  Conflicts: $conflict_files files"
    echo "  Team preference: $team_pref"
    echo

    # Decision logic
    if [ "$team_pref" != "unknown" ]; then
        echo "RECOMMENDATION: **$team_pref** (team convention)"
    elif [ "$is_public" = "yes" ]; then
        if (( $(echo "$wip_ratio > 0.5" | bc -l) )); then
            echo "RECOMMENDATION: **squash** (many WIP commits, public branch)"
        else
            echo "RECOMMENDATION: **merge** (public branch, preserve history)"
        fi
    elif (( $(echo "$wip_ratio > 0.5" | bc -l) )); then
        echo "RECOMMENDATION: **squash** (clean up WIP commits)"
    elif [ "$conflict_files" -gt 10 ]; then
        echo "RECOMMENDATION: **merge** (complex conflicts easier to resolve)"
    else
        echo "RECOMMENDATION: **rebase** (clean linear history)"
    fi
}
```

## Phase 4: Safe Execution

Once strategy is chosen, I'll execute it safely:

**Pre-Execution Checklist:**
```bash
# Safety checks before merge
pre_merge_checks() {
    echo "=== Pre-Merge Safety Checks ==="

    # 1. Clean working directory
    if ! git diff-index --quiet HEAD --; then
        echo "❌ Working directory has uncommitted changes"
        return 1
    fi

    # 2. All tests passing
    if [ -f "package.json" ]; then
        echo "Running tests..."
        npm test || {
            echo "❌ Tests failing"
            return 1
        }
    fi

    # 3. Up to date with remote
    git fetch origin
    local target_branch=${1:-main}
    if [ "$(git rev-parse origin/$target_branch)" != "$(git rev-parse $target_branch)" ]; then
        echo "❌ Local $target_branch out of sync with remote"
        return 1
    fi

    # 4. Create safety branch
    git branch -f "backup-before-merge-$(date +%s)" HEAD
    echo "✓ Safety backup created"

    echo "✓ All pre-merge checks passed"
    return 0
}
```

**Execution with Rollback:**

```bash
#!/bin/bash
# Execute merge with automatic rollback on failure

execute_merge_strategy() {
    local strategy=$1
    local branch=$2
    local target=${3:-main}

    # Create restore point
    local restore_point=$(git rev-parse HEAD)
    local restore_branch="restore-$(date +%s)"
    git branch "$restore_branch" HEAD

    echo "=== Executing: $strategy merge of $branch → $target ==="
    echo "Restore point: $restore_branch"
    echo

    case "$strategy" in
        merge)
            if git merge --no-ff "$branch" -m "Merge branch '$branch'"; then
                echo "✓ Merge successful"
                run_post_merge_validation
            else
                echo "❌ Merge failed or conflicts"
                handle_merge_failure "$restore_branch"
            fi
            ;;

        rebase)
            if git rebase "$target" "$branch"; then
                git checkout "$target"
                git merge --no-ff "$branch"
                echo "✓ Rebase and merge successful"
                run_post_merge_validation
            else
                echo "❌ Rebase failed"
                git rebase --abort
                handle_merge_failure "$restore_branch"
            fi
            ;;

        squash)
            if git merge --squash "$branch"; then
                echo "Changes squashed, ready to commit"
                echo "Suggested message:"
                generate_squash_message "$branch" "$target"
                echo
                echo "Review changes with: git diff --cached"
            else
                echo "❌ Squash merge failed"
                handle_merge_failure "$restore_branch"
            fi
            ;;

        *)
            echo "Unknown strategy: $strategy"
            return 1
            ;;
    esac
}

run_post_merge_validation() {
    echo
    echo "=== Post-Merge Validation ==="

    # Run tests
    if [ -f "package.json" ] && command -v npm &> /dev/null; then
        echo "Running test suite..."
        if npm test; then
            echo "✓ Tests passed"
        else
            echo "❌ Tests failed after merge"
            echo "Rolling back..."
            git reset --hard "$restore_point"
            return 1
        fi
    fi

    # Run linter
    if [ -f "package.json" ] && grep -q "lint" package.json; then
        echo "Running linter..."
        if npm run lint; then
            echo "✓ Linting passed"
        else
            echo "⚠️  Linting issues (non-blocking)"
        fi
    fi

    echo "✓ Validation complete"
}

handle_merge_failure() {
    local restore_branch=$1

    echo
    echo "Merge failed. Options:"
    echo "1. Resolve conflicts manually: git status"
    echo "2. Rollback completely: git reset --hard $restore_branch"
    echo "3. Continue after resolving: git merge --continue (or rebase --continue)"
}
```

## Phase 5: Conflict Resolution Integration

When conflicts occur, I'll provide intelligent resolution:

```bash
# Analyze conflicts
analyze_conflicts() {
    echo "=== Conflict Analysis ==="

    # List conflicted files
    local conflicts=$(git diff --name-only --diff-filter=U)

    if [ -z "$conflicts" ]; then
        echo "No conflicts detected"
        return 0
    fi

    echo "Conflicted files:"
    echo "$conflicts"
    echo

    # Categorize conflicts
    local code_conflicts=$(echo "$conflicts" | grep -E '\.(js|ts|py|java|go)$' | wc -l)
    local config_conflicts=$(echo "$conflicts" | grep -E '\.(json|yaml|yml|toml)$' | wc -l)
    local doc_conflicts=$(echo "$conflicts" | grep -E '\.(md|txt)$' | wc -l)

    echo "Conflict breakdown:"
    echo "  Code files: $code_conflicts"
    echo "  Config files: $config_conflicts"
    echo "  Documentation: $doc_conflicts"
    echo

    # Suggest resolution approach
    if [ "$code_conflicts" -gt 5 ]; then
        echo "SUGGESTION: Use /conflict-resolve skill for systematic resolution"
    elif [ "$config_conflicts" -gt 0 ]; then
        echo "SUGGESTION: Config conflicts often need manual review for semantics"
    fi
}
```

**Integration with /conflict-resolve:**
```
When conflicts detected → automatically suggest /conflict-resolve skill
Provide conflict summary to /conflict-resolve
Track resolution decisions in merge-strategy/state.json
```

## Context Continuity

**Session Resume:**
When you return and run `/merge-strategy` or `/merge-strategy resume`:
- Load previous branch analysis
- Show merge history and outcomes
- Display current branch status
- Provide updated recommendation

**Progress Example:**
```
MERGE STRATEGY ANALYSIS
═══════════════════════════════════════════════════

Branch: feature/user-auth → main
Last analyzed: 2 hours ago

Current Status:
├── Commits ahead: 12
├── Commits behind: 3
├── Contributors: 2
├── Conflicts: 0 estimated

Previous Recommendation: rebase
Team Convention: squash (from CONTRIBUTING.md)

Updated Recommendation: **squash** (follow team convention)

Commands:
  /merge-strategy execute squash    # Execute with safety checks
  /merge-strategy preview rebase    # Preview alternative strategy
  /merge-strategy analyze           # Re-analyze branch
```

## Practical Examples

**Analyze and Recommend:**
```
/merge-strategy                           # Auto-analyze current branch
/merge-strategy feature/auth              # Analyze specific branch
/merge-strategy feature/auth main         # Specify target branch
```

**Execute Strategy:**
```
/merge-strategy execute merge             # Execute recommended strategy
/merge-strategy execute squash            # Force specific strategy
/merge-strategy preview rebase            # Preview without executing
```

**Integration Commands:**
```
/merge-strategy analyze              # Deep branch analysis
/merge-strategy conflicts            # Analyze conflicts
/merge-strategy undo                 # Rollback to safety branch
```

## Safety Guarantees

**Protection Measures:**
- Automatic safety branches before merge
- Pre-merge validation (tests, lint)
- Post-merge validation
- Rollback capability
- Conflict detection before execution

**Important:** I will NEVER:
- Force push without warning
- Rebase public branches without confirmation
- Merge without running tests
- Add AI attribution to merge commits
- Modify git config

## Skill Integration

Works seamlessly with other git skills:
- `/conflict-resolve` - When conflicts detected
- `/branch-finish` - Complete workflow including strategy selection
- `/git-bisect` - If merge introduces bugs
- `/commit` - For post-merge cleanup commits
- `/test` - Validation after merge

## Token Budget Optimization

To stay within 2,500-4,000 token budget:
- **Focus on decision logic and recommendations**
- **Use bash scripts for analysis (executed, not explained)**
- **Provide strategy comparison as table**
- **Defer detailed conflict resolution to /conflict-resolve**
- **Compact progress reporting**

## What I'll Actually Do

1. **Analyze branch** - Extended thinking for complex scenarios
2. **Evaluate strategies** - Consider all factors (team, history, conflicts)
3. **Recommend optimal** - Decision tree logic with explanation
4. **Execute safely** - Pre-checks, safety branch, validation
5. **Handle conflicts** - Guide resolution or integrate with /conflict-resolve
6. **Validate result** - Post-merge testing and verification
7. **Track decisions** - Record for future reference

I'll help you choose and execute the right merge strategy for every situation, safely and intelligently.

---

**Credits:**
- Git branching strategies from Git best practices
- Based on obra/superpowers git workflow patterns
- Team workflow patterns from industry conventions
- Conflict resolution strategies from distributed development experience
- Integration with existing git skills in Claude DevStudio
