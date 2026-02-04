---
name: start-research
description: "Start a research exploration using the technical-research skill. For early-stage ideas, feasibility checks, and broad exploration before formal discussion."
disable-model-invocation: true
---

Invoke the **technical-research** skill for this conversation.

## Workflow Context

This is **Phase 1** of the six-phase workflow:

| Phase | Focus | You |
|-------|-------|-----|
| **1. Research** | EXPLORE - ideas, feasibility, market, business | ◀ HERE |
| 2. Discussion | WHAT and WHY - decisions, architecture, edge cases | |
| 3. Specification | REFINE - validate into standalone spec | |
| 4. Planning | HOW - phases, tasks, acceptance criteria | |
| 5. Implementation | DOING - tests first, then code | |
| 6. Review | VALIDATING - check work against artifacts | |

**Stay in your lane**: Explore freely. This is the time for broad thinking, feasibility checks, and learning. Don't jump to formal discussions or specifications yet.

---

## Instructions

Follow these steps EXACTLY as written. Do not skip steps or combine them. Present output using the EXACT format shown in examples - do not simplify or alter the formatting.

**CRITICAL**: This guidance is mandatory.

- After each user interaction, STOP and wait for their response before proceeding
- Never assume or anticipate user choices
- Even if the user's initial prompt seems to answer a question, still confirm with them at the appropriate step
- Complete each step fully before moving to the next
- Do not act on gathered information until the skill is loaded - it contains the instructions for how to proceed

---

## Step 0: Run Migrations

**This step is mandatory. You must complete it before proceeding.**

Invoke the `/migrate` skill and assess its output.

**If files were updated**: STOP and wait for the user to review the changes (e.g., via `git diff`) and confirm before proceeding to Step 1. Do not continue automatically.

**If no updates needed**: Proceed to Step 1.

---

## Step 1: Get the Seed Idea

Ask:

```
What's on your mind?

- What idea or topic do you want to explore?
- What prompted this - a problem, opportunity, curiosity?
```

**STOP.** Wait for user response before proceeding.

→ Proceed to **Step 2**.

---

## Step 2: Understand Current Knowledge

Ask:

```
What do you already know?

- Any initial thoughts or research you've done?
- Constraints or context I should be aware of?
```

**STOP.** Wait for user response before proceeding.

→ Proceed to **Step 3**.

---

## Step 3: Determine Starting Point

Ask:

```
Where should we start?

- Technical feasibility? Market landscape? Business model?
- Or just talk it through and see where it goes?
```

**STOP.** Wait for user response before proceeding.

→ Proceed to **Step 4**.

---

## Step 4: Gather Final Context

Ask:

```
Any constraints or context I should know about upfront?

(Or "none" if we're starting fresh)
```

**STOP.** Wait for user response before proceeding.

→ Proceed to **Step 5**.

---

## Step 5: Invoke the Skill

After completing the steps above, this skill's purpose is fulfilled.

Invoke the [technical-research](../technical-research/SKILL.md) skill for your next instructions. Do not act on the gathered information until the skill is loaded - it contains the instructions for how to proceed.

**Example handoff:**
```
Research session for: {topic}
Output: docs/workflow/research/exploration.md

Context:
- Prompted by: {problem, opportunity, or curiosity}
- Already knows: {any initial thoughts or research, or "starting fresh"}
- Starting point: {technical feasibility, market, business model, or "open exploration"}
- Constraints: {any constraints mentioned, or "none"}

Invoke the technical-research skill.
```
