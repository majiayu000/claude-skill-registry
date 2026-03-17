---
name: langsmith-agent-builder
version: "1.0.0"
description: LangSmith Agent Builder - No-code platform for creating AI agents with built-in tools (Gmail, Slack, GitHub, Linear), OAuth integrations, MCP server support, Slack deployment, and programmatic invocation via LangGraph SDK
---

# LangSmith Agent Builder

LangSmith Agent Builder enables users to create helpful AI agents without code. Start from a template, connect your accounts, and let the agent handle routine work while you stay in control.

## When to Use

- Creating AI agents without writing code
- Automating email management and drafting
- Building Slack-integrated AI assistants
- Connecting agents to Google Calendar, Gmail, GitHub, Linear
- Setting up approval workflows for agent actions
- Deploying agents to Slack workspaces
- Invoking agents programmatically via Python/JavaScript
- Integrating custom tools via MCP servers
- Building multi-agent workflows with sub-agents

## Core Concepts

### Agents
Autonomous AI assistants that can access tools, perform tasks, and interact with external services on your behalf.

### Templates
Pre-built agent configurations for common use cases (email assistant, team updates) that can be customized.

### Tools
Built-in integrations with services like Gmail, Slack, GitHub, Linear, and more. Agents use tools to perform actions.

### Triggers
Automation rules that invoke agents based on events (new email, Slack message, schedule).

### Sub-agents
Specialized agents that can be called by a parent agent for complex multi-step workflows.

### Approval Workflows
Human-in-the-loop checkpoints where agents pause for user confirmation before taking sensitive actions.

---

## Getting Started

### Prerequisites

- LangSmith account (smith.langchain.com)
- Gmail/Google account (for email/calendar tools)
- OpenAI or Anthropic API key

### Step 1: Obtain API Key

**OpenAI:**
1. Visit platform.openai.com/api-keys
2. Create a new secret key
3. Name it "Agent Builder"
4. Save securely (begins with `sk-`)

**Anthropic:**
1. Go to console.anthropic.com/settings/keys
2. Create a new key
3. Store safely (starts with `sk-ant-`)

### Step 2: Configure API Key in LangSmith

