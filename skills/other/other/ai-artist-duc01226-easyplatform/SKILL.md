---
name: ai-artist
version: 1.0.0
description: '[AI & Tools] Write and optimize prompts for AI-generated outcomes across text and image models. Use when crafting prompts for LLMs (Claude, GPT, Gemini), image generators (Midjourney, DALL-E, Stable Diffusion, Imagen, Flux), or video generators (Veo, Runway). Covers prompt structure, style keywords, negative prompts, chain-of-thought, few-shot examples, iterative refinement, and domain-specific patterns for marketing, code, and creative writing.'

allowed-tools: NONE
license: MIT
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Write and optimize prompts for AI text, image, and video generation models (Claude, GPT, Midjourney, DALL-E, Stable Diffusion, Flux, Veo).

**Workflow:**

1. **Identify** — Determine model type (LLM, image, video) and desired outcome
2. **Structure** — Apply model-specific prompt patterns (Role/Context/Task for LLMs, Subject/Style/Composition for images)
3. **Refine** — Iterate with A/B testing, style keywords, negative prompts

**Key Rules:**

- Use clarity, context, structure, and iteration as core principles
- Apply model-specific syntax (Midjourney `--ar`, SD weighted tokens, etc.)
- Load reference files for detailed guidance per domain (marketing, code, writing, data)

# AI Artist - Prompt Engineering

Craft effective prompts for AI text and image generation models.

## Core Principles

1. **Clarity** - Be specific, avoid ambiguity
2. **Context** - Set scene, role, constraints upfront
3. **Structure** - Use consistent formatting (markdown, XML tags, delimiters)
4. **Iteration** - Refine based on outputs, A/B test variations

## Quick Patterns

### LLM Prompts (Claude/GPT/Gemini)

```
[Role] You are a {expert type} specializing in {domain}.
[Context] {Background information and constraints}
[Task] {Specific action to perform}
[Format] {Output structure - JSON, markdown, list, etc.}
[Examples] {1-3 few-shot examples if needed}
```

### Image Generation (Midjourney/DALL-E/Stable Diffusion)

```
[Subject] {main subject with details}
[Style] {artistic style, medium, artist reference}
[Composition] {framing, angle, lighting}
[Quality] {resolution modifiers, rendering quality}
[Negative] {what to avoid - only if supported}
```

**Example**: `Portrait of a cyberpunk hacker, neon lighting, cinematic composition, detailed face, 8k, artstation quality --ar 16:9 --style raw`

## References

Load for detailed guidance:

| Topic        | File                                | Description                                                |
| ------------ | ----------------------------------- | ---------------------------------------------------------- |
| LLM          | `references/llm-prompting.md`       | System prompts, few-shot, CoT, output formatting           |
| Image        | `references/image-prompting.md`     | Style keywords, model syntax, negative prompts             |
| Nano Banana  | `references/nano-banana.md`         | Gemini image prompting, narrative style, multi-image input |
| Advanced     | `references/advanced-techniques.md` | Meta-prompting, chaining, A/B testing                      |
| Domain Index | `references/domain-patterns.md`     | Universal pattern, links to domain files                   |
| Marketing    | `references/domain-marketing.md`    | Headlines, product copy, emails, ads                       |
| Code         | `references/domain-code.md`         | Functions, review, refactoring, debugging                  |
| Writing      | `references/domain-writing.md`      | Stories, characters, dialogue, editing                     |
| Data         | `references/domain-data.md`         | Extraction, analysis, comparison                           |

## Model-Specific Tips

| Model            | Key Syntax                                          |
| ---------------- | --------------------------------------------------- |
| Midjourney       | `--ar`, `--style`, `--chaos`, `--weird`, `--v 6.1`  |
| DALL-E 3         | Natural language, no parameters, HD quality option  |
| Stable Diffusion | Weighted tokens `(word:1.2)`, LoRA, negative prompt |
| Flux             | Natural prompts, style mixing, `--guidance`         |
| Imagen/Veo       | Descriptive text, aspect ratio, style references    |

## Anti-Patterns

- Vague instructions ("make it better")
- Conflicting constraints
- Missing context for domain tasks
- Over-prompting with redundant details
- Ignoring model-specific strengths/limits

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
