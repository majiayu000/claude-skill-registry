---
name: sandbox-test
description: "Run an isolated Claude Code instance for testing. Use when you need a fresh environment without global CLAUDE.md or parent project settings. Trigger for: sandbox, isolated test, fresh instance, clean environment, test without global config."
---

# Sandbox Test

Run a Claude Code instance isolated from your global config.

## Why This Exists

Claude loads CLAUDE.md from parent directories up to home. Your global `~/CLAUDE.md` and any parent project configs affect every session. To test something without that context (like simulating a new user), you need to break the parent chain.

## How To Run Isolated Test

```bash
# Use the helper script (auto-increments if folder exists)
/Users/teren/projects/sensei/pcl-workshop-playground/scripts/sandbox.sh
```

This copies the workshop playground to `/tmp/workshop-test` (or `-2`, `-3`, etc. if it exists), then opens Claude in that directory.

## Why /tmp Works

- `/tmp` has no CLAUDE.md in its parent chain
- Only the project's own `.claude/` folder is loaded
- Simulates a fresh user environment

## Alternative: Specific Folder

If you want persistent test environments:

```bash
mkdir -p ~/sandbox
cp -r /path/to/project ~/sandbox/test-project
cd ~/sandbox/test-project
claude
```

Just make sure `~/sandbox/` has no CLAUDE.md file.

## What Gets Isolated

- Global `~/CLAUDE.md` - NOT loaded
- Global hooks from `~/.claude/settings.json` - still loaded (these are session-level)
- Project `.claude/` folder - loaded normally

## What Doesn't Get Isolated

- Global hooks still fire
- MCP servers still connect
- Your API credentials still work

This is about config isolation, not full sandboxing.
