---
name: tmuxinator
description: Use when creating, editing, or debugging tmuxinator project configurations, setting up complex tmux session layouts, or automating development environment startup with multiple windows and panes
---

# Tmuxinator

## Overview

Tmuxinator manages complex tmux sessions through YAML configuration files. Define windows, panes, layouts, and startup commands once, then launch reproducible development environments with a single command.

## When to Use

- Setting up multi-window/pane development environments
- Automating project-specific terminal layouts
- Creating reproducible tmux sessions across machines
- Debugging tmuxinator configuration issues

**Not for:** Simple single-window sessions (just use `tmux` directly)

## Quick Reference

| Command | Alias | Purpose |
|---------|-------|---------|
| `tmuxinator new PROJECT` | `n` | Create/edit project config |
| `tmuxinator new --local PROJECT` | - | Create `.tmuxinator.yml` in current dir |
| `tmuxinator start PROJECT` | `s` | Launch session |
| `tmuxinator start PROJECT -n NAME` | - | Launch with custom session name |
| `tmuxinator start PROJECT --append` | - | Append windows to current session |
| `tmuxinator stop PROJECT` | - | Kill session |
| `tmuxinator stop-all` | - | Kill all tmuxinator sessions |
| `tmuxinator list` | `l`, `ls` | List all projects |
| `tmuxinator copy OLD NEW` | `c`, `cp` | Duplicate config |
| `tmuxinator delete PROJECT` | `rm` | Remove config |
| `tmuxinator debug PROJECT` | - | Show generated shell commands |
| `tmuxinator doctor` | - | Diagnose issues |

## Configuration Locations

1. `~/.tmuxinator/PROJECT.yml` (default)
2. `$XDG_CONFIG_HOME/tmuxinator/PROJECT.yml`
3. `$TMUXINATOR_CONFIG/PROJECT.yml`
4. `.tmuxinator.yml` in project root (local config)

## Complete Configuration Reference

### Project Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `name` | string | required | Session name (no periods allowed) |
| `root` | string | `~/` | Base directory for all windows |
| `socket_name` | string | - | Custom tmux socket name |
| `attach` | boolean | `true` | Auto-attach to session after creation |
| `startup_window` | string/int | first | Window to select on startup (name or index) |
| `startup_pane` | int | `0` | Pane to select within startup window |
| `tmux_options` | string | - | Options passed to tmux (e.g., `-f ~/.tmux.alt.conf`) |
| `tmux_command` | string | `tmux` | Alternative command (e.g., `byobu`) |
| `pre_window` | string/list | - | Commands run before each pane's commands |
| `enable_pane_titles` | boolean | `false` | Show pane titles (tmux 2.6+) |
| `pane_title_position` | string | - | Title position: `top`, `bottom`, or `off` |
| `pane_title_format` | string | - | Custom pane title format string |

### Lifecycle Hooks

| Hook | When It Runs |
|------|--------------|
| `on_project_start` | Every session start, before windows created |
| `on_project_first_start` | Only on initial session creation |
| `on_project_restart` | When reattaching to existing session |
| `on_project_exit` | When detaching from session |
| `on_project_stop` | When `tmuxinator stop` is called |
| `pre_window` | Before each pane's commands (use for env setup) |

All hooks accept a string or list of strings:

```yaml
on_project_start:
  - docker-compose up -d
  - redis-server --daemonize yes
```

### Window Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `layout` | string | - | Pane layout (see Layout Options) |
| `root` | string | project root | Override working directory for this window |
| `panes` | list | - | List of pane definitions |
| `synchronize` | string | - | Sync pane input: `before` or `after` |

### Pane Options

| Option | Type | Description |
|--------|------|-------------|
| `pane_title` | string | Title for this pane (requires `enable_pane_titles`) |
| `commands` | list | Commands to run (alternative to inline list) |

### Layout Options

| Layout | Description |
|--------|-------------|
| `even-horizontal` | Panes spread left-to-right, equal width |
| `even-vertical` | Panes spread top-to-bottom, equal height |
| `main-horizontal` | Large pane on top, others spread below |
| `main-vertical` | Large pane on left, others spread right |
| `tiled` | Even grid of panes |

Control main pane size:
- `main_pane_width`: columns or percentage for main-vertical
- `main_pane_height`: rows or percentage for main-horizontal

Custom layouts use tmux's layout string format (copy from `tmux list-windows`).

## Full Example Configuration

```yaml
# Required
name: myproject

# Project root (default: ~/)
root: ~/Code/myproject

# Optional: custom tmux socket
socket_name: myproject

# Optional: pass options to tmux command
tmux_options: -f ~/.tmux.custom.conf

# Optional: use alternative tmux (e.g., byobu)
tmux_command: tmux

# Optional: auto-attach to session (default: true)
attach: true

# Optional: select specific window/pane on startup
startup_window: editor
startup_pane: 1

# Optional: pane titles (tmux 2.6+)
enable_pane_titles: true
pane_title_position: top
pane_title_format: " #T "

# Lifecycle hooks
on_project_start: docker-compose up -d
on_project_first_start: npm install
on_project_restart: echo "Welcome back"
on_project_exit: docker-compose stop
on_project_stop: docker-compose down

# Run before every pane command (env managers, etc.)
pre_window: nvm use 18

# Windows
windows:
  # Simple: window name with single command
  - server: bundle exec rails s

  # Window with layout and multiple panes
  - editor:
      layout: main-vertical
      # Synchronize pane input ('before' or 'after' pane creation)
      synchronize: after
      panes:
        - vim .
        - guard
        - # empty pane (just shell)

  # Window with custom root
  - frontend:
      root: ~/Code/myproject/client
      panes:
        - npm start
        - npm run test -- --watch

  # Pane with multiple sequential commands
  - backend:
      panes:
        -
          - cd api
          - source venv/bin/activate
          - python manage.py runserver

  # Named panes with titles
  - monitoring:
      panes:
        - pane_title: "Logs"
          commands:
            - tail -f logs/app.log
        - pane_title: "System"
          commands:
            - htop
```

