---
name: architecture-fit-check
description: Framework for evaluating if change-set specs fit existing codebase architecture
---

# Architecture Fit Check

This skill provides the framework for evaluating whether proposed change-set specs (especially `kind: delta`) can be implemented within the existing codebase architecture.

## Primary Question

**Can an implementer translate these change-set specs into the repo's current architecture with routine changes + small refactors?**

The answer is not about whether change-set specs align with canonical capability specs — canonical specs describe *what* the system does, not *how* it's built. Evaluate fit against the actual codebase architecture.

## Process

### 1. Research the Repo Architecture

Use the `research` skill to understand the codebase:

- "What are the main architectural layers and module boundaries?"
- "Where are the entry points and how do they call into core logic?"
- "What patterns exist for dependency injection, interfaces, or adapters?"
- "Is there any existing eventing, pubsub, job queue, or workflow pattern?"
- "Find precedent implementations similar to these delta requirements."

Do not skip this step. You cannot evaluate fit without understanding how the repo is actually built.

### 2. Identify Constraints

Based on research, identify constraints that matter:

- **Structural**: Module boundaries, dependency directions, layering rules
- **Behavioral**: Error handling, state management, concurrency model
- **Interface**: API contracts, extension points, data formats
- **Operational**: Testing approach, build/CI, runtime model

### 3. Evaluate Each Delta Against Constraints

For each capability being added/modified:
- Can it be implemented using existing patterns?
- Does it require crossing boundaries in new ways?
- Does it introduce new primitives the repo doesn't have?

### 4. Check for Workaround Smell

Before finalizing, ask yourself:
- Am I proposing adjustments that are really just glue/hacks?
- Would these adjustments create inconsistent patterns?
- Is the "fit" path creating tech debt just to avoid a paradigm discussion?

If yes to any, the verdict should recommend paradigm work.

## Verdicts

### FITS
Choose when:
- All constraints satisfied
- Changes follow existing patterns
- Implementation stays inside 1-2 domains/modules
- No new "system primitive" required

### FITS_WITH_ADJUSTMENTS
Choose when:
- Minor constraint violations fixable with targeted work
- Adjustments are truly minimal and localized
- Examples: new module boundary, new interface + adapter, extract small utility

### NO_FIT
Choose when:
- Clean solution requires a new paradigm many modules must participate in
- Would require reorganizing layering/dependency direction repo-wide
- Changes runtime/operational assumptions

## Output Format

Document your findings:

```markdown
## Architecture Fit Evaluation

### Verdict: FITS | FITS_WITH_ADJUSTMENTS | NO_FIT

### Constraints Evaluated
- <List of architecture constraints checked>

### Satisfied
- <Constraints that pass>

### Violated
- <Constraints that fail, or "None">

### Minimal Adjustments (if FITS_WITH_ADJUSTMENTS)
- <Specific changes needed>

### Paradigm Work Needed (if NO_FIT)
- <What kind of new mechanism is required>
- Load the `paradigm-design` skill to explore options
```
