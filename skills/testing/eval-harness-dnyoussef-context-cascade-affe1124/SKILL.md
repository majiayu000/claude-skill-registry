/*============================================================================*/
/* EVAL-HARNESS SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: eval-harness
version: 1.1.0
description: |
  [assert|neutral] Frozen evaluation harness that gates all self-improvement changes. Contains benchmark suites, regression tests, and human approval gates. Evaluates cognitive frame application and cross-lingual integr [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- evaluation
- benchmark
- regression
- frozen
- gate
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute eval-harness workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "eval-harness",
  category: "foundry",
  version: "1.1.0",
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
  keywords: ["eval-harness", "foundry", "workflow"],
  context: "user needs eval-harness capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Eval Harness (Frozen Evaluation)

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose

Gate ALL self-improvement changes with objective evaluation.

**CRITICAL**: This harness does NOT self-improve. It is manually maintained and expanded. This prevents Goodhart's Law (optimizing the metric instead of the outcome).

## Core Principle

> "A self-improvement loop is only as good as its evaluation harness."

Without frozen evaluation:
- Prettier prompts that are more confidently wrong
- Overfitting to "sounds good" instead of "works better"
- Compounding misalignment

---

## Benchmark Suites

### Suite 1: Prompt Generation Quality

**ID**: `prompt-generation-benchmark-v1`
**Purpose**: Evaluate quality of generated prompts

```yaml
benchmark:
  id: prompt-generation-benchmark-v1
  version: 1.0.0
  last_modified: "2025-12-15"
  frozen: true

  tasks:
    - id: "pg-001"
      name: "Simple Task Prompt"
      input: "Create a prompt for file reading"
      expected_qualities:
        - has_clear_action_verb
        - has_input_specification
        - has_output_specification
        - has_error_handling
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

    - id: "pg-002"
      name: "Complex Workflow Prompt"
      input: "Create a prompt for multi-step deployment"
      expected_qualities:
        - has_plan_and_solve_structure
        - has_validation_gates
        - has_rollback_instructions
        - has_success_criteria
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

    - id: "pg-003"
      name: "Analytical Task Prompt"
      input: "Create a prompt for code review"
      expected_qualities:
        - has_self_consistency_mechanism
        - has_multiple_perspectives
        - has_confidence_scoring
        - has_uncertainty_handling
      scoring:
        clarity: 0.0-1.0
        completeness: 0.0-1.0
        precision: 0.0-1.0

  minimum_passing:
    average_clarity: 0.7
    average_completeness: 0.7
    average_precision: 0.7
    required_qualities_hit_rate: 0.8
```

### Suite 2: Skill Generation Quality

**ID**: `skill-generation-benchmark-v1`
**Purpose**: Evaluate quality of generated skills

```yaml
benchmark:
  id: skill-generation-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "sg-001"
      name: "Micro-Skill Generation"
      input: "Create skill for JSON validation"
      expected_qualities:
        - has_single_responsibility
        - has_input_output_contract
        - has_error_handling
        - has_test_cases
      scoring:
        functionality: 0.0-1.0
        contract_compliance: 0.0-1.0
        error_coverage: 0.0-1.0

    - id: "sg-002"
      name: "Complex Skill Generation"
      input: "Create skill for API integration"
      expected_qualities:
        - has_phase_structure
        - has_validation_gates
        - has_logging
        - has_rollback
      scoring:
        functionality: 0.0-1.0
        structure_compliance: 0.0-1.0
        safety_coverage: 0.0-1.0

  minimum_passing:
    average_functionality: 0.75
    average_compliance: 0.8
    required_qualities_hit_rate: 0.85
```

### Suite 3: Expertise File Quality

**ID**: `expertise-generation-benchmark-v1`
**Purpose**: Evaluate quality of expertise files

```yaml
benchmark:
  id: expertise-generation-benchmark-v1
  version: 1.0.0
  frozen: true

  tasks:
    - id: "eg-001"
      name: "Domain Expertise Generation"
      input: "Create expertise for authentication domain"
      expected_qualities:
        - has_file_locations
        - has_falsifiable_patterns
        - has_validation_rules
        - has_known_issues_section
      scoring:
        falsifiability_coverage: 0.0-1.0
        pattern_precision: 0.0-1.0
        validation_completeness: 0.0-1.0

  minimum_passing:
    falsifiability_coverage: 0.8
    pattern_precision: 0.7
    validation_completeness: 0.75
```

### Suite 4: Cogniti

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
  pattern: "skills/foundry/eval-harness/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "eval-harness-{session_id}",
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

[commit|confident] <promise>EVAL_HARNESS_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
