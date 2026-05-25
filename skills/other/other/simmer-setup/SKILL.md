---
name: simmer-setup
description: >
  Setup subskill for simmer. Inspects the artifact or workspace, infers evaluation
  contracts and search space, proposes a complete assessment to the user, and produces
  a setup brief after confirmation. Conversational, not form-based — the agent does
  the work of understanding the problem, then presents what it found. Do not invoke
  directly — called by simmer orchestrator.
---

# Simmer Setup

Inspect the artifact, infer what "better" means and how to measure it, propose an assessment to the user, produce the setup brief that drives the entire refinement loop.

**Core principle:** Inspect first, infer second, propose third, confirm last. The agent does the thinking — the user validates, adjusts, or overrides. Never ask the user to describe something the agent can read.

## Phase 1: Identify and Inspect

### Identify the Artifact

Look for:
- A file path mentioned or open in context
- Text pasted by the user
- A directory path or workspace
- A description of something to generate from scratch (seedless mode)

If ambiguous, ask once:

```
What are we refining?
1. A file (give me the path)
2. Something you'll paste
3. A workspace/directory (give me the path)
4. Generate from a description (I'll create the starting point)
```

Set mode and artifact type:

| Mode | Artifact Type | When |
|------|--------------|------|
| **from-file** | single-file | User provides a file path |
| **from-paste** | single-file | User pastes content |
| **from-workspace** | workspace | User provides a directory path |
| **seedless** | single-file or workspace | User describes what to create |

### Inspect the Artifact

**For single-file (from-file or from-paste):**
- Read the file/content
- Identify what kind of artifact it is (prose, code, prompt, config, etc.)
- Note any evaluator references (test commands, benchmark scripts mentioned in comments)
- Note any output format expectations visible in the content

**For workspace (from-workspace):**
- List the directory contents
- Read key files: config files, entry points, scripts, READMEs
- Look specifically for:
  - **Evaluator scripts**: files named `evaluate.*`, `test.*`, `benchmark.*`, or scripts referenced in configs/READMEs
  - **Validation scripts**: files named `validate.*`, `check.*`, or quick-test variants
  - **Config files**: `config.json`, `config.yaml`, `.env`, etc. — these reveal what parameters can be varied
  - **Output examples**: any sample output, expected output, or ground truth files
  - **Strategy/plugin dirs**: directories like `strategies/`, `plugins/`, `models/` that indicate extensibility points
  - **Prompt files**: `prompt.md`, `system.txt`, template files — things the generator can modify

**For seedless:**
- No inspection needed — work from the user's description
- Classify the artifact type from the description

## Phase 2: Classify and Infer

### Problem Class Detection

Infer the problem class from what you found during inspection. **Never ask the user what class this is.**

```
IF mode == "seedless" AND description is prose/creative:
    → text/creative

ELSE IF artifact_type == "workspace" AND (evaluator script found OR user mentioned evaluator):
    → pipeline/engineering

ELSE IF evaluator found OR artifact is code:
    → code/testable

ELSE:
    → text/creative
```

### What to Infer Per Class

**Text/Creative — infer criteria only:**
- Suggest 2-3 criteria based on the artifact type (see seed criteria table below)
- No contracts, no evaluator, no search space
- This path should feel lightweight

**Code/Testable — infer criteria + evaluation:**
- Suggest criteria based on the code's purpose
- If an evaluator script was found, note it as the proposed evaluator
- If the code produces structured output, infer the output contract from its format
- Note any constraints visible in the code (model references, API endpoints, etc.)

**Pipeline/Engineering — infer everything:**
- **Criteria**: from evaluator output metrics (if evaluator script is readable, look at what it measures)
- **Evaluator**: the evaluator script found during inspection
- **Output contract**: from pipeline output format, evaluator expectations, or example output
- **Validation command**: any quick-test script found, or propose a subset run (e.g., "run on 1 input instead of all N")
- **Search space**: from config parameters (models, temperatures, strategies), extensibility points (strategy dirs), and prompt files
- **Background**: from config values (API endpoints, model names already configured), directory structure

