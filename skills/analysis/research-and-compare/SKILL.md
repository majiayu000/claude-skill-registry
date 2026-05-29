---
name: research-and-compare
description: Research and compare the Stateless Agent Methodology (SAM) against other methodologies using only verifiable reference material. Produce overlap/divergence analysis that is useful for comparing strategy, methodologies, and potential implementations, and for identifying weaknesses in the current SAM methodology while changes are still cheap. Creates structured comparison documents following the SAM comparison template, including terminology normalization + attribution notes.
argument-hint: <url-or-path-or-name>
context: fork
agent: general-purpose
model: sonnet
user-invocable: true
---

# Research and Compare Methodology Framework

**CRITICAL RESEARCH CONSTRAINT**: You MUST NOT make comparisons based on training data knowledge. All comparisons MUST be based on verifiable reference material that you read during this session.

## Your Mission

Compare the Stateless Agent Methodology (SAM) with another methodology/framework specified by the user, producing a structured comparison document following the universal comparison template.

**Primary intent (when this skill triggers)**:

1. Identify **overlap** (shared mechanisms / invariants) and **divergence** (different tradeoffs).
2. Use divergence to surface **weaknesses / gaps / risks** in the current SAM design (planning phase where change is cheap).
3. Identify **implementation pairing opportunities** (e.g., “SAM + {runtime/infrastructure}”) without changing SAM’s core semantics.
4. Normalize terminology so comparisons don’t get stuck on names (taxonomy is intentionally unset in SAM docs).

## Input Specification

You will receive one of the following:

- **URL**: Web link to methodology documentation
- **File path**: Local or relative path to methodology documentation
- **Methodology name**: Name to research (you must find authoritative sources)

Input provided: `$ARGUMENTS`

## Execution Protocol

### Phase 1: Load Template Structure

**MANDATORY FIRST STEP**: Read the comparison template to understand the required structure:

```
Read(file_path="methodology_development/../.claude/skills/research-and-compare/methodology_comparison_template.md")
```

**Verification**: Confirm you understand the template's 6-section structure:

- **Section 0**: Comparison Header (metadata and decision context)
- **Section 1**: Pre-Comparison Reflection (MANDATORY tailored rubric - this is your gating step)
- **Section 2**: Comparison Map (one-screen orientation with personas)
- **Section 3**: Domain Worksheets (evidence-based evaluation per selected domain)
- **Section 4**: Decision Matrix (optional weighted scoring)
- **Section 5**: Outputs (actionable recommendations with tradeoffs)
- **Section 6**: Evidence Log (full traceability for every claim)

### Phase 2: Load SAM Reference Material (Item A)

**MANDATORY SECOND STEP**: Read the complete SAM methodology document:

```
Read(file_path="methodology_development/stateless-agent-methodology.md")
```

**Verification**: Confirm you have read SAM completely. This is **Item A** in your comparison.

Extract and note:

- SAM's 7-stage pipeline
- Core principles (stateless agents, externalized memory, verification at boundaries)
- Design constraints
- Success metrics
- Key architectural patterns

**Terminology / taxonomy alignment rule (MANDATORY)**:

- Treat filenames in SAM docs as **example implementations**, not canonical identifiers.
- When SAM docs use tokens, preserve them. When they use filenames, map them to semantic tokens:
  - Canonical artifact pattern: `ARTIFACT:{TYPE}({SCOPE_OR_ID})`
  - Disambiguators: `CTX:*`, `PREREQ:*`, `EXEC:*`, `VERIFY:*`
  - Preserve original filenames as `(e.g. ...)` examples.

**Canonical taxonomy sources (local)**:

- `methodology_development/stateless-software-engineering-framework.md` (semantic tokens + disambiguators + example file/SQL backends)
- `methodology_development/stateless-agent-methodology.md` (SAM process doc aligned to tokens)

**File reference rule (MANDATORY)**:

- When referencing repository files in the comparison document, use **relative paths** (repo-relative) rather than absolute filesystem paths.
- Prefer markdown-linkable relative paths where appropriate (e.g., `./methodology_development/stateless-agent-methodology.md`), and avoid `/home/...` style paths.

### Phase 3: Acquire Target Methodology Documentation (Item B)

Based on input type, gather complete authoritative material:

**If URL provided**:

