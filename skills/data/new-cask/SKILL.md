---
name: new-cask
argument-hint: "<download-url>"
context: fork
description: >-
  This skill should be used when the user asks to "add a cask to homebrew",
  "create a homebrew cask", "add an app to homebrew", "new cask for",
  "homebrew cask for", "package an app for homebrew", "submit to homebrew-cask",
  "make a cask", "contribute a cask", or wants to package a macOS application
  for Homebrew.
---

# Creating a New Homebrew Cask

## Reference Documentation

Official docs (read as needed):

- `$(brew --repository)/docs/Adding-Software-to-Homebrew.md` - Contribution overview
- `$(brew --repository)/docs/Cask-Cookbook.md` - Stanza reference
- `$(brew --repository)/docs/Brew-Livecheck.md` - Livecheck strategies
- `$(brew --repository)/docs/Acceptable-Casks.md` - Acceptance criteria

## Workflow Overview

1. **Pre-flight checks** - Duplicate detection, rejection history, acceptability
2. **Information gathering** - URLs, versions, checksums, auto-updates, zap paths
3. **Cask creation** - Write the .rb file with proper stanzas
4. **Testing** - Audit, style, livecheck, install/uninstall
5. **PR submission** - Branch, commit, push, create PR with AI disclosure

## Pre-flight Checks

Before investing time:

1. **Check for duplicates**: Search existing casks and open PRs

   ```bash
   brew search <name>
   gh pr list -R Homebrew/homebrew-cask --search "<name>"
   ```

2. **Check rejection history**: Some apps are explicitly rejected

   ```bash
   gh issue list -R Homebrew/homebrew-cask --search "<name> is:closed"
   ```

3. **Verify acceptability**: Review `$(brew --repository)/docs/Acceptable-Casks.md`
   - No trial-only software
   - No malware or potentially unwanted programs
   - Must have stable releases

### Token Collisions

When an app name conflicts with an existing cask:

1. Check what the existing cask is: `brew info --cask <name>`
2. If different products (e.g., CLI tool vs GUI app from same vendor), suffix appropriately:
   - GUI app when CLI exists: `<name>-app`
   - Different vendor's product: `<vendor>-<name>`
3. Example: `codex` (CLI) vs `codex-app` (GUI desktop app)

### URL Types

The skill accepts various URL types:

- **Direct download URL** (preferred): `https://example.com/App.dmg`
- **Product/download page**: Will scrape for download links
- **GitHub repo**: Will check releases for download assets
- **No URL**: Will ask for app name and search for download source

If the URL isn't a direct download, first identify the actual installer URL before proceeding with checksum calculation.

## Information Gathering

### 1. Find Download URLs

Look for direct download links on the vendor's website. Check for architecture-specific URLs:

- Apple Silicon (arm64): URLs often contain `arm64`, `aarch64`, `apple`, or `universal`
- Intel (x64/x86_64): URLs often contain `x64`, `x86_64`, `intel`

**Common URL patterns:**

- `/latest` redirects (use `strategy :header_match` for livecheck)
- RELEASES.json feeds (use `strategy :json` for livecheck)
- GitHub releases (use `strategy :github_latest` for livecheck)

### 2. Discover Version Numbers

Try these approaches:

1. Check URL structure - version often in filename
2. Follow `/latest` URLs and inspect redirect:
   ```bash
   curl -sIL "<url>/latest" | grep -i location
   ```
3. Look for RELEASES.json, releases.json, or similar feeds
4. Check app's "About" or website changelog

**Important**: When versions differ by architecture, use `on_arm`/`on_intel` blocks.

### 3. Calculate Checksums

Download and checksum each architecture:

```bash
# ARM64
curl -Lo /tmp/app-arm.dmg "<arm64-url>"
shasum -a 256 /tmp/app-arm.dmg

# Intel
curl -Lo /tmp/app-intel.dmg "<intel-url>"
shasum -a 256 /tmp/app-intel.dmg
```

**Unversioned URLs**: When the download URL doesn't contain version info (always points to latest), use `sha256 :no_check` instead of a checksum.

### 4. Detect Auto-updates

Check if the app self-updates (affects `auto_updates` stanza):

- Look for "Check for Updates" in app menus
- Check for Sparkle framework: `ls "/Applications/<App>.app/Contents/Frameworks" | grep -i sparkle`
- Look for ShipIt (Electron apps): bundle ID contains `.ShipIt`
- Check Info.plist for `SUFeedURL` (Sparkle appcast)

If auto-updates exist, add `auto_updates true` to the cask.

### 5. Discover Zap Paths

Use the `brew createzap` helper (requires tapping first):

```bash
brew tap nrlquaker/createzap
brew createzap "<app-name>"
brew createzap "com.example.bundle-id"  # Try bundle ID if app name fails
```

**Important**: Ask the user to launch the app and use it briefly before running `createzap` a second time. This ensures runtime files (caches, preferences, logs) are created and captured.

**Manual discovery** (if createzap fails):

```bash
# Search common paths
sudo find ~/Library -iname "*<app-name>*" 2>/dev/null
sudo find ~/Library -iname "*<bundle-id>*" 2>/dev/null
```

Common locations:

- `~/Library/Application Support/<app-or-vendor>/`
- `~/Library/Caches/<bundle-id>/`
- `~/Library/Preferences/<bundle-id>.plist`
- `~/Library/Saved Application State/<bundle-id>.savedState/`
- `~/Library/Logs/<app-name>/`
- `~/Library/HTTPStorages/<bundle-id>/`

#### Shared Configuration Directories

Some apps share config directories with related tools (e.g., GUI app + CLI tool). Check if paths like `~/.appname` are used by other casks:

