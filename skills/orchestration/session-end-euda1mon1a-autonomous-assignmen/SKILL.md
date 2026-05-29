---
name: session-end
description: Mandatory session close-out with IG audit, AAR, HISTORIAN, and RELEASE_MANAGER. Enforces clean session handoff.
model_tier: sonnet
parallel_hints:
  can_parallel_with: []
  must_serialize_with: [startup, startupO]
  preferred_batch_size: 1
context_hints:
  max_file_context: 60
  compression_level: 1
  requires_git_context: true
  requires_db_context: false
escalation_triggers:
  - pattern: "uncommitted.*changes"
    reason: "Uncommitted work needs human decision on how to handle"
  - pattern: "failing.*tests"
    reason: "Test failures need human review before session close"
---

# Session End Skill

> **Purpose:** Clean session close-out with governance checks
> **Trigger:** `/session-end` or `/bye` or `/done`
> **Enforcement:** Controlled by `.claude/Governance/config.json`

## Checklist (Required)

### 1. Stack Health
- [ ] Run `./scripts/stack-health.sh` - all services GREEN
- [ ] Run `./scripts/stack-health.sh --full` - lint/typecheck clean

### 2. Work State
- [ ] All changes committed or stashed
- [ ] No failing tests introduced
- [ ] Linters pass (ruff, eslint)

### 4. Documentation
- [ ] CHANGELOG updated if features added
- [ ] TODOs resolved or documented in HUMAN_TODO.md

### 5. Mandatory Governance Agents (ALWAYS INVOKED)

Regardless of governance_enabled setting, these agents are ALWAYS invoked at session end:

| Agent | Purpose | Cannot Skip |
|-------|---------|-------------|
| DELEGATION_AUDITOR (IG) | Audit spawn counts, chain violations, bypasses | ✓ |
| COORD_AAR | After-action review, lessons learned | ✓ |
| HISTORIAN | Session record for continuity | ✓ |
| RELEASE_MANAGER | Version status, release readiness | ✓ |

**Note:** Use `/session-end --force` only in true emergencies. Skipping these agents loses institutional memory.

**DELEGATION_AUDITOR (IG):**
- Spawn count for session
- Chain-of-command violations
- Bypass justifications

**COORD_AAR (After Action Review):**
- What went well
- What could improve
- Patterns discovered
- Lessons learned

**HISTORIAN:**
- Major features completed
- Architectural decisions
- Notable incidents
- Session continuity

**RELEASE_MANAGER:**
- Current version status
- Uncommitted changes check
- Release readiness assessment
- Next release steps

### 4. Knowledge Preservation (G-Staff Integration)

**Invoke G4_CONTEXT_MANAGER (RAG/Vector Updates):**
- Index new session artifacts for retrieval
- Update embeddings for modified documentation
- Ensure next session has full context access

**Invoke KNOWLEDGE_CURATOR (via COORD_OPS):**
- Extract cross-session patterns
- Update PATTERNS.md, DECISIONS.md
- Create session handoff documentation

**Invoke G4_LIBRARIAN (optional):**
- Archive session transcripts
- Catalog new skills/agents created
- Update knowledge graph relationships

## Quick Exit (Emergency)

```
/session-end --force
```
Skips all checks. Logs bypass.

## Output Format

```
================================================================================
                           SESSION END REPORT
================================================================================

## Stack Health
[output of ./scripts/stack-health.sh --full]

## Work Summary
- Commits: [count]
- Files Modified: [count]
- Tests Added/Modified: [count]

## Git Status
[output of git status]

## IG Report (DELEGATION_AUDITOR)
- Total Spawns: [count]
- Chain-of-Command Violations: [count]
- Bypasses: [list with justifications]

## After Action Review (AAR)
### What Went Well
- [item]

### What Could Improve
- [item]

### Patterns Discovered
- [item]

### Lessons Learned
- [item]

## HISTORIAN Entry
[Summary for session history]

## Release Status (RELEASE_MANAGER)
- Current Version: [version]
- Uncommitted Changes: [yes/no]
- Release Readiness: [ready/blocked/needs-review]
- Next Steps: [recommendations]

## Knowledge Preservation (G-Staff)
- G4_CONTEXT_MANAGER: [documents indexed for RAG]
- KNOWLEDGE_CURATOR: [patterns extracted, handoff created]
- G4_LIBRARIAN: [artifacts cataloged] (if invoked)

## Recommendations for Next Session
- [item]

================================================================================
                              SESSION CLOSED
================================================================================
```

## Execution Steps

1. **Stack Health Check**
   ```bash
   ./scripts/stack-health.sh --full
   ```
   - Must be GREEN to proceed
   - YELLOW acceptable with justification
   - RED blocks session end (fix issues first)

2. **Check Git State**
   ```bash
   git status
   git diff --stat
   ```

4. **Run Linters** (if not already done by stack-health)
   ```bash
   cd backend && ruff check . --fix
   cd frontend && npm run lint:fix
   ```

5. **Verify Tests**
   ```bash
   cd backend && pytest --tb=no -q
   cd frontend && npm test -- --passWithNoTests
   ```

6. **Check Governance Config**
   ```bash
   cat .claude/Governance/config.json
   ```

7. **Generate IG Report** (DELEGATION_AUDITOR)
   - Review session for agent spawns
   - Check for chain-of-command violations
   - Document any bypasses

8. **Conduct AAR** (COORD_AAR)
   - Reflect on session outcomes
   - Identify improvements
   - Capture patterns and lessons

9. **Update HISTORIAN**
   - Write to `.claude/History/sessions/`
   - Include major decisions and outcomes

10. **Release Status Check** (RELEASE_MANAGER)
    - Check version status
    - Verify no blocking issues
    - Document release readiness

11. **Knowledge Preservation** (G-Staff)
    - Spawn G4_CONTEXT_MANAGER for RAG/vector updates
    - Spawn KNOWLEDGE_CURATOR for pattern synthesis
    - Optionally spawn G4_LIBRARIAN for archival

12. **Final Handoff**
   - Summarize state for next session
   - Note any pending work
   - Verify RAG index updated

## Integration with Other Skills

- **startup/startupO**: Session-end complements startup for session lifecycle
- **code-review**: Can be invoked before session-end for final review
- **pre-pr-checklist**: Session-end incorporates similar checks

## Aliases

- `/session-end` - Full protocol
- `/bye` - Alias for `/session-end`
- `/done` - Alias for `/session-end`
- `/session-end --force` - Emergency exit, skips checks
- `/session-end --quick` - Minimal checks, no AAR
