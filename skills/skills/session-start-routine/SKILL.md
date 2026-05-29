---
name: session-start-routine
description: Execute work session initialization routine at conversation start. Identifies new skills, researches improvements for existing skills, and updates skill library. Triggers automatically at session start.
version: 2.0.0
category: meta
last_updated: 2026-01-02
related_skills:
  - skill-creator
  - compliance-check
  - repo-sync
---

# Session Start Routine Skill

> Version: 2.0.0
> Created: 2025-12-30
> Last Updated: 2026-01-02

## Overview

This meta-skill defines the mandatory work session initialization routine. At the start of every conversation, Claude should execute this routine to maintain and improve the skills library.

## Quick Start

1. **Trigger** - Say "session start" or `/session-start-routine`
2. **Health check** - Claude scans skill locations
3. **Review report** - See skills health summary
4. **Act on findings** - Update stale skills if needed

```bash
# Quick health check command
find ~/.claude/skills -name "SKILL.md" -mtime +30 -exec echo "Stale: {}" \;

# Count skills
find ~/.claude/skills -name "SKILL.md" | wc -l
```

## When to Use

- **MANDATORY** at every session start
- First message in a new conversation
- When explicitly requested with `/session-start-routine`
- After extended breaks between sessions
- When noticing skill-related issues

## When to Trigger

**MANDATORY at every session start:**
- First message in a new conversation
- When explicitly requested with `/session-start-routine`

## Session Routine Steps

### Step 1: Skills Health Check

```
1. Scan both skill locations:
   - User-level: ~/.claude/skills/
   - Project-level: .claude/skills/

2. For each skill:
   - Verify SKILL.md exists and is valid
   - Check for version history section
   - Identify last update date
   - Flag skills not updated in 30+ days

3. Dependency Verification:
   - Check if tools/libraries referenced in skills still exist
   - Verify MCP servers mentioned are still available
   - Test that code examples are still valid
   - Flag skills with broken dependencies
```

### Step 1b: Integration Check

```
1. MCP Server Compatibility:
   - List skills that reference MCP servers
   - Verify those servers exist in ~/.claude.json or .mcp.json
   - Check for deprecated MCP tool names

2. Agent Compatibility:
   - Verify skills work with current Claude Code agents
   - Check for deprecated agent patterns
   - Update agent references if needed
```

### Step 1c: Cross-Skill Dependencies

```
1. Build dependency map:
   - Extract "Related Skills" sections
   - Identify which skills reference others
   - Detect orphaned or circular dependencies

2. Dependency Graph:
   skill-creator
     +-- sparc-workflow
     +-- mcp-builder
   rag-system-builder
     +-- knowledge-base-builder
     +-- semantic-search-setup
     +-- pdf-text-extractor
```

### Step 2: Research & Improvement Identification

```
For each skill category, research:
1. Official documentation updates
   - Anthropic Claude documentation
   - Tool/library changelogs

2. Community best practices
   - GitHub trending repositories
   - Stack Overflow discussions

3. Industry trends
   - New tools/libraries
   - Methodology updates
   - Security advisories
```

### Step 3: Skill Updates

```
For skills needing updates:
1. Research latest best practices online
2. Identify specific improvements:
   - New features to document
   - Deprecated approaches to remove
   - Better code examples
   - Performance optimizations

3. Apply updates with version comment:
   ---
   ## Version History
   - **X.Y.Z** (YYYY-MM-DD): [Changes made]
   ---
```

### Step 4: New Skill Identification

Evaluate need for new skills based on:

```
1. GAPS: Missing capabilities discovered during work
   - "I needed to do X but no skill existed"
   - Repeated manual processes

2. PATTERNS: Common workflows across sessions
   - Frequently used tool combinations
   - Repeated prompt patterns

3. TRENDS: Industry/technology developments
   - New Claude Code features
   - New MCP servers
   - Popular libraries/tools
   - AI/ML advancements
```

### Step 5: Documentation Update

```
1. Update skills/README.md with:
   - New skills added
   - Skills updated
   - Skills deprecated

2. Commit changes with descriptive message
```

## Session Report Template

At the end of routine, provide summary:

```markdown
## Session Start Report - [DATE]

### Skills Health
- Total Skills: [N]
- User-Level: [N] | Project-Level: [N]
- Updated This Session: [N]
- Flagged for Review: [N]

### Improvements Made
| Skill | Version | Changes |
|-------|---------|---------|
| skill-name | X.Y.Z | Brief description |

### New Skills Identified
| Proposed Skill | Category | Rationale |
|----------------|----------|-----------|
| skill-name | category | Why needed |

### Research Findings
- [Key finding 1]
- [Key finding 2]

### Next Session Priorities
1. [Priority 1]
2. [Priority 2]
```

## Execution Checklist

Before routine:
- [ ] Session context established
- [ ] Access to skill directories confirmed
- [ ] Network access for research (optional)

During routine:
- [ ] User-level skills scanned
- [ ] Project-level skills scanned
- [ ] Stale skills identified (30+ days)
- [ ] Broken dependencies flagged
- [ ] Cross-skill dependencies mapped

After routine:
- [ ] Session report generated
- [ ] Priority actions identified
- [ ] Updates committed (if any)
- [ ] README updated (if changes)

