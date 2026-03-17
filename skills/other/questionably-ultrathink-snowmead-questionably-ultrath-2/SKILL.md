---
name: questionably-ultrathink-skill
description: |
  Use this skill when facing complex problems requiring rigorous reasoning, systematic decomposition, or factual verification.

  Activation triggers:

  * "be thorough", "analyze carefully", "make sure this is right"
  * Complex multi-part questions
  * Architecture or security decisions
  * "verify", "double-check", "are you sure"
  * High-stakes technical decisions
  * Debugging complex issues
allowed-tools: [Task, Read, Grep, Glob, WebSearch, WebFetch, AskUserQuestion, Bash, Write]
---

# UltraThink Reasoning Framework

You orchestrate advanced reasoning through isolated, verified atomic solving.

\<architecture\_overview>

## Architecture: Isolated Solving with Factored Verification

### The Problem with Traditional Decomposition

Traditional approaches have a critical flaw: the same agent that generates questions also sees all answers. This creates bias contamination - knowledge of other questions/answers influences each response.

### The Solution: True Factored Execution

1. **Graph Generator** creates ONLY the DAG of questions (no solving)
2. **Claim Generator (cove-claim-qs)** generates claims and verification questions (NO fact-checking)
3. **Verifiers** research and answer verification questions in COMPLETE ISOLATION (no context about claims)
4. **Verification Maintainer** cross-checks claims vs verifier answers, synthesizes final answer
5. **Graph Maintainer** rewrites dependent questions with solved answers (contraction)

**Key insight:** Only cove-verifier does actual research/fact-checking. All other agents either generate structure or process verified facts.

### Factored Verification Flow (Per Atom)

```
ORCHESTRATOR (you)
    │
    ├─(1)─► cove-claim-qs
    │           │  Input: ATOM_DIR
    │           └──► reads question.md
    │               writes claims.md
    │               writes verifiers/{N}.md (ONLY question, no claim text)
    │               returns "CLAIMS_GENERATED"
    │
    ├─(2)─► reads claims.md frontmatter to get claim_count
    │
    ├─(3)─► cove-verifier #1 ──► reads/overwrites verifiers/1.md, returns "VERIFIER_DONE"
    ├─(3)─► cove-verifier #2 ──► reads/overwrites verifiers/2.md, returns "VERIFIER_DONE" (PARALLEL)
    ├─(3)─► cove-verifier #N ──► reads/overwrites verifiers/N.md, returns "VERIFIER_DONE"
    │           │  Input: VERIFIER_FILE (pre-created with ONLY the question)
    │           └──► Verifier has ZERO context about the claim
    │
    └─(4)─► cove-verification-maintainer
                │  Input: ATOM_DIR only
                │  (reads claims.md + verifiers/*.md itself)
                │
                └──► creates answer.md (final answer + verification trace), returns "VERIFICATION_COMPLETE"
```

**Key Principles:**
- State is determined by FILE EXISTENCE and CONTENT
- `question.md` exists → atom created
- `claims.md` exists → claims generated
- `verifiers/{N}.md` exists with question only → pre-created by cove-claim-qs, ready for verifier
- `verifiers/{N}.md` has "# Answer" section → verification question answered
- `answer.md` exists → verification complete, final answer synthesized
- You only read: metadata.md (DAG structure), claims.md frontmatter (claim_count), FINAL/answer.md (at end)
- Agents return minimal confirmations - they read/write files themselves

\</architecture\_overview>

\<background\_execution>

## Background Execution for Pipeline Parallelism

You can run subagents in the background to advance multiple independent paths simultaneously instead of waiting sequentially. This dramatically improves throughput when processing multiple atoms.

### When to Use Background Execution

Use `run_in_background: true` in Task tool calls when:

* Multiple atoms at the same level need verification independently
* Verification for one atom doesn't depend on another atom's verification
* You want to start the next atom's pipeline while waiting on verifier responses

### Pattern: Parallel Pipeline Advancement

Instead of waiting for ALL verifiers to complete before moving to the next atom:

```
SEQUENTIAL (slow):
A1: claims → verifiers → wait → maintainer → done
A2: claims → verifiers → wait → maintainer → done
```

Use background execution for pipeline parallelism:

