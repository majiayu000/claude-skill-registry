---
name: build-with-exa
version: 0.1.0
description: >
  Build applications and agents with Exa's API Platform: search, contents,
  answer, context, Agent API, monitors, websets, OpenAI-compatible endpoints,
  and exa-py / exa-js. Use when choosing Exa endpoints, writing Exa API calls,
  integrating semantic web search or research into products, or debugging Exa
  request shapes. Load references/ on demand for endpoint details.
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Skill
author: Exa Labs (ported by mktg)
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: 🧩
---

## On Activation

1. Confirm `EXA_API_KEY` is available for any live API call. SDK examples assume the key is set.
2. Default new integrations to `POST /search` with `type: "auto"` and `contents.highlights: true`. Escalate to Agent API only for multi-step research / list-building.
3. Load only the `references/*.md` file needed for the current endpoint - do not dump the whole tree into context.
4. For agent-native marketing research inside mktg projects, prefer `exa-search`, `company-research`, or `lead-generation` over inventing a custom integration.

# Build with Exa

## Scope

Included by default:

- Core retrieval APIs: search endpoint, contents endpoint, answer endpoint, context endpoint
- Long-running research workflows: Agent API (`/agent`)
- Async and recurring workflows: Monitors API, Websets API
- SDK guidance: Python `exa-py`, TypeScript `exa-js`

> Note on data retention: `/search`, `/answer`, and deep research are Zero Data Retention (ZDR). The Agent API (`/agent`), Websets, and Monitors are not ZDR. If a use case requires ZDR, stay on the ZDR surfaces or contact Exa.

## Installation

```bash
# Python
pip install exa-py

# TypeScript / JavaScript
npm install exa-js
```

## Authentication

```bash
export EXA_API_KEY="your_api_key_here"
```

Exa accepts either the `x-api-key` header or `Authorization: Bearer <key>`.

## API Decision Workflow

Before picking an endpoint, decide which workflow shape fits:

- Raw web content for your own LLM or agent: start with `/search` using `type: "auto"` and `contents: { highlights: true }`
- Synthesized structured output: start with `/search` using the search type that fits your latency and reasoning needs, then add `outputSchema` and `systemPrompt`
- Long-running multi-step research, list-building, or enrichment with structured output: use the Agent API (`/agent`)

**Default to the search endpoint.** Use the search endpoint (`/search`) for most new integrations, then move to a more specialized Exa surface only when the task shape clearly calls for it.

1. Need general semantic web retrieval, synthesized output, filters, or content extraction from search results: use the search endpoint (`/search`)
2. Already know the URLs and need clean page extraction or freshness controls: use the contents endpoint (`/contents`)
3. Need pages related to a known seed URL: use the search endpoint (`/search`) with a query derived from the page (for example title, topic, or text from `/contents`)
4. Need a grounded answer with citations from Exa-managed search: use the answer endpoint (`/answer`)
5. Need code-focused retrieval from repos, docs, and Stack Overflow: use the context endpoint (`/context`)
6. Need OpenAI SDK drop-in compatibility for chat or responses clients: use the OpenAI-compatible endpoints (`/chat/completions`, `/responses`)
7. Need asynchronous multi-step research, list-building, enrichment, or follow-up questions over prior research: use the Agent API (`/agent`)
8. Need scheduled recurring search with webhook delivery: use the Monitors API (`/monitors`)
9. Need async verified and enriched entity collection workflows: use the Websets API (`/websets/v0`)

## Quick Start

For more complete examples, see the relevant reference file in the table below.

**Python** (`/search`):

```python
from exa_py import Exa

exa = Exa(api_key="YOUR_EXA_API_KEY")
result = exa.search(
    "latest developments in LLMs",
    type="auto",
    contents={"highlights": True}
)

for item in result.results:
    print(item.title, item.url)
```

**TypeScript** (`/search`):

```typescript
import Exa from "exa-js";

const exa = new Exa();
const result = await exa.search("latest developments in LLMs", {
  type: "auto",
  contents: { highlights: true }
});

for (const item of result.results) {
  console.log(item.title, item.url);
}
```

