---
name: git-staging
description: Stage files, hunks, or specific lines in git non-interactively.
---

# Non-interactive Git Staging

## When to use this skill

Use this skill when you need to:

- Stage only specific hunks from a file (not the entire file)
- Stage only specific lines within a hunk
- Avoid interactive git commands (`git add -p`, `git add -i`, etc.)
- Programmatically control exactly what gets staged

## Step 1: Assess the changes

Before choosing a staging method, determine what changes exist:

```bash
git status                    # See which files have changes
git diff --no-ext-diff        # See all unstaged changes
git diff --cached --no-ext-diff  # See already-staged changes
```

**Decision tree:**

- If only ONE file has changes and you want ALL of them staged → use `git add <file>`
- If ONE file has multiple unrelated hunks and you want only SOME → use Method 2 or 3
- If MULTIPLE files need staging → stage per-file with `git add` for each, or selectively with patch method

## Why not use `git add -p`?

Interactive git commands require a TTY and human input. AI agents cannot
reliably fake interactive sessions - attempts using `echo "y"` or `yes` are
fragile and often fail. Instead, construct patches programmatically and apply
them directly to the index.

## Core technique

The key insight is that `git apply --cached` applies a patch directly to the
staging area (index) without modifying the working tree. This lets you stage
precise changes non-interactively.

## Temporary files

All temporary patch files should be written to `tmp/` within the repository
(not `/tmp`) to avoid permission prompts. Ensure the directory exists first:

```bash
mkdir -p tmp
```

## Methods

### Method 1: Stage entire file

When you want to stage all changes in a file:

```bash
git add <file>
```

### Method 2: Stage specific hunks via patch

When you need to stage only certain hunks from a file:

1. Generate the full diff for the file:
   ```bash
   git diff <file> > tmp/full.patch
   ```

2. Edit the patch to keep only the hunks you want to stage (use the Edit tool
   or create a new file with only the desired hunks)

3. Apply the edited patch to the index:
   ```bash
   git apply --cached tmp/selected.patch
   ```

### Method 3: Stage specific lines within a hunk

When you need to stage only certain lines within a hunk, you must carefully
edit the patch to maintain validity:

1. Generate the diff:
   ```bash
   git diff <file> > tmp/full.patch
   ```

2. Edit the patch, following these rules for the hunk you're modifying:
   - Keep the `@@` hunk header but adjust the line counts
   - To **exclude an added line** (`+`): remove the entire line from the patch
   - To **exclude a removed line** (`-`): change `-` to a space (` `) to make
     it context
   - Adjust the line counts in the `@@ -X,Y +X,Z @@` header to match

3. Apply:
   ```bash
   git apply --cached tmp/selected.patch
   ```

## Patch format reference

A unified diff patch has this structure:

```diff
diff --git a/file.txt b/file.txt
index abc123..def456 100644
--- a/file.txt
+++ b/file.txt
@@ -10,6 +10,8 @@ optional context label
 context line (unchanged)
-removed line
+added line
 context line (unchanged)
```

### Hunk header format

`@@ -START,COUNT +START,COUNT @@`

- First pair: original file (lines being removed or used as context)
- Second pair: new file (lines being added or used as context)
- COUNT = number of lines in that side of the hunk (context + changes)

### Line prefixes

- ` ` (space): context line (unchanged, appears in both versions)
- `-`: line only in original (will be removed)
- `+`: line only in new version (will be added)

## Example: Staging only the second hunk

Given a file with two hunks of changes:

```bash
# Generate full diff
git diff --no-ext-diff myfile.py > tmp/full.patch
```

The patch might look like:

```diff
diff --git a/myfile.py b/myfile.py
index abc123..def456 100644
--- a/myfile.py
+++ b/myfile.py
@@ -5,6 +5,7 @@ import os
 def foo():
     pass
+    # Added comment in first hunk

 def bar():
@@ -20,6 +21,7 @@ def bar():
 def baz():
     pass
+    # Added comment in second hunk
```

To stage only the second hunk, create a new patch with just that hunk:

```diff
diff --git a/myfile.py b/myfile.py
index abc123..def456 100644
--- a/myfile.py
+++ b/myfile.py
@@ -20,6 +21,7 @@ def bar():
 def baz():
     pass
+    # Added comment in second hunk
```

Then apply:

```bash
git apply --cached tmp/second-hunk.patch
```

## Example: Excluding specific added lines

If you have a hunk with multiple additions but only want to stage some:

Original hunk:
```diff
@@ -10,4 +10,7 @@
 existing line
+line I want to stage
+line I do NOT want to stage
+another line I want to stage
 more context
```

Edit to exclude the unwanted line (remove it entirely and adjust count):
```diff
@@ -10,4 +10,6 @@
 existing line
+line I want to stage
+another line I want to stage
 more context
```

Note: The `+10,7` became `+10,6` because we removed one added line.

## Verification

After applying, verify what was staged:

```bash
git diff --cached          # Show staged changes
git diff                   # Show unstaged changes (should include excluded hunks)
git status                 # Overview of staged/unstaged state
```

## Common pitfalls

1. **Invalid line counts**: If the `@@` header counts don't match the actual
   lines in the hunk, `git apply` will fail. Always recount after editing.

2. **Missing newline at EOF**: Patches are sensitive to trailing newlines.
   Watch for `\ No newline at end of file` markers.

3. **Whitespace corruption**: Ensure context lines start with a space, not
   an empty prefix. Some editors strip trailing spaces.

4. **Index mismatch**: The `index abc123..def456` line is optional for
   `git apply --cached`. If you have issues, try removing it.

## Troubleshooting

If `git apply --cached` fails:

1. Test the patch first without `--cached`:
   ```bash
   git apply --check tmp/selected.patch
   ```

2. Use verbose mode to see what's happening:
   ```bash
   git apply --cached -v tmp/selected.patch
   ```

3. Common error messages:
   - "patch does not apply": Line counts are wrong or context doesn't match
   - "patch fragment without header": Missing the `diff --git` or `---/+++` lines
