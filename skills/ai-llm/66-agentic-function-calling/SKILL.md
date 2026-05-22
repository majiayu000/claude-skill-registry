---
sidebar_position: 0
title: "Build Your Agentic Tuning Skill"
chapter: 66
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill-First Learning Setup"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can clone a fresh skills-lab, write a LEARNING-SPEC.md, and create an initial skill from official documentation"

  - name: "Agentic Tuning Pattern Recognition"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can explain why tool-calling fine-tuning differs from standard instruction tuning and identify the key components needed"

  - name: "Documentation-Grounded Skill Building"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can use Context7 or official docs to ground skill creation in authoritative sources rather than memory"

learning_objectives:
  - objective: "Set up a fresh skills-lab environment for agentic tuning exploration"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Successful clone and environment verification"

  - objective: "Write a LEARNING-SPEC.md capturing your agentic tuning learning goals"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Specification includes intent, success criteria, and non-goals"

  - objective: "Create initial agentic-tuning skill from official documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill file created with proper structure and doc-grounded content"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (skill-first learning, LEARNING-SPEC, doc-grounding, agentic tuning overview) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Research OpenAI's function-calling format and compare with Claude's tool_use format before building skill"
  remedial_for_struggling: "Focus on cloning the repo and writing just the Intent section of LEARNING-SPEC.md"
---

# Build Your Agentic Tuning Skill

Before diving into tool-calling patterns, structured outputs, and JSON accuracy metrics, you'll build the skill that will guide your learning throughout this chapter. This isn't just preparation—it's the first step in creating a reusable asset you'll refine as you progress.

By the end of this lesson, you'll have a working `agentic-tuning` skill grounded in official documentation. Each subsequent lesson will test and improve this skill, transforming your learning into accumulated intelligence.

## Why Skill-First for Agentic Tuning?

Agentic fine-tuning involves specialized knowledge that's rapidly evolving:

- **Function-calling formats**: OpenAI, Claude, and open-source models use different tool-call schemas
- **Structured output training**: Special tokens, JSON schemas, validation techniques
- **SDK integration patterns**: How to connect fine-tuned models to agent frameworks
- **Evaluation metrics**: Tool accuracy, argument validation, end-to-end success rates

Building a skill from official documentation ensures you're working with current, accurate patterns rather than relying on potentially outdated training data.

## Step 1: Clone Skills-Lab Fresh

Every chapter starts with a clean environment. No assumptions about prior state.

```bash
# Navigate to your projects directory
cd ~/projects

# Clone fresh (or pull latest if exists)
git clone https://github.com/panaversity/skills-lab.git ch66-agentic-tuning
cd ch66-agentic-tuning

# Verify structure
ls -la
```

**Output:**
```
drwxr-xr-x  skills/
drwxr-xr-x  specs/
drwxr-xr-x  data/
-rw-r--r--  README.md
-rw-r--r--  requirements.txt
```

Create your chapter workspace:

```bash
mkdir -p skills/agentic-tuning
mkdir -p specs/task-agent-backend
mkdir -p data/tool-calling
```

## Step 2: Write Your LEARNING-SPEC.md

The LEARNING-SPEC defines what you're learning, why it matters, and how you'll know you've succeeded.

Create `specs/task-agent-backend/LEARNING-SPEC.md`:

```markdown
# LEARNING-SPEC: Agentic Fine-Tuning for Task API

## Intent

Fine-tune a language model to reliably call Task API tools (create_task,
update_task, complete_task, list_tasks) with 95%+ JSON accuracy, enabling
use as a drop-in replacement for GPT-4 in OpenAI Agents SDK workflows.

## Why This Matters

- **Cost reduction**: GPT-4 costs $10K+/month at high volume; custom model ~$300
- **Latency improvement**: <500ms vs ~1s for API calls
- **Full control**: Train on proprietary data, deploy on your infrastructure
- **Differentiation**: Competitors can't replicate your specialized agent

## Success Criteria

1. **Tool-calling accuracy > 95%**: Model selects correct tool for given intent
2. **Valid JSON output > 99%**: All outputs parse without errors
3. **Argument accuracy > 90%**: Parameters match expected schema
4. **SDK compatibility**: Works as drop-in replacement in OpenAI Agents SDK
5. **Latency < 500ms**: Acceptable response time on consumer hardware

## What I'll Learn

- [ ] Structured output fundamentals (why JSON matters for agents)
- [ ] Tool-calling data patterns (OpenAI format, multi-turn conversations)
- [ ] Dataset creation for tool-calling (synthetic generation, validation)
- [ ] Fine-tuning configuration (special tokens, loss masking)
- [ ] Evaluation framework (tool accuracy, end-to-end testing)
- [ ] SDK integration (LiteLLM, OpenAI Agents SDK compatibility)
- [ ] Error handling (graceful degradation, retry strategies)

## Non-Goals

- Building a general-purpose assistant (we focus on Task API only)
- Achieving human-level reasoning (we want reliable tool execution)
- Supporting arbitrary tool schemas (we optimize for our four tools)
- Production deployment (covered in Chapter 70)

## Prerequisites

- Chapter 65: Persona-tuned Task API model
- Chapter 64: Understanding of SFT workflow
- Part 6: OpenAI Agents SDK familiarity
```

