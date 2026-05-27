---
name: component-research
description: This skill should be used when the user asks to "evaluate if TBC covers
  a use case", "decide which TBC component to use", "check if a TBC template fits",
  "research TBC capabilities", "find the right TBC template", "analyze if custom step
  is needed", "compare TBC templates", or needs to determine whether To-Be-Continuous
  framework components can solve a CI/CD requirement before generating configuration.
version: 1.0.0
---

# TBC Component Research

Process for determining if a To-Be-Continuous (TBC) component fits a use case or requires customization.

## Flow 

Research → Evaluate → AskUserQuestion → User selects → Proceed

## Purpose

This skill provides a systematic research process to evaluate TBC framework capabilities against user requirements. Use this BEFORE generating any configuration to ensure the correct solution path.

## When to Use

- Before generating `.gitlab-ci.yml` with TBC
- When user requests functionality that may or may not be covered by TBC
- When deciding between TBC template, variant, or custom solution
- When user asks for something and the approach needs validation

## Solution Priority Hierarchy

**ALWAYS follow this priority order. Higher priority = preferred solution.**

| Priority | Solution | When to Use |
|----------|----------|-------------|
| 1 (Highest) | TBC template direct | Template inputs cover use case 100% |
| 2 | Template + existing variant | Template needs authentication/secrets variant |
| 3 | Variant from other template | Another template has variant that fits |
| 4 | New component | Create new TBC template |
| 5 | New component + variant | Create new template with variant |
| 6 (Lowest) | Custom step | **ONLY after exhausting 1-5** |

**Key Principle:** The user may request a solution (e.g., "custom script") but be incorrect. This process disciplines correct framework usage by evaluating ALL options before accepting user's proposed approach.

## Decision Process Overview

```
User Request
    │
    ▼
╔═══════════════════════════════════════════╗
║  IDENTIFY CORE NEED (MANDATORY FIRST)     ║
║  Invoke identify-core-need skill          ║
╚═══════════════════════════════════════════╝
    │
    ▼
╔═══════════════════════════════════════════╗
║  DEEP RESEARCH PHASE (MANDATORY)          ║
║  See references/decision-process.md       ║
╚═══════════════════════════════════════════╝
    │
    ▼
Evaluate Priority 1-6 with evidence
    │
    ▼
╔═══════════════════════════════════════════╗
║  ASK USER FOR CLARIFICATION               ║
║  Present options using AskUserQuestion    ║
╚═══════════════════════════════════════════╝
    │
    ▼
Proceed based on user selection
```

## Quick Decision Steps

### Step 1: Identify Core Need

**Invoke the `identify-core-need` skill before proceeding.**

This skill handles:
- Clarifying ambiguous requests (AskUserQuestion)
- Applying Behavioral Principles (no artificial distinctions)
- Extracting Core Need (action + target + triggers)
- Documenting Validation Log

**Only proceed to Step 2 when Core Need is clearly defined with Validation Log complete.**

### Step 2: Search Template Catalog

Read `schemas/_meta.json` from `building-with-tbc` skill for complete template inventory. Check:
- Template names and versions
- Available variants
- Project paths for YML download

### Step 3: Evaluate Template Fit

For each potentially matching template:
1. Read `schemas/{template}.json` for inputs
2. Check if required inputs match use case
3. Check if optional inputs cover customization needs
4. Review available variants in `references/variantes.md`

### Step 4: Deep Research (If Partial Match)

When template partially covers the need, execute **Deep Research Phase**:

1. **Download actual YML** from GitLab using URL pattern:
   ```
   https://gitlab.com/{project}/-/raw/{version}/{file}
   ```

2. **Analyze YML content**: stages, jobs, scripts, tools, extension points

3. **WebSearch tool documentation** for underlying tools

4. **Cross-reference** user need vs template vs tool capabilities

See `references/decision-process.md` for complete Deep Research protocol.

### Step 5: Present Options to User

**CRITICAL: Do NOT decide autonomously. Present findings and ask user to choose.**

After gathering evidence, use `AskUserQuestion` tool to present viable options:

```
AskUserQuestion:
  header: "TBC Approach"
  question: "Based on research, which approach for {use case}?"
  options:
    - label: "{Template} direct"
      description: "Covers {X}% of requirements. {brief evidence}"
    - label: "{Template} + variant"
      description: "Adds {capability}. {brief evidence}"
    - label: "Custom step"
      description: "TBC doesn't cover {gap}. Requires manual job."
```

**Guidelines for AskUserQuestion:**
- Maximum 4 options (tool limit)
- Each option must include evidence from research
- Describe trade-offs clearly in descriptions
- Order options by Priority (1-6) - best option first
- User can always select "Other" for alternatives

**Example Question:**

```
header: "TBC Approach"
question: "Which approach for Docker image build with Trivy scan?"
options:
  - label: "docker template"
    description: "Builds and pushes images. Trivy scan via TBC_DOCKER_SCAN_IMAGE=true"
  - label: "docker + custom scan"
    description: "Use docker template but add separate Trivy job for more control"
  - label: "Custom Dockerfile job"
    description: "Full control but loses TBC caching and best practices"
```

## Output Format

After user selects an option, document the decision path:

```
## Decision Path

User Request: "{request}"
    │
    ▼
Core Need: {action} + {target}
    │
    ▼
Templates Checked: {list}
    │
    ▼
Match Analysis: {findings}
    │
    ▼
Options Presented: {options shown to user}
    │
    ▼
User Selection: {user's choice}
    │
    ▼
Proceeding with: Priority {N} - {solution}

Evidence:
- {source-1}: {finding}
- {source-2}: {finding}
```

## Reference Files

| Need | Reference |
|------|-----------|
| Deep Research protocol | `references/decision-process.md` |

## Integration with building-with-tbc

After user selects an option via AskUserQuestion:
1. Document decision path with user's selection
2. If TBC component selected → invoke `building-with-tbc` skill to generate config
3. If custom step selected → document WHY TBC doesn't fit before proceeding

## Common Scenarios

### Scenario: Template Exists but Partial Fit

Follow Deep Research to check if:
- Template extension points (before_script, scripts-dir) can enable the feature
- Underlying tool supports the requirement
- Variant pattern from other template can be applied

### Scenario: User Requests Custom Script

**Do NOT accept immediately.** Execute full research process:
1. Identify what user actually needs
2. Check if any TBC template covers it
3. Check variants
4. Only if documented failure → accept custom approach

### Scenario: Multiple Templates Possible

Compare each template's fit:
- Which covers more requirements?
- Which has better extension points?
- Which has relevant variants?
