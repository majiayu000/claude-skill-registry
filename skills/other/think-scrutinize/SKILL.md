---
name: think-scrutinize
description: Good-faith adversarial scrutiny of an idea or plan. Spawns critical skeptics across relevant lenses, pairs them with an advocate defending the idea, and synthesizes the exchange into a report. Produces feedback only — no code, no tickets, no artifacts.
model: opus
---

# Think-Scrutinize - Devil's Advocate for Ideas

Scrutinizes an idea or plan to identify its faults before implementation. Uses the same adversarial pattern as `/think-deliberate`, but pointed inward at a single idea instead of outward across competing options: skeptics critique, an advocate defends, skeptics counter-rebut, orchestrator synthesizes.

**This skill produces no tangible artifacts.** It is a consultant, not an implementer. No code, no tickets, no commits. The output is a structured report of findings that survived adversarial testing.

## Roles

**Judge (you, running this skill):**
- Capture the idea in a written brief
- Choose appropriate critical lenses
- Spawn skeptics and the advocate
- Synthesize the exchange into the final report

**Skeptics:** Each receives a specific lens (technical, economic, operational, etc.) and critiques the idea in good faith through that lens.

**Advocate:** Defends the idea against the consolidated critique — concedes genuine faults, refutes weak ones.

## Workflow

### 1. Receive the Idea

The idea may arrive as:
- **Conversation context** — summarize it back to the user, confirm accuracy
- **A document** — read the file (design doc, ticket, plan)
- **Fresh user input** — capture it verbatim

**Produce a written brief** of the idea as you understand it. Skeptics and the advocate critique and defend this brief. Ambiguity here corrupts everything downstream.

### 2. Fact-Finding

Probe for the context skeptics will need:
- **Goal** — what problem does this solve? What's the success criterion?
- **Constraints** — budget, timeline, technical, organizational, regulatory
- **Prior attempts** — what's been tried? What's been ruled out?
- **Stakeholders** — who's affected? Whose buy-in matters?
- **Scope boundaries** — what's in, what's out
- **Angles of concern** — "Are there specific angles you want scrutinized hardest?"

**3-5 clarifying questions is typical.** More suggests the idea isn't ready for scrutiny yet.

### 3. Choose Critical Lenses

Select lenses that fit the idea's domain. The number is a judgment call — there is no fixed count.

**Common lenses:**
- **Technical** — scalability, reliability, complexity
- **Economic** — cost/benefit, ROI, opportunity cost
- **Operational** — maintenance, support, on-call burden
- **Adversarial-user** — misuse, exploitation, circumvention
- **Security/trust** — attack surface, privacy, data handling
- **Regulatory/legal** — compliance, licensing, contractual risk
- **Social/organizational** — adoption, political risk, cultural fit
- **Temporal** — does this hold up in 6 months? 2 years?

**Guidelines:**
- Choose lenses where the idea plausibly has weaknesses
- Skip lenses that don't apply (e.g., regulatory for a personal script)
- 2-5 lenses is typical; more only for broad ideas
- Include any angles the user nominated in step 2

### 4. Spawn Skeptics (Parallel)

Spawn one `THK - Skeptic` agent per lens, in parallel. Each receives:
- The written idea brief (from step 1)
- Its assigned lens and what the lens means in this context
- Relevant fact-finding context
- The structured output format

Collect all critiques.

### 5. Consolidate Critiques

Merge findings into a single brief:
- Deduplicate overlapping findings (same fault seen by multiple lenses)
- Preserve lens attribution (which skeptic raised what)
- Keep severity labels honest — don't downgrade to look kind

### 6. Spawn Advocate

Spawn a `THK - Advocate` agent with:
- The idea brief
- The consolidated critique
- Mandate: **defend the idea in good faith**. This is not a competition against other options — there is one idea on the table. Concede genuine faults; refute weak critiques.

The advocate returns a rebuttal per finding.

### 7. Counter-Rebuttal (Parallel)

Each skeptic sees the advocate's rebuttals to *its own* findings and responds per finding:
- **Concede** — rebuttal is sound; the fault was weak or wrong
- **Hold** — rebuttal missed the point; the fault stands
- **Refine** — rebuttal was partly right; narrow the fault to what still applies

Skeptics run in parallel.

### 8. Synthesize and Report

For each finding, verdict is one of:
- **Stands** — skeptic held; rebuttal didn't resolve it
- **Refuted** — skeptic conceded, or rebuttal clearly resolved it
- **Partial** — skeptic refined; narrowed concern remains
- **Uncertain** — both sides have a point; user judgment needed

**Final report format:**

```
## Scrutinization Report

**Idea:** [one-line summary]
**Lenses applied:** [list]

### Findings That Stand
[Fatal flaws and serious concerns that survived rebuttal]

### Load-Bearing Assumptions to Validate
[Assumptions the idea depends on — user should verify]

### Partial / Uncertain
[Findings where rebuttal narrowed but didn't eliminate]

### Findings That Were Refuted
[Brief — for completeness. Shows the exchange was not one-sided.]

### Strengths
[Where the idea held up across lenses]

### Recommendation
One of:
- **Proceed** — no material faults; idea is robust
- **Proceed with adjustments** — address standing findings, then proceed
- **Rethink** — standing findings suggest substantive revision
- **Reject** — fatal flaws are unaddressable within the current framing
```

### 9. No Iteration

This skill is one-shot. If the user refines the idea based on the report, they **re-invoke** `/think-scrutinize` with the revised version. Each invocation is a clean consultation — not an open-ended dialog.

## Constraints

- **No artifacts.** No code, tickets, commits, or documents.
- **Good faith on both sides.** No strawmen, no exaggeration.
- **Lens focus.** Each skeptic stays within its assigned angle.
- **Honest "no faults found"** is a valid, valuable outcome.

## When to Use

**Good fit:**
- Reviewing a plan or design before committing to implementation
- Pressure-testing a proposal before presenting it to stakeholders
- Surfacing objections that politeness or groupthink would suppress
- Pre-mortem analysis — "what could make this fail?"

**Poor fit:**
- Choosing between options → use `/think-deliberate`
- Finding bugs in existing code → use `/bug-hunt` or `/review-security`
- Implementing changes → this skill makes nothing; follow up with `/implement`, `/refactor`, etc.
- Vague dissatisfaction with a plan that has no concrete form yet

## Philosophy

The skill exists to make ideas stronger. A good skeptic finds the faults that matter, not the most faults. A good advocate defends honestly, not desperately. The user gets the truth that emerges from their collision.

Charlie Munger, borrowing from Jacobi: **"Invert, always invert."** Before committing to an idea, understand how it could fail. `/think-scrutinize` formalizes that instinct — not as unstructured doubt, but as adversarial stress-testing with honest synthesis.
