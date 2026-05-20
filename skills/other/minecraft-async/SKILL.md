---
name: minecraft-async
description: Manage a preinstalled local Minecraft Java client asynchronously for CTF and automation workflows. Use when Codex needs to launch Minecraft in offline mode with alternate usernames, inspect Minecraft logs, focus or type into the X11 game window, send chat or slash commands quickly, or join a multiplayer server by launching the installed client directly instead of relying on the official launcher.
---

# OpenCROW I/O - Minecraft Async

Prefer the `opencrow-minecraft-mcp` server for status, launch, chat, commands, screenshots, and log reads. Fall back to `scripts/mcx` only when you need to inspect or debug the backend directly.

## MCP First

- Use `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities` first.
- Use the typed Minecraft operations:
  - `minecraft_status`
  - `minecraft_launch`
  - `minecraft_join_server`
  - `minecraft_join_world`
  - `minecraft_focus`
  - `minecraft_send_text`
  - `minecraft_chat`
  - `minecraft_command`
  - `minecraft_screenshot`
  - `minecraft_read_log`
  - `minecraft_stop`
- Treat the MCP server as the main interface and `scripts/mcx` as the implementation fallback.

Use `scripts/mcx` to control the already-installed Minecraft Java client under `~/.minecraft` when you are operating outside MCP.

## Workflow

1. Check `status` to confirm the install, versions, X11 display, and any running session.
2. Launch with the `direct` backend for offline usernames against the existing install.
3. Use `join-server` or `join-world` when you need the client to open directly into a target.
4. Use `focus`, `chat`, `command`, or `send-text` for fast in-game actions.
5. Capture a screenshot when the visual state matters.
6. Inspect `latest.log` and the managed launcher log when something fails.
7. Stop the managed session explicitly when done.

## Commands

```bash
# Inspect install, window, logs, and managed session state
scripts/mcx status

# Launch the existing client directly in offline mode
scripts/mcx launch --username ra13118 --version 1.21.8

# Launch and connect to a server immediately via quick play
scripts/mcx join-server --username ra13118 --server dyn-01.midnightflag.fr:13118 --version 1.21.8

# Launch directly into a local world by save-folder name
scripts/mcx join-world --username ra13118 --world NewWorld --version 1.21.8

# Focus the game window, open chat, and send text
scripts/mcx chat --text 'hello from Codex'

# Focus the game window, open slash-command mode, and run a command
scripts/mcx command --text 'tp @s 0 100 0'

# Type raw text into the currently focused field
scripts/mcx send-text --text 'seed?'

# Capture the current game window to a PNG
scripts/mcx screenshot --output /tmp/minecraft-state.png

# Read the latest Minecraft log
scripts/mcx read-log --which latest --tail 80

# Stop the managed session
scripts/mcx stop
```

## Backends

- Prefer the default `direct` backend. It launches the installed client from `~/.minecraft/versions`, `libraries`, and `assets` without the official launcher and supports offline usernames.
- Use `--backend cmd-launcher` only when `cmd-launcher` is already installed and you deliberately want its instance model. Read [references/backends.md](references/backends.md) first.
- Treat `join-server` and `join-world` as launch-time operations. They use direct quick-play arguments and are more reliable before the client is already in-game.

## Example Workflows

### Connect To A Server

```bash
scripts/mcx join-server \
  --session server-demo \
  --username ra13118 \
  --version 1.21.8 \
  --server dyn-01.midnightflag.fr:13118
```

After the client loads:

```bash
scripts/mcx screenshot --output /tmp/server-state.png
scripts/mcx chat --text 'hello'
scripts/mcx command --text 'trigger ready'
```

### Enter A Local World And Teleport

First inspect save-folder names:

```bash
scripts/mcx status
```

Then launch directly into the world and teleport:

```bash
scripts/mcx join-world \
  --session world-demo \
  --username ra13118 \
  --version 1.21.8 \
  --world NewWorld
```

When the world finishes loading:

```bash
scripts/mcx command --text 'tp @s 52 -64 193'
scripts/mcx screenshot --output /tmp/world-teleport.png
```

The `--world` value should match the save directory name under `~/.minecraft/saves`.

### Troubleshoot A Disconnect Or Bad State

```bash
scripts/mcx read-log --which both --tail 120
scripts/mcx screenshot --output /tmp/minecraft-error-state.png
```

Use the screenshot for visual diagnosis and the logs for protocol or world-load failures.

## Operational Rules

- Use one managed session name per task flow if you need multiple launches; otherwise keep the default `default` session.
- Use `status` before `join-world` so you can copy the exact save-folder name.
- Read `read-log --which both --tail 120` before retrying a failed launch.
- Use `command` for slash commands and `chat` for normal messages instead of `send-text` when possible.
- Use `screenshot` when the visual state matters. It captures the current game window to a local PNG file.
- Expect X11 window control to require a live `DISPLAY`; if no display is available, limit work to launch and log inspection.
- If a client is already running and you need a different offline username or initial server, stop it and relaunch.

## References

- Read [references/backends.md](references/backends.md) for install layout, backend selection, log locations, and X11 caveats.
