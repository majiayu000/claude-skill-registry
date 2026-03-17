---
name: nav-upgrade
description: Automates Navigator plugin updates. Detects current version, updates plugin, verifies installation, updates project CLAUDE.md, and validates new features. Auto-invoke when user mentions upgrading Navigator or getting new features.
allowed-tools: Bash, Read, Write, Edit, TodoWrite
version: 1.0.0
---

# Navigator Upgrade Skill

Automate Navigator plugin updates with version detection, conflict resolution, and post-update validation.

## When to Invoke

Auto-invoke when user says:
- "Update Navigator"
- "Upgrade Navigator plugin"
- "Get latest Navigator version"
- "Update to Navigator v3.3.0"
- "Install new Navigator features"
- "Check for Navigator updates"

## What This Does

**6-Step Workflow**:
1. **Version Detection**: Check current Navigator version vs latest
2. **Plugin Update**: Execute `/plugin update navigator`
3. **Verification**: Confirm update succeeded
4. **CLAUDE.md Update**: Update project configuration (via nav-update-claude)
5. **Hooks Setup**: Install/update token monitoring hooks in project
6. **Feature Discovery**: Show new features available

**Time Savings**: Manual update (10-15 min) → Automated (2 min)

---

## Prerequisites

- Navigator plugin installed
- Project initialized with Navigator
- Internet connection for plugin update

---

## Workflow Protocol

### Step 1: Version Detection

**Execute**: `version_detector.py`

**Check both stable and pre-release versions**:
```bash
# Current installed version
grep '"version"' .claude-plugin/plugin.json

# Get all releases (including pre-releases)
curl -s https://api.github.com/repos/alekspetrov/navigator/releases

# Parse:
# - Latest stable (prerelease: false)
# - Latest pre-release (prerelease: true)
# - Compare with current version
```

**Output scenarios**:

**Scenario 1: Stable update available**
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.2.0",
  "latest_prerelease": null,
  "recommendation": "update_to_stable"
}
```

**Scenario 2: Pre-release available (user on stable)**
```json
{
  "current_version": "4.0.0",
  "latest_stable": "4.0.0",
  "latest_prerelease": "4.3.0",
  "recommendation": "offer_prerelease_option"
}
```

**Present choice**:
```
✅ You're on the latest stable version (v4.0.0)

⚡ Experimental version available: v4.3.0

New in v4.3.0 (Experimental):
• Multi-Claude agentic workflows
• 30% success rate (use for simple features)
• PM integration with ticket closing

Options:
[1] Stay on stable v4.0.0 (recommended)
[2] Try experimental v4.3.0 (early adopter)

Your choice [1-2]:
```

**Scenario 3: Already on latest (stable or pre-release)**
```
✅ You're on v4.3.0 (latest experimental)

Latest stable: v4.0.0
Status: You're ahead of stable (testing experimental features)

New features in your version:
- Multi-Claude workflows
- Task agents in sub-Claude phases
```

Skip to Step 5 (Feature Discovery).

**Scenario 4: On pre-release, newer stable available**
```
⚠️  You're on v4.3.0 (experimental)
Latest stable: v4.6.0

Recommendation: Update to stable v4.6.0
Experimental features from v4.3.0 are now stable.
```

---

### Step 2: Plugin Update

**Scenario-based update strategy**:

#### Scenario 2: Pre-release Available (User on Stable)

When pre-release detected, present choice using AskUserQuestion tool:

```markdown
✅ You're on latest stable version (v4.0.0)

⚡ Experimental version available: v4.3.0

New in v4.3.0 (Experimental):
• Multi-Claude agentic workflows
• 30% success rate (use for simple features)
• PM integration with ticket closing

**Question**: Which version would you like?

**Options**:
[1] **Stay on stable v4.0.0** (recommended)
    - Production-ready
    - No experimental features
    - Most reliable

[2] **Try experimental v4.3.0** (early adopter)
    - Multi-Claude workflows
    - Latest features
    - 30% completion rate
    - Help test new functionality

