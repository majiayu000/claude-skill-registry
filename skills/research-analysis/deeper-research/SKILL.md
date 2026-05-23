---
name: deeper-research
description: Comprehensive 6-phase research funnel — 8-10 parallel survey agents sweep wide, a synthesizer compiles evidence, deep-dive and adversarial agents run in parallel to elaborate and challenge findings, a final synthesizer reconciles everything, and an integrator maps verified findings to a concrete codebase plan with full traceability
---

# Deeper Research

A six-phase evidence-gathering funnel for problems where the cost of a wrong
design exceeds the cost of thorough research. Doubles the agent count of
`/deep-research` (21-23 agents vs 7), approaches the problem from 8-10
independent lenses, and adds adversarial review to challenge conclusions before
they reach the implementation plan.

The funnel narrows progressively: a wide initial survey generates raw findings,
synthesis distills them, parallel deep-dives and adversarial challenges stress-
test the synthesis from both directions, a final synthesis reconciles all
streams, and an integrator grounds everything in the codebase with full
traceability from finding IDs to implementation steps.

## When to Use

- **Highest-stakes design decisions**: foundational architecture, core data
  structures, protocols that are impossible to change later
- **Novel or unfamiliar territory at scale**: combining multiple research
  domains where cross-pollination matters
- **When `/deep-research` isn't enough**: you need adversarial challenge of
  findings, deeper dives into gaps, and full traceability
- **Safety-critical + performance-critical intersection**: where you need both
  theoretical correctness AND production evidence
- **When the problem is worth 21+ agent invocations**: this is expensive by
  design

## When NOT to Use

- Use `/deep-research` for standard research tasks (7 agents, 3 phases)
- Use `/design-tournament` when the problem is understood and you need to
  explore implementation approaches
- Straightforward features or well-understood domains
- Problems with clear single solutions

## Invocation

```
/deeper-research <problem statement>
/deeper-research --lenses=10 <problem>        # Full 10 lenses (default: 8)
/deeper-research --lenses=5 <problem>         # Minimal (5 core lenses)
/deeper-research --no-adversarial <problem>   # Skip Phase 4
/deeper-research --skip-deep-dive <problem>   # Skip Phase 3
```

If no argument is given, ask the user for the problem statement before
proceeding.

## Architecture

```
Orchestrator: Problem Decomposition (inline, produces Research Brief)
      |
Phase 1: Wide Survey (8-10 parallel agents)
      |
Phase 2: First Synthesis (1 agent)
      |
      +--- Phase 3: Deep-Dives (3-5 parallel) ---+
      |                                            |  <- run in parallel
      +--- Phase 4: Adversarial (4 parallel)  ----+
      |                                            |
      +--------------------------------------------+
      |
Phase 5: Final Synthesis (1 agent)
      |
Phase 6: Integration (1 agent)
```

**Key structural decision**: Phase 3 and Phase 4 run in parallel in a single
message. This saves a serial step and creates an information firewall —
adversarial agents challenge Phase 2's conclusions independently of Phase 3's
elaborations, preventing anchoring bias.

### Finding ID Scheme (Traceability)

Every finding gets a traceable ID used through all subsequent phases:

```
P1.{agent#}.F{n}  — Phase 1, Agent 4, Finding 3 -> P1.4.F3
S1.F{n}           — First Synthesis findings
P3.{agent#}.F{n}  — Deep-dive findings
P4.{agent#}.F{n}  — Adversarial findings
S2.F{n}           — Final Synthesis findings
```

Every step in Phase 6's implementation plan cites these IDs.

### Output Budgets Per Phase

| Phase | Agents | Max Per Agent | Total to Next Phase |
|-------|--------|---------------|---------------------|
| 1     | 8-10   | ~3000 tokens  | ~24-30k -> Phase 2  |
| 2     | 1      | ~6000 tokens  | 6k -> Phases 3, 4, 5 |
| 3     | 3-5    | ~4000 tokens  | ~12-20k -> Phase 5  |
| 4     | 4      | ~2500 tokens  | ~10k -> Phase 5     |
| 5     | 1      | ~8000 tokens  | 8k -> Phase 6       |
| 6     | 1      | unconstrained | final output        |

### Evidence Strength Scale

Used by ALL agents across all phases.

| Level | Label | Description | Example |
|-------|-------|-------------|---------|
| 5 | **Proven at scale** | Battle-tested in production systems handling similar workloads | FoundationDB's simulation testing, TigerBeetle's storage engine |
| 4 | **Peer-reviewed** | Published in reputable venue with formal analysis | OSDI/SOSP paper with proofs |
| 3 | **Implemented & tested** | Open-source implementation with benchmarks/tests | Well-maintained crate with >1k stars, comprehensive test suite |
| 2 | **Documented practice** | Technical blog from credible engineering org | Blog post from Cloudflare, Datadog, AWS engineering |
| 1 | **Anecdotal** | Forum discussion, personal blog, Stack Overflow answer | Useful for leads but needs corroboration |

---

## Orchestrator: Problem Decomposition (Inline)

Before launching Phase 1, the orchestrator (you) produces a **Structured
Research Brief**. This is NOT a separate agent — do this inline.

### Steps

1. **Parse the problem statement** and identify:
   - Core sub-problems (2-5 distinct questions to answer)
   - Key search terms and domain-specific vocabulary
   - Constraints from the problem statement

2. **Quick codebase scan**: Use Glob, Grep, and Read to gather:
   - Relevant file paths and module structure
   - Existing patterns and conventions
   - Current approach (if any) to the problem
   - Dependencies and their versions

3. **Select lenses**: Based on the problem, select which of the 10 research
   lenses are active (default: 8 core lenses; with `--lenses=10` add the two
   optional lenses; with `--lenses=5` use lenses 1-5 only).

