---
name: skill-creator
description: >
  Guide for creating, improving, benchmarking, and packaging Claude Agent Skills
  (SKILL.md files). Invoke when users want to create a skill from scratch,
  improve or test an existing skill, benchmark skill performance with variance
  analysis, or optimize a skill description for triggering accuracy. Also invoke
  when users say "turn this into a skill", "make a skill for X", "help me write a
  SKILL.md", "my skill isn't firing correctly", or want to convert a
  workflow/conversation into a reusable skill. Invoke proactively when a
  conversation has produced a repeatable workflow worth capturing. If the user
  mentions SKILL.md, skill files, skill descriptions, or skill triggering, this
  skill applies.
---

# Skill Creator

Create new skills and iteratively improve them. The lifecycle:

1. Decide what the skill should do and how
2. Draft the skill
3. Run test prompts through claude-with-the-skill
4. Evaluate results qualitatively and quantitatively with the user
5. Rewrite based on feedback
6. Repeat until satisfied, then expand the test set
7. Package and deliver

Determine where the user is in this lifecycle and help them progress. Starting
from scratch ("I want a skill for X") -- help narrow scope, draft, test, iterate.
Already have a draft -- go straight to eval/iterate. Just want a better
description -- jump to Description Optimization.

Be flexible: if the user says "just vibe with me, no evals," do that.

---

## Available Resources

Before starting, verify what is available in the environment. The full workflow
requires these bundled resources:

| Resource | Path | Used for |
|---|---|---|
| Grader instructions | `agents/grader.md` | Assertion evaluation |
| Comparator instructions | `agents/comparator.md` | Blind A/B comparison |
| Analyzer instructions | `agents/analyzer.md` | Benchmark pattern analysis |
| Schema reference | `references/schemas.md` | evals.json, grading.json formats |
| Assertion patterns | `references/eval-patterns.md` | Writing discriminating assertions |
| Troubleshooting | `references/troubleshooting.md` | Common errors and fixes |
| Eval review template | `assets/eval_review.html` | Description optimization UI |
| Benchmark aggregator | `scripts/aggregate_benchmark` | `python -m scripts.aggregate_benchmark` |
| Description optimizer | `scripts/run_loop` | `python -m scripts.run_loop` |
| Eval viewer | `eval-viewer/generate_review.py` | Human review interface |

**If resources are missing:** The core loop (draft -> test -> review -> improve)
still works without them -- grade inline and present results in-conversation
instead of the browser viewer. Note what is unavailable to the user and adapt.

---

## Communicating with the user

The skill creator serves people across a wide range of technical backgrounds.
Non-developers are opening terminals for the first time because Claude makes
things possible; experienced engineers are also common.

Pay attention to context cues:
- "evaluation" and "benchmark" are borderline but generally OK
- Avoid "JSON" or "assertion" without a brief explanation unless the user has
  already used those terms

Err toward clarity. A short inline definition never hurts.

---

## Creating a skill

### Capture Intent

The current conversation may already contain the workflow to capture. If the user
says "turn this into a skill" or "make this repeatable," mine the conversation
history first:
- What tools were used, in what sequence?
- What corrections did the user make?
- What were the input and output formats?
- What would a different user need to know to reproduce this?

Fill gaps with the user and confirm before drafting.

If starting from scratch, establish:

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases, contexts, task types)
3. What is the expected output -- files, structured data, prose, or a workflow?
4. Should test cases be set up? Skills with verifiable outputs (file transforms,
   code generation, fixed workflows) benefit from them. Skills with subjective
   outputs (writing style, creative direction) often do not. Suggest the
   appropriate default based on skill type, but let the user decide.

### Interview and Research

Ask about edge cases, input/output examples, success criteria, and dependencies
before writing test prompts. If useful MCPs are available (docs search, similar
skill lookup), research in parallel via subagents. Come prepared so the interview
is lightweight.

### Write the SKILL.md

Based on the interview, compose the skill. Every skill has:

- **name**: Identifier (kebab-case)
- **description**: The primary triggering mechanism. Describe what the skill does
  AND when to use it. All "when to trigger" information goes here, not in the
  body. Apply the "pushy principle" -- err toward including trigger contexts
  rather than omitting them. Example: instead of "Builds REST APIs," write
  "Builds REST APIs. Invoke whenever users ask about endpoints, routes, HTTP
  methods, API design, or want to add a backend -- even if they don't say 'REST.'"
- **compatibility**: Required tools or dependencies (optional, rarely needed)
- **skill body**: Instructions, workflow, examples, references

#### Skill output template

Use this as the starting structure -- fill in or remove sections as needed:

