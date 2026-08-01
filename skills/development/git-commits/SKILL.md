---
name: git-commits
description: 'Create well-structured git commits. ALWAYS use this skill when committing
  - even for simple single-file commits. Triggers: "commit", "stage", "add and commit",
  or after completing any code changes.'
---

---
name: git-commits
description: Create well-structured git commits. ALWAYS use this skill when committing - even for simple single-file commits. Triggers: "commit", "stage", "add and commit", or after completing any code changes.
---

# Git Commits

**Always invoke this skill for every commit.** This ensures consistent, well-structured commits.

## Workflow

1. Run `git status` and `git diff` to see changes
2. Run `git log --oneline -5` to see recent commit style
3. Determine if changes should be one or multiple commits
4. Stage and commit with clear message

## When to Split vs Combine

**Separate commits:**
- CSS vs PHP logic
- Different features (even in same file)
- Refactoring vs new functionality
- Multiple bug fixes (one per fix)

**Single commit:**
- Related changes for one feature
- A handler + its CSS
- Tests for the feature being added

## Commit Message Format

```
<summary line - what and why, not how>

<optional body with more context>
```

## Examples

**Input:** Single file change to update details
```diff
-  $title = __( 'Old title', 'simple-history' );
+  $title = __( 'New title', 'simple-history' );
```
**Output:**
```
Update 5.22.0 update details title
```

**Input:** Multiple related changes across files
```diff
# file1.php
+ public function new_feature() { ... }

# file2.php
+ add_filter( 'hook', [ $this, 'new_feature' ] );
```
**Output:**
```
Add new feature for X

Register hook and implement handler.
```

## Multiple Repositories

When changes span core + premium:
1. Commit core first, then premium
2. Use related commit messages
