---
name: workspace-cli
description: Use the workspace-hub unified CLI for repository management, compliance, development tools, and system configuration. Use for navigating workspace tools and executing common operations.
version: 1.1.0
category: workspace-hub
type: skill
capabilities:
  - interactive_menu_navigation
  - repository_management
  - compliance_tools_access
  - development_utilities
  - system_configuration
tools:
  - Bash
  - Read
related_skills:
  - repo-sync
  - compliance-check
  - sparc-workflow
---

# Workspace CLI Skill

> Unified CLI interface for all workspace-hub management tools across 26+ repositories.

## Quick Start

```bash
# Launch interactive menu
./scripts/workspace

# Direct repository sync
./scripts/repository_sync status all

# Quick compliance check
./scripts/compliance/verify_compliance.sh
```

## When to Use

- Starting a work session and need quick access to common tools
- Managing multiple repositories with bulk operations
- Running compliance checks across the workspace
- Accessing development tools and refactoring utilities
- Configuring system settings and remote connections

## Prerequisites

- Access to workspace-hub repository
- Bash shell (Linux/macOS/WSL)
- Scripts marked as executable (`chmod +x ./scripts/workspace`)

## Overview

The Workspace CLI provides a unified interface to all workspace-hub management tools. This skill covers navigation, common operations, and integration with other workspace systems.

## Direct Script Access

```bash
# Repository management
./scripts/repository/configure_repos.sh

# Compliance tools
./scripts/compliance/verify_compliance.sh

# Development tools
./scripts/development/refactor-analysis.sh

# System tools
./scripts/system/sync
```

## Main Menu Structure

```
+================================================================+
|              Workspace Hub - Management Console                 |
+================================================================+

Workspace Management:

  1) Repository Management
  2) Compliance & Standards
  3) Remote Connection Tools
  4) Development Tools
  5) System Setup & Configuration
  6) Help & Documentation

  0) Exit
```

## Execution Checklist

- [ ] Navigate to workspace-hub root directory
- [ ] Verify scripts are executable (`chmod +x ./scripts/workspace`)
- [ ] Launch CLI with `./scripts/workspace`
- [ ] Select appropriate menu category
- [ ] Execute required operation
- [ ] Verify operation success
- [ ] Exit cleanly (option 0)

## Category Details

### 1. Repository Management

Access multi-repository git operations:

```
Repository Management:

  1) Repository Sync Manager       # Full git operations menu
  2) Configure Repository URLs     # Setup GitHub URLs
  3) Check All Repository Status   # Quick status overview

  0) Back to main menu
```

**Common Operations:**

```bash
# List all repositories
./scripts/repository_sync list all

# Sync all work repositories
./scripts/repository_sync sync work -m "Update"

# Pull latest from all repos
./scripts/repository_sync pull all

# Check status
./scripts/repository_sync status all
```

### 2. Compliance & Standards

Enforce coding standards and guidelines:

```
Compliance & Standards:

  1) Propagation Tools            # Spread standards
  2) Compliance Enforcement       # Setup and hooks
  3) Verification Tools           # Check status

  0) Back to main menu
```

**Propagation Tools:**
```bash
# Sync CLAUDE.md to all repos
./scripts/compliance/propagate_claude_config.py

# Sync AI guidelines
./scripts/compliance/propagate_guidelines.sh

# Enable interactive mode
./scripts/compliance/propagate_interactive_mode.sh
```

**Enforcement:**
```bash
# Initial setup
./scripts/compliance/setup_compliance.sh

# Install git hooks
./scripts/compliance/install_compliance_hooks.sh

# Verify compliance
./scripts/compliance/verify_compliance.sh
```

### 3. Remote Connection Tools

Manage remote workspace connections:

```
Remote Connection Tools:

  1) Linux Connection Tools
  2) Windows Connection Tools
  3) Tailscale Connection Tools

  0) Back to main menu
```

