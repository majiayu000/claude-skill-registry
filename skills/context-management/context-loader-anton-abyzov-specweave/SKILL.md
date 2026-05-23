---
name: context-loader
description: Explains how SpecWeave achieves context efficiency through Claude's native progressive disclosure and sub-agent parallelization. Use when asking about token usage, context management, or how SpecWeave scales with large projects. Leverages Claude's built-in mechanisms without custom caching.
---

# Context Management in SpecWeave

## Overview

SpecWeave achieves efficient context usage through **two native Claude Code mechanisms**:

1. **Progressive Disclosure** (Skills) - Claude's built-in skill loading system
2. **Sub-Agent Parallelization** - Isolated context windows for parallel work

**Important**: SpecWeave does NOT use custom context manifests or caching systems. It leverages Claude's native capabilities.

---

## 1. Progressive Disclosure (Skills)

### How It Works

Claude Code uses a **two-level progressive disclosure system** for skills:

#### Level 1: Metadata Only (Always Loaded)

```yaml
---
name: nextjs
description: NextJS 14+ implementation specialist. Creates App Router projects...
---
```

**What Claude sees initially:**
- Only the YAML frontmatter (name + description)
- ~50-100 tokens per skill
- **All** skills' metadata is visible
- Claude can decide which skills are relevant

#### Level 2: Full Skill Content (Loaded On-Demand)

```markdown
# NextJS Skill

[Full documentation, examples, best practices...]
[Could be 5,000+ tokens]
```

**What Claude loads:**
- Full SKILL.md content **only if** skill is relevant to current task
- Prevents loading 35+ skills (175,000+ tokens) when you only need 2-3
- **This is the actual mechanism** that saves tokens

### Example Workflow

```
User: "Create a Next.js authentication page"
    ↓
Claude reviews skill metadata (35 skills × 75 tokens = 2,625 tokens)
    ↓
Claude determines relevant skills:
  - nextjs (matches "Next.js")
  - frontend (matches "page")
  - (NOT loading: python-backend, devops, hetzner-provisioner, etc.)
    ↓
Claude loads ONLY relevant skills:
  - nextjs: 5,234 tokens
  - frontend: 3,891 tokens
    ↓
Total loaded: 9,125 tokens (vs 175,000+ if loading all skills)
Token reduction: ~95%
```

### References

