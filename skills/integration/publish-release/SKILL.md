---
name: publish-release
version: 1.2.0
date: 2026-01-20
description: Publish a new release to GitHub Packages. Use when ready to release, after tests pass and version is updated. Creates git tag and pushes to trigger GitHub Actions.
canonical_repo: https://github.com/stoicstudio/ClaudeSkills
canonical_path: skills/publish-release/SKILL.md
---

# publish-release

Publishes a new release to GitHub Packages via GitHub Actions.

> **Canonical Source**: This skill is maintained at [stoicstudio/ClaudeSkills](https://github.com/stoicstudio/ClaudeSkills).
> Run `/update-skill publish-release` or see [Updating This Skill](#updating-this-skill) below.

## Prerequisites

Before running, ensure:
1. All code changes are complete
2. `dotnet test` passes
3. `VersionInfo.cs` has been updated with new version number
4. `CHANGELOG.md` has been updated with release notes
5. _PROJECT_NAME_ is determined for the current project

## Steps

1. **Read current version info** from `src/_PROJECT_NAME_/VersionInfo.cs`:
   - Extract `Version` (e.g., "1.3.0")
   - Extract `VersionName` (e.g., "Agent Adoption Guidance")

2. **Check git status** to see what files have changed

3. **Stage all changes**:
   ```bash
   git add -A
   ```

4. **Create commit** with version in message (use HEREDOC for proper formatting):
   ```bash
   git commit -m "$(cat <<'EOF'
   v{Version}: {VersionName}

   {Brief summary of changes from CHANGELOG.md}

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

5. **Create git tag**:
   ```bash
   git tag v{Version}
   ```

6. **Push to origin** (triggers GitHub Actions NuGet publish):
   ```bash
   git push origin master --tags
   ```

7. **Announce completion**: "As Above, so Below" - the local changes now manifest in the remote repository.

## Workflow Monitoring

After push, monitor the GitHub Actions workflow until completion:

1. **Determine check interval** by querying the last successful workflow duration:
   ```bash
   gh run list --repo {owner}/{repo} --status success --limit 5 --json databaseId,updatedAt,createdAt
   ```
   - Calculate average duration from recent successful runs
   - Use `duration / 3` as the check interval (minimum 30 seconds, maximum 2 minutes)
   - If no previous runs, default to 1 minute interval

2. **Get the triggered workflow run ID**:
   ```bash
   gh run list --repo {owner}/{repo} --limit 1 --json databaseId,status,conclusion,headBranch
   ```
   - Verify the run is for the correct tag/branch (v{Version})

3. **Poll workflow status** at the calculated interval:
   ```bash
   gh run view {run_id} --repo {owner}/{repo} --json status,conclusion
   ```
   - Continue polling while `status` is `queued`, `in_progress`, or `waiting`
   - Stop when `status` is `completed`

4. **Report final result**:
   - If `conclusion` is `success`: Report success with package availability
   - If `conclusion` is `failure`: Report failure and provide link to logs:
     ```bash
     gh run view {run_id} --repo {owner}/{repo} --web
     ```

## Post-Release

After workflow completes successfully:
1. Package will be available at: https://github.com/{owner}/{repo}/packages
2. Users can update with: `dotnet tool update --global {package-name}`

---

## Updating This Skill

This skill is distributed from the canonical repository. To update your local copy:

### Manual Update

```bash
# From your project root
curl -sL https://raw.githubusercontent.com/stoicstudio/ClaudeSkills/main/skills/publish-release/SKILL.md \
  -o .claude/skills/publish-release/SKILL.md
```

### Check for Updates

Compare your local version with canonical:
```bash
# Get canonical version
curl -sL https://raw.githubusercontent.com/stoicstudio/ClaudeSkills/main/skills/publish-release/SKILL.md | head -5

# Check local version
head -5 .claude/skills/publish-release/SKILL.md
```

### Bulk Update (All Projects)

Use the sync script from the canonical repo:
```bash
# Clone or update ClaudeSkills repo
cd /path/to/ClaudeSkills
git pull

# Run sync to update all configured projects
./sync.sh
```
