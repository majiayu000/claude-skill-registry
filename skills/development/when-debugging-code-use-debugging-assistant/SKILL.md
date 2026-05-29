/*============================================================================*/
/* SKILL SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: SKILL
version: 1.0.0
description: |
  [assert|neutral] SKILL skill for delivery workflows [ground:given] [conf:0.95] [state:confirmed]
category: delivery
tags:
- general
author: system
cognitive_frame:
  primary: aspectual
  goal_analysis:
    first_order: "Execute SKILL workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic delivery processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "SKILL",
  category: "delivery",
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
  keywords: ["SKILL", "delivery", "workflow"],
  context: "user needs SKILL capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Debugging Assistant Skill

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Intelligent debugging workflow that systematically identifies symptoms, performs root cause analysis, generates fixes with explanations, validates solutions, and prevents regressions through comprehensive testing.

## Metadata

- **Skill ID:** `when-debugging-code-use-debugging-assistant`
- **Category:** Development/Debugging
- **Complexity:** HIGH
- **Agents Required:** coder, code-analyzer, tester
- **Prerequisites:** Access to codebase, error logs, test environment

## Trigger Conditions

Use this skill when encountering:
- Runtime errors or exceptions
- Unexpected behavior or incorrect output
- Performance degradation or memory leaks
- Race conditions or timing issues
- Integration failures
- Test failures requiring investigation

## 5-Phase Debugging Protocol (SOP)

### Phase 1: Symptom Identification

**Objective:** Gather comprehensive information about the issue

**Agent:** code-analyzer

**Actions:**
1. Collect error messages, stack traces, and logs
2. Document expected vs actual behavior
3. Identify reproduction steps
4. Determine scope and frequency of occurrence
5. Classify issue severity and impact

**Outputs:**
- Symptom report with complete context
- Reproduction steps (manual or automated)
- Environmental context (OS, runtime version, dependencies)
- Issue classification (bug, regression, edge case)

**Success Criteria:**
- Issue can be consistently reproduced
- All relevant context is documented
- Scope of impact is clearly defined

### Phase 2: Root Cause Analysis

**Objective:** Trace execution flow and identify the underlying cause

**Agent:** code-analyzer + coder

**Actions:**
1. Trace execution path from entry point to failure
2. Examine variable states and data transformations
3. Identify assumptions that may be violated
4. Check boundary conditions and edge cases
5. Review recent code changes that may have introduced the issue
6. Analyze dependencies and external system interactions

**Techniques:**
- Binary search debugging (narrow down location)
- Hypothesis-driven investigation
- Comparative analysis (working vs broken code paths)
- Temporal analysis (when did it start failing?)

**Outputs:**
- Root cause statement with evidence
- Affected code locations and line numbers
- Explanation of why the bug occurs
- Related issues or side effects

**Success Criteria:**
- Clear understanding of the mechanism causing the failure
- Reproducible test case that isolates the root cause
- Documented reasoning chain from symptom to cause

### Phase 3: Fix Generation

**Objective:** Develop and explain solution options

**Agent:** coder

**Actions:**
1. Generate 2-3 solution approaches
2. Evaluate trade-offs for each approach
3. Select optimal solution based on:
   - Correctness and completeness
   - Performance impact
   - Code maintainability
   - Risk of side effects
4. Implement the fix with clear comments
5. Document why this approach was chosen

**Fix Patterns:**
- **Null Safety:** Add null checks, use optional chaining
- **Race Conditions:** Add synchronization, use promises properly
- **Memory Leaks:** Clean up listeners, break circular references
- **Type Errors:** Add runtime validation, improve type definitions
- **Logic Errors:** Correct conditions, fix off-by-one errors

**Outputs:**
- Implemented fix with explanation
- Alternative approaches considered
- Potential side effects documented
- Migration notes if API changes

**Success Criteria:**
- Fix addresses root cause, not just symptoms
- Code is clean and maintainable
- No new issues introduced
- Clear explanation provided

### Phase 4: Validation Testing

**Objective:** Confirm the fix resolves the issue without breaking existing functionality

**Agent:** tester

**Actions:**
1. Create test case that reproduces original bug
2. Verify test fails before fix (proves test validity)
3. Apply fix and verify test passes
4. Run full re

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
  pattern: "skills/delivery/SKILL/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "SKILL-{session_id}",
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

[commit|confident] <promise>SKILL_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
