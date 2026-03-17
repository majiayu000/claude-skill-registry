---
name: auto-routing
version: 1.0.0
description: Intelligent agent routing and topology selection based on task characteristics
author: Investment Analysis Platform
category: orchestration
tags: [routing, agents, topology, swarms, coordination]
invocable: false
---

# Auto-Routing Skill

Intelligent routing of tasks to optimal agents and swarms based on task characteristics, file patterns, and workflow context.

## Overview

This skill provides:
- **Keyword-Based Routing**: Match task keywords to specialized agents
- **File Pattern Routing**: Route based on file paths being modified
- **Topology Selection**: Choose optimal coordination topology
- **Swarm Configuration**: Configure multi-agent swarm execution
- **Load Balancing**: Distribute work across available agents

## Routing Algorithms

### 1. Keyword Pattern Matching

Match task descriptions to agent specializations:

```javascript
const keywordPatterns = {
  "investment-analysis": {
    pattern: /underwrite|credit|loan|collateral|lien|ucc|security.package/i,
    agents: ["deal-underwriter", "investment-analyst"],
    priority: 1
  },
  "financial-modeling": {
    pattern: /dcf|lbo|valuation|model|projection|scenario|sensitivity/i,
    agents: ["financial-modeler"],
    priority: 1
  },
  "portfolio-risk": {
    pattern: /stock|portfolio|risk|var|sharpe|sortino|beta|drawdown|volatility/i,
    agents: ["financial-analysis-swarm", "risk-assessor", "portfolio-manager"],
    priority: 1
  },
  "infrastructure": {
    pattern: /docker|kubernetes|k8s|deploy|ci.?cd|github.?actions|pipeline|prometheus|grafana/i,
    agents: ["infrastructure-devops-swarm"],
    priority: 2
  },
  "backend": {
    pattern: /api|endpoint|fastapi|rest|graphql|database|postgres|timescale|redis|celery/i,
    agents: ["backend-api-swarm"],
    priority: 2
  },
  "frontend": {
    pattern: /react|component|dashboard|chart|visualization|ui|ux|material.?ui/i,
    agents: ["ui-visualization-swarm"],
    priority: 2
  },
  "data-ml": {
    pattern: /etl|pipeline|airflow|dag|ml|model|training|prophet|xgboost|feature/i,
    agents: ["data-ml-pipeline-swarm", "data-science-architect"],
    priority: 2
  },
  "quality": {
    pattern: /test|coverage|pytest|jest|e2e|integration|unit|quality|lint/i,
    agents: ["project-quality-swarm", "tdd-guide", "e2e-runner"],
    priority: 3
  },
  "security": {
    pattern: /security|vulnerability|audit|compliance|gdpr|sec|permission|access/i,
    agents: ["security-compliance-swarm", "security-reviewer"],
    priority: 2
  }
};
```

### 2. File Pattern Routing

Route tasks based on file paths:

```javascript
const filePatterns = {
  "backend/**/*.py": "backend-api-swarm",
  "backend/api/**/*.py": "backend-api-swarm",
  "backend/services/**/*.py": "backend-api-swarm",
  "frontend/**/*.tsx": "ui-visualization-swarm",
  "frontend/**/*.ts": "ui-visualization-swarm",
  "frontend/web/src/**/*.tsx": "ui-visualization-swarm",
  "backend/ml/**/*.py": "data-ml-pipeline-swarm",
  "data_pipelines/**": "data-ml-pipeline-swarm",
  "**/financial/**": "financial-analysis-swarm",
  "backend/analysis/**/*.py": "financial-analysis-swarm",
  "infrastructure/**": "infrastructure-devops-swarm",
  "docker-compose*.yml": "infrastructure-devops-swarm",
  "Dockerfile*": "infrastructure-devops-swarm",
  ".github/workflows/**": "infrastructure-devops-swarm",
  "**/*.test.ts": "project-quality-swarm",
  "**/*.test.tsx": "project-quality-swarm",
  "**/tests/**": "project-quality-swarm"
};
```

### 3. Topology Selection

Select optimal topology based on task characteristics:

```javascript
function selectTopology(task) {
  const factors = {
    complexity: assessComplexity(task),      // 1-4
    agentCount: estimateAgentCount(task),    // 1-4
    coordinationNeeds: assessCoordination(task), // 1-4
    parallelism: assessParallelism(task)     // 1-4
  };

  const score =
    factors.complexity * 0.30 +
    factors.agentCount * 0.25 +
    factors.coordinationNeeds * 0.25 +
    factors.parallelism * 0.20;

  if (score <= 1.5) return "star";
  if (score <= 2.5) return "mesh";
  if (score <= 3.5) return "hierarchical";
  return "hive_mind";
}
```

**Topology Characteristics**:

