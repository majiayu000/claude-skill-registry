---
name: skill-enhancer
description: AI-powered enhancement of skill SKILL.md files. Use to transform basic templates into comprehensive, high-quality skill documentation.
tools: Read, Write, Bash
---

# Skill Enhancer Skill

## Purpose

Single responsibility: Enhance basic SKILL.md files using AI to extract better examples, create comprehensive guides, and improve overall skill quality. (BP-4)

## Grounding Checkpoint (Archetype 1 Mitigation)

Before executing, VERIFY:

- [ ] Skill directory exists with SKILL.md and references/
- [ ] Reference files contain actual content (not empty)
- [ ] Enhancement mode selected (local or API)
- [ ] Backup of original SKILL.md created

**DO NOT enhance without backing up original content.**

## Uncertainty Escalation (Archetype 2 Mitigation)

ASK USER instead of guessing when:

- Content quality too low for meaningful enhancement
- Multiple valid enhancement directions possible
- Target audience unclear
- Enhancement scope undefined (full vs partial)

**NEVER hallucinate content not present in references.**

## Context Scope (Archetype 3 Mitigation)

| Context Type | Included | Excluded |
|--------------|----------|----------|
| RELEVANT | SKILL.md, references/, skill purpose | Other skills |
| PERIPHERAL | Similar high-quality skills as examples | Unrelated documentation |
| DISTRACTOR | Source scraping details | Enhancement history |

## Enhancement Modes

| Mode | Method | Cost | Quality |
|------|--------|------|---------|
| Local | Claude Code Max plan | Free | 9/10 |
| API | Anthropic API | ~$0.05-0.20 | 9/10 |
| Manual | Guided template | Free | Variable |

## Workflow Steps

### Step 1: Backup Original (Grounding)

```bash
# Create backup
cp output/<skill-name>/SKILL.md output/<skill-name>/SKILL.md.backup

# Record backup timestamp
echo "Backup created: $(date)" > output/<skill-name>/.enhancement_backup
```

### Step 2: Analyze Current Content

```bash
# Check current SKILL.md quality
wc -l output/<skill-name>/SKILL.md
grep -c '```' output/<skill-name>/SKILL.md  # Code examples
grep -c '^## ' output/<skill-name>/SKILL.md  # Sections

# List reference files
ls -la output/<skill-name>/references/

# Sample reference content
head -50 output/<skill-name>/references/*.md
```

### Step 3: Execute Enhancement

**Option A: Local Enhancement (Recommended)**

Using Claude Code Max (no API costs):

```bash
# With skill-seekers
skill-seekers enhance output/<skill-name>/ --local

# This opens Claude Code in new terminal
# AI analyzes references and enhances SKILL.md
# Takes 30-60 seconds
```

**Option B: API Enhancement**

```bash
# Set API key
export ANTHROPIC_API_KEY=sk-ant-...

# Run API enhancement
skill-seekers enhance output/<skill-name>/ --api
```

**Option C: Manual Enhancement Template**

Use this prompt with any AI:

```
Analyze the reference documentation in the following files:
[list reference files]

Based on this documentation, enhance the SKILL.md to include:
1. 5-10 practical code examples (extracted from references)
2. Comprehensive quick reference section
3. Key concepts explanation
4. Common patterns and best practices
5. FAQ based on common questions in docs

Keep all content grounded in the actual documentation.
Do not invent features not present in references.
```

### Step 4: Validate Enhancement

```bash
# Compare before/after
wc -l output/<skill-name>/SKILL.md.backup output/<skill-name>/SKILL.md

# Check for code examples
grep -c '```' output/<skill-name>/SKILL.md

# Verify no hallucinations (spot check)
# Examples in SKILL.md should reference content in references/
```

### Step 5: Review Changes

```bash
# Show diff
diff output/<skill-name>/SKILL.md.backup output/<skill-name>/SKILL.md | head -100

# Or visual diff if available
code --diff output/<skill-name>/SKILL.md.backup output/<skill-name>/SKILL.md
```

## Recovery Protocol (Archetype 4 Mitigation)

On error:

1. **PAUSE** - Keep backup intact
2. **DIAGNOSE** - Check error type:
   - `API error` → Switch to local mode
   - `Low quality output` → Restore backup, try different approach
   - `Timeout` → Retry with smaller reference set
   - `Hallucination detected` → Restore backup, manual enhancement
3. **ADAPT** - Switch enhancement mode
4. **RETRY** - With different parameters (max 3 attempts)
5. **ESCALATE** - Restore backup, present options to user

**Rollback command:**
```bash
mv output/<skill-name>/SKILL.md.backup output/<skill-name>/SKILL.md
```

## Checkpoint Support

State saved to: `.aiwg/working/checkpoints/skill-enhancer/`

```
checkpoints/skill-enhancer/
├── original_skill_md.md    # Backup of original
├── reference_analysis.json # What was analyzed
├── enhancement_config.json # Settings used
└── enhancement_log.txt     # Process log
```

## Enhancement Quality Metrics

| Metric | Before | Target After |
|--------|--------|--------------|
| SKILL.md lines | ~75 | ~300-500 |
| Code examples | 0-2 | 5-10 |
| Sections | 3-5 | 8-12 |
| Quick reference | None | Comprehensive |
| FAQ | None | 5-10 questions |

## Quality Validation

After enhancement, verify:

1. **No Hallucinations**: All examples exist in references
2. **Completeness**: All major topics covered
3. **Accuracy**: Code examples are syntactically correct
4. **Usefulness**: Answers common questions
5. **Navigation**: Clear links to reference files

```bash
# Spot-check example against references
example=$(grep -A 5 '```' output/<skill-name>/SKILL.md | head -6)
grep -r "$example" output/<skill-name>/references/
# Should find matching content
```

## Configuration Options

```json
{
  "skill_dir": "output/myskill/",
  "mode": "local",
  "options": {
    "max_examples": 10,
    "include_faq": true,
    "include_quick_ref": true,
    "preserve_sections": ["Description", "Key Features"],
    "enhance_sections": ["Code Examples", "Quick Reference", "FAQ"]
  },
  "quality": {
    "min_examples": 5,
    "min_lines": 200,
    "require_navigation": true
  }
}
```

## Common Enhancement Patterns

### Pattern 1: Example Extraction
Find code blocks in references, select most practical ones.

### Pattern 2: FAQ Generation
Identify question-like content, common patterns, edge cases.

### Pattern 3: Quick Reference
Extract key APIs, common parameters, return types.

### Pattern 4: Best Practices
Identify recommendations, warnings, tips in documentation.

## Troubleshooting

| Issue | Diagnosis | Solution |
|-------|-----------|----------|
| No improvement | References too sparse | Add more reference content first |
| Hallucinations | AI invented features | Restore backup, use stricter prompt |
| Timeout | References too large | Enhance in sections |
| Quality low | Poor reference quality | Clean references first |

## References

- Skill Seekers Enhancement: https://github.com/jmagly/Skill_Seekers
- REF-001: Production-Grade Agentic Workflows (BP-2 direct functions, BP-4)
- REF-002: LLM Failure Modes (Archetype 2 over-helpfulness critical)
