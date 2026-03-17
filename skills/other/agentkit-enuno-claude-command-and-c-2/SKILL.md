---
name: agentkit
version: "1.1.0"
description: Coinbase AgentKit - Toolkit for enabling AI agents with crypto wallets and onchain capabilities. Use for building autonomous agents that can execute transfers, swaps, DeFi operations, NFT minting, smart contract deployment, and gasless transactions via Smart Wallets.
---

# Coinbase AgentKit Skill

AgentKit is Coinbase Developer Platform's toolkit that enables AI agents to interact with blockchain networks through secure wallet management and comprehensive onchain capabilities. Built on the Coinbase Developer Platform (CDP) SDK, it provides everything needed to create autonomous agents that can perform sophisticated blockchain operations.

**Core Mission**: "Every AI agent deserves a wallet."

**Repository Stats**: 1,000+ GitHub stars | 590 forks | 90+ contributors | 578 dependent projects

## When to Use This Skill

This skill should be triggered when:
- Building AI agents with crypto wallet capabilities
- Creating autonomous agents that need to execute blockchain transactions
- Implementing token transfers, swaps, or DeFi operations in AI agents
- Deploying smart contracts or NFTs through AI agents
- Integrating LangChain, Vercel AI SDK, MCP, or OpenAI Agents SDK with blockchain functionality
- Building chatbots that can perform onchain actions
- Setting up agents with Coinbase CDP wallet infrastructure
- Creating multi-chain agents (EVM + Solana)
- Implementing gasless transactions with Smart Wallets
- Integrating x402 payment capabilities with AI agents
- Using Pydantic AI or Strands Agents with blockchain features

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

# Nightly builds (bleeding edge)
npm install @coinbase/agentkit@nightly
```

**Python Packages:**
```bash
# Core package (v0.7.4+)
pip install coinbase-agentkit

# LangChain integration
pip install coinbase-agentkit-langchain

# OpenAI Agents SDK integration
pip install coinbase-agentkit-openai-agents-sdk

# Pydantic AI integration
pip install coinbase-agentkit-pydantic-ai

# Strands Agents integration
pip install coinbase-agentkit-strands

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
| `@coinbase/agentkit` | Core SDK with wallet providers and action providers (50+ actions) |
| `@coinbase/agentkit-langchain` | LangChain framework integration |
| `@coinbase/agentkit-vercel-ai-sdk` | Vercel AI SDK integration |
| `@coinbase/agentkit-model-context-protocol` | MCP server integration |
| `coinbase-agentkit` | Python core SDK (v0.7.4, 30+ actions) |
| `coinbase-agentkit-langchain` | Python LangChain integration |
| `coinbase-agentkit-openai-agents-sdk` | OpenAI Agents SDK integration |
| `coinbase-agentkit-pydantic-ai` | Pydantic AI integration |
| `coinbase-agentkit-strands` | Strands Agents integration |

## Wallet Providers

### EVM Wallet Providers

| Provider | Description |
|----------|-------------|
| `CdpEvmWalletProvider` | CDP V2 API Server Wallet (standard) |
| `CdpSmartWalletProvider` | CDP Smart Wallets (ERC-4337, gasless transactions) |
| `SmartWalletProvider` | CDP Smart Wallets (alternative interface) |
| `ViemWalletProvider` | Viem library-based wallet |
| `PrivyWalletProvider` | Privy embedded/server wallets |
| `ZeroDevWalletProvider` | ZeroDev smart accounts (chain abstraction) |
| `EthAccountWalletProvider` | Local private key for any EVM chain |

### SVM (Solana) Wallet Providers

| Provider | Description |
|----------|-------------|
| `CdpV2SolanaWalletProvider` | CDP V2 API for Solana |
| `CdpSolanaWalletProvider` | CDP Solana wallet (mainnet, devnet, testnet) |
| `SolanaKeypairWalletProvider` | Direct keypair wallet |
| `PrivyWalletProvider` | Privy Solana mode |

### Wallet Provider Configuration

```typescript
// CDP EVM Wallet Provider
const walletProvider = await CdpEvmWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  // Optional: persist wallet
  cdpWalletData: existingWalletData,
});

// Smart Wallet Provider (gasless transactions)
const smartWalletProvider = await CdpSmartWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  signer: cdpWalletProvider,
  // Enable gasless via paymaster
  paymasterUrl: "https://paymaster.base.org",
});

// Solana Wallet Provider
const solanaProvider = await CdpSolanaWalletProvider.configureWithWallet({
  networkId: "solana-devnet",
});

// ZeroDev Wallet Provider (chain abstraction)
const zeroDevProvider = await ZeroDevWalletProvider.configureWithWallet({
  projectId: "your-zerodev-project-id",
  networkId: "base-sepolia",
});
```

