---
name: verify
description: File structure verification - ensuring skill directory exists with all
  3 reference files in correct locations.
---

# Checkpoint: Create review-standards skill

## Verification Strategy
File structure verification - ensuring skill directory exists with all 3 reference files in correct locations.

## Subagents Launched
None required - this is file organization work.

## Confidence Assessment
- Confidence level: 95%
- Rationale: Simple file move operation with new SKILL.md creation. Structure verified via directory listing.

## Learnings
- Skills use relative markdown links (`./references/file.md`) which resolve correctly because skills have proper path resolution
- The existing checklists.md already used relative links (`./issue-patterns.md`) so no modification needed

## Human QA Checklist

### Prerequisites
None - this checkpoint creates new files.

### Verification Steps
- [ ] Verify skill directory exists: `ls -la plugins/unitwork/skills/review-standards/`
- [ ] Verify SKILL.md contains skill metadata with name and description
- [ ] Verify references/ directory contains all 3 files: issue-patterns.md, review-standards.md, checklists.md
- [ ] Verify old standards directory still exists (will be deleted in Unit 4)

### Notes
The skill is created but not yet referenced by the commands/agents. That happens in Units 2 and 3.
