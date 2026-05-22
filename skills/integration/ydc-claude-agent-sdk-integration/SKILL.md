---
name: ydc-claude-agent-sdk-integration
description: Integrate Claude Agent SDK with You.com HTTP MCP server for Python and TypeScript. Use when developer mentions Claude Agent SDK, Anthropic Agent SDK, or integrating Claude with MCP tools.
license: MIT
compatibility: Python 3.10+ or TypeScript 5.2+ (for v2), Node.js 18+
metadata:
  author: youdotcom-oss
  category: sdk-integration
  version: "1.0.0"
  keywords: claude,anthropic,claude-agent-sdk,agent-sdk,mcp,you.com,integration,http-mcp,web-search,python,typescript
---

# Integrate Claude Agent SDK with You.com MCP

Interactive workflow to set up Claude Agent SDK with You.com's HTTP MCP server.

## Workflow

1. **Ask: Language Choice**
   * Python or TypeScript?

2. **If TypeScript - Ask: SDK Version**
   * v1 (stable, generator-based) or v2 (preview, send/receive pattern)?
   * Note: v2 requires TypeScript 5.2+ for `await using` support

3. **Install Package**
   * Python: `pip install claude-agent-sdk`
   * TypeScript: `npm install @anthropic-ai/claude-agent-sdk`

4. **Ask: Environment Variables**
   * Using standard `YDC_API_KEY` and `ANTHROPIC_API_KEY`?
   * Or custom names?
   * Have they set them?
   * If NO: Guide to get keys:
     - YDC_API_KEY: https://you.com/platform/api-keys
     - ANTHROPIC_API_KEY: https://console.anthropic.com/settings/keys

5. **Ask: File Location**
   * NEW file: Ask where to create and what to name
   * EXISTING file: Ask which file to integrate into (add HTTP MCP config)

6. **Create/Update File**

   **For NEW files:**
   * Use the complete template code from the "Complete Templates" section below
   * User can run immediately with their API keys set

   **For EXISTING files:**
   * Add HTTP MCP server configuration to their existing code
   * Python configuration block:
     ```python
     from claude_agent_sdk import query, ClaudeAgentOptions

     options = ClaudeAgentOptions(
         mcp_servers={
             "ydc": {
                 "type": "http",
                 "url": "https://api.you.com/mcp",
                 "headers": {
                     "Authorization": f"Bearer {os.getenv('YDC_API_KEY')}"
                 }
             }
         },
         allowed_tools=[
             "mcp__ydc__you_search",
             "mcp__ydc__you_express",
             "mcp__ydc__you_contents"
         ]
     )
     ```

   * TypeScript configuration block:
     ```typescript
     const options = {
       mcpServers: {
         ydc: {
           type: 'http' as const,
           url: 'https://api.you.com/mcp',
           headers: {
             Authorization: `Bearer ${process.env.YDC_API_KEY}`
           }
         }
       },
       allowedTools: [
         'mcp__ydc__you_search',
         'mcp__ydc__you_express',
         'mcp__ydc__you_contents'
       ]
     };
     ```

## Complete Templates

Use these complete templates for new files. Each template is ready to run with your API keys set.

### Python Template (Complete Example)

```python
"""
Claude Agent SDK with You.com HTTP MCP Server
Python implementation with async/await pattern
"""

import os
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

# Validate environment variables
ydc_api_key = os.getenv("YDC_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not ydc_api_key:
    raise ValueError(
        "YDC_API_KEY environment variable is required. "
        "Get your key at: https://you.com/platform/api-keys"
    )

if not anthropic_api_key:
    raise ValueError(
        "ANTHROPIC_API_KEY environment variable is required. "
        "Get your key at: https://console.anthropic.com/settings/keys"
    )


async def main():
    """
    Example: Search for AI news and get results from You.com MCP server
    """
    # Configure Claude Agent with HTTP MCP server
    options = ClaudeAgentOptions(
        mcp_servers={
            "ydc": {
                "type": "http",
                "url": "https://api.you.com/mcp",
                "headers": {"Authorization": f"Bearer {ydc_api_key}"},
            }
        },
        allowed_tools=[
            "mcp__ydc__you_search",
            "mcp__ydc__you_express",
            "mcp__ydc__you_contents",
        ],
        model="claude-sonnet-4-5-20250929",
    )

    # Query Claude with MCP tools available
    async for message in query(
        prompt="Search for the latest AI news from this week",
        options=options,
    ):
        # Handle different message types
        if message.type == "text":
            print(message.content)
        elif message.type == "tool_use":
            print(f"\n[Tool: {message.name}]")
            print(f"Input: {message.input}")
        elif message.type == "tool_result":
            print(f"Result: {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript v1 Template (Complete Example)

```typescript
/**
 * Claude Agent SDK with You.com HTTP MCP Server
 * TypeScript v1 implementation with generator-based pattern
 */

