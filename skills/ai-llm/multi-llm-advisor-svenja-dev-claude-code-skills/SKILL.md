---
name: multi-llm-advisor
description: Fetches additional perspectives from OpenAI Codex and Google Gemini for architecture, review, and debugging. Transparently displays all LLM calls.
triggers:
  - architecture decisions
  - code review requests
  - debugging complex issues
  - when user asks for second opinion
---

# Multi-LLM Advisor

This skill calls Codex 5.1 Pro and Gemini 3 Pro to provide additional perspectives.

## When to Activate

- Architecture decisions (new features, refactoring)
- Code review (before commits, PRs)
- Debugging (complex errors, performance issues)
- On explicit request ("second opinion", "different perspective")

## Usage

```
Use the multi-llm-advisor skill to get architecture feedback on [topic]
Use the multi-llm-advisor skill to review this code
Use the multi-llm-advisor skill to debug [issue]
```

## Transparency Format

Every invocation displays the following:

```
+==============================================================+
|  MULTI-LLM ADVISOR - [MODE: ARCHITECTURE|REVIEW|DEBUG]       |
+==============================================================+
|  CONTEXT SENT TO LLMs:                                       |
|  - Files: [list]                                             |
|  - Question: [prompt]                                        |
|  - Tokens: ~[count]                                          |
+--------------------------------------------------------------+
|  CODEX 5.1 PRO RESPONSE:                                     |
|  [response]                                                  |
+--------------------------------------------------------------+
|  GEMINI 3 PRO RESPONSE:                                      |
|  [response]                                                  |
+--------------------------------------------------------------+
|  SYNTHESIS (Claude's Recommendation):                        |
|  [combined analysis]                                         |
+==============================================================+
```

## Prompt Templates

### Architecture Mode
```
You are a senior software architect. Analyze this architecture decision:

CONTEXT:
{context}

QUESTION:
{question}

CURRENT STACK:
{stack}

Provide:
1. Pros/Cons of the proposed approach
2. Alternative approaches (max 2)
3. Potential risks and mitigations
4. Recommendation with reasoning

Be concise. Max 300 words.
```

### Review Mode
```
You are a senior code reviewer. Review this code:

CODE:
{code}

LANGUAGE: {language}
PROJECT TYPE: {project_type}

Focus on:
1. Security vulnerabilities (OWASP Top 10)
2. Performance issues
3. Maintainability concerns
4. TypeScript/type safety (if applicable)

Format: Bullet points, max 200 words.
```

### Debug Mode
```
You are a debugging expert. Analyze this issue:

ERROR/SYMPTOM:
{error}

RELEVANT CODE:
{code}

CONTEXT:
{context}

Provide:
1. Root cause analysis (most likely)
2. 2-3 diagnostic steps
3. Suggested fix with code

Be specific and actionable. Max 250 words.
```

## API Configuration

Environment variables (store in `.env` or system env):
- `OPENAI_API_KEY` - For Codex 5.1 Pro
- `GOOGLE_AI_API_KEY` - For Gemini 3 Pro (same as gemini-image-gen)

## Script Location

`~/.claude/skills/multi-llm-advisor/advisor.ts`

## Hook Integration

Triggered via `multi-llm-advisor-hook.ts` when:
- PreToolUse: Detects architecture/review/debug keywords
- Manual: User explicitly requests second opinion

## Real-World Example

When building the Gemini API integration at [fabrikIQ.com](https://www.fabrikiq.com), this skill helped decide between:
- Vertex AI (enterprise, EU region support) vs Google AI Studio (simpler)
- Streaming vs batch responses for large manufacturing datasets
- The synthesis recommended Vertex AI for GDPR compliance, which proved correct.
