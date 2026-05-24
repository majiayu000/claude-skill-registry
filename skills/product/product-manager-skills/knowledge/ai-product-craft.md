# AI Product Craft

Compressed decision logic for AI product managers: readiness assessment, context architecture, orchestration patterns, and validation methodology. Derived from ai-shaped-readiness-advisor, context-engineering-advisor, and pol-probe-advisor.

---

## AI-Shaped Readiness

### AI-First vs. AI-Shaped

| Dimension | AI-First (table stakes) | AI-Shaped (defensible) |
|-----------|------------------------|------------------------|
| Mindset | Automate existing tasks | Redesign how work gets done |
| Goal | Speed up artifact creation | Compress learning cycles |
| AI Role | Task assistant | Strategic co-intelligence |
| Test | Competitor replicates by adding headcount | Competitor must redesign entire org |

### The 5 Competencies

**1. Context Design** — Build a durable "reality layer" humans and AI both trust. Treat AI attention as scarce. Persist constraints + glossary; retrieve everything else on demand. Foundational: blocks all other competencies if missing.

**2. Agent Orchestration** — Repeatable, traceable AI workflows (research -> synthesis -> critique -> decision -> log rationale). Version-controlled prompts. Each step shows its work. One-off prompts are tactical; orchestrated workflows are strategic.

**3. Outcome Acceleration** — Compress learning cycles, not just task speed. Eliminate validation lag (PoL probes in days, not weeks). Remove approval delays (AI pre-validates against constraints). Cut meeting overhead (async AI synthesis).

**4. Team-AI Facilitation** — AI operates as co-intelligence, not accountability shield. Review norms (AI outputs = drafts). Evidence standards (cite sources, reject "I think"). Decision authority (AI recommends, humans decide). Psychological safety to challenge AI.

**5. Strategic Differentiation** — New customer capabilities competitors can't replicate by throwing bodies at it. Workflow rewiring requiring full org redesign to copy. Economics competitors can't match (10x cost advantage through AI).

### Maturity Levels (per competency)

- **Level 1 — AI-First:** One-off prompts, no structure, efficiency only
- **Level 2 — Emerging:** Some saved prompts/templates, scattered docs, modest gains
- **Level 3 — Transitioning:** Multi-step workflows, structured context, learning cycles compressing
- **Level 4 — AI-Shaped:** Autonomous orchestrated workflows, durable reality layer, defensible moat

### Priority Dependency Chain

```
Context Design (foundation)
  └─> Agent Orchestration (requires context)
        └─> Outcome Acceleration (requires orchestration)
              └─> Strategic Differentiation (requires all above)
Team-AI Facilitation ──── (parallel track, required for scale)
```

If Context Design is Level 1-2, fix it first. Everything else is fragile without it.

---

## Context Engineering

### Context Stuffing vs. Context Engineering

| Dimension | Stuffing | Engineering |
|-----------|----------|-------------|
| Mindset | Volume = quality | Structure = quality |
| Approach | "Add everything just in case" | "What decision am I making?" |
| Persistence | Persist all context | Retrieve with intent |
| Agent chains | Share everything between agents | Bounded context per agent |
| Failure response | Retry until it works | Fix the structure |
| Economic model | Context as storage | Context as attention (scarce) |

**Why stuffing fails:** Accuracy degrades significantly as context grows — models prioritize beginning and end, ignore the middle (Liu et al. 2023, "Lost in the Middle"). Dead ends and errors accumulate (context rot). Retries become normalized.

### 5 Diagnostic Questions

1. **What specific decision does this support?** Can't answer = don't need it.
2. **Can retrieval replace persistence?** Just-in-time beats always-available.
3. **Who owns the context boundary?** No owner = unbounded growth.
4. **What fails if we exclude this?** No concrete failure = delete it.
5. **Are we fixing structure or avoiding it?** Stuffing often masks bad info architecture.

### Persist vs. Retrieve Rule

- **Persist (80%+ of interactions):** Core constraints, user preferences, operational glossary, non-negotiable rules
- **Retrieve (<20% of interactions):** Project details, historical PRDs, competitive analysis, past transcripts
- **Gray zone (20-80%):** Weigh retrieval latency vs. context window cost

### Two-Layer Memory Architecture

**Short-term (conversational):** Immediate interaction history. Single session. Summarize/truncate older parts.

**Long-term (persistent):** Constraints registry + operational glossary + user preferences. Vector database for semantic retrieval. Two subtypes:
- Declarative: facts ("We follow HIPAA")
- Procedural: patterns ("Always validate feasibility before usability")

### Research -> Plan -> Reset -> Implement Cycle

The core context rot prevention pattern:

