---
name: macos-brew
cluster: macos
description: "Homebrew: formulae, casks, services, taps, PATH /opt/homebrew, pin versions, bundle"
tags: ["homebrew","brew","packages","macos"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "homebrew brew install package macos formula cask tap"
---

## Purpose

This skill automates Homebrew operations on macOS, enabling efficient management of software packages, including formulae, casks, services, taps, and version pinning. It focuses on core Homebrew features to handle package installation, updates, and system integration via the /opt/homebrew PATH.

## When to Use

Use this skill for macOS package management tasks, such as installing dependencies in scripts, updating tools in CI/CD pipelines, or configuring development environments. Apply it when dealing with Homebrew-specific features like casks for GUI apps or taps for custom repositories, especially in automated workflows or when ensuring reproducible setups.

## Key Capabilities

- **Formulae Management**: Install, upgrade, or remove command-line tools (e.g., via `brew install wget`), including dependency resolution and version pinning using `brew pin <formula>`.
- **Casks Handling**: Manage GUI applications (e.g., `brew install --cask google-chrome`), with options to ignore dependencies or force reinstalls.
- **Services Control**: Start, stop, or restart background services (e.g., `brew services start postgresql`), integrating with macOS launchd.
- **Taps Integration**: Add external repositories (e.g., `brew tap homebrew/cask`), enabling access to non-core packages.
- **PATH and Bundle Management**: Configure /opt/homebrew in PATH for scripts, and use `brew bundle` to manage package lists from a Brewfile for reproducible environments.
- **Version Pinning**: Lock package versions to prevent updates (e.g., `brew pin node@14`), ensuring stability in production setups.

## Usage Patterns

Invoke this skill in shell scripts or automation tools by calling `brew` commands directly. Always check for Homebrew installation first using `which brew` or `command -v brew`. For scripted installs, use a Brewfile: create a file with lines like `brew 'git'` and `cask 'docker'`, then run `brew bundle --file Brewfile`. In AI agents, wrap commands in try-catch blocks for error handling, and export PATH with `/opt/homebrew/bin` prepended. Example: In a bash script, install and pin a package like this:

```bash
brew install node@14
brew pin node@14
```

Another pattern: For services, combine with conditional checks, e.g., only start if not running: `brew services list | grep -q postgresql || brew services start postgresql`.

## Common Commands/API

Homebrew is CLI-based, so use these commands directly in scripts. All commands run via `brew <subcommand> [flags] [args]`.

- **Install Formula**: `brew install <formula> --force` to overwrite existing; e.g., `brew install git --force`.
- **Install Cask**: `brew install --cask <cask> --no-quarantine` to skip macOS security prompts; e.g., `brew install --cask visual-studio-code --no-quarantine`.
- **Update Packages**: `brew update && brew upgrade <formula>`; add `--ignore-pinned` to upgrade pinned versions.
- **Manage Taps**: `brew tap <user/repo>` to add a tap; e.g., `brew tap homebrew/cask-fonts`.
- **Handle Services**: `brew services start <service>` or `brew services restart <service> --all`; e.g., `brew services stop redis`.
- **Bundle Operations**: `brew bundle --file Brewfile` to install from a file; Brewfile format: `brew 'package'` or `cask 'app'`.
- **Pin Versions**: `brew pin <formula>` to pin; `brew unpin <formula>` to release; e.g., `brew pin python@3.9`.
- **Cleanup**: `brew cleanup -s` to remove old versions; always run after upgrades.

For API-like usage, pipe outputs to scripts, e.g., `brew list --versions | grep node` to query installed versions.

## Integration Notes

Integrate Homebrew into scripts by ensuring /opt/homebrew/bin is in PATH; add `export PATH="/opt/homebrew/bin:$PATH"` to .zshrc or scripts. In CI/CD (e.g., GitHub Actions), install Homebrew first with `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`. No authentication is required, but if extending to private taps, use Git credentials via environment variables like `export HOMEBREW_GIT_EMAIL="user@example.com"`. For cross-tool integration, combine with macOS tools: e.g., after `brew install ffmpeg`, use it in Python scripts via subprocess. Config format for Brewfile: plain text with lines like `brew 'jq' # JSON processor`. Always verify Homebrew version with `brew --version` before complex operations.

## Error Handling

Handle common errors by checking exit codes; `brew` commands return non-zero on failure. For "formula not found", use `brew search <formula>` first or install with `brew install <formula> 2>/dev/null || echo "Error: Formula missing"`. If "Permission denied", run with sudo or fix ownership on /opt/homebrew (e.g., `sudo chown -R $(whoami) /opt/homebrew`). For network issues during `brew update`, retry with `brew update --verbose` and check connectivity. In scripts, wrap commands like: 

```bash
if ! brew install git; then
  echo "Installation failed; check logs" >&2
  exit 1
fi
```

Log outputs with `brew install <formula> >> install.log 2>&1`. For version conflicts, use `brew doctor` to diagnose and resolve.

## Concrete Usage Examples

1. **Install and Pin a Development Tool**: To set up a project with a specific Node.js version, run: `brew install node@14` followed by `brew pin node@14`. This ensures the version doesn't auto-update, maintaining consistency.
   
2. **Manage a Service for a Web App**: For a Redis-backed app, start the service with `brew services start redis`, and verify with `brew services list | grep redis`. If it fails, check with `brew doctor` and restart.

## Graph Relationships

- Connected to "macos" cluster for broader macOS tools.
- Relates to "packages" tag, linking to general package managers like apt or yum skills.
- Associated with "homebrew" tag, potentially linking to advanced scripting or CI tools in the ecosystem.
