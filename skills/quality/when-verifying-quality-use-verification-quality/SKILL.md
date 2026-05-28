/*============================================================================*/
/* WHEN-VERIFYING-QUALITY-USE-VERIFICATION-QUALITY SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-verifying-quality-use-verification-quality
version: 1.0.0
description: |
  [assert|neutral] Comprehensive quality verification and validation through static analysis, dynamic testing, integration validation, and certification gates [ground:given] [conf:0.95] [state:confirmed]
category: testing-quality
tags:
- general
author: system
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-verifying-quality-use-verification-quality workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic testing-quality processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-verifying-quality-use-verification-quality",
  category: "testing-quality",
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
  keywords: ["when-verifying-quality-use-verification-quality", "testing-quality", "workflow"],
  context: "user needs when-verifying-quality-use-verification-quality capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Quality Verification and Validation

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Purpose

Execute comprehensive quality verification across static analysis, dynamic testing, integration validation, and certification gates to ensure code meets production standards with measurable quality metrics and approval documentation.

## MCP Requirements

This skill operates using Claude Code's built-in tools only. No additional MCP servers required.

All verification features (static analysis, testing, validation gates, audit trails) use native Claude Flow commands and built-in quality tools.

## Core Principles

- **Multi-Dimensional Quality**: Static + dynamic + integration + certification
- **Evidence-Based**: Measurable quality metrics with objective thresholds
- **Automated Gates**: Validation checkpoints with pass/fail criteria
- **Audit Trail**: Complete documentation for compliance and certification
- **Continuous Validation**: Quality checks at every stage of development

## Phase 1: Static Analysis

### Objective
Analyze code quality, maintainability, complexity, and adherence to standards without execution.

### Agent Configuration
```yaml
agent: code-analyzer
specialization: static-analysis
tools: SonarQube, ESLint, TypeScript
```

### Execution Steps

**1. Initialize Static Analysis**
```bash
# Pre-task setup
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-analyzer" \
  --description "Static code quality analysis" \
  --task-type "static-analysis"

# Restore session context
npx claude-flow@alpha hooks session-restore \
  --session-id "quality-verification-${BUILD_ID}" \
  --agent-id "code-analyzer"
```

**2. Code Quality Metrics**
```bash
# SonarQube analysis
sonar-scanner \
  -Dsonar.projectKey=${PROJECT_KEY} \
  -Dsonar.sources=./src \
  -Dsonar.host.url=${SONAR_URL} \
  -Dsonar.login=${SONAR_TOKEN}

# ESLint quality scan
npx eslint . --format json --output-file eslint-report.json

# TypeScript type checking
npx tsc --noEmit --pretty false 2> typescript-errors.txt
```

**3. Complexity Analysis**
```javascript
// McCabe cyclomatic complexity
const complexityMetrics = {
  max_complexity: 10,        // Threshold
  high_complexity_files: [], // Functions with complexity >10
  average_complexity: 0,     // Project average

  // Cognitive complexity (Sonar)
  max_cognitive_complexity: 15,
  high_cognitive_files: []
};

// Analyze each function
function analyzeComplexity(ast) {
  const metrics = {
    cyclomatic: calculateCyclomaticComplexity(ast),
    cognitive: calculateCognitiveComplexity(ast),
    nesting_depth: calculateNestingDepth(ast),
    halstead: calculateHalsteadMetrics(ast)
  };

  return metrics;
}
```

**4. Maintainability Index**
```javascript
// Maintainability Index = 171 - 5.2*ln(V) - 0.23*G - 16.2*ln(L)
// V = Halstead Volume
// G = Cyclomatic Complexity
// L = Lines of Code

const maintainabilityMetrics = {
  project_score: 0,          // 0-100
  high_risk_files: [],       // Score <20 (red)
  medium_risk_files: [],     // Score 20-50 (yellow)
  maintainable_files: []     // Score >50 (green)
};
```

**5. Code Duplication Detection**
```bash
# Run jscpd for copy-paste detection
npx jscpd ./src --format json --output ./jscpd-report.json

# Analyze duplication
# Threshold: <5% duplication
```

**6. Generate Static Analysis Report**
```markdown
## Static Analysis Results

### Code Quality Metrics
| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Maintainability Index | 67.3 | >65 | ✅ PASS |
| Cyclomatic Complexity | 8.2 | <10 | ✅ PASS |
| Cognitive Complexity | 12.4 | <15 | ✅ PASS |
| Code Duplication | 3.8% | <5% | ✅ PASS |
| Technical Debt Ratio | 2.1% | <5% | ✅ PASS |

### High Complexity Files (Refactoring Candidates)
- `src/api/order-processor.js` - Complexity: 18 (⚠️ Threshold: 10)
- `src/utils/data-transformer.js` - Complexity: 14 (⚠️ Threshold: 10)

### Code Smells
- **67 code smells detected**
  - 12 Bloater (long methods

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
  pattern: "skills/testing-quality/when-verifying-quality-use-verification-quality/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-verifying-quality-use-verification-quality-{session_id}",
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

[commit|confident] <promise>WHEN_VERIFYING_QUALITY_USE_VERIFICATION_QUALITY_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
