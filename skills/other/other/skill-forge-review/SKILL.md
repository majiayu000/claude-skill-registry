---
name: skill-forge-review
description: >
  Audit and validate existing Claude Code skills for quality, triggering accuracy,
  structure compliance, and best practices. Scores skills on a 0-100 scale and
  provides prioritized improvement recommendations. Use when user says "review skill",
  "audit skill", "check skill", "validate skill", or "skill quality".
---

# Skill Review & Validation

## Process

### Step 1: Locate Skill Files

Accept input as:
- Path to a skill directory
- Skill name (search in `~/.claude/skills/`)
- URL to a GitHub repository

Read all `.md` files, scripts, and asset files.

### Step 2: Structure Validation

Run `python scripts/validate_skill.py <path>` for programmatic checks.

Manual verification:
- [ ] SKILL.md exists (exact case)
- [ ] No README.md inside skill folder
- [ ] Folder name matches `name` field
- [ ] Valid kebab-case naming (1-64 chars)
- [ ] No "claude" or "anthropic" in name

### Step 3: Frontmatter Audit

| Check | Pass Criteria |
|-------|--------------|
| Name format | kebab-case, 1-64 chars, no leading/trailing hyphens |
| Description present | Non-empty, 1-1024 characters |
| Description has WHAT | Explains capabilities |
| Description has WHEN | Includes trigger phrases |
| Description has keywords | Domain-specific terms included |
| No XML tags | No < or > characters |
| Optional fields valid | license, compatibility (<500 chars), metadata |

### Step 4: Triggering Analysis

Assess the description for activation quality:

**Under-triggering risks:**
- Too generic ("Helps with projects")
- Missing common paraphrases
- No domain keywords
- Missing file type mentions (if relevant)

**Over-triggering risks:**
- Too broad ("Processes documents")
- Overlaps with built-in Claude capabilities
- Missing negative triggers for disambiguation

**Generate test queries:**
- 5 queries that SHOULD trigger the skill
- 5 queries that SHOULD NOT trigger
- 3 edge cases (ambiguous queries)

### Step 5: Instruction Quality

| Criterion | Score (0-10) |
|-----------|-------------|
| Specificity | Are instructions actionable? (not "validate properly") |
| Completeness | All workflows covered? |
| Error handling | Common failures addressed? |
| Examples | Concrete examples provided? |
| Progressive disclosure | Detailed docs in references/ not SKILL.md? |
| Length | Under 500 lines / 5000 tokens? |
| Cross-references | Clear links to references/scripts? |

### Step 6: Architecture Review (Multi-skill)

For skills with sub-skills:
- [ ] Main skill has clear routing table
- [ ] Sub-skills have focused responsibilities
- [ ] Cross-references are valid (files exist)
- [ ] Naming follows `parent-child` convention
- [ ] Shared references in parent, not duplicated
- [ ] Agents have clear roles (if Tier 4)

### Step 7: Script Quality (if present)

- [ ] Docstrings with purpose, input, output
- [ ] CLI interface (argparse or similar)
- [ ] Structured output (JSON)
- [ ] Error handling (try/except with clear messages)
- [ ] No hardcoded paths or secrets
- [ ] Minimal dependencies

### Step 8: Generate Skill Health Score

**Scoring methodology (0-100):**

| Category | Weight | Checks |
|----------|--------|--------|
| Frontmatter Quality | 25% | Name, description, format |
| Trigger Accuracy | 20% | WHAT + WHEN + keywords |
| Instruction Quality | 25% | Specificity, completeness, examples |
| Structure Compliance | 15% | File naming, organization, references |
| Script Quality | 10% | If applicable (full marks if no scripts needed) |
| Progressive Disclosure | 5% | Proper use of 3-level system |

### Step 9: Generate Trigger Eval Set

After reviewing, generate a structured trigger eval set for ongoing testing:

1. Run `python scripts/generate_eval_set.py <path>` to auto-generate a starter set
2. Review and refine the generated queries:
   - Ensure 8-10 should-trigger queries cover different phrasings and edge cases
   - Ensure 8-10 should-not-trigger queries are near-misses (not obviously irrelevant)
   - Include casual speech, typos, and uncommon domain uses in should-trigger set
3. Save the eval set to `evals/evals.json` in the skill directory

**Good queries** are realistic and specific (include file paths, context, domain details).
**Bad queries** are overly generic ("format this data") or obviously irrelevant.

4. Run `python scripts/optimize_description.py <path> --eval-set evals/evals.json`
   to score the current description and get improvement suggestions
5. Recommend running `/skill-forge eval <path>` for full functional evaluation

### Step 10: Generate Report

```markdown
# Skill Review: [name]

## Health Score: [X]/100

## Summary
[2-3 sentence assessment]

## Scores by Category
| Category | Score | Notes |
|----------|-------|-------|
| Frontmatter | X/25 | [issues] |
| Triggering | X/20 | [issues] |
| Instructions | X/25 | [issues] |
| Structure | X/15 | [issues] |
| Scripts | X/10 | [issues] |
| Disclosure | X/5 | [issues] |

## Critical Issues (fix immediately)
- [issue 1]
- [issue 2]

## High Priority (fix within 1 week)
- [issue 1]

## Recommendations
- [suggestion 1]
- [suggestion 2]

## Suggested Test Queries
### Should Trigger
1. [query]
2. [query]
3. [query]

### Should NOT Trigger
1. [query]
2. [query]
3. [query]
```
