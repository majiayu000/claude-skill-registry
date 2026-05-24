---
name: think-brainstorm
description: Good-faith divergent brainstorming for achieving a goal. Validates assumptions, then spawns brainstormers running different techniques (first-principles, working-backwards, lateral, analogical, constraints-shift, etc.) in isolation, and synthesizes the pool into a report of standouts, reasonable ideas, and hybrid combinations. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Brainstorm - Divergent Idea Generation

Generates candidate approaches for achieving a goal. Uses parallel brainstormers each applying a different technique in isolation (to avoid anchoring), then synthesizes the pool into a catalog of ideas. The skill is purely *generative* — evaluation, choice, and critique belong to `/think-deliberate` and `/think-scrutinize`.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured catalog of ideas the user can pick from.

## Roles

**Judge (you, running this skill):**
- Capture the goal in a written brief
- Validate the assumptions embedded in the goal
- Choose appropriate brainstorming techniques
- Spawn brainstormers and synthesize the exchange into a report

**Brainstormers:** Each receives a specific technique (first-principles, working-backwards, lateral, analogical, constraints-shift, worst-possible-idea, six-hats-green, SCAMPER) and generates ideas within that mode, in isolation from other brainstormers.

## Workflow

### 1. Receive the Goal

The goal may arrive as:
- **Conversation context** — summarize it back, confirm
- **A document** — read the file (problem statement, project brief, design goal)
- **Fresh user input** — capture it verbatim

**Produce a written brief** of the goal as you understand it. Brainstormers operate on this brief. Ambiguity here corrupts everything downstream.

### 2. Validate Assumptions

**This is a dedicated phase, not opportunistic.** Before any generation, extract the assumptions the goal depends on — both stated and unstated — and validate them with the user.

**Look for:**
- **Problem-framing assumptions**: does the user assume X is the real problem? (Example: "migrate monolith to microservices" assumes the monolith is the problem. Maybe one hot table is the actual pain.)
- **Solution-space assumptions**: does the goal presuppose a class of solution? (Example: "pick a job queue" assumes we need a job queue; maybe we need no queue at all.)
- **Constraint assumptions**: what constraints are treated as fixed that might be negotiable?
- **Success-criteria assumptions**: how will we know we succeeded? Is that actually what the user wants?

**Present findings to the user.** For each assumption, ask: is this correct, negotiable, or wrong? Update the goal brief based on responses.

**Sometimes this phase alone dissolves or reframes the problem.** That's a valuable outcome — better to stop here than brainstorm solutions to the wrong problem. If the user wants to proceed anyway, proceed with the refined brief.

### 3. Choose Techniques

Select 3-6 techniques from the palette based on the goal's shape. The orchestrator decides autonomously — the user does not pick techniques.

**Available techniques:**
- **first-principles** — strip to irreducible requirements, reason up
- **working-backwards** — imagine success, trace paths back
- **lateral** — random entry + provocation; deliberately break conventional thought
- **analogical** — structural analogies from unrelated domains (biomimicry, cross-industry, mathematical)
- **constraints-shift** — force the goal through artificial constraints (10x budget, ship tomorrow, forbid the obvious tool)
- **worst-possible-idea** — generate bad ideas, invert them
- **six-hats-green** — de Bono's creative hat; pure generative mode
- **SCAMPER** — *only when refining an existing solution*; applies each verb (substitute, combine, adapt, etc.)

**Selection heuristics:**
- Greenfield goal? Skip SCAMPER.
- Goal with a natural-world analog? Include analogical.
- Goal constrained by conventional thinking? Include lateral.
- Goal with clear end-state? Include working-backwards.
- Goal with questionable fundamentals? Include first-principles.
- No obvious analog, established domain? Skip analogical.

**Irrelevant techniques are dropped**, not forced. Better 3 fitted techniques than 7 forced ones.

### 4. Spawn Brainstormers (Parallel, Isolated)

Spawn one `THK - Brainstormer` agent per chosen technique, in parallel. Each receives:
- The written goal brief (from step 1, refined in step 2)
- Its assigned technique
- Validated assumptions and relevant context
- Instruction to generate 5-10 ideas with rationale

**No cross-talk between brainstormers.** This is the Nominal Group Technique principle — independent generation first, pooling second. Isolated brainstormers produce more diverse output than coordinated ones (research-backed: open brainstorming anchors on early ideas).

