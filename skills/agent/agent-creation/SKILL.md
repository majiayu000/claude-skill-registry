---
name: agent-creation
description: "Guides agents and users to create standards-compliant agent definitions using templates in markdown frontmatter format, ensuring context gathering, clarity, and proper metadata. Forces agents to ask clarifying questions when context is insufficient. Token-efficient documentation required. All content must be in English. Trigger: When creating a new agent definition, setting up project agents, or documenting agent workflows."
skills:
  - english-writing
---

# Agent Creation Skill

## Overview

Provides actionable instructions for creating standards-compliant agent definitions using templates. Agents are defined in markdown files (AGENTS.md) with YAML frontmatter specifying metadata and a clear, readable structure. This skill enforces context gathering before agent creation to ensure robust and well-defined agents.

## Objective

Enable agents and users to generate agent definitions that strictly follow the required structure and conventions using the provided template. Ensure sufficient context is gathered through clarifying questions before proceeding with agent creation. Validate each agent against the JSON schema and provide a compliance checklist to ensure all requirements are met.

---

## When to Use

Use this skill when:

- Creating a new agent definition from scratch
- Setting up project-specific agents
- Documenting agent workflows and responsibilities
- Defining agent context and skill requirements

Don't use this skill for:

- Creating individual skills (use skill-creation instead)
- Creating context prompts (use prompt-creation instead)
- Modifying existing agents without full context

---

## References

