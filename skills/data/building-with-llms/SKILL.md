---
name: building-with-llms
description: Help users build effective AI applications. Use when someone is building with LLMs, writing prompts, designing AI features, implementing RAG, creating agents, running evals, or trying to improve AI output quality.
---

# Building with LLMs

Help the user build effective AI applications using practical techniques from 60 product leaders and AI practitioners.

## How to Help

When the user asks for help building with LLMs:

1. **Understand their use case** - Ask what they're building (chatbot, agent, content generation, code assistant, etc.)
2. **Diagnose the problem** - Help identify if issues are prompt-related, context-related, or model-selection related
3. **Apply relevant techniques** - Share specific prompting patterns, architecture approaches, or evaluation methods
4. **Challenge common mistakes** - Push back on over-reliance on vibes, skipping evals, or using the wrong model for the task

## Core Principles

### Prompting

**Few-shot examples beat descriptions**
Sander Schulhoff: "If there's one technique I'd recommend, it's few-shot prompting—giving examples of what you want. Instead of describing your writing style, paste a few previous emails and say 'write like this.'"

**Provide your point of view**
Wes Kao: "Sharing my POV makes output way better. Don't just ask 'What would you say?' Tell it: 'I want to say no, but I'd like to preserve the relationship. Here's what I'd ideally do...'"

**Use decomposition for complex tasks**
Sander Schulhoff: "Ask 'What subproblems need solving first?' Get the list, solve each one, then synthesize. Don't ask the model to solve everything at once."

**Self-criticism improves output**
Sander Schulhoff: "Ask the LLM to check and critique its own response, then improve it. Models can catch their own errors when prompted to look."

**Roles help style, not accuracy**
Sander Schulhoff: "Roles like 'Act as a professor' don't help accuracy tasks. But they're great for controlling tone and style in creative work."

**Put context at the beginning**
Sander Schulhoff: "Place long context at the start of your prompt. It gets cached (cheaper), and the model won't forget its task when processing."

### Architecture

**Context engineering > prompt engineering**
Bret Taylor: "If a model makes a bad decision, it's usually lack of context. Fix it at the root—feed better data via MCP or RAG."

**RAG quality = data prep quality**
Chip Huyen: "The biggest gains come from data preparation, not vector database choice. Rewrite source data into Q&A format. Add annotations for context humans take for granted."

**Layer models for robustness**
Bret Taylor: "Having AI supervise AI is effective. Layer cognitive steps—one model generates, another reviews. This moves you from 90% to 99% accuracy."

**Use specialized models for specialized tasks**
Amjad Masad: "We use Claude Sonnet for coding, other models for critiquing. A 'society of models' with different roles outperforms one general model."

**200ms is the latency threshold**
Ryan J. Salva (GitHub Copilot): "The sweet spot for real-time suggestions is ~200ms. Slower feels like an interruption. Design your architecture around this constraint."

### Evaluation

**Evals are mandatory, not optional**
Kevin Weil (OpenAI): "Writing evals is becoming a core product skill. A 60% reliable model needs different UX than 95% or 99.5%. You can't design without knowing your accuracy."

**Binary scores > Likert scales**
Hamel Husain: "Force Pass/Fail, not 1-5 scores. Scales produce meaningless averages like '3.7'. Binary forces real decisions."

**Start with vibes, evolve to evals**
Howie Liu: "For novel products, start with open-ended vibes testing. Only move to formal evals once use cases converge."

**Validate your LLM judge**
Hamel Husain: "If using LLM-as-judge, you must eval the eval. Measure agreement with human experts. Iterate until it aligns."

### Building & Iteration

**Retry failures—models are stochastic**
Benjamin Mann (Anthropic): "If it fails, try the exact same prompt again. Success rates are much higher on retry than on banging on a broken approach."

**Be ambitious in your asks**
Benjamin Mann: "The difference between effective and ineffective Claude Code users: ambitious requests. Ask for the big change, not incremental tweaks."

**Cross-pollinate between models**
Guillermo Rauch: "When stuck after 100+ iterations, copy the code to a different model (e.g., from v0 to ChatGPT o1). Fresh perspective unblocks you."

**Compounding engineering**
Dan Shipper: "For every unit of work, make the next unit easier. Save prompts that work. Build a library. Your team's AI effectiveness compounds."

### Working with AI Tools

**Learn to read and debug, not memorize syntax**
Amjad Masad: "The ROI on coding doubles every 6 months because AI amplifies it. Focus on reading code and debugging—syntax is handled."

**Use chat mode to understand**
Anton Osika: "Use 'chat mode' to ask the AI to explain its logic. 'Why did you do this? What am I missing?' Treat it as a tutor."

**Vibe coding is a real skill**
Elena Verna: "I put vibe coding on my resume. Build functional prototypes with natural language before handing to engineering."

## Questions to Help Users

- "What are you building and what's the core user problem?"
- "What does the model get wrong most often?"
- "Are you measuring success systematically or going on vibes?"
- "What context does the model have access to?"
- "Have you tried few-shot examples?"
- "What happens when you retry failed prompts?"

## Common Mistakes to Flag

- **Vibes forever** - Eventually you need real evals, not just "it feels good"
- **Prompt-only thinking** - Often the fix is better context, not better prompts
- **One model for everything** - Different models excel at different tasks
- **Giving up after one failure** - Stochastic systems need retries
- **Skipping the human review** - AI output needs human validation, especially early on

## Deep Dive

For all 110 insights from 60 guests, see `references/guest-insights.md`

## Related Skills

- AI Product Strategy
- AI Evals
- Vibe Coding
- Evaluating New Technology
