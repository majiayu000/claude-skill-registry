---
name: mega-plan
version: "3.2.0"
description: Project-level multi-task orchestration system. Manages multiple hybrid:worktree features in parallel with dependency resolution, coordinated PRD generation, and unified merge workflow.
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Task
  - Glob
  - Grep
  - AskUserQuestion
hooks:
  PreToolUse:
    # Show mega-plan context and parallel execution reminder for relevant tools
    - matcher: "Write|Edit|Bash|Task"
      hooks:
        - type: command
          command: |
            # Show mega-plan context if we're in a mega-plan project
            if [ -f "mega-plan.json" ] || [ -f ".mega-execution-context.md" ]; then
              if command -v python3 &> /dev/null; then
                # Update and display context reminder
                python3 "${CLAUDE_PLUGIN_ROOT}/skills/mega-plan/scripts/mega-context-reminder.py" both 2>/dev/null || true
              fi
            fi
            # Detect potential wrong-branch execution
            if [ -f "mega-plan.json" ] && [ -d ".worktree" ]; then
              CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
              if [ "$CURRENT_BRANCH" = "main" ] || [ "$CURRENT_BRANCH" = "master" ]; then
                echo ""
                echo "!!! WARNING: You are on $CURRENT_BRANCH but worktrees exist !!!"
                echo "!!! Feature work should happen in .worktree/<feature>/ directories !!!"
                echo ""
              fi
            fi
  PostToolUse:
    # Sync status and update context file after significant operations
    - matcher: "Write|Edit"
      hooks:
        - type: command
          command: |
            if [ -f "mega-plan.json" ]; then
              if command -v python3 &> /dev/null; then
                python3 "${CLAUDE_PLUGIN_ROOT}/skills/mega-plan/scripts/mega-sync.py" 2>/dev/null || true
                python3 "${CLAUDE_PLUGIN_ROOT}/skills/mega-plan/scripts/mega-context-reminder.py" update 2>/dev/null || true
              fi
            fi
---

# Mega Plan

A project-level orchestration system that sits above `hybrid-ralph` to manage multiple parallel features as a unified project plan.

## Auto-Recovery Protocol (CRITICAL)

**At the START of any interaction**, perform this check to recover context after compression/truncation:

1. Check if `.mega-execution-context.md` exists in the project root
2. If YES:
   - Read the file content using Read tool
   - Display: "Detected ongoing mega-plan execution"
   - Show current batch and active worktrees from the file
   - **CRITICAL**: All feature work MUST happen in worktrees, NOT main branch
   - If unsure of state, suggest: `/plan-cascade:mega-resume --auto-prd`

3. If NO but `mega-plan.json` exists:
   - Run: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/mega-plan/scripts/mega-context-reminder.py" both`
   - This will generate the context file and display current state

This ensures context recovery even after:
- Context compression (AI summarizes old messages)
- Context truncation (old messages deleted)
- New conversation session
- Claude Code restart

## Architecture

```
Level 1: Mega Plan (Project Level)
    └── Level 2: Features (Feature Level) = hybrid:worktree
              └── Level 3: Stories (Story Level) = hybrid internal parallelism
```

## Quick Start

### Create a Mega Plan

Generate a mega-plan from your project description:

```
/mega:plan Build an e-commerce platform with user authentication, product catalog, shopping cart, and order processing
```

This will:
1. Analyze your project description
2. Break it into features with dependencies
3. Create `mega-plan.json`, `mega-findings.md`, `.mega-status.json`
4. Display the plan for review

### Approve and Execute

After reviewing the mega-plan:

```
/mega:approve
```

Or with automatic PRD approval for all features:

```
/mega:approve --auto-prd
```

This will:
1. Calculate feature batches based on dependencies
2. Create worktrees for Batch 1 features
3. Generate PRDs in each worktree
4. Wait for PRD approvals (or auto-approve with `--auto-prd`)
5. Execute story batches within each feature
6. Progress to next feature batch when complete

### Monitor Progress

```
/mega:status
```

Shows:
- Overall project progress percentage
- Feature status by batch
- Story progress within each feature
- Current batch details

### Complete and Merge

When all features are complete:

```
/mega:complete
```

This will:
1. Verify all features are complete
2. Merge features in dependency order
3. Clean up worktrees and branches
4. Remove mega-plan files

## File Structure

```
project-root/
├── mega-plan.json              # Project-level plan
├── mega-findings.md            # Shared findings (read-only in worktrees)
├── .mega-status.json           # Execution status
├── .worktree/
│   ├── feature-auth/
│   │   ├── prd.json           # Feature PRD
│   │   ├── findings.md        # Feature-specific findings
│   │   ├── progress.txt       # Story progress
│   │   ├── mega-findings.md   # Read-only link to shared findings
│   │   └── .planning-config.json
│   └── feature-products/
│       └── ...
```

## Commands Reference

### /mega:plan

Generate a mega-plan from project description.

```
/mega:plan <project description>
```

**Example:**
```
/mega:plan Create a blog platform with user accounts, article management, comments, and RSS feeds
```

### /mega:edit

Edit the mega-plan in your default editor.

```
/mega:edit
```

### /mega:approve

Approve the mega-plan and begin execution.

```
/mega:approve [--auto-prd]
```

**Options:**
- `--auto-prd`: Automatically approve all generated PRDs (skip manual review)

**Approval Modes:**

| Mode | Trigger | Use Case |
|------|---------|----------|
| Manual PRD Review | `/mega:approve` | Need to review each feature's PRD |
| Auto PRD Approval | `/mega:approve --auto-prd` | Trust PRD generation, want fast execution |

### /mega:status

Show detailed execution status.

