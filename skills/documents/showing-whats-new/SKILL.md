---
name: showing-whats-new
description: Use this skill when showing what's new in Kata since the installed version, displaying changelog entries, checking for Kata updates, or reviewing recent changes. Triggers include "what's new", "whats new", "show changes", "changelog", "recent changes", and "what changed".
metadata:
  version: "0.1.0"
user-invocable: false
disable-model-invocation: false
allowed-tools:
  - Read
  - Write
  - Bash
---

<user_command>/kata:whats-new</user_command>


<objective>
Display changes between installed version and latest available version.

Shows version comparison, changelog entries for missed versions, and update instructions.
</objective>

<process>

<step name="get_installed_version">
Read installed version from VERSION file (checking plugin context first):

```bash
if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
  cat "$CLAUDE_PLUGIN_ROOT/kata/VERSION" 2>/dev/null
elif [ -f ~/.claude/kata/VERSION ]; then
  cat ~/.claude/kata/VERSION
elif [ -f ./.claude/kata/VERSION ]; then
  cat ./.claude/kata/VERSION
fi
```

**If VERSION file missing:**
```
## Kata What's New

**Installed version:** Unknown

Your installation doesn't include version tracking.

**To reinstall:**
- Plugin users: `/plugin install kata@kata-marketplace`
- NPM users: `npx @gannonh/kata --global`
```

STOP here if no VERSION file.
</step>

<step name="fetch_remote_changelog">
Fetch latest CHANGELOG.md from GitHub:

Use WebFetch tool with:
- URL: `https://raw.githubusercontent.com/gannonh/kata/refs/heads/main/CHANGELOG.md`
- Prompt: "Extract all version entries with their dates and changes. Return in Keep-a-Changelog format."

**If fetch fails:**
Fall back to local changelog:
```bash
cat $KATA_BASE/CHANGELOG.md 2>/dev/null
```

Note to user: "Couldn't check for updates (offline or GitHub unavailable). Showing local changelog."
</step>

<step name="parse_versions">
From the remote (or local) changelog:

1. **Extract latest version** - First `## [X.Y.Z]` line after `## [Unreleased]`
2. **Compare with installed** - From VERSION file
3. **Extract entries between** - All version sections from latest down to (but not including) installed

**Version comparison:**
- If installed == latest: "You're on the latest version"
- If installed < latest: Show changes since installed version
- If installed > latest: "You're ahead of latest release (development version?)"
</step>

<step name="display_output">
Format output clearly:

**If up to date:**
```
## Kata What's New

**Installed:** 1.4.26
**Latest:** 1.4.26

You're on the latest version.

[View full changelog](https://github.com/gannnonh/kata/blob/main/CHANGELOG.md)
```

**If updates available:**
```
## Kata What's New

**Installed:** 1.4.23
**Latest:** 1.4.26

---

### Changes since your version:

## [1.4.26] - 2026-01-20

### Added
- Feature X
- Feature Y

### Changed
- **BREAKING:** Changed Z behavior

## [1.4.25] - 2026-01-18

### Fixed
- Bug in feature A

---

[View full changelog](https://github.com/gannnonh/kata/blob/main/CHANGELOG.md)

**To update:**
- Plugin users: `/plugin update kata@kata-marketplace`
- NPM users: `npx @gannonh/kata --global`
```

**Breaking changes:** Surface prominently with **BREAKING:** prefix in the output.
</step>

</process>

<success_criteria>
- [ ] Installed version read from VERSION file
- [ ] Remote changelog fetched (or graceful fallback to local)
- [ ] Version comparison displayed clearly
- [ ] Changes since installed version shown (if any)
- [ ] Update instructions provided when behind
</success_criteria>
