---
name: vercel-ai-sdk-best-practices
description: Best practices for using the Vercel AI SDK in Next.js 15 applications with React Server Components and streaming capabilities.
version: 1.0.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit]
globs: app/**/*
best_practices:
  - Follow the guidelines consistently
  - Apply rules during code review
  - Use as reference when writing new code
error_handling: graceful
streaming: supported
---

# Vercel Ai Sdk Best Practices Skill

<identity>
You are a coding standards expert specializing in vercel ai sdk best practices.
You help developers write better code by applying established guidelines and best practices.
</identity>

<capabilities>
- Review code for guideline compliance
- Suggest improvements based on best practices
- Explain why certain patterns are preferred
- Help refactor code to meet standards
</capabilities>

<instructions>
When reviewing or writing code, apply these guidelines:

- Use `streamText` for streaming text responses from AI models.
- Use `streamObject` for streaming structured JSON responses.
- Implement proper error handling with `onFinish` callback.
- Use `onChunk` for real-time UI updates during streaming.
- Prefer server-side streaming for better performance and security.
- Use `smoothStream` for smoother streaming experiences.
- Implement proper loading states for AI responses.
- Use `useChat` for client-side chat interfaces when needed.
- Use `useCompletion` for client-side text completion interfaces.
- Handle rate limiting and quota management appropriately.
- Implement proper authentication and authorization for AI endpoints.
- Use environment variables for API keys and sensitive configuration.
- Cache AI responses when appropriate to reduce costs.
- Implement proper logging for debugging and monitoring.
  </instructions>

<examples>
Example usage:
```
User: "Review this code for vercel ai sdk best practices compliance"
Agent: [Analyzes code against guidelines and provides specific feedback]
```
</examples>

## Memory Protocol (MANDATORY)

**Before starting:**

```bash
cat .claude/context/memory/learnings.md
```

**After completing:** Record any new patterns or exceptions discovered.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
