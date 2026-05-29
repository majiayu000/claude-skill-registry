---
name: classify-lesson-types
description: Interview the user to classify each SLT by lesson type and build up lesson type heuristics.
license: MIT
metadata:
  author: Andamio
  version: 1.0.0
---

# Skill: Classify Lesson Types

## Description
Walks through each SLT in a set and interviews the user to determine the appropriate lesson type. Builds a classification document and refines heuristics about when each lesson type applies.

## Lesson Types

| # | Type | Inputs | Best For |
|---|------|--------|----------|
| 1 | **Product Demo** | SLT + screenshots | UI walkthroughs, platform features, "click here then here" sequences |
| 2 | **Developer Documentation** | SLT + code + docs link | API usage, library integration, code-heavy technical skills |
| 3 | **How To Guide** | SLT + optional materials | Step-by-step procedures, workflows, processes without heavy UI or code |
| 4 | **Organization Onboarding** | SLT + org context | Org-specific setup, policies, team conventions |
| 5 | **Exploration** | SLT + framing questions | Big ideas, thought leadership, worldview challenges, conceptual territory |

## Instructions

### Path Resolution

Resolve file paths based on your execution context:

- **Plugin context** (`${CLAUDE_PLUGIN_ROOT}` is set): Read knowledge from `${CLAUDE_PLUGIN_DATA}/knowledge/` (user data), falling back to `${CLAUDE_PLUGIN_ROOT}/knowledge/` (seed data). Read research from `${CLAUDE_PLUGIN_ROOT}/knowledge/research/`.
- **Clone/symlink context** (default): Read knowledge from `knowledge/` relative to the project root (research is at `knowledge/research/`).

### Pre-Execution Knowledge Check

Before classifying SLTs, read the knowledge base for heuristics that should improve your initial guesses. **If any knowledge file does not exist, skip it and proceed without prior heuristics — rely on the lesson type definitions below.**

1. **Read `knowledge/lesson-types/heuristics.yaml`**
   - Use verb_patterns to inform initial classification
   - Use subject_patterns to refine based on topic
   - Note confidence levels — high confidence patterns can be stated more firmly

2. **Read `knowledge/lesson-types/edge-cases.yaml`**
   - Check if this SLT matches a known ambiguous pattern
   - If so, skip to the discriminating_question that resolved it before

3. **Surface heuristics to user** (if relevant patterns exist):
   ```markdown
   ### Classification Insight

   Based on previous courses:
   - "explain" verbs → Exploration (87% of the time)
   - API/library subjects → Developer Documentation (92% of the time)
   - This SLT matches a known edge case — asking the same clarifying question that resolved it before.
   ```

---

The user will provide a markdown file containing SLTs. Read the file, then for each SLT:

### 1. Present the SLT and Your Initial Read

For each SLT, share:
- The SLT text
- Your initial guess at lesson type (with brief reasoning)
- One or two clarifying questions that would help confirm or revise

### 2. Interview with Discriminating Questions

Ask questions that help distinguish between candidate lesson types. Good discriminating questions:

**Product Demo vs. How To Guide:**
- "Does this SLT require showing the actual UI, or could it be taught with written steps alone?"
- "Is the learner clicking through an interface, or following a conceptual procedure?"

**Developer Documentation vs. How To Guide:**
- "Is code the primary artifact the learner produces, or is code incidental to a broader workflow?"
- "Would a code-free learner still benefit from this SLT?"

**Exploration vs. How To Guide:**
- "Is there a 'right answer' or correct procedure, or is this about developing perspective?"
- "Does this SLT ask the learner to adopt a stance or challenge assumptions?"

**Organization Onboarding vs. others:**
- "Does this SLT only make sense within a specific organization's context?"
- "Would a generic version of this SLT exist, or is it inherently org-specific?"

### 3. Capture the Decision and Reasoning

After the user responds, record:
- The chosen lesson type
- Key factors that determined the choice
- Any edge cases or "it could also be..." notes

### 4. Build Heuristics

As you work through the SLT set, notice patterns:
- Which SLT verbs tend toward which lesson types?
- What subject matter clusters with each type?
- Where do ambiguities arise, and how were they resolved?

## Output Format

After classifying all SLTs, produce a markdown document:

```markdown
# Lesson Type Classification: [Course Name]

## Summary

| Lesson Type | Count | SLTs |
|-------------|-------|------|
| Product Demo | [n] | 1.2, 2.1, ... |
| Developer Documentation | [n] | ... |
| How To Guide | [n] | ... |
| Organization Onboarding | [n] | ... |
| Exploration | [n] | ... |

## Classifications

### Module 1: [Module Name]

#### SLT 1.1: "[SLT text]"
- **Lesson Type**: [type]
- **Key Factors**: [why this type fits]
- **Edge Notes**: [any ambiguity or "could also be..." notes]
- **Inputs Needed**: [what context/assets this lesson will require]

[Repeat for each SLT]

---

[Repeat for each module]

## Heuristics Developed

Patterns observed during classification that can guide future SLT sets:

### Verb Patterns
- SLTs with "[verb]" tend toward [lesson type] because...

### Subject Matter Patterns
- [Topic area] SLTs tend toward [lesson type] because...

### Ambiguity Patterns
- When an SLT could be [type A] or [type B], we resolved by asking...

## Context Shopping List

Assets needed to build lessons, organized by type:

### Screenshots Needed (Product Demo)
- [ ] [description of screenshot for SLT X.Y]

### Code Examples Needed (Developer Documentation)
- [ ] [description of code for SLT X.Y]

### Framing Questions Needed (Exploration)
- [ ] [topic area for SLT X.Y]

### Org Context Needed (Organization Onboarding)
- [ ] [context needed for SLT X.Y]
```

## Guidelines

- **Interview, don't dictate.** Your initial guess is a starting point for conversation, not a verdict.
- **One SLT at a time.** Don't batch — the interview loses value if rushed.
- **Capture reasoning, not just labels.** The heuristics section is as valuable as the classifications.
- **Flag hybrid cases.** Some SLTs genuinely span types. Note these rather than forcing a single label.
- **Build the shopping list as you go.** Each classification implies inputs; capture them immediately.
- **Refine heuristics across sessions.** If this skill is run multiple times, the heuristics section should grow more precise.
