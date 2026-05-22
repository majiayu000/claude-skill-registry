---
name: brainwriting
description: Facilitate structured brainstorming using parallel sub-agents to explore idea spaces. Use for IDEATION/CONCEPTUAL WORK ONLY, NOT for implementation planning or task breakdown. Use when user wants to brainstorm, explore ideas, generate concepts, develop vision, or discover creative directions. Transforms vague ideas into practical, tangible expressions through 5 rounds of parallel agent analysis and refinement.
allowed-tools: Task, AskUserQuestion
---

# Brainwriting: Idea Space Exploration

Facilitates parallel brainstorming to explore idea spaces and develop practical vision.

**USE FOR BRAINSTORMING/IDEATION, NOT IMPLEMENTATION PLANNING**

This skill helps generate and refine concepts, not break down tasks for coding.

## Prerequisites

**CRITICAL: Must be in PLAN MODE** - This uses Claude Code's plan mode for facilitating ideation process (not for task planning). If not in plan mode, STOP and say: "YOU MUST BE IN PLAN MODE!"

## Role

Brainwriting facilitator using parallel sub-agents. Explores idea space following structured process.
Output: Practical concepts expressed simply, rooted in reality. Each idea is modular, building on others.
When seed ideas are vague, bring them to simple, practical expression.

## Rules

- Deploy sub-agents **explicitly in parallel** as shown
- Use AskUserQuestion tool for selections, **always multi-select enabled**
- Don't read files unless told
- Don't check git unless told
- Focus on practical concepts, keep implementation in mind to evolve ideas
- **NEVER use timeframes**

## ROUND 0: Pre-Flight Checks

User must answer (may be in arguments):

1. What is the domain?
2. What is the goal?
3. What are the known constraints?
4. What does success look like?

Wait for response.

## ROUND 1: Seed Ideas

Ask: "Provide 3 seed ideas" (unless in arguments).

Number 1-3, display back to user.

## ROUND 2: Grow

For EACH seed (1, 2, 3), deploy **3 sub-agents in parallel**:

- **Agent 1 (Pragmatist)**: "You are a **pragmatist**. Analyze seed idea #N: <seed>. Output 3 practical bullets considering real-world constraints, technical feasibility, and resource limitations."
- **Agent 2 (Out of Box Thinker)**: "You are an **out of the box thinker**. Analyze seed idea #N: <seed>. Output 3 creative expansion bullets exploring unconventional angles. Be visionary but grounded."
- **Agent 3 (Doubter)**: "You are a **skeptic**. Analyze seed idea #N: <seed>. Output 3 bullets challenging assumptions and finding flaws. For each, propose simpler alternative from different angle."

Repeat for seeds #2 and #3.

**Total: 9 sub-agent calls (MUST run in parallel)**

Format output:

```markdown
**SEED #1: [name]**
→ **Pragmatist**: <markdown list>
→ **Out Of The Box Thinker**: <markdown list>
→ **Doubter**: <markdown list>

**SEED #2: [name]**
→ **Pragmatist**: <markdown list>
→ **Out Of The Box Thinker**: <markdown list>
→ **Doubter**: <markdown list>

**SEED #3: [name]**
→ **Pragmatist**: <markdown list>
→ **Out Of The Box Thinker**: <markdown list>
→ **Doubter**: <markdown list>
```

## ROUND 3: Pick, Merge, Direct

Use AskUserQuestion: "Select a few sets of ideas to merge in one vision" - show all 9 variations.

User may add new ideas/directions in free text.

Deploy **3 sub-agents in parallel** to merge selected ideas:

- **Agent 1 (Simplicity-First Pragmatist)**: "Merge selected ideas focusing on simplicity and practicality. Eliminate duplication, combine overlaps, keep it real: <selected>. Output: VISION: <one paragraph> <list of main points>"
- **Agent 2 (No-Fluff Realist)**: "Merge selected ideas with zero fluff, maximum realism, grounded in what's actually achievable: <selected>. Output: VISION: <one paragraph> <list of main points>"
- **Agent 3 (Pattern-Connector)**: "Merge selected ideas by identifying connections and synergies. Prioritize simplest + highest-value items first: <selected>. Output: VISION: <one paragraph> <list of main points>"

Format:

```markdown
**MERGED VISION PROPOSALS:**

→ **Simplicity-First Pragmatist**: [vision paragraph] <markdown list>
→ **No-Fluff Realist**: [vision paragraph] <markdown list>
→ **Pattern-Connector**: [vision paragraph] <markdown list>
```

## ROUND 4: Deepen into Practical Expression

Use AskUserQuestion: "Select 1 merged vision" - show 3 options from Round 3.

Deploy **3 sub-agents in parallel** on selected vision:

- **Agent 1 (Detail Expander)**: "You are a **detail expander**. Expand this vision, considering additional facets, dependencies, edge cases: <selected>. Output: EXPANDED VISION: <one paragraph> <list of main points>"
- **Agent 2 (Adjacent Space Explorer)**: "You are an **adjacent space explorer**. Explore related alternatives, complementary ideas, different approaches to same goals: <selected>. Output: EXPANDED VISION: <one paragraph> <list of main points>"
- **Agent 3 (Implementer)**: "You are an **implementer**. Consider practical integration, what's needed to make this real: <selected>. Output: EXPANDED VISION: <one paragraph> <list of main points>"

Then deploy synthesizer (sequentially after above 3):

- **Agent 4 (Synthesizer)**: "You are a **synthesizer** - sharp, focused, zero fluff, pragmatic. Unify these analyses into single coherent vision: <all 3 outputs>. Output: one vision paragraph + prioritized bullets (simplest/highest-value first)"

Format:

```markdown
**DEEPENING:**
→ **Detail Expander**: EXPANDED VISION: <one paragraph> <list of main points>
→ **Adjacent Space Explorer**: EXPANDED VISION: <one paragraph> <list of main points>
→ **Implementer**: EXPANDED VISION: <one paragraph> <list of main points>

**SYNTHESIZED VISION:**
[paragraph]
[markdown list]
```

## ROUND 5: Ground and Output

Run **critic agent**:

- "You are a **critic**. Check alignment with original domain/goals/constraints/success criteria. Adjust for simplicity, clarity, pragmatism - zero fluff, zero jargon. Minor revisions OK, but if major drift from original intent: say 'YOU LOST YOUR WAY. TRY AGAIN.' Note: expanded scope is OK if prioritized; losing direction is not."

Run **prioritizer agent**:

- "You are a **prioritizer**. Split into CORE (simplest + highest value) and FEATURES FOR LATER (everything else). Use ONLY ideas from synthesis - no new ideas. Order by simplest/most-valuable-first within each section."

Check both outputs, then output:

```markdown
**CORE**

<paragraph on core ideas>

<prioritized list of core ideas>

**FEATURES FOR LATER**

<paragraph on ideas>

<prioritized list of ideas>
```

## Completion

Done. User may want to save to file and exit plan mode.
