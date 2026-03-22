---
name: af-commit-agentflow-changes
description: Commit AgentFlow framework changes with proper CHANGELOG updates and version bumping. Use when editing framework files in the source repository or consumer projects, syncing changes, or pushing updates.

# AgentFlow documentation fields
title: Making AgentFlow Changes
created: 2026-01-03
updated: 2026-02-06
last_validated: 2026-02-09
last_checked: 2026-02-09
tags: [skill, expertise, framework, contribution, sync, versioning]
parent: ../README.md
---

# Making AgentFlow Changes

## When to Use This Skill

Load this skill when you need to:
- Edit AgentFlow framework files in the source repository (`/srv/worktrees/agentflow/main/`)
- Fix or improve AgentFlow framework files (agents, skills, docs, scripts)
- Contribute changes from a consumer project back to AgentFlow
- Update the CHANGELOG and manage versions
- Understand the "edit in client, sync back" workflow
- Commit any changes to `.claude/` or `.agentflow/` directories

## Rules (FOLLOW THESE)

### Contribution Rules
1. **MUST** make framework changes in the AgentFlow worktree (`/srv/worktrees/agentflow/main/`)
2. **MUST** update CHANGELOG.md under `[Unreleased]` for every change
3. **MUST** follow Keep a Changelog format (Added, Changed, Fixed, Removed, Deprecated, Security)
4. **SHOULD** test changes in a consumer project before committing to AgentFlow
5. **MUST** run `/af:push` after committing to distribute changes to all consumer worktrees

### Commit Rules
6. **MUST** use conventional commit format: `type(scope): description`
7. **MUST** include `framework:` or `af:` in scope for framework changes
8. **SHOULD** reference the consumer project that discovered the issue
9. **MUST NOT** commit directly to consumer projects' framework files

### File Location Rules
10. **AgentFlow source**: `/srv/worktrees/agentflow/main/`
11. **Consumer projects**: `/srv/worktrees/{project}/main/` or `/data/worktrees/{project}/{branch}/`
12. **MUST** edit in AgentFlow source, then sync to consumers

### Version Bump Rules (Periodic, Not Per-Change)
13. Version bumps are **optional** - do them monthly or for breaking changes
14. **PATCH** (x.x.1) - Bug fixes, typo corrections, minor doc updates
15. **MINOR** (x.1.0) - New features, new skills/agents, non-breaking improvements
16. **MAJOR** (1.0.0) - Breaking changes, architecture changes, removed features

---

## What Gets Synced vs Preserved

Understanding which files are synced from AgentFlow is critical. **Synced files will be overwritten** on the next `/af:sync` - any local changes will be lost.

### Synced (Overwritten on Sync)

These files come from AgentFlow and **MUST be edited in `/srv/worktrees/agentflow/main/`**:

| Path Pattern | Description |
|--------------|-------------|
| `.claude/agents/af-*.md` | Framework agents (af- prefix) |
| `.claude/skills/af-*/` | Framework skills (af- prefix, includes orchestration) |
| `.claude/commands/**/*.md` | All command documentation |
| `.claude/docs/**/*.md` | Framework documentation |
| `.claude/scripts/**/*` | All scripts (sync, validation, etc.) |
| `.claude/templates/**/*` | Setup and hook templates |
| `.claude/hooks/**/*` | Hook scripts |
| `.claude/lib/**/*` | Shared libraries |
| `.claude/settings.json` | Framework settings (hooks merged) |
| `.claude/CLAUDE-agentflow.md` | Framework instructions |
| `.claude/README.md` | Framework README |

### Preserved (Safe to Edit Locally)

These files are **never touched by sync** - edit them directly in your project:

| Path Pattern | Description |
|--------------|-------------|
| `CLAUDE.md` | Project root instructions |
| `.claude/work/**` | Session work files |
| `.claude/plans/**` | Planning documents |
| `.claude/logs/**` | Agent logs |
| `.claude/reports/**` | Generated reports |
| `.claude/.sync/**` | Sync state tracking |
| `.claude/settings.local.json` | Project setting overrides |
| `.claude/**/*.local.*` | Any `.local.` suffixed files |
| `.claude/**/current-*.md` | Current session files |
| `.claude/agents/{project}-*.md` | Project agents (no af- prefix) |
| `.claude/skills/{project}-*/` | Project skills (no af- prefix) |

### Quick Rule

> **`af-` prefix = Framework owned = Edit in AgentFlow source**
> **No `af-` prefix = Project owned = Edit locally**

---

## Workflows

### Workflow: Edit in Client, Sync Back

