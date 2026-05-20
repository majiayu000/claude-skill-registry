---
name: prd
description: Create agent-friendly Linear tickets with PRDs, sub-issues, and clear success criteria. Use when planning features or breaking down work for agentic coding.
---

# PRD Skill - Create Agent-Friendly Tickets

You are an expert at breaking down features into well-structured, agent-friendly Linear tickets.

## When to Use

Use this skill when:
- Planning a new feature
- Breaking down a large task into sub-issues
- Creating tickets that AI agents will implement

## Process

1. **Understand the Request**
   - Ask clarifying questions if the scope is unclear
   - Identify the core problem being solved

2. **Create the Epic/Parent Issue**
   Use `linear issues create` with:
   - Clear, action-oriented title
   - Problem/Context section
   - Requirements (must-have vs nice-to-have)
   - Success criteria (testable, specific)

3. **Break Down into Sub-Issues**
   Each sub-issue should:
   - Be completable in one focused session (<150k tokens of context)
   - Have clear, verifiable success criteria
   - Include verification commands (tests to run)
   - Define boundaries (what's in/out of scope)

4. **Set Up Dependencies**
   Use `--depends-on` and `--blocked-by` to create proper dependency chains.

## Ticket Structure

```markdown
## Problem/Context
[1-2 sentences explaining why this work is needed]

## Requirements
### Must Have
- [ ] Requirement 1
- [ ] Requirement 2

### Nice to Have
- [ ] Optional feature

## Success Criteria
- [ ] Specific, testable criterion 1
- [ ] Specific, testable criterion 2

## Verification
```bash
# Commands to verify the work is complete
make test
npm run lint
```

## Boundaries
### In Scope
- What this ticket covers

### Out of Scope
- What should be separate tickets
```

## Example Commands

```bash
# Create parent issue
linear issues create "User Authentication System" \
  --team ENG \
  --description "$(cat prd.md)" \
  --priority 2

# Create sub-issue
linear issues create "Implement OAuth2 login flow" \
  --team ENG \
  --parent ENG-100 \
  --description "Implement OAuth2 with Google provider..."

# Set dependencies
linear issues update ENG-102 --blocked-by ENG-101
```

## Discovering Related Work

Before creating tickets, search for existing related work:

```bash
# Find existing work on this topic
linear search "authentication" --team ENG

# Check if dependencies already exist
linear search "OAuth" --has-dependencies --team ENG

# Look for potential blockers
linear search "user database" --team ENG
```

**Pro tip:** Use `/link-deps` skill after creating tickets to discover and establish dependencies.

## Best Practices

1. **Size tickets appropriately** - Each should be 1-4 hours of focused work
2. **Include test commands** - Always specify how to verify completion
3. **Be explicit about scope** - Prevent scope creep with clear boundaries
4. **Use Labels** - Add `agent-ready` label for tickets ready for AI implementation
5. **Establish dependencies** - Use `--blocked-by` and `--depends-on` to show work order
6. **Search first** - Check for existing related issues before creating duplicates
