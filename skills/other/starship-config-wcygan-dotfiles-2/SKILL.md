---
name: starship-config
description: Configure and optimize Starship cross-shell prompt with presets, custom modules, and performance tuning. Use when setting up Starship, creating prompt configs, customizing prompt appearance, or troubleshooting prompt issues. Keywords: starship, prompt, shell prompt, PS1, starship.toml, preset, prompt config, shell theme
---

# Starship Configuration Manager

Manages complete Starship prompt configuration lifecycle including setup, customization, and optimization.

## Instructions

### 1. Understand Context

Check project structure:
- **Config location**: `config/starship/starship.toml` (symlinked to `~/.config/starship.toml`)
- **Existing config**: Read current `starship.toml` if present
- **Shell integration**: Check `config/fish/conf.d/30-starship.fish` for hook
- **Nix package**: Verify starship in `flake.nix`

### 2. Configuration Operations

#### Setup New Config

```toml
# Minimal starting point
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$cmd_duration\
$line_break\
$character"""

[character]
success_symbol = "[➜](bold green)"
error_symbol = "[➜](bold red)"

[directory]
truncation_length = 3
truncate_to_repo = true
```

#### Apply Preset

Available presets: `nerd-font-symbols`, `pure-preset`, `pastel-powerline`, `tokyo-night`, `gruvbox-rainbow`

```bash
# Preview preset
starship preset <preset-name> -o - | less

# Apply preset
starship preset <preset-name> -o ~/.config/starship.toml
```

#### Custom Module Configuration

Common modules to configure:

**Language/Runtime:**
```toml
[golang]
symbol = "🐹 "
format = "via [$symbol($version )]($style)"

[rust]
symbol = "🦀 "
format = "via [$symbol($version )]($style)"

[nodejs]
symbol = "⬢ "
format = "via [$symbol($version )]($style)"

[deno]
symbol = "🦕 "
format = "via [$symbol($version )]($style)"
```

**Git:**
```toml
[git_branch]
symbol = "🌱 "
format = "on [$symbol$branch]($style) "

[git_status]
conflicted = "🏳"
ahead = "⇡${count}"
behind = "⇣${count}"
diverged = "⇕⇡${ahead_count}⇣${behind_count}"
untracked = "🤷"
stashed = "📦"
modified = "📝"
staged = '[++\($count\)](green)'
renamed = "👅"
deleted = "🗑"
```

**Performance:**
```toml
[cmd_duration]
min_time = 500
format = "took [$duration](bold yellow)"

[directory]
read_only = " 🔒"
```

#### Context-Aware Variables

```toml
# Show Kubernetes context when kubectl available
[kubernetes]
disabled = false
format = 'on [⛵ ($context \($namespace\))](dimmed green) '

# Show AWS profile
[aws]
format = 'on [$symbol($profile )]($style)'
symbol = "☁️  "

# Show Docker context
[docker_context]
format = "via [🐋 $context](blue bold)"
```

### 3. Performance Optimization

#### Disable Expensive Modules

```toml
# Disable modules in large repos
[package]
disabled = true

[nodejs]
disabled = true  # Only if not a Node project

# Timeout protection
[cmd_duration]
min_time = 500
show_milliseconds = false

[git_status]
disabled = false
# Limit git operations in large repos
ahead_behind_limit = 1000
```

#### Scan Timeout Configuration

```toml
scan_timeout = 30  # ms, default is 30

[directory]
scan_timeout = 10
```

### 4. Testing Configuration

```bash
# Validate TOML syntax
starship config

# Explain current config
starship explain

# Print configuration value
starship print-config

# Test in isolation
env STARSHIP_CONFIG=./test-config.toml fish
```

### 5. Troubleshooting

**Prompt not appearing:**
- Check shell integration: `config/fish/conf.d/30-starship.fish`
- Verify: `starship init fish | source`
- Confirm starship installed: `type -q starship`

**Slow prompt:**
- Enable timings: `starship timings`
- Disable expensive modules
- Increase scan timeout
- Check git status on large repos

**Modules missing:**
- Verify symbols/fonts: Nerd Font required
- Check module requirements (e.g., `kubectl` for kubernetes module)
- Review `disabled = false` settings

**Config not loading:**
- Check config path: `echo $STARSHIP_CONFIG` (should be unset or correct path)
- Verify symlink: `ls -la ~/.config/starship.toml`
- Validate TOML: `starship config`

### 6. Integration with Dotfiles

**When modifying:**
1. Edit `config/starship/starship.toml`
2. Test with `exec fish -l`
3. Verify symlink active: `ls -la ~/.config/starship.toml`
4. Commit to git if satisfied

**When creating new:**
1. Write to `config/starship/starship.toml`
2. Ensure `scripts/link-config.sh` handles starship symlink
3. Verify link in `~/.config/starship.toml`
4. Add to README if new setup step required

### 7. Output Format

When generating configs:

**Use Edit tool** for existing configs:
- Modify specific sections
- Preserve user customizations
- Add/update modules

**Use Write tool** for new configs:
- Complete working configuration
- Include comments explaining sections
- Follow TOML formatting

**Include testing steps:**
```bash
# Reload shell
exec fish -l

# Verify prompt renders
starship explain

# Check performance
starship timings
```

## Module Priority Guide

**Essential modules** (always include):
- `character` - prompt symbol
- `directory` - current path
- `git_branch`, `git_status` - git info
- `cmd_duration` - command timing

**Language modules** (include based on project):
- Deno/Node projects: `deno`, `nodejs`
- Go projects: `golang`
- Rust projects: `rust`
- Java projects: `java`

**Context modules** (optional):
- `kubernetes` - if using kubectl
- `docker_context` - if using Docker
- `aws` - if using AWS CLI

**Avoid in performance-critical environments:**
- `package` - slow in large node_modules
- Heavy git status in monorepos

## Reference Documentation

- Official config: https://starship.rs/config/
- Advanced config: https://starship.rs/advanced-config/
- Presets gallery: https://starship.rs/presets/

## Project Context

This is a Nix-based dotfiles repository:
- Starship installed via `flake.nix`
- Config lives in `config/starship/starship.toml`
- Symlinked to `~/.config/starship.toml` by `scripts/link-config.sh`
- Fish shell integration in `config/fish/conf.d/30-starship.fish`
- Cross-platform support: macOS, Ubuntu, Fedora