1. Navigate to smith.langchain.com
2. Go to Settings → Secrets tab
3. Click "Add secret"
4. Enter key name: `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
5. Paste your API key
6. Save

### Step 3: Create Your Agent

1. Switch to Agent Builder in LangSmith
2. Select Templates from navigation
3. Choose a template (e.g., Email Assistant)
4. Click "Use this template"
5. Authorize your accounts when prompted

### Step 4: Test and Configure

In the Test Chat panel:
```
"Apply a 'Review' label to emails requiring my attention."
```

Monitor proposed actions and approve each step using Continue.

---

## Built-in Tools

### Communication & Collaboration

| Tool | Capabilities |
|------|-------------|
| **Gmail** | Read/send emails, create drafts, manage labels |
| **Slack** | Send DMs, post to channels, read message history |
| **LinkedIn** | Publish posts with images or links |

### Productivity & Planning

| Tool | Capabilities |
|------|-------------|
| **Google Calendar** | List events, get details, create new events |
| **Google Sheets** | Create spreadsheets, read ranges |
| **Linear** | Manage issues, list teams, create/update/delete issues |
| **Pylon** | List and update issues |

### Data & Analytics

| Tool | Capabilities |
|------|-------------|
| **BigQuery** | Execute SQL queries |

### Code & Development

| Tool | Capabilities |
|------|-------------|
| **GitHub** | Manage PRs/issues, create PRs, comment, read repo files |

### Content Discovery

| Tool | Capabilities |
|------|-------------|
| **Exa** | Web search with content fetching, LinkedIn profile search |
| **Tavily** | Web search functionality |

### General Utilities

| Tool | Capabilities |
|------|-------------|
| **Webpage Reader** | Read webpage text content |
| **Image Extractor** | Extract image URLs and metadata |
| **Notifications** | Send user confirmations |

---

## Authentication Methods

### OAuth-Based Tools
These tools use OAuth for secure authentication:
- Google (Gmail, Calendar, Sheets)
- Slack
- Linear
- GitHub
- LinkedIn

When adding these tools, you'll be prompted to authorize via OAuth flow.

### API Key-Based Tools
These tools require workspace secrets (API keys):

| Tool | Secret Name |
|------|-------------|
| Exa Search | `EXA_API_KEY` |
| Tavily Search | `TAVILY_API_KEY` |
| Twitter/X | `TWITTER_API_KEY`, `TWITTER_API_KEY_SECRET` |

---

## Workspace Setup

### Required Secrets

Configure at least one LLM API key:

```
OPENAI_API_KEY=sk-...
# OR
ANTHROPIC_API_KEY=sk-ant-...
```

**Agent Builder-Specific Keys** (optional, for better tracking):
```
AGENT_BUILDER_OPENAI_API_KEY=sk-...
AGENT_BUILDER_ANTHROPIC_API_KEY=sk-ant-...
```

These take precedence over standard workspace secrets.

### Setting Up Secrets

1. Navigate to Settings in LangSmith
2. Select the Secrets tab
3. Click "Add secret"
4. Enter the key name (e.g., `OPENAI_API_KEY`)
5. Paste the API key value
6. Save

### Optional Tool Secrets

```
EXA_API_KEY=...
TAVILY_API_KEY=...
TWITTER_API_KEY=...
TWITTER_API_KEY_SECRET=...
```

---

## Agent Configuration

### Adding Tools

1. Open your agent in edit mode
2. Click "+ Add tool"
3. Select from available integrations:
   - Gmail, Slack, GitHub, Linear, etc.
4. Complete OAuth authorization or enter API keys
5. Configure tool-specific settings

### Creating Sub-agents

1. Click "+ Add sub-agent"
2. Configure the sub-agent's:
   - Name and description
   - Available tools
   - Custom instructions
3. Reference sub-agent in parent agent's prompt

### Configuring Approval Pauses

For sensitive operations:
1. Edit agent configuration
2. Enable "Request approval" for specific tools
3. Agent will pause and notify before executing

### Modifying Tool Settings

1. Navigate to agent settings
2. Locate the integration
3. Adjust configuration or click "Disconnect" to remove

---

## Triggers and Automation

### Available Trigger Types

| Trigger | Description |
|---------|-------------|
| **Email** | Activate on new emails matching criteria |
| **Slack** | Respond to messages in specific channels |
| **Schedule** | Run at specified times (cron-like) |

### Setting Up Triggers

1. Open agent configuration
2. Navigate to Triggers section
3. Select trigger type
4. Configure conditions:
   - Email: sender, subject filters
   - Slack: channel, mention requirements
   - Schedule: frequency, time

---

## Calling Agents from Code

### Prerequisites

- LangSmith account with Agent Builder agent
- Personal Access Token (PAT)
- LangGraph SDK

### Installation

**Python:**
```bash
pip install langgraph-sdk python-dotenv
```

**TypeScript:**
```bash
npm install @langchain/langgraph-sdk
```

### Configuration

Create `.env` file:
```bash
LANGSMITH_API_KEY=lsv2_pt_...
AGENT_ID=your-agent-id
AGENT_URL=https://your-agent-url
```

### Python Example

```python
from langgraph_sdk import get_client
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize client
client = get_client(
    url=os.getenv("AGENT_URL"),
    api_key=os.getenv("LANGSMITH_API_KEY")
)

# Get agent info
agent = await client.assistants.get(os.getenv("AGENT_ID"))
print(f"Agent: {agent['name']}")

# Create thread and invoke
thread = await client.threads.create()

response = await client.runs.create(
    thread_id=thread["thread_id"],
    assistant_id=os.getenv("AGENT_ID"),
    input={
        "messages": [
            {"role": "user", "content": "Summarize my unread emails"}
        ]
    }
)

# Stream response
async for chunk in client.runs.stream(
    thread_id=thread["thread_id"],
    assistant_id=os.getenv("AGENT_ID"),
    input={"messages": [{"role": "user", "content": "What's on my calendar today?"}]}
):
    print(chunk)
```

### TypeScript Example

```typescript
import { Client } from "@langchain/langgraph-sdk";
import dotenv from "dotenv";

dotenv.config();

const client = new Client({
  apiUrl: process.env.AGENT_URL,
  apiKey: process.env.LANGSMITH_API_KEY,
});

// Get agent
const agent = await client.assistants.get(process.env.AGENT_ID);
console.log(`Agent: ${agent.name}`);

// Create thread
const thread = await client.threads.create();