1. Use `WebFetch` to retrieve the content
2. If URL requires navigation, use `WebSearch` to find related documentation
3. Read enough primary docs until you cover the full workflow end-to-end (do not stop at 2-3 pages if the methodology spans more)

**If file path provided**:

1. Use `Read` to load the file
2. If file references other files, read those as well
3. Verify you have complete methodology description

**If methodology name provided**:

1. Use `WebSearch` to find authoritative sources (prioritize: official docs > academic papers > implementations)
2. Use `WebFetch` to retrieve primary documentation
3. Read minimum 2-3 authoritative sources
4. Verify sources are current (check dates)

**This is Item B** in your comparison.

**Terminology normalization for Item B (MANDATORY)**:

- Do NOT treat target methodology filenames (e.g., `plan.md`, `research.md`) as canonical.
- Normalize to SAM/SSE semantic tokens and keep original terms as examples.
- Add an attribution footnote in the output doc noting that terminology/taxonomy was normalized for comparison.

**Breadth rule for target evidence (MANDATORY; no “holding back”)**:

This is a short, high-context task in a forked context: do not reserve or “save” context for later. Load whatever is needed now to make the comparison decision-grade.

When the target has an implementation (not just a paper), read broadly until you can describe both semantics and expected usage:

- Read **user guides** and **README(s)** (how users actually run it)
- Read **setup / installation** instructions
- Read **code** if it exists (at least the entrypoints and any “orchestrator” logic)
- Read **agents/skills/prompts** if the target defines them (to understand structure + expectations)
- Read **transcripts / examples / demos** if present (how it behaves in practice)
- Read any **schemas / manifests** (e.g., MCP manifests, config formats)

### Phase 4: Evidence Verification Checkpoint

**STOP. BEFORE proceeding, verify ALL checkboxes:**

**SAM knowledge (Item A)**:

- [ ] I have read the complete SAM methodology document
- [ ] I understand SAM's 7-stage pipeline
- [ ] I know SAM's core principles and input constraints
- [ ] I have specific line numbers/sections to reference

**Target methodology knowledge (Item B)**:

- [ ] I have read authoritative source material
- [ ] I can cite specific sections/quotes with URLs
- [ ] I understand the core workflow/architecture
- [ ] I have documented all source URLs with access dates

**Anti-hallucination verification**:

- [ ] I am NOT relying on training data for either methodology
- [ ] Every claim I will make can be cited to a source I read THIS SESSION
- [ ] If I don't have source material for a claim, I will NOT make that claim
- [ ] I will mark uncertain comparisons as "NOT_COMPARABLE" with explanation

**If ANY checkbox is unchecked, STOP and gather more material.**

### Phase 5: Complete Section 0 - Comparison Header

Fill out the header from template (lines 7-18):

```markdown
## 0) Comparison Header

- **Item A**: Stateless Agent Methodology (SAM)
- **Item B**: {target methodology name}
- **Comparison category**: technical_framework
- **Decision posture**: describe_tradeoffs_only
- **Audience**: Software teams evaluating LLM agent workflows
- **Primary decision to enable**: "Which methodology fits our LLM agent project needs?"
- **Stakes / cost of wrong choice**: high (methodology affects project architecture)
- **Time budget**: {your research time}
- **Evidence constraint**: high_rigor_required
- **Non-negotiables**: Evidence-based only, must support LLM agents, must address hallucination risks
```

### Phase 6: Complete Section 1 - Pre-Comparison Reflection (MANDATORY GATING STEP)

**This section is MANDATORY before evaluation. Complete ALL subsections from template (lines 21-131):**

#### 1.1 Fit-for-purpose framing (template lines 26-37)

Answer these questions:

- **What problem exists**: Why compare SAM to {target}?
- **Who experiences the problem**: Software teams building LLM agents
- **Success signals**: Reliable agent implementation, reduced hallucinations, verifiable outputs
- **Failure modes**: Agent failures, wasted implementation time, undetectable errors
- **Out of scope**: Explicitly list non-goals

#### 1.2 Assumptions and boundary conditions (lines 39-45)

List assumptions about both methodologies:

- Assumption 1: {state assumption} → Evidence needed: {how to validate}
- Assumption 2: {state assumption} → Evidence needed: {how to validate}
- Document boundary conditions: team skills, project constraints, technology stack

