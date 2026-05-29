---
name: reference-creation
description: "Create and organize reference files for complex skills with 40+ patterns. Guides sub-topic identification, file structure, README creation, and cross-linking. All content must be in English. Trigger: When creating complex skill with 40+ patterns or 4+ natural sub-topics."
skills:
  - conventions
  - critical-partner
  - process-documentation
  - english-writing
allowed-tools:
  - file-operations
  - read-file
  - write-file
---

# Reference Creation Skill

## Overview

This skill guides the creation of reference files for complex skills (40+ patterns). Reference files organize content into focused sub-topic guides, improving navigability, token efficiency, and maintainability.

## Objective

Enable creation of well-structured `references/` directories with README navigation, proper file naming, cross-linking, and validation for complex skills.

## When to Use

Use this skill when:

- Skill has **40+ patterns** in Critical Patterns section
- Skill covers **4+ distinct sub-topics** (hooks, components, performance, server)
- SKILL.md would exceed **300 lines** with all patterns inline
- Skill has **natural sub-topics** that can be independently learned
- Skill covers **multiple contexts** (browser vs Node vs Edge)
- **Advanced techniques** would overwhelm beginners in main SKILL.md

## Critical Patterns

### ✅ REQUIRED: Assess Complexity First

Before creating references, verify skill meets threshold:

```
Complexity indicators:
- 40+ patterns? ✅
- 4+ sub-topics? ✅
- Natural groupings? ✅
- SKILL.md would exceed 300 lines? ✅

At least 2 indicators → Create references/
```

**Anti-pattern**: Creating references for simple skills (<15 patterns).

### ✅ REQUIRED: Identify Sub-Topics

Extract sub-topics from pattern clusters:

```
Process:
1. List ALL patterns in SKILL.md
2. Group by theme (what goes together?)
3. Identify clusters of 10-20 related patterns
4. Name clusters descriptively (not "advanced" or "misc")
5. Validate: Each cluster independently learnable?
```

**Example (React skill):**

```
70 patterns identified →
  - hooks.md (25 patterns: useState, useEffect, custom hooks)
  - components.md (18 patterns: composition, props, HOCs)
  - performance.md (15 patterns: memo, useMemo, code splitting)
  - server-features.md (12 patterns: SSR, RSC, data fetching)
```

### ✅ REQUIRED: Name Files Descriptively

Follow strict naming conventions:

```bash
# ✅ CORRECT
hooks.md
server-components.md
type-guards.md
async-patterns.md

# ❌ WRONG
advanced.md        # Too vague
misc.md            # Catch-all, no focus
part2.md           # Meaningless ordering
ReactAdvanced.md   # Wrong case
```

**Rule**: `{topic-description}.md` (lowercase, hyphens, descriptive)

### ✅ REQUIRED [CRITICAL]: Create README.md

Every `references/` directory MUST have README.md:

```markdown
# {Skill Name} References

> {One-line description}

## Quick Navigation

| Reference                    | Purpose   | Read When     |
| ---------------------------- | --------- | ------------- |
| [sub-topic.md](sub-topic.md) | {Purpose} | {When needed} |

## Reading Strategy

### For Simple Use Cases

- Read main SKILL.md only

### For Complex Use Cases

- MUST read: {reference1}, {reference2}
- CHECK: {reference3}
- Optional: {reference4}

## File Descriptions

### [sub-topic.md](sub-topic.md) (### lines)

{Detailed description}

**Read when**: {Specific trigger}
```

**Purpose**: Acts as GPS for 4-9 reference files.

### ✅ REQUIRED: Distribute Content

**SKILL.md should contain (300 lines max):**

- Top 10-15 CRITICAL patterns only
- Basic examples (<15 lines each)
- Decision Tree with references links
- Resources section listing ALL references

**Reference files should contain (200-600 lines each):**

- Deep dive into ONE sub-topic
- 10-20 patterns for that topic
- Real-world examples (complete code)
- Common pitfalls
- Advanced techniques
- Edge cases

```markdown
## SKILL.md Pattern Example

### ✅ REQUIRED [CRITICAL]: Custom Hooks

{Brief inline example}

**For advanced hook patterns, composition, custom hook guidelines:**
See [references/hooks.md](references/hooks.md).
```

### ✅ REQUIRED: Cross-Link Files

**Link from SKILL.md to references:**

```markdown
## Resources

### Detailed Guides

- [Hooks](references/hooks.md) - useState, useEffect, custom hooks
- [Components](references/components.md) - Composition, HOCs, render props
- [Performance](references/performance.md) - Memoization, code splitting

**See [references/README.md](references/README.md) for complete navigation.**
```

**Link between references:**

```markdown
## Related Topics

- See [components.md](components.md) for component composition patterns
- See [performance.md](performance.md) for optimization techniques
```

### ✅ REQUIRED: Reference File Structure

Each reference file MUST follow this structure:

