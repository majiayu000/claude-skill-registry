---
name: doctor
description: 诊断和修复 oh-my-ccg 安装问题
---

# oh-my-ccg Doctor

Diagnose the oh-my-ccg installation and identify issues.

## Checks

1. **Plugin installed**: Verify .claude-plugin exists and is valid JSON
2. **Hooks registered**: Verify hooks/hooks.json exists and all script files present
3. **MCP servers responding**:
   - oh-my-ccg-tools: Call `rpi_state_read` → verify response
   - oh-my-ccg-codex: Call `ask_codex(agent_role="architect", prompt="ping")` → verify response
   - oh-my-ccg-gemini: Call `ask_gemini(agent_role="designer", prompt="ping")` → verify response
4. **State directory**: Verify .oh-my-ccg/ directory structure exists
5. **Codex CLI**: Test `codex --version` via Bash
6. **Gemini CLI**: Test `gemini --version` via Bash
7. **OpenSpec available**: Test `npx openspec --version` (optional dependency)
8. **Node.js version**: Verify >= 18.x
9. **TypeScript build**: Run `npx tsc --noEmit`

## Output
```
oh-my-ccg Doctor Report:
  ✅ Plugin manifest (.claude-plugin)
  ✅ Hooks (8/8 scripts found)
  ✅ MCP tools server (rpi_state_read responded)
  ✅ MCP codex server (ask_codex responded)
  ❌ MCP gemini server (ask_gemini failed — gemini CLI not found)
  ✅ State directory (.oh-my-ccg/)
  ✅ Codex CLI (codex v1.x.x)
  ❌ Gemini CLI (not found)
  ✅ OpenSpec (v1.1.1) — optional
  ✅ Node.js (v22.x.x)
  ✅ TypeScript (zero errors)

Issues found: 2
  [W1] Gemini CLI not installed. Multi-model routing will fall back to Codex only.
       Fix: npm install -g @google/gemini-cli
  [W2] MCP gemini server not responding.
       Fix: Install Gemini CLI, then restart Claude Code to reload MCP servers.
```

## Auto-fix
If `--fix` flag is present, attempt to resolve issues automatically:
- Create missing directories
- Regenerate config files with defaults
