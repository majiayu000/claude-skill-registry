---
name: docs-seeker
description: "Fetch up-to-date documentation for any library, framework, API, or service into context. Use when the user wants to look up API references, check function signatures or required fields, find feature-specific docs, or verify how an external tool actually works. Triggers for queries about third-party libraries like Stripe, SQLAlchemy, Tailwind, FastAPI, shadcn, Drizzle, Hono, Better Auth — any time the answer lives in official docs rather than in the project codebase. Use this instead of guessing from trained knowledge, which is stale."
---

## Why fetch instead of recall

Trained knowledge rots. Library APIs rename fields, deprecate hooks, restructure auth flows, and change defaults between minor versions. Answering from memory is how you get confidently wrong code. Replace memory with retrieval — cheaply, from sources designed for AI consumption.

## The source hierarchy (and why)

Prefer sources in this order. The ranking is about *signal per token*, not just availability.

1. **`llms.txt` on the official docs site** — hand-curated by the project, AI-optimized, token-dense, always current. This is the ideal source when it exists. Try `{official-docs-url}/llms.txt` first for any library with a docs site; many projects ship one even if they don't advertise it. If `llms.txt` is just an index of links, follow the most relevant ones. `llms-full.txt` exists on some sites and contains the full corpus — only reach for it when the user explicitly wants comprehensive docs, since it's large.

2. **Context7** — a mirror that ingests GitHub repos and exposes them at `https://context7.com/{org}/{repo}/llms.txt`, with optional `?topic={keyword}` filtering. Use this when the project has no official `llms.txt`, or when you want to scope to one feature. The `{org}/{repo}` path mirrors GitHub exactly — derive it from the user's `package.json`, imports, lockfile, or the project's GitHub URL rather than guessing. For docs sites without a clear repo, Context7 also hosts `https://context7.com/websites/{normalized-path}/llms.txt`.

3. **GitMCP** — any GitHub repo is accessible by swapping `github.com` → `gitmcp.io` in the URL. Useful when Context7 doesn't have the repo indexed, or when you need source-of-truth README/examples straight from the repo.

4. **WebSearch** — last resort. Slower, noisier, and you'll spend tokens filtering results. Only fall here when the three structured sources all miss. When you do search, query for `"{library} llms.txt"` first — it often surfaces an official or community-maintained one.

On any 404, timeout, or empty response: move to the next tier immediately. Never retry a failed source.

## Topic scoping

When the user's query targets a specific feature (e.g., "shadcn date picker", "Next.js middleware", "Stripe webhooks"), append `?topic={keyword}` to the Context7 URL to narrow the fetch. Pick a short root keyword that captures the feature — judgment call, no rigid rules. The goal is fewer tokens, higher relevance. If the topic URL returns nothing useful, drop the topic and try the general URL.

## Reading the docs you find

Once you have URLs, the question is how to read them without polluting the main context.

- **A handful of small pages, or content the orchestrator clearly needs verbatim**: read directly with `WebFetch`. Fast, simple, no overhead.
- **Many pages, or large pages where you only need specific answers**: fan out to parallel subagents, each reading a subset and returning a condensed summary. This protects the main context window from doc bloat and parallelizes I/O. Use judgment on fan-out count — a couple for moderate sets, more for large ones. The tradeoff is latency/tokens vs. main-context pollution; lean toward subagents whenever the raw docs would be noisy relative to what the orchestrator actually needs.

When delegating to subagents, tell them exactly what question to answer and what to return (e.g., "return the exact signature and required fields for `stripe.webhooks.constructEvent`, plus any version notes") — not "summarize these docs". Specific asks give specific answers.

## Version awareness

Before fetching, check what version the project actually uses — `package.json`, `requirements.txt`, `go.mod`, lockfiles. Fetching the latest docs when the project is pinned two majors behind is a common way to hand back wrong answers. If a version-specific doc path exists (e.g., `/v2/llms.txt`, `/docs/4.x/`), prefer it.

## Gotchas

- **Don't fabricate.** If every source misses, say so clearly and ask the user for a URL or a different approach. A made-up API signature is worse than "I couldn't find it."
- **Don't over-fetch.** The orchestrator asked a question; pull what answers it, not the entire manual. Every token you add competes for attention downstream.
- **Don't trust your own cache.** If you recall that a library's docs live at a certain URL, verify — sites reorganize. A fresh fetch beats a confident memory.
- **Report what you used.** When you hand results back, note which source succeeded (llms.txt / Context7 / GitMCP / WebSearch) and the URLs fetched. This lets the orchestrator judge freshness and lets the user follow up.

## Constraints

- Use `WebFetch` to read URLs. Do not invoke MCP servers for this.
- Prefer `llms.txt` over `llms-full.txt` unless comprehensive docs are explicitly requested.
- Never retry a failed source — move down the tier list.