Your choice?
```

**If user chooses [1] (Stay stable)**:
```
✓ Staying on v4.0.0 (latest stable)

No action needed. Run nav-upgrade again when you're ready to try experimental features.
```

**If user chooses [2] (Try experimental)**:
```bash
# Uninstall current version
/plugin uninstall navigator

# Add marketplace (if not already added)
/plugin marketplace add alekspetrov/navigator

# Install specific pre-release version
# Note: /plugin update only fetches stable, must install specific version
git clone https://github.com/alekspetrov/navigator.git /tmp/navigator-v4.3.0
cd /tmp/navigator-v4.3.0
git checkout v4.3.0

# Install from local checkout
/plugin install /tmp/navigator-v4.3.0
```

**Then verify installation**:
```bash
/plugin list | grep navigator
# Should show: navigator (v4.3.0)
```

#### Scenario 1: Stable Update Available

**Execute**: `/plugin update navigator`

**Monitor output**:
```
Updating navigator...
✅ Navigator updated to v4.2.0
```

**If update fails**:
```
❌ Update failed: [error message]

Troubleshooting:
1. Restart Claude Code
2. Try: /plugin uninstall navigator && /plugin install navigator
3. Check internet connection
4. Report issue: https://github.com/alekspetrov/navigator/issues
```

**Automatic retry** (once):
If update fails, try uninstall/reinstall automatically:
```bash
/plugin uninstall navigator
/plugin marketplace add alekspetrov/navigator
/plugin install navigator
```

---

### Step 3: Verification

**Execute**: `plugin_verifier.py`

**Verify**:
1. Plugin version matches latest
2. New skills registered in plugin.json
3. Skills are invokable

**Test new skills** (v3.3.0 example):
```bash
# Test that visual-regression skill exists
ls ~/.config/claude/plugins/navigator/skills/visual-regression/SKILL.md 2>/dev/null || echo "Skill not found"
```

**Output**:
```
✅ Update Verification

Version: v3.3.0 ✅
New Skills Registered: visual-regression ✅
Skills Invokable: ✅

Update successful!
```

**If verification fails**:
```
⚠️ Update completed but verification failed

Issue: visual-regression skill not found
Fix: Restart Claude Code to reload skills

After restarting, verify:
"Set up visual regression for Button"
```

Prompt user to restart Claude Code.

---

### Step 4: Update Project CLAUDE.md (Automatic)

**After plugin update, automatically invoke**: `nav-update-claude` skill

```
🔄 Syncing project CLAUDE.md with updated plugin...

✓ Using template from GitHub (v4.3.0)
✓ Extracted customizations
✓ Generated updated CLAUDE.md
```

**What happens automatically**:
1. Detects new plugin version (e.g., v4.3.0)
2. Fetches matching template from GitHub
3. Preserves project customizations
4. Updates CLAUDE.md in current project
5. Shows diff for review

**Template sync benefits**:
- ✅ CLAUDE.md always matches installed plugin version
- ✅ No template drift (v4.0 templates with v4.3 plugin)
- ✅ Pre-release templates accessible
- ✅ Offline fallback to bundled templates

**User action required**:
```
Review changes and commit:

git add CLAUDE.md
git commit -m "chore: update CLAUDE.md to Navigator v4.3.0"
```

**See**: `nav-update-claude` skill for details.

---

### Step 5: Setup Token Monitoring Hooks

**Install or update project hooks** for token budget monitoring:

```bash
# Create .claude directory if not exists
mkdir -p .claude

# Check if settings.json exists
if [ -f ".claude/settings.json" ]; then
  # Backup existing settings
  cp .claude/settings.json .claude/settings.json.backup
  echo "✓ Backed up existing .claude/settings.json"
fi

# Write hook configuration
cat > .claude/settings.json << 'EOF'
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|Bash|Task",
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"${CLAUDE_PLUGIN_DIR}/hooks/monitor-tokens.py\"",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
EOF

echo "✓ Token monitoring hook installed"
```

**What this enables**:
- Monitors context usage after each tool call
- Warns at 70% usage, critical alert at 85%
- Suggests `/nav:compact` when approaching limits
- Prevents context crashes during long sessions

**Output**:
```
✓ Token monitoring hook installed

