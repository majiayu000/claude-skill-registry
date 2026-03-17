---
name: ghe-changelog
description: This skill should be used when updating the project CHANGELOG, tracking requirement changes, recording design decisions, or documenting version history. Uses git-diff to detect and categorize changes to both code and requirements. Trigger on "changelog", "version history", "what changed", or after significant commits.
---

## IRON LAW: User Specifications Are Sacred

**THIS LAW IS ABSOLUTE AND ADMITS NO EXCEPTIONS.**

1. **Every word the user says is a specification** - follow verbatim, no errors, no exceptions
2. **Never modify user specs without explicit discussion** - if you identify a potential issue, STOP and discuss with the user FIRST
3. **Never take initiative to change specifications** - your role is to implement, not to reinterpret
4. **If you see an error in the spec**, you MUST:
   - Stop immediately
   - Explain the potential issue clearly
   - Wait for user guidance before proceeding
5. **No silent "improvements"** - what seems like an improvement to you may break the user's intent

**Violation of this law invalidates all work produced.**

## Background Agent Boundaries

When running as a background agent, you may ONLY write to:
- The project directory and its subdirectories
- The parent directory (for sub-git projects)
- ~/.claude (for plugin/settings fixes)
- /tmp

Do NOT write outside these locations.

---

## GHE_REPORTS Rule (MANDATORY)

**ALL reports MUST be posted to BOTH locations:**
1. **GitHub Issue Thread** - Full report text (NOT just a link!)
2. **GHE_REPORTS/** - Same full report text (FLAT structure, no subfolders!)

**Report naming:** `<TIMESTAMP>_<title or description>_(<AGENT>).md`
**Timestamp format:** `YYYYMMDDHHMMSSTimezone`

**ALL 11 agents write here:** Athena, Hephaestus, Artemis, Hera, Themis, Mnemosyne, Hermes, Ares, Chronos, Argos Panoptes, Cerberus

**REQUIREMENTS/** is SEPARATE - permanent design documents, never deleted.

**Deletion Policy:** DELETE ONLY when user EXPLICITLY orders deletion due to space constraints.

---

# GHE Changelog Management

## Overview

GHE maintains a comprehensive CHANGELOG that tracks:
1. **Product Changes** - Code, features, bug fixes
2. **Design Changes** - Architecture, patterns, decisions
3. **Requirements Changes** - REQ file updates, new requirements

## CHANGELOG Structure

```
CHANGELOG.md (root)
├── [Unreleased]           # Changes not yet in a release
├── [X.Y.Z] - YYYY-MM-DD   # Released versions
│   ├── Added              # New features
│   ├── Changed            # Modified behavior
│   ├── Deprecated         # Features to be removed
│   ├── Removed            # Deleted features
│   ├── Fixed              # Bug fixes
│   ├── Security           # Security patches
│   ├── Requirements       # REQ file changes
│   └── Design             # Architecture changes
```

## Automated Changelog Generation

### Using git-diff to Detect Changes

```bash
#!/bin/bash
# Generate changelog entries from recent commits

# Get commits since last tag
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
if [ -z "$LAST_TAG" ]; then
  COMMITS=$(git log --oneline)
else
  COMMITS=$(git log --oneline ${LAST_TAG}..HEAD)
fi

# Categorize changes
ADDED=""
CHANGED=""
FIXED=""
REQUIREMENTS=""
DESIGN=""

while read -r commit; do
  HASH=$(echo "$commit" | cut -d' ' -f1)
  MSG=$(echo "$commit" | cut -d' ' -f2-)

  # Get files changed
  FILES=$(git diff-tree --no-commit-id --name-only -r "$HASH")

  # Categorize by commit message and files
  if echo "$MSG" | grep -qiE "^(add|feat|new):"; then
    ADDED="$ADDED\n- $MSG"
  elif echo "$MSG" | grep -qiE "^(fix|bug|patch):"; then
    FIXED="$FIXED\n- $MSG"
  elif echo "$MSG" | grep -qiE "^(change|update|refactor):"; then
    CHANGED="$CHANGED\n- $MSG"
  elif echo "$FILES" | grep -q "^REQUIREMENTS/"; then
    REQUIREMENTS="$REQUIREMENTS\n- $MSG"
  elif echo "$FILES" | grep -qE "^(docs/|DESIGN|ARCHITECTURE)"; then
    DESIGN="$DESIGN\n- $MSG"
  else
    CHANGED="$CHANGED\n- $MSG"
  fi
done <<< "$COMMITS"
```

### Detailed Diff Analysis

```bash
# Get detailed changes for a specific file type
analyze_changes() {
  local PATTERN=$1
  local SINCE=$2

  git diff "$SINCE" --stat -- "$PATTERN" | while read line; do
    FILE=$(echo "$line" | awk '{print $1}')
    INSERTIONS=$(echo "$line" | grep -oP '\d+(?= insertion)')
    DELETIONS=$(echo "$line" | grep -oP '\d+(?= deletion)')

    echo "- \`$FILE\`: +$INSERTIONS/-$DELETIONS lines"
  done
}

# Example usage
echo "### Code Changes"
analyze_changes "src/**/*.py" "$LAST_TAG"

