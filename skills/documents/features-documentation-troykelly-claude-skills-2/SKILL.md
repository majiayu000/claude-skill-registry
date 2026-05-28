---
name: features-documentation
description: Use when user-facing features change. Ensures features documentation is updated. Pauses work if documentation has drifted, triggering documentation-audit skill.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - Edit
  - Write
  - mcp__github__*
model: opus
---

# Features Documentation Enforcement

## Overview

Ensures all user-facing feature changes are reflected in features documentation. When documentation drift is detected, work pauses until documentation is synchronized.

**Core principle:** Users must be able to discover and understand all features. Undocumented features don't exist to users.

**Announce at start:** "I'm using features-documentation to verify feature documentation sync."

## When This Skill Triggers

This skill is triggered when changes affect user-facing functionality:

| Change Type | Examples | Trigger Reason |
|-------------|----------|----------------|
| New feature | New button, page, capability | Must be documented |
| Feature modification | Changed behavior, new options | Docs must reflect current state |
| Feature removal | Deprecated/removed capability | Remove from docs |
| UI changes | New flows, changed interactions | User guidance needed |
| Configuration | New settings, options | Users need to know options |

## Documentation Locations

Check these locations for features documentation:

| File | Purpose |
|------|---------|
| `docs/features.md` | Primary features documentation |
| `docs/FEATURES.md` | Alternative location |
| `FEATURES.md` | Root-level features doc |
| `docs/user-guide.md` | User-facing guide |
| `docs/guide.md` | Usage guide |
| `README.md` (Features section) | Embedded features list |

## The Protocol

### Step 1: Detect Feature Changes

```bash
# Check if current changes affect user-facing features
FEATURE_CHANGED=false

# UI components
if git diff --name-only HEAD~1 | grep -qE "(components/|pages/|views/|screens/)"; then
  FEATURE_CHANGED=true
fi

# Feature flags
if git diff --name-only HEAD~1 | grep -qE "(features\.|feature-flags|config/)"; then
  FEATURE_CHANGED=true
fi

# Configuration/settings
if git diff --name-only HEAD~1 | grep -qE "(settings|preferences|config)"; then
  FEATURE_CHANGED=true
fi

echo "Feature Changed: $FEATURE_CHANGED"
```

### Step 2: Find Documentation File

```bash
find_feature_docs() {
  for file in docs/features.md docs/FEATURES.md FEATURES.md \
              docs/user-guide.md docs/guide.md; do
    if [ -f "$file" ]; then
      echo "$file"
      return 0
    fi
  done

  # Check README for Features section
  if [ -f "README.md" ] && grep -q "## Features" README.md; then
    echo "README.md"
    return 0
  fi

  return 1
}

DOC_FILE=$(find_feature_docs)
if [ -z "$DOC_FILE" ]; then
  echo "WARNING: No features documentation file found"
  echo "PAUSE: Trigger documentation-audit skill to create"
fi
```

### Step 3: Verify Feature Coverage

```bash
verify_feature_coverage() {
  local doc_file=$1
  local issues_found=false

  # Extract feature names from code (common patterns)
  CODE_FEATURES=$(find . -name "*.ts" -name "*.tsx" \
    -exec grep -h "feature:" {} \; 2>/dev/null | \
    sed 's/.*feature:\s*["'\'']\([^"'\'']*\)["'\''].*/\1/' | sort -u)

  # Extract documented features
  DOC_FEATURES=$(grep -oP '(?<=^## |^### |^\* \*\*)[^*]+(?=\*\*|$)' "$doc_file" | \
    tr '[:upper:]' '[:lower:]' | sort -u)

  # Find undocumented features
  for feature in $CODE_FEATURES; do
    feature_lower=$(echo "$feature" | tr '[:upper:]' '[:lower:]')
    if ! echo "$DOC_FEATURES" | grep -q "$feature_lower"; then
      echo "UNDOCUMENTED: $feature"
      issues_found=true
    fi
  done

  if [ "$issues_found" = "true" ]; then
    return 1
  fi
  return 0
}
```

### Step 4: Handle Drift

If documentation drift is detected:

```markdown
## Features Documentation Drift Detected

**Status:** PAUSED
**Reason:** Features documentation is out of sync with code

### Undocumented Features
- **Dark Mode** (added in `components/ThemeToggle.tsx`)
- **Export to PDF** (added in `features/export/`)
- **Multi-language Support** (added in `i18n/`)

### Action Required
1. Invoke `documentation-audit` skill
2. Update features documentation
3. Resume current work after sync complete

---
*features-documentation skill paused work*
```

Then invoke documentation-audit:

```
Use Skill tool: documentation-audit
```

## Documentation Requirements

When updating features documentation, include:

### Required for Each Feature

| Section | Description |
|---------|-------------|
| **Name** | Clear, user-friendly name |
| **Description** | What it does, why it's useful |
| **How to Use** | Step-by-step instructions |
| **Prerequisites** | Requirements, permissions |
| **Configuration** | Available options/settings |
| **Examples** | Common use cases |
| **Limitations** | Known constraints |

### Example Feature Entry

```markdown
## Dark Mode

Switch between light and dark color themes for comfortable viewing in any lighting condition.

### How to Use

1. Click the **Settings** icon in the top navigation
2. Select **Appearance**
3. Choose your preferred theme:
   - **Light** - Best for bright environments
   - **Dark** - Reduces eye strain in low light
   - **System** - Follows your OS preference

### Configuration

| Setting | Options | Default |
|---------|---------|---------|
| Theme | Light, Dark, System | System |
| Transition | Instant, Animated | Animated |

### Keyboard Shortcut

Press `Ctrl+Shift+T` (Windows/Linux) or `Cmd+Shift+T` (Mac) to toggle.

### Notes

- Theme preference is saved to your account
- Some third-party embeds may not respect dark mode
```

## Features Document Structure

```markdown
# Features

## Overview
Brief description of the product and its core purpose.

## Core Features

### [Feature 1 Name]
[Feature 1 content]

### [Feature 2 Name]
[Feature 2 content]

## Advanced Features

### [Feature 3 Name]
[Feature 3 content]

## Experimental Features

### [Beta Feature Name]
[Beta feature content with experimental warning]

## Deprecated Features

### [Deprecated Feature]
[Migration guidance]

---
*Last updated: [DATE]*
```

## Validation

After updating documentation:

```bash
# Check markdown validity
npx markdownlint docs/features.md

# Check for broken links
npx markdown-link-check docs/features.md

# Check all features have required sections
grep -c "^### How to Use" docs/features.md
```

## Checklist

Before resuming work:

- [ ] Features documentation file exists
- [ ] All user-facing features documented
- [ ] How-to-use instructions provided
- [ ] Configuration options listed
- [ ] Examples included
- [ ] Deprecated features marked
- [ ] Documentation validates
- [ ] Changes committed

## Integration

This skill coordinates with:

| Skill | Purpose |
|-------|---------|
| `documentation-audit` | Full documentation sync |
| `issue-driven-development` | Triggered during implementation |
| `comprehensive-review` | Validates documentation complete |

## When to Skip

This skill can be skipped when:
- Changes are purely internal (no user-visible impact)
- Changes are to backend/infrastructure only
- Changes are to test files only
- Changes are to documentation itself
- Project is a library without UI
