---
name: inngest-agent-evals
description: "Use when building, migrating, or debugging Agent Evals on Inngest: scoring AI agent or workflow outcomes, deferred scorers, sessions, traces, step experiments, experiment variant attribution, Insights queries, or production eval loops for prompts, models, tools, providers, and agent behavior. Covers TypeScript SDK v4 scoring beta APIs, `scoreMiddleware`, `step.score`, `inngest.score`, `createScorer`, `defer`, `group.experiment`, `experimentRef`, `meta.sessions`, and when to use durable workflow primitives for outcome-based evaluation."
---

# Inngest Agent Evals

Use this skill when the user wants to evaluate AI agents or AI workflows in
production, add scoring, compare prompts/models/tools, group related runs, or
debug why an agent outcome was good or bad.

Agent Evals is not a separate package. It is the production evaluation workflow
built from Inngest functions, durable steps, scores, deferred scorers, sessions,
traces, experiments, and Insights.

## Canonical References

Check the public docs first when exact API details matter:

- Agent Evals overview: https://www.inngest.com/docs/learn/agent-evals
- Scoring guide: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/scoring
- Deferred scoring guide: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/deferred-scoring
- Step experiments guide: https://www.inngest.com/docs/features/inngest-functions/steps-workflows/step-experiments
- Sessions: https://www.inngest.com/docs/features/events-triggers/sessions
- Traces: https://www.inngest.com/docs/platform/monitor/traces
- Insights: https://www.inngest.com/docs/platform/monitor/insights
- Scoring reference: https://www.inngest.com/docs/reference/typescript/v4/functions/scoring
- `group.experiment()` reference: https://www.inngest.com/docs/reference/typescript/v4/functions/group-experiment
- Launch context: https://www.inngest.com/blog/introducing-agent-evals

## Decision Flow

Start from the outcome, not the mechanism:

1. Identify the product or quality signal: helpful click, ticket resolution,
   conversion, guardrail pass, retrieval quality, model confidence, latency,
   cost, human review, or LLM-as-judge result.
2. Decide when the signal appears:
   - During the run: use direct scoring with `step.score()` or
     `inngest.score()`.
   - After the run: use deferred scoring with `createScorer()` and `defer()`,
     or explicit `inngest.score({ runId })`.
3. Decide how humans will inspect related work:
   - Use `meta.sessions` for repeated high-cardinality identifiers such as
     `conversation_id`, `ticket_id`, `agent_run_id`, or `import_id`.
   - Use Insights for ad hoc historical analysis, low-cardinality filters, SQL
     aggregates, and broad investigation.
4. Decide whether to compare variants:
   - Use `group.experiment()` for prompt, model, provider, tool, workflow, or
     rollout comparisons.
   - Pass `experimentRef` to deferred or later scores when the score should be
     credited to the selected variant.
5. Preserve traceability:
   - Keep model calls, tool calls, waits, database writes, and scoring work in
     durable steps so traces explain why the score happened.

## Setup Requirements

- Use TypeScript SDK v4 and install the latest SDK: `npm install inngest@latest`.
- Scoring and deferred scoring are beta APIs; verify current imports against
  the docs before shipping user-facing examples.
- `step.score()` requires `scoreMiddleware()` from `inngest/experimental` on
  the Inngest client.
- `createScorer()` is imported from `inngest/experimental` and the scorer must
  be registered in the serve handler with other functions.
- Sessions sent through the TypeScript SDK require v4.7.0 or later.
- Step experiments require v4.8.0 or later for `group.experiment()` and the
  `experiment` helper from `inngest`.

Client shape:

```typescript
import { Inngest } from "inngest";
import { scoreMiddleware } from "inngest/experimental";

export const inngest = new Inngest({
  id: "support-agent",
  middleware: [scoreMiddleware()],
});
```

## Sessions

Add sessions when events belong to a user flow, conversation, ticket, import,
or agent task that someone will inspect repeatedly.

```typescript
await inngest.send({
  name: "support/ticket.created",
  data: {
    ticketId: "tk_123",
    message: "I can't sign in.",
  },
  meta: {
    sessions: {
      ticket_id: "tk_123",
    },
  },
});
```

Rules:

- Use stable, non-secret, high-cardinality IDs.
- Keep the key generic, such as `conversation_id`; put the actual ID in the
  value.
- Pass sessions explicitly through `step.invoke()` and `step.sendEvent()` when
  downstream runs should join the same session.
- Do not use sessions for labels like `environment: prod`; use Insights for
  that style of filtering.

## Direct Scoring

Use direct scoring when the score is known during the function run.

Good direct scores:

- guardrail pass/fail
- JSON validity
- retrieval confidence
- tool success
- model confidence
- inline LLM-as-judge result

```typescript
export const answerTicket = inngest.createFunction(
  {
    id: "answer-ticket",
    triggers: [{ event: "support/ticket.created" }],
  },
  async ({ event, step }) => {
    const answer = await step.run("generate-answer", () =>
      generateAnswer(event.data.ticketId)
    );

    const passed = await step.run("check-answer", () => validateAnswer(answer));

    await step.score("score-answer-quality", {
      name: "answer-quality",
      value: passed,
    });

    return { answer, passed };
  }
);
```

