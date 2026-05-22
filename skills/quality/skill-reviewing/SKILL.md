---
name: skill-reviewing
description: Comprehensive review of Claude Code skills and agents against v0.5
  guidelines. Validates metadata, implementation, and architecture. Use when
  reviewing existing packages or during skill development.
---

# Skill Reviewing

Provides comprehensive validation of Claude Code skills and agents against:
- Plugin Storage Conventions (NORMATIVE)
- Agent Tool Use Best Practices
- Architecture Guidelines v0.5

## Capabilities

This skill orchestrates three specialized review agents, each focusing on a distinct concern:

| Agent | Focus | Source Document |
|-------|-------|-----------------|
| `skill-metadata-storage-review` | Frontmatter & persistence | PLUGIN-STORAGE-CONVENTIONS.md |
| `skill-implementation-review` | Code mechanics & security | agent-tool-use-best-practices.md |
| `skill-architecture-review` | Design patterns & structure | claude-code-skills-agents-guidelines-0.4.md |

## Agent Delegation

All three agents are invoked via Agent Runner for parallel execution:

### Metadata & Storage Reviewer
**Validates:**
- YAML frontmatter (name, version, description)
- Version consistency with registry.yaml
- Storage paths (logs, settings, outputs)
- Secret handling
- Documentation completeness

**Returns:** `{success, data: {checks_performed, checks_passed, warnings, errors}, error}`

### Implementation Reviewer
**Validates:**
- JSON fencing
- Hook implementation (Python preferred)
- Dependency declarations
- Security patterns
- Cross-platform compatibility

**Returns:** `{success, data: {checks_performed, checks_passed, warnings, errors}, error}`

### Architecture Reviewer
**Validates:**
- Two-tier skill/agent separation
- Response contract compliance
- Single responsibility principle
- Agent size and complexity
- File organization

**Returns:** `{success, data: {checks_performed, checks_passed, warnings, errors}, error}`

## Orchestration Pattern

When user requests a review:

1. **Determine target**
   - Parse user input to identify what to review
   - Resolve to absolute path if needed
   - Determine target_type: "agent", "skill", or "package"

2. **Invoke agents in parallel**
   Use Agent Runner to invoke all three reviewers concurrently with parameters:

   **For skill-metadata-storage-review:**
   ```json
   {
     "target_type": "<agent|skill|package>",
     "target_path": "/absolute/path/to/target",
     "package_name": "<package-name-if-applicable>",
     "check_registry": true,
     "registry_path": ".claude/agents/registry.yaml"
   }
   ```

   **For skill-implementation-review:**
   ```json
   {
     "target_path": "/absolute/path/to/target",
     "check_hooks": true,
     "check_dependencies": true,
     "check_security": true,
     "manifest_path": "manifest.yaml"
   }
   ```

   **For skill-architecture-review:**
   ```json
   {
     "target_type": "<agent|skill|package>",
     "target_path": "/absolute/path/to/target",
     "check_two_tier": true,
     "check_contracts": true,
     "check_naming": true,
     "registry_path": ".claude/agents/registry.yaml"
   }
   ```

3. **Aggregate results**
   - Collect fenced JSON from all three agents
   - Parse and merge findings
   - Group by severity: errors, warnings, info
   - Organize by concern area (metadata, implementation, architecture)

4. **Format report**
   Present findings to user in this structure:

   ```
   ## Review Summary: [package-name]

   ✅ Metadata & Storage: X checks passed, Y warnings, Z errors
   ⚠️  Implementation: X checks passed, Y warnings, Z errors
   ✅ Architecture: X checks passed, Y warnings, Z errors

   ### Critical Issues (must fix)
   [List all errors with file:line and suggested actions]

   ### Warnings (should fix)
   [List all warnings with suggestions]

   ### Info (optional improvements)
   [List all info-level findings]
   ```

## Usage Examples

**Review entire package:**
```
/skill-reviewing sc-managing-worktrees
```

**Review specific agent:**
```
/skill-reviewing .claude/agents/sc-worktree-create.md
```

**Review skill:**
```
/skill-reviewing .claude/skills/managing-worktrees/
```

**Review during development:**
```
Review the skill I just created in .claude/skills/my-new-skill/
```

## Error Handling

### If Any Reviewer Fails
- Report which reviewer failed and why
- Include partial results from successful reviewers
- Suggest corrective action (e.g., "Registry file not found at .claude/agents/registry.yaml")
- Do not fail entire review if one agent has issues

### If All Reviewers Return No Issues
- Congratulate user on clean implementation
- Show summary: "All X checks passed across metadata, implementation, and architecture"
- Optionally suggest next steps (testing, documentation improvements)

### If Target Not Found
- Return clear error message
- Suggest correct paths for common targets
- Examples:
  - Agents: `.claude/agents/<name>.md`
  - Skills: `.claude/skills/<name>/SKILL.md`
  - Packages: `packages/<name>/`

## Notes

- **Parallel Execution:** All three agents run independently in isolated contexts
- **Structured Output:** Each agent returns fenced JSON for reliable parsing
- **Read-Only:** No agent modifies files; this is analysis only
- **Comprehensive:** Covers three orthogonal concerns for complete validation
- **Actionable:** Every finding includes suggested_action for quick fixes

## Related Documentation

- [Design Document](../../docs/design/skill-review-system.md) — Complete specification
- [Architecture Guidelines v0.5](../../docs/claude-code-skills-agents-guidelines-0.4.md) — Source guidelines
- [Plugin Storage Conventions](../../docs/PLUGIN-STORAGE-CONVENTIONS.md) — NORMATIVE storage rules
- [Tool Use Best Practices](../../docs/agent-tool-use-best-practices.md) — Implementation patterns
