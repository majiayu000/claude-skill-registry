---
name: ai-maestro-agents-management
description: Creates, manages, and orchestrates AI agents using the AI Maestro CLI. Use when the user asks to "create agent", "list agents", "delete agent", "rename agent", "hibernate agent", "wake agent", "install plugin", "show agent", "export agent", "restart agent", "install marketplace", or any agent lifecycle management task.
allowed-tools: Bash
compatibility: Requires AI Maestro (aimaestro.dev) with Bash shell access
metadata:
  author: 23blocks
  version: 2.0.0
---

# AI Maestro Agent Management

## Purpose

Manage AI agents through the AI Maestro CLI. This skill provides commands for creating, updating, deleting, hibernating, and waking agents. It also handles plugin management and agent import/export.

## CRITICAL: This is an Agent Management Skill

**This skill is for managing other agents**, not for inter-agent communication (use `agent-messaging` skill for that).

## CLI Script

**Script:** `aimaestro-agent.sh` (Bash, macOS/Linux)

**Installation:** `./install-agent-cli.sh`

**Requirements:** macOS or Linux, Bash 4.0+, tmux 3.0+, jq, curl

---

## PART 1: AGENT LIFECYCLE

### 1. List Agents

```bash
aimaestro-agent.sh list [--status online|offline|hibernated|all] [--format table|json|names] [-q|--quiet] [--json]
```

Examples: `list`, `list --status online`, `list --format json`, `list -q`

### 2. Show Agent Details

```bash
aimaestro-agent.sh show <agent> [--format pretty|json]
```

### 3. Create Agent

**`--dir` is required.**

```bash
aimaestro-agent.sh create <name> --dir <path> [options] [-- <program-args>...]
```

Options: `-p/--program`, `-m/--model`, `-t/--task`, `--tags`, `--no-session`, `--no-folder`, `--force-folder`

Examples:
```bash
aimaestro-agent.sh create my-api --dir /Users/dev/projects/my-api
aimaestro-agent.sh create backend-service \
  --dir /Users/dev/projects/backend \
  --task "Implement user authentication with JWT" \
  --tags "api,auth,security"
aimaestro-agent.sh create debug-agent --dir /Users/dev/projects/debug -- --verbose --debug
```

### 4. Update Agent

```bash
aimaestro-agent.sh update <agent> [options]
```

Options: `-t/--task`, `-m/--model`, `--tags`, `--add-tag`, `--remove-tag`, `--args`

Examples:
```bash
aimaestro-agent.sh update backend-api --task "Focus on payment integration"
aimaestro-agent.sh update backend-api --add-tag "critical"
aimaestro-agent.sh update backend-api --args "--continue --chrome"
```

### 5. Delete Agent

**Destructive operation.** Requires `--confirm`.

```bash
aimaestro-agent.sh delete <agent> --confirm [--keep-folder] [--keep-data]
```

### 6. Rename Agent

```bash
aimaestro-agent.sh rename <old-name> <new-name> [--rename-session] [--rename-folder] [-y]
```

### 7. Hibernate Agent

```bash
aimaestro-agent.sh hibernate <agent>
```

### 8. Wake Agent

```bash
aimaestro-agent.sh wake <agent> [--attach]
```

### 9. Restart Agent

```bash
aimaestro-agent.sh restart <agent> [--wait <seconds>]
```

Hibernates, waits (default 3s), then wakes. Cannot restart the current session.

### 10. Session Management

```bash
aimaestro-agent.sh session add <agent> [--role <role>]
aimaestro-agent.sh session remove <agent> [--index <n>] [--all]
aimaestro-agent.sh session exec <agent> <command...>
```

---

## PART 2: PLUGIN MANAGEMENT

### 11. Install Plugin

```bash
aimaestro-agent.sh plugin install <agent> <plugin> [-s|--scope user|project|local] [--no-restart]
```

### 12. Uninstall Plugin

```bash
aimaestro-agent.sh plugin uninstall <agent> <plugin> [-s|--scope user|project|local] [--force|-f]
```

### 13. Update Plugin

```bash
aimaestro-agent.sh plugin update <agent> <plugin> [-s|--scope user|project|local]
```

### 14. Load Plugin (Session Only)

```bash
aimaestro-agent.sh plugin load <agent> <path> [<path>...]
```

### 15. List Plugins

```bash
aimaestro-agent.sh plugin list <agent>
```

### 16. Enable/Disable Plugins

```bash
aimaestro-agent.sh plugin enable <agent> <plugin> [-s|--scope user|project|local]
aimaestro-agent.sh plugin disable <agent> <plugin> [-s|--scope user|project|local]
```

### 17. Validate Plugin

```bash
aimaestro-agent.sh plugin validate <agent> <plugin-path>
```

### 18. Reinstall Plugin

```bash
aimaestro-agent.sh plugin reinstall <agent> <plugin> [-s|--scope user|project|local]
```

### 19. Clean Plugin Cache

```bash
aimaestro-agent.sh plugin clean <agent> [--dry-run|-n]
```

### 20. Plugin Marketplace

```bash
aimaestro-agent.sh plugin marketplace list <agent>
aimaestro-agent.sh plugin marketplace add <agent> <source> [--no-restart]
aimaestro-agent.sh plugin marketplace remove <agent> <name> [--force|-f]
aimaestro-agent.sh plugin marketplace update <agent> [<name>]
```

Source formats: `owner/repo`, `github:owner/repo`, HTTPS/SSH Git URLs, `#branch`, local directory, remote URL.

Examples:
```bash
aimaestro-agent.sh plugin marketplace add backend-api owner/repo
aimaestro-agent.sh plugin marketplace add backend-api https://github.com/o/r.git#v1.0.0
aimaestro-agent.sh plugin marketplace remove backend-api my-marketplace --force
```

---

## PART 3: EXPORT/IMPORT

### 21. Export Agent

```bash
aimaestro-agent.sh export <agent> [-o <output-file>]
```

Default output: `<agent>.agent.json`. Currently exports configuration only.

### 22. Import Agent

```bash
aimaestro-agent.sh import <file> [--name <new-name>] [--dir <new-dir>]
```

---

## PART 4: SKILL MANAGEMENT

### 23. List Skills (Registry)

```bash
aimaestro-agent.sh skill list <agent>
```

### 24. Add Skill (Registry)

```bash
aimaestro-agent.sh skill add <agent> <skill-id> [--type marketplace|custom] [--path <path>]
```

### 25. Remove Skill (Registry)

```bash
aimaestro-agent.sh skill remove <agent> <skill-id>
```

### 26. Install Skill (Filesystem)

```bash
aimaestro-agent.sh skill install <agent> <source> [-s|--scope user|project|local] [--name <name>]
```

Examples:
```bash
aimaestro-agent.sh skill install my-agent ./my-skill.skill
aimaestro-agent.sh skill install my-agent ./path/to/skill-folder --scope project
aimaestro-agent.sh skill install backend-api ./debug-skill --scope local
```

### 27. Uninstall Skill (Filesystem)

```bash
aimaestro-agent.sh skill uninstall <agent> <skill-name> [-s|--scope user|project|local]
```

---

## Error Handling

**Agent not found:** `aimaestro-agent.sh list` to see available agents.

**Script not found:** Check `which aimaestro-agent.sh` and verify `~/.local/bin` is in PATH.

**API not running:** `curl http://localhost:23000/api/hosts/identity` — start AI Maestro if down.

For detailed output formats, scenarios, troubleshooting, error table, and architecture, see [references/REFERENCE.md](./references/REFERENCE.md).
