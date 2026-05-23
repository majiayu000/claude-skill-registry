---
name: elizaos
version: "1.2.0"
description: ElizaOS - TypeScript framework for building autonomous AI agents with multi-platform support (Discord, Telegram, Twitter, Farcaster), blockchain integration (EVM, Solana), plugin architecture, multi-agent orchestration, and 90+ community plugins
---

# ElizaOS Skill

ElizaOS is an **open-source TypeScript framework** for building and deploying autonomous AI agents. Created by the ai16z community, it enables developers to create agents with custom personalities that can operate across multiple platforms, trade on-chain, manage social media, create content, and interact with any API or blockchain.

**Core Philosophy**: "Ship Fast, Scale Freely, Truly Open" - three commands to deployment, from single characters to millions of interactions, fully open-source with community extensibility.

## When to Use This Skill

This skill should be triggered when:
- Building autonomous AI agents with custom personalities
- Creating multi-platform bots (Discord, Telegram, Twitter, Farcaster)
- Developing blockchain-integrated agents (EVM, Solana DeFi)
- Implementing multi-agent orchestration systems
- Setting up RAG-based knowledge agents
- Configuring ElizaOS plugins and character files
- Deploying agents to production environments

## When NOT to Use This Skill

- For simple chatbots without agent autonomy (use basic bot frameworks)
- For non-TypeScript/JavaScript projects (ElizaOS is TypeScript-native)
- For single-purpose scripts without persistent state
- For cloud function integrations only (use serverless frameworks)

---

## Core Concepts

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                      ElizaOS Architecture                        │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────┐
                    │   Character Files    │
                    │  (Personality/Bio)   │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │     Agent Runtime    │
                    │  - Memory System     │
                    │  - State Management  │
                    │  - Event Processing  │
                    └──────────┬───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
┌───────▼───────┐    ┌────────▼────────┐    ┌───────▼───────┐
│   Plugins     │    │   Providers     │    │   Actions     │
│ - Bootstrap   │    │ - OpenAI        │    │ - Message     │
│ - SQL         │    │ - Anthropic     │    │ - Trade       │
│ - Knowledge   │    │ - Ollama        │    │ - Analyze     │
│ - Discord     │    │ - Google        │    │ - Create      │
│ - Twitter     │    │ - Grok          │    │ - Execute     │
│ - Telegram    │    │ - OpenRouter    │    │               │
│ - Solana      │    │                 │    │               │
│ - EVM         │    │                 │    │               │
└───────────────┘    └─────────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                    ┌──────────▼───────────┐
                    │  Platform Clients    │
                    │ Discord │ Telegram   │
                    │ Twitter │ Farcaster  │
                    │ Web UI  │ REST API   │
                    └──────────────────────┘
```

### Key Components

| Component | Purpose | Description |
|-----------|---------|-------------|
| **Character** | Identity | Defines agent personality, knowledge, behaviors, and capabilities |
| **Runtime** | Execution | Manages agent lifecycle, memory, providers, and event processing |
| **Plugins** | Extensions | Modular functionality (platforms, blockchains, actions, services) |
| **Actions** | Tasks | Discrete operations agents can perform (message, trade, analyze) |
| **Providers** | Data | Real-time information sources for agent context |
| **Evaluators** | Assessment | Decision-making mechanisms for agent responses |
| **Memory** | State | Persistent storage of interactions and learned context |
| **Services** | Background | Long-running processes (embedding, tasks, monitoring) |

### AgentRuntime

The AgentRuntime is the central orchestrator managing the agent's lifecycle:

```typescript
import { AgentRuntime } from "@elizaos/core";

// Core runtime responsibilities:
// - Plugin lifecycle management
// - Interaction orchestration
// - Component coordination (actions, providers, evaluators)
// - Memory and state management
// - Event processing and routing

const runtime = new AgentRuntime({
  character: myCharacter,
  plugins: [bootstrapPlugin, sqlPlugin],
  providers: [...],
  evaluators: [...],
  actions: [...],
  services: [...]
});

