---
name: parallel-deep-research
description: "Deep multi-source research via Parallel API. Use when user explicitly asks for thorough research, comprehensive analysis, or investigation of a topic. For quick lookups or news, use parallel-search instead."
homepage: https://parallel.ai
---

# Parallel Deep Research

Deep, multi-source research for complex topics requiring synthesis from many sources. Returns comprehensive reports with citations.

## When to Use

Trigger this skill when the user asks for:
- "deep research on...", "thorough investigation of...", "comprehensive report about..."
- "research everything about...", "full analysis of..."
- Complex topics requiring synthesis from 10+ sources
- Competitive analysis, market research, due diligence
- Questions where depth and accuracy matter more than speed

**NOT for:**
- Quick lookups or simple questions (use parallel-search)
- Current news or recent events (use parallel-search with `--after-date`)
- Reading specific URLs (use parallel-extract)

## Quick Start

```bash
parallel-cli research run "your research question" --processor pro-fast --json -o ./report
```

## CLI Reference

### Basic Usage

```bash
parallel-cli research run "<question>" [options]
```

### Common Flags

| Flag | Description |
|------|-------------|
| `-p, --processor <tier>` | Processor tier (see table below) |
| `--json` | Output as JSON |
| `-o, --output <path>` | Save results to file (creates .json and .md) |
| `-f, --input-file <path>` | Read query from file (for long questions) |
| `--timeout N` | Max wait time in seconds (default: 3600) |
| `--no-wait` | Return immediately, poll later with `research status` |

### Processor Tiers

| Processor | Time | Use Case |
|-----------|------|----------|
| `lite-fast` | 10-20s | Quick lookups |
| `base-fast` | 15-50s | Simple questions |
| `core-fast` | 15s-100s | Moderate research |
| `pro-fast` | 30s-5min | Exploratory research (default) |
| `ultra-fast` | 1-10min | Multi-source deep research |
| `ultra2x-fast` | 1-20min | Difficult deep research |
| `ultra4x-fast` | 1-40min | Very difficult research |
| `ultra8x-fast` | 1min-1hr | Most challenging research |

Non-fast variants (e.g., `pro`, `ultra`) take longer but use fresher data.

### Examples

**Basic research:**
```bash
parallel-cli research run "What are the latest developments in quantum computing?" \
  --processor pro-fast \
  --json -o ./quantum-report
```

**Deep competitive analysis:**
```bash
parallel-cli research run "Compare Stripe, Square, and Adyen payment platforms: features, pricing, market position, and developer experience" \
  --processor ultra-fast \
  --json -o ./payments-analysis
```

**Long research question from file:**
```bash
# Create question file
cat > /tmp/research-question.txt << 'EOF'
Investigate the current state of AI regulation globally:
1. What regulations exist in the US, EU, and China?
2. What's pending or proposed?
3. How do companies like OpenAI, Google, and Anthropic respond?
4. What industry groups are lobbying for/against regulation?
EOF

parallel-cli research run -f /tmp/research-question.txt \
  --processor ultra-fast \
  --json -o ./ai-regulation-report
```

**Non-blocking research:**
```bash
# Start research without waiting
parallel-cli research run "research question" --no-wait

# Check status later
parallel-cli research status <task-id>

# Poll until complete
parallel-cli research poll <task-id> --json -o ./report
```

## Best-Practice Prompting

### Research Question
Write 2-5 sentences describing:
- The specific question or topic
- Scope boundaries (time period, geography, industries)
- What aspects matter most (pricing? features? market share?)
- Desired output format (comparison table, timeline, pros/cons)

**Good:**
```
Compare the top 5 CRM platforms for B2B SaaS companies with 50-200 employees.
Focus on: pricing per seat, integration ecosystem, reporting capabilities.
Include recent 2024-2026 changes and customer reviews from G2/Capterra.
```

**Poor:**
```
Tell me about CRMs
```

## Response Format

Returns structured JSON with:
- `task_id` — unique identifier for polling
- `status` — `pending`, `running`, `completed`, `failed`
- `result` — when complete:
  - `summary` — executive summary
  - `findings[]` — detailed findings with sources
  - `sources[]` — all referenced URLs with titles

## Output Handling

When presenting research results:
- Lead with the **executive summary** verbatim
- Present **key findings** without paraphrasing
- Include **source URLs** for all facts
- Note any **conflicting information** between sources
- Preserve all facts, names, numbers, dates, quotes

## Running Out of Context?

For long conversations, save results and use `sessions_spawn`:

```bash
parallel-cli research run "<question>" --json -o /tmp/research-<topic>
```

Then spawn a sub-agent:
```json
{
  "tool": "sessions_spawn",
  "task": "Read /tmp/research-<topic>.json and present the executive summary and key findings with sources.",
  "label": "research-summary"
}
```

## Error Handling

| Exit Code | Meaning |
|-----------|---------|
| 0 | Success |
| 1 | Unexpected error (network, parse) |
| 2 | Invalid arguments |
| 3 | API error (non-2xx) |

## Prerequisites

1. Get an API key at [parallel.ai](https://parallel.ai)
2. Install the CLI:

```bash
curl -fsSL https://parallel.ai/install.sh | bash
export PARALLEL_API_KEY=your-key
```

## References

- [API Docs](https://docs.parallel.ai)
- [Research API Reference](https://docs.parallel.ai/api-reference/research)