echo "### Requirements Changes"
analyze_changes "REQUIREMENTS/**/*.md" "$LAST_TAG"
```

## Requirements Changelog Section

Track all REQ file changes:

```bash
# Generate requirements changelog
generate_req_changelog() {
  local SINCE=$1

  echo "### Requirements"
  echo ""

  # New requirements
  NEW_REQS=$(git diff "$SINCE" --diff-filter=A --name-only -- "REQUIREMENTS/*.md")
  if [ -n "$NEW_REQS" ]; then
    echo "#### New Requirements"
    for req in $NEW_REQS; do
      REQ_ID=$(grep "^req_id:" "$req" | cut -d' ' -f2)
      TITLE=$(grep "^# REQ-" "$req" | sed 's/^# //')
      echo "- **$REQ_ID**: $TITLE"
    done
    echo ""
  fi

  # Modified requirements
  MOD_REQS=$(git diff "$SINCE" --diff-filter=M --name-only -- "REQUIREMENTS/*.md")
  if [ -n "$MOD_REQS" ]; then
    echo "#### Updated Requirements"
    for req in $MOD_REQS; do
      REQ_ID=$(grep "^req_id:" "$req" | cut -d' ' -f2)
      OLD_VER=$(git show "$SINCE:$req" 2>/dev/null | grep "^version:" | cut -d' ' -f2)
      NEW_VER=$(grep "^version:" "$req" | cut -d' ' -f2)
      echo "- **$REQ_ID**: v$OLD_VER -> v$NEW_VER"
    done
    echo ""
  fi

  # Deprecated requirements
  DEP_REQS=$(git diff "$SINCE" --name-only -- "REQUIREMENTS/*.md" | while read req; do
    if grep -q "status: deprecated" "$req" 2>/dev/null; then
      echo "$req"
    fi
  done)
  if [ -n "$DEP_REQS" ]; then
    echo "#### Deprecated Requirements"
    for req in $DEP_REQS; do
      REQ_ID=$(grep "^req_id:" "$req" | cut -d' ' -f2)
      echo "- **$REQ_ID** (deprecated)"
    done
  fi
}
```

## Design Decision Tracking

Track architecture and design changes:

```markdown
### Design Decisions

