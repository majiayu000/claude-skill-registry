---
name: refine
version: 2.1.0
description: Transform ideas into Product Backlog Items using BA best practices, hypothesis validation, and domain research. Use when converting ideas to PBIs, validating problem hypotheses, adding acceptance criteria, or refining requirements. Triggers on "create pbi", "refine idea", "convert to pbi", "acceptance criteria", "make actionable", "validate hypothesis".
allowed-tools: Read, Write, Edit, Grep, Glob, TodoWrite, WebSearch, AskUserQuestion
infer: true
---

# Idea Refinement to PBI

Transform captured ideas into actionable Product Backlog Items using BA best practices, Hypothesis-Driven Development, and domain research.

## MUST READ References

**IMPORTANT: You MUST read these reference files for complete protocol. Do NOT skip.**

- **MUST READ** `.claude/skills/shared/team-frameworks.md` — RICE, MoSCoW, INVEST, SPIDR frameworks
- **MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` — BDD/Gherkin scenario templates
- **MUST READ** `.claude/skills/shared/module-detection-keywords.md` — module detection keywords

## When to Use

- Idea artifact ready for refinement
- Need to validate problem hypothesis before building
- Converting concept to implementable item
- Adding acceptance criteria to requirements

## Workflow

| Phase | Name                | Key Activity                 | Output                 |
| ----- | ------------------- | ---------------------------- | ---------------------- |
| 1     | Idea Intake         | Load artifact, detect module | Context loaded         |
| 2     | Domain Research     | WebSearch market/competitors | Research summary       |
| 3     | Problem Hypothesis  | Validate problem exists      | Confirmed hypothesis   |
| 4     | Elicitation         | Apply BABOK techniques       | Requirements extracted |
| 5     | Acceptance Criteria | Write BDD scenarios (min 3)  | GIVEN/WHEN/THEN        |
| 6     | Prioritization      | Apply RICE/MoSCoW            | Priority assigned      |
| 7     | Validation          | Interview user (MANDATORY)   | Assumptions confirmed  |
| 8     | PBI Generation      | Create artifact              | PBI file saved         |

---

## Phase 1: Idea Intake & Context Loading

1. Read idea artifact from path or find by ID in `team-artifacts/ideas/`
2. Extract: problem statement, value proposition, target users, scope
3. Check `module` field in frontmatter

**If module present:** Load domain context (see Business Feature Context Loading below)

**If module absent:** Run `Glob("docs/business-features/*/README.md")`, analyze keywords, prompt if ambiguous

**Skip:** Infrastructure ideas, cross-cutting concerns

### Business Feature Context Loading

#### Step 1: Detect Module

**From PBI/Idea frontmatter:**

1. Check `module` field
2. If missing, detect from keywords in `.claude/skills/shared/module-detection-keywords.md`

#### Step 2: Load Feature Context

```text
Glob("docs/business-features/{module}/detailed-features/*.md")
```

1. Read `docs/business-features/{module}/README.md` (overview + feature list, ~2K tokens)
2. Identify closest matching feature based on idea keywords
3. Read corresponding feature documentation:
   - Full feature doc: `docs/business-features/{module}/detailed-features/*.md` (3-5K tokens)
   - Or `.ai.md` companion: `docs/business-features/{module}/detailed-features/*.ai.md` (~1K tokens)
4. Extract context:
   - **Business Rules:** BR-{MOD}-XXX format
   - **Test Cases:** TC-{MOD}-XXX format with GIVEN/WHEN/THEN
   - **Evidence patterns:** file:line format
   - **Related entities and services**

#### Multi-Module Support

- If 2+ modules detected, load context for ALL detected modules
- Combine business rules and test case patterns from all modules
- May increase total token budget beyond single-module target

#### Token Budget

Target 8-12K tokens total for feature context:

- Module README: ~2K tokens
- Full feature doc sections: 3-5K per feature
- Multi-module: Load all detected modules (may increase total)

### Entity Domain Investigation

**Skip if:** No module detected (non-domain idea).

After loading feature context, investigate related entities in codebase.

#### Using .ai.md Files

1. Read `.ai.md` companion file for detected feature:

   ```text
   Glob("docs/business-features/{module}/detailed-features/*.ai.md")
   ```

2. Extract from `## Domain Model` section:
   - Entity names and base classes
   - Key properties and types
   - Navigation relationships
   - Computed properties

#### Codebase Correlation

1. Use `## File Locations` section paths to verify entities exist
2. Extract from `## Key Expressions` section:
   - Static expression methods for queries
   - Validation rules

#### Cross-Service Dependencies

Check `## Service Boundaries` section for:

- Events produced/consumed
- Related services affected

#### Discrepancy Handling

If `.ai.md` content differs from source code, flag for doc update but continue with documented info.

#### Entity Investigation Output

```markdown
## Entity Investigation Results

### Primary Entities
- `{EntityName}` - {Brief description} - [Source](path)

### Related Entities
- `{RelatedEntity}` - via {Relationship}

### Key Expressions
- `{ExpressionName}(params)` - {Purpose}

### Cross-Service Events
- Produces: `{EventName}`
- Consumes: `{EventName}` from {Service}

### Discrepancies (if any)
- {Note outdated docs for follow-up}
```

---

## Phase 2: Domain Research

### When to Trigger

- New market/domain unfamiliar to team
- Competitive landscape unclear
- Industry best practices needed
- User explicitly requests `--research`

### When to Skip

- Internal tooling with no market equivalent
- Well-understood domain
- Time-constrained refinement

### Research Process

1. Extract key domain terms from idea
2. Use WebSearch for context:

   | Query Type        | Template                                   |
   | ----------------- | ------------------------------------------ |
   | Market trends     | `"{domain} market trends 2026"`            |
   | Competitors       | `"{domain} software solutions comparison"` |
   | Best practices    | `"{feature-type} best practices UX"`       |
   | Similar solutions | `"how {competitor} handles {feature}"`     |

3. Summarize findings (max 3 bullets)

### Research Output

```markdown
## Domain Research Summary
- **Market context:** {1-sentence finding}
- **Competitor landscape:** {key players, gaps identified}
- **Best practices:** {relevant pattern to adopt}
- **Sources:** {links}
```

---

## Phase 3: Problem Hypothesis Validation

### Why This Matters

42% of startups fail due to no market need (CB Insights). Validate before building.

### Problem Hypothesis Template

```markdown
**We believe** [target users/persona]
**Experience** [specific problem]
**Because** [root cause]
**We'll know this is true when** [validation metric/evidence]
```

### Value Hypothesis Template

```markdown
**We believe** [feature/solution]
**Will deliver** [value/benefit]
**To** [target users]
**We'll know we're right when** [success metric]
```

### Validation Process

1. Draft hypothesis from idea content
2. Use AskUserQuestion to validate:
   - "Is this the core problem we're solving?"
   - "Who exactly experiences this? How often?"
   - "What evidence do we have this problem exists?"
3. If validated, proceed to Phase 4
4. If invalidated, return idea for clarification

### When to Skip Hypothesis

- `--skip-hypothesis` flag provided
- Idea already contains validated hypothesis
- Bug fix or technical debt (no new problem)

---

## Phase 4: Requirements Elicitation (BABOK Core 5)

Select technique based on context:

### 1. Interviews

**When:** Deep individual insights needed, stakeholder perspectives vary

**Process:**

1. Prepare open-ended questions (why, how, what-if)
2. Active listening - don't lead the witness
3. Follow-up on unexpected answers
4. Document verbatim quotes for evidence

**Output:** Stakeholder needs, pain points, constraints

### 2. Workshops

**When:** Group consensus needed, complex requirements, multiple stakeholders

**Process:**

1. Define clear agenda and timebox (90 min max)
2. Use facilitator (neutral party)
3. Capture all voices (round-robin, silent voting)
4. Document decisions and dissent

**Output:** Prioritized requirements, consensus decisions

### 3. Document Analysis

**When:** Existing systems/processes to understand, regulatory requirements

**Process:**

1. Gather artifacts: specs, manuals, reports, existing code
2. Extract implicit requirements
3. Note gaps and inconsistencies
4. Cross-reference with stakeholder input

**Output:** As-is state, compliance requirements, gaps

### 4. Observation (Job Shadowing)

**When:** Understand real workflow, users can't articulate needs

**Process:**

1. Shadow users in their environment
2. Note workarounds and pain points
3. Don't interrupt or suggest - just observe
4. Ask clarifying questions afterward

**Output:** Actual vs stated workflow, hidden requirements

### 5. Prototyping

**When:** Visual validation needed, UI/UX requirements unclear

**Process:**

1. Start low-fidelity (sketches, wireframes)
2. Iterate based on feedback
3. Increase fidelity as requirements stabilize
4. Document design decisions

**Output:** Validated UI requirements, interaction patterns

---

## Phase 5: Acceptance Criteria (BDD Format)

**MUST READ** `.claude/skills/shared/bdd-gherkin-templates.md` for templates.

| Practice                  | Description                       |
| ------------------------- | --------------------------------- |
| Single trigger            | "When" clause has ONE action      |
| 3 scenarios minimum       | Happy path, edge case, error case |
| No implementation details | Focus on behavior, not how        |
| Testable outcomes         | "Then" must be verifiable         |
| Stakeholder language      | No technical jargon               |

### Test Case Format (Domain Features)

For domain features, use:

- **Format:** `TC-{MOD}-{FEATURE}-XXX` (e.g., TC-GRO-GOAL-001)
- **Evidence:** `file:line` format
- See `business-analyst` skill for detailed patterns

---

## Phase 6: Prioritization & Estimation

Read `.claude/skills/shared/team-frameworks.md` for RICE, MoSCoW, and INVEST frameworks.

### Effort Estimation

| T-Shirt | Days  | When to Use                         |
| ------- | ----- | ----------------------------------- |
| XS      | 0.5-1 | Config change, simple fix           |
| S       | 1-2   | Single component, clear scope       |
| M       | 3-5   | Multiple components, some unknowns  |
| L       | 5-10  | Cross-cutting, integration needed   |
| XL      | 10+   | Epic - break down further           |

---

## Phase 7: Validation Interview (MANDATORY)

After drafting PBI, validate with user.

### Question Categories

| Category            | Example Question                                  |
| ------------------- | ------------------------------------------------- |
| **Assumptions**     | "We assume X is true. Correct?"                   |
| **Scope**           | "Should Y be included or explicitly excluded?"    |
| **Dependencies**    | "This requires Z. Is that available?"             |
| **Edge Cases**      | "What happens when data is empty/null?"           |
| **Business Impact** | "Will this affect existing reports/workflows?"    |
| **Entities**        | "Create new entity or extend existing X?"         |

### Interview Process

1. Generate 3-5 questions from assumptions, scope, dependencies
2. Use `AskUserQuestion` tool to interview
3. Document in PBI under `## Validation Summary`
4. Update PBI based on answers

### Validation Output Format

```markdown
## Validation Summary

**Validated:** {date}

### Confirmed Decisions
- {decision}: {user choice}

### Assumptions Confirmed
- {assumption}: Confirmed/Modified

### Open Items
- [ ] {follow-up items}
```

**This step is NOT optional - always validate before marking complete.**

---

## Phase 8: PBI Artifact Generation

### Save Location

`team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`

### Required Sections

1. Frontmatter (ID, source_idea, priority, effort, status, module)
2. Description
3. Business Value
4. Problem Hypothesis (from Phase 3)
5. Related Business Rules (if domain)
6. Acceptance Criteria (from Phase 5)
7. Out of Scope
8. Dependencies
9. Validation Summary (from Phase 7)

### PBI Business Feature Context Section

Include this section in the PBI output if domain-related:

```markdown
## Business Feature Context
**Module:** {module}
**Related Feature:** {feature_name}
**Existing Business Rules:** {BR_IDs} (see docs/business-features/{module}/...)
**Test Case Patterns:** {TC_format} with GIVEN/WHEN/THEN
**Evidence Format:** file:line (e.g., {example})
**Related Entities:** {entity_list}
```

### Update Source Idea

After PBI creation:

- Set source idea status to `approved`
- Add link to created PBI in idea file

### Template Reference

**MUST READ:** `team-artifacts/templates/pbi-template.md`

---

## Anti-Patterns to Avoid

| Anti-Pattern                   | Better Approach                      |
| ------------------------------ | ------------------------------------ |
| Refining vague ideas           | Return to `/idea` for clarification  |
| Skipping hypothesis validation | Always run Phase 3 for new features  |
| Solution-first thinking        | Start with problem, not solution     |
| Generic acceptance criteria    | Use GIVEN/WHEN/THEN with specifics   |
| Ignoring domain context        | Load business docs if applicable     |
| Too large PBI (XL+)            | Break into smaller items             |
| Missing "Out of Scope"         | Explicitly list exclusions           |
| Assuming instead of asking     | Run validation interview             |

---

## Definition of Ready Checklist

Before marking PBI as "Ready":

| Criterion               | Check                                    |
| ----------------------- | ---------------------------------------- |
| **I**ndependent         | No blocking dependencies on other PBIs   |
| **N**egotiable          | Details can still be refined with team   |
| **V**aluable            | Clear user/business value articulated    |
| **E**stimable           | Team can estimate effort (XS-XL)         |
| **S**mall               | Can complete in single sprint            |
| **T**estable            | Has 3+ GIVEN/WHEN/THEN scenarios         |
| **Problem Validated**   | Hypothesis confirmed in Phase 3          |
| **Domain Context**      | BR/entity context loaded (if applicable) |
| **Stakeholder Aligned** | Validation interview completed           |

---

## BR/TC Validation Checklist

For domain-related PBIs, include this checklist in the output:

```markdown
## BR/TC Validation Checklist

### Existing Business Rules Referenced
- [ ] BR-{MOD}-XXX: {Rule description} - Verified applicable
- [ ] BR-{MOD}-YYY: {Rule description} - Verified applicable

### New Business Rules Introduced
- [ ] BR-{MOD}-ZZZ: {New rule description} - Review needed

### Test Case Pattern Alignment
- [ ] TC format follows TC-{MOD}-{FEATURE}-XXX pattern
- [ ] All ACs use GIVEN/WHEN/THEN format
- [ ] Evidence format specified (file:line)

### Conflict Check
- [ ] No conflicts with existing BRs identified
- [ ] Clarifications documented if needed
```

---

## Example

```bash
/refine team-artifacts/ideas/260119-po-idea-goal-progress-notification.md
```

Creates with EasyPlatform context: `team-artifacts/pbis/260119-ba-pbi-goal-progress-notification.md`

- Includes BR-GRO-XXX references
- Uses TC-GRO-GOAL-XXX test case format
- Lists related entities (Goal, Employee, Notification)

---

## Output

- **Path:** `team-artifacts/pbis/{YYMMDD}-pbi-{slug}.md`
- **ID Pattern:** `PBI-{YYMMDD}-{NNN}`

## Related

| Type               | Reference                              |
| ------------------ | -------------------------------------- |
| **Role Skill**     | `business-analyst`                     |
| **Input**          | `/idea` output                         |
| **Next Step**      | `/story`, `/test-spec`, `/design-spec` |
| **Prioritization** | `/prioritize`                          |

## Triggers

Activates on: refine, refinement, pbi, backlog item, acceptance criteria, hypothesis, validate idea

## IMPORTANT Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
