---
name: skill-creator
description: Use when creating a new skill, rewriting an existing skill, or running evaluations to improve skill quality and trigger accuracy.
---

# Skill Creator

Create, evaluate, and iteratively improve skills.

## The Loop

Every skill follows this cycle. Figure out where the user is and jump in:

1. **Capture intent** — understand what the skill does and when it triggers
2. **Draft the skill** — write SKILL.md and any bundled resources
3. **Run test cases** — spawn with-skill and baseline runs in parallel
4. **Evaluate with the user** — generate the eval viewer, run quantitative evals, get feedback
5. **Improve** — rewrite based on feedback, rerun, repeat
6. **Optimize description** — tune triggering accuracy (after skill is stable)

The user might arrive at any stage. Maybe they already have a draft — skip to eval. Maybe they want to vibe without formal evals — adapt. The loop is a guide, not a mandate.

## Capturing Intent

If the current conversation already contains a workflow to capture ("turn this into a skill"), extract from history first: tools used, step sequence, corrections made, input/output formats observed. Fill gaps with the user.

Key questions:
- What should this skill enable Claude to do?
- When should it trigger? (phrases, contexts)
- Expected output format?
- Are test cases appropriate? Objectively verifiable outputs (file transforms, data extraction, code generation) benefit from test cases. Subjective outputs (writing style, art) often don't.

Proactively research edge cases, dependencies, and similar existing skills before writing.

## Writing Skills

### Anatomy

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

### Progressive Disclosure

Skills use three-level loading:
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** — loaded on demand (unlimited; scripts execute without loading)

Keep SKILL.md under 500 lines. If approaching this limit, push detail into reference files with clear pointers. For large references (>300 lines), include a table of contents.

For multi-domain skills, organize by variant:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```

### Description

The description is the primary triggering mechanism. Include both what the skill does AND specific contexts for when to use it. Claude tends to *under-trigger* — it won't use skills when they'd be useful. Counteract this by making descriptions slightly pushy: instead of "Build dashboards for internal data", write "Build dashboards for internal data. Use whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"

### Writing Principles

Apply prompt design principles from:

!`cat ~/.claude/skills/prompt/SKILL.md`

Key calibrations specific to skill writing:
- **Explain why, not just what.** "ALWAYS" and "NEVER" in all caps are yellow flags — reframe as reasoning so the model applies the principle in novel situations.
- **Teach theory of mind.** A skill that helps the model understand the *user's* goal generalizes better than one specifying exact steps.
- **No-surprise principle.** Skills must not contain malware, exploit code, or content that would surprise the user if described.

## Test Cases

After drafting, create 2-3 realistic test prompts — things a real user would say. Share with user for confirmation, then run.

Save to `evals/evals.json`:
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

See `references/schemas.md` for the full schema (including `assertions`, added after first run).

## Running Evals

This section is one continuous sequence. Do NOT use `/skill-test` or other testing skills.

Put results in `<skill-name>-workspace/` as a sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`, etc.) and eval (`eval-0/`, `eval-1/`, etc.). Create directories as you go.

### Spawn All Runs in One Turn

