---
name: draft-slts
description: Draft Student Learning Targets for a new course or module.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Draft Student Learning Targets

## Description

Generates well-formed Student Learning Targets (SLTs) for a course or module based on topic, audience, and learning goals. Follows education research best practices and Andamio protocol conventions.

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). Read research from `${CLAUDE_PLUGIN_ROOT}/knowledge/research/`.
- **Clone/symlink context** (default): Read knowledge from `knowledge/` relative to the project root (research is at `knowledge/research/`).

### Pre-Execution Knowledge Check

Before drafting SLTs, read the knowledge base for patterns that should influence your work. **If any knowledge file does not exist, skip it and proceed without prior patterns — note "No prior data available" in output.**

1. **Read `knowledge/slt-patterns/verb-bank.yaml`**
   - Note effective verbs by Bloom's level
   - Prefer verbs with high success_count

2. **Read `knowledge/slt-patterns/quality-issues.yaml`**
   - Note problematic patterns to avoid
   - Especially avoid patterns with high frequency

3. **Surface knowledge to user** (if relevant patterns exist):
   ```markdown
   ### Tips from Previous Courses

   **Effective verbs at this level:** compare, distinguish, implement (12 successes)
   **Patterns to avoid:** "understand X" (flagged 8 times), task-focused phrasing
   ```

---

The user will describe a course or module they want to create. Gather the following information (ask if not provided):

1. **Topic**: What is the course/module about?
2. **Audience**: Who are the learners? What's their background?
3. **Learning goals**: What should learners be able to do after completing this?
4. **Module count**: How many modules? (Default: 3-4)
5. **SLTs per module**: How many SLTs per module? (Default: 2-4)

Always read `knowledge/research/slt-research-report.md` for full research context before drafting.

### The SLT Formula

Every SLT must follow this structure:

**I can + [measurable verb] + [specific outcome] + [observable evidence/context]**

Examples:
- Weak: "I can understand blockchain" (unmeasurable, vague)
- Better: "I can explain what a blockchain is" (measurable, but no evidence)
- Strong: "I can compare a Portable Access Token to a traditional platform account by identifying at least two differences in ownership, portability, and revocability" (measurable verb, specific outcome, observable evidence)

### Verb Selection (Bloom's Taxonomy)

Use verbs that match the cognitive level appropriate for the content:

| Level | Verbs | When to Use |
|-------|-------|-------------|
| **Remember** | list, name, identify, recall | Foundational facts, terminology |
| **Understand** | explain, describe, summarize, compare | Conceptual understanding |
| **Apply** | use, demonstrate, implement, execute | Procedural skills |
| **Analyze** | distinguish, examine, compare, contrast | Breaking down complex topics |
| **Evaluate** | judge, justify, critique, assess | Making judgments |
| **Create** | design, construct, develop, produce | Building something new |

**Progression principle**: Early modules should include more Remember/Understand/Apply. Later modules can include Analyze/Evaluate/Create.

### Verbs to Avoid

Never use these unmeasurable verbs:
- understand, know, learn, appreciate, be aware of, become familiar with

These cannot be assessed. Replace with specific, observable actions.

### Output Format

Generate SLTs in this exact format:

```markdown
# SLTs: [Course Name]

## Module 1: [Module Title]

- 1.1: I can [verb] [specific outcome] [evidence/context].
- 1.2: I can [verb] [specific outcome] [evidence/context].
- 1.3: I can [verb] [specific outcome] [evidence/context].

## Module 2: [Module Title]

- 2.1: I can [verb] [specific outcome] [evidence/context].
- 2.2: I can [verb] [specific outcome] [evidence/context].

## Module 3: [Module Title]

- 3.1: I can [verb] [specific outcome] [evidence/context].
- 3.2: I can [verb] [specific outcome] [evidence/context].
- 3.3: I can [verb] [specific outcome] [evidence/context].
```

### Guidelines

1. **One capability per SLT.** If an SLT has "and" connecting two different skills, split it.

2. **Make it assessable.** Ask: "Could a teacher design an assignment to verify this?" If not, rewrite.

3. **Write for the learner.** SLTs should make learners curious, not anxious. Name tools and frameworks, but leave implementation details to the lessons.

4. **Build progression.** Module 1 SLTs should be achievable early. Later modules can build on earlier ones.

5. **2-4 SLTs per module is ideal.** More than 5 per module suggests the module should be split.

6. **Consider the assignment.** Each module needs one assignment that can assess all its SLTs. If the SLTs don't fit a coherent assignment, reorganize.

7. **Mark optional modules.** If a module is optional/advanced, note it in the title: "Module 4: [Title] (Optional)"

### Quality Checklist

Before outputting, verify each SLT:

- [ ] Starts with "I can"
- [ ] Uses a measurable verb (not understand/know/learn)
- [ ] Has a specific outcome (not vague)
- [ ] Includes observable evidence or context
- [ ] Can be assessed through an assignment
- [ ] Is appropriate for the stated audience
- [ ] Fits the cognitive progression (Bloom's levels build across modules)

### After Drafting

Suggest the user:
1. Review and refine the SLTs with their team
2. Run `/assess-slts` to get quality feedback
3. Create `00-course.md` with lesson types and assignments based on the finalized SLTs