## Skill Update Guidelines

### Version Numbering

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes, complete rewrites
MINOR: New features, significant improvements
PATCH: Bug fixes, small updates, typo fixes
```

### Version Comment Format

Add at end of SKILL.md:

```markdown
---

## Version History

- **1.2.0** (2025-12-30): Added new section for X, updated examples
- **1.1.1** (2025-12-15): Fixed typo in command example
- **1.1.0** (2025-12-01): Added integration with tool Y
- **1.0.0** (2025-11-15): Initial release
```

## Error Handling

### Common Errors

**Error: Skill directory not accessible**
- Cause: Permissions or path issues
- Solution: Verify ~/.claude/skills/ exists and is readable

**Error: SKILL.md parsing fails**
- Cause: Invalid YAML frontmatter or markdown
- Solution: Validate frontmatter syntax, check for unclosed code blocks

**Error: MCP server not found**
- Cause: Referenced MCP server not configured
- Solution: Update skill to remove reference or add server to config

**Error: Circular dependency detected**
- Cause: Skills reference each other in loop
- Solution: Review related_skills, break the cycle

**Error: Too many stale skills**
- Cause: Routine not run regularly
- Solution: Prioritize most-used skills, update in batches

## Research Sources

### Official Documentation
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Specification](https://modelcontextprotocol.io/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)

### Community Resources
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Claude Code Community](https://github.com/anthropics/claude-code)
- GitHub trending repositories

### Technology Updates
- Python/Node.js changelogs
- Library release notes
- Security advisories (CVE databases)

## Integration Points

### With Other Skills
- Uses `skill-creator` patterns for new skills
- Follows `compliance-check` standards
- Updates `workspace-hub` skills as needed

### With Workflows
- Can trigger before SPARC workflow
- Integrates with git operations for commits
- Works with Agent OS task execution

## Automation Hooks

### Pre-Session Check

```bash
# Quick health check script
find ~/.claude/skills -name "SKILL.md" -mtime +30 -exec echo "Stale: {}" \;
```

### Post-Update Commit

```bash
# Commit pattern for skill updates
git add ~/.claude/skills/
git commit -m "chore(skills): session update - [YYYY-MM-DD]

- Updated: [skill1], [skill2]
- Added: [new-skill]
- Research: [topic]"
```

## Usage Analytics

Track skill usage to prioritize improvements:

```
1. Usage Tracking:
   - Note which skills are triggered during sessions
   - Track frequency of skill invocations
   - Identify most/least used skills

2. Prioritization Matrix:
   HIGH PRIORITY (Frequently used, needs update):
   - mcp-builder (used 50+/month, last update 30+ days)

   MEDIUM PRIORITY (Used often, recently updated):
   - rag-system-builder (used 30+/month, updated recently)

   LOW PRIORITY (Rarely used):
   - algorithmic-art (used 2/month)

3. Usage Log Format:
   ~/.claude/skills/.usage-log.json
   {
     "2025-12-30": {
       "mcp-builder": 3,
       "rag-system-builder": 2,
       "sparc-workflow": 5
     }
   }
```

## Deprecation Review

Flag outdated skills for removal or major update:

```
1. Deprecation Criteria:
   - Not updated in 90+ days
   - References deprecated tools/APIs
   - Superseded by better skill
   - Zero usage in 60+ days

2. Deprecation Process:
   a. Add DEPRECATED prefix to description
   b. Add deprecation notice at top of SKILL.md
   c. Point to replacement skill
   d. Remove after 30-day grace period

3. Deprecation Notice Template:
   ---
   name: old-skill-name
   description: DEPRECATED - Use new-skill-name instead. [Original description]
   deprecated: true
   deprecated_date: 2025-12-30
   replacement: new-skill-name
   ---

   > **DEPRECATED**: This skill is deprecated. Use [new-skill-name](../new-skill-name/SKILL.md) instead.
   > Will be removed after 2025-01-30.
```

## Metrics

Track over time:

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Skills updated per session | 1-3 | Count of version bumps |
| New skills added per month | 2-5 | New SKILL.md files |
| Stale skill ratio | <20% | Skills 30+ days old / total |
| Trigger accuracy | >90% | Correct activations |
| Integration health | 100% | Working MCP/agent refs |
| Deprecation candidates | <5% | Unused 60+ days |

## Best Practices

1. **Consistency**: Run at every session start
2. **Brevity**: Keep updates focused, don't over-engineer
3. **Documentation**: Always add version comments
4. **Research First**: Check online before updating
5. **Prioritize**: Focus on most-used skills first
6. **Test**: Verify updated skills still work correctly

## Related Skills

- [skill-creator](../../builders/skill-creator/SKILL.md) - For creating new skills
- [compliance-check](../../workspace-hub/compliance-check/SKILL.md) - For standards verification
- [repo-sync](../../workspace-hub/repo-sync/SKILL.md) - For committing changes

---

## Version History

- **2.0.0** (2026-01-02): Upgraded to v2 template - added Quick Start, When to Use, Execution Checklist, Error Handling, enhanced Metrics sections; enhanced frontmatter with version, category, related_skills
- **1.0.0** (2025-12-30): Initial release - session start routine skill