New in v4.6.0:
  - Automatic context budget monitoring
  - Warns before you hit context limits
  - Suggests compact at optimal times
```

---

### Step 6: Post-Upgrade Setup Check

**Check if new features require setup**:

```bash
# Check for skills with setup requirements
if [ -f "$NAVIGATOR_PATH/skills/product-design/setup.sh" ]; then
  # Check if venv exists
  if [ ! -d "$NAVIGATOR_PATH/skills/product-design/venv" ]; then
    echo "⚠️  product-design skill requires setup"
    NEEDS_SETUP=true
  fi
fi
```

**If setup needed, show instructions**:

```markdown
⚠️  New Feature Requires Setup

The product-design skill (v3.4.0+) requires Python dependencies:

**One-time setup** (30 seconds):
```bash
cd ~/.claude/plugins/marketplaces/jitd-marketplace/skills/product-design
./setup.sh
```

**What this installs**:
- Python MCP SDK for direct Figma connection
- 95% orchestration reduction
- 92% token savings

**After setup, use**:
"Review this Figma design: [URL]"
```

**Record setup needed in TodoWrite** for tracking.

---

### Step 7: Feature Discovery

**Show new features** available in updated version.

**For v3.3.0 update**:
````markdown
🎉 Navigator v3.3.0 Update Complete!

## New Features Available

### visual-regression Skill (NEW)
Set up Storybook + Chromatic in 5 minutes instead of 2-3 hours.

**Usage**:
```
"Set up visual regression for ProfileCard"
"Add Chromatic to Button component"
"Configure visual tests for Input, Card, Modal"
```

**What it does**:
✅ Generates Storybook stories with all variants
✅ Configures Chromatic/Percy/BackstopJS
✅ Creates CI workflows (GitHub Actions, GitLab CI)
✅ Adds accessibility tests

**Complete Design Pipeline** (v3.2 + v3.3):
1. "Review this design from Figma" (v3.2)
2. Implement components
3. "Set up visual regression" (v3.3 NEW)
4. Automated visual testing in CI

### Updated Skills Count
- **17 total skills** (was 16)
- 10 core Navigator skills
- 7 development skills

### Integration
visual-regression integrates with product-design skill for complete design→code→testing workflow.

## Try It Now

If you have Storybook in this project:
```
"Set up visual regression for [ComponentName]"
```

If you don't have Storybook:
```bash
npx storybook init
```

Then:
```
"Set up visual regression for [ComponentName]"
```

## Documentation

- Release Notes: https://github.com/alekspetrov/navigator/releases/tag/v3.3.0
- Skill Docs: skills/visual-regression/SKILL.md
- Examples: skills/visual-regression/examples/
- SOP: .agent/sops/testing/visual-regression-setup.md (created in your project)
````

---

## Predefined Functions

### functions/version_detector.py

**Purpose**: Detect current and latest Navigator versions

**Usage**:
```bash
python3 functions/version_detector.py
```

**Output**:
```json
{
  "current_version": "3.2.0",
  "latest_version": "3.3.0",
  "update_available": true,
  "release_url": "https://github.com/alekspetrov/navigator/releases/tag/v3.3.0",
  "changes": {
    "new_skills": ["visual-regression"],
    "updated_skills": ["product-design"],
    "new_features": ["Multi-tool VR support", "CI workflows"],
    "breaking_changes": []
  }
}
```

### functions/plugin_updater.py

**Purpose**: Execute plugin update with retry logic

**Usage**:
```bash
python3 functions/plugin_updater.py --target-version 3.3.0
```

**Actions**:
1. Execute `/plugin update navigator`
2. If fails, retry with uninstall/reinstall
3. Verify update succeeded
4. Return status

### functions/plugin_verifier.py

**Purpose**: Verify update completed successfully

**Usage**:
```bash
python3 functions/plugin_verifier.py --expected-version 3.3.0
```

**Checks**:
- Plugin version matches expected
- New skills exist in filesystem
- Skills registered in plugin.json
- Skills are invokable (test invocation)

---

## Error Handling

### Update Failed: Network Error

```
❌ Update failed: Could not connect to plugin marketplace