- [What are Skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Agent Skills Engineering](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

> "Skills work through progressive disclosure—Claude determines which Skills are relevant and loads the information it needs to complete that task, helping to prevent context window overload."

---

## 2. Sub-Agent Parallelization

### How It Works

Sub-agents in Claude Code have **isolated context windows**:

```
Main conversation (100K tokens used)
    ↓
Launches 3 sub-agents in parallel
    ↓
├─ Sub-agent 1: Fresh context (0K tokens used)
├─ Sub-agent 2: Fresh context (0K tokens used)
└─ Sub-agent 3: Fresh context (0K tokens used)
```

**Benefits:**

1. **Context Isolation**
   - Each sub-agent starts with empty context
   - Doesn't inherit main conversation's 100K tokens
   - Can load its own relevant skills

2. **Parallelization**
   - Multiple agents work simultaneously
   - Each with own context budget
   - Results merged back to main conversation

3. **Token Multiplication**
   - Main: 200K token limit
   - Sub-agent 1: 200K token limit
   - Sub-agent 2: 200K token limit
   - **Effective capacity**: 600K+ tokens across parallel work

### Example Workflow

```
User: "Build a full-stack Next.js app with auth, payments, and admin"
    ↓
Main conversation launches 3 sub-agents in parallel:
    ↓
├─ Sub-agent 1 (Frontend)
│  - Loads: nextjs, frontend skills
│  - Context: 12K tokens
│  - Implements: Auth UI, payment forms
│
├─ Sub-agent 2 (Backend)
│  - Loads: nodejs-backend, security skills
│  - Context: 15K tokens
│  - Implements: API routes, auth logic
│
└─ Sub-agent 3 (DevOps)
   - Loads: devops, hetzner-provisioner skills
   - Context: 8K tokens
   - Implements: Deployment configs
    ↓
All 3 work in parallel with isolated contexts
    ↓
Results merged back to main conversation
    ↓
Total effective context: 35K tokens across 3 agents
(vs 175K+ if loaded all skills in main conversation)
```

### References

- [Sub-Agents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)

---

## Actual Token Savings

### Progressive Disclosure Savings

**Scenario**: User asks about Next.js

**Without progressive disclosure:**
```
Load all 35 skills: ~175,000 tokens
Context bloat: Massive
```

**With progressive disclosure:**
```
Metadata (all skills): ~2,625 tokens
Load relevant (2 skills): ~9,000 tokens
Total: ~11,625 tokens
Reduction: ~93%
```

### Sub-Agent Savings

**Scenario**: Complex multi-domain task

**Single agent approach:**
```
Load all relevant skills: ~50,000 tokens
Main conversation history: ~80,000 tokens
Total context used: ~130,000 tokens
Risk: Approaching context limit
```

**Sub-agent approach:**
```
Main conversation: ~5,000 tokens (coordination only)
Sub-agent 1: ~15,000 tokens (isolated)
Sub-agent 2: ~18,000 tokens (isolated)
Sub-agent 3: ~12,000 tokens (isolated)
Total: ~50,000 tokens across 4 contexts
Reduction: ~62% (130K → 50K)
```

**Note**: Exact percentages vary by task complexity. These are approximate based on typical usage patterns.

---

## How SpecWeave Leverages These Mechanisms

### 1. Skill Organization (Progressive Disclosure)

SpecWeave organizes **35+ skills** with clear, focused descriptions:

```yaml
# Good: Focused description
---
name: nextjs
description: NextJS 14+ App Router specialist. Server Components, SSR, routing.
---

# Bad: Vague description
---
name: frontend
description: Does frontend stuff
---
```

**Why this matters:**
- Clear descriptions help Claude identify relevance quickly
- Prevents loading irrelevant skills
- Maximizes progressive disclosure benefits

### 2. Agent Coordination (Sub-Agent Parallelization)

SpecWeave's **role-orchestrator** skill automatically:
- Detects multi-domain tasks
- Launches specialized sub-agents (PM, Architect, DevOps, etc.)
- Each sub-agent loads only its relevant skills
- Coordinates results back to main conversation

**Example:**

```
User: "/sw:inc 'Full-stack SaaS with Stripe payments'"
    ↓
role-orchestrator activates
    ↓
Launches sub-agents in parallel:
  ├─ PM agent (requirements)
  ├─ Architect agent (system design)
  ├─ Security agent (threat model)
  └─ DevOps agent (deployment)
    ↓
Each loads only relevant skills in isolated context
    ↓
Results merged into increment spec
```

---

## Common Misconceptions

### ❌ Myth 1: "SpecWeave has custom context manifests"

**Reality:** No. SpecWeave uses Claude's native progressive disclosure. Skills load based on Claude's relevance detection, not custom YAML manifests.

### ❌ Myth 2: "SpecWeave caches loaded context"

**Reality:** No custom caching. Claude Code handles caching internally (if applicable). SpecWeave doesn't implement additional caching layers.

### ❌ Myth 3: "70-90% token reduction"

**Reality:** Token savings vary by task:
- Simple tasks: 90%+ (load 1-2 skills vs all 35)
- Complex tasks: 50-70% (load 5-10 skills + use sub-agents)
- Exact percentages depend on task complexity

### ✅ Truth: "It just works"

**Reality:** Progressive disclosure and sub-agents are **automatic**. You don't configure them. Claude handles skill loading, sub-agent context isolation happens automatically when agents are launched.

---

## Best Practices

### For Skill Descriptions

**Do:**
- Be specific about what the skill does
- Include trigger keywords users might say
- List technologies/frameworks explicitly

**Don't:**
- Write vague descriptions ("helps with coding")
- Omit key activation triggers
- Mix multiple unrelated domains in one skill

### For Sub-Agent Usage

**When to use sub-agents:**
- Multi-domain tasks (frontend + backend + devops)
- Parallel work (multiple features simultaneously)
- Large codebase exploration (different modules)

**When NOT to use sub-agents:**
- Simple single-domain tasks
- Sequential work requiring shared context
- When main conversation context is already low

---

## Debugging Context Usage

### Check Active Skills

When Claude mentions using a skill:

```
User: "Create a Next.js page"
Claude: "🎨 Using nextjs skill..."
```

**This means:**
- Progressive disclosure worked
- Only nextjs skill loaded (not all 35)
- Context efficient

### Check Sub-Agent Usage

When Claude mentions launching agents:

```
Claude: "🤖 Launching 3 specialized agents in parallel..."
```

**This means:**
- Sub-agent parallelization active
- Each agent has isolated context
- Efficient multi-domain processing

---

## Summary

SpecWeave achieves context efficiency through:

1. **Progressive Disclosure (Native Claude)**
   - Skills load only when relevant
   - Metadata-first approach
   - 90%+ savings on simple tasks

2. **Sub-Agent Parallelization (Native Claude Code)**
   - Isolated context windows
   - Parallel processing
   - 50-70% savings on complex tasks

**No custom manifests. No custom caching. Just smart use of Claude's native capabilities.**

---

## References

- [Claude Skills Documentation](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Agent Skills Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Sub-Agents Documentation](https://docs.claude.com/en/docs/claude-code/sub-agents)