**Linux:**
```bash
./scripts/connection/connect-workspace-linux.sh
./scripts/connection/sync-tabby-linux.sh
```

**Windows:**
```powershell
./scripts/connection/connect-workspace-windows.ps1
./scripts/connection/sync-tabby-windows.ps1
```

**Tailscale:**
```bash
./scripts/connection/connect-workspace-tailscale.sh    # Bash
./scripts/connection/connect-workspace-tailscale.ps1   # PowerShell
```

### 4. Development Tools

AI-powered development and code quality:

```
Development Tools:

  1) Factory.ai Tools             # Install Factory.ai
  2) Refactor Analysis            # Code quality analysis
  3) Droid CLI                    # Factory.ai droid wrapper

  0) Back to main menu
```

**Refactor Analysis:**
```bash
# Run full analysis
./scripts/development/refactor-analysis.sh

# Output in .refactor-reports/
```

Analysis includes:
- Code duplication (jscpd)
- Dead code detection (knip)
- Slow test identification
- Large file detection
- Outdated dependencies

**Factory.ai:**
```bash
# Install Factory.ai
./scripts/development/install_factory_ai.sh

# Use droid CLI
./scripts/development/droid --help
```

### 5. System Setup & Configuration

System-level configuration:

```
System Setup & Configuration:

  1) Workspace Sync               # Full workspace sync
  2) Setup XRDP                   # Remote desktop
  3) View System Information      # Workspace stats

  0) Back to main menu
```

**Workspace Sync:**
```bash
./scripts/system/sync
```

Performs:
- Git repository synchronization
- MCP server installation
- UV environment setup
- NPM package management
- Agent configuration

### 6. Help & Documentation

Access documentation and help:

```
Help & Documentation:

  1) Repository Sync Documentation
  2) View README
  3) Available Commands
  4) Quick Start Guide

  0) Back to main menu
```

## Script Organization

```
scripts/
+-- workspace                    # Main CLI entry point
|
+-- repository/                  # Repository management
|   +-- configure_repos.sh
|   +-- check_all_status.sh
|
+-- compliance/                  # Compliance tools
|   +-- propagate_claude_config.py
|   +-- propagate_guidelines.sh
|   +-- propagate_interactive_mode.sh
|   +-- setup_compliance.sh
|   +-- install_compliance_hooks.sh
|   +-- verify_compliance.sh
|
+-- connection/                  # Remote connections
|   +-- connect-workspace-linux.sh
|   +-- connect-workspace-windows.ps1
|   +-- connect-workspace-tailscale.sh
|   +-- connect-workspace-tailscale.ps1
|   +-- sync-tabby-linux.sh
|   +-- sync-tabby-windows.ps1
|
+-- development/                 # Development tools
|   +-- install_factory_ai.sh
|   +-- refactor-analysis.sh
|   +-- droid
|
+-- system/                      # System configuration
    +-- sync
    +-- setup_xrdp.sh
```

## Common Workflows

### Daily Development Start

```bash
# 1. Launch workspace CLI
./scripts/workspace

# 2. Repository Management -> Repository Sync Manager
# 3. Navigate to: Pull -> All
# Or directly:
./scripts/repository_sync pull all
```

### End of Day Sync

```bash
# Sync all work with commit message
./scripts/repository_sync sync work -m "$(date +%Y-%m-%d) updates"
```

### Setup New Repository

```bash
# 1. Configure URLs
./scripts/repository/configure_repos.sh

# 2. Clone repository
./scripts/repository_sync clone <repo-name>

# 3. Setup compliance
./scripts/compliance/setup_compliance.sh
```

### Code Quality Check

```bash
# Run refactor analysis
./scripts/development/refactor-analysis.sh

# Check compliance
./scripts/compliance/verify_compliance.sh
```

### Propagate Standards

