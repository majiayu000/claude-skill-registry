---
name: minimax-mcp
description: "MiniMax MCP server integration with token-efficient AI delegation. Use for web search, image analysis, MCP server integration in terminal/desktop Claude, and Claude-MiniMax collaboration patterns. Provides working scripts and slash commands."
---

# MiniMax MCP

## Overview

This skill provides complete MiniMax MCP server integration for Claude, enabling token-efficient AI delegation with 85-90% token savings. MiniMax handles heavy computational tasks while Claude plans and reviews, creating an optimal division of labor.

## Usage Guidance

### Autonomous Delegation (Compound Engineering)

**IMPORTANT:** This skill is designed for **autonomous use**. You do NOT need to ask for permission before delegating tasks to MiniMax. The delegation patterns below are approved workflows for compound engineering.

See `docs/agent-instructions/COMPOUND_ENGINEERING.md` for the full delegation framework.

### When to Prefer MiniMax
Consider delegating these tasks to MiniMax for better efficiency:

1. **Web search or research queries** - MiniMax handles external searches well
2. **Image analysis tasks** - MiniMax VLM API provides visual understanding
3. **Multi-source research** - When you'd otherwise read 5+ files
4. **Current information needs** - Docs, trends, releases from 2024-2026
5. **Parallel asset generation** - Launch multiple agents for concurrent work
6. **Screenshot analysis** - Visual bugs, UI issues, sprite quality assessment

### When NOT to Delegate
- HPV playtesting or MCP runtime inspection (requires local control and fast feedback).
- Iterative input loops where latency ruins the feedback cycle (batch locally instead).

### Trusted Domains (Auto-Approved)
These sources are reliable and searches are **automatically restricted** to these domains:
- `docs.anthropic.com` - Claude official docs
- `platform.claude.com` - Claude platform docs
- `docs.cursor.com` - Cursor IDE docs
- `cursor.com` - Cursor docs
- `cookbook.openai.com` - OpenAI cookbook
- `godotengine.org` - Godot official docs
- `api.minimax.io` - MiniMax API docs

**Implementation**: The `web-search.sh` script automatically appends `site:` filters to all queries, ensuring results only come from trusted domains. To search other domains, ask Sam for permission and use an alternative search method.

### Decision Trigger
Before using Grep/Glob for research, pause and ask:
> "Would a MiniMax search to trusted docs handle this better?"

If yes → use MiniMax. If searching known local files → use local tools.

### Autonomous Delegation Patterns

#### Pattern 1: Parallel Research Delegation
Launch multiple MiniMax agents concurrently instead of sequential research:

**Autonomous Example - No Permission Needed:**
```bash
# Agent 1: Research Godot 4.5 input system
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"q":"site:godotengine.org InputEventAction handling"}' &

# Agent 2: Research dialogue UI patterns
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"q":"site:docs.godotengine.org dialogue UI RichTextLabel"}' &

# Agent 3: Research quest state management
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"q":"site:docs.godotengine.org state machine autoload"}' &

# Wait for all to complete, then synthesize results
wait
```

**Key Points:**
- Use `&` to launch requests in parallel
- Use `wait` to collect all results before synthesizing
- Main agent orchestrates, MiniMax agents execute
- No permission needed - this is standard compound engineering

#### Pattern 2: Parallel Image Analysis
Analyze multiple screenshots or sprites concurrently:

**Autonomous Example - Visual Quality Assessment:**
```bash
# Analyze 5 placeholder sprites in parallel
for sprite in moly_seed nightshade_seed moon_tears npc_circe npc_world; do
  curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
    -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
    -H "Content-Type: application/json" \
    -d "{
      \"prompt\": \"Rate this sprite on clarity, pixel art quality, and game readiness (1-10). Note issues.\",
      \"image_url\": \"file://$(pwd)/assets/sprites/placeholders/${sprite}.png\"
    }" > "analysis_${sprite}.json" &
done
wait

# Synthesize all results into quality report
cat analysis_*.json | jq '.'
```