#### 1.3 Evidence plan (lines 47-58)

- **Primary evidence sources**: Official docs, specs, published comparisons, case studies
- **Comparability rules**: Only compare documented features; mark NOT_COMPARABLE when evidence differs
- **Version/time window**:
  - SAM: {current date, document version}
  - Target: {version/date from sources}

#### 1.4 Scoring stance (lines 60-74)

Choose one:

- **narrative-only** (recommended for methodologies - no forced numeric scores)
- **hybrid** (numeric where measurable, narrative for qualitative)
- **weighted_matrix** (full numeric scoring with justification)

Selected: {your choice}

#### 1.5 Tailored domain set (lines 76-118)

**Select essential domains** (5-9 that drive the decision):

- [ ] Core approach / mechanism / workflow
- [ ] Effectiveness / outcomes
- [ ] Costs + constraints
- [ ] Risks / failure modes + mitigations
- [ ] Adoption / learning curve
- [ ] Maintainability / operability
- [ ] {others as appropriate}

**Optional domains** (only if decision-relevant):

- [ ] Performance / efficiency
- [ ] Compatibility / interoperability
- [ ] Ecosystem / support / community
- [ ] Evidence quality / reproducibility
- [ ] {others from template}

**Domain-specific extensions** (max 5):
For each new domain:

- Why decision-critical?
- What evidence resolves it?
- Which existing domain it refines?

#### 1.6 Stopping criteria (lines 119-130)

Verify readiness:

- [ ] Chosen essentials answered with decision-grade evidence
- [ ] Adding domains would not change recommendation
- [ ] Remaining unknowns are low-impact or evidence-blocked

Decision: READY_TO_COMPARE | NEEDS_MORE_EXTENSION | NEEDS_MORE_EVIDENCE

### Phase 7: Complete Section 2 - Comparison Map (template lines 133-153)

#### 2.1 One-sentence summaries

- **SAM in one sentence**: {from SAM doc}
- **Target in one sentence**: {from target docs}

#### 2.2 "Best for" and "avoid if" personas

- **SAM best for**: {cite SAM use cases}
- **SAM avoid if**: {cite SAM limitations}
- **Target best for**: {cite target use cases}
- **Target avoid if**: {cite target limitations}

#### 2.3 Non-negotiables check

- SAM: PASS | FAIL (rationale: {cite evidence})
- Target: PASS | FAIL (rationale: {cite evidence})

### Phase 8: Complete Section 3 - Domain Worksheets (template lines 155-279)

**FOR EACH domain selected in Phase 6 (Section 1.5), complete a full worksheet.**

Each worksheet MUST include (per template structure):

#### Domain: {domain name}

**Definition**: What this domain means in this comparison

**Starter questions** (from template):

- {Use template's starter questions for this domain}

**Specialize**:

- Add 3 domain-specific questions for SAM vs {target}

**Evidence**:

- SAM: {cite sources with line numbers}
- Target: {cite sources with URLs + access dates}
- Comparability: {state if comparable or NOT_COMPARABLE with reason}

**Findings**:

- A (SAM): {findings with specific citations}
- B (Target): {findings with specific citations}

**Tradeoffs**:

- What improves: {cite evidence}
- What worsens: {cite evidence}

**Verdict**:

- {A_better | B_better | depends}
- Confidence: {low | med | high}
- Rationale: {cite evidence}

**Complete worksheets for all selected domains.**

### Phase 9: Complete Section 4 - Decision Matrix (template lines 281-313)

**ONLY if you selected "weighted_matrix" in Phase 6 (1.4):**

#### 4.1 Criteria list and weights

| Criterion | Definition              | Weight   | Evidence type   | Notes   |
| --------- | ----------------------- | -------- | --------------- | ------- |
| {c1}      | {contextual definition} | {weight} | {evidence type} | {notes} |

#### 4.2 Scoring table

| Criterion | Weight | A score | B score | Rationale + citations |
| --------- | ------ | ------- | ------- | --------------------- |
| {c1}      | {w1}   | {a1}    | {b1}    | {cite evidence}       |

#### 4.3 Sensitivity check (REQUIRED for numeric decisions)

- Re-run with weights shifted ±20% on top 3 criteria
- Test pessimistic assumptions on weakest-evidence criteria
- **Stable winner**: {yes | no}
- **If not stable, what drives flips?**: {analysis}

### Phase 10: Complete Section 5 - Outputs (template lines 315-345)

#### 5.1 Recommendation (choose format)

- **Single winner**: {A | B} because {top 3 reasons with citations}
- **Ranked**: 1) {winner} 2) {runner-up} with rationale
- **Best-for personas**: {persona -> methodology mapping}
- **Tradeoff-only** (no winner): {detailed tradeoff analysis}

