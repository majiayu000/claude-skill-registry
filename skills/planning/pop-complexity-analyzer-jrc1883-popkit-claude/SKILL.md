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

For standalone complexity analysis:

```bash
/popkit:dev analyze "Refactor database layer"
```

### 3. From Skills (Python)

Skills can invoke complexity analysis programmatically:

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

Save complexity analysis for downstream skills:

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

The analyzer produces structured JSON output:

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
  "reasoning": "Complexity Score: 7/10 (Architecture changes, high impact). Primary factors: architecture changes required, external dependencies, security considerations. This is a complex task requiring architectural consideration.",
  "factors": {
    "files_affected": 60.0,
    "loc_estimate": 50.0,
    "dependencies": 50.0,
    "architecture_change": 100.0,
    "breaking_changes": 0.0,
    "testing_complexity": 50.0,
    "security_impact": 100.0,
    "integration_points": 0.0
  },
  "estimated_tokens": {
    "discovery": 5000,
    "planning": 12000,
    "implementation": 35000,
    "testing": 10000,
    "review": 6000,
    "total": 68000
  },
  "suggested_agents": ["code-architect", "refactoring-expert", "security-auditor"]
}
```

## Integration Points

### 1. Agent Router

The agent router uses complexity scores to select appropriate agents:

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

PRD parser uses complexity for feature prioritization:

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

Planning workflows use complexity to determine approach:

```python
complexity_result = analyze_complexity(task_description)
score = complexity_result["complexity_score"]

if score <= 4:
    # Use quick mode (5 steps)
    workflow = "quick_mode"
elif score <= 7:
    # Use standard mode (7 phases)
    workflow = "standard_mode"
else:
    # Use full planning mode with architecture review
    workflow = "full_mode_with_architecture"
```

### 4. Merge Conflict Resolver

Complexity scores prioritize conflict resolution:

```python
conflicts = detect_conflicts()
for conflict in conflicts:
    complexity = analyze_complexity(conflict.description)
    conflict.priority = complexity["complexity_score"]

# Resolve highest complexity conflicts first
conflicts.sort(key=lambda c: c.priority, reverse=True)
```

## Subtask Recommendations

Based on complexity score, the analyzer suggests subtask counts:

| Complexity | Subtasks | Strategy            |
| ---------- | -------- | ------------------- |
| 1-2        | 1        | Single task         |
| 3-4        | 2-3      | Simple breakdown    |
| 5-6        | 3-5      | Moderate breakdown  |
| 7-8        | 5-7      | Detailed breakdown  |
| 9-10       | 8-12     | Extensive breakdown |

## Phase Distribution

The analyzer recommends phase distribution for task planning:

**Trivial (1-2):**

- Implementation: 1
- Testing: 1

**Simple (3-4):**

- Planning: 1
- Implementation: 2
- Testing: 1

**Moderate (5-6):**

- Planning: 1
- Implementation: 3
- Testing: 2
- Review: 1

**Complex (7-8):**

- Discovery: 1
- Planning: 2
- Implementation: 4
- Testing: 2
- Review: 1
- Integration: 1

**Very Complex (9-10):**

- Discovery: 2
- Architecture: 2
- Planning: 3
- Implementation: 5
- Testing: 3
- Review: 2
- Integration: 2
- Documentation: 1

## Risk Factor Detection

The analyzer identifies potential risks:

| Risk Factor            | Trigger                  | Impact                 |
| ---------------------- | ------------------------ | ---------------------- |
| breaking_changes       | Breaking change keywords | Compatibility issues   |
| security_critical      | Auth/security keywords   | Security review needed |
| architecture_impact    | Architecture keywords    | Design review required |
| integration_complexity | Integration keywords     | External coordination  |
| performance_sensitive  | Performance keywords     | Performance testing    |
| data_migration         | Migration keywords       | Data safety concerns   |

## Token Estimation

The analyzer estimates token usage for planning:

| Complexity | Total Tokens | Planning | Implementation | Testing |
| ---------- | ------------ | -------- | -------------- | ------- |
| 1-2        | 7,000        | 2,000    | 5,000          | -       |
| 3-4        | 17,000       | 4,000    | 10,000         | 3,000   |
| 5-6        | 38,000       | 8,000    | 20,000         | 6,000   |
| 7-8        | 68,000       | 12,000   | 35,000         | 10,000  |
| 9-10       | 135,000      | 20,000   | 60,000         | 20,000  |

## Agent Recommendations

Based on complexity, appropriate agents are suggested:

| Complexity | Suggested Agents                                             |
| ---------- | ------------------------------------------------------------ |
| 1-3        | rapid-prototyper, code-explorer                              |
| 4-6        | refactoring-expert, code-explorer, test-writer               |
| 7-8        | code-architect, refactoring-expert, security-auditor         |
| 9-10       | code-architect, system-designer, tech-lead, security-auditor |

## Keyword Detection

The analyzer uses keyword detection to identify complexity factors:

**Architecture:** architecture, refactor, redesign, restructure, migrate
**Breaking Changes:** breaking, incompatible, migration, deprecated
**Security:** auth, authentication, authorization, security, crypto, encryption
**Integration:** integrate, api, webhook, third-party, external
**Database:** database, schema, migration, query, index
**Testing:** e2e, integration test, test coverage, regression

## Customization

Custom weights can be provided for specific use cases:

```python
from popkit_shared.utils.complexity_scoring import ComplexityAnalyzer

