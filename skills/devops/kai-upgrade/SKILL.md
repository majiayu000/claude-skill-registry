---
name: kai-upgrade
description: Update kai-marketing to the latest version. Pulls latest code, re-registers skills, shows what changed. Does NOT modify content state or MARKETING.md.
---

# /kai-upgrade — Self-Updater

Update kai-marketing to the latest version. Safe — only updates skill definitions, knowledge files, and bin/ tools. Never touches your content state, config, or MARKETING.md.

## The Skill

### Step 1: Detect Install Location

Find the kai-marketing root directory:
```bash
KAI_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
echo "Install location: $KAI_ROOT"
```

Check if it's a git repo:
```bash
cd "$KAI_ROOT" && git rev-parse --is-inside-work-tree 2>/dev/null
```

If not a git repo: "This install was copied, not cloned. Re-install with: `git clone https://github.com/cgallic/kai-marketing.git ~/.claude/skills/kai-marketing`"

### Step 2: Check Current Version

```bash
cat "$KAI_ROOT/VERSION"
```

### Step 3: Pull Latest

```bash
cd "$KAI_ROOT" && git pull origin main 2>&1
```

If pull fails (network, conflicts): Show the error and suggest manual resolution.

### Step 4: Show What Changed

```bash
OLD_VERSION=$(git show HEAD~1:VERSION 2>/dev/null || echo "unknown")
NEW_VERSION=$(cat VERSION)
echo "Updated: v${OLD_VERSION} → v${NEW_VERSION}"
```

Show recent changelog entries:
```bash
git log --oneline -10
```

If a CHANGELOG.md exists, show entries between old and new version.

### Step 5: Re-Register Skills

```bash
cd "$KAI_ROOT" && ./setup
```

### Step 6: Confirm

```
kai-marketing upgraded: v{old} → v{new}
  Skills re-registered
  Knowledge base updated
  Content state untouched
```
