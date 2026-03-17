---
name: when-optimizing-prompts-use-prompt-architect
version: 1.0.0
description: Comprehensive framework for analyzing, creating, and refining prompts for AI systems using evidence-based techniques
category: utilities
tags: [prompt-engineering, optimization, ai-systems, llm]
agents: [researcher, coder]
difficulty: intermediate
estimated_duration: 20-40min
success_criteria:
  - Prompt structure optimized
  - Anti-patterns eliminated
  - Evidence-based techniques applied
  - Effectiveness validated
validation_method: A/B testing
dependencies:
  - claude-flow@alpha
prerequisites:
  - Prompt to optimize OR use case defined
outputs:
  - Optimized prompt
  - Analysis report
  - A/B test results
triggers:
  - Poor AI response quality
  - Inconsistent outputs
  - New prompt needed
  - Prompt refactoring required
---

# Prompt Architect - Evidence-Based Prompt Engineering

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
  --description "Analyze prompt structure and quality" \
  --complexity "medium"

npx claude-flow@alpha hooks post-task \
  --task-id "prompt-analysis" \
  --output "analysis-report.json"
```

## Phase 2: Structure Optimization

### Objective
Reorganize prompt for logical flow and clarity

### Agent: Coder (Prompt Specialist)

**Step 2.1: Apply Template Structure**
```javascript
const optimizedStructure = {
  systemContext: {
    domain: extractDomain(prompt),
    background: generateContextualBackground(),
    constraints: extractOrInferConstraints(prompt)
  },
  roleDefinition: {
    persona: definePersona(task),
    expertise: listRequiredExpertise(),
    perspective: defineWorkingPerspective()
  },
  taskDescription: {
    primary: extractPrimaryTask(prompt),
    secondary: extractSecondaryTasks(prompt),
    scope: defineScope(),
    outOfScope: defineWhatNotToDo()
  },
  constraints: {
    required: extractRequirements(prompt),
    forbidden: extractProhibitions(prompt),
    optional: extractPreferences(prompt)
  },
  formatSpecification: {
    outputFormat: specifyFormat(),
    structure: defineStructure(),
    examples: []
  },
  qualityCriteria: {
    success: defineSuccessCriteria(),
    validation: defineValidationMethod(),
    metrics: defineMetrics()
  }
};

await memory.store('prompt-architect/structure', optimizedStructure);
```

**Step 2.2: Build Optimized Prompt**
```markdown
# System Context
${optimizedStructure.systemContext.background}

Domain: ${optimizedStructure.systemContext.domain}
Constraints: ${optimizedStructure.systemContext.constraints.join(', ')}

# Role
You are ${optimizedStructure.roleDefinition.persona} with expertise in:
${optimizedStructure.roleDefinition.expertise.map(e => `- ${e}`).join('\n')}

Your perspective: ${optimizedStructure.roleDefinition.perspective}

# Task
Primary objective: ${optimizedStructure.taskDescription.primary}

${optimizedStructure.taskDescription.secondary.length > 0 ?
  'Secondary objectives:\n' + optimizedStructure.taskDescription.secondary.map(t => `- ${t}`).join('\n') : ''}

Scope: ${optimizedStructure.taskDescription.scope}
Out of scope: ${optimizedStructure.taskDescription.outOfScope.join(', ')}

# Constraints
MUST: ${optimizedStructure.constraints.required.map(r => `- ${r}`).join('\n')}
MUST NOT: ${optimizedStructure.constraints.forbidden.map(f => `- ${f}`).join('\n')}
PREFER: ${optimizedStructure.constraints.optional.map(o => `- ${o}`).join('\n')}

# Output Format
${optimizedStructure.formatSpecification.outputFormat}

Structure:
${optimizedStructure.formatSpecification.structure}

# Quality Criteria
Success is defined as:
${optimizedStructure.qualityCriteria.success.map(s => `- ${s}`).join('\n')}

