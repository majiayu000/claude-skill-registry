---
name: deep-research
description: Deep research via Gemini CLI OR free search APIs — runs in background sub-agent to save Claude tokens.
homepage: https://github.com/Khamel83/oneshot
allowed-tools: Read, Write, Edit, Bash, Task, TaskOutput
metadata: {"oneshot":{"emoji":"🔬","requires":{"bins":["gemini"],"optional":["curl"]}}}
---

# Deep Research Skill

Conduct deep research using **either** Gemini CLI **or** free search APIs. Runs in a background sub-agent so you don't burn Claude tokens.

## When To Use

User says any of:
- "Research: [topic]" or "Deep research on [topic]"
- "Look into [topic]" or "Investigate [topic]"
- "What do you know about [topic]?"
- "Find out about [topic]"
- Web search fails and you need to research

## Two Research Modes

### Mode 1: Gemini CLI (Primary)
- Uses your Google AI subscription
- Deep, contextual research
- No Claude tokens burned
- Requires: `gemini` CLI installed

### Mode 2: Free Search APIs (Fallback)
- Tavily, Brave, or Bing APIs
- Web-style search results
- No rate limits like WebSearch
- Requires: Free API key (sign up once)

---

## How It Works

### Step 1: Clarifying Questions (Always)

Before running any research, ask 2-3 quick questions to focus the work:

**Start with the goal:**
> "Before I dive in - what's your goal here? Are you learning about this topic, making a decision, writing something, or just curious?"

**Then adapt based on their answer:**

If learning/curious:
- "Any specific aspect you're most interested in?"
- "How technical should I go? (High-level overview vs deep technical detail)"

If decision-making:
- "What decision are you trying to make?"
- "Any specific criteria or constraints I should focus on?"

If writing/creating:
- "What's the output? (Blog post, report, presentation?)"
- "Who's the audience?"

**Keep it natural — 2-3 questions max.** Don't interrogate.

### Step 2: Choose Mode & Spawn Agent

Check if `gemini` CLI is available. If yes, use Mode 1. If no, ask user if they want Mode 2 (and offer to help set up).

**MODE 1 - Gemini CLI:**

```
Task(
  subagent_type: "general-purpose",
  prompt: "DEEP RESEARCH TASK: [FULL TOPIC WITH CONTEXT]

You are a research sub-agent. Use Gemini CLI to conduct thorough research and save results.

CONTEXT FROM USER:
[Include all conversation context about goals, depth, audience]

INSTRUCTIONS:

1. Run Gemini CLI with a comprehensive research prompt:
   gemini --yolo \"[COMPREHENSIVE RESEARCH PROMPT]\"

   The research prompt should cover:
   - Overview & Core Concepts - what is this, terminology, why it matters
   - Current State - latest developments, major players
   - Technical Deep Dive - how it works, mechanisms, key techniques
   - Practical Applications - real-world use cases, tools available
   - Challenges & Open Problems - technical, ethical, barriers
   - Future Outlook - trends, predictions, emerging areas
   - Resources - key papers, researchers, communities, courses

2. Save output to: ~/github/oneshot/research/[slug]/research.md

3. Structure the report:
   ```markdown
   # Research: [Topic]

   **Date:** [timestamp]
   **Goal:** [user's goal from context]
   **Depth:** [overview/technical/deep-dive]

   ## Executive Summary
   [3-5 bullet points of key findings]

   ## Overview & Core Concepts
   [...]

   ## Current State
   [...]

   ## Technical Deep Dive
   [...]

   ## Practical Applications
   [...]

   ## Challenges & Open Problems
   [...]

   ## Future Outlook
   [...]

   ## Resources
   - Papers: [...]
   - Tools: [...]
   - Communities: [...]
   - Courses: [...]
   ```

4. Be thorough (aim for 500+ lines). Include specific examples and citations.",
  description: "Gemini research: [topic]",
  run_in_background: true
)
```

**MODE 2 - Free Search APIs:**

```
Task(
  subagent_type: "general-purpose",
  prompt: "WEB RESEARCH TASK: [FULL TOPIC WITH CONTEXT]

You are a research sub-agent. Use free search APIs to gather information and compile a research report.

CONTEXT FROM USER:
[Include all conversation context about goals, depth, audience]

AVAILABLE SEARCH APIs (use in order, fallback if one fails):

1. Tavily Search (1000 free searches/month)
   curl -s https://api.tavily.com/search \\
     -H \"Content-Type: application/json\" \\
     -d '{\"api_key\": \"TAVILY_API_KEY\", \"query\": \"[query]\", \"search_depth\": \"advanced\", \"include_answer\": true}'

2. Brave Search API (2000 free requests/month)
   curl -s \"https://api.search.brave.com/res/v1/web/search?q=[query]&count=10\" \\
     -H \"Accept: application/json\" \\
     -H \"X-Subscription-Token: BRAVE_API_KEY\"

3. Bing Web Search API (1000 free queries/month)
   curl -s \"https://api.bing.microsoft.com/v7.0/search?q=[query]&count=10\" \\
     -H \"Ocp-Apim-Subscription-Key: BING_API_KEY\"

API keys are stored in ~/github/oneshot/secrets/research_secrets.enc.json
Decrypt with: sops -d --extract '[\"tavily_api_key\"]' ~/github/oneshot/secrets/research_secrets.enc.json

INSTRUCTIONS:

1. Design 3-5 search queries that cover different aspects of the topic
2. Run searches using the available APIs
3. Compile results into a comprehensive report
4. Save to: ~/github/oneshot/research/[slug]/research.md

5. Structure the report (same as Mode 1 above)

Be thorough. Synthesize information from multiple sources.",
  description: "API research: [topic]",
  run_in_background: true
)
```

### Step 3: Present Findings

When the background agent completes:
- Use TaskOutput to get the results
- Share the key findings with the user
- Offer to read the full report or dive deeper on sections

---

## Output Location

Research saved to:
```
~/github/oneshot/research/<slug>/research.md
```

---

## Setup

### Option 1: Gemini CLI (Recommended for deep research)

```bash
# Install via npm
npm install -g @google/gemini-cli

# Authenticate
gemini auth login
```

### Option 2: Free Search APIs (Recommended for web-style research)

Pick one (or more for redundancy):

**Tavily** (1000 free searches/month - Best for AI answers):
- Sign up: https://tavily.com
- Get API key from dashboard

**Brave Search** (2000 free requests/month - Clean results):
- Sign up: https://brave.com/search/api/
- Get API key from dashboard

**Bing Search** (1000 free queries/month - Familiar results):
- Sign up: https://www.microsoft.com/cognitive-services
- Get Bing Web Search API key

Then store the key securely:

```bash
cd ~/github/oneshot/secrets
sops research_secrets.enc.json
```

Add:
```json
{
  "tavily_api_key": "your-key-here",
  "brave_api_key": "your-key-here",
  "bing_api_key": "your-key-here"
}
```

---

## Quick Decision Guide

| Need | Use |
|------|-----|
| Deep, contextual understanding | Gemini CLI |
| Quick facts, current info | Search APIs |
| Long-form research | Gemini CLI |
| Web-style results | Search APIs |
| No extra setup | Search APIs (just get key) |

---

## Tips

- Research typically takes 3-8 minutes
- Check `~/github/oneshot/research/` for past research
- Always include conversation context in the task
- Use slugified names (e.g., "quantum-computing-basics")
- The `--yolo` flag in gemini auto-approves file operations

## Keywords

research, deep research, gemini, background agent, tavily, brave search, bing search