4. **Produce the Research Brief** in this format:

```markdown
## Research Brief

### Problem Statement
{user's problem, restated for clarity}

### Sub-Problems
1. {sub-problem 1}
2. {sub-problem 2}
...

### Key Search Terms
- {term 1}: {why it matters}
- {term 2}: {why it matters}
...

### Codebase Context
- {file path}: {what it contains and why it's relevant}
...

### Active Lenses
{numbered list of selected lenses with brief rationale for optional ones}

### Constraints
- {constraint from problem or codebase}
...
```

Include this Research Brief in every Phase 1 agent's prompt.

---

## Phase 1 — Wide Survey (8-10 Parallel Agents)

Launch all selected research agents **in a single message** using the Task tool
with `subagent_type=general-purpose`. Each agent has a distinct research lens
but receives the same problem statement and Research Brief.

### 10 Research Lenses

**Core 8 (always active unless `--lenses=5`):**

1. Foundational Theory & Algorithms
2. Production Systems & Battle-Tested Implementations
3. Failure Modes, Post-Mortems & Anti-Patterns
4. Rust Ecosystem & Implementation Patterns
5. Industry Practice & System Architecture
6. Formal Verification & Correctness
7. Performance Engineering & Measurement
8. Testing & Validation Strategies

**Optional 2 (active with `--lenses=10`, orchestrator selects based on problem):**

9. Adjacent Domains & Cross-Pollination
10. API & Interface Design

**Minimal 5 (with `--lenses=5`):** Lenses 1-5 only (matches `/deep-research`).

### Common Preamble (included in every Phase 1 agent's prompt)

```
You are Research Agent {AGENT_ID} — a {SPECIALTY} specialist conducting Phase 1
of a comprehensive research funnel.

## Problem Under Investigation
{PROBLEM}

## Research Brief
{RESEARCH_BRIEF}

## Your Research Mission

You are one of {N} independent research agents. Your job is to gather HARD
EVIDENCE — not opinions — about how this problem has been solved before.
Every claim must have a source. Unsourced claims are worthless.

### Research Process

1. **Understand the codebase context**: Use Glob, Grep, and Read to understand
   the relevant parts of the codebase. The Research Brief gives you starting
   points — explore from there.

2. **Search for external evidence**: Use WebSearch and WebFetch to find:
   - Academic papers and technical reports
   - Documentation from production systems that solve similar problems
   - RFCs, specifications, and formal descriptions
   - Post-mortems and failure analyses
   - Conference talks, technical blog posts from credible sources
   - Existing open-source implementations

3. **Evaluate and document**: For each piece of evidence, record:
   - Source (URL, paper title, system name)
   - Key finding or technique
   - Relevance to our specific problem
   - Evidence strength (see scale below)

### Evidence Strength Scale

| Level | Label | Description |
|-------|-------|-------------|
| 5 | Proven at scale | Battle-tested in production at similar workloads |
| 4 | Peer-reviewed | Published in reputable venue with formal analysis |
| 3 | Implemented & tested | Open-source with benchmarks/tests |
| 2 | Documented practice | Tech blog from credible org |
| 1 | Anecdotal | Forum/blog, needs corroboration |

### Focus Area
{FOCUS}

### Rules

- EVERY finding must have a concrete source. No source = don't include it.
- Prefer primary sources over secondary summaries.
- If you find contradictory evidence, report BOTH sides with sources.
- Distinguish between "X is theoretically optimal" and "X works in production."
- Note when evidence is from a different domain and may not transfer directly.
- Search for COUNTER-evidence too — what are the failure modes?
- If a search returns no useful results, say so. Do not fabricate references.
- Stay within your budget: aim for ~3000 tokens of output.

### Output Format

Return a markdown document starting with:
`# P1 Research — Agent {AGENT_ID}: {SPECIALTY}`

Then these sections:

#### 1. Codebase Context
What you found in the current codebase that's relevant. File paths and line
numbers for key structures.

#### 2. Findings
For each piece of evidence (aim for 5-12 findings):

**P1.{AGENT_ID}.F{N}: {title}**
- **Source**: {URL or citation}
- **Evidence strength**: {1-5} — {label}
- **Summary**: {2-4 sentences}
- **Key technique/insight**: {the actionable takeaway}
- **Applicability**: {high/medium/low} — {why}
- **Caveats**: {limitations, different assumptions}

#### 3. Patterns & Consensus
What approaches appear repeatedly across your sources? Where do experts agree?

#### 4. Disagreements & Open Questions
Where do sources contradict each other? What remains unresolved?

#### 5. Recommended Reading
Top 3-5 sources the team should read, ranked by relevance.
```

---

### Agent Focus Areas

#### Agent 1 — Foundational Theory & Algorithms

```
{SPECIALTY}: Foundational Theory & Algorithms
{AGENT_ID}: 1
{FOCUS}:
Search for the THEORETICAL foundations of this problem:
- Seminal papers and algorithms (Lamport, Dijkstra, Knuth, etc.)
- Formal correctness proofs or verification approaches
- Complexity bounds — what's provably optimal?
- Mathematical models and invariants
- Type-theoretic or formal methods approaches

Start with WebSearch queries like:
- "{problem keywords} algorithm formal proof"
- "{problem keywords} paper OSDI SOSP VLDB SIGMOD"
- "{problem keywords} correctness verification"
- "{problem keywords} complexity bounds"

