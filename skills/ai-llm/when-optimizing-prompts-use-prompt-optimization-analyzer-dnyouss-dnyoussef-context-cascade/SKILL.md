/*============================================================================*/
/* WHEN-OPTIMIZING-PROMPTS-USE-PROMPT-OPTIMIZATION-ANALYZER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-optimizing-prompts-use-prompt-optimization-analyzer
version: 1.0.0
description: |
  [assert|neutral] Active diagnostic tool for analyzing prompt quality, detecting anti-patterns, identifying token waste, and providing optimization recommendations [ground:given] [conf:0.95] [state:confirmed]
category: foundry
tags:
- meta-tool
- prompt-engineering
- optimization
- analysis
- diagnostics
author: ruv
cognitive_frame:
  primary: evidential
  goal_analysis:
    first_order: "Execute when-optimizing-prompts-use-prompt-optimization-analyzer workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic foundry processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-optimizing-prompts-use-prompt-optimization-analyzer",
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
  keywords: ["when-optimizing-prompts-use-prompt-optimization-analyzer", "foundry", "workflow"],
  context: "user needs when-optimizing-prompts-use-prompt-optimization-analyzer capability"
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

# Prompt Optimization Analyzer

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



**Purpose:** Analyze prompt quality and provide actionable optimization recommendations to reduce token waste, improve clarity, and enhance effectiveness.

## When to Use This Skill

- Before publishing new skills or slash commands
- When prompts exceed token budgets
- When responses are inconsistent or unclear
- During skill maintenance and refinement
- When analyzing existing prompt libraries

## Analysis Dimensions

### 1. Token Efficiency Analysis
- Redundancy detection (repeated concepts, phrases)
- Verbosity measurement (word count vs. information density)
- Compression opportunities (equivalent shorter forms)
- Example bloat (excessive or redundant examples)

### 2. Anti-Pattern Detection
- Vague instructions ("do something good")
- Ambiguous terminology (undefined jargon)
- Conflicting requirements (contradictory rules)
- Missing context (insufficient background)
- Over-specification (unnecessary constraints)

### 3. Trigger Issue Analysis
- Unclear activation conditions
- Overlapping trigger patterns
- Missing edge cases
- Too broad/narrow scope

### 4. Structural Optimization
- Information architecture (logical flow)
- Section organization (grouping, hierarchy)
- Reference efficiency (cross-references, links)
- Progressive disclosure (layered detail)

## Execution Process

### Phase 1: Token Waste Detection

```bash
# Analyze prompt for redundancy
npx claude-flow@alpha hooks pre-task --description "Analyzing prompt for token waste"

# Store original metrics
npx claude-flow@alpha memory store --key "optimization/original-tokens" --value "{
  \"total_tokens\": <count>,
  \"redundancy_score\": <0-100>,
  \"verbosity_score\": <0-100>
}"
```

**Analysis Script:**
```javascript
// Embedded token analysis
function analyzeTokenWaste(promptText) {
  const metrics = {
    totalWords: promptText.split(/\s+/).length,
    totalChars: promptText.length,
    redundancyScore: 0,
    verbosityScore: 

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
  pattern: "skills/foundry/when-optimizing-prompts-use-prompt-optimization-analyzer/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-optimizing-prompts-use-prompt-optimization-analyzer-{session_id}",
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

[commit|confident] <promise>WHEN_OPTIMIZING_PROMPTS_USE_PROMPT_OPTIMIZATION_ANALYZER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
