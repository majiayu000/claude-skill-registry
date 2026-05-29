---
name: agentkit
version: "1.0.0"
description: Coinbase AgentKit - Toolkit for enabling AI agents with crypto wallets and onchain capabilities. Use for building autonomous agents that can execute transfers, swaps, DeFi operations, NFT minting, and smart contract interactions.
---

# Coinbase AgentKit Skill

AgentKit is Coinbase's developer toolkit that enables AI agents to interact with blockchain networks through secure wallet management and comprehensive onchain capabilities. Built on the Coinbase Developer Platform (CDP) SDK, it provides everything needed to create autonomous agents that can perform sophisticated blockchain operations.

**Core Mission**: "Every AI agent deserves a wallet."

## When to Use This Skill

This skill should be triggered when:
- Building AI agents with crypto wallet capabilities
- Creating autonomous agents that need to execute blockchain transactions
- Implementing token transfers, swaps, or DeFi operations in AI agents
- Deploying smart contracts or NFTs through AI agents
- Integrating LangChain, Vercel AI SDK, or MCP with blockchain functionality
- Building chatbots that can perform onchain actions
- Setting up agents with Coinbase CDP wallet infrastructure
- Creating multi-chain agents (EVM + Solana)
- Integrating x402 payment capabilities with AI agents

## Quick Reference

### Installation

**TypeScript (Node.js 22+):**
```bash
# Quick start with CLI
npm create onchain-agent@latest
cd onchain-agent
mv .env.local .env
npm install
npm run dev
```

**Python (3.10+):**
```bash
# Quick start with CLI
pipx run create-onchain-agent
cd onchain-agent
mv .env.local .env
poetry install
poetry run python chatbot.py
```

**Framework-Specific Packages:**
```bash
# Core package
npm install @coinbase/agentkit

# LangChain integration
npm install @coinbase/agentkit @coinbase/agentkit-langchain

# Vercel AI SDK integration
npm install @coinbase/agentkit-vercel-ai-sdk @coinbase/agentkit ai @ai-sdk/openai

# MCP integration
npm install @coinbase/agentkit @coinbase/agentkit-model-context-protocol

# Nightly builds
npm install @coinbase/agentkit@nightly
```

**Python Packages:**
```bash
# Core package
pip install coinbase-agentkit

# LangChain integration
pip install coinbase-agentkit-langchain

# OpenAI Agents SDK integration
pip install coinbase-agentkit-openai-agents-sdk

# Nightly builds
pip install --pre coinbase-agentkit
```

### Environment Setup

```bash
# Required
CDP_API_KEY_NAME=your_api_key_name
CDP_API_KEY_PRIVATE_KEY=your_private_key
OPENAI_API_KEY=your_openai_key

# Optional
NETWORK_ID=base-sepolia  # or base-mainnet, ethereum-mainnet, solana-devnet
```

### Basic Agent Setup (TypeScript)

```typescript
import { AgentKit, CdpWalletProvider } from "@coinbase/agentkit";
import { getLangChainTools } from "@coinbase/agentkit-langchain";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";

// Initialize wallet provider
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
});

// Create AgentKit instance
const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [
    cdpApiActionProvider,
    erc20ActionProvider,
    walletActionProvider,
  ],
});

// Get tools for LangChain
const tools = await getLangChainTools(agentKit);

// Create agent
const llm = new ChatOpenAI({ model: "gpt-4o" });
const agent = createReactAgent({ llm, tools });

// Execute
const result = await agent.invoke({
  messages: [{ role: "user", content: "What's my wallet address?" }],
});
```

### Basic Agent Setup (Python)

```python
from coinbase_agentkit import AgentKit, CdpWalletProvider
from coinbase_agentkit_langchain import get_langchain_tools
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

# Initialize wallet provider
wallet_provider = CdpWalletProvider.configure_with_wallet(
    network_id="base-sepolia"
)

# Create AgentKit instance
agent_kit = AgentKit.from_config(wallet_provider=wallet_provider)

# Get tools for LangChain
tools = get_langchain_tools(agent_kit)

# Create agent
llm = ChatOpenAI(model="gpt-4o")
agent = create_react_agent(llm, tools)

# Execute
result = agent.invoke({
    "messages": [{"role": "user", "content": "What's my wallet balance?"}]
})
```

