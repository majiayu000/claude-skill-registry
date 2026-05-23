---
name: workflow-orchestrator
version: 5.1.0
description: |
  Orchestrates git workflow for Python feature/release/hotfix development.
  Loads and coordinates other skills based on current context.
  Includes PR feedback handling via work-item generation.

  Use when:
  - User says "next step?" or "continue workflow"
  - Working in git repo with TODO_[feature|release|hotfix]_*.md files
  - Need to determine workflow phase and load appropriate skills
  - Handling PR feedback via work-items

  Triggers: next step, continue, what's next, workflow status, PR feedback

  Coordinates: tech-stack-adapter, git-workflow-manager, bmad-planner,
  speckit-author, quality-enforcer, workflow-utilities

  Context management: Prompt user to run /context when context usage
  is high, then /init to reset before continuing workflow.
---

# Workflow Orchestrator

## Purpose

Main coordinator for multi-branch git workflow. Detects current context
and loads appropriate skills dynamically.

## Context Detection Algorithm

```python
def detect_context():
    """Determine current workflow phase and required skills."""
    import os
    from pathlib import Path

    # Get repository info
    repo_root = Path(os.popen('git rev-parse --show-toplevel').read().strip())
    current_dir = Path.cwd()
    current_branch = os.popen('git branch --show-current').read().strip()

    # Determine if in worktree
    is_worktree = current_dir != repo_root

    # Find TODO file
    if is_worktree:
        # Look for TODO in parent (main repo)
        todo_pattern = '../TODO_*.md'
        import glob
        todos = glob.glob(str(current_dir / todo_pattern))
        if todos:
            todo_file = Path(todos[0]).name
            workflow_type = todo_file.split('_')[1]  # feature|release|hotfix
        else:
            return None, None, None
    else:
        # In main repo
        import glob
        todos = glob.glob(str(repo_root / 'TODO_*.md'))
        if todos:
            todo_file = Path(todos[0]).name
            workflow_type = todo_file.split('_')[1]
        else:
            workflow_type = None
            todo_file = None

    return {
        'repo_root': repo_root,
        'current_dir': current_dir,
        'current_branch': current_branch,
        'is_worktree': is_worktree,
        'workflow_type': workflow_type,
        'todo_file': todo_file
    }
```

## Skill Loading Logic

When user says "next step?":

1. **Always load tech-stack-adapter first (once per session)**
   ```
   Read tech-stack-adapter/SKILL.md
   Execute: python tech-stack-adapter/scripts/detect_stack.py
   Store: TEST_CMD, BUILD_CMD, COVERAGE_CMD, etc.
   ```

2. **Detect context and load appropriate skills**
   ```python
   context = detect_context()

   if context['is_worktree']:
       # In feature/release/hotfix worktree
       if context['workflow_type'] in ['feature', 'release', 'hotfix']:
           load_skill('speckit-author')  # For spec.md, plan.md
           load_skill('git-workflow-manager')  # For commits, pushes
   else:
       # In main repo on contrib branch
       if 'contrib' in context['current_branch']:
           load_skill('bmad-planner')  # For requirements, architecture
           load_skill('git-workflow-manager')  # For branch operations

   # Always available for quality checks
   load_skill('quality-enforcer')  # When running tests, checking coverage
   load_skill('workflow-utilities')  # For utilities
   ```

3. **Parse TODO file to determine current step**
   ```python
   import yaml
   from pathlib import Path

   def parse_todo_file(todo_path):
       """Extract workflow progress from TODO file."""
       content = Path(todo_path).read_text()

       # Extract YAML frontmatter
       if content.startswith('---'):
           parts = content.split('---', 2)
           frontmatter = yaml.safe_load(parts[1])
           body = parts[2]
       else:
           return None

       return {
           'workflow_progress': frontmatter.get('workflow_progress', {}),
           'quality_gates': frontmatter.get('quality_gates', {}),
           'metadata': frontmatter.get('metadata', {})
       }
   ```

4. **Prompt user with next step**
   ```
   Next step from workflow:
   Phase <N>, Step <N.M>: <description>

   This will:
   - <action 1>
   - <action 2>
   - <action 3>

   Would you like to proceed? (Y/n)
   ```

5. **Wait for explicit "Y" confirmation**
   - Do NOTHING until user confirms
   - If "n", wait for next instruction

