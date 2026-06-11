---
name: reference-enrichment
description: "Analyze agent/skill reference depth and generate missing domain-specific reference files."
user-invocable: true
argument-hint: "<agent-or-skill-name> [--decompose]"
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
routing:
  triggers:
    - "enrich references"
    - "improve reference depth"
    - "generate references"
    - "add reference files"
    - "reference enrichment"
    - "decompose skill"
    - "extract references"
    - "slim down skill"
    - "skill too long"
    - "move content to references"
  category: meta-tooling
  complexity: medium
  pairs_with:
    - verification-before-completion
---

# Reference Enrichment Skill

Enrich an agent or skill's reference files from Level 0-2 to Level 3+, or decompose bloated body
files by extracting domain content into references. Enrichment adds knowledge; decomposition moves
knowledge to where progressive disclosure says it belongs. The enrichment pipeline runs five phases
with explicit gates because each phase feeds the next — starting Phase 3 without Phase 2 research
produces filler, not depth.

## Workflow

### Phase 0: DECOMPOSE

**Goal**: Extract domain-heavy content from a bloated SKILL.md or agent body into reference files.

**When to use**: When a component's body exceeds ~500 lines and contains catalogs, code examples, specification tables, or agent rosters that should live in `references/` per PHILOSOPHY.md's progressive disclosure architecture.

**Trigger**: Invoke with `--decompose` argument, or when the request matches "decompose", "extract references", "slim down", "too long", or "move to references".

1. Run the detection script to identify extractable content:
   ```bash
   python3 scripts/detect-decomposition-targets.py --skill {name}
   ```
   (or `--agent {name}`)

2. If no extractable blocks found, report "nothing to decompose" and stop

3. Save a snapshot of the original file: `cp {path} /tmp/decomp-before-{name}.md`

4. For each extractable block identified by the detection script:
   a. Read the content block and its surrounding context
   b. Determine the best reference filename:
      - Use the detection script's suggestion as a starting point
      - If a reference file with related content already exists, MERGE into it
      - Follow naming convention: `references/{topic}.md` (lowercase, hyphens)
   c. Create or update the reference file following `references/reference-file-template.md`
   d. Remove the content from the body (MOVE, not copy)
   e. Add a loading table entry in the body that maps task signals to the new reference file

5. Ensure the body retains:
   - YAML frontmatter
   - Brief overview paragraph
   - Phase workflow (phases, gates, decision points)
   - Loading table with entries for all reference files
   - Error handling section
   - References section

6. Validate the decomposition:
   ```bash
   python3 scripts/validate-decomposition.py \
       --before /tmp/decomp-before-{name}.md \
       --after {path} \
       --refs {refs_dir}/
   ```

7. If validation FAILS: restore from snapshot and report the failure. Do not proceed.

8. If validation PASSES: run structural checks:
   ```bash
   python3 scripts/validate-references.py --skill {name}  # or --agent {name}
   python3 scripts/audit-reference-depth.py --skill {name} --verbose  # or --agent {name}
   ```

**Gate**: Validation passes. Body line count reduced. All extracted content exists in reference files. Loading table entries exist for all new references.

---

### Phase 1: DISCOVER

**Goal**: Identify which sub-domains are missing reference coverage.

1. Run the gap analyzer: `python3 skills/meta/reference-enrichment/scripts/gap-analyzer.py --agent {name}`
   (or `--skill {name}`)
2. Read the component's .md file to understand its stated purpose, triggers, and domain claims
3. Read any existing reference files to map current coverage
4. Compare stated domains against covered domains to identify gaps

Output format:
```
DISCOVER: {name}
  Current level: {0-3}
  Existing references: [{filenames}]
  Stated domains: [{domains from description and body}]
  Gaps: [{sub-domains with no reference coverage}]
  Recommended files: [{filename} → {why}]
```

**Gate**: Gap report exists with at least one identified gap. If no gaps exist (Level 3 already),
report and stop — over-generating creates noise, not signal.

---

### Phase 2: RESEARCH

**Goal**: Compile concrete, domain-specific content for each gap.

For each identified gap:
1. Read existing Level 3 reference files in this repo as exemplars — golang-general-engineer's
   references/ is the benchmark: version-specific patterns, grep commands, error-fix mappings
2. Identify: version-specific patterns (what changed in version X.Y), common failure modes with
   detection commands (`grep -rn "pattern" --include="*.ext"`), error-fix mappings
   (error message → root cause → fix), project-specific conventions visible in the codebase

Dispatch up to 5 parallel research agents — one per sub-domain gap — because sequential research
bottlenecks the pipeline. Each agent receives: the sub-domain, the component's .md as context,
and a path to an exemplar Level 3 reference file.

