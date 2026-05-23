---
name: createProjectSkills
description: Atlas skill for designing and creating Claude Skills for project-specific codebases. USE WHEN you need to capture repeatable workflows, complex multi-step processes, or domain-specific patterns that Claude should handle consistently.
context: fork
user-invocable: false
---

# Creating Claude Skills

This skill helps you design and create effective Claude Skills for the Kompass Rails application.

## Quick Reference

**Skill locations:**

- **Personal:** `~/.claude/skills/<skill-name>/SKILL.md` (private to you)
- **Project:** `.claude/skills/<skill-name>/SKILL.md` (shared with team)

**When to use each:**

- Use **Personal** for your own workflow, cross-project utilities
- Use **Project** for team-shared skills, project-specific patterns

**Frontmatter format:**

```yaml
---
name: skill-name-in-kebab-case
description: What it does and when to use it (max 1024 chars)
---
```

**Requirements:**

- Name: Gerund form (verb + -ing), lowercase, letters/numbers/hyphens only, max 64 chars
- Description: Third person, specific about WHAT and WHEN, no XML tags
- SKILL.md: Keep under 500 lines (use reference files for additional content)

## When to Create a Skill vs. Improving CLAUDE.md

**Create a skill when:**

- ✅ Pattern requires 3+ coordinated steps that must happen in specific order
- ✅ Complex workflow with multiple decision points
- ✅ Task has validation loops (do → check → fix → repeat)
- ✅ Domain-specific conventions that aren't obvious from code alone
- ✅ You find yourself repeatedly explaining the same multi-step process
- ✅ Risk of missing critical steps in a workflow

**Update CLAUDE.md when:**

- ❌ Simple convention or preference (Ruby keyword shorthand, bin/rails usage)
- ❌ General architectural knowledge (event sourcing overview)
- ❌ Single-step operation
- ❌ Claude already knows this (Rails conventions, Ruby syntax)
- ❌ No specific execution order required

**Rule of thumb:** If it's knowledge, put it in CLAUDE.md. If it's a workflow, make it a skill.

## Discovery Workflow

### 1. Identify Skill Candidates

Review recent work for patterns you explain repeatedly:

```bash
# Look for repeated patterns in conversation
cat TEMPLATES.md  # See common patterns worth capturing
```

**Strong candidates in this codebase:**

- Event-sourced feature generation (Command → Decider → Event → Reactor → ReadModel)
- Temporal query implementation (valid_at, created_at, as_of patterns)
- Read model reactor creation
- Multi-step forms with Turbo
- Background job workflows with Commands::Async

### 2. Validate the Need

Ask:

- Does this require multiple steps in specific order? (If no, probably not a skill)
- Would missing a step cause problems? (If no, probably not a skill)
- Does Claude get this wrong when you just explain it? (If no, probably not a skill)
- Is this specific to our domain/codebase? (If no, probably not a skill)

If you answered "yes" to most questions, proceed to create the skill.

## Writing Workflow

### Step 1: Create the Skill Structure

**Use the creation script with location flags:**

For personal skills:

```bash
~/.claude/skills/creating-claude-skills/scripts/create_skill.sh \
  skill-name \
  "Description with 'Use when' clause" \
  --personal
```

For project skills:

```bash
./.claude/skills/creating-claude-skills/scripts/create_skill.sh \
  skill-name \
  "Description with 'Use when' clause" \
  --project
```

**Auto-detection:** If you omit the flag, the script auto-detects:

- In git repository → creates project skill
- Outside git repository → creates personal skill

**Choose based on:**

- Use `--personal` for your own workflow, cross-project utilities
- Use `--project` for team-shared skills, project-specific patterns

**Plan freedom level:**

- **High freedom (text guidance):** Flexible tasks where approaches vary (designing features)
- **Medium freedom (pseudocode):** Preferred patterns but some flexibility (creating controllers)
- **Low freedom (scripts):** Fragile operations requiring consistency (database operations)

**Plan content distribution:**

- SKILL.md: Core workflow, essential examples (< 500 lines)
- Reference files: Deep dives, extensive examples, optional details
- Scripts: Deterministic operations, validation tools

### Step 2: Customize the Frontmatter

```yaml
---
name: action-oriented-gerund-name
description: Verb phrase stating what it does. Second sentence explaining when to use it.
---
```

**Good examples:**

- `generating-event-sourced-features: Create complete event-sourced features with Commands, Deciders, Events, Reactors, and ReadModels. Use when building new domain functionality.`
- `writing-focused-specs: Write behavior-focused RSpec tests that validate business logic without testing implementation details. Use when creating tests for Deciders, Reactors, or integration flows.`

**Bad examples:**

- `helper: Helps with things` (too vague)
- `eventing: For events` (not descriptive)
- `rails-patterns: Rails conventions` (too broad, belongs in CLAUDE.md)

### Step 3: Structure the Instructions

**Recommended structure:**

