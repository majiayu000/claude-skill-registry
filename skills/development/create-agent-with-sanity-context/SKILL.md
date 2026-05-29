---
name: create-agent-with-sanity-context
description: Build AI agents with structured access to Sanity content via Context MCP. Covers Studio setup, agent implementation, and advanced patterns like client-side tools and custom rendering.
---

# Build an Agent with Sanity Context

Give AI agents intelligent access to your Sanity content. Unlike embedding-only approaches, Context MCP is schema-aware—agents can reason over your content structure, query with real field values, follow references, and combine structural filters with semantic search.

**What this enables:**

- Agents understand the relationships between your content types
- Queries use actual schema fields, not just text similarity
- Results respect your content model (categories, tags, references)
- Semantic search is available when needed, layered on structure

Note: Context MCP understands your schema structure but not your domain. You'll provide domain context (what your content is for, how to use it) through the agent's system prompt.

## What You'll Need

Before starting, gather these credentials:

| Credential                | Where to get it                                                                                                                                                        |
| ------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Sanity Project ID**     | Your `sanity.config.ts` or [sanity.io/manage](https://sanity.io/manage)                                                                                                |
| **Dataset name**          | Usually `production` — check your `sanity.config.ts`                                                                                                                   |
| **Sanity API read token** | Create at [sanity.io/manage](https://sanity.io/manage) → Project → API → Tokens. See [HTTP Auth docs](https://www.sanity.io/docs/content-lake/http-auth#k967e449638bc) |
| **LLM API key**           | From your LLM provider (Anthropic, OpenAI, etc.) — any provider works                                                                                                  |

## How Context MCP Works

An MCP server that gives AI agents structured access to Sanity content. The core integration pattern:

1. **MCP Connection**: HTTP transport to the Context MCP URL
2. **Authentication**: Bearer token using Sanity API read token
3. **Tool Discovery**: Get available tools from MCP client, pass to LLM
4. **System Prompt**: Domain-specific instructions that shape agent behavior

**MCP URL formats:**

- `https://api.sanity.io/:apiVersion/agent-context/:projectId/:dataset` — Access all content in the dataset
- `https://api.sanity.io/:apiVersion/agent-context/:projectId/:dataset/:slug` — Access filtered content (requires agent context document with that slug)

The slug-based URL uses the GROQ filter defined in your agent context document to scope what content the agent can access. Use this for production agents that should only see specific content types.

**The integration is simple**: Connect to the MCP URL, get tools, use them. The reference implementation shows one way to do this—adapt to your stack and LLM provider.

## Available MCP Tools

| Tool              | Purpose                                                         |
| ----------------- | --------------------------------------------------------------- |
| `initial_context` | Get compressed schema overview (types, fields, document counts) |
| `groq_query`      | Execute GROQ queries with optional semantic search              |
| `schema_explorer` | Get detailed schema for a specific document type                |

**For development and debugging:** The general Sanity MCP provides broader access to your Sanity project (schema deployment, document management, etc.). Useful during development but not intended for customer-facing applications.

## Before You Start: Understand the User's Situation

A complete integration has **three distinct components** that may live in different places:

| Component                   | What it is                                                      | Examples                                                                        |
| --------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **1. Studio Setup**         | Configure the context plugin and create agent context documents | Sanity Studio (separate repo or embedded)                                       |
| **2. Agent Implementation** | Code that connects to Context MCP and handles LLM interactions  | Next.js API route, Express server, Python service, or any MCP-compatible client |
| **3. Frontend (Optional)**  | UI for users to interact with the agent                         | Chat widget, search interface, CLI—or none for backend services                 |

**Studio setup and agent implementation are required.** Frontend is optional—many agents run as backend services or integrate into existing UIs.

Ask the user which part they need help with:

- **Components in different repos** (most common): You may only have access to one component. Complete what you can, then tell the user what steps remain for the other repos.
- **Co-located components**: All three in the same project—work through them one at a time (Studio → Agent → Frontend).
- **Already on step 2 or 3**: If you can't find a Studio in the codebase, ask the user if Studio setup is complete.

Also understand:

1. **Their stack**: What framework/runtime? (Next.js, Remix, Node server, Python, etc.)
2. **Their AI library**: Vercel AI SDK, LangChain, direct API calls, etc.
3. **Their domain**: What will the agent help with? (Shopping, docs, support, search, etc.)

The reference patterns use Next.js + Vercel AI SDK, but adapt to whatever the user is working with.

## Workflow

### Quick Validation (Optional)

Before building an agent, you can validate MCP access directly using the base URL (no slug required):

```bash
curl -X POST https://api.sanity.io/YOUR_API_VERSION/agent-context/YOUR_PROJECT_ID/YOUR_DATASET \
  -H "Authorization: Bearer $SANITY_API_READ_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "tools/list", "id": 1}'
```

This confirms your token works and the MCP endpoint is reachable. The base URL gives access to all content—useful for testing before setting up content filters via agent context documents.

### Step 1: Set up Sanity Studio

Configure the context plugin and create agent context documents to scope what content the agent can access.

See [references/studio-setup.md](references/studio-setup.md)

### Step 2: Build the Agent (Adapt to user's stack)

**Already have an agent or MCP client?** You just need to connect it to your Context MCP URL with a Bearer token. The tools will appear automatically.

**Building from scratch?** The reference implementation uses Next.js + Vercel AI SDK with Anthropic, but the pattern works with any LLM provider (OpenAI, local models, etc.). It's comprehensive—covering everything from basic chat to advanced patterns. **Start with the basics and add advanced patterns as needed.**

See [references/nextjs-agent.md](references/nextjs-agent.md)

The reference covers:

- **Core setup** (required): MCP connection, authentication, basic chat route
- **System prompts** (required): Domain-specific instructions for your agent
- **Frontend** (optional): React chat component
- **Advanced patterns** (optional): Client-side tools, auto-continuation, custom rendering

## GROQ with Semantic Search

Context MCP supports `text::embedding()` for semantic ranking:

```groq
*[_type == "article" && category == "guides"]
  | score(text::embedding("getting started tutorial"))
  | order(_score desc)
  { _id, title, summary }[0...10]
```

Always use `order(_score desc)` when using `score()` to get best matches first.

## Adapting to Different Stacks

The MCP connection pattern is framework and LLM-agnostic. Whether Next.js, Remix, Express, or Python FastAPI—the HTTP transport works the same. Any LLM provider that supports tool calling will work.

See [references/nextjs-agent.md](references/nextjs-agent.md#adapting-to-other-stacks) for:

- Framework-specific route patterns (Express, Remix, Python)
- AI library integrations (LangChain, direct API calls)
- System prompt examples for different domains (e-commerce, docs, support)

## Best Practices

- **Start simple**: Build the basic integration first, then add advanced patterns as needed
- **Schema design**: Use descriptive field names—agents rely on schema understanding
- **GROQ queries**: Always include `_id` in projections so agents can reference documents
- **Content filters**: Start broad, then narrow based on what the agent actually needs
- **System prompts**: Be explicit about forbidden behaviors and formatting rules

## Troubleshooting

### Context MCP returns errors or no schema

Context MCP requires your schema to be available server-side. This happens automatically when your Studio runs, but if it's not working:

1. **Check Studio version**: Ensure you're on Sanity Studio v5.1.0 or later
2. **Open your Studio**: Simply opening the Studio in a browser triggers schema deployment
3. **Verify deployment**: After opening Studio, retry the MCP connection

### Other common issues

See [references/nextjs-agent.md](references/nextjs-agent.md#troubleshooting) for:

- Token authentication errors
- Empty results / no documents found
- Tools not appearing
