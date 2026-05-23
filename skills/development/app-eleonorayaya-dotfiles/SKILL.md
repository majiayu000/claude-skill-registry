---
name: app
description: Create, modify, and manage shizuku app configurations. Use when the user wants to create a new app, add template files to an app, or modify existing app structure.
---

# Shizuku App Manager

This skill helps create and manage shizuku application configurations.

## What This Skill Does

When invoked, this skill helps you:
1. **Scaffold new apps** - Create complete directory structure and registration
2. **Add template files** - Create and manage .tmpl files in app contents
3. **Modify existing apps** - Update app configurations and template data
4. **Add installer logic** - Implement Install() method for Homebrew packages

## App Structure Overview

Each shizuku app follows this pattern:

```
apps/{appName}/
├── {appName}.go           # App struct with methods
└── contents/              # Template files and assets (optional)
    ├── file.conf          # Regular files (copied as-is)
    └── file.tmpl          # Go templates (processed)
```

## Modern App Architecture

Apps use an **interface-based design** with optional capabilities:

### Core Interface (Required)
All apps must implement the `App` interface:
- `Name() string` - Returns the app name
- `Enabled(config *shizukuconfig.Config) bool` - Checks if app is enabled

### Optional Interfaces
Apps can optionally implement:
- `FileSyncer` - For apps that sync configuration files
  - `Sync(outDir string, config *shizukuconfig.Config) error`
- `Installer` - For apps that need installation
  - `Install(config *shizukuconfig.Config) error`
- `EnvProvider` - For apps that provide environment variables/aliases
  - `Env() (*shizukuapp.EnvSetup, error)`

## Creating a New App

### Step 1: Gather Requirements

Ask the user:
1. **App name** - What is the name of the application? (e.g., "tmux", "alacritty")
2. **Default enabled** - Should this app be enabled by default? (most apps: true, optional services: false)
3. **Installation** - Does the app need installation via Homebrew? (y/n)
   - If yes: package name, cask vs formula, any taps needed?
4. **File syncing** - Does the app need to sync configuration files? (y/n)
   - If yes: destination path (e.g., "~/.config/tmux/")
5. **Template data** - Does the app need any template variables? (y/n)
6. **Remote files** - Does the app need to download any remote resources like plugins? (y/n)
7. **Environment** - Does the app need environment variables or aliases? (y/n)

### Step 2: Create Directory Structure

```bash
mkdir -p apps/{appName}
# Only create contents/ if the app will sync files
mkdir -p apps/{appName}/contents
```

### Step 3: Create the Go File

Create `apps/{appName}/{appName}.go` with the appropriate template:

#### Minimal App (No File Syncing)

```go
package {appName}

import (
	"github.com/eleonorayaya/shizuku/internal/shizukuconfig"
)

type App struct{}

func New() *App {
	return &App{}
}

func (a *App) Name() string {
	return "{appName}"
}

func (a *App) Enabled(config *shizukuconfig.Config) bool {
	return config.GetAppConfigBool(a.Name(), "enabled", {defaultEnabled})
}
```

#### App with Installation

```go
package {appName}

import (
	"fmt"

	"github.com/eleonorayaya/shizuku/internal/shizukuconfig"
	"github.com/eleonorayaya/shizuku/internal/util"
)

type App struct{}

func New() *App {
	return &App{}
}

func (a *App) Name() string {
	return "{appName}"
}

func (a *App) Enabled(config *shizukuconfig.Config) bool {
	return config.GetAppConfigBool(a.Name(), "enabled", {defaultEnabled})
}

func (a *App) Install(config *shizukuconfig.Config) error {
	// For Homebrew formula
	if err := util.InstallBrewPackage("{packageName}"); err != nil {
		return fmt.Errorf("failed to install {packageName}: %w", err)
	}

	// For Homebrew cask
	// if err := util.InstallCask("{caskName}"); err != nil {
	//     return fmt.Errorf("failed to install {caskName}: %w", err)
	// }

	// For custom tap
	// if err := util.AddTap("{tapName}"); err != nil {
	//     return fmt.Errorf("failed to add tap: %w", err)
	// }

	return nil
}
```

#### App with File Syncing

```go
package {appName}

import (
	"fmt"

	"github.com/eleonorayaya/shizuku/internal/shizukuapp"
	"github.com/eleonorayaya/shizuku/internal/shizukuconfig"
)

type App struct{}

func New() *App {
	return &App{}
}

func (a *App) Name() string {
	return "{appName}"
}

func (a *App) Enabled(config *shizukuconfig.Config) bool {
	return config.GetAppConfigBool(a.Name(), "enabled", {defaultEnabled})
}

func (a *App) Sync(outDir string, config *shizukuconfig.Config) error {
	data := map[string]any{}

	fileMap, err := shizukuapp.GenerateAppFiles("{appName}", data, outDir)
	if err != nil {
		return fmt.Errorf("failed to generate app files: %w", err)
	}

	if err := shizukuapp.SyncAppFiles(fileMap, "{destinationPath}"); err != nil {
		return fmt.Errorf("failed to sync app files: %w", err)
	}

	return nil
}
```

#### App with Remote Files

```go
func (a *App) Sync(outDir string, config *shizukuconfig.Config) error {
	data := map[string]any{}

	fileMap, err := shizukuapp.GenerateAppFiles("{appName}", data, outDir)
	if err != nil {
		return fmt.Errorf("failed to generate app files: %w", err)
	}

	remoteFiles := map[string]string{
		"plugins/file.wasm": "https://example.com/file.wasm",
	}
	pluginMap, err := internal.FetchRemoteAppFiles(outDir, "{appName}", remoteFiles)
	if err != nil {
		return fmt.Errorf("failed to fetch remote files: %w", err)
	}
	maps.Copy(fileMap, pluginMap)

	if err := shizukuapp.SyncAppFiles(fileMap, "{destinationPath}"); err != nil {
		return fmt.Errorf("failed to sync app files: %w", err)
	}

	return nil
}
```

