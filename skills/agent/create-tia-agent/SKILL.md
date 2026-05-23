---
name: create-tia-agent
description: Guides users through creating a new TIA XMPP agent based on mistral-minimal. Use when the user wants to create, build, set up, or scaffold a new agent, bot, or when they ask how to get started with TIA.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Create TIA Agent

This Skill helps you create a new TIA XMPP agent by copying and customizing the `mistral-minimal` example.

## Instructions

When a user wants to create a new agent, follow these steps:

### 1. Understand Requirements

Ask the user:
- **Agent name**: What should the agent be called? (lowercase, no spaces)
- **LLM provider**: Which LLM API? (Mistral, Groq, Claude, OpenAI, Ollama, etc.)
- **Location**: Where should the new agent directory be created? (default: `../my-agent`)
- **Server**: Which XMPP server? (default: `tensegrity.it`)
- **Room**: Which MUC room to join? (default: `general@conference.tensegrity.it`)

### 2. Copy mistral-minimal Template

```bash
cp -r mistral-minimal /path/to/new-agent
cd /path/to/new-agent
```

### 3. Update Configuration Files

#### package.json
- Update `name` field to the agent name
- Verify dependencies (tia-agents, hyperdata-clients, dotenv)

#### .env
- Copy `.env.example` to `.env`
- Add the required API key (e.g., `MISTRAL_API_KEY`, `GROQ_API_KEY`, etc.)
- Optionally override XMPP settings

#### config/agents/*.ttl
- Rename `mistral2.ttl` to `<agent-name>.ttl`
- Update all occurrences of `mistral2` to the new agent name
- Update `xmpp:service`, `xmpp:domain` if using different server
- Update `agent:roomJid` if joining different room
- Update `agent:nickname` to desired display name

#### mistral-example.js
- Rename to `<agent-name>.js` or keep as-is
- Update `PROFILE_NAME` default to match your agent name
- Update package.json `main` and `start` script if renamed

### 4. Customize the Provider

If using a different LLM provider, edit `mistral-provider.js`:

**For Groq:**
```javascript
import { Groq } from "hyperdata-clients";

export class GroqProvider extends BaseLLMProvider {
  initializeClient(apiKey) {
    return new Groq({ apiKey });
  }

  async completeChatRequest({ messages, maxTokens, temperature }) {
    return await this.client.client.chat.completions.create({
      model: this.model,
      messages,
      max_tokens: maxTokens,
      temperature
    });
  }

  extractResponseText(response) {
    return response.choices[0]?.message?.content?.trim() || null;
  }
}
```

**For Claude:**
```javascript
import { Claude } from "hyperdata-clients";

export class ClaudeProvider extends BaseLLMProvider {
  initializeClient(apiKey) {
    return new Claude({ apiKey });
  }

  async completeChatRequest({ messages, maxTokens, temperature }) {
    return await this.client.client.messages.create({
      model: this.model,
      messages,
      max_tokens: maxTokens,
      temperature
    });
  }

  extractResponseText(response) {
    return response.content[0]?.text?.trim() || null;
  }
}
```

Update the import and class name in the main agent file accordingly.

### 5. Install and Run

```bash
npm install
npm start
```

### 6. Verify Connection

The agent should:
1. Auto-register with the XMPP server (if no password in secrets.json)
2. Connect and join the specified room
3. Respond when mentioned by name

Test by sending a message in the room: `@agent-name hello`

## Common Customizations

### Change System Prompt

Edit the agent's `.ttl` file:

```turtle
agent:aiProvider [
  a agent:MistralProvider ;
  agent:model "mistral-small-latest" ;
  agent:systemPrompt "You are a helpful assistant specializing in..." ;
  agent:apiKeyEnv "MISTRAL_API_KEY"
] .
```

### Enable Lingue Protocol Features

In the `.ttl` file:

```turtle
agent:aiProvider [
  a agent:MistralProvider ;
  agent:lingueEnabled true ;
  agent:lingueConfidenceMin 0.7 ;
  agent:ibisSummaryEnabled true
] .
```

### Change Model

Update the model in the `.ttl` file:

```turtle
agent:aiProvider [
  a agent:MistralProvider ;
  agent:model "mistral-large-latest"
] .
```

Or for Groq:
```turtle
agent:aiProvider [
  a agent:GroqProvider ;
  agent:model "llama-3.3-70b-versatile"
] .
```

### Add Multiple Rooms

Agents can only join one room via the profile, but you can:
1. Create multiple agent profiles (one per room)
2. Run the same agent code with different `AGENT_PROFILE` env vars

### Custom Message Handling

Extend the provider's `handle` method or create a custom provider by extending `BaseProvider`.

## File Structure Reference

```
my-agent/
├── config/agents/
│   ├── my-agent.ttl           # Agent profile
│   ├── mistral-base.ttl       # Base profile (keep or customize)
│   └── secrets.json           # Auto-generated XMPP passwords
├── my-provider.js             # LLM provider implementation
├── my-agent.js                # Main agent runner
├── package.json               # Dependencies and scripts
├── .env                       # API keys and overrides
├── .env.example               # Template
└── README.md                  # Documentation

```

## Troubleshooting

### Agent won't connect
- Check XMPP server settings in `.ttl` file
- Verify `NODE_TLS_REJECT_UNAUTHORIZED=0` if using self-signed certs
- Check server is reachable: `telnet tensegrity.it 5222`

### API errors
- Verify API key is correct in `.env`
- Check API key environment variable name matches `agent:apiKeyEnv` in profile
- Ensure API key has necessary permissions

### Agent doesn't respond
- Check the agent joined the room (look for presence in XMPP client)
- Try mentioning the agent: `@agent-name hello`
- Check logs for errors

### Profile loading errors
- Verify `.ttl` syntax (common issue: missing dots at end of statements)
- Check all prefixes are defined
- Ensure agent resource identifier matches filename

## Next Steps

After creating your agent:

1. **Customize behavior**: Edit system prompts and model parameters
2. **Add features**: Implement custom handlers in the provider
3. **Deploy**: Run on a server with `pm2` or systemd
4. **Monitor**: Watch logs and chat activity
5. **Iterate**: Adjust prompts and settings based on behavior

## Additional Resources

- [TIA Documentation](https://danja.github.io/tia/)
- [Provider Guide](docs/provider-guide.md)
- [Lingue Protocol](https://danja.github.io/lingue/)
- [hyperdata-clients](https://www.npmjs.com/package/hyperdata-clients)

## Examples

See [mistral-minimal/README.md](mistral-minimal/README.md) for the complete reference implementation.
