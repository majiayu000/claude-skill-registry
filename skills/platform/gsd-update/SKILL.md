---
name: gsd-update
description: Update GSD installation to latest version from npm
allowed-tools: Read, Bash
---

<objective>
Check current GSD version, compare with latest available on npm, and update if needed.

Purpose: Keep GSD up-to-date with latest features and bug fixes.
Output: Version comparison, changelog, and updated installation.
</objective>

<execution_context>
@{{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json
@{{PLATFORM_ROOT}}/get-shit-done/CHANGELOG.md
</execution_context>

<process>

<step name="detect_platform">
Detect which platform is being used based on manifest file:

```bash
# Check for manifest file to detect installation
if [ -f "./{{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json" ]; then
  MANIFEST_FILE="./{{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json"
  SCOPE="local"
elif [ -f "${HOME}/{{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json" ]; then
  MANIFEST_FILE="${HOME}/{{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json"
  SCOPE="global"
else
  echo "Error: GSD installation not found"
  echo "No manifest file at {{PLATFORM_ROOT}}/get-shit-done/.gsd-install-manifest.json"
  echo ""
  echo "Run installation first: npx get-shit-done-multi --{{PLATFORM_NAME}}"
  exit 1
fi

# Extract platform from manifest
PLATFORM=$(cat "${MANIFEST_FILE}" | grep -o '"platform"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)

# Determine install command
if [ "${SCOPE}" = "global" ]; then
  INSTALL_CMD="npx get-shit-done-multi@latest --${PLATFORM} --global"
else
  INSTALL_CMD="npx get-shit-done-multi@latest --${PLATFORM} --local"
fi

echo "Platform detected: ${PLATFORM} (${SCOPE})"
echo "Manifest file: ${MANIFEST_FILE}"
```
</step>

<step name="check_current_version">
Read current installed version from manifest:

```bash
if [ -f "${MANIFEST_FILE}" ]; then
  CURRENT_VERSION=$(cat "${MANIFEST_FILE}" | grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
  echo "Current version: ${CURRENT_VERSION}"
else
  echo "Error: Manifest file not found at ${MANIFEST_FILE}"
  exit 1
fi
```
</step>

<step name="check_npm_versions">
Check available versions on npm:

```bash
echo ""
echo "Checking npm registry..."

# Get latest version from npm
LATEST_VERSION=$(npm view get-shit-done-multi version 2>/dev/null)

if [ -z "${LATEST_VERSION}" ]; then
  echo "Error: Could not fetch version info from npm"
  echo "Check your internet connection"
  exit 1
fi

echo "Latest version: ${LATEST_VERSION}"
echo ""

# Get recent versions (last 5)
echo "Recent versions available:"
npm view get-shit-done-multi versions --json 2>/dev/null | \
  jq -r '.[-5:] | reverse | .[]' 2>/dev/null || \
  echo "  (Could not fetch version list)"
echo ""
```
</step>

<step name="compare_versions">
Compare current vs latest:

```bash
if [ "${CURRENT_VERSION}" = "${LATEST_VERSION}" ]; then
  echo "✓ You're running the latest version (${CURRENT_VERSION})"
  echo ""
  echo "No update needed."
  exit 0
fi

# Simple version comparison (works for semantic versions)
if [ "${CURRENT_VERSION}" != "unknown" ]; then
  echo "📦 Update available: ${CURRENT_VERSION} → ${LATEST_VERSION}"
else
  echo "📦 Latest version available: ${LATEST_VERSION}"
fi
echo ""
```
</step>

<step name="display_changelog">
Display recent changes:

```bash
echo "=== Recent Changes ==="
echo ""

# CHANGELOG is in get-shit-done directory (same as manifest)
CHANGELOG_FILE="${MANIFEST_FILE%/*}/CHANGELOG.md"

if [ -f "${CHANGELOG_FILE}" ]; then
  # Show latest version changes (top section)
  awk '/^## \[/{p++} p==1' "${CHANGELOG_FILE}" | head -30
else
  echo "(CHANGELOG.md not available locally)"
  echo "View at: https://github.com/shoootyou/get-shit-done-multi/blob/main/CHANGELOG.md"
fi

echo ""
```
</step>

<step name="confirm_update">
Ask for update confirmation:

```bash
echo "Update command: ${INSTALL_CMD}"
echo ""
echo "This will:"
echo "  1. Download latest version from npm"
echo "  2. Regenerate platform-specific skills and agents"
echo "  3. Update all GSD files in place"
echo ""
read -p "Proceed with update? (y/n): " CONFIRM

if [ "${CONFIRM}" != "y" ] && [ "${CONFIRM}" != "Y" ]; then
  echo "Update cancelled"
  echo ""
  echo "To update later, run: ${INSTALL_CMD}"
  exit 0
fi
```
</step>

<step name="run_update">
Execute npm installation:

```bash
echo ""
echo "Running update..."
echo "Command: ${INSTALL_CMD}"
echo ""

# Run the installation command
eval "${INSTALL_CMD}"

UPDATE_EXIT_CODE=$?

if [ ${UPDATE_EXIT_CODE} -ne 0 ]; then
  echo ""
  echo "✗ Update failed with exit code ${UPDATE_EXIT_CODE}"
  echo ""
  echo "Try running manually: ${INSTALL_CMD}"
  exit 1
fi
```
</step>

<step name="verify_update">
Verify the update succeeded:

```bash
echo ""
echo "Verifying update..."

# Read new version from manifest
if [ -f "${MANIFEST_FILE}" ]; then
  NEW_VERSION=$(cat "${MANIFEST_FILE}" | grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
  
  if [ "${NEW_VERSION}" = "${LATEST_VERSION}" ]; then
    echo "✓ Successfully updated to ${NEW_VERSION}"
  else
    echo "⚠ Version mismatch:"
    echo "  Expected: ${LATEST_VERSION}"
    echo "  Installed: ${NEW_VERSION}"
  fi
else
  echo "⚠ Could not verify version (manifest file not found)"
  NEW_VERSION="${LATEST_VERSION}"
fi
```
</step>

<step name="present_summary">
Show update summary:

```
## GSD UPDATE COMPLETE

**Previous version:** ${CURRENT_VERSION}
**New version:** ${NEW_VERSION}

✓ Downloaded from npm
✓ Skills and agents regenerated
✓ Installation verified

### Next Steps

1. Test a command to ensure everything works:
   {{COMMAND_PREFIX}}help

2. Review changelog for new features and changes

3. If using Claude Code, restart to reload commands

### Resources

- Changelog: ${CHANGELOG_FILE}
- Manifest: ${MANIFEST_FILE}
- Issues: https://github.com/shoootyou/get-shit-done-multi/issues
- Docs: https://github.com/shoootyou/get-shit-done-multi/blob/main/README.md

---

**Having issues?** Run {{COMMAND_PREFIX}}verify-installation for diagnostics.
```
</step>

</process>

<anti_patterns>
- Don't try to update via git (use npm package)
- Don't modify manifest file manually
- Don't skip version check (always compare first)
- Don't assume update succeeded without verification
- Don't mix --global and --local scopes (use same scope as current installation)
</anti_patterns>