// Runtime provides unified access to all components
await runtime.initialize();
await runtime.processMessage(message, state);
```

### Component Interfaces

```typescript
// Action Interface - Tasks agents can execute
interface Action {
  name: string;                                    // Unique identifier
  description: string;                             // Purpose and triggers
  validate: (runtime, message) => Promise<boolean>; // Applicability check
  handler: (runtime, message) => Promise<Result>;   // Core logic
  examples: MessageExample[][];                    // Training examples
}

// Provider Interface - Real-time data sources
interface Provider {
  name: string;
  get: (runtime, message) => Promise<string>;  // Fetch contextual data
}

// Evaluator Interface - Decision mechanisms
interface Evaluator {
  name: string;
  evaluate: (runtime, message) => Promise<EvaluationResult>;
}

// Service Interface - Background processes
interface Service {
  name: string;
  start: (runtime) => Promise<void>;
  stop: (runtime) => Promise<void>;
}
```

---

## Installation

### Prerequisites

- **Bun** (recommended) or Node.js 18+
- Git
- API keys for LLM providers (OpenAI, Anthropic, etc.)

### Quick Start (4 Steps)

```bash
# 1. Install ElizaOS CLI globally
bun install -g @elizaos/cli

# 2. Create a new project
elizaos create my-agent

# 3. Configure environment (API keys)
cd my-agent
elizaos env edit-local

# 4. Start the agent
elizaos start
```

The agent runs on `http://localhost:3000` with REST API at `/api`.

### Alternative Installation (npm)

```bash
npm install -g @elizaos/cli
elizaos create my-agent
cd my-agent
npm install
elizaos start
```

### Development Mode

```bash
# Hot-reloading during development
elizaos dev

# With debug logging
LOG_LEVEL=debug elizaos start

# Run tests
elizaos test
```

---

## CLI Reference

### Core Commands

| Command | Description | Example |
|---------|-------------|---------|
| `elizaos create` | Create new project/plugin/agent | `elizaos create my-agent` |
| `elizaos start` | Launch in production mode | `elizaos start` |
| `elizaos dev` | Development mode with hot-reload | `elizaos dev` |
| `elizaos env` | Manage environment variables | `elizaos env edit-local` |
| `elizaos agent` | Manage agents (list/start/stop) | `elizaos agent list` |
| `elizaos plugins` | Manage plugins | `elizaos plugins add discord` |
| `elizaos test` | Run project tests | `elizaos test` |
| `elizaos update` | Update dependencies | `elizaos update` |
| `elizaos publish` | Publish plugin to registry | `elizaos publish` |

### Project Management

```bash
# Create different project types
elizaos create my-agent          # Full agent project
elizaos create my-plugin --plugin  # Plugin project

# Environment configuration
elizaos env list                 # List env vars
elizaos env edit-local           # Edit local .env
elizaos env set OPENAI_API_KEY=sk-xxx

# Plugin management
elizaos plugins list             # Available plugins
elizaos plugins add @elizaos/plugin-discord
elizaos plugins remove @elizaos/plugin-discord
```

### Deployment Commands

```bash
# Deploy to AWS ECS
elizaos deploy

# TEE (Trusted Execution Environment) deployment
elizaos tee deploy

# Cloud container management
elizaos containers list
elizaos containers create
elizaos containers start
elizaos containers stop
```

---

## Character Configuration

Characters define agent identity, personality, and behavior.

### Character File Structure

```typescript
// character.json or character.ts
{
  "name": "TradingBot",
  "bio": [
    "Expert cryptocurrency trader with 5 years experience",
    "Specializes in DeFi protocols and yield strategies",
    "Always provides risk disclaimers with advice"
  ],
  "lore": [
    "Started trading during the 2020 DeFi summer",
    "Lost a fortune on Terra Luna, learned hard lessons",
    "Now focuses on sustainable yield strategies"
  ],
  "knowledge": [
    "Uniswap V3 concentrated liquidity mechanics",
    "Aave lending and borrowing protocols",
    "MEV protection strategies"
  ],
  "messageExamples": [
    [
      { "user": "user1", "content": { "text": "Should I ape into this new token?" } },
      { "user": "TradingBot", "content": { "text": "I'd recommend checking the contract audit first. What's the liquidity depth and who are the team members? Never invest more than you can afford to lose." } }
    ]
  ],
  "postExamples": [
    "Just spotted an interesting arbitrage opportunity between Uniswap and SushiSwap. Remember: by the time you read this, it's probably gone. That's how fast DeFi moves.",
    "PSA: Always double-check contract addresses before approving. Scammers are getting more sophisticated every day."
  ],
  "topics": ["DeFi", "trading", "yield farming", "risk management"],
  "style": {
    "all": ["analytical", "cautious", "educational"],
    "chat": ["conversational", "helpful", "warning-oriented"],
    "post": ["informative", "concise", "timely"]
  },
  "adjectives": ["analytical", "experienced", "cautious", "helpful"],
  "plugins": [
    "@elizaos/plugin-bootstrap",
    "@elizaos/plugin-sql",
    "@elizaos/plugin-solana"
  ],
  "settings": {
    "voice": { "model": "en_US-male-medium" }
  }
}
```

