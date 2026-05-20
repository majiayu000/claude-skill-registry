---
name: skill-forge-evolve
description: >
  Improve and iterate on existing Claude Code skills based on usage feedback,
  test results, or changing requirements. Handles under/over-triggering fixes,
  instruction refinement, new sub-skill addition, and architecture evolution.
  Use when user says "improve skill", "fix skill", "skill not triggering",
  "skill triggers too much", "update skill", or "evolve skill".
---

# Skill Evolution & Improvement

## Process

### Step 1: Diagnose the Issue

Ask the user or analyze logs to identify the problem category:

**Category A: Triggering Issues**
- Under-triggering: Skill doesn't activate when it should
- Over-triggering: Skill activates when it shouldn't
- Mis-triggering: Wrong sub-skill activates

**Category B: Execution Issues**
- Incomplete workflows: Skill stops before finishing
- Incorrect output: Results don't match expectations
- Missing error handling: Failures not handled gracefully
- Performance: Too slow or too many token used

**Category C: Architecture Issues**
- Missing capability: New use case not covered
- Scale issues: Skill too large, needs decomposition
- Cross-reference problems: Links to non-existent files

**Category D: Quality Issues**
- Inconsistent results: Different outputs for same input
- Vague instructions: Claude interprets differently each time
- Missing examples: No concrete guidance

### Step 2: Apply Fix by Category

#### Fix: Under-Triggering

1. Read current description
2. Identify missing trigger phrases
3. Add domain keywords and paraphrases
4. Add file type mentions if relevant
5. Test with 5 queries that should now trigger

**Common causes:**
- Description too generic
- Missing common paraphrases
- Technical jargon without lay terms

**Fix template:**
```yaml
# Before (under-triggers)
description: Analyzes code quality

# After (specific triggers)
description: >
  Static code analysis and quality assessment. Checks code style,
  complexity, security vulnerabilities, and test coverage. Use when
  user says "code review", "code quality", "lint", "static analysis",
  "code smell", "code audit", or "check my code".
```

#### Fix: Over-Triggering

1. Read current description
2. Identify why unrelated queries trigger it
3. Add negative triggers ("Do NOT use for...")
4. Make description more specific
5. Test with 5 queries that should NOT trigger

**Fix template:**
```yaml
# Before (over-triggers)
description: Processes documents for review

# After (specific + negative triggers)
description: >
  Processes PDF legal documents for contract clause extraction and
  compliance review. Use for legal contracts, NDAs, terms of service.
  Do NOT use for general document editing, formatting, or non-legal PDFs.
```

#### Fix: Execution Issues

1. Identify the failing step in the workflow
2. Add explicit validation gates between steps
3. Add error handling with clear recovery instructions
4. Add "If X fails, then Y" fallback paths
5. Consider adding a script for fragile operations

#### Fix: Quality Issues

1. Replace vague instructions with specific ones
2. Add concrete examples of expected input/output
3. Add explicit "do this, not that" comparisons
4. Add quality check steps before final output
5. Consider adding a validation script

### Step 3: Iteration Workspace Protocol

Use structured workspaces to track improvements across iterations:

```
eval-workspace/
  iteration-1/          # First version
    eval-0/with_skill/  # Eval results
    eval-0/baseline/
    benchmark.json      # Aggregated metrics
    benchmark.md        # Human-readable report
    feedback.json       # User feedback
  iteration-2/          # After first improvement
    eval-0/with_skill/
    eval-0/baseline/
    benchmark.json
    benchmark.md
    feedback.json
```

**The iteration loop:**
1. Apply the fix to the skill
2. Run `/skill-forge eval <path>` into `iteration-<N+1>/`
3. Run `/skill-forge benchmark <path>` with `--previous iteration-<N>/`
4. Review benchmark comparison for regressions
5. Collect user feedback into `feedback.json`
6. Read feedback and iterate (back to Step 2)

**Stop iterating when:**
- User says they're happy
- All feedback is empty (everything looks good)
- Benchmark shows no meaningful progress between iterations
- Pass rate meets the defined thresholds

### Step 3b: Self-Annealing Loop

For quick fixes without full eval pipeline:

```
1. Apply the fix
2. Test with the original failing case
3. Test with 3 other cases (regression check)
4. If fix works:
   -> Update the directive/SKILL.md
   -> Document the learning in references or SKILL.md
5. If fix fails:
   -> Diagnose why
   -> Try alternative approach
   -> Repeat
```

### Step 3c: Description Optimization Loop

For triggering issues (Category A), use the automated optimization loop:

1. Generate trigger eval set: `python scripts/generate_eval_set.py <path>`
2. Review and refine the eval set with the user
3. Run optimization: `python scripts/optimize_description.py <path> --eval-set evals.json`
4. Review the train/test split scores and improvement suggestions
5. Apply suggested description changes
6. Re-run optimization to measure improvement
7. Select the description with the highest **test score** (not train — avoids overfitting)
8. Iterate up to 5 times or until test score plateaus

### Step 4: Architecture Evolution

When a skill outgrows its tier:

**Tier 1 -> Tier 2** (needs scripts):
1. Identify the fragile/deterministic operation
2. Create script in `scripts/`
3. Update SKILL.md to reference the script
4. Test script independently

**Tier 2 -> Tier 3** (needs sub-skills):
1. Identify distinct workflows that can be separated
2. Extract each into its own `skills/{parent}-{child}/SKILL.md`
3. Update main SKILL.md with routing table
4. Move shared knowledge to `references/`
5. Update install.sh

**Tier 3 -> Tier 4** (needs agents):
1. Identify workflows that can run in parallel
2. Create agent definitions in `agents/`
3. Update the audit/full-analysis sub-skill to delegate to agents
4. Test parallel execution

### Step 5: Version Management

After evolution:
1. Update `metadata.version` in frontmatter (if present)
2. Add learning to SKILL.md or reference file
3. Update any affected cross-references
4. Re-run validation: `python scripts/validate_skill.py <path>`
5. Test full workflow end-to-end

## Common Evolution Patterns

### Pattern: Adding Industry Detection
When a skill needs to adapt behavior by user type:
```markdown
## Industry Detection
Detect user type from context:
- **Type A**: [signals] -> [behavior]
- **Type B**: [signals] -> [behavior]
```

### Pattern: Adding Quality Gates
When output quality is inconsistent:
```markdown
## Quality Gates
Before delivering output:
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
```

### Pattern: Adding Scoring
When users need measurable output:
```markdown
## Scoring (0-100)
| Category | Weight |
|----------|--------|
| Category A | 30% |
| Category B | 30% |
| Category C | 20% |
| Category D | 20% |
```
