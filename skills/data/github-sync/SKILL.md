---
name: github-sync
description: Two-way synchronization between SpecWeave specs and GitHub Projects (push & pull by default). Use when asking about GitHub integration setup, troubleshooting sync issues, or configuring sync settings. For actual syncing, use /sw-github:sync-spec command.
---

# GitHub Sync - Two-way Spec ↔ Project Synchronization

**Purpose**: Seamlessly synchronize SpecWeave specs with GitHub Projects for team visibility and project management.

**Default Behavior**: **Two-way sync** (push & pull) - Changes in either system are automatically synchronized

**⚠️ IMPORTANT**: This skill provides HELP and GUIDANCE about GitHub sync. For actual syncing, users should use the `/sw-github:sync-spec` command directly. This skill should NOT auto-activate when the command is being invoked.

## When to Activate

✅ **Do activate when**:
- User asks: "How do I set up GitHub sync?"
- User asks: "What GitHub credentials do I need?"
- User asks: "How does the GitHub integration work?"
- User needs help configuring GitHub integration

❌ **Do NOT activate when**:
- User invokes `/sw-github:sync-spec` command (command handles it)
- Command is already running (avoid duplicate invocation)
- Task completion hook is syncing (automatic process)

**Integration**: Works with `/sw-github:sync-spec` command

---

## CORRECT Architecture

**CRITICAL**: SpecWeave syncs **SPECS** to GitHub, NOT increments!

```
✅ CORRECT:
.specweave/docs/internal/specs/spec-001.md  ↔  GitHub Project
├─ User Story US-001                        ↔  GitHub Issue #1
├─ User Story US-002                        ↔  GitHub Issue #2
└─ User Story US-003                        ↔  GitHub Issue #3

❌ WRONG (OLD, REMOVED!):
.specweave/increments/0001-feature  ↔  GitHub Issue (DEPRECATED!)
```

**Why Specs, Not Increments?**
- ✅ **Specs = Permanent** (living docs, feature-level knowledge base)
- ❌ **Increments = Temporary** (implementation snapshots, can be deleted after done)
- ✅ **GitHub should mirror PERMANENT work**, not temporary iterations

---

## How GitHub Sync Works

### 1. Spec → GitHub Project (Export)

**Trigger**: When spec is created or updated

**Actions**:
1. Create GitHub Project with:
   - Title: `[SPEC-001] Core Framework & Architecture`
   - Description: Spec overview + progress
   - Columns: Backlog, In Progress, Done
   - Linked to repository

2. Store project ID in spec metadata:
   ```yaml
   # .specweave/docs/internal/specs/spec-001.md (frontmatter)
   ---
   externalLinks:
     github:
       projectId: 123
       projectUrl: https://github.com/users/anton-abyzov/projects/123
       syncedAt: 2025-11-11T10:00:00Z
   ---
   ```

3. Create GitHub Issues for each user story:
   - Title: `[US-001] As a developer, I want to install SpecWeave via NPM`
   - Body: Acceptance criteria as checkboxes
   - Labels: `user-story`, `spec:spec-001`, `priority:P1`
   - Linked to project

**Example GitHub Project**:
```markdown
# [SPEC-001] Core Framework & Architecture

**Status**: In Progress (75% complete)
**Priority**: P0 (Critical)
**Feature Area**: Foundation & Plugin System

## Overview

The core framework and architecture spec covers SpecWeave's foundational capabilities:
- TypeScript-based CLI framework
- Plugin system architecture
- Cross-platform compatibility

## Progress

- ✅ US-001: NPM installation (Complete)
- ✅ US-002: Plugin system (Complete)
- ⏳ US-003: Context optimization (In Progress)
- ⏳ US-004: Intelligent agents (In Progress)

**Overall**: 2/4 user stories complete (50%)

---

🤖 Auto-synced by SpecWeave GitHub Plugin
```

### 2. User Story Progress Updates (Spec → GitHub)

**Trigger**: After each task completion (via post-task-completion hook)