#### 5.2 "Flaws but not dealbreakers"

- SAM: {acceptable limitations with citations}
- Target: {acceptable limitations with citations}

#### 5.3 Worth considering (near-misses / niche fits)

- {methodology}: {why it might fit in specific contexts}

#### 5.4 The competition (explicitly excluded)

- **Excluded domains**: {list with rationale}
- **Excluded alternatives**: {other methodologies not compared, with reason}

#### 5.5 What to look forward to (update triggers)

- **Revisit when**: {new version, new evidence, changed constraints, new regulation}
- **Next review date**: {suggested date}

### Phase 11: Complete Section 6 - Evidence Log (template lines 347-356)

**Create full traceability table for EVERY non-trivial claim:**

| Claim                     | Evidence                                     | Date/version  | Confidence     | Notes        |
| ------------------------- | -------------------------------------------- | ------------- | -------------- | ------------ |
| SAM uses 7-stage pipeline | stateless-agent-methodology.md lines 104-180 | 2026-01-27    | high           | Direct quote |
| Target uses {pattern}     | {URL}                                        | {access date} | {low/med/high} | {context}    |

**Every claim in your comparison MUST have an entry here with:**

- Source location (file path + line numbers OR URL)
- Date accessed (for web sources)
- Confidence level (low/med/high)
- Contextual notes if needed

### Phase 12: Write Complete Document

**Output location**:

```
methodology_development/sam-vs-{slug}.md
```

**Slug generation**:

- Lowercase target methodology name
- Replace spaces with hyphens
- Remove special characters
- Max 40 characters
- Example: "OctoCode RDD" → "octocode-rdd"

**Document structure**: Follow template exactly with ALL sections completed (Sections 0-6).

---

## Comparison Validity Rules

---

## SAM-Specific Weakness Discovery (MANDATORY)

This skill is not just for “which is better?”; it is also for **stress-testing SAM while change is cheap**.

Add to **Section 5 (Outputs)** (append subsections as 5.6+; do not renumber existing 5.1–5.5):

- **5.6 Overlap inventory (Convergence)**:

  - List shared mechanisms across A and B (e.g., fresh sessions, artifact handoffs, deterministic checks).
  - For each: what SAM already has vs what is missing (clarity, enforcement, infrastructure).

- **5.7 Divergence-driven weaknesses in SAM**:

  - Convert each divergence into a testable gap statement.
  - For each gap: propose remediation options with labels:
    - **CORE CHANGE** (changes SAM semantics)
    - **PROFILE/PAIRING** (e.g., “SAM + {runtime}” without changing core)
    - **DOC/TAXONOMY** (clarify semantics; no behavior change)

- **5.8 Terms worth borrowing (taxonomy unset, semantics fixed)**:

  - Identify target terms that are more succinct labels for an existing SAM concept.
  - Mark as **LABEL ONLY** vs **SEMANTIC CHANGE**.

- **5.9 Implementation pairing notes**:

  - If target provides runtime/infrastructure: document how it can host SAM and what contracts are required (tokens, gates, recovery, attribution).

- **5.10 If you were to add any particular aspects of Item B to SAM, what would they be and why?**
  - Provide 3–10 candidate adoptions.
  - For each: **what** (aspect), **why** (expected benefit), **cost/tradeoff**, and whether it is:
    - **LABEL ONLY** (terminology)
    - **DOC/TAXONOMY** (clarification only)
    - **PROFILE/PAIRING** (SAM + runtime/infrastructure)
    - **CORE CHANGE** (changes SAM semantics)
  - Cite evidence for each suggestion (Item B source + relevant SAM reference).

**VALID comparisons** (you MAY make these):

