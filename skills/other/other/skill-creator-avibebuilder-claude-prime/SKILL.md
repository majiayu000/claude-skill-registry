---
name: skill-creator
description: "Use when the user wants to work on a Claude Code skill file (SKILL.md): writing one from scratch, testing whether an existing one works well, running evals or benchmarks, improving its instructions, or fixing why it isn't triggering. Triggers on: 'make a skill for X', 'test this skill', 'run evals on my SKILL.md', 'touch-skill', sharing a SKILL.md and asking if it's ready to ship. The key signal is intent to create, validate, or improve a skill — not just mention one. Do NOT trigger for general Claude Code questions, hook debugging, or CLAUDE.md configuration."
---

# Skill Creator

Default operating mode: autonomous — create or update the skill, run evals, improve it, optimize the description, and return with a final report. Only pause for human review if the user explicitly requests it or you hit an ambiguity that can't be resolved from the evidence alone.

At a high level, the process of creating a skill goes like this:

- Decide what you want the skill to do and roughly how it should do it
- Write a draft of the skill
- Create a few test prompts and run claude-with-access-to-the-skill on them
- Evaluate the results both qualitatively and quantitatively
  - While the runs happen in the background, draft some quantitative evals if there aren't any (if there are some, you can either use as is or modify if you feel something needs to change about them)
  - Use the `eval-viewer/generate_review.py` script to show the results if the user wants to review
- Rewrite the skill based on eval results, benchmark data, and user feedback (if review was requested)
- Repeat until quality thresholds are met or the user is satisfied
- Optimize the description for triggering accuracy parallel

Figure out where the user is in this process and then jump in and help them progress through these stages. Route based on what they need. Of course, you should always be flexible and if the user is like "I don't need to run a bunch of evaluations, just vibe with me", you can do that instead.

**Workspace convention**: All eval artifacts go in `tmp/<skill-name>-workspace/` under the project root (the directory containing `.claude/`). This directory is gitignored. Within the workspace, organize by iteration (`iteration-1/`, `iteration-2/`, etc.).

**Nested invocation**: When invoked as a subagent with an explicit `outputs` directory, use that `outputs/` directory as the root for all inner workspaces — not `tmp/<skill-name>-workspace/`.

Track your progress with tasks/todos — without them, description optimization and the judge step are commonly skipped.

## Communicating with the user 

The skill creator is liable to be used by people across a wide range of familiarity with coding jargon. If you haven't heard (and how could you, it's only very recently that it started), there's a trend now where the power of Claude is inspiring plumbers to open up their terminals, parents and grandparents to google "how to install npm". On the other hand, the bulk of users are probably fairly computer-literate.

So please pay attention to context cues to understand how to phrase your communication! In the default case, just to give you some idea:

- "evaluation" and "benchmark" are borderline, but OK
- for "JSON" and "assertion" you want to see serious cues from the user that they know what those things are before using them without explaining them

It's OK to briefly explain terms if you're in doubt, and feel free to clarify terms with a short definition if you're unsure if the user will get it.

---

## Creating a skill

### Capture Intent

Start by understanding the user's intent. The current conversation might already contain a workflow the user wants to capture (e.g., they say "turn this into a skill"). If so, extract answers from the conversation history first — the tools used, the sequence of steps, corrections the user made, input/output formats observed. 
**Skip if in autonomous mode**: The user may need to fill the gaps, and should confirm before proceeding to the next step.

1. What should this skill enable Claude to do?
2. When should this skill trigger? (what user phrases/contexts)
3. What's the expected output format?
4. What evaluation strategy fits? Objectively verifiable outputs (file transforms, code generation) → expectations and baselines. Subjective outputs (writing style, art) → qualitative analysis.

**Skip if in autonomous mode**: If a gap is genuinely irresolvable from context and would materially change the skill's correctness, pause and ask. Otherwise infer, state it, and proceed.

### Interview and Research

Proactively ask questions about edge cases, input/output formats, example files, success criteria, and dependencies. Wait to write test prompts until you've got this part ironed out. SKIP this interview in autonomous mode, let make decisions yourself

