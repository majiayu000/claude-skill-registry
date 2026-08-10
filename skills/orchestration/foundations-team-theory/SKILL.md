---
name: foundations-team-theory
description: Team-theory primitives for cooperative multi-agent decisions, subagent allocation, communication value, Dec-POMDPs, and decentralized control. Use when organizing agents.
compatibility: Portable core only.
version: "1.1"
last_validated: 2026-07-11
---

# Team Theory Foundations


10 canonical team-theory primitives for *cooperative* multi-agent decision problems — agents share a payoff but each sees a different slice of the world. Game theory handles strategic conflict; decision theory handles solo choice under uncertainty; team theory handles the regime in between, which is exactly where subagents and orchestrated AI agents operate.

The field was founded by Jacob Marschak (1955) and formalized by Roy Radner (1962). It is the formal basis for: when to centralize a decision, what each agent must observe, when communication pays for itself, and why decentralized teams can be optimal even with free communication channels. Modern multi-agent reinforcement learning (Dec-POMDPs, MARL) is its computational descendant.

## When to Apply

**Apply team-theory when:**
- Multiple agents with **shared payoff** but **partitioned observations** (the canonical subagent setting)
- Designing what each subagent sees vs. what is centralized
- Choosing between centralized orchestrator, decentralized swarm, and hierarchical structures
- Costing communication: is it worth the latency / token / coordination overhead?
- Building agent teams where role specialization matters (each agent owns a different observation lane)
- Multi-agent RL or Dec-POMDP problem framing

**Skip and use simpler alternatives when:**
- Agents have **divergent incentives** → use [foundations-game-theory](../foundations-game-theory/SKILL.md) (mechanism design, auctions, debates)
- Single agent / single-shot decision under uncertainty → use [foundations-decision-theory](../foundations-decision-theory/SKILL.md)
- Communication itself is the bottleneck on a known structure → use [foundations-information-theory](../foundations-information-theory/SKILL.md) (channel capacity)
- The problem is recursive control of a viable system, not a one-shot team decision → use [foundations-cybernetics-vsm](../foundations-cybernetics-vsm/SKILL.md)
- All agents see the same information — there is no team problem; centralize trivially

## Contents