1. **Research:** Agent gathers data. Context grows large and messy. Expected.
2. **Plan:** Synthesize into high-density SPEC.md/PLAN.md (source of truth).
3. **Reset:** Clear entire context window. Non-negotiable.
4. **Implement:** Fresh session with only the plan as context.

**Why it works:** Eliminates context rot, dead ends, and goal drift. Agent starts clean with compressed, high-signal context.

### Efficiency Formula

```
Context Efficiency = (Accuracy x Coherence) / (Tokens x Latency)
```

Key finding: RAG with 25% of available tokens preserves 95% accuracy while cutting latency and cost.

### Context Manifest Template

```
Always Persisted:  constraints (technical, regulatory), user prefs, glossary
Retrieved On-Demand: historical PRDs, transcripts, competitive analysis
Excluded:          meeting notes >30 days, full codebase, marketing materials
Boundary Owner:    [Name]
Next Review:       [Date + 90 days]
```

---

## Agent Orchestration

### Core Workflow Pattern

```
Research -> Synthesis -> Critique -> Decision -> Log Rationale
```

Each step must be: traceable (cites sources), bounded (own context window), version-controlled (prompts in Git), consistent (same inputs -> predictable process).

### Maturity Progression

1. **Ad-hoc prompts:** Type into ChatGPT as needed. No reuse.
2. **Saved templates:** Reusable prompts, custom GPTs/Claude Projects. Manual steps.
3. **Multi-step workflows:** Research -> synthesis -> critique. Manual handoffs between steps.
4. **Autonomous orchestration:** Runs end-to-end. Traceable. Version-controlled. Auditable.

### Bounded Context per Agent

Anti-pattern: Agent A passes everything to Agent B to Agent C (context window explodes to 100k+).

Fix: Each agent outputs a bounded synthesis (2-page max) to the next agent. Apply Research->Plan->Reset->Implement between agent handoffs.

### Building Your First Orchestrated Workflow

1. Pick most frequent AI use case
2. Document every step you currently take manually
3. Design loop: research -> synthesis -> critique -> decision -> log
4. Implement (Claude Projects for simple; API orchestration for complex)
5. Run on 3 past examples; compare to manual process
6. Version-control prompts; train 2 teammates; iterate

---

## AI Validation (PoL Probes)

### The 5 Probe Types

| Probe | Core Question | Timeline | AI-Specific Use |
|-------|---------------|----------|-----------------|
| **Feasibility Check** | Can we build this? | 1-2 days | GenAI prompt chains, API sniff tests, data integrity sweeps |
| **Task-Focused Test** | Can users complete this without friction? | 2-5 days | Test AI-generated UIs, chatbot flows, recommendation quality |
| **Narrative Prototype** | Does this earn buy-in? | 1-3 days | Explain AI capabilities to stakeholders via Loom/video |
| **Synthetic Data Simulation** | Can we model without production risk? | 2-4 days | Test prompt logic, simulate edge cases, Monte Carlo on AI outputs |
| **Vibe-Coded Probe** | Will this survive real user contact? | 2-3 days | Frankensoft stack (ChatGPT Canvas + Replit + Airtable) for workflow validation |

### Selection Logic

Work backwards from hypothesis:
1. What specific risk am I eliminating?
2. What's the cheapest path to harsh truth?
3. Match method to hypothesis, not tooling comfort.

**Golden rule:** Use the cheapest prototype that tells the harshest truth.

### AI-Specific Feasibility Checks

For AI product features, feasibility checks are critical because AI capabilities are non-obvious:
- **Prompt chain testing:** Run 100 real examples through your proposed prompt. Measure error rate.
- **API sniff tests:** Verify third-party AI integrations return expected format, latency, cost.
- **Data integrity sweeps:** Check if your data supports the AI feature (quality, volume, format).
- **Disposal protocol:** Delete all spike code after documenting findings. Spike-and-delete, not spike-and-ship.

### Success Criteria Template

- **Pass:** [Quantitative threshold, e.g., <5% error rate, 80%+ task completion]
- **Fail:** [Observable failure, e.g., >18% errors, users abandon mid-flow]
- **Learn:** [Specific insight regardless of pass/fail]

Write criteria before building. "We'll know it when we see it" is not a success criterion.

### Troubleshooting Common AI Product Issues

**Hallucination (output contains fabricated facts):**
1. Measure: run 100+ real queries, categorize errors (factual, format, reasoning, refusal)
2. Reduce context window — strip to minimum required tokens per the 5 diagnostic questions above
3. Add retrieval with source citations — ground answers in specific documents, not parametric memory
4. Add output validation — regex/rule checks for structured fields, LLM-as-judge for open text
5. Set confidence thresholds — if model confidence is low, return "I don't know" instead of guessing

