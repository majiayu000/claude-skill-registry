---
name: skill-creation
description: "Guide for creating standards-compliant skills with templates, references, and validation. All content must be in English. Trigger: When creating a new skill or documenting patterns."
skills:
  - reference-creation
  - critical-partner
  - process-documentation
  - skill-sync
  - english-writing
allowed-tools:
  - file-operations
  - read-file
  - write-file
---

# Skill Creation

## Overview

Create standards-compliant skills from simple single-file to complex multi-reference architectures. Covers directory setup, frontmatter requirements, content structure, inline examples, delegation patterns, and synchronization.

## Objective

Enable creation of skills at ANY complexity level (simple <15 patterns to complex 40+) that are discoverable, reusable, token-efficient, and follow project conventions. Each skill must have unique responsibility and delegate appropriately to conventions/a11y.

---

## When to Use

Use this skill when:

- Creating new skill from scratch
- Pattern is used repeatedly and AI needs guidance
- Project conventions differ from generic best practices
- Complex workflows need structured instructions
- Technology has multiple sub-topics requiring organization

Don't create when:

- Documentation already exists (create reference instead)
- Pattern is trivial or self-explanatory
- It's a one-off task

---

## English Writing

All generated code, documentation, comments, and prompt content must follow the [english-writing](../english-writing/SKILL.md) skill. Do not duplicate these rules here.

---

## 📚 Extended Mandatory Read Protocol

**This skill has a `references/` directory with detailed guides for skill creation.**

### Reading Rules

**MUST read [references/dependencies-matrix.md](references/dependencies-matrix.md)** when:

- Creating ANY new skill (required for all skill types)
- Determining skills field in frontmatter
- Validating existing skill dependencies
- Adding new skill categories

**CHECK [references/structure.md](references/structure.md)** when:

- Creating medium/complex skills (15+ patterns)
- Deciding if assets/ or references/ needed
- Organizing multiple examples or templates

**CHECK [references/frontmatter.md](references/frontmatter.md)** when:

- Validating frontmatter format
- Understanding required vs optional fields
- Troubleshooting schema validation errors

**CHECK [references/content-patterns.md](references/content-patterns.md)** when:

- Writing Critical Patterns section
- Creating inline examples
- Structuring Decision Trees

**CHECK [references/validation.md](references/validation.md)** when:

- Finalizing skill before sync
- Running compliance checks
- Debugging validation errors

---

## Quick Reference

| Complexity | Indicators                 | Structure                        | Read                                                                    |
| ---------- | -------------------------- | -------------------------------- | ----------------------------------------------------------------------- |
| Simple     | <15 patterns, single topic | SKILL.md only                    | This file + dependencies-matrix.md                                      |
| Medium     | 15-40 patterns, 2-3 topics | SKILL.md + assets/               | [structure.md](references/structure.md)                                 |
| Complex    | 40+ patterns, 4+ topics    | SKILL.md + assets/ + references/ | ✅ **MUST invoke** [reference-creation](../reference-creation/SKILL.md) |

**CRITICAL**: For complex skills (40+ patterns), **MUST invoke** [reference-creation](../reference-creation/SKILL.md) skill for creating references/ directory.

**ALL skills MUST read**: [dependencies-matrix.md](references/dependencies-matrix.md) to determine correct frontmatter dependencies.

---

## Critical Patterns

### ✅ REQUIRED [CRITICAL]: Use Template for Consistency

```bash
cp skills/skill-creation/assets/SKILL-TEMPLATE.md skills/{skill-name}/SKILL.md
# Fill placeholders: {skill-name}, {description}, {Trigger}, etc.
```

### ✅ REQUIRED [CRITICAL]: Include Trigger in Description

```yaml
# ✅ CORRECT
description: TypeScript strict patterns. Trigger: When implementing TypeScript in .ts/.tsx files.

# ❌ WRONG: Missing Trigger
description: TypeScript strict patterns.
```

**See** [frontmatter.md](references/frontmatter.md) for complete frontmatter guide.

### ✅ REQUIRED [CRITICAL]: Add Decision Tree

Every skill MUST include Decision Tree for AI guidance.

```markdown
## Decision Tree
```

Condition? → Action
Otherwise → Default

```

```

### ✅ REQUIRED [CRITICAL]: Include Inline Examples

Place focused example (<15 lines) immediately after each Critical Pattern.

````markdown
### ✅ REQUIRED: Hook Dependencies

Always include dependencies.

```typescript
useEffect(() => {
  fetchData(userId);
}, [userId]);
```
````

```

**See** [content-patterns.md](references/content-patterns.md) for writing patterns and examples.

### ✅ REQUIRED: Create References for Complex Skills

**When skill has 40+ patterns or 4+ natural sub-topics**, use `references/` directory.

```