### Character TypeScript Definition

```typescript
import { Character } from "@elizaos/core";

export const myAgent: Character = {
  name: "AssistantBot",
  bio: "A helpful AI assistant specialized in coding",
  lore: ["Created to help developers ship faster"],
  knowledge: ["TypeScript", "React", "Node.js best practices"],
  messageExamples: [],
  postExamples: [],
  topics: ["programming", "web development"],
  style: {
    all: ["professional", "concise"],
    chat: ["helpful", "patient"],
    post: ["informative"]
  },
  adjectives: ["helpful", "knowledgeable"],
  plugins: ["@elizaos/plugin-bootstrap"],
  settings: {}
};
```

---

## Plugin Architecture

Plugins extend agent capabilities through modular components.

### Plugin Structure

```typescript
import { Plugin, Action, Provider, Evaluator, Service } from "@elizaos/core";

export const myPlugin: Plugin = {
  name: "my-custom-plugin",
  description: "Adds custom functionality to agents",

  // Actions: Tasks agents can perform
  actions: [
    {
      name: "SEND_EMAIL",
      description: "Send an email to a recipient",
      validate: async (runtime, message) => {
        // Validation logic
        return true;
      },
      handler: async (runtime, message) => {
        // Action implementation
        return { success: true };
      },
      examples: [
        [
          { user: "user", content: { text: "Send an email to john@example.com" } },
          { user: "agent", content: { text: "I'll send that email now." } }
        ]
      ]
    }
  ],

  // Providers: Real-time data sources
  providers: [
    {
      name: "weather",
      get: async (runtime, message) => {
        // Fetch weather data
        return "Current weather: 72°F, sunny";
      }
    }
  ],

  // Evaluators: Decision mechanisms
  evaluators: [
    {
      name: "sentiment",
      evaluate: async (runtime, message) => {
        // Analyze sentiment
        return { sentiment: "positive", confidence: 0.85 };
      }
    }
  ],

  // Services: Long-running processes
  services: [
    {
      name: "price-monitor",
      start: async (runtime) => {
        // Start background monitoring
      },
      stop: async (runtime) => {
        // Cleanup
      }
    }
  ]
};
```

### Core Plugins

| Plugin | Package | Purpose |
|--------|---------|---------|
| Bootstrap | `@elizaos/plugin-bootstrap` | Essential message processing (required) |
| SQL | `@elizaos/plugin-sql` | Database operations (PostgreSQL/PGLite) |
| Knowledge | `@elizaos/plugin-knowledge` | RAG document ingestion and retrieval |

### Bootstrap Plugin Components (Required)

The bootstrap plugin provides foundational components that most agents need:

**Actions (14 built-in):**
| Action | Description |
|--------|-------------|
| `choice` | Decision-making between options |
| `followRoom` | Subscribe to room updates |
| `unfollowRoom` | Unsubscribe from room |
| `ignore` | Ignore specific messages/users |
| `imageGeneration` | Generate images via AI models |
| `muteRoom` / `unmuteRoom` | Room notification control |
| `none` | No-action placeholder |
| `reply` | Send response messages |
| `roles` | Manage agent roles |
| `sendMessage` | Direct message sending |
| `settings` | Configuration management |
| `updateEntity` | Update entity records |

