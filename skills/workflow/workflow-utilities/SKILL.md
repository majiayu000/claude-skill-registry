---
name: workflow-utilities
version: 5.2.0
description: |
  Shared utilities for file deprecation, directory structure creation,
  TODO file updates, workflow lifecycle management, archive management,
  and VCS abstraction (GitHub/Azure DevOps PR feedback methods).
  Used by all other skills.

  Use when: Need shared utilities, deprecating files, updating TODO,
  registering/archiving workflows, managing TODO.md manifest, VCS operations,
  PR feedback handling

  Triggers: deprecate, archive, update TODO, create directory, register workflow,
  archive workflow, sync manifest, VCS operations, PR feedback
---

# Workflow Utilities

## Purpose

Provides reusable Python utilities for common workflow tasks that are used
across multiple skills.

## Scripts

### deprecate_files.py

Archive deprecated files with timestamp into ARCHIVED/ directory.

```bash
python .claude/skills/workflow-utilities/scripts/deprecate_files.py \
  <todo_file> <description> <file1> [file2 ...]
```

**Arguments:**
- `todo_file`: Path to TODO file (for timestamp extraction)
- `description`: Short description (e.g., 'old-auth-flow')
- `files`: One or more file paths to deprecate

**Creates:**
- `ARCHIVED/YYYYMMDDTHHMMSSZ_<description>.zip`

### directory_structure.py

Create standard directory structure with required files.

```bash
python .claude/skills/workflow-utilities/scripts/directory_structure.py \
  <directory>
```

**Arguments:**
- `directory`: Path to directory to create/populate

**Creates:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (with its own CLAUDE.md and README.md)

### todo_updater.py

Update task status and workflow progress in TODO file.

```bash
python .claude/skills/workflow-utilities/scripts/todo_updater.py \
  <todo_file> <task_id> <status> [context_usage]
```

**Arguments:**
- `todo_file`: Path to TODO file
- `task_id`: Task ID (e.g., 'impl_003')
- `status`: New status ('pending' | 'complete' | 'blocked')
- `context_usage` (optional): Context usage percentage

**Updates:**
- Task status in YAML frontmatter
- `completed_at` timestamp
- `workflow_progress.last_task`
- `workflow_progress.last_update`

### archive_manager.py

List and extract archived files.

```bash
# List archives
python .claude/skills/workflow-utilities/scripts/archive_manager.py list [directory]

# Extract archive
python .claude/skills/workflow-utilities/scripts/archive_manager.py extract <archive> [output_dir]
```

### workflow_registrar.py

Register new workflow in TODO.md master manifest.

```bash
python .claude/skills/workflow-utilities/scripts/workflow_registrar.py \
  <todo_file> <workflow_type> <slug> [--title TITLE]
```

**Arguments:**
- `todo_file`: Path to TODO_*.md file
- `workflow_type`: Workflow type ('feature' | 'release' | 'hotfix')
- `slug`: Workflow slug
- `--title` (optional): Workflow title (auto-generated if not provided)

**Updates:**
- Adds workflow to `TODO.md workflows.active[]` array
- Updates `TODO.md last_update` timestamp

**When to use:**
- After creating BMAD planning (Phase 1)
- After creating feature worktree (Phase 2)
- Ensures TODO.md tracks all active workflows

### workflow_archiver.py

Archive completed workflow and update TODO.md manifest.

```bash
python .claude/skills/workflow-utilities/scripts/workflow_archiver.py \
  <todo_file> [--summary SUMMARY] [--version VERSION]
```

**Arguments:**
- `todo_file`: Path to TODO_*.md file to archive
- `--summary` (optional): Summary of what was completed
- `--version` (optional): Semantic version (e.g., '1.5.0')

**Actions:**
1. Moves TODO_*.md → ARCHIVED/TODO_*.md
2. Updates TODO.md: moves workflow from active[] to archived[] array
3. Updates TODO.md statistics (total_workflows_completed)
4. Extracts metadata from workflow file (version, summary)

**When to use:**
- Phase 4.3: After PR merged to contrib branch
- Before creating PR contrib → develop

### sync_manifest.py

Synchronize TODO.md manifest with filesystem state.

```bash
# Preview changes
python .claude/skills/workflow-utilities/scripts/sync_manifest.py --dry-run

# Sync TODO.md
python .claude/skills/workflow-utilities/scripts/sync_manifest.py
```

**Actions:**
1. Scans current directory for TODO_*.md files (active)
2. Scans ARCHIVED/ for TODO_*.md files (archived)
3. Rebuilds TODO.md workflows.active[] and workflows.archived[] arrays
4. Updates statistics

**When to use:**
- Recovery: TODO.md out of sync with filesystem
- Verification: Check TODO.md reflects actual files
- Migration: Rebuilding TODO.md from scratch