## Package Reference

| Package | Purpose |
|---------|---------|
| `@coinbase/agentkit` | Core SDK with wallet providers and action providers |
| `@coinbase/agentkit-langchain` | LangChain framework integration |
| `@coinbase/agentkit-vercel-ai-sdk` | Vercel AI SDK integration |
| `@coinbase/agentkit-model-context-protocol` | MCP server integration |
| `coinbase-agentkit` | Python core SDK |
| `coinbase-agentkit-langchain` | Python LangChain integration |
| `coinbase-agentkit-openai-agents-sdk` | OpenAI Agents SDK integration |
| `coinbase-agentkit-pydantic-ai` | Pydantic AI integration |

## Wallet Providers

### EVM Wallet Providers

| Provider | Description |
|----------|-------------|
| `CdpWalletProvider` | CDP API Wallet (standard) |
| `CdpV2EvmWalletProvider` | CDP V2 API (newer interface) |
| `SmartWalletProvider` | CDP Smart Wallets (account abstraction) |
| `ViemWalletProvider` | Viem library-based wallet |
| `PrivyWalletProvider` | Privy embedded wallets |
| `ZeroDevWalletProvider` | ZeroDev smart accounts |

### SVM (Solana) Wallet Providers

| Provider | Description |
|----------|-------------|
| `CdpV2SolanaWalletProvider` | CDP V2 API for Solana |
| `SolanaKeypairWalletProvider` | Direct keypair wallet |

### Wallet Provider Configuration

```typescript
// CDP Wallet Provider
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  // Optional: persist wallet
  cdpWalletData: existingWalletData,
});

// Smart Wallet Provider (from CDP wallet)
const smartWalletProvider = await SmartWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  signer: cdpWalletProvider,
});

// Solana Wallet Provider
const solanaProvider = await CdpV2SolanaWalletProvider.configureWithWallet({
  networkId: "solana-devnet",
});
```

## Action Providers

AgentKit includes 50+ TypeScript and 30+ Python action providers:

### Core Actions

| Action Provider | Actions |
|-----------------|---------|
| `walletActionProvider` | `get_wallet_details`, `get_balance`, `native_transfer` |
| `cdpApiActionProvider` | `request_faucet_funds`, `trade`, `register_basename` |
| `erc20ActionProvider` | `transfer`, `get_balance`, `approve`, `check_allowance` |

### DeFi Actions

| Action Provider | Actions |
|-----------------|---------|
| `compoundActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `aaveActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `morphoActionProvider` | `morpho_deposit`, `morpho_withdraw` |
| `moonwellActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `jupiterActionProvider` | Solana token swaps |

### NFT & Token Actions

| Action Provider | Actions |
|-----------------|---------|
| `erc721ActionProvider` | `mint_nft`, `transfer_nft`, `get_nft_balance` |
| `zoraActionProvider` | Zora NFT platform integration |
| `openseaActionProvider` | OpenSea marketplace integration |
| `wethActionProvider` | `wrap_eth`, `unwrap_eth` |

### Social & Other Actions

| Action Provider | Actions |
|-----------------|---------|
| `farcasterActionProvider` | Post casts, read feed |
| `twitterActionProvider` | Tweet, read timeline |
| `basenameActionProvider` | Register `.base.eth` names |
| `pythActionProvider` | Price oracle data |
| `x402ActionProvider` | x402 payment integration |

### Using Action Providers

```typescript
import {
  AgentKit,
  CdpWalletProvider,
  cdpApiActionProvider,
  erc20ActionProvider,
  compoundActionProvider,
  walletActionProvider,
} from "@coinbase/agentkit";

const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [
    cdpApiActionProvider,
    erc20ActionProvider,
    compoundActionProvider({ networkId: "base-sepolia" }),
    walletActionProvider,
  ],
});
```

## Framework Integrations

### LangChain Integration

```typescript
import { AgentKit, CdpWalletProvider } from "@coinbase/agentkit";
import { getLangChainTools } from "@coinbase/agentkit-langchain";
import { ChatOpenAI } from "@langchain/openai";
import { createReactAgent } from "@langchain/langgraph/prebuilt";
import { MemorySaver } from "@langchain/langgraph";

// Setup AgentKit
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
});
const agentKit = await AgentKit.from({ walletProvider });

