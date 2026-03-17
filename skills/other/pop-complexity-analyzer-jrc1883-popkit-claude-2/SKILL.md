---
name: complexity-analyzer
description: "Analyzes task/feature complexity (1-10) and recommends subtask breakdown for planning and prioritization. Provides actionable recommendations for agent selection, phase distribution, and risk assessment. Silent analysis that feeds into other workflows."
inputs:
  - from: any
    field: task_description
    required: true
  - from: any
    field: metadata
    required: false
outputs:
  - field: complexity_score
    type: number
  - field: recommended_subtasks
    type: number
  - field: phase_distribution
    type: object
  - field: analysis_report
    type: file_path
next_skills:
  - pop-writing-plans
  - pop-brainstorming
  - pop-executing-plans
workflow:
  id: complexity-analysis
  name: Complexity Analysis Workflow
  version: 1
  description: Analyze task complexity and provide recommendations
  steps:
    - id: extract_context
      description: Extract task description and metadata
      type: analysis
      next: calculate_complexity
    - id: calculate_complexity
      description: Calculate complexity score and factors
      type: analysis
      next: generate_recommendations
    - id: generate_recommendations
      description: Generate subtask and phase recommendations
      type: analysis
      next: output_results
    - id: output_results
      description: Output analysis results
      type: output
      next: complete
    - id: complete
      description: Analysis complete
      type: terminal
---

# Complexity Analysis Engine

## Overview

Analyzes task and feature complexity using multiple factors to provide 1-10 scoring with actionable recommendations. This is a **foundational skill** used by other PopKit workflows.

**Automatic integration:** This skill is automatically invoked by planning workflows, PRD parsers, and agent routers. It operates silently in the background to provide complexity intelligence.

## Complexity Scoring (1-10)

| Score | Level        | Description                       | Example                             |
| ----- | ------------ | --------------------------------- | ----------------------------------- |
| 1-2   | Trivial      | Single file, minimal changes      | Fix typo, update constant           |
| 3-4   | Simple       | Few files, straightforward logic  | Add button, update styling          |
| 5-6   | Moderate     | Multiple files, some complexity   | Add form validation, API endpoint   |
| 7-8   | Complex      | Architecture changes, high impact | Refactor module, add auth system    |
| 9-10  | Very Complex | System-wide changes, high risk    | Migrate architecture, redesign core |

## Complexity Factors

The analyzer evaluates 8 factors with configurable weights:

| Factor              | Weight | Description                       |
| ------------------- | ------ | --------------------------------- |
| Files Affected      | 15%    | Number of files that need changes |
| LOC Estimate        | 15%    | Estimated lines of code           |
| Dependencies        | 15%    | External/internal dependencies    |
| Architecture Change | 20%    | Impact on system architecture     |
| Breaking Changes    | 15%    | Compatibility impact              |
| Testing Complexity  | 10%    | Testing requirements              |
| Security Impact     | 5%     | Security considerations           |
| Integration Points  | 5%     | External integrations             |

## Usage Patterns

### 1. Automatic Analysis (Preferred)

Complexity analysis is automatically performed when you use development workflows:

```bash
/popkit:dev "Add user authentication"
# Automatically analyzes complexity
# Displays: "Analyzing complexity... Score: 7/10 (Complex)"
# Recommends: "5-7 subtasks suggested"
# Selects appropriate agents based on complexity
```

### 2. Explicit Analysis

```bash
/popkit:dev analyze "Refactor database layer"
```

### 3. From Skills (Python)

```python
from popkit_shared.utils.complexity_scoring import analyze_complexity

# Analyze a task
result = analyze_complexity(
    "Add real-time notifications with WebSockets",
    metadata={
        "files_affected": 8,
        "dependencies": 5
    }
)

# Access results
score = result["complexity_score"]  # 7
subtasks = result["recommended_subtasks"]  # 6
phases = result["phase_distribution"]  # {"planning": 2, "implementation": 4, ...}
risks = result["risk_factors"]  # ["integration_complexity", "architecture_impact"]
agents = result["suggested_agents"]  # ["code-architect", "refactoring-expert"]
```

### 4. Integration with Skill Context

```python
from popkit_shared.utils.skill_context import save_skill_context, SkillOutput
from popkit_shared.utils.complexity_scoring import analyze_complexity

# Analyze complexity
result = analyze_complexity(task_description)

# Save for downstream skills
save_skill_context(SkillOutput(
    skill_name="pop-complexity-analyzer",
    status="completed",
    output={
        "complexity_score": result["complexity_score"],
        "recommended_subtasks": result["recommended_subtasks"],
        "phase_distribution": result["phase_distribution"],
        "risk_factors": result["risk_factors"],
        "suggested_agents": result["suggested_agents"]
    },
    artifacts=[],
    next_suggested="pop-writing-plans"
))
```