```
PARALLEL PIPELINE (fast):
A1: claims → verifiers (background)
A2: claims → verifiers (background)
A1: check verifier files → maintainer (when ready)
A2: check verifier files → maintainer (when ready)
```

### How to Use Background Execution

**Step 1: Spawn verifiers in background**

```
Task tool:
- subagent_type: "questionably-ultrathink:cove-verifier"
- prompt: |
    VERIFIER_FILE: .questionably-ultrathink/{session-id}/atoms/{atom-id}/verifiers/{N}.md
- run_in_background: true
```

This returns immediately with an `output_file` path and task ID.

**Step 2: Continue to next atom**

While verifiers run in background, spawn the next atom's claim generator and verifiers.

**Step 3: Check on background tasks**

Use `TaskOutput` tool or `Read` the output file to check if background tasks completed:

```
TaskOutput tool:
- task_id: "{task_id}"
- block: false  # Non-blocking check
```

Or use Grep to check if verifier files have been completed (have "# Answer" section):

```
Grep: "# Answer" in .questionably-ultrathink/{session-id}/atoms/{atom-id}/verifiers/{N}.md
```

**Step 4: Process completed verification**

Once an atom's verifiers are all complete (all verifier files have "# Answer" sections), spawn its verification maintainer. You can do this while other atoms' verifiers are still running.

### Example: Level 0 with A1 and A2

```
1. Spawn cove-claim-qs for A1 and A2 (parallel, blocking)
   - This creates claims.md AND verifiers/{N}.md files (with just questions)

2. Read claims.md frontmatter from A1 → spawn N verifiers with VERIFIER_FILE paths (run_in_background: true)
3. Read claims.md frontmatter from A2 → spawn N verifiers with VERIFIER_FILE paths (run_in_background: true)

4. Check A1 verifiers (Grep for "# Answer" in verifier files)
   - If all complete → spawn A1's cove-verification-maintainer
   - If not → continue

5. Check A2 verifiers (Grep for "# Answer" in verifier files)
   - If all complete → spawn A2's cove-verification-maintainer
   - If not → continue

6. Repeat checks until all maintainers have run (all atoms have answer.md)
7. Proceed to contract and next level
```

### Guidelines

* **Claim generators can run in parallel but should block** - You need `claims.md` to know the claim count
* **Verifiers should run in background** - They're independent and you can advance other atoms while waiting
* **Maintainers should block** - You need `answer.md` created before contracting
* **Track task IDs** - Keep a list of background task IDs so you can check on them
* **Balance parallelism** - Don't spawn too many background tasks; group by atom for manageable tracking

\</background\_execution>

\<clarification\_first>

## Phase 0: Clarify Intent First (MANDATORY)

**ALWAYS start by assessing if clarification is needed.** Before invoking any agents, consider:

* Does the problem have multiple valid interpretations?
* Are scope, constraints, or success criteria unclear?
* Could different priorities lead to different analyses?

If ANY of these apply, use `AskUserQuestion` BEFORE proceeding.

Skip clarification ONLY when the user's intent is unambiguous.
\</clarification\_first>

\<rigor\_selection>

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
  \</rigor\_selection>

\<available\_agents>

## Available Agents

**CRITICAL WARNING:** You are the orchestrator. NEVER invoke yourself. Only YOU can spawn agents via the Task tool.

### aot-graph-generator

**Purpose:** Build the DAG structure of atomic questions (NO solving)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-graph-generator"`

**Input:** Session ID, rigor level, clarified query
**Output:** Creates `metadata.md` + `atoms/{id}/question.md` for each atom

### cove-claim-qs

**Purpose:** Generate claims, verification questions, AND pre-create verifier files for ONE atomic question (NO fact-checking)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:cove-claim-qs"`

**Input:** `ATOM_DIR` path (reads `question.md` itself)
**Output:** Creates `claims.md` AND `verifiers/{N}.md` files in atom directory, returns `CLAIMS_GENERATED: {atom-id}`

**CRITICAL:** This agent does NOT research or fact-check. It:
1. Generates claims and verification questions → writes to `claims.md`
2. Pre-creates verifier files with ONLY the question → writes to `verifiers/{N}.md`

The verifier files contain ONLY the verification question (no claim text). This ensures factored verification - verifiers can't be biased toward confirming claims they never see.

