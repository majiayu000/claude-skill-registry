---
name: skill-forge-publish
description: >
  Package and distribute Claude Code skills for sharing via GitHub, Claude.ai
  uploads, or team deployment. Creates install scripts, documentation, and
  .skill packages. Use when user says "publish skill", "share skill",
  "package skill", "distribute skill", or "release skill".
---

# Skill Publishing & Distribution

## Process

### Step 1: Pre-Publish Validation

Run the full review before publishing:
1. Execute `/skill-forge review <path>` and ensure score >= 80/100
2. Fix any critical or high-priority issues
3. Test with at least 5 trigger queries
4. Verify all cross-references resolve

### Step 2: Create Install Script

Generate `install.sh` that handles:

```bash
#!/usr/bin/env bash
# Install script for [skill-name]
# Usage: bash install.sh

set -euo pipefail

SKILL_DIR="$HOME/.claude/skills"
AGENT_DIR="$HOME/.claude/agents"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing [skill-name] skill..."

# Create directories
mkdir -p "$SKILL_DIR" "$AGENT_DIR"

# Copy main skill
cp -r "$SCRIPT_DIR/skill-name" "$SKILL_DIR/"
echo "  Installed: skill-name"

# Copy sub-skills
for skill in "$SCRIPT_DIR/skills"/skill-name-*/; do
    if [ -d "$skill" ]; then
        skill_basename=$(basename "$skill")
        cp -r "$skill" "$SKILL_DIR/"
        echo "  Installed: $skill_basename"
    fi
done

# Copy agents (if any)
if [ -d "$SCRIPT_DIR/agents" ]; then
    cp "$SCRIPT_DIR/agents"/*.md "$AGENT_DIR/" 2>/dev/null || true
    echo "  Installed agents"
fi

echo ""
echo "Installation complete!"
echo "Test with: /skill-name"
```

### Step 3: Create README.md (repo-level, NOT inside skill folder)

```markdown
# [Skill Name]

[1-2 sentence description focusing on outcomes, not features]

## What it does

[Bullet list of key capabilities]

## Installation

### Claude Code
```
git clone https://github.com/[user]/[repo]
cd [repo]
bash install.sh
```

### Claude.ai
1. Download the latest release (.zip)
2. Go to Settings > Capabilities > Skills
3. Click "Upload skill"
4. Select the downloaded .zip file

## Commands

| Command | Description |
|---------|-------------|
| `/skill-name` | [description] |
| `/skill-name cmd` | [description] |

## Examples

### [Example 1 title]
```
User: "[example input]"
```
[Description of what happens and expected output]

## Architecture

```
[file tree diagram]
```

## License

[License type]
```

### Step 4: Package for Distribution

**For Claude.ai upload:**
Run `python scripts/package_skill.py <path> <output-dir>` to create a `.skill` zip file.

**For GitHub:**
1. Create repository with README.md at root
2. Skill folder(s) at root level
3. install.sh at root level
4. Add LICENSE file
5. Add .gitignore (exclude .tmp/, __pycache__/, *.pyc)

**For team deployment (Claude.ai admin):**
- Skills can be deployed workspace-wide by admins
- Package as .skill zip and upload through admin console

### Step 5: Create .gitignore

```
__pycache__/
*.pyc
*.pyo
.tmp/
*.egg-info/
dist/
build/
.env
*.skill
```

### Step 6: Release Checklist

- [ ] All files validated (score >= 80)
- [ ] install.sh tested on clean system
- [ ] README.md covers installation, usage, and examples
- [ ] LICENSE file included
- [ ] .gitignore configured
- [ ] No secrets or API keys in any file
- [ ] Test queries documented
- [ ] Version tagged (if using git)

### Step 7: Post-Publish

After publishing:
1. Test installation from scratch on a clean environment
2. Run all trigger test queries
3. Collect initial user feedback
4. Plan first iteration based on feedback
5. Set up issue templates for bug reports

## Distribution Channels

| Channel | Best For | Format |
|---------|----------|--------|
| GitHub | Open source, community | Repository + install.sh |
| Claude.ai upload | Personal use | .skill zip |
| Team admin | Organization-wide | .skill zip via admin console |
| Claude Plugin Marketplace | Wide distribution | .claude-plugin/ manifest |
