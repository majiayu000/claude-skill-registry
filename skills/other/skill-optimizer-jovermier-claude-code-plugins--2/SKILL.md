---
name: skill-optimizer
description: Refactors Claude Code skills to reduce token usage 80-95% using Progressive Disclosure Architecture (PDA). Splits monolithic skills into orchestrator + reference files, extracts scripts, creates reference/ directories. Use when optimizing skills, improving skill efficiency, refactoring large/bloated skills, reducing token costs, applying PDA, modularizing skills, breaking down skills, or converting encyclopedia-style skills to orchestrator pattern.
allowed-tools: Read, Write, Edit, Glob
---

# Skill Optimizer

## Purpose

Transform existing Claude Code skills into optimized, efficient versions using Progressive Disclosure Architecture (PDA) and best practices. Achieve 80-95% token reduction while improving maintainability.

## When to Use

- User asks to "optimize this skill" or "improve this skill"
- Optimizing skill metadata for better detection/discovery
- Improving YAML frontmatter description for trigger coverage
- Refactoring monolithic skills
- Applying PDA to existing skills
- Reducing token costs
- Improving skill maintainability

## Optimization Process

### Phase 0: Metadata Optimization (Highest Impact)

**Always start here.** Optimizing the YAML frontmatter yields the highest ROI for skill detection and should be done first, before any content refactoring.

0. **Optimize YAML Frontmatter**
   - Analyze current `name` and `description` fields
   - Identify all potential trigger phrases and edge cases
   - Research best practices for skill discovery
   - Update description with comprehensive trigger coverage

   **Description Optimization Guidelines:**
   - Maximum 1024 characters (use available space)
   - Include both what the skill does AND when to use it
   - Add specific trigger phrases users might say
   - Include concrete metrics (e.g., "80-95% token savings")
   - Mention problem keywords (e.g., "large/bloated", "monolithic")
   - List action verbs (e.g., "optimize", "refactor", "modularize")
   - Add pattern keywords (e.g., "orchestrator", "PDA", "encyclopedia-style")
   - Write in third person
   - Balance specificity with coverage

   **Metadata Checklist:**
   - [ ] Description includes concrete metrics/savings
   - [ ] Problem keywords present (large, bloated, monolithic)
   - [ ] Multiple action verbs listed
   - [ ] Pattern terminology included (orchestrator, PDA)
   - [ ] Edge case triggers covered
   - [ ] Third-person voice maintained
   - [ ] Under 1024 character limit
   - [ ] Name follows conventions (lowercase, hyphens, <64 chars)

1. **Assess Current State**
   - Read SKILL.md
   - Calculate file size
   - Identify content types
   - Map reference opportunities

2. **Determine Optimization Strategy**
   ```
   If SKILL.md < 5KB:
     → Minor improvements only
     → Keep current structure

   If SKILL.md 5-10KB:
     → Consider progressive disclosure
     → Evaluate content organization

   If SKILL.md > 10KB:
     → Apply PDA strongly recommended
     → Split into orchestrator + references

   If SKILL.md > 20KB:
     → PDA essential
     → Major refactor needed
   ```

3. **Identify Content for Extraction**
   - API documentation → reference/api.md
   - Detailed examples → reference/examples.md
   - Troubleshooting → reference/troubleshooting.md
   - Domain-specific docs → reference/[domain].md

### Phase 2: Refactoring

4. **Create Orchestrator SKILL.md**
   - Keep only essential routing logic (3-5KB max)
   - Add conditional loading instructions
   - Include quick reference section
   - Link to detailed references

5. **Extract Reference Files**
   - Create reference/ directory
   - Move detailed docs to separate files
   - Add tables of contents for long files
   - Ensure one-level depth from SKILL.md

6. **Add Scripts (if applicable)**
   - Create scripts/ directory
   - Move mechanical operations to scripts
   - Document script usage
   - Add execution instructions

### Phase 3: Validation

7. **Verify PDA Implementation**
   - SKILL.md is now 3-5KB
   - References load on-demand
   - All links work correctly
   - File structure is standard

8. **Calculate Token Savings**
   ```
   Before: [original KB] KB per request
   After: [new KB] KB + on-demand average
   Savings: [percentage]%
   ```

9. **Test Navigation**
   - Can user find information quickly?
   - Are references clearly linked?
   - Is structure intuitive?

## Optimization Patterns

### Pattern 1: Encyclopedia to Orchestrator

**Before (50KB monolith):**
```markdown
# plantuml.md

## Sequence Diagrams
[8KB of syntax docs]

## Class Diagrams
[10KB of syntax docs]

## Flowcharts
[5KB of syntax docs]

... [27KB more]
```

**After (3KB orchestrator):**
```markdown
---
name: plantuml-diagrams
description: Generate PlantUML diagrams...
---

# PlantUML Diagram Generator

Analyze user request to determine diagram type.

**For sequence diagrams:**
1. Read reference/plantuml_sequence.md
2. Generate PlantUML code
3. Bash: scripts/plantuml.sh generate [code]

**For class diagrams:**
1. Read reference/plantuml_class.md
2. Generate PlantUML code
3. Bash: scripts/plantuml.sh generate [code]

**For flowcharts:**
1. Read reference/plantuml_flowchart.md
2. Generate PlantUML code
3. Bash: scripts/plantuml.sh generate [code]
```

**Savings:** 78-94%

### Pattern 2: Domain Split

**Before (25KB all-in-one):**
```markdown
# bigquery-skill

## Finance Data
[6KB of finance schema]

## Sales Data
[7KB of sales schema]

## Product Data
[6KB of product schema]

## Marketing Data
[6KB of marketing schema]
```