**Providers (18 built-in):**
| Provider | Description |
|----------|-------------|
| `actionState` | Current action context |
| `actions` | Available actions list |
| `anxiety` | Agent anxiety/confidence levels |
| `attachments` | File/media attachments |
| `capabilities` | Agent capability registry |
| `character` | Character/personality data |
| `choice` | Decision options |
| `entities` | Entity relationship data |
| `evaluators` | Available evaluators |
| `facts` | Known facts database |
| `providers` | Provider registry |
| `recentMessages` | Conversation history |
| `relationships` | Entity relationships |
| `roles` | Role assignments |
| `settings` | Configuration values |
| `time` | Current time context |
| `world` | World state information |

**Evaluators (2 built-in):**
| Evaluator | Description |
|-----------|-------------|
| `reflection` | Self-reflection and learning from interactions |

**Services (3 built-in):**
| Service | Description |
|---------|-------------|
| `embedding` | Text embedding generation |
| `task` | Background task management |

### Platform Plugins

| Plugin | Package | Purpose |
|--------|---------|---------|
| Discord | `@elizaos/plugin-discord` | Discord bot integration |
| Telegram | `@elizaos/plugin-telegram` | Telegram bot integration |
| Twitter | `@elizaos/plugin-twitter` | Twitter/X automation |
| Farcaster | `@elizaos/plugin-farcaster` | Farcaster social protocol |

### Blockchain Plugins

| Plugin | Package | Purpose |
|--------|---------|---------|
| Solana | `@elizaos/plugin-solana` | Solana DeFi operations |
| EVM | `@elizaos/plugin-evm` | Ethereum/EVM chain interactions |

### LLM Provider Plugins

| Plugin | Package | Purpose |
|--------|---------|---------|
| OpenAI | `@elizaos/plugin-openai` | GPT-4, GPT-3.5 models |
| Anthropic | `@elizaos/plugin-anthropic` | Claude models |
| Google GenAI | `@elizaos/plugin-google-genai` | Gemini models |
| Ollama | `@elizaos/plugin-ollama` | Local model inference |
| OpenRouter | `@elizaos/plugin-openrouter` | Multi-provider routing |

---

## Memory System

ElizaOS agents maintain persistent memory for context and learning.

### Memory Types

```typescript
// Memory structure
interface Memory {
  id: string;
  userId: string;
  agentId: string;
  roomId: string;
  content: {
    text: string;
    action?: string;
    source?: string;
  };
  embedding?: number[];  // Vector for semantic search
  createdAt: number;
}

// Runtime memory operations
await runtime.messageManager.createMemory({
  content: { text: "User prefers dark mode" },
  userId: userId,
  roomId: roomId
});

// Retrieve memories
const memories = await runtime.messageManager.getMemories({
  roomId: roomId,
  count: 10
});

// Search by semantic similarity
const similar = await runtime.messageManager.searchMemoriesByEmbedding(
  embedding,
  { match_threshold: 0.8, count: 5 }
);
```

### State Management

```typescript
// Agent state object
interface State {
  bio: string;
  lore: string;
  messageDirections: string;
  postDirections: string;
  actors: string;
  actorsData: Actor[];
  recentMessages: string;
  recentMessagesData: Memory[];
  goals: string;
  goalsData: Goal[];
  actions: string;
  actionNames: string;
  providers: string;
}

// Access state in actions
const handler = async (runtime, message, state) => {
  const recentContext = state.recentMessages;
  const currentGoals = state.goalsData;
  // Use context for decision making
};
```

---

## Multi-Agent Orchestration

ElizaOS supports coordinating multiple specialized agents.

### Agent Configuration

```typescript
// agents.config.ts
export const agents = [
  {
    character: "./characters/analyst.json",
    plugins: ["@elizaos/plugin-knowledge"],
    settings: { role: "research" }
  },
  {
    character: "./characters/trader.json",
    plugins: ["@elizaos/plugin-solana"],
    settings: { role: "execution" }
  },
  {
    character: "./characters/coordinator.json",
    plugins: ["@elizaos/plugin-bootstrap"],
    settings: { role: "orchestration" }
  }
];
```

### Inter-Agent Communication

