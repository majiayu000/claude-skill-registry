---
name: unityctl-plugins
description: Create unityctl plugins. Use when the user wants to create, scaffold, or write a unityctl plugin (script or executable).
---

# Creating unityctl Plugins

There are two plugin types: **script** (C# running inside Unity) and **executable** (any program on disk).

## Script Plugins

Run C# inside the Unity Editor via the `script.execute` RPC. Best for commands that need Unity APIs.

### Quick start

```bash
unityctl plugin create my-tool   # scaffolds .unityctl/plugins/my-tool/
```

### Structure

```
.unityctl/plugins/my-tool/
  plugin.json    # manifest
  hello.cs       # handler script
```

### plugin.json

```json
{
  "name": "my-tool",
  "version": "1.0.0",
  "description": "My custom tool",
  "commands": [
    {
      "name": "stats",
      "description": "Show scene stats",
      "arguments": [
        { "name": "scene", "description": "Scene name", "required": false }
      ],
      "options": [
        { "name": "verbose", "type": "bool", "description": "Show details" },
        { "name": "format", "type": "string", "description": "Output format" }
      ],
      "handler": { "type": "script", "file": "stats.cs" }
    }
  ],
  "skill": { "file": "SKILL.md" }
}
```

### Handler script

Must define `public class Script` with `public static object Main(string[] args)`. Arguments and options are passed as the `args` array.

```csharp
using UnityEngine;
using UnityEditor;

public class Script
{
    public static object Main(string[] args)
    {
        var count = Object.FindObjectsByType<GameObject>(FindObjectsSortMode.None).Length;
        return $"Scene has {count} GameObjects";
    }
}
```

The return value is sent back as the command output. The script runs on Unity's main thread and has access to all Unity and UnityEditor APIs.

### Custom skill documentation

Add a `"skill": { "file": "SKILL.md" }` entry to plugin.json and create the markdown file. It will be included in the composed SKILL.md when running `unityctl skill rebuild`. Without it, documentation is auto-generated from the manifest.

### Location

| Level | Directory | Precedence |
|-------|-----------|------------|
| Project | `.unityctl/plugins/` | Higher |
| User | `~/.unityctl/plugins/` | Lower |

Use `--global` / `-g` with `plugin create` to scaffold at user level.

Plugin names must be lowercase alphanumeric with hyphens (e.g. `my-tool`, `scene-stats`). Must start and end with a letter or digit.

## Executable Plugins

Any executable named `unityctl-<name>` becomes available as `unityctl <name>`. Best for workflows outside Unity: build pipelines, CI scripts, multi-step orchestration.

### How it works

Place an executable (shell script, Python, Go binary, .bat/.cmd/.ps1 on Windows) named `unityctl-<name>` in `.unityctl/plugins/` or on PATH. All arguments after the command name are passed through.

Executables in plugin directories are registered at startup (appear in `--help`). Executables on PATH are resolved lazily when invoked — like `git` resolving `git foo` → `git-foo`.

```bash
unityctl smoke 30          # finds and runs unityctl-smoke with arg "30"
unityctl deploy --staging  # finds and runs unityctl-deploy with arg "--staging"
```

### Environment variables

The CLI sets these before launching the executable:

| Variable | Description |
|----------|-------------|
| `UNITYCTL_PROJECT_PATH` | Resolved Unity project root |
| `UNITYCTL_BRIDGE_PORT` | Bridge HTTP port |
| `UNITYCTL_BRIDGE_URL` | Full bridge URL (e.g. `http://localhost:62908`) |
| `UNITYCTL_AGENT_ID` | Agent ID if `--agent-id` was passed |
| `UNITYCTL_JSON` | `"1"` if `--json` was passed |

### Example

```bash
#!/usr/bin/env bash
# Save as: unityctl-smoke (chmod +x)
unityctl logs clear
unityctl play enter
sleep "${1:-10}"
unityctl screenshot capture --json > /tmp/smoke.json
ERRORS=$(unityctl logs -n 1000 --json | jq '[.entries[] | select(.level == "Error")] | length')
unityctl play exit
[ "$ERRORS" -eq 0 ] && echo "PASS" || { echo "FAIL: $ERRORS error(s)"; exit 1; }
```

### Companion skill file

Place `unityctl-<name>.skill.md` next to the executable to provide custom documentation for SKILL.md composition. Without it, a minimal section is auto-generated.

### Platform notes

- **Windows**: matches `.exe`, `.cmd`, `.bat`, `.ps1` extensions
- **Unix**: matches any file with execute permission; extensions are stripped from the command name (`unityctl-foo.sh` becomes `unityctl foo`)

## Precedence

built-in command > script plugin > executable plugin. A plugin cannot shadow a built-in command.

## After changes

Run `unityctl skill rebuild` to update the composed SKILL.md with plugin documentation.

## Management commands

```bash
unityctl plugin list              # list all plugins (script + executable)
unityctl plugin create <name>     # scaffold a script plugin
unityctl plugin create <name> -g  # scaffold at user level (~/.unityctl/plugins/)
unityctl plugin remove <name>     # remove a script plugin
```
