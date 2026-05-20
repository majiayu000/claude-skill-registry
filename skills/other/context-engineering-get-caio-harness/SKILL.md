---
name: context-engineering
description: "Manages context window for cost, performance, and quality in Claude API workflows and agent sessions. Use when building multi-step agent pipelines, designing system prompts for repeated API calls, managing long coding sessions, or debugging degraded agent performance. Covers KV cache optimization, token budgeting, subagent delegation, compaction, attention mechanics, and the 200K pricing cliff."
version: 2.0.0
---

# Context Engineering

## Purpose

Every token sent to an LLM costs money, increases latency, and past ~32K tokens degrades model performance. Context engineering is the discipline of delivering the smallest possible set of high-signal tokens that achieves the desired outcome — across both individual sessions and production API pipelines.

The difference between a $0.50 query and a $5.00 query is context management, not prompt engineering.

## When to Use

- **Agent pipeline design**: Before building any multi-step Claude API workflow
- **System prompt architecture**: When structuring prompts for repeated calls
- **Long coding sessions**: Context approaching limits (70%+ utilization)
- **Degraded performance**: Agent losing track mid-session
- **Cost review**: When agent costs exceed expectations
- **Scale prep**: Before moving from prototype to production volume

## Core Concept

Context is **everything** available to the model at inference time: system prompts, tool definitions, retrieved documents, message history, and tool outputs (often 80%+ of total tokens).

The context window is not just a size limit — it's an **attention budget** that depletes as context grows. Models exhibit the "lost-in-the-middle" phenomenon: information at the beginning and end gets strong attention, the middle gets lost.

### The Triple Penalty

Every unnecessary token hits you three ways:

1. **Cost** — Opus 4.6: $15/M input, $75/M output. Cached input: $1.875/M (8x cheaper)
2. **Latency** — More tokens = slower responses
3. **Quality** — Past 32K tokens, sharp performance degradation (context rot)

Output tokens cost 5x input tokens. This is the single most important cost fact.

---

## Part 1: Prompt Architecture

### Stable Prefixes for KV Cache Hits

**The most important optimization for production agents.**

LLMs process prompts token by token. If your prompt starts identically to a previous request, the model reuses cached key-value computations for that prefix. Cached tokens cost 8-10x less than uncached.

#### Prompt Layering (Always Follow This Order)

```
┌─────────────────────────────────────────┐
│  LAYER 1: STATIC (cached across ALL calls)    │
│  - System instructions                         │
│  - Tool definitions (never add/remove dynamically) │
│  - Skills (anti-slop, analysis frameworks)     │
│  - Few-shot examples                           │
├─────────────────────────────────────────┤
│  LAYER 2: SEMI-STATIC (cached per workspace)  │
│  - Workspace context (ICP, competitors)        │
│  - Content pillars, voice calibration          │
│  - Client-specific configuration               │
├─────────────────────────────────────────┤
│  LAYER 3: DYNAMIC (changes per call)           │
│  - The actual content to analyze/process       │
│  - Current user request                        │
│  - Timestamps (date only, never seconds)       │
└─────────────────────────────────────────┘
```

#### Cache Killers (Never Do These)

```
✗ Timestamps with seconds/milliseconds at prompt start
✗ Dynamic content before static content
✗ Randomly ordered tool definitions
✗ Non-deterministic JSON serialization (use sort_keys or consistent key ordering)
✗ Conditionally adding/removing tools between calls
```

#### Implementation

```typescript
// GOOD: Stable prefix, dynamic content last
const messages = [
  {
    role: "system",
    content: [
      { type: "text", text: STATIC_INSTRUCTIONS, cache_control: { type: "ephemeral" } },
      { type: "text", text: workspaceContext, cache_control: { type: "ephemeral" } },
      { type: "text", text: dynamicContent } // No cache control — this changes
    ]
  }
];

// BAD: Timestamp at start kills all caching
const messages = [
  {
    role: "system",
    content: `Current time: ${new Date().toISOString()}\n\n${STATIC_INSTRUCTIONS}`
  }
];
```

Cache TTL is 5 minutes (Anthropic) to 10 minutes (OpenAI). Including date is fine; including seconds guarantees zero cache hits. Route requests by session ID to maximize warm cache hits.

### Attention-Favored Positions

Place critical information where attention is strongest:

| Content | Position | Why |
|---------|----------|-----|
| System instructions | Beginning | Highest attention |
| Current task/goal | Beginning | Sets frame |
| Critical constraints | Beginning or end | Avoid middle dead zone |
| Historical context | Middle | Acceptable loss |
| Supporting documents | Middle | Lower priority |
| Recent conversation | End | Recency bias |
| Current objectives | End | Combats drift |

