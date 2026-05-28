/*============================================================================*/
/* WHEN-CHAINING-AGENT-PIPELINES-USE-STREAM-CHAIN SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-chaining-agent-pipelines-use-stream-chain
version: 1.0.0
description: |
  [assert|neutral] Chain agent outputs as inputs in sequential or parallel pipelines for data flow orchestration [ground:given] [conf:0.95] [state:confirmed]
category: workflow
tags:
- pipeline
- streaming
- data-flow
- chaining
- orchestration
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-chaining-agent-pipelines-use-stream-chain workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic workflow processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-chaining-agent-pipelines-use-stream-chain",
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
  keywords: ["when-chaining-agent-pipelines-use-stream-chain", "workflow", "workflow"],
  context: "user needs when-chaining-agent-pipelines-use-stream-chain capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

## Orchestration Skill Guidelines

### When to Use This Skill
- **Multi-agent coordination** requiring centralized orchestration
- **Complex workflows** with multiple dependent tasks
- **Parallel execution** benefiting from concurrent agent spawning
- **Quality-controlled delivery** needing validation and consensus
- **Production workflows** requiring audit trails and state management

### When NOT to Use This Skill
- **Single-agent tasks** with no coordination requirements
- **Simple sequential work** completing in <30 minutes
- **Trivial operations** with no quality gates
- **Exploratory work** not needing formal orchestration

### Success Criteria
- [assert|neutral] *All agents complete successfully** with 100% task completion [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Coordination overhead minimal** (<20% of total execution time) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *No orphaned agents** - All spawned agents tracked and terminated [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *State fully recoverable** - Can resume from any failure point [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] *Quality gates pass** - All validation checks successful [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases to Handle
- **Agent failures** - Detect and replace failed agents automatically
- **Timeout scenarios** - Configure per-agent timeout with escalation
- **Resource exhaustion** - Limit concurrent agents, queue excess work
- **Conflicting results** - Implement conflict resolution strategy
- **Partial completion** - Support incremental progress with rollback

### Guardrails (NEVER Violate)
- [assert|emphatic] NEVER: lose orchestration state** - Persist to memory after each phase [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: track all agents** - Maintain real-time agent registry [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: cleanup resources** - Terminate agents and free memory on completion [ground:policy] [conf:0.98] [state:confirmed]
- [assert|emphatic] NEVER: skip validation** - Run quality checks before marking complete [ground:policy] [conf:0.98] [state:confirmed]
- [assert|neutral] ALWAYS: handle errors** - Every orchestration step needs error handling [ground:policy] [conf:0.98] [state:confirmed]

### Evidence-Based Validation
- **Verify all agent outputs** - Check actual results vs expected contracts
- **Validate execution order** - Confirm dependencies respected
- **Measure performance** - Track execution time vs baseline
- **Check resource usage** - Monitor memory, CPU, network during execution
- **Audit state consistency** - Verify orchestration state matches reality


# Agent Pipeline Chaining SOP

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

This skill implements agent pipeline chaining where outputs from one agent become inputs to the next, supporting both sequential and parallel execution patterns with streaming data flows.

## Agents & Responsibilities

### task-orchestrator
**Role:** Pipeline coordination and orchestration
**Responsibilities:**
- Design pipeline architecture
- Connect agent stages
- Monitor data flow
- Handle pipeline errors

### memory-coordinator
**Role:** Data flow and state management
**Responsibilities:**
- Store intermediate results
- Coordinate data passing
- Manage pipeline state
- Ensure data consistency

## Phase 1: Design Pipeline

### Objective
Design pipeline architecture with stages, data flows, and execution strategy.

### Scripts

```bash
# Design pipeline architecture
npx claude-flow@alpha pipeline design \
  --stages "research,analyze,code,test,review" \
  --flow sequential \
  --output pipeline-design.json

# Define data flow
npx claude-flow@alpha pipeline dataflow \
  --design pipeline-design.json \
  --output data

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
  pattern: "skills/workflow/when-chaining-agent-pipelines-use-stream-chain/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-chaining-agent-pipelines-use-stream-chain-{session_id}",
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

[commit|confident] <promise>WHEN_CHAINING_AGENT_PIPELINES_USE_STREAM_CHAIN_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