- https://agents.md/
- https://agents.md/#examples
- [Agent Skills Home](https://agentskills.io/home)

---

## Instructions

### Step 1: Gather Context (CRITICAL - DO NOT SKIP)

**Before creating an agent definition, you MUST ask clarifying questions when context is missing. Do not proceed until you have sufficient information.**

**Required context to gather:**

- What is the primary purpose of this agent?
- What type of input will the agent receive? (e.g., files, text, objects, user queries)
- What is the expected output format? (e.g., markdown, JSON, text, files)
- Which skills does the agent need to accomplish its tasks?
- Are there any specific workflows, policies, or constraints the agent must follow?
- Who is the target audience for this agent? (e.g., developers, end-users, AI assistants)
- What technologies, frameworks, or tools will the agent interact with?
- What is the project context where this agent will operate?
- Are there any tone or communication style requirements? (e.g., formal, casual, technical)

**Do not proceed with creating the agent until you have:**

- A clear understanding of the agent's purpose and responsibilities
- Defined input and output formats (if applicable)
- Identified all required skills
- Understood any special policies, constraints, or workflows
- Gathered sufficient context about the project environment

### Step 2: Directory and File Structure

- Create a new directory under `agents/` named after the project or agent (lowercase, hyphens, no spaces).
- Add an `AGENTS.md` file inside the directory.

### Step 3: YAML Frontmatter

The frontmatter must include:

**Required fields:**

- **name**: Agent identifier (lowercase, hyphens only, e.g., `my-project-agent`). Keep concise.
- **description**: Clear, concise explanation of purpose and responsibilities. Token-efficient: eliminate redundancy, keep specificity.
- **skills**: List required skills using YAML `- item` syntax (never `[]`). Must be existing skills from `skills/` directory.
  - **Mandatory for ALL agents**: Always include `critical-partner`
  - **Mandatory for technical/management agents**: Always include `process-documentation`

**Optional fields (include only if they add specificity):**

- **input**: Expected input type/format (e.g., `"user query | string"`). Omit if obvious from description.
- **output**: Expected output type/format (e.g., `"markdown report"`). Omit if obvious from description.

**Formatting rules:**

- Use YAML list syntax: `- item` (never `[]` for arrays)
- Omit empty fields completely
- Be precise and token-efficient: every word must serve AI and human understanding

Example frontmatter:

```yaml
---
name: my-project-agent
description: Development assistant for Project X. Expert in TypeScript, React, and MUI.
skills:
  - typescript
  - react
  - mui
  - critical-partner
  - process-documentation
  - conventions
  - a11y
---
```

### Step 4: Content Structure

After the frontmatter, include the following sections:

1. **# Agent Name** (h1): Title describing the agent (e.g., "SBD Project Agent").
2. **## Purpose**: Clear statement of the agent's primary goal and responsibilities. Be specific and actionable.
3. **## ⚠️ Mandatory Skill Reading** (REQUIRED): Critical instructions for reading skills before task execution. Must include:
   - Skill Reading Protocol (5-step process)
   - Warning about not proceeding without reading skills
   - Notification Policy for multi-skill tasks (2+ skills)
   - **Reference to Extended Mandatory Read Protocol** in AGENTS.md
   - Link to Mandatory Skills table
4. **## Mandatory Skills** (REQUIRED): Table with triggers, required skills, and paths. Use format: `| Trigger (When to Read) | Required Skill | Path |`

   **Critical trigger that MUST be included in all agents:**
   - "Write commit messages, PRs, or documentation" → technical-communication

   **Additional triggers based on agent's skills**: Add specific triggers for each skill the agent uses (e.g., "Create React components" → react, "Create TypeScript types" → typescript)

**Important**: The Mandatory Skill Reading section must inform AI agents that when working with complex skills (40+ patterns), they should consult the skill's Decision Tree and Quick Reference Table to determine if reading references/ is required. See [AGENTS.md Extended Mandatory Read Protocol](../../AGENTS.md#extended-mandatory-read-protocol) for complete guidance. 5. **## Supported stack** (if applicable): List technologies, frameworks, libraries, and versions used in the project. 6. **## Skills Reference** (optional but recommended): Table listing all skills with descriptions and paths. 7. **## Workflows** (optional): Common workflows the agent handles (e.g., "Feature Development," "Code Review"). 8. **## Policies** (optional): Project-specific rules, constraints, or guidelines the agent must follow.

### Step 5: Writing Guidelines

All generated code, documentation, comments, and prompt content must follow the [english-writing](../english-writing/SKILL.md) skill. Do not duplicate these rules here.

- Be token-efficient: precise and concise without losing specificity
- Organize content with proper markdown structure (headings, lists, code blocks, tables)

### Step 6: Validation

Before finalizing, verify:

- [ ] Directory created under `agents/` with correct naming
- [ ] `AGENTS.md` file exists with proper frontmatter
- [ ] Required fields: `name`, `description`, `skills`
- [ ] `critical-partner` included in skills (mandatory for ALL agents)
- [ ] `process-documentation` included for technical/management agents
- [ ] All referenced skills exist in `skills/` directory
- [ ] Skills use YAML list syntax (`- item`), not arrays (`[]`)
- [ ] Empty fields omitted
- [ ] Content sections present: Purpose, and others as appropriate
- [ ] Token-efficient documentation: no redundancy
- [ ] Content in English with American spelling

---

## Decision Tree

```
Context gathered (9 questions answered)? → NO → Stop: Ask clarifying questions
All required skills identified? → NO → Ask: Which skills needed?
Agent for technical/management? → YES → Include process-documentation in skills
Creating first agent? → YES → Use AGENT-TEMPLATE.md as starting point
Agent has complex workflows (3+ phases)? → YES → Add detailed Workflow section
Agent needs skill reference reading? → YES → Include Extended Protocol reference
Mandatory Skill Reading section included? → NO → Stop: Must include (REQUIRED)
critical-partner in skills list? → NO → Stop: Must include (mandatory)
All referenced skills exist in skills/? → NO → Stop: Verify skill paths
Ready to create? → YES → Proceed with agent creation
```

---

## 🔍 Self-Check Protocol (For AI Agents)

**Before finalizing agent creation, verify:**

- [ ] I gathered all 9 context questions (purpose, input, output, skills, workflows, audience, technologies, project context, tone)
- [ ] I read the entire agent-creation SKILL.md (this file)
- [ ] I consulted the Decision Tree for my specific case
- [ ] I included ⚠️ Mandatory Skill Reading section with 5-step protocol
- [ ] I referenced Extended Mandatory Read Protocol in AGENTS.md
- [ ] I included Mandatory Skills table with triggers
- [ ] Mandatory Skills table includes "Write commit messages, PRs, or documentation" → technical-communication
- [ ] critical-partner is in skills list (REQUIRED for ALL agents)
- [ ] process-documentation is in skills list (if technical/management agent)
- [ ] All referenced skills exist in skills/ directory
- [ ] YAML syntax correct (lists use `- item`, not `[]`)
- [ ] Empty fields omitted from frontmatter
- [ ] Agent has unique, clear purpose statement

**Confidence check:** Can you answer these questions?

1. What is this agent's primary responsibility? (Answer: Should be in Purpose section)
2. Which skills will this agent use most frequently? (Answer: Should be in Mandatory Skills table)
3. When should the agent read skill references? (Answer: When Decision Tree indicates MUST or [CRITICAL] pattern says so)

**If you answered NO to any checklist item or cannot answer the confidence questions:**

1. Stop immediately
2. Re-read the missing section or gather missing context
3. Restart from Step 1 of the workflow

**For complete validation:** See [Compliance Checklist](#compliance-checklist) below.

---

## Example: Complete Agent Definition

```markdown
---
name: example-agent
description: Development assistant for Example Project. Provides guidance on TypeScript, React, and accessibility standards.
skills:
  - typescript
  - react
  - critical-partner
  - process-documentation
  - conventions
  - a11y
---

# Example Project Agent

## Purpose

This agent serves as the primary development assistant for the Example Project, ensuring code quality, accessibility compliance, and adherence to TypeScript and React best practices.

## Supported stack

- **Languages**: TypeScript 5.0+, JavaScript (ES2020+)
- **Framework**: React 18+
- **Build**: Vite

## Skills Reference

| Skill Name            | Description                 | Path                                  |
| --------------------- | --------------------------- | ------------------------------------- |
| typescript            | TypeScript best practices   | skills/typescript/SKILL.md            |
| react                 | React patterns and hooks    | skills/react/SKILL.md                 |
| critical-partner      | Code review and improvement | skills/critical-partner/SKILL.md      |
| process-documentation | Change documentation        | skills/process-documentation/SKILL.md |
| conventions           | General coding conventions  | skills/conventions/SKILL.md           |
| a11y                  | Accessibility standards     | skills/a11y/SKILL.md                  |

## Workflows

### Feature Development

1. Gather requirements
2. Design component architecture
3. Implement with TypeScript and React
4. Ensure accessibility compliance
5. Document changes

## Policies

- All code must be strictly typed (no `any`)
- Components must be keyboard-accessible
- Follow React hooks best practices
```

---

## Compliance Checklist

Before finalizing an agent, verify:

### Structure & Files

- [ ] Directory created under `agents/` with correct naming (lowercase, hyphens)
- [ ] `AGENTS.md` file exists with proper frontmatter
- [ ] All sections present: Purpose, Mandatory Skill Reading, Mandatory Skills table

### Frontmatter Compliance

- [ ] Required fields: `name`, `description`, `skills`
- [ ] Description clear and precise without redundancy
- [ ] `critical-partner` included in skills (mandatory for ALL agents)
- [ ] `process-documentation` included for technical/management agents
- [ ] All referenced skills exist in `skills/` directory
- [ ] Skills use YAML list syntax (`- item`), not arrays (`[]`)
- [ ] Empty fields omitted completely
- [ ] Token-efficient: every word adds value

### Content Quality

- [ ] Context gathered (9 key questions answered before creation)
- [ ] Purpose section clear and actionable
- [ ] ⚠️ **Mandatory Skill Reading section included** with:
  - [ ] 5-step Skill Reading Protocol
  - [ ] Warning about not proceeding without reading
  - [ ] Notification Policy for multi-skill tasks
  - [ ] **Reference to Extended Mandatory Read Protocol in AGENTS.md**
- [ ] **Mandatory Skills table included** with triggers, skills, and paths
  - [ ] Table includes "Write commit messages, PRs, or documentation" → technical-communication
- [ ] Decision Tree present (if agent has complex workflows)
- [ ] Self-Check Protocol consulted and completed

### Post-Creation Steps

- [ ] Agent added to AGENTS.md Available Agents section (if applicable)
- [ ] Agent reviewed by critical-partner skill
- [ ] Changes documented with process-documentation skill
- [ ] Ready for sync with `make sync` (if applicable)

---

## References

- [skill-creation](../skill-creation/SKILL.md): Creating new skills
- [critical-partner](../critical-partner/SKILL.md): Code review guidance
- [process-documentation](../process-documentation/SKILL.md): Change documentation
