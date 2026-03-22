---
name: moa
description: "Mixture of Agents: Make 3 frontier models argue, then synthesize their best insights into one superior answer. ~$0.03/query."
author: John Scianna (@Scianna)
version: 1.2.0
requires:
  - OPENROUTER_API_KEY
cost: ~$0.03 per query (paid tier)
---

# Mixture of Agents (MoA)

**TL;DR:** Make 3 AI models argue with each other. Get an answer better than any single model. Cost: ~$0.03.

## Two Usage Modes

### A. Standalone CLI (Node.js)
```bash
export OPENROUTER_API_KEY="your-key"
node scripts/moa.js "Your complex question"
```

### B. OpenClaw Skill (Agent-orchestrated)
```bash
# Install
clawhub install moa

# Or copy to ~/clawd/skills/moa/
```

The agent can then invoke MoA for complex analysis tasks.

---

## Origin Story

The concept of "Mixture of Agents" comes from research showing LLMs can improve each other's outputs through collaboration. I built this for VC deal analysis—when evaluating startups, you want multiple perspectives, not one model's opinion.

**The journey:**
1. Started with 5 free OpenRouter models (Llama, Gemini, Mistral, Qwen, Nemotron)
2. Rate limits killed me at 2am during peak hours
3. Switched to 3 paid frontier specialists
4. Result: ~$0.03/query, answers better than any single model

---

## When to Use

- **Complex analysis** — due diligence, market research, technical evaluation
- **Brainstorming** — get diverse ideas, synthesize the best
- **Fact-checking** — cross-reference across models with different training data
- **High-stakes decisions** — when one model's blind spots could hurt you
- **Contrarian thinking** — different models have different biases

**When NOT to use:**
- Quick Q&A (too slow, 30-90s latency)
- Real-time chat (not designed for streaming)
- Simple lookups (overkill)

---

## Model Configuration

### Paid Tier (Default) — Recommended

| Role | Model | ~Latency | Strength |
|------|-------|----------|----------|
| Proposer 1 | `moonshotai/kimi-k2.5` | 23s | Long context, strong reasoning |
| Proposer 2 | `z-ai/glm-5` | 36s | Technical depth, different training corpus |
| Proposer 3 | `minimax/minimax-m2.5` | 64s | Nuance catching, thorough analysis |
| Aggregator | `moonshotai/kimi-k2.5` | 15s | Fast synthesis |

**Why these models?**
- Frontier-class but less congested than GPT-4/Claude
- Different training data = genuinely different perspectives
- Chinese models excel at certain reasoning tasks
- Combined cost still cheaper than single Opus call

**Cost breakdown:**
```
3 proposers × ~$0.008 = $0.024
1 aggregator × ~$0.005 = $0.005
─────────────────────────────
Total: ~$0.029/query
```

### Free Tier (Fallback)
5 models: Llama 3.3 70B, Gemini 2.0 Flash, Mistral Small, Nemotron 70B, Qwen 2.5 72B

⚠️ **Warning:** Free tier hits rate limits during peak hours. Use `--free` flag only for testing.

---

## How It Works

```
        ┌─────────────┐
        │   PROMPT    │
        └──────┬──────┘
               │
    ┌──────────┼──────────┐
    ▼          ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐
│Kimi 2.5│ │ GLM 5  │ │MiniMax │  ← Parallel (they "argue")
│(reason)│ │(depth) │ │(nuance)│
└───┬────┘ └───┬────┘ └───┬────┘
    │          │          │
    └──────────┼──────────┘
               ▼
       ┌──────────────┐
       │  AGGREGATOR  │
       │  (Kimi 2.5)  │
       │              │
       │ • Best of 3  │
       │ • Resolve    │
       │   conflicts  │
       │ • Synthesize │
       └──────┬───────┘
              ▼
       ┌──────────────┐
       │ FINAL ANSWER │
       │ (Synthesized)│
       └──────────────┘
```

---

## API Reference

### Function Signature

```typescript
interface MoAOptions {
  prompt: string;           // Required: The question to analyze
  tier?: 'paid' | 'free';   // Default: 'paid'
}

interface MoAResult {
  synthesis: string;        // The final aggregated answer
}

// Throws on complete failure (all models down, invalid key)
// Returns partial synthesis if 1-2 models fail
async function handle(options: MoAOptions): Promise<string>
```

### CLI Usage

```bash
# Paid tier (default)
node scripts/moa.js "Your complex question"

# Free tier
node scripts/moa.js "Your question" --free
```

### Programmatic Usage

```javascript
const { handle } = require('./scripts/moa.js');

const synthesis = await handle({ 
  prompt: "Analyze the competitive moats in AI code generation",
  tier: 'paid'
});

console.log(synthesis);
```

---

## Failure Modes

| Scenario | Behavior |
|----------|----------|
| **1 proposer fails** | Synthesis from remaining 2 models |
| **2 proposers fail** | Synthesis from 1 model (degraded) |
| **All proposers fail** | Returns error message |
| **Invalid API key** | Immediate error with setup instructions |
| **Rate limit (free tier)** | Returns rate limit error |

The system is designed to degrade gracefully. A 2/3 response is still valuable.

---

## Example Use Cases

### VC Due Diligence
```bash
node scripts/moa.js "Analyze the competitive landscape for AI code generation. \
Who has defensible moats? Who's likely to be commoditized? Be specific."
```

### Technical Evaluation
```bash
node scripts/moa.js "Compare RLHF vs DPO vs RLAIF for LLM alignment. \
Which scales better? What are the failure modes of each?"
```

### Market Research
```bash
node scripts/moa.js "What are the emerging use cases for embodied AI in 2026? \
Focus on robotics, drones, and autonomous systems. Include specific companies."
```

---

## Performance Expectations

| Metric | Paid Tier | Free Tier |
|--------|-----------|-----------|
| **P50 Latency** | ~45s | ~60s |
| **P95 Latency** | ~90s | ~120s+ |
| **Success Rate** | >99% | ~80% (rate limits) |
| **Cost/Query** | ~$0.03 | $0.00 |

---

## Tips

1. **Be specific** — Vague prompts get vague synthesis
2. **Ask for structure** — "Give me pros/cons" or "List top 5" helps the aggregator
3. **Use for analysis, not chat** — MoA shines for complex reasoning
4. **Batch your queries** — 30-90s per query, so plan accordingly

---

## Installation

### Via ClawHub (Recommended)
```bash
clawhub install moa
```

### Manual
1. Copy `skills/moa/` to your `~/clawd/skills/` directory
2. Set `OPENROUTER_API_KEY` in your environment
3. The agent can now invoke MoA for complex queries

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | Yes | Your OpenRouter API key |

Get your key at: https://openrouter.ai/keys

---

## Credits

- MoA concept: [Together AI Research](https://www.together.ai/blog/together-moa)
- Implementation: [@Scianna](https://x.com/Scianna)
- Built for: [OpenClaw](https://github.com/openclaw/openclaw)
