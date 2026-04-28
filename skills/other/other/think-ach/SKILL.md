---
name: think-ach
description: Analysis of Competing Hypotheses. Operationalizes Richards Heuer's CIA-tradition technique for systematically narrowing among multiple hypotheses against evidence. Builds an explicit hypothesis-vs-evidence matrix and focuses on disconfirmation rather than confirmation — the central insight: hypotheses cannot be proven, only disconfirmed; the surviving hypothesis is the one with the least disconfirming evidence. Spawns parallel hypothesizers (in isolation, across hypothesis-generation angles) and parallel evidence-gatherers (across evidence classes), then synthesizes into a matrix, diagnosticity analysis, sensitivity analysis, and falsification milestones. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-ACH - Analysis of Competing Hypotheses

Systematically narrows among multiple hypotheses against evidence using Richards Heuer's Analysis of Competing Hypotheses (ACH) technique. Generates hypotheses (parallel, isolated), enumerates evidence (parallel, isolated), builds an explicit matrix mapping each piece of evidence against each hypothesis, focuses on *disconfirming* evidence to rank hypotheses, and reports the surviving leader along with sensitivity analysis and falsification milestones.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured analysis the user can act on — a hypothesis leaderboard with the matrix that supports it.

## The technique

ACH was developed by Richards J. Heuer Jr. for the CIA Directorate of Intelligence and is documented in his book *Psychology of Intelligence Analysis* (1999). It was designed specifically to counter the cognitive failure modes that intelligence analysts (and everyone else reasoning under uncertainty) habitually exhibit:

- **Confirmation bias** — seeking evidence that confirms a preferred hypothesis rather than evidence that disconfirms competing ones
- **Premature closure** — locking in on the first plausible hypothesis and stopping the search
- **Anchoring** — letting the leading candidate dominate subsequent reasoning
- **Cherry-picking evidence** — emphasizing convenient evidence and rationalizing away inconvenient evidence
- **Failure to consider alternatives** — never enumerating the full hypothesis space

ACH's structural countermeasures:

1. **Force enumeration of all plausible hypotheses upfront** (anti-anchoring; anti-premature-closure)
2. **Build an explicit matrix** of evidence × hypothesis (anti-cherry-picking; makes the analysis legible)
3. **Focus on disconfirmation** — the central insight: a hypothesis cannot be proven, only disconfirmed. The surviving hypothesis is the one with the *least disconfirming evidence*, not the most confirming. (Anti-confirmation-bias.)
4. **Identify diagnosticity** — surface which evidence actually discriminates among hypotheses; drop evidence consistent with all
5. **Sensitivity analysis** — for each load-bearing piece of evidence, ask "what if this is wrong?" and watch how the conclusion changes
6. **Report all hypotheses, not just the leader** — preserve the alternatives so the user knows what's still in play
7. **Identify falsification milestones** — what future observation would distinguish the top candidates?

## When to use vs `/think-diagnose`

These two skills overlap in problem domain (multi-candidate evaluation under uncertainty) but are structurally distinct.

- **`/think-diagnose`** — open-ended causal exploration. *Generative + evaluative.* Lens-driven brainstorming of candidate causes (technical, human-factors, environmental, measurement-artifact, etc.) plus narrative evidence evaluation. Use when the user has a *phenomenon* and wants to understand its causes broadly. Output: leading candidates with distinguishing evidence needed.

- **`/think-ach`** — rigorous narrowing among hypotheses. *Primarily evaluative*, with explicit matrix structure and disconfirmation focus. Use when the user has *competing hypotheses* (provided or just-generated) and wants to systematically narrow among them. ACH is broader than diagnosis — it applies to causal attribution, forecasting, attribution-of-responsibility, strategic assessment, and similar multi-hypothesis questions.

Natural workflow when both apply: `/think-diagnose` generates candidate causes; `/think-ach` rigorously narrows among them. They are complementary, not duplicative.

ACH also stands alone for non-causal questions ("which of these scenarios is most likely?", "which actor is most likely responsible?", "which interpretation of the data is most defensible?").