#### The Todo Pattern

For multi-step agent workflows, maintain a `current_objectives` string appended to the end of context. This "recites" what the agent should be doing, preventing drift across long tool-call chains.

```typescript
const contextSuffix = `
## Current Objectives
- Analyzing newsletter batch (3/8 complete)
- Priority: identify content opportunities for AI pillar
- Next: process remaining 5 items, then compile digest
`;
```

---

## Part 2: Token Reduction

### Progressive Disclosure

Load information only when needed, not upfront. This mirrors human cognition — we don't memorize entire codebases, we use indexes to retrieve relevant information on demand.

**Bad:** Load all skill content at session start
**Good:** Load skill names/descriptions; full content loads on activation

**Bad:** Dump entire file contents into context
**Good:** Load file metadata first, then specific sections as needed

### Store Tool Outputs in Filesystem, Not Context

Cursor's A/B testing showed this reduces total agent tokens by 46.9%.

Agents don't need complete information in the conversation. They need the ability to access information on demand.

```typescript
// BAD: Stuffing tool output into conversation
const result = await searchDatabase(query);
messages.push({ role: "tool", content: JSON.stringify(result) }); // 5,000 tokens

// GOOD: Write to file, pass reference
const result = await searchDatabase(query);
await writeFile(`/tmp/search-${id}.json`, JSON.stringify(result));
messages.push({ role: "tool", content: `Results written to /tmp/search-${id}.json. ${result.length} items found. Use read_file to inspect specific items.` }); // 50 tokens
```

**Apply to:** shell command outputs, search results, API responses, newsletter content, enrichment data. Store full content, pass summary + file path.

### Design Two-Phase Tools

A vague tool returns everything. A precise tool returns exactly what the agent needs.

```typescript
// Phase 1: Lightweight search returns metadata only
async function searchContacts(query: string, filters: ContactFilters) {
  // Returns: [{ id, name, company, title, relevance_score }]
}

// Phase 2: Agent decides which contacts deserve full data
async function getContactDetail(contactId: string) {
  // Returns: Full enrichment, email history, research notes
}
```

| Tool | Phase 1 (cheap) | Phase 2 (on demand) |
|------|-----------------|-------------------|
| Intel search | Titles + snippets + scores | Full article content |
| Contact lookup | Name + company + title | Full enrichment + research |
| Email search | Subject + sender + date | Full email body |
| Company research | Summary + signals | Full analysis report |

Each filter parameter on Phase 1 reduces returned tokens by up to 10x.

### Clean Data Before It Enters Context

Garbage tokens are still tokens. Preprocess aggressively before any LLM call.

```typescript
function cleanForAnalysis(html: string): string {
  return pipeline(html, [
    stripUnsubscribeLinks,
    stripTrackingPixels,
    stripNavigationChrome,
    convertHtmlToMarkdown,  // Markdown uses ~50% fewer tokens than HTML
    collapseWhitespace,
    truncateToMaxWords(3000)
  ]);
}
```

| Content type | Raw tokens | After cleaning | Savings |
|-------------|-----------|----------------|---------|
| HTML email | ~10,000 | ~2,000 | 80% |
| Web page | ~25,000 | ~3,000 | 88% |
| SEC filing | ~50,000 | ~5,000 | 90% |
| API response | ~3,000 | ~500 | 83% |

**Rule: Convert HTML to Markdown before any LLM call. Always.**

### Templates Over Regeneration

Output tokens cost 5x input tokens. Stop regenerating the same patterns from scratch.

```typescript
// BAD: Regenerate from scratch every time ($0.50 per email)
const email = await claude.generate("Write a cold outreach email to {prospect}...");

// GOOD: Load template, fill personalization ($0.05 per email)
const template = await loadTemplate("cold-outreach-v2");
const hooks = await claude.generate(
  `Given this research on ${prospect.name}, generate personalization hooks.
   Return JSON only: { hooks: string[], opener: string, relevance: string }`,
  { max_tokens: 200 }
);
const email = applyTemplate(template, hooks);
```

**CAIO applications:** outreach sequences, intel analysis (structured JSON, not prose), content drafts (pillar framework + unique parts only), client reports.

---

## Part 3: Model & Cost Optimization

### Subagent Delegation Matrix

Not every task needs your most expensive model. The orchestrator should see condensed results, not raw context.

