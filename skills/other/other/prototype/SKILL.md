---
name: prototype
description: "Rapid prototyping workflow. Skips normal standards to quickly validate a game concept or mechanic. Produces throwaway code and a structured prototype report."
argument-hint: "[concept-description]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write, Edit, Bash
---

When this skill is invoked:

1. **Read the concept description** from the argument. Identify the core
   question this prototype must answer. If the concept is vague, state the
   question explicitly before proceeding.

2. **Read CLAUDE.md** for project context and the current tech stack. Understand
   what engine, language, and frameworks are in use so the prototype is built
   with compatible tooling.

3. **Create a prototype plan**: Define in 3-5 bullet points what the minimum
   viable prototype looks like. What is the core question? What is the absolute
   minimum code needed to answer it? What can be skipped?

4. **Create the prototype directory**: `prototypes/[concept-name]/` where
   `[concept-name]` is a short, kebab-case identifier derived from the concept.

5. **Implement the prototype** in the isolated directory. Every file must begin
   with:
   ```
   // PROTOTYPE - NOT FOR PRODUCTION
   // Question: [Core question being tested]
   // Date: [Current date]
   ```
   Standards are intentionally relaxed:
   - Hardcode values freely
   - Use placeholder assets
   - Skip error handling
   - Use the simplest approach that works
   - Copy code rather than importing from production

6. **Test the concept**: Run the prototype. Observe behavior. Collect any
   measurable data (frame times, interaction counts, feel assessments).

7. **Generate the Prototype Report** and save it to
   `prototypes/[concept-name]/REPORT.md`:

```markdown
## Prototype Report: [Concept Name]

### Hypothesis
[What we expected to be true -- the question we set out to answer]

### Approach
[What we built, how long it took, what shortcuts we took]

### Result
[What actually happened -- specific observations, not opinions]

### Metrics
[Any measurable data collected during testing]
- Frame time: [if relevant]
- Feel assessment: [subjective but specific -- "response felt sluggish at
  200ms delay" not "felt bad"]
- Player action counts: [if relevant]
- Iteration count: [how many attempts to get it working]

### Recommendation: [PROCEED / PIVOT / KILL]

[One paragraph explaining the recommendation with evidence]

### If Proceeding
[What needs to change for a production-quality implementation]
- Architecture requirements
- Performance targets
- Scope adjustments from the original design
- Estimated production effort

### If Pivoting
[What alternative direction the results suggest]

### If Killing
[Why this concept does not work and what we should do instead]

### Lessons Learned
[Discoveries that affect other systems or future work]
```

8. **Output a summary** to the user with: the core question, the result, and
   the recommendation. Link to the full report at
   `prototypes/[concept-name]/REPORT.md`.

### Important Constraints

- Prototype code must NEVER import from production source files
- Production code must NEVER import from prototype directories
- If the recommendation is PROCEED, the production implementation must be
  written from scratch -- prototype code is not refactored into production
- Total prototype effort should be timeboxed to 1-3 days equivalent of work
- If the prototype scope starts growing, stop and reassess whether the
  question can be simplified
