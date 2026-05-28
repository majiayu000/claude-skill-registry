/*============================================================================*/
/* PLAYBOOK-ARCHITECT SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: playbook-architect
version: 1.0.0
description: |
  [assert|neutral] Comprehensive framework for creating, analyzing, and optimizing playbooks that orchestrate skill sequences. Use when creating new playbooks, improving existing playbook workflows, or applying evidence [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- foundry
- creation
- meta-tools
- orchestration
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute playbook-architect workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "playbook-architect",
  category: "foundry",
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
  keywords: ["playbook-architect", "foundry", "workflow"],
  context: "user needs playbook-architect capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

<!-- SKILL SOP IMPROVEMENT v1.0 -->
## Skill Execution Criteria

### When to Use This Skill
- Creating new playbooks for recurring workflow patterns
- Improving existing playbooks with inconsistent or suboptimal routing
- Building playbook libraries for team standardization
- Optimizing high-stakes workflows where execution order impacts outcomes
- Debugging why playbooks aren't producing expected results
- Adding new categories of playbooks (gap analysis)
- Consolidating overlapping playbooks

### When NOT to Use This Skill
- For single-skill invocations (use skill directly)
- When existing playbook already covers the workflow optimally
- For one-off tasks without reuse value
- When task is purely conversational without orchestration needs

### Success Criteria
- [assert|neutral] primary_outcome: "Optimized playbook with clear trigger conditions, correct skill sequencing, proper dependency handling, and maximized parallelization" [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] quality_threshold: 0.92 [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] verification_method: "Playbook executes successfully across diverse test cases, routes correctly based on intent keywords, and achieves stated success metrics" [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases
- case: "Overlapping trigger keywords with existing playbooks"
  handling: "Apply MECE analysis to disambiguate, add priority weights or more specific keywords"
- case: "Circular dependencies between skills in sequence"
  handling: "Detect cycles, restructure into DAG (Directed Acyclic Graph), split if necessary"
- case: "Missing MCP requirements for skill execution"
  handling: "Add mcp_requirements section, validate MCPs are available before routing"

### Skill Guardrails
NEVER:
  - "Create playbooks without validating skill availability (skills must exist in registry)"
  - "Sequence skills with unmet dependencies (prerequisites must complete before dependents)"
  - "Skip parallelization analysis (concurrent execution is 2-8x faster)"
  - "Duplicate existing playbooks without clear differentiation"
  - "Create playbooks with vague trigger conditions (keywords must be specific)"
ALWAYS:
  - "Validate all skills in sequence exist in skills/ directory"
  - "Apply dependency analysis to identify sequential vs parallel phases"
  - "Include success criteria with measurable metrics"
  - "Document MCP requirements for each playbook"
  - "Add fallback skills for critical steps"

### Evidence-Based Execution
self_consistency: "After playbook creation, trace execution path with multiple test intents to verify consistent routing and skill activation"
program_of_thought: "Decompose playbook design into: 1) Intent analysis, 2) Skill mapping, 3) Dependency detection, 4) Parallelization optimization, 5) MCP requirements, 6) Success criteria definition"
plan_and_solve: "Plan: Analyze workflow requirements -> Execute: Design skill sequence with dependencies -> Verify: Test with diverse trigger conditions + edge cases"
<!-- END SKILL SOP IMPROVEMENT -->

# Playbook Architect - META-PLAYBOOK Creation Framework

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



A comprehensive framework for creating, analyzing, and optimizing playbooks that orchestrate skill sequences. This skill applies the same evidence-based methodology used in prompt-architect and agent-creator to the playbook layer of the system.

## Overview

Playbooks are **orchestrated sequences of skills** that execute in response to specific user intents. Unlike individual skills (which do ONE thing well), playbooks coordinate MULTIPLE skills to accomplish complex workflows.

The Playbook Architect provides systematic methods to:
- Create new playbooks with proper structure and routing
- Analyze existing playbooks for optimization opportunities
- Apply evidence-based orchestration patterns
- Maximize parallelizatio

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
  pattern: "skills/foundry/playbook-architect/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "playbook-architect-{session_id}",
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

[commit|confident] <promise>PLAYBOOK_ARCHITECT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