import { query } from '@anthropic-ai/claude-agent-sdk';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const anthropicApiKey = process.env.ANTHROPIC_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!anthropicApiKey) {
  throw new Error(
    'ANTHROPIC_API_KEY environment variable is required. ' +
      'Get your key at: https://console.anthropic.com/settings/keys'
  );
}

/**
 * Example: Search for AI news and get results from You.com MCP server
 */
async function main() {
  // Query Claude with HTTP MCP configuration
  const result = query({
    prompt: 'Search for the latest AI news from this week',
    options: {
      mcpServers: {
        ydc: {
          type: 'http' as const,
          url: 'https://api.you.com/mcp',
          headers: {
            Authorization: `Bearer ${ydcApiKey}`,
          },
        },
      },
      allowedTools: [
        'mcp__ydc__you_search',
        'mcp__ydc__you_express',
        'mcp__ydc__you_contents',
      ],
      model: 'claude-sonnet-4-5-20250929',
    },
  });

  // Process messages as they arrive
  for await (const msg of result) {
    if (msg.type === 'text') {
      console.log(msg.content);
    } else if (msg.type === 'tool_use') {
      console.log(`\n[Tool: ${msg.name}]`);
      console.log(`Input: ${JSON.stringify(msg.input, null, 2)}`);
    } else if (msg.type === 'tool_result') {
      console.log(`Result: ${msg.content}`);
    }
  }
}

main().catch(console.error);
```

### TypeScript v2 Template (Complete Example)

```typescript
/**
 * Claude Agent SDK with You.com HTTP MCP Server
 * TypeScript v2 implementation with send/receive pattern
 * Requires TypeScript 5.2+ for 'await using' support
 */

import { unstable_v2_createSession } from '@anthropic-ai/claude-agent-sdk';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const anthropicApiKey = process.env.ANTHROPIC_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!anthropicApiKey) {
  throw new Error(
    'ANTHROPIC_API_KEY environment variable is required. ' +
      'Get your key at: https://console.anthropic.com/settings/keys'
  );
}

/**
 * Example: Search for AI news and get results from You.com MCP server
 */
async function main() {
  // Create session with HTTP MCP configuration
  // 'await using' ensures automatic cleanup when scope exits
  await using session = unstable_v2_createSession({
    mcpServers: {
      ydc: {
        type: 'http' as const,
        url: 'https://api.you.com/mcp',
        headers: {
          Authorization: `Bearer ${ydcApiKey}`,
        },
      },
    },
    allowedTools: [
      'mcp__ydc__you_search',
      'mcp__ydc__you_express',
      'mcp__ydc__you_contents',
    ],
    model: 'claude-sonnet-4-5-20250929',
  });

  // Send message to Claude
  await session.send('Search for the latest AI news from this week');

  // Receive and process messages
  for await (const msg of session.receive()) {
    if (msg.type === 'text') {
      console.log(msg.content);
    } else if (msg.type === 'tool_use') {
      console.log(`\n[Tool: ${msg.name}]`);
      console.log(`Input: ${JSON.stringify(msg.input, null, 2)}`);
    } else if (msg.type === 'tool_result') {
      console.log(`Result: ${msg.content}`);
    }
  }
}

main().catch(console.error);
```

## HTTP MCP Server Configuration

All templates use You.com's **HTTP MCP server** for simplicity:

**Python:**
```python
mcp_servers={
    "ydc": {
        "type": "http",
        "url": "https://api.you.com/mcp",
        "headers": {
            "Authorization": f"Bearer {ydc_api_key}"
        }
    }
}
```

**TypeScript:**
```typescript
mcpServers: {
  ydc: {
    type: 'http' as const,
    url: 'https://api.you.com/mcp',
    headers: {
      Authorization: `Bearer ${ydcApiKey}`
    }
  }
}
```

**Benefits of HTTP MCP:**
- ✅ No local installation required
- ✅ Stateless request/response model
- ✅ Always up-to-date with latest version
- ✅ Consistent across all environments
- ✅ Production-ready and scalable
- ✅ Works with existing HTTP infrastructure

## Available You.com Tools

After configuration, Claude can discover and use:
- `mcp__ydc__you_search` - Web and news search
- `mcp__ydc__you_express` - AI-powered answers with web context
- `mcp__ydc__you_contents` - Web page content extraction

## Environment Variables

Both API keys are required:

```bash
# Add to your .env file or shell profile
export YDC_API_KEY="your-you-api-key-here"
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