6. **Execute step using loaded skills**
   - Call appropriate skill methods
   - Update TODO file via workflow-utilities
   - Commit changes via git-workflow-manager

## Workflow Phases

### Phase 0: Initial Setup
1. Verify prerequisites (gh CLI, uv, git)
2. Create .claude/skills/ directory structure
3. Generate workflow files (WORKFLOW.md, CLAUDE.md, README.md)
4. Initialize contrib/<gh-user> branch

**Skills loaded:** tech-stack-adapter, git-workflow-manager, workflow-utilities

### Phase 1: Planning (Main Repo)
**Interactive BMAD planning session:**

1. **Load bmad-planner skill**
2. **BMAD Analyst (Interactive):**
   - Asks: What problem does this solve? Who will use it?
   - Generates: planning/<feature>/requirements.md
3. **BMAD Architect (Interactive):**
   - Reads requirements.md for context
   - Asks: Technology preferences? Performance targets?
   - Generates: planning/<feature>/architecture.md
4. **BMAD PM (Interactive):**
   - Reads requirements + architecture
   - Breaks down into epics with dependencies
   - Generates: planning/<feature>/epics.md
5. **Commit planning documents to contrib branch**

**Output:** planning/<feature>/ directory with requirements.md, architecture.md, epics.md

**Skills loaded:** bmad-planner, workflow-utilities

**Next:** Create feature worktree and move to Phase 2

### Phase 2: Feature Development (Worktree)

**Step 2.1:** Create feature worktree from contrib branch (git-workflow-manager)

**Step 2.2:** Switch to worktree directory

**Step 2.3:** Call SpecKit interactive tool

**Invocation:**
```python
import subprocess
import sys

# Call create_specifications.py
result = subprocess.run([
    'python',
    '.claude/skills/speckit-author/scripts/create_specifications.py',
    workflow_type,  # feature, release, or hotfix
    slug,          # feature slug (e.g., my-feature)
    gh_user,       # GitHub username
    '--todo-file', f'../TODO_{workflow_type}_{timestamp}_{slug}.md'
], check=True)

# Script handles:
# - BMAD context detection (../planning/<slug>/)
# - Interactive Q&A with user (5-15 questions)
# - Generates specs/<slug>/spec.md and plan.md
# - Creates compliant directory structure
# - Updates TODO_*.md with tasks from plan.md
# - Commits changes to feature branch

print("✓ SpecKit specifications created")
```

**What SpecKit does:**
1. **Detect BMAD context:** Checks ../planning/<feature>/ for requirements, architecture, epics
2. **Interactive Q&A:** Asks implementation-specific questions (adapts based on BMAD availability)
3. **Generate specs:** Creates specs/<feature>/spec.md and plan.md from templates
4. **Update TODO:** Parses tasks from plan.md, updates TODO_*.md YAML frontmatter
5. **Commit:** Stages and commits all changes

**Step 2.4:** Implement code following spec.md

**Step 2.5:** Write tests targeting ≥80% coverage

**Step 2.6:** Create containers (if applicable)

**Input from Phase 1:** BMAD planning documents (requirements, architecture, epics) - optional but recommended

**Output:** Working implementation with tests, specs, and updated TODO

**Skills used:** speckit-author (callable tool), git-workflow-manager, quality-enforcer, workflow-utilities

### Phase 3: Quality Assurance
1. Run tests with coverage
2. Validate quality gates
3. Calculate semantic version

**Skills loaded:** quality-enforcer, workflow-utilities

### Phase 4: Integration

**Step 4.1:** Create PR from feature → contrib/<gh-user> (git-workflow-manager)

**Step 4.2:** Reviewers add comments and conversations in GitHub/Azure DevOps web portal

**Step 4.3:** Handle PR Feedback via Work-Items (Optional)

**When to use:**
- PR has unresolved conversations requiring substantive changes
- Changes are too large to fix on same feature branch
- Want to approve PR while tracking feedback separately

**Decision tree:**
```
PR reviewed with comments
├─ Simple fixes (typos, formatting, minor adjustments)
│  └─ Fix directly on feature branch, push update, skip to Step 4.4
└─ Substantive changes (new features, refactoring, architecture changes)
   └─ Generate work-items, continue to Step 4.3
```

