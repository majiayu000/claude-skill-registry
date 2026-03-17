---
name: dotfiles-manage
description: Manage dotfiles using dotter (symlink manager and templater). Use when deploying, adding, removing, or organizing configuration files in ~/dotfiles.
---

# Manage Dotfiles Skill

Manage dotfiles using [dotter](https://github.com/SuperCuber/dotter) - a dotfile manager and templater.

## Environment

- **Dotfiles repo**: `~/dotfiles`
- **Dotter config**: `~/dotfiles/.dotter/`
  - `global.toml`: Package definitions (files to deploy)
  - `local.toml`: Machine-specific package selection
  - `cache.toml`: Deployment state cache

## Core Commands

```bash
# Deploy all configured files
dotter deploy

# Preview changes without applying
dotter deploy --dry-run

# Undeploy all managed files
dotter undeploy

# Watch for changes and auto-deploy
dotter watch
```

## Workflow: Add New Dotfile

### Step 1: Add Source File

Place the configuration file in `~/dotfiles`:

```bash
# Example: adding a new config
cp ~/.config/app/config.toml ~/dotfiles/.config/app/config.toml
```

### Step 2: Define in global.toml

Add a new package or extend existing one in `~/dotfiles/.dotter/global.toml`:

```toml
# New package
[myapp.files]
".config/app/config.toml" = "~/.config/app/config.toml"

# Or extend existing package
[existing-package.files]
".config/app/config.toml" = "~/.config/app/config.toml"
```

**File mapping format**: `"source" = "target"`
- Source: relative path from dotfiles repo root
- Target: absolute path or `~` for home directory

### Step 3: Enable Package (if new)

Add package to `~/dotfiles/.dotter/local.toml`:

```toml
packages = ["doom", "myapp"]
```

### Step 4: Deploy

```bash
cd ~/dotfiles && dotter deploy
```

## Workflow: Remove Dotfile

1. **Undeploy first**: `dotter undeploy`
2. **Remove from global.toml**: Delete the file mapping
3. **Remove package from local.toml** (if removing entire package)
4. **Redeploy**: `dotter deploy`
5. **Clean up source** (optional): Remove file from dotfiles repo

## Package Organization

Group related files into packages:

```toml
# Shell configuration
[shell.files]
".zshrc" = "~/.zshrc"
".zprofile" = "~/.zprofile"
".config/starship.toml" = "~/.config/starship.toml"

# Editor configuration
[nvim.files]
".config/nvim" = "~/.config/nvim"

# Git configuration
[git.files]
".gitconfig" = "~/.gitconfig"
".gitignore_global" = "~/.gitignore_global"
```

## Templating

Dotter supports Handlebars templating for machine-specific values:

```toml
# In global.toml - define variables
[package.variables]
email = "default@example.com"

# In local.toml - override per machine
[variables]
email = "work@company.com"
```

In template files, use `\{{email}}` syntax.

## Troubleshooting

**Conflict with existing file:**
```bash
# Force overwrite (use with caution)
dotter deploy --force
```

**Check deployment status:**
```bash
dotter deploy --dry-run --verbose
```

**View what's currently deployed:**
```bash
cat ~/dotfiles/.dotter/cache.toml
```

## Best Practices

- Keep packages granular and focused
- Use descriptive package names
- Commit changes to dotfiles repo after modifications
- Test with `--dry-run` before deploying
- Use templating for machine-specific values (email, paths)