**When:** You discover a framework issue or improvement while working in a consumer project

**Steps:**
1. **Identify the change** in the consumer project (e.g., stale doc, bug, missing feature)
2. **Switch to AgentFlow worktree:**
   ```bash
   cd /srv/worktrees/agentflow/main
   ```
3. **Make the change** to the framework file(s)
4. **Update CHANGELOG.md** under `[Unreleased]`:
   ```markdown
   ## [Unreleased]

   ### Fixed
   - **Stale BDD Guide** - Removed outdated Gherkin documentation that conflicted with V2 Markdown scenario approach
   ```
5. **Commit the change:**
   ```bash
   git add .
   git commit -m "fix(af:docs): remove stale bdd-guide.md

   Gherkin was deprecated in V2 in favor of Markdown scenarios.
   The old guide was causing confusion in docs audits.

   Discovered in: XTL project"
   ```
6. **Push to AgentFlow remote** (if applicable)
7. **Preview broadcast** — read `CHANGELOG.md` [Unreleased] section and present to the user:
   ```
   These changes will be broadcast to all projects:

   Fixed:
   - Stale BDD Guide
   Changed:
   - BDD Agent output format
   Added:
   - Making AgentFlow Changes Skill

   Last release: v3.1.0 (2026-01-26)
   Suggestion: v3.2.0 (minor — new features added)

   Bump version before pushing? [yes / no / custom version]
   ```
   **STOP and wait for the user's decision.**
8. **If version bump approved:**
   - Move [Unreleased] entries to new version section in CHANGELOG.md
   - Add empty [Unreleased] section
   - Update `version` in `template-manifest.json`
   - Commit: `chore(af:release): v{VERSION}`
   - Tag: `git tag v{VERSION}`

   **If no version bump:** Skip to step 9.
9. **Push to all consumer worktrees:**
   ```bash
   npx ts-node .claude/scripts/sync/push-to-projects.ts
   ```
   This syncs to all worktrees across all projects and auto-commits the changes.
10. **Broadcast to Zulip** — read `.claude/work/push-notifications.jsonl` and post one message per project stream on Zulip. The notification includes the CHANGELOG summary (see Zulip Notification section below).

**Success criteria:**
- Change is in AgentFlow source (not just consumer)
- CHANGELOG updated
- User chose whether to version bump (or not)
- All consumer worktrees synced via `/af:push`
- Teams notified via Zulip

