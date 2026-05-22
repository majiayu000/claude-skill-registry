---
name: llm-router
description: This skill should be used when users want to route LLM requests to different AI providers (OpenAI, Grok/xAI, Groq, DeepSeek, OpenRouter) using SwiftOpenAI-CLI. Use this skill when users ask to "use grok", "ask grok", "use groq", "ask deepseek", or any similar request to query a specific LLM provider in agent mode.
---

# LLM Router

## Overview

Route AI requests to different LLM providers using SwiftOpenAI-CLI's agent mode. This skill automatically configures the CLI to use the requested provider (OpenAI, Grok, Groq, DeepSeek, or OpenRouter), ensures the tool is installed and up-to-date, and executes one-shot agentic tasks.

## Core Workflow

When a user requests to use a specific LLM provider (e.g., "use grok to explain quantum computing"), follow this workflow:

### Step 1: Ensure SwiftOpenAI-CLI is Ready

Check if SwiftOpenAI-CLI is installed and up-to-date:

```bash
scripts/check_install_cli.sh
```

This script will:
- Check if `swiftopenai` is installed
- Verify the version (minimum 1.4.4)
- Install or update if necessary
- Report the current installation status

### Step 2: Configure the Provider

Based on the user's request, identify the target provider and configure SwiftOpenAI-CLI:

```bash
scripts/configure_provider.sh <provider> [model]
```

**Supported providers:**
- `openai` - OpenAI (GPT-4, GPT-5, etc.)
- `grok` - xAI Grok models
- `groq` - Groq (Llama, Mixtral, etc.)
- `deepseek` - DeepSeek models
- `openrouter` - OpenRouter (300+ models)

**Examples:**

```bash
# Configure for Grok
scripts/configure_provider.sh grok grok-4-0709

# Configure for Groq with Llama
scripts/configure_provider.sh groq llama-3.3-70b-versatile

# Configure for DeepSeek Reasoner
scripts/configure_provider.sh deepseek deepseek-reasoner

# Configure for OpenAI GPT-5
scripts/configure_provider.sh openai gpt-5
```

The script automatically:
- Sets the provider configuration
- Sets the appropriate base URL
- Sets the default model
- Provides guidance on API key configuration

### Step 3: Verify API Key

The configuration script automatically checks if an API key is set and will **stop with clear instructions** if no API key is found.

**If API key is missing:**

The script exits with error code 1 and displays:
- ⚠️ Warning that API key is not set
- Instructions for setting via environment variable
- Instructions for setting via config (persistent)

**Do not proceed to Step 4 if the configuration script fails due to missing API key.**

Instead, inform the user they need to set their API key first:

**Option 1 - Environment variable (session only):**
```bash
export XAI_API_KEY=xai-...           # for Grok
export GROQ_API_KEY=gsk_...          # for Groq
export DEEPSEEK_API_KEY=sk-...       # for DeepSeek
export OPENROUTER_API_KEY=sk-or-...  # for OpenRouter
export OPENAI_API_KEY=sk-...         # for OpenAI
```

**Option 2 - Config file (persistent):**
```bash
swiftopenai config set api-key <api-key-value>
```

After the user sets their API key, re-run the configuration script to verify.

### Step 4: Execute the Agentic Task

Run the user's request using agent mode:

```bash
swiftopenai agent "<user's question or task>"
```

**Agent mode features:**
- One-shot task execution
- Built-in tool calling
- MCP (Model Context Protocol) integration support
- Conversation memory with session IDs
- Multiple output formats

**Examples:**

```bash
# Simple question
swiftopenai agent "What is quantum entanglement?"

# With specific model override
swiftopenai agent "Write a Python function" --model grok-3

# With session for conversation continuity
swiftopenai agent "Remember my name is Alice" --session-id chat-123
swiftopenai agent "What's my name?" --session-id chat-123

# With MCP tools (filesystem example)
swiftopenai agent "Read the README.md file" \
  --mcp-servers filesystem \
  --allowed-tools "mcp__filesystem__*"
```

## Usage Patterns

### Pattern 1: Simple Provider Routing

**User Request:** "Use grok to explain quantum computing"

**Execution:**

```bash
# 1. Check CLI installation
scripts/check_install_cli.sh

# 2. Configure for Grok
scripts/configure_provider.sh grok grok-4-0709

# 3. Execute the task
swiftopenai agent "Explain quantum computing"
```

### Pattern 2: Specific Model Selection