**Invocation:**
```python
import subprocess

# Generate work-items from unresolved PR conversations
result = subprocess.run([
    'python',
    '.claude/skills/git-workflow-manager/scripts/generate_work_items_from_pr.py',
    pr_number  # e.g., '94'
], check=True)

# Script outputs:
# ✓ Found 3 unresolved conversations
# ✓ Created work-item: pr-94-issue-1 (URL)
# ✓ Created work-item: pr-94-issue-2 (URL)
# ✓ Created work-item: pr-94-issue-3 (URL)

# For each work-item, repeat Phase 2-4:
# 1. Create feature worktree: create_worktree.py feature pr-94-issue-1 contrib/<user>
# 2. Implement fix (SpecKit optional for simple fixes)
# 3. Run quality gates
# 4. Create PR: feature/YYYYMMDDTHHMMSSZ_pr-94-issue-1 → contrib/<user>
# 5. Merge in web portal
# 6. Repeat for remaining work-items
```

**What it does:**
- Detects VCS provider (GitHub or Azure DevOps)
- Fetches unresolved PR conversations (GitHub: `isResolved==false`, Azure: `status==active|pending`)
- Creates work-items (GitHub issues or Azure DevOps tasks) with slug pattern `pr-{pr_number}-issue-{sequence}`
- Links work-items to original PR
- Preserves conversation context (file, line, author, timestamps)

**Benefits:**
- Enables PR approval without blocking on follow-up work
- Creates traceable lineage: PR → work-items → feature branches → new PRs
- Compatible with all issue trackers (GitHub, Azure DevOps, others)

**Step 4.4:** User approves and merges PR in GitHub/Azure DevOps web portal

**Step 4.5:** Archive workflow and delete worktree

**Step 4.6:** Update BMAD planning with as-built details (optional but recommended)

**Invocation:**
```python
import subprocess

# Call update_asbuilt.py from main repo on contrib branch
result = subprocess.run([
    'python',
    '.claude/skills/speckit-author/scripts/update_asbuilt.py',
    f'planning/{slug}',  # BMAD planning directory
    f'specs/{slug}'      # SpecKit specs directory
], check=True)

# Script handles:
# - Reads as-built specs from specs/<slug>/
# - Compares with original planning from planning/<slug>/
# - Interactive Q&A about deviations and metrics
# - Updates planning/ files with "As-Built" sections
# - Commits updates to contrib branch

print("✓ BMAD planning updated with as-built details")
print("  Feedback loop completed")
```

**What update_asbuilt.py does:**
1. **Read as-built specs:** specs/<slug>/spec.md and plan.md
2. **Analyze deviations:** Compare with planning/<slug>/ documents
3. **Gather metrics:** Interactive Q&A about effort, performance, lessons learned
4. **Update planning:** Appends "As-Built" sections to requirements.md, architecture.md, epics.md
5. **Commit:** Saves feedback for future planning

**Benefits:**
- Improves future planning accuracy
- Documents what actually happened vs what was planned
- Identifies patterns in estimation and technology choices
- Creates living documentation

**Step 4.7:** Rebase contrib/<gh-user> onto develop (git-workflow-manager)

**Step 4.8:** Create PR from contrib/<gh-user> → develop

**Skills used:** git-workflow-manager, speckit-author (update_asbuilt.py, optional)

### Phase 5: Release (Worktree)
1. Create release worktree from develop
2. Final QA and documentation
3. Create PR to main
4. Tag release after merge

**Skills loaded:** git-workflow-manager, quality-enforcer

## Data Flow Between Phases

### Phase 1 → Phase 2: BMAD to SpecKit

**Phase 1 produces:**
```
planning/<feature>/
├── requirements.md    # Business requirements, user stories, acceptance criteria
├── architecture.md    # Technology stack, data models, API design
└── epics.md          # Epic breakdown, priorities, dependencies
```

**Create Worktree:**
```bash
# Worktree creation preserves link to main repo
git worktree add ../repo_feature_<slug> feature/<timestamp>_<slug>
```

**Phase 2 consumes:**
```python
# SpecKit reads from main repo
planning_context = {
    'requirements': Path('../planning/<feature>/requirements.md').read_text(),
    'architecture': Path('../planning/<feature>/architecture.md').read_text(),
    'epics': Path('../planning/<feature>/epics.md').read_text()
}

# Uses context to generate
specs/<feature>/
├── spec.md     # Detailed specification (informed by requirements + architecture)
└── plan.md     # Implementation tasks (informed by epics + architecture)
```

