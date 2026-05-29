---
name: when-analyzing-user-intent-use-intent-analyzer
version: 1.0.0
description: Advanced intent interpretation system using cognitive science principles and probabilistic intent mapping
category: utilities
tags: [intent-analysis, cognitive-science, disambiguation, user-understanding]
agents: [researcher, analyst, planner]
difficulty: intermediate
estimated_duration: 15-30min
success_criteria:
  - Clear understanding of user intent achieved
  - Ambiguities resolved through targeted questions
  - Actionable task definition created
  - User confirmation obtained
validation_method: user_confirmation
dependencies:
  - claude-flow@alpha
  - hooks-integration
prerequisites:
  - User request captured
  - Context information available
outputs:
  - Interpreted intent document
  - Clarifying questions (if needed)
  - Action plan
triggers:
  - Ambiguous user requests
  - Complex multi-part instructions
  - Vague or unclear requirements
---

# Intent Analyzer - Advanced User Intent Interpretation

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

**Step 2.2: Build Component Tree**
```javascript
const componentTree = {
  primary: {
    intent: inferPrimaryIntent(tokens),
    confidence: 0.85
  },
  secondary: tokens.actions.slice(1).map(action => ({
    intent: action,
    confidence: 0.60
  })),
  implicit: inferImplicitRequirements(tokens, contextClues)
};

await memory.store('intent/component-tree', componentTree);
```

**Step 2.3: Identify Dependencies**
```javascript
const dependencies = {
  sequential: findSequentialDeps(componentTree),
  parallel: findParallelDeps(componentTree),
  conditional: findConditionalDeps(componentTree)
};

// Example:
// {
//   sequential: ['database schema' -> 'API endpoints' -> 'tests'],
//   parallel: ['frontend', 'backend'],
//   conditional: ['if authentication: setup OAuth']
// }
```

### Validation Criteria
- [ ] All action verbs identified
- [ ] Component tree constructed
- [ ] Dependencies mapped
- [ ] Implicit requirements surfaced

### Script Template
```bash
#!/bin/bash
# decompose-intent.sh

INPUT_FILE="$1"
OUTPUT_FILE="$2"

# Read user input
USER_REQUEST=$(cat "$INPUT_FILE")

# Decompose using researcher agent
npx claude-flow@alpha agent-spawn \
  --type researcher \
  --task "Decompose this request into components: $USER_REQUEST" \
  --output "$OUTPUT_FILE"

# Store results
npx claude-flow@alpha hooks post-edit \
  --file "$OUTPUT_FILE" \
  --memory-key "intent-analyzer/decomposition"
```

## Phase 3: Map Probabilities

### Objective
Assign likelihood scores to possible interpretations

### Agent: Analyst

**Step 3.1: Generate Interpretation Candidates**
```javascript
const interpretations = [
  {
    id: 'interp-1',
    description: 'User wants a complete REST API with authentication',
    probability: 0.75,
    evidence: ['mentions API', 'security constraint'],
    assumptions: ['Express.js framework', 'JWT auth']
  },
  {
    id: 'interp-2',
    description: 'User wants to add auth to existing API',
    probability: 0.20,
    evidence: ['existing project detected'],
    assumptions: ['API already exists']
  },
  {
    id: 'interp-3',
    description: 'User wants auth documentation/research',
    probability: 0.05,
    evidence: ['vague phrasing'],
    assumptions: ['exploratory phase']
  }
];

await memory.store('intent/interpretations', interpretations);
```

**Step 3.2: Apply Bayesian Reasoning**
```javascript
function updateProbabilities(interpretations, newEvidence) {
  return interpretations.map(interp => {
    const priorProb = interp.probability;
    const likelihoodGivenEvidence = calculateLikelihood(interp, newEvidence);
    const posteriorProb = (priorProb * likelihoodGivenEvidence) /
                          calculateNormalization(interpretations, newEvidence);

    return { ...interp, probability: posteriorProb };
  });
}

const updatedInterpretations = updateProbabilities(interpretations, contextClues);
```

**Step 3.3: Rank by Confidence**
```javascript
const rankedInterpretations = updatedInterpretations
  .sort((a, b) => b.probability - a.probability)
  .map((interp, index) => ({
    ...interp,
    rank: index + 1,
    confidenceLevel: interp.probability > 0.8 ? 'HIGH' :
                     interp.probability > 0.5 ? 'MEDIUM' : 'LOW'
  }));

await memory.store('intent/ranked-interpretations', rankedInterpretations);
```

