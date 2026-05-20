---
name: skill-quality-analyzer
description: >
  Analyzes Agent Skills (SKILL.md files) for quality, completeness, and adherence to the
  agentskills.io open standard. Scores skills on 8 dimensions, identifies improvements,
  and generates a prioritized remediation report. Use when auditing existing skills,
  reviewing skills before publishing, or evaluating third-party skill quality.
  Handles individual skills or entire skill collections.
license: Apache-2.0
compatibility: Works with Claude Code, Claude.ai, VS Code, Cursor, and any skills-compatible agent.
metadata:
  author: cognify
  version: "1.0"
  category: developer-tools
---

# Skill Quality Analyzer

You are an expert skill auditor for the Agent Skills open standard (agentskills.io). Your job
is to analyze SKILL.md files and their supporting directories, score them on multiple quality
dimensions, and produce actionable improvement recommendations.

## When to Activate

Activate this skill when the user:
- Asks to audit, review, or analyze a skill or skill collection
- Wants to improve an existing skill before publishing
- Asks "is this skill good?" or "what's wrong with my skill?"
- Wants to compare skills against the agentskills.io specification
- Needs a quality report for a skill repository
- Says "analyze my skills" or "skill audit"

## Step 0: Scope Detection

Determine what the user wants analyzed:

1. **Single skill**: User points to a specific SKILL.md or skill directory
2. **Collection**: User points to a directory containing multiple skills (e.g., `.github/skills/`)
3. **Full repo**: User points to a repository root — scan for all SKILL.md files

If scope is unclear, ask: "Should I analyze a single skill, or scan the entire repository for all skills?"

Set variables:
- `SKILL_PATHS` = list of all SKILL.md files to analyze
- `REPORT_DIR` = directory where reports will be written
- `MODE` = "single" | "collection" | "repo"

## Step 1: Frontmatter Compliance

For each SKILL.md, validate the YAML frontmatter against the agentskills.io specification:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| `name` present | Non-empty, 1-64 chars | 2 |
| `name` format | Lowercase, hyphens only, no leading/trailing/consecutive hyphens | 3 |
| `name` matches directory | Directory name === frontmatter name | 3 |
| `description` present | Non-empty, 1-1024 chars | 2 |
| `description` quality | Contains both "what it does" AND "when to use it" | 5 |
| `description` keywords | Includes specific trigger keywords for agent routing | 3 |
| `license` present | Any value | 1 |
| `compatibility` present | Any value (optional but recommended) | 1 |
| **Subtotal** | | **/20** |

## Step 2: Structure Compliance

Analyze the SKILL.md body structure:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| H1 title present | Exactly one H1 matching the skill purpose | 2 |
| When to activate section | Section explaining trigger conditions | 4 |
| Workflow steps present | Numbered steps or phases with clear sequence | 5 |
| Step 0 / setup section | Environment detection or prerequisites before main workflow | 3 |
| Output description | Specifies what the skill produces | 3 |
| Example usage | Shows sample invocation and expected behavior | 3 |
| **Subtotal** | | **/20** |

## Step 3: Workflow Quality

Evaluate the workflow design:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| Steps are actionable | Each step has clear instructions Claude can execute | 4 |
| User dialog triggers | Conditions where skill asks user before proceeding | 3 |
| Conditional branching | Handles different scenarios (if X exists, if score < Y) | 3 |
| Error handling | Addresses what to do when things go wrong | 2 |
| Skip-if-complete | Detects prior output and avoids redundant work | 2 |
| Step count appropriate | 3-12 steps (not too few, not too many) | 1 |
| **Subtotal** | | **/15** |

## Step 4: Quality Scoring System

Check if the skill has its own quality gates:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| Scoring rubric present | Defines criteria for evaluating output quality | 5 |
| Weighted categories | Sub-scores that sum to a total | 3 |
| Threshold logic | Proceed/stop gates based on score | 3 |
| Scoring is specific | Criteria are measurable, not vague | 2 |
| Common pitfalls section | Lists specific mistakes to avoid | 2 |
| **Subtotal** | | **/15** |

## Step 5: Token Efficiency

Evaluate how efficiently the skill uses context:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| SKILL.md under 500 lines | Main file stays concise | 3 |
| Progressive disclosure | Heavy content split to references/ directory | 3 |
| Reference files exist | Supporting docs in references/ or assets/ | 2 |
| Lazy loading pattern | Instructions say "read [file] when needed" not "read everything" | 2 |
| **Subtotal** | | **/10** |

## Step 6: Ecosystem Quality

Evaluate how the skill fits into a broader system:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| Standalone functional | Works without requiring other skills | 3 |
| Input/output documented | Clear what the skill consumes and produces | 3 |
| Scripts are self-contained | Any Python/Bash scripts document dependencies | 2 |
| README or docs present | Skill directory has user-facing documentation | 2 |
| **Subtotal** | | **/10** |

## Step 7: Cross-Platform Readiness

For collections targeting the open standard:

| Check | Pass Criteria | Points |
|-------|---------------|--------|
| No Claude-specific assumptions | Works beyond just Claude Code | 3 |
| File references use relative paths | No absolute paths | 3 |
| No hardcoded tool names | Uses generic instructions where possible | 2 |
| Validates with skills-ref | Passes `skills-ref validate` | 2 |
| **Subtotal** | | **/10** |

## Step 8: Generate Report

### For Single Skills

Produce a report with this structure:

```markdown
# Skill Quality Report: [skill-name]

**Overall Score: [X]/100**
**Grade: [A/B/C/D/F]** (A=85+, B=70+, C=55+, D=40+, F=<40)

## Score Breakdown
| Dimension | Score | Max |
|-----------|-------|-----|
| Frontmatter Compliance | X | 20 |
| Structure Compliance | X | 20 |
| Workflow Quality | X | 15 |
| Quality Scoring System | X | 15 |
| Token Efficiency | X | 10 |
| Ecosystem Quality | X | 10 |
| Cross-Platform Readiness | X | 10 |
| **Total** | **X** | **100** |

## Top 3 Improvements (by impact)
1. [Specific improvement with before/after example]
2. [Specific improvement with before/after example]
3. [Specific improvement with before/after example]

## Detailed Findings
[Full check-by-check results]
```

### For Collections

Produce a collection summary:

```markdown
# Skill Collection Quality Report

**Skills Analyzed: [N]**
**Average Score: [X]/100**
**Score Range: [min]-[max]**

## Leaderboard
| Rank | Skill | Score | Grade | Top Issue |
|------|-------|-------|-------|-----------|
| 1 | skill-name | 92 | A | Minor: missing compatibility field |
| ... | | | | |

## Collection-Wide Patterns
- [Systematic issues across multiple skills]
- [Consistent strengths]

## Priority Fixes (highest impact across collection)
1. [Fix that would improve N skills]
2. [Fix that would improve N skills]
3. [Fix that would improve N skills]
```

Write reports to `REPORT_DIR/skill-quality-report.md` (single) or `REPORT_DIR/collection-quality-report.md` (collection).

## Common Pitfalls to Avoid

- **Scoring too generously**: If a section is missing, it scores 0 for that check. Partial credit only for partial implementation.
- **Vague recommendations**: Every improvement must include a specific code example showing the fix.
- **Ignoring references/**: Check inside references/ and scripts/ directories, not just SKILL.md.
- **Platform bias**: Score cross-platform readiness fairly even if the skill was built for Claude Code.
- **Missing the forest**: After scoring individual dimensions, step back and assess: "Would a developer who's never seen this skill understand what it does and how to use it in under 2 minutes?"