```markdown
# Skill Name

Brief overview (1-2 sentences).

## Core Workflow

1. **Step Name:** What to do
   - Sub-steps if needed
   - Key decision points

2. **Step Name:** Next action
   - Validation checks
   - Error handling

## Codebase-Specific Conventions

- Ruby keyword shorthand: `method(date:, people:)` not `method(date: date, people: people)`
- Commands: Always use `bin/rails` not `rails`
- [Any patterns specific to this skill's domain]

## Examples

[Concrete input/output examples from this codebase]

## Validation Checklist

- [ ] Item to check
- [ ] Another item
- [ ] Final verification

## References

For detailed information, see:

- `cat REFERENCE_FILE.md` - Description of what's in it
```

### Step 4: Add Examples from This Codebase

**Use real code patterns:**

```ruby
# Good example - shows actual conventions
class Events::Duty::Created < Events::Base
  attribute :duty_id, Types::String
  attribute :client_id, Types::String
  attribute :name, Types::String

  validates :duty_id, :client_id, :name, presence: true
end
```

**Show input/output pairs** to demonstrate expected detail level and style.

### Step 5: Implement Progressive Disclosure

Keep SKILL.md focused. Move to reference files:

**SKILL.md (< 500 lines):**

- Core workflow steps
- Essential examples
- Quick reference

**Reference files (load on demand):**

````markdown
For detailed architecture patterns:

```bash
cat ARCHITECTURE.md
```
````

For complete examples:

```bash
cat EXAMPLES.md
```

````

### Step 6: Create Utility Scripts

**validation scripts:**
```bash
#!/bin/bash
# scripts/validate_skill.sh
# Check SKILL.md format, length, frontmatter
````

**Helper scripts:**

```bash
#!/bin/bash
# scripts/create_structure.sh
# Generate boilerplate for new features
```

**Key principles:**

- Scripts solve problems, don't punt to Claude
- Document why constants have specific values
- Handle error conditions explicitly
- Use forward slashes for paths (cross-platform)

### Step 7: Validate

Run validation (path depends on where skill is located):

**For personal skills:**

```bash
~/.claude/skills/creating-claude-skills/scripts/validate_skill.sh <skill-dir>
```

**For project skills:**

```bash
./.claude/skills/creating-claude-skills/scripts/validate_skill.sh <skill-dir>
```

Check:

- [ ] Frontmatter valid (name, description present and correct format)
- [ ] SKILL.md under 500 lines
- [ ] Description explains WHAT and WHEN
- [ ] Examples use actual codebase conventions
- [ ] No deeply nested references (max 1 level)
- [ ] Consistent terminology throughout
- [ ] Validation steps for critical operations
- [ ] Scripts include error handling

## Codebase-Specific Considerations

### Event Sourcing Patterns

Skills dealing with event sourcing should reference the flow:

1. Command (user intention)
2. Decider (validation, event production)
3. Event (immutable fact)
4. Reactor (side effects)
5. ReadModel (query optimization)

### Ruby Conventions

Always demonstrate:

- Keyword shorthand: `create_event(duty_id:, name:)`
- `bin/rails` commands: `bin/rails generate migration`
- Dry-rb patterns: `Success(event)`, `Failure(errors)`

### Testing Philosophy

Skills about testing should emphasize:

- Test BEHAVIOR not IMPLEMENTATION
- Focus on events created and data correctness
- Test validation failures with proper errors
- Test noop scenarios
- Avoid testing that classes derive from bases or respond_to methods

### Technology Stack

Reference when relevant:

- Tailwind CSS for styling
- Stimulus for JavaScript interactivity
- Turbo for SPA-like navigation
- Pundit for authorization
- Sidekiq for background jobs

## Templates

See common skill templates:

```bash
cat TEMPLATES.md
```

## Examples

See working examples of skills for this codebase:

```bash
cat EXAMPLES.md
```

## Quality Checklist

Before finalizing any skill:

- [ ] Name uses gerund form (verb + -ing)
- [ ] Name is lowercase with hyphens only
- [ ] Description states WHAT and WHEN clearly
- [ ] SKILL.md is under 500 lines
- [ ] Examples use actual codebase patterns
- [ ] Ruby keyword shorthand in all examples
- [ ] Uses `bin/rails` not `rails`
- [ ] References are one level deep only
- [ ] Scripts include error handling
- [ ] No time-sensitive information
- [ ] Consistent terminology throughout
- [ ] Validation steps for critical operations
- [ ] Adds value beyond what's in CLAUDE.md
- [ ] Solves a real repeated problem

## Anti-Patterns

**Avoid:**

- ❌ Skills that just restate CLAUDE.md content
- ❌ Skills for single-step operations
- ❌ Vague or overly generic descriptions
- ❌ Assuming tools/gems are installed
- ❌ Deeply nested file references (> 1 level)
- ❌ Mixing terminology (pick one term and stick to it)
- ❌ Missing concrete examples
- ❌ Scripts that punt error handling to Claude
- ❌ Time-sensitive information (dates, versions)

## Iteration Process

1. **Build evaluation first:** Test Claude WITHOUT the skill to identify gaps
2. **Create minimal skill:** Address the specific gaps only
3. **Test with fresh context:** Use new Claude instance to test
4. **Observe navigation:** Notice how Claude uses your references
5. **Iterate based on behavior:** Refine based on actual performance gaps

Remember: **Conciseness is essential.** Every line competes for context window space. Challenge every explanation with "Does Claude really need this?" Default to assuming Claude is knowledgeable.
