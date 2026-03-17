# Workspace Health Check Skill

Assesses workspace alignment and suggests cleanup or realignment actions at key transition points.

## Trigger Conditions

This skill should be invoked:
- At the end of phase transitions (flow commands)
- After completing major features or intensive processes
- When documentation appears out of sync
- Manually via "check workspace health" or similar

## Natural Language Triggers

- "check workspace health"
- "is my workspace aligned"
- "workspace status"
- "do I need to realign"
- "cleanup recommendations"

## Assessment Checklist

### 1. Working Directory Health

```yaml
checks:
  - name: working_directory_size
    description: Check if .aiwg/working/ has accumulated stale files
    threshold: ">10 files or >1MB"
    action: Suggest /workspace-prune-working

  - name: orphan_drafts
    description: Draft artifacts not linked to requirements
    action: Suggest review or archival

  - name: stale_locks
    description: Lock files older than 24h
    action: Suggest cleanup
```

### 2. Documentation Alignment

```yaml
checks:
  - name: phase_documentation
    description: Current phase docs match project state
    sources:
      - .aiwg/planning/phase-plan-*.md
      - .aiwg/reports/*-completion-report.md
    action: Suggest /workspace-realign if mismatched

  - name: requirement_coverage
    description: All requirements have linked artifacts
    action: Suggest /check-traceability

  - name: architecture_drift
    description: Code diverged from documented architecture
    action: Suggest architecture review or ADR update
```

### 3. Artifact Freshness

```yaml
checks:
  - name: stale_artifacts
    description: Key artifacts not updated in >30 days during active dev
    artifacts:
      - SAD (Software Architecture Document)
      - Risk Register
      - Test Strategy
    action: Flag for review

  - name: completion_markers
    description: Artifacts marked complete but phase still active
    action: Suggest status update
```

## Output Format

```markdown
## Workspace Health Report

**Overall Status**: [Healthy | Needs Attention | Requires Realignment]

### Quick Actions
- [ ] Run `/workspace-prune-working` - 15 stale files in working/
- [ ] Review 3 orphaned draft artifacts
- [ ] Update risk register (last modified 45 days ago)

### Detailed Findings

#### Working Directory
- Status: Needs cleanup
- Files: 15 (threshold: 10)
- Oldest: inception-notes-draft.md (created 2024-11-15)
- Recommendation: Promote or archive before next phase

#### Documentation Alignment
- Phase: Construction
- Last phase report: Elaboration completion (2024-12-01)
- Missing: Construction kickoff documentation
- Recommendation: Run `/flow-elaboration-to-construction` completion steps

#### Traceability
- Requirements covered: 85%
- Orphan code files: 3
- Recommendation: Run `/check-traceability` for details
```

## Integration Points

### Flow Command Endings

Add to flow command templates:

```markdown
## Post-Completion

After this flow completes, consider running a workspace health check:

[workspace-health] Assessing workspace alignment...

If issues found, the skill will suggest appropriate cleanup commands.
```

### Proactive Invocation

The orchestrator should invoke this skill:
1. When transitioning between SDLC phases
2. After completing iteration cycles
3. When user requests project status
4. Before major deployments

## Implementation Notes

This skill should:
1. Read workspace state from `.aiwg/` structure
2. Compare against expected state for current phase
3. Generate actionable recommendations
4. NOT automatically execute cleanup (user confirms)

## Related Commands

- `/workspace-prune-working` - Clean up working directory
- `/workspace-realign` - Reorganize documentation structure
- `/workspace-reset` - Full workspace reset (destructive)
- `/project-status` - Current project state
- `/check-traceability` - Verify requirement links
