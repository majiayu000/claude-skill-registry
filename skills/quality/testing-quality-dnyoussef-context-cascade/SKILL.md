/*============================================================================*/
/* TESTING-QUALITY SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: testing-quality
version: 2.1.0
description: |
  [assert|neutral] Testing quality assessment for test suite health, coverage analysis, and test effectiveness. Use when auditing test quality, improving test coverage, or assessing test reliability and maintainability. [ground:given] [conf:0.95] [state:confirmed]
category: research
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute testing-quality workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic research processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "testing-quality",
  category: "research",
  version: "2.1.0",
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
  keywords: ["testing-quality", "research", "workflow"],
  context: "user needs testing-quality capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Testing Quality

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



Assessment and improvement of test suite quality, coverage, and effectiveness.

## Phase 0: Expertise Loading

```yaml
expertise_check:
  domain: testing-quality
  file: .claude/expertise/testing-quality.yaml

  if_exists:
    - Load quality metrics
    - Load coverage thresholds
    - Apply assessment criteria

  if_not_exists:
    - Flag discovery mode
    - Document patterns learned
```

## When to Use This Skill

Use testing-quality when:
- Auditing test suite health
- Analyzing test coverage gaps
- Assessing test reliability
- Improving test maintainability
- Identifying flaky tests

## Quality Dimensions

| Dimension | Metrics |
|-----------|---------|
| Coverage | Line, branch, function |
| Reliability | Flake rate, consistency |
| Speed | Execution time, parallelization |
| Maintainability | Complexity, duplication |

## Quality Metrics

### Coverage Analysis
```yaml
metrics:
  line_coverage: ">= 80%"
  branch_coverage: ">= 75%"
  function_coverage: ">= 80%"
  critical_path_coverage: "100%"
```

### Test Health
```yaml
metrics:
  flaky_test_rate: "< 1%"
  test_execution_time: "< 5 min"
  test_to_code_ratio: ">= 1:1"
  assertion_density: ">= 2 per test"
```

## Anti-Patterns

```yaml
anti_patterns:
  - Flaky tests (non-deterministic)
  - Test interdependence
  - Over-mocking
  - Missing assertions
  - Slow tests in CI
  - Commented-out tests
```

## MCP Requirements

- **claude-flow**: For orchestration
- **Bash**: For coverage tools

## Recursive Improvement Integration (v2.1)

### Eval Harness Integration

```yaml
benchmark: testing-quality-benchmark-v1
  tests:
    - tq-001: Coverage analysis accuracy
    - tq-002: Anti-pattern detection
  minimum_scores:
    analysis_accuracy: 0.90
    detection_rate: 0.85
```

### Memory Namespace

```yaml
namespaces:
  - testing-quality/audits/{id}: Quality audits
  - testing-quality/metrics: Health metrics
  - improvement/audits/testing-quality: Skill audits
```

### Uncertainty Handling

```yaml
confidence_check:
  if confidence >= 0.8:
    - Proceed with assessment
  if confidence 0.5-0.8:
    - Confirm scope
  if confidence < 0.5:
    - Ask for test suite details
```

### Cross-Skill Coordination

Works with: **testing**, **code-review-assistant**, **functionality-audit**

---

## !! SKILL COMPLETION VERIFICATION (MANDATORY) !!

- [ ] **Agent Spawning**: Spawned agent via Task()
- [ ] **Agent Registry Validation**: Agent from registry
- [ ] **TodoWrite Called**: Called with 5+ todos
- [ ] **Work Delegation**: Delegated to agents

**Remember: Skill() -> Task() -> TodoWrite() - ALWAYS**

## Core Principles

Testing Quality operates on 3 fundamental principles:

### Principle 1: Comprehensive Coverage Across Multiple Dimensions
Test quality is not just about line coverage percentage but about effectiveness across coverage, reliability, speed, and maintainability dimensions.

In practice:
- Line coverage measures which code is executed, but branch coverage ensures all decision paths are tested
- Function coverage validates all callable units are invoked, while critical path coverage ensures 100% validation of essential workflows
- Coverage metrics combined with assertion density ensure tests actually validate behavior, not just execute code
- Test-to-code ratio (>= 1:1) ensures adequate test investment relative to implementation complexity

### Principle 2: Test Reliability Through Determinism
Flaky tests that pass or fail non-deterministically erode confidence in the entire test suite and mask real failures.

In practice:
- Flaky test rate must be <1% with any non-deterministic tests immediately investigated and fixed
- Test isolation prevents interdependence where one test's side effects affect another's results
- Reproducible test environments (seeded random data, controlled timing) eliminate environmental variability
- Test execution monitoring tracks consistency over multiple 

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
  pattern: "skills/research/testing-quality/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "testing-quality-{session_id}",
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

[commit|confident] <promise>TESTING_QUALITY_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