### cove-verifier

**Purpose:** Research and answer ONE verification question in complete isolation (no context about the claim being verified)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:cove-verifier"`

**Input:** `VERIFIER_FILE` path (the pre-created file containing ONLY the verification question)
**Output:** Overwrites `VERIFIER_FILE` with question + answer + confidence + sources, returns `VERIFIER_DONE`

**CRITICAL:** The verifier reads ONLY its pre-created file which contains ONLY the verification question. It has ZERO knowledge of the claim text. This is the key to factored verification - the verifier cannot be biased toward confirming a claim it never sees.

### cove-verification-maintainer

**Purpose:** Cross-check claims against independent verifier answers; synthesize final answer
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:cove-verification-maintainer"`

**Input:** `ATOM_DIR` only (reads `claims.md` and `verifiers/*.md` itself)
**Output:** Creates `answer.md` in atom directory, returns `VERIFICATION_COMPLETE: {atom-id}`

### aot-graph-maintainer

**Purpose:** Contract unsolved atom questions with solved answers from dependencies
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-graph-maintainer"`

**Input:** `SESSION_DIR` only (reads metadata.md and answer.md files to discover solved atoms)
**Output:** Updates `question.md` files for dependent atoms, returns `CONTRACTION_COMPLETE: {count}`

### aot-judge (Optional - High-Stakes Only)

**Purpose:** Evaluate answer quality across atoms at a level (coherence, contradictions, completeness)
**Invoke:** `Task` tool with `subagent_type: "questionably-ultrathink:aot-judge"`

**Input:** Session ID and level number
**Output:** Returns `JUDGE_RESULT: {PASS|ISSUES}` and `RE_SOLVE: [{atom-ids or "none"}]`

**Use when:**

* Rigor level is High-Stakes
* After solving all atoms at a level
* When you want additional quality assurance beyond factored verification
\</available\_agents>

\<full\_pipeline>

## Full Pipeline Orchestration

You orchestrate the full pipeline by chaining agent calls. Follow these phases exactly.

\<phase\_1>

### Phase 1: Generate Session & Build Graph

**Step 1.1: Generate Session ID**

Generate a short session ID (8 characters, alphanumeric):

```
Example: a1b2c3d4
```

**Step 1.2: Create Session Directory**

```bash
mkdir -p .questionably-ultrathink/{session-id}/atoms
```

Note: Verifier directories are created inside each atom folder by the verifier agents.

**Step 1.3: Get Timestamp and Invoke Graph Generator**

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-graph-generator"
- prompt: |
    SESSION_ID: {session-id}
    TIMESTAMP: {ISO timestamp from `date -u`}
    RIGOR: {rigor-level}
    QUERY: {clarified query}
```

**Expected response:** `GRAPH_CREATED: {atom-count}`

**What this produces:**

* `.questionably-ultrathink/{session-id}/metadata.md` with DAG structure (immutable)
* `.questionably-ultrathink/{session-id}/atoms/{id}/question.md` for each atom

**Step 1.4: Read Metadata**

Read the metadata file to get the solve order:

```
Read: .questionably-ultrathink/{session-id}/metadata.md
```

Extract `solve_order` - the list of atoms grouped by level.
\</phase\_1>

\<phase\_2>

### Phase 2: Iterative Solve Loop with Factored Verification

Process each level in order. **State is determined by file existence:**

- `question.md` exists → atom created
- `claims.md` exists → claims generated, ready for verification
- `answer.md` exists → verification complete

**For each level in solve\_order:**

**Step 2a: Check atom states using Glob**

For each atom at the current level, check which files exist:

```
Glob: .questionably-ultrathink/{session-id}/atoms/{atom-id}/claims.md
Glob: .questionably-ultrathink/{session-id}/atoms/{atom-id}/answer.md
```

This determines where each atom is in the pipeline.

**Step 2b: Spawn cove-claim-qs for atoms missing claims.md (PARALLEL)**

For atoms where `claims.md` does NOT exist, spawn the claim generator:

```
Task tool:
- subagent_type: "questionably-ultrathink:cove-claim-qs"
- prompt: |
    ATOM_DIR: .questionably-ultrathink/{session-id}/atoms/{atom-id}
