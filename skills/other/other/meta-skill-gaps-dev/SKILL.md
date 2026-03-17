---
name: meta-skill-gaps-dev
description: Identify skill coverage gaps and improvement opportunities. Use when analyzing missing skills for a task, creating skill gap issues, evaluating skill effectiveness, or refining skill progressive disclosure.
---

# Skill Gap Analysis & Improvement

Systematic methodology for identifying missing skills and improving existing ones.

## When to Use This Skill

- Analyzing skill coverage for a multi-domain task
- Creating issues for missing skills
- Evaluating whether loaded skills were effective
- Refining skills that loaded too much/too little context
- Identifying opportunities for derivative skills

---

## Gap Detection

### Domain Taxonomy

Map user requests to expected skill categories:

| Domain Type | Pattern | Examples |
|-------------|---------|----------|
| **Language** | `lang-<lang>-<pattern>-<focus>` | `lang-rust-library-dev`, `lang-zig-dev` |
| **Platform** | `cloud-<platform>-<service>-<focus>` | `cloud-aws-lambda-dev` |
| **Tool** | `<category>-<tool>-<focus>` | `iac-terraform-modules-eng` |
| **Service** | `<service>-<focus>` | `openmetadata-sdk-dev` |
| **Pattern** | `meta-<pattern>-<focus>` | `meta-library-dev`, `meta-sdk-patterns-eng` |
| **Method** | `method-<method>-<focus>` | `method-tdd-dev` |

### Gap Detection Algorithm

```
1. Parse user request for domain keywords
2. For each keyword:
   a. Search local skills: components/skills/*<keyword>*
   b. Search loaded skills in current context
   c. If no match → GAP DETECTED
3. Check for compound gaps:
   - Language + Pattern (e.g., "Zig" + "library" → no lang-zig-library-dev)
   - Service + Pattern (e.g., "OpenMetadata" + "plugin" → no openmetadata-plugin-dev)
```

### Gap Categories

| Gap Type | Description | Priority |
|----------|-------------|----------|
| **Complete** | No skill for the domain at all | High |
| **Derivative** | Meta-skill exists but no domain-specific derivative | Medium |
| **Compound** | Domain skills exist separately but not combined | Medium |
| **Depth** | Skill exists but lacks needed detail | Low |

---

## Issue Creation Workflow

### When to Create Issues

Create issue when:
- User confirms gap should be addressed
- Gap is "Complete" or "Derivative" type
- Domain is general enough to benefit future tasks

Skip issue when:
- One-off project-specific need
- User declines
- Very niche domain unlikely to recur

### Issue Template

```markdown
## Summary

Skill gap identified: No coverage for <domain>.

**Detected during:** <brief task description>
**Gap type:** <Complete | Derivative | Compound | Depth>
**User request snippet:** "<relevant quote>"

## Proposed Skill

| Field | Value |
|-------|-------|
| **Name** | `<proposed-skill-name>` |
| **Extends** | `<meta-skill if derivative>` |
| **Category** | `<lang \| cloud \| iac \| method \| ...>` |
| **Focus** | `<dev \| ops \| eng>` |

## Context

<Why this skill would be useful>

## Related Skills

- `<existing-related-skill-1>`
- `<existing-related-skill-2>`
```

### GitHub CLI Command

```bash
gh issue create --repo aRustyDev/ai \
  --title "feat(skills): add <skill-name> skill" \
  --body "<issue-body>" \
  --label "skill-gap"
```

---

## Skill Effectiveness Review

### Review Triggers

Evaluate skills when:
- Task completes successfully
- User corrects Claude's approach
- User provides information the skill should have covered
- Significant context was loaded but unused

### Evaluation Criteria

| Criterion | Question | Score |
|-----------|----------|-------|
| **Relevance** | Did the skill match the task? | 0-3 |
| **Coverage** | Did it cover what was needed? | 0-3 |
| **Precision** | Was loaded context mostly used? | 0-3 |
| **Accuracy** | Was the information correct? | 0-3 |

**Scoring:**
- 0 = Not at all
- 1 = Partially
- 2 = Mostly
- 3 = Completely