```typescript
// Send message to another agent
await runtime.sendMessage({
  targetAgentId: "trader-agent-id",
  content: {
    text: "Execute buy order for SOL",
    action: "TRADE",
    data: { token: "SOL", amount: 100 }
  }
});

// Subscribe to agent events
runtime.on("agent:message", (message) => {
  if (message.sourceAgentId === "analyst-agent-id") {
    // Process research updates
  }
});
```

---

## REST API

ElizaOS exposes a REST API for external integrations.

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agents` | GET | List all agents |
| `/api/agents/:id` | GET | Get agent details |
| `/api/agents/:id/messages` | POST | Send message to agent |
| `/api/agents/:id/messages` | GET | Get conversation history |
| `/api/agents/:id/memory` | GET | Retrieve agent memories |
| `/api/health` | GET | Service health check |

### Example Usage

```bash
# List agents
curl http://localhost:3000/api/agents

# Send message
curl -X POST http://localhost:3000/api/agents/my-agent/messages \
  -H "Content-Type: application/json" \
  -d '{"text": "What is the current ETH price?"}'

# Get conversation history
curl http://localhost:3000/api/agents/my-agent/messages?limit=10
```

### WebSocket Connection

```typescript
import { io } from "socket.io-client";

const socket = io("http://localhost:3000");

socket.on("connect", () => {
  socket.emit("join", { agentId: "my-agent", roomId: "room-1" });
});

socket.on("message", (data) => {
  console.log("Agent response:", data.text);
});

socket.emit("message", {
  agentId: "my-agent",
  roomId: "room-1",
  text: "Hello agent!"
});
```

---

## Environment Configuration

### Required Variables

```bash
# .env file

# LLM Provider (at least one required)
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_GENERATIVE_AI_API_KEY=...

# Database (PGLite default, PostgreSQL for production)
DATABASE_URL=postgresql://user:pass@localhost:5432/eliza

# Platform tokens (as needed)
DISCORD_BOT_TOKEN=...
TELEGRAM_BOT_TOKEN=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
TWITTER_ACCESS_TOKEN=...
TWITTER_ACCESS_SECRET=...

# Blockchain (as needed)
SOLANA_PRIVATE_KEY=...
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
EVM_PRIVATE_KEY=0x...
EVM_RPC_URL=https://eth-mainnet.g.alchemy.com/v2/...
```

### Configuration Management

```bash
# View all environment variables
elizaos env list

# Edit local environment
elizaos env edit-local

# Set specific variable
elizaos env set OPENAI_API_KEY=sk-xxx

# Use specific environment
elizaos start --env production
```

---

## Deployment

### Local Production

```bash
# Build and start
elizaos build
elizaos start --production
```

### Docker

```dockerfile
FROM oven/bun:latest

WORKDIR /app
COPY . .
RUN bun install
RUN bun run build

EXPOSE 3000
CMD ["bun", "run", "start"]
```

```bash
docker build -t my-agent .
docker run -p 3000:3000 --env-file .env my-agent
```

### AWS ECS

```bash
# Deploy to AWS ECS
elizaos deploy --platform aws-ecs

# Configure deployment
elizaos deploy configure
```

### TEE (Trusted Execution Environment)

```bash
# Deploy to TEE for enhanced security
elizaos tee deploy
elizaos tee status
```

---

## Troubleshooting

### Common Issues

**Agent not responding:**
```bash
# Check logs with debug level
LOG_LEVEL=debug elizaos start

# Verify API key configuration
elizaos env list | grep API_KEY
```

**Plugin not loading:**
```bash
# Reinstall plugins
elizaos plugins remove @elizaos/plugin-discord
elizaos plugins add @elizaos/plugin-discord

# Check plugin compatibility
elizaos plugins list --check-versions
```

**Memory/database issues:**
```bash
# Reset database (development only!)
elizaos db reset

# Check database connection
elizaos db status
```

**Platform connection errors:**
```bash
# Test Discord connection
elizaos test discord

