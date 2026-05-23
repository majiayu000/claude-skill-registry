---
name: skill-auditor
description: Audit existing skills (global and project-level) for agent-friendliness, consistency, and best practices. Use when asked to "audit my skills", "review skill setup", "analyze skill quality", "check skill health", "improve my skills", or when wanting an assessment of the overall skill ecosystem. Provides actionable recommendations for improving skill effectiveness.
---

# Skill Auditor

Comprehensive assessment of your skill ecosystem with actionable recommendations.

## Workflow

### Phase 1: Inventory

Gather all skills from:

1. **Global skills**: `~/.claude/skills/*/SKILL.md`
2. **Project skills**: `./skills/*/SKILL.md` or `./.claude/skills/*/SKILL.md`

For each skill, extract:
- Name and description from frontmatter
- Line count of SKILL.md
- Presence of reference files, scripts, assets
- Any non-standard frontmatter fields

### Phase 2: Individual Assessment

Evaluate each skill against these criteria:

#### Frontmatter Quality

| Criterion | Check |
|-----------|-------|
| **Description completeness** | Does it explain both WHAT and WHEN? |
| **Trigger coverage** | Are all reasonable trigger phrases included? |
| **Description length** | Sufficient detail without being excessive (50-300 words ideal) |
| **Non-standard fields** | Any fields beyond name/description? (often unnecessary) |

#### Content Quality

| Criterion | Check |
|-----------|-------|
| **Line count** | Under 500 lines? (Over suggests need for reference split) |
| **Progressive disclosure** | Does it use reference files for detailed content? |
| **Actionability** | Are instructions concrete and procedural? |
| **Output contracts** | Does it specify expected output format? |
| **Examples** | Does it include good/bad examples where helpful? |

#### Structure Quality

| Criterion | Check |
|-----------|-------|
| **Reference organization** | Are references in `references/` directory? |
| **Script availability** | Are reusable operations scripted? |
| **Internal links** | Are reference files linked from SKILL.md? |
| **Naming consistency** | Do file names follow conventions? |

### Phase 3: Ecosystem Assessment

Evaluate the skill collection as a whole:

#### Coverage Analysis

- **Domain clusters**: What areas do skills cover? Any gaps?
- **Overlap detection**: Do multiple skills cover similar territory?
- **Workflow completeness**: Can common tasks be handled end-to-end?

#### Consistency Analysis

- **Style uniformity**: Do skills use consistent formatting?
- **Trigger pattern consistency**: Are similar skills triggered similarly?
- **Output format consistency**: Do related skills produce compatible outputs?

#### Organization Analysis

- **Global vs project split**: Are skills appropriately scoped?
- **Naming conventions**: Are names consistent and discoverable?
- **Documentation quality**: Is the overall system documented?

### Phase 4: Generate Report

## Output Format

```markdown
# Skill Ecosystem Audit

**Generated**: [timestamp]
**Skills audited**: [count] global, [count] project-level

## Executive Summary

[2-3 sentences: overall health, biggest opportunities, critical issues if any]

**Health Score**: [X/100]

## Quick Stats

| Metric | Value | Assessment |
|--------|-------|------------|
| Total skills | [n] | — |
| Avg SKILL.md lines | [n] | [Good/High/Concerning] |
| Skills over 500 lines | [n] | [Needs attention if >0] |
| Skills with references | [n]% | [Good if >30%] |
| Skills with scripts | [n]% | — |
| Duplicate coverage areas | [n] | [Needs review if >0] |

## Top Recommendations

### Priority 1: [Most impactful improvement]
[Specific action with affected skills]

### Priority 2: [Second improvement]
[Specific action with affected skills]

### Priority 3: [Third improvement]
[Specific action with affected skills]

## Individual Skill Assessments

### [skill-name] — [Grade: A/B/C/D]

**Strengths:**
- [What works well]

**Issues:**
- [Specific problem] → [Specific fix]

**Quick wins:**
- [ ] [Actionable improvement]

[Repeat for each skill, ordered by grade (worst first for attention)]

## Domain Coverage Map

| Domain | Skills | Coverage |
|--------|--------|----------|
| [e.g., Design] | [list] | [Complete/Partial/Gap] |
| [e.g., Code Quality] | [list] | [Complete/Partial/Gap] |

## Overlap Analysis

[If overlaps exist, describe which skills overlap and recommend consolidation]

## Ecosystem Recommendations

### Organization
- [Recommendations for how skills are organized]

### Consistency
- [Recommendations for standardizing across skills]

### Missing Skills
- [Suggestions for skills that would complement the ecosystem]
```

## Grading Rubric

### Individual Skills

| Grade | Criteria |
|-------|----------|
| **A** | Clear triggers, concise content (<300 lines), uses references appropriately, has output contract, well-organized |
| **B** | Good triggers, reasonable length, mostly organized, minor improvements possible |
| **C** | Triggers could be better, content somewhat long, organization issues, needs work |
| **D** | Weak triggers, bloated content (>500 lines), poor organization, significant rewrite needed |

### Ecosystem Health Score

Calculate from:
- Average individual grade (40%)
- Coverage breadth without overlap (20%)
- Consistency across skills (20%)
- Progressive disclosure usage (10%)
- Script/automation presence (10%)

## Common Issues & Fixes

### "Description doesn't include trigger phrases"
**Fix**: Add explicit "Use when..." phrases that match how users actually invoke the skill.

### "SKILL.md over 500 lines"
**Fix**: Move detailed content to `references/` files. Keep only workflow and essential quick-reference in SKILL.md.

### "No output contract"
**Fix**: Add a section specifying what format the skill's output should take.

### "Duplicate coverage with [other-skill]"
**Fix**: Either consolidate into one skill, or clearly differentiate triggers so they don't compete.

### "Missing reference links"
**Fix**: If references exist, link them from SKILL.md with guidance on when to load each.

### "Non-standard frontmatter fields"
**Fix**: Remove fields beyond `name` and `description` unless specifically needed for skill behavior (rare).

## Proactive Recommendations

Based on common skill ecosystem patterns, also check for:

1. **Missing meta-skill**: Is there a skill for creating/improving skills? (skill-creator)
2. **Missing checkpoint skill**: Is there a way to pause and assess? (checkpoint)
3. **Missing handoff skill**: Can sessions be continued? (bootstrap)
4. **Missing review skills**: Are there skills for quality gates? (code review, design critique)

## Running the Audit

### Quick audit (overview only)
```bash
# Count skills and sizes
find ~/.claude/skills -name "SKILL.md" -exec wc -l {} \; | sort -n
find ./skills -name "SKILL.md" -exec wc -l {} \; 2>/dev/null | sort -n
```

### Full audit
1. Inventory all skills
2. Read each SKILL.md frontmatter and assess
3. Check for reference/script directories
4. Compile findings into report format above

## When to Audit

- **After adding several new skills**: Check for overlap and consistency
- **Periodically (quarterly)**: Ensure ecosystem stays healthy
- **Before sharing skills**: Verify quality before distribution
- **When skills feel ineffective**: Diagnose what's not working