**Research existing skills** — MUST read `references/available-skill-resources.md` for curated skill repositories, then fetch the README or index of relevant repos to check whether skills for this domain already exist. Don't deep-dive into repos with nothing relevant — a quick scan of the index is enough to know if there's something worth borrowing.

Check available MCPs - if useful for research (searching docs, finding similar skills, looking up best practices), research in parallel via subagents if available, otherwise inline. Come prepared with context to reduce burden on the user.

### Write the SKILL.md

Based on the user interview, fill in these components:

- **name**: Skill identifier
- **description**: When to trigger, what it does. This is the primary triggering mechanism - include both what the skill does AND specific contexts for when to use it. All "when to use" info goes here, not in the body. Note: currently Claude has a tendency to "undertrigger" skills -- to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit "pushy". So for instance, instead of "How to build a simple fast dashboard to display internal Anthropic data.", you might write "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'" **Length: hard limit is 1024 characters (the optimizer enforces this); aim for under ~650 characters in practice — past that, every extra clause competes for attention with the other skills' descriptions and tends to dilute rather than sharpen triggering.**
- **compatibility**: Required tools, dependencies (optional, rarely needed)
- **the rest of the skill :)**

### Skill Writing Guide

#### Anatomy of a Skill

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Progressive Disclosure

Skills use a three-level loading system:
1. **Metadata** (name + description) - Always in context (~100 words)
2. **SKILL.md body** - In context whenever skill triggers (<500 lines ideal)
3. **Bundled resources** - As needed (unlimited, scripts can execute without loading)

These word counts are approximate and you can feel free to go longer if needed.

**Key patterns:**
- Keep SKILL.md under 500 lines; if you're approaching this limit, add an additional layer of hierarchy along with clear pointers about where the model using the skill should go next to follow up.
- Reference files clearly from SKILL.md with guidance on when to read them
- For large reference files (>300 lines), include a table of contents
- **Routing lives at the parent.** "When to use" conditions go in the SKILL.md reference table — not inside the spoke file. By the time the agent reads a "## When to Use" section, it's already paid the load cost. Reference files cover HOW; parent covers WHEN.

**Domain organization**: When a skill supports multiple domains/frameworks, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude reads only the relevant reference file.

#### Principle of Lack of Surprise

This goes without saying, but skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described. Don't go along with requests to create misleading skills or skills designed to facilitate unauthorized access, data exfiltration, or other malicious activities. Things like a "roleplay as an XYZ" are OK though.

#### Writing Patterns

Prefer using the imperative form in instructions.

**Defining output formats** - You can do it like this:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Examples pattern** - It's useful to include examples. You can format them like this (but if "Input" and "Output" are in the examples you might want to deviate a little):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Writing Style

Try to explain to the model why things are important in lieu of heavy-handed musty MUSTs. Use theory of mind and try to make the skill general and not super-narrow to specific examples. Start by writing a draft and then look at it with fresh eyes and improve it.

### Test Cases

After writing the skill draft, come up with 2-3 realistic test prompts — the kind of thing a real user would actually say. Share them with the user if they want to review: "Here are a few test cases I'd like to try. Do these look right, or do you want to add more?" In autonomous mode, proceed directly.

Save test cases to `<workspace>/evals.json`. Don't write expectations yet — just the prompts. You'll draft expectations in Step 2 while the runs are in progress.

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

See `references/schemas.md` for the full schema (including the `expectations` field).

Good test cases are realistic (messy, specific — what a real user would type), substantive (complex enough that the skill makes a difference), diverse (different use cases, not three variations of the same prompt), and discriminating (test skill-specific behaviors, not generic task completion — ask "would bare Claude pass this?" and if yes, make it harder).

Also prepare 20 trigger eval queries for description optimization and save to `<workspace>/trigger-eval.json`. See the Description Optimization section below for the format. Doing this now means description optimization can launch immediately.

## Running and evaluating test cases

This section is one continuous sequence — don't stop partway through. Do NOT use `/skill-test` or any other testing skill.

Within the workspace, organize results by iteration (`iteration-1/`, `iteration-2/`, etc.) and within that, each test case gets a descriptive directory name (e.g., `handle-multi-page-pdf/`). Don't create all of this upfront — just create directories as you go.