```markdown
# {Sub-Topic Name}

> {One-line description}

## Overview

{2-3 sentences context}

---

## Core Patterns

### Pattern Name 1

{Explanation with inline example}

### Pattern Name 2

{Explanation with inline example}

{10-20 patterns...}

---

## Common Pitfalls

- **Pitfall 1**: {Description and solution}
- **Pitfall 2**: {Description and solution}

---

## Real-World Examples

### Example: {Use Case}

{Complete working code example}

---

## Advanced Techniques

{Optimization, edge cases}

---

## Related Topics

- See [other-reference.md](other-reference.md) for...
```

### ✅ REQUIRED: Validate Structure

Before finalizing:

```bash
# Check references/ has README
ls skills/{skill-name}/references/README.md

# Count reference files (4-9 is optimal)
ls skills/{skill-name}/references/*.md | wc -l

# Verify file sizes (200-600 lines ideal)
wc -l skills/{skill-name}/references/*.md

# Check cross-links work
grep -r "references/" skills/{skill-name}/SKILL.md
```

**Validation checklist**:

- [ ] README.md exists with Quick Navigation table
- [ ] 4-9 reference files (not too many, not too few)
- [ ] Each file 200-600 lines (split if over 800)
- [ ] Descriptive file names (no "advanced" or "misc")
- [ ] SKILL.md links to all references
- [ ] References cross-link to each other
- [ ] Resources section has "See README.md" link

### ✅ REQUIRED: Update Main SKILL.md

After creating references:

```markdown
## Resources

### Quick Reference

| Reference                               | Lines | Purpose   |
| --------------------------------------- | ----- | --------- |
| [sub-topic.md](references/sub-topic.md) | 400   | {Purpose} |

**See [references/README.md](references/README.md) for detailed navigation.**

### Related Skills

- [skill-creation](../skill-creation/SKILL.md) - Creating skills
- [conventions](../conventions/SKILL.md) - Coding standards
```

### ❌ NEVER: Create Catch-All References

Don't create vague references:

```bash
# ❌ WRONG
references/advanced.md    # What's "advanced"?
references/misc.md        # Catch-all, no focus
references/other.md       # Not descriptive
references/extras.md      # Vague
```

Instead, identify SPECIFIC sub-topics:

```bash
# ✅ CORRECT
references/optimization.md     # Specific: performance patterns
references/server-actions.md   # Specific: SSR feature
references/type-inference.md   # Specific: TS feature
```

### ❌ NEVER: Duplicate Content

References should EXPAND on SKILL.md, not repeat it:

**❌ Bad:**

- SKILL.md has useState example
- hooks.md has same useState example (duplication)

**✅ Good:**

- SKILL.md has basic useState example (5 lines)
- hooks.md has 5-7 useState patterns NOT in SKILL.md

### ❌ NEVER: Create Too Many Small Files

Avoid fragmentation:

**❌ Bad (10 files, 50 lines each):**

```
references/useState.md (50 lines)
references/useEffect.md (60 lines)
references/useContext.md (40 lines)
```

**✅ Good (1 file, 400 lines, organized):**

```
references/hooks.md (400 lines)
  - useState section
  - useEffect section
  - useContext section
```

**Guideline**: 4-9 references optimal. More = harder to discover.

## Decision Tree

```
Skill complexity: <40 patterns?
→ Yes: Use SKILL.md only (no references needed)
→ No: Continue assessment

Natural sub-topics exist (4+)?
→ No: Consider if patterns are truly related to same skill
→ Yes: Plan references/ directory

Each sub-topic has 10+ patterns?
→ No: Merge sub-topics or keep inline in SKILL.md
→ Yes: Create reference file for each sub-topic

References count: 4-9 files?
→ No: Consolidate (if >9) or add more sub-topics (if <4)
→ Yes: Create references/ with README.md

SKILL.md exceeds 300 lines after removing patterns?
→ Yes: Move more content to references
→ No: Good balance achieved

README.md created with navigation?
→ No: MUST create README.md (CRITICAL)
→ Yes: Validate cross-links and sync
```

## Conventions

Refer to [conventions](../conventions/SKILL.md) for:

- General file naming standards
- Directory organization patterns

Refer to [skill-creation](../skill-creation/SKILL.md) for:

- Main SKILL.md structure requirements
- Frontmatter and validation
- Token efficiency guidelines

### Reference-Specific Conventions

- **File length**: 200-600 lines ideal, max 800 before splitting
- **Sub-topic count**: 4-9 references optimal
- **README mandatory**: Every references/ MUST have README.md
- **Cross-linking**: Link from SKILL.md, between references, back to SKILL.md
- **Naming**: lowercase-with-hyphens.md, descriptive (no "advanced")

## Example: React Skill References

Complete reference structure for React skill (70 patterns):

