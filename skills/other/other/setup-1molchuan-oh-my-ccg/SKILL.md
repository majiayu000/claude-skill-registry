---
name: setup
description: oh-my-ccg 初始安装向导
---

# oh-my-ccg Setup

Guided setup wizard for first-time installation.

## Steps

### Step 1: Plugin Verification
Check if oh-my-ccg is properly installed as a Claude Code plugin.
If not installed, guide user through:
```
/plugin marketplace add oh-my-ccg
```

### Step 2: MCP Server Connectivity
Verify all 3 MCP servers are operational by calling their tools:

1. **oh-my-ccg-tools**: Call `rpi_state_read` → should respond (even if empty state)
2. **oh-my-ccg-codex**: Call `ask_codex(agent_role="architect", prompt="ping")` → confirms Codex CLI works
3. **oh-my-ccg-gemini**: Call `ask_gemini(agent_role="designer", prompt="ping")` → confirms Gemini CLI works

If Codex or Gemini fails, guide CLI installation:
- Codex CLI: `npm install -g @openai/codex`
- Gemini CLI: `npm install -g @google/gemini-cli`

### Step 3: HUD Preset Selection
Ask user to choose HUD preset:
- minimal (1 line — low bandwidth terminals)
- focused (4 lines — daily development, recommended)
- full (10 lines — deep debugging, team collaboration)
- analytics (4 lines — cost tracking)

Save choice to .oh-my-ccg/config.json

### Step 4: OpenSpec Initialization (Optional)
Check if OpenSpec CLI is available: `npx openspec --version`
- If available: run `npx openspec init --tools claude`
- If not available: inform user this is optional and can be installed later with `npm install -g @fission-ai/openspec`

### Step 5: Completion Report
Show setup summary and next steps:
```
oh-my-ccg Setup Complete!

  Plugin:    ✅ Installed
  MCP Tools: ✅ Responding
  Codex:     ✅/❌ Available/Unavailable
  Gemini:    ✅/❌ Available/Unavailable
  OpenSpec:  ✅/❌ Initialized/Not installed (optional)
  HUD:       <selected> preset

Next: /oh-my-ccg:research "your requirement"
```