// Create LangChain tools
const tools = await getLangChainTools(agentKit);

// Create agent with memory
const llm = new ChatOpenAI({ model: "gpt-4o" });
const memory = new MemorySaver();
const agent = createReactAgent({
  llm,
  tools,
  checkpointSaver: memory,
});

// Stream responses
const stream = await agent.stream(
  { messages: [{ role: "user", content: "Transfer 0.01 ETH to 0x..." }] },
  { configurable: { thread_id: "session-1" } }
);

for await (const chunk of stream) {
  console.log(chunk);
}
```

### Vercel AI SDK Integration

```typescript
import { AgentKit, CdpWalletProvider } from "@coinbase/agentkit";
import { getVercelAITools } from "@coinbase/agentkit-vercel-ai-sdk";
import { openai } from "@ai-sdk/openai";
import { generateText } from "ai";

// Setup AgentKit
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
});
const agentKit = await AgentKit.from({ walletProvider });

// Get Vercel AI tools
const tools = getVercelAITools(agentKit);

// Generate response
const { text } = await generateText({
  model: openai("gpt-4o"),
  tools,
  maxSteps: 10,
  prompt: "What is my wallet balance?",
});
```

### MCP Server Integration

```typescript
import { AgentKit, CdpWalletProvider } from "@coinbase/agentkit";
import { getMcpTools } from "@coinbase/agentkit-model-context-protocol";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// Setup AgentKit
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
});
const agentKit = await AgentKit.from({ walletProvider });

// Create MCP server
const server = new McpServer({ name: "agentkit-mcp", version: "1.0.0" });

// Register AgentKit tools
const tools = getMcpTools(agentKit);
tools.forEach((tool) => server.tool(tool.name, tool.description, tool.schema, tool.handler));

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "agentkit": {
      "command": "node",
      "args": ["/path/to/agentkit-mcp-server.js"],
      "env": {
        "CDP_API_KEY_NAME": "your_key_name",
        "CDP_API_KEY_PRIVATE_KEY": "your_private_key",
        "NETWORK_ID": "base-sepolia"
      }
    }
  }
}
```

### OpenAI Agents SDK Integration (Python)

```python
from agents import Agent, Runner
from coinbase_agentkit import AgentKit, CdpWalletProvider
from coinbase_agentkit_openai_agents_sdk import get_openai_tools

# Setup AgentKit
wallet_provider = CdpWalletProvider.configure_with_wallet(
    network_id="base-sepolia"
)
agent_kit = AgentKit.from_config(wallet_provider=wallet_provider)

# Get OpenAI tools
tools = get_openai_tools(agent_kit)

# Create agent
agent = Agent(
    name="Crypto Agent",
    instructions="You are an AI agent with a crypto wallet. Help users with onchain operations.",
    tools=tools,
)

# Run agent
result = await Runner.run(agent, "What's my wallet address?")
print(result.final_output)
```

## Supported Networks

### EVM Networks

| Network | ID | Status |
|---------|----|---------|
| Base Mainnet | `base-mainnet` | Production |
| Base Sepolia | `base-sepolia` | Testnet |
| Ethereum Mainnet | `ethereum-mainnet` | Production |
| Ethereum Sepolia | `ethereum-sepolia` | Testnet |
| Arbitrum | `arbitrum-mainnet` | Production |
| Optimism | `optimism-mainnet` | Production |
| Polygon | `polygon-mainnet` | Production |

### SVM Networks

| Network | ID | Status |
|---------|----|---------|
| Solana Mainnet | `solana-mainnet` | Production |
| Solana Devnet | `solana-devnet` | Testnet |

## Common Patterns

### Persisting Wallet Data

```typescript
// Export wallet data for persistence
const walletData = await walletProvider.exportWallet();
// Store walletData securely (encrypted in database, etc.)

// Restore wallet from data
const restoredProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  cdpWalletData: walletData,
});
```

### Creating Custom Action Providers

```typescript
import { ActionProvider, CreateAction, ActionMetadata } from "@coinbase/agentkit";
import { z } from "zod";

class MyActionProvider extends ActionProvider {
  @CreateAction({
    name: "my_custom_action",
    description: "Does something custom",
    schema: z.object({
      param: z.string().describe("A parameter"),
    }),
  })
  async myCustomAction(params: { param: string }): Promise<string> {
    // Implementation
    return `Processed: ${params.param}`;
  }
}