## Roles

**Judge (you, running this skill):**
- Receive the question and any seed hypotheses
- Validate the question is ACH-shaped
- Spawn hypothesizers in isolation across angles
- Spawn evidence-gatherers in isolation across evidence classes
- Build the matrix (evaluating each cell independently)
- Run diagnosticity, disconfirmation-focused ranking, sensitivity analysis, and falsification-milestone identification
- Synthesize the report

**Hypothesizers** (`THK - ACH Hypothesizer`): Each receives the question and an assigned *angle* (leading, alternative, adversarial, null, deceptive, surprise). Generates hypotheses from that angle in isolation.

**Evidence-gatherers** (`THK - ACH Evidence Gatherer`): Each receives the question and an assigned *evidence class* (direct-observational, documentary-historical, structural, behavioral, absent, anomalous). Enumerates relevant evidence in that class in isolation.

## Workflow

### 1. Receive the Question and Any Seed Hypotheses

The question may arrive as:
- **Conversation context** — summarize back, confirm
- **A document** — read the file (incident report, design analysis, intelligence brief)
- **Fresh user input** — capture verbatim

The user may also provide seed hypotheses they already have in mind. Capture them as inputs to step 3 (they don't replace the parallel hypothesizers — they augment).

**Produce a written brief** of the question. A good brief includes:
- **The question** — what is being analyzed (a phenomenon, a forecast, an attribution claim, a scenario assessment)?
- **Scope** — what's in, what's out
- **Available evidence** — what evidence is available in principle (what records, observations, sources can be drawn on)?
- **Seed hypotheses** — any hypotheses the user has already articulated

### 2. Validate the Question Is ACH-Shaped

ACH applies when:

- **Multiple plausible hypotheses exist** — at least 3, ideally 4-7. With only 1-2 hypotheses, ACH is overkill; with 10+, the matrix becomes unwieldy and hypotheses are usually too granular.
- **Evidence is available** — there's enough material to discriminate among hypotheses. Pure speculation is not ACH territory.
- **Hypotheses are roughly mutually exclusive** — they should make different predictions about evidence. Hypotheses that all predict the same things cannot be discriminated.
- **The user wants rigorous narrowing** — not exploratory ideation. If the user wants to *generate* hypotheses, route to `/think-diagnose` (for causal questions) or `/think-brainstorm` (for action options) first.

If the question fails any check, **say so plainly and offer the alternative**:
- Too few hypotheses or too vague → `/think-diagnose` to generate causes, or `/think-brainstorm` to generate options
- Too thin evidence → narrow the question, or wait until more evidence is available
- Hypotheses not mutually exclusive → reframe so they make distinguishable predictions

### 3. Enumerate Hypotheses (Parallel, Isolated)

Spawn 4-6 `THK - ACH Hypothesizer` agents in parallel, each with a different angle.

**Hypothesis-generation angles:**

- **leading** — the obvious, popular, or most-favored hypothesis
- **alternative** — hypotheses that contradict the leading candidate
- **adversarial** — someone benefits from a specific outcome; intentional action by an actor
- **null** — nothing unusual is happening; appearances are normal; the boring hypothesis
- **deceptive** — appearances are intentionally misleading; someone is covering up
- **surprise** — an unexpected hypothesis that fits the evidence; the one nobody volunteered

**Selection heuristics:**

- Always include **leading** and **alternative** — these establish the basic competition
- Include **null** unless the phenomenon being analyzed is structurally non-null (i.e., something has demonstrably happened that requires explanation)
- Include **adversarial** when the question involves actors with motivations
- Include **deceptive** when the question involves trust, intelligence, security, or signals that could be manipulated
- Include **surprise** when the question is novel or the user is concerned about missing the right answer

User-provided seed hypotheses are added to the pool *after* the hypothesizers run — including them upfront would anchor the hypothesizers.

**No cross-talk between hypothesizers.** This is the NGT principle. Independent generation prevents the leading hypothesis from anchoring all the others.

The orchestrator merges and deduplicates. Final hypothesis count: typically 5-9.

### 4. Enumerate Evidence (Parallel, Isolated)

Spawn 3-5 `THK - ACH Evidence Gatherer` agents in parallel, each with a different evidence class.

**Evidence classes:**

- **direct-observational** — things directly observed (logs, sensor data, witness accounts, metric readings)
- **documentary-historical** — recorded artifacts (decision documents, prior reports, message threads, configuration history)
- **structural** — features of the system or environment that constrain what's possible (architecture, permissions, physical layout, access patterns)
- **behavioral** — patterns of action over time (user behavior, system behavior, organizational rhythms)
- **absent** — what's *not* there (the dog that didn't bark; missing logs, missing alerts, missing complaints)
- **anomalous** — observations that don't fit any obvious story; unexplained data points

