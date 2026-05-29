---
name: investigation-workflow
version: 1.0.0
description: |
  6-phase investigation workflow for understanding existing systems. Auto-activates for research tasks.
  Optimized for exploration and understanding, not implementation. Includes parallel agent deployment
  for efficient deep dives and automatic knowledge capture to prevent repeat investigations.
auto_activates:
  - "investigate how"
  - "explain the architecture"
  - "understand the system"
  - "how does"
  - "why does"
  - "analyze"
  - "research"
  - "explore"
explicit_triggers:
  - /amplihack:investigation-workflow
  - /investigate
confirmation_required: true
skip_confirmation_if_explicit: true
token_budget: 4000
---

# Investigation Workflow Skill

## Purpose

This skill provides a systematic 6-phase workflow for investigating and understanding existing systems, codebases, and architectures. Unlike development workflows optimized for implementation, this workflow is optimized for exploration, understanding, and knowledge capture.

## When to Use This Skill

**Investigation Tasks** (use this workflow):

- "Investigate how the authentication system works"
- "Explain the neo4j memory integration"
- "Understand why CI is failing consistently"
- "Analyze the reflection system architecture"
- "Research what hooks are triggered during session start"

**Development Tasks** (use DEFAULT_WORKFLOW.md instead):

- "Implement OAuth support"
- "Build a new API endpoint"
- "Add feature X"
- "Fix bug Y"

## Core Philosophy

**Exploration First**: Define scope and strategy before diving into code
**Parallel Deep Dives**: Deploy multiple agents simultaneously for efficient information gathering
**Verification Required**: Test understanding through practical application
**Knowledge Capture**: Document findings to prevent repeat investigations

## The 6-Phase Investigation Workflow

### Phase 1: Scope Definition

**Purpose**: Define investigation boundaries and success criteria before any exploration.

**Tasks**:

- **FIRST**: Identify explicit user requirements - What specific questions must be answered?
- **Use** prompt-writer agent to clarify investigation scope
- **Use** ambiguity agent if questions are unclear
- Define what counts as "understanding achieved"
- List specific questions that must be answered
- Set boundaries: What's in scope vs. out of scope
- Estimate investigation depth needed (surface-level vs. deep dive)

**Success Criteria**:

- Clear list of questions to answer
- Defined scope boundaries
- Measurable success criteria (e.g., "can explain system flow", "can diagram architecture")

**Deliverables**:

