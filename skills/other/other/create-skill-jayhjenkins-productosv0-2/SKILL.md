---
name: create-skill
description: Use when creating new skills or improving existing ones - enforces test-driven skill development with RED-GREEN-REFACTOR methodology and Claude Search Optimization
---

# Create Skill

## The Core Principle

**Writing skills IS Test-Driven Development applied to process documentation.**

Skills follow the RED-GREEN-REFACTOR cycle:
1. **RED**: Create a failing test scenario (expected behavior that doesn't work yet)
2. **GREEN**: Write the skill that makes the test pass
3. **REFACTOR**: Optimize for clarity and token efficiency

## The Iron Law

**NO SKILL WITHOUT A FAILING TEST FIRST**

This applies to:
- New skills ✓
- Skill edits ✓
- "Simple additions" ✓
- Documentation updates ✓

No exceptions. No rationalizations. Test first, always.

## SKILL.md Format Requirements

### Required YAML Frontmatter

Every SKILL.md must begin with exactly two required fields:

```yaml
---
name: skill-name-with-hyphens
description: Use when [triggering conditions] - [what it does in third person]
---
```

**Name Requirements:**
- Lowercase alphanumeric + hyphens only
- No spaces, underscores, or special characters
- Max 64 characters
- Must match directory name exactly

**Description Requirements:**
- **Critical for discovery** - Claude uses this to auto-activate skills
- Start with "Use when..." to highlight triggers
- Include specific symptoms and situations
- Third-person perspective
- Max 200 characters (ideally under 500 for complex skills)
- Avoid technology-specific language unless skill requires it
- Front-load most distinctive triggering conditions

**Optional Field:**
```yaml
allowed-tools: Read, Write, Grep, Glob, Bash
```
Restricts which tools Claude can use during skill execution.

### Required Content Sections

#### 1. Purpose (Essential)
- What is this skill?
- Core principle in 1-2 sentences
- Establishes fundamental concept

#### 2. When to Use This Skill (Essential)
- Bullet list with symptoms and use cases
- Triggering conditions
- **When NOT to use** section (critical for preventing misapplication)
- Small inline flowchart if decision is non-obvious

#### 3. Workflow Steps / Implementation (Essential)
- Step-by-step procedure
- Specific file paths and operations
- Error handling guidance
- Inline code for simple patterns
- Links to supporting files for heavy reference material

#### 4. Quality Gates (If Applicable)
- Mandatory validation steps
- Related quality-gate skills to invoke
- Success criteria
- Iron laws (non-negotiable requirements)
- **Required**: Use the `documentation-sync` quality gate before considering skill complete

#### 5. Common Mistakes (Essential)
- What goes wrong
- How to fix it
- Red flags and warning signs
- Anti-rationalization blocks

#### 6. Success Criteria (Essential)
- How to verify successful execution
- Expected outputs and artifacts
- Validation checkpoints

#### 7. Related Skills (Optional)
- Dependencies (mark with asterisks: `**skill-name**`)
- Complementary skills
- Integration points

#### 8. Real-World Impact (Optional)
- Concrete results and metrics
- Before/after comparisons

## Token Efficiency Guidelines

**Length Targets:**
- Getting-started workflows: <150 words
- Frequently-loaded skills: <200 words
- Other skills: <500 words

**Optimization Techniques:**
- One excellent example beats many mediocre ones
- Choose most relevant programming language for examples
- Use tables for quick reference
- Inline code only; external files for heavy references

## Claude Search Optimization (CSO)

### Description Best Practices

**Good Description Pattern:**
```yaml
description: Use when [specific symptom/situation] - [enforces specific behavior/methodology] to [outcome]
```

**Examples:**

❌ **Bad**: "Helps with debugging"
✓ **Good**: "Use when tests fail or bugs reproduce inconsistently - enforces 4-phase root cause investigation before attempting fixes"

❌ **Bad**: "Content creation helper"
✓ **Good**: "Use when drafting marketing content requiring source integrity - enforces citation compliance with inline links and verbatim quotes"

❌ **Bad**: "Meeting processing tool"
✓ **Good**: "Use when extracting product signals from meeting transcripts - systematically identifies asks, problems, quotes across time windows"

### Triggering Conditions

Include concrete symptoms that Claude will recognize:
- "tests fail"
- "bugs reproduce inconsistently"
- "drafting content"
- "creating epics"
- "processing meeting transcripts"
- "verifying citations"

## Testing Framework

### Test-First Workflow

**1. Define Expected Behavior**
Create a scenario where you want the skill to activate and enforce specific behavior.

**2. Create Failing Test**
Document what currently happens (incorrect behavior).

**3. Write the Skill**
Implement the skill to make the test pass.

**4. Validate**
Run the scenario and verify the skill activates correctly.

**5. Pressure Test**
Add psychological pressure to ensure enforcement:
- Time constraints
- Sunk cost bias scenarios
- Authority framing
- Commitment mechanisms

### Skill Type-Specific Testing

**Discipline-Enforcing Skills** (e.g., citation-compliance, epic-validation):
- Test compliance under time pressure
- Use persuasion principles (urgency, authority, scarcity)
- Verify skill blocks rationalization attempts
- Confirm iron laws are enforced

**Technique Skills** (e.g., meeting-synthesis, source-normalization):
- Test application to new scenarios
- Verify correct procedure execution
- Check integration with other skills

**Workflow Skills** (e.g., content-pipeline, product-planning):
- Test end-to-end execution
- Verify checkpoints and quality gates
- Confirm state management and resumption

## Cross-Referencing Rules

**Use Skill Names Explicitly:**
✓ "Use the `citation-compliance` skill"
✓ "Invoke `meeting-synthesis` before proceeding"

**Mark Required Dependencies:**
✓ "**Required**: Use the `epic-validation` skill"

**Avoid @ Syntax:**
❌ "@citation-compliance" (force-loads file, pollutes context)

## Flowchart Guidelines

**Only include flowcharts for:**
- Non-obvious decisions
- Process loops
- "A vs B" choice points

**Never use flowcharts for:**
- Reference information
- Code examples
- Linear instruction sequences

## Quality Standards

### Validation Checklist

Before considering a skill complete:

- [ ] YAML frontmatter has exactly `name` and `description`
- [ ] Description optimized for CSO (starts with "Use when...")
- [ ] All required sections present
- [ ] Token count within guidelines for skill type
- [ ] Test scenario created and passed
- [ ] Pressure testing completed (for discipline skills)
- [ ] Cross-references use skill names (not @ syntax)
- [ ] Common mistakes section includes anti-rationalization blocks
- [ ] Iron laws clearly stated (if applicable)
- [ ] Success criteria are verifiable
- [ ] Documentation-sync quality gate passed (all 6 files updated)

## Skill Categories

Choose the appropriate category:

**Meta** (`.claude/skills/meta/`):
- System improvement
- Skill management
- Self-adaptation capabilities

**Quality Gates** (`.claude/skills/quality-gates/`):
- Validation and compliance checks
- Atomic, reusable verification
- Pass/fail criteria

**Context Assembly** (`.claude/skills/context-assembly/`):
- Reusable context gathering patterns
- Data synthesis and normalization
- Evidence collection

**Workflows** (`.claude/skills/workflows/`):
- Complete multi-stage processes
- Orchestrate multiple sub-skills
- State management and checkpoints

## Iron Laws for Skill Creation

1. **NO SKILL WITHOUT A FAILING TEST FIRST** - Universal, no exceptions
2. **DESCRIPTIONS MUST BE CSO-OPTIMIZED** - Auto-discovery depends on this
3. **TOKEN EFFICIENCY IS MANDATORY** - Respect length guidelines
4. **ONE EXCELLENT EXAMPLE > MANY MEDIOCRE** - Quality over quantity
5. **IRON LAWS MUST BE CLEARLY STATED** - No ambiguity in enforcement
6. **NO SKILL COMPLETE WITHOUT DOCUMENTATION SYNC** - All 6 files must be updated

## Success Criteria

You've created a skill correctly when:
- Test scenario was written first (RED phase)
- Skill makes the test pass (GREEN phase)
- Token count is optimized (REFACTOR phase)
- Description triggers automatic activation
- Common mistakes include anti-rationalization blocks
- Related skills are properly referenced
- Quality gates are enforced without compromise
- Documentation sync validated (all 6 files consistent)

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing skill before test | Delete skill, write test first |
| Generic description | Add specific symptoms and triggers |
| Too many examples | Keep one excellent example |
| Using @ syntax for cross-refs | Use skill names explicitly |
| Missing iron laws | Add non-negotiable requirements |
| Forgetting pressure testing | Add psychological pressure scenarios |
| Skipping documentation updates | Use documentation-sync quality gate (all 6 files) |

## Related Skills

- **using-skills**: Establishes mandatory skill usage protocol
- **skill-discovery**: Helps find existing skills before creating new ones
- **documentation-sync**: Required quality gate for maintaining documentation consistency