### Validation Criteria
- [ ] At least 3 interpretations generated
- [ ] Probabilities sum to ~1.0
- [ ] Evidence listed for each interpretation
- [ ] Confidence levels assigned

### Memory Pattern
```bash
# Store probability analysis
npx claude-flow@alpha hooks post-task \
  --task-id "probability-mapping" \
  --metrics '{"interpretations": 3, "top_confidence": 0.75}'
```

## Phase 4: Clarify Ambiguities

### Objective
Ask targeted questions to resolve uncertainty

### Agent: Planner

**Step 4.1: Identify Decision Points**
```javascript
const ambiguities = rankedInterpretations.flatMap(interp => {
  if (interp.probability < 0.8 && interp.rank <= 2) {
    return interp.assumptions.map(assumption => ({
      interpretation: interp.id,
      assumption: assumption,
      impact: calculateImpact(assumption),
      question: generateClarifyingQuestion(assumption)
    }));
  }
  return [];
});

// Example output:
// {
//   interpretation: 'interp-1',
//   assumption: 'Express.js framework',
//   impact: 'HIGH',
//   question: 'Which framework would you prefer: Express.js, Fastify, or NestJS?'
// }
```

**Step 4.2: Prioritize Questions**
```javascript
const prioritizedQuestions = ambiguities
  .sort((a, b) => {
    // Sort by: HIGH impact first, then by interpretation probability
    if (a.impact !== b.impact) {
      return b.impact === 'HIGH' ? 1 : -1;
    }
    const interpA = rankedInterpretations.find(i => i.id === a.interpretation);
    const interpB = rankedInterpretations.find(i => i.id === b.interpretation);
    return interpB.probability - interpA.probability;
  })
  .slice(0, 3); // Max 3 questions to avoid overwhelming user

await memory.store('intent/questions', prioritizedQuestions);
```

**Step 4.3: Format Questions for User**
```javascript
const questionSet = {
  header: `I want to make sure I understand your request correctly. Can you clarify:`,
  questions: prioritizedQuestions.map((q, i) => ({
    number: i + 1,
    text: q.question,
    options: generateOptions(q.assumption),
    rationale: `This helps determine: ${q.impact.toLowerCase()} impact on ${q.interpretation}`
  })),
  footer: `These clarifications will help me provide exactly what you need.`
};

// Present to user
console.log(formatQuestionSet(questionSet));
```

**Step 4.4: Process User Responses**
```javascript
async function processResponses(responses) {
  // Update interpretation probabilities based on answers
  const refinedInterpretations = rankedInterpretations.map(interp => {
    let newProb = interp.probability;

    responses.forEach(response => {
      if (response.confirmsAssumption(interp)) {
        newProb *= 1.5; // Boost probability
      } else if (response.contradicsAssumption(interp)) {
        newProb *= 0.3; // Reduce probability
      }
    });

    return { ...interp, probability: newProb };
  });

  // Re-normalize probabilities
  const total = refinedInterpretations.reduce((sum, i) => sum + i.probability, 0);
  const normalized = refinedInterpretations.map(i => ({
    ...i,
    probability: i.probability / total
  }));

  await memory.store('intent/refined-interpretations', normalized);
  return normalized;
}
```

### Validation Criteria
- [ ] High-impact ambiguities identified
- [ ] Questions prioritized effectively
- [ ] User responses processed
- [ ] Probabilities updated

### Script Template
```bash
#!/bin/bash
# clarify-ambiguities.sh

INTERPRETATIONS_FILE="$1"

# Generate clarifying questions
QUESTIONS=$(npx claude-flow@alpha agent-spawn \
  --type planner \
  --task "Generate clarifying questions from: $(cat $INTERPRETATIONS_FILE)")

# Present to user (interactive)
echo "$QUESTIONS"
echo ""
echo "Your responses:"
read -p "1. " RESPONSE_1
read -p "2. " RESPONSE_2
read -p "3. " RESPONSE_3

# Store responses
cat > responses.json <<EOF
{
  "responses": [
    {"question": 1, "answer": "$RESPONSE_1"},
    {"question": 2, "answer": "$RESPONSE_2"},
    {"question": 3, "answer": "$RESPONSE_3"}
  ],
  "timestamp": "$(date -Iseconds)"
}
EOF

npx claude-flow@alpha hooks post-edit \
  --file "responses.json" \
  --memory-key "intent-analyzer/user-responses"
```

## Phase 5: Synthesize Understanding

### Objective
Form clear, actionable interpretation with user confirmation

### Agent: Analyst + Planner