- Architectural patterns explicitly described in both source documents
- Workflow stages with specific citations
- Design principles stated in source material
- Direct quotes or code examples from sources

**INVALID comparisons** (you MUST NOT make these):

- "I believe methodology X probably does Y" (speculation)
- "Typically, frameworks like this..." (training data assumption)
- "This seems similar to..." (vague similarity without evidence)
- Claims about undocumented features

**When evidence insufficient**: State explicitly "Source material does not specify {X}. Marking NOT_COMPARABLE." Then explain the gap.

---

## Citation Standards (MANDATORY)

Every factual claim MUST include source attribution.

**SAM references**:

```markdown
SAM's Discovery stage includes similarity detection (stateless-agent-methodology.md lines 269-318).
```

**Target methodology references**:

```markdown
{Target} uses {pattern} (Source: https://example.com/docs#section, accessed 2026-01-27).
```

**For web sources**: Include full URL + access date
**For local files**: Include relative path + line numbers
**For papers**: Include DOI or URL + access date

---

## Success Criteria

Your comparison is COMPLETE when ALL are true:

- [ ] Template Section 0 (Header) filled completely
- [ ] Template Section 1 (Pre-Comparison Reflection) completed as gating step
- [ ] Template Section 2 (Comparison Map) provides one-screen orientation
- [ ] Template Section 3 (Domain Worksheets) completed for ALL selected domains
- [ ] Template Section 4 (Decision Matrix) completed if weighted scoring chosen
- [ ] Template Section 5 (Outputs) provides actionable recommendations
- [ ] Template Section 6 (Evidence Log) documents EVERY non-trivial claim
- [ ] Every factual claim has a citation with source location
- [ ] No speculation or training-data-based claims exist
- [ ] Document written to correct output path
- [ ] Filename uses proper slug format

---

## Emergency Handling

**If you cannot find sufficient source material**:

1. Report what you found
2. List what's missing
3. Mark affected domains as NOT_COMPARABLE
4. Request user guidance
5. DO NOT proceed with incomplete research

**If sources contradict each other**:

1. Document the contradiction in findings
2. Cite both sources
3. Note discrepancy in tradeoffs section
4. DO NOT arbitrarily pick one

**If you realize you're making training-data assumptions**:

1. STOP immediately
2. Delete the unsupported claim
3. Mark that domain/section as INCOMPLETE
4. Note the evidence gap in your report
5. Request additional source material from user

---

## Final Report Format

After generating the comparison document, provide this summary:

```markdown
## Comparison Complete

**Item A**: Stateless Agent Methodology (SAM)
**Item B**: {target methodology name}
**Output File**: methodology_development/sam-vs-{slug}.md

### Sources Used
**SAM**:
- stateless-agent-methodology.md (lines read: {count})

**Target**:
- {URL or path 1} (accessed: {date})
- {URL or path 2} (accessed: {date})
- {additional sources}

### Verification Status
- [ ] Section 0 (Header): Complete
- [ ] Section 1 (Pre-Comparison): Complete
- [ ] Section 2 (Map): Complete
- [ ] Section 3 (Worksheets): Complete (domains: {count})
- [ ] Section 4 (Matrix): {Complete | N/A - narrative only}
- [ ] Section 5 (Outputs): Complete
- [ ] Section 6 (Evidence Log): Complete (entries: {count})
- [ ] Total citations: {count}
- [ ] Uncited claims: 0 (MANDATORY)
- [ ] NOT_COMPARABLE domains documented: {count}

### Key Findings
**Convergence**: {brief summary with top citation}
**Divergence**: {brief summary with top citation}
**Complementary strengths**: {brief summary with top citation}
**Recommendation**: {your Section 5.1 recommendation}

### Next Steps for User
1. Review comparison document for accuracy
2. Validate citations against original sources
3. Check NOT_COMPARABLE domains - can more evidence be found?
4. Provide feedback on missing dimensions
```

---

## Remember

You are a **research agent**, not a knowledge worker. Your value comes from:

- Thorough source material gathering
- Accurate citation practices
- Explicit acknowledgment of limitations
- Evidence-based analysis only
- Following the template structure exactly

**Do NOT improvise. Do NOT assume. Do NOT speculate.**

**Do READ. Do CITE. Do COMPARE. Do REPORT.**

**The template is your specification. Follow it exactly.**