## Step 3: Fetch Official Documentation

Use your AI assistant with Context7 or web fetch to gather authoritative sources.

**Prompt to AI:**

```
Fetch the official OpenAI documentation on function calling format.
I need to understand:
1. The exact JSON schema for function definitions
2. How tool calls appear in chat completion responses
3. The format for tool_choice parameter
4. How multi-turn conversations with tool calls work

Focus on the format used for fine-tuning, not just API usage.
```

**Key patterns you'll discover:**

```json
// Function definition format
{
  "type": "function",
  "function": {
    "name": "create_task",
    "description": "Create a new task with title, due date, and priority",
    "parameters": {
      "type": "object",
      "properties": {
        "title": {"type": "string", "description": "Task title"},
        "due_date": {"type": "string", "description": "Due date in YYYY-MM-DD"},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]}
      },
      "required": ["title"]
    }
  }
}
```

```json
// Tool call in assistant response
{
  "role": "assistant",
  "content": null,
  "tool_calls": [
    {
      "id": "call_abc123",
      "type": "function",
      "function": {
        "name": "create_task",
        "arguments": "{\"title\": \"Review budget\", \"priority\": \"high\"}"
      }
    }
  ]
}
```

## Step 4: Create Your Agentic-Tuning Skill

Now build your initial skill based on what you've learned.

Create `skills/agentic-tuning/SKILL.md`:

```markdown
---
name: agentic-tuning
description: "This skill should be used when fine-tuning language models for reliable tool-calling and structured output generation. Use when creating agent backends, training for function calling, or building models that need 95%+ JSON accuracy."
---

# Agentic Tuning Skill

## Purpose

Guide fine-tuning workflows that produce models capable of reliable tool-calling
and structured output generation for use as agent backends.

## When to Use This Skill

Activate when:
- Training models for function calling / tool use
- Optimizing for structured JSON output
- Building custom backends for OpenAI Agents SDK
- Replacing expensive API calls with custom models
- Improving tool-calling accuracy in existing models

## Core Patterns

### 1. Tool Definition Format (OpenAI Compatible)

```json
{
  "type": "function",
  "function": {
    "name": "tool_name",
    "description": "Clear description of what tool does",
    "parameters": {
      "type": "object",
      "properties": {
        "param1": {"type": "string", "description": "..."},
        "param2": {"type": "integer", "description": "..."}
      },
      "required": ["param1"]
    }
  }
}
```

### 2. Training Data Format

Each example must include:
- System prompt with tool definitions
- User message with intent
- Assistant response with tool_call (not natural language)

```json
{
  "messages": [
    {"role": "system", "content": "You are a task assistant. Tools: [...]"},
    {"role": "user", "content": "Create a high priority task for budget review"},
    {"role": "assistant", "content": null, "tool_calls": [...]}
  ]
}
```

### 3. Evaluation Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Tool Selection Accuracy | >95% | Correct tool for intent |
| JSON Validity | >99% | Parses without error |
| Argument Accuracy | >90% | Schema-compliant parameters |
| End-to-End Success | >85% | Task actually completed |

## Decision Framework

### When to Fine-Tune vs. Prompt Engineer

Fine-tune when:
- You have 500+ tool-calling examples
- Current accuracy is below 90%
- Latency requirements demand smaller models
- Cost savings justify training investment

Prompt engineer when:
- You have fewer than 200 examples
- Base model achieves >95% accuracy with good prompts
- Requirements are still evolving rapidly

## Common Mistakes to Avoid

1. **Natural language instead of tool calls**: Assistant should return
   `tool_calls`, not descriptions like "I'll create that task for you"

2. **Missing tool definitions in system prompt**: Every training example
   must include the full tool schema

3. **Inconsistent argument formats**: Use ISO dates (YYYY-MM-DD),
   consistent enum values, proper types

4. **Single-turn only**: Include multi-turn examples with tool results

## References

- OpenAI Function Calling Guide: https://platform.openai.com/docs/guides/function-calling
- Fine-tuning for Function Calling: https://platform.openai.com/docs/guides/fine-tuning
- OpenAI Agents SDK: https://github.com/openai/openai-agents-python
```