**Step 5.1: Select Final Interpretation**
```javascript
const finalInterpretation = refinedInterpretations
  .sort((a, b) => b.probability - a.probability)[0];

const synthesis = {
  understanding: finalInterpretation.description,
  confidence: finalInterpretation.probability,
  breakdown: {
    primaryGoal: extractPrimaryGoal(finalInterpretation),
    subTasks: extractSubTasks(finalInterpretation),
    constraints: finalInterpretation.evidence,
    assumptions: finalInterpretation.assumptions
  },
  actionPlan: generateActionPlan(finalInterpretation)
};

await memory.store('intent/final-synthesis', synthesis);
```

**Step 5.2: Generate Confirmation Statement**
```javascript
const confirmation = {
  summary: `Based on your input, I understand you want to: ${synthesis.understanding}`,
  details: {
    scope: synthesis.breakdown.primaryGoal,
    approach: synthesis.actionPlan.strategy,
    deliverables: synthesis.actionPlan.outputs
  },
  confidence: `I'm ${(synthesis.confidence * 100).toFixed(0)}% confident in this interpretation.`,
  verification: `Does this match your expectations? If not, please let me know what I misunderstood.`
};

// Present to user
console.log(formatConfirmation(confirmation));
```

**Step 5.3: Create Execution Brief**
```javascript
const executionBrief = {
  metadata: {
    skillName: 'intent-analyzer',
    timestamp: new Date().toISOString(),
    confidence: synthesis.confidence
  },
  userIntent: {
    original: userInput.request,
    interpreted: synthesis.understanding,
    clarifications: questionSet.questions.length
  },
  actionPlan: {
    phases: synthesis.actionPlan.phases,
    agents: synthesis.actionPlan.requiredAgents,
    estimatedDuration: synthesis.actionPlan.duration,
    dependencies: synthesis.actionPlan.dependencies
  },
  successCriteria: synthesis.actionPlan.successCriteria,
  riskFactors: identifyRisks(synthesis)
};

await memory.store('intent/execution-brief', executionBrief);

// Export for next workflow
await fs.writeFile(
  '/tmp/intent-analysis-result.json',
  JSON.stringify(executionBrief, null, 2)
);
```

**Step 5.4: Handoff to Execution**
```javascript
// If confidence is high, prepare for immediate execution
if (synthesis.confidence > 0.85) {
  console.log('\n✅ High confidence understanding achieved.');
  console.log('Ready to proceed with execution.');

  // Generate TodoWrite for execution phase
  const todos = executionBrief.actionPlan.phases.map((phase, i) => ({
    id: `exec-${i + 1}`,
    content: phase.description,
    status: i === 0 ? 'in_progress' : 'pending',
    activeForm: phase.activeDescription,
    priority: phase.priority,
    agent: phase.assignedAgent
  }));

  // Output todos for execution
  console.log('\nGenerated execution plan:');
  console.log(JSON.stringify(todos, null, 2));
} else {
  console.log('\n⚠️  Confidence below threshold. Recommend additional clarification.');
}
```

### Validation Criteria
- [ ] Final interpretation selected (confidence > 0.8)
- [ ] User confirmation obtained
- [ ] Execution brief created
- [ ] Handoff to next workflow prepared

### Memory Pattern
```bash
# Session completion
npx claude-flow@alpha hooks session-end \
  --session-id "intent-analyzer-${TIMESTAMP}" \
  --export-metrics true \
  --summary "Intent analysis completed with ${CONFIDENCE}% confidence"

# Store final results
npx claude-flow@alpha hooks post-task \
  --task-id "intent-synthesis" \
  --output "/tmp/intent-analysis-result.json"
