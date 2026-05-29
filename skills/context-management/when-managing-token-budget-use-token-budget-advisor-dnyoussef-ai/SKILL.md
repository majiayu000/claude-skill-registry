---
name: when-managing-token-budget-use-token-budget-advisor
version: 1.0.0
description: Proactive token budget management tool for assessing usage, analyzing task complexity, generating chunking strategies, and creating execution plans that stay within budget limits
tags:
  - meta-tool
  - token-management
  - budget-optimization
  - task-planning
  - chunking
complexity: MEDIUM
agents_required:
  - planner
  - code-analyzer
auto_trigger: false
---

# Token Budget Advisor

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
  usage.buffer = Math.floor(usage.limit * 0.15); // 15% safety buffer
  usage.available = usage.remaining - usage.buffer;

  // Calculate status
  const usagePercent = (usage.used / usage.limit) * 100;
  if (usagePercent > 90) {
    usage.status = "critical";
  } else if (usagePercent > 75) {
    usage.status = "warning";
  } else if (usagePercent > 50) {
    usage.status = "caution";
  } else {
    usage.status = "healthy";
  }

  return usage;
}

function getCurrentTokenUsage() {
  // Extract from context or tracking
  // This is a placeholder - actual implementation depends on system
  return 36000; // Example current usage
}
```

**Historical Pattern Analysis:**
```javascript
function analyzeUsagePatterns(historyData) {
  const patterns = {
    avgPerTask: 0,
    peakUsage: 0,
    typicalDuration: 0,
    commonOverages: []
  };

  if (historyData.length === 0) {
    // No history, use conservative estimates
    patterns.avgPerTask = 15000;
    patterns.peakUsage = 40000;
    patterns.typicalDuration = 30; // minutes
    return patterns;
  }

  // Calculate averages
  patterns.avgPerTask = historyData.reduce((sum, task) =>
    sum + task.tokens, 0) / historyData.length;

  patterns.peakUsage = Math.max(...historyData.map(t => t.tokens));

  patterns.typicalDuration = historyData.reduce((sum, task) =>
    sum + task.duration, 0) / historyData.length;

  // Identify common overage causes
  const overages = historyData.filter(t => t.exceeded_estimate);
  const causes = {};
  overages.forEach(o => {
    causes[o.reason] = (causes[o.reason] || 0) + 1;
  });
  patterns.commonOverages = Object.entries(causes)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([reason, count]) => ({ reason, count }));

  return patterns;
}
```

### Phase 2: Task Complexity Analysis

**Complexity Estimator:**
```javascript
function estimateTaskComplexity(taskDescription) {
  const complexity = {
    baseTokens: 0,
    multipliers: {},
    totalEstimate: 0,
    confidence: "low",
    factors: []
  };

  // Base estimation by task type
  const taskType = inferTaskType(taskDescription);
  const baseEstimates = {
    "simple-edit": 2000,
    "feature-implementation": 15000,
    "refactoring": 8000,
    "architecture-design": 12000,
    "full-stack-development": 40000,
    "debugging": 5000,
    "testing": 6000,
    "documentation": 4000,
    "integration": 10000,
    "migration": 20000
  };

  complexity.baseTokens = baseEstimates[taskType] || 10000;
  complexity.factors.push({ type: "base", value: complexity.baseTokens, reason: `Task type: ${taskType}` });

  // Apply multipliers

  // Multiple agents
  const agentCount = estimateAgentCount(taskDescription);
  if (agentCount > 3) {
    complexity.multipliers.agents = 1.3;
    complexity.factors.push({ type: "multiplier", value: 1.3, reason: `${agentCount} agents required` });
  }

  // External integrations
  if (/\b(api|database|github|external|integration)\b/i.test(taskDescription)) {
    complexity.multipliers.integration = 1.4;
    complexity.factors.push({ type: "multiplier", value: 1.4, reason: "External integrations" });
  }

  // Testing requirements
  if (/\b(test|coverage|tdd|e2e)\b/i.test(taskDescription)) {
    complexity.multipliers.testing = 1.25;
    complexity.factors.push({ type: "multiplier", value: 1.25, reason: "Testing requirements" });
  }

  // Documentation
  if (/\b(document|readme|guide|tutorial)\b/i.test(taskDescription)) {
    complexity.multipliers.documentation = 1.15;
    complexity.factors.push({ type: "multiplier", value: 1.15, reason: "Documentation needed" });
  }

  // Complexity keywords
  if (/\b(complex|advanced|comprehensive|full|complete|entire)\b/i.test(taskDescription)) {
    complexity.multipliers.complexity = 1.5;
    complexity.factors.push({ type: "multiplier", value: 1.5, reason: "High complexity indicators" });
  }

  // Calculate total
  const totalMultiplier = Object.values(complexity.multipliers)
    .reduce((product, mult) => product * mult, 1);

  complexity.totalEstimate = Math.ceil(complexity.baseTokens * totalMultiplier);

  // Confidence assessment
  const factorCount = Object.keys(complexity.multipliers).length;
  if (factorCount >= 3) {
    complexity.confidence = "high";
  } else if (factorCount >= 1) {
    complexity.confidence = "medium";
  } else {
    complexity.confidence = "low";
  }

  return complexity;
}

