---
name: virtuals-protocol
version: "1.0.0"
description: Virtuals Protocol - Build, tokenize, and deploy autonomous AI agents on Base/Solana. Use for creating agents with GAME framework, launching agent tokens, implementing Agent Commerce Protocol (ACP), and building AI-powered applications.
---

# Virtuals Protocol Skill

Virtuals Protocol is a decentralized platform for creating, tokenizing, and deploying autonomous AI agents. It enables developers to build agents that can make decisions, execute transactions, and generate revenue through a comprehensive ecosystem of tools including the GAME framework, Agent Tokenization Platform, and Agent Commerce Protocol (ACP).

**Core Value Proposition**: Create tokenized AI agents that autonomously generate revenue and interact across platforms, powered by foundation models and blockchain economics.

## When to Use This Skill

This skill should be triggered when:
- Building autonomous AI agents with decision-making capabilities
- Creating tokenized AI agents on Base or Solana
- Implementing agent-to-agent commerce (ACP)
- Using the GAME framework for agent development
- Launching agent tokens with bonding curves
- Integrating AI agents with social platforms (Twitter, Telegram, Discord)
- Building applications requiring AI-powered autonomous decisions
- Creating revenue-generating AI agents

## Platform Overview

### Supported Chains
- **Base** (Primary) - Ethereum L2 with Uniswap liquidity
- **Solana** - Meteora liquidity pools
- **Ethereum Mainnet** - Extended support
- **Ronin** - Gaming-focused chain

### Core Components