| Topology | Coordination | Communication | Fault Tolerance | Best For |
|----------|--------------|---------------|-----------------|----------|
| Star | Centralized | Hub-spoke | Low | Planning, simple routing |
| Mesh | Distributed | Peer-to-peer | High | Complex implementation |
| Hierarchical | Layered | Top-down | Moderate | Code review, releases |
| Parallel | Minimal | Aggregated | High | Multiple reviewers |
| Hive Mind | Collective | Broadcast | Very High | Complex problem solving |

### 4. Swarm Configuration

Configure swarms for multi-agent execution:

```javascript
const swarmConfigs = {
  "infrastructure-devops-swarm": {
    topology: "hierarchical",
    coordinator: "infrastructure-devops-swarm",
    subAgents: ["security-agent", "infrastructure-agent"],
    memoryNamespace: "infrastructure"
  },
  "financial-analysis-swarm": {
    topology: "hive_mind",
    coordinator: "queen-investment-orchestrator",
    subAgents: ["investment-analyst", "deal-underwriter", "financial-modeler", "risk-assessor", "portfolio-manager"],
    memoryNamespace: "investment-analysis",
    consensusProtocol: "raft"
  },
  "code-review-swarm": {
    topology: "parallel",
    coordinator: "project-quality-swarm",
    subAgents: ["security-reviewer", "code-reviewer", "code-analyzer", "performance-optimizer"],
    aggregationStrategy: "merge_findings"
  }
};
```

## Routing Decision Flow

```
Task Received
    │
    ▼
┌─────────────────────────┐
│ 1. Parse Task Keywords  │
│    Match against patterns│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 2. Identify File Patterns│
│    Route by file paths   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 3. Select Topology      │
│    Based on complexity   │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 4. Configure Swarm      │
│    Set coordinator, agents│
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ 5. Execute with Selected│
│    Configuration         │
└─────────────────────────┘
```

## Command Routing

Map commands to agents:

```javascript
const commandRouting = {
  // Investment Commands
  "/underwrite": { agent: "deal-underwriter", model: "opus" },
  "/model": { agent: "financial-modeler", model: "opus" },
  "/analyze-structure": { agent: "deal-underwriter", model: "opus" },
  "/scenario": { agent: "financial-modeler", model: "opus" },
  "/stock-analysis": { agent: "financial-analysis-swarm", model: "opus" },

  // Development Commands
  "/plan": { agent: "planner", model: "opus" },
  "/build-fix": { agent: "build-error-resolver", model: "opus" },
  "/code-review": { agent: "code-reviewer", model: "opus" },
  "/tdd": { agent: "tdd-guide", model: "opus" },
  "/e2e": { agent: "e2e-runner", model: "opus" },

  // Infrastructure Commands
  "/docker": { agent: "infrastructure-devops-swarm", model: "opus" },
  "/deploy": { agent: "infrastructure-devops-swarm", model: "opus" },

  // GitHub Commands
  "/github-swarm": { agent: "github-swarm-coordinator", model: "opus" }
};
```

## Model Selection

Route to appropriate model based on task:

```javascript
const modelRouting = {
  opus: {
    useFor: [
      "Complex architectural decisions",
      "Financial modeling and analysis",
      "Security reviews",
      "Code reviews",
      "Orchestration"
    ],
    agents: [
      "queen-investment-orchestrator",
      "investment-analyst",
      "deal-underwriter",
      "architect",
      "code-reviewer",
      "security-reviewer"
    ]
  },
  sonnet: {
    useFor: [
      "General development",
      "Testing",
      "Documentation",
      "Issue triage"
    ],
    agents: ["coder", "tester", "doc-updater", "issue-triager"]
  },
  haiku: {
    useFor: [
      "Lightweight frequent tasks",
      "Simple queries",
      "Status checks"
    ],
    agents: []
  }
};
```

## Load Balancing

Distribute work across agents:

```javascript
function loadBalance(task, availableAgents) {
  const strategy = "least_loaded"; // or "round_robin", "weighted"

  switch (strategy) {
    case "least_loaded":
      return availableAgents.sort((a, b) =>
        a.currentLoad - b.currentLoad
      )[0];

    case "round_robin":
      return availableAgents[nextIndex++ % availableAgents.length];

    case "weighted":
      return weightedSelect(availableAgents, task.complexity);
  }
}
```

## Fallback Routing

When no specific route matches:

```javascript
const fallbackConfig = {
  agent: "team-coordinator",
  model: "opus",
  description: "Routes unknown tasks to team coordinator for optimal agent selection"
};
```

## Usage

This skill is used internally by the workflow engine and agent orchestration system. It is not directly invocable but provides routing logic for:

1. `/workflow` command phase execution
2. Direct swarm invocation
3. Automatic agent spawning
4. Dynamic topology switching

## Configuration

Routing configuration is stored in:
- `.claude/config/agent-registry.json` - Agent and command routing
- `.claude/config/topology-rules.json` - Topology selection rules
- `.claude/config/workflow-engine.json` - Phase routing

## Related Components

- `team-coordinator` agent - Master routing
- `smart-agent` agent - Dynamic spawning
- `topology-optimizer` agent - Topology optimization
- `workflow-engine.json` - Phase configuration