**Actions**:
1. **Update GitHub Issue** (for user story):
   - Updates acceptance criteria checkboxes
   - Marks completed ACs with `[x]`
   - Updates issue description
   - Updates labels (`in-progress`, `testing`, `ready-for-review`)

2. **Update GitHub Project**:
   - Moves cards between columns (Backlog → In Progress → Done)
   - Updates project progress percentage
   - Posts progress comment

**Example Issue Update**:
```markdown
**User Story**: US-001

As a developer, I want to install SpecWeave via NPM so that I can use it in my projects

## Acceptance Criteria

- [x] AC-001-01: `npm install -g specweave` works
- [x] AC-001-02: `specweave init` creates `.specweave/` structure
- [ ] AC-001-03: Version command shows current version (In Progress)

---

**Progress**: 2/3 ACs complete (67%)

🤖 Auto-updated by SpecWeave (2025-11-11)
```

### 3. Spec Completion (Close Project)

**Trigger**: All user stories in spec are complete

**Actions**:
1. Close all GitHub Issues (user stories)
2. Archive GitHub Project
3. Post final comment:
   ```markdown
   ✅ **Spec Completed**

   **Final Stats**:
   - 35 user stories completed (100%)
   - 4 increments implemented (0001, 0002, 0004, 0005)
   - Duration: 6 weeks

   **Deliverables**:
   - Core framework architecture
   - Plugin system
   - Cross-platform CLI

   Spec complete. Project archived.

   ---
   🤖 Auto-closed by SpecWeave
   ```

### 4. GitHub Project → Spec (Import)

**Use Case**: Import existing GitHub Projects as SpecWeave specs

**Command**: `/sw-github:import-project <project-number>`

**Actions**:
1. Fetch project via GitHub GraphQL API
2. Create spec structure:
   - Parse project title → spec title
   - Parse project body → spec overview
   - Map issues → user stories
   - Map labels → priority

3. Generate spec.md with user stories and acceptance criteria
4. Link project to spec in metadata

---

## Configuration

Configure GitHub sync in `.specweave/config.json`:

```json
{
  "plugins": {
    "enabled": ["specweave-github"],
    "settings": {
      "specweave-github": {
        "repo": "owner/repo",
        "autoSyncSpecs": true,
        "syncDirection": "two-way",
        "defaultLabels": ["specweave", "spec"],
        "syncFrequency": "on-change"
      }
    }
  }
}
```

---

## GitHub CLI Requirements

This skill requires GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install GitHub CLI
brew install gh              # macOS
sudo apt install gh          # Ubuntu
choco install gh             # Windows

# Authenticate
gh auth login

# Verify
gh auth status
```

---

## Manual Sync Operations

### Sync Spec to GitHub

```bash
/sw-github:sync-spec spec-001
```

Creates or updates GitHub Project for spec-001.

### Sync All Specs

```bash
/sw-github:sync-spec --all
```

Syncs all specs to GitHub Projects.

### Import Project

```bash
/sw-github:import-project 123
```

Imports GitHub Project #123 as a SpecWeave spec.

### Check Status

```bash
/sw-github:status spec-001
```

Shows sync status (project ID, last sync time, progress %).

---

## Workflow Integration

### Full Automated Workflow

```bash
# 1. Create spec (PM agent)
User: "Create spec for user authentication"
PM: Creates .specweave/docs/internal/specs/spec-005-user-auth.md

# 2. Auto-sync to GitHub (hook)
→ GitHub Project created automatically
→ Issues created for each user story

# 3. Implement increments
/sw:increment "Add login flow"
→ Increment 0010 created (implements US-001, US-002)

# 4. Work on tasks
/sw:do
→ Task completed
→ Hook fires
→ Spec updated (AC marked complete)
→ GitHub Project updated automatically

