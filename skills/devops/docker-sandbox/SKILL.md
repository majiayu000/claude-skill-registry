---
name: docker-sandbox
description: Docker sandbox environment management for dotfiles. Use when user mentions "build docker", "start container", "enter shell", "clean container", "check status", "make build", "make shell", "make clean", development environment, or container management.
---

# Docker Sandbox Management

dotfilesをテストするためのDocker開発環境を管理する。

## Available Commands

| Command | Description |
|---------|-------------|
| `make build` | Build Docker image |
| `make start` | Start container in background |
| `make shell` | Attach to container (auto-starts if needed) |
| `make run` | Run temporary container (removed after exit) |
| `make stop` | Stop container |
| `make clean` | Remove container and volume |
| `make status` | Show current worktree status |
| `make list` | List all dotfiles containers |

## Common Workflows

### Initial Setup

```bash
make build   # Build image
make shell   # Enter development environment
```

### Test Configuration Changes

After editing dotfiles on host:

```bash
make shell
# Inside container:
source ~/.zshrc              # Reload zsh
tmux source ~/.tmux.conf     # Reload tmux (inside tmux)
:source $MYVIMRC             # Reload neovim (inside nvim)
```

### Reset Environment

```bash
make clean   # Remove container and volume
make build   # Rebuild image
make shell   # Enter fresh environment
```

## Container Architecture

- **Image**: `dotfiles:{worktree-name}`
- **Container**: `dotfiles-{worktree-name}`
- **Volume**: `dotfiles-{worktree-name}-home` (persists home directory)
- **Mount**: `~/.dotfiles` (read-only)

## Included Tools

- Neovim (stable)
- tmux 3.5
- zsh
- Node.js (latest LTS)
- Python3 + pynvim

## Troubleshooting

### Container won't start

1. Check status: `make status`
2. View logs: `docker logs dotfiles-{worktree-name}`
3. Rebuild: `make clean && make build`

### Changes not reflected

dotfiles are mounted read-only. Edit on host, then reload inside container.
