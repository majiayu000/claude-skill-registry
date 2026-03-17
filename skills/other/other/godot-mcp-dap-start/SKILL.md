---
name: godot-mcp-dap-start
description: Start or restart the Godot editor MCP server and debugger/DAP ports for this project. Use when MCP tools are missing, handshake fails, or the debug port is absent; includes a single-editor restart workflow and command checks.
---

# Godot MCP + Debug Start

## Overview
Ensure a single Godot editor instance is running, MCP is reachable, and the debug port is available for HPV and runtime inspection.

## Workflow (Option A: clean restart)
1. Run the start script to ensure MCP is up:
   - `powershell -ExecutionPolicy Bypass -File scripts/ensure_godot_mcp.ps1`
2. If MCP handshake fails or multiple editors are running, rerun with a forced restart:
   - `powershell -ExecutionPolicy Bypass -File scripts/ensure_godot_mcp.ps1 -ForceRestart`
3. If you need the debug port for runtime inspection, rerun with:
   - `powershell -ExecutionPolicy Bypass -File scripts/ensure_godot_mcp.ps1 -StartGameForDebug`

## Success Criteria
- Port 9080 is listening and `godot-mcp-cli --list-tools` succeeds.
- When `-StartGameForDebug` is used, port 6007 is listening.

## Notes
- Do not ask the user to click the MCP panel. Use the script first.
- Use a single Godot editor instance to avoid MCP conflicts.
- See `references/commands.md` for CLI and port checks.
