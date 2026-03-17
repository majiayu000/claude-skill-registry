---
name: oh-my-ccg-init
description: 初始化 oh-my-ccg 环境 — 验证 MCP 服务器、Codex、Gemini
---

# oh-my-ccg Environment Initialization

You are executing the oh-my-ccg initialization skill. Follow these steps exactly:

## Step 1: Verify MCP Servers

Test connectivity of each plugin MCP server by calling their tools:

1. **oh-my-ccg-tools**: Call `rpi_state_read` → confirms tools server is operational
2. **oh-my-ccg-codex**: Call `ask_codex(agent_role="architect", prompt="ping")` → confirms Codex CLI is reachable
3. **oh-my-ccg-gemini**: Call `ask_gemini(agent_role="designer", prompt="ping")` → confirms Gemini CLI is reachable

Record which servers responded successfully.

## Step 2: Create State Directory

Via Bash, create the directory structure:
```
mkdir -p .oh-my-ccg/state .oh-my-ccg/plans
```

If `.oh-my-ccg/config.json` does not exist, create it with defaults:
```json
{
  "hud": { "preset": "focused" }
}
```

## Step 3: Initialize RPI State

Use the **oh-my-ccg-tools** MCP server's `rpi_state_write` tool to write:
```json
{
  "phase": "init",
  "changeId": null,
  "constraints": [],
  "decisions": [],
  "artifacts": [],
  "history": []
}
```

## Step 4: OpenSpec (Optional)

Check if OpenSpec CLI is available:
```bash
npx openspec --version
```
- If available: run `npx openspec init --tools claude`
- If not available: skip (OpenSpec is an optional dependency)

## Step 5: Report Status

Output a summary:
```
oh-my-ccg Environment Status:
  MCP Tools:  ✅/❌ (rpi_state_read responded)
  Codex:      ✅/❌ (ask_codex responded)
  Gemini:     ✅/❌ (ask_gemini responded)
  OpenSpec:   ✅/❌ (version or "not installed — optional")
  State Dir:  ✅ Created
  RPI State:  ✅ Initialized (phase: init)
```

If Codex or Gemini is unavailable, provide installation guidance:
- Codex CLI: `npm install -g @openai/codex`
- Gemini CLI: `npm install -g @google/gemini-cli`
