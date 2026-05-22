---
name: external-sync-wizard
description: Expert guide for setting up bidirectional sync between SpecWeave and GitHub Issues, JIRA, or Azure DevOps. Use when configuring external tool integration, mapping fields between systems, or troubleshooting sync issues. Covers webhook setup, authentication, and conflict resolution strategies.
---

# External Sync Wizard Expert

I'm a specialist in configuring synchronization between SpecWeave (your local source of truth) and external project management tools like GitHub Issues, Jira, and Azure DevOps.

## When to Use This Skill

Ask me when you need help with:
- **Setting up GitHub Issues sync** with SpecWeave increments
- **Configuring Jira Epic** integration
- **Azure DevOps Work Items** synchronization
- **Choosing sync direction** (bidirectional, export, import, manual)
- **Understanding sync architecture** and source of truth principles
- **Troubleshooting sync issues** or conflicts
- **Migrating from external tools** to SpecWeave

## My Expertise

### SpecWeave's Sync Architecture

**Critical Understanding**: `.specweave/docs/specs/` is the **permanent, local source of truth**. External tools (GitHub, Jira, ADO) are **MIRRORS** of this truth.

#### Correct Sync Direction

```
✅ CORRECT Architecture:
.specweave/docs/specs/  ↔  GitHub Issues
.specweave/docs/specs/  ↔  Jira Epics
.specweave/docs/specs/  ↔  Azure DevOps Work Items

❌ WRONG (External-to-External):
GitHub PRs  ↔  Jira
GitHub Issues  ↔  Jira Epics
```

**The Hub is LOCAL**, not external!

### Sync Direction Options

When setting up sync, users choose from 4 options:

| Option | Direction | Description | Use Case |
|--------|-----------|-------------|----------|
| **Bidirectional** | Local ↔ External | Changes sync **both ways** | Team collaboration (recommended) |
| **Export only** | Local → External | Push **from Local to External** | SpecWeave is source of truth |
| **Import only** | External → Local | Pull **from External to Local** | Onboarding existing projects |
| **Manual sync** | On-demand | No auto-sync, use commands manually | Testing, one-off syncs |

**Default recommendation**: **Bidirectional** (most useful for teams)

---

## Interactive Setup Wizards

### GitHub Sync Setup

#### Step 1: Authentication

**Question**: "Do you want to sync increments to GitHub Issues?"

**If YES** → Proceed to authentication setup:
- Install GitHub CLI: `brew install gh` (macOS) or equivalent
- Authenticate: `gh auth login`
- Select repository: `gh repo set-default`

**If NO** → Skip GitHub sync setup

#### Step 2: Sync Direction

**CRITICAL**: The prompt MUST say "between local increments and GitHub", NOT "between GitHub and Jira"!

**Question**:
```
"What should be the sync behavior between local increments (.specweave/) and GitHub Issues?"
```

**Options**:

**1. Bidirectional sync (Recommended)**
```
Local increments ↔ GitHub Issues

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only (completed/abandoned not auto-synced)
- Example: Complete task in SpecWeave → GitHub issue updates with progress

Best for: Teams using both SpecWeave and GitHub for project tracking
```

**2. Export only (Local → GitHub)**
```
Local increments → GitHub Issues

Features:
- SpecWeave is source of truth, GitHub is read-only mirror
- Changes push from local to GitHub only
- GitHub changes are ignored (must update locally)
- Example: Create increment in SpecWeave → GitHub issue created automatically

Best for: Solo developers who prefer SpecWeave but want GitHub visibility
```

**3. Import only (GitHub → Local)**
```
GitHub Issues → Local increments

Features:
- GitHub is source of truth, local workspace mirrors it
- Changes pull from GitHub to local only
- Good for: Onboarding existing GitHub projects
- Example: Close GitHub issue → Local increment status updates

Best for: Migrating from GitHub-first workflow to SpecWeave
```

**4. Manual sync only**
```
Use /sw-github:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens
- Good for: Testing, one-off syncs, experimental increments

Best for: Advanced users who want explicit control
```

