/*============================================================================*/
/* ADVANCED-COORDINATION SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: advanced-coordination
version: 1.0.0
description: |
  [assert|neutral] Advanced multi-agent coordination patterns for complex distributed systems. Use when coordinating 5+ agents with dynamic task dependencies, implementing Byzantine fault tolerance, or managing distribu [ground:given] [conf:0.95] [state:confirmed]
category: orchestration
tags:
- orchestration
- coordination
- swarm
author: ruv
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute advanced-coordination workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "advanced-coordination",
  category: "orchestration",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Aspectual",
  source: "Russian",
  force: "Complete or ongoing?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["advanced-coordination", "orchestration", "workflow"],
  context: "user needs advanced-coordination capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## Orchestration Skill Guidelines

### When to Use This Skill
- **Multi-agent coordination** requiring topology-aware task distribution
- **Cloud-based orchestration** with Flow Nexus platform integration
- **Event-driven workflows** needing message-based coordination
- **Distributed systems** spanning multiple execution environments
- **Scalable swarms** with adaptive topology management

### When NOT to Use This Skill
- **Single-agent tasks** with no coordination overhead
- **Local-only execution** not using cloud features
- **Simple sequential work** without event-driven needs
- **Static topologies** not requiring adaptive scaling

### Success Criteria
- [assert|neutral] *Coordination topology established** (mesh/hierarchical/star) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *All agents registered** in coordination namespace [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Event routing functional** with <50ms message latency [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *No coordination deadlocks** - All agents progressing [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Scalability validated** - Handles target agent count [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases to Handle
- **Network partitions** - Implement partition tolerance with eventual consistency
- **Message loss** - Add message acknowledgment and retry logic
- **Agent disconnection** - Detect disconnects, redistribute work
- **Topology reconfiguration** - Support live topology changes without restart
- **Rate limiting** - Handle cloud API rate limits with backoff

### Guardrails (NEVER Violate)
- [assert|emphatic] NEVER: lose coordination state** - Persist topology and agent registry [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate topology** - Check for cycles, orphaned nodes [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: monitor message queues** - Prevent queue overflow [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: skip health checks** - Continuous agent liveness monitoring [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: handle failures gracefully** - No cascading failures [ground:policy] [conf:0.98] [state:confirmed]

### Evidence-Based Validation
- **Verify topology structure** - Validate graph properties (connected, acyclic if needed)
- **Check message delivery** - Confirm all messages reached targets
- **Measure coordination overhead** - Calculate % time spent on coordination vs work
- **Validate agent reachability** - Ping all agents, verify responses
- **Audit scalability** - Test with max agent count, measure performance


# Advanced Coordination - Distributed Agent Management

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Sophisticated coordination protocols for large-scale multi-agent systems with fault tolerance and consensus requirements.

## When to Use This Skill

Use when coordinating complex multi-agent workflows with 5+ concurrent agents, implementing fault-tolerant distributed systems, managing dynamic task dependencies across agents, or requiring consensus protocols (RAFT, Byzantine, Gossip).

## Coordination Strategies

### RAFT Consensus
- Leader election among agents
- Replicated log consistency
- Fault tolerance for N/2+1 failures
- Strong consistency guarantees

### Gossip Protocol
- Peer-to-peer agent communication
- Eventually consistent state sharing
- Highly scalable (100+ agents)
- Network partition resilient

### Byzantine Fault Tolerance
- Malicious or faulty agent detection
- 3F+1 redundancy for F failures
- Cryptographic verification
- Critical system integrity

## Process

1. **Analyze coordination requirements**
   - Determine number of agents needed
   - Identify fault tolerance needs
   - Assess consistency requirem

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
  pattern: "skills/orchestration/advanced-coordination/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "advanced-coordination-{session_id}",
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

[commit|confident] <promise>ADVANCED_COORDINATION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
