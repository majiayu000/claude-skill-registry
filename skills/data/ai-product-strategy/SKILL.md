---
name: ai-product-strategy
description: Help users define AI product strategy. Use when someone is building an AI product, deciding where to apply AI in their product, planning an AI roadmap, evaluating build vs buy for AI capabilities, or figuring out how to integrate AI into existing products.
---

# AI Product Strategy

Help the user make strategic decisions about AI products using frameworks from 94 product leaders and AI practitioners.

## How to Help

When the user asks for help with AI product strategy:

1. **Understand the context** - Ask what they're building, what problem they're solving, and where they are in the AI journey
2. **Clarify the problem** - Help distinguish between "AI for AI's sake" and genuine user problems that AI can solve
3. **Guide architecture decisions** - Help them think through build vs buy, model selection, and human-AI boundaries
4. **Plan for iteration** - Emphasize feedback loops, evals, and building for rapid model improvements

## Core Principles

### Start with the problem, not the AI
Aishwarya Naresh Reganti: "In all the advancements of AI, one slippery slope is to keep thinking about solution complexity and forget the problem you're trying to solve. Start with minimal impact use cases to gain a grip on current capabilities."

### Define the human-AI boundary
Adriel Frederick: "When working on algorithmic products, your job is figuring out what the algorithm should be responsible for, what people are responsible for, and the framework for making decisions." This boundary is the core PM decision.

### AI is magical duct tape
Alex Komoroske: "LLMs are magical duct tape—distilled intuition of society. They make writing 'good enough' software significantly cheaper but increase marginal inference costs." Understand the new cost structure.

### Build for the slope, not the snapshot
Asha Sharma: "You have to build for the slope instead of the snapshot of where you are." AI capabilities change fast—build flexible architectures that can swap models as they improve.

### Design for squishiness
Alex Komoroske: "Even at 99% accuracy, if it punches the user in the face 1% of the time, that's not a viable product. Design assuming the AI will be squishy and not fully accurate."

### Flywheels beat first-mover advantage
Aishwarya Naresh Reganti: "It's not about being first to have an agent. It's about building the right flywheels to improve over time." Log human actions to create data loops for system improvement.

### Society of models, not single models
Amjad Masad: "Future products will be made of many different models—it's quite a heavy engineering project." Use specialized models for different tasks (reasoning vs speed vs coding).

### Use the right tool for each task
Albert Cheng: "We run chess engines for evaluations. LLMs translate that into natural language. Use the right technology for the right task." Don't use LLMs where deterministic algorithms excel.

### Humans are the bottleneck
Alexander Embiricos: "The current limiting factor is human typing speed and multitasking on prompts. Build systems that are 'default useful' without constant prompting."

### Account for non-determinism
Aishwarya Naresh Reganti: "Most people ignore the non-determinism. You don't know how users will behave with natural language, and you don't know how the LLM will respond." Build for variability.

### Agents need autonomy + complexity + natural interaction
Aparna Chennapragada: "Effective agents have (1) increasing autonomy to handle higher-order tasks, (2) ability to handle complex multi-step workflows, and (3) natural, often asynchronous interaction."

### Rebuild your intuitions
Aishwarya Naresh Reganti: "Leaders have to get hands-on—not implementing, but rebuilding intuitions. Be comfortable that your intuitions might not be right." Block time daily to stay current.

## Questions to Help Users

- "What specific user problem are you solving with AI?"
- "What should the AI decide vs. what should humans decide?"
- "How will you handle the 5% of cases where the AI fails?"
- "What feedback loops will improve the system over time?"
- "Are you building for today's model capabilities or anticipating improvements?"
- "Have you set up evals and observability?"

## Common Mistakes to Flag

- **AI for AI's sake** - Adding AI features without clear user problems
- **Single-model thinking** - Not considering specialized models for different tasks
- **Ignoring the failures** - Not designing UX for when AI gets it wrong
- **Static architecture** - Building systems that can't evolve with model improvements
- **Skipping evals** - Not establishing measurement and observability from day one
- **Over-automation** - Removing humans from loops where they add value

## Deep Dive

For all 179 insights from 94 guests, see `references/guest-insights.md`

## Related Skills

- Building with LLMs
- AI Evals
- Evaluating New Technology
- Platform Strategy
