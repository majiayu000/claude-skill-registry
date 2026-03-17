---
name: self-improvement
description: |
  Capture user feedback and corrections to enhance repository documentation and skills.
  Transforms conversational feedback into persistent knowledge by updating the appropriate
  CLAUDE.md files, skills, or other documentation.

  Use when: (1) User provides a correction or clarification, (2) User says "remember this",
  (3) User provides feedback about how something should work, (4) After completing work where
  new patterns or knowledge were discovered, (5) User explicitly asks to update documentation.

  Triggers: "remember this", "update the skill", "add this to documentation", "you should know",
  "in the future", "always do", "never do", "that's wrong", "actually it should be",
  "/self-improvement", "capture this", "document this pattern", "add to CLAUDE.md"
user-invocable: false
---

# Self-Improvement Skill

Capture feedback and corrections to continuously enhance repository knowledge.

## Philosophy

This skill implements the "Continuous Improvement" principle: knowledge gained during work should be captured immediately, not lost. When users provide feedback, corrections, or new patterns emerge, this skill determines where that knowledge belongs and updates the appropriate documentation.

**Key principle**: Documentation updates should go hand-in-hand with the work that revealed them. Don't create separate PRs for documentation - include them in the current branch.

## Quick Start

```
Feedback Types:
- Correction      → Fix incorrect information in source
- Clarification   → Add missing context to existing docs
- New Pattern     → Add to appropriate CLAUDE.md or skill
- Anti-Pattern    → Add to root CLAUDE.md anti-patterns
- Workflow        → Update or create skill
- Preference      → Add to appropriate CLAUDE.md
```

## Execution Flow

### Phase 1: Feedback Classification

Analyze the user's feedback to determine its type:

| Feedback Signal | Classification | Typical Target |
|-----------------|----------------|----------------|
| "That's wrong" / "Actually..." | Correction | Source of incorrect info |
| "You should also know..." | Clarification | Related existing section |
| "When doing X, always Y" | New Pattern | Module CLAUDE.md or skill |
| "Never do X" / "Don't X" | Anti-Pattern | Root CLAUDE.md |
| "The workflow should be..." | Workflow | Skill (new or existing) |
| "I prefer..." / "Always use..." | Preference | Appropriate CLAUDE.md |

### Phase 2: Target Location Discovery

Use this decision tree to find where the knowledge belongs:

```
Is this correcting existing documentation?
├─ YES → Find and update the source of the incorrect information
│        Search: CLAUDE.md files, skills, referenced docs
└─ NO → Continue

Is this about enterprise principles or universal processes?
├─ YES → Root CLAUDE.md
│        Sections: Core Principles, Anti-Patterns, Universal Standards
└─ NO → Continue

Is this specific to a subsystem?
├─ Infrastructure (terragrunt, modules, stacks) → infrastructure/CLAUDE.md
├─ Kubernetes Platform (helm, flux, resourcesets) → kubernetes/platform/CLAUDE.md
├─ Kubernetes Clusters (bootstrap, per-cluster) → kubernetes/clusters/CLAUDE.md
├─ Task Runner (taskfiles, commands) → .taskfiles/CLAUDE.md
└─ NO → Continue

Is this a procedural workflow with 5+ steps?
├─ YES → Skill (create new or update existing)
│        Check: Does a related skill already exist?
└─ NO → Continue

Is this a quick reference or simple pattern?
├─ YES → Add to appropriate module CLAUDE.md
└─ NO → Ask user for guidance
```

### Phase 3: User Confirmation

**ALWAYS use AskUserQuestion before making updates.**

Present the proposed update:
1. Show the classified feedback type
2. Show the proposed target location
3. Show a preview of the proposed change
4. Offer alternatives if uncertain

Example confirmation flow:
```
I've identified this as a "New Pattern" that should be added to
infrastructure/CLAUDE.md in the "Testing Patterns" section.

Proposed addition:
───────────────────────────────────────────────────
When writing module tests, always include a negative test case
that verifies the module fails gracefully with invalid inputs.
───────────────────────────────────────────────────

Options:
1. Add to infrastructure/CLAUDE.md (Recommended)
2. Add to a different location
3. Create as a new skill
4. Skip - don't document this
```

### Phase 4: Apply Update

After user confirmation:

1. **For CLAUDE.md updates:**
   - Read the target file
   - Find the appropriate section
   - Add the new content with proper formatting
   - Maintain existing style and structure

2. **For skill updates:**
   - Read the existing skill SKILL.md
   - Identify the relevant section
   - Add or modify content
   - Update references if needed

3. **For new skills:**
   - Use the skill-creator guidance
   - Create SKILL.md with proper frontmatter
   - Register in settings if needed

4. **For corrections:**
   - Find all occurrences of the incorrect information
   - Update each occurrence
   - Verify no broken references result

## Integration with PR Workflow

**Documentation updates are part of the current work, not separate.**

When working on a branch:
- Include documentation updates in the same commits
- Group related code and doc changes together
- Don't create separate "update docs" commits unless substantial

When completing work:
- Review what was learned during implementation
- Proactively suggest documentation updates for new patterns
- Capture user feedback immediately, in the same PR

## Content Formatting Guidelines

### For CLAUDE.md additions

Match the existing style:
- Use tables for structured comparisons
- Use bullet points for lists
- Use code blocks for examples
- Keep entries concise - this is reference material
- Use Mermaid diagrams for flows, architectures, and decision trees — never create new ASCII art diagrams
- See root CLAUDE.md "Diagram Standards" section for Mermaid type selection and formatting rules

### For skill additions

Follow skill patterns:
- Procedural, step-by-step guidance
- Include error handling
- Add examples with context
- Reference supporting docs

### For anti-pattern additions

Format consistently with existing anti-patterns:
```markdown
## Anti-Pattern Category

- **NEVER** do X because Y
- **NEVER** do Z without explicit human approval
```

## Examples

### Example 1: User Correction

**User**: "Actually, you should use `task tg:plan-dev` not `task tg:plan dev`"

**Classification**: Correction
**Target**: Search for incorrect command usage
**Action**: Find and fix all occurrences of the incorrect command format

### Example 2: New Pattern

**User**: "When adding a new Helm release, always check kubesearch first for examples"

**Classification**: New Pattern
**Target**: kubernetes/platform/CLAUDE.md or flux-gitops skill
**Action**: Add to the appropriate location after confirmation

### Example 3: Preference

**User**: "I prefer smaller, focused commits over large combined ones"

**Classification**: Preference
**Target**: Root CLAUDE.md, Universal Standards section
**Action**: Add or update commit guidelines

### Example 4: Anti-Pattern Discovery

**User**: "Never use `kubectl apply` directly, always go through GitOps"

**Classification**: Anti-Pattern
**Target**: Root CLAUDE.md, Anti-Patterns section
**Action**: Add to Kubernetes Safety anti-patterns

## Proactive Self-Improvement

This skill should also be invoked proactively when:

1. **After completing implementation work**: Review what was learned and suggest documentation updates

2. **When patterns repeat**: If explaining the same concept twice, suggest capturing it

3. **When user corrects an approach**: Immediately offer to document the correction

4. **When discovering undocumented behavior**: Offer to add it to relevant docs

## Error Handling

If uncertain about placement:
- Always ask the user via AskUserQuestion
- Provide multiple options with explanations
- Default to asking rather than guessing wrong

If the target file doesn't exist:
- For CLAUDE.md: Check if it should be created (new module?)
- For skills: Offer to create a new skill
- For other docs: Ask user for guidance

If the update would be substantial:
- Preview the full change before applying
- Consider if it should be a separate skill instead
- Break large updates into logical chunks
