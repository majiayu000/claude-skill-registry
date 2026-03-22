---
name: gwt-pty-communication
description: PTY based communication tools for Project Mode orchestration (Lead/Coordinator/Developer).
---

# gwt PTY Communication

Use gwt terminal commands as the transport for agent-to-agent communication.

## Commands

- `send_keys_to_pane`: send text to a specific pane.
- `send_keys_broadcast`: send text to all running panes.
- `capture_scrollback_tail`: read pane output for status/progress.
- `list_terminals`: list active pane ids.
- `close_terminal`: stop a pane when escalation is needed.

## Notes

- Prefer targeted `send_keys_to_pane` for deterministic orchestration.
- Use `capture_scrollback_tail` before sending follow-up instructions.

## Environment

- `GWT_PROJECT_ROOT`: absolute path to the project root. PTY commands are scoped to the caller's project; panes belonging to other projects are not visible or accessible.
- `GWT_PANE_ID`: pane ID of the current terminal session.
- `GWT_BRANCH`: branch name of the current session.
- `GWT_AGENT`: agent name of the current session.