- [Quick Reference](#quick-reference)
- [Primitive Index](#primitive-index)
- [Formal Supporting Theory](#formal-supporting-theory)
- [Anti-Patterns](#anti-patterns)
- [Decision Checklist](#decision-checklist)
- [Composition Recipes](#composition-recipes)
- [Workflow](#workflow)
- [ASCII Flow](#ascii-flow)
- [Navigation](#navigation)
- [Related Skills](#related-skills)
- [Fact-Checking](#fact-checking)

---

## Quick Reference

| # | Primitive | When to Reach For It |
|---|-----------|----------------------|
| 1 | [Team Decision Problem](#1-team-decision-problem) | Frame any shared-goal multi-agent setup before designing it |
| 2 | [Information Structure](#2-information-structure) | Decide what each agent observes; classify centralized / decentralized / partial / nested |
| 3 | [Person-by-Person Optimality](#3-person-by-person-optimality) | Local optimality check — necessary but not sufficient for team optimum |
| 4 | [Value of Communication](#4-value-of-communication) | "Should agents share state?" — quantify expected payoff lift vs. cost |
| 5 | [Radner's LQG Theorem](#5-radners-lqg-theorem) | Linear-quadratic-Gaussian teams admit a closed-form linear optimal rule |
| 6 | [Witsenhausen Counterexample](#6-witsenhausen-counterexample) | Why naive linearity fails when one agent's action signals to another |
| 7 | [Information Cost](#7-information-cost) | Bound observation/communication budgets; rationalize bounded rationality |
| 8 | [Organizational Forms](#8-organizational-forms) | Pick centralized vs. decentralized vs. hierarchical structure; see #8a (centralize/decentralize decision test) and #8b (team-size/coordination-cost curve) in `references/primitives-overview.md` |
| 9 | [Dec-POMDP / MARL Extension](#9-dec-pomdp--marl-extension) | Sequential team problems with state dynamics — modern computational form |
| 10 | [Common-Task Condition](#10-common-task-condition) | Boundary condition: when does shared payoff actually hold? |

Full definitions, inputs, outputs, failure modes, and worked examples: [`references/primitives-overview.md`](references/primitives-overview.md).

---

## Primitive Index

| # | Primitive | Failure Mode It Addresses |
|---|-----------|--------------------------|
| 1 | Team Decision Problem | Modeling cooperative agents as either a single decision-maker (loses decentralization value) or as strategic players (overstates conflict) |
| 2 | Information Structure | Agents observing redundant signals; missing observations; uncosted communication assumed free |
| 3 | Person-by-Person Optimality | Local-optimum trap: each agent optimal given others' fixed rules, but the joint policy is suboptimal |
| 4 | Value of Communication | "Add a Slack channel between agents" with no expected-payoff justification; channel may cost more than it earns; inter-agent message routing also degrades information efficiency via Data Processing Inequality even at zero explicit channel cost |
| 5 | Radner's LQG Theorem | Reinventing optimization for LQG teams when a closed-form linear rule exists |
| 6 | Witsenhausen Counterexample | Assuming linear policies are optimal when an agent's action carries signaling content |
| 7 | Information Cost | Designing perfect-observation agents in a world where observation has latency, token, and money cost |
| 8 | Organizational Forms | Defaulting to a central orchestrator when a decentralized or hierarchical form would dominate |
| 9 | Dec-POMDP / MARL Extension | Treating each timestep as a fresh team problem; ignoring history and state |
| 10 | Common-Task Condition | Calling a system a "team" when payoffs actually diverge — game theory regime, not team regime |

---

## Formal Supporting Theory

| Theory Area | Use When | Applied Primitives It Grounds |
|---|---|---|
| Marschak–Radner team theory | Need normative framing of cooperative multi-agent decisions | #1, #2, #3, #4, #5, #8 |
| Decentralized stochastic control | Action of one agent affects information of another | #6, #9 |
| Information economics | Need to cost observation and communication | #4, #7 |
| Organization economics | Compare centralized hierarchy, decentralized markets, polyarchy | #8 |
| Dec-POMDP and MARL | Sequential team problems with state dynamics | #9 |
| Mechanism design boundary | Where shared payoff breaks down | #10 (then exit to game-theory) |

See [`references/primitives-overview.md`](references/primitives-overview.md) for the formal-theory map and theorem statements.

---

## Anti-Patterns

| Anti-Pattern | Team Theory Diagnosis | Fix |
|---|---|---|
| One central orchestrator reads everything, decides everything | Centralized information structure used where decentralized partition is cheaper and equally optimal under Radner conditions | Apply #2 + #5: if the team is LQG-like and observations are local, a decentralized linear rule matches centralized payoff at lower cost |
| Each subagent given full system context "just in case" | Information cost (#7) ignored; redundant observations dominate token budget | Partition observations to what each agent's action depends on; redundancy must justify itself |
| Local optimization per subagent declared "team-optimal" | Person-by-person optimality (#3) confused with team optimum; PBPO is necessary, not sufficient | Verify joint optimum by varying any two policies simultaneously, not one at a time |
| "Add a comms channel between agents" added without payoff analysis | Value of communication (#4) not computed; channel may cost more than it earns | Compute expected payoff with vs. without the channel; if delta < cost, drop it |
| "Multi-agent by default for complex tasks" | Coordination overhead costs are O(N²) in token accumulation; DPI shows message routing loses conditioning information available in unified context | Default to single-agent for sequential reasoning tasks; require empirical evidence that parallelization actually helps before adding agents (Tran & Kiela 2026) |
| "Assume natural-language inter-agent messages are lossless" | Natural-language agent-to-agent messages are lossy compressions; semantic drift accumulates across rounds even with no explicit error (Rath 2026); embedding-space exchange is lossless at lower token cost (LatentMAS, ICML 2026 Spotlight) | For high-precision cooperative tasks, route inter-agent signals through shared latent representations rather than text (primitive #2 information structure design) |
| "Default to all-to-all communication between agents" | Dense topologies amplify error propagation in LLM multi-agent systems (Shen et al. 2025); moderately sparse topologies outperform both fully dense and fully sparse | Design inter-agent communication graphs at moderate sparsity; use adaptive topology if task structure changes dynamically (CARD, ICLR 2026) |
| Assume linear/affine policies optimal in non-LQG team | Witsenhausen (#6) shows nonlinear policies can dominate when signaling exists | Check if any agent's action affects another agent's observation; if yes, allow nonlinear policies |
| Treat all multi-agent setups as game-theoretic | Common-task condition (#10) holds — agents share a goal — so mechanism-design overhead is wasted | Skip incentive compatibility; design for joint optimization directly |
| Treat all multi-agent setups as team problems | Common-task condition (#10) fails — agents have divergent goals — team theory underestimates conflict | Switch to game theory (auctions, mechanism design) |
| "Psychological safety assumed universally positive" (human teams) | Curvilinear boundary condition (Edmondson & Bransby 2023, Annual Review of OB, citing Eldor, Hodor & Cappelli 2023): high psychological safety can harm routine in-role performance by redirecting attention to exploration; benefit is robust for learning/adaptive tasks only; accountability structures moderate the downside. Also commonly conflated with comfort/niceness — see patterns-scenarios-traps.md for misreads | Apply psychological safety practices to adaptive/learning contexts; pair with accountability norms for routine-execution tasks; do not assume monotonic benefit; don't mistake candor-friendly for conflict-free |
| Hierarchical orchestrator-worker with no information flow back up | Polyarchy/hierarchy structure (#8) chosen by default; loses bottom-up signal that decentralized form preserves | Add upward observation channel or switch to decentralized form; for tasks with parallelizable subtasks at scale (>4 agents), consider emergent self-organization protocols where agents self-assign roles — this form dominates fixed hierarchy at scale (Dochkina 2026) |
| "Just add more agents/people, coordination scales for free" | Team-size/coordination-cost curve (#8b): pairwise coordination channels grow ~n(n-1)/2 with team size under high coupling; the marginal member's coordination cost can exceed their contribution (Brooks's Law) | Before adding a member/agent, count how many existing members it must (not could) coordinate with; if most, cut coupling first (modularize, assign a single owner for shared state) rather than adding capacity |
| "We are a centralized [org/agent system]" or "we are a decentralized one" applied blanket-wide | Centralize-vs-decentralize is a per-decision judgment (#8a: information compressibility, reversibility, coupling, blast radius of a wrong local call), not a company-wide or system-wide constant | Apply the four-question test per decision class; expect most real orgs and agent systems to be centralized on some decisions (shared state, brand, safety) and decentralized on others (local execution) |

---

## Decision Checklist

- [ ] **Shared payoff?** If no, exit to [foundations-game-theory](../foundations-game-theory/SKILL.md). If yes, continue (#10)
- [ ] **What does each agent observe?** Map the information structure explicitly (#2)
- [ ] **Are observations redundant?** Trim — observation has cost (#7)
- [ ] **Is communication channel justified?** Compute expected payoff lift; reject if < cost (#4)
- [ ] **For multi-agent topologies with N>2 agents: is the topology moderately sparse?** Dense (all-to-all) connections amplify error propagation in LLM systems and degrade beyond a threshold (#2, #4)
- [ ] **Is the team LQG-like (linear dynamics, quadratic payoff, Gaussian noise)?** If yes, closed-form linear rule available (#5)
- [ ] **Does any agent's action affect another agent's observation?** If yes, signaling exists — allow nonlinear policies (#6)
- [ ] **Sequential decisions over time with state?** Frame as Dec-POMDP (#9)
- [ ] **Picked an organizational form?** Centralized / decentralized / hierarchical — justify choice against the alternatives (#8)
- [ ] **Verified team-optimum, not just person-by-person optimum?** Vary joint policies, not single-agent policies (#3)
- [ ] **Virtual/distributed team?** Match communication medium to task type — divergent/generative tasks are virtuality-tolerant; convergent/evaluative tasks require video-first (Sinnemann & Weiss 2025 meta-analysis, N=7,004 teams, no significant main effect; moderation by task type and medium is significant)

---

## Composition Recipes

### Designing a subagent team for a research task

_Context_: Orchestrator needs to dispatch N subagents on a multi-source research task with a shared answer goal.

1. Verify common-task condition (#10): all subagents and orchestrator share the payoff "produce one accurate answer." If not, exit to game-theory.
2. Map information structure (#2): which sources/files/tools does each subagent observe? Avoid redundant assignment. For human-in-the-loop teams: the temporal ordering of observation matters — simultaneous presentation of human and AI outputs outperforms sequential (human-first then AI) on average (npj Artificial Intelligence 2025, N=52 clinical studies). Design observation lanes with this moderator in mind. **CTP conditions (Hemmer et al. 2024, EJIS 2025)**: human-AI complementarity — performance exceeding either agent or human alone — requires either (a) information asymmetry (human has local context AI lacks) or (b) capability asymmetry (human provides judgment on novel cases AI cannot handle). If neither condition holds, removing the human from the loop and relying on AI alone typically dominates. Verify both conditions before designing a human-in-the-loop step.
3. Cost observations (#7): each tool call has token + latency cost. Allocate observations so that marginal payoff per token decreases monotonically.
4. Compute value of communication (#4): does mid-task chatter between subagents lift expected payoff more than its cost? Default: no — most subagent teams are decentralized with synthesis at the end.
5. Pick organizational form (#8): single orchestrator + parallel decentralized workers (the "split-and-merge" pattern) is the LQG-analog default. Hierarchical only if subgoals are themselves teams.
6. Verify team-optimum (#3): inspect whether changing two subagent prompts simultaneously could improve joint payoff. If yes, the design is person-by-person optimal but not team-optimal.

### Choosing between orchestrator-led and swarm forms

_Context_: A product team must pick between a single planner agent that delegates everything (centralized) and a peer-to-peer agent network (decentralized).

1. Check #5 conditions: linear dynamics, quadratic-like payoff, Gaussian-like noise. Few real agent systems meet this — but it gives the upper bound.
2. Cost the communication channel: orchestrator-led requires every observation to flow up and every decision to flow down. Decentralized requires only local observation but needs convergence on the synthesis.
3. Apply #8: under high information cost and low signaling content, decentralized dominates. Under low info cost and high coupling between agents' actions, centralized dominates. For tasks with 4+ agents and parallelizable subtasks, add a fourth option: emergent self-organization with minimal structure (sequential protocol + autonomous role assignment). At 256 agents this scales sub-linearly; fixed hierarchies do not. Justified by Dochkina (2026, arXiv:2603.28990) and CARD (Wu et al., ICLR 2026).
4. Worked example: code review across 5 files. Files are independent (no signaling, low coupling). Decentralized form (5 parallel reviewers + final aggregator) dominates orchestrator-led. Code review across one tightly-coupled module: signaling is high (one agent's finding changes another's interpretation); centralized or hierarchical wins.

### Sizing the orchestrator's context budget

_Context_: How much should the orchestrator observe vs. push down to subagents?

1. Apply #7: every token in the orchestrator's context has cost. The orchestrator should hold only what is needed to decide *who decides what*, not the underlying domain content.
2. Apply #2: orchestrator's information structure should be the meta-state (task graph, subagent roster, success signals), not the object-level state.
3. Anti-pattern: orchestrator reads all source files and then asks subagents to summarize them — observation paid for twice. Fix: orchestrator observes file *list*; subagents observe file *contents*.

### Designing subagent context as an information-structure problem (AI app builders)

_Context_: You are building a multi-agent AI application and must decide what context (system prompt, retrieved docs, tool permissions, conversation history) each subagent receives.

1. **Name the information structure first (#2).** For each subagent, write a one-row entry: `agent | observation sources | action produced`. This is the `η` partition — make it explicit before writing any code.
2. **Apply the task-type rule.** Parallelizable subtasks with no shared state (e.g., reviewing independent files, generating independent sections) → decentralized partition, zero cross-agent context. Sequential or tightly-coupled subtasks → centralized or hierarchical; pass only the predecessor's *decision output*, not its full reasoning trace.
3. **Strip context to decision-relevant signals (#7).** Each token in a subagent's context window is an observation cost. Give the subagent only what changes its action. If a document section never alters the subagent's output, remove it from its context.
4. **Check for signaling (#6).** If subagent A's output becomes part of subagent B's context (e.g., B reads A's draft), you are in non-classical territory. Do not assume A's optimal policy is the same as if it were working in isolation — A should write with B's downstream use in mind (nonlinear policy).
5. **Compute value of communication before adding agent-to-agent messaging (#4).** Does mid-task chatter between subagents increase the joint answer quality by more than the latency + token cost? Default answer is no for most parallelizable tasks; require evidence before adding it.
6. **For >4 subagents on parallelizable work, prefer decentralized + late synthesis over a central orchestrator reading everything** — observation cost is O(N) in the centralized form vs. O(1) per agent in the decentralized form (#8, Dochkina 2026).

---

## Workflow

1. Confirm common-task condition (#10). If payoffs diverge, exit to game-theory.
2. Map the information structure (#2): one agent per row, one observation source per column, fill the matrix.
3. Cost the observations (#7) and the communication channels (#4).
4. Pick organizational form (#8) — centralized, decentralized, hierarchical — justified against alternatives.
5. Check LQG conditions (#5); if met, use the closed-form rule. If not, watch for signaling (#6) and allow nonlinear policies.
6. Verify joint optimum (#3), not just per-agent optimum.
7. For sequential problems with state, frame as Dec-POMDP (#9) and pick an MARL solver.

---

## ASCII Flow

```text
Cooperative multi-agent decision
  -> Confirm shared payoff and common-task condition
     +-- payoff diverges -> exit to game theory
     +-- shared payoff holds -> map information structure
  -> Cost observation and communication channels
  -> Choose centralized, decentralized, or hierarchical form
  -> Check joint optimum and sequential-state needs
  -> Return team design, information lanes, communication rule, and solver path
```

---

## Navigation

- Domain-agnostic primitives overview: [`references/primitives-overview.md`](references/primitives-overview.md)
- Formal theory map and production boundaries: [`references/formal-theory-map.md`](references/formal-theory-map.md)
- Patterns, scenarios, and traps for multi-agent / subagent design: [`references/patterns-scenarios-traps.md`](references/patterns-scenarios-traps.md)
- Sources: [`data/sources.json`](data/sources.json)

---

## Related Skills

- [foundations-game-theory](../foundations-game-theory/SKILL.md) — exit here when payoffs diverge
- [foundations-decision-theory](../foundations-decision-theory/SKILL.md) — single-agent uncertain choice
- [foundations-information-theory](../foundations-information-theory/SKILL.md) — pricing the channel
- [foundations-cybernetics-vsm](../foundations-cybernetics-vsm/SKILL.md) — recursive viable-system control
- [foundations-grounding-communication](../foundations-grounding-communication/SKILL.md) — *how* agents share state once you decide they should (see also: temporal information structure in human-AI teams — primitive #2, npj AI 2025)
- `agents-subagents` — applied subagent patterns
- [agents-swarm-orchestration](../agents-swarm-orchestration/SKILL.md) — applied multi-agent orchestration

---

## Fact-Checking

- Marschak (1955) "Elements for a Theory of Teams." *Management Science* 1(2). Founded the field.
- Marschak and Radner (1972) *Economic Theory of Teams*. Yale. Canonical text.
- Radner (1962) "Team Decision Problems." *Annals of Mathematical Statistics* 33(3). LQG theorem.
- Witsenhausen (1968) "A Counterexample in Stochastic Optimum Control." *SIAM J. Control* 6(1). Nonlinear-dominance result.
- Bernstein, Givan, Immerman, Zilberstein (2002) "The Complexity of Decentralized Control of Markov Decision Processes." *Math. of Operations Research*. Dec-POMDP framing — NEXP-complete.
- Oliehoek and Amato (2016) *A Concise Introduction to Decentralized POMDPs*. Springer.
- Numeric thresholds (cost-of-communication, observation budgets) are domain-specific. Verify against primary references before using as decision authority.
- Brooks, F.P. (1975/1995) *The Mythical Man-Month*. Addison-Wesley. Source for the team-size / coordination-cost curve (#8b): pairwise coordination links grow combinatorially with team size, used here as a qualitative mechanism, not a quantitative team-theory result.
- Eldor, Hodor, and Cappelli (2023, *Organizational Behavior and Human Decision Processes* 177) is the primary empirical source for the psychological-safety curvilinear boundary condition cited via Edmondson & Bransby (2023); author names confirmed 2026-07-11, full text remains paywalled.
- DPI argument for single-agent dominance: Tran & Kiela (2026, arXiv:2604.02460) demonstrate empirically across four model families and five MAS architectures that single-agent systems match or exceed multi-agent on multi-hop reasoning under equal token budgets, with theoretical grounding in the Data Processing Inequality.
- Latent-space inter-agent communication: LatentMAS (Zou et al. 2025, arXiv:2511.20639, ICML 2026 Spotlight) demonstrates that sharing last-layer embeddings between LLM agents achieves lossless information exchange with 14.6% accuracy gains and 4× inference speedup over text-based multi-agent baselines across 9 benchmarks. Code at github.com/Gen-Verse/LatentMAS.
- Emergent self-organization at scale: Dochkina (2026, arXiv:2603.28990, IEEE Access) demonstrates across 25,000 tasks and 8 model families that self-organizing agents with minimal structure outperform designed hierarchies by 14% (Cohen's d=1.86) and scale sub-linearly to 256 agents. Corroborated by CARD (Wu et al., ICLR 2026) and MegaAgent (ACL 2025).
- Human-AI teaming mode as information structure: Systematic review (npj AI, Nature portfolio, December 2025, N=52 clinical studies) finds simultaneous human-AI observation outperforms sequential mode; corroborated by PRISMA review of 104 studies (Kargarnovin et al., Frontiers in Robotics and AI, 2026) and PNAS Nexus complementarity framework (Gonzalez et al., 2026).

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
