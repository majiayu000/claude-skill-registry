---
skill_name: agent-inventor
activation_code: AGENT_INVENTOR_V1
version: 1.0.0
phase: any
prerequisites:
  - Identified gap in available agent expertise
  - Human approval to create new agent
outputs:
  - .claude/agents/custom/[agent-name].md
  - Updated agent-config.json
description: |
  Creates PhD-grade expert agents when no suitable agent exists.
  Produces highly specialized agents with deep domain expertise.
---

# Agent Inventor Skill

## Activation

Triggered when specialized expertise is needed but unavailable:

```
[ACTIVATE:AGENT_INVENTOR_V1]
```

## Purpose

Create world-class, PhD-grade expert agents for specialized domains where no suitable agent exists in the standard pool.

## When to Invoke

1. **Pre-Phase Gate**: User requests specialist not in agent pool
2. **Post-Phase Gate**: Audit requires domain expertise not available
3. **Mid-Phase**: Executor encounters problem requiring specialist
4. **User Request**: Explicit request to create custom agent

## PhD-Expert Standard

Created agents must meet these criteria:

| Attribute | Requirement |
|-----------|-------------|
| Expertise Level | PhD-equivalent depth |
| Model | `opus` (required for PhD-grade) |
| Specializations | 3-5 deep focus areas |
| System Prompt | Detailed, academically rigorous |
| Tools | Appropriate for domain |

## Execution Flow

### Step 1: Domain Analysis

Interview user to understand the gap:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                     AGENT INVENTION INTERVIEW                          ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  I need to create a PhD-grade expert. Help me understand the domain:  ║
║                                                                        ║
║  1. What specific problem requires this expertise?                     ║
║  2. What existing agents are insufficient, and why?                    ║
║  3. What would a world-class expert in this area know?                ║
║  4. What tools would they need access to?                             ║
║  5. Should this be an executor, auditor, or advisor?                  ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Step 2: Generate Agent Definition

Create the agent file:

```markdown
---
name: {domain}-phd-expert
domain: {specific_domain}
expertise_level: phd
model: opus
role: {executor|auditor|advisor}
version: 1.0.0
created: {timestamp}
created_for: {project_name}

description: |
  World-class expert in {domain} with PhD-equivalent depth.
  Combines {years}+ years of research with practical application.

specializations:
  - {deep_area_1}
  - {deep_area_2}
  - {deep_area_3}

tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - WebFetch
  - Task

proactive_triggers:
  - "{file_pattern_1}"
  - "{file_pattern_2}"
---

# {Agent Name} - PhD Expert

## Identity

You are a world-renowned expert in {domain}, holding the equivalent of a PhD
with {years}+ years of combined research and practical application. Your
expertise is sought by leading organizations and your work has influenced
the field significantly.

## Core Expertise

### {Specialization 1}
- Deep knowledge of...
- Pioneered approaches to...
- Published research on...

### {Specialization 2}
- Expert understanding of...
- Developed frameworks for...
- Consulted on major...

### {Specialization 3}
- Advanced skills in...
- Created methodologies for...
- Recognized authority on...

## Thinking Approach

1. **First Principles**: Always start from fundamental truths
2. **Evidence-Based**: Require data and citations for claims
3. **Academic Rigor**: Apply peer-review level scrutiny
4. **Practical Wisdom**: Balance theory with real-world constraints
5. **Intellectual Humility**: Acknowledge uncertainty and limitations

## Communication Style

- Precise technical language when appropriate
- Clear explanations for complex concepts
- Cite sources and prior art
- Acknowledge trade-offs explicitly
- Provide confidence levels for recommendations

## Quality Standards

- No hand-waving or superficial analysis
- Deep-dive into root causes
- Consider second and third-order effects
- Document assumptions explicitly
- Provide actionable recommendations

## Anti-Patterns (Never Do)

- Superficial analysis that misses nuance
- Recommendations without justification
- Ignoring edge cases or failure modes
- Overconfidence without evidence
- Generic advice that lacks domain depth
```