```markdown
---
name: skill-name
description: >
  [What this skill does and when to trigger it. One to three sentences.
  Apply the pushy principle: include adjacent trigger contexts.]
---

# [Skill Name]

[One paragraph: what this skill enables and when to use it.]

## [Core workflow or main section]

[Instructions in imperative form. Explain the *why* behind each step.]

## Output format

[Concrete template for what this skill produces.]

## Examples

**Example 1:**
Input: [realistic user prompt]
Output: [expected result]

## Reference files

- Read `references/advanced.md` when [specific situation]
- Run `scripts/transform.py` for [repeatable operation]
```

#### Anatomy of a skill directory

```
skill-name/
+-- SKILL.md (required)
+-- Optional bundled resources:
    +-- scripts/    - Scripts for deterministic/repetitive tasks
    +-- references/ - Docs loaded into context as needed
    +-- assets/     - Templates, icons, fonts
```

Progressive loading:
1. **Metadata** (name + description) -- always in context
2. **SKILL.md body** -- in context when the skill triggers (&lt;500 lines ideal)
3. **Bundled resources** -- loaded as needed, scripts can run without loading

Keep SKILL.md under 500 lines. If approaching that limit, add a layer of
hierarchy with clear pointers to reference files. For reference files over 300
lines, add a table of contents.

**Domain organization** -- when a skill covers multiple frameworks/variants:

```
cloud-deploy/
+-- SKILL.md (workflow + selection logic)
+-- references/
    +-- aws.md
    +-- gcp.md
    +-- azure.md
```

Claude reads only the relevant reference file.

#### Writing patterns

**Output templates** -- be concrete:
```markdown
## Report structure
ALWAYS use this template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples** -- include realistic ones:
```markdown
## Commit message format
**Example:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

**Writing style** -- use imperative form. Explain the *why* rather than issuing
rules. Avoid ALWAYS/NEVER in all caps where the reasoning can be explained
instead -- models respond better to understanding than mandates. Write a draft,
then read it fresh and improve it.

**Security** -- skills must not contain malware, exploit code, or anything that
would surprise the user if they read the description. Do not create skills
designed to facilitate unauthorized access or data exfiltration. Roleplay skills
are fine.

### Test Cases

After drafting, write 2-3 realistic test prompts -- things a real user would
actually type. Share them: "Here are a few test cases I'd like to try. Do these
look right, or do you want to add more?"

Save to `evals/evals.json`. Do not write assertions yet -- just prompts.
Assertions get drafted while runs are in progress.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

See `references/schemas.md` for the full schema including the `assertions` field.

---

## Running and evaluating test cases

This is one continuous sequence -- do not stop partway through. Do NOT use
`/skill-test` or any other testing skill.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory.
Organize by iteration, then by eval name, then by configuration, then by run.
Create directories as you go, not all upfront.

### Workspace layout

```
<skill-name>-workspace/
+-- iteration-1/
|   +-- eval-<name>/                    <-- one per test case (descriptive name)
|   |   +-- eval_metadata.json          <-- eval ID, prompt, assertions
|   |   +-- with_skill/
|   |   |   +-- run-1/
|   |   |       +-- outputs/            <-- files the subagent produced
|   |   |       |   +-- metrics.json
|   |   |       +-- timing.json         <-- from task notification
|   |   |       +-- grading.json        <-- written by grader agent
|   |   +-- without_skill/              <-- or old_skill/ when improving
|   |       +-- run-1/
|   |           +-- outputs/
|   |           +-- timing.json
|   |           +-- grading.json
|   +-- benchmark.json                  <-- written by aggregate_benchmark.py
|   +-- benchmark.md
+-- iteration-2/
    +-- ...
```

### Step 1: Spawn all runs (with-skill AND baseline) in the same turn

For each test case, spawn two subagents simultaneously -- one with the skill, one
without. Do not do with-skill runs first and baseline runs later. Launch
everything at once so results arrive around the same time.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<name>/with_skill/run-1/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** -- depends on context:
- **New skill**: no skill at all. Same prompt, save to
  `<workspace>/iteration-<N>/eval-<name>/without_skill/run-1/outputs/`
- **Improving existing skill**: snapshot the old version first
  (`cp -r <skill-path> <workspace>/skill-snapshot/`), point baseline at snapshot,
  save to `old_skill/run-1/outputs/`

Write `eval_metadata.json` at the eval level (e.g.,
`<workspace>/iteration-N/eval-<name>/eval_metadata.json`). Give each eval a
descriptive name based on what it tests -- not just "eval-0":

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Step 2: While runs are in progress, draft assertions

Do not just wait for runs to finish -- use this time productively. Draft
quantitative assertions for each test case and explain them to the user. If
assertions already exist in `evals/evals.json`, review and explain them.