```bash
# Update all repos with latest standards
./scripts/compliance/propagate_claude_config.py
./scripts/compliance/propagate_guidelines.sh
./scripts/compliance/propagate_interactive_mode.sh
```

## Error Handling

### Menu Display Issues

```bash
# Check terminal supports ANSI
echo $TERM

# Run with basic terminal
TERM=xterm ./scripts/workspace
```

### Script Not Found

```bash
# Verify workspace root
pwd
# Should be: /mnt/github/workspace-hub

# Make scripts executable
chmod +x ./scripts/workspace
chmod +x ./scripts/*/*.sh
```

### Permission Denied

```bash
# Fix permissions
chmod +x ./scripts/workspace
chmod +x ./scripts/*/*.sh
chmod +x ./scripts/*/*.py
```

### Configuration Missing

```bash
# Run configuration helper
./scripts/repository/configure_repos.sh

# Or edit directly
nano config/repos.conf
```

## Metrics & Success Criteria

- **Navigation Speed**: Access any tool in < 3 menu selections
- **Script Execution**: 100% success rate for available scripts
- **Cross-Platform**: Works on Linux, macOS, WSL
- **Documentation**: All menu options have help text
- **Error Handling**: Clear error messages with recovery steps

## Navigation Tips

### Keyboard Navigation

- **Number keys**: Select menu options
- **0**: Go back / Exit
- **Ctrl+C**: Force exit

### Direct Access

Skip menus with direct commands:

```bash
# Instead of navigating menus
./scripts/workspace

# Use direct script path
./scripts/repository_sync sync all -m "Quick update"
```

### Command Aliases

Add to `.bashrc` or `.zshrc`:

```bash
# Workspace CLI aliases
alias ws='./scripts/workspace'
alias rs='./scripts/repository_sync'
alias rsync='./scripts/repository_sync sync all'
alias rstatus='./scripts/repository_sync status all'
alias rpull='./scripts/repository_sync pull all'
```

## Integration Points

### With Repository Sync

The CLI wraps repository_sync for menu access:

```bash
# Menu access
./scripts/workspace -> 1 -> 1

# Direct access
./scripts/repository_sync <command>
```

### With Compliance System

```bash
# Menu access
./scripts/workspace -> 2 -> 3

# Direct access
./scripts/compliance/verify_compliance.sh
```

### With AI Agents

AI agents can use CLI scripts:

```python
# Run status check
subprocess.run(['./scripts/repository_sync', 'status', 'all'])

# Verify compliance
subprocess.run(['./scripts/compliance/verify_compliance.sh'])
```

### Related Skills

- [repo-sync](../repo-sync/SKILL.md) - Repository synchronization
- [compliance-check](../compliance-check/SKILL.md) - Compliance verification
- [sparc-workflow](../sparc-workflow/SKILL.md) - Development methodology

## Environment Variables

### Supported Variables

```bash
# Default editor for config editing
export EDITOR=vim

# Log level
export LOG_LEVEL=INFO

# Parallel operations
export PARALLEL_JOBS=4
```

### Configuration File

Location: `config/workspace.conf`

```bash
# Workspace configuration
DEFAULT_SYNC_MESSAGE="Workspace sync"
PARALLEL_ENABLED=true
MAX_PARALLEL_JOBS=4
```

## References

- [WORKSPACE_CLI.md](../docs/modules/cli/WORKSPACE_CLI.md)
- [REPOSITORY_SYNC.md](../docs/modules/cli/REPOSITORY_SYNC.md)
- [CLI_MENU_STRUCTURE.md](../docs/modules/cli/CLI_MENU_STRUCTURE.md)

---

## Version History

- **1.1.0** (2026-01-02): Upgraded to SKILL_TEMPLATE_v2 format - added When to Use, Execution Checklist, Error Handling consolidation, Metrics, Integration Points
- **1.0.0** (2024-10-15): Initial release with 6 main categories, script organization, workflows, navigation, troubleshooting