Look at: arxiv.org, dl.acm.org, usenix.org proceedings, PhD theses, textbooks
```

---

#### Agent 2 — Production Systems & Battle-Tested Implementations

```
{SPECIALTY}: Production Systems & Battle-Tested Implementations
{AGENT_ID}: 2
{FOCUS}:
Search for how REAL SYSTEMS in production solve this problem:
- Database engines (FoundationDB, TigerBeetle, CockroachDB, SQLite, DuckDB)
- Storage systems (RocksDB, LevelDB, WiscKey)
- Distributed systems (etcd, Raft implementations, Paxos variants)
- High-performance systems (DPDK, SPDK, io_uring users)
- Language runtimes (Go GC, Rust allocators, JVM internals)
- Operating systems (Linux kernel, FreeBSD, Fuchsia)

For each system found:
- What approach do they use?
- What scale does it operate at?
- What trade-offs did they make and why?
- Link to source code or design docs when available.
```

---

#### Agent 3 — Failure Modes, Post-Mortems & Anti-Patterns

```
{SPECIALTY}: Failure Modes, Post-Mortems & Anti-Patterns
{AGENT_ID}: 3
{FOCUS}:
Search for how this problem GOES WRONG:
- Post-mortems from outages caused by similar systems
- CVEs and security advisories in related implementations
- Known anti-patterns and common mistakes
- Performance cliffs and degenerate cases
- Subtle bugs found in production (Jepsen reports, fuzzing results)
- Memory safety issues in similar C/C++/Rust implementations

For each failure found:
- What went wrong?
- Root cause analysis
- How was it detected?
- How was it fixed or mitigated?
- What invariant was violated?
```

---

#### Agent 4 — Rust Ecosystem & Implementation Patterns

```
{SPECIALTY}: Rust Ecosystem & Implementation Patterns
{AGENT_ID}: 4
{FOCUS}:
Search for how this problem is solved IN RUST specifically:
- Existing crates that address this problem (crates.io, lib.rs)
- Rust-specific patterns (ownership for safety, typestate, const generics)
- Unsafe code patterns and safety proofs in similar Rust projects
- Benchmarks comparing Rust implementations
- Rust RFCs and compiler internals if relevant

For each crate or pattern found:
- API design — how is it exposed to users?
- Safety story — how is unsafe (if any) encapsulated?
- Performance characteristics — any benchmarks?
- Maintenance status — actively maintained? Production users?
- Code quality — tests, docs, CI, fuzzing?

Also check the Rust standard library and popular foundational crates
(crossbeam, tokio, rayon, parking_lot, etc.) for relevant patterns.
```

---

#### Agent 5 — Industry Practice & System Architecture

```
{SPECIALTY}: Industry Practice & System Architecture
{AGENT_ID}: 5
{FOCUS}:
Search for how ENGINEERING ORGANIZATIONS approach this problem:
- Technical blog posts from major engineering orgs (Google, Meta, AWS,
  Cloudflare, Datadog, Discord, Figma, Fly.io)
- Conference talks (Strange Loop, RustConf, P99 CONF, QCon)
- Architecture Decision Records (ADRs) in open-source projects
- RFCs and design documents from relevant projects
- Books and practitioner guides

For each practice found:
- What organization or project uses this approach?
- At what scale?
- What alternatives did they evaluate?
- What would they do differently in hindsight?
- Is this approach specific to their constraints or generalizable?
```

---

#### Agent 6 — Formal Verification & Correctness

```
{SPECIALTY}: Formal Verification & Correctness
{AGENT_ID}: 6
{FOCUS}:
Search for FORMAL APPROACHES to verifying this problem's correctness:
- TLA+ specifications for similar protocols/algorithms
- Model checking results (SPIN, Alloy, CBMC)
- Rust-specific verification tools (Kani, MIRI, Prusti, Creusot)
- Property-based testing strategies that catch classes of bugs
- Linearizability proofs, refinement proofs
- Verified implementations in proof assistants (Coq, Lean, Dafny)

For each approach found:
- What properties does it verify?
- What bugs has it found in real systems?
- How practical is it for our codebase scale?
- Setup cost vs ongoing value
- Limitations — what can't it catch?

Also search for:
- "{problem keywords} TLA+ specification"
- "{problem keywords} model checking"
- "{problem keywords} Kani verification rust"
- "{problem keywords} linearizability proof"
```

---

#### Agent 7 — Performance Engineering & Measurement

```
{SPECIALTY}: Performance Engineering & Measurement
{AGENT_ID}: 7
{FOCUS}:
Search for PERFORMANCE CHARACTERISTICS and measurement strategies:
- Benchmark methodologies for this class of problem
- Cache-aware and cache-oblivious approaches
- SIMD/vectorization opportunities
- Memory layout optimizations (SoA vs AoS, arena allocation)
- Lock-free and wait-free alternatives with measured overhead
- Amortization strategies and batching techniques
- Tail latency analysis (p50/p99/p999)
- Throughput vs latency trade-offs with concrete numbers

For each technique found:
- What speedup was measured? (absolute numbers, not just percentages)
- What hardware/workload was it tested on?
- What are the performance cliffs or degenerate cases?
- How does it interact with the memory hierarchy?
- Is the improvement consistent or workload-dependent?

Also search for:
- "{problem keywords} benchmark performance"
- "{problem keywords} cache optimization"
- "{problem keywords} latency throughput"
- "{problem keywords} SIMD vectorization"
```

---

#### Agent 8 — Testing & Validation Strategies

```
{SPECIALTY}: Testing & Validation Strategies
{AGENT_ID}: 8
{FOCUS}:
Search for how this problem is TESTED and VALIDATED:
- Property-based testing approaches (QuickCheck, proptest strategies)
- Fuzz testing results and techniques (AFL, libFuzzer, cargo-fuzz)
- Deterministic simulation testing (FoundationDB, TigerBeetle VOPR)
- Chaos engineering approaches for this domain
- Integration test patterns for distributed/concurrent systems
- Regression test suites from major implementations
- Mutation testing results