Validation method: ${optimizedStructure.qualityCriteria.validation}
```

**Step 2.3: Add Progressive Disclosure**
```javascript
// For complex prompts, use hierarchical structure
const progressivePrompt = {
  essential: generateEssentialInstructions(),
  details: generateDetailedGuidance(),
  advanced: generateAdvancedTechniques(),
  examples: generateExamples(),
  troubleshooting: generateTroubleshootingGuide()
};

// Structure with collapsible sections
const enhancedPrompt = `
${progressivePrompt.essential}

<details>
<summary>Detailed Guidance</summary>
${progressivePrompt.details}
</details>

<details>
<summary>Advanced Techniques</summary>
${progressivePrompt.advanced}
</details>

<details>
<summary>Examples</summary>
${progressivePrompt.examples}
</details>
`;
```

### Validation Criteria
- [ ] All 7 components present
- [ ] Logical flow established
- [ ] Progressive disclosure applied
- [ ] Clear hierarchy visible

### Script Template
```bash
#!/bin/bash
# optimize-structure.sh

INPUT_PROMPT="$1"
OUTPUT_PROMPT="$2"

# Analyze structure
ANALYSIS=$(npx claude-flow@alpha agent-spawn \
  --type researcher \
  --task "Analyze prompt structure: $(cat $INPUT_PROMPT)")

# Optimize
OPTIMIZED=$(npx claude-flow@alpha agent-spawn \
  --type coder \
  --task "Restructure prompt based on analysis: $ANALYSIS")

echo "$OPTIMIZED" > "$OUTPUT_PROMPT"

npx claude-flow@alpha hooks post-edit \
  --file "$OUTPUT_PROMPT" \
  --memory-key "prompt-architect/optimized"
```

## Phase 3: Apply Evidence-Based Techniques

### Objective
Incorporate proven prompt engineering methods

### Agent: Researcher + Coder

**Step 3.1: Add Chain-of-Thought**
```markdown
# Chain-of-Thought Enhancement

Before providing your final answer, think through the problem step by step:

1. **Understand**: Restate the problem in your own words
2. **Analyze**: Break down into components
3. **Reason**: Work through the logic
4. **Synthesize**: Combine insights
5. **Conclude**: Provide final answer

Format your response as:
<thinking>
[Your step-by-step reasoning]
</thinking>

<answer>
[Your final answer]
</answer>
```

**Step 3.2: Add Self-Consistency**
```markdown
# Self-Consistency Pattern

Generate 3 independent solutions to this problem using different approaches:

Approach 1: [Method 1]
Approach 2: [Method 2]
Approach 3: [Method 3]

Then compare the solutions and select the most robust answer, explaining why it's superior.
```

**Step 3.3: Add ReAct Pattern**
```markdown
# ReAct (Reasoning + Acting) Pattern

For each step in your process:

**Thought**: [What you're thinking]
**Action**: [What you're doing]
**Observation**: [What you learned]

Repeat this cycle until the task is complete.

Example:
Thought: I need to understand the data structure
Action: Analyze the schema
Observation: It's a relational database with 5 tables
Thought: I should check for relationships
Action: Examine foreign keys
Observation: Tables are connected via user_id
```

**Step 3.4: Add Few-Shot Examples**
```javascript
const examples = [
  {
    input: '[Example input 1]',
    reasoning: '[How to approach it]',
    output: '[Expected output 1]'
  },
  {
    input: '[Example input 2]',
    reasoning: '[How to approach it]',
    output: '[Expected output 2]'
  },
  {
    input: '[Example input 3 - edge case]',
    reasoning: '[How to handle edge case]',
    output: '[Expected output 3]'
  }
];

const fewShotSection = `
# Examples

${examples.map((ex, i) => `
## Example ${i + 1}

**Input**: ${ex.input}

**Reasoning**: ${ex.reasoning}

**Output**:
\`\`\`
${ex.output}
\`\`\`
`).join('\n')}

