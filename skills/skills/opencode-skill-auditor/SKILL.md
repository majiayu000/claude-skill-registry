---
name: opencode-skill-auditor
description: Audit existing OpenCode skills to identify modularization opportunities and eliminate redundancy
license: Apache-2.0
compatibility: opencode
metadata:
  audience: developers
  workflow: analysis-and-optimization
---

## What I do

- Analyze the current set of OpenCode skills for redundancy, overlap, and duplication
- Identify granular functionality that can be extracted into reusable skill components
- Recommend modularization strategies to improve skill ecosystem efficiency
- Ensure proposed new skills follow DRY principles and OpenCode best practices
- Provide comprehensive gap analysis and skill optimization recommendations
- Generate detailed reports on skill interdependencies and coupling issues
- Suggest consolidation opportunities for closely related skillsets

## When to use me

Use this when:
- You need to analyze the existing skill ecosystem for optimization opportunities
- You want to identify redundant functionality across multiple skills
- You're planning to refactor or consolidate the skill library
- You need to ensure new skills won't duplicate existing capabilities
- You want to improve maintainability and reduce code duplication in skills
- You're developing a strategy for skill ecosystem growth and organization

Ask me to analyze specific skill directories, focus on particular capability areas, or provide comprehensive ecosystem audits.

## Prerequisites

- Access to the skills directory containing all OpenCode skill definitions
- Basic understanding of OpenCode skill structure and YAML frontmatter format
- Familiarity with modular design principles and DRY methodology
- Permission to read and analyze skill documentation files
- (Optional) Git history access for tracking skill evolution and dependencies

## Steps

1. **Skill Discovery**
   ```bash
   # Locate all skill definitions in the repository
   find . -name "SKILL.md" -type f | sort
   
   # Extract skill metadata for analysis
   grep -h "^name:" skills/*/SKILL.md | sort
   ```

2. **Capability Analysis**
   - Read each skill's "What I do" section to identify core functionalities
   - Extract and categorize capability patterns across all skills
   - Map skill descriptions to functional domains and use cases

3. **Redundancy Detection**
   - Compare skill descriptions for overlapping functionality
   - Identify similar capability patterns and use case scenarios
   - Flag skills with near-identical purposes or target audiences

4. **Granularity Assessment**
   - Evaluate whether skills can be broken down into smaller, reusable components
   - Identify compound skills that contain multiple distinct capabilities
   - Assess potential for extracting shared functionality into base skills

5. **Dependency Mapping**
   - Analyze skill interdependencies and coupling relationships
   - Identify skills that reference or build upon other skills
   - Map the skill hierarchy and dependency graph

6. **Recommendation Generation**
   - Propose specific modularization strategies with concrete examples
   - Suggest skill consolidation opportunities with migration paths
   - Recommend new granular skills to fill identified gaps
   - Provide priority rankings based on impact and feasibility

7. **Best Practices Validation**
   - Ensure proposed changes follow OpenCode naming conventions
   - Validate that new skill structures maintain proper YAML frontmatter
   - Verify that modularization preserves existing functionality

## Best Practices

- **Systematic Analysis**: Process skills in logical groups by capability domain or workflow type
- **Documentation-First**: Always preserve existing functionality and user-facing behavior
- **Incremental Changes**: Propose modularization in stages to minimize disruption
- **Backward Compatibility**: Ensure existing integrations continue to work during transitions
- **Clear Naming**: Use descriptive, distinguishable names for new granular skills
- **Cross-Reference**: Maintain clear documentation of relationships between original and modularized skills
- **Community Input**: Consider existing usage patterns and community feedback when proposing changes

## Common Issues

**Issue: Skills appear similar but serve different contexts**
- Solution: Focus on specific use cases and target audiences in your analysis
- Consider context-specific optimizations that justify separate skills

**Issue: Over-granularization leading to skill fragmentation**
- Solution: Balance between reusability and usability
- Group related capabilities logically while maintaining meaningful skill boundaries

**Issue: Missing documentation for skill interdependencies**
- Solution: Create dependency mapping as part of your analysis
- Document implicit relationships and usage patterns

**Issue: Legacy skills with outdated structures**
- Solution: Prioritize updates to skills that don't follow current best practices
- Provide migration paths for modernizing skill structures

**Issue: Difficulty measuring impact of proposed changes**
- Solution: Use usage metrics and community feedback when available
- Implement A/B testing or gradual rollouts for significant changes

## Analysis Commands

```bash
# Quick skill overview with metadata
for skill in skills/*/SKILL.md; do
  echo "=== $(basename $(dirname "$skill")) ==="
  grep -E "^name:|^description:|^metadata:" "$skill"
  echo
done

# Find skills with similar descriptions
grep -h "^description:" skills/*/SKILL.md | sort | uniq -c | sort -nr

# Analyze skill distribution by workflow type
grep -A1 "workflow:" skills/*/SKILL.md | grep "workflow:" | sort | uniq -c

# Check for naming convention compliance
ls skills/ | grep -E "^[a-z0-9]+(-[a-z0-9]+)*$"
```