### Seed Criteria Table

Use when proposing criteria. The agent should prefer criteria inferred from the actual artifact over these generic seeds.

| Artifact type | Suggested criteria |
|---|---|
| Document / spec | clarity, completeness, actionability |
| Creative writing | narrative tension, specificity, voice consistency |
| Email / comms | value prop clarity, tone match, call to action strength |
| Prompt / instructions | instruction precision, output predictability, edge case coverage |
| API design | contract completeness, developer ergonomics, consistency |
| Code (non-cookoff) | simplicity, robustness, readability |
| Adventure hook / game content | narrative tension, player agency, specificity |
| Blog post / article | argument clarity, engagement, structure |
| Pipeline / workflow | coverage, efficiency, noise |
| Configuration / infra | correctness, resource efficiency, maintainability |

## Phase 3: Propose or Proceed

**Sufficiency check:** Before proposing, check whether the user's initial prompt + inspection results already provide everything needed for the brief:
- Artifact identified? (path, content, or description)
- Criteria determinable? (user stated them, or inferable from evaluator)
- Primary criterion stated? (user said it, or not applicable for text/creative)
- Evaluation method known? (evaluator script found, or judge-only for text)
- Iteration count? (user stated, or default 3)

**If all fields are covered** (from user prompt + inspection), skip the proposal and go directly to Phase 5 (emit brief). This is the common case when running as a subagent — the calling prompt provides intent/constraints and inspection fills in contracts.

**If some fields are missing or ambiguous**, present everything you inferred as a single conversational assessment. The user confirms, adjusts, or overrides. **This is ONE message, not a sequence of questions.**

### Text/Creative Assessment

```
This is a [artifact type] — I'll use judge-only evaluation (no scripts to run).

For criteria, I'd suggest:
- [criterion 1]: [inferred description of what good looks like]
- [criterion 2]: [inferred description]
- [criterion 3]: [inferred description]

3 iterations, starting from [seed description].
Sound right, or want to adjust anything?
```

### Code/Testable Assessment

```
This is [what the code does]. I found [evaluator/test script] which I'll
use to evaluate each iteration.

For criteria:
- [criterion 1]: [inferred from evaluator metrics or code purpose]
- [criterion 2]: [inferred]
- [criterion 3]: [inferred]

[If output contract inferred]: Output should be [format description].
[If constraints found]: I see [model/API/resource constraints].

3 iterations. Which criterion matters most, or are they equal?
```

### Pipeline/Engineering Assessment

```
This is a pipeline optimization problem. Here's what I found:

**Evaluator:** [script path] — measures [what it measures, from reading the script]
**Output contract:** [inferred from pipeline output format / evaluator expectations]
**Validation:** [script path or proposed subset command] — [what it checks, estimated time]
**Search space:** [inferred from config + directory structure]
  - Models: [from config values]
  - Prompts: [prompt files found]
  - Topology: [strategy dirs, extensibility points]

For criteria:
- [criterion 1]: [from evaluator metrics] — [primary?]
- [criterion 2]: [from evaluator metrics]
- [criterion 3]: [from evaluator metrics]

**Constraints:** [API endpoints, available infrastructure from config]

[N] iterations. Does this look right? Anything to add or change?
```

### What the User Can Do

The user can:
- **Confirm as-is** ("looks good", "yes", "go") → proceed to brief
- **Adjust specifics** ("change the primary to X", "add Y to search space") → incorporate and proceed
- **Override** ("no, the evaluator is actually X", "ignore that script") → replace inferred value
- **Add information** ("I also have models A and B available", "budget is $X") → merge into brief
- **Ask for clarification** ("what does the evaluator actually measure?") → explain, then re-propose

**One round of confirmation is the goal.** If the user's adjustments are clear, incorporate them and emit the brief. Don't re-propose unless the user asks to see the updated assessment.

## Phase 4: Elicit What's Missing

After the proposal, if the user confirmed but key fields are still unknown, ask **only about what you couldn't infer**. Frame each question with why you need it.

