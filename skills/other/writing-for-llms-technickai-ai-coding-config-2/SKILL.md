---
name: writing-for-llms
# prettier-ignore
description: Use when writing prompts, agent instructions, SKILL.md, commands, system prompts, Task tool prompts, prompt engineering, or LLM-to-LLM content
version: 1.0.0
category: meta
triggers:
  - "prompt"
  - "write prompt"
  - "system prompt"
  - "agent instructions"
  - "SKILL.md"
  - "prompt engineering"
  - "Task tool"
---

Apply the full prompt engineering standards from @rules/prompt-engineering.mdc

<key-principles>
- Show correct patterns only - never show anti-patterns, even labeled "wrong"
- State goals, not process - trust the executing model's capabilities
- Use XML tags for structure in complex prompts
- Clarity over brevity - every word that adds clarity is worth including
- Few-shot examples must follow identical structure
- Front-load critical information
- Consistent terminology throughout
</key-principles>

<quality-check>
Before finalizing:
- No anti-patterns shown anywhere
- All examples structurally consistent
- Goals clear, process not over-prescribed
- Terminology consistent
- Critical info front-loaded
</quality-check>
