---
name: prompt-engineering
description: >
  Prompt engineering patterns for Claude including system prompts, few-shot examples,
  chain-of-thought, structured output, templates, and prefilling. Use when the user is
  writing prompts, designing system instructions, extracting structured data, building
  prompt templates, or optimizing Claude responses for quality and consistency.
---

# Prompt Engineering

Patterns and techniques for crafting effective Claude prompts. Covers system prompts,
few-shot learning, chain-of-thought reasoning, structured output, and prefilling.

## When to Use
- User is writing or optimizing prompts for Claude
- User needs structured JSON output from Claude
- User is designing system prompts or instructions
- User wants chain-of-thought reasoning or few-shot examples
- User is building prompt templates for reuse

## Core Patterns

### System Prompts

System prompts set Claude's persona, constraints, and output format. Place stable
instructions here; they are cached separately and can use prompt caching.

```python
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="""You are a senior code reviewer. Follow these rules:
1. Focus on bugs, security issues, and performance problems.
2. Rate severity as CRITICAL, HIGH, MEDIUM, or LOW.
3. Provide a fix for each issue found.
4. If the code is clean, say "No issues found." and nothing else.""",
    messages=[{"role": "user", "content": f"Review this code:\n```\n{code}\n```"}]
)
```

### Few-Shot Examples

Provide 2-4 input/output examples to demonstrate the exact format and reasoning you expect.
Use the messages array with alternating user/assistant turns.

```python
messages = [
    {"role": "user", "content": "Classify: 'My order never arrived and nobody responds to emails'"},
    {"role": "assistant", "content": '{"category": "shipping", "sentiment": "negative", "priority": "high"}'},
    {"role": "user", "content": "Classify: 'Love the new feature update, works great!'"},
    {"role": "assistant", "content": '{"category": "feedback", "sentiment": "positive", "priority": "low"}'},
    {"role": "user", "content": f"Classify: '{user_input}'"}
]

message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=256,
    messages=messages
)
```

### Chain-of-Thought Reasoning

Ask Claude to reason step-by-step before giving a final answer. Use extended thinking
for complex problems that benefit from deep reasoning.

```python
# Extended thinking (built-in chain-of-thought)
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # tokens allocated for reasoning
    },
    messages=[{"role": "user", "content": "Debug this function and explain the root cause:\n" + code}]
)

# Access thinking and response separately
for block in message.content:
    if block.type == "thinking":
        print("Reasoning:", block.thinking)
    elif block.type == "text":
        print("Answer:", block.text)
```

```python
# Manual chain-of-thought via prompt
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=2048,
    system="Think step-by-step. Show your reasoning in <reasoning> tags, then give the final answer.",
    messages=[{"role": "user", "content": "What is the time complexity of merge sort and why?"}]
)
```

### Structured Output (JSON Mode)

Force Claude to return valid JSON by combining system instructions with prefilling.

```python
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="""Extract entities from the text. Return a JSON object with this exact schema:
{
  "people": [{"name": string, "role": string}],
  "organizations": [{"name": string, "type": string}],
  "locations": [{"name": string, "context": string}]
}
Return ONLY valid JSON, no other text.""",
    messages=[
        {"role": "user", "content": f"Extract entities from: {text}"},
        {"role": "assistant", "content": "{"}  # Prefill forces JSON start
    ]
)

# Reconstruct the full JSON (prefill is not included in response)
import json
result = json.loads("{" + message.content[0].text)
```

### Prefilling Assistant Responses

Prefill the assistant turn to control output format, language, or starting point.

```python
# Force a specific output format
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Translate to French: 'Hello, how are you?'"},
        {"role": "assistant", "content": "Bonjour"}  # Forces French output
    ]
)

# Force code-only output
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=2048,
    messages=[
        {"role": "user", "content": "Write a Python function to calculate fibonacci numbers."},
        {"role": "assistant", "content": "```python\n"}  # Forces code block
    ]
)
```

### Prompt Templates

Build reusable prompt templates with clear variable boundaries using XML tags.

```python
REVIEW_TEMPLATE = """Review the following pull request diff.

<diff>
{diff}
</diff>

<context>
Repository: {repo_name}
Language: {language}
PR Description: {pr_description}
</context>

<instructions>
1. Identify bugs, security issues, and performance problems.
2. Suggest improvements with code examples.
3. Rate overall quality: APPROVE, REQUEST_CHANGES, or COMMENT.
</instructions>"""

message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=4096,
    messages=[{
        "role": "user",
        "content": REVIEW_TEMPLATE.format(
            diff=diff_text,
            repo_name="my-app",
            language="TypeScript",
            pr_description="Add user authentication"
        )
    }]
)
```

## Anti-Patterns
- Using vague instructions like "be helpful" instead of specific behavioral rules
- Putting variable content in the system prompt (defeats prompt caching)
- Providing more than 5 few-shot examples (diminishing returns, wastes tokens)
- Not using XML tags to delimit sections in complex prompts
- Asking Claude to "never" do something instead of stating what it should do
- Using temperature=1.0 for structured output (use 0.0 for deterministic JSON)
- Prefilling with invalid syntax that forces Claude into a broken output format

## Quick Reference

| Technique | When to Use |
|-----------|-------------|
| System prompt | Stable instructions, persona, output format |
| Few-shot | Classification, formatting, style matching |
| Chain-of-thought | Math, logic, debugging, multi-step reasoning |
| Extended thinking | Complex analysis, deep reasoning tasks |
| Prefilling | Force output format, language, code blocks |
| XML tags | Delimit sections in complex prompts |
| JSON mode | Structured data extraction, API responses |

Key tips:
- Put the most important instructions at the beginning and end of the system prompt.
- Use XML tags (`<context>`, `<instructions>`, `<examples>`) for clear prompt structure.
- Set temperature=0 for deterministic tasks, temperature=0.5-1.0 for creative tasks.
- Prefilled content is NOT included in the response -- prepend it when parsing.
