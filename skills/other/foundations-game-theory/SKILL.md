---
name: foundations-game-theory
description: Game-theory primitives for strategic decision systems, auctions, incentives, attribution, negotiation, debate, and trust. Use when modeling strategic coordination.
compatibility: Claude Code + Codex. Portable core — primitives apply across domains.
version: "1.1"
last_validated: 2026-07-11
---

# Game Theory Foundations


22 applied game-theory primitives for strategic decision systems, backed by a formal theory map. Each applied primitive solves a specific incentive or coordination failure. Primitives are domain-agnostic: the same mechanism that prevents free-riding in agent teams prevents cost-shifting in partnership contracts; the same auction that routes tasks routes ad placements.

For the agent-team applied recipe layer (team.yaml manifest fields, agent-team anti-patterns, agent-team decision checklist, composition recipes for typical agent-team scenarios), see [`agents-subagents/references/game-theory-agent-teams.md`](../agents-subagents/references/game-theory-agent-teams.md).

## Contents

- [Quick Reference](#quick-reference)
- [Primitive Index](#primitive-index)
- [Formal Supporting Theory](#formal-supporting-theory)
- [Expert Judgment: When the Model Helps vs Misleads](#expert-judgment-when-the-model-helps-vs-misleads)
- [Anti-Patterns](#anti-patterns)
- [Misuse Boundaries](#misuse-boundaries)
- [Decision Checklist](#decision-checklist)
- [Composition Recipes](#composition-recipes)
- [Workflow](#workflow)
- [ASCII Flow](#ascii-flow)
- [Current Pattern Review](#current-pattern-review)
- [Navigation](#navigation)
- [Fact-Checking](#fact-checking)

---

## Quick Reference

| Primitive | Domain | Recipe Stub |
|-----------|--------|-------------|
| [Belief-Driven Coordination (ECON)](#1-belief-driven-coordination-econ) | Multi-party teams, distributed analysis, agent teams | Members optimize against beliefs about co-members; reduces redundant work and inter-member chat |
| [Adversarial Debate](#2-adversarial-debate) | Content moderation, risk review, audit | Two heterogeneous evaluators + reasoning-tree synthesis; no majority vote |
| [Auction-Based Routing](#3-auction-based-task-routing) | Ad placement, task delegation, resource allocation | Sealed-bid truthful auction; highest-value-per-cost wins |
| [Shapley Contribution](#4-shapley-contribution-scoring) | Attribution, revenue sharing, team composition | Marginal-contribution average across subsets |
| [Reputation-Gated Autonomy](#5-reputation-gated-autonomy) | Supplier qualification, agent oversight, fraud gating | Tiered trust: proven → standard → probationary; oversight inversely proportional |
| [Cooperation and Defection](#6-cooperation-and-defection) | Partnership design, incentive alignment, compliance | Iterated PD structure; payoff-scale to detect defection tendency |
| [Mechanism Design for Synthesis](#7-mechanism-design-for-synthesis) | Decision aggregation, voting, policy-making | Vickrey truthful-revelation; dissent is a required section |
| [Courtroom-Style Debate](#8-courtroom-style-debate) | Legal review, risk go/no-go, claim verification | Plaintiff/defense/court structure + progressive RAG + role-switching |
| [Pareto-Nash Multi-Objective](#9-pareto-nash-multi-objective) | Product tradeoffs, regulatory vs growth, pricing tiers | Map Pareto frontier; pick dominant options; flag non-dominated set |
| [Evolutionary Coordination Search](#10-evolutionary-coordination-search) | Algorithm selection, prompt tuning, rule evolution | LLM-mutated program + fitness signal; ShinkaEvolve for sample efficiency |
| [Prediction Market Confidence](#11-prediction-market--confidence-betting) | Forecasting, risk calibration, hiring decisions | Stake-weighted confidence; CritiCal calibration step before stake |
| [Negotiation ZOPA/BATNA](#12-negotiation-protocol-zopabatna) | Pricing, partnership terms, resource contention | Map BATNA/ZOPA per party; target overlap zone; use interests not positions |
| [Reasoning-Tree Audit](#13-reasoning-tree-audit) | High-stakes synthesis, compliance review, claim checking | Trace claims to evidence at First Point of Disagreement; reject unsupported majority |
| [Per-Claim Credibility Scoring](#14-per-claim-credibility-scoring) | Misinformation detection, adversarial content, security | Evidence quality × corroboration weight per claim; isolate high-risk claims |
| [Generative Social Choice](#15-generative-social-choice) | Multi-stakeholder policy, diverse-user product decisions | Maximin selection across candidate outputs; preserve minority-signal coverage |
| [Meta-Debate Role Routing](#16-meta-debate-role-routing) | Debate setup, role-fit selection, agent teams | Two-stage proposal + peer-review picks plaintiff/defense/judge from a pool |
| [Online Shapley Prompt Evolution](#17-online-shapley-prompt-evolution) | High-frequency teams, prompt tuning over many runs | Per-member prompt mutation guided by Shapley contribution (HiveMind) |
| [Beyond Majority Voting (BMV)](#18-beyond-majority-voting) | Best-of-N synthesis (discrete answer), ensemble selection | Optimal Weight (confidence × calibration) + Inverse Surprising Popularity |
| [Radial Consensus Score (RCS)](#19-radial-consensus-score) | Best-of-N synthesis (open-ended generation), self-consistency | Embedding-centroid selector for semantically clustered, lexically diverse answers |
| [Conformal Social Choice](#20-conformal-social-choice-actescalate) | High-stakes debate verdicts, act/escalate gates | Calibrated prediction set: singleton acts, multi-answer set escalates |
| [Attested Delegation Contracts](#21-attested-delegation-contracts) | Cross-trust subagent routing, agent marketplaces, external tools | Route by verified capability and bounded contract, not self-claimed quality |
| [Coalition Formation Routing](#22-coalition-formation-routing) | Large teams, departments, multi-workstream audits | Form stable subteams before synthesis; avoid flat-panel overload |

---

## When to Apply

**Apply game-theory primitives when:**
- Multiple agents/teams/users with potentially divergent incentives
- Synthesis where minority-correct outcomes matter (high-stakes, irreversible)
- Auctions, bidding, mechanism design, or pricing where strategic behaviour exists
- Repeated interactions where reputation, cooperation, or trust evolves
- Best-of-N selection across 5+ candidates (BMV/RCS)
- Cross-trust delegation, dynamic agent pools, or high-stakes act/escalate decisions

**Skip and use simpler alternatives when:**
- Single agent / single-shot task — game theory is about *interactions*, not solo work
- Routine task with high majority-correct rate — a deterministic check or oracle is cheaper
- Hard verification exists (test suite, schema, calculator) — use the oracle, not voting
- Team < 3 members on a low-stakes call — overhead exceeds diversity gain
- Information-only retrieval / pure compression — use foundations-information-theory instead
- Single-system reliability/SLO question — use foundations-reliability-theory or queueing-theory

---

## Primitive Index

Each primitive has a full playbook (problem, solution, how-it-works, launch-prompt template, domain applications, citations).

| # | Mechanism | Failure Mode It Addresses |
|---|-----------|--------------------------|
| 1 | [Belief-Driven Coordination (ECON)](assets/templates/game-theory/01-econ-belief-driven.md) | Pooling equilibrium — members read same context, produce same analysis |
| 2 | [Adversarial Debate](assets/templates/game-theory/02-adversarial-debate.md) | Confabulation consensus, correlated bias |
| 3 | [Auction-Based Task Routing](assets/templates/game-theory/03-auction-task-routing.md) | Static routing, ambiguous selection |
| 4 | [Shapley Contribution Scoring](assets/templates/game-theory/04-shapley-contribution.md) | Free-riding, unverifiable attribution |
| 5 | [Reputation-Gated Autonomy](assets/templates/game-theory/05-reputation-gating.md) | Uniform trust regardless of track record |
| 6 | [Cooperation and Defection](assets/templates/game-theory/06-cooperation-defection.md) | Shallow output, scope dumping, echo chambers |
| 7 | [Mechanism Design for Synthesis](assets/templates/game-theory/07-mechanism-design-synthesis.md) | Loudest-wins aggregation, suppressed dissent |
| 8 | [Courtroom-Style Debate (PROClaim)](assets/templates/game-theory/08-courtroom-proclaim.md) | Evidence stagnation, position-anchored reasoning |
| 9 | [Pareto-Nash Multi-Objective](assets/templates/game-theory/09-pareto-nash.md) | Single-objective optimization on multi-objective problems |
| 10 | [Evolutionary Coordination Search](assets/templates/game-theory/10-alphaevolve.md) | Hand-tuned rules are sub-optimal vs. measured fitness |
| 11 | [Prediction Market / Confidence Betting](assets/templates/game-theory/11-prediction-market.md) | Verbose output dominates synthesis |
| 12 | [Negotiation Protocol (ZOPA/BATNA)](assets/templates/game-theory/12-negotiation-zopa-batna.md) | Adversarial framing on genuine compromise situations |
| 13 | [Reasoning-Tree Audit](assets/templates/game-theory/13-reasoning-tree-audit.md) | Confident-but-wrong consensus; majority vote unsafe |
| 14 | [Per-Claim Credibility Scoring](assets/templates/game-theory/14-credibility-scoring.md) | Single-claim failure modes reputation gating misses |
| 15 | [Generative Social Choice](assets/templates/game-theory/15-generative-social-choice.md) | Multi-stakeholder buy-in; averaging erases minority evidence |
| 16 | [Meta-Debate Role Routing](assets/templates/game-theory/16-meta-debate-routing.md) | Wrong specialist gets the wrong debate role; static role assignment |
| 17 | [Online Shapley Prompt Evolution](assets/templates/game-theory/17-online-shapley-prompt-evolution.md) | Weak team members never improve; static prompts under-utilize Shapley signal |
| 18 | [Beyond Majority Voting (BMV)](assets/templates/game-theory/18-beyond-majority-voting.md) | Majority vote on best-of-N erases minority-correct answers (calibration ignored) |
| 19 | [Radial Consensus Score (RCS)](assets/templates/game-theory/19-radial-consensus-score.md) | Lexical-overlap voting fails on semantically clustered open-ended generations |
| 20 | [Conformal Social Choice Act/Escalate](assets/templates/game-theory/20-conformal-social-choice.md) | Wrong consensus turns into irreversible action |
| 21 | [Attested Delegation Contracts](assets/templates/game-theory/21-attested-delegation-contracts.md) | Self-claimed quality corrupts routing across trust boundaries |
| 22 | [Coalition Formation Routing](assets/templates/game-theory/22-coalition-formation-routing.md) | Large flat panels duplicate work and produce unstable synthesis |

---

## Formal Supporting Theory

The 22 primitives are the applied layer, not the whole field. Use [`references/formal-theory-map.md`](references/formal-theory-map.md) when the task needs formal assumptions, proof obligations, or classical theory coverage.

| Theory Area | Use When | Applied Primitives It Grounds |
|---|---|---|
| Game forms | Need to classify normal-form, extensive-form, Bayesian, repeated, stochastic, or cooperative structure | #1, #6, #8, #9, #10, #12 |
| Solution concepts | Need dominance, minimax, Nash, Bayesian Nash, subgame-perfect, perfect Bayesian, or correlated equilibrium | #1, #2, #6, #8, #9, #10, #18 |
| Mechanism and auction design | Need incentive compatibility, individual rationality, revelation principle, VCG, Myerson, reserves, or bid shading | #3, #7, #11, #20, #21 |
| Information economics | Need signaling, screening, adverse selection, moral hazard, principal-agent framing, or attestation | #5, #7, #12, #14, #21 |
| Cooperative game theory | Need Shapley, core, nucleolus, Banzhaf, coalition formation, or surplus sharing | #4, #6, #15, #17, #22 |
| Market design and matching | Need stable matching, deferred acceptance, matching with contracts, or allocation without prices | #3, #7, #12, #15 |
| Bargaining theory | Need Nash bargaining, Rubinstein bargaining, BATNA/ZOPA, outside options, or alternating offers | #12 |
| Learning in games | Need no-regret, fictitious play, CFR, PSRO, self-play, or empirical game-theoretic analysis — including no-regret Nash policy convergence in RLHF (INPO, ICLR 2025 Oral) and smooth RM+ last-iterate convergence [NeurIPS 2025] | #6, #10, #11, #17 |
| Strategic failure analysis | Need collusion, equilibrium selection, Goodharting, manipulation, or off-equilibrium threats | all primitives |

---

## Expert Judgment: When the Model Helps vs Misleads

Applying a primitive correctly is mechanical. Knowing whether the game-theoretic frame is the right frame at all — and which game — is the actual expert skill. This section is judgment, not a lookup table.

### The equilibrium selection problem

Most interesting games (repeated games especially — see the Folk Theorem in [`formal-theory-map.md`](references/formal-theory-map.md)) have **many** equilibria, not one. A non-expert computes an equilibrium and reports it as "the" prediction. An expert checks multiplicity first and asks what actually selects among the candidates in this specific situation — precedent, an explicit contract, a public commitment, a focal point, or repeated-play reputation. Reporting "the Nash equilibrium is X" without naming the selection mechanism is a tell that the analysis stopped one step too early.

### Common-knowledge assumptions failing in practice

Nash equilibrium, Bayesian Nash equilibrium, and most mechanism-design proofs assume common knowledge of rationality, of payoffs (or their distribution), and of the rules of the game itself. Real organizations violate all three routinely:

- A "competitor" may be a satisficer bound by an internal OKR or a legacy contract, not a profit-maximizing best-responder — modeling them as rational invites a confidently wrong prediction.
- Bidders or negotiating parties often do not share a common prior on value — private information about downstream use, not risk attitude, is driving the gap.
- LLM agents do not reliably best-respond at all: pro-social bias, framing sensitivity, and authority compliance are documented, repeated deviations from Nash play (see the LLM rationality trap in [`patterns-scenarios-traps.md`](references/patterns-scenarios-traps.md)). Any incentive-compatibility argument built on "agents best-respond" needs a held-out behavioral check before it is trusted for LLM participants.

Habit: before invoking a solution concept, ask "would every party recognize this as the same game I do?" If not, either model it explicitly as a game of incomplete information (Bayesian game) or drop equilibrium language and use the frame as a heuristic only.

### Mapping a business situation to the right game

Non-experts reach for "prisoner's dilemma" or "Nash equilibrium" as a generic label for any tense multi-party situation. An expert asks a short sequence of diagnostic questions before naming a game form or picking a primitive:

1. **Who are the real strategic actors?** Not every interested party is a strategic player — a regulator reacting on a multi-year lag is closer to an exogenous constraint than a player in a weekly pricing game.
2. **One-shot or repeated — do the players expect to meet again?** A single vendor negotiation is a bargaining problem (#12); an ongoing supplier relationship is a repeated game where reputation and folk-theorem-style cooperation are available — analyzing it as one-shot recommends defection that is actually irrational given the relationship's shadow of the future.
3. **Simultaneous or sequential, and who commits first?** Prices set quarterly and observed by competitors before they respond is closer to Stackelberg (sequential, first-mover) than Cournot/Bertrand (simultaneous) — the right model changes the recommendation from "best-respond" to "commit and signal."
4. **Is value created cooperatively or contested?** Cooperative-game tools (Shapley, core) fit attribution and surplus-sharing (#4); competitive tools (auctions, Nash) fit contested allocation (#3, #9). Applying auction logic to a joint-venture split, or Shapley logic to a zero-sum negotiation, produces answers that are precise and wrong.
5. **Is there a credible commitment device?** A threat or promise only constrains behavior if the counterparty believes it will be carried out even against the threatener's own later interest. A pricing "war" threat with no sunk cost or public commitment behind it is cheap talk — treat it as information about intent, not as a binding constraint on the game tree.
6. **Is this actually a game, or an oracle-verifiable fact?** The most common non-expert error in this whole domain is running a debate, auction, or negotiation protocol over a question that has a deterministic answer — a test suite, a contract clause, a calculator. See [Misuse Boundaries](#misuse-boundaries).

### Mechanism-design failure modes that only surface in production

Textbook mechanism design proves *existence* of a truthful, efficient, individually rational mechanism under an idealized participant model. Each row below is a normal way real deployments break that idealization — not an edge case to footnote.

| Failure Mode | What Breaks | Real-World Trigger | Mitigation |
|---|---|---|---|
| **Collusion / bidder rings** | Dominant-strategy truthfulness assumes independent bidders; a ring that agrees off-mechanism to suppress bids and split the surplus defeats VCG and second-price auctions alike | Repeated auctions with a small, stable, identifiable bidder pool | Reserve prices, bidder-pool rotation, anti-collusion monitoring ([`AntiCollusionAI`](references/patterns-scenarios-traps.md)); detect via markup-over-marginal-cost drift over many rounds, not spot price |
| **False-name bids** | A single bidder submits multiple identities; VCG is provably **not** false-name-proof in combinatorial auctions, and no false-name-proof mechanism is Pareto efficient in general (Yokoo, Sakurai & Matsubara, *Games and Economic Behavior*, 2004) | Any auction where identity is cheap to fabricate — email-based registration, sybil-able agent pools, unverified marketplace accounts | Require attested identity before bidding (mirrors #21 Attested Delegation Contracts) — price identity verification into the mechanism, not as an afterthought |
| **Participation constraints failing** | Individual rationality assumes the average outside option; when the *highest*-value participants have the best outside options, they opt out first and adversely select the remaining pool | A mechanism designed around expected participants, not the marginal one who is deciding whether to walk | Check IR against the highest-value participant's outside option; Myerson & Satterthwaite (1983) show no mechanism for private-value bilateral trade can be simultaneously efficient, budget-balanced, and individually rational — some efficiency loss or subsidy is structurally unavoidable |
| **Budget imbalance** | VCG is efficient and truthful but generally runs a deficit or surplus that must land somewhere | Multi-sided mechanisms with no natural residual claimant | Decide upfront who absorbs the imbalance (platform take-rate, budget-neutral variant, or accept the inefficiency) rather than discovering it at settlement |
| **Computational infeasibility** | Exact VCG for combinatorial allocation requires solving an often NP-hard optimization for the winning allocation and every counterfactual-without-bidder-*i* allocation | Task/resource routing over bundles, not single-item slots | Use approximate/greedy VCG variants and disclose the resulting efficiency loss, or restrict to single-item/separable settings where exact VCG is tractable |

**Practical tell**: if a mechanism is called "truthful" or "incentive-compatible" but nobody can name (a) the participation constraint being satisfied, (b) how false identities are prevented, and (c) who absorbs budget imbalance, the claim has not actually been checked.

---

## Anti-Patterns

| Anti-Pattern | Game Theory Diagnosis | Fix |
|-------------|----------------------|-----|
| Majority vote in high-stakes aggregation | Correlated errors pass; LLMs share biases | Reasoning-tree audit (#13) traces each claim to evidence |
| Single-objective optimization on a tradeoff decision | Pareto-dominant alternatives go unexamined | Map Pareto frontier (#9) before committing |
| Attribution by seniority or loudness | Free-riding goes undetected; poor performers stay | Shapley marginal-contribution scoring (#4) |
| Flat trust applied uniformly | High-risk counterparties get same autonomy as proven ones | Reputation-gated tiers (#5) calibrate oversight to track record |
| Adversarial debate forced on genuine compromises | Positions harden; ZOPA never located | Switch to negotiation protocol (#12) when there is a continuous tradeoff |
| Confidence staking without calibration | Overconfident participants dominate synthesis | CritiCal calibration step before prediction market (#11) staking |
| Synthesis suppresses dissent | Minority-correct signal is erased | Dissent required as a section in mechanism-design synthesis (#7) |
| Uniform cooperation assumed in partnerships | Defection undetected until costly | Iterated payoff-scale test (#6) surfaces defection tendency early |
| All members read same context, produce overlapping analysis | Pooling equilibrium — no belief differentiation | Belief-driven coordination (#1) gives each member a unique lane |
| Static debate role assignment regardless of question | Wrong-specialist assignment dominates outcome | Meta-debate role routing (#16) — propose + peer-review picks plaintiff/defense/judge |
| Best-of-N collapsed by majority vote | Calibration and minority-correct signal lost | Beyond Majority Voting (#18) — Optimal Weight + Inverse Surprising Popularity |
| Open-ended generation scored by lexical overlap | Semantically equivalent answers split the vote | Radial Consensus Score (#19) — embedding-centroid selector |
| Consensus treated as permission to act | Wrong agreement becomes automated harm | Conformal Social Choice (#20) — act only on singleton calibrated set |
| Routing by self-claimed delegate quality | Strategic or misconfigured delegates attract work | Attested Delegation Contracts (#21) — verify identity/capability and bound authority |
| Large team run as one flat panel | Duplicate work, coalition instability, synthesis overload | Coalition Formation Routing (#22) — stable subteams before final synthesis |

---

## Misuse Boundaries

| Misuse | Why It Is Wrong | Required Correction |
|---|---|---|
| Applying game theory when a deterministic validator exists | Hard oracles beat strategic synthesis | Run tests, compilers, schema checks, SQL, or calculators first |
| Calling a workflow incentive-compatible without payoffs | Truth-telling is not a label; it requires a payoff structure | State the mechanism, utility model, and best-response argument |
| Treating LLM agents as economic agents with stable preferences | Models follow prompts and context, not durable utility functions | Reframe as an operational heuristic unless preferences are explicit |
| Using Shapley when contribution is not measurable | Attribution becomes story-telling | Define the value function and approximation before scoring |
| Using debate when disagreement is caused by missing data | Debate amplifies uncertainty instead of resolving it | Retrieve, measure, or ask for missing evidence first |
| Using RCS/BMV when a hard oracle exists | Selection mechanisms can suppress the verifiable answer | Use the oracle, then optionally synthesize explanations |
| Using reputation as proof of claim truth | Strong participants can make local errors | Run per-claim credibility scoring |
| Using equilibrium language without checking equilibrium selection | Multiple equilibria can imply opposite recommendations | List candidate equilibria and the selection assumption |
| Optimizing one metric in a multi-party mechanism | Goodharting shifts harm to unmeasured parties | Add Pareto and stakeholder checks before launch |
| Hiding minority evidence in synthesis | Minority-correct answers are a common failure case | Preserve dissent, runner-up, and outlier evidence |
| Calling a multi-principal synthesis incentive-compatible without designing a payment scheme | Truthful reporting is strictly dominated without payments in multi-stakeholder settings (NeurIPS 2024 proof) | Add affine maximizer (weighted VCG) payment or explicitly scope to a single-principal setting |

---

## Decision Checklist

- [ ] **Routing**: Is the problem multi-option with measurable fit signal? → auction (#3)
- [ ] **Attribution**: Does the output depend on contributions from multiple sources? → Shapley (#4)
- [ ] **Aggregation**: Does synthesis combine claims with varying quality? → reasoning-tree audit (#13) + mechanism-design synthesis (#7)
- [ ] **Trust calibration**: Are participants heterogeneous in track record? → reputation gating (#5)
- [ ] **Tradeoff detection**: Are there multiple incommensurable objectives? → Pareto-Nash (#9) or negotiation (#12)
- [ ] **High-stakes binary decision**: Needs evidential audit trail? → courtroom debate (#8)
- [ ] **Adversarial context**: Claims may be injected or manipulated? → per-claim credibility scoring (#14)
- [ ] **Multi-stakeholder output**: Multiple user types with different needs? → generative social choice (#15)
- [ ] **Prediction / forecast**: Confidence calibration required? → prediction market (#11)
- [ ] **Long-running coordination rule**: Has a measurable quality signal over many runs? → evolutionary coordination search (#10)
- [ ] **Multi-party context-sharing risk**: Members may produce overlapping analysis? → belief-driven coordination (#1)
- [ ] **Best-of-N synthesis (discrete answer)**: Need to recover minority-correct? → BMV (#18)
- [ ] **Best-of-N synthesis (open-ended)**: Lexically diverse but semantically clustered candidates? → RCS (#19)
- [ ] **Repeated team optimization**: 50+ runs with measurable contribution signal? → online Shapley prompt evolution (#17)
- [ ] **Debate role-fit ambiguity**: Best plaintiff/defense not the obvious specialist? → meta-debate role routing (#16)
- [ ] **High-stakes act/escalate**: Debate agreement is not enough? → conformal social choice (#20)
- [ ] **Cross-trust delegation**: Delegate can self-claim quality or authority? → attested delegation contract (#21)
- [ ] **Large team topology**: 6+ members or distinct workstreams? → coalition formation routing (#22)

---

## Composition Recipes

See [`assets/templates/game-theory/README.md`](assets/templates/game-theory/README.md) for full domain-scenario stacks.

Quick stacks:

- **Pricing / monetization**: #9 (Pareto-Nash for objective mapping) + #12 (BATNA/ZOPA for negotiation range) + #7 (synthesis dissent required)
  **Inputs:** Competitor price points, own marginal cost, demand elasticity estimate, switching cost for buyer.
  **Rules:** Map Pareto frontier across price/margin/volume objectives (#9); compute BATNA floor and ZOPA ceiling per party (#12); run Bertrand floor check — if product is undifferentiated, price collapses to marginal cost; differentiation (feature, brand, lock-in) is required to hold above floor; synthesis must surface dissenting price band (#7).
  **Outputs:** Price band (floor = marginal cost or BATNA, ceiling = ZOPA upper bound), differentiation requirement to sustain above-floor pricing, dissent note if any Pareto-dominated option was preferred by a stakeholder.

- **Ad bidding / task routing**: #3 (auction routing) + #4 (Shapley ROI attribution) + #11 (confidence-weighted forecast)
  **Inputs:** Bidder count, valuation distribution (private or correlated), bid visibility (sealed vs. open), budget constraints.
  **Rules:** If private values and bids sealed → 2nd-price (Vickrey) dominant; if bids are publicly visible → 1st-price + reserve (visible bids flip incentive to overbid for signalling, collapsing the 2nd-price guarantee); attribute ROI across winning bidder's components via Shapley marginal contribution; calibrate confidence forecasts via CritiCal step before staking.
  **Outputs:** Mechanism choice (1st-price + reserve vs. 2nd-price), expected revenue estimate, per-component Shapley ROI attribution, calibrated confidence interval on forecast.

  **Worked example — marketplace switching from 1st-price to 2nd-price (Vickrey) auction.** Bidders: 4, valuations [10, 8, 6, 4]. 1st-price equilibrium: rational bid shading produces bids ≈ [7.5, 6, 4.5, 3] → revenue = 7.5 (winner pays own bid). 2nd-price truthful: bids = [10, 8, 6, 4] → revenue = 8 (winner pays 2nd-highest). Truthfulness gain: +6.7% revenue, plus zero bid-shading complexity → fewer abandoned bids and lower ops cost. Anti-pattern: don't run 2nd-price with publicly visible bids — incentive flips to overbid for signalling and the dominant-strategy guarantee collapses.

- **Security / adversarial context**: #14 (per-claim credibility) + #13 (reasoning-tree audit) + #8 (courtroom for go/no-go)
  **Inputs:** Claim set under review, evidence sources per claim, adversarial threat model (injection vector, attacker capability), go/no-go decision stakes.
  **Rules:** Score each claim independently on evidence quality × corroboration weight (#14); trace every claim to its First Point of Disagreement in the reasoning tree (#13); run courtroom plaintiff/defense/judge only after per-claim scoring — debate over unsupported claims amplifies uncertainty rather than resolving it.
  **Outputs:** Per-claim credibility score, reasoning-tree audit trail, go/no-go recommendation with dissent preserved, list of claims that failed credibility threshold and require retrieval before re-evaluation.

- **Partnership design**: #6 (cooperation-defection payoff test) + #5 (reputation gating) + #12 (ZOPA negotiation)
  **Inputs:** Partner track record (prior-interaction count n, defection incidents), payoff matrix cells for cooperation vs. defection on the proposed arrangement, each party's BATNA and stated interests.
  **Rules:** If n < 3 interactions → require contractual escrow or clawback clause (iterated PD cannot be relied on with insufficient history); if n ≥ 3 and no defection → tit-for-tat sufficient; assign reputation tier (probationary / standard / proven) based on defection rate and interaction depth (#5); locate ZOPA as overlap between each party's reservation value and walk-away point (#12); flag if no ZOPA exists — do not negotiate, renegotiate the scope.
  **Outputs:** Recommended contract structure (escrow clause if n < 3, tit-for-tat terms if n ≥ 3), reputation tier assigned, ZOPA range or no-deal flag, payoff-scale test result (cooperation dominant or defection dominant under current incentives).

- **High-quality synthesis**: #13 (reasoning-tree audit) + #7 (mechanism-design synthesis) + #11 (confidence betting)
  **Inputs:** Candidate outputs or claims, evidence source per claim, participant confidence estimates, synthesis stakes (reversible vs. irreversible decision).
  **Rules:** Audit reasoning tree to First Point of Disagreement before aggregating (#13); require dissent as a mandatory section in synthesis output (#7); run CritiCal calibration on participant confidence before staking (#11) — overconfident participants otherwise dominate.
  **Outputs:** Synthesized recommendation with dissent section, per-claim evidence trace, calibrated confidence interval, list of unresolved disagreements requiring further evidence.

- **High-stakes act/escalate**: #13 (reasoning-tree audit) + #11 (confidence elicitation) + #20 (conformal social choice)
  **Inputs:** Candidate actions, member probability distributions, calibration table or shadow-case history, escalation cost.
  **Rules:** Treat agreement as evidence, not proof; pool distributions; act only when the calibrated prediction set is singleton; escalate when the set has multiple plausible answers.
  **Outputs:** Singleton action or escalation reason, prediction set, confidence/calibration note, evidence that would shrink the set.

- **Cross-trust delegation**: #21 (attested delegation contracts) + #3 (auction routing) + #5 (reputation gating)
  **Inputs:** Delegate pool, attested capabilities, authority boundary, acceptance criteria, failure policy.
  **Rules:** Filter by verified capability before any bidding; never route by self-claimed quality; give the winner a bounded contract; update reputation only from verified outcomes.
  **Outputs:** Eligible delegate set, chosen delegate, delegation contract, typed failure/recovery path, reputation update.

- **Large-team coalition routing**: #22 (coalition formation) + #1 (belief-driven coordination) + #4 (coalition-level Shapley)
  **Inputs:** Workstreams, member capabilities, dependency map, synthesis owner, deadline.
  **Rules:** Form stable coalitions around workstreams; run local coalition analysis first; synthesize coalition leads rather than every raw member output; check that no load-bearing workstream is unowned.
  **Outputs:** Coalition map, local findings, cross-coalition conflicts, final synthesis.

- **Multi-party teams (always-on baseline)**: #1 (belief-driven coordination) + #4 (Shapley) + #7 (synthesis with required dissent)
  **Inputs:** Team member count, context overlap risk (do members share the same documents/signals?), contribution measurability (can each member's marginal value be isolated?).
  **Rules:** Assign each member a unique belief lane to break pooling equilibrium (#1); compute Shapley marginal-contribution score per member per run (#4); synthesis must include dissent section — loudest-wins aggregation is the default failure mode (#7).
  **Outputs:** Belief lane assignment per member, Shapley contribution scores, synthesized output with dissent preserved, free-rider flag if any member's marginal contribution is near zero.

- **Best-of-N (discrete answer)**: #18 (BMV) — Optimal Weight + Inverse Surprising Popularity
  **Inputs:** N candidate answers (discrete), per-candidate confidence score, calibration data if available.
  **Rules:** Weight each candidate by confidence × calibration accuracy (Optimal Weight); apply Inverse Surprising Popularity to recover minority-correct answers that majority vote would suppress; do not apply if a hard oracle (test suite, schema check, calculator) is available — use the oracle directly.
  **Outputs:** Selected answer with weighted score, runner-up with score delta, flag if minority-correct candidate was recovered.

- **Best-of-N (open-ended generation)**: #19 (RCS) — embedding-centroid selector across 5+ candidates
  **Inputs:** 5+ candidate generations (open-ended text), embedding model, semantic similarity threshold.
  **Rules:** Embed all candidates; compute centroid; select candidate closest to centroid as representative; do not use lexical-overlap voting — semantically equivalent answers split the vote under lexical scoring.
  **Outputs:** Selected generation (centroid-nearest), semantic cluster map, outlier candidates flagged for manual review if they are far from centroid but potentially high-value.

- **High-frequency team optimization**: #4 (Shapley) + #17 (online Shapley prompt evolution) + #5 (reputation gating)
  **Inputs:** Run count (minimum 50 for meaningful Shapley signal), per-member contribution measurability, current prompt set per member.
  **Rules:** Compute Shapley contribution per member per run (#4); use Shapley signal to guide per-member prompt mutation each epoch (#17); gate autonomy by accumulated reputation tier — probationary members get tighter review until track record reaches standard tier (#5); do not apply online Shapley prompt evolution below 50 runs — signal is too noisy for reliable mutation.
  **Outputs:** Updated prompt per member (mutated toward higher Shapley contribution), reputation tier per member, contribution trend chart (improving / stable / degrading).

- **Building a multi-agent LLM application (full-stack recipe)**: #1 (belief-driven coordination) + #21 (attested delegation) + #5 (reputation gating) + #20 (conformal act/escalate) + #4 (Shapley attribution)
  **Inputs:** Agent pool (roles, capabilities, trust provenance), task decomposition map, reversibility of downstream actions, success metric per agent.
  **Rules:** Assign belief lanes at design time so agents receive differentiated context and cannot pool into a uniform analysis (#1); route sub-tasks only to delegates with attested (not self-claimed) capability — the provenance paradox shows self-claimed routing performs worse than random (#21); start every new agent on probationary tier; promote to standard tier only after 3+ verified successful runs (#5); before any irreversible action (payment, send, deploy), check that the conformal prediction set is singleton — multi-answer set triggers human escalation (#20); compute Shapley marginal contribution per agent per release epoch to detect free-riders and guide prompt or architecture revision (#4). Anti-pattern: do not run a flat panel of 6+ agents — form coalitions by workstream first (#22).
  **Outputs:** Belief-lane assignment per agent, attested-capability registry, reputation tier per agent, act/escalate gate policy, Shapley contribution report per epoch, coalition map if team ≥ 6.

---

## Navigation

- Per-mechanism playbooks: [`assets/templates/game-theory/`](assets/templates/game-theory/) (one file per primitive)
- Composition guide: [`assets/templates/game-theory/README.md`](assets/templates/game-theory/README.md)
- Formal theory map: [`references/formal-theory-map.md`](references/formal-theory-map.md)
- April 2026 patterns, scenarios, and traps: [`references/patterns-scenarios-traps.md`](references/patterns-scenarios-traps.md)
- Domain-agnostic primitives overview: [`references/primitives-overview.md`](references/primitives-overview.md)
- Sources: [`data/sources.json`](data/sources.json)

---

## Current Pattern Review

Use [`references/patterns-scenarios-traps.md`](references/patterns-scenarios-traps.md) before applying a primitive to production or agent-team routing. It distinguishes durable game-theory mechanisms from fast-moving LLM-agent papers, lists scenario-specific stacks, and calls out traps such as majority-vote collapse, uncalibrated confidence, static role assignment, overusing debate, and source claims that have not been rechecked against primary papers.

---

## Workflow

1. Identify the strategic failure mode in your system (attribution, routing, synthesis, trust, negotiation, adversarial risk).
2. Use the [Quick Reference](#quick-reference) table to map failure mode → primitive.
3. Open the per-mechanism playbook in [`assets/templates/game-theory/`](assets/templates/game-theory/) for the full problem/solution/launch-prompt template.
4. For multi-failure scenarios, use the [Composition Recipes](#composition-recipes) or the full [`assets/templates/game-theory/README.md`](assets/templates/game-theory/README.md) to stack primitives.
5. Check [`references/patterns-scenarios-traps.md`](references/patterns-scenarios-traps.md) for April 2026 trap coverage before shipping the mechanism.
6. For agent-team applied recipes (team.yaml manifest fields, agent-team anti-patterns, decision checklist for team launches), load [`agents-subagents/references/game-theory-agent-teams.md`](../agents-subagents/references/game-theory-agent-teams.md).
7. For other domain applied recipes — pricing, paid advertising, CRO, security, market intel — see each domain skill's `references/game-theory-applied.md` (or `game-theory-pricing.md` for `startup-business-models`).

---

## ASCII Flow

```text
Strategic interaction or incentive failure
  -> Identify actors, payoffs, information, and repeatedness
  -> Classify failure: attribution, routing, synthesis, trust, negotiation, adversarial risk
  -> Select applied mechanism
     +-- shared payoff only -> consider team theory instead
     +-- divergent incentives -> continue with game-theory primitive
  -> Check formal assumptions and pattern traps
  -> Produce mechanism, launch rule, evidence requirement, and fallback
```

---

## Related Skills

- `agents-subagents` — agent-team applied recipes: team.yaml manifest fields, agent-team anti-patterns, decision checklist
- [`marketing-paid-advertising`](../marketing-paid-advertising/references/game-theory-applied.md) — paid auction recipes (GSP/VCG, bid shading, budget pacing)
- [`startup-business-models`](../startup-business-models/references/game-theory-pricing.md) — pricing recipes (VCG, Hotelling, Folk Theorem, signaling)
- [`marketing-cro`](../marketing-cro/references/game-theory-applied.md) — experimentation recipes (Thompson, MAB, sequential testing)
- [`software-security-appsec`](../software-security-appsec/references/game-theory-applied.md) and [`qa-security-testing`](../qa-security-testing/references/game-theory-applied.md) — defender/attacker recipes (Stackelberg, honeypots)
- [`startup-market-intel`](../startup-market-intel/references/game-theory-applied.md) — competitive recipes (Stackelberg, Bertrand, Cournot, Hotelling positioning)

---

## Fact-Checking

- Verify paper results (accuracy deltas, token counts) against primary arxiv sources before treating them as benchmarks.
- Mechanism effectiveness is task- and domain-specific. Test on a held-out sample before deploying at scale.
- Source links and verified dates in each per-mechanism file are the canonical evidence tier.
- If web access is unavailable, mark runtime-specific claims as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.