Now apply the same pattern to: [ACTUAL INPUT]
`;
```

**Step 3.5: Add Constraint Framing**
```markdown
# Constraint-Based Optimization

This task requires balancing multiple constraints:

1. **Quality**: Must meet 90% accuracy
2. **Speed**: Must complete in < 2 seconds
3. **Resources**: Memory usage < 100MB
4. **Safety**: No external API calls

When these constraints conflict, prioritize in this order: Safety > Quality > Speed > Resources

If you cannot satisfy all constraints, explicitly state which ones are violated and why.
```

### Validation Criteria
- [ ] CoT reasoning added
- [ ] Self-consistency pattern included
- [ ] Examples provided (2-3)
- [ ] Constraints clearly framed

### Memory Pattern
```bash
npx claude-flow@alpha hooks post-edit \
  --file "enhanced-prompt.md" \
  --memory-key "prompt-architect/techniques-applied"
```

## Phase 4: Validate Effectiveness

### Objective
Test prompt performance and measure improvement

### Agent: Researcher

**Step 4.1: Define Test Cases**
```javascript
const testCases = [
  {
    id: 'test-1',
    type: 'typical',
    input: '[Common use case]',
    expectedOutput: '[What should happen]',
    successCriteria: '[How to measure success]'
  },
  {
    id: 'test-2',
    type: 'edge-case',
    input: '[Unusual scenario]',
    expectedOutput: '[How to handle]',
    successCriteria: '[Validation method]'
  },
  {
    id: 'test-3',
    type: 'stress',
    input: '[Complex/ambiguous input]',
    expectedOutput: '[Robust handling]',
    successCriteria: '[Quality threshold]'
  }
];

await memory.store('prompt-architect/test-cases', testCases);
```

**Step 4.2: Run A/B Tests**
```javascript
async function runABTest(originalPrompt, optimizedPrompt, testCases) {
  const results = {
    original: [],
    optimized: []
  };

  for (const testCase of testCases) {
    // Test original prompt
    const originalResult = await testPrompt(originalPrompt, testCase.input);
    results.original.push({
      testId: testCase.id,
      output: originalResult,
      score: scoreOutput(originalResult, testCase.expectedOutput),
      meetsSuccessCriteria: evaluateCriteria(originalResult, testCase.successCriteria)
    });

    // Test optimized prompt
    const optimizedResult = await testPrompt(optimizedPrompt, testCase.input);
    results.optimized.push({
      testId: testCase.id,
      output: optimizedResult,
      score: scoreOutput(optimizedResult, testCase.expectedOutput),
      meetsSuccessCriteria: evaluateCriteria(optimizedResult, testCase.successCriteria)
    });
  }

  return results;
}

const abTestResults = await runABTest(originalPrompt, optimizedPrompt, testCases);
await memory.store('prompt-architect/ab-test-results', abTestResults);
```

**Step 4.3: Calculate Metrics**
```javascript
const metrics = {
  original: {
    avgScore: calculateAverage(abTestResults.original.map(r => r.score)),
    successRate: calculateSuccessRate(abTestResults.original),
    consistency: calculateConsistency(abTestResults.original)
  },
  optimized: {
    avgScore: calculateAverage(abTestResults.optimized.map(r => r.score)),
    successRate: calculateSuccessRate(abTestResults.optimized),
    consistency: calculateConsistency(abTestResults.optimized)
  },
  improvement: {
    scoreImprovement: 0, // calculated below
    successRateImprovement: 0,
    consistencyImprovement: 0
  }
};

metrics.improvement = {
  scoreImprovement: ((metrics.optimized.avgScore - metrics.original.avgScore) / metrics.original.avgScore * 100).toFixed(2) + '%',
  successRateImprovement: ((metrics.optimized.successRate - metrics.original.successRate) / metrics.original.successRate * 100).toFixed(2) + '%',
  consistencyImprovement: ((metrics.optimized.consistency - metrics.original.consistency) / metrics.original.consistency * 100).toFixed(2) + '%'
};

await memory.store('prompt-architect/metrics', metrics);
```