**Latency (AI response too slow for UX):**
1. Profile the pipeline — which step is slow? (retrieval, inference, post-processing)
2. Reduce input tokens — smaller context = faster inference. Apply persist vs. retrieve rule.
3. Use streaming — display partial results as they generate
4. Cache common queries — if 30% of queries are similar, pre-compute answers
5. Consider smaller model for simple tasks — route easy queries to fast model, hard queries to capable model

**Inconsistency (same input, different outputs):**
1. Lower temperature — 0.0-0.3 for factual tasks, 0.5-0.7 for creative tasks
2. Pin model version — don't use "latest" in production
3. Structured output — JSON schema or enum constraints reduce variation
4. Add few-shot examples — 2-3 input/output pairs anchor the response pattern
5. Evaluate on a fixed test set — track consistency score across versions

---

## Quality Gates

### AI Product Anti-Patterns

**1. Prompt-and-Pray**
Shipping AI features with untested prompts. No evaluation framework, no error rate measurement. Fix: Run feasibility checks (100+ examples) before committing to build.

**2. Context Stuffing at Scale**
Pasting entire knowledge bases into AI. "More tokens = better results." Fix: Apply the 5 diagnostic questions. Accuracy degrades significantly as context grows (Lost in the Middle effect).

**3. No Evals**
Launching AI features without quantitative success criteria. "Users seem to like it." Fix: Define pass/fail thresholds before building. Measure error rates, task completion, hallucination frequency.

**4. Efficiency Masquerading as Strategy**
"We use AI to write PRDs 2x faster — we're AI-shaped!" If a competitor matches it by hiring 2 more people, it's table stakes. Fix: Ask the replication test — does copying require org redesign?

**5. Tool Fetishism**
"Should we use Claude or ChatGPT?" Tool debates replace workflow redesign. Fix: Tools don't matter. Workflows matter.

**6. Speed Without Learning**
Shipping faster without validating faster. AI accelerates building the wrong thing. Fix: Compress learning cycles (PoL probes in days), not just build cycles.

**7. Prototype Theater**
Building polished demos to impress executives instead of testing hypotheses with users. Fix: Test with users first, present findings to executives. Narrative prototypes over production polish.

**8. Skipping the Reset**
Never clearing context between research and implementation. Context rot poisons execution. Fix: Mandatory reset after plan synthesis. Start implementation with only the high-density plan.

**9. Individual AI, Not Team AI**
"I'm AI-shaped, but my team isn't." Can't scale; workflows die when you're on vacation. Fix: Codify review norms, evidence standards, decision authority. Team transformation > individual productivity.

**10. Testing Multiple Variables**
One probe testing workflow + pricing + UI simultaneously. Ambiguous results. Fix: One probe, one hypothesis. Three hypotheses = three probes.

### The Falsification Protocol

For every AI feature decision, complete:
> "If I exclude [context/feature/test], then [specific failure] will occur in [specific scenario]."

If you can't complete the sentence, you don't need it. Vague failures ("AI might not fully understand") are not valid.

### Minimum Viable AI Product Checklist

- [ ] Hypothesis written before building
- [ ] Feasibility check run (100+ examples, error rate measured)
- [ ] Context architecture defined (persist vs. retrieve vs. exclude)
- [ ] Success criteria quantified (pass/fail/learn thresholds)
- [ ] Disposal date set for probes (spike-and-delete)
- [ ] Context boundary owner assigned
- [ ] AI outputs treated as drafts (human review protocol)
- [ ] Learning cycle measured (before vs. after AI intervention)

---

## Interaction Rules (Coaching Mode)

When coaching is active for AI product topics, use these rules.

| Trigger | Action | Stop When |
|---------|--------|-----------|
| User wants to add AI without stating the user problem | Push: "What does the user do today without AI, and what's painful about it? AI is the how, not the why." | User describes the non-AI workflow and the pain point |
| No validation plan for AI feature accuracy | Challenge: "How will you know if the AI output is good enough? Define your error rate threshold and how you'll measure it." | User defines pass/fail criteria with numbers |
| Context architecture is undefined ("just send everything to the LLM") | Push: "What context does the model actually need? What's noise? Context stuffing is the #1 cost and quality killer." | User identifies what to include, exclude, and retrieve |
| User treats AI output as final (no human review step) | Challenge: "What happens when the AI is wrong? Who catches it, and what do they see?" | User describes the human review loop |
| Agent orchestration has no fallback for failure | Push: "What happens when step 3 of your agent pipeline fails? Does the user wait forever, get a partial result, or see an error?" | User defines the failure mode for each step |
| User has answered 2 follow-ups on the same point | Stop pushing. Summarize what's still weak and give best-guess output. | -- |
