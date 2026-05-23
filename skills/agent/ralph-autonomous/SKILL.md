---
name: ralph-autonomous
description: Use this skill when Ralph is working autonomously through Brain Dump backlogs. Covers ticket selection, implementation patterns, and autonomous workflow management.
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: autonomous
---

# Ralph Autonomous Workflow

This skill guides Ralph when working autonomously through Brain Dump backlogs without direct user supervision.

## Autonomous Mode Principles

### Core Philosophy

- **No User Input Required**: Ralph makes decisions independently
- **Context-Driven**: Uses PRD and progress files for guidance
- **Incremental Progress**: One ticket per session, verify completion
- **Self-Documenting**: Logs all decisions and progress via MCP

### Decision Framework

Ralph evaluates tickets based on:

1. **Priority** (high > medium > low)
2. **Dependencies** (foundational work first)
3. **Complexity** (quick wins vs major features)
4. **Current Context** (progress from previous sessions)

## Standard Operating Procedure

### Session Start

```bash
# 1. Load current context
read('plans/prd.json')           # Get incomplete tickets
read('plans/progress.txt')         # Previous session context

# 2. Analyze ticket landscape
list_tickets()                     # Current state overview
find_project_by_path()            # Verify project context
```

### Ticket Selection Algorithm

```typescript
// Pseudo-code for Ralph's selection logic
function selectTicket(tickets: Ticket[]): Ticket {
  // Filter: only incomplete tickets
  const incomplete = tickets.filter((t) => !t.passes);

  // Sort by priority, then dependencies
  const sorted = incomplete.sort((a, b) => {
    if (a.priority !== b.priority) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return dependencyCount(a) - dependencyCount(b);
  });

  // Choose optimal ticket
  return sorted[0]; // Highest priority, least blocked
}
```

### Work Execution Pattern

```bash
# 1. Initialize ticket work
workflow "start-work"(selectedTicketId)

# 2. Implementation phase
# - Read existing code patterns
# - Follow project conventions
# - Write minimal, focused changes

# 3. Verification
pnpm test                         # Must pass
pnpm type-check                   # Must pass
pnpm lint                        # Should pass

# 4. Complete ticket
workflow "complete-work"(ticketId, summary)
```

## Intelligent Decision Making

### When Stuck on Implementation

```bash
# Log the issue
comment "add"(ticketId,
  "Blocked: [specific issue]. Will continue with next ticket.",
  "ralph",
  "blocker")

# Move on (don't waste time)
return next_best_ticket()
```

### Handling Dependencies

If selected ticket has unmet dependencies:

1. **Check if dependency ticket exists**

   ```bash
   dependency_tickets = tickets.filter(t =>
     selectedTicket.dependencies.includes(t.id)
   )
   ```

2. **If dependency exists** → Work on dependency first
3. **If dependency missing** → Create dependency ticket

### Scope Creep Prevention

```bash
# Before starting implementation
verify_ticket_scope(ticket) {
  estimated_time = estimate_complexity(ticket)
  if (estimated_time > 4_hours) {
    # Break into smaller tickets
    split_ticket(ticket)
    return smallest_piece()
  }
}
```

## Code Implementation Patterns

### Read Before Writing

```bash
# Always understand existing patterns
find_similar_implementations(ticket.description)
read_existing_components(ticket.related_area)
```

### Minimal Changes

- Only implement what's in acceptance criteria
- No "gold plating" or extra features
- Follow existing conventions exactly

### Testing Requirements

```typescript
// Every ticket must pass these checks
interface TicketCompletion {
  tests_pass: boolean; // pnpm test succeeds
  types_check: boolean; // pnpm type-check succeeds
  acceptance_met: boolean; // All AC items verified
  no_regressions: boolean; // No existing functionality broken
}
```

## Progress Tracking

### Session Logging

Ralph automatically logs:

```bash
# Start of session
comment "add"("session-start",
  `Ralph session started. Available tickets: ${count}`,
  "ralph",
  "session")

# Ticket decisions
comment "add"(ticketId,
  `Selected ticket: ${ticket.title}. Reason: ${reason}`,
  "ralph",
  "decision")

# Implementation progress
comment "add"(ticketId,
  `Completed: ${component}. Next: ${next_step}`,
  "ralph",
  "progress")

# Blockers and issues
comment "add"(ticketId,
  `Issue: ${problem}. Solution: ${approach}`,
  "ralph",
  "issue-resolution")
```

### Progress Updates in File

```bash
# plans/progress.txt - persistent context
echo "$(date): Ralph completed ticket ${ticketId}" >> plans/progress.txt
echo "Next session context: ${next_priorities}" >> plans/progress.txt
```

## Quality Assurance

### Pre-Completion Checklist

Before calling `workflow "complete-work"()`:

```typescript
const completion_checklist = {
  code_quality: verify_style_conventions(),
  error_handling: verify_error_boundaries(),
  performance: no_performance_regressions(),
  documentation: updated_docs_if_needed(),
  testing: all_tests_passing(),
  acceptance: all_criteria_met(),
};

if (!completion_checklist.all_true()) {
  fix_remaining_issues();
}
```

### Self-Correction

If Ralph makes mistakes:

1. **Detect** through testing or review
2. **Log** the issue transparently
3. **Correct** immediately
4. **Document** lessons learned

## Emergency Procedures

### MCP Server Down

```bash
# Fallback to manual workflow
if (!mcp_tools_available()) {
  git checkout -b "feature/ralph-manual"
  # Work without ticket tracking
  # Update PRD manually when done
}
```

### Database Issues

```bash
# Work offline if needed
if (!database_accessible()) {
  create_local_branch()
  implement_changes()
  # Sync tickets when database recovers
}
```

## Optimization Patterns

### Learning from History

Ralph improves over time by analyzing:

- Previous implementation choices
- Common blockers and patterns
- Estimation accuracy
- Code quality feedback

### Batch Operations

When multiple similar tickets exist:

```typescript
// Batch similar work for efficiency
similar_tickets = find_similar_tickets(current);
if (similar_tickets.length > 1) {
  implement_common_base();
  complete_individual_variants();
}
```

## Communication Style

### Autonomous Updates

Ralph provides updates without being asked:

- Every 30 minutes during long tasks
- When major decisions are made
- When blockers are encountered
- Before moving to next ticket

### Transparency

All decision-making is documented:

```bash
comment "add"(ticketId,
  `Decision: Chose approach X over Y because:
  1. Performance: 50% faster
  2. Maintainability: Less code
  3. Compatibility: Works with existing system`,
  "ralph",
  "decision")
```

## Session Completion

### Final Status Report

When all tickets are complete:

```bash
echo "PRD_COMPLETE"  # Signal completion

# Generate summary
comment "add"("project-complete",
  `All ${total_tickets} tickets completed.
  Total time: ${elapsed_time}.
  Key achievements: ${highlights}`,
  "ralph",
  "summary")
```

### Handoff Preparation

```bash
# Prepare for next session
update_progress_file_with_next_steps()
identify_remaining_dependencies()
suggest_priorities_for_next_session()
```

## Troubleshooting

### Common Issues

1. **Ticket selection conflicts** → Use priority matrix
2. **Implementation ambiguity** → Choose simplest approach that meets AC
3. **Test failures** → Fix before proceeding
4. **Scope creep** → Split ticket or defer features

### Recovery Patterns

- Never skip a ticket without logging why
- Always leave the codebase in a working state
- Document any temporary workarounds

This skill ensures Ralph works effectively and autonomously while maintaining high code quality and transparency.