Good assertions are objectively verifiable and have descriptive names -- someone
glancing at benchmark results should immediately understand what each one checks.
For subjective skills (writing style, design quality), skip assertions and rely
on qualitative review. See `references/eval-patterns.md` for assertion patterns
by task type and the discriminating assertion test.

Update `eval_metadata.json` files and `evals/evals.json` with assertions once
drafted. Preview for the user: explain what they will see in the viewer.

### Step 3: As runs complete, capture timing data

When each subagent task completes, save timing data immediately to `timing.json`
in the run directory (e.g., `with_skill/run-1/timing.json`):

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This data only comes through task completion notifications -- capture it then.

### Step 4: Grade, aggregate, and launch the viewer

**GENERATE THE EVAL VIEWER BEFORE EVALUATING INPUTS YOURSELF. Get outputs in front of the human first.**

Once all runs complete:

1. **Grade each run** -- spawn a grader subagent for each run directory (both
   with_skill and without_skill/old_skill get their own grader). Use this prompt:

   ```
   You are a grader agent. Read agents/grader.md from <skill-creator-path>
   to load your full instructions, then grade this eval run:

   - Expectations: ["assertion 1", "assertion 2", ...]
   - Transcript path: <workspace>/iteration-N/eval-<name>/with_skill/run-1/transcript.md
   - Outputs dir:    <workspace>/iteration-N/eval-<name>/with_skill/run-1/outputs/

   Save grading.json to <workspace>/iteration-N/eval-<name>/with_skill/run-1/grading.json.
   ```

   Required field names in `grading.json`: `text`, `passed`, `evidence` (not
   `name`/`met`/`details` -- the viewer depends on these exact names). For
   assertions that can be checked programmatically, write and run a script.

2. **Aggregate** -- run:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Produces `benchmark.json` and `benchmark.md`. List with_skill before baseline.
   If generating `benchmark.json` manually, see `references/schemas.md` for the
   exact schema the viewer expects.

3. **Analyst pass** -- read the benchmark data and surface patterns the aggregate
   stats might hide: non-discriminating assertions (always pass regardless of
   skill), high-variance evals (possibly flaky), time/token tradeoffs. See
   `agents/analyzer.md` ("Analyzing Benchmark Results" section).

4. **Launch the viewer**:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, add `--previous-workspace <workspace>/iteration-<N-1>`.

   **No display / headless**: use `--static <output_path>` to write a standalone
   HTML file. The "Submit All Reviews" button downloads `feedback.json` -- copy
   it into the workspace directory when done.

5. **Tell the user**: "I've opened the results in your browser. 'Outputs' tab
   lets you review each test case and leave feedback. 'Benchmark' tab shows the
   quantitative comparison. Come back when you're done."

### What the user sees

**Outputs tab**: one test case at a time -- prompt, output, previous output
(collapsed, iteration 2+), formal grades (collapsed), feedback textbox, previous
feedback.

**Benchmark tab**: pass rates, timing, token usage per configuration, per-eval
breakdowns, analyst observations.

Navigation: prev/next buttons or arrow keys. "Submit All Reviews" saves
`feedback.json`.

### Step 5: Read the feedback

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "chart is missing axis labels"},
    {"run_id": "eval-1-with_skill", "feedback": ""},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this"}
  ],
  "status": "complete"
}
```

Empty feedback means the user was satisfied. Focus improvements on cases with
specific complaints. Kill the viewer when done: `kill $VIEWER_PID 2>/dev/null`

---

## Improving the skill

This is the heart of the loop. Tests have been run, the user has reviewed -- now
make the skill better.

### How to think about improvements

**Generalize from feedback, do not overfit to examples.** The skill will run
across countless different prompts. A skill that works only for the test examples
is useless. Rather than fiddly constraints, try different metaphors, different
working patterns, different framings -- cheap to try, potentially transformative.

**Keep the prompt lean.** Read the transcripts, not just final outputs. If the
skill makes the model waste time on unproductive steps, remove those
instructions. Deadweight is not neutral -- it adds noise and slows execution.

**Explain the why, not just the what.** Models have good theory of mind. They
perform better with reasoning than rules. If ALWAYS or NEVER in all caps appears,
try instead to explain why the thing matters. "Show the loading state before
fetching so users aren't left wondering if anything happened" outperforms "ALWAYS
show loading state."

**Bundle repeated work.** If all test case transcripts show the subagent writing
the same helper script, write it once, put it in `scripts/`, point the skill at
it. Every future invocation benefits.

Take time here. Read the draft revision with fresh eyes. Try to genuinely
understand what the user wants and what is blocking them, then transmit that
understanding into the instructions.

### The iteration loop

1. Apply improvements to the skill
2. Rerun all test cases into `iteration-<N+1>/`, including baselines
3. Launch the viewer with `--previous-workspace` pointing at the previous
   iteration
4. Wait for the user to review
5. Read feedback, improve again, repeat

Stop when: the user says they are happy, feedback is all empty, or meaningful
progress has stopped.

---

## Advanced: Blind comparison

For rigorous comparison between two skill versions, use the blind comparison
system: read `agents/comparator.md` and `agents/analyzer.md`. An independent
agent judges quality without knowing which version is which. Most users do not
need this -- the human review loop is usually sufficient.

---

## Description Optimization

The `description` field is the primary mechanism controlling whether Claude
invokes a skill. After creating or improving a skill, offer to optimize the
description for triggering accuracy.

### Step 1: Generate trigger eval queries

Create 20 queries -- a mix of should-trigger and should-not-trigger. Save as
JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

**Make queries realistic and specific.** Include file paths, personal context,
column names, company names, casual speech, typos, abbreviations, varying
lengths. Focus on edge cases, not clear-cut cases.

Bad: `"Format this data"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called
something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column
that shows the profit margin as a percentage. The revenue is in column C and
costs are in column D i think"`