```
skills/react/
├── SKILL.md (350 lines)
│   ├── Top 15 critical patterns
│   ├── Decision tree
│   └── Links to 4 references
└── references/
    ├── README.md (200 lines)
    ├── hooks.md (400 lines)
    │   ├── useState patterns (8)
    │   ├── useEffect patterns (7)
    │   ├── Custom hooks (6)
    │   └── Hook composition (4)
    ├── components.md (350 lines)
    │   ├── Functional components (6)
    │   ├── Props patterns (5)
    │   ├── Composition (4)
    │   └── HOCs vs hooks (3)
    ├── performance.md (300 lines)
    │   ├── React.memo (4)
    │   ├── useMemo/useCallback (5)
    │   ├── Code splitting (3)
    │   └── Profiling (3)
    └── server-features.md (250 lines)
        ├── Server Components (4)
        ├── Server Actions (3)
        ├── Streaming (3)
        └── Data fetching (2)
```

**SKILL.md excerpt:**

```markdown
### ✅ REQUIRED [CRITICAL]: Proper Hook Dependencies

{5-line example}

**For advanced patterns:** See [references/hooks.md](references/hooks.md).
```

**references/README.md excerpt:**

```markdown
## Quick Navigation

| Reference                      | Lines | Purpose                           |
| ------------------------------ | ----- | --------------------------------- |
| [hooks.md](hooks.md)           | 400   | useState, useEffect, custom hooks |
| [components.md](components.md) | 350   | Composition, HOCs, props          |

## Reading Strategy

### For Complex React Apps (40+ components)

- **MUST read**: hooks.md, components.md
- **CHECK**: performance.md
- **Optional**: server-features.md
```

## Edge Cases

- **Version-specific patterns**: Create separate files (`hooks-react-17.md`, `hooks-react-18.md`) or sections within file
- **Cross-cutting concerns**: Create dedicated reference (e.g., `token-efficiency.md` in skill-creation)
- **Migration from monolithic**: Use 8-step workflow, create references incrementally
- **Too few patterns per sub-topic**: Merge sub-topics or keep inline in SKILL.md
- **References exceeding 800 lines**: Split into sub-references (`hooks-state.md`, `hooks-effects.md`)

## 🔍 Self-Check Protocol (For AI Agents)

**Before completing references/ creation, verify you have:**

### 1. Context & Planning

- [ ] Confirmed skill has 40+ patterns or 4+ natural sub-topics
- [ ] Identified all sub-topics with 10-20 related patterns each
- [ ] Determined file count (4-9 files target)
- [ ] Verified no catch-all files needed (no "advanced", "misc")

### 2. Structure & Organization

- [ ] Created README.md with Quick Navigation table
- [ ] Named files descriptively (lowercase, hyphens)
- [ ] Each file 200-600 lines (max 800)
- [ ] SKILL.md retains top 15 critical patterns
- [ ] References expand (not duplicate) SKILL.md content

### 3. Cross-Linking & Navigation

- [ ] SKILL.md links to all references in Decision Tree
- [ ] SKILL.md has "See README.md" in Resources
- [ ] Each reference links back to SKILL.md
- [ ] Related references cross-link to each other
- [ ] Verified all links work (grep test)

### 4. Quality & Compliance

- [ ] No content duplication between files
- [ ] Consistent structure across all references
- [ ] Token-efficient (omit empty sections)
- [ ] Critical-partner review completed
- [ ] Synced with `make sync`

**Confidence check:**

1. Can I identify which reference file contains any specific pattern?
2. Is the README.md navigation clear and helpful?
3. Would splitting further improve clarity, or create fragmentation?

**If you answered NO to any:** Stop and refine the structure before proceeding.

**For complete validation:** See [Validation Checklist](#validation-checklist) below.

## Validation Checklist

Before finalizing references/:

- [ ] **Complexity justified**: 40+ patterns or 4+ natural sub-topics
- [ ] **Sub-topics identified**: Each has 10-20 related patterns
- [ ] **File naming**: Lowercase, hyphens, descriptive (no "advanced")
- [ ] **README.md created**: Quick Navigation + Reading Strategy + File Descriptions
- [ ] **Reference count**: 4-9 files (optimal range)
- [ ] **File sizes**: Each 200-600 lines (max 800)
- [ ] **Content distribution**: SKILL.md has top 15 critical patterns, references have deep-dives
- [ ] **Cross-linking**: SKILL.md → references, references → SKILL.md, references ↔ references
- [ ] **No duplication**: References expand, not repeat SKILL.md
- [ ] **No catch-alls**: No "advanced.md", "misc.md", "other.md"
- [ ] **Structure consistency**: All references follow template structure
- [ ] **Validation commands**: Run wc -l, grep for links, check README exists
- [ ] **Critical-partner review**: Run quality check
- [ ] **Sync**: Run `make sync` to propagate to model directories

## Resources

### Templates

- [REFERENCE-TEMPLATE.md](assets/REFERENCE-TEMPLATE.md) - Template for individual reference files

### Related Skills

- [skill-creation](../skill-creation/SKILL.md) - Main skill creation workflow (invokes this skill)
- [conventions](../conventions/SKILL.md) - General coding and organizational standards
- [critical-partner](../critical-partner/SKILL.md) - Quality validation
- [process-documentation](../process-documentation/SKILL.md) - Documenting changes and processes

### External References

- GitHub README conventions
- Documentation best practices