Collect all idea sets.

### 5. Synthesize

Combine the isolated idea sets into a coherent catalog:

**5a. Deduplicate** — when multiple techniques produced structurally the same idea, merge them (preserve technique attribution from all contributors — that's signal: multiple angles landed here).

**5b. Cluster** — group related ideas by theme or approach. The clusters are often more interesting than individual ideas.

**5c. Construct hybrids** — look for cross-technique combinations where two ideas together are stronger than either alone. Example: a first-principles rethink combined with an analogical example that shows how it's been done elsewhere. Flag hybrids as constructed (the orchestrator's contribution, not any single agent's).

**5d. Surface standouts** — identify the 3-7 most interesting ideas across axes:
- **Novel** — unexpected, breaks conventional framing
- **Promising** — plausible high impact on the goal
- **Counterintuitive** — worth a second look even if it sounds wrong

**5e. Drop weak ideas** — ideas that fall apart under basic scrutiny don't belong in the catalog. Don't evaluate rigorously (that's `/think-scrutinize`), but don't pad either.

**5f. Note raised questions** — the brainstorming exercise often surfaces questions the user hadn't considered. These are frequently the real insight.

### 6. Report

**Final report format:**

```
## Brainstorm Report

**Goal:** [one-line clarified goal]
**Techniques applied:** [list]

### Validated Assumptions

- [Assumption] — [user's response: confirmed / revised / discarded]

### Standouts

[3-7 most promising/novel/counterintuitive ideas — no technique attribution.
 Each stands on its merit.]

1. **[Name]** — [description]
   Why it's a standout: [novel / promising / counterintuitive and why]

### Hybrid Ideas

[Cross-technique combinations the orchestrator constructed. Flag as
 synthesized, not generated. Each names the parent techniques.]

- **[Hybrid name]** — [description]
  Combines: [technique A's idea] + [technique B's idea]
  Why the combination matters: [brief rationale]

### Other Reasonable Ideas

[Remaining ideas worth keeping, clustered by theme. Technique attribution
 included in the catalog for transparency.]

**Cluster: [theme]**
- [idea] *(first-principles)*
- [idea] *(lateral)*
...

**Cluster: [theme]**
- ...

### Questions the Exercise Raised

[Often the real insight — questions about the goal, the constraints, the
 problem framing that emerged through generation.]

### Suggested Next Steps

- To choose among standouts: `/think-deliberate`
- To stress-test a promising idea: `/think-scrutinize`
- To refine the goal and re-brainstorm: re-invoke `/think-brainstorm`
```

### 7. No Iteration

This skill is one-shot. If the user wants to go deeper on a specific direction, they refine the goal and **re-invoke**. If they want to choose between standouts, they hand off to `/think-deliberate`. If they want to stress-test one, `/think-scrutinize`. Each invocation is a clean consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Isolated generation.** Brainstormers do not see each other's output.
- **Technique fit > technique count.** Drop techniques that don't fit the goal.
- **Generation, not evaluation.** Surface standouts by axis, don't rank or pick.
- **Honest "technique produced little"** is a valid brainstormer outcome.

## When to Use

**Good fit:**
- Early-stage exploration — you know the goal, not the approach
- Escaping conventional thinking on a stuck problem
- Wanting a diverse set of candidate approaches before choosing one
- Pre-mortem alternative: "what could we even do here?"

**Poor fit:**
- Choosing between known options → use `/think-deliberate`
- Stress-testing an existing plan → use `/think-scrutinize`
- Implementing an idea → this skill makes nothing; follow up with `/scope` or `/implement`
- Goals so vague no meaningful assumptions can be extracted (refine the goal first)

## Philosophy

Brainstorming is valuable when generation is constrained by convention, anchoring, or exhaustion. The skill formalizes techniques that deliberately break those constraints — and runs them in parallel, isolated, so each produces its own distinct contribution.

The rule is divergence. Evaluation, ranking, and selection happen elsewhere. Here, the goal is to surface possibilities the user hadn't considered — including ones they might initially dismiss.

Osborn's four rules still apply under the hood: defer judgment, quantity over quality, welcome wild ideas, build on others' ideas (the synthesis phase does this for us). But modern research favors Nominal Group Technique over classical group brainstorming — independent generation, then pooling. This skill is NGT with AI.
