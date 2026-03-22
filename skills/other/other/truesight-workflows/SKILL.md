---
name: truesight-workflows
description: Orchestrator for Truesight MCP skills. Use this when the user needs help choosing the right Truesight workflow or when intent is ambiguous across LLM evaluate, error analysis, review, templates, or evaluation creation.
---

# Truesight Workflows

Use this skill as the routing entrypoint across all Truesight MCP skills.

## Role and scope

This skill is a router. It decides intent and routes to exactly one skill path.

Do not execute deep workflow steps here unless the user already asked for a very specific action and no further routing is needed.

## Routing map

- Build custom live eval from scratch -> `create-evaluation`
- Evaluate one or more traces with an existing live eval -> `evaluate-trace`
- Analyze failure modes in dataset traces -> `error-analysis`
- Judge flagged items and add labeled outputs back to dataset -> `review-and-promote-traces`
- Start quickly from pre-built template -> `bootstrap-template-evaluation`
- Audit current eval setup and maturity -> `eval-audit`
- Build custom review web interface -> `build-review-interface`

## Interactive Q&A protocol (mandatory)

<HARD-GATE>
BEFORE the first scoping question, search for a structured question tool (e.g., `AskUserQuestion` or similar interactive widget) and load it. Use that tool for EVERY scoping question. Fall back to plain-text lettered options ONLY if no such tool exists in the environment.
</HARD-GATE>

When user intent is unclear, ask one question at a time using the structured question tool (loaded per the HARD-GATE above). Structure each with a short header, options with labels and descriptions, and place the recommended option first. Do not add "(Recommended)" or similar annotations to option labels.

Question format:

```
Which workflow do you want to run first?
A) Evaluate traces with an existing live eval
B) Run error analysis on a dataset
C) Review and promote flagged traces
D) Bootstrap from a template
E) Create a new evaluation from scratch
F) Audit my eval setup
G) Build a custom review interface
```

Rules:
- Ask exactly one routing question per message.
- Use one follow-up question only if the answer is still ambiguous.
- After routing is clear, hand off immediately to the target skill.

## Guardrails

- If user asks for `create-evaluation`, do not decompose it into smaller skills.
- Keep guidance scoped to currently available Truesight MCP tools.
- If user asks for functionality outside current MCP capabilities, state the gap clearly and offer the closest supported workflow.