**Note:** If using `maps.Copy`, add import: `"maps"`

#### App with Environment Variables

```go
func (a *App) Env() (*shizukuapp.EnvSetup, error) {
	return &shizukuapp.EnvSetup{
		Variables: []shizukuapp.EnvVar{
			{Key: "EDITOR", Value: "nvim"},
		},
		Aliases: []shizukuapp.Alias{
			{Name: "vim", Command: "nvim"},
		},
	}, nil
}
```

### Step 4: Register the App

1. Open `apps/app.go`
2. Add import: `"github.com/eleonorayaya/shizuku/apps/{appName}"`
3. Add to the return slice in `GetApps()`:
   ```go
   {appName}.New(),
   ```

**IMPORTANT:** Apps are registered in `apps/app.go`, NOT in `cmd/sync/sync.go` or `cmd/install/install.go`. Those commands automatically load all apps via `apps.GetApps()`.

### Step 5: Build and Test

```bash
task build
task run -- list        # Verify app appears
task run -- install     # Test installation (if implemented)
task run -- sync        # Test file syncing (if implemented)
```

## Configuration System

### Checking if App is Enabled

All apps implement `Enabled()` which checks the config:

```go
func (a *App) Enabled(config *shizukuconfig.Config) bool {
	return config.GetAppConfigBool(a.Name(), "enabled", true)  // default: true
}
```

- Most apps default to `true` (core functionality)
- Optional services default to `false` (protonpass, protonvpn, sfsymbols)

### User Config Example

Users can control apps in `~/.config/shizuku/shizuku.yml`:

```yaml
apps:
  nvim:
    enabled: false
  terraform:
    enabled: false
  protonpass:
    enabled: true
```

### Using Other Config Values

Use `config.GetAppConfigBool()` for boolean values:

```go
useNerdFont := config.GetAppConfigBool(a.Name(), "nerd_font", true)
```

Use `config.GetAppConfig()` for other types:

```go
theme, ok := config.GetAppConfig(a.Name(), "theme")
if ok {
	themeStr, ok := theme.(string)
	if ok {
		data["Theme"] = themeStr
	}
}
```

## Adding Template Files

When the user wants to add configuration files to an app:

1. **Ask for file path** - Relative to contents/ directory (e.g., "config.conf")
2. **Ask if it's a template** - Does it need variable substitution? (y/n)
3. **Create the file** - If template, use `.tmpl` extension
4. **Update template data** - If template, add necessary variables to the `data` map in the Sync method

### Template Example

If creating `contents/config.conf.tmpl`:
```
# {{ .AppName }} Configuration
theme = "{{ .Theme }}"
```

Update the Sync method:
```go
data := map[string]any{
	"AppName": "MyApp",
	"Theme":   "monade",
}
```

## Modifying Existing Apps

When modifying an app:
1. **Read the current Go file** to understand existing structure
2. **List contents/** to see existing files (if applicable)
3. **Make requested changes** while preserving the app pattern
4. **Ensure all required interfaces are still implemented**

## Important Notes

- **No comments** - Don't add comments unless explicitly requested (per CLAUDE.md)
- **Error wrapping** - Always use `fmt.Errorf("context: %w", err)` pattern
- **Template extension** - `.tmpl` files are processed, extension is removed in output
- **File syncing** - `SyncAppFiles` handles directory creation and file copying
- **App struct** - Always use `type App struct{}` with `New() *App` constructor
- **Interface implementation** - Implement only the interfaces the app needs
- **Registration** - Apps are registered in `apps/app.go`, not in command files

## Installation Utilities

Available Homebrew utilities in `internal/util/homebrew.go`:
- `InstallBrewPackage(packageName string) error` - Install formula (auto-checks if exists)
- `InstallCask(caskName string) error` - Install cask (auto-checks if exists)
- `AddTap(tapName string) error` - Add Homebrew tap (auto-checks if exists)
- `BrewPackageExists(packageName string) (bool, error)` - Check if package is installed

All utilities are **idempotent** - safe to call multiple times.

## Workflow

1. Use TodoWrite to track the scaffolding steps
2. Ask clarifying questions using AskUserQuestion
3. Create all necessary files
4. Update `apps/app.go` registration
5. Suggest running `task build` and `task run -- list` to verify

## Examples

### Simple App (Installation Only)
- App: rust
- Default enabled: true
- Installation: `InstallBrewPackage("rustup")`
- No file syncing

### App with File Syncing
- App: nvim
- Default enabled: true
- Installation: `InstallBrewPackage("neovim")`
- Syncs to: ~/.config/nvim/
- Provides: Environment variables (EDITOR=nvim, alias vim=nvim)

### Optional Service App
- App: protonpass
- Default enabled: false
- Installation: `InstallCask("proton-pass")`
- No file syncing

### App with Templates
- App: sketchybar
- Default enabled: true
- Installation: Tap + formula
- Syncs to: ~/.config/sketchybar/
- Templates: Uses {{ .Theme }} and other variables

### App with Remote Files
- App: zellij
- Default enabled: true
- Installation: `InstallBrewPackage("zellij")`
- Syncs to: ~/.config/zellij/
- Remote: Downloads zjstatus.wasm plugin from GitHub

### App with Custom Installer
- App: kitty
- Default enabled: true
- Installation: Uses curl installation script (not Homebrew)
- Syncs to: ~/.config/kitty/