### Step 0: Launch description optimization in the background

Description optimization only depends on the frontmatter description and trigger eval queries — it's independent of the skill body. Run it in parallel with the eval loop:

```bash
cd <skill-creator-dir> && python -m scripts.run_loop \
  --eval-set <workspace>/trigger-eval.json \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 --report none --verbose \
  --output <workspace>/run-loop-results.json \
  > <workspace>/run-loop.log 2>&1 &
echo "run_loop PID: $!"
```

Save the PID — you'll need it later to check completion. Continue immediately to Step 1.

### Step 1: Spawn eval runs

**Every eval must use a real subagent that actually executes the task.** Reading a skill and imagining it would work is not evaluation — it's guesswork. Spawn all test cases in parallel, each as a separate subagent:

```
Execute this task with the following skill loaded.

Read the skill at [skill SKILL.md path] first — it contains your instructions.

Task: [eval prompt]
Input files: [eval files if any, or "none"]
Save outputs to: [workspace path]/iteration-[N]/[eval-name]/with_skill/outputs/
Outputs to save: [what the user cares about — e.g., "the .docx file", "the final CSV"]

Also required: write `outputs/transcript.md` — one line per tool call, in order, as you go: `- <Tool> | <key args> | <ok|error>`. Graders use this to verify process assertions. No transcript = failed process assertions.

Do NOT revert or clean up the project after completing the task. The orchestrator handles cleanup after grading.
```

**Project cleanup timing:** Executors must not revert changes — doing so destroys evidence before graders can inspect it (new files, diffs, task artifacts). The orchestrator is responsible for restoring the project state **after** all graders have finished. This sequence matters: grade first, clean second.

**Baseline runs (new skills only)** — When creating a new skill, the first iteration MUST include baseline runs alongside with-skill runs. Run the same prompts without the skill loaded and save outputs to `without_skill/outputs/`. This measures whether the skill actually adds value over bare Claude. For subsequent iterations, baseline from iteration 1 still applies — no need to rerun.

**Baseline runs for existing skills** — When improving an existing skill, baseline runs are optional. Only run them when the user explicitly requests comparison. Existing skills have already proven their value.