```

## Success Metrics

### Quantitative
- Interpretation confidence score > 0.8
- Number of clarifying questions asked < 5
- User confirmation obtained: YES/NO
- Time to resolution < 30 minutes

### Qualitative
- User expresses satisfaction with understanding
- No major revisions needed after confirmation
- Action plan is clear and executable
- Ambiguities resolved effectively

## Common Patterns

### Pattern 1: Multi-Part Request
```javascript
// When user request has multiple independent goals
if (componentTree.primary.length > 1) {
  // Decompose into separate intent analyses
  const subIntents = componentTree.primary.map(async (component) => {
    return await analyzeIntent(component, contextClues);
  });

  // Synthesize into coordinated plan
  const coordinatedPlan = synthesizeMultiIntent(await Promise.all(subIntents));
}
```

### Pattern 2: Vague Request
```javascript
// When specificity score is low
if (characteristics.specificityScore < 0.4) {
  // Use more Socratic questioning
  const questions = generateOpenEndedQuestions(userInput);

  // Iterate until specificity improves
  while (getCurrentSpecificity() < 0.6) {
    const response = await askUser(questions.shift());
    updateInterpretations(response);
  }
}
```

### Pattern 3: Expert User
```javascript
// When user expertise level is high
if (contextClues.userExpertise === 'expert') {
  // Skip basic clarifications
  const technicalInterpretations = interpretations.filter(
    i => i.technicalDepth === 'advanced'
  );

  // Assume technical knowledge
  const brief = generateTechnicalBrief(technicalInterpretations[0]);
}
```

## Troubleshooting

### Issue: Low Confidence After Clarification
**Solution**: Request specific examples from user
```javascript
if (synthesis.confidence < 0.7 && clarificationRound > 1) {
  console.log('Could you provide a specific example of what you want?');
  const example = await getUserExample();
  interpretations = refineWithExample(interpretations, example);
}
```

### Issue: Contradictory User Responses
**Solution**: Highlight contradiction and ask for priority
```javascript
const contradictions = detectContradictions(responses);
if (contradictions.length > 0) {
  console.log(`I notice some conflicting requirements: ${contradictions}`);
  console.log('Which is more important to you?');
  const priority = await getUserPriority(contradictions);
}
```

### Issue: Too Many Interpretations
**Solution**: Focus on top 2 and ask direct choice
```javascript
if (rankedInterpretations[1].probability > 0.3) {
  console.log('I see two main possibilities:');
  console.log(`A) ${rankedInterpretations[0].description}`);
  console.log(`B) ${rankedInterpretations[1].description}`);
  console.log('Which better matches your intent?');
}
```

## Integration Examples

### With SPARC Workflow
```bash
# Use intent analyzer before SPARC specification phase
npx claude-flow@alpha skill-run intent-analyzer \
  --input "user-request.txt" \
  --output "/tmp/intent-brief.json"

# Feed result to SPARC
npx claude-flow@alpha sparc run spec-pseudocode \
  --context "/tmp/intent-brief.json"
```

### With Cascade Orchestrator
```javascript
// Integrate as first step in cascade
const cascade = {
  steps: [
    {
      skill: 'intent-analyzer',
      input: userRequest,
      output: 'intent-brief'
    },
    {
      skill: 'feature-dev-complete',
      input: '${intent-brief}',
      conditional: '${intent-brief.confidence} > 0.8'
    }
  ]
};
```

### With Agent Swarm
```bash
# Spawn intent analyzer as coordinator
npx claude-flow@alpha swarm-init --topology hierarchical
npx claude-flow@alpha agent-spawn --type analyst --role coordinator

# Agents report findings to analyzer for synthesis
npx claude-flow@alpha task-orchestrate \
  --task "Analyze user intent from multiple perspectives" \
  --coordinator "intent-analyzer"
```

## Memory Schema

```javascript
{
  "intent-analyzer/": {
    "session-${id}/": {
      "raw-input": { /* Phase 1 */ },
      "characteristics": { /* Phase 1 */ },
      "context-clues": { /* Phase 1 */ },
      "component-tree": { /* Phase 2 */ },
      "interpretations": { /* Phase 3 */ },
      "ranked-interpretations": { /* Phase 3 */ },
      "questions": { /* Phase 4 */ },
      "user-responses": { /* Phase 4 */ },
      "refined-interpretations": { /* Phase 4 */ },
      "final-synthesis": { /* Phase 5 */ },
      "execution-brief": { /* Phase 5 */ }
    }
  }
}
```

## Performance Optimization

### Caching Common Patterns
```javascript
// Cache frequently seen intent patterns
const intentCache = new Map();

async function checkCache(userInput) {
  const embedding = await generateEmbedding(userInput);
  const similar = findSimilar(embedding, intentCache);

  if (similar && similar.similarity > 0.9) {
    console.log('Using cached interpretation...');
    return similar.interpretation;
  }

  return null;
}
```

### Parallel Interpretation Generation
```javascript
// Generate interpretations concurrently
const interpretationPromises = [
  generateLiteralInterpretation(userInput),
  generateInferredInterpretation(userInput, context),
  generateExpertInterpretation(userInput, expertise),
  generateNovelInterpretation(userInput) // Think outside the box
];

const interpretations = await Promise.all(interpretationPromises);
```

## Skill Completion

Upon successful completion, this skill outputs:
1. **intent-analysis-result.json**: Complete execution brief
2. **confidence-score.txt**: Final confidence percentage
3. **clarification-log.md**: Record of questions and answers
4. **next-steps.md**: Recommended workflow to execute

The skill is complete when user confirmation is obtained and confidence > 0.8.