**Visual Aid** (include in prompt):
```
✅ CORRECT Architecture:
Local (.specweave/) ↔ GitHub Issues

❌ WRONG:
GitHub ↔ Jira
```

#### Step 3: Auto-Create Issues

**Question**: "Should SpecWeave auto-create GitHub issues when planning increments?"

**Options**:

**1. Yes, auto-create (Recommended)**
```
Every /sw:increment creates a GitHub issue automatically

Benefits:
- Immediate team visibility
- Bidirectional sync works from day 1
- Zero manual work
- Links: spec.md, plan.md, tasks.md included in issue

Best for: Teams that want automatic GitHub integration
```

**2. No, manual creation**
```
Use /sw-github:create-issue manually when needed

Benefits:
- Create issues only for important increments
- More control over what goes to GitHub
- Good for: Experimental/internal increments

Best for: Solo developers or selective GitHub usage
```

---

### Jira Sync Setup

#### Step 1: Authentication

**Question**: "Do you want to sync increments to Jira Epics?"

**If YES** → Proceed to authentication setup:
- Jira domain: `your-company.atlassian.net`
- API token: Generate from Jira settings
- Email: Your Jira account email
- Project key: `PROJ` (e.g., `AUTH`, `PAY`, `INFRA`)

**If NO** → Skip Jira sync setup

#### Step 2: Sync Direction

**Question**:
```
"What should be the sync behavior between local increments (.specweave/) and Jira Epics?"
```

**Options**:

**1. Bidirectional sync (Recommended)**
```
Local increments ↔ Jira Epics

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only
- Example: Complete task in SpecWeave → Jira epic status updates

Best for: Teams using both SpecWeave and Jira for project management
```

**2. Export only (Local → Jira)**
```
Local increments → Jira Epics

Features:
- SpecWeave is source of truth, Jira is read-only mirror
- Changes push from local to Jira only
- Jira changes are ignored (must update locally)
- Example: Create increment in SpecWeave → Jira epic created automatically

Best for: Developers who prefer SpecWeave but need Jira reporting
```

**3. Import only (Jira → Local)**
```
Jira Epics → Local increments

Features:
- Jira is source of truth, local workspace mirrors it
- Changes pull from Jira to local only
- Good for: Onboarding existing Jira projects
- Example: Update Jira epic → Local increment syncs

Best for: Migrating from Jira-first workflow to SpecWeave
```

**4. Manual sync only**
```
Use /sw-jira:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens

Best for: Advanced users or testing scenarios
```

---

### Azure DevOps Sync Setup

#### Step 1: Authentication

**Question**: "Do you want to sync increments to Azure DevOps work items?"

**If YES** → Proceed to authentication setup:
- Organization URL: `https://dev.azure.com/your-org`
- Personal Access Token (PAT): Generate from ADO settings
- Project name: `MyProject`
- Area path: (optional) for multi-team organizations

**If NO** → Skip ADO sync setup

#### Step 2: Sync Direction

**Question**:
```
"What should be the sync behavior between local increments (.specweave/) and Azure DevOps work items?"
```

**Options**:

**1. Bidirectional sync (Recommended)**
```
Local increments ↔ ADO Work Items

Features:
- Changes sync both ways automatically (on task completion)
- Conflicts: You will be prompted to resolve when both sides change
- Scope: Active increments only
- Example: Complete task in SpecWeave → ADO work item updates

Best for: Enterprise teams using Azure DevOps
```

**2. Export only (Local → ADO)**
```
Local increments → ADO Work Items

Features:
- SpecWeave is source of truth, ADO is read-only mirror
- Changes push from local to ADO only
- ADO changes are ignored (must update locally)
- Example: Create increment in SpecWeave → ADO work item created automatically

Best for: Developers who prefer SpecWeave with ADO visibility
```