**Warning:** Replaces TODO.md arrays with filesystem state. Manual metadata edits may be lost.

### VCS Abstraction Layer (vcs/)

Provides unified interface for GitHub and Azure DevOps operations via CLI adapters.

**Purpose:**
- Abstract VCS provider differences (GitHub vs Azure DevOps)
- Enable workflow portability across VCS platforms
- Provide consistent interface for PR operations, issue management, and PR feedback

**Location:** `.claude/skills/workflow-utilities/scripts/vcs/`

**Key files:**
- `provider.py` - Auto-detect VCS provider from git remote URL
- `base_adapter.py` - Base adapter interface (abstract methods)
- `github_adapter.py` - GitHub CLI (gh) adapter implementation
- `azure_adapter.py` - Azure DevOps CLI (az) adapter implementation
- `config.py` - VCS configuration

**Provider Detection:**
```python
from .vcs.provider import detect_from_remote, VCSProvider

# Auto-detect from git remote
provider = detect_from_remote()
# Returns: VCSProvider.GITHUB or VCSProvider.AZURE_DEVOPS

# Manual detection from URL
provider = detect_from_url("https://github.com/user/repo.git")
# Returns: VCSProvider.GITHUB
```

**Base Adapter Interface:**

All adapters implement these methods:

```python
class BaseVCSAdapter(ABC):
    @abstractmethod
    def create_pr(self, title: str, body: str, source_branch: str, target_branch: str) -> str:
        """Create pull request, returns PR URL."""
        pass

    @abstractmethod
    def fetch_pr_comments(self, pr_number: int) -> list:
        """Fetch review comments from a pull request.

        Returns:
            List of comment dictionaries with keys:
                - author: Comment author
                - body: Comment text
                - file: File path (if file comment)
                - line: Line number (if file comment)
                - created_at: Comment timestamp
        """
        pass

    @abstractmethod
    def update_pr(self, pr_number: int, title: str = None, body: str = None) -> None:
        """Update pull request title or description."""
        pass

    @abstractmethod
    def get_pr_status(self, pr_number: int) -> dict:
        """Get pull request status (approval, merge state).

        Returns:
            Dictionary with keys:
                - state: PR state (open/closed/merged)
                - mergeable: Boolean indicating if PR can be merged
                - approved: Boolean indicating if PR is approved
                - reviews_required: Number of approvals required
        """
        pass
```

**GitHub Adapter (github_adapter.py):**

Uses GitHub CLI (`gh`) for all operations.

```python
from .vcs.github_adapter import GitHubAdapter

adapter = GitHubAdapter()

# Create PR
pr_url = adapter.create_pr(
    title="feat: auth system (v1.6.0)",
    body="PR body content",
    source_branch="feature/20251103T143000Z_auth",
    target_branch="contrib/stharrold"
)
# Returns: "https://github.com/user/repo/pull/94"

# Fetch PR comments
comments = adapter.fetch_pr_comments(94)
# Returns: [
#   {
#     'author': 'reviewer1',
#     'body': 'Please add error handling here',
#     'file': 'src/auth.py',
#     'line': 42,
#     'created_at': '2025-11-08T10:30:00Z'
#   },
#   ...
# ]

# Update PR
adapter.update_pr(94, title="feat: auth system (v1.7.0)")

# Get PR status
status = adapter.get_pr_status(94)
# Returns: {
#   'state': 'open',
#   'mergeable': True,
#   'approved': True,
#   'reviews_required': 1
# }
```

**Azure DevOps Adapter (azure_adapter.py):**

Uses Azure CLI (`az`) for all operations.

```python
from .vcs.azure_adapter import AzureDevOpsAdapter

adapter = AzureDevOpsAdapter()

# Create PR
pr_url = adapter.create_pr(
    title="feat: auth system (v1.6.0)",
    body="PR body content",
    source_branch="feature/20251103T143000Z_auth",
    target_branch="contrib/stharrold"
)
# Returns: "https://dev.azure.com/org/project/_git/repo/pullrequest/94"

# Fetch PR comments (threads)
comments = adapter.fetch_pr_comments(94)
# Returns: [
#   {
#     'author': 'reviewer1@example.com',
#     'body': 'Please add error handling here',
#     'file': 'src/auth.py',
#     'line': 42,
#     'created_at': '2025-11-08T10:30:00Z',
#     'status': 'active'  # Azure-specific: active/pending/resolved
#   },
#   ...
# ]

# Update PR
adapter.update_pr(94, title="feat: auth system (v1.7.0)")

# Get PR status
status = adapter.get_pr_status(94)
# Returns: {
#   'state': 'active',  # Azure-specific: active/completed/abandoned
#   'mergeable': True,
#   'approved': True,
#   'reviews_required': 2
# }
```

