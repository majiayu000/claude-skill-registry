---
name: prompt-engineering
description: Prompt templates, few-shot examples, chain-of-thought, structured output, evals
---

# Prompt Engineering

## Prompt Templates

### System Prompt Structure

```python
SYSTEM_PROMPT = """You are a {role} specialized in {domain}.

## Task
{task_description}

## Rules
{numbered_rules}

## Output Format
{format_spec}

## Examples
{few_shot_examples}
"""
```

### Few-Shot Template

```python
def build_few_shot_prompt(task: str, examples: list[dict], query: str) -> str:
    prompt = f"Task: {task}\n\n"
    for i, ex in enumerate(examples, 1):
        prompt += f"Example {i}:\nInput: {ex['input']}\nOutput: {ex['output']}\n\n"
    prompt += f"Now process:\nInput: {query}\nOutput:"
    return prompt

# Usage
examples = [
    {"input": "The food was great", "output": '{"sentiment": "positive", "confidence": 0.95}'},
    {"input": "Terrible service", "output": '{"sentiment": "negative", "confidence": 0.90}'},
    {"input": "It was okay", "output": '{"sentiment": "neutral", "confidence": 0.70}'},
]
prompt = build_few_shot_prompt("Classify sentiment as JSON", examples, "Really loved it!")
```

## Chain-of-Thought Patterns

### Explicit CoT

```
Analyze this code for security vulnerabilities.

Think step by step:
1. Identify all user inputs
2. Trace each input through the code
3. Check if any input reaches a sensitive operation without sanitization
4. For each vulnerability found, classify severity (critical/high/medium/low)
5. Suggest a fix for each vulnerability

Code:
{code}
```

### Self-Consistency (Multiple CoT paths)

```python
import json
from collections import Counter

async def self_consistent_answer(question: str, n_paths: int = 5) -> str:
    answers = []
    for _ in range(n_paths):
        response = await llm.generate(
            f"Think step by step and answer: {question}\n\nFinal answer:",
            temperature=0.7,  # Higher temp for diversity
        )
        final = extract_final_answer(response)
        answers.append(final)

    # Majority vote
    most_common = Counter(answers).most_common(1)[0][0]
    return most_common
```

## Structured Output

### JSON Mode with Schema

```python
from pydantic import BaseModel, Field
from openai import OpenAI

class CodeReview(BaseModel):
    issues: list[dict] = Field(description="List of issues found")
    severity: str = Field(description="Overall severity: low|medium|high|critical")
    summary: str = Field(description="One-line summary")
    suggestions: list[str] = Field(description="Improvement suggestions")

client = OpenAI()

response = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Review code and output structured analysis."},
        {"role": "user", "content": f"Review this code:\n```\n{code}\n```"},
    ],
    response_format=CodeReview,
)

review = response.choices[0].message.parsed
```

### XML Tags for Claude

```
<task>Analyze the following error log and extract structured information.</task>

<rules>
- Extract timestamp, severity, service name, and error message
- Classify root cause category
- Output in the specified XML format
</rules>

<input>
{error_log}
</input>

<output_format>
<analysis>
  <timestamp>ISO 8601</timestamp>
  <severity>ERROR|WARN|FATAL</severity>
  <service>service name</service>
  <message>error message</message>
  <root_cause>category</root_cause>
  <suggested_fix>actionable fix</suggested_fix>
</analysis>
</output_format>
```

## Prompt Evaluation Framework

```python
class PromptEvaluator:
    def __init__(self, test_cases: list[dict]):
        self.test_cases = test_cases  # [{"input": ..., "expected": ..., "criteria": ...}]

    async def evaluate(self, prompt_template: str) -> dict:
        results = []
        for case in self.test_cases:
            prompt = prompt_template.format(**case["input"])
            output = await llm.generate(prompt)
            score = self._score(output, case["expected"], case.get("criteria", {}))
            results.append({"input": case["input"], "output": output, "score": score})

        return {
            "avg_score": sum(r["score"] for r in results) / len(results),
            "pass_rate": sum(1 for r in results if r["score"] >= 0.8) / len(results),
            "failures": [r for r in results if r["score"] < 0.8],
        }

    def _score(self, output: str, expected: str, criteria: dict) -> float:
        scores = []
        if "contains" in criteria:
            scores.append(1.0 if criteria["contains"] in output else 0.0)
        if "format" in criteria:
            scores.append(1.0 if self._check_format(output, criteria["format"]) else 0.0)
        if "max_length" in criteria:
            scores.append(1.0 if len(output) <= criteria["max_length"] else 0.0)
        return sum(scores) / len(scores) if scores else 0.5
```

## Checklist

- [ ] System prompt defines role, task, rules, and output format
- [ ] Few-shot examples cover edge cases (not just happy path)
- [ ] Chain-of-thought used for reasoning-heavy tasks
- [ ] Structured output enforced via JSON mode or XML tags
- [ ] Prompts tested with evaluation suite (10+ test cases)
- [ ] Temperature set appropriately (0 for deterministic, 0.7+ for creative)
- [ ] Prompt versioned and tracked alongside code
- [ ] Negative examples included ("Do NOT do X")

## Anti-Patterns

- Vague instructions without concrete examples
- Asking for multiple unrelated tasks in one prompt
- Not specifying output format (getting unparseable responses)
- Using temperature=0 for tasks needing diversity
- Prompt injection vulnerable (no input sanitization)
- Testing with only 1-2 examples (not statistically meaningful)
- Hardcoding prompts in application code (not configurable)
- Ignoring token limits (prompt + expected output exceeds context)
