---
name: eleven-agent-manager
description: Manage ElevenLabs Conversational AI agent configuration including prompts, voice settings, MCP servers, and conversation settings. Use when updating agent behavior, voice, or integrations.
---

# ElevenLabs Agent Manager

## Overview
This skill provides tools and workflows for managing ElevenLabs Conversational AI agents, including updating prompts, voice settings, MCP server configurations, and monitoring conversations.

## API Configuration
- **API Key**: Set in environment as `ELEVENLABS_API_KEY`
- **Agent ID**: `agent_2601kf1fmbnseaxvp5kvc4zc21bz` (Mega Agent 2)
- **Base URL**: `https://api.elevenlabs.io/v1/convai`

## Available Operations

### 1. Update Agent Prompt
Update the system prompt that guides agent behavior.

```bash
python3 scripts/eleven_api.py update-prompt "Your new prompt here"
```

### 2. Get Agent Config
Retrieve current agent configuration.

```bash
python3 scripts/eleven_api.py get-config
```

### 3. Update Voice Settings
Change voice ID, stability, speed, or similarity boost.

```bash
python3 scripts/eleven_api.py update-voice --voice-id "HHstJSjlLg0NG8fanfeK" --speed 1.1
```

### 4. List MCP Servers
Show linked MCP servers.

```bash
python3 scripts/eleven_api.py list-mcp
```

### 5. Get Recent Conversations
View recent conversation summaries.

```bash
python3 scripts/eleven_api.py conversations --limit 10
```

### 6. Get Conversation Transcript
Get full transcript of a specific conversation.

```bash
python3 scripts/eleven_api.py transcript <conversation_id>
```

## Configuration Options

### Voice Settings
| Parameter | Description | Default |
|-----------|-------------|---------|
| voice_id | ElevenLabs voice ID | HHstJSjlLg0NG8fanfeK |
| stability | Voice consistency (0-1) | 0.5 |
| speed | Speech rate | 1.1 |
| similarity_boost | Voice similarity (0-1) | 0.8 |

### Turn Settings
| Parameter | Description | Default |
|-----------|-------------|---------|
| turn_timeout | Seconds to wait for response | 7.0 |
| mode | Conversation mode | turn |

### MCP Server Settings
| Parameter | Description |
|-----------|-------------|
| approval_policy | auto_approve_all, require_approval_all, require_approval_per_tool |
| transport | SSE or HTTP |
| url | MCP server endpoint |

## Workflow Examples

### Update Agent for New Use Case
1. Get current config: `python3 scripts/eleven_api.py get-config`
2. Draft new prompt based on requirements
3. Update prompt: `python3 scripts/eleven_api.py update-prompt "..."`
4. Test via voice widget

### Add Skills to Agent Context
1. List current skills in prompt
2. Generate skill summary from /home/ec2-user/mega-agent2/.claude/skills/
3. Update prompt with new skills list

### Troubleshoot MCP Integration
1. Check MCP server status: `curl http://127.0.0.1:8082/health`
2. List MCP servers: `python3 scripts/eleven_api.py list-mcp`
3. Check tool discovery: Use ElevenLabs API to verify tools

## Resources
- [ElevenLabs Docs](https://elevenlabs.io/docs/conversational-ai)
- [MCP Protocol](https://modelcontextprotocol.io)
- Agent Widget: https://elevenlabs.io/convai/agent_2601kf1fmbnseaxvp5kvc4zc21bz