**3. Import only (ADO → Local)**
```
ADO Work Items → Local increments

Features:
- ADO is source of truth, local workspace mirrors it
- Changes pull from ADO to local only
- Good for: Onboarding existing ADO projects
- Example: Update ADO work item → Local increment syncs

Best for: Migrating from ADO-first workflow to SpecWeave
```

**4. Manual sync only**
```
Use /sw-ado:sync command when needed

Features:
- No automatic sync via hooks
- Full control over when sync happens

Best for: Advanced users or selective sync scenarios
```

---

## Implementation Notes

### When Generating Increment Planning Wizard

1. ✅ Check `config.plugins.enabled` array
2. ✅ ONLY ask about enabled plugins (GitHub/Jira/ADO)
3. ✅ For each enabled plugin, ask: "Local ↔ [Provider]" sync direction
4. ❌ NEVER ask about external-to-external sync (e.g., "GitHub ↔ Jira")

### Configuration Storage

**Secrets** (`.env` - gitignored):
```bash
# GitHub
GITHUB_TOKEN=ghp_xxx

# Jira
JIRA_API_TOKEN=xxx
JIRA_EMAIL=user@example.com

# Azure DevOps
ADO_PAT=xxx
```

**Configuration** (`.specweave/config.json` - committed to git):
```json
{
  "plugins": {
    "enabled": ["github", "jira", "ado"]
  },
  "sync": {
    "github": {
      "enabled": true,
      "direction": "bidirectional",
      "autoCreateIssue": true,
      "repo": "owner/repo"
    },
    "jira": {
      "enabled": true,
      "direction": "bidirectional",
      "domain": "company.atlassian.net",
      "projectKey": "PROJ"
    },
    "ado": {
      "enabled": true,
      "direction": "export-only",
      "organization": "your-org",
      "project": "MyProject"
    }
  }
}
```

---

## Sync Workflows

### Bidirectional Sync (Automatic)

**Trigger**: Task completion hook (`post-task-completion.sh`)

**Flow**:
1. User completes task in SpecWeave → `tasks.md` updated
2. Hook detects change → Reads increment metadata
3. If GitHub enabled → Updates GitHub issue with progress
4. If Jira enabled → Updates Jira epic status
5. If ADO enabled → Updates ADO work item

**Conflict Resolution**:
- If both local and external changed → Prompt user to resolve
- Show diff: Local changes vs External changes
- User chooses: Keep local, Keep external, or Merge

### Export-Only Sync

**Trigger**: Task completion hook

**Flow**:
1. User completes task in SpecWeave
2. Hook pushes changes to external tool
3. External tool changes are ignored (one-way flow)

**Use Case**: SpecWeave is the authoritative source, external tools are read-only mirrors

### Import-Only Sync

**Trigger**: Manual `/specweave-[tool]:sync` command

**Flow**:
1. User runs sync command
2. Fetch changes from external tool
3. Update local increments with external data
4. Local changes are NOT pushed (one-way flow)

**Use Case**: Onboarding existing projects from external tools

### Manual Sync

**Trigger**: Explicit command

**Flow**:
1. User runs `/sw-github:sync [increment-id]`
2. Choose direction: pull, push, or bidirectional
3. Execute sync operation
4. Report results to user

**Use Case**: Testing, one-off syncs, advanced control

---

## Common Questions

### Q: What happens if I have GitHub and Jira both enabled?

**A**: SpecWeave syncs to BOTH independently:
```
.specweave/docs/specs/ ↔ GitHub Issues
.specweave/docs/specs/ ↔ Jira Epics
```

GitHub and Jira do NOT sync with each other. SpecWeave is the hub.

### Q: Can I change sync direction later?

**A**: Yes! Edit `.specweave/config.json`:
```json
{
  "sync": {
    "github": {
      "direction": "export-only"  // Change from bidirectional
    }
  }
}
```

### Q: What if I delete a GitHub issue manually?

**A**: Depends on sync direction:
- **Bidirectional**: SpecWeave increment marked as deleted (soft delete)
- **Export-only**: GitHub issue recreated on next sync
- **Import-only**: Local increment deleted
- **Manual**: No effect until manual sync

