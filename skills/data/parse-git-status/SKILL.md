---
name: parse-git-status
description: Parse git status output into structured data showing staged, modified, and untracked files. Use for pre-flight validation, checking clean working directory, or listing changed files before commits.
---

# Parse Git Status

Parse git status command output into structured JSON for programmatic analysis.

## When to Use

- Pre-flight checks before workflow execution
- Validate clean working directory
- List modified files for commit
- Check for uncommitted changes

## Instructions

### Step 1: Receive Git Status Output

Accept raw git status output as input.

**Expected Input**:

- `gitStatusOutput`: String (raw output from `git status --porcelain` or regular `git status`)

### Step 2: Parse Branch Information

Extract current branch and tracking information.

**Patterns**:

- `## branch-name`: Current branch
- `## branch-name...origin/branch-name`: Tracking branch
- `[ahead N]` or `[behind N]`: Ahead/behind commits

### Step 3: Categorize Files

Parse file status indicators and categorize.

**Status Indicators** (porcelain format):

- `M `: Modified (staged)
- ` M`: Modified (unstaged)
- `A `: Added (staged)
- `D `: Deleted (staged)
- `R `: Renamed (staged)
- `??`: Untracked
- `!!`: Ignored

### Step 4: Return Structured Data

Return parsed data as JSON object.

**Expected Output**:

```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 0,
  "behind": 0,
  "staged": ["file1.ts", "file2.ts"],
  "modified": ["file3.ts"],
  "deleted": [],
  "renamed": [],
  "untracked": ["file4.ts"],
  "clean": false
}
```

## Error Handling

- **Invalid Git Output**: Return error describing format issue
- **Not a Git Repository**: Return error indicating no git repo
- **Empty Output**: Return clean status with empty arrays

## Examples

### Example 1: Clean Working Directory

**Input**:

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

**Output**:

```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 0,
  "behind": 0,
  "staged": [],
  "modified": [],
  "deleted": [],
  "renamed": [],
  "untracked": [],
  "clean": true
}
```

### Example 2: Modified Files

**Input** (porcelain format):

```
## main...origin/main [ahead 2]
M  src/utils.ts
 M src/types.ts
A  src/new-feature.ts
?? temp-file.js
```

**Output**:

```json
{
  "branch": "main",
  "tracking": "origin/main",
  "ahead": 2,
  "behind": 0,
  "staged": ["src/utils.ts", "src/new-feature.ts"],
  "modified": ["src/types.ts"],
  "deleted": [],
  "renamed": [],
  "untracked": ["temp-file.js"],
  "clean": false
}
```

### Example 3: Detached HEAD

**Input**:

```
## HEAD (no branch)
 M README.md
```

**Output**:

```json
{
  "branch": "HEAD (detached)",
  "tracking": null,
  "ahead": 0,
  "behind": 0,
  "staged": [],
  "modified": ["README.md"],
  "deleted": [],
  "renamed": [],
  "untracked": [],
  "clean": false
}
```

## Validation

- [ ] Parses branch information correctly
- [ ] Categorizes files by status
- [ ] Handles empty/clean status
- [ ] Parses ahead/behind indicators
- [ ] Handles detached HEAD state
- [ ] Returns clean:true only when appropriate

## Supporting Files

None required - pure parsing logic.