For each test case, spawn **both** with-skill and baseline teammates simultaneously — not sequentially. This matters for wall-clock time.

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about>
```

**Baseline run** depends on context:
- **New skill** → no skill at all. Save to `without_skill/outputs/`.
- **Improving existing skill** → snapshot old version first (`cp -r`), point baseline at snapshot. Save to `old_skill/outputs/`.

Write `eval_metadata.json` per test case with a descriptive name (not "eval-0"). If iteration uses new/modified eval prompts, create fresh metadata files — don't assume carryover.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Draft Assertions While Runs Execute

Use the wait productively. Draft quantitative assertions for each test case and explain them to the user. Good assertions are objectively verifiable and have descriptive names that read clearly in the benchmark viewer.

Subjective skills (writing style, design quality) are better evaluated qualitatively — don't force assertions onto things that need human judgment.

Update `eval_metadata.json` and `evals/evals.json` with assertions.

### Capture Timing Data as Runs Complete

When a teammate task completes, the notification contains `total_tokens` and `duration_ms`. Save immediately to `timing.json` in the run directory — this data is not persisted elsewhere.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

### Grade, Aggregate, Launch Viewer

Once all runs complete:

1. **Grade each run** — spawn a grader teammate using `agents/grader.md`. Save to `grading.json` per run. The expectations array must use fields `text`, `passed`, `evidence` — the viewer depends on these exact names. For programmatically checkable assertions, write and run a script rather than eyeballing it.

2. **Aggregate** — run from the skill-creator directory:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Produces `benchmark.json` and `benchmark.md`. Put each with_skill version before its baseline counterpart. See `references/schemas.md` for the exact schema.

3. **Analyst pass** — spawn an analyst teammate using `agents/analyzer.md` to surface patterns the aggregate stats hide (non-discriminating assertions, high-variance evals, time/token tradeoffs).

4. **Launch viewer** — always use `generate_review.py`, never custom HTML:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   For iteration 2+, add `--previous-workspace <workspace>/iteration-<N-1>`.

   **Headless/Cowork:** Use `--static <output_path>` for standalone HTML. Feedback downloads as `feedback.json` — copy into workspace directory.

5. **Tell the user** the viewer is ready and to come back when they're done reviewing.

### Read Feedback

When user finishes, read `feedback.json`. Empty feedback = the user thought it was fine. Focus improvements on test cases with specific complaints.

Kill the viewer: `kill $VIEWER_PID 2>/dev/null`

## Improving the Skill

### Improvement Principles

- **Generalize from examples.** You're iterating on a few test cases to move fast, but the skill will be used across millions of prompts. If a fix only works for the current examples, it's overfitting. When a stubborn issue persists, try different metaphors or patterns rather than adding fiddly constraints.
- **Keep the prompt lean.** Read transcripts, not just outputs. If the skill causes the model to waste time on unproductive steps, remove those instructions.
- **Explain the why.** Transmit your understanding of the user's intent into the instructions. Rigid MUSTs are less effective than motivated reasoning.
- **Extract repeated work.** If all test runs independently wrote similar helper scripts, bundle that script in `scripts/` and reference it from the skill.

### Iteration Loop

1. Apply improvements
2. Rerun all test cases into `iteration-<N+1>/`, including baselines. For new skills, baseline is always `without_skill`. For improvements, use judgment on baseline version.
3. Launch viewer with `--previous-workspace` pointing to previous iteration
4. Wait for user review
5. Read feedback, improve, repeat

Stop when: the user is happy, feedback is all empty, or improvements plateau.

## Blind Comparison (Optional)

For rigorous A/B comparison between skill versions. Spawn comparator and analyzer teammates using `agents/comparator.md` and `agents/analyzer.md`. Gives two outputs to an independent teammate without revealing which is which.

Most users won't need this — the human review loop is usually sufficient.

## Description Optimization

After the skill is stable, optimize the description for triggering accuracy.

### Generate Trigger Eval Queries

Create 20 queries — mix of should-trigger (8-10) and should-not-trigger (8-10). Save as JSON:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

**Query quality matters.** Queries must be realistic — concrete, specific, with file paths, personal context, company names, URLs. Mix lengths, include typos and casual speech.

Bad: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`
Good: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

**Should-trigger queries:** Different phrasings of the same intent, some formal, some casual. Include cases where the user doesn't name the skill explicitly but clearly needs it.

**Should-not-trigger queries:** Near-misses are the most valuable — queries sharing keywords but needing something different. Adjacent domains, ambiguous phrasing. "Write a fibonacci function" as a negative for a PDF skill tests nothing.

**Triggering mechanics:** Skills appear in Claude's `available_skills` list. Claude only consults skills for tasks it can't handle directly — simple one-step queries may not trigger even with a perfect description. Eval queries should be substantive enough to benefit from skill consultation.

### Review with User

Use the HTML template from `assets/eval_review.html`:
1. Replace `__EVAL_DATA_PLACEHOLDER__` with the JSON array (no quotes — JS variable)
2. Replace `__SKILL_NAME_PLACEHOLDER__` and `__SKILL_DESCRIPTION_PLACEHOLDER__`
3. Write to `/tmp/eval_review_<skill-name>.html` and open
4. User edits queries, exports eval set
5. Check `~/Downloads/` for the export (may have numeric suffix)

### Run Optimization

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Run in background. Periodically tail output to give user updates. The loop splits 60% train / 40% test, evaluates 3x per query for reliability, uses extended thinking for improvements, and selects by test score to avoid overfitting.

### Apply Result

Take `best_description` from output JSON and update SKILL.md frontmatter. Show before/after and scores.

## Environment Adaptations

### Claude.ai

No teammates — run test cases serially yourself. Skip baselines and quantitative benchmarking. Present results directly in conversation instead of the viewer. Skip description optimization (requires `claude -p` CLI).

### Cowork

Full workflow works. Use `--static <output_path>` for viewer (no display). Generate the eval viewer *before* evaluating outputs yourself — get results in front of the human first. Feedback downloads as a file.

### Packaging (if `present_files` tool available)

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Direct user to the resulting `.skill` file.

## Reference Files

- `agents/grader.md` — assertion evaluation against outputs
- `agents/comparator.md` — blind A/B output comparison
- `agents/analyzer.md` — benchmark pattern analysis
- `references/schemas.md` — JSON schemas for all data files
