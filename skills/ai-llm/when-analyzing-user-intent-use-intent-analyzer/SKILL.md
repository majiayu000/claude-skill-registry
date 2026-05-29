/*============================================================================*/
/* WHEN-ANALYZING-USER-INTENT-USE-INTENT-ANALYZER SKILL :: VERILINGUA x VERIX EDITION                      */
/*============================================================================*/

---
name: when-analyzing-user-intent-use-intent-analyzer
version: 1.0.0
description: |
  [assert|neutral] Advanced intent interpretation system using cognitive science principles and probabilistic intent mapping [ground:given] [conf:0.95] [state:confirmed]
category: utilities
tags:
- intent-analysis
- cognitive-science
- disambiguation
- user-understanding
author: ruv
cognitive_frame:
  primary: honorific
  goal_analysis:
    first_order: "Execute when-analyzing-user-intent-use-intent-analyzer workflow"
    second_order: "Ensure quality and consistency"
    third_order: "Enable systematic utilities processes"
---

/*----------------------------------------------------------------------------*/
/* S0 META-IDENTITY                                                            */
/*----------------------------------------------------------------------------*/

[define|neutral] SKILL := {
  name: "when-analyzing-user-intent-use-intent-analyzer",
  category: "utilities",
  version: "1.0.0",
  layer: L1
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S1 COGNITIVE FRAME                                                          */
/*----------------------------------------------------------------------------*/

[define|neutral] COGNITIVE_FRAME := {
  frame: "Honorific",
  source: "Japanese",
  force: "Who is the audience?"
} [ground:cognitive-science] [conf:0.92] [state:confirmed]

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.

/*----------------------------------------------------------------------------*/
/* S2 TRIGGER CONDITIONS                                                       */
/*----------------------------------------------------------------------------*/

[define|neutral] TRIGGER_POSITIVE := {
  keywords: ["when-analyzing-user-intent-use-intent-analyzer", "utilities", "workflow"],
  context: "user needs when-analyzing-user-intent-use-intent-analyzer capability"
} [ground:given] [conf:1.0] [state:confirmed]

/*----------------------------------------------------------------------------*/
/* S3 CORE CONTENT                                                             */
/*----------------------------------------------------------------------------*/

# Intent Analyzer - Advanced User Intent Interpretation

## Kanitsal Cerceve (Evidential Frame Activation)
Kaynak dogrulama modu etkin.



## Overview

Advanced intent interpretation system that analyzes user requests using cognitive science principles and extrapolates logical volition. Use when user requests are ambiguous, when deeper understanding would improve response quality, or when helping users clarify what they truly need.

## When to Use This Skill

- User request is vague or ambiguous
- Multiple interpretations are possible
- High-stakes decision requires clarity
- User may not know exactly what they need
- Complex requirements need decomposition
- Implicit assumptions need surfacing

## Theoretical Foundation

### Cognitive Science Principles

1. **Probabilistic Intent Mapping**: Assign likelihood scores to possible interpretations
2. **First Principles Decomposition**: Break complex requests into fundamental components
3. **Socratic Clarification**: Ask targeted questions to narrow possibilities
4. **Context Integration**: Leverage environment and history for disambiguation
5. **Volition Extrapolation**: Infer underlying goals beyond stated request

### Evidence-Based Patterns

- **Self-Consistency**: Generate multiple interpretations and find consensus
- **Chain-of-Thought**: Trace reasoning from input to understanding
- **Program-of-Thought**: Structure analysis as executable logic
- **Plan-and-Solve**: Decompose understanding into steps

## Phase 1: Capture User Input

### Objective
Gather complete user request with full context

### Agent Coordination
```bash
# Pre-task hook
npx claude-flow@alpha hooks pre-task \
  --description "Capture user input for intent analysis" \
  --complexity "low" \
  --expected-duration "2min"

# Session restore
npx claude-flow@alpha hooks session-restore \
  --session-id "intent-analyzer-${TIMESTAMP}"
```

### Implementation

**Step 1.1: Extract Raw Input**
```javascript
const userInput = {
  request: "[User's exact words]",
  context: {
    environment: process.env,
    workingDirectory: process.cwd(),
    recentHistory: [] // Last 5 interactions
  },
  timestamp: new Date().toISOString()
};

// Store in memory
await memory.store('intent/raw-input', userInput);
```

**Step 1.2: Identify Input Characteristics**
```javascript
const characteristics = {
  length: userInput.request.split(' ').length,
  hasMultipleParts: /and|then|also|additionally/i.test(userInput.request),
  containsQuestions: /\?/.test(userInput.request),
  specificityScore: calculateSpecificity(userInput.request),
  domainIndicators: extractDomains(userInput.request)
};

await memory.store('intent/characteristics', characteristics);
```

**Step 1.3: Gather Context Clues**
```javascript
const contextClues = {
  fileSystem: await analyzeFileSystem(),
  recentEdits: await getRecentEdits(),
  projectType: await inferProjectType(),
  userExpertise: await estimateExpertiseLevel()
};

await memory.store('intent/context-clues', contextClues);
```

### Validation Criteria
- [ ] Complete user request captured
- [ ] Context information gathered
- [ ] Characteristics identified
- [ ] Memory storage confirmed

### Memory Pattern
```bash
# Store phase completion
npx claude-flow@alpha hooks post-edit \
  --file "memory://intent/raw-input" \
  --memory-key "intent-analyzer/phase1/completion"
```

## Phase 2: Decompose Intent

### Objective
Break down request into fundamental components using first principles

### Agent: Researcher

**Step 2.1: Tokenize Request**
```javascript
const tokens = {
  actions: extractActionVerbs(userInput.request),
  subjects: extractSubjects(userInput.request),
  constraints: extractConstraints(userInput.request),
  outcomes: extractDesiredOutcomes(userInput.request)
};

// Example output:
// {
//   actions: ['create', 'optimize', 'test'],
//   subjects: ['API', 'database', 'authentication'],
//   constraints: ['must be secure', 'under 100ms'],
//   outcomes: ['production-ready', 'scalable']
// }
```

*

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
  pattern: "skills/utilities/when-analyzing-user-intent-use-intent-analyzer/{project}/{timestamp}",
  store: ["executions", "decisions", "patterns"],
  retrieve: ["similar_tasks", "proven_patterns"]
} [ground:system-policy] [conf:1.0] [state:confirmed]

[define|neutral] MEMORY_TAGGING := {
  WHO: "when-analyzing-user-intent-use-intent-analyzer-{session_id}",
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

[commit|confident] <promise>WHEN_ANALYZING_USER_INTENT_USE_INTENT_ANALYZER_VERILINGUA_VERIX_COMPLIANT</promise> [ground:self-validation] [conf:0.99] [state:confirmed]