**Selection heuristics:**

- Always include **direct-observational** if any direct observation exists
- Include **documentary-historical** for any non-instantaneous question
- Include **structural** for any system, code, or architectural question
- Include **behavioral** when the question involves agents (people or systems) acting over time
- Always include **absent** for security, intelligence, or deception-relevant questions — what's missing is often the most diagnostic evidence
- Include **anomalous** when the user has flagged unexplained observations

**No cross-talk between evidence-gatherers.** Independent enumeration prevents one strong piece of evidence from dominating attention; allows surfacing of evidence that the leading-hypothesis frame would suppress.

The orchestrator merges and deduplicates. Final evidence count: typically 8-20 items.

### 5. Build the Matrix

For each (hypothesis, evidence) cell, assess:

- **C** — *Consistent*: the evidence is consistent with this hypothesis being true
- **I** — *Inconsistent*: the evidence contradicts this hypothesis
- **N/A** — *Not applicable*: the evidence has no bearing on this hypothesis (different from "consistent" — silence is not support)

Optional intensity markers (**CC** strongly consistent, **II** strongly inconsistent) when the evidence is unusually decisive.

**Critical discipline:** evaluate each cell independently. Do not let prior cells anchor subsequent ones. This is structurally easier when working through the matrix systematically (e.g., one row at a time, then verify columns).

The matrix is the central artifact of the analysis. Display it explicitly in the report.

### 6. Diagnosticity Analysis

Some evidence discriminates among hypotheses; some doesn't. Discriminating evidence is *diagnostic*; non-discriminating evidence is *not diagnostic* and should be set aside.

For each piece of evidence, look across the row:

- **High diagnosticity** — evidence is consistent with some hypotheses and inconsistent with others. This is the load-bearing evidence; the analysis hinges on it.
- **Low diagnosticity** — evidence is consistent with all (or inconsistent with all). It tells us nothing about the relative likelihood. Drop it from the analysis or mark it as low-value.

Heuer's insight: *diagnosticity, not quantity, drives ACH conclusions.* A single piece of high-diagnosticity evidence outweighs ten pieces of low-diagnosticity evidence.

### 7. Disconfirmation-Focused Leaderboard

Rank hypotheses by *number of inconsistent (I) marks*, not by number of consistent marks.

This is the central insight. ACH is built on Karl Popper's falsification principle: a hypothesis cannot be proven, only failed-to-be-disproven. The hypothesis with the fewest disconfirmations is the most likely to survive further scrutiny.

The intuition: any hypothesis can accumulate "consistent" evidence. What kills hypotheses is *inconsistency*. The hypothesis that survives the disconfirmation tests — that is, has the fewest serious inconsistencies — is the leading candidate.

**Critical:** do not collapse to a single answer. ACH preserves all hypotheses in the leaderboard. The 2nd-place hypothesis is not "wrong"; it's "currently second." Future evidence can move it.

### 8. Sensitivity Analysis

For each load-bearing piece of evidence (high-diagnosticity, decisive), ask:

- What if this evidence is wrong?
- What if it's misinterpreted?
- What if it was fabricated, planted, or selectively presented?
- What if it has an alternative interpretation we haven't surfaced?

For each, watch what happens to the leaderboard. If a single piece of evidence flipping changes the leader, that evidence is *load-bearing* and worth verifying before acting on the analysis.