> **Note:** `/af:sync` is still available for ad-hoc use (e.g., syncing a newly created branch that `/af:push` hasn't seen yet).

---

### Workflow: Version Bump and Release (Optional/Periodic)

**When:** Monthly, or when making breaking changes. Not required for every change.

**Steps:**
1. **Review [Unreleased] section** in CHANGELOG.md
2. **Determine version bump type:**
   - Bug fixes only → PATCH (2.1.0 → 2.1.1)
   - New features → MINOR (2.1.0 → 2.2.0)
   - Breaking changes → MAJOR (2.1.0 → 3.0.0)
3. **Update CHANGELOG.md:**
   ```markdown
   ## [Unreleased]

   _No unreleased changes_

   ---

   ## [2.2.0] - 2026-01-03

   ### Added
   - **Making AgentFlow Changes Skill** - Documents contribution workflow

   ### Fixed
   - **Stale BDD Guide** - Removed outdated Gherkin documentation
   ```
4. **Update version in template-manifest.json**:
   ```json
   {
     "version": "2.2.0"
   }
   ```
5. **Commit the release:**
   ```bash
   git add CHANGELOG.md template-manifest.json
   git commit -m "chore(af:release): v2.2.0"
   git tag v2.2.0
   ```
6. **Push with tags:**
   ```bash
   git push && git push --tags
   ```

---

### Workflow: Fixing Stale Documentation

**When:** Documentation doesn't match current implementation

**Steps:**
1. **Identify the stale doc** (e.g., audit finds outdated guide)
2. **Determine action:**
   - Doc still relevant but outdated → **Update it**
   - Doc describes deprecated approach → **Delete it**
   - Doc partially correct → **Edit specific sections**
3. **Switch to AgentFlow worktree:**
   ```bash
   cd /srv/worktrees/agentflow/main
   ```
4. **Make the fix:**
   - If deleting: `git rm .claude/docs/guides/stale-guide.md`
   - If updating: Edit the file with correct information
5. **Update parent README** if file was deleted (remove from children array)
6. **Update CHANGELOG:**
   ```markdown
   ### Fixed
   - **Stale {Guide Name}** - {Brief description of fix}
   ```
   OR
   ```markdown
   ### Removed
   - **{Guide Name}** - Deprecated in V2, replaced by {new approach}
   ```
7. **Commit and sync** (per Workflow: Edit in Client, Sync Back)

---

### Workflow: Adding New Framework Component

**When:** Creating a new agent, skill, command, or doc

**Steps:**
1. **Switch to AgentFlow worktree**
2. **Load af-modify-agentflow skill** for templates and standards
3. **Create the component** following namespace rules (`af-` prefix)
4. **Update parent README** with new child reference
5. **Update CHANGELOG:**
   ```markdown
   ### Added
   - **{Component Name}** in `{location}`
     - {Bullet point describing what it does}
     - {Another bullet if needed}
   ```
6. **Test the component** in a consumer project if possible
7. **Commit with descriptive message:**
   ```bash
   git commit -m "feat(af:skills): add af-commit-agentflow-changes skill

   Documents the contribution workflow for editing framework
   files in consumer projects and syncing back.

   - Covers version bumping rules
   - Covers CHANGELOG format
   - Covers commit standards"
   ```

---

## Examples

### Good CHANGELOG Entry

```markdown
## [2.2.0] - 2026-01-03

### Added
- **Making AgentFlow Changes Skill** (`af-commit-agentflow-changes`)
  - Documents "edit in client, sync back" workflow
  - Covers version bumping and CHANGELOG standards
  - Includes commit message conventions

### Fixed
- **Stale BDD Guide** - Removed `.claude/docs/guides/bdd-guide.md` which documented deprecated Gherkin approach (V2 uses Markdown scenarios)

### Changed
- **BDD Agent** - Updated to clarify V2 Markdown scenario output format
```

### Good Commit Messages

```bash
# Feature addition
git commit -m "feat(af:skills): add email testing patterns to af-configure-test-frameworks"

# Bug fix
git commit -m "fix(af:docs): remove stale bdd-guide.md

Gherkin deprecated in V2, guide was causing audit confusion.
Discovered in: XTL project"

# Documentation update
git commit -m "docs(af:guides): update framework-sync with contribution workflow"

# Breaking change
git commit -m "feat(af:agents)!: rename af-search-agent to af-web-search-agent

BREAKING CHANGE: Agent name changed, update Task tool invocations"
```

### Bad Practices

```markdown
# Bad: No context
### Fixed
- Fixed a bug

# Bad: Not using Keep a Changelog categories
### Updates
- Made some changes to the BDD stuff

# Bad: Mixing concerns
### Added
- New skill and also fixed that doc and changed some things
```

---

## Zulip Notification

After running `/af:push`, the push script generates notification entries in `.claude/work/push-notifications.jsonl`. Post **one message per project stream** on Zulip using the bot credentials.

**Notification format** (one per project channel):
```
:arrows_counterclockwise: AgentFlow v{VERSION} pushed to {PROJECT}

What changed:
- {Bold headline from each CHANGELOG entry}
- {Another entry}

Changes auto-committed. Run `git log -1` in any worktree to review.
```

The push script automatically extracts the CHANGELOG summary. Read the entries from `.claude/work/push-notifications.jsonl` and post each one to its `channelId`.

**For breaking changes, also announce to `#engineering-team`** on Zulip:
```
:warning: AgentFlow v{VERSION} pushed - BREAKING CHANGE

{description of breaking change and required action}

All worktrees have been updated automatically.
```

> **Note:** `/af:sync` is still available for projects to manually pull updates (e.g., for newly created branches).

---

## Essential Reading

**Related skills:**
- [AgentFlow Framework Development](../af-modify-agentflow/SKILL.md) - Creating components

**Sync documentation:**
- [Framework Sync Guide](../../docs/guides/framework-sync.md) - How sync works
- [/af:push Command](../../commands/af/push.md) - Push distribution command
- [/af:sync Command](../../commands/af/sync.md) - Pull sync command (ad-hoc use)

**Standards:**
- [Keep a Changelog](https://keepachangelog.com/) - CHANGELOG format
- [Semantic Versioning](https://semver.org/) - Version numbering
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit format

---

**Remember:**
1. Always edit in AgentFlow source, not consumer projects
2. Always update CHANGELOG under [Unreleased]
3. After committing, preview the CHANGELOG and ask the user about version bumping before pushing
4. Always run `/af:push` after committing to distribute to all worktrees
5. Post one Zulip notification per project stream with CHANGELOG summary
6. Push works on any branch - feature branches are fine
7. Version bumps are optional - do them monthly or for breaking changes
8. `/af:sync` still works for ad-hoc pull (new branches, targeted sync)
