---
name: unity-editor
description: Remote control Unity Editor via CLI using unityctl. Activate when user mentions Unity Editor, play mode, asset compilation, Unity console logs, C# script debugging, Unity tests, scene loading, screenshots, or video recording. Use for launching/stopping editor, entering/exiting play mode, compiling scripts, viewing logs, loading scenes, running tests, capturing screenshots, recording video, or executing arbitrary C# in Unity context.
---

# unityctl - Unity Editor Remote Control

Control a running Unity Editor from the command line without batch mode.

## Setup (Required First)

Run `unityctl status` first to check what's already running. If Unity is already connected, skip straight to commands.

```bash
unityctl status                # Check current state — may already be connected
unityctl bridge start          # Start bridge daemon (idempotent, skips if running)
unityctl editor run            # Launch Unity Editor (or open project manually)
unityctl wait                  # Block until Unity is connected (up to 120s)
```

## Commands

```bash
# Status & Bridge
unityctl status              # Check Unity, bridge, and connection status
unityctl bridge start/stop   # Manage bridge daemon

# Editor
unityctl editor run/stop     # Launch or stop Unity Editor

# Compile (run after modifying C# scripts or importing packages)
unityctl asset refresh       # Compile scripts, returns errors on failure

# Play Mode
unityctl play enter/exit     # Enter or exit play mode

# Logs
unityctl logs                # Show logs since last clear (auto-clears on play/compile)
unityctl logs -n 50          # Limit entries
unityctl logs --stack        # Include stack traces
unityctl logs --full         # Ignore clear boundary

# Scenes
unityctl scene list          # List scenes
unityctl scene load <path>   # Load scene (e.g., Assets/Scenes/Main.unity)
unityctl scene load <path> --additive  # Load additively (without unloading current)

# Testing
unityctl test run            # Run edit mode tests
unityctl test run --mode playmode

# Screenshots
unityctl screenshot capture  # Capture game view

# Video Recording (requires com.unity.recorder package)
# Note: record start auto-enters play mode if not already playing
unityctl record start                  # Start recording (manual stop)
unityctl record start --duration 10    # Record 10 seconds, blocks until done
unityctl record start --frames 300     # Record exactly 300 frames, blocks until done
unityctl record stop                   # Stop recording, returns file path + duration

# Scene Snapshot (structured observation with instance IDs)
unityctl snapshot                          # Scene hierarchy tree (default depth 2)
unityctl snapshot --depth 4                # Deeper traversal
unityctl snapshot --id 14200 --components  # Drill into one object with all properties
unityctl snapshot --id 14200 --filter "type:Rigidbody"  # Filter drill-down result
unityctl snapshot --interactive            # UI focus: text content, button states
unityctl snapshot --layout                 # RectTransform anchors/sizes
unityctl snapshot --filter "type:Rigidbody"  # Filter by type:T, name:N*, tag:T
unityctl snapshot --scene Assets/Scenes/Other.unity      # Snapshot another scene (read-only)
unityctl snapshot --prefab Assets/Prefabs/Player.prefab  # Snapshot a prefab asset

# Prefab Editing
unityctl prefab open Assets/Prefabs/Player.prefab  # Open prefab in isolation mode
unityctl prefab open Assets/Prefabs/Player.prefab --context 14200  # In-context editing
unityctl prefab close                              # Close prefab stage, return to scene
unityctl prefab close --save                       # Save changes then close
unityctl prefab close --discard                    # Discard changes then close

# Dialog Detection (native OS popups blocking Unity)
unityctl dialog list                   # List detected popup dialogs
unityctl dialog dismiss                # Dismiss first dialog (clicks first button)
unityctl dialog dismiss --button "OK"  # Click specific button
```

## Scene Observation & Manipulation Workflow

Use `snapshot` to observe, `eval --id` to act, then `snapshot` to verify:

```bash
unityctl snapshot                          # See the scene, get instance IDs [i:N]
unityctl script eval --id 14200 'target.transform.position = new Vector3(0, 10, 0); return "moved";'
unityctl snapshot                          # Verify changes
```

Multiple targets with `--id` (uses `targets[]` array):
```bash
unityctl script eval --id 14200,14210 'targets[0].transform.SetParent(targets[1].transform); return "done";'
```

## Script Execution

Evaluate C# expressions directly (common usings like UnityEngine, UnityEditor, System auto-included):

```bash
unityctl script eval 'Application.version'
unityctl script eval 'GameObject.FindObjectsOfType<Camera>().Length'
unityctl script eval --id -1290 'target.transform.position'
unityctl script eval -u UnityEngine.SceneManagement 'SceneManager.GetActiveScene().name'
unityctl script eval -u UnityEngine.UI,UnityEngine.SceneManagement 'SceneManager.GetActiveScene().name'  # comma-separated
```

Pass arguments to the script with `--`:
```bash
unityctl script eval 'args[0]' -- hello
```

### Full Script Execution

For complex scripts with custom classes, multiple methods, or logic beyond a single expression. Use the Write tool to create a `.cs` file, then execute it. The script must define a class with a static `Main()` method returning `object` (JSON-serialized):

```cs
// /tmp/MyScript.cs
using UnityEngine;

public class Script
{
    public static object Main()
    {
        var player = GameObject.Find("Player");
        return player?.transform.position.ToString() ?? "not found";
    }
}
```

```bash
unityctl script execute /tmp/MyScript.cs
unityctl script execute /tmp/SpawnObjects.cs -- Cube 5 'My Object'
```

Use `Main(string[] args)` to accept arguments passed after `--`.

**Important:** Always use the Write tool to create the `.cs` file rather than shell heredocs (`cat << 'EOF'`), which break on single quotes in C# code.

Use `-t <seconds>` on `script eval`/`script execute` for long-running operations (default 30s):

```bash
unityctl script eval -t 600 -u UnityEditor 'return BuildPipeline.BuildPlayer(opts).summary.result.ToString();'
```

## Typical Workflow

```bash
# After editing C# files...
unityctl asset refresh       # Compile (fix errors if any)
unityctl snapshot            # Observe scene state
unityctl play enter
unityctl snapshot            # Check runtime state with instance IDs
unityctl logs                # Check runtime logs
unityctl play exit
```

## Troubleshooting

Run `unityctl status` first to diagnose issues.

| Problem | Solution |
|---------|----------|
| Bridge not responding | `unityctl bridge stop && unityctl bridge start` |
| Editor not connected | Normal - exponential backoff, up to 15 seconds |
| Connection lost after compile | Normal - domain reload, auto-reconnects |
| "Project not found" | `unityctl setup` or `unityctl config set project-path <path>` |
| Can't tell when Unity is ready | `unityctl wait --timeout 300` |
| Command timed out | A native dialog may be blocking Unity: `unityctl dialog list` |
| Progress bar stuck | Check with `unityctl dialog list`, wait or dismiss |
| Editor not found | Use `--unity-path` to specify Unity executable |

## Plugin Commands

### Plugin: sample-script

Sample script plugin demonstrating the plugin system

- `unityctl sample-script hello [name] [--loud]`
  Say hello from Unity

### Plugin: sample-exec (executable)

A sample executable plugin that prints connection info. Demonstrates the `unityctl-{name}` naming convention.

- `unityctl sample-exec [args...]`
  Prints greeting and bridge connection details.