**User Request:** "Ask DeepSeek Reasoner to solve this math problem step by step"

**Execution:**

```bash
# 1. Check CLI installation
scripts/check_install_cli.sh

# 2. Configure for DeepSeek with Reasoner model
scripts/configure_provider.sh deepseek deepseek-reasoner

# 3. Execute with explicit model
swiftopenai agent "Solve x^2 + 5x + 6 = 0 step by step" --model deepseek-reasoner
```

### Pattern 3: Fast Inference with Groq

**User Request:** "Use groq to generate code quickly"

**Execution:**

```bash
# 1. Check CLI installation
scripts/check_install_cli.sh

# 2. Configure for Groq (known for fast inference)
scripts/configure_provider.sh groq llama-3.3-70b-versatile

# 3. Execute the task
swiftopenai agent "Write a function to calculate fibonacci numbers"
```

### Pattern 4: Access Multiple Models via OpenRouter

**User Request:** "Use OpenRouter to access Claude"

**Execution:**

```bash
# 1. Check CLI installation
scripts/check_install_cli.sh

# 2. Configure for OpenRouter
scripts/configure_provider.sh openrouter anthropic/claude-3.5-sonnet

# 3. Execute with Claude via OpenRouter
swiftopenai agent "Explain the benefits of functional programming"
```

## Provider-Specific Considerations

### OpenAI (GPT-5 Models)

GPT-5 models support advanced parameters:

```bash
# Minimal reasoning for fast coding tasks
swiftopenai agent "Write a sort function" \
  --model gpt-5 \
  --reasoning minimal \
  --verbose low

# High reasoning for complex problems
swiftopenai agent "Explain quantum mechanics" \
  --model gpt-5 \
  --reasoning high \
  --verbose high
```

**Verbosity levels:** `low`, `medium`, `high`
**Reasoning effort:** `minimal`, `low`, `medium`, `high`

### Grok (xAI)

Grok models are optimized for real-time information and coding:

- `grok-4-0709` - Latest with enhanced reasoning
- `grok-3` - General purpose
- `grok-code-fast-1` - Optimized for code generation

### Groq

Known for ultra-fast inference with open-source models:

- `llama-3.3-70b-versatile` - Best general purpose
- `mixtral-8x7b-32768` - Mixture of experts

### DeepSeek

Specialized in reasoning and coding:

- `deepseek-reasoner` - Advanced step-by-step reasoning
- `deepseek-coder` - Coding specialist
- `deepseek-chat` - General chat

### OpenRouter

Provides access to 300+ models:

- Anthropic Claude models
- OpenAI models
- Google Gemini models
- Meta Llama models
- And many more

## API Key Management

### Recommended: Use Environment Variables for Multiple Providers

The **best practice** for using multiple providers is to set all API keys as environment variables. This allows seamless switching between providers without reconfiguring keys.

**Add to your shell profile** (`~/.zshrc` or `~/.bashrc`):

```bash
# API Keys for LLM Providers
export OPENAI_API_KEY=sk-...
export XAI_API_KEY=xai-...
export GROQ_API_KEY=gsk_...
export DEEPSEEK_API_KEY=sk-...
export OPENROUTER_API_KEY=sk-or-v1-...
```

After adding these, reload your shell:

```bash
source ~/.zshrc  # or source ~/.bashrc
```

**How it works:**
- SwiftOpenAI-CLI automatically uses the **correct provider-specific key** based on the configured provider
- When you switch to Grok, it uses `XAI_API_KEY`
- When you switch to OpenAI, it uses `OPENAI_API_KEY`
- No need to reconfigure keys each time

### Alternative: Single API Key via Config (Not Recommended for Multiple Providers)

If you only use **one provider**, you can store the key in the config file:

```bash
swiftopenai config set api-key <your-key>
```

**Limitation:** The config file only stores ONE api-key. If you switch providers, you'd need to reconfigure the key each time.

### Checking Current API Key

```bash
# View current configuration (API key is masked)
swiftopenai config list

# Get specific API key setting
swiftopenai config get api-key
```

**Priority:** Provider-specific environment variables take precedence over config file settings.

## Advanced Features

### Interactive Configuration

For complex setups, use the interactive wizard:

```bash
swiftopenai config setup
```

This launches a guided setup that walks through:
- Provider selection
- API key entry
- Model selection
- Debug mode configuration
- Base URL setup (if needed)

### Session Management

Maintain conversation context across multiple requests:

