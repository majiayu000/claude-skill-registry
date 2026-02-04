---
name: exit
description: Safely terminate the current Claude Code session. Use when user explicitly asks to end session.
---
<!-- @agent-architect owns this file. Delegate changes, don't edit directly. -->

<prerequisites>
All tasks complete. Changes committed if applicable. Summarize accomplishments.
</prerequisites>

<execution>
claude-exit
</execution>

<notes>
Script verifies parent is 'claude' before sending SIGTERM. Fallback: tell user to type /exit or press Ctrl+D.
</notes>