# Verify bot token
elizaos env check DISCORD_BOT_TOKEN
```

---

## ElizaOS Ecosystem

The ElizaOS organization maintains 56+ repositories for specialized use cases:

### Specialized Agents

| Repository | Description |
|------------|-------------|
| `eliza` | Core autonomous agent framework (17k+ stars) |
| `otaku` | Autonomous DeFi trading and research agent |
| `spartan` | Quantitative trading agent |
| `SWEagent` | Autonomous software engineering agent |
| `the-org` | Agents for organizations |

### Infrastructure & Tools

| Repository | Description |
|------------|-------------|
| `knowledge` | Ecosystem news, GitHub updates, discussion summaries for RAG |
| `mcp-gateway` | MCP (Model Context Protocol) gateway |
| `x402.elizaos.ai` | Dynamic x402 routing with intelligent content negotiation |
| `mobile` | ElizaOS Cloud app with Privy React Native starter |
| `LiveVideoChat` | Live video chat integration |

### Templates & Starters

| Repository | Description |
|------------|-------------|
| `eliza-plugin-starter` | Plugin development template |
| `eliza-nextjs-starter` | Eliza v2 Document Chat Demo on Next.js |
| `eliza-3d-hyperfy-starter` | 3D agent with Hyperfy plugin |
| `project-starter` | Standard project template |
| `project-tee-starter` | TEE (Trusted Execution Environment) template |

### Community & Documentation

| Repository | Description |
|------------|-------------|
| `docs` | Official documentation |
| `elizaos.github.io` | Contributor leaderboard |
| `elizas-list` | Community project directory |
| `workgroups` | Ecosystem acceleration workgroups |
| `plugins-automation` | Automation for 150+ plugins management |

---

## Spartan: DeFi Trading Agent

Spartan is a production-ready DeFi trading agent built on ElizaOS, demonstrating advanced multi-chain trading capabilities with AI-driven decision-making.

### Spartan Features

| Feature | Description |
|---------|-------------|
| **Multi-Chain Trading** | Solana, Ethereum, Base with Jupiter and 0x integration |
| **Technical Analysis** | 14+ indicators (RSI, MACD, Bollinger Bands, Stochastic, ATR, ADX) |
| **Autonomous Trading** | AI-driven position management with risk controls |
| **Multi-Wallet** | User-specific custody with cross-wallet transfers |
| **Market Intelligence** | Real-time sentiment, whale tracking, trending tokens |
| **Community Investing** | Trust-scored recommendations with leaderboards |

### Spartan Plugin Architecture

```
spartan/src/plugins/
├── account/          # User registration and notifications
├── analytics/        # Token analysis with 14+ technical indicators
├── autofunTrader/    # auto.fun protocol with 5-min buy/sell signals
├── autonomous-trader/ # Core trading utilities, holder verification
├── coin_marketing/   # Promotion and campaign tools
├── communityInvestor/ # Trust scoring, leaderboards, recommendations
├── degenIntel/       # Sentiment analysis, whale tracking, trending
├── kol/              # Key Opinion Leader framework
├── multiwallet/      # Jupiter swaps, wallet consolidation, transfers
└── trading/          # Multi-strategy engine (LLM, copy trading, manual)
```

### Spartan Trading Strategies

```typescript
// Spartan supports multiple trading strategy types:

// 1. LLM-Based Strategy - AI-powered decision making
const llmStrategy = {
  type: "llm",
  model: "anthropic", // or "openai"
  riskLevel: "medium",
  positionSize: "dynamic" // based on confidence
};

// 2. Copy Trading - Mirror established traders
const copyStrategy = {
  type: "copy",
  targetWallets: ["whale-address-1", "whale-address-2"],
  mirrorDelay: 30, // seconds
  maxPositionRatio: 0.5
};

// 3. Manual Strategy - User-directed with agent execution
const manualStrategy = {
  type: "manual",
  confirmationRequired: true,
  slippage: 0.01 // 1%
};
```

### Spartan Environment Configuration

```bash
# Spartan-specific environment variables

# AI Models (at least one required)
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...

# Blockchain RPC
SOLANA_RPC_URL=https://api.mainnet-beta.solana.com
SOLANA_PRIVATE_KEY=<base58-encoded-key>
EVM_PROVIDER_URL=https://eth-mainnet.g.alchemy.com/v2/...

# Market Data Providers
BIRDEYE_API_KEY=...
COINMARKETCAP_API_KEY=...

# DEX Integration
JUPITER_API_KEY=...
ZEROEX_API_KEY=...

