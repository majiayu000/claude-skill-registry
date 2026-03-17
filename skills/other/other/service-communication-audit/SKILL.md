---
name: service-communication-audit
description: "Use when analyzing, designing, or fixing how services communicate — especially when communication is unstable, one-directional, fire-and-forget, lacks backpressure, or has no recovery path. Covers inter-service sync, connection lifecycle, tick rate analysis, failure mode mapping, and protocol design for self-healing systems. Use when user mentions instability between services, sync issues, reconnection problems, or asks to review how two systems talk to each other."
---

# Service Communication Audit

Systematic audit of how services talk to each other. Not just finding broken wires — questioning whether each wire should exist, in which direction, at what rate, and what comes back.

The core principle: **deep modules with simple interfaces, not webs of shallow wiring.** The consumer sees one health surface, one response, one interface. The implementation behind it can be as complex as needed — the consumer doesn't know or care. Every design decision filters through: "does this expose internal wiring to the consumer, or does it stay behind the module boundary?"

The full field guide is at `references/communication-audit-guide.md` (~40 principles). Do NOT summarize the guide in prompts — workers read it directly.

## When To Use

- Services communicate but the connection is unstable or brittle
- Fire-and-forget calls with no acknowledgment or retry
- One service crashes and the other doesn't notice or recover
- No backpressure — failures cause hammering instead of backing off
- "It works if you start things in the right order" (startup race)
- Health checks that lie
- Multiple data channels crammed into one tick at one rate

## How It Works

### Step 1: Scope The Audit

Identify which services and which communication paths to audit. Determine:
- The service directories / crate paths
- Which boundaries to focus on (all, or specific problem area)
- Any auto-generated code to exclude (bindings, protobuf)

### Step 2: Delegate The Auditor

Delegate using `teams` with `anthropic/claude-opus-4-6`. The worker must:

1. Read `references/communication-audit-guide.md` completely first
2. Map ALL communication boundaries before analyzing any single one
3. Find **specific code locations** for every failure mode
4. Show the current code and the proposed fix for each finding
5. Produce a rate analysis with justified Hz for every channel

**Critical instruction quality rules:**

- "Trace every failure path to what the end user sees" — not "this could fail"
- "Show the exact code that hammers, the exact line that drops damage events" — not "error handling could be improved"
- "Calculate the serialization cost at N entities × Hz" — not "this seems frequent"
- "Do NOT produce a checklist. Do NOT say '❌ Missing'."

### Step 3: Formulate The Dispatch

```
teams(action: 'delegate', tasks: [{
  text: '<audit request — see template below>',
  assignee: 'comm-auditor',
  model: 'anthropic/claude-opus-4-6'
}])
```

Template (fill in `{placeholders}`):

```
# Service Communication Audit

Read the field guide at {skill_dir}/references/communication-audit-guide.md completely first. It contains 30 principles across 5 areas: mapping, failure modes, Hz analysis, protocol design, and anti-patterns.

## Target
Services: {service names and directories}
Focus area: {specific problem or "full audit"}
Exclude: {auto-generated files, bindings, etc.}

## Rules
- Map ALL communication paths FIRST, then analyze.
- Every finding must include the EXACT current code (file:line) and proposed fix.
- Trace every failure to user impact. "This could fail" is not a finding.
- Calculate actual Hz/throughput numbers, not estimates.
- Do NOT produce a checklist. Produce a narrative with evidence.

## Deliverables

### 1. Communication Map
Table of every boundary: source, destination, transport, direction, rate, criticality tier (ephemeral/important/critical/fatal), acknowledgment (none/_then/response), failure behavior.

### 2. Failure Mode Catalog  
For each failure mode found (§6–§12 in guide): the exact code, the cascade to user impact, the fix. Show BEFORE/AFTER code.

### 3. Rate Analysis
For each rate-driven channel: current Hz, all consumers traced, actual Hz needed, serialization cost at scale, verdict.

### 4. Design Reasoning (MOST IMPORTANT)
For each boundary, answer the §31–§40 questions:
- Why does this data cross this boundary? What breaks without it? (§31)
- Could the response carry data that's currently a subscription? (§33)
- What's the minimum subscription set if responses carry everything they can? (§35)
- What would make this fully self-healing with zero human intervention? (§37)
- Describe the ideal protocol in plain language before proposing code (§40)

### 5. Protocol Design
Proposed channel separation, acknowledgment strategy, connection state machine, health reporting architecture. Must follow from the design reasoning, not from "fix the current bugs."

### 6. Ticket List
Each issue as: title, problem (with code evidence), fix approach, acceptance criteria. Group into epic. Wire dependencies.

## Output
Write findings to {output_ticket_id} or create a new ticket tagged `research,communication-audit`.
```

### Step 4: Present Results

Summarize the top findings in a table:

| # | Issue | Severity | Current Code | Impact |
|---|-------|----------|-------------|--------|

Point to the full report for details. If the user wants to act, create tickets from the findings using `tk`.

### Step 5: Create Tickets (if acting)

For each finding, create a ticket. Wire dependencies:
- State machine / connection lifecycle → foundation
- Error handling unification → before circuit breaker
- Connection retry → before backpressure
- Hz reduction → independent, can parallelize

Search for existing related tickets first: `tk ls --status=open`, `totalrecall tk recall "<topic>"`.

## What The Guide Covers

| Part | Principles | Area |
|------|-----------|------|
| I | §1–§5 | Mapping: boundaries, criticality, data flow, subscriptions, startup races |
| II | §6–§12 | Failure modes: permanent blindness, hammering, silent data loss, lying health, theater recovery, hollow shell, startup cascade |
| III | §13–§16 | Hz analysis: trace to consumer, separate rate from criticality, FFI cost, delta vs full |
| IV | §17–§23 | Protocol: circuit breaker, nuclear recovery, evidence-based health, readiness gates, request-response, layered health, ack channels |
| V | §24–§30 | Anti-patterns: "SDK handles it", log without counting, one flush, passive staleness, client sees internals, unquestioned Hz, individual bulk commands |
| VI | §31–§40 | **Design reasoning**: why does this data cross this boundary, who owns this in 5 years, could the response carry this, minimum subscription set, big module thinking, acknowledgment enables everything, design the protocol you wish you had |

**Part VI is the most important part.** Parts I–V find what's broken and fix it. Part VI questions whether the boundary should exist at all, whether the direction is right, whether subscriptions could be responses. This is the part that changes architecture, not just error handling.