Write an `eval_metadata.json` for each test case (expectations can be empty for now). Give each eval a descriptive name based on what it's testing — not just "eval-0". Use this name for the directory too. If this iteration uses new or modified eval prompts, create these files for each new eval directory — don't assume they carry over from previous iterations.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "expectations": []
}
```

### Step 2: While runs are in progress, draft expectations

Don't just wait for the runs to finish — you can use this time productively. Draft quantitative expectations for each test case. Good expectations are objectively verifiable and have descriptive names — they should read clearly in the benchmark viewer so someone glancing at the results immediately understands what each one checks. Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force expectations onto things that need human judgment.

Write expectations that test what the skill specifically teaches, not just structural presence. Before writing each one, ask: **"Would bare Claude likely get this right without the skill?"** If yes, the expectation isn't discriminating — make it harder. Target project-specific conventions, ordering/sequencing the skill introduces, and exact implementation details (column names, error codes, ID formats) rather than topic mentions.

Update the `eval_metadata.json` files and `evals.json` with the expectations once drafted.

### Step 3: As runs complete, capture timing data

When each subagent task completes, you receive a notification containing `total_tokens` and `duration_ms`. Save this data immediately to `timing.json` in the run directory:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

This is the only opportunity to capture this data — it comes through the task notification and isn't persisted elsewhere. Process each notification as it arrives rather than trying to batch them.

### Step 4: Grade, aggregate, and analyze

Once all runs are done:

1. **Grade each run** — spawn grader subagents in parallel (one per eval case), or grade inline for simple expectations. Each reads `agents/grader.md` and evaluates expectations against the outputs. When spawning, pass these inputs explicitly:

   ```
   Read agents/grader.md at <skill-creator-path>/agents/grader.md — it contains your role.

   transcript_path: <run>/outputs/transcript.md
   outputs_dir: <run>/outputs/
   expectations: [...]
   ```

   Save results to `grading.json` in each run directory. The grading.json expectations array must use the fields `text`, `passed`, and `evidence` — the viewer depends on these exact field names. For expectations that can be checked programmatically, write and run a script rather than eyeballing it.

2. **Aggregate into benchmark** — run the aggregation script from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   This produces `benchmark.json` and `benchmark.md` with pass_rate, time, and tokens for each configuration. If generating benchmark.json manually, see `references/schemas.md` for the exact schema.

3. **Do an analyst pass** — read the benchmark data and surface patterns the aggregate stats might hide. See `agents/analyzer.md` for what to look for — non-discriminating expectations, high-variance evals, time/token tradeoffs, and repeated failure modes that should become skill instructions or bundled scripts.

4. **Spawn a judge agent** to evaluate quality and decide whether to continue, stop, or revise evals. The judge runs on **every iteration including iteration 1** — if the skill is already good enough, there's no reason to burn another iteration. Always spawn the judge with `model: "opus"` — judgment calls benefit from the most capable model:

   ```
   Read agents/judge.md at <skill-creator-path>/agents/judge.md — it contains your role and output format.

   Then evaluate:
   - Previous benchmark: `<workspace>/iteration-<N-1>/benchmark.md` (skip for iteration 1)
   - Current benchmark: `<workspace>/iteration-<N>/benchmark.md`
   - Remaining failures: [paste analyst notes]
   - Skill diff: [paste the diff of what changed, or "Initial version" for iteration 1]
   ```

   Save the full output to `<workspace>/iteration-<N>/judge-output.json`.

   **Trust the judge's decision.** If it says stop, stop. Don't override.

   **Stop thresholds (all must be met):**
   - **Pass rate ≥ 80%** from real agent runs
   - **Quality score ≥ 8.0** per the judge's rubric
   - **Eval confidence = "high" or "medium"**

5. **If the user wants review**, launch the viewer:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, also pass `--previous-workspace <workspace>/iteration-<N-1>`.

   **If staying autonomous**, write down iteration takeaways: what failed, why, and whether the skill is beating the baseline.

### Assertion Quality Gate (new skills, iteration 1 only)

After aggregating benchmark data for the first iteration of a new skill, check whether the assertions are actually discriminating:

1. **Compare with-skill vs without-skill pass rates.** If the delta is less than 15%, the assertions likely aren't testing skill-specific behavior — bare Claude can pass them too.
2. **If both score 100%**, the assertions are definitively non-discriminating. The eval set needs revision before continuing.

When the gate fails:
- Pause the improvement loop
- Review grader `eval_feedback` for flagged weak assertions
- Revise assertions to test project-specific knowledge, skill-specific workflows, or behaviors Claude wouldn't exhibit without the skill
- Restart iteration 1 with the revised assertions

Do NOT mix assertion revisions with skill improvements across iterations — changing what you measure while changing what you're testing makes it impossible to track whether the skill actually improved.

This gate does not apply to existing skill improvements (no baseline data to compare against).

### Step 5: Read feedback (if review was requested)

When the user tells you they're done, read `feedback.json`. Empty feedback means the user thought it was fine. Focus your improvements on the test cases where the user had specific complaints. Kill the viewer when done (`kill $VIEWER_PID 2>/dev/null`).

---

## Improving the skill

This is the heart of the loop. You've run the test cases, you have benchmark data, and now you need to make the skill better.

### How to think about improvements

1. **Generalize from the evidence.** The big picture thing that's happening here is that we're trying to create skills that can be used a million times (maybe literally, maybe even more who knows) across many different prompts. Here you're iterating on only a few examples because it helps move faster. But if the skill works only for those examples, it's useless. Rather than put in fiddly overfitty changes, or oppressively constrictive MUSTs, if there's some stubborn issue, you might try branching out and using different metaphors, or recommending different patterns of working. It's relatively cheap to try and maybe you'll land on something great.

2. **Keep the prompt lean.** Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs — if it looks like the skill is making the model waste a bunch of time doing things that are unproductive, you can try getting rid of the parts of the skill that are making it do that and seeing what happens.

3. **Explain the why.** Try hard to explain the **why** behind everything you're asking the model to do. Today's LLMs are *smart*. They have good theory of mind and when given a good harness can go beyond rote instructions and really make things happen. Even if the feedback is terse or frustrated, try to actually understand the task and why the user is writing what they wrote, and what they actually wrote, and then transmit this understanding into the instructions. If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning so that the model understands why the thing you're asking for is important. That's a more humane, powerful, and effective approach.

4. **Look for repeated work across test cases.** Read the transcripts from the test runs and notice if the subagents all independently wrote similar helper scripts or took the same multi-step approach to something. If all 3 test cases resulted in the subagent writing a `create_docx.py` or a `build_chart.py`, that's a strong signal the skill should bundle that script. Write it once, put it in `scripts/`, and tell the skill to use it. This saves every future invocation from reinventing the wheel.

This task is pretty important and your thinking time is not the blocker; take your time and really mull things over. I'd suggest writing a draft revision and then looking at it anew and making improvements. Really do your best to get into the head of the user and understand what they want and need.

### The iteration loop

After improving the skill:

1. Apply your improvements
2. Write `<workspace>/iteration-<N+1>/skill_changes.json` documenting what changed:
   ```json
   ["Added error handling section", "Removed redundant examples", "Bundled helper script"]
   ```
   Each entry should be a human-readable string. For iteration 1, write `["Initial version"]`.
3. Rerun all test cases into `iteration-<N+1>/` (with-skill only — baseline from iteration 1 still applies)
4. Grade, aggregate, analyze, and judge (Steps 2-4 above — the judge runs every iteration)
5. If the user asked for review, launch the reviewer with `--previous-workspace` pointing at the previous iteration

**Safety limit: pause at 3 iterations.** The judge should stop this at 1-2 naturally. Reaching 3 without meeting thresholds means something structural is wrong — stop and diagnose whether the problem is the skill or the test cases. If the root cause is bad test cases, rewrite evals rather than continuing.

Keep going until:
- The judge says stop (autonomous mode)
- The user says they're happy (interactive mode)
- The feedback is all empty (everything looks good)
- You're not making meaningful progress

---

## Advanced: Blind comparison

For situations where you want a more rigorous comparison between two versions of a skill (e.g., the user asks "is the new version actually better?"), there's a blind comparison system. Read `agents/comparator.md` and `agents/analyzer.md` for the details. The basic idea is: give two outputs to an independent agent without telling it which is which, and let it judge quality. Then analyze why the winner won.

This is optional, requires subagents, and most users won't need it. The human review loop is usually sufficient.

---

## Description Optimization

The description field in SKILL.md frontmatter is the primary mechanism that determines whether Claude invokes a skill. If you launched description optimization in Step 0 during the eval loop, check on it now. Otherwise, run it after the skill body is finalized.

### Step 1: Generate trigger eval queries

Create 20 eval queries — a mix of should-trigger and should-not-trigger. Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

The queries must be realistic and something a Claude Code or Claude.ai user would actually type. Not abstract requests, but requests that are concrete and specific and have a good amount of detail. For instance, file paths, personal context about the user's job or situation, column names and values, company names, URLs. A little bit of backstory. Some might be in lowercase or contain abbreviations or typos or casual speech. Use a mix of different lengths, and focus on edge cases rather than making them clear-cut (the user will get a chance to sign off on them).

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

For the **should-trigger** queries (8-10), think about coverage. You want different phrasings of the same intent — some formal, some casual. Include cases where the user doesn't explicitly name the skill or file type but clearly needs it. Throw in some uncommon use cases and cases where this skill competes with another but should win.

For the **should-not-trigger** queries (8-10), the most valuable ones are the near-misses — queries that share keywords or concepts with the skill but actually need something different. Think adjacent domains, ambiguous phrasing where a naive keyword match would trigger but shouldn't, and cases where the query touches on something the skill does but in a context where another tool is more appropriate.

The key thing to avoid: don't make should-not-trigger queries obviously irrelevant. "Write a fibonacci function" as a negative test for a PDF skill is too easy — it doesn't test anything. The negative cases should be genuinely tricky.

### Step 2: Review with user (or skip in autonomous mode)

Present the eval set to the user for review using the HTML template:

1. Read the template from `assets/eval_review.html`
2. Replace the placeholders:
   - `__EVAL_DATA_PLACEHOLDER__` → the JSON array of eval items (no quotes around it — it's a JS variable assignment)
   - `__SKILL_NAME_PLACEHOLDER__` → the skill's name
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → the skill's current description
3. Write to a temp file (e.g., `/tmp/eval_review_<skill-name>.html`) and open it: `open /tmp/eval_review_<skill-name>.html`
4. The user can edit queries, toggle should-trigger, add/remove entries, then click "Export Eval Set"
5. The file downloads to `~/Downloads/eval_set.json` — check the Downloads folder for the most recent version

In autonomous mode, skip this step and proceed directly to the optimization loop.

### Step 3: Run the optimization loop

```bash
cd <skill-creator-dir> && python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 --report none --verbose \
  --output <workspace>/run-loop-results.json \
  > <workspace>/run-loop.log 2>&1 &