| Task | Model | Why |
|------|-------|-----|
| Data extraction | Haiku | Structured, low-judgment |
| Classification (reply type, intent) | Haiku | Binary/categorical decisions |
| Summarization | Sonnet | Needs comprehension, not creativity |
| Email personalization | Sonnet | Needs quality, not genius |
| ICP scoring | Sonnet | Structured rubric, moderate judgment |
| Newsletter analysis | Sonnet | Comprehension + extraction |
| Content drafting | Opus | Needs voice, judgment, creativity |
| Strategic analysis | Opus | Needs reasoning, synthesis |

#### Context Isolation Pattern

```typescript
// BAD: One agent accumulates everything
for (const newsletter of newsletters) {
  agent.addContext(newsletter.fullText); // Context grows with every item
}

// GOOD: Subagents with isolated context
async function analyzeNewsletter(newsletter: Newsletter) {
  return new Agent({
    model: "sonnet",
    systemPrompt: ANALYSIS_INSTRUCTIONS, // Cached across calls
    context: newsletter.fullText          // Isolated per call
  }).analyze(); // Returns condensed JSON
}

const analyses = await Promise.all(newsletters.map(analyzeNewsletter));
```

Design subagent tasks for single-turn completion. More iterations = more context accumulation.

### Output Token Budgeting

Set task-appropriate `max_tokens`. Don't leave it unlimited.

```typescript
const TASK_LIMITS: Record<string, number> = {
  classification: 50,
  extraction: 200,
  personalization: 300,
  short_answer: 500,
  analysis: 2000,
  content_draft: 3000,
  code_generation: 4000,
};
```

Default to JSON output for agent-to-agent communication. Prose for human-facing content only.

```
// PROSE (expensive): "The company's revenue was 94.5 billion dollars,
// representing a 12.3 percent increase year-over-year..."

// JSON (cheap): {"revenue": 94.5, "unit": "B", "yoy_change": 12.3}
```

### The 200K Pricing Cliff

Crossing 200K input tokens doubles per-token cost. This is a cliff, not a gradient.

| Model | Under 200K | Over 200K |
|-------|-----------|-----------|
| Opus input | $15/M | $30/M |
| Opus output | $75/M | $112.50/M |
| Sonnet input | $3/M | $6/M |
| Sonnet output | $15/M | $22.50/M |

```typescript
class ContextBudget {
  private cumulativeTokens = 0;
  private readonly CLIFF = 180_000; // Buffer before 200K

  async addToolResult(tokenCount: number) {
    this.cumulativeTokens += tokenCount;
    if (this.cumulativeTokens > this.CLIFF) {
      await this.compactContext();
    }
  }
}
```

The cost of a compression step is far less than doubling your per-token rate for the rest of the conversation.

### Parallel Tool Calls

Every sequential tool call re-sends full conversation context. Parallel calls reduce round trips.

```typescript
// BAD: 5 sequential calls = 5x context transmission
const company = await getCompany(id);
const contacts = await getContacts(id);
const deals = await getDeals(id);

// GOOD: Model requests multiple tool calls in single response
// Design tools so independent operations can be batched
```

Fewer round trips = less context accumulation = cheaper and faster.

### Application-Level Response Caching

The cheapest token is the one you never send to the API.

```typescript
class AnalysisCache {
  async getOrAnalyze(contentHash: string, analyzer: () => Promise<Analysis>) {
    const cached = await this.cache.get(contentHash);
    if (cached && !this.isStale(cached)) return cached; // $0.00
    const result = await analyzer();
    await this.cache.set(contentHash, result);
    return result;
  }
}
```

**Good cache candidates:** newsletter analysis, company research (refresh weekly), ICP scores (refresh on config change), template outputs.

**Bad cache candidates:** content drafts (should vary), personalization hooks (context-dependent), reply classification (unique per reply).

---

## Part 4: Session Management

### Context Budget Allocation

For long-running agent sessions, design with explicit budgets:

| Component | Typical % | Notes |
|-----------|-----------|-------|
| System prompt | 5-10% | Stable, loads once |
| Tool definitions | 10-15% | Stable across session |
| Retrieved docs | 20-30% | Dynamic, load on demand |
| Message history | 30-40% | Grows over session |
| Tool outputs | Variable | Can dominate if unchecked |
| Reserved buffer | 10% | Always keep headroom |

### Compaction Triggers

Monitor and act when:

- **70% utilization**: Consider compaction
- **80% utilization**: Actively compress
- **90% utilization**: Critical — summarize aggressively

### Compaction Priority Order

When approaching limits, compress in this priority:

1. **Tool outputs** — Summarize findings/metrics, remove raw data
2. **Old conversation turns** — Distill to decisions and commitments
3. **Retrieved documents** — Extract key facts only
4. **NEVER compress** — System prompts, active task context

### Observation Masking

