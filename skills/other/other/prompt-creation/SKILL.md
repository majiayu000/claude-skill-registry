---
name: prompt-creation
description: Techniques and templates for creating optimal prompts following Anthropic conventions
allowed-tools: Read, Write
---

# Prompt Creation

Skill for creating high-performance prompts following 2025 best practices and Anthropic conventions.

## Documentation

- [techniques.md](docs/techniques.md) - Structuring techniques (CoT, Few-shot, etc.)
- [templates.md](docs/templates.md) - Reusable templates

## Anthropic Official Structure (9 Elements)

Each system prompt should cover these 9 aspects:

### 1. Task Context
```markdown
# Task Context
You are an expert [ROLE] specializing in [DOMAIN].
Your goal is to [PRIMARY_OBJECTIVE].
```

### 2. Tone Context
```markdown
# Tone
- Tone: [formal/casual/technical/friendly]
- Length: [concise/detailed/adaptive]
- Format: [prose/lists/tables/mixed]
```

### 3. Task Description + Rules
```markdown
# Task Description
Here are important rules:
- Always [MANDATORY_BEHAVIOR]
- Never [FORBIDDEN_BEHAVIOR]
- If [CONDITION] then [ACTION]

If unsure, say "I don't have enough information to answer."
```

### 4. Examples (Few-shot)
```markdown
# Examples

<example>
Input: [STANDARD_CASE_INPUT]
Output: [EXPECTED_OUTPUT]
</example>

<example>
Input: [EDGE_CASE_INPUT]
Output: [EXPECTED_OUTPUT]
</example>
```

### 5. Input Data
```markdown
# Input Data
<document>
[USER_PROVIDED_CONTENT]
</document>
```

### 6. Immediate Task
```markdown
# Immediate Task
Now, [SPECIFIC_ACTION] the above [document/code/data].
```

### 7. Precognition (Scratchpad)
```markdown
# Precognition
First, in <scratchpad> tags, analyze the key points.
Then provide your final answer in <answer> tags.
```

### 8. Output Formatting
```markdown
# Output Format

## Analysis
[Problem understanding]

## Solution
[Main response]

## Recommendations
[Additional suggestions]
```

### 9. Prefill (Assistant Turn)
```markdown
# Prefill
<scratchpad>
```

## Emphasis Techniques

In order of increasing effectiveness:

| Level | Syntax | Usage |
|-------|--------|-------|
| 1 | `Please do X` | Suggestion |
| 2 | `You should do X` | Recommendation |
| 3 | `Always do X` | Standard rule |
| 4 | `YOU MUST do X` | Strong rule |
| 5 | `IMPORTANT: Do X` | Critical rule |
| 6 | `CRITICAL - ZERO TOLERANCE: Do X` | Absolute rule |

## Creation Workflow

```
1. DEFINE the objective (1 sentence)
   ↓
2. IDENTIFY target audience
   ↓
3. LIST constraints
   ↓
4. CHOOSE techniques (CoT? Few-shot?)
   ↓
5. WRITE with 9-element structure
   ↓
6. ADD guardrails
   ↓
7. TEST mentally (edge cases)
   ↓
8. ITERATE if necessary
```

## Forbidden

- Never create prompts without clear objective
- Never write ambiguous instructions
- Never forget error cases
- Never ignore target model context