For each strategy found:
- What bugs did it find that other methods missed?
- What properties are being tested?
- How long does the test suite take to run?
- False positive/negative rates
- Setup complexity vs bug-finding effectiveness
- How does it compose with other testing strategies?

Also search for:
- "{problem keywords} property based testing"
- "{problem keywords} fuzz testing"
- "{problem keywords} simulation testing deterministic"
- "{problem keywords} Jepsen test"
```

---

#### Agent 9 — Adjacent Domains & Cross-Pollination (Optional)

```
{SPECIALTY}: Adjacent Domains & Cross-Pollination
{AGENT_ID}: 9
{FOCUS}:
Search for ANALOGOUS PROBLEMS in adjacent domains that may yield insights:
- How do other fields solve structurally similar problems?
- Biological systems (immune systems, neural networks, swarm behavior)
- Hardware design patterns (CPU pipelines, cache coherence protocols)
- Telecommunications (routing, congestion control, error correction)
- Game engines (ECS architectures, spatial indexing, frame scheduling)
- Financial systems (order matching, consensus, audit trails)
- Signal processing (filtering, streaming aggregation)

For each cross-domain insight:
- What is the analogous problem in the other domain?
- What technique do they use?
- How does it translate to our software context?
- What doesn't transfer? (different constraints, assumptions)
- Has anyone already applied this cross-domain insight?

Be creative but rigorous — every analogy must have a concrete technical
mapping, not just a hand-wavy metaphor.
```

---

#### Agent 10 — API & Interface Design (Optional)

```
{SPECIALTY}: API & Interface Design
{AGENT_ID}: 10
{FOCUS}:
Search for API DESIGN PATTERNS for this class of problem:
- How do established libraries expose this functionality?
- Builder patterns, typestate patterns, const generic patterns
- Error handling conventions (Result types, error hierarchies)
- Configuration and tuning knobs — what do users need to control?
- Composability — how does this integrate with other abstractions?
- Documentation patterns — what do users need to know?

For each API pattern found:
- What makes it easy to use correctly?
- What makes it hard to use incorrectly?
- How does it handle evolution (new features, deprecation)?
- What foot-guns exist in similar APIs?
- Ergonomics vs performance trade-offs

Also search for:
- "{problem keywords} rust API design"
- "{problem keywords} builder pattern"
- "{problem keywords} type safe API"
- "effective rust {problem keywords}"
```

---

### Collecting Phase 1 Results

After all agents complete, gather their outputs. If any agent fails or times
out, proceed with the agents that succeeded (minimum 5 required for Phase 2).

---

## Phase 2 — First Synthesis (Single Agent)

Launch **1 synthesis agent** using the Task tool with
`subagent_type=general-purpose`.

### First Synthesizer Prompt

```
You are the First Research Synthesizer. {N} independent research agents have
investigated the same problem from different angles in Phase 1. Your job is to
cross-reference their findings into a single, evidence-ranked knowledge base
AND identify specific gaps that need deeper investigation.

## Original Problem
{PROBLEM}

## Research Brief
{RESEARCH_BRIEF}

## Phase 1 Research Reports
{ALL_PHASE_1_REPORTS}

## Your Task

### 1. Evidence Inventory

