---
name: questionably-ultrathink
description: |
  Advanced reasoning skill integrating Atom of Thoughts (AoT) and Chain of Verification (CoVe) frameworks.

  Use when facing complex problems requiring rigorous reasoning, systematic decomposition, or factual verification.

  Activation triggers:
  - "be thorough", "analyze carefully", "make sure this is right"
  - Complex multi-part questions
  - Architecture or security decisions
  - "verify", "double-check", "are you sure"
  - High-stakes technical decisions
  - Debugging complex issues
allowed-tools: [Task, Read, Grep, Glob, WebSearch, WebFetch, AskUserQuestion, Bash, Write]
---

# UltraThink Reasoning Framework

You orchestrate advanced reasoning through isolated, verified atomic solving.

<architecture_overview>

## Architecture: Isolated Solving with Question Contraction

### The Problem with Traditional Decomposition

Traditional approaches have a critical flaw: the same agent that generates questions also sees all answers. This creates bias contamination - knowledge of other questions/answers influences each response.

### The Solution: True Factored Execution

1. **Graph Generator** creates ONLY the DAG of questions (no solving)
2. **Atomic Solver** answers ONE question per spawn (complete isolation)
3. **Graph Maintainer** rewrites dependent questions with solved answers (contraction)
4. Each solver sees ONLY its contracted question - nothing else

### Flow Diagram

```
SKILL → Graph Generator (DAG only, no solving)
     ↓
     For each level:
         → Fresh Solver per atom (isolated, only sees question)
         → Graph Maintainer (contracts dependent questions)
     ↓
     Repeat until FINAL solved
     ↓
     Synthesize response
```

</architecture_overview>

<clarification_first>

## Phase 0: Clarify Intent First (MANDATORY)

**ALWAYS start by assessing if clarification is needed.** Before invoking any agents, consider:

* Does the problem have multiple valid interpretations?
* Are scope, constraints, or success criteria unclear?
* Could different priorities lead to different analyses?

If ANY of these apply, use `AskUserQuestion` BEFORE proceeding.

Skip clarification ONLY when the user's intent is unambiguous.
</clarification_first>

<rigor_selection>

## Phase 0.5: Select Analysis Rigor

After clarifying intent, determine the analysis depth:

```
question: "What level of analysis rigor do you need?"
header: "Rigor"
options:
  - label: "Standard (Recommended)"
    description: "Single pass through the DAG. Good for most questions."
  - label: "Thorough"
    description: "Re-solves atoms with LOW confidence. Takes longer but more reliable."
  - label: "High-Stakes"
    description: "Maximum rigor. Re-solves any atom below HIGH confidence. Use for security, architecture, or production decisions."
```

**Skip this question if:**

* User already specified rigor in their request (e.g., "be thorough", "this is high-stakes")
* Query is simple enough that standard analysis is obviously sufficient
</rigor_selection>

<available_agents>

## Available Agents

**CRITICAL WARNING:** You are the orchestrator. NEVER invoke yourself.

### aot-graph-generator

**Purpose:** Build the DAG structure of atomic questions (NO solving)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-graph-generator"`

**Input:** Session ID, rigor level, clarified query
**Output:** metadata.md + atom files with questions only (status: unsolved)

### aot-graph-maintainer

**Purpose:** Contract unsolved atom questions with solved answers
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-graph-maintainer"`

**Input:** Session ID, list of solved atoms with answers
**Output:** Rewrites dependent atom questions with "Given..." context

### cove-atomic-solver

**Purpose:** Answer ONE atomic question in complete isolation with self-verification
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:cove-atomic-solver"`

**Input:** The question text ONLY (extracted from atom file)
**Output:** Verified answer with sources, verification trace, and confidence (numerical + categorical)

**CRITICAL:** Pass ONLY the question text to cove-atomic-solver. Do NOT pass session ID, atom ID, or any other context.

### aot-judge (Optional - High-Stakes Only)

**Purpose:** Evaluate answer quality across atoms at a level (coherence, contradictions, completeness)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-judge"`

**Input:** Session ID, level number, list of solved atoms to evaluate
**Output:** Evaluation report with specific atoms flagged for re-solve (if issues found)

**Use when:**

* Rigor level is High-Stakes
* After solving all atoms at a level
* When you want additional quality assurance beyond self-verification

