/*============================================================================*/
/* WHEN-USING-ADVANCED-SWARM-USE-SWARM-ADVANCED SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-using-advanced-swarm-use-swarm-advanced
version: 1.0.0
description: |
  [assert|neutral] Advanced swarm patterns with dynamic topology switching and self-organizing behaviors for complex multi-agent coordination [ground:given] [conf:0.95] [state:confirmed]
category: workflow
tags:
- swarm
- advanced
- coordination
- topology
- self-organizing
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-using-advanced-swarm-use-swarm-advanced workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic workflow processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-using-advanced-swarm-use-swarm-advanced",
  category: "workflow",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Evidential",
  source: "Turkish",
  force: "How do you know?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-using-advanced-swarm-use-swarm-advanced", "workflow", "workflow"],
  context: "user needs when-using-advanced-swarm-use-swarm-advanced capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## Orchestration Skill Guidelines

### When to Use This Skill
- **Parallel multi-agent execution** requiring concurrent task processing
- **Complex implementation** with 6+ independent tasks
- **Theater-free development** requiring 0% tolerance validation
- **Dynamic agent selection** from 86+ agent registry
- **High-quality delivery** needing Byzantine consensus validation

### When NOT to Use This Skill
- **Single-agent tasks** with no parallelization benefit
- **Simple sequential work** completing in <2 hours
- **Planning phase** (use research-driven-planning first)
- **Trivial changes** to single files

### Success Criteria
- [assert|neutral] *Agent+skill matrix generated** with optimal assignments [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Parallel execution successful** with 8.3x speedup achieved [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Theater detection passes** with 0% theater detected [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Integration tests pass** at 100% rate [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *All agents complete** with no orphaned workers [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases to Handle
- **Agent failures** - Implement agent health monitoring and replacement
- **Task timeout** - Configure per-task timeout with escalation
- **Consensus failure** - Have fallback from Byzantine to weighted consensus
- **Resource exhaustion** - Limit max parallel agents, queue excess
- **Conflicting outputs** - Implement merge conflict resolution strategy

### Guardrails (NEVER Violate)
- [assert|emphatic] NEVER: lose agent state** - Persist agent progress to memory continuously [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: track swarm health** - Monitor all agent statuses in real-time [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: validate consensus** - Require 4/5 agreement for theater detection [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: skip theater audit** - Zero tolerance, any theater blocks merge [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: cleanup workers** - Terminate agents on completion/failure [ground:policy] [conf:0.98] [state:confirmed]

### Evidence-Based Validation
- **Check all agent statuses** - Verify each agent completed successfully
- **Validate parallel execution** - Confirm tasks ran concurrently, not sequentially
- **Measure speedup** - Calculate actual speedup vs sequential baseline
- **Audit theater detection** - Run 6-agent consensus, verify 0% detection
- **Verify integration** - Execute sandbox tests, confirm 100% pass rate


# Advanced Swarm Coordination SOP

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

This skill implements advanced swarm patterns with dynamic topology switching, self-organizing behaviors, and intelligent coordination for complex multi-agent systems. It enables sophisticated swarm orchestration with adaptive topology selection and performance optimization.

## Agents & Responsibilities

### hierarchical-coordinator
**Role:** Tree-based coordination with leader-follower patterns
**Responsibilities:**
- Manage hierarchical swarm structures
- Coordinate parent-child agent relationships
- Handle task delegation cascades
- Monitor hierarchy performance

### mesh-coordinator
**Role:** Peer-to-peer coordination with full connectivity
**Responsibilities:**
- Enable direct agent-to-agent communication
- Manage mesh network topology
- Coordinate distributed consensus
- Handle fault tolerance

### adaptive-coordinator
**Role:** Dynamic topology switching based on workload
**Responsibilities:**
- Analyze task complexity and requirements
- Switch topologies dynamically
- Optimize resource allocation
- Monitor and adapt to performance

## Phase 1

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
  pattern: "skills/workflow/when-using-advanced-swarm-use-swarm-advanced/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-using-advanced-swarm-use-swarm-advanced-{session_id}",
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

[commit|confident] <promise>WHEN_USING_ADVANCED_SWARM_USE_SWARM_ADVANCED_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