#### [DD-001] Decision Title
- **Date**: YYYY-MM-DD
- **Status**: Accepted | Superseded | Deprecated
- **Context**: Why was this decision needed?
- **Decision**: What was decided?
- **Consequences**: What are the implications?
- **Related**: REQ-XXX, Issue #N
```

### Automated Design Detection

```bash
# Detect design-impacting changes
detect_design_changes() {
  local SINCE=$1

  # Architecture files
  ARCH_CHANGES=$(git diff "$SINCE" --name-only -- \
    "docs/architecture*.md" \
    "docs/design*.md" \
    "DESIGN*.md" \
    "ADR/*.md" \
    "**/README.md")

  # Major structural changes (new directories, renamed files)
  STRUCT_CHANGES=$(git diff "$SINCE" --summary | grep -E "^(create|rename|delete) mode")

  # Interface changes
  INTERFACE_CHANGES=$(git diff "$SINCE" -- "**/*.py" | grep -E "^[\+\-].*def __init__|^[\+\-].*class |^[\+\-].*@abstractmethod")

  if [ -n "$ARCH_CHANGES" ] || [ -n "$STRUCT_CHANGES" ] || [ -n "$INTERFACE_CHANGES" ]; then
    echo "### Design Changes Detected"
    echo ""
    echo "Review the following for design documentation updates:"
    echo ""
    [ -n "$ARCH_CHANGES" ] && echo "**Architecture docs modified**:" && echo "$ARCH_CHANGES" | sed 's/^/- /'
    [ -n "$STRUCT_CHANGES" ] && echo "**Structural changes**:" && echo "$STRUCT_CHANGES" | sed 's/^/- /'
    [ -n "$INTERFACE_CHANGES" ] && echo "**Interface changes detected** (review for breaking changes)"
  fi
}
```

## Full Changelog Update Command

```bash
#!/bin/bash
# update-changelog.sh - Full changelog update

set -e

CHANGELOG="CHANGELOG.md"
LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "initial")
DATE=$(date +%Y-%m-%d)

# Backup current changelog
cp "$CHANGELOG" "${CHANGELOG}.bak"

# Generate new entries
NEW_ENTRIES=$(cat <<EOF

## [Unreleased]

### Added
$(git log "$LAST_TAG"..HEAD --oneline --grep="^add\|^feat\|^new" | sed 's/^[a-f0-9]* /- /')

### Changed
$(git log "$LAST_TAG"..HEAD --oneline --grep="^change\|^update\|^refactor" | sed 's/^[a-f0-9]* /- /')

### Fixed
$(git log "$LAST_TAG"..HEAD --oneline --grep="^fix\|^bug\|^patch" | sed 's/^[a-f0-9]* /- /')

$(generate_req_changelog "$LAST_TAG")

$(detect_design_changes "$LAST_TAG")

EOF
)

# Insert after header
sed -i "/^# Changelog/a\\$NEW_ENTRIES" "$CHANGELOG"

echo "Changelog updated. Review and commit."
```

## Integration with GHE Workflow

### After Each Phase Completion

```bash
# Post phase completion, update changelog
update_changelog_for_phase() {
  local PHASE=$1
  local ISSUE=$2

  ISSUE_TITLE=$(gh issue view "$ISSUE" --json title --jq '.title')

  case $PHASE in
    "dev")
      echo "- [$ISSUE_TITLE](#$ISSUE) - Development complete" >> CHANGELOG.md
      ;;
    "test")
      echo "- [$ISSUE_TITLE](#$ISSUE) - Tests passing" >> CHANGELOG.md
      ;;
    "review")
      echo "- [$ISSUE_TITLE](#$ISSUE) - Reviewed and approved" >> CHANGELOG.md
      ;;
  esac
}
```

### On Release

```bash
# Prepare release changelog
prepare_release() {
  local VERSION=$1
  local DATE=$(date +%Y-%m-%d)

  # Move unreleased to new version
  sed -i "s/## \[Unreleased\]/## [$VERSION] - $DATE\n\n## [Unreleased]/" CHANGELOG.md

  # Commit
  git add CHANGELOG.md
  git commit -m "Release $VERSION changelog"
  git tag "v$VERSION"
}
```

## Settings Awareness

Respects `.claude/ghe.local.md`:
```yaml
changelog_file: CHANGELOG.md      # Changelog location
track_requirements: true          # Include REQ changes
track_design: true               # Include design changes
auto_update: true                # Update on phase completion
```

## Best Practices

1. **Commit Messages Matter** - Use conventional commits (feat:, fix:, etc.)
2. **Version Requirements** - Always version REQ files when changing
3. **Document Design Decisions** - Create ADRs for major changes
4. **Review Before Release** - Always review auto-generated entries
5. **Link Everything** - Reference issues, PRs, and requirements
