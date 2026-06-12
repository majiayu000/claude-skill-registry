---
name: inngest-agents
description: Use when building durable AI agents or agentic workflows with Inngest and AgentKit, including model calls, tool calls, multi-agent networks, human approval, realtime progress, provider rate limits, and crash-safe execution. Covers AgentKit, `step.ai`, `step.run`, `step.waitForEvent`, native realtime, and when to use lower-level Inngest primitives instead of an in-memory agent loop.
---

# Inngest Agents

Use this skill when the user wants to build, migrate, or debug an AI agent,
multi-step AI workflow, tool-calling loop, support agent, research agent,
human-in-the-loop review flow, or realtime agent UI.

Inngest's AgentKit defines agents with `createAgent`; when an AgentKit run is
owned by an Inngest function, model calls use Inngest `step.ai` so they retry
and cache model results durably. Use the lower-level Inngest step primitives
around the agent for database reads/writes, tool side effects, waits,
approvals, realtime progress, and flow control.

Official references:

- AgentKit agents: https://agentkit.inngest.com/concepts/agents
- `createAgent`: https://agentkit.inngest.com/reference/create-agent
- AI inference and `step.ai`: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/step-ai-orchestration
- AgentKit realtime hooks: https://www.inngest.com/changelog/2025-09-24-agentkit-use-agent

## Copyable Example

When starting a durable support or tool-calling agent from scratch, inspect the
companion example at `../../examples/durable-agent`. It shows the expected
agent-first shape: quick HTTP trigger, typed events, AgentKit inside an
Inngest function, step-scoped context loading, human approval with
`step.waitForEvent`, and durable side effects after approval.

## When to Use Inngest for Agents

Good fit:

- Agent can take longer than one HTTP request.
- Agent calls tools, APIs, databases, browsers, sandboxes, or MCP servers.
- Agent needs to survive deploys, crashes, serverless timeouts, or model/API
  failures.
- Agent may wait for human approval, external callbacks, scheduled follow-up,
  or user input.
- Agent progress should stream to a UI from the durable workflow.
- Model/provider calls need concurrency or throttle limits.
- Duplicate sends, charges, writes, or model calls would be costly.

Not usually worth it:

- One short, read-only model call with no side effects and no need for durable
  progress.
- UI-only autocomplete where losing the request is acceptable.

## Architecture

Use this shape unless the repo already has a stronger established pattern:

1. The HTTP/server action layer validates auth, stores the user's intent if
   needed, emits an event with a stable `id`, and returns quickly.
2. An Inngest function owns the agent run.
3. Load state and external context inside `step.run`.
4. Create AgentKit agents inside the function or import agent/network
   factories.
5. Run model inference through AgentKit / `step.ai`; wrap non-model tool side
   effects in `step.run`.
6. Use `step.waitForEvent` or `step.waitForSignal` for human approval and
   external callbacks.
7. Publish durable progress with native realtime.
8. Apply flow control at the function level for provider and tenant limits.

## Basic AgentKit Function

Prefer a small, typed function first; add networks and extra tools after the
single-agent path is proven.

```typescript
import { createAgent, openai } from "@inngest/agent-kit";
import { inngest } from "@/inngest/client";

export const summarizeTicket = inngest.createFunction(
  {
    id: "summarize-ticket",
    triggers: [{ event: "support/ticket.created" }],
    concurrency: [{ key: "event.data.accountId", limit: 2 }]
  },
  async ({ event, step }) => {
    const ticket = await step.run("load-ticket", () => {
      return getTicket(event.data.ticketId);
    });

    const writer = createAgent({
      name: "support-summary-writer",
      system: "Write a concise support-ticket summary with next actions.",
      model: openai({ model: "gpt-4o" })
    });

    const { output } = await writer.run(JSON.stringify(ticket));

    await step.run("save-summary", () => {
      return saveTicketSummary(event.data.ticketId, output);
    });

    return { ticketId: event.data.ticketId };
  }
);
```