function inferTaskType(description) {
  const patterns = {
    "simple-edit": /\b(fix typo|update|change|rename|small)\b/i,
    "feature-implementation": /\b(implement|add feature|create|build)\b/i,
    "refactoring": /\b(refactor|reorganize|restructure|cleanup)\b/i,
    "architecture-design": /\b(design|architect|plan|structure)\b/i,
    "full-stack-development": /\b(full.?stack|frontend.*backend|complete app)\b/i,
    "debugging": /\b(debug|fix bug|resolve error|troubleshoot)\b/i,
    "testing": /\b(test|tdd|coverage|qa)\b/i,
    "documentation": /\b(document|write.*guide|readme|tutorial)\b/i,
    "integration": /\b(integrat|connect|link|api.*call)\b/i,
    "migration": /\b(migrat|convert|port|upgrade)\b/i
  };

  for (const [type, pattern] of Object.entries(patterns)) {
    if (pattern.test(description)) {
      return type;
    }
  }

  return "feature-implementation"; // Default
}

function estimateAgentCount(description) {
  let count = 1; // At least one agent

  if (/\b(frontend|backend|database)\b/i.test(description)) count++;
  if (/\b(test|qa)\b/i.test(description)) count++;
  if (/\b(review|quality)\b/i.test(description)) count++;
  if (/\b(document)\b/i.test(description)) count++;
  if (/\b(deploy|devops|ci.?cd)\b/i.test(description)) count++;

  return count;
}
```

### Phase 3: Chunking Strategy

**Planner Agent Task:**
```bash
# Spawn planner agent for chunking strategy
# Agent instructions:
# 1. Analyze task dependencies
# 2. Identify logical boundaries
# 3. Optimize chunk sizes (within budget)
# 4. Define inter-chunk communication
# 5. Create state management plan
# 6. Store strategy in memory

npx claude-flow@alpha memory store --key "budget/chunking-strategy" --value "{
  \"chunks\": [...],
  \"dependencies\": {...},
  \"communication\": {...}
}"
```

**Chunking Algorithm:**
```javascript
function generateChunkingStrategy(task, availableBudget) {
  const strategy = {
    chunks: [],
    totalEstimate: 0,
    fitsInBudget: false,
    recommendation: ""
  };

  const complexity = estimateTaskComplexity(task.description);

  // If task fits in budget, no chunking needed
  if (complexity.totalEstimate <= availableBudget * 0.85) {
    strategy.chunks.push({
      id: "chunk-1",
      name: task.name,
      description: task.description,
      estimatedTokens: complexity.totalEstimate,
      dependencies: [],
      priority: "high"
    });
    strategy.totalEstimate = complexity.totalEstimate;
    strategy.fitsInBudget = true;
    strategy.recommendation = "Execute as single task";
    return strategy;
  }

  // Task needs chunking
  const idealChunkSize = Math.floor(availableBudget * 0.4); // 40% of available per chunk
  const chunkCount = Math.ceil(complexity.totalEstimate / idealChunkSize);

  // Break down by logical phases
  const phases = decomposeIntoPhases(task.description);

  phases.forEach((phase, index) => {
    const phaseEstimate = Math.ceil(complexity.totalEstimate / phases.length);

    strategy.chunks.push({
      id: `chunk-${index + 1}`,
      name: phase.name,
      description: phase.description,
      estimatedTokens: phaseEstimate,
      dependencies: phase.dependencies,
      priority: phase.priority,
      outputs: phase.outputs,
      nextChunkInputs: phase.nextChunkInputs
    });
  });

  strategy.totalEstimate = strategy.chunks.reduce((sum, c) => sum + c.estimatedTokens, 0);
  strategy.fitsInBudget = strategy.chunks.every(c => c.estimatedTokens <= availableBudget);

  if (strategy.fitsInBudget) {
    strategy.recommendation = `Execute in ${strategy.chunks.length} sequential chunks`;
  } else {
    strategy.recommendation = "Task too large - consider scope reduction or multi-session execution";
  }

  return strategy;
}