## Step 5: Verify Your Skill

Test that your skill provides useful guidance:

**Prompt to AI:**

```
Read my agentic-tuning skill at skills/agentic-tuning/SKILL.md.
Now help me create a single training example for a user who says
"Add a task to call mom tomorrow, low priority."
Apply the patterns from the skill.
```

**Expected output structure:**

```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are TaskMaster, a task management assistant. You have access to the following tools:\n\n[{\"type\": \"function\", \"function\": {\"name\": \"create_task\", ...}}]"
    },
    {
      "role": "user",
      "content": "Add a task to call mom tomorrow, low priority."
    },
    {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_001",
          "type": "function",
          "function": {
            "name": "create_task",
            "arguments": "{\"title\": \"Call mom\", \"due_date\": \"2024-01-16\", \"priority\": \"low\"}"
          }
        }
      ]
    }
  ]
}
```

If your skill produces examples like this, you're ready to proceed.

## Reflect on Your Skill

Before moving to Lesson 1, consider:

1. **What patterns did you extract?** Which documentation sources proved most valuable?

2. **What's still unclear?** Note questions to answer in upcoming lessons (multi-turn conversations, tool results, error handling).

3. **What would improve the skill?** You'll refine it as you learn more about evaluation metrics and SDK integration.

## Looking Ahead

Your `agentic-tuning` skill is now grounded in official documentation. In the lessons ahead, you'll:

- **Lesson 1**: Understand why structured output matters for agents
- **Lesson 2**: Learn tool-calling patterns in depth
- **Lesson 3**: Train for consistent structured outputs
- **Lesson 4**: Create Task API tool-calling datasets
- **Lesson 5**: Run your first agentic fine-tuning job
- **Lesson 6**: Handle multi-turn conversations
- **Lesson 7**: Evaluate tool accuracy systematically
- **Lesson 8**: Build the complete Task Agent Backend

Each lesson will test and improve your skill. By Chapter 66's end, you'll have a production-ready skill for any agentic fine-tuning project.

## Try With AI

Use your AI companion to enhance your skill.

### Prompt 1: Expand Tool Definitions

```
I'm building an agentic-tuning skill for Task API. I have four tools:
- create_task: Create new tasks with title, due date, priority
- update_task: Modify existing tasks by ID
- complete_task: Mark a task as done
- list_tasks: Get tasks filtered by status/priority/date

Help me write the complete JSON schema for each tool following
OpenAI's function calling format. Ask me clarifying questions
about the exact parameters each tool should accept.
```

**What you're learning**: Schema design through dialogue—your AI partner helps you think through edge cases (optional vs required params, enum values, date formats).

### Prompt 2: Identify Skill Gaps

```
Review my LEARNING-SPEC.md for agentic fine-tuning. What topics
am I likely missing? What common challenges do people face when
fine-tuning for tool-calling that I should add to my skill's
"Common Mistakes to Avoid" section?
```

**What you're learning**: Gap analysis—anticipating challenges before encountering them, improving your skill proactively.

### Prompt 3: Connect to Your Domain

```
I'm learning agentic fine-tuning with Task API as the example.
But my real goal is [describe your domain—customer support,
sales automation, data analysis, etc.]. Help me understand
how the patterns from this chapter apply to my domain. What
tools would MY agent need?
```

**What you're learning**: Pattern transfer—translating Task API examples to your actual use case.

### Safety Note

As you build your skill from documentation, verify key claims. AI can help synthesize patterns, but official docs are the source of truth for format specifications. When in doubt, test with the actual API.