## Tool Calls

Tools can be defined with AgentKit, but agent-safe tools should still follow
durability rules:

- Read-only tool calls can run as part of the agent when replaying is harmless.
- External side effects should be isolated with stable IDs and `step.run`
  boundaries, or implemented as tool handlers that use the provided `step`.
- Tool outputs should be small enough for step state limits.
- Validate tool parameters with schemas; never trust model-provided arguments.
- Use tenant/user IDs from authenticated event data, not only from model text.

Tool side-effect checklist:

```text
- What external state can this tool change?
- What idempotency key prevents duplicate writes?
- What should happen if the model calls the same tool twice?
- Is the output safe to store in function run state?
- Does the tool need provider-specific concurrency or throttle limits?
```

## Human in the Loop

Use a durable wait instead of polling a database or keeping state in memory.

```typescript
const approval = await step.waitForEvent("wait-for-approval", {
  event: "support/reply.approved",
  timeout: "3d",
  match: "data.ticketId"
});

if (!approval) {
  await step.run("mark-review-timeout", () => {
    return markTicketNeedsManualReview(event.data.ticketId);
  });
  return { status: "timed_out" };
}

await step.run("send-reply", () => {
  return sendSupportReply({
    ticketId: event.data.ticketId,
    approvalId: approval.data.approvalId
  });
});
```

## Realtime Progress

For v4 native realtime:

- Use `step.realtime.publish` between steps.
- Use `inngest.realtime.publish` inside an existing `step.run`.
- Do not install the v3 `@inngest/realtime` package for v4 projects.
- Do not build a process-local WebSocket as the only source of progress for a
  durable function.

For AgentKit-specific UI hooks, check the installed `@inngest/agent-kit`
version and current docs before wiring `useAgent` or `useChat`.

## Flow Control and Cost

Agent workloads often need provider and tenant limits:

- Use account-scoped concurrency or throttle keys for model providers.
- Key per tenant or account where fairness matters.
- Use deterministic event IDs so duplicate user actions do not spawn duplicate
  expensive runs.
- Keep successful model/tool results in steps so retrying a later failure does
  not re-charge earlier model calls.

Example:

```typescript
{
  id: "support-agent-run",
  triggers: [{ event: "support/agent.requested" }],
  throttle: {
    limit: 120,
    period: "1m",
    key: `"openai"`
  },
  concurrency: [
    { key: "event.data.accountId", limit: 3 }
  ]
}
```

## Brownfield Migration

When migrating an existing agent:

1. Search for model calls, tool loops, in-memory state, streaming handlers,
   approval polling, and external side effects.
2. Keep prompt/tool behavior stable at first.
3. Move the trigger into an event and an Inngest function.
4. Move model calls to AgentKit / `step.ai`.
5. Move side-effecting tools into `step.run` or durable tool handlers.
6. Replace process-local waits with `step.waitForEvent` or
   `step.waitForSignal`.
7. Add realtime after the durable run is working.

Use `inngest-brownfield-audit` first when the repo has multiple possible
workflows and the user has not picked one.

## Anti-Patterns

- Agent loop state only in memory.
- One giant `try/catch` around all model and tool calls.
- Retrying the entire agent after one tool failure.
- Charging repeatedly for successful model calls after a later step fails.
- `setTimeout`, cron polling, or Redis TTL as the human-review mechanism.
- Side-effecting tools with no idempotency key.
- Streaming progress from a server process that can die while the durable work
  continues elsewhere.
- Adding AgentKit without registering the surrounding Inngest function.

## Verification

- Typecheck the agent, tool schemas, and event payloads.
- Unit-test tool handlers separately from model behavior.
- Test that the HTTP entrypoint emits one deterministic event and returns fast.
- Test that duplicate event IDs do not duplicate final side effects.
- If possible, run the Inngest dev server and inspect the agent steps/traces.