function decomposeIntoPhases(description) {
  // Intelligent phase decomposition
  const phases = [];

  // Phase 1: Research and Planning
  phases.push({
    name: "Research & Planning",
    description: "Analyze requirements, research best practices, design approach",
    dependencies: [],
    priority: "high",
    outputs: ["requirements.md", "architecture-design.md"],
    nextChunkInputs: ["architecture-design.md"]
  });

  // Phase 2: Core Implementation
  phases.push({
    name: "Core Implementation",
    description: "Implement main functionality based on design",
    dependencies: ["chunk-1"],
    priority: "high",
    outputs: ["src/**/*.js", "core-features"],
    nextChunkInputs: ["core-features"]
  });

  // Phase 3: Testing
  phases.push({
    name: "Testing & Validation",
    description: "Create tests, validate functionality, fix bugs",
    dependencies: ["chunk-2"],
    priority: "medium",
    outputs: ["tests/**/*.test.js", "coverage-report"],
    nextChunkInputs: ["coverage-report"]
  });

  // Phase 4: Documentation & Polish
  phases.push({
    name: "Documentation & Polish",
    description: "Write documentation, refine code, finalize",
    dependencies: ["chunk-3"],
    priority: "low",
    outputs: ["README.md", "docs/**/*.md", "final-code"],
    nextChunkInputs: []
  });

  return phases;
}
```

### Phase 4: Priority Optimization

**Priority Matrix:**
```javascript
function optimizePriorities(chunks, constraints) {
  const prioritized = chunks.map(chunk => {
    const score = calculatePriorityScore(chunk, constraints);
    return { ...chunk, priorityScore: score };
  });

  // Sort by priority score (higher = more important)
  prioritized.sort((a, b) => b.priorityScore - a.priorityScore);

  return prioritized;
}

function calculatePriorityScore(chunk, constraints) {
  let score = 0;

  // Base priority
  const priorityWeights = { high: 100, medium: 50, low: 25 };
  score += priorityWeights[chunk.priority] || 50;

  // Dependency blocking (blocks other chunks)
  const blockingCount = countDependents(chunk.id, constraints.dependencies);
  score += blockingCount * 20;

  // Critical path
  if (isOnCriticalPath(chunk, constraints)) {
    score += 30;
  }

  // Quick wins (low tokens, high value)
  if (chunk.estimatedTokens < 5000 && chunk.value === "high") {
    score += 25;
  }

  // Risk mitigation (high-risk items earlier)
  if (chunk.risk === "high") {
    score += 15;
  }

  return score;
}
```

### Phase 5: Execution Planning

**Execution Plan Format:**
```markdown
## Token Budget Execution Plan

### Budget Status
- Limit: 200,000 tokens
- Used: 36,000 tokens (18%)
- Remaining: 164,000 tokens
- Buffer: 30,000 tokens (15%)
- **Available: 134,000 tokens**
- Status: ✅ Healthy

### Task Analysis
**Task:** Build full-stack e-commerce application
**Estimated Complexity:** 68,000 tokens
- Base: 40,000 (full-stack development)
- Multipliers: 1.7x (testing, documentation, integrations)
- Confidence: High

### Chunking Strategy
**Approach:** Sequential 4-chunk execution
**Fits in budget:** ✅ Yes (max chunk: 20,000 tokens)