**After (2KB orchestrator):**
```markdown
---
name: bigquery-analytics
description: Analyze business data...
---

# BigQuery Data Analysis

## Available Datasets

**Finance**: Revenue, ARR, billing → Read [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline → Read [reference/sales.md](reference/sales.md)
**Product**: API usage, features → Read [reference/product.md](reference/product.md)
**Marketing**: Campaigns → Read [reference/marketing.md](reference/marketing.md)

## Process

1. Determine domain from user request
2. Read appropriate reference file
3. Construct query
4. Execute and format results
```

**Savings:** 80-92%

### Pattern 3: Script Extraction

**Before (inline instructions):**
```markdown
## Upload to Notion

1. Parse markdown file
2. Convert to Notion blocks
3. Call Notion API with page ID
4. Handle errors
[15KB of detailed API instructions]
```

**After (script + reference):**
```markdown
## Upload to Notion

**Process:**
1. Validate: `python scripts/validate.py [file]`
2. Upload: `python scripts/upload.py [file] [database-id]`
3. Report: URL returned

**For API details:** See [reference/notion-api.md](reference/notion-api.md)
```

**Savings:** 70-85%

## Refactoring Checklist

### Metadata Optimization (Phase 0 - Do First)
- [ ] YAML frontmatter reviewed
- [ ] Description includes concrete metrics
- [ ] Problem keywords added (large, bloated, monolithic)
- [ ] Multiple action verbs listed
- [ ] Pattern terminology included
- [ ] Trigger phrases comprehensive
- [ ] Character count verified (max 1024)
- [ ] Third-person voice maintained

### Structure Optimization
- [ ] SKILL.md reduced to 3-5KB
- [ ] reference/ directory created
- [ ] scripts/ directory created (if needed)
- [ ] File organization follows standards
- [ ] Paths use forward slashes

### Content Optimization
- [ ] Essential info in SKILL.md
- [ ] Detailed docs in reference/
- [ ] Examples moved to reference/examples.md
- [ ] API docs in reference/api.md
- [ ] Troubleshooting in reference/troubleshooting.md

### Link Optimization
- [ ] All references one level deep
- [ ] Links use relative paths
- [ ] Link text is descriptive
- [ ] No broken links
- [ ] Cross-references where helpful

### Token Optimization
- [ ] Progressive disclosure implemented
- [ ] On-demand loading pattern used
- [ ] Scripts for mechanical work
- [ ] Redundant content removed
- [ ] Token savings calculated

## Output Format

```markdown
# Skill Optimization Report

## Summary
**Before:** [original size] KB
**After:** [new size] KB + [avg on-demand] KB
**Token Savings:** [percentage]%

## Changes Made

### Structure Changes
- Created reference/ directory
- Split content into [N] reference files
- Created scripts/ with [N] scripts

### Content Reorganization
- SKILL.md now [size] KB (was [old size] KB)
- Moved [topic] to reference/[file].md
- Extracted [content] to scripts/[script].py

### Token Efficiency
**Per-request usage:**
- Before: Always [old KB] KB
- After: [base KB] KB + [on-demand KB] KB (average)
- Savings: [percentage]%

**Annual cost savings** (at 100 requests/day):
- Before: $[cost]/year
- After: $[new cost]/year
- Saved: $[savings]/year

## New File Structure
```
skill-name/
├── SKILL.md ([size] KB)
├── reference/
│   ├── api.md ([size] KB)
│   ├── examples.md ([size] KB)
│   └── troubleshooting.md ([size] KB)
└── scripts/
    ├── validate.py
    └── process.py
```

## Usage Examples
**Before optimization:**
```
> [request]
# Loads 50KB every time
```

**After optimization:**
```
> [request for X]
# Loads 3KB + 8KB (X reference) = 11KB

> [request for Y]
# Loads 3KB + 5KB (Y reference) = 8KB
```

## Next Steps
1. Test the optimized skill
2. Verify all links work
3. Monitor token usage
4. Adjust as needed
```

## Common Optimizations

### For API Documentation
**Extract to:** reference/api.md
**Include in SKILL.md:** "For API details, see reference/api.md"

### For Examples
**Extract to:** reference/examples.md
**Include in SKILL.md:** "For examples, see reference/examples.md"

### For Troubleshooting
**Extract to:** reference/troubleshooting.md
**Include in SKILL.md:** "For troubleshooting, see reference/troubleshooting.md"

### For Domain-Specific Content
**Extract to:** reference/[domain].md
**Include in SKILL.md:** Conditional loading based on request

### For Mechanical Operations
**Extract to:** scripts/[operation].py
**Include in SKILL.md:** "Run: python scripts/[operation].py"

## Quality Validation

After optimization, verify:

1. **Functionality Preserved**
   - All original capabilities maintained
   - No information lost
   - User experience improved

2. **Performance Improved**
   - Token usage reduced
   - Load time faster
   - Maintenance easier

3. **Usability Enhanced**
   - Easier to navigate
   - Clear organization
   - Intuitive structure

## Integration with Other Skills

- **skill-reviewer** - Review before optimizing
- **skill-generator** - If complete rewrite needed
- **skill-architect** - For complete workflow management

## See Also

- [SKILL_GENERATOR.md](.claude/skills/skill-generator/SKILL.md) - Create new skills
- [SKILL_REVIEWER.md](.claude/skills/skill-reviewer/SKILL.md) - Review skill quality
- [SKILL_ARCHITECT.md](.claude/skills/skill-architect/SKILL.md) - Complete workflow
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md) - PDA reference

## Sources

Based on:
- [CLAUDE_SKILLS_ARCHITECTURE.md](../../../docs/CLAUDE_SKILLS_ARCHITECTURE.md)
- Progressive Disclosure Architecture principles