```
/mega:status
```

### /mega:complete

Complete the mega-plan and merge all features.

```
/mega:complete [target-branch]
```

**Arguments:**
- `target-branch` (optional): Override the target branch from mega-plan

## mega-plan.json Format

```json
{
  "metadata": {
    "created_at": "2026-01-28T10:00:00Z",
    "version": "1.0.0"
  },
  "goal": "Project goal",
  "description": "Original user description",
  "execution_mode": "auto",
  "target_branch": "main",
  "features": [
    {
      "id": "feature-001",
      "name": "feature-auth",
      "title": "User Authentication",
      "description": "Detailed description for PRD generation",
      "priority": "high",
      "dependencies": [],
      "status": "pending"
    }
  ]
}
```

## Feature Status Flow

```
pending → prd_generated → approved → in_progress → complete
                                           ↓
                                        failed
```

| Status | Description |
|--------|-------------|
| `pending` | Feature not yet started |
| `prd_generated` | Worktree created, PRD generated |
| `approved` | PRD approved, ready for execution |
| `in_progress` | Stories are being executed |
| `complete` | All stories complete |
| `failed` | Feature execution failed |

## Execution Modes

### Auto Mode

Features and their story batches execute automatically:

```
Batch 1 (Features) → PRDs generated → approved → stories execute → complete
         ↓
Batch 2 (Features) → PRDs generated → approved → stories execute → complete
         ↓
All complete → /mega:complete
```

### Manual Mode

Each batch waits for explicit confirmation:

```
Batch 1 → PRDs generated → [you review] → /approve in each worktree
         ↓
Batch 2 → PRDs generated → [you review] → /approve in each worktree
         ↓
All complete → /mega:complete
```

## Workflows

### Complete Workflow

```
1. /mega:plan "Build e-commerce platform"
   ↓
2. Review generated mega-plan.json
   ↓
3. /mega:edit (if needed) or /mega:approve
   ↓
4. Feature worktrees created (Batch 1)
   ↓
5. PRDs generated in each worktree
   ↓
6. Review and /approve in each worktree (or use --auto-prd)
   ↓
7. Stories execute in parallel
   ↓
8. Monitor with /mega:status
   ↓
9. Batch 2 features start when Batch 1 complete
   ↓
10. All complete → /mega:complete
```

### Multi-Terminal Workflow

```bash
# Terminal 1: Main orchestration
/mega:plan "Project description"
/mega:approve
/mega:status  # Monitor progress

# Terminal 2: Feature 1 work
cd .worktree/feature-auth
/approve  # Approve PRD
# ... stories execute ...

# Terminal 3: Feature 2 work (parallel!)
cd .worktree/feature-products
/approve  # Approve PRD
# ... stories execute ...

# Terminal 1: After all complete
/mega:complete
```

## Relationship with Hybrid Ralph

Mega Plan orchestrates **multiple** hybrid-ralph workflows:

| Component | Mega Plan | Hybrid Ralph |
|-----------|-----------|--------------|
| Scope | Project-level | Feature-level |
| Unit | Features | Stories |
| Files | mega-plan.json | prd.json |
| Findings | mega-findings.md (shared) | findings.md (per-feature) |
| Worktrees | Creates for features | Works within worktree |
| Merge | All features → target | N/A (handled by mega) |

## Core Python Modules

### mega_generator.py

Generates mega-plan from project descriptions.

```bash
# Validate mega-plan
python3 mega_generator.py validate

# Show execution batches
python3 mega_generator.py batches

# Show progress
python3 mega_generator.py progress
```

### mega_state.py

Thread-safe state management.

```bash
# Read mega-plan
python3 mega_state.py read-plan

# Read status
python3 mega_state.py read-status

# Sync from worktrees
python3 mega_state.py sync-worktrees
```

### feature_orchestrator.py

Orchestrates feature execution.

```bash
# Show execution plan
python3 feature_orchestrator.py plan

# Show status
python3 feature_orchestrator.py status
```

### merge_coordinator.py

Coordinates final merge.

```bash
# Verify all complete
python3 merge_coordinator.py verify

# Show merge plan
python3 merge_coordinator.py plan

# Complete (merge & cleanup)
python3 merge_coordinator.py complete
```

## Findings Management

### Shared Findings (mega-findings.md)

- Located at project root
- Contains findings relevant to all features
- Read-only copy placed in each worktree
- Updated only from project root

### Feature Findings (findings.md)

- Located in each feature worktree
- Contains feature-specific discoveries
- Tagged with story IDs
- Independent per feature

## Best Practices

1. **Clear Feature Boundaries**: Each feature should be independent enough to develop in isolation
2. **Minimize Dependencies**: Fewer dependencies mean more parallelism
3. **Meaningful Names**: Use descriptive feature names (they become directory names)
4. **Review PRDs**: Take time to review generated PRDs before approving
5. **Monitor Progress**: Use `/mega:status` regularly to track execution
6. **Handle Failures**: If a feature fails, fix it in its worktree before completing

## Troubleshooting

### Worktree Conflict

```
Error: Worktree already exists
```

Solution: Remove stale worktree or use different feature name.

### Merge Conflict

```
Error: Merge conflict in feature-001
```

Solution:
1. Resolve conflict in target branch
2. Re-run `/mega:complete`

### Incomplete Features

```
Error: Incomplete features: feature-002, feature-003
```

Solution:
1. Check `/mega:status` for details
2. Complete stories in incomplete features
3. Re-run `/mega:complete`

## See Also

- [hybrid-ralph](../hybrid-ralph/SKILL.md) - Feature-level PRD execution
- [planning-with-files](../planning-with-files/SKILL.md) - Base planning skill
