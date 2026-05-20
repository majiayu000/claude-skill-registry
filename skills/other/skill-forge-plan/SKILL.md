---
name: skill-forge-plan
description: >
  Architecture and design planning for new Claude Code skills. Guides through
  use case definition, complexity tier selection, sub-skill decomposition,
  and file structure planning. Use when user says "plan skill", "design skill",
  "skill architecture", or "skill planning".
---

# Skill Architecture & Design Planning

## Process

### Step 1: Domain Discovery

Ask the user these questions (adapt based on context):

1. **What domain is this skill for?** (e.g., SEO, advertising, DevOps, data analysis)
2. **What are the top 2-3 use cases?** What should users be able to accomplish?
3. **What trigger phrases would users say?** List 5-10 natural language triggers.
4. **Does it need external tools?** MCP servers, APIs, CLI tools?
5. **Who is the target user?** Developer, marketer, analyst, general user?

### Step 2: Use Case Decomposition

For each use case, define:

```
Use Case: [Name]
Trigger: User says "[phrases]"
Steps:
1. [First action]
2. [Decision point or validation]
3. [Next action]
Result: [What success looks like]
Tools Needed: [built-in, MCP, scripts]
```

### Step 3: Complexity Tier Assessment

Evaluate based on answers:

| Signal | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|--------|--------|--------|--------|--------|
| Use cases | 1-2 | 2-3 | 4-8 | 8+ |
| Needs scripts? | No | Yes | Maybe | Yes |
| Sub-skills needed? | No | No | Yes | Yes |
| Parallel execution? | No | No | No | Yes |
| Reference docs? | No | Maybe | Yes | Yes |
| Industry templates? | No | No | Maybe | Yes |

**Decision matrix:**
- Single workflow, no scripts -> **Tier 1** (minimal)
- Needs deterministic validation -> **Tier 2** (workflow)
- Multiple distinct workflows -> **Tier 3** (multi-skill)
- Complex domain with parallel delegation -> **Tier 4** (ecosystem)

### Step 4: Architecture Design

Based on tier, generate the architecture:

**Tier 1 Output:**
```
skill-name/
  SKILL.md
```

**Tier 2 Output:**
```
skill-name/
  SKILL.md
  scripts/
    validate.py
    process.py
  references/
    domain-knowledge.md
```

**Tier 3 Output:**
```
skill-name/              # Main orchestrator
  SKILL.md
  references/
    shared-reference.md
skills/
  skill-name-sub1/
    SKILL.md
  skill-name-sub2/
    SKILL.md
```

**Tier 4 Output:**
```
skill-name/              # Main orchestrator
  SKILL.md
  references/
    ref1.md
    ref2.md
  scripts/
    script1.py
    script2.py
  assets/
    template1.md
    template2.md
skills/
  skill-name-sub1/
    SKILL.md
  skill-name-sub2/
    SKILL.md
  ...
agents/
  skill-name-role1.md
  skill-name-role2.md
```

### Step 5: Sub-Skill Decomposition (Tier 3-4 only)

For each sub-skill, define:
- **Name**: `{parent}-{function}` (kebab-case)
- **Responsibility**: Single, clear purpose
- **Inputs**: What it needs from the orchestrator
- **Outputs**: What it returns
- **Cross-references**: Other sub-skills or references it needs
- **Self-contained?**: Can it run independently or needs orchestration?

### Step 6: Routing Table

Design the command routing:

```markdown
| Command | Routes to | Purpose |
|---------|-----------|---------|
| /skill-name | main SKILL.md | Interactive mode |
| /skill-name sub1 | skills/skill-name-sub1/ | Sub-workflow 1 |
| /skill-name sub2 | skills/skill-name-sub2/ | Sub-workflow 2 |
```

### Step 7: Reference File Planning

Identify knowledge that should be extracted to reference files:
- Domain-specific rules and thresholds
- Industry templates
- API documentation
- Quality gates and validation criteria

Rule of thumb: If information is >50 lines and only needed for specific sub-workflows,
extract it to `references/`.

### Step 8: Generate Plan Document

Create a structured plan document:

```markdown
# Skill Plan: [name]

## Overview
- Domain: [domain]
- Tier: [1-4]
- Sub-skills: [count]
- Scripts: [count]

## Use Cases
[list from Step 2]

## Architecture
[diagram from Step 4]

## Sub-Skills
[details from Step 5]

## Routing
[table from Step 6]

## Reference Files
[list from Step 7]

## Next Steps
Run `/skill-forge build [name]` to scaffold the skill.
```

## Examples

### Example: Planning a DevOps Skill

User: "I want to create a skill for managing Docker containers and Kubernetes deployments"

Discovery reveals:
- 6 use cases (container management, K8s deploy, monitoring, logs, scaling, troubleshooting)
- Needs scripts for kubectl and docker commands
- Multiple distinct workflows
- Cross-references between monitoring and troubleshooting

Assessment: **Tier 3** (multi-skill orchestrator)

Architecture:
```
devops/                     # Main orchestrator
  SKILL.md
  scripts/
    health_check.py         # Cluster health check
    log_parser.py           # Log analysis
  references/
    k8s-patterns.md         # Deployment patterns
    docker-best-practices.md
skills/
  devops-docker/SKILL.md  # Container management
  devops-k8s/SKILL.md     # Kubernetes deployments
  devops-monitor/SKILL.md # Monitoring and alerts
  devops-logs/SKILL.md    # Log analysis
  devops-scale/SKILL.md   # Scaling strategies
  devops-fix/SKILL.md     # Troubleshooting
```