## Action Providers

AgentKit includes **50+ TypeScript** and **30+ Python** action providers:

### Core Actions

| Action Provider | Actions |
|-----------------|---------|
| `walletActionProvider` | `get_wallet_details`, `get_balance`, `native_transfer` |
| `cdpApiActionProvider` | `request_faucet_funds`, `trade`, `register_basename` |
| `erc20ActionProvider` | `transfer`, `get_balance`, `approve`, `check_allowance` |
| `erc721ActionProvider` | `mint_nft`, `transfer_nft`, `get_nft_balance` |

### DeFi Protocol Actions

| Action Provider | Actions |
|-----------------|---------|
| `compoundActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `aaveActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `morphoActionProvider` | `morpho_deposit`, `morpho_withdraw` |
| `moonwellActionProvider` | `supply`, `withdraw`, `borrow`, `repay` |
| `superfluidActionProvider` | Token streaming operations |
| `yelayActionProvider` | Vault operations |

### Swap & Bridge Actions

| Action Provider | Actions |
|-----------------|---------|
| `jupiterActionProvider` | Solana token swaps |
| `zeroXActionProvider` | 0x swap integration |
| `sushiActionProvider` | Sushi swap integration |
| `acrossActionProvider` | Cross-chain bridging |

### NFT & Token Actions

| Action Provider | Actions |
|-----------------|---------|
| `zoraActionProvider` | Zora NFT platform, coin creation |
| `openseaActionProvider` | OpenSea marketplace integration |
| `wethActionProvider` | `wrap_eth`, `unwrap_eth` |
| `clankerActionProvider` | Clanker token creation |
| `flaunchActionProvider` | Token launch functionality |
| `wowActionProvider` | WOW memecoin trading |

### Social & External Actions

| Action Provider | Actions |
|-----------------|---------|
| `farcasterActionProvider` | Post casts, read feed |
| `twitterActionProvider` | Tweet, read timeline |
| `basenameActionProvider` | Register `.base.eth` names |
| `sshActionProvider` | SSH operations |
| `hyperbolicActionProvider` | AI compute generation |

### Data & Oracle Actions

| Action Provider | Actions |
|-----------------|---------|
| `pythActionProvider` | Price oracle data feeds |
| `defillamaActionProvider` | DeFi data aggregation |
| `messariActionProvider` | Crypto research data |
| `zerionActionProvider` | Portfolio tracking |

### Payment & Infrastructure Actions

| Action Provider | Actions |
|-----------------|---------|
| `x402ActionProvider` | x402 payment integration for paid APIs |
| `onrampActionProvider` | Fiat-to-crypto conversion |
| `nillionActionProvider` | Encrypted data (SecretVault) |
| `ensoActionProvider` | DeFi aggregation |

### Using Action Providers

```typescript
import {
  AgentKit,
  CdpWalletProvider,
  cdpApiActionProvider,
  erc20ActionProvider,
  compoundActionProvider,
  walletActionProvider,
  x402ActionProvider,
  superfluidActionProvider,
} from "@coinbase/agentkit";

const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [
    cdpApiActionProvider,
    erc20ActionProvider,
    compoundActionProvider({ networkId: "base-sepolia" }),
    walletActionProvider,
    x402ActionProvider,
    superfluidActionProvider,
  ],
});
```

## Smart Wallets & Gasless Transactions

Smart Wallets are ERC-4337 compliant smart contract wallets providing:
- **Gasless transactions** - No ETH required for gas fees
- **Batch operations** - Multiple actions in one transaction
- **Account recovery** - Secure recovery mechanisms
- **Sponsored transactions** - Via paymaster integration

**Note**: Smart Wallets are currently only supported on Base networks (base-sepolia, base-mainnet).

```typescript
import { CdpSmartWalletProvider } from "@coinbase/agentkit";

// Configure Smart Wallet with gasless transactions
const smartWalletProvider = await CdpSmartWalletProvider.configureWithWallet({
  networkId: "base-mainnet",
  // Enable gasless via paymaster
  paymasterUrl: "https://your-paymaster.example.com",
});

// Create AgentKit with smart wallet
const agentKit = await AgentKit.from({
  walletProvider: smartWalletProvider,
  actionProviders: [walletActionProvider, erc20ActionProvider],
});

// Agent can now transact without holding ETH for gas
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

### Pydantic AI Integration (Python)

```python
from coinbase_agentkit import AgentKit, CdpWalletProvider
from coinbase_agentkit_pydantic_ai import get_pydantic_tools

# Setup AgentKit
wallet_provider = CdpWalletProvider.configure_with_wallet(
    network_id="base-sepolia"
)
agent_kit = AgentKit.from_config(wallet_provider=wallet_provider)