```bash
grep -r "~/\.<appname>" "$(brew --repository homebrew/cask)/Casks/"
```

If shared, add a comment and exclude from zap:

```ruby
zap trash: [
  # "~/.appname", # Shared with appname CLI cask
  "~/Library/Application Support/AppName",
  ...
]
```

## Cask Structure

### Basic Template

```ruby
cask "<token>" do
  version "<version>"
  sha256 "<checksum>"

  url "<download-url>"
  name "<Full App Name>"
  desc "<One-line description>"
  homepage "<homepage-url>"

  livecheck do
    url "<livecheck-url>"
    strategy :<strategy>
  end

  auto_updates true  # if applicable
  depends_on macos: ">= :<minimum-version>"  # if applicable

  app "<App Name>.app"

  zap trash: [
    # paths here
  ]
end
```

### Unversioned Download URLs

When the download URL doesn't contain version info (always points to latest):

```ruby
version "1.2.3"
sha256 :no_check  # URL doesn't include version

url "https://example.com/download/App.dmg",
    verified: "example.com/download/"
```

For Sparkle livecheck with unversioned URLs, use `&:short_version` to return only the display version (not build number):

```ruby
livecheck do
  url "https://example.com/appcast.xml"
  strategy :sparkle, &:short_version
end
```

### Architecture-Specific Versions

When ARM and Intel have different versions:

```ruby
cask "<token>" do
  arch arm: "arm64", intel: "x64"

  on_arm do
    version "<arm-version>"
    sha256 "<arm-checksum>"
  end
  on_intel do
    version "<intel-version>"
    sha256 "<intel-checksum>"
  end

  url "https://example.com/app/#{arch}/App-v#{version}.dmg"
  # ... rest of cask
end
```

### URL Verification

When download domain differs from homepage, add `verified:`:

```ruby
url "https://cdn.example.com/downloads/app.dmg",
    verified: "cdn.example.com/downloads/"
```

## Livecheck Configuration

Choose the appropriate strategy based on how versions are published. See `references/livecheck-strategies.md` in this skill's directory for detailed patterns.

**Quick reference:**

| Source Type               | Strategy         |
| ------------------------- | ---------------- |
| `/latest` redirect URL    | `:header_match`  |
| JSON feed (RELEASES.json) | `:json`          |
| GitHub releases           | `:github_latest` |
| Sparkle appcast           | `:sparkle`       |
| HTML page with links      | `:page_match`    |

## Testing Checklist

### 1. Manual Testing (install/uninstall)

```bash
export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_FROM_API=1

# Test installation - verify app works
brew install --cask <cask-name>

# Test uninstallation
brew uninstall --cask <cask-name>

unset HOMEBREW_NO_AUTO_UPDATE HOMEBREW_NO_INSTALL_FROM_API
```

### 2. Automated Checks (audit, style, livecheck)

Use the `scripts/test-cask` helper in this skill's directory, or run manually:

```bash
export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_FROM_API=1
brew audit --cask --new <cask-name>
brew style --fix <cask-name>
brew livecheck --cask <cask-name>
unset HOMEBREW_NO_AUTO_UPDATE HOMEBREW_NO_INSTALL_FROM_API
```

## PR Submission

### Git Setup

Before pushing, verify remotes to ensure pushing to your fork (not the main Homebrew repo):

```bash
cd "$(brew --repository homebrew/cask)"
git remote -v
```

The main Homebrew repo is typically `origin`. Identify your fork's remote name (e.g., your GitHub username).

### Prepare the Branch

```bash
cd "$(brew --repository homebrew/cask)"
git checkout main
git pull origin main
git checkout -b <cask-name>
git add Casks/<first-letter>/<cask-name>.rb
git commit -m "<cask-name> <version> (new cask)"
```

### Push and Create PR

Push to your fork (not origin):

```bash
git push -u <your-fork-remote> <cask-name>
```

Before creating the PR, read the template at `$(brew --repository homebrew/cask)/.github/PULL_REQUEST_TEMPLATE.md`. Use the template verbatim as the PR body, checking boxes for completed items.

### PR Checklist Verification

Before checking boxes in the PR template, ensure these were actually run:

- `brew audit --cask --online <cask-name>` - Required for all cask changes
- `brew audit --cask --new <cask-name>` - Required for new casks
- `brew style --fix <cask-name>` - Must report no offenses
- `HOMEBREW_NO_INSTALL_FROM_API=1 brew install --cask <cask-name>` - Must succeed
- `brew uninstall --cask <cask-name>` - Must succeed

### AI Disclosure

The PR template requires AI disclosure. Use this format:

```markdown
## AI Disclosure

I have a skill that automates my standard cask creation workflow: gathering app info
(version, bundle ID, min macOS), checking for auto-update frameworks, finding zap paths,
writing the cask file, and running all the standard tests (audit, style, livecheck,
install/uninstall). I supervised the process throughout.
```

## Common Issues and Solutions

### Different versions per architecture

Use `on_arm`/`on_intel` blocks with arch-specific `version` and `sha256`.

### Livecheck not finding versions

- Debug with `brew livecheck --debug --cask <cask-name>`
- Try different strategies or URLs
- For `/latest` URLs, use `:header_match`
- For JSON feeds, use `:json` with appropriate block
- For unversioned URLs with Sparkle, use `&:short_version`

### Audit failures

- Read error messages carefully - they're usually specific
- `verified:` needed when URL domain != homepage domain
- Use glob `*` instead of specific versions in zap paths (e.g., `sfl*` not `sfl2`)
- "Download does not require additional version components" → use `&:short_version` in Sparkle livecheck

### PR review feedback

Common reviewer requests:

- More specific livecheck strategy
- Additional zap paths
- Better description wording
- Architecture handling improvements