- Investigation scope document with:
  - Core questions to answer
  - Success criteria
  - Scope boundaries (what's included/excluded)
  - Estimated depth and timeline

### Phase 2: Exploration Strategy

**Purpose**: Plan which agents to deploy and what to investigate, preventing inefficient random exploration.

**Tasks**:

- **Use** architect agent to design exploration strategy
- **Use** patterns agent to check for similar past investigations
- Identify key areas to explore (code paths, configurations, documentation)
- Select specialized agents for parallel deployment in Phase 3
- Create investigation roadmap with priorities
- Identify potential dead ends to avoid
- Plan verification approach (how to test understanding)

**Agent Selection Guidelines**:

- **For code understanding**: analyzer, patterns agents
- **For system architecture**: architect, api-designer agents
- **For performance issues**: optimizer, analyzer agents
- **For security concerns**: security, patterns agents
- **For integration flows**: integration, database agents

**Success Criteria**:

- Clear exploration roadmap
- List of agents to deploy in Phase 3
- Prioritized investigation areas

**Deliverables**:

- Exploration strategy document with:
  - Investigation roadmap
  - Agent deployment plan for Phase 3
  - Priority order for exploration
  - Expected outputs from each exploration

### Phase 3: Parallel Deep Dives

**Purpose**: Deploy multiple exploration agents simultaneously to gather information efficiently.

**CRITICAL**: This phase uses PARALLEL EXECUTION by default.

**Tasks**:

- **Deploy selected agents in PARALLEL** based on Phase 2 strategy
- **Common parallel patterns**:
  - `[analyzer(module1), analyzer(module2), analyzer(module3)]` - Multiple code areas
  - `[analyzer, patterns, security]` - Multiple perspectives on same area
  - `[architect, database, integration]` - System architecture exploration
- Each agent explores their assigned area independently
- Collect findings from all parallel explorations
- Identify connections and dependencies between findings
- Note any unexpected discoveries or anomalies

**Parallel Agent Examples**:

```
Investigation: "How does the reflection system work?"
→ [analyzer(.claude/tools/amplihack/hooks/), patterns(reflection), integration(logging)]

Investigation: "Why is CI failing?"
→ [analyzer(ci-config), patterns(ci-failures), integration(github-actions)]

Investigation: "Understand authentication flow"
→ [analyzer(auth-module), security(auth), patterns(auth), integration(external-auth)]
```

**Success Criteria**:

- All planned agents deployed and completed
- Findings from each exploration collected
- Connections between findings identified

**Deliverables**:

- Findings report with:
  - Summary from each parallel exploration
  - Code paths and flow diagrams
  - Architectural insights
  - Unexpected discoveries
  - Open questions for verification

### Phase 4: Verification & Testing

**Purpose**: Test and validate understanding through practical application.

**Tasks**:

- Create hypotheses based on Phase 3 findings
- **Design practical tests** to verify understanding:
  - Trace specific code paths manually
  - Examine logs and outputs
  - Test edge cases and assumptions
  - Verify configuration effects
- Run verification tests
- **Document what was tested and results**
- Identify gaps in understanding
- Refine hypotheses based on test results
- Repeat verification for any unclear areas

**Verification Examples**:

```
Understanding: "Authentication uses JWT tokens"
Verification: Trace actual token creation and validation in code

Understanding: "CI fails because of dependency conflict"
Verification: Check CI logs, reproduce locally, verify fix works

Understanding: "Reflection analyzes all user messages"
Verification: Examine reflection logs, trace message processing
```

**Success Criteria**:

- All hypotheses tested
- Understanding verified through practical tests
- Gaps in understanding identified and filled

**Deliverables**:

- Verification report with:
  - Tests performed
  - Results and observations
  - Confirmed understanding
  - Remaining gaps or uncertainties

### Phase 5: Synthesis

**Purpose**: Compile findings into coherent explanation that answers original questions.

**Tasks**:

- **Use** reviewer agent to check completeness of findings
- **Use** patterns agent to identify reusable patterns discovered
- Synthesize findings from Phases 3-4 into coherent explanation
- Create visual artifacts (diagrams, flow charts) if helpful
- Answer each question from Phase 1 scope definition
- Identify what worked well vs. what was unexpected
- Note any assumptions or uncertainties remaining
- Prepare clear explanation suitable for user

**Synthesis Outputs**:

1. **Executive Summary**: 2-3 sentence answer to main question
2. **Detailed Explanation**: Complete explanation with supporting evidence
3. **Visual Aids**: Diagrams showing system flow, architecture, etc.
4. **Key Insights**: Non-obvious discoveries or patterns
5. **Remaining Unknowns**: What's still unclear or uncertain

**Success Criteria**:

- All Phase 1 questions answered
- Explanation is clear and complete
- Findings supported by evidence from verification
- Visual aids clarify complex areas

**Deliverables**:

- Investigation report with all 5 synthesis outputs
- Ready for knowledge capture in Phase 6

### Phase 6: Knowledge Capture

**Purpose**: Create durable documentation so this investigation never needs to be repeated.

**Tasks**:

- **Update .claude/context/DISCOVERIES.md** with key insights
- **Update .claude/context/PATTERNS.md** if reusable patterns found
- Create or update relevant documentation files
- Add inline code comments for critical understanding
- **Optional**: Create GitHub issue for follow-up improvements
- **Optional**: Update architecture diagrams if needed
- Ensure future investigators can find this knowledge easily

**Documentation Guidelines**:

```markdown
## Discovery: [Brief Title]

**Context**: What was investigated and why
**Key Findings**:

- Main insight 1
- Main insight 2
  - **Supporting Evidence**: Links to code, logs, or verification tests
  - **Implications**: How this affects the project
  - **Related Patterns**: Links to similar patterns in PATTERNS.md
```

**Success Criteria**:

- DISCOVERIES.md updated with investigation results
- Relevant documentation files updated
- Knowledge is discoverable by future investigators
- No information loss

**Deliverables**:

- Updated DISCOVERIES.md
- Updated PATTERNS.md (if applicable)
- Updated project documentation
- Optional: GitHub issues for improvements
- Investigation session log in `.claude/runtime/logs/`

## Transitioning to Development Workflow

**After investigation completes**, if the task requires implementation (not just understanding), transition to **DEFAULT_WORKFLOW.md**:

1. **Resume at Step 4** (Research and Design) with the knowledge gained from investigation
2. **Or resume at Step 5** (Implement the Solution) if the investigation already provided clear design guidance
3. **Use investigation findings** from DISCOVERIES.md and session logs to inform design decisions

**Example Hybrid Workflow**:

```
User: "/ultrathink investigate how authentication works, then add OAuth support"

Phase 1: Investigation
→ Run INVESTIGATION_WORKFLOW.md (6 phases)
→ Complete understanding of existing auth system
→ Document findings in DISCOVERIES.md

Phase 2: Development
→ Transition to DEFAULT_WORKFLOW.md
→ Resume at Step 4 (Research and Design)
→ Use investigation insights to design OAuth integration
→ Continue through Step 15 (implementation → testing → PR)
```

**When to Transition**:

- Investigation reveals implementation is needed
- User explicitly requested both investigation + development
- Follow-up work identified during knowledge capture

## Efficiency Targets

**Target Efficiency**: This workflow targets a 30-40% reduction in message count compared to ad-hoc investigation.

| Ad-Hoc Approach         | Investigation Workflow    |
| ----------------------- | ------------------------- |
| 70-90 messages          | 40-60 messages            |
| Frequent backtracking   | Planned exploration       |
| Redundant investigation | Parallel deep dives       |
| Unclear scope           | Explicit scope definition |
| Lost knowledge          | Documented insights       |

**Efficiency Gains Come From**:

1. **Scope Definition** prevents scope creep and wandering
2. **Exploration Strategy** prevents random unproductive exploration
3. **Parallel Deep Dives** maximize information gathering speed
4. **Verification Phase** catches misunderstandings early
5. **Synthesis** ensures all questions answered
6. **Knowledge Capture** prevents repeat investigations

## Comparison to DEFAULT_WORKFLOW.md

### Similarities (Structural Consistency)

Both workflows share core principles:

- Explicit phases with clear deliverables
- Agent-driven execution at each phase
- Quality gates preventing premature progression
- Knowledge capture and documentation
- TodoWrite tracking for progress management

### Differences (Investigation vs. Development)

| Aspect             | Investigation Workflow     | DEFAULT_WORKFLOW.md      |
| ------------------ | -------------------------- | ------------------------ |
| **Goal**           | Understanding              | Implementation           |
| **Phases**         | 6 phases                   | Multi-step workflow      |
| **Execution**      | Exploration-first          | Implementation-first     |
| **Parallel Focus** | Phase 3 (Deep Dives)       | Various steps            |
| **Testing**        | Understanding verification | Code validation          |
| **Deliverable**    | Documentation              | Working code             |
| **Git Usage**      | Optional                   | Required (branches, PRs) |

### Phase Mapping (For User Familiarity)

| Investigation Phase           | DEFAULT_WORKFLOW Equivalent        | Purpose                              |
| ----------------------------- | ---------------------------------- | ------------------------------------ |
| Phase 1: Scope Definition     | Step 1: Requirements Clarification | Define what success looks like       |
| Phase 2: Exploration Strategy | Step 4: Research and Design        | Plan the approach                    |
| Phase 3: Parallel Deep Dives  | Step 5: Implementation             | Execute the plan (explore vs. build) |
| Phase 4: Verification         | Steps 7-8: Testing                 | Validate results                     |
| Phase 5: Synthesis            | Step 11: Review                    | Ensure quality and completeness      |
| Phase 6: Knowledge Capture    | Step 15: Cleanup                   | Make results durable                 |

## Integration with UltraThink

**UltraThink Workflow Detection**: When `/ultrathink` is invoked, it automatically detects investigation tasks using keywords and suggests this workflow.

**Automatic Workflow Suggestion**:

```
User: "/ultrathink investigate how authentication works"

UltraThink: Detected investigation task. Using INVESTIGATION_WORKFLOW.md
→ Reading workflow from .claude/workflow/INVESTIGATION_WORKFLOW.md
→ Following 6-phase investigation workflow
→ Starting Phase 1: Scope Definition
```

## Customization

To customize this workflow:

1. Edit `.claude/workflow/INVESTIGATION_WORKFLOW.md` to modify, add, or remove phases
2. Adjust agent deployment strategies for your needs
3. Add project-specific investigation patterns
4. Update efficiency targets based on your metrics

Changes take effect immediately for future investigations.

## Success Metrics

Track these metrics to validate workflow effectiveness:

- **Message Count**: Target 30-40% reduction vs. ad-hoc (to be validated)
- **Investigation Time**: Track time to completion
- **Knowledge Reuse**: How often DISCOVERIES.md prevents repeat work
- **Completeness**: Percentage of investigations with full documentation
- **User Satisfaction**: Clear understanding achieved

## Key Principles

- **Scope first, explore second** - Define boundaries before diving in
- **Parallel exploration is key** - Deploy multiple agents simultaneously in Phase 3
- **Verify understanding** - Test your hypotheses in Phase 4
- **Capture knowledge** - Always update DISCOVERIES.md in Phase 6
- **This workflow optimizes for understanding, not implementation**

When in doubt about investigation vs. development:

- **Investigation**: "I need to understand X"
- **Development**: "I need to build/fix/implement X"

## Related Resources

- **Source Workflow**: `.claude/workflow/INVESTIGATION_WORKFLOW.md` (complete 436-line specification)
- **Knowledge Extraction**: Use knowledge-extractor skill after investigations to capture learnings
- **Agent Catalog**: `.claude/agents/CATALOG.md` for all available agents
- **Pattern Library**: `.claude/context/PATTERNS.md` for reusable investigation patterns