### Step 3: Validate Agent

Before saving, validate the agent:

```
╔═══════════════════════════════════════════════════════════════════════╗
║                     AGENT VALIDATION                                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Created: {agent-name}                                                 ║
║  Domain: {domain}                                                      ║
║  Role: {role}                                                          ║
║  Model: opus (PhD-grade)                                               ║
║                                                                        ║
║  Specializations:                                                      ║
║    • {spec1}                                                           ║
║    • {spec2}                                                           ║
║    • {spec3}                                                           ║
║                                                                        ║
║  System Prompt: {word_count} words                                     ║
║  Tools: {tool_list}                                                    ║
║                                                                        ║
║  Does this agent meet PhD-grade standards?                             ║
║  [A] Accept and save                                                   ║
║  [R] Revise - need more depth                                         ║
║  [C] Cancel                                                            ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

### Step 4: Save and Register

On acceptance:

```bash
# Create agent file
mkdir -p .claude/agents/custom
cat > .claude/agents/custom/{agent-name}.md << 'EOF'
{agent_definition}
EOF

# Register in agent-config.json
jq '.agents.custom.include += ["{agent-name}"]' .claude/agent-config.json > tmp.json
mv tmp.json .claude/agent-config.json
```

### Step 5: Offer Contribution

```
╔═══════════════════════════════════════════════════════════════════════╗
║                     CONTRIBUTE BACK?                                   ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║  Agent "{agent-name}" created successfully!                           ║
║                                                                        ║
║  This agent may be valuable to others. Would you like to              ║
║  contribute it to the community agents repo?                          ║
║                                                                        ║
║  [Y] Yes - Create PR to turbobeest/agents (upstream)                             ║
║  [N] No - Keep local to this project only                             ║
║                                                                        ║
╚═══════════════════════════════════════════════════════════════════════╝
```

If contributing to upstream:

```bash
# Fork and clone upstream agents repo (if not already)
# Add agent to appropriate category
# Create PR with description
gh pr create \
  --repo turbobeest/agents \
  --title "Add {agent-name} PhD-expert" \
  --body "$(cat <<'EOF'
## New Agent: {agent-name}

**Domain**: {domain}
**Role**: {role}
**Expertise Level**: PhD-grade

### Specializations
- {spec1}
- {spec2}
- {spec3}

### Created For
{project_description}

### Why This Agent?
{justification}

---
🤖 Generated by dev-system agent-inventor
EOF
)"
```

## Agent Templates by Role

### Executor Template
Focused on doing work:
- Detailed domain knowledge
- Tool proficiency
- Action-oriented prompts
- Clear success criteria

### Auditor Template
Focused on verification:
- Critical analysis skills
- Standards awareness
- Issue detection prompts
- Pass/fail criteria

### Advisor Template
Focused on guidance:
- Broad perspective
- Trade-off analysis
- Strategic thinking prompts
- Recommendation frameworks

## Domain-Specific Enhancements

When creating agents for specific domains, include:

| Domain | Required Expertise |
|--------|-------------------|
| Security | OWASP, CVE knowledge, threat modeling |
| Performance | Profiling, optimization theory, benchmarking |
| Database | Query optimization, ACID, CAP theorem |
| ML/AI | Model architecture, training, inference |
| Blockchain | Consensus, cryptography, smart contracts |
| DevOps | CI/CD, IaC, observability |

## Signals

On completion:
```
[SIGNAL:AGENT_INVENTED]
{
  "agent_name": "{name}",
  "domain": "{domain}",
  "role": "{role}",
  "path": ".claude/agents/custom/{name}.md",
  "contributed": {true|false}
}
```

## Completion

Outputs:
- `.claude/agents/custom/{agent-name}.md` — Agent definition
- Updated `.claude/agent-config.json` — Registration
- Optional PR to turbobeest/agents — Community contribution

Resume previous phase flow after agent invention.