// Register custom provider
const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [new MyActionProvider()],
});
```

### Multi-Chain Agent

```typescript
// EVM wallet for Base
const evmProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
});

// Solana wallet
const solanaProvider = await CdpV2SolanaWalletProvider.configureWithWallet({
  networkId: "solana-devnet",
});

// Create agents for each chain
const evmAgentKit = await AgentKit.from({ walletProvider: evmProvider });
const solanaAgentKit = await AgentKit.from({ walletProvider: solanaProvider });
```

### x402 Payment Integration

```typescript
import { AgentKit, CdpWalletProvider, x402ActionProvider } from "@coinbase/agentkit";

const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [x402ActionProvider],
});

// Agent can now make x402 payments for paid APIs
```

## CLI Tools

### TypeScript CLI

```bash
# Install globally
npm install -g @coinbase/agentkit

# Generate components
agentkit generate wallet-provider    # Custom wallet provider
agentkit generate action-provider    # Custom action provider
agentkit generate prepare            # Framework-agnostic setup
agentkit generate create-agent       # Framework-specific agent
```

### Python CLI

```bash
# Create new project
pipx run create-onchain-agent

# With beginner defaults
pipx run create-onchain-agent --beginner
```

## Security Considerations

- **Wallet Isolation**: Each agent should have its own dedicated wallet
- **Fund Limits**: Only fund agent wallets with amounts needed for operations
- **Key Management**: Store CDP API keys and wallet data securely
- **Network Selection**: Use testnets (base-sepolia, solana-devnet) for development
- **Action Auditing**: Log all agent actions for review

**Important Disclaimer**: "Acts proposed or performed by an agent through AgentKit software are NOT acts of Coinbase." Use at your own risk.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **wallet-providers.md** - Detailed wallet provider configuration
- **action-providers.md** - Complete action provider reference
- **framework-integrations.md** - LangChain, Vercel AI SDK, MCP, OpenAI examples
- **examples.md** - Full chatbot and agent implementations

## Resources

- [AgentKit Documentation](https://docs.cdp.coinbase.com/agent-kit/welcome)
- [GitHub Repository](https://github.com/coinbase/agentkit)
- [npm Package](https://www.npmjs.com/package/@coinbase/agentkit)
- [PyPI Package](https://pypi.org/project/coinbase-agentkit/)
- [Python API Reference](https://coinbase.github.io/agentkit/coinbase-agentkit/python/index.html)
- [AgentKit Quickstart](https://docs.cdp.coinbase.com/agent-kit/getting-started/quickstart)
- [Architecture Explained](https://docs.cdp.coinbase.com/agent-kit/core-concepts/architecture-explained)
- [Wallet Management](https://docs.cdp.coinbase.com/agent-kit/core-concepts/wallet-management)
- [MCP Integration](https://docs.cdp.coinbase.com/agent-kit/core-concepts/model-context-protocol)
- [Vercel AI SDK Integration](https://docs.cdp.coinbase.com/agent-kit/core-concepts/vercel-ai-sdk)
- [Community Guides](https://docs.cdp.coinbase.com/agent-kit/support/community-guides)
- [FAQ](https://docs.cdp.coinbase.com/agent-kit/support/faq)

## Notes

- AgentKit is framework-agnostic (works with LangChain, Vercel AI SDK, MCP, OpenAI, etc.)
- AgentKit is wallet-agnostic (supports CDP, Privy, Viem, ZeroDev wallets)
- 50+ action providers in TypeScript, 30+ in Python
- Supports EVM chains (Base, Ethereum, Arbitrum, etc.) and Solana
- USDC held in agent wallets is eligible for 4.1% rewards
- Built on CDP SDK with secure wallet infrastructure
- Licensed under Apache 2.0

## Version History

- **1.0.0** (2026-01-08): Initial release
  - Core AgentKit documentation
  - Wallet providers reference (CDP, Smart, Viem, Privy, Solana)
  - Action providers reference (50+ actions)
  - Framework integrations (LangChain, Vercel AI SDK, MCP, OpenAI)
  - Multi-chain support (EVM + Solana)
  - CLI tools documentation
