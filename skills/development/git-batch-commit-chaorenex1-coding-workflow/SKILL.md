---
name: git-batch-commit
description: Intelligently detects when too many files are staged and automatically groups them by feature or functionality using Conventional Commits with user language preference
---

# Git Batch Commit Optimizer

This skill optimizes version control workflows by detecting when too many files are staged for commit and automatically organizing them into logical, feature-based batches with Conventional Commit messages.

## Capabilities

- **Smart Threshold Detection**: Automatically detects when staging area contains too many files (threshold-based analysis)
- **Intelligent File Grouping**: Groups files by feature/functionality, not just directory structure
- **Change Analysis**: Analyzes git diff to understand what each file modification does
- **Conventional Commits**: Generates commit messages following the standard (feat/fix/docs/refactor/chore/style/test/perf)
- **Language-Aware Messages**: Commit messages follow user's language preference (English/Chinese/etc.)
- **Multi-Batch Execution**: Executes multiple commits in logical sequence

## Input Requirements

Git repository state:
- Working directory with git repository
- Modified/staged/untrayed files ready for commit
- User language preference (defaults to English)
- Optional: Custom threshold for file count (default: 10 files)
- Optional: Specific Conventional Commit scope preferences

Formats accepted:
- Direct git status/diff output
- File paths with change descriptions
- Text description of changes made

## Output Formats

Results include:
- Analysis of file count and recommended batching strategy
- Grouped file sets by feature/functionality
- Conventional Commit messages for each batch (type/scope/description)
- Execution plan showing commit sequence
- Summary report of commits created

Output structure:
```json
{
  "analysis": {
    "total_files": 25,
    "threshold": 10,
    "requires_batching": true,
    "recommended_batches": 3
  },
  "batches": [
    {
      "batch_id": 1,
      "commit_type": "feat",
      "scope": "authentication",
      "files": ["auth.py", "login.py"],
      "message": "feat(authentication): add OAuth2 login support"
    }
  ],
  "execution_summary": "Created 3 commits across feat, fix, and docs types"
}
```

## How to Use

**Example 1 - Auto-detect and batch:**
"Analyze my git staging area and create appropriate batch commits"

**Example 2 - With language preference:**
"Create batch commits in Chinese for all these staged files"

**Example 3 - Custom threshold:**
"Use a threshold of 15 files and batch my commits accordingly"

**Example 4 - Specific commit types:**
"Group these changes and use 'feat' and 'refactor' commit types"

## Scripts

- `git_analyzer.py`: Parses git status/diff, detects file counts, analyzes change types
- `batch_committer.py`: Groups files by feature, generates Conventional Commit messages, executes commits
- `commit_language.py`: Handles multilingual commit message generation

## Conventional Commit Types

**Standard Types Used:**
- **feat**: New feature or functionality
- **fix**: Bug fix
- **docs**: Documentation changes only
- **refactor**: Code restructuring without feature changes
- **chore**: Maintenance tasks (dependencies, configs)
- **style**: Code style/formatting (no logic change)
- **test**: Adding or updating tests
- **perf**: Performance improvements

**Scope Examples**: `(api)`, `(ui)`, `(auth)`, `(database)`, `(core)`

## Best Practices

1. **Review before execution**: Always review the proposed batches before committing
2. **Meaningful scopes**: Use clear, project-specific scopes for better commit history
3. **Atomic commits**: Each batch should represent a cohesive unit of change
4. **Language consistency**: Keep commit language consistent within a project
5. **Threshold tuning**: Adjust threshold based on project size and team preferences
6. **Feature grouping**: Prefer functional grouping over directory-based grouping

## Limitations

- Requires git repository in working directory
- Cannot automatically resolve conflicts between batches
- Scope detection depends on file naming conventions and change analysis
- Language detection may require explicit user preference
- Some complex refactorings may need manual grouping
- Does not handle pre-commit hooks automatically (user must ensure hooks pass)

## Configuration Options

Optional configuration via `git_batch_config.json`:
```json
{
  "threshold": 10,
  "default_language": "en",
  "preferred_scopes": ["api", "ui", "core", "tests"],
  "commit_types": ["feat", "fix", "docs", "refactor", "chore"],
  "auto_execute": false
}
```

## Safety Features

- **Dry-run mode**: Preview batches before committing
- **Rollback support**: Can amend or reset if issues detected
- **Validation**: Checks for unstaged critical files
- **Conflict detection**: Warns about potential file dependencies across batches
