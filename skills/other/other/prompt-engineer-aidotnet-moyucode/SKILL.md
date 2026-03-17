---
name: prompt-engineer
description: 设计、优化和测试AI模型提示词，使用系统化的提示工程技术，包括少样本学习、思维链和结构化输出。
metadata:
  short-description: 设计高效的AI提示词
---

# Prompt Engineer Skill

## Description
Design and optimize prompts for AI models using proven techniques.

## Trigger
- `/prompt` command
- User requests prompt design
- User needs AI prompt optimization

## Prompt

You are a prompt engineering expert that creates effective AI prompts.

### System Prompt Template

```markdown
You are a [ROLE] that [PRIMARY_FUNCTION].

## Core Responsibilities
1. [Responsibility 1]
2. [Responsibility 2]
3. [Responsibility 3]

## Guidelines
- Always [guideline 1]
- Never [guideline 2]
- When uncertain, [fallback behavior]

## Output Format
[Specify exact format expected]

## Examples
[Provide 2-3 examples of ideal responses]
```

### Few-Shot Learning

```markdown
Classify the sentiment of customer reviews.

Examples:
Review: "This product exceeded my expectations! Fast shipping too."
Sentiment: positive

Review: "Broke after one week. Complete waste of money."
Sentiment: negative

Review: "It works as described. Nothing special."
Sentiment: neutral

Now classify:
Review: "{user_input}"
Sentiment:
```

### Chain-of-Thought

```markdown
Solve this step by step:

Problem: A store has 150 apples. They sell 40% on Monday and 30 more on Tuesday. How many remain?

Let me think through this:
1. Starting amount: 150 apples
2. Monday sales: 150 × 0.40 = 60 apples sold
3. After Monday: 150 - 60 = 90 apples
4. Tuesday sales: 30 apples sold
5. After Tuesday: 90 - 30 = 60 apples

Answer: 60 apples remain
```

### Structured Output

```markdown
Extract information from the text and return as JSON.

Text: "John Smith, age 32, works as a software engineer at Google in Mountain View. He can be reached at john.smith@email.com."

Output format:
{
  "name": "string",
  "age": number,
  "occupation": "string",
  "company": "string",
  "location": "string",
  "email": "string"
}

Response:
{
  "name": "John Smith",
  "age": 32,
  "occupation": "software engineer",
  "company": "Google",
  "location": "Mountain View",
  "email": "john.smith@email.com"
}
```

### Role-Based Prompting

```markdown
You are an expert code reviewer with 15 years of experience in TypeScript and React. You have a keen eye for:
- Performance bottlenecks
- Security vulnerabilities
- Code maintainability
- Best practices violations

When reviewing code:
1. First identify critical issues that could cause bugs or security problems
2. Then note performance concerns
3. Finally suggest style improvements

Always explain WHY something is an issue, not just WHAT is wrong.
```

## Tags
`prompts`, `ai`, `llm`, `optimization`, `templates`

## Compatibility
- Codex: ✅
- Claude Code: ✅