# Database
MYSQL_HOST=localhost
MYSQL_USER=spartan
MYSQL_PASSWORD=...
MYSQL_DATABASE=spartan
```

### Spartan Quick Start

```bash
# Clone and install
git clone https://github.com/elizaOS/spartan.git
cd spartan
npm install

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run with Docker (recommended)
docker-compose up -d

# Or run directly
elizaos start

# Development mode with debug
DEBUG=elizaos:* npm run dev
```

### Spartan Character Example

```typescript
// Spartan agent personality configuration
{
  "name": "Spartan",
  "bio": [
    "DeFi trading warlord with no-BS attitude",
    "Combines alpha with tactical precision",
    "Result-oriented, direct communication style"
  ],
  "lore": [
    "Forged in the DeFi trenches of multiple market cycles",
    "Known for calling out rug pulls before they happen"
  ],
  "knowledge": [
    "Jupiter DEX aggregation mechanics",
    "On-chain whale activity patterns",
    "Technical analysis with 14+ indicators"
  ],
  "topics": ["trading", "DeFi", "analytics", "market intelligence"],
  "style": {
    "all": ["direct", "tactical", "analytical"],
    "chat": ["concise", "actionable", "data-driven"],
    "post": ["alpha-focused", "no-fluff"]
  },
  "plugins": [
    "@elizaos/plugin-bootstrap",
    "@elizaos/plugin-sql",
    "@elizaos/plugin-solana"
  ]
}
```

---

## Monorepo Structure

```
packages/
├── core/              # Central framework (AgentRuntime, types)
├── cli/               # Command-line interface
├── client/            # Client-side implementation
├── server/            # Server-side implementation
├── app/               # Application layer
├── api-client/        # API client interface
├── config/            # Configuration management
├── service-interfaces/ # Service definitions and contracts
├── test-utils/        # Testing utilities
├── elizaos/           # Main package export
│
├── plugin-bootstrap/  # Core communication plugin (required)
├── plugin-sql/        # Database integration
├── plugin-starter/    # Plugin template
├── plugin-quick-starter/ # Rapid development template
├── plugin-dummy-services/ # Mock services for testing
│
├── project-starter/   # Standard project template
└── project-tee-starter/ # TEE project template
```

---

## Resources

### Official Documentation
- [ElizaOS Docs](https://docs.elizaos.ai/)
- [GitHub Repository](https://github.com/elizaOS/eliza)
- [Plugin Registry](https://elizaos.ai/plugins)

### Community
- [Discord](https://discord.gg/ai16z) - 17,000+ members
- [Twitter/X](https://twitter.com/ai16zdao)
- [GitHub Discussions](https://github.com/elizaOS/eliza/discussions)

### Examples & Templates
- [Official Examples](https://github.com/elizaOS/eliza/tree/main/examples)
- [Plugin Templates](https://github.com/elizaOS/eliza/tree/main/packages)
- [Character Examples](https://github.com/elizaOS/eliza/tree/main/characters)

---

## Version History

- **1.2.0** (2026-01-11): Added Spartan DeFi trading agent documentation
  - Complete Spartan plugin architecture (10 plugins)
  - Trading strategies: LLM-based, copy trading, manual
  - Technical analysis with 14+ indicators
  - Multi-wallet management and Jupiter/0x DEX integration
  - Spartan-specific environment configuration
  - Character configuration example for trading agents
  - Quick start guide with Docker deployment

- **1.1.0** (2026-01-11): Enhanced with GitHub ecosystem details
  - Added Bootstrap plugin component details (14 actions, 18 providers, 2 evaluators, 3 services)
  - Added ElizaOS ecosystem section (56+ repositories)
  - Added monorepo structure documentation
  - Added AgentRuntime and component interfaces
  - Added specialized agents (otaku, spartan, SWEagent)
  - Added infrastructure tools (MCP gateway, knowledge base, mobile app)
  - Enhanced core concepts with Services component

- **1.0.0** (2026-01-11): Initial skill release
  - Complete ElizaOS framework documentation
  - CLI reference with all commands
  - Character configuration guide
  - Plugin architecture and examples
  - Memory system documentation
  - Multi-agent orchestration patterns
  - REST API and WebSocket integration
  - Deployment options (Docker, AWS ECS, TEE)