**Get your API keys:**
- You.com: https://you.com/platform/api-keys
- Anthropic: https://console.anthropic.com/settings/keys

## Validation Checklist

Before completing:

- [ ] Package installed: `claude-agent-sdk` (Python) or `@anthropic-ai/claude-agent-sdk` (TypeScript)
- [ ] Environment variables set: `YDC_API_KEY` and `ANTHROPIC_API_KEY`
- [ ] Template copied or configuration added to existing file
- [ ] HTTP MCP server configured (`https://api.you.com/mcp`)
- [ ] Authorization header includes `Bearer ${YDC_API_KEY}`
- [ ] Allowed tools list includes You.com tools
- [ ] File is executable (Python) or can be compiled (TypeScript)
- [ ] Ready to test with example query

## Testing Your Integration

**Python:**
```bash
python your-file.py
```

**TypeScript:**
```bash
# With tsx (recommended for quick testing)
npx tsx your-file.ts

# Or compile and run
tsc your-file.ts && node your-file.js
```

## Common Issues

<details>
<summary><strong>Cannot find module @anthropic-ai/claude-agent-sdk</strong></summary>

Install the package:

```bash
# NPM
npm install @anthropic-ai/claude-agent-sdk

# Bun
bun add @anthropic-ai/claude-agent-sdk

# Yarn
yarn add @anthropic-ai/claude-agent-sdk

# pnpm
pnpm add @anthropic-ai/claude-agent-sdk
```

</details>

<details>
<summary><strong>YDC_API_KEY environment variable is required</strong></summary>

Set your You.com API key:

```bash
export YDC_API_KEY="your-api-key-here"
```

Get your key at: https://you.com/platform/api-keys

</details>

<details>
<summary><strong>ANTHROPIC_API_KEY environment variable is required</strong></summary>

Set your Anthropic API key:

```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

Get your key at: https://console.anthropic.com/settings/keys

</details>

<details>
<summary><strong>MCP connection fails with 401 Unauthorized</strong></summary>

Verify your YDC_API_KEY is valid:
1. Check the key at https://you.com/platform/api-keys
2. Ensure no extra spaces or quotes in the environment variable
3. Verify the Authorization header format: `Bearer ${YDC_API_KEY}`

</details>

<details>
<summary><strong>Tools not available or not being called</strong></summary>

Ensure `allowedTools` includes the correct tool names:
- `mcp__ydc__you_search` (not `you_search`)
- `mcp__ydc__you_express` (not `you_express`)
- `mcp__ydc__you_contents` (not `you_contents`)

Tool names must include the `mcp__ydc__` prefix.

</details>

<details>
<summary><strong>TypeScript error: Cannot use 'await using'</strong></summary>

The v2 SDK requires TypeScript 5.2+ for `await using` syntax.

**Solution 1: Update TypeScript**
```bash
npm install -D typescript@latest
```

**Solution 2: Use manual cleanup**
```typescript
const session = unstable_v2_createSession({ /* options */ });
try {
  await session.send('Your query');
  for await (const msg of session.receive()) {
    // Process messages
  }
} finally {
  session.close();
}
```

**Solution 3: Use v1 SDK instead**
Choose v1 during setup for broader TypeScript compatibility.

</details>



## Additional Resources

* You.com MCP Server: https://documentation.you.com/developer-resources/mcp-server
* Claude Agent SDK (Python): https://platform.claude.com/docs/en/agent-sdk/python
* Claude Agent SDK (TypeScript v1): https://platform.claude.com/docs/en/agent-sdk/typescript
* Claude Agent SDK (TypeScript v2): https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview
* API Keys:
  - You.com: https://you.com/platform/api-keys
  - Anthropic: https://console.anthropic.com/settings/keys
