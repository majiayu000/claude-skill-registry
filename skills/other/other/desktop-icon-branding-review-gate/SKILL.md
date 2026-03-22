---
name: "desktop-icon-branding-review-gate"
description: "How to review a Windows desktop icon slice that touches both app branding and MSI packaging"
domain: "testing"
confidence: "medium"
source: "hicks-app-icon-gate"
---

## Context

Use this when a Windows desktop slice introduces or replaces the app icon and the deliverable includes both desktop-shell branding and MSI packaging.

## Pattern

1. Separate **icon generation** from **icon adoption**. First prove the `.ico` really comes from the supplied source assets and contains the expected sizes; then prove the app and installer actually use it.
2. Treat the built exe as the source of truth for Windows shell branding. Review taskbar, Alt+Tab, Explorer, and installed executable behavior against the built artifact, not just the repository asset.
3. For WPF/custom chrome, do not confuse a missing inline title-bar glyph with a missing app icon. The real requirement is that shell-facing Windows surfaces resolve the branded exe icon correctly.
4. In WiX, shortcut branding is often inherited from the target exe. Do not require separate shortcut icon authoring unless the installer actually adds it.
5. Only require Add/Remove Programs icon coverage when the MSI authoring explicitly wires an ARP icon property/resource. If the installer does not declare that support, treat it as a non-goal instead of an implied failure.
6. Re-run the installer lifecycle after branding changes. A correct icon is not enough if the rebuilt MSI loses per-user scope, stops launching, or regresses uninstall cleanliness.
7. For PNG-backed `.ico` files, prefer proving provenance by reading the icon directory and comparing each embedded frame payload against the supplied PNGs. Exact payload matches are stronger evidence than screenshot-based checks or decoder-dependent pixel hashes.
8. When WiX sets an explicit shortcut icon, inspect the shortcut's `IconLocation` target as well as the `.lnk` itself. Windows Installer may cache the icon under `%APPDATA%\Microsoft\Installer\...`, and that cached file is the reliable thing to compare back to the source icon.

## Good signs

- The generated `.ico` contains the intended multi-resolution set from the provided source images
- The desktop project embeds the `.ico` into the built exe
- Taskbar, Alt+Tab, Explorer, and Start Menu shortcut all resolve to the same branded icon after install
- The MSI still installs under a user-profile path without elevation and launches the installed app successfully
- Each `.ico` frame can be traced back to the provided PNG set without resampling guesswork
- A WiX-authored shortcut icon cache file matches the shipped app icon even if the `.lnk` file's extracted icon hash differs

## Anti-patterns

- Accepting an `.ico` because it exists without checking where it came from or which sizes it contains
- Checking only repository files and never looking at the built exe or installed shortcut
- Demanding a separate WiX shortcut icon when the current shortcut can correctly inherit from the target exe
- Claiming ARP icon coverage without the corresponding installer property/resource wiring
- Treating branding as done even though the rebuilt MSI regressed per-user installation behavior
- Rejecting a correctly branded WiX shortcut just because the `.lnk` file hashes differently than the target exe, without checking the cached icon path the shortcut actually uses