# 5. Complete spec
→ All user stories done
→ GitHub Project archived automatically
```

### Team Collaboration

**For Developers**:
- Work in SpecWeave specs locally
- Automatic GitHub Project updates keep team informed
- No manual project management needed

**For Project Managers**:
- View all specs as GitHub Projects
- Track progress in GitHub Projects UI
- Comment on issues to communicate with developers

**For Stakeholders**:
- See progress in familiar GitHub interface
- No need to understand SpecWeave structure
- Clear visibility into feature development status

---

## Conflict Resolution

**What if project and spec diverge?**

The spec is always the source of truth. GitHub Projects are a mirror for visibility.

**Sync conflicts** (rare):
1. Spec status conflicts with project state
2. Manual edits to project/issue body/title

**Resolution**:
- Run `/sw-github:sync-spec spec-001 --force` to overwrite project from spec
- Or manually update spec metadata to match project

---

## Privacy & Security

**What gets synced?**
- ✅ Spec title, overview, progress
- ✅ User stories and acceptance criteria
- ✅ User story completion status
- ❌ Code diffs, file contents (never synced)
- ❌ Internal notes, sensitive data

**Security**:
- Uses GitHub token from environment (GITHUB_TOKEN or GH_TOKEN)
- Respects repository permissions (read/write)
- No data sent to third parties

---

## Benefits

**For SpecWeave Users**:
- ✅ No manual GitHub project management
- ✅ Automatic team visibility
- ✅ Single source of truth (spec docs)
- ✅ GitHub integration without leaving IDE

**For Teams**:
- ✅ Track SpecWeave work in GitHub Projects
- ✅ Use milestones, labels, assignees as usual
- ✅ Comment on issues to communicate with developers
- ✅ View progress in real-time

**For Organizations**:
- ✅ Unified project tracking across repos
- ✅ GitHub-native workflow (familiar to all)
- ✅ Audit trail (all syncs timestamped)
- ✅ Integration with GitHub Actions, webhooks

---

## Troubleshooting

**Project not created?**
- Check GitHub CLI: `gh auth status`
- Verify repo permissions (write access)
- Check config: `.specweave/config.json`

**Sync failing?**
- Check network connectivity
- Verify project still exists (not deleted)
- Check rate limits: `gh api rate_limit`

**Progress not updating?**
- Check `autoSyncSpecs: true` in config
- Verify hook execution: `.specweave/logs/hooks-debug.log`
- Manually sync: `/sw-github:sync-spec spec-001`

---

## Advanced Usage

### Custom Project Templates

Create `.specweave/github/project-template.md`:

```markdown
# [{{spec.id.toUpperCase()}}] {{spec.title}}

{{spec.overview}}

## SpecWeave Details

- **Spec**: [spec.md]({{spec.url}})
- **Priority**: {{spec.priority}}
- **Feature Area**: {{spec.featureArea}}

## User Stories

{{spec.userStories.map(us => `- ${us.id}: ${us.title}`).join('\n')}}
```

### Selective Sync

Sync only specific specs:

```json
{
  "plugins": {
    "settings": {
      "specweave-github": {
        "syncSpecs": [
          "spec-001-core-framework",
          "spec-005-user-authentication"
        ]
      }
    }
  }
}
```

### Multi-Repo Sync

For monorepos with multiple GitHub repositories:

```json
{
  "plugins": {
    "settings": {
      "specweave-github": {
        "repos": {
          "frontend": {
            "repo": "myorg/frontend",
            "specs": ["spec-001-*", "spec-002-*"]
          },
          "backend": {
            "repo": "myorg/backend",
            "specs": ["spec-003-*", "spec-004-*"]
          }
        }
      }
    }
  }
}
```

---

## Related

- **github-issue-tracker**: Track individual tasks as issue comments (DEPRECATED - use spec sync instead)
- **github-manager agent**: AI agent for GitHub operations
- **Commands**: `/sw-github:sync-spec`, `/sw-github:import-project`, `/sw-github:status`

---

**Version**: 2.0.0 (Spec-based architecture)
**Plugin**: specweave-github
**Last Updated**: 2025-11-11