```

**Expected response:** `CLAIMS_GENERATED: {atom-id}`

**CRITICAL:**

* The agent reads `question.md` and writes `claims.md` itself
* It generates claims and verification questions only
* It does NOT research or fact-check (cove-verifier does that)

**Invoke ALL atoms at the same level in parallel** (single message with multiple Task calls).

**Step 2c: Read claims.md frontmatter to get claim count**

For atoms with `claims.md` but missing `answer.md`, read ONLY the frontmatter to get `claim_count`:

```
Read: .questionably-ultrathink/{session-id}/atoms/{atom-id}/claims.md
```

Extract `claim_count` from frontmatter - this tells you how many verifiers to spawn.

**Step 2d: Check which verifiers are complete and spawn for incomplete ones (PARALLEL or BACKGROUND)**

The verifier files were pre-created by cove-claim-qs with ONLY the verification question. Check which have been completed (have an Answer section):

```
Grep: "# Answer" in .questionably-ultrathink/{session-id}/atoms/{atom-id}/verifiers/*.md
```

Or check file size - pre-created files are small (question only), completed files are larger.

For each INCOMPLETE verifier file (1 to claim_count), spawn a fresh verifier:

```
Task tool:
- subagent_type: "questionably-ultrathink:cove-verifier"
- prompt: |
    VERIFIER_FILE: .questionably-ultrathink/{session-id}/atoms/{atom-id}/verifiers/{N}.md
- run_in_background: true  # Optional: enables pipeline parallelism
```

**Expected response:** `VERIFIER_DONE`

**CRITICAL:**

* The verifier file was pre-created by cove-claim-qs with ONLY the verification question
* The verifier reads this file and has ZERO context about the claim being verified
* It overwrites the file with question + answer + confidence + sources
* This is what makes it "factored" verification - complete isolation

**Parallelization options:**

1. **Parallel within atom (blocking):** Invoke ALL verifiers for one atom in parallel (single message with multiple Task calls). Wait for completion before moving to next atom.

2. **Background for pipeline parallelism (recommended):** Spawn verifiers with `run_in_background: true`. This lets you immediately start the next atom's verification while the first atom's verifiers run. Check on background tasks with `TaskOutput` (block: false) and spawn maintainers as each atom's verifiers complete. See `<background_execution>` section for details.

**Step 2e: Wait for verifiers to complete**

**For blocking calls:** Verifiers return `VERIFIER_DONE` when complete.

**For background calls:** Use `TaskOutput` tool to check completion:

```
TaskOutput tool:
- task_id: "{task_id from background spawn}"
- block: true   # Wait for completion
- timeout: 30000  # 30 second timeout
```

Or use `block: false` to check without waiting (for pipeline advancement).

**Checking verifier completion:** Verifier files at `.questionably-ultrathink/{session-id}/atoms/{atom-id}/verifiers/{N}.md` are pre-created with just the question. A completed verifier file has an "# Answer" section added by the verifier agent.

**Step 2f: Spawn verification maintainer when all verifiers are complete**

When all verifier files have been completed (all have "# Answer" sections), spawn the maintainer:

```
Task tool:
- subagent_type: "questionably-ultrathink:cove-verification-maintainer"
- prompt: |
    ATOM_DIR: .questionably-ultrathink/{session-id}/atoms/{atom-id}
```

**Expected response:** `VERIFICATION_COMPLETE: {atom-id}`

The maintainer will:

* Read `claims.md` to get claims and verification questions
* Read `verifiers/*.md` files from the atom directory
* Compare each claim to its verification answer
* Mark claims as VERIFIED, REVISED, REFUTED, or UNCERTAIN
* Synthesize the final answer from verified facts
* Create `answer.md` with the full verification trace

**Step 2g: Contract dependent atoms**

After ALL atoms at current level have `answer.md`, invoke the graph maintainer:

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-graph-maintainer"
- prompt: |
    SESSION_DIR: .questionably-ultrathink/{session-id}
```

**Expected response:** `CONTRACTION_COMPLETE: {count}`

The maintainer will:
* Read `metadata.md` for the DAG structure
* Read `answer.md` from solved atoms to get their answers
* Update `question.md` for next-level atoms with "Given..." context

**Step 2h: Continue to next level**

Repeat 2a-2g for each level until FINAL has `answer.md`.
\</phase\_2>

\<phase\_3>

### Phase 3: Synthesize Final Response

After FINAL has `answer.md`:

```
Read: .questionably-ultrathink/{session-id}/atoms/FINAL/answer.md
```

The FINAL atom's answer IS your synthesis - it was designed as the synthesis question. Present this answer to the user with appropriate confidence markers.

**You only read FINAL/answer.md** - all other atom answers have already been incorporated through contraction.
\</phase\_3>

\<rigor\_based\_iteration>

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

**Checking Confidence:**

Read the `answer.md` frontmatter for each atom to get its `confidence_score`:

```
Read: .questionably-ultrathink/{session-id}/atoms/{atom-id}/answer.md
```

**If re-solving needed:**

1. Delete the `claims.md` and `answer.md` files (and `verifiers/` directory) for atoms needing re-solve
2. Spawn a fresh cove-claim-qs to regenerate claims
3. Run the full factored verification pipeline again
4. If dependencies changed, re-contract and re-solve dependents

**Early Stop Conditions:**

* No confidence improvement after re-solve (converged)
* Re-solve attempts reach 3 (track this in your orchestration state)

**For High-Stakes rigor (optional judge step):**

After solving all atoms at a level, you MAY invoke the optional judge agent:

```
Task tool:
- subagent_type: "questionably-ultrathink:aot-judge"
- prompt: "Session ID: {session-id}. Level: {level}. Evaluate answers for coherence, contradictions, and completeness."
```

The judge evaluates answer quality without re-answering. If issues found, delete the relevant files and re-run the pipeline for those atoms.
\</rigor\_based\_iteration>

\</full\_pipeline>

\<pipeline\_output\_format>

## Pipeline Output Format

Use this structure for your final output:

````
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

### Phase 2: Iterative Solving with Factored Verification

**Level 0** (parallel):
- [A1] {question}
  - Initial answer: {answer}
  - Verification: {N claims verified, M revised}
  - Final confidence: HIGH

- [A2] {question}
  - Initial answer: {answer}
  - Verification: {N claims verified}
  - Final confidence: MEDIUM

*Contracting A3 with A1, A2 answers...*

**Level 1**:
- [A3] "Given {A1}, {A2}, {question}?"
  - Initial answer: {answer}
  - Verification: {N claims verified}
  - Final confidence: HIGH

*Contracting FINAL with A3 answer...*

**Level 2**:
- [FINAL] "Given {A3}, {synthesis question}?"
  - Final answer: {answer}

### Phase 3: Synthesis

{The FINAL atom's verified answer}

### Final Response

{Clean presentation of the answer}

### Confidence Assessment

| Atom | Initial | After Verification | Notes |
|------|---------|-------------------|-------|
| A1 | 0.75 | 0.90 | All claims verified |
| A2 | 0.60 | 0.55 | 1 claim revised |
| A3 | 0.80 | 0.85 | All claims verified |
| FINAL | 0.85 | 0.85 | All claims verified |

**Overall Confidence:** {HIGH | MEDIUM | LOW}

### Uncertainty Flags
{Any remaining areas of uncertainty}
````

\</pipeline\_output\_format>

\<quick\_reference>

## Quick Reference

| Situation | Action |
|-----------|--------|
| Multi-part question | Run full pipeline |
| User requests verification | Run full pipeline |
| High-stakes decision | Run full pipeline with high-stakes rigor |
| Simple factual question | Skip UltraThink, answer directly |

\</quick\_reference>

\<skip\_ultrathink>

## When to Use Standard Responses

Skip UltraThink for:

* Simple, direct questions with single answers
* Opinion/recommendation requests (no facts to verify)
* Quick lookups where user prioritizes speed
* Questions where you have high confidence already
  \</skip\_ultrathink>

\<confidence\_markers>

## Confidence Markers

After using UltraThink, mark your confidence:

* **\[VERIFIED]** - All atoms passed factored verification, all claims verified
* **\[HIGH CONFIDENCE]** - Most atoms HIGH, no LOW, minor revisions only
* **\[NEEDS EXTERNAL VERIFICATION]** - User should confirm externally
* **\[UNCERTAIN]** - Significant LOW confidence atoms or many revised claims
  \</confidence\_markers>

You must execute the questionably-ultrathink workflow.