---

## Execution Sequence

### Chunk 1: Research & Planning (Priority: High)
**Estimated tokens:** 12,000
**Cumulative:** 48,000 / 200,000 (24%)

**Tasks:**
1. [ ] Analyze requirements and use cases
2. [ ] Research e-commerce best practices
3. [ ] Design system architecture
4. [ ] Plan database schema
5. [ ] Define API contracts

**Outputs:**
- requirements.md
- architecture-design.md
- database-schema.sql
- api-spec.yaml

**Success Criteria:**
- Complete architecture documented
- Database schema validated
- API contracts defined

**Checkpoint:**
```bash
npx claude-flow@alpha memory store --key "ecommerce/phase1-complete" --value "{outputs}"
npx claude-flow@alpha hooks post-task --task-id "chunk-1" --tokens-used <actual>
```

---

### Chunk 2: Core Implementation (Priority: High)
**Estimated tokens:** 20,000
**Cumulative:** 68,000 / 200,000 (34%)
**Dependencies:** Chunk 1 outputs

**Tasks:**
1. [ ] Implement database models
2. [ ] Create REST API endpoints
3. [ ] Build authentication system
4. [ ] Implement product catalog
5. [ ] Create shopping cart logic

**Inputs:**
- architecture-design.md
- database-schema.sql
- api-spec.yaml

**Outputs:**
- backend/models/**/*.js
- backend/routes/**/*.js
- backend/middleware/auth.js

**Success Criteria:**
- All API endpoints functional
- Authentication working
- Core features implemented

**Checkpoint:**
```bash
npx claude-flow@alpha memory store --key "ecommerce/phase2-complete" --value "{outputs}"
```

---

### Chunk 3: Testing & Validation (Priority: Medium)
**Estimated tokens:** 18,000
**Cumulative:** 86,000 / 200,000 (43%)
**Dependencies:** Chunk 2 outputs

**Tasks:**
1. [ ] Write unit tests for models
2. [ ] Create API integration tests
3. [ ] Test authentication flows
4. [ ] Validate cart operations
5. [ ] Generate coverage report

**Inputs:**
- backend/**/*.js

**Outputs:**
- tests/unit/**/*.test.js
- tests/integration/**/*.test.js
- coverage-report.html

**Success Criteria:**
- >80% code coverage
- All critical paths tested
- No failing tests

**Checkpoint:**
```bash
npx claude-flow@alpha memory store --key "ecommerce/phase3-complete" --value "{outputs}"
```

---

### Chunk 4: Documentation & Polish (Priority: Low)
**Estimated tokens:** 18,000
**Cumulative:** 104,000 / 200,000 (52%)
**Dependencies:** Chunk 3 outputs

**Tasks:**
1. [ ] Write API documentation
2. [ ] Create deployment guide
3. [ ] Add inline code comments
4. [ ] Generate README
5. [ ] Final code review and polish

**Inputs:**
- All previous outputs

**Outputs:**
- docs/API.md
- docs/DEPLOYMENT.md
- README.md
- Final polished codebase

**Success Criteria:**
- Complete documentation
- Deployment guide tested
- Code quality passing

**Final Checkpoint:**
```bash
npx claude-flow@alpha memory store --key "ecommerce/complete" --value "{all-outputs}"
npx claude-flow@alpha hooks post-task --task-id "ecommerce-app" --success true
```

---

## Budget Tracking

| Checkpoint | Estimated | Actual | Remaining | Status |
|------------|-----------|--------|-----------|--------|
| Start | 0 | 36,000 | 164,000 | ✅ |
| Chunk 1 | 12,000 | TBD | TBD | ⏳ |
| Chunk 2 | 20,000 | TBD | TBD | ⏳ |
| Chunk 3 | 18,000 | TBD | TBD | ⏳ |
| Chunk 4 | 18,000 | TBD | TBD | ⏳ |
| **Total** | **68,000** | TBD | TBD | ⏳ |

## Contingency Plans

### If Chunk Exceeds Estimate
1. Stop at natural breakpoint
2. Store progress in memory
3. Re-assess remaining budget
4. Adjust subsequent chunks
5. Continue or defer remaining work

