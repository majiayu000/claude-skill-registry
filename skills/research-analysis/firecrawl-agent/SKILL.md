---
name: firecrawl-agent
description: Perform autonomous deep web research using Firecrawl's agent. Searches, navigates, and extracts data from websites without needing URLs. Use when users need web research, company information, competitive analysis, or structured data extraction from the web.
license: MIT
compatibility: Requires Python 3.9+, firecrawl-py package, and FIRECRAWL_API_KEY environment variable
metadata:
  author: ethanolivertroy
  version: "1.0.0"
allowed-tools: Bash(python:*) Read
---

# Firecrawl Agent Skill

This skill enables autonomous deep web research using Firecrawl's `/agent` endpoint. The agent can search, navigate, and extract structured data from websites without requiring URLs upfront.

## When to Use This Skill

Use this skill when you need to:
- **Research companies** - Find founders, funding, employee counts, tech stacks
- **Gather competitive intelligence** - Compare products, pricing, features
- **Extract structured data** - Get specific information in a defined schema
- **Answer questions requiring web research** - When information isn't in your knowledge base

## Quick Start

Run a simple research query:

```bash
cd firecrawl-agent/scripts
python firecrawl_agent.py "Find the founders and founding year of Anthropic"
```

## Prerequisites

1. **Install dependencies**:
   ```bash
   pip install -r scripts/requirements.txt
   ```

2. **Set API key**:
   ```bash
   export FIRECRAWL_API_KEY=your_api_key_here
   ```
   Get your API key at: https://www.firecrawl.dev/

## Usage

### Basic Research (No Schema)

```bash
python scripts/firecrawl_agent.py "What are the main features of Notion?"
```

### Research with Structured Output

For predictable, structured responses, provide a JSON schema:

```bash
python scripts/firecrawl_agent.py \
  "Find information about Stripe" \
  --schema '{"company_name": "string", "founded_year": "number", "founders": ["string"], "headquarters": "string"}'
```

### Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `prompt` | Your research query (required) | - |
| `--schema` | JSON schema for structured output | None |
| `--model` | Model to use: `spark-1-mini` or `spark-1-pro` | `spark-1-mini` |
| `--urls` | Comma-separated starting URLs | None |
| `--max-credits` | Maximum credits to spend | 50 |

### Model Selection

- **`spark-1-mini`** (default): Faster, cheaper, good for straightforward queries
- **`spark-1-pro`**: More capable, better for complex research requiring deeper navigation

```bash
# Use pro model for complex research
python scripts/firecrawl_agent.py \
  "Compare the pricing tiers of Notion, Coda, and Obsidian" \
  --model spark-1-pro
```

### Providing Starting URLs

If you know relevant URLs, provide them to focus the search:

```bash
python scripts/firecrawl_agent.py \
  "Extract the pricing information" \
  --urls "https://stripe.com/pricing,https://stripe.com/enterprise"
```

## Common Use Cases

### Company Research

```bash
python scripts/firecrawl_agent.py \
  "Research Anthropic: founders, funding rounds, key products, and employee count" \
  --schema '{"name": "string", "founders": ["string"], "funding_total": "string", "products": ["string"], "employee_count": "string"}'
```

### Product Comparison

```bash
python scripts/firecrawl_agent.py \
  "Compare Vercel and Netlify deployment platforms" \
  --model spark-1-pro
```

### Contact Information

```bash
python scripts/firecrawl_agent.py \
  "Find contact information for Acme Corp" \
  --schema '{"email": "string", "phone": "string", "address": "string", "social_links": ["string"]}'
```

## Output Format

The script outputs JSON with the following structure:

```json
{
  "success": true,
  "status": "completed",
  "data": {
    // Your extracted data here
  },
  "sources": [
    "https://example.com/page1",
    "https://example.com/page2"
  ],
  "credits_used": 12
}
```

## Error Handling

Common errors and solutions:

| Error | Cause | Solution |
|-------|-------|----------|
| `FIRECRAWL_API_KEY not set` | Missing API key | Export the environment variable |
| `Rate limit exceeded` | Too many requests | Wait and retry, or upgrade plan |
| `Credit limit reached` | `maxCredits` exceeded | Increase `--max-credits` or simplify query |
| `Invalid schema` | Malformed JSON schema | Validate your JSON syntax |

## Cost Management

- The agent uses credits based on complexity and pages visited
- **Free tier**: 5 runs per day
- Set `--max-credits` to cap spending:
  ```bash
  python scripts/firecrawl_agent.py "Research topic" --max-credits 25
  ```

## Reference Documentation

- See `references/REFERENCE.md` for complete API parameter documentation
- See `references/SCHEMAS.md` for common schema patterns
- See `assets/example_schemas/` for ready-to-use Pydantic models

## Notes

- Firecrawl agent is in "research preview" - pricing is dynamic
- Results are available for 24 hours after completion
- Complex queries may take 30-60 seconds to complete
