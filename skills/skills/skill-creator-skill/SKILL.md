---
name: skill-creator
description: Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.
---

# Skill Creator

## Purpose

A meta-skill that guides the creation of high-quality, effective skills. Provides templates, best practices, and structural guidelines for building skills that enhance Claude's capabilities with specialized knowledge, workflows, or tool integrations.

## When to Use

- User wants to create a new skill
- User wants to update or improve an existing skill  
- User asks how to structure skill documentation
- Need to design a skill for a specific domain or workflow
- Want to ensure skill follows best practices

## Core Skill Structure

### Required Components

Every skill must have these elements:

1. **Frontmatter**
   ```yaml
   ---
   name: skill-name
   description: One-line description when to use this skill
   ---
   ```

2. **Title & Purpose**
   ```markdown
   # Skill Name
   
   ## Purpose
   Clear, concise statement of what this skill does
   ```

3. **When to Use**
   ```markdown
   ## When to Use
   - Specific trigger 1
   - Specific trigger 2
   - Context where this helps
   ```

4. **Core Capabilities**
   ```markdown
   ## Core Capabilities
   
   ### Domain Expertise
   - Key knowledge area 1
   - Key knowledge area 2
   
   ### Tools & Methods
   - Specific techniques
   - Frameworks used
   ```

### Optional but Recommended Components

5. **Workflow**
   ```markdown
   ## Workflow
   
   1. Step 1: What to do first
   2. Step 2: Next action
   3. Step 3: Final deliverable
   ```

6. **Best Practices**
   ```markdown
   ## Best Practices
   
   - Do this
   - Avoid that
   - Remember this
   ```

7. **Examples**
   ```markdown
   ## Examples
   
   ### Example 1: Common Use Case
   **Input**: User request
   **Approach**: How to handle
   **Output**: Expected result
   ```

8. **Anti-Patterns**
   ```markdown
   ## Anti-Patterns
   
   ❌ **Don't**: Bad practice
   ✅ **Do**: Good alternative
   ```

## Skill Creation Workflow

### Step 1: Define Scope

Ask yourself:
- What problem does this skill solve?
- Who will use it?
- What triggers its use?
- What's the expected outcome?

### Step 2: Identify Core Knowledge

Document:
- Domain-specific terminology
- Key concepts and principles
- Common patterns in this domain
- Tools and technologies involved

### Step 3: Structure the Workflow

Map out:
- Entry conditions
- Step-by-step process
- Decision points
- Exit criteria and deliverables

### Step 4: Add Practical Elements

Include:
- Real-world examples
- Common pitfalls to avoid
- Best practices from the field
- Quality criteria

### Step 5: Write Clear Triggers

Make "When to Use" specific:
- ✅ "User needs SQL query optimization for PostgreSQL databases"
- ❌ "User needs database help"

- ✅ "Debugging production outages in distributed systems"
- ❌ "Fixing bugs"

## Skill Quality Criteria

### Clarity
- [ ] Name is self-explanatory
- [ ] Description clearly states when to use
- [ ] Purpose is stated in 1-2 sentences
- [ ] No jargon without explanation

### Completeness
- [ ] All required sections present
- [ ] Workflow is actionable
- [ ] Examples cover common cases
- [ ] Edge cases addressed

### Specificity
- [ ] Triggers are concrete
- [ ] Steps are detailed enough to follow
- [ ] Tools/methods are named explicitly
- [ ] Success criteria defined

### Usability
- [ ] Easy to scan and navigate
- [ ] Consistent formatting
- [ ] Logical section ordering
- [ ] Cross-references where helpful

## Skill Templates

### Technical Domain Skill Template

```markdown
---
name: domain-expert
description: Use when user needs [specific technical task] in [technology/domain]
---

# Domain Expert

## Purpose

Expert in [domain] specializing in [specific areas]. Helps with [key problems solved].

## When to Use

- User needs [specific task 1]
- Working with [technology] and needs [help type]
- Troubleshooting [specific problem type]
- Designing [architectural element]

## Core Capabilities

### [Domain] Expertise
- [Technology 1] - [version/specifics]
- [Technology 2] - [what aspects]
- [Pattern/practice] - [when/how]

### Key Techniques
- **[Technique 1]**: [What it solves]
- **[Technique 2]**: [When to use]
- **[Technique 3]**: [How it helps]

## Workflow

1. **Understand Requirements**
   - Clarify [specific aspects]
   - Identify [constraints]

2. **Apply [Domain] Patterns**
   - Use [pattern 1] for [scenario]
   - Consider [trade-off]

3. **Implement Solution**
   - Follow [best practice]
   - Ensure [quality criteria]

4. **Validate**
   - Test [aspects]
   - Verify [requirements met]

## Best Practices

- **[Practice 1]**: [Reasoning]
- **[Practice 2]**: [Benefit]
- **[Practice 3]**: [Why important]

## Common Patterns

### [Pattern 1]
**When**: [Scenario]
**How**: [Implementation approach]
**Why**: [Benefits]

### [Pattern 2]
**When**: [Scenario]
**How**: [Implementation approach]
**Why**: [Benefits]

## Anti-Patterns

❌ **Don't**: [Bad practice]
   - Why it fails: [Reason]
   - Better approach: [Alternative]

❌ **Avoid**: [Common mistake]
   - Problem: [What goes wrong]
   - Instead: [Correct way]

## Examples

### Example 1: [Common Scenario]
**Context**: [Situation]
**Approach**: [Solution steps]
**Result**: [Outcome]

## Tools & Technologies

- **[Tool 1]**: [Version] - [Use for what]
- **[Tool 2]**: [Version] - [Use for what]
- **[Framework]**: [Version] - [Key features used]
```