```bash
# Start a session
swiftopenai agent "My project is a React app" --session-id project-123

# Continue the session
swiftopenai agent "What framework did I mention?" --session-id project-123
```

### MCP Tool Integration

Connect to external services via Model Context Protocol:

```bash
# With GitHub MCP
swiftopenai agent "List my repos" \
  --mcp-servers github \
  --allowed-tools "mcp__github__*"

# With filesystem MCP
swiftopenai agent "Read package.json and explain dependencies" \
  --mcp-servers filesystem \
  --allowed-tools "mcp__filesystem__*"

# Multiple MCP servers
swiftopenai agent "Complex task" \
  --mcp-servers github,filesystem,postgres \
  --allowed-tools "mcp__*"
```

### Output Formats

Control how results are presented:

```bash
# Plain text (default)
swiftopenai agent "Calculate 5 + 3" --output-format plain

# Structured JSON
swiftopenai agent "List 3 colors" --output-format json

# Streaming JSON events (Claude SDK style)
swiftopenai agent "Analyze data" --output-format stream-json
```

## Troubleshooting

### Common Issues

**Issue: "swiftopenai: command not found"**

Solution: Run the check_install_cli.sh script, which will install the CLI automatically.

**Issue: Authentication errors**

Solution: Verify the correct API key is set for the provider:

```bash
# Check current config
swiftopenai config list

# Set the appropriate API key
swiftopenai config set api-key <your-key>

# Or use environment variable
export XAI_API_KEY=xai-...  # for Grok
```

**Issue: Model not available**

Solution: Verify the model name matches the provider's available models. Check `references/providers.md` for correct model names or run:

```bash
swiftopenai models
```

**Issue: Rate limiting or quota errors**

Solution: These are provider-specific limits. Consider:
- Using a different model tier
- Switching to a different provider temporarily
- Checking your API usage dashboard

### Debug Mode

Enable debug mode to see detailed HTTP information:

```bash
swiftopenai config set debug true
```

This shows:
- HTTP status codes and headers
- API request details
- Response metadata

## Resources

This skill includes bundled resources to support LLM routing:

### scripts/

- **check_install_cli.sh** - Ensures SwiftOpenAI-CLI is installed and up-to-date
- **configure_provider.sh** - Configures the CLI for a specific provider

### references/

- **providers.md** - Comprehensive reference on all supported providers, models, configurations, and capabilities

## Best Practices

1. **Always check installation first** - Run `check_install_cli.sh` before routing requests
2. **Configure provider explicitly** - Use `configure_provider.sh` to ensure correct setup
3. **Verify API keys** - Check that the appropriate API key is set for the target provider
4. **Choose the right model** - Match the model to the task (coding, reasoning, general chat)
5. **Use sessions for continuity** - Leverage `--session-id` for multi-turn conversations
6. **Enable debug mode for troubleshooting** - When issues arise, debug mode provides valuable insights
7. **Reference provider documentation** - Consult `references/providers.md` for detailed provider information

## Examples

### Example 1: Routing to Grok for Real-Time Information

```bash
# User: "Use grok to tell me about recent AI developments"

scripts/check_install_cli.sh
scripts/configure_provider.sh grok grok-4-0709
swiftopenai agent "Tell me about recent AI developments"
```

### Example 2: Using DeepSeek for Step-by-Step Reasoning

```bash
# User: "Ask deepseek to explain how to solve this algorithm problem"

scripts/check_install_cli.sh
scripts/configure_provider.sh deepseek deepseek-reasoner
swiftopenai agent "Explain step by step how to implement quicksort"
```

### Example 3: Fast Code Generation with Groq

```bash
# User: "Use groq to quickly generate a REST API"

scripts/check_install_cli.sh
scripts/configure_provider.sh groq llama-3.3-70b-versatile
swiftopenai agent "Generate a REST API with authentication in Python"
```

### Example 4: Accessing Claude via OpenRouter

```bash
# User: "Use openrouter to access claude and write documentation"

scripts/check_install_cli.sh
scripts/configure_provider.sh openrouter anthropic/claude-3.5-sonnet
swiftopenai agent "Write comprehensive documentation for a todo app API"
```

### Example 5: GPT-5 with Custom Parameters

```bash
# User: "Use gpt-5 with high reasoning to solve this complex problem"

scripts/check_install_cli.sh
scripts/configure_provider.sh openai gpt-5
swiftopenai agent "Design a distributed caching system" \
  --model gpt-5 \
  --reasoning high \
  --verbose high
```
