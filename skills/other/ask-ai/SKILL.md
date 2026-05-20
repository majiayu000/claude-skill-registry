---
name: ask-ai
description: "Use external AI assistants (ChatGPT, Claude, Gemini, DeepSeek) when agent encounters difficult problems. Trigger when: (1) User explicitly asks to consult AI, (2) Agent cannot solve the problem independently, (3) Knowledge gaps or needing deeper explanations, (4) Complex problems requiring multi-round reasoning. Provides two modes: Ask Mode (ask user first) and Trust Mode (auto ask)."
---

# ask-ai

Use external AI assistants when you need help solving complex problems.

## When to Use

- User explicitly asks: "Ask AI", "Ask ChatGPT", "Consult AI"
- You encounter knowledge gaps or cannot solve independently
- Need deeper explanations or multi-round reasoning
- Complex problems requiring external expertise

## Two Modes

| Mode | Behavior |
|------|----------|
| **Ask Mode** (default) | Ask user first: "Need help from GPT?" |
| **Trust Mode** | Automatically ask AI without asking |

**Switch modes:** Say "Trust Mode" → auto mode | "Ask Mode" → default

## Supported AI

- ChatGPT: https://chatgpt.com
- Claude: https://claude.ai  
- Gemini: https://gemini.google.com
- DeepSeek: https://chat.deepseek.com

## Workflow

**Ask Mode:**
1. Encounter difficult problem → Ask user: "This is tricky. Want me to ask GPT?"
2. User agrees → Open AI assistant
3. Get answer → Report to user

**Trust Mode:**
1. Encounter difficult problem → Automatically open AI
2. Get answer → Solve directly

## Communication

- Asking: "Let me ask GPT for help. Is that okay?"
- Auto: "I'll ask GPT for help. One moment."
- After answer: "Got the answer from [AI]: [summary]. Want details?"