**Note:** The judge does NOT re-answer questions. It evaluates existing answers for quality issues.
</available_agents>

<full_pipeline>

## Full Pipeline Orchestration

You orchestrate the full pipeline by chaining agent calls. Follow these phases exactly.

<phase_1>

### Phase 1: Generate Session & Build Graph

**Step 1.1: Generate Session ID**

Generate a short session ID (8 characters, alphanumeric):

```
Example: a1b2c3d4
```

**Step 1.2: Invoke Graph Generator**

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-graph-generator"
- prompt: "Session ID: {session-id}. Rigor: {rigor-level}. Build the question DAG for this query: {clarified query}"
```

**What this produces:**

* `.questionably-ultrathink/{session-id}/metadata.md` with DAG structure
* `.questionably-ultrathink/{session-id}/atoms/*.md` with questions only (status: unsolved)

**Step 1.3: Read Metadata**

Read the metadata file to get the solve order:

```
Read: .questionably-ultrathink/{session-id}/metadata.md
```

Extract `solve_order` - the list of atoms grouped by level.
</phase_1>

<phase_2>

### Phase 2: Iterative Solve Loop

Process each level in order:

**For each level in solve_order:**

**Step 2a: Read atom questions at this level**

For each atom at the current level:

```
Read: .questionably-ultrathink/{session-id}/atoms/{atom-id}.md
```

Extract the question text (may be contracted if level > 0).

**Step 2b: Spawn FRESH solver for each atom (PARALLEL)**

For each atom at this level, invoke a fresh solver with ONLY the question:

```
Task tool:
- subagent_type: "questionably-ultrathink:cove-atomic-solver"
- prompt: "{the question text only, nothing else}"
```

**CRITICAL:**

* Pass ONLY the question text
* NO session ID, NO atom ID, NO "verify atom X" language
* The solver must be completely isolated

**Invoke ALL atoms at the same level in parallel** (single message with multiple Task calls).

**Step 2c: Extract answers and update atom files**

For each solved atom, YOU (the orchestrator) update the atom file:

Read the solver's output and extract:

* The initial answer (before verification)
* The self-verification section (all claims and their verification status)
* The final answer (after any revisions)
* Sources
* Confidence level (both numerical 0-1 and categorical)

Write the updated atom file with FULL verification trace:

```markdown
---
atom_id: {atom-id}
level: {level}
dependencies: [{deps}]
status: solved
contracted: {true if was contracted}
solved_at: {ISO timestamp when solving completed}
solve_attempts: {number, starting at 1}
parallel_group: [{list of atom IDs solved in same parallel batch}]
confidence_score: {0.0-1.0 numerical score}
---

# Question
{the question}

# Verification Trace

## Initial Answer
{The solver's first formulation before self-verification}

## Self-Verification

**Claim 1:** "{specific claim from initial answer}"
- Verification Q: {independent question the solver asked}
- Independent Answer: {answer without bias}
- Status: ✓ VERIFIED | ⚠️ REVISED | ❓ UNCERTAIN

**Claim 2:** ...
{Include ALL claims the solver verified}

# Answer
{the final verified/revised answer}

# Sources
- {source 1}
- {source 2}

# Confidence
{0.XX} ({HIGH | MEDIUM | LOW}) - {explanation}
```

**IMPORTANT:** Preserve the FULL verification trace from the solver's output. This provides:

* Audit trail for how answers were derived
* Ability to diagnose LOW confidence atoms
* Evidence for re-solve decisions

**Step 2d: Contract dependent atoms**

If there are more levels to process, invoke the graph maintainer:

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-graph-maintainer"
- prompt: "Session ID: {session-id}. Solved atoms:
  - A1: {answer summary}
  - A2: {answer summary}"
```

This rewrites next-level atom questions with the solved answers as "Given..." context.

**Step 2e: Continue to next level**

Repeat 2a-2d for each level until FINAL is solved.
</phase_2>

<phase_3>

### Phase 3: Synthesize Final Response

After FINAL is solved:

1. Read all solved atom files
2. Combine answers into coherent response
3. Apply appropriate confidence markers

The FINAL atom's answer IS your synthesis - it was designed as the synthesis question.
</phase_3>

<rigor_based_iteration>

### Rigor-Based Re-Solving

After completing all levels, check confidence based on rigor:

| Rigor Level | Re-solve When | Confidence Threshold |
|-------------|---------------|---------------------|
| Standard | Never (single pass) | N/A |
| Thorough | Any atom has LOW confidence | score < 0.4 |
| High-Stakes | Any atom below HIGH confidence | score < 0.7 |

**Confidence Score Mapping:**

* 0.0 - 0.4 = LOW
* 0.4 - 0.7 = MEDIUM
* 0.7 - 1.0 = HIGH

**Status Lifecycle:**

```
unsolved → in_progress → solved → (needs_re_solve → in_progress → solved) → verified
```

1. `unsolved` - Initial state from graph generator
2. `in_progress` - Currently being solved (mark BEFORE spawning solver)
3. `solved` - Solver completed (mark after extracting answer)
4. `needs_re_solve` - Confidence below threshold for rigor level
5. `verified` - Passed rigor check (final state)

**If re-solving needed:**

1. Mark atoms needing re-solve with `status: needs_re_solve`
2. Increment `solve_attempts` counter
3. For each, spawn a fresh solver with the same question
4. Update atom files with new answers (preserve previous attempt in trace)
5. If dependencies changed, re-contract and re-solve dependents

**Early Stop Conditions:**

* No confidence improvement after re-solve (converged)
* `solve_attempts` reaches 3 (prevent infinite loops)

**For High-Stakes rigor (optional judge step):**

After solving all atoms at a level, you MAY invoke the optional judge agent:

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-judge"
- prompt: "Session ID: {session-id}. Level: {level}. Evaluate answers for coherence, contradictions, and completeness."
```

The judge evaluates answer quality without re-answering. If issues found, mark specific atoms for re-solve with judge feedback.
</rigor_based_iteration>

</full_pipeline>

<pipeline_output_format>

## Pipeline Output Format

Use this structure for your final output:

```
## UltraThink Analysis

### Original Query
{The user's question}

### Analysis Settings
- **Rigor Level**: {Standard | Thorough | High-Stakes}
- **Session ID**: {session-id}

### Phase 1: Graph Construction

**Dependency Graph:**
```
Level 0: A1, A2 (independent)
Level 1: A3 ← [A1, A2]
Level 2: FINAL ← [A3]
```

### Phase 2: Iterative Solving

**Level 0** (parallel):
- [A1] {question} → {answer} (confidence: HIGH)
- [A2] {question} → {answer} (confidence: MEDIUM)

*Contracting A3 with A1, A2 answers...*

**Level 1**:
- [A3] "Given {A1}, {A2}, {question}?" → {answer} (confidence: HIGH)

*Contracting FINAL with A3 answer...*

**Level 2**:
- [FINAL] "Given {A3}, {synthesis question}?" → {answer}

### Phase 3: Synthesis

{The FINAL atom's verified answer}

### Final Response

{Clean presentation of the answer}

### Confidence Assessment

| Atom | Confidence | Notes |
|------|------------|-------|
| A1 | HIGH | {notes} |
| A2 | MEDIUM | {notes} |
| A3 | HIGH | {notes} |
| FINAL | HIGH | {notes} |

**Overall Confidence:** {HIGH | MEDIUM | LOW}

### Uncertainty Flags
{Any remaining areas of uncertainty}
```

</pipeline_output_format>

<quick_reference>

## Quick Reference

| Situation | Action |
|-----------|--------|
| Multi-part question | Run full pipeline |
| User requests verification | Run full pipeline |
| High-stakes decision | Run full pipeline with high-stakes rigor |
| Simple factual question | Skip UltraThink, answer directly |

</quick_reference>

<skip_ultrathink>

## When to Use Standard Responses

Skip UltraThink for:

* Simple, direct questions with single answers
* Opinion/recommendation requests (no facts to verify)
* Quick lookups where user prioritizes speed
* Questions where you have high confidence already
</skip_ultrathink>

<confidence_markers>

## Confidence Markers

After using UltraThink, mark your confidence:

* **[VERIFIED]** - All atoms passed self-verification
* **[HIGH CONFIDENCE]** - Most atoms HIGH, no LOW
* **[NEEDS EXTERNAL VERIFICATION]** - User should confirm externally
* **[UNCERTAIN]** - Significant LOW confidence atoms remain
</confidence_markers>

You must execute the questionably-ultrathink workflow.
