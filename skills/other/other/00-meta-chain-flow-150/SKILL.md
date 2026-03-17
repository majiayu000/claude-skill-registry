---
name: 00-meta-chain-flow-150
description: "[00] META. Orchestrate skills into dynamic chains for complex tasks. Analyzes the task, discovers available skills, builds an optimal chain, explains why each skill is needed, and executes step-by-step with user confirmation. Use for any complex task requiring multiple thinking/research/analysis steps. Triggers on \"plan this\", \"how to approach\", \"what's the strategy\", \"build a plan\", or any multi-step problem requiring skill orchestration."
---

# Meta-Chain-Flow 150 Protocol

**Core Principle:** Orchestrate skills dynamically. Analyze the task, discover available skills, build the right chain, explain the reasoning, execute step-by-step with confirmation.

## What This Skill Does

This is a **meta-skill** — an orchestrator that:
- **Analyzes** the task to understand what's needed
- **Discovers** available skills (finds where they are, what exists)
- **Builds** a chain of appropriate skills in the right order
- **Explains** why each skill is in the chain
- **Executes** step-by-step with user confirmation
- **Adapts** the chain as new information emerges

## The Orchestration Model

```
🔗 CHAIN-FLOW 150 (Orchestrator)
        ↓
[1. Analyze Task] → What type of problem is this?
        ↓
[2. Discover Skills] → What skills are available? Where?
        ↓
[3. Build Chain] → Which skills? In what order?
        ↓
[4. Explain Why] → Justify each skill in the chain
        ↓
[5. Execute] → Step by step with confirmation
        ↓
[6. Adapt] → Modify chain if situation changes
```

## Skill Discovery

Chain-Flow finds available skills by:

### Where to Look for Skills
```
📁 SKILL LOCATIONS (search in order)
├── ./.codex/skills/          # Project skills folder (canonical)
├── ./skills/                 # Legacy project skills (if present)
├── ./.claude/skills/         # Legacy project Claude skills (if present)
├── ~/.claude/skills/         # Personal skills (home directory, if present)
├── Plugin skills             # From installed plugins
└── Built-in capabilities     # Agent's native abilities
```

### How to Discover Skills
```bash
# Find all skill directories
ls -la ./.codex/skills/ 2>/dev/null
ls -la ./skills/ 2>/dev/null
ls -la ./.claude/skills/ 2>/dev/null
ls -la ~/.claude/skills/ 2>/dev/null

# Read each SKILL.md to understand capabilities
cat ./.codex/skills/*/SKILL.md | head -20  # Read descriptions
```

### Discovery Process
1. **Scan directories** — Find all folders with SKILL.md
2. **Read name + description** — Understand what each skill does
3. **Map triggers** — Know when each skill applies
4. **Build skill inventory** — Create list of available skills
5. **Match to task** — Select relevant skills for current task

## The 150% Orchestration Rule

- **100% Core:** Build appropriate skill chain + execute with confirmation
- **50% Enhancement:** Explain reasoning + adapt chain dynamically

## When to Use This Skill

**Universal trigger:** Any complex task that needs multiple skills combined.

**Specific triggers:**
- Complex multi-step problems
- Tasks requiring research + thinking + execution
- When you're not sure which approach to take
- Strategic planning for projects
- Any request where single skill isn't enough

**Key insight:** Most real problems need chains of skills, not single skills.

## Chain Building Process

### Step 1: ANALYZE THE TASK
Understand what the task requires:
- What's the nature of the problem?
- What types of thinking/research/execution needed?
- What's the complexity level?
- What are the unknowns?

### Step 2: DISCOVER AVAILABLE SKILLS
Find what skills are available:
```
🔍 Skill Discovery:
- Scanning ./.codex/skills/ ...
- Scanning ./skills/ ...
- Scanning ./.claude/skills/ ...
- Scanning ~/.claude/skills/ ...

Found Skills:
├── goal-clarity-150    — Clarify objectives and success criteria
├── research-deep-150   — Deep research from internal + external sources
├── impact-map-150      — Map what changes affect
├── action-plan-150     — Create actionable plans with steps/risks
├── deep-think-150      — Quality reasoning and analysis
├── max-quality-150     — High quality execution
├── 74-mid-session-save-150    — Mid-session checkpoint for continuity
├── gated-exec-150      — Execute with confirmation gates
├── proof-grade-150     — Verify facts with confidence levels
├── integrity-check-150 — Final quality self-check
├── task-track-150      — Manage task lifecycle and status
├── tidy-up-150         — Quick cleanup after milestones
├── ask-ai-150          — Consult external AI models
└── skill-forge-150     — Create new skills when needed

Reading descriptions to match task requirements...
```

### Step 3: BUILD THE CHAIN
Construct the skill sequence:
- Which skills are relevant?
- What's the logical order?
- Are there dependencies between skills?

### Step 4: EXPLAIN THE CHAIN
Justify each skill:
```
📋 Proposed Chain:

1. goal-clarity-150
   WHY: Task requirements are ambiguous, need to clarify first

2. research-deep-150  
   WHY: Need to understand current system + best practices

3. impact-map-150
   WHY: Changes will affect multiple components

4. deep-think-150
   WHY: Architecture decision with trade-offs

5. max-quality-150
   WHY: Critical feature, needs high quality execution
```

### Step 5: EXECUTE WITH CONFIRMATION
Go step by step:
```
🔗 Chain Execution:

Step 1/5: goal-clarity-150
[Execute skill...]
✅ Complete. Proceed to Step 2? (Yes/No/Modify chain)
```