Examples of things you might not be able to infer:
- Primary criterion (if not obvious from the user's initial request)
- Background constraints not visible in files (budget, deadline, available hardware)
- Whether the user wants to explore outside visible parameters

**Do NOT ask about things you already inferred.** If you found `evaluate.sh` and read what it measures, don't ask "how should we evaluate?"

**Maximum 3 criteria.** If you inferred more than 3 from the evaluator, pick the 3 most impactful and propose those. If the user mentioned criteria in their initial request, use those over inferred ones.

For each criterion, you need a description of what 10/10 looks like. If you can infer this from the evaluator (e.g., "100% coverage" from a coverage metric), use it. If not, ask: "What does a 10/10 look like for [criterion]?"

## Phase 5: Output Setup Brief

Produce this exact format — it is consumed by every subsequent subskill:

```
ARTIFACT: [full content if from-paste, file path if from-file, directory path if from-workspace, description if seedless]
ARTIFACT_TYPE: [single-file | workspace]
CRITERIA:
  - [criterion 1]: [what a 10/10 looks like]
  - [criterion 2]: [what a 10/10 looks like]
  - [criterion 3]: [what a 10/10 looks like]
PRIMARY: [criterion name — omit if equally weighted]
EVALUATOR: [command to run — omit for judge-only]
BACKGROUND: [constraints and resources — omit if not provided]
OUTPUT_CONTRACT: [valid output format description — omit for text/creative]
VALIDATION_COMMAND: [quick check command — omit if no cheap validation exists]
SEARCH_SPACE: [what's in scope to explore — omit if unconstrained]
JUDGE_MODE: [single | board — auto-select, see below]
ITERATIONS: [N]
MODE: [seedless | from-file | from-paste | from-workspace]
OUTPUT_DIR: [path, default: docs/simmer]
```

Default iteration count is 3. Override if user specified ("simmer this, 10 rounds"). Don't ask about iteration count — 3 is the default.

### Judge Mode Auto-Selection

Select `JUDGE_MODE` based on problem complexity. **Do not ask the user** — infer from the artifact and criteria.

| Condition | JUDGE_MODE |
|-----------|-----------|
| text/creative AND ≤2 criteria AND short artifact (email, tweet, tagline, single paragraph) | `single` |
| text/creative AND 3 criteria or longer/complex artifact | `board` |
| code/testable (any) | `board` |
| pipeline/engineering (any) | `board` |

**User overrides:** If the user said "with a single judge," use `single`. If they said "with a judge board" or "with a panel," use `board`. User intent wins — but check for mismatches:

**Complexity mismatch nudge:** If the user requested single judge but the artifact is complex (workspace, evaluator present, 3 criteria, code/pipeline), nudge once:

> "This is a [workspace/pipeline/complex] artifact with [N criteria / an evaluator / multiple files] — a judge board would give you better diagnosis here. Want to use the board instead, or stick with single judge?"

One question, one time. If they say single, respect it and move on.

The `OUTPUT_DIR` defaults to `docs/simmer`. Override if the user specifies a different location or if running in a test/scratch context.

Return this brief to the orchestrator. Do not proceed to generation or judging — that is the orchestrator's job.

## Example Flows

### Text/Creative (Minimal Friction)

```
User: "Simmer a DND adventure hook for a one-shot session.
The party is level 5, exploring a haunted lighthouse."

Agent: [no inspection needed — seedless creative writing]

Agent: "This is a creative writing piece — I'll use judge-only evaluation.

For criteria I'd suggest:
- Narrative tension: scenes have stakes, time pressure, and consequences
- Player agency: multiple meaningful decision points, not just a railroad
- Specificity: concrete details (names, descriptions, sensory hooks) not generic fantasy

3 iterations, seedless. Sound right?"

User: "yes"

→ Emit brief, hand to orchestrator
```

### Pipeline/Engineering (Full Inspection)

```
User: "Simmer this pipeline at /tmp/pipeline —
I want the best model/prompt/topology for extracting entities."

Agent: [reads directory: config.json, run_pipeline.py, prompt.md,
        evaluate.sh, validate.sh, strategies/]
       [reads config.json: model=qwen3.5:4b, strategy=single-call]
       [reads evaluate.sh: measures coverage, precision, tokens per video]
       [reads validate.sh: runs 1 video, checks JSON format]
       [reads prompt.md: extraction prompt with JSON schema]
       [reads run_pipeline.py: supports pluggable strategies from strategies/ dir]

Agent: "This is a pipeline optimization problem. Here's what I found:

**Evaluator:** ./evaluate.sh — runs all 3 test videos, measures coverage
against ground truth, precision, and token count per model.
**Output contract:** JSON object with 'entities' array, each element has
'name' (string) and 'type' (string). Inferred from pipeline output format
and evaluator expectations.
**Validation:** ./validate.sh — runs 1 video, checks output is valid JSON
with correct schema. Takes ~1 min vs 5-30 min for full eval.
**Search space:**
  - Models: currently qwen3.5:4b in config.json (what else is available?)
  - Prompts: prompt.md (unlimited changes)
  - Topology: single-call currently, but run_pipeline.py supports pluggable
    strategies from strategies/ dir — multi-call is explorable

For criteria:
- Coverage: extracts maximum entities from ground truth (primary?)
- Efficiency: lowest token count while maintaining coverage
- Noise: minimal false positives

What models do you have available? And is coverage the primary goal?"

User: "qwen3.5 4b/9b/27b on Ollama. Yes, coverage is primary. 5 iterations."

→ Emit brief with all inferred + confirmed values
```

### Code/Testable (Light Inspection)

```
User: "Simmer this extraction prompt at local_extract_test.py as PROMPT_V4_FULL"

Agent: [reads local_extract_test.py — finds prompt, test harness,
        evaluator command pattern]

Agent: "This is a prompt optimization with a test harness. I see the evaluator
runs via: OLLAMA_MODEL=qwen3.5:27b python3 local_extract_test.py v4_full

Output should be JSON with 'entities' array (name + type from the taxonomy).

For criteria:
- Coverage: extracts every entity from ground truth
- Noise: zero false positives
- Conceptual depth: captures painting theory, not just concrete items

Which matters most?"

User: "Coverage is primary. 3 iterations."

→ Emit brief
```

## Common Mistakes

**Asking the user to describe something you can read**
- Problem: User has to describe files sitting in the workspace
- Fix: Read the files first. Only ask about what you can't infer.

**Presenting a form instead of an assessment**
- Problem: "What does valid output look like?" when evaluate.sh shows exactly what format it expects
- Fix: Read the evaluator, infer the contract, propose it

**Asking too many questions in sequence**
- Problem: 6-8 back-and-forth exchanges before work starts
- Fix: Propose everything in one assessment message. User confirms or adjusts.

**Not reading evaluator/validation scripts**
- Problem: Agent knows scripts exist but doesn't read them to understand what they measure
- Fix: Read the scripts. Extract metrics, formats, expectations.

**Over-inspecting for text/creative**
- Problem: Creative writing doesn't need workspace inspection, contracts, or validation
- Fix: Text/creative path stays lightweight — suggest criteria, confirm, go.

**Proposing more than 3 criteria**
- Problem: Judge signal gets diluted, generator tries to fix too many things
- Fix: Cap at 3, ask user to prioritize if you inferred more

**Not asking what 10/10 looks like**
- Problem: Criteria are vague, judge has no anchor for scoring
- Fix: Infer 10/10 from evaluator metrics where possible. Ask when you can't infer.

**Starting to generate or judge**
- Problem: Setup's job is ONLY to produce the brief
- Fix: Return the brief to the orchestrator, stop

**Forcing evaluator output format**
- Problem: User has to modify their existing scripts to match a contract
- Fix: No format requirements on evaluator output — the judge interprets whatever it produces

**Re-proposing after minor adjustments**
- Problem: User says "change primary to X" and agent re-presents the entire assessment
- Fix: Incorporate the adjustment and emit the brief. Only re-propose if the user asks to review.
