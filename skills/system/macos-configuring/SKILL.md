---
name: macos-configuring
description: Use when configuring macOS settings via terminal, setting up a new machine, asking to configure Finder/Dock/screenshots/keyboard/apps, generating setup scripts, or troubleshooting why a setting didn't take effect.
---

# Configuring macOS

How to configure macOS programmatically. Don't document specific commands here - use training knowledge or web search for those. This skill is about the process.

## Responding to "Configure my X"

When the user asks to configure something:

1. **Training knowledge** - Try what you know first
2. **Search references** - Check macos-defaults.com or mathiasbynens/.macos
3. **Last resort: Discovery** - Use the diff technique below
4. **After writing** - Tell user what restart is needed (see table)
5. **Generating script?** - Use the script template

## Discovering Unknown Settings (Last Resort)

When training and references don't have the answer:

```bash
# 1. Snapshot current state
defaults read > /tmp/before.plist

# 2. User changes setting in System Settings GUI

# 3. Diff to find what changed
defaults read > /tmp/after.plist
diff /tmp/before.plist /tmp/after.plist
```

For app-specific: `defaults read com.apple.APPNAME > /tmp/before.plist`

To find an app's domain:
```bash
osascript -e 'id of app "Photos"'           # Returns bundle ID
ls ~/Library/Preferences/ | grep -i photos  # Or check filesystem
defaults domains | tr ',' '\n' | grep -i photos
```

## Applying Changes

Settings require process restart. **Never auto-logout or auto-restart** - tell the user what they need to do.

| What Changed | How to Apply |
|--------------|--------------|
| Dock, hot corners, Spaces | `killall Dock` (safe to run) |
| Finder, desktop | `killall Finder` (safe to run) |
| Menu bar items | `killall SystemUIServer` (safe to run) |
| Keyboard, fn key, input | Tell user: "Logout and log back in" |
| Login window | Tell user: "Restart your Mac" |
| Uncertain | Try `killall cfprefsd`, then tell user to logout |

## Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "Configuring [category]..."

defaults write DOMAIN KEY -TYPE VALUE

killall PROCESS 2>/dev/null || true

echo "Done."
```

## Troubleshooting

| Problem | Cause & Fix |
|---------|-------------|
| Setting reverts | App overwrote on quit. Close app first. |
| No effect | Wrong domain (`defaults find KEYWORD`), or needs logout not killall |
| Cached values | `killall cfprefsd` flushes preference cache |
| Permission denied | May need `sudo`, or protected by SIP |

## Quick Reference

```bash
defaults write DOMAIN KEY -TYPE VALUE   # Set
defaults read DOMAIN KEY                # Get
defaults delete DOMAIN KEY              # Remove
defaults find KEYWORD                   # Search all domains
```

Types: `-string`, `-int`, `-float`, `-bool`, `-array`, `-dict`

## Resources

- [macos-defaults.com](https://macos-defaults.com/) - Searchable database of known settings
- [mathiasbynens/.macos](https://github.com/mathiasbynens/dotfiles/blob/main/.macos) - Comprehensive example script
