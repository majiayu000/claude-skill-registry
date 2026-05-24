/*============================================================================*/
/* COORDINATION SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: coordination
version: 2.0.0
description: |
  [assert|neutral] Advanced multi-agent coordination patterns including mesh, hierarchical, and adaptive topologies with state synchronization, consensus mechanisms, and distributed task execution. Use when orchestratin [ground:given] [conf:0.95] [state:confirmed]
category: orchestration
tags:
- coordination
- multi-agent
- orchestration
- topology
- consensus
author: ruv
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute coordination workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "coordination",
  category: "orchestration",
  version: "2.0.0",
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
  keywords: ["coordination", "orchestration", "workflow"],
  context: "user needs coordination capability"
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


# Agent Coordination Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Advanced multi-agent coordination system implementing sophisticated topologies (mesh, hierarchical, ring, star), consensus mechanisms (Byzantine, Raft, gossip), and distributed task execution patterns. This skill enables orchestration of complex workflows requiring multiple agents to collaborate, synchronize state, reach consensus, and execute tasks in a coordinated manner.

## When to Use This Skill

Activate this skill when:
- **Complex Multi-Agent Workflows**: Need to coordinate 3+ agents with interdependencies
- **Distributed Decision-Making**: Require consensus among multiple agents
- **Sophisticated Topologies**: Need mesh, hierarchical, or adaptive network structures
- **State Synchronization**: Agents must share and synchronize state
- **Fault-Tolerant Execution**: Require Byzantine fault tolerance or graceful degradation
- **Dynamic Scaling**: Agent count or topology changes during execution
- **Performance Optimization**: Need optimal agent allocation and load balancing

## Core Coordination Patterns

### 1. Topology Patterns

###

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
  pattern: "skills/orchestration/coordination/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "coordination-{session_id}",
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

[commit|confident] <promise>COORDINATION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
