/*============================================================================*/
/* META-LOOP-ORCHESTRATOR SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: meta-loop-orchestrator
version: 1.0.0
description: |
  [assert|neutral] Orchestrates the recursive self-improvement meta loop by coordinating foundry skills (agent-creator, skill-forge, prompt-forge) with Ralph Wiggum persistence loops. Use when running recursive improvem [ground:given] [conf:0.95] [state:confirmed]
category: orchestration
tags:
- orchestration
- meta-loop
- recursive-improvement
- foundry
- ralph-wiggum
author: Context Cascade
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute meta-loop-orchestrator workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic orchestration processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "meta-loop-orchestrator",
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
  keywords: ["meta-loop-orchestrator", "orchestration", "workflow"],
  context: "user needs meta-loop-orchestrator capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Meta Loop Orchestrator

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Orchestrates the recursive self-improvement pipeline by coordinating foundry skills with Ralph Wiggum persistence loops. This skill enables bounded self-improvement where skills, agents, and prompts can improve themselves while being gated by frozen eval harness validation.

## SKILL-SPECIFIC GUIDANCE

### When to Use This Skill

- Recursive improvement of foundry skills (agent-creator, skill-forge, prompt-forge)
- Self-improvement cycles on the plugin's own components
- Coordinating multiple foundry skills in a pipeline
- Running auditor validation on foundry outputs
- Executing eval harness gated improvement cycles

### When NOT to Use This Skill

- One-time skill/agent creation (use individual foundry skills directly)
- Tasks not involving self-improvement of plugin components
- Non-foundry skills (use cascade-orchestrator instead)
- Quick fixes without full validation cycle

### Success Criteria
- [assert|neutral] All nested Ralph loops complete within max iterations [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] All 4 auditors pass validation [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Eval harness shows improvement >= 0% (no regression) [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] Changes committed and monitoring initiated [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases

- If nested Ralph loop hits max iterations: Escalate to human
- If auditor fails repeatedly: Route back to foundry skill
- If eval harness regression detected: REJECT and rollback

### Critical Guardrails

NEVER:
- Modify eval harness code (FROZEN)
- Skip auditor validation
- Commit without eval harness pass
- Disable monitoring phase
- Bypass human gates for large changes (>500 lines)

ALWAYS:
- Run all 4 auditors in parallel
- Store all intermediate states in memory-mcp
- Maintain rollback capability
- Log all iterations for debugging

## Core Architecture

```
META-LOOP ORCHESTRATION FLOW
============================

INPUT: Task + Target + Foundry Skill
                |
                v
        +---------------+
        |   PREPARE     |
        |   - Parse     |
        |   - Load exp  |
        |   - Select    |
        +---------------+
                |
                v
    +=======================+
    |   EXECUTE (Ralph #1)  |
    |   Foundry skill runs  |
    |   until proposal ready|
    +=======================+
                |
                v
    +=======================+
    |  IMPLEMENT (Ralph #2) |
    |   Apply changes to    |
    |   target file(s)      |
    +=======================+
                |
                v
    +-------+-------+-------+-------+
    |       |       |       |       |
    v       v       v       v       v
  [R#3]   [R#4]   [R#5]   [R#6]   <- Parallel Ralph Loops
  Prompt  Skill   Expert  Output
  Audit   Audit   Audit   Audit
    |       |       |       |
    +-------+-------+-------+
                |
                v
    +=======================+
    |    EVAL (Ralph #7)    |
    |    Run eval harness   |
    |    Fix until pass     |
    +=======================+
                |
                v
        +---------------+
        |    COMPARE    |
        |   baseline vs |
        |   candidate   |
        +---------------+
                |
        +-------+-------+
        |               |
        v               v
     ACCEPT          REJECT
        |               |
        v               v
     COMMIT        LOG FAILURE
        |           (retry)
        v
    +=======================+
    |  MONITOR (Ralph #8)   |
    |    7-day watch        |
    +=======================+
        |
        v
     COMPLETE
```

## Phase Definitions

### Phase 1: PREPARE

```yaml
prepare:
  actions:
    - Parse task and target from input
    - Detect domain from target

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
  pattern: "skills/orchestration/meta-loop-orchestrator/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "meta-loop-orchestrator-{session_id}",
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

[commit|confident] <promise>META_LOOP_ORCHESTRATOR_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