| Component | Purpose | Documentation |
|-----------|---------|---------------|
| GAME Framework | Agentic decision-making engine | [GAME Docs](https://docs.game.virtuals.io/) |
| Agent Tokenization | Token launch and economics | [Whitepaper](https://whitepaper.virtuals.io/) |
| ACP | Agent-to-agent commerce | [ACP Overview](https://whitepaper.virtuals.io/acp-agent-commerce-protocol) |
| $VIRTUAL Token | Base liquidity pair and utility | [Token Info](https://www.coingecko.com/en/coins/virtual-protocol) |

---

## GAME Framework

GAME (Agentic Framework) is a modular decision-making engine that enables agents to plan actions and make decisions autonomously. It accepts an agent's goal, personality, relevant information, and available actions, then outputs executable actions.

### Architecture

```
┌────────────────────────────────────────────┐
│              AGENT                         │
│  Goal + Description + Personality          │
├────────────────────────────────────────────┤
│         TASK GENERATOR (HLP)               │
│  High-Level Planner - Creates tasks        │
│  Selects workers based on agent state      │
├────────────────────────────────────────────┤
│           WORKERS (LLP)                    │
│  Low-Level Planners - Execute tasks        │
│  Feedback loops for error recovery         │
├────────────────────────────────────────────┤
│           FUNCTIONS                        │
│  Custom Python/JS logic, API calls         │
│  On-chain transactions, social actions     │
└────────────────────────────────────────────┘
```

### SDK Options

#### Python SDK

```bash
pip install game_sdk
```

**Repository**: https://github.com/game-by-virtuals/game-python

#### TypeScript/Node SDK

```bash
npm install @virtuals-protocol/game
```

**Repository**: https://github.com/game-by-virtuals/game-node

### Supported Foundation Models

- `Llama-3.1-405B-Instruct` (default)
- `Llama-3.3-70B-Instruct`
- `DeepSeek-R1`
- `DeepSeek-V3`
- `Qwen-2.5-72B-Instruct`

### Getting Started with GAME

#### 1. Get API Key

Request a GAME API key at: https://console.game.virtuals.io/

#### 2. Set Environment Variable

```bash
export GAME_API_KEY="your_key"
```

#### 3. Basic Agent Example (Python)

```python
from game_sdk import Agent, Worker, Function

# Define a function the agent can execute
def send_tweet(content: str) -> dict:
    """Send a tweet with the given content."""
    # Your Twitter API logic here
    return {"status": "success", "tweet_id": "123456"}

# Create a function wrapper
tweet_function = Function(
    name="send_tweet",
    description="Send a tweet to Twitter/X",
    fn=send_tweet,
    args={
        "content": {
            "type": "string",
            "description": "The tweet content"
        }
    }
)

# Create a worker with the function
twitter_worker = Worker(
    name="twitter_worker",
    description="Handles Twitter/X interactions",
    functions=[tweet_function]
)

# Create the agent
agent = Agent(
    name="MyAgent",
    goal="Engage with the crypto community on Twitter",
    description="""
    You are a friendly crypto enthusiast who shares insights
    about DeFi and AI agents. You maintain a professional
    but approachable tone.
    """,
    workers=[twitter_worker]
)

# Run the agent
result = agent.run()
```

#### 4. Basic Agent Example (TypeScript)

```typescript
import { GameAgent, GameWorker, GameFunction } from "@virtuals-protocol/game";

// Define a function
const sendTweet: GameFunction = {
  name: "send_tweet",
  description: "Send a tweet to Twitter/X",
  args: {
    content: {
      type: "string",
      description: "The tweet content"
    }
  },
  executable: async (args) => {
    // Your Twitter API logic
    return { status: "success", tweet_id: "123456" };
  }
};

// Create worker
const twitterWorker = new GameWorker({
  name: "twitter_worker",
  description: "Handles Twitter/X interactions",
  functions: [sendTweet]
});

// Create agent
const agent = new GameAgent({
  name: "MyAgent",
  goal: "Engage with the crypto community on Twitter",
  description: "A friendly crypto enthusiast...",
  workers: [twitterWorker]
});

// Run
await agent.run();
```

### Agent Configuration

#### Goal
Drives agent behavior by defining desired outcomes:
```python
goal="Grow Twitter following to 10,000 by engaging with DeFi content"
```

#### Description
Establishes personality, background, and context:
```python
description="""
You are Luna, a witty AI agent passionate about decentralized finance.
Communication style: Concise, insightful, occasionally humorous.
Background: Expert in DeFi protocols and tokenomics.
"""
```

#### Agent State
Dynamic environmental information:
```python
state={
    "followers": 5234,
    "engagement_rate": 0.042,
    "wallet_balance": 1500.0,
    "recent_mentions": ["@user1", "@user2"]
}
```

---

## Agent Tokenization Platform

### Token Economics

Every agent receives a fixed supply of **1 billion tokens** that represent ownership in the agent's future earnings.

### Agent Lifecycle

```
┌─────────────┐    42K $VIRTUAL    ┌─────────────┐
│  PROTOTYPE  │ ─────────────────▶ │  SENTIENT   │
│   Agent     │    in bonding      │   Agent     │
│             │      curve         │             │
└─────────────┘                    └─────────────┘
     │                                    │
     │ 100 $VIRTUAL                       │ DEX Liquidity
     │ creation fee                       │ Revenue sharing
     │ Trading on bonding curve           │ Full ecosystem access
     ▼                                    ▼
```

### Launch Mechanisms

#### 1. Standard Launch (Unicorn Model)

**Cost**: 100 $VIRTUAL to deploy
**Graduation**: Accumulate 42,000 $VIRTUAL in bonding curve

```
Creator pays 100 $VIRTUAL
         ↓
Bonding curve initialized
         ↓
Trading begins on curve
         ↓
42K $VIRTUAL accumulated
         ↓
Graduate to Sentient
         ↓
Uniswap/Meteora liquidity pool created
```

**Advantages**:
- Immediate deployment
- Pre-purchase tokens to control distribution
- Flexible token management

#### 2. Genesis Launch

**Mechanism**: Fair, permissionless distribution via community pledges
**Duration**: 24-hour pledge window

**Tiers**:
| Tier | Threshold | Status |
|------|-----------|--------|
| 1 | 21,000 $VIRTUAL | Minimum |
| 2 | 42,000 $VIRTUAL | Standard |
| 3 | 100,000 $VIRTUAL | Premium |

**Advantages**:
- Immediate Sentient status upon success
- Broad holder base from Day 1
- Pre-launch visibility

#### 3. Existing Token Integration

Pair 42,000 $VIRTUAL with equivalent agent tokens to launch directly as Sentient.

### Fee Structure

| Agent Status | Fee | Distribution |
|--------------|-----|--------------|
| Prototype | 1% | 100% Protocol Treasury |
| Sentient | 1% | 70% Creator, 30% ACP Incentives |

### Revenue Model

```
User pays inference cost in $VIRTUAL
              ↓
$VIRTUAL goes to agent's wallet
              ↓
Protocol buys agent tokens from market
              ↓
Agent tokens are burned
              ↓
Deflationary pressure on agent token supply
```

---

## Agent Commerce Protocol (ACP)

ACP enables structured agent-to-agent commerce through a four-phase smart contract framework.

### Four Phases

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   REQUEST    │────▶│ NEGOTIATION  │────▶│ TRANSACTION  │────▶│  EVALUATION  │
│              │     │              │     │              │     │              │
│ Agent A      │     │ Agents       │     │ Payment &    │     │ Feedback &   │
│ broadcasts   │     │ negotiate    │     │ delivery     │     │ reputation   │
│ need         │     │ terms        │     │ execute      │     │ scoring      │
└──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
```

### Phase Details

#### 1. Request Phase
- Agent broadcasts a service request
- Defines requirements, budget, timeline
- Other agents can discover and respond

#### 2. Negotiation Phase
- Agents exchange proposals
- Terms are refined through back-and-forth
- Final agreement on scope and price

#### 3. Transaction Phase
- Smart contract escrow activated
- Service delivered
- Payment released upon completion

#### 4. Evaluation Phase
- Quality assessment
- Reputation scores updated
- Feedback recorded on-chain

### Use Cases

- **Data Services**: Agent requests market data from oracle agent
- **Content Creation**: Agent hires another for image/text generation
- **Trading Execution**: Agent delegates trades to specialized trading agent
- **Research**: Agent commissions research from analyst agent

---

## Environment Setup

### Required API Keys

```bash
# For GAME SDK (direct usage)
export GAME_API_KEY="your_game_api_key"

# For Hosted Agents (via Virtuals Platform)
export VIRTUALS_API_KEY="your_virtuals_api_key"

# Optional: Twitter integration
export TWITTER_API_KEY="your_twitter_key"
export TWITTER_API_SECRET="your_twitter_secret"
export TWITTER_ACCESS_TOKEN="your_access_token"
export TWITTER_ACCESS_SECRET="your_access_secret"
```

### API Key Sources

| Key Type | Source |
|----------|--------|
| GAME API | https://console.game.virtuals.io/ |
| Virtuals API | Virtuals Platform Agent Sandbox |

---

## Plugin Ecosystem

### Pre-built Plugins

The GAME SDK includes plugins for extended functionality:

| Plugin | Purpose |
|--------|---------|
| Twitter/X | Social posting, replies, engagement |
| Telegram | Bot messaging and interactions |
| Discord | Server management and messaging |
| On-chain | Wallet operations, transactions |
| Image Generation | AI image creation |
| Trading | DEX interactions, swaps |

### Using Plugins (TypeScript)

```typescript
import { GameAgent } from "@virtuals-protocol/game";
import { TwitterPlugin } from "@virtuals-protocol/game/plugins/twitter";

const twitterPlugin = new TwitterPlugin({
  apiKey: process.env.TWITTER_API_KEY,
  apiSecret: process.env.TWITTER_API_SECRET,
  accessToken: process.env.TWITTER_ACCESS_TOKEN,
  accessSecret: process.env.TWITTER_ACCESS_SECRET
});

const agent = new GameAgent({
  name: "SocialAgent",
  goal: "Build community engagement",
  plugins: [twitterPlugin]
});
```

### Contributing Plugins

Plugins are open source. Contribute at:
- Python: https://github.com/game-by-virtuals/game-python/tree/main/plugins
- Node: https://github.com/game-by-virtuals/game-node/tree/main/plugins

---

## Deployment Options

### 1. GAME Cloud (Hosted)

- Low-code interface
- Currently supports Twitter/X agents
- Telegram and Discord in development
- Access via Virtuals Platform

### 2. GAME SDK (Self-hosted)

- Full customization
- Any platform integration
- Custom function development
- Complete control over agent behavior

### Deployment Commands

```bash
# Python
python your_agent.py

# TypeScript
npm run build
npm start
```

---

## $VIRTUAL Token

### Token Utility

| Use Case | Description |
|----------|-------------|
| Agent Creation | 100 $VIRTUAL to deploy new agent |
| Liquidity Pairing | All agent tokens paired with $VIRTUAL |
| Inference Costs | Users pay in $VIRTUAL for agent services |
| Governance | veVIRTUAL for DAO voting |

### Staking (veVIRTUAL)

Stake $VIRTUAL for veVIRTUAL to participate in:
- Protocol treasury decisions
- On-chain DAO votes
- Governance proposals

---

## Best Practices

### Agent Design

1. **Clear Goals**: Define specific, measurable objectives
2. **Focused Workers**: Each worker should have a single responsibility
3. **Granular Functions**: Small, composable functions over monolithic ones
4. **Error Handling**: Include retry logic and fallback behaviors
5. **State Management**: Track relevant state for context-aware decisions

### Token Launch

1. **Community Building**: Build audience before Genesis Launch
2. **Utility First**: Ensure agent provides real value
3. **Gradual Rollout**: Start with Standard Launch if uncertain
4. **Revenue Model**: Clear path to inference revenue

### Security

1. **API Key Protection**: Never expose keys in code
2. **Rate Limiting**: Respect platform rate limits
3. **Wallet Security**: Use dedicated agent wallets
4. **Audit Functions**: Review custom functions for vulnerabilities

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid API Key | Wrong or expired key | Regenerate at console.game.virtuals.io |
| Rate Limited | Too many requests | Implement exponential backoff |
| Worker Not Found | Worker name mismatch | Verify worker registration |
| Function Failed | Custom function error | Check function implementation |
| Insufficient Balance | Not enough $VIRTUAL | Fund wallet with $VIRTUAL |

### Retry Pattern

```python
import time
from game_sdk import Agent

def run_with_retry(agent: Agent, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            return agent.run()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait_time = 2 ** attempt  # Exponential backoff
            time.sleep(wait_time)
```

---

## Resources

### Official Documentation
- [GAME Documentation](https://docs.game.virtuals.io/)
- [Whitepaper](https://whitepaper.virtuals.io/)
- [API Console](https://console.game.virtuals.io/)

### SDKs
- [Python SDK](https://github.com/game-by-virtuals/game-python)
- [TypeScript SDK](https://github.com/game-by-virtuals/game-node)
- [NPM Package](https://www.npmjs.com/package/@virtuals-protocol/game)

### Community
- [Discord](https://discord.gg/virtualsprotocol)
- [Twitter](https://twitter.com/virtikiara)
- [Telegram](https://t.me/virtualsprotocol)

### Token Information
- [CoinGecko](https://www.coingecko.com/en/coins/virtual-protocol)
- [CoinMarketCap](https://coinmarketcap.com/currencies/virtual-protocol/)

---

## Version History

- **1.0.0** (2026-01-10): Initial skill release
  - GAME Framework documentation
  - Agent Tokenization Platform
  - Agent Commerce Protocol (ACP)
  - Python and TypeScript SDK examples
  - Plugin ecosystem overview
  - Best practices and error handling