### Step 6: ADAPT IF NEEDED
Modify chain based on new information:
```
🔄 Chain Adaptation:

New information discovered: Security implications found
→ Adding: security-check skill after impact-map
→ Updated chain: 1→2→3→3.5(new)→4→5

Continue with updated chain? (Yes/No)
```

## Output Format

When using Chain-Flow 150:

```
🔗 **Chain-Flow 150 Activated**

**Task Analysis:**
[Understanding of what's needed]

**Skills Discovered:**
- [List of available skills with brief descriptions]

**Proposed Chain:**
```
1. [skill-name] → WHY: [justification]
2. [skill-name] → WHY: [justification]  
3. [skill-name] → WHY: [justification]
...
```

**Execution Plan:**
- Estimated steps: [N]
- Confirmation: After each skill
- Adaptation: Will modify if needed

**Ready to begin chain execution?**
```

## Chain Execution Format

During execution:

```
🔗 **Chain-Flow: Step [X/N]**

**Current Skill:** [skill-name]
**Purpose:** [why this skill now]

[Skill execution output...]

**Step Complete:** ✅

**Next:** [next-skill-name]
**Continue?** (Yes / No / Modify Chain / Skip to Step N)
```

## Common Chain Patterns

### Pattern: New Feature Development
```
goal-clarity-150 → research-deep-150 → impact-map-150 → 
action-plan-150 → max-quality-150
```

### Pattern: Complex Project
```
goal-clarity-150 → research-deep-150 → impact-map-150 → 
deep-think-150 → action-plan-150 → max-quality-150
```

### Pattern: Bug Investigation
```
research-deep-150 (logs, git) → impact-map-150 → 
deep-think-150 → action-plan-150 (fix steps) → max-quality-150
```

### Pattern: Architecture Decision
```
goal-clarity-150 → research-deep-150 (options) → 
deep-think-150 (trade-offs) → impact-map-150 → action-plan-150
```

### Pattern: Code Review
```
research-deep-150 (understand) → impact-map-150 → 
deep-think-150 (issues) → max-quality-150 (feedback)
```

### Pattern: Migration/Refactoring
```
goal-clarity-150 → impact-map-150 → research-deep-150 → 
action-plan-150 (detailed steps) → max-quality-150
```

## Operational Rules

1. **DISCOVER FIRST:** Always find what skills are available
2. **JUSTIFY EACH:** Explain why each skill is in the chain
3. **CONFIRM STEPS:** Get user confirmation between skills
4. **ADAPT FREELY:** Modify chain when new information emerges
5. **SKIP ALLOWED:** User can skip skills if not needed
6. **CHAIN IS FLEXIBLE:** Not rigid — adjust to reality

## Failure Modes & Recovery

| Failure | Detection | Recovery |
|---------|-----------|----------|
| **Wrong chain** | Results don't help | Re-analyze, rebuild chain |
| **Missing skill** | Gap in chain | Add skill or use alternative |
| **Wrong order** | Dependencies broken | Reorder chain |
| **Over-engineering** | Too many skills | Simplify chain |
| **Under-engineering** | Skipped needed skill | Add missing skill |

## Examples

### ❌ Without Chain-Flow
```
User: "Add payment processing to the app"
AI: [Jumps straight to coding]
Result: Missed security requirements, broke existing checkout, 
no understanding of payment gateway options
```

### ✅ With Chain-Flow 150
```
User: "Add payment processing to the app"

🔗 Chain-Flow 150 Activated

Task Analysis:
Complex integration task with security, external APIs, 
and business logic implications.

Skills Discovered:
- goal-clarity-150, research-deep-150, impact-map-150
- action-plan-150, deep-think-150, max-quality-150

Proposed Chain:

1. goal-clarity-150
   WHY: Payment requirements vary (subscriptions? one-time? refunds?)
   
2. research-deep-150
   WHY: Need to evaluate Stripe vs PayPal vs others + security standards
   
3. impact-map-150
   WHY: Touches checkout, user accounts, database, notifications
   
4. deep-think-150
   WHY: Architecture decision for payment service integration

5. action-plan-150
   WHY: Create detailed implementation plan with rollback points
   
6. max-quality-150
   WHY: Payment code must be high quality (money involved)

Ready to begin? Starting with goal-clarity-150...

---

🔗 Chain-Flow: Step 1/5

Current Skill: goal-clarity-150
Purpose: Clarify payment requirements before research

[Executing goal-clarity-150...]

Questions:
- One-time payments, subscriptions, or both?
- Which currencies?
- Refund policy needed?
- PCI compliance level required?

[User answers...]

Step Complete: ✅
Requirements documented.

Next: research-deep-150
Continue? (Yes/No/Modify)
```

## Relationship to Other Skills

Chain-Flow is the **orchestrator** — it doesn't replace other skills, it **combines** them:

```
                    🔗 CHAIN-FLOW-150
                    (Orchestrator)
                         ↓
    ┌────────────────────┼────────────────────┐
    ↓                    ↓                    ↓
goal-clarity    research-deep         impact-map
    ↓                    ↓                    ↓
deep-think         max-quality          [others]
```

---

**Remember:** Complex problems need chains of skills, not single skills. Chain-Flow builds the right chain, explains why, and executes step-by-step with your confirmation. You stay in control while getting the benefit of orchestrated skill application.