This step is critical. Informal reasoning treats evidence as ground truth. ACH is explicit that evidence is itself fallible.

### 9. Falsification Milestones

For the top 2-3 hypotheses, identify future observations that would distinguish among them:

- "If hypothesis A is correct, we should observe X within Y timeframe."
- "If hypothesis B is correct, we should observe Z."
- "Observation W would disconfirm both A and B; observation V would disconfirm only A."

This makes the analysis falsifiable and gives the user observable signals to monitor.

### 10. Report

**Final report format:**

```
## ACH Report

**Question:** [one-line]
**Hypothesis-generation angles applied:** [list]
**Evidence classes applied:** [list]

### Hypotheses

H1. **[hypothesis]** — *(angle: [angle])*
H2. **[hypothesis]** — *(angle: [angle])*
H3. **[hypothesis]** — *(angle: [angle])*
...

### Evidence

E1. [evidence] — *(class: [class])*
E2. [evidence] — *(class: [class])*
...

### Matrix

|     | H1 | H2 | H3 | H4 |
|-----|----|----|----|----|
| E1  | C  | I  | N/A | C  |
| E2  | I  | CC | C  | N/A|
| E3  | I  | C  | C  | I  |
| ... | ...| ...| ... | ...|

### Diagnosticity

**High-diagnosticity evidence (load-bearing):**
- E2 — [why it discriminates]
- E5 — [why it discriminates]

**Low-diagnosticity evidence (set aside):**
- E1 — consistent with H1 and H4; tells us little about which leads
- ...

### Leaderboard (ordered by least disconfirming evidence)

1. **[Hypothesis]** — N inconsistencies — [brief narrative]
2. **[Hypothesis]** — N+k inconsistencies — [brief narrative]
3. **[Hypothesis]** — N+m inconsistencies — [brief narrative]
...

### Sensitivity Analysis

**Load-bearing evidence and what changes if it's wrong:**

- **E2** is currently strongly inconsistent with H1 and consistent with H2. If E2 is misinterpreted, H1 jumps from rank 2 to rank 1. *Verifying E2 is the highest-leverage check.*
- ...

### Falsification Milestones

To distinguish the top hypotheses:

- **If H1 is correct**, we should observe [X] within [timeframe].
- **If H2 is correct**, we should observe [Y].
- Observation [Z] would disconfirm H1 but not H2.

### Notes and Caveats

- Hypotheses dropped during refinement (and why): ...
- Evidence we didn't have access to that could shift the analysis: ...
- Confidence in this analysis (qualitative): high / moderate / low / uncertain — and why

### Suggested Next Steps

- To verify load-bearing evidence: targeted investigation
- To narrow further as new evidence arrives: re-invoke `/think-ach` with the updated set
- To stress-test the leading hypothesis adversarially: `/think-scrutinize`
- If a critical observation comes in: re-run the matrix on the new evidence
```

### 11. No Iteration

This skill is one-shot. ACH analyses are fragile to silently-changing inputs — if the question, hypothesis set, or evidence set changes, **re-invoke** with the updated inputs. Each invocation is a clean consultation.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Disconfirmation is the rank principle.** The leaderboard is ordered by least-inconsistent, not most-consistent. This is non-negotiable; the technique loses its anti-confirmation-bias property if you flip it.
- **Independent cell evaluation.** When building the matrix, evaluate each cell on its own merits without letting prior cells anchor.
- **Isolated generation.** Hypothesizers and evidence-gatherers do not see each other's output during their phases.
- **Calibrated qualitative confidence.** No fabricated percentages. *High / moderate / low / uncertain* only.
- **Preserve alternatives.** The 2nd-place and lower hypotheses are not "wrong" — they are "currently disconfirmed less than possible new evidence might change."
- **Honest "evidence didn't apply"** is allowed and valuable — N/A is a meaningful matrix entry.

## When to Use

**Good fit:**