skills/{skill-name}/
├── SKILL.md (300 lines max)
└── references/
├── {sub-topic-1}.md
├── {sub-topic-2}.md
└── {sub-topic-3}.md

````

**For complex skills (40+ patterns):** Invoke [reference-creation](../reference-creation/SKILL.md) skill.

### ✅ REQUIRED: Delegate to General Skills

```yaml
# ✅ CORRECT: Delegate to conventions
skills:
  - conventions
  - a11y

## Conventions
Refer to conventions for:
- Naming patterns

### Skill-Specific
- TypeScript strict mode required
````

```yaml
# ❌ WRONG: Duplicating conventions content
## Conventions
- Use camelCase for variables...
```

### ✅ REQUIRED: Token Efficiency

- Omit empty frontmatter arrays/objects
- Description under 150 characters
- Remove filler words ("comprehensive", "detailed")
- Every word adds unique value

**For skills with 40+ patterns: MUST read** [token-efficiency.md](references/token-efficiency.md) for compression strategies and organization techniques.

**For simpler skills: CHECK** [token-efficiency.md](references/token-efficiency.md) for optional optimization techniques.

### ✅ REQUIRED: Validate Structure

Before finalizing:

```bash
# Validate frontmatter
cat SKILL.md | yq eval '.frontmatter' -

# Validate against schema
yq eval-o=json SKILL.md | \
  yq eval-all '.' skills/skill-creation/assets/frontmatter-schema.json -
```

**See** [validation.md](references/validation.md) for complete checklist.

### ❌ NEVER: Duplicate Conventions

Don't rewrite rules that exist in conventions or a11y. Delegate first, then add skill-specific rules.

---

## Decision Tree

```
How many patterns?
  → <15 patterns? → Simple (SKILL.md only)
  → 15-40 patterns? → Medium (consider assets/ if templates needed)
  → 40+ patterns? → Complex (references/ required, MUST invoke reference-creation skill)

Has 2+ natural sub-topics? → Use references/ (even if <40 patterns)
SKILL.md will exceed 300 lines? → Use references/

Need templates/schemas? → Create assets/ directory
Need validation schema? → Add to assets/, reference in frontmatter

Determining skill dependencies (CRITICAL)?
  → MUST read references/dependencies-matrix.md first
  → Find category in matrix (Frontend/Backend/Testing/etc.)
  → Copy exact dependencies from category pattern
  → Update matrix with new skill example (Auto-Maintenance Protocol)

Generic rules? → Delegate to conventions
Accessibility rules? → Delegate to a11y
Generates user-facing content/UI? → Add humanizer to skills
Architecture patterns needed? → Delegate to architecture-patterns

After creation? → Run skill-sync or make sync to propagate
```

---

## Workflow

### Step 1: Determine Complexity

| Patterns | Sub-Topics | Structure                        | Reference                                                               |
| -------- | ---------- | -------------------------------- | ----------------------------------------------------------------------- |
| <15      | 1          | SKILL.md only                    | This file                                                               |
| 15-40    | 2-3        | SKILL.md + assets/               | [structure.md](references/structure.md)                                 |
| 40+      | 4+         | SKILL.md + assets/ + references/ | ✅ **MUST invoke** [reference-creation](../reference-creation/SKILL.md) |

### Step 2: Create Structure

```bash
# Simple
mkdir skills/{skill-name}
cp skills/skill-creation/assets/SKILL-TEMPLATE.md skills/{skill-name}/SKILL.md

# Medium
mkdir -p skills/{skill-name}/assets