**Raw HTTP** (`/search`):

```bash
curl -X POST "https://api.exa.ai/search" \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{
    "query": "latest developments in LLMs",
    "type": "auto",
    "contents": {
      "highlights": true
    }
  }'
```

## Anti-Patterns
- On the search endpoint, `text`, `highlights`, and `summary` belong inside `contents`, not at the top level.
- On the contents endpoint, `text`, `highlights`, and `summary` are top-level fields, not nested inside `contents`.
- Pick one of `highlights`, `text`, or `summary` by default. Do not stack them unless the use case truly needs multiple views of the same page.
- `numSentences` and `highlightsPerUrl` are deprecated highlight knobs. Prefer `highlights: true`, or set `maxCharacters` only when you have a fixed budget.
- Prefer `maxAgeHours` for freshness guidance. Older `livecrawl` examples still exist, but `maxAgeHours` is the normative control for new integrations.
- Stick to the documented `category` set and do not invent categories like `github`, `documentation`, `qa`, or `pdf`. Specialized categories such as `people` and `company` also restrict which filters are valid; check the search reference before combining categories with domain or date filters.
- OpenAI-compatible endpoints are for compatibility-first use cases. Prefer native Exa endpoints for new integrations when you want clearer request semantics.
- Do not treat `/agent` as a drop-in replacement for `/search`. It is higher-latency and async, so use the dedicated Agent reference when that workflow shape is the real fit. Consider using it over websets or deep where appropriate. 
- Treat `/research/v1` as legacy. Do not present it as the default for new work.
- Treat `/findSimilar` as deprecated. Prefer `/search` (optionally after `/contents` on the seed URL) for related-page discovery.

## Reference Files

| File | Topics |
|------|--------|
| [references/search.md](references/search.md) | Search endpoint request/response shape, search types, filters, nested contents, structured output |
| [references/contents.md](references/contents.md) | Contents endpoint extraction, freshness, statuses, top-level content fields |
| [references/answer.md](references/answer.md) | Grounded answer generation with citations and structured output |
| [references/context.md](references/context.md) | Code-focused retrieval with `tokensNum` |
| [references/agent.md](references/agent.md) | Agent API for async multi-step research, enrichment, structured output, polling, and events |
| [references/openai-compat.md](references/openai-compat.md) | OpenAI-compatible endpoints, model routing, `extra_body` usage |
| [references/monitors.md](references/monitors.md) | Standalone Monitors API for scheduled recurring search |
| [references/websets.md](references/websets.md) | Websets API for async verified and enriched collection building |
| [references/sdks.md](references/sdks.md) | Python and TypeScript SDK naming, methods, and shape differences |
| [references/http-requests.md](references/http-requests.md) | Minimal raw HTTP examples across major Exa surfaces |
| [references/models-and-modes.md](references/models-and-modes.md) | Search type selection, answer/research model routing, latency tradeoffs |
| [references/prompting-and-patterns.md](references/prompting-and-patterns.md) | Durable query, prompting, freshness, and output-schema patterns |
| [references/common-mistakes.md](references/common-mistakes.md) | Parameter-shape corrections |

## Canonical Docs

- Docs home: `https://exa.ai/docs`
- Documentation index: `https://exa.ai/docs/llms.txt`
- Search reference: `https://exa.ai/docs/reference/search`
- Agent API guide: `https://exa.ai/docs/reference/agent-api-guide`
- Exa Connect overview: `https://exa.ai/docs/reference/agent-api/connect/overview`
- Python SDK spec: `https://exa.ai/docs/sdks/python-sdk-specification`
- TypeScript SDK spec: `https://exa.ai/docs/sdks/typescript-sdk-specification`

## Attribution

Ported from [exa-labs/agent-skills](https://github.com/exa-labs/agent-skills) - adapted for mktg's drop-in contract on 2026-07-18.

Upstream commit: 390ffee2d7e1d0dce2ed8efe4994c2b3c1c0173b

Drift detection: if the upstream skill changes, re-run `mktg-steal https://github.com/exa-labs/agent-skills` to evaluate the diff.