# Get Pydantic AI tools
tools = get_pydantic_tools(agent_kit)
```

## Supported Networks

### EVM Networks

| Network | ID | Status |
|---------|----|--------|
| Base Mainnet | `base-mainnet` | Production |
| Base Sepolia | `base-sepolia` | Testnet |
| Ethereum Mainnet | `ethereum-mainnet` | Production |
| Ethereum Sepolia | `ethereum-sepolia` | Testnet |
| Arbitrum | `arbitrum-mainnet` | Production |
| Optimism | `optimism-mainnet` | Production |
| Polygon | `polygon-mainnet` | Production |

### SVM Networks

| Network | ID | Status |
|---------|----|--------|
| Solana Mainnet | `solana-mainnet` | Production |
| Solana Devnet | `solana-devnet` | Testnet |
| Solana Testnet | `solana-testnet` | Testnet |

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

### Python Custom Action Provider

```python
from coinbase_agentkit import ActionProvider, create_action
from pydantic import BaseModel

class MyParams(BaseModel):
    param: str

class MyActionProvider(ActionProvider):
    @create_action(
        name="my_custom_action",
        description="Does something custom",
        schema=MyParams,
    )
    async def my_custom_action(self, params: MyParams) -> str:
        return f"Processed: {params.param}"
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

### Idempotent Wallet Creation

```typescript
// Create deterministic wallet using idempotency key
const walletProvider = await CdpWalletProvider.configureWithWallet({
  networkId: "base-sepolia",
  idempotencyKey: "user-123-wallet",  // Same key always returns same wallet
});
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
- **Smart Wallet Benefits**: Use Smart Wallets for enhanced security features

**Important Disclaimer**: "Acts proposed or performed by an agent through AgentKit software are NOT acts of Coinbase." Use at your own risk. The software is novel and experimental, provided on an AS-IS basis.

## Q1 2025 Milestones

Key features shipped in Q1 2025:
- **Smart Wallet Integration**: Gasless transactions via CDP Smart Wallet API
- **Built-in Faucet**: Seamless testing on Base Sepolia
- **Onramps**: Fiat-to-crypto conversion in agent apps
- **Smart Contract Deployment**: Agents can deploy contracts onchain
- **Solana Support**: Expanded beyond EVM ecosystem
- **Quickstart CLI**: One-command project setup
- **OpenAI Agents SDK Integration**: Day-one support

## USDC Rewards

USDC held in agent wallets is eligible for 4.1% rewards when using CDP wallets.

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **wallet-providers.md** - Detailed wallet provider configuration
- **action-providers.md** - Complete action provider reference (50+ actions)
- **framework-integrations.md** - LangChain, Vercel AI SDK, MCP, OpenAI, Pydantic examples

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
- [Smart Wallets Guide](https://docs.cdp.coinbase.com/agent-kit/core-concepts/smart-wallets)
- [Community Guides](https://docs.cdp.coinbase.com/agent-kit/support/community-guides)
- [FAQ](https://docs.cdp.coinbase.com/agent-kit/support/faq)
- [AgentKit Q1 Update](https://www.coinbase.com/developer-platform/discover/launches/agentkit-q1-update)

## Notes

- AgentKit is framework-agnostic (works with LangChain, Vercel AI SDK, MCP, OpenAI, Pydantic AI, Strands, etc.)
- AgentKit is wallet-agnostic (supports CDP, Privy, Viem, ZeroDev wallets)
- 50+ action providers in TypeScript, 30+ in Python
- Supports EVM chains (Base, Ethereum, Arbitrum, etc.) and Solana
- USDC held in agent wallets is eligible for 4.1% rewards
- Smart Wallets enable gasless transactions on Base networks
- Built on CDP SDK with secure wallet infrastructure
- Licensed under Apache 2.0

## Version History

- **1.1.0** (2026-01-09): Enhanced with Q1 2025 updates
  - Added Smart Wallet gasless transaction documentation
  - Added 20+ new action providers (Across, Superfluid, Enso, Zora coins, etc.)
  - Added Pydantic AI and Strands Agents integrations
  - Added ZeroDev and additional wallet providers
  - Updated Python package version to 0.7.4
  - Added Q1 2025 milestones section
  - Enhanced custom action provider examples
  - Added idempotent wallet creation pattern

- **1.0.0** (2026-01-08): Initial release
  - Core AgentKit documentation
  - Wallet providers reference (CDP, Smart, Viem, Privy, Solana)
  - Action providers reference (50+ actions)
  - Framework integrations (LangChain, Vercel AI SDK, MCP, OpenAI)
  - Multi-chain support (EVM + Solana)
  - CLI tools documentation
