---
name: careercopilot-agent-scaffolder
description: "Scaffolds a new Python agent for autonomous AI tasks in 'src/agents/'. Agents are autonomous components that handle complex operations (resume analysis, job matching, KSC generation). Use when asked to create a new AI agent or automation component."
---

# Agent Scaffolder Workflow

1.  Ask the user for the new agent's name (e.g., `resume_analyzer_agent`).
2.  Read the template: `cat .claude/skills/careercopilot-agent-scaffolder/templates/agent.py.tpl`
3.  Replace the `{{AGENT_NAME}}` placeholder with the user's provided name (e.g., `resume_analyzer_agent`).
4.  Write the new file to `src/agents/{{AGENT_NAME}}.py`.
5.  Report success and show the path to the new file.