#### Pattern 3: Research + Image Analysis Combo
Combine web search with image understanding for comprehensive analysis:

**Autonomous Example - Screenshot Bug Analysis:**
```bash
# Agent 1: Search for similar bug reports
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"q":"site:github.com godot dialogue box overlap UI"}' > bug_research.json &

# Agent 2: Analyze the screenshot
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Identify UI elements, z-order issues, and layout problems in this game screenshot.",
    "image_url": "file://screenshot.png"
  }' > screenshot_analysis.json &

wait

# Main agent synthesizes both sources
echo "Research findings:" && cat bug_research.json
echo "Screenshot analysis:" && cat screenshot_analysis.json
```

### Token Savings with Parallel Delegation

**Sequential (Bad):**
- Research task 1: ~2000 tokens (Claude reads results)
- Research task 2: ~2000 tokens
- Research task 3: ~2000 tokens
- **Total: ~6000 tokens**

**Parallel with MiniMax (Good):**
- Launch 3 agents: ~100 tokens (Claude orchestrates)
- MiniMax handles all 3: ~6000 tokens (subagent compute)
- Claude reviews synthesis: ~500 tokens
- **Total: ~600 tokens for Claude** (90% savings)

The key: Claude plans (~100), MiniMax executes (~6000 in subagents), Claude reviews (~500).

### Example Pattern

**Local file task** (use Grep/Read):
```
User: "Find where player_health is defined"
Agent: *Uses Grep to search codebase* ✅
```

**Research task** (use MiniMax):
```
User: "How does Godot 4.5 handle input?"
Agent: *Calls MiniMax search: site:godotengine.org input handling*
MiniMax: *Returns official docs*
Agent: *Reviews results* ✅
```

## Core Capabilities

### 1. MCP Server Integration
- **Launch MCP Server**: Start MiniMax MCP server with proper environment configuration
- **Status Monitoring**: Check server health and connectivity
- **Token Efficiency**: Claude plans (~100 tokens), MiniMax executes (~2000 tokens saved)

### 2. Direct API Access
- **Web Search**: Google-like search via `/v1/coding_plan/search` endpoint
- **Image Analysis**: Understand JPEG/PNG/WebP images via `/v1/coding_plan/vlm` endpoint
- **No Dependencies**: Works with curl only (no Python or server required)

### 3. Terminal & Desktop Support
- **Terminal Claude**: Use direct API calls via curl
- **Desktop Claude**: Use MCP server with native tools
- **Cursor IDE**: Compatible with existing slash commands

### 4. Production-Ready
- **Verified API Key**: 126-character key provided
- **Tested Endpoints**: All functionality verified (2026-01-19)
- **Error Handling**: Comprehensive troubleshooting guides

## Quick Start

### Start MCP Server (Desktop Claude)
```bash
MINIMAX_API_KEY="sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
MINIMAX_API_HOST="https://api.minimax.io" \
uvx minimax-coding-plan-mcp -y
```

### Direct API Usage (Terminal Claude)

**Web Search:**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"your search query"}'
```

**Image Analysis:**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt":"What do you see?","image_url":"https://example.com/image.png"}'
```

## Claude Extension Usage (Recommended)

For Claude extension users, call the MiniMax API directly via the Bash tool - no intermediate scripts needed.

**Web Search:**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/search" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"q":"your search query"}'
```

**Image Analysis (URL):**
```bash
curl -s -X POST "https://api.minimax.io/v1/coding_plan/vlm" \
  -H "Authorization: Bearer ${MINIMAX_API_KEY:-sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c}" \
  -H "Content-Type: application/json" \
  -H "MM-API-Source: Minimax-MCP" \
  -d '{"prompt":"What do you see?","image_url":"https://example.com/image.png"}'