### Q: How do I onboard an existing GitHub project?

**A**:
1. Set sync direction: **Import-only**
2. Run: `/sw-github:import-all`
3. SpecWeave creates increments from GitHub issues
4. Review and adjust as needed
5. Switch to **Bidirectional** when ready

### Q: Can I sync only specific increments?

**A**: Yes! Use manual sync:
```bash
/sw-github:sync 0042-auth-feature  # Sync specific increment
```

Auto-sync only affects **active** increments (not completed/abandoned).

---

## Troubleshooting

### Issue: GitHub issue not created after `/sw:increment`

**Diagnosis**:
1. Check GitHub CLI: `gh auth status`
2. Check config: `.specweave/config.json` → `sync.github.autoCreateIssue: true`
3. Check metadata: `.specweave/increments/####/metadata.json` has `github` section

**Fix**:
```bash
# Manual creation
/sw-github:create-issue 0042-auth-feature
```

### Issue: Jira epic not updating

**Diagnosis**:
1. Check Jira credentials in `.env`
2. Check Jira domain and project key in `config.json`
3. Check sync direction (must be bidirectional or export-only)
4. Check hook logs: `.specweave/logs/sync-*.log`

**Fix**:
```bash
# Manual sync
/sw-jira:sync 0042-auth-feature --force
```

### Issue: Conflict during bidirectional sync

**Diagnosis**:
- Both local and external modified the same field (e.g., status)

**Resolution Options**:
1. **Keep local**: Local changes overwrite external
2. **Keep external**: External changes overwrite local
3. **Merge**: Apply both changes (manual resolution)

**Example**:
```
⚠️  Conflict detected for increment 0042-auth-feature

Field: status
Local value: in-progress
GitHub value: completed

Choose resolution:
1. Keep local (in-progress)
2. Keep external (completed)
3. Merge manually

Your choice:
```

---

## Best Practices

### 1. Start with Bidirectional

Most teams benefit from bidirectional sync:
- Developers update in SpecWeave
- PMs/stakeholders track progress in GitHub/Jira
- Changes sync automatically

### 2. Use Export-Only for Solo Projects

If you're working alone and just need GitHub visibility:
- Set direction: export-only
- SpecWeave is your source of truth
- GitHub is a read-only mirror

### 3. Import-Only for Onboarding

When migrating from GitHub/Jira to SpecWeave:
1. Start with import-only
2. Pull all existing work into SpecWeave
3. Review and clean up
4. Switch to bidirectional once confident

### 4. Manual Sync for Testing

When experimenting or testing:
- Disable auto-sync
- Use manual commands
- Verify behavior before enabling auto-sync

### 5. One Source of Truth

**Golden Rule**: Never manually edit the same field in both SpecWeave and external tool simultaneously.

**Example**:
- ❌ WRONG: Update task status in SpecWeave AND GitHub manually
- ✅ CORRECT: Update in SpecWeave, let sync propagate to GitHub

---

## Related Slash Commands

### GitHub
- `/sw-github:sync [increment-id]` - Manual sync
- `/sw-github:create-issue [increment-id]` - Create issue
- `/sw-github:close-issue [increment-id]` - Close issue
- `/sw-github:import-all` - Import all GitHub issues
- `/sw-github:status [increment-id]` - Check sync status

### Jira
- `/sw-jira:sync [increment-id]` - Manual sync
- `/sw-jira:create-epic [increment-id]` - Create epic
- `/sw-jira:import-all` - Import all Jira epics
- `/sw-jira:status [increment-id]` - Check sync status

### Azure DevOps
- `/sw-ado:sync [increment-id]` - Manual sync
- `/sw-ado:create-workitem [increment-id]` - Create work item
- `/sw-ado:import-all` - Import all ADO work items
- `/sw-ado:status [increment-id]` - Check sync status

---

**Remember**: SpecWeave is your local source of truth. External tools are mirrors. Sync is about keeping mirrors up-to-date, not managing dual sources of truth.

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/external-sync-wizard.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.

