---
name: estimate
description: "Estimates task effort by analyzing complexity, dependencies, historical velocity, and risk factors. Produces a structured estimate with confidence levels."
argument-hint: "[task-description]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

When this skill is invoked:

1. **Read the task description** from the argument. If the description is too
   vague to estimate meaningfully, ask for clarification before proceeding.

2. **Read CLAUDE.md** for project context: tech stack, coding standards,
   architectural patterns, and any estimation guidelines.

3. **Read relevant design documents** from `design/gdd/` if the task relates
   to a documented feature or system.

4. **Scan the codebase** to understand the systems affected by this task:
   - Identify files and modules that would need to change
   - Assess the complexity of those files (size, dependency count, cyclomatic
     complexity)
   - Identify integration points with other systems
   - Check for existing test coverage in the affected areas

5. **Read past sprint data** from `production/sprints/` if available:
   - Look for similar completed tasks and their actual effort
   - Calculate historical velocity (planned vs actual)
   - Identify any estimation bias patterns (consistently over or under)

6. **Analyze the following factors**:

   **Code Complexity**:
   - Lines of code in affected files
   - Number of dependencies and coupling level
   - Whether this touches core/engine code vs leaf/feature code
   - Whether existing patterns can be followed or new patterns are needed

   **Scope**:
   - Number of systems touched
   - New code vs modification of existing code
   - Amount of new test coverage required
   - Data migration or configuration changes needed

   **Risk**:
   - New technology or unfamiliar libraries
   - Unclear or ambiguous requirements
   - Dependencies on unfinished work
   - Cross-system integration complexity
   - Performance sensitivity

7. **Generate the estimate**:

```markdown
## Task Estimate: [Task Name]
Generated: [Date]

### Task Description
[Restate the task clearly in 1-2 sentences]

### Complexity Assessment

| Factor | Assessment | Notes |
|--------|-----------|-------|
| Systems affected | [List] | [Core, gameplay, UI, etc.] |
| Files likely modified | [Count] | [Key files listed below] |
| New code vs modification | [Ratio, e.g., 70% new / 30% modification] | |
| Integration points | [Count] | [Which systems interact] |
| Test coverage needed | [Low / Medium / High] | [Unit, integration, manual] |
| Existing patterns available | [Yes / Partial / No] | [Can follow existing code or new ground] |

**Key files likely affected:**
- `[path/to/file1]` -- [what changes here]
- `[path/to/file2]` -- [what changes here]
- `[path/to/file3]` -- [what changes here]

### Effort Estimate

| Scenario | Days | Assumption |
|----------|------|------------|
| Optimistic | [X] | Everything goes right, no surprises, requirements are clear |
| Expected | [Y] | Normal pace, minor issues, one round of review feedback |
| Pessimistic | [Z] | Significant unknowns surface, blocked for a day, requirements change |

**Recommended budget: [Y days]**

[If historical data is available: "Based on [N] similar tasks that averaged
[X] days actual vs [Y] days estimated, a [correction factor] adjustment has
been applied."]

### Confidence: [High / Medium / Low]

**High** -- Clear requirements, familiar systems, follows existing patterns,
similar tasks completed before.

**Medium** -- Some unknowns, touches moderately complex systems, partial
precedent from previous work.

**Low** -- Significant unknowns, new technology, unclear requirements, or
cross-cutting concerns across many systems.

[Explain which factors drive the confidence level for this specific task.]

### Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Specific risk] | [High/Med/Low] | [Days added if realized] | [How to reduce] |
| [Another risk] | [Likelihood] | [Impact] | [Mitigation] |

### Dependencies

| Dependency | Status | Impact if Delayed |
|-----------|--------|-------------------|
| [What must be done first] | [Done / In Progress / Not Started] | [How it affects this task] |

### Suggested Breakdown

| # | Sub-task | Estimate | Notes |
|---|----------|----------|-------|
| 1 | [Research / spike] | [X days] | [If unknowns need investigation first] |
| 2 | [Core implementation] | [X days] | [The main work] |
| 3 | [Integration with system X] | [X days] | [Connecting to existing code] |
| 4 | [Testing and validation] | [X days] | [Writing tests, manual verification] |
| 5 | [Code review and iteration] | [X days] | [Review feedback, fixes] |
| | **Total** | **[Y days]** | |

### Historical Comparison
[If similar tasks exist in sprint history:]

| Similar Task | Estimated | Actual | Relevant Difference |
|-------------|-----------|--------|-------------------|
| [Past task 1] | [X days] | [Y days] | [What makes it similar/different] |
| [Past task 2] | [X days] | [Y days] | [What makes it similar/different] |

### Notes and Assumptions
- [Key assumption that affects the estimate]
- [Another assumption]
- [Any caveats about scope boundaries -- what is included vs excluded]
- [Recommendations: e.g., "Consider a spike first if requirement X is unclear"]
```

8. **Output the estimate** to the user with a brief summary: recommended
   budget, confidence level, and the single biggest risk factor.

### Guidelines

- Always give a range (optimistic / expected / pessimistic), never a single
  number. Single-point estimates create false precision.
- The recommended budget should be the expected estimate, not the optimistic
  one. Padding is not dishonest -- it is realistic.
- If confidence is Low, recommend a time-boxed spike or prototype before
  committing to the full estimate.
- Be explicit about what is included and excluded. Scope ambiguity is the
  most common source of estimation error.
- Round to half-day increments. Estimating in hours implies false precision
  for tasks longer than a day.
- If the task is too large to estimate confidently (more than 10 days
  expected), recommend breaking it into smaller tasks and estimating those
  individually.
- Do not pad estimates silently. If risk exists, call it out explicitly in
  the risk factors section so the team can decide how to handle it.