**PR Feedback Methods (Added v5.2.0):**

Three new methods for PR feedback handling:

1. **fetch_pr_comments(pr_number)**
   - GitHub: Uses `gh pr view --json reviews,comments`
   - Azure: Uses `az repos pr show --query threads`
   - Returns unified comment format (author, body, file, line, timestamp)
   - Used by `generate_work_items_from_pr.py` to extract unresolved conversations

2. **update_pr(pr_number, title, body)**
   - GitHub: Uses `gh pr edit`
   - Azure: Uses `az repos pr update`
   - Updates PR title or description
   - Used for updating PR with work-item links

3. **get_pr_status(pr_number)**
   - GitHub: Uses `gh pr view --json state,mergeable,reviews`
   - Azure: Uses `az repos pr show --query status,mergeStatus`
   - Returns approval and merge status
   - Used for validation before creating work-items

**Integration Example (from git-workflow-manager):**
```python
from pathlib import Path
import sys

# Add vcs module to path
vcs_path = Path('.claude/skills/workflow-utilities/scripts')
sys.path.insert(0, str(vcs_path))

from vcs.provider import detect_from_remote, VCSProvider
from vcs.github_adapter import GitHubAdapter
from vcs.azure_adapter import AzureDevOpsAdapter

# Auto-detect provider
provider = detect_from_remote()

# Initialize adapter
if provider == VCSProvider.GITHUB:
    adapter = GitHubAdapter()
elif provider == VCSProvider.AZURE_DEVOPS:
    adapter = AzureDevOpsAdapter()
else:
    raise ValueError(f"Unsupported VCS provider: {provider}")

# Fetch unresolved PR comments
comments = adapter.fetch_pr_comments(94)
unresolved = [c for c in comments if not c.get('resolved', False)]

# For each unresolved comment, create work-item
for i, comment in enumerate(unresolved, start=1):
    # ... create GitHub issue or Azure DevOps task
    pass
```

**When to use VCS abstraction:**
- Creating PRs (Phase 4: Integration)
- Fetching PR feedback (Phase 4: PR Feedback)
- Updating PR status
- Any VCS-specific operation that needs to work across GitHub and Azure DevOps

**Key features:**
- Provider auto-detection from git remote
- Unified interface (same method signatures)
- CLI-based (no API tokens required in most cases)
- Error handling with helpful messages
- Portable across GitHub and Azure DevOps

## Usage Examples

### Deprecating Old Files

```python
import subprocess

# Deprecate old implementation files
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/deprecate_files.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'old-validator',
    'src/old_validator.py',
    'tests/test_old_validator.py'
], check=True)
```

### Creating Standard Directories

```python
import subprocess

# Create planning directory with standard structure
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/directory_structure.py',
    'planning/json-validator'
], check=True)
```

### Updating TODO Tasks

```python
import subprocess

# Mark task as complete
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/todo_updater.py',
    'TODO_feature_20251022T143022Z_json-validator.md',
    'impl_003',
    'complete',
    '35'  # context usage percentage
], check=True)
```

### Managing Workflow Lifecycle

```python
import subprocess

# Register new workflow in TODO.md (Phase 1/2)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_registrar.py',
    'TODO_feature_20251103T143000Z_auth.md',
    'feature',
    'auth',
    '--title', 'User Authentication System'
], check=True)

# Archive completed workflow (Phase 4.3)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/workflow_archiver.py',
    'TODO_feature_20251103T143000Z_auth.md',
    '--summary', 'Implemented OAuth2 authentication with Google and GitHub',
    '--version', '1.5.0'
], check=True)

# Sync TODO.md with filesystem (recovery)
subprocess.run([
    'python',
    '.claude/skills/workflow-utilities/scripts/sync_manifest.py'
], check=True)
```

## Directory Standards

All directories created by these utilities follow the standard structure:

```
directory/
├── CLAUDE.md      # Context for Claude Code
├── README.md      # Human-readable documentation
└── ARCHIVED/      # Deprecated files (except if directory IS archived)
    ├── CLAUDE.md
    └── README.md
```

## Integration with Other Skills

All skills can use these helper functions:

```python
# Example from bmad-planner
from pathlib import Path
import subprocess

def create_planning_with_structure(feature_name):
    """Create planning directory with standard structure."""

    planning_dir = Path('planning') / feature_name

    # Create directory structure
    subprocess.run([
        'python',
        '.claude/skills/workflow-utilities/scripts/directory_structure.py',
        str(planning_dir)
    ], check=True)

    # Now create planning documents
    # ...
```

## Best Practices

- Always use these utilities for consistency
- Don't manually create directory structures
- Use deprecation for old files, not deletion
- Update TODO file after each meaningful step
- Check archives before deleting files permanently
