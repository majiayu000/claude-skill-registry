/*============================================================================*/
/* WHEN-MANAGING-TOKEN-BUDGET-USE-TOKEN-BUDGET-ADVISOR SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-managing-token-budget-use-token-budget-advisor
version: 1.0.0
description: |
  [assert|neutral] Proactive token budget management tool for assessing usage, analyzing task complexity, generating chunking strategies, and creating execution plans that stay within budget limits [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- meta-tool
- token-management
- budget-optimization
- task-planning
- chunking
author: ruv
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute when-managing-token-budget-use-token-budget-advisor workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-managing-token-budget-use-token-budget-advisor",
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
  keywords: ["when-managing-token-budget-use-token-budget-advisor", "foundry", "workflow"],
  context: "user needs when-managing-token-budget-use-token-budget-advisor capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

<!-- SKILL SOP IMPROVEMENT v1.0 -->
## Skill Execution Criteria

### When to Use This Skill
- [AUTO-EXTRACTED from skill description and content]
- [Task patterns this skill is optimized for]
- [Workflow contexts where this skill excels]

### When NOT to Use This Skill
- [Situations where alternative skills are better suited]
- [Anti-patterns that indicate wrong skill choice]
- [Edge cases this skill doesn't handle well]

### Success Criteria
- primary_outcome: "[SKILL-SPECIFIC measurable result based on skill purpose]"
- [assert|neutral] quality_threshold: 0.85 [ground:acceptance-criteria] [conf:0.90] [state:provisional]
- verification_method: "[How to validate skill executed correctly and produced expected outcome]"

### Edge Cases
- case: "Ambiguous or incomplete input"
  handling: "Request clarification, document assumptions, proceed with explicit constraints"
- case: "Conflicting requirements or constraints"
  handling: "Surface conflict to user, propose resolution options, document trade-offs"
- case: "Insufficient context for quality execution"
  handling: "Flag missing information, provide template for needed context, proceed with documented limitations"

### Skill Guardrails
NEVER:
  - "[SKILL-SPECIFIC anti-pattern that breaks methodology]"
  - "[Common mistake that degrades output quality]"
  - "[Shortcut that compromises skill effectiveness]"
ALWAYS:
  - "[SKILL-SPECIFIC requirement for successful execution]"
  - "[Critical step that must not be skipped]"
  - "[Quality check that ensures reliable output]"

### Evidence-Based Execution
self_consistency: "After completing this skill, verify output quality by [SKILL-SPECIFIC validation approach]"
program_of_thought: "Decompose this skill execution into: [SKILL-SPECIFIC sequential steps]"
plan_and_solve: "Plan: [SKILL-SPECIFIC planning phase] -> Execute: [SKILL-SPECIFIC execution phase] -> Verify: [SKILL-SPECIFIC verification phase]"
<!-- END SKILL SOP IMPROVEMENT -->

# Token Budget Advisor

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



**Purpose:** Proactively manage token budgets by analyzing current usage, estimating task complexity, generating intelligent chunking strategies, prioritizing work, and creating step-by-step execution plans that stay within budget limits.

## When to Use This Skill

- Before starting large or complex tasks
- When approaching token budget limits
- During multi-phase project planning
- When tasks fail due to token exhaustion
- For optimizing resource allocation
- When coordinating multiple agents

## Analysis Dimensions

### 1. Budget Assessment
- Current token usage vs. limits
- Remaining budget calculation
- Historical usage patterns
- Projected usage for pending tasks
- Buffer allocation for safety

### 2. Task Complexity Analysis
- Token estimation by task type
- Agent requirements and costs
- Integration complexity
- Testing overhead
- Documentation needs

### 3. Chunking Strategy
- Logical task boundaries
- Dependency analysis
- Chunk size optimization
- Inter-chunk communication
- State management between chunks

### 4. Priority Optimization
- Critical path identification
- Value vs. cost analysis
- Risk assessment
- Quick wins identification
- Deferrable work detection

### 5. Execution Planning
- Step-by-step task sequence
- Budget tracking per step
- Checkpoint planning
- Rollback strategies
- Progress monitoring

## Execution Process

### Phase 1: Budget Assessment

```bash
# Initialize budget analysis
npx claude-flow@alpha hooks pre-task --description "Analyzing token budget"

# Retrieve current usage
npx claude-flow@alpha memory retrieve --key "token-usage/current"
```

**Budget Calculation:**
```javascript
function assessBudget(tokenLimit = 200000) {
  const usage = {
    limit: tokenLimit,
    used: getCurrentTokenUsage(),
    remaining: 0,
    buffer: 0,
    available: 0,
    status: "unknown"
  };

  usage.remaining = usage.limit - usage.used;
  usage.buffer = Math.floor(usage.limit * 0

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
  pattern: "skills/foundry/when-managing-token-budget-use-token-budget-advisor/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-managing-token-budget-use-token-budget-advisor-{session_id}",
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

[commit|confident] <promise>WHEN_MANAGING_TOKEN_BUDGET_USE_TOKEN_BUDGET_ADVISOR_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