Create a master list of ALL unique findings across all agents. For findings
reported by multiple agents, merge them and note corroboration. Preserve
the original finding IDs (P1.{agent#}.F{n}) for traceability.

For each merged finding:
- **ID**: S1.F{N}
- **Title**: {descriptive title}
- **Original IDs**: {list of P1.x.Fy IDs that contribute to this finding}
- **Sources**: {all sources citing this finding, with URLs}
- **Corroboration**: {how many agents independently found this}
- **Evidence strength**: {1-5, use the highest-quality source}
- **Applicability**: {high/medium/low for our specific problem}

### 2. Consensus Matrix

Identify the key design decisions for this problem, then for each decision
show where the evidence points:

| Decision | Option A | Option B | Evidence For A | Evidence For B | Verdict |
|----------|----------|----------|----------------|----------------|---------|

Verdict: STRONG CONSENSUS, LEAN (direction), CONTESTED, or INSUFFICIENT EVIDENCE.

### 3. Evidence-Ranked Techniques

Rank all discovered techniques/approaches by weighted evidence score:

Score = (evidence_strength x applicability x corroboration_count)

| Rank | Technique | Score | Evidence | Applicability | Corroboration | Key Source |
|------|-----------|-------|----------|---------------|---------------|------------|

### 4. Risk Register

From the failure modes research, compile a risk register:

| Risk ID | Risk | Likelihood | Impact | Mitigation | Source |
|---------|------|------------|--------|------------|--------|

### 5. Contradictions & Gaps

- Where do sources disagree? What's the strongest evidence on each side?
- What aspects of the problem have NO evidence? Where are we flying blind?
- What evidence exists but doesn't transfer to our specific context?

### 6. Deep-Dive Targets

THIS IS CRITICAL. Identify 3-5 specific questions that Phase 1 could NOT
adequately answer. For each:

- **Target {N}**: {specific question}
- **Why it matters**: {impact on the design}
- **What we know so far**: {best evidence available, with finding IDs}
- **What's missing**: {specific gap in knowledge}
- **Suggested starting lens**: {which research angle is most promising}
- **Suggested search terms**: {concrete queries to try}

These targets become the marching orders for Phase 3 deep-dive agents.

### 7. Key Insights

The 5-10 most important things learned from Phase 1 that should directly
influence the design. Each must cite at least one source by finding ID.

### Rules

- Do NOT add your own findings — you are synthesizing, not researching.
- If an agent's finding has no source, downgrade it to evidence strength 0
  and flag it as UNVERIFIED.
- Preserve ALL source URLs from the original reports.
- If agents contradict each other, present both sides — do not pick a winner
  unless the evidence clearly favors one side.
- Be explicit about what we DON'T know, not just what we do.
- Stay within your budget: aim for ~6000 tokens of output.

### Output Format

Return a markdown document starting with:
`# First Research Synthesis (S1)`

Include all sections above, plus:

#### Executive Summary
3-5 bullet points capturing the most critical findings.
```

---

## Phase 3 — Targeted Deep-Dives (3-5 Parallel Agents)

Launch **3-5 deep-dive agents in parallel** using the Task tool with
`subagent_type=general-purpose`. Each agent gets a specific gap/question
identified in Phase 2's Deep-Dive Targets.

**Phase 3 and Phase 4 MUST be launched in a single message** so they run
concurrently. This is the key structural optimization.

### Deep-Dive Agent Prompt

```
You are Deep-Dive Agent {AGENT_ID} — a targeted researcher investigating a
specific gap identified during Phase 2 synthesis.

## Original Problem
{PROBLEM}

## Your Specific Target
{DEEP_DIVE_TARGET}

## Relevant Context from Phase 1
{CURATED_EXCERPTS}

(Above: curated excerpts from Phase 1 reports relevant to your target.
Not the full reports — only the pertinent findings.)

## Your Research Mission

Phase 1 surveyed broadly. You go DEEP on one specific question. Your evidence
bar is HIGHER than Phase 1: only Level 3-5 evidence counts (implemented/tested
or stronger). Level 1-2 evidence should only be mentioned if nothing stronger
exists, clearly flagged as weak.

### Research Process

1. Start from the suggested search terms in your target, but don't stop there.
2. Follow citation chains — if a paper references relevant work, chase it.
3. Read actual source code of implementations, not just documentation.
4. Look for benchmarks, test suites, and real-world usage data.
5. Cross domain boundaries if the suggested lens doesn't yield results —
   you are unconstrained in where you search.

### Rules

- Higher evidence bar: Level 3-5 preferred. Flag Level 1-2 as WEAK.
- Go DEEP, not wide. 5 thoroughly investigated findings beat 15 surface-level ones.
- Read source code. Link to specific files/functions, not just repositories.
- If the target question has no good answer in the literature, say so clearly.
- Stay within your budget: aim for ~4000 tokens of output.

### Output Format

Return a markdown document starting with:
`# P3 Deep-Dive — Agent {AGENT_ID}: {TARGET_TITLE}`

#### 1. Target Question
{restate the specific question}

#### 2. Findings
For each finding (aim for 3-8, quality over quantity):

**P3.{AGENT_ID}.F{N}: {title}**
- **Source**: {URL or citation}
- **Evidence strength**: {3-5} — {label} (or {1-2} flagged as WEAK)
- **Summary**: {3-5 sentences, more detail than Phase 1}
- **Key technique/insight**: {the actionable takeaway}
- **Applicability**: {high/medium/low} — {why}
- **Caveats**: {limitations}
- **Source code reference**: {specific file/function if applicable}

#### 3. Answer to Target Question
A direct, evidence-backed answer to the question posed. If the answer is
"it depends", specify exactly what it depends on with evidence for each case.

#### 4. Remaining Unknowns
What this deep-dive could NOT resolve, and what would be needed to resolve it.
```

---

## Phase 4 — Adversarial Review (4 Parallel Agents)

Launch **4 adversarial agents in parallel** using the Task tool with
`subagent_type=general-purpose`.

Each receives Phase 2's synthesis (NOT Phase 3 output — they run in parallel
to prevent anchoring).

### Adversarial Agent Common Preamble

```
You are an adversarial reviewer in Phase 4 of a comprehensive research funnel.
Your role is to CHALLENGE the conclusions from Phase 2's synthesis — not to
confirm them. Your mandate is: {MANDATE}.

## Original Problem
{PROBLEM}

## Phase 2 Synthesis (what you are challenging)
{PHASE_2_SYNTHESIS}

## Rules

- Your job is to find WEAKNESSES, not to agree.
- Every challenge must be backed by evidence (sources, logic, or concrete
  counter-examples). Vague skepticism is worthless.
- If you genuinely cannot find weakness in a conclusion, say so — forced
  contrarianism is as bad as uncritical acceptance.
- Focus on the TOP-RANKED approaches and strongest claims — those are where
  overconfidence is most dangerous.
- Stay within your budget: aim for ~2500 tokens of output.
```

---

#### Adversarial Agent 1 — Devil's Advocate

```
{MANDATE}: Construct the strongest possible case that the top-ranked approach
is WRONG or will fail in our specific context.

{AGENT_ID}: 1

### Your Task

1. Identify the #1 ranked technique from the synthesis.
2. Search for evidence that it FAILS:
   - Production failures, regressions, or abandonments of this approach
   - Contexts where it underperforms alternatives
   - Hidden assumptions that may not hold in our codebase
   - Scaling limits or performance cliffs
3. Construct the strongest counter-argument you can.
4. Rate your own confidence that the counter-argument is valid (0-100).

### Output Format

`# P4 Adversarial — Agent 1: Devil's Advocate`

**Target**: {the approach being challenged}

**The Case Against**:
{your strongest argument, with sources}

**P4.1.F{N}**: {each specific counter-finding, using standard format}

**Confidence in counter-argument**: {0-100}%
**Verdict**: APPROACH IS {SOUND / WEAKENED / FLAWED} — {summary}
```

---

#### Adversarial Agent 2 — Cross-Validator

```
{MANDATE}: Verify the top 7-10 factual claims from the synthesis against
primary sources. Check that citations actually say what they're claimed to say.

{AGENT_ID}: 2

### Your Task

1. Pick the 7-10 most important factual claims from the synthesis (those
   that load-bearing design decisions rest on).
2. For EACH claim:
   a. Go to the cited source (WebFetch the URL if possible).
   b. Verify the claim matches what the source actually says.
   c. Check for important caveats or qualifications that were dropped.
   d. Look for errata or corrections published after the original.
3. Rate each claim: VERIFIED, PARTIALLY VERIFIED, UNVERIFIABLE, or REFUTED.

### Output Format

`# P4 Adversarial — Agent 2: Cross-Validator`

| # | Claim (finding ID) | Source | Verdict | Notes |
|---|-------------------|--------|---------|-------|

**P4.2.F{N}**: {each verification finding, using standard format}

For any PARTIALLY VERIFIED or REFUTED claims, provide detailed explanation.

**Summary**: {X of Y claims verified, Z partially, W refuted}
```

---

#### Adversarial Agent 3 — Assumptions Auditor

```
{MANDATE}: List every assumption — stated AND unstated — in the Phase 2
synthesis, and check each one's validity for our specific context.

{AGENT_ID}: 3

### Your Task

1. Read the synthesis carefully and extract EVERY assumption, including:
   - Explicit assumptions stated in the text
   - Implicit assumptions (e.g., "this scales linearly" without proof)
   - Domain transfer assumptions (evidence from system X applied to our system)
   - Environmental assumptions (hardware, OS, workload characteristics)
   - Temporal assumptions (what was true when the source was written)
2. For each assumption, assess:
   - Is it valid in OUR specific context? (check the codebase)
   - What happens if it's wrong?
   - Can it be verified before committing to the design?

### Output Format

`# P4 Adversarial — Agent 3: Assumptions Auditor`

| # | Assumption | Source Finding | Stated/Implicit | Valid? | Risk if Wrong |
|---|-----------|----------------|-----------------|--------|---------------|

**P4.3.F{N}**: {each assumption finding, using standard format}

**High-Risk Assumptions**: {list of assumptions that, if wrong, would
invalidate the recommended approach}

**Verification Plan**: {how to test the most critical assumptions}
```

---

#### Adversarial Agent 4 — Contrarian Searcher

```
{MANDATE}: Search ONLY for evidence that the leading approach is wrong,
dangerous, or inferior to alternatives. You are looking for disconfirming
evidence specifically.

{AGENT_ID}: 4

### Your Task

1. Identify the top 2-3 recommended approaches from the synthesis.
2. For EACH, actively search for:
   - Systems that TRIED this approach and ABANDONED it (and why)
   - Benchmarks where this approach LOSES to alternatives
   - Known failure modes specific to this approach
   - Academic papers arguing AGAINST this approach
   - Alternative approaches that the synthesis may have underweighted
3. Use WebSearch with queries designed to find negative evidence:
   - "{approach} problems issues limitations"
   - "{approach} vs {alternative} benchmark comparison"
   - "{approach} abandoned replaced migration"
   - "{approach} failure post-mortem regression"
   - "why not {approach}"

### Output Format

`# P4 Adversarial — Agent 4: Contrarian Searcher`

**P4.4.F{N}**: {each disconfirming finding, using standard format}

**Strongest Alternative Not in Synthesis**: {if you found a viable approach
the synthesis missed entirely, describe it with evidence}

**Overall Assessment**: {Does the contrarian evidence materially change the
recommended approach, or is it edge-case/context-specific?}
```

---

## Phase 5 — Final Synthesis (Single Agent)

After Phase 3 (deep-dives) AND Phase 4 (adversarial) both complete, launch
**1 final synthesis agent** using the Task tool with
`subagent_type=general-purpose`.

### Final Synthesizer Prompt

```
You are the Final Research Synthesizer. You are reconciling THREE streams of
information:

1. **Phase 2's First Synthesis**: The initial evidence-ranked findings
2. **Phase 3's Deep-Dives**: Targeted investigations into gaps
3. **Phase 4's Adversarial Review**: Challenges to Phase 2's conclusions

Your job is to produce the DEFINITIVE research synthesis that accounts for
all evidence — including evidence AGAINST the leading approaches.

## Original Problem
{PROBLEM}

## Phase 2 First Synthesis
{PHASE_2_SYNTHESIS}

## Phase 3 Deep-Dive Reports
{ALL_DEEP_DIVE_REPORTS}

## Phase 4 Adversarial Reports
{ALL_ADVERSARIAL_REPORTS}

## Your Task

### 1. Reconciliation

For each major finding or recommendation from Phase 2:
- Was it STRENGTHENED by deep-dives? (new supporting evidence)
- Was it CHALLENGED by adversarial review? (counter-evidence found)
- Was it UNCHANGED? (adversarial review found no issues)

Present this as a reconciliation table:

| S1 Finding | Deep-Dive Impact | Adversarial Impact | Final Status |
|------------|------------------|--------------------|--------------|
| S1.F1: ... | Strengthened by P3.1.F2 | Unchallenged | CONFIRMED |
| S1.F3: ... | Gap partially filled by P3.2.F1 | Weakened by P4.1.F3 | REVISED |
| S1.F5: ... | No new data | Refuted by P4.4.F2 | DOWNGRADED |

Final Status options: CONFIRMED, REVISED, DOWNGRADED, REFUTED, UNCHANGED

### 2. Updated Evidence Ranking

Re-rank all techniques, incorporating:
- New evidence from deep-dives
- Adjustments from adversarial challenges
- Any new approaches surfaced by the contrarian searcher

| Rank | Technique | Original Rank | Change | Score | Confidence | Key Evidence |
|------|-----------|---------------|--------|-------|------------|--------------|

### 3. Verified Claims vs Challenged Claims

Based on the cross-validator's work:
- **Verified (build on these)**: {list with finding IDs}
- **Challenged (proceed with caution)**: {list with finding IDs and concerns}
- **Unverifiable (note the uncertainty)**: {list}

### 4. Assumption Risk Matrix

Based on the assumptions auditor's work:
- **Safe assumptions**: {verified or low-risk if wrong}
- **Risky assumptions**: {unverified and high-impact if wrong}
- **Critical to verify before implementation**: {ordered by risk}

### 5. Updated Risk Register

Merge the original risk register with adversarial findings:

| Risk ID | Risk | Likelihood | Impact | Mitigation | Source | Phase |
|---------|------|------------|--------|------------|--------|-------|

### 6. Final Key Insights

The 10-15 most important findings, incorporating all phases. Each must cite
finding IDs for full traceability. For any insight that was adversarially
challenged, note the challenge and why the insight survives (or how it was
revised).

### 7. Implementation Guidance

Based on ALL evidence, provide:
- **Recommended approach**: {with confidence level and finding IDs}
- **Key design constraints**: {from evidence, not opinion}
- **Critical risks to mitigate**: {from the risk register}
- **What to verify first**: {assumptions that must be tested}
- **What to monitor in production**: {based on failure mode evidence}

### Rules

- Every claim must trace back to finding IDs (P1.x.Fy, S1.Fn, P3.x.Fy, P4.x.Fy).
- Do NOT suppress adversarial findings. If the adversarial review found real
  issues, they must be reflected in the final ranking and guidance.
- If deep-dives found strong new evidence, integrate it fully.
- Be explicit about confidence levels — distinguish between "strong evidence
  supports X" and "X seems reasonable but evidence is thin."
- Stay within your budget: aim for ~8000 tokens of output.

### Output Format

Return a markdown document starting with:
`# Final Research Synthesis (S2)`

Include all sections above, plus:

#### Executive Summary
5-7 bullet points capturing the definitive findings after all phases.
```

---

## Phase 6 — Integration (Single Agent)

Launch **1 integration agent** using the Task tool with
`subagent_type=general-purpose`.

This agent maps the final synthesis to a concrete implementation plan with
full traceability.

### Integrator Prompt

```
You are the Research-to-Plan Integrator. You have a comprehensive, adversarially
verified research synthesis and access to the codebase. Your job is to produce a
concrete, evidence-backed implementation plan where every decision traces back
to research findings.

## Original Problem
{PROBLEM}

## Final Research Synthesis
{PHASE_5_SYNTHESIS}

## Your Task

### Step 1: Codebase Mapping

Thoroughly explore the codebase to understand:
- Current architecture and module structure (use Glob, Grep, Read)
- Existing patterns and conventions
- What infrastructure already exists that can be leveraged
- What constraints the current architecture imposes
- Dependencies and their versions

Map each research finding to specific locations in the codebase:
- Which files/modules would be affected?
- What existing abstractions can be reused?
- Where do new abstractions need to be introduced?

### Step 2: Implementation Plan

Produce a step-by-step implementation plan where EVERY design decision
cites finding IDs from the research:

#### Plan Format

For each step:

**Step {N}: {title}**
- **What**: {concrete description — types, signatures, module placement}
- **Why**: {justification citing specific finding IDs: S2.F1, P1.4.F3, etc.}
- **Evidence**: {the specific technique/paper/system this is based on}
- **Adversarial check**: {what the adversarial review said about this approach,
  and how the design accounts for it}
- **Files**: {exact file paths to create or modify}
- **Risks**: {from the risk register, with mitigation}
- **Assumptions**: {from the assumptions audit — which must be verified}
- **Acceptance criteria**: {how to verify this step is correct}

### Step 3: Evidence Trail

Create a full traceability matrix:

| Plan Step | Research Finding(s) | Phase | Evidence Strength | Confidence |
|-----------|--------------------|----|-------|------------|
| Step 1    | S2.F1, P1.2.F3     | 1,5 | 4     | HIGH       |

Confidence levels:
- HIGH: Multiple strong sources agree, adversarial review did not challenge
- MEDIUM: Evidence exists but adversarial review raised valid concerns
- LOW: Limited evidence, or adversarial review found significant counter-evidence
- NOVEL: No direct evidence found — flag for extra review

Any step with LOW or NOVEL confidence gets a mandatory note explaining
what additional validation is needed.

### Step 4: Adversarial Concerns Integration

For each concern raised by Phase 4 adversarial agents:
- How does the implementation plan address it?
- If it's not addressed, why not? (with evidence)
- What monitoring or fallback is in place?

### Step 5: Alternative Approaches

For any CONTESTED decisions from the synthesis, describe:
- The alternative approach
- What evidence supports it
- Under what conditions we'd switch to it
- How to structure the code so switching is feasible

### Step 6: Validation Strategy

How to verify the implementation is correct:
- What properties should be tested (unit, property-based, fuzz)?
- What benchmarks should be run?
- What failure modes from the risk register need explicit test cases?
- What assumptions need empirical verification?
- Are there formal verification opportunities (Kani, MIRI)?

### Rules

- Every design decision MUST cite finding IDs. If there's no evidence for a
  choice, flag it explicitly as NOVEL/UNJUSTIFIED.
- Be concrete: file paths, type signatures, function names.
- Respect existing codebase conventions.
- The plan should be implementable by a developer who hasn't read the full
  research — include enough context in each step.
- Include estimated complexity per step (S/M/L) but NOT time estimates.
- Do NOT suppress or ignore adversarial findings.

### Output Format

Return a markdown document starting with:
`# Implementation Plan`

Include all sections above, plus:

#### References
A numbered bibliography of all sources cited in the plan, with URLs.
Each citation in the plan body should reference this list: [1], [2], etc.
```

---

## Final Output Format

After the integrator (Phase 6) completes, present the combined output:

```markdown
## Deeper Research Results

### Problem
{one-line restatement}

### Executive Summary
{from the final synthesizer's executive summary — Phase 5}

### Evidence Highlights
| # | Finding | Evidence Strength | Corroboration | Adversarial Status | Sources |
|---|---------|-------------------|---------------|--------------------|---------|
{top 10-15 findings from the final synthesis, ranked by score}

### Implementation Plan
{the integrator's full plan from Phase 6}

### Consensus & Contested Decisions
{consensus matrix from the final synthesis}

### Risk Register
{merged risk register from the final synthesis}

### Adversarial Summary
| Adversarial Agent | Key Challenge | Impact on Recommendations |
|-------------------|---------------|---------------------------|
| Devil's Advocate  | ...           | ...                       |
| Cross-Validator   | X/Y verified  | ...                       |
| Assumptions Auditor | N risky assumptions | ...              |
| Contrarian Searcher | ...         | ...                       |

### Traceability
{evidence trail table from the integrator}

### Full Research (collapsed)
<details><summary>Phase 1 Reports</summary>

<details><summary>Agent 1: Foundational Theory</summary>
{full report}
</details>
<details><summary>Agent 2: Production Systems</summary>
{full report}
</details>
{repeat for all Phase 1 agents}

</details>

<details><summary>Phase 2: First Synthesis</summary>
{full synthesis report}
</details>

<details><summary>Phase 3: Deep-Dive Reports</summary>
{all deep-dive reports}
</details>

<details><summary>Phase 4: Adversarial Reports</summary>
{all adversarial reports}
</details>

<details><summary>Phase 5: Final Synthesis</summary>
{full final synthesis report}
</details>

### References
{consolidated bibliography from integrator}
```

---

## Configuration

```
/deeper-research <problem>                    # Default: 8 lenses
/deeper-research --lenses=10 <problem>        # Full 10 lenses
/deeper-research --lenses=5 <problem>         # Minimal (5 core lenses)
/deeper-research --no-adversarial <problem>   # Skip Phase 4
/deeper-research --skip-deep-dive <problem>   # Skip Phase 3
```

### Agent Counts by Configuration

| Config | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 | Total |
|--------|---------|---------|---------|---------|---------|---------|-------|
| Default (8 lenses) | 8 | 1 | 3-5 | 4 | 1 | 1 | 18-20 |
| Full (10 lenses) | 10 | 1 | 3-5 | 4 | 1 | 1 | 20-22 |
| Minimal (5 lenses) | 5 | 1 | 3-5 | 4 | 1 | 1 | 15-17 |
| No adversarial | 8 | 1 | 3-5 | 0 | 1 | 1 | 14-16 |
| Skip deep-dive | 8 | 1 | 0 | 4 | 1 | 1 | 15 |
| Both skipped | 8 | 1 | 0 | 0 | 1 | 1 | 11 |

### Phase Skip Behavior

- **`--no-adversarial`**: Phase 4 is skipped entirely. Phase 5 synthesizes
  Phase 2 + Phase 3 only (no adversarial reconciliation). Phase 6 has no
  adversarial concerns to address.
- **`--skip-deep-dive`**: Phase 3 is skipped entirely. Phase 4 still runs
  (challenging Phase 2). Phase 5 synthesizes Phase 2 + Phase 4 only.
- **Both flags**: Phases 3 and 4 both skipped. Phase 5 receives only Phase 2's
  synthesis (effectively a pass-through with updated formatting). Consider
  using `/deep-research` instead.

### Minimum Agent Requirements

- Phase 1: minimum 5 agents must succeed (of 8-10 launched)
- Phase 2: exactly 1 (required)
- Phase 3: minimum 2 agents must succeed (of 3-5 launched)
- Phase 4: minimum 3 agents must succeed (of 4 launched)
- Phase 5: exactly 1 (required)
- Phase 6: exactly 1 (required)

## Tips

- **Problem statement quality matters**: Include domain-specific terminology,
  relevant file paths, and specific constraints. The Research Brief amplifies
  this, but garbage in = garbage out.
- **Use `--lenses=10` for cross-cutting concerns**: When the problem spans
  multiple domains (e.g., a data structure that needs both formal correctness
  AND API ergonomics), the optional lenses provide crucial coverage.
- **Use `--lenses=5` when you need more depth, not breadth**: If the problem
  is narrow but deep, 5 lenses with deep-dives gives better results than 10
  surface-level surveys.
- **The adversarial phase is the key differentiator**: It catches overconfidence,
  citation errors, and hidden assumptions. Only skip it (`--no-adversarial`) for
  exploratory research where you don't need verified conclusions.
- **Deep-dives are targeted, not redundant**: They investigate specific gaps
  from Phase 2, not the same questions as Phase 1. Phase 2's Deep-Dive Targets
  section is critical for this.
- **Traceability is the contract**: Every implementation step in Phase 6 must
  cite finding IDs. If a step has no citations, it's unjustified.
- **This skill feeds into `/design-tournament`**: Use deeper-research to
  establish the evidence base, then design-tournament to explore implementation
  approaches grounded in that evidence.
- **For the most critical decisions**: Run `/deeper-research --lenses=10` with
  all phases, then feed the output into `/design-tournament` for implementation
  exploration. This gives maximum coverage at ~28 total agents.