**Gate**: Each gap has at least 10 concrete findings (version numbers, function names, grep
patterns, code examples). Generic advice ("follow best practices") does not count toward this gate.

---

### Phase 3: COMPILE

**Goal**: Assemble research into structured reference files.

For each gap, create one reference file following `references/reference-file-template.md`:
- One file per major sub-domain (not one monolithic file) because focused files are faster to
  load and easier to update as language versions change
- Max 500 lines per file (CLAUDE.md standard) — split into sub-topics if content exceeds this
- Include: overview paragraph, pattern table with version ranges, failure mode table with
  detection commands, error-fix mappings where applicable
- Match the tone of existing Level 3 references: direct, concrete, no hedging

**Do-pairing rule (mandatory):** Every failure mode block written during this phase must include
a "Do instead" counterpart. If the retro learning or research does not carry enough information
to write a concrete positive counterpart, omit the failure mode entirely rather than shipping it
without the paired "Do instead". A bare negative block encodes no actionable knowledge and will
fail structural validation. If a prohibition is a genuine absolute with no correct alternative,
annotate it with `<!-- no-pair-required: reason -->` inline before the block.

Write files to: `agents/{name}/references/` or `skills/{name}/references/`

**Gate**: Each generated file is between 80-500 lines. Run both checks:
```bash
python3 scripts/validate-references.py --agent {name}
python3 scripts/validate-references.py --check-do-framing
```
Both must exit 0 before proceeding to Phase 4.

After validation passes, run the `condense` skill on each generated reference file to strip prose
filler while preserving patterns, detection commands, and error-fix mappings.

---

### Phase 4: VALIDATE

**Goal**: Confirm the reference files meet Level 3+ depth before integrating.

**Tier 1 (Deterministic):**
```bash
python3 scripts/audit-reference-depth.py --agent {name} --json
```
Verify the `level` field is 3 in the output. If still below Level 3, the files are too
generic — return to Phase 2 for the weak sub-domain.

**Tier 2 (LLM self-assessment):**
Read each generated file and apply the rubric from `references/quality-rubric.md`. Ask: would
a reviewer using only this file produce Level 3 quality output? Concrete test: pick one
failure mode from the file — does it include a grep command to detect it?

**Gate**: Both tiers pass. If Tier 2 fails for a specific sub-domain, loop back to Phase 2 for
that gap only (not all gaps). Maximum 2 loops per gap before flagging for manual enrichment.

---

### Phase 5: INTEGRATE

**Goal**: Wire the new references into the component so they are actually loaded.

1. Read the component's .md file
2. Add or update a loading table in the body — pattern from `skills/meta/do/references/repo-architecture.md`:
   ```
   | Task type | Load |
   |-----------|------|
   | {task}    | `references/{file}.md` |
   ```
3. Write the updated .md file
4. Run validation:
   ```bash
   python3 scripts/validate-references.py --agent {name}
   python3 -m pytest scripts/tests/test_reference_loading.py -k {name} -v
   ```
5. Stage all changes: `git add agents/{name}/ skills/{name}/`

**Gate**: Validation passes. Changes staged. Report the level change (was: N, now: M) and list
each new file with its line count.

---

## Reference Material

Load when the task type matches:

| Task type | Load |
|-----------|------|
| Understanding Level 0-3 criteria | `references/quality-rubric.md` |
| Creating new reference files | `references/reference-file-template.md` |
| Decomposing bloated components | Run `python3 scripts/detect-decomposition-targets.py --skill {name}` first |

---

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| classifying reference depth Level 0-3 (DISCOVER gaps, VALIDATE Tier 2) | `quality-rubric.md` | Loads detailed guidance from `quality-rubric.md`. |
| writing new reference files (Phase 3 COMPILE) | `reference-file-template.md` | Loads detailed guidance from `reference-file-template.md`. |

## Error Handling

**Gap analyzer fails**: The component may not exist in expected paths. Check both `agents/` and
`skills/` directories, and `~/.claude/agents/` for deployed copies.

**Phase 2 gate fails** (fewer than 10 concrete findings): The domain may be too narrow or already
well-documented upstream. Flag and suggest manual enrichment with project-specific production
incidents rather than generic docs research.

**Phase 4 Tier 1 still below Level 3 after compile**: The files are too short or too generic. Read one
file, apply the rubric directly, identify the weakest section, and target Phase 2 research at
that section specifically.

**validate-references.py not found**: Script may not exist for this component. Skip that check,
proceed with `audit-reference-depth.py` as the sole Tier 1 gate.

**Decomposition validation fails**: Content was lost during extraction. Restore from the
snapshot at `/tmp/decomp-before-{name}.md`. Check that each extracted content block appears
in a reference file. Common cause: a code block was partially extracted or a table was split
across the body and a reference file.
