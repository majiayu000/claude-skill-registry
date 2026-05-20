---
name: worktree
description: Create a new git worktree and switch the session into it
user-invocable: true
disable-model-invocation: true
---
Create an isolated worktree for the current session using the EnterWorktree tool.

If the user provided a name argument, pass it as the worktree name. Otherwise let EnterWorktree generate a random name.