echo "run_loop PID: $!"
```

Use the model ID from your system prompt (the one powering the current session) so the triggering test matches what the user actually experiences.

This handles the full optimization loop automatically. It splits the eval set into 60% train and 40% held-out test, evaluates the current description (running each query 3 times to get a reliable trigger rate), then calls Claude to propose improvements based on what failed. It re-evaluates each new description on both train and test, iterating up to 5 times.

### How skill triggering works

Understanding the triggering mechanism helps design better eval queries. Skills appear in Claude's `available_skills` list with their name + description, and Claude decides whether to consult a skill based on that description. The important thing to know is that Claude only consults skills for tasks it can't easily handle on its own — simple, one-step queries like "read this PDF" may not trigger a skill even if the description matches perfectly, because Claude can handle them directly with basic tools. Complex, multi-step, or specialized queries reliably trigger skills when the description matches.

This means your eval queries should be substantive enough that Claude would actually benefit from consulting a skill. Simple queries like "read file X" are poor test cases — they won't trigger skills regardless of description quality.

### Step 4: Apply the result

Take `best_description` from `<workspace>/run-loop-results.json` and update the skill's SKILL.md frontmatter. Show the user before/after and report the scores.

If `best_description` is unchanged from the original (the loop found no improvement), you have two options: (1) accept the original and stop, or (2) manually write a new candidate based on the failing test queries. If you choose (2), rerun the loop with `--description-override "<candidate>"` before applying — never apply an untested manual description directly to SKILL.md.

---

## Final Report

Always generate and open a visual HTML report:

```bash
python <skill-creator-path>/eval-viewer/generate_report.py \
  <workspace> \
  --skill-name "<name>" \
  --run-loop-results <workspace>/run-loop-results.json \
  -o <workspace>/report.html
