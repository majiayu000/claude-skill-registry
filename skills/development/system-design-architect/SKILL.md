/*============================================================================*/
/* SYSTEM-DESIGN-ARCHITECT SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: system-design-architect
version: 1.0.0
description: |
  [assert|neutral] Comprehensive system design methodology using Dr. Synthara's organism-based approach. Treats systems as living organisms with specialized organs (API, DB, cache, queues), circulation (load balancing), [ground:given] [conf:0.95] [state:confirmed]
category: specialists
tags:
- system-design
- architecture
- scaling
- infrastructure
- interviews
author: Context Cascade (Dr. Synthara methodology)
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute system-design-architect workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic specialists processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "system-design-architect",
  category: "specialists",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Compositional",
  source: "German",
  force: "Build from primitives?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["system-design-architect", "specialists", "workflow"],
  context: "user needs system-design-architect capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# System Design Architect

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



A comprehensive system design skill using the organism-based mental model: systems are living creatures with organs, circulation, immune systems, and survival mechanisms.

## SKILL-SPECIFIC GUIDANCE

### When to Use This Skill

- Designing new systems from scratch
- System design interviews (FAANG-level)
- Architecture reviews and evolution planning
- Scaling existing systems (10x, 100x)
- Production readiness assessments
- Identifying and removing SPOFs

### When NOT to Use This Skill

- Simple CRUD applications with no scale needs
- Prototypes where architecture doesn't matter yet
- When requirements are completely undefined
- Premature optimization scenarios

### Success Criteria
- [assert|neutral] Clear non-negotiable invariants defined [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] All SPOFs identified and mitigated [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Decision trees applied for each component choice [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Trade-offs explicitly documented [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] 90-second narrative can explain the design [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] - [ground:acceptance-criteria] [conf:0.90] [state:provisional]

## Phase 0: Pin the Target Before Drawing Boxes

**You are designing for constraints, not for tech.**

### Constraint Extraction Checklist

| Constraint | Questions to Ask |
|------------|------------------|
| **Users & Usage** | DAU/MAU? Peak QPS? Read/write ratio? Payload sizes? |
| **Latency Target** | p50/p95/p99? Mobile vs desktop? Global vs local? |
| **Availability** | SLO (99.9? 99.99?)? RTO/RPO? |
| **Consistency** | Strong vs eventual? Where does correctness matter? |
| **Data Shape** | Relational? Document? Graph? Hot keys? |
| **Security** | Auth model? Threat surface? Compliance? |
| **Growth Path** | What changes if traffic 10x? 100x? |

### What I'm Thinking as a Designer

"What are the non-negotiable invariants?"

Examples:
- "No double-charging" (payments)
- "Messages never delivered out of order per conversation" (chat)
- "Inventory can't go negative" (e-commerce)
- "Tokens must be revocable" (auth)

---

## Phase 1: Baseline Single-Server Organism

Start with a simple diagram you can explain in 30 seconds:

```
Domain -> DNS -> Server IP
Client -> HTTPS -> Server
Server -> Business Logic -> DB -> Response
```

This sets a clean foundation to EVOLVE from, instead of prematurely microservicing.

---

## Phase 2: First Evolution - Split Tiers

Split into:
- **Web/App Tier**: Stateless compute (horizontally scalable by default)
- **Data Tier**: Database + durable storage

**Design Rule**: The web/app tier should be horizontally scalable BY DEFAULT.

**What I'm Thinking**: "Where is state living? Where does it need to live?"

If state lives in app memory, scaling breaks it.

---

## Decision Tree 1: Scaling

```
Need to handle more load?
|
+-- Mostly CPU/RAM bound + small scale + OK if brief downtime?
|   +-- Vertical scale (scale up) as short-term patch
|
+-- Need high availability OR growth beyond one machine?
    +-- Horizontal scale (scale out)
        +-- Add load balancer
        +-- Make app tier stateless
        +-- Move state to shared systems (DB/cache/object storage)
```

**System-Designer Thought**: Vertical scaling is a DELAY TACTIC; horizontal scaling is an ARCHITECTURE CHOICE.

---

## Decision Tree 2: Database Choice

```
What is the data + correctness need?
|
+-- Strong transactions / invariants (money, inventory, ledgers)?
|   +-- SQL (Postgres/MySQL) + ACID + constraints
|
+-- Clear relationships + joins matter?
|   +-- SQL (normalized + indexes)
|
+-- Semi-structured JSON + evolving schema + high scale writes?
|   +-- Document or wide-co

/*----------------------------------------------------------------------------*/
/* S4 SUCCESS CRITERIA                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] SUCCESS_CRITERIA := {
  primary: "Skill execution completes successfully",
  quality: "Output meets quality thresholds",
  verification: "Results validated against requirements"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S5 MCP INTEGRATION                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] MCP_INTEGRATION := {
  memory_mcp: "Store execution results and patterns",
  tools: ["mcp__memory-mcp__memory_store", "mcp__memory-mcp__vector_search"]
} [ground:witnessed:mcp-config] [conf:0.95] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S6 MEMORY NAMESPACE                                                         */
/*----------------------------------------------------------------------------*/

[define|neutral] MEMORY_NAMESPACE := {
  pattern: "skills/specialists/system-design-architect/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "system-design-architect-{session_id}",
  WHEN: "ISO8601_timestamp",
  PROJECT: "{project_name}",
  WHY: "skill-execution"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S7 SKILL COMPLETION VERIFICATION                                            */
/*----------------------------------------------------------------------------*/

[direct|emphatic] COMPLETION_CHECKLIST := {
  agent_spawning: "Spawn agents via Task()",
  registry_validation: "Use registry agents only",
  todowrite_called: "Track progress with TodoWrite",
  work_delegation: "Delegate to specialized agents"
} [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S8 ABSOLUTE RULES                                                           */
/*----------------------------------------------------------------------------*/

[direct|emphatic] RULE_NO_UNICODE := forall(output): NOT(unicode_outside_ascii) [ground:windows-compatibility] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_EVIDENCE := forall(claim): has(ground) AND has(confidence) [ground:verix-spec] [conf:1.0] [state:confirmed]

[direct|emphatic] RULE_REGISTRY := forall(agent): agent IN AGENT_REGISTRY [ground:system-policy] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* PROMISE                                                                     */
/*----------------------------------------------------------------------------*/

[commit|confident] <promise>SYSTEM_DESIGN_ARCHITECT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