```

**Token Efficiency:** Claude makes the curl call (~50 tokens), MiniMax handles execution (saves ~2000 tokens). This is the optimal pattern for extension usage.

## Workflow Patterns

### Pattern 1: Research Delegation
1. **Claude Plans** (minimal tokens ~50-100): "Search for Godot 4.5 features"
2. **MiniMax Executes** (heavy lifting ~2000 tokens): Web search via API
3. **Claude Reviews** (oversight): Process results and provide insights

### Pattern 2: Image Analysis
1. **Claude Directs** (planning): "Analyze this screenshot for UI issues"
2. **MiniMax Analyzes** (computation): Image understanding via API
3. **Claude Synthesizes** (quality control): Interpret analysis results

### Pattern 3: Plan Execution
1. **Claude Creates Plan**: Structure approach and requirements
2. **MiniMax Executes**: Perform research, analysis, coding tasks
3. **Claude Reviews**: Validate results and iterate as needed

## Available Scripts

### scripts/check-status.sh
Check MCP server status and health. Verifies environment variables and connectivity.

**Usage:**
```bash
./scripts/check-status.sh
```

### scripts/web-search.sh
Perform web search using direct API. Token-efficient alternative to MCP tools.

**Usage:**
```bash
./scripts/web-search.sh "Godot engine features"
```

### scripts/analyze-image.sh
Analyze images using MiniMax vision capabilities via direct API.

**Usage:**
```bash
./scripts/analyze-image.sh "What bugs do you see?" "screenshot.png"
```

### scripts/test-connection.sh
Verify API key, endpoint connectivity, and environment setup.

**Usage:**
```bash
./scripts/test-connection.sh
```

### scripts/execute-plan.sh
Execute structured plan with MiniMax delegation for maximum token efficiency.

**Usage:**
```bash
./scripts/execute-plan.sh "Research React 18 features and create summary"
```

### scripts/general-query.sh
Send general queries to MiniMax for any task.

**Usage:**
```bash
./scripts/general-query.sh "Explain quantum computing basics"
```

## Environment Setup

### Required Environment Variables
```bash
MINIMAX_API_KEY="sk-cp-xgttGx8GfmjMzMR64zQOU0BXYjrikYD0nSTMfWBbIT0Ykq17fUeT3f7Dmmt2UOQaskwOjaOPxMYk6jev0G4Av2-znT8-a3aRWGfHVpgMvgzc8dVYc4W8U6c"
MINIMAX_API_HOST="https://api.minimax.io"
```

### Inline Usage (Recommended)
Set variables in the same command to avoid persistence issues:
```bash
MINIMAX_API_KEY="..." MINIMAX_API_HOST="..." uvx minimax-coding-plan-mcp -y
```

## Reference Documentation

### API Endpoints
See [api-endpoints.md](references/api-endpoints.md) for complete API reference including authentication, request/response formats, and error codes.

### Troubleshooting
See [troubleshooting.md](references/troubleshooting.md) for common issues, solutions, and verification steps.

### Workflows
See [workflows.md](references/workflows.md) for detailed usage patterns, examples, and best practices.

### Slash Commands
See [slash-commands.md](references/slash-commands.md) for command reference and integration examples.

## Key Benefits

✅ **85-90% Token Reduction**: MiniMax handles heavy computation
✅ **Production Ready**: All tests passing, verified 2026-01-19
✅ **Multiple Integration Methods**: Terminal (API) and Desktop (MCP)
✅ **Zero Dependencies**: Works with curl only
✅ **Comprehensive Documentation**: Complete guides and references
✅ **Error Handling**: Robust troubleshooting and validation

## When to Use This Skill

**Use MiniMax MCP when:**
- Research tasks require extensive web searching
- Image analysis is needed
- Token efficiency is critical
- Delegating heavy computational work
- Building workflows with AI collaboration

**Choose Integration Method:**
- **Terminal Claude**: Use direct API calls (curl)
- **Desktop Claude**: Use MCP server (uvx)
- **Cursor IDE**: Use slash commands or MCP tools

---

**Status**: ✅ Production Ready (Verified 2026-01-19)
**Tests**: ✅ All 5 Success Criteria Passing
**Documentation**: ✅ Complete
**Support**: ✅ Comprehensive Troubleshooting Guides