- The user has 3-7+ competing hypotheses and wants rigorous narrowing
- A causal investigation has surfaced multiple candidate causes; rigorous discrimination is needed
- An attribution question (who did X? what's responsible for Y?) with multiple actors / mechanisms
- A forecasting question with multiple competing scenarios and evidence available
- An intelligence-style question where confirmation bias is a known risk
- After `/think-diagnose` has generated candidates and the user wants formal narrowing

**Poor fit:**

- Only 1-2 hypotheses (use `/think-scrutinize` to stress-test the leading one)
- Hypotheses too vague or non-mutually-exclusive (refine them first via `/think-reframe`)
- Insufficient evidence to discriminate (narrow the question, or accept that the analysis can only weakly distinguish)
- The user wants to *generate* hypotheses (use `/think-diagnose` for causes or `/think-brainstorm` for options first)
- Decisions among options (use `/think-deliberate` — option selection is structured differently from hypothesis selection)

**Rule of thumb:**

- "Which of these competing hypotheses is most likely correct?" → `/think-ach`
- "What could be causing this phenomenon?" → `/think-diagnose`
- "Which option should I pick?" → `/think-deliberate`
- "What's wrong with this idea?" → `/think-scrutinize`

## Relationship to Other Skills

| Skill                | Relationship                                                                                              |
|----------------------|-----------------------------------------------------------------------------------------------------------|
| `/think-diagnose`    | Natural upstream — generates candidate causes that ACH then rigorously narrows                            |
| `/think-brainstorm`  | Natural upstream — when ACH operates on candidate options/scenarios rather than causes                    |
| `/think-scrutinize`  | Natural downstream — adversarially stress-test the leading hypothesis                                     |
| `/think-deliberate`  | Adjacent — operates on options-to-pick rather than hypotheses-to-narrow; different cognitive mode         |
| `/think-reframe`     | Upstream when hypotheses are too vague or non-mutually-exclusive                                          |
| `/think-premortem`   | Adjacent — both deal with hypothetical states, but premortem imagines failures while ACH evaluates competing real-world hypotheses |

**ACH and diagnose compared (important).** Diagnose is open-ended causal exploration via lens-driven brainstorming + narrative evidence assessment. ACH is rigorous narrowing via explicit matrix + disconfirmation focus. They have different cognitive modes:

- *Diagnose:* generative + evaluative, lens-driven, narrative
- *ACH:* primarily evaluative, matrix-driven, disconfirmation-focused

Use diagnose when "what could be happening?" Use ACH when "given these candidate hypotheses, which survives the evidence?" The two compose well: diagnose generates, ACH narrows.

**ACH and scrutinize compared.** Scrutinize stress-tests *one* idea adversarially. ACH narrows among *many* hypotheses systematically. ACH is breadth (many hypotheses, structured discrimination); scrutinize is depth (one hypothesis, adversarial dialectic). Natural ordering: ACH narrows to the leader, scrutinize stress-tests the leader.

## Philosophy

The default mode of reasoning under uncertainty is to find a hypothesis that fits the evidence and stop. This produces the well-known failure modes ACH was designed to counter: confirmation bias (we seek what fits), premature closure (we lock in too early), anchoring (the first hypothesis dominates), cherry-picking (convenient evidence wins).

Heuer's insight is that these failures share a common root: *we ask the wrong question.* "Does this evidence fit my hypothesis?" invites confirmation; "Does this evidence disconfirm my hypothesis?" invites honesty. The matrix structure forces the second question for every cell, against every hypothesis, in every direction — and the disconfirmation-focused ranking ensures that the answer cannot be ignored.

ACH operationalizes Karl Popper's falsification principle for everyday reasoning: hypotheses cannot be proven, only failed-to-be-disproven. The surviving hypothesis is the one that has been hardest to kill.

This plugin's `/think-*` namespace formalizes the disciplines that humans habitually skip. ACH is the discipline against confirmation bias when many hypotheses are in play. The matrix is the discipline; the disconfirmation focus is the principle; the diagnosticity and sensitivity steps are the rigor; the falsification milestones are the calibration to future evidence. Together they form one of the strongest cognitive countermeasures available — not because the technique is sophisticated, but because the structural commitments are unskippable.