Tool outputs served their purpose once the decision was made. Replace verbose outputs with compact references:

```
[Obs:ref_123 elided. Key: 15 files found, 3 with errors]
```

**Never mask:** critical observations, recent turns (last 2-3), active reasoning chains.
**Always mask:** repeated outputs, boilerplate headers/footers, already-summarized content.

### Server-Side Compaction

For long-running sessions (50+ tool calls), use Anthropic's server-side compaction:

```typescript
const response = await anthropic.messages.create({
  model: "claude-sonnet-4-5-20250514",
  max_tokens: 4096,
  context_window_strategy: {
    type: "summarize",
    trigger_tokens: 150_000, // Before 200K cliff
    preserve_instructions: "Preserve all numerical data, company names, contact details, and analytical conclusions. Discard raw tool outputs and intermediate reasoning."
  },
  messages: conversationHistory
});
```

Stack with prompt caching: add cache breakpoints on system prompt so it stays cached when compaction occurs.

---

## Part 5: Integration with Harness

The harness implements several context-engineering patterns:

- **Skills system**: Progressive disclosure of capability knowledge
- **Phase-based development**: Limits scope to manageable chunks
- **Ticket system**: Focused task context per work item
- **Build log**: Offloads historical context to filesystem
- **Subagent definitions**: Isolated context per agent type

### Filesystem as Extended Memory

```
progress/
  build-log.md      # Session history
  decisions/        # Key decisions made
  context-cache/    # Temporary context storage
```

Before summarizing away context, write it to a file. Reference the file path instead of keeping content in context.

---

## Cost Estimation Worksheet

Use when speccing new agent features:

```
Feature: [name]
Calls per task: [N]
Model: [opus/sonnet/haiku]

Input tokens per call:
  System prompt (cached):     _____ tokens × $1.875/M = $_____
  Workspace context (cached): _____ tokens × $1.875/M = $_____
  Dynamic content (uncached): _____ tokens × $15/M    = $_____

Output tokens per call:
  Expected output:            _____ tokens × $75/M    = $_____

Per-task cost: $_____ × [N calls] = $_____
Monthly volume: _____ tasks × $_____ = $_____

Optimization targets:
  Cache hit rate:              ____%
  Subagent delegation savings: ____%
  Template savings:            ____%
  Optimized monthly cost:      $_____
```

### CAIO Reference Costs (Optimized)

| Workflow | Calls | Est. Cost/task | Monthly (CAIO) |
|----------|-------|---------------|----------------|
| Newsletter analysis | 1 | $0.02 | $1.60 (80/mo) |
| Content draft | 1 | $0.05 | $2.00 (40/mo) |
| Weekly digest | 1 | $0.10 | $0.40 |
| Prospect research | 3 | $0.08 | $16.00 (200/mo) |
| Email personalization | 1 | $0.03 | $6.00 (200/mo) |
| Reply classification | 1 | $0.01 | $2.00 (200/mo) |

---

## Pre-Build Checklist

Before implementing any agent workflow:

```
□ System prompt uses stable prefix pattern (static → semi-static → dynamic)
□ Tool definitions are static (no conditional add/remove)
□ JSON serialization is deterministic
□ Tool outputs go to filesystem, not conversation context
□ Tools use two-phase pattern (search → retrieve)
□ Each subtask assigned to cheapest capable model
□ Output token limits set per task type
□ Data cleaned before entering context (HTML → Markdown minimum)
□ Application-level caching for repeated queries
□ Context budget tracks cumulative tokens vs 200K cliff
□ Independent tool calls designed for parallel execution
□ Critical information placed at beginning or end, never middle
□ Compaction triggers set at 70/80/90% utilization
□ Cost estimate completed with monthly projections
```

## Guidelines Summary

1. Treat context as finite with diminishing returns
2. Stable prefixes first — this is the #1 cost lever
3. Output tokens cost 5x input — budget accordingly
4. Use progressive disclosure — defer loading until needed
5. Store tool outputs in filesystem, not conversation
6. Delegate to cheapest capable model
7. Monitor utilization and trigger compaction at 70-80%
8. Place critical information at beginning and end, never middle
9. Clean all data (HTML → Markdown) before it enters context
10. The 200K cliff doubles your cost — stay under it
11. Cache at the application level — cheapest token is one you never send
12. Design for graceful degradation, not avoidance

## References

- [Fintool: The Context Tax](https://fintool.com/blog/context-tax) — Production cost optimization patterns
- [Manus: Context Engineering](https://manus.im/blog/context-engineering) — KV cache and stable prefix architecture
- [Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering)
- Anthropic's context window research
- "Lost in the Middle" attention mechanics studies