**Action thresholds:**
- Total < 6: Major revision needed
- Total 6-9: Refinement opportunities
- Total 10-12: Skill is effective

### Common Issues

| Symptom | Diagnosis | Solution |
|---------|-----------|----------|
| Large unused sections | Over-broad trigger | Narrow description keywords |
| User provided missing info | Coverage gap | Add missing section |
| Wrong approach suggested | Outdated content | Update with correct patterns |
| Too generic | Missing derivative | Create domain-specific skill |
| Loaded but not helpful | Trigger too broad | Refine trigger phrases |

---

## Progressive Disclosure Refinement

### When to Refactor

Refactor skill structure when:
- SKILL.md exceeds 500 lines
- Specific sections rarely used together
- Different user personas need different depths

### Refactoring Patterns

**Extract to References:**
```
Before: 800-line SKILL.md with everything inline

After:
├── SKILL.md (200 lines - overview, quick reference)
└── references/
    ├── detailed-workflow.md
    ├── api-reference.md
    └── troubleshooting.md
```

**Split by Use Case:**
```
Before: One skill covers dev + ops + troubleshooting

After:
├── <tool>-dev/SKILL.md     (development)
├── <tool>-ops/SKILL.md     (operations)
└── <tool>-debug/SKILL.md   (troubleshooting)
```

**Create Derivatives:**
```
Before: Generic skill tries to cover all languages

After:
├── meta-<pattern>-<focus>/SKILL.md     (foundational)
├── lang-rust-<pattern>-<focus>/SKILL.md  (Rust-specific)
└── lang-python-<pattern>-<focus>/SKILL.md (Python-specific)
```

### Reference File Structure

```markdown
# <Reference Title>

## When to Load This Reference

<Specific scenarios when this content is needed>

## Content

<Detailed content that doesn't need to be in main SKILL.md>
```

---

## Derivative Skill Detection

### When to Suggest Derivatives

Suggest derivative when:
- Meta-skill loaded but user needs language-specific patterns
- Multiple languages/platforms apply same pattern
- User asks for "<domain> <pattern>" combination

### Derivative Gap Examples

| User Request | Meta-Skill | Missing Derivative |
|--------------|------------|-------------------|
| "Zig library" | `meta-library-dev` | `lang-zig-library-dev` |
| "Python SDK for Stripe" | `meta-sdk-patterns-eng` | `lang-python-sdk-dev` |
| "Rust CLI tool" | `meta-cli-patterns-dev` | `lang-rust-cli-dev` |
| "Go plugin for OpenMetadata" | `meta-plugin-dev` | `openmetadata-plugin-go-dev` |

### Derivative Creation Checklist

Before creating derivative:
- [ ] Meta-skill exists and is stable
- [ ] Domain has enough specific content to warrant skill
- [ ] Not a one-off need
- [ ] User confirms value

---

## Feedback Collection

### What to Track

| Data Point | Purpose |
|------------|---------|
| Skills loaded | Measure coverage |
| Sections referenced | Identify unused content |
| User corrections | Find accuracy issues |
| Missing information | Find coverage gaps |
| Task success/failure | Correlate with skill quality |

### Session Summary Format

```markdown
## Skill Usage Summary

**Task:** <brief description>

### Skills Loaded
| Skill | Sections Used | Effectiveness |
|-------|---------------|---------------|
| `skill-1` | Overview, Quick Ref | High |
| `skill-2` | None (loaded but unused) | Low |

### Gaps Identified
- [ ] No skill for <domain-1>
- [ ] `skill-2` missing <topic> coverage

### Improvement Opportunities
- `skill-1`: Consider extracting <section> to reference
- `skill-2`: Trigger too broad, refine description
```

---

## Quick Reference

| Task | Action |
|------|--------|
| Check for gaps | Search `components/skills/*<keyword>*` |
| Create gap issue | `gh issue create --repo aRustyDev/ai ...` |
| Evaluate skill | Score relevance, coverage, precision, accuracy |
| Refactor large skill | Extract to `references/` |
| Create derivative | Follow `meta-skill-authoring-dev` → Derivatives section |

## References

- `meta-skill-authoring-dev` - How to create skills
- `rules/skill-gap-detection.md` - When to invoke this skill
