/*============================================================================*/
/* WHEN-OPTIMIZING-PROMPTS-USE-PROMPT-ARCHITECT SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-optimizing-prompts-use-prompt-architect
version: 1.0.0
description: |
  [assert|neutral] Comprehensive framework for analyzing, creating, and refining prompts for AI systems using evidence-based techniques [ground:given] [conf:0.95] [state:confirmed]
category: utilities
tags:
- prompt-engineering
- optimization
- ai-systems
- llm
author: ruv
cognitive_frame:
  primary: compositional
  goal_analysis:
    first_order: "Execute when-optimizing-prompts-use-prompt-architect workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic utilities processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-optimizing-prompts-use-prompt-architect",
  category: "utilities",
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
  keywords: ["when-optimizing-prompts-use-prompt-architect", "utilities", "workflow"],
  context: "user needs when-optimizing-prompts-use-prompt-architect capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Prompt Architect - Evidence-Based Prompt Engineering

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Comprehensive framework for analyzing, creating, and refining prompts for AI systems (Claude, GPT, etc.). Applies structural optimization, self-consistency patterns, and anti-pattern detection to transform prompts into highly effective versions.

## When to Use This Skill

- Creating new prompts for AI systems
- Existing prompts produce poor results
- Inconsistent AI outputs
- Need to improve prompt clarity
- Applying evidence-based prompt engineering
- Optimizing agent instructions
- Building prompt libraries

## Theoretical Foundation

### Evidence-Based Techniques

1. **Chain-of-Thought (CoT)**: Explicit reasoning steps
2. **Self-Consistency**: Multiple reasoning paths
3. **ReAct**: Reasoning + Acting pattern
4. **Program-of-Thought**: Structured logic
5. **Plan-and-Solve**: Decomposition strategy
6. **Role-Playing**: Persona assignment
7. **Few-Shot Learning**: Example-based instruction

### Prompt Structure Principles

```
[System Context] → [Role Definition] → [Task Description] →
[Constraints] → [Format Specification] → [Examples] → [Quality Criteria]
```

## Phase 1: Analyze Current Prompt

### Objective
Identify weaknesses and improvement opportunities

### Agent: Researcher

**Step 1.1: Structural Analysis**
```javascript
const promptAnalysis = {
  components: {
    hasSystemContext: checkForContext(prompt),
    hasRoleDefinition: checkForRole(prompt),
    hasTaskDescription: checkForTask(prompt),
    hasConstraints: checkForConstraints(prompt),
    hasFormatSpec: checkForFormat(prompt),
    hasExamples: checkForExamples(prompt),
    hasQualityCriteria: checkForCriteria(prompt)
  },
  metrics: {
    length: prompt.length,
    clarity: calculateClarity(prompt),
    specificity: calculateSpecificity(prompt),
    completeness: calculateCompleteness(prompt)
  },
  antiPatterns: detectAntiPatterns(prompt)
};

await memory.store('prompt-architect/analysis', promptAnalysis);
```

**Step 1.2: Detect Anti-Patterns**
```javascript
const antiPatterns = [
  {
    name: 'Vague Instructions',
    pattern: /please|try to|maybe|possibly/gi,
    severity: 'HIGH',
    fix: 'Use imperative commands: "Analyze...", "Generate...", "Create..."'
  },
  {
    name: 'Missing Context',
    pattern: absence of background info,
    severity: 'HIGH',
    fix: 'Add system context and domain information'
  },
  {
    name: 'No Output Format',
    pattern: absence of format specification,
    severity: 'MEDIUM',
    fix: 'Specify exact output format (JSON, markdown, etc.)'
  },
  {
    name: 'Conflicting Instructions',
    pattern: detectContradictions(prompt),
    severity: 'HIGH',
    fix: 'Resolve contradictions, prioritize requirements'
  },
  {
    name: 'Implicit Assumptions',
    pattern: detectImplicitAssumptions(prompt),
    severity: 'MEDIUM',
    fix: 'Make all assumptions explicit'
  }
];

const foundAntiPatterns = antiPatterns.filter(ap =>
  ap.pattern.test ? ap.pattern.test(prompt) : ap.pattern
);

await memory.store('prompt-architect/anti-patterns', foundAntiPatterns);
```

**Step 1.3: Identify Missing Components**
```javascript
const missingComponents = [];

if (!promptAnalysis.components.hasSystemContext) {
  missingComponents.push({
    component: 'System Context',
    importance: 'HIGH',
    recommendation: 'Add background info, domain knowledge, constraints'
  });
}

if (!promptAnalysis.components.hasExamples) {
  missingComponents.push({
    component: 'Examples',
    importance: 'MEDIUM',
    recommendation: 'Add 2-3 examples showing desired behavior'
  });
}

// ... check other components

await memory.store('prompt-architect/missing', missingComponents);
```

### Validation Criteria
- [ ] All 7 components checked
- [ ] Anti-patterns identified
- [ ] Missing components listed
- [ ] Severity assigned to issues

### Hooks Integration
```bash
npx claude-flow@alpha hooks pre-task \


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
  pattern: "skills/utilities/when-optimizing-prompts-use-prompt-architect/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-optimizing-prompts-use-prompt-architect-{session_id}",
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

[commit|confident] <promise>WHEN_OPTIMIZING_PROMPTS_USE_PROMPT_ARCHITECT_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