### Validation Criteria
- [ ] Test cases defined (3+ cases)
- [ ] A/B testing completed
- [ ] Metrics calculated
- [ ] Improvement demonstrated

### Script Template
```bash
#!/bin/bash
# validate-prompt.sh

ORIGINAL="$1"
OPTIMIZED="$2"
TEST_CASES="$3"

# Run A/B tests
RESULTS=$(npx claude-flow@alpha agent-spawn \
  --type researcher \
  --task "A/B test prompts: original='$ORIGINAL' optimized='$OPTIMIZED' tests='$TEST_CASES'")

# Calculate improvement
METRICS=$(echo "$RESULTS" | jq '.improvement')

echo "Improvement Metrics:"
echo "$METRICS" | jq '.'

# Store results
npx claude-flow@alpha hooks post-task \
  --task-id "prompt-validation" \
  --metrics "$METRICS"
```

## Phase 5: Refine Iteratively

### Objective
Continuous improvement based on validation results

### Agent: Coder

**Step 5.1: Analyze Failures**
```javascript
const failures = abTestResults.optimized.filter(r => !r.meetsSuccessCriteria);

const failureAnalysis = failures.map(failure => {
  const testCase = testCases.find(tc => tc.id === failure.testId);

  return {
    testId: failure.testId,
    testType: testCase.type,
    expectedOutput: testCase.expectedOutput,
    actualOutput: failure.output,
    gap: analyzeGap(testCase.expectedOutput, failure.output),
    rootCause: identifyRootCause(failure, optimizedPrompt),
    recommendedFix: suggestFix(rootCause)
  };
});

await memory.store('prompt-architect/failure-analysis', failureAnalysis);
```

**Step 5.2: Apply Refinements**
```javascript
let refinedPrompt = optimizedPrompt;

for (const analysis of failureAnalysis) {
  switch (analysis.rootCause.type) {
    case 'MISSING_CONSTRAINT':
      refinedPrompt = addConstraint(refinedPrompt, analysis.recommendedFix.constraint);
      break;
    case 'AMBIGUOUS_INSTRUCTION':
      refinedPrompt = clarifyInstruction(refinedPrompt, analysis.recommendedFix.clarification);
      break;
    case 'INSUFFICIENT_EXAMPLES':
      refinedPrompt = addExample(refinedPrompt, analysis.recommendedFix.example);
      break;
    case 'MISSING_EDGE_CASE_HANDLING':
      refinedPrompt = addEdgeCaseGuidance(refinedPrompt, analysis.recommendedFix.guidance);
      break;
  }
}

await memory.store('prompt-architect/refined-prompt', refinedPrompt);
```

**Step 5.3: Re-validate**
```javascript
const revalidationResults = await runABTest(optimizedPrompt, refinedPrompt, testCases);

const improvementFromOptimized = {
  scoreImprovement: calculateImprovement(
    metrics.optimized.avgScore,
    calculateAverage(revalidationResults.optimized.map(r => r.score))
  ),
  successRateImprovement: calculateImprovement(
    metrics.optimized.successRate,
    calculateSuccessRate(revalidationResults.optimized)
  )
};

// If refined version is better, adopt it
if (improvementFromOptimized.scoreImprovement > 5) {
  console.log('✅ Refinement successful. Adopting refined version.');
  finalPrompt = refinedPrompt;
} else {
  console.log('✅ Optimized version is sufficient.');
  finalPrompt = optimizedPrompt;
}

await memory.store('prompt-architect/final-prompt', finalPrompt);
```