```

The `--run-loop-results` flag is optional — include it only if description optimization was run. After generating: `open <workspace>/report.html`

Include a brief text summary: what you changed and why, key outcomes, description optimization result, any remaining risks.

If the user asked whether a skill is ready to ship, give a direct recommendation: **Ship**, **Ship with caveats**, or **Not ready** — with specific reasons.

**Packaging**: For a distributable `.skill` file, run `python -m scripts.package_skill <path/to/skill-folder>`.

---

## Reference files

The agents/ directory contains instructions for specialized subagents. Read them when you need to spawn the relevant subagent.

- `agents/grader.md` — How to evaluate expectations against outputs
- `agents/judge.md` — Independent agent that decides whether to continue or stop iterating
- `agents/comparator.md` — How to do blind A/B comparison between two outputs
- `agents/analyzer.md` — How to analyze why one version beat another

The references/ directory has additional documentation:
- `references/schemas.md` — JSON structures for evals.json, grading.json, benchmark.json, etc.
- `references/available-skill-resources.md` — Curated skill repositories for research

---

The core loop, one more time:

- Figure out what the skill is about
- Draft or edit the skill
- Run claude-with-access-to-the-skill on test prompts
- Evaluate the outputs (grade, benchmark, review if requested)
- Improve and repeat until thresholds met
- Optimize the description
- Generate final report

Track these steps with tasks/todos to make sure nothing gets skipped. Good luck!