# Custom weights (must sum to ~1.0)
custom_weights = {
    "files_affected": 0.10,
    "loc_estimate": 0.10,
    "dependencies": 0.10,
    "architecture_change": 0.30,  # Emphasize architecture
    "breaking_changes": 0.20,     # Emphasize compatibility
    "testing_complexity": 0.10,
    "security_impact": 0.05,
    "integration_points": 0.05
}

analyzer = ComplexityAnalyzer(weights=custom_weights)
result = analyzer.analyze("Refactor core module")
```

## Best Practices

1. **Automatic by Default:** Let workflows invoke complexity analysis automatically
2. **Trust the Score:** Complexity scores are calibrated for accuracy
3. **Use Recommendations:** Follow subtask and phase recommendations
4. **Monitor Risks:** Pay attention to identified risk factors
5. **Right-Size Agents:** Use suggested agents for better results
6. **Iterate if Needed:** Re-analyze after scope changes

## Examples

### Example 1: Simple Task

```python
result = analyze_complexity("Update button color in settings")

# Result:
# complexity_score: 2
# recommended_subtasks: 1
# phase_distribution: {"implementation": 1, "testing": 1}
# risk_factors: []
# suggested_agents: ["rapid-prototyper"]
```

### Example 2: Moderate Task

```python
result = analyze_complexity("Add user profile page with avatar upload")

# Result:
# complexity_score: 5
# recommended_subtasks: 4
# phase_distribution: {"planning": 1, "implementation": 3, "testing": 2, "review": 1}
# risk_factors: []
# suggested_agents: ["refactoring-expert", "code-explorer"]
```

### Example 3: Complex Task

```python
result = analyze_complexity("Implement JWT authentication with refresh tokens")

# Result:
# complexity_score: 7
# recommended_subtasks: 6
# phase_distribution: {"discovery": 1, "planning": 2, "implementation": 4, "testing": 2, "review": 1, "integration": 1}
# risk_factors: ["security_critical"]
# suggested_agents: ["code-architect", "refactoring-expert", "security-auditor"]
```

### Example 4: Very Complex Task

```python
result = analyze_complexity("Migrate monolith to microservices architecture")

# Result:
# complexity_score: 10
# recommended_subtasks: 12
# phase_distribution: {"discovery": 2, "architecture": 2, "planning": 3, "implementation": 5, "testing": 3, "review": 2, "integration": 2, "documentation": 1}
# risk_factors: ["breaking_changes", "architecture_impact", "integration_complexity"]
# suggested_agents: ["code-architect", "system-designer", "tech-lead", "security-auditor"]
```

## Future Enhancements

- **Machine Learning:** Train on historical task data for improved accuracy
- **Project Context:** Consider project-specific factors (team size, tech stack)
- **Historical Calibration:** Adjust scoring based on actual task completion times
- **Dependency Graph:** Analyze task dependencies for better sequencing
- **Resource Estimation:** Estimate time and resources beyond token usage

## Related Skills

- `pop-writing-plans` - Uses complexity for plan generation
- `pop-brainstorming` - Uses complexity to determine depth
- `pop-executing-plans` - Uses complexity for batch sizing

## Related Commands

- `/popkit:dev` - Automatic complexity analysis
- `/popkit:issue` - Complexity-based prioritization
- `/popkit:milestone` - Aggregate complexity reporting