**Step 5.4: Generate Documentation**
```markdown
# Prompt Optimization Report

## Original Prompt
\`\`\`
${originalPrompt}
\`\`\`

## Final Prompt
\`\`\`
${finalPrompt}
\`\`\`

## Changes Applied
${changesApplied.map(change => `- ${change}`).join('\n')}

## Performance Metrics

| Metric | Original | Optimized | Improvement |
|--------|----------|-----------|-------------|
| Avg Score | ${metrics.original.avgScore} | ${metrics.optimized.avgScore} | ${metrics.improvement.scoreImprovement} |
| Success Rate | ${metrics.original.successRate}% | ${metrics.optimized.successRate}% | ${metrics.improvement.successRateImprovement} |
| Consistency | ${metrics.original.consistency} | ${metrics.optimized.consistency} | ${metrics.improvement.consistencyImprovement} |

## Test Results
${testCases.map(tc => `
### ${tc.id} (${tc.type})
- **Expected**: ${tc.expectedOutput}
- **Original Result**: ${getResult('original', tc.id)}
- **Optimized Result**: ${getResult('optimized', tc.id)}
- **Status**: ${getStatus('optimized', tc.id)}
`).join('\n')}

## Recommendations
${generateRecommendations(finalPrompt)}
```

### Validation Criteria
- [ ] Failures analyzed
- [ ] Refinements applied
- [ ] Re-validation completed
- [ ] Documentation generated

### Memory Pattern
```bash
npx claude-flow@alpha hooks session-end \
  --session-id "prompt-architect-${TIMESTAMP}" \
  --export-metrics true \
  --summary "Prompt optimized with ${IMPROVEMENT}% improvement"
```

## Success Metrics

### Quantitative
- Score improvement > 20%
- Success rate > 85%
- Consistency score > 0.8
- All test cases pass

### Qualitative
- Clear structure
- No anti-patterns
- Evidence-based techniques applied
- User satisfaction with outputs

## Common Patterns

### Pattern 1: Role-Based Optimization
```markdown
You are an expert ${domain} specialist with ${years} years of experience.
Your expertise includes: ${expertise_list}
You approach problems by: ${methodology}
```

### Pattern 2: Constraint-First Design
```markdown
# Constraints (Read First)
MUST: ${required_constraints}
MUST NOT: ${forbidden_actions}
OPTIMIZE FOR: ${optimization_targets}

# Task
[task description with constraints in mind]
```

### Pattern 3: Format-Driven Output
```markdown
Your output MUST follow this exact structure:

\`\`\`json
{
  "analysis": "...",
  "recommendations": [...],
  "confidence": 0.XX
}
\`\`\`

Do not deviate from this format.
```

## Integration Examples

### With Agent Creation
```javascript
// Use prompt architect to optimize agent system prompts
const agentPrompt = await optimizePrompt({
  role: 'backend-developer',
  domain: 'Node.js API development',
  constraints: ['RESTful design', 'security-first', 'test-driven'],
  outputFormat: 'production-ready code'
});
```

### With SPARC Workflow
```bash
# Optimize specification prompts
npx claude-flow@alpha skill-run prompt-architect \
  --input "sparc-spec-prompt.md" \
  --output "optimized-spec-prompt.md"

# Use optimized prompt in SPARC
npx claude-flow@alpha sparc run spec-pseudocode \
  --prompt-file "optimized-spec-prompt.md"
```

## Memory Schema

```javascript
{
  "prompt-architect/": {
    "session-${id}/": {
      "analysis": {},
      "anti-patterns": [],
      "missing": [],
      "structure": {},
      "techniques-applied": [],
      "test-cases": [],
      "ab-test-results": {},
      "metrics": {},
      "failure-analysis": [],
      "refined-prompt": "",
      "final-prompt": ""
    }
  }
}
```

## Skill Completion

Outputs:
1. **final-prompt.md**: Optimized prompt ready for use
2. **optimization-report.md**: Detailed analysis and results
3. **ab-test-results.json**: Performance comparison data
4. **prompt-library-entry.md**: Cataloged for reuse

Skill complete when metrics show >20% improvement and all test cases pass.