# Complex (MUST read references-overview.md first)
mkdir -p skills/{skill-name}/{assets,references}
```

### Step 3: Fill Template

- Copy SKILL-TEMPLATE.md to new directory
- Replace all placeholders
- Add frontmatter (name, description with Trigger, skills, dependencies)
- Fill required sections (Overview, Objective, When to Use, Critical Patterns, Decision Tree, Conventions, Example, Edge Cases)

**See** [frontmatter.md](references/frontmatter.md) for frontmatter requirements.

### Step 4: Add Inline Examples

Place example (<15 lines) after each Critical Pattern.

**See** [content-patterns.md](references/content-patterns.md) for example patterns.

### Step 5: Add Decision Tree

Use condition→action format.

```
Condition? → Action
Otherwise → Default
```

### Step 6: Delegate to Conventions and Add Dependencies

Before adding rules, check if conventions/a11y/humanizer/architecture-patterns covers them. Delegate first.

- **General coding standards** → Delegate to [conventions](../conventions/SKILL.md)
- **Accessibility rules** → Delegate to [a11y](../a11y/SKILL.md)
- **Human-centric communication** → Delegate to [humanizer](../humanizer/SKILL.md)
- **Architecture patterns** (SOLID, Clean, DDD) → Delegate to [architecture-patterns](../architecture-patterns/SKILL.md)

**Add only skill-specific rules** that don't exist elsewhere.

#### **CRITICAL**: Determine Skill Dependencies

**MUST read [references/dependencies-matrix.md](references/dependencies-matrix.md)** to determine correct skills field for frontmatter.

The matrix provides exact dependencies by category:

- Frontend frameworks (React, Vue) → conventions, a11y, typescript, javascript, architecture-patterns, humanizer
- Backend frameworks (Express, Nest) → conventions, nodejs, typescript, architecture-patterns (NO humanizer)
- UI libraries (MUI, Chakra) → conventions, a11y, react, typescript, humanizer
- Testing tools (Jest, Playwright) → conventions, typescript, javascript (NO humanizer)
- Build tools (Vite, Webpack) → conventions only
- And 17 more categories with exact patterns

**After creating your skill**: Update dependencies-matrix.md with your new skill example (Auto-Maintenance Protocol in matrix).

### Step 7: Validate

- Use Compliance Checklist (below)
- Validate frontmatter against schema
- Check all sections present
- Verify token efficiency

**See** [validation.md](references/validation.md) for complete validation guide.

### Step 8: Sync

```bash
make sync
# or
npm run sync
```

---

## Conventions

Refer to [conventions](../conventions/SKILL.md) for:

- Naming patterns
- Code organization
- Documentation standards

Refer to [a11y](../a11y/SKILL.md) for:

- Semantic HTML
- ARIA attributes

Refer to [humanizer](../humanizer/SKILL.md) for:

- Human-centric communication
- Empathy in user-facing content
- Clear error messages and feedback

Refer to [architecture-patterns](../architecture-patterns/SKILL.md) for:

- SOLID principles (SRP, DIP, ISP, etc.)
- Clean/Hexagonal Architecture
- Domain-Driven Design patterns

**Don't duplicate** content from these skills. Delegate with clear references.

### Skill-Creation-Specific

- Use lowercase-with-hyphens for directory/file names
- Include Trigger clause in description
- Add Decision Tree to every skill
- Inline examples under 15 lines
- Complex skills (40+): Use references/
- SKILL.md max 300 lines (complex skills)
- Omit empty frontmatter arrays/objects

---

## Example

See [examples.md](references/examples.md) for complete examples:

- Simple skill (Prettier, <15 patterns)
- Medium skill (Formik, 15-40 patterns)
- Complex skill (React, 40+ patterns with references/)

---

## Edge Cases

### Migrating Existing Skill to Complex

If skill grows beyond 40 patterns:

1. Read [references-overview.md](references/references-overview.md)
2. Identify natural sub-topics
3. Create references/ directory
4. Follow [references-implementation.md](references/references-implementation.md)
5. Keep top 10-15 patterns in SKILL.md
6. Link to references throughout

### Version-Specific Patterns

For breaking changes across versions:

```
references/
├── current.md (v3)
├── legacy.md (v2)
└── migration.md
```

### Transversal Topics

Topics that apply across skill (like token-efficiency in skill-creation):

- Create separate reference file
- Link from multiple Critical Patterns
- Mark as "transversal" in overview

---

## Self-Check Protocol

Before creating skill, verify:

### Planning

- [ ] I identified skill complexity (simple/medium/complex)
- [ ] I read this SKILL.md completely
- [ ] If complex (40+ patterns), I will invoke [reference-creation](../reference-creation/SKILL.md) skill
- [ ] I understand references/ creation is delegated to reference-creation skill
- [ ] I checked if conventions/a11y already covers topic

### Structure

- [ ] I used SKILL-TEMPLATE.md as starting point
- [ ] Directory name is lowercase-with-hyphens
- [ ] Created assets/ if templates/schemas needed
- [ ] Created references/ if 40+ patterns or 4+ sub-topics

### Content

- [ ] Frontmatter includes required fields (name, description with Trigger)
- [ ] Empty frontmatter arrays/objects omitted
- [ ] **CRITICAL**: Used Skill Dependencies Matrix (Step 6) to determine skills field
- [ ] **Verified**: Skills field matches skill type (frontend/backend/testing/etc.)
- [ ] All sections present (Overview, Objective, When to Use, Critical Patterns, Decision Tree, Conventions, Example, Edge Cases)
- [ ] Each Critical Pattern has inline example (<15 lines)
- [ ] Decision Tree uses condition→action format
- [ ] Delegated to conventions/a11y/humanizer/architecture-patterns before adding rules
- [ ] **If user-facing UI/content**: Added humanizer to skills
- [ ] Token-efficient (no filler, every word adds value)

### Validation

- [ ] SKILL.md under 300 lines (complex skills)
- [ ] Frontmatter validates against schema
- [ ] All referenced skills exist
- [ ] Compliance Checklist completed (see below)

**Confidence Check:**

1. Can AI create skill in ANY topic using this guide?
2. Are conditions clear when to read each reference?
3. Is SKILL.md focused (top patterns only for complex)?

If NO to any: Re-read relevant sections.

---

## Compliance Checklist

Before finalizing:

### Structure

- [ ] Directory under `skills/` (lowercase, hyphens)
- [ ] SKILL.md created from template
- [ ] Complexity assessed (simple/medium/complex)
- [ ] assets/ if templates/schemas (optional)
- [ ] references/ if 40+ patterns or 4+ sub-topics (required for complex)

### Frontmatter

- [ ] Required: `name`, `description` (with Trigger clause)
- [ ] Optional fields add value (not obvious)
- [ ] Empty arrays/objects omitted
- [ ] Arrays use `- item` syntax (never `[]`)
- [ ] External libraries in `dependencies` with version ranges
- [ ] **CRITICAL**: Internal skills in `skills` field follow Dependencies Matrix (Step 6)
- [ ] **Verified**: Frontend skill has conventions, a11y, typescript, humanizer
- [ ] **Verified**: Backend skill has conventions, nodejs, typescript, architecture-patterns (NO humanizer)
- [ ] All referenced skills exist
- [ ] Validates against [frontmatter-schema.json](assets/frontmatter-schema.json)

### Content

- [ ] Overview (2-5 sentences)
- [ ] Objective (clear purpose)
- [ ] When to Use (with Don't use when)
- [ ] Critical Patterns (✅/❌ markers)
- [ ] Inline examples after EACH pattern (<15 lines)
- [ ] Decision Tree (condition→action format)
- [ ] Conventions (delegate to conventions/a11y/humanizer first)
- [ ] **User-facing UI/content**: humanizer delegation added
- [ ] Example (practical demonstration)
- [ ] Edge Cases (boundary conditions)
- [ ] Resources (if assets/ or references/ exist)

### Quality

- [ ] Delegates to conventions/a11y/humanizer/architecture-patterns (not duplicated)
- [ ] **User-facing UI/content skill**: Includes humanizer in skills field
- [ ] Token-efficient (no redundancy, filler removed)
- [ ] SKILL.md under 300 lines (complex skills)
- [ ] Complex skills: references/ properly structured
- [ ] Each reference links back to SKILL.md
- [ ] Cross-links between references

### Post-Creation

- [ ] Added to AGENTS.md Available Skills table
- [ ] Added to AGENTS.md Mandatory Skills table (if auto-invoke)
- [ ] Synced to model directories (make sync)
- [ ] Reviewed by critical-partner (recommended)

---

## Resources

### Templates

- [SKILL-TEMPLATE.md](assets/SKILL-TEMPLATE.md) - Main skill template
- [REFERENCE-TEMPLATE.md](assets/REFERENCE-TEMPLATE.md) - Reference file template (complex skills)
- [frontmatter-schema.json](assets/frontmatter-schema.json) - Validation schema

### Detailed Guides (Read When Needed)

| Reference                                             | When to Read              | Required?   |
| ----------------------------------------------------- | ------------------------- | ----------- |
| [frontmatter.md](references/frontmatter.md)           | Creating any skill        | Recommended |
| [structure.md](references/structure.md)               | Medium/complex skills     | Recommended |
| [content-patterns.md](references/content-patterns.md) | Writing patterns/examples | Recommended |
| [token-efficiency.md](references/token-efficiency.md) | Optimizing content        | Optional    |
| [examples.md](references/examples.md)                 | Learning from examples    | Optional    |
| [validation.md](references/validation.md)             | Pre-finalization checks   | Recommended |

**For complex skills (40+ patterns):** Invoke [reference-creation](../reference-creation/SKILL.md) skill instead of reading references above.

**Reading Protocol:**

- **Simple skills (<15 patterns)**: Read this SKILL.md only
- **Medium skills (15-40 patterns)**: Read SKILL.md + structure.md, frontmatter.md
- **Complex skills (40+ patterns)**: Read SKILL.md + **MUST read** references-overview.md + references-implementation.md

---

## References

- [conventions skill](../conventions/SKILL.md) - General coding conventions
- [a11y skill](../a11y/SKILL.md) - Universal accessibility standards
- [skill-sync](../skill-sync/SKILL.md) - Multi-model synchronization
- [Agent Skills Home](https://agentskills.io/home) - Official specification
- [SKILL.md Format](https://agents.md/) - Agents.md specification
