---
name: gauntlet-curate
description: Audits the DSA problem bank for coverage gaps and proposes new YAML entries. Use when refreshing the problem bank during update-plugins runs.
model_hint: standard
---

# Gauntlet Curate

Survey the DSA problem bank, identify coverage gaps, and propose
new YAML entries for human review.

## When This Skill Fires

Invoke this skill manually with `Skill(gauntlet:gauntlet-curate)`
when the problem bank needs a coverage review. The skill is intended
to participate in `/update-plugins` runs but is not yet wired into
that command (see openpackage.yml registration). It is distinct from
`gauntlet:curate`, which handles per-annotation knowledge capture
and is what `/gauntlet-curate` invokes today.

## Steps

1. **Locate the problem bank** at `plugins/gauntlet/data/problems/`.
   Read `_manifest.yaml` to load the expected NeetCode counts per
   category.

2. **Survey current coverage** by counting problems in each YAML
   file (skipping `_manifest.yaml`).
   Run the analysis script:

   ```bash
   cd plugins/gauntlet
   python scripts/curate_problems.py data/problems/ --output /tmp/gauntlet-curate-report.md
   ```

3. **Identify gaps**: categories whose actual count falls below
   the `neetcode_count` in the manifest.
   The script sorts gaps largest-first so the worst shortfalls
   appear at the top.

4. **Review existing problems** in each gap category to understand
   what is already covered before proposing additions.

5. **Propose new YAML entries** following the schema below.
   Add proposals to the report under "Proposed New Problems".
   Do NOT write proposals directly into `data/problems/*.yaml`.

6. **Validate proposals** by running:

   ```bash
   python -c "
   import yaml, sys
   sys.path.insert(0, 'src')
   from gauntlet.models import BankProblem
   proposals = yaml.safe_load(open('proposals.yaml'))
   for p in proposals:
       BankProblem.from_dict(p)
   print('All proposals valid.')
   "
   ```

7. **Present the report** to the human for review.
   The report includes the coverage table, gap list, and proposed
   entries.
   The human decides which proposals to merge into the YAML files.

## Problem Schema

Each proposed entry must follow this schema:

```yaml
- id: category-NNN
  title: Problem Title
  difficulty: easy       # easy | medium | hard | extra_hard
  prompt: |
    Problem statement with constraints and examples.
  hints:
    - First hint.
    - Second hint.
  solution_outline: |
    Approach and time/space complexity.
  tags: [tag1, tag2]
  neetcode_id: neetcode-NNN
  challenge_type: explain_why  # explain_why | multiple_choice | trace
                                # | code_complete | debug | rank
```

Required fields: `id`, `title`, `difficulty`, `prompt`.
Optional fields default to empty values.

## Safety Constraints

- Never modify files under `data/problems/` directly.
- Never run with a `--write` or `--fix` flag: the script
  intentionally has none.
- All output is a proposal report for human approval.
- Existing hand-curated problems are never touched.

## Output

A markdown report at the path specified by `--output`, containing:

- Coverage summary table (expected vs. actual per category)
- Gaps list sorted by missing count
- YAML schema template for new proposals
- Space for the human reviewer to add proposed entries

Human review is required before any YAML file changes.
