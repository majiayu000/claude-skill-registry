---
name: claude
description: Anthropic Claude AI models for analysis and coding. Use for AI assistants.
---

# Claude

Claude (by Anthropic) is OpenAI's main competitor. It is famous for its **large context window** (200k+), low hallucination rates, and "Artifacts" UI.

## When to Use

- **Coding**: Claude 3.5 Sonnet is widely considered the best coding model in 2025.
- **Long Context**: Analyzing massive PDFs or codebases.
- **Safety**: Enterprise-grade safety guardrails.

## Core Concepts

### Models

- **Opus**: The smartest, largest model.
- **Sonnet**: The sweet spot. Fast and incredibly capable.
- **Haiku**: Fast and cheap.

### Artifacts

A UI feature (now an API pattern) where the model generates standalone content (React components, SVGs) in a side window.

### Computer Use

Claude can interact with a computer GUI (moving mouse, clicking) via API.

## Best Practices (2025)

**Do**:

- **Use Sonnet for Dev**: It beats GPT-4o in many coding benchmarks.
- **Use XML Tags**: Claude loves `<instructions>` and `<context>` tags in prompts.
- **Prefill Responses**: Guide Claude by prefilling the `{"role": "assistant", "content": "{"}` to force JSON.

**Don't**:

- **Don't ignore System Prompts**: Claude relies heavily on strong system instructions.

## References

- [Anthropic Documentation](https://docs.anthropic.com/)
