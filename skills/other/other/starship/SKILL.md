---
name: starship
description: >-
  You are an expert in Starship, the minimal, blazing-fast, cross-shell
  prompt written in Rust. You help developers customize their terminal prompt
  with git status, language versions, cloud context, battery level, time, and
  custom modules — working identically across Bash, Zsh, Fish, PowerShell, and
  any shell with a single TOML config file.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: Developer Tools
  tags:
    - terminal
    - prompt
    - shell
    - customization
    - rust
    - fast
    - cross-shell
---

# Starship — Cross-Shell Prompt

You are an expert in Starship, the minimal, blazing-fast, cross-shell prompt written in Rust. You help developers customize their terminal prompt with git status, language versions, cloud context, battery level, time, and custom modules — working identically across Bash, Zsh, Fish, PowerShell, and any shell with a single TOML config file.

## Core Capabilities

### Configuration

```toml
# ~/.config/starship.toml
format = """
$username\
$hostname\
$directory\
$git_branch\
$git_status\
$nodejs\
$python\
$rust\
$golang\
$docker_context\
$kubernetes\
$aws\
$terraform\
$cmd_duration\
$line_break\
$character"""

[character]
success_symbol = "[❯](bold green)"
error_symbol = "[❯](bold red)"

[directory]
truncation_length = 3
truncate_to_repo = true
style = "bold cyan"

[git_branch]
symbol = "🌿 "
style = "bold purple"

[git_status]
conflicted = "⚔️ "
ahead = "⇡${count} "
behind = "⇣${count} "
diverged = "⇕⇡${ahead_count}⇣${behind_count} "
untracked = "?${count} "
stashed = "📦 "
modified = "!${count} "
staged = "+${count} "
deleted = "✘${count} "

[nodejs]
symbol = "⬢ "
detect_files = ["package.json", ".nvmrc"]
style = "bold green"

[python]
symbol = "🐍 "
detect_extensions = ["py"]
style = "bold yellow"

[rust]
symbol = "🦀 "
style = "bold red"

[docker_context]
symbol = "🐳 "
only_with_files = true

[kubernetes]
disabled = false
symbol = "☸ "
detect_files = ["k8s", "kubernetes"]

[aws]
symbol = "☁️ "
format = '[$symbol($profile )(\($region\))]($style)'

[cmd_duration]
min_time = 2000                           # Show if command took >2s
format = "took [$duration]($style) "
style = "bold yellow"

[time]
disabled = false
format = "🕐 [$time]($style) "
time_format = "%H:%M"

# Custom module
[custom.docker_running]
command = "docker ps -q | wc -l | tr -d ' '"
when = "docker ps -q"
symbol = "🐳 "
format = "[$symbol$output containers]($style) "
style = "blue"
```

## Installation

```bash
# macOS
brew install starship

# Linux
curl -sS https://starship.rs/install.sh | sh

# Add to shell:
# Bash: eval "$(starship init bash)" >> ~/.bashrc
# Zsh: eval "$(starship init zsh)" >> ~/.zshrc
# Fish: starship init fish | source >> ~/.config/fish/config.fish
```

## Best Practices

1. **Cross-shell** — Same config works in Bash, Zsh, Fish, PowerShell; switch shells without reconfiguring
2. **Lazy detection** — Modules only show when relevant (Node.js only in JS projects); clean prompt by default
3. **Git status at a glance** — Shows ahead/behind, modified, staged, untracked counts inline
4. **Command duration** — Set `min_time = 2000` to show timing for slow commands; helps identify bottlenecks
5. **Cloud context** — Show AWS profile, K8s context, Terraform workspace; never deploy to wrong environment
6. **Custom modules** — Use `[custom.name]` for any shell command output; docker containers, VPN status, etc.
7. **Presets** — Start with a preset: `starship preset nerd-font-symbols -o ~/.config/starship.toml`
8. **Performance** — Written in Rust; renders in <10ms; never slows down your terminal