### If Approaching Budget Limit
1. Prioritize critical chunks
2. Defer low-priority work
3. Reduce scope if necessary
4. Document deferred items

### Rollback Strategy
- All chunks store outputs in memory
- Can resume from any checkpoint
- Incremental progress preserved
```

## Concrete Example: Real Budget Management

### Scenario
**Task:** Build authentication system with OAuth, JWT, and user management
**Budget:** 200,000 tokens, currently 45,000 used (155,000 remaining)

### Budget Analysis
```json
{
  "limit": 200000,
  "used": 45000,
  "remaining": 155000,
  "buffer": 30000,
  "available": 125000,
  "status": "healthy",
  "usagePercent": "22.5%"
}
```

### Complexity Estimation
```json
{
  "baseTokens": 15000,
  "multipliers": {
    "integration": 1.4,
    "testing": 1.25,
    "security": 1.3
  },
  "totalEstimate": 34125,
  "confidence": "high",
  "factors": [
    {"type": "base", "value": 15000, "reason": "Feature implementation"},
    {"type": "multiplier", "value": 1.4, "reason": "OAuth integration"},
    {"type": "multiplier", "value": 1.25, "reason": "Testing requirements"},
    {"type": "multiplier", "value": 1.3, "reason": "Security considerations"}
  ]
}
```

### Chunking Strategy
```json
{
  "chunks": [
    {
      "id": "chunk-1",
      "name": "OAuth Integration",
      "estimatedTokens": 12000,
      "priority": "high"
    },
    {
      "id": "chunk-2",
      "name": "JWT & Session Management",
      "estimatedTokens": 10000,
      "priority": "high",
      "dependencies": ["chunk-1"]
    },
    {
      "id": "chunk-3",
      "name": "User Management CRUD",
      "estimatedTokens": 8000,
      "priority": "medium",
      "dependencies": ["chunk-2"]
    },
    {
      "id": "chunk-4",
      "name": "Testing & Security Audit",
      "estimatedTokens": 9000,
      "priority": "high",
      "dependencies": ["chunk-1", "chunk-2", "chunk-3"]
    }
  ],
  "totalEstimate": 39000,
  "fitsInBudget": true,
  "recommendation": "Execute in 4 sequential chunks"
}
```

### Result
- **Total estimated:** 39,000 tokens (31% of available)
- **Peak chunk:** 12,000 tokens (well within budget)
- **Safety margin:** 86,000 tokens remaining after completion
- **Execution:** Can proceed confidently with chunked approach

## Integration with Development Workflow

### Pre-Task Budget Check
```bash
# Before starting any significant task
npx claude-flow@alpha hooks pre-task --description "Authentication system"

# Run budget analysis (spawn planner agent)
# Agent performs budget assessment and creates execution plan

# Review plan
npx claude-flow@alpha memory retrieve --key "budget/execution-plan"

# Proceed with confidence or adjust scope
```

### Mid-Task Monitoring
```bash
# After each chunk
npx claude-flow@alpha hooks post-task --task-id "chunk-2" --tokens-used <actual>

# Check remaining budget
npx claude-flow@alpha memory retrieve --key "token-usage/current"

# Adjust remaining chunks if needed
```

### Post-Task Review
```bash
# After completion
npx claude-flow@alpha hooks post-task --task-id "auth-system" --success true

# Analyze accuracy
# Compare estimated vs actual for future improvements
```

## Success Metrics

- Budget adherence: 95%+ chunks within estimate
- Planning accuracy: ±20% estimation error
- Zero budget overruns: No tasks fail due to token exhaustion
- Optimal chunking: Max chunk utilization 40-60% of available
- Efficient execution: <15% unused budget per session

## Related Skills

- `when-optimizing-prompts-use-prompt-optimization-analyzer` - Reduce token waste
- `when-analyzing-skill-gaps-use-skill-gap-analyzer` - Portfolio optimization
- `task-orchestrator` - Multi-agent coordination

## Notes

- Run before large tasks (>20K token estimate)
- Always maintain 15% safety buffer
- Track actual vs estimated for learning
- Adjust chunking based on task type
- Store plans in memory for resumption
- Use checkpoints for long-running work