Fix:
1. Check internet connection
2. Try again in a few minutes
3. Manual update: /plugin uninstall navigator && /plugin install navigator
```

### Update Failed: Permission Denied

```
❌ Update failed: Permission denied

Fix:
1. Close Claude Code
2. Check ~/.config/claude/plugins/ permissions
3. Restart Claude Code
4. Try update again
```

### Verification Failed: Skills Not Found

```
⚠️ Update completed but new skills not found

Fix:
1. Restart Claude Code (required for skill reload)
2. Verify: /plugin list
3. Test: "Set up visual regression for Button"
```

Automatically prompt user to restart.

### CLAUDE.md Update Conflicts

```
⚠️ CLAUDE.md update has conflicts with your customizations

Options:
[1] Keep my customizations (merge new features)
[2] Use new template (lose customizations)
[3] Show me the diff first

Reply with choice
```

Let user decide how to handle conflicts.

---

## Upgrade Paths

### From v3.0.x to v3.3.0

**Changes**:
- +2 skills (nav-markers in v3.1, visual-regression in v3.3)
- OpenTelemetry integration (v3.1)
- Product design skill (v3.2)
- Visual regression skill (v3.3)

**Breaking changes**: None (fully backward compatible)

### From v3.1.x to v3.3.0

**Changes**:
- Product design skill (v3.2)
- Visual regression skill (v3.3)
- Updated skills count (17 total)

**Breaking changes**: None

### From v3.2.x to v3.3.0

**Changes**:
- Visual regression skill
- Integration with product-design workflow
- Updated skills count (17 total)

**Breaking changes**: None

---

## Post-Update Checklist

After upgrade, verify:

- ✅ `/plugin list` shows new version
- ✅ CLAUDE.md updated with new patterns
- ✅ New skills auto-invoke on natural language
- ✅ Existing skills still work
- ✅ No conflicts in project configuration

**If all checked**: Update successful!

---

## Rollback

If update causes issues:

```
"Rollback Navigator to v3.2.0"
```

This will:
1. Uninstall current version
2. Install specific version from marketplace
3. Update CLAUDE.md to match
4. Verify rollback succeeded

---

## Integration Points

### With nav-update-claude

After plugin update, automatically invokes `nav-update-claude` to sync project configuration.

### With nav-start

After update, `nav-start` shows new features available in session statistics.

### With nav-init

If upgrading before project initialization, suggests running `nav-init` with latest features.

---

## Examples

### Example 1: Simple Update

```
User: "Update Navigator"

→ Detects: v3.2.0 → v3.3.0 available
→ Updates plugin
→ Updates CLAUDE.md
→ Shows: "visual-regression skill now available"
→ Suggests: "Set up visual regression for [Component]"
```

### Example 2: Already on Latest

```
User: "Update Navigator"

→ Detects: Already on v3.3.0
→ Shows new features available
→ Suggests trying visual-regression if not used yet
```

### Example 3: Update with Restart Required

```
User: "Update Navigator"

→ Updates plugin
→ Verification: Skills not found (needs restart)
→ Prompts: "Please restart Claude Code to complete update"
→ After restart: Verification succeeds
```

---

## Best Practices

1. **Update regularly**: Check for updates monthly
2. **Read release notes**: Understand new features before using
3. **Test new skills**: Try new features in test project first
4. **Report issues**: File GitHub issues for update problems
5. **Backup CLAUDE.md**: Keep backup before update (auto-created)

---

## Version History

- **v1.0.0**: Initial nav-upgrade skill (Navigator v3.3.1)

---

## Future Enhancements

- Auto-update check on `nav-start` (opt-in)
- Changelog display in CLI
- Update notifications for major versions
- Automated migration scripts for breaking changes

---

**Last Updated**: 2025-10-21
**Skill Type**: Core Navigator
**Auto-Invocation**: Yes
