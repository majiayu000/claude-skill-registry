---
name: mastra
description: >-
  You are an expert in Mastra, the TypeScript framework for building AI
  agents, RAG pipelines, and workflows. You help developers create production
  AI applications with type-safe agent definitions, tool integration,
  vector-based knowledge retrieval, multi-step workflows with branching and
  error handling, and integration with 50+ third-party services — designed for
  TypeScript teams who want agent capabilities without Python dependencies.
license: Apache-2.0
compatibility: ''
metadata:
  author: terminal-skills
  version: 1.0.0
  category: AI & Machine Learning
  tags:
    - agent
    - framework
    - typescript
    - tools
    - rag
    - workflow
    - production
---

# Mastra — TypeScript AI Agent Framework

You are an expert in Mastra, the TypeScript framework for building AI agents, RAG pipelines, and workflows. You help developers create production AI applications with type-safe agent definitions, tool integration, vector-based knowledge retrieval, multi-step workflows with branching and error handling, and integration with 50+ third-party services — designed for TypeScript teams who want agent capabilities without Python dependencies.

## Core Capabilities

### Agent Definition

```typescript
import { Agent } from "@mastra/core";
import { openai } from "@mastra/openai";
import { z } from "zod";

const supportAgent = new Agent({
  name: "Customer Support",
  model: openai("gpt-4o"),
  instructions: `You are a customer support agent for a SaaS product.
    Use the knowledge base to answer questions.
    Create tickets for issues you can't resolve.
    Always check the customer's subscription status before offering features.`,

  tools: {
    searchKnowledgeBase: {
      description: "Search the product knowledge base",
      parameters: z.object({ query: z.string() }),
      execute: async ({ query }) => {
        const results = await vectorStore.search(query, { topK: 5 });
        return results.map(r => ({ title: r.metadata.title, content: r.content }));
      },
    },
    getCustomerInfo: {
      description: "Get customer subscription and account details",
      parameters: z.object({ email: z.string().email() }),
      execute: async ({ email }) => {
        const customer = await db.customers.findByEmail(email);
        return { plan: customer.plan, since: customer.createdAt, tickets: customer.openTickets };
      },
    },
    createTicket: {
      description: "Create a support ticket for the engineering team",
      parameters: z.object({
        title: z.string(),
        description: z.string(),
        priority: z.enum(["low", "medium", "high", "critical"]),
        customerEmail: z.string().email(),
      }),
      execute: async (params) => {
        const ticket = await db.tickets.create(params);
        return { ticketId: ticket.id, message: `Ticket ${ticket.id} created` };
      },
    },
  },
});

// Use the agent
const response = await supportAgent.generate(
  "I'm having issues with the API rate limiter. My email is alice@acme.com",
);
console.log(response.text);

// Streaming
const stream = await supportAgent.stream("Help me set up webhooks");
for await (const chunk of stream) {
  process.stdout.write(chunk);
}
```

### RAG Pipeline

```typescript
import { createVectorStore } from "@mastra/rag";
import { openai } from "@mastra/openai";

const vectorStore = createVectorStore({
  provider: "pgvector",                    // Or pinecone, qdrant, chroma
  connectionString: process.env.DATABASE_URL,
  embeddingModel: openai.embedding("text-embedding-3-small"),
});

// Index documents
await vectorStore.upsert([
  { id: "doc-1", content: "How to set up webhooks: ...", metadata: { title: "Webhooks Guide", category: "api" } },
  { id: "doc-2", content: "Rate limiting policy: ...", metadata: { title: "Rate Limits", category: "api" } },
]);

// Search
const results = await vectorStore.search("webhook configuration", {
  topK: 5,
  filter: { category: "api" },
});
```

### Workflows

```typescript
import { Workflow, Step } from "@mastra/core";

const onboardingWorkflow = new Workflow({
  name: "customer-onboarding",
  steps: [
    new Step({
      id: "validate",
      execute: async ({ input }) => {
        const customer = await validateCustomer(input.email);
        return { customer, isNewCustomer: !customer.hasCompletedOnboarding };
      },
    }),
    new Step({
      id: "setup-account",
      when: ({ previous }) => previous.validate.isNewCustomer,
      execute: async ({ previous }) => {
        await createDefaultProject(previous.validate.customer.id);
        await seedSampleData(previous.validate.customer.id);
        return { projectCreated: true };
      },
    }),
    new Step({
      id: "send-welcome",
      execute: async ({ previous, input }) => {
        const template = previous.setup_account?.projectCreated ? "new-user" : "returning-user";
        await sendEmail(input.email, template);
        return { emailSent: true };
      },
    }),
  ],
});

await onboardingWorkflow.execute({ email: "new@customer.com" });
```

## Installation

```bash
npm install @mastra/core @mastra/openai @mastra/rag
```

## Best Practices

1. **TypeScript-native** — Full type safety for agents, tools, workflows; no Python required
2. **Tool definitions** — Use Zod schemas for tool parameters; type-safe at compile AND runtime
3. **RAG built-in** — Vector store abstraction with pgvector, Pinecone, Qdrant; no separate RAG library
4. **Workflows** — Multi-step with conditional branching (`when`), error handling, and retries
5. **Streaming** — Use `.stream()` for real-time responses; works with any frontend
6. **50+ integrations** — Pre-built connectors for Slack, GitHub, Linear, Notion, etc.
7. **Agent memory** — Built-in conversation memory; configurable per agent
8. **Evaluation** — Built-in eval framework; test agent quality before deployment