**Should-trigger queries (8-10):** Cover different phrasings of the same intent.
Include cases where the user clearly needs the skill but does not name it.
Include uncommon use cases and cases where this skill competes with another but
should win.

**Should-not-trigger queries (8-10):** The most valuable are near-misses --
queries that share keywords but need something different. Adjacent domains,
ambiguous phrasing where keyword-matching would fire but should not. Do not use
obviously irrelevant negatives -- they test nothing.

### Step 2: Review with user

1. Read `assets/eval_review.html`
2. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array (no quotes -- JS
   variable assignment)
3. Replace `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__`
4. Write to `/tmp/eval_review_<skill-name>.html` and open it
5. User can edit queries, toggle should-trigger, add/remove entries, then
   "Export Eval Set"
6. Check Downloads for the most recent `eval_set.json`

### Step 3: Run the optimization loop

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Use the model ID from the system prompt so the test matches what the user
actually experiences. Run in background and tail output periodically for updates.

The loop: 60/40 train/test split, evaluate current description (3 runs per query
for variance), propose improvements from failures, re-evaluate, pick best by
test score (not train, to avoid overfitting), repeat up to 5 iterations.

**How triggering works:** Claude sees skills as `(name, description)` pairs and
decides whether to consult a skill based on that. It only consults skills for
tasks it cannot easily handle alone -- eval queries should be substantive enough
that a skill would actually help. Simple one-step queries will not trigger skills
even with perfect description matching.

### Step 4: Apply the result

Take `best_description` from the JSON output, update the skill's SKILL.md
frontmatter. Show before/after to the user and report scores.

---

## Package and Present

If the `present_files` tool is available:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Present the resulting `.skill` file to the user for installation.

---

## Claude.ai-specific instructions

Same core workflow, different mechanics:

**Running test cases:** No subagents. Read SKILL.md, follow instructions to
complete each test prompt directly, one at a time. Skip baselines. Less rigorous
(the skill author is also running it), but useful as a sanity check -- human
review compensates.

**Reviewing results:** If no browser is available, present results directly in
conversation. For file outputs (.docx, .xlsx), save to filesystem and tell the
user where to find them. Ask for feedback inline.

**Benchmarking:** Skip quantitative benchmarking -- baseline comparisons are not
meaningful without subagents. Focus on qualitative user feedback.

**Description optimization:** Requires `claude -p` CLI. Skip if unavailable.

**Blind comparison:** Requires subagents. Skip.

**Updating an existing skill:**
- Preserve the original name (directory name and `name` frontmatter field
  unchanged)
- The installed skill path may be read-only -- copy to `/tmp/skill-name/`, edit
  there, package from the copy
- Direct writes may fail; stage in `/tmp/` first

---

## Cowork-specific instructions

- Subagents work. If severe timeout problems arise, run test prompts in series.
- No browser/display: use `--static <output_path>` for the eval viewer, then
  provide the link for the user to open locally.
- **Generate the eval viewer before evaluating inputs.** See Step 4 above.
- Feedback: "Submit All Reviews" downloads `feedback.json`. Read from there.
- Description optimization (`run_loop.py`) works fine -- uses `claude -p`.
- Save description optimization until the skill is fully done and the user
  agrees.
- Updating an existing skill: same instructions as Claude.ai section above.

---

Track these lifecycle steps in TodoWrite if available. In Cowork, specifically
add "Create evals JSON and run `eval-viewer/generate_review.py` so human can
review test cases" as a todo item. For a full list of bundled resources, see the
Available Resources table near the top of this file.
