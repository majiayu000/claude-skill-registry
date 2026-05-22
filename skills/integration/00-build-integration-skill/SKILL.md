---
sidebar_position: 0
title: "Build Your Agent Integration Skill"
description: "Create your agent-integration skill from OpenAI SDK and LiteLLM documentation before learning framework integration"
chapter: 71
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill-First Learning"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "3. Digital Content Creation"
    measurable_at_this_level: "Student creates a working agent-integration skill using natural language conversation with Claude"

  - name: "SDK Documentation Research"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "1. Information and Data Literacy"
    measurable_at_this_level: "Student fetches and synthesizes SDK documentation to build comprehensive skill"

learning_objectives:
  - objective: "Build an agent-integration skill using natural conversation with Claude"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Student has a working agent-integration skill in .claude/skills/"

  - objective: "Synthesize OpenAI SDK and LiteLLM documentation into actionable patterns"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill contains verified patterns from official documentation"

cognitive_load:
  new_concepts: 2
  assessment: "Two concepts (skill creation, SDK research) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Add MCP server patterns and error handling templates during creation"
  remedial_for_struggling: "Follow exact prompts provided step-by-step"
---

# Build Your Agent Integration Skill

Your Task API model is deployed and running via Ollama. Now you need to connect it to agent frameworks like OpenAI Agents SDK, Claude Code, and MCP servers.

Before learning integration patterns, you will **own** an agent-integration skill. This skill becomes your reusable reference for connecting custom models to any framework.

This lesson follows the **Skill-First Learning Pattern**: build the skill, then learn what it knows.

## Why Skill-First for Agent Integration?

Agent framework integration involves multiple interconnected patterns:

| Pattern | What It Handles |
|---------|-----------------|
| **LiteLLM Proxy** | Unified OpenAI-compatible API for any backend |
| **Base URL Config** | Redirect SDK calls to custom endpoints |
| **Tool Calling** | Structured outputs for function invocation |
| **Error Fallback** | Graceful degradation to foundation models |
| **MCP Integration** | Model Context Protocol server setup |

Learning these patterns without a reference leads to trial-and-error debugging. Your skill captures verified patterns from official documentation, giving you a reliable starting point.

## Step 1: Get the Skills Lab

If you completed Chapter 70, you already have the skills-lab. If not:

1. Go to [github.com/panaversity/claude-code-skills-lab](https://github.com/panaversity/claude-code-skills-lab)
2. Click the green **Code** button
3. Select **Download ZIP**
4. Extract the ZIP file
5. Open the extracted folder in your terminal

```bash
cd claude-code-skills-lab
claude
```

## Step 2: Create Your Agent Integration Skill

Copy and paste this prompt:

```
Using your skill creator skill, create a new skill called "agent-integration"
for connecting custom LLM backends to agent frameworks.

I need patterns for:
- LiteLLM proxy configuration for OpenAI SDK compatibility
- OpenAI Agents SDK with custom base_url
- Tool calling with custom models (structured outputs)
- Error handling and fallback to foundation models
- MCP server integration with custom backends

Use context7 skill to study:
- OpenAI Python SDK documentation
- LiteLLM documentation
- FastMCP documentation

Build from official docs only, no assumed knowledge.
```

Claude will:
1. Fetch OpenAI SDK, LiteLLM, and FastMCP documentation via Context7
2. Ask clarifying questions about your deployment setup (Ollama vs vLLM, local vs cloud)
3. Create a comprehensive skill with patterns, templates, and troubleshooting guides

Your skill appears at `.claude/skills/agent-integration/`.

## Step 3: Verify Your Skill

Check that your skill exists:

```bash
ls .claude/skills/agent-integration/
```

**Expected Output:**
```
SKILL.md
```

Open the skill and confirm it includes:
- LiteLLM proxy configuration examples
- OpenAI SDK base_url patterns
- Tool calling JSON schema templates
- Error handling patterns
- MCP server integration code

## What Your Skill Contains

A well-built agent-integration skill includes these sections:

### LiteLLM Proxy Setup

```yaml
# config.yaml for LiteLLM
model_list:
  - model_name: task-api-model
    litellm_params:
      model: ollama/task-api-model
      api_base: http://localhost:11434
```

### OpenAI SDK Configuration

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000/v1",  # LiteLLM proxy
    api_key="sk-local"  # Placeholder for local
)
```

### Tool Calling Schema

```python
tools = [{
    "type": "function",
    "function": {
        "name": "create_task",
        "description": "Create a new task",
        "parameters": {
            "type": "object",
            "properties": {
                "title": {"type": "string"},
                "priority": {"type": "string", "enum": ["low", "medium", "high"]}
            },
            "required": ["title"]
        }
    }
}]
```

### Error Fallback Pattern

```python
def call_with_fallback(prompt, tools):
    try:
        return custom_client.chat.completions.create(
            model="task-api-model",
            messages=[{"role": "user", "content": prompt}],
            tools=tools
        )
    except Exception:
        return openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            tools=tools
        )
```

## Done

You now own an agent-integration skill built from official OpenAI SDK, LiteLLM, and FastMCP documentation.

The rest of this chapter teaches you what your skill knows:
- **Lessons 1-3**: Integration fundamentals (backends, proxy, SDK)
- **Lessons 4-6**: Production patterns (tool calling, MCP, error handling)
- **Lesson 7**: Capstone that combines everything into a complete Task API Agent

As you complete each lesson, your skill improves. By the chapter's end, you have a production-ready integration skill for any custom model.

## Try With AI

### Prompt 1: Examine Your Skill

```
Open my agent-integration skill at .claude/skills/agent-integration/SKILL.md
and explain its structure. What sections does it have? What patterns are
included? Are there any gaps I should fill in as I complete this chapter?
```

**What you're learning**: Understanding skill structure and identifying improvement opportunities.

### Prompt 2: Compare to Your Setup

```
I have my Task API model running on Ollama at localhost:11434. Review my
agent-integration skill and tell me which patterns apply to my setup.
What configuration changes would I need for a different setup (like vLLM
or cloud deployment)?
```

**What you're learning**: Mapping general patterns to your specific deployment context.

### Prompt 3: Identify Learning Path

```
Based on what's in my agent-integration skill, which patterns do I already
understand from previous chapters, and which are new? Help me prioritize
what to focus on in the upcoming lessons.
```

**What you're learning**: Self-assessment and learning prioritization through skill analysis.