**Why this connection matters:**
- **Consistency:** Technology choices in spec.md match architecture.md stack
- **Completeness:** spec.md acceptance criteria cover requirements.md success criteria
- **Traceability:** plan.md tasks map to epics.md breakdown
- **Less rework:** Planning clarifies before coding starts

## Context Management

**CRITICAL:** Monitor context usage and enforce 100K token threshold.

### Token Threshold Protocol

```python
def check_context_usage(current_tokens):
    """
    Monitor context usage and trigger checkpoint at 100K tokens.

    Effective capacity: ~136K tokens (200K - 64K overhead)
    Checkpoint threshold: 100K tokens (~73% of effective capacity)
    """
    CHECKPOINT_THRESHOLD = 100_000

    if current_tokens >= CHECKPOINT_THRESHOLD:
        print("\n⚠️  CONTEXT CHECKPOINT: 100K tokens reached")
        print("\n📝 Saving workflow state...")

        # 1. Update TODO_*.md with current state
        update_todo_frontmatter(
            phase=current_phase,
            step=current_step,
            last_task=last_completed_task,
            status=current_status
        )

        # 2. Add context checkpoint entry
        add_context_checkpoint(
            token_usage=current_tokens,
            phase=current_phase,
            step=current_step,
            notes=generate_status_summary()
        )

        # 3. Update task statuses
        for task in all_tasks:
            update_task_status(task.id, task.status)

        # 4. Commit changes
        git_commit("chore: context checkpoint at 100K tokens")

        print("✓ State saved to TODO_*.md")
        print("\n🔄 REQUIRED ACTIONS:")
        print("  1. Run: /init (updates CLAUDE.md memory files)")
        print("  2. Run: /compact (compresses memory buffer)")
        print("  3. Continue working - context preserved in TODO_*.md")
        print("\nToken usage will be reduced after /init + /compact.")

        return True  # Triggers pause for user action

    # Warn at 80K tokens (10K before checkpoint)
    elif current_tokens >= 80_000:
        print(f"\n⚠️  Context usage: {current_tokens:,} tokens")
        print("   Approaching 100K checkpoint threshold")
        print("   Recommendation: Complete current task before checkpoint")

    return False
```

### Automatic State Saving

When checkpoint is triggered, save to TODO_*.md:

**YAML Frontmatter:**
- `workflow_progress.last_update`: Current timestamp
- `workflow_progress.last_task`: Most recent task ID
- `context_checkpoints[]`: Add new checkpoint entry
- All `tasks[].status`: Update to current state (pending/in_progress/completed)

**TODO Body:**
- Append "## Context Checkpoint" section
- Document: completed tasks, current task, next tasks, blockers

### Continue After Checkpoint

After `/init` and `/compact`, token usage is reduced by:
- Updating CLAUDE.md memory files with current state
- Compressing memory buffer to remove redundant context
- TODO_*.md preserves all workflow state

User can then:
- Continue with current task
- Say "next step?" for next task
- Reference TODO_*.md to see progress

Claude will:
1. Work with reduced token count (memory optimized)
2. Reference TODO_*.md for workflow state as needed
3. Continue from last checkpoint without data loss

## Interactive Confirmation Pattern

```python
def prompt_for_confirmation(step_info):
    """Always wait for explicit Y before proceeding."""
    print(f"\nNext step from workflow:")
    print(f"Step {step_info['phase']}.{step_info['step']}: {step_info['description']}")
    print(f"\nThis will:")
    for action in step_info['actions']:
        print(f"  - {action}")
    print(f"\nWould you like to proceed with Step {step_info['phase']}.{step_info['step']}? (Y/n)")

    # WAIT for user response - do NOT proceed automatically
    # Only continue if user types "Y"
```

## Directory Standards

**Every directory must have:**
- `CLAUDE.md` - Context-specific guidance
- `README.md` - Human-readable documentation
- `ARCHIVED/` subdirectory (except ARCHIVED itself)

Use workflow-utilities/scripts/directory_structure.py to create compliant directories.

## Key Behaviors

✓ Load orchestrator first, then relevant skills per phase
✓ Always wait for "Y" confirmation
✓ Monitor context via /context command
✓ Save state and /init when context > 50%
✓ Update TODO file after each step
✓ Commit changes with descriptive messages
✓ Use workflow-utilities for shared utilities
