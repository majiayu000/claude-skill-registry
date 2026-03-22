---
name: team
description: "Quickly assemble a temporary AI Agent team for a task. Automatically selects the best members from .claude/agents/."
argument-hint: "[task description]"
disable-model-invocation: true
---

# Assemble Temporary Team

Based on the task below, select the most suitable members from the company's AI Agents and form a temporary team to collaborate on it.

## Task

$ARGUMENTS

## Available Agents

All agents are defined in `.claude/agents/`:

| Agent | File | Role |
|-------|------|------|
| CEO | `ceo-bezos` | Strategic decisions, business models, PR/FAQ, prioritization |
| CTO | `cto-vogels` | Technical architecture, technology selection, system design |
| Critic | `critic-munger` | Challenge decisions, identify fatal flaws, Pre-Mortem, prevent groupthink |
| Product Design | `product-norman` | Product definition, user experience, usability |
| UI Design | `ui-duarte` | Visual design, design system, color and typography |
| Interaction Design | `interaction-cooper` | User flows, Personas, interaction patterns |
| Full-Stack Dev | `fullstack-dhh` | Code implementation, technical proposals, development |
| QA | `qa-bach` | Test strategy, quality gates, bug analysis |
| DevOps/SRE | `devops-hightower` | Deployment pipelines, CI/CD, infrastructure, monitoring |
| Marketing | `marketing-godin` | Positioning, brand, acquisition, content |
| Operations | `operations-pg` | User operations, growth, community, PMF |
| Sales | `sales-ross` | Sales funnel, conversion strategy |
| CFO | `cfo-campbell` | Pricing strategy, financial models, cost control, unit economics |
| Research | `research-thompson` | Market research, competitive analysis, industry trends, opportunity discovery |

## Execution Steps

### 1. Analyze the Task, Select Members

Select 2-5 of the most relevant Agents as team members based on the task. Selection principles:
- **Only pick who's needed** -- more people is not better; match precisely to the task
- **Consider the collaboration chain** -- if the task spans design to development, include key roles along the chain
- **Avoid redundancy** -- don't select agents with overlapping roles

Briefly state who you selected and why, then immediately begin assembling the team.

### 2. Assemble the Agent Team

Use the Agent Teams feature to form a temporary team:
- Create a team with `team_name` based on a short task name (English, kebab-case)
- Create a specific task for each member (TaskCreate) with sufficient context in the description
- Spawn each teammate using the Task tool with `subagent_type` set to `general-purpose`, injecting the full content of the corresponding agent file as the role definition in the prompt
- When spawning, tell each teammate: their role definition, the task to complete, and that output documents go in `docs/<role>/`

### 3. Coordinate and Synthesize

- As team lead, coordinate each member's work
- Collect outputs from all members and synthesize into a unified conclusion or plan
- If there are disagreements, list each side's viewpoint for the CEO to decide
- Clean up team resources when done

## Notes

- Communicate in English
- Each member's output documents go in `docs/<role>/` as defined
- Teams are temporary -- disband once the task is complete
- The CEO (Bezos) is the ultimate decision-maker; other agents provide recommendations but do not override