## Dynamic Configuration (ERB)

Configs are processed as ERB templates before YAML parsing:

```yaml
# Environment variables
root: <%= ENV["PROJECT_DIR"] || "~/Code/default" %>
name: <%= ENV["USER"] %>-dev

# Command-line arguments: tmuxinator start myproject arg1 arg2
# Access via @args array (positional)
root: <%= @args[0] %>

# Key-value arguments: tmuxinator start myproject env=prod db=mysql
# Access via @settings hash
<% if @settings["env"] == "production" %>
root: /var/www/app
<% else %>
root: ~/Code/app
<% end %>

# Conditional windows
windows:
  - main: vim
<% if @settings["with_docker"] %>
  - docker: docker-compose logs -f
<% end %>
```

## Window and Pane Patterns

**Simple window with command:**
```yaml
windows:
  - server: npm run dev
```

**Window with multiple panes:**
```yaml
windows:
  - dev:
      panes:
        - vim
        - npm run watch
        - npm run test -- --watch
```

**Pane with sequential commands (send-keys style):**
```yaml
windows:
  - build:
      panes:
        - # Commands sent sequentially
          - cd backend
          - source venv/bin/activate
          - python manage.py runserver
```

**Per-window root override:**
```yaml
windows:
  - frontend:
      root: ~/Code/myproject/frontend
      panes:
        - npm start
```

**Synchronized panes (same input to all):**
```yaml
windows:
  - cluster:
      synchronize: after
      panes:
        - ssh server1
        - ssh server2
        - ssh server3
```

**Named panes with titles (tmux 2.6+):**
```yaml
enable_pane_titles: true
pane_title_position: top

windows:
  - main:
      panes:
        - pane_title: "Editor"
          commands:
            - vim
        - pane_title: "Tests"
          commands:
            - npm test
```

## Common Patterns

### Full-Stack Development

```yaml
name: fullstack
root: ~/Code/myapp

on_project_start:
  - docker-compose up -d postgres redis

on_project_stop:
  - docker-compose down

pre_window: nvm use 18

windows:
  - editor:
      layout: main-vertical
      panes:
        - vim .
        - lazygit
  - backend:
      root: ~/Code/myapp/api
      panes:
        - npm run dev
        - npm run test -- --watch
  - frontend:
      root: ~/Code/myapp/web
      panes:
        - npm start
        - # empty for commands
  - services:
      panes:
        - docker-compose logs -f
        - htop
```

### Remote Development (SSH)

```yaml
name: remote-dev
root: ~

windows:
  - remote:
      panes:
        - # Use array for SSH commands
          - ssh user@server
          - cd /var/www/app
          - vim .
```

### Microservices

```yaml
name: microservices
root: ~/Code

windows:
  - api-gateway:
      root: ~/Code/gateway
      panes:
        - npm run dev
  - users-service:
      root: ~/Code/users
      panes:
        - npm run dev
  - orders-service:
      root: ~/Code/orders
      panes:
        - npm run dev
  - logs:
      layout: tiled
      panes:
        - docker logs -f gateway
        - docker logs -f users
        - docker logs -f orders
```

### Environment-Aware Config

```yaml
name: app-<%= @settings["env"] || "dev" %>
root: <%= @settings["env"] == "prod" ? "/var/www/app" : "~/Code/app" %>

<% if @settings["env"] == "prod" %>
attach: false
on_project_start: sudo systemctl start nginx
<% end %>

windows:
  - app:
      panes:
        - <%= @settings["env"] == "prod" ? "tail -f /var/log/app.log" : "npm run dev" %>
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Window names reset | Add `export DISABLE_AUTO_TITLE=true` to shell rc |
| Commands truncated | Move long commands to scripts, source them |
| Project name invalid | Remove periods from name (tmux uses `.` as delimiter) |
| Layout inconsistent | Use `tmuxinator debug PROJECT` to see generated script |
| Session exists error | Use `tmuxinator stop PROJECT` first, or `-n` for new name |
| Panes not in order | Layouts applied after creation; order may shift |
| rbenv/nvm not loading | Use `pre_window` to set version before commands |
| Hooks not running | Check hook names (deprecated `pre`/`post` → `on_project_*`) |

## Debugging

```bash
# Show what tmuxinator will execute
tmuxinator debug myproject

# Check for configuration issues
tmuxinator doctor

# Verify YAML syntax
ruby -ryaml -e "YAML.load_file('~/.tmuxinator/myproject.yml')"

# Test ERB processing
ruby -rerb -ryaml -e "puts ERB.new(File.read('~/.tmuxinator/myproject.yml')).result"
```

## Installation

```bash
# Preferred (requires Ruby)
gem install tmuxinator

# Alternative
brew install tmuxinator
```

Requires tmux 1.8+ (avoid 2.5 due to bugs). Shell completions available in the GitHub repo's `completion/` directory.
