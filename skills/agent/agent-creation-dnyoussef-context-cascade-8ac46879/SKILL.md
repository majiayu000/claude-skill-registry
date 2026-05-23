/*============================================================================*/
/* AGENT-CREATION SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: agent-creation
version: 1.0.0
description: |
  [assert|neutral] Systematic agent creation using evidence-based prompting principles and 4-phase SOP methodology. Use when creating new specialist agents, refining existing agent prompts, or designing multi-agent syst [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- foundry
- creation
- meta-tools
author: ruv
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute agent-creation workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "agent-creation",
  category: "foundry",
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
  keywords: ["agent-creation", "foundry", "workflow"],
  context: "user needs agent-creation capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

<!-- SKILL SOP IMPROVEMENT v1.0 -->
## Skill Execution Criteria

### When to Use This Skill
- Creating new specialist agents with domain-specific expertise
- Refining existing agent system prompts for better performance
- Designing multi-agent coordination systems
- Implementing role-based agent hierarchies
- Building production-ready agents with embedded domain knowledge

### When NOT to Use This Skill
- For simple one-off tasks that don't need agent specialization
- When existing agents already cover the required domain
- For casual conversational interactions without systematic requirements
- When the task is better suited for a slash command or micro-skill

### Success Criteria
- [assert|neutral] primary_outcome: "Production-ready agent with optimized system prompt, clear role definition, and validated performance" [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] quality_threshold: 0.9 [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- [assert|neutral] verification_method: "Agent successfully completes domain-specific tasks with consistent high-quality output, passes validation tests, and integrates with Claude Agent SDK" [ground:acceptance-criteria] [conf:0.90] [state:provisional]

### Edge Cases
- case: "Vague agent requirements"
  handling: "Use Phase 1 (Initial Analysis) to research domain, identify patterns, and clarify scope before proceeding"
- case: "Overlapping agent capabilities"
  handling: "Conduct agent registry search, identify gaps vs duplicates, propose consolidation or specialization"
- case: "Agent needs multiple conflicting personas"
  handling: "Decompose into multiple focused agents with clear coordination pattern"

### Skill Guardrails
NEVER:
  - "Create agents without deep domain research (skipping Phase 1 undermines quality)"
  - "Use generic prompts without evidence-based techniques (CoT, few-shot, role-based)"
  - "Skip validation testing (Phase 3) before considering agent production-ready"
  - "Create agents that duplicate existing registry agents without justification"
ALWAYS:
  - "Complete all 4 phases: Analysis -> Prompt Engineering -> Testing -> Integration"
  - "Apply evidence-based prompting: Chain-of-Thought for reasoning, few-shot for patterns, clear role definition"
  - "Validate with diverse test cases and measure against quality criteria"
  - "Document agent capabilities, limitations, and integration points"

### Evidence-Based Execution
self_consistency: "After agent creation, test with same task multiple times to verify consistent outputs and reasoning quality"
program_of_thought: "Decompose agent creation into: 1) Domain analysis, 2) Capability mapping, 3) Prompt architecture, 4) Test design, 5) Validation, 6) Integration"
plan_and_solve: "Plan: Research domain + identify capabilities -> Execute: Build prompts + test cases -> Verify: Multi-run consistency + edge case handling"
<!-- END SKILL SOP IMPROVEMENT -->

# Agent Creation - Systematic Agent Design

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Evidence-based agent creation following best practices for prompt engineering and agent specialization.

---

## When to Use This Skill

Use when creating new specialist agents for specific domains, refining existing agent capabilities, designing multi-agent coordination systems, or implementing role-based agent hierarchies.

---

## 4-Phase Agent Creation SOP

### Phase 1: Specification
- Define agent purpose and domain
- Identify core capabilities needed
- Determine input/output formats
- Specify quality criteria

**Tools**: Use `resources/scripts/generate_agent.sh` for automated generation

### Phase 2: Prompt Engineering
- Apply evidence-based prompting principles
- Use Chain-of-Thought for reasoning tasks
- Implement few-shot learning with examples (2-5 examples)
- Define role and persona clearly

**Reference**: See `references/prompting-principles.md` for detailed techniques

### Phase 3: Testing & Vali

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
  pattern: "skills/foundry/agent-creation/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "agent-creation-{session_id}",
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

[commit|confident] <promise>AGENT_CREATION_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