### Process/Workflow Skill Template

```markdown
---
name: process-specialist
description: Use when user needs [specific process/workflow] for [outcome]
---

# Process Specialist

## Purpose

Guides [specific process] to achieve [specific outcome]. Ensures [quality aspects] through [methodology].

## When to Use

- Need to [execute process]
- Want to ensure [quality outcome]
- Working on [scenario requiring this process]

## Core Process

### Phase 1: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]
3. [Action 3]: [Details]

**Outputs**: [What you have after this phase]

### Phase 2: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]

**Outputs**: [What you have after this phase]

### Phase 3: [Name]
**Goal**: [What to achieve]

Steps:
1. [Action 1]: [Details]
2. [Action 2]: [Details]

**Deliverable**: [Final output]

## Decision Points

### When to [Decision]
- If [condition], then [choice A]
- If [condition], then [choice B]

## Quality Gates

After each phase, verify:
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]

## Best Practices

- **[Practice]**: [Why it matters]
- **[Practice]**: [Impact on quality]

## Common Pitfalls

- **Pitfall**: [What people do wrong]
  - **Impact**: [What happens]
  - **Solution**: [How to avoid]
```

## Writing Tips

### Be Specific
❌ "Use when working with databases"
✅ "Use when optimizing SQL queries for PostgreSQL 14+ production databases"

### Be Actionable
❌ "Think about security"
✅ "Run OWASP ZAP scan and review all HIGH severity findings"

### Be Structured
Use consistent heading levels:
- `##` for major sections
- `###` for subsections
- `####` for detailed breakdowns

### Use Visual Indicators
- ✅ for good practices
- ❌ for anti-patterns
- 🔍 for investigation steps
- ⚠️ for warnings
- 💡 for tips

### Include Context
Don't just list what to do—explain why:
```markdown
## Instead of:
- Use connection pooling

## Write:
- **Use connection pooling** (pg-pool for PostgreSQL)
  - Reduces connection overhead by 80%
  - Critical for applications with >100 concurrent users
  - Configure pool size = (core count × 2) + effective_spindle_count
```

## Skill Maintenance

### When to Update
- New version of core technology released
- Better practices emerge in the field
- User feedback reveals gaps
- Related skills are created (cross-reference)

### Version Control
Consider adding to frontmatter:
```yaml
---
name: skill-name
description: One-line description
---
```

## Skill Integration

### Cross-References
Link to related skills:
```markdown
## Related Skills
- Use [[debugger-skill]] when issues arise
- Combine with [[performance-engineer-skill]] for optimization
- Precede with [[architect-reviewer-skill]] for design validation
```

### Skill Composition
Complex workflows can chain skills:
```markdown
## Workflow
1. Use [[requirement-analyst]] to gather needs
2. Apply this skill for implementation
3. Use [[code-reviewer]] for quality assurance
4. Use [[deployment-engineer]] to ship
```

## Examples

### Example 1: Creating a Python Pro Skill

**Context**: Need a skill for advanced Python development

**Process**:
1. Define scope: Python 3.11+ with focus on FastAPI and type safety
2. Identify triggers: "modern Python", "type hints", "FastAPI"
3. Structure core capabilities:
   - Python 3.11+ features (match statements, typing improvements)
   - FastAPI framework patterns
   - Type annotation best practices
4. Add workflow: Design API → Type models → Implement routes → Test
5. Include examples: FastAPI route with full type annotations

**Result**: A focused, actionable skill for modern Python development

### Example 2: Creating a Git Workflow Skill

**Context**: Need to codify team's git branching strategy

**Process**:
1. Define scope: Git workflow for feature development
2. Identify triggers: "create branch", "make PR", "git workflow"
3. Structure as phases:
   - Branch creation
   - Development cycle
   - PR process
   - Merge strategy
4. Add decision points: When to rebase vs merge
5. Include examples: Standard feature development flow

**Result**: Clear procedural guide for consistent git usage

## Validation Checklist

Before finalizing a skill, check:

### Structure
- [ ] Frontmatter complete (name, description)
- [ ] Title and purpose clear
- [ ] "When to Use" section has specific triggers
- [ ] Core capabilities well-defined

### Content
- [ ] Information is accurate and current
- [ ] Examples are realistic and helpful
- [ ] Best practices are justified
- [ ] Anti-patterns show alternatives

### Usability
- [ ] Can scan and find info quickly
- [ ] Sections flow logically
- [ ] Formatting is consistent
- [ ] Cross-references are correct

### Quality
- [ ] No spelling/grammar errors
- [ ] Technical terms defined
- [ ] Code examples (if any) are correct
- [ ] Meets all quality criteria above

## Meta: About This Skill

This skill itself demonstrates the principles it teaches:
- Clear frontmatter and structure
- Specific "When to Use" triggers
- Actionable workflows
- Concrete examples
- Quality criteria

When creating skills, use this as both a guide and a template.