Use stable score names. Changing a score name creates a separate metric.
Score values must be finite numbers or booleans.

## Deferred Scoring

Use deferred scoring when the useful signal arrives after the parent workflow
finishes, such as user feedback, conversion, ticket reopen, retention, or a
slow LLM-as-judge run.

```typescript
import { createScorer } from "inngest/experimental";
import { z } from "zod";

export const feedbackScorer = createScorer(
  inngest,
  {
    id: "support-feedback-scorer",
    schema: z.object({ ticketId: z.string() }),
  },
  async ({ event, step }) => {
    const feedback = await step.waitForEvent("wait-for-feedback", {
      event: "support/feedback.received",
      timeout: "7d",
      if: `async.data.ticketId == '${event.data.ticketId}'`,
    });

    return {
      name: "user-feedback",
      value: feedback?.data.helpful ? 1 : 0,
    };
  }
);
```

Trigger it from the producing function:

```typescript
async ({ event, step, defer }) => {
  const answer = await step.run("generate-answer", () =>
    generateAnswer(event.data.ticketId)
  );

  defer("score-feedback", {
    function: feedbackScorer,
    data: { ticketId: event.data.ticketId },
  });

  return { answer };
}
```

Guardrails:

- Register scorers with `serve({ functions: [...] })`.
- `defer()` is fire-and-forget; do not `await` it.
- The parent run is attributed automatically for deferred scorers.
- Return a default score or `null` when a signal times out, based on the
  product semantics.

## Experiments

Use `group.experiment()` when comparing prompts, models, providers, tools,
workflow rewrites, or operational settings against real traffic.

```typescript
import { experiment } from "inngest";

const { result, variant, experimentRef } = await group.experiment(
  "answer-style",
  {
    variants: {
      concise: () => step.run("answer-concise", () => answerConcise(event.data)),
      detailed: () =>
        step.run("answer-detailed", () => answerDetailed(event.data)),
    },
    select: experiment.bucket(event.data.accountId, {
      weights: { concise: 50, detailed: 50 },
    }),
  }
);
```

Selection strategy:

- `experiment.weighted()` for run-level traffic splits.
- `experiment.bucket(stableId, { weights })` when a user, account, or tenant
  should usually keep the same experience.
- `experiment.custom()` when assignment comes from a database, flag service, or
  rollout table.
- `experiment.fixed()` to force one variant during testing or after choosing a
  winner.

Rules:

- Each variant callback must call at least one `step.*` tool.
- Keep experiment IDs and variant names stable because they appear in traces.
- The selected variant is memoized for retries and replays.
- Persist `experimentRef` and the parent run ID if a later, separate process
  will score the selected variant.

When deferred scoring a variant, pass the ref:

```typescript
defer("score-answer-feedback", {
  function: feedbackScorer,
  data: { ticketId: event.data.ticketId },
  experiment: experimentRef,
});
```

When scoring from a later run explicitly:

```typescript
await inngest.score.experiment({
  name: "clickthrough",
  value: 1,
  experiment: experimentRef,
  runId: originalRunId,
});
```

## Brownfield Migration

When adding Agent Evals to an existing app:

1. Search for existing agent/workflow outputs and where users act on them.
2. Find durable identifiers already in the domain: conversation ID, ticket ID,
   account ID, import ID, run ID, or recommendation ID.
3. Add `meta.sessions` at event producers before building dashboards around
   correlation.
4. Add one direct score where the outcome is already known.
5. Add a deferred scorer only after the signal event exists or can be emitted
   cleanly.
6. Add `group.experiment()` only around one isolated decision at a time.
7. Keep old prompt/model/tool behavior stable until scoring proves the new path.

Use `inngest-brownfield-audit` first when the repo has many candidate
workflows. Use `inngest-agents` with this skill when the work is an AgentKit or
durable agent workflow.

## Anti-Patterns

- Starting with a prompt experiment before naming the outcome metric.
- Scoring with unstable names, strings, objects, `NaN`, or `Infinity`.
- Forgetting `scoreMiddleware()` and then assuming `step.score()` is missing.
- Running scorers in an external queue when the scorer needs durable waits.
- Keeping experiment assignment only in memory.
- Scoring an experiment variant from a later run without the original `runId`.
- Using sessions for low-cardinality labels or sensitive personal data.
- Leaving model/tool work outside steps, making traces unable to explain the
  score.

## Verification

- Typecheck the Inngest client, functions, scorer schemas, and serve handler.
- Confirm scorers are registered with the serve endpoint.
- Test the producer emits events with expected `meta.sessions`.
- Test direct scores use stable names and finite number/boolean values.
- Test deferred scorer timeout behavior.
- For experiments, test that each variant callback contains step work and that
  later scoring receives `experimentRef` plus the original run ID when needed.
- If possible, run the Inngest dev server and inspect traces, sessions, scores,
  and experiment variant selection in the dashboard or through available CLI/API
  tooling.