// Invoke agent
const response = await client.runs.create(
  thread.thread_id,
  process.env.AGENT_ID,
  {
    input: {
      messages: [
        { role: "user", content: "Check my GitHub notifications" }
      ]
    }
  }
);
```

### Authentication Headers

When using raw API:
```
X-API-Key: lsv2_pt_...
X-Auth-Scheme: langsmith-api-key
```

---

## MCP Server Integration

### Overview

Agent Builder integrates with Model Context Protocol (MCP) servers for custom tool access beyond built-in options.

### Configuring MCP Servers

1. Navigate to workspace settings
2. Add MCP server configuration
3. Configure authentication headers if required
4. System auto-discovers available tools

### Using MCP Tools

Once configured, MCP tools appear in the tool selection panel. Agent Builder:
- Automatically discovers available tools
- Applies configured auth headers during invocation
- Handles tool responses like built-in tools

---

## Slack Integration

### Setting Up Slack App

1. Navigate to Agent Builder settings
2. Select Slack integration
3. Click "Add to Slack"
4. Authorize in your Slack workspace
5. Configure allowed channels

### Using Agents in Slack

Once integrated:
- Mention the agent in channels: `@AgentName help me with...`
- Send DMs directly to the agent
- Agent can post updates and notifications

### Slack-Specific Features

- Read message history for context
- Post to specific channels
- Send direct messages
- React to messages (limited)

---

## Agent Visibility

### Private Agents
- Only visible to creator
- Personal use and testing
- Cannot be shared with workspace

### Workspace Agents
- Visible to all workspace members
- Can be invoked by team members
- Read-only access for non-owners
- Shared tool configurations

### Changing Visibility

1. Open agent settings
2. Navigate to Visibility section
3. Toggle between Private and Workspace
4. Save changes

---

## Templates

### Available Templates

| Template | Description |
|----------|-------------|
| **Email Assistant** | Manage inbox, draft responses, apply labels |
| **Team Updates** | Aggregate updates from Linear, GitHub, Slack |
| **Research Assistant** | Search web, summarize findings |
| **Calendar Manager** | Schedule meetings, check availability |

### Using Templates

1. Browse templates in Agent Builder
2. Click "Use this template"
3. Authorize required services
4. Customize prompts and settings
5. Test in chat panel

### Customizing Templates

After selecting a template:
- Modify agent instructions/prompt
- Add or remove tools
- Configure triggers
- Adjust approval requirements
- Add sub-agents

---

## Best Practices

### Security

- Store API keys in workspace secrets, not prompts
- Enable approval pauses for destructive actions
- Use Agent Builder-specific keys for usage tracking
- Regularly rotate API keys

### Agent Design

- Start with templates, customize incrementally
- Use clear, specific prompts
- Test thoroughly before deploying triggers
- Implement approval workflows for sensitive operations

### Performance

- Minimize unnecessary tool calls in prompts
- Use sub-agents for specialized tasks
- Configure appropriate trigger conditions
- Monitor agent runs in LangSmith

### Debugging

- Use Test Chat panel for interactive debugging
- Review tool call logs in LangSmith
- Check workspace secrets configuration
- Verify OAuth connections are active

---

## Troubleshooting

### "API key not found"
```
Ensure workspace secret is configured:
Settings → Secrets → Add OPENAI_API_KEY or ANTHROPIC_API_KEY
```

### OAuth Tool Not Working
```
1. Go to agent settings
2. Click "Disconnect" on the tool
3. Re-authorize via OAuth flow
4. Test tool access
```

### Agent Not Responding to Triggers
```
1. Verify trigger conditions
2. Check workspace secrets
3. Ensure tool authorizations are active
4. Review trigger logs in LangSmith
```

### MCP Tools Not Available
```
1. Check MCP server configuration
2. Verify authentication headers
3. Ensure MCP server is running
4. Check tool discovery logs
```

---

## Pricing and Limits

Agent Builder usage is tied to your LangSmith plan:
- Free tier: Limited agent runs
- Plus tier: Increased limits
- Enterprise: Custom limits

Check docs.langchain.com/langsmith/pricing for current details.

---

## Resources

- **Documentation**: https://docs.langchain.com/langsmith/agent-builder
- **LangSmith**: https://smith.langchain.com
- **LangGraph SDK (Python)**: https://pypi.org/project/langgraph-sdk/
- **LangGraph SDK (JS)**: https://www.npmjs.com/package/@langchain/langgraph-sdk
- **MCP Framework**: https://modelcontextprotocol.io

---

## Example Workflows

### Email Management Agent

```
Agent: Email Assistant
Tools: Gmail
Triggers: New email in inbox

Prompt:
"You are an email assistant. For each new email:
1. Categorize by priority (urgent, normal, low)
2. Apply appropriate labels
3. Draft responses for urgent items
4. Summarize action items daily"
```

### GitHub PR Reviewer

```
Agent: PR Review Assistant
Tools: GitHub, Slack
Triggers: New PR opened

Prompt:
"When a new PR is opened:
1. Read the PR description and changed files
2. Summarize the changes
3. Check for common issues
4. Post summary to #dev-updates Slack channel
5. If changes look significant, request approval before commenting"
```

### Daily Standup Aggregator

```
Agent: Standup Bot
Tools: Linear, GitHub, Slack
Triggers: Daily at 9 AM

Prompt:
"Every morning:
1. Fetch yesterday's completed Linear issues
2. Get merged PRs from GitHub
3. Compile into a standup summary
4. Post to #standup Slack channel"
```