## Output Format

```json
{
  "complexity_score": 7,
  "complexity_level": "COMPLEX",
  "recommended_subtasks": 6,
  "phase_distribution": {
    "discovery": 1,
    "planning": 2,
    "implementation": 4,
    "testing": 2,
    "review": 1,
    "integration": 1
  },
  "risk_factors": ["architecture_impact", "security_critical"],
  "reasoning": "Complexity Score: 7/10 (Architecture changes, high impact)...",
  "suggested_agents": ["code-architect", "refactoring-expert", "security-auditor"]
}
```

## Integration Points

### 1. Agent Router

```python
from popkit_shared.utils.complexity_scoring import quick_score

task = "Refactor authentication module"
complexity = quick_score(task)

if complexity >= 8:
    agent = "code-architect"  # Senior agent for complex tasks
elif complexity >= 5:
    agent = "refactoring-expert"
else:
    agent = "rapid-prototyper"
```

### 2. PRD Parser

```python
features = parse_prd(document)
for feature in features:
    complexity = analyze_complexity(feature.description)
    feature.complexity_score = complexity["complexity_score"]
    feature.subtasks_recommended = complexity["recommended_subtasks"]

# Sort by complexity (tackle simple features first)
features.sort(key=lambda f: f.complexity_score)
```

### 3. Planning Workflows

```python
complexity_result = analyze_complexity(task_description)
score = complexity_result["complexity_score"]

if score <= 4:
    workflow = "quick_mode"  # 5 steps
elif score <= 7:
    workflow = "standard_mode"  # 7 phases
else:
    workflow = "full_mode_with_architecture"
```

## Subtask Recommendations

| Complexity | Subtasks | Strategy            |
| ---------- | -------- | ------------------- |
| 1-2        | 1        | Single task         |
| 3-4        | 2-3      | Simple breakdown    |
| 5-6        | 3-5      | Moderate breakdown  |
| 7-8        | 5-7      | Detailed breakdown  |
| 9-10       | 8-12     | Extensive breakdown |

## Phase Distribution

**Trivial (1-2):** Implementation: 1, Testing: 1

**Simple (3-4):** Planning: 1, Implementation: 2, Testing: 1

**Moderate (5-6):** Planning: 1, Implementation: 3, Testing: 2, Review: 1

**Complex (7-8):** Discovery: 1, Planning: 2, Implementation: 4, Testing: 2, Review: 1, Integration: 1

**Very Complex (9-10):** Discovery: 2, Architecture: 2, Planning: 3, Implementation: 5, Testing: 3, Review: 2, Integration: 2, Documentation: 1

## Risk Factor Detection

| Risk Factor            | Trigger                  | Impact                 |
| ---------------------- | ------------------------ | ---------------------- |
| breaking_changes       | Breaking change keywords | Compatibility issues   |
| security_critical      | Auth/security keywords   | Security review needed |
| architecture_impact    | Architecture keywords    | Design review required |
| integration_complexity | Integration keywords     | External coordination  |
| performance_sensitive  | Performance keywords     | Performance testing    |
| data_migration         | Migration keywords       | Data safety concerns   |

## Agent Recommendations

| Complexity | Suggested Agents                                             |
| ---------- | ------------------------------------------------------------ |
| 1-3        | rapid-prototyper, code-explorer                              |
| 4-6        | refactoring-expert, code-explorer, test-writer               |
| 7-8        | code-architect, refactoring-expert, security-auditor         |
| 9-10       | code-architect, system-designer, tech-lead, security-auditor |

## Keyword Detection

**Architecture:** architecture, refactor, redesign, restructure, migrate
**Breaking Changes:** breaking, incompatible, migration, deprecated
**Security:** auth, authentication, authorization, security, crypto, encryption
**Integration:** integrate, api, webhook, third-party, external
**Database:** database, schema, migration, query, index
**Testing:** e2e, integration test, test coverage, regression

## Best Practices

1. **Automatic by Default:** Let workflows invoke complexity analysis automatically
2. **Trust the Score:** Complexity scores are calibrated for accuracy
3. **Use Recommendations:** Follow subtask and phase recommendations
4. **Monitor Risks:** Pay attention to identified risk factors
5. **Right-Size Agents:** Use suggested agents for better results
6. **Iterate if Needed:** Re-analyze after scope changes

## Related Skills

- `pop-writing-plans` - Uses complexity for plan generation
- `pop-brainstorming` - Uses complexity to determine depth
- `pop-executing-plans` - Uses complexity for batch sizing

## Related Commands

- `/popkit:dev` - Automatic complexity analysis
- `/popkit:issue` - Complexity-based prioritization
- `/popkit:milestone` - Aggregate complexity reporting
