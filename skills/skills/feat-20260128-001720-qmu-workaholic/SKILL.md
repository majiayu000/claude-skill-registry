---
created_at: 2026-01-28T00:32:39+09:00
author: a@qmu.jp
type: housekeeping
layer: [Config]
effort: XS
commit_hash: 16b0e61
category: Removed
---

# Remove block-commands skill

## Overview

The `block-commands` skill documents how to use `.claude/settings.json` deny rules to block dangerous commands. However, `.claude/settings.json` is a repository-local file that is not distributed with plugins. Users installing the plugin would not get these deny rules, making this approach ineffective for a marketplace plugin.

The skill should be removed since it documents a pattern we no longer recommend for plugin distribution.

## Key Files

- `plugins/core/skills/block-commands/SKILL.md` - Skill to delete

## Related History

The block-commands skill was created alongside moving git prohibitions to settings.json, but this approach has proven unsuitable for distributed plugins.

Past tickets that touched similar areas:

- `20260127094857-use-deny-for-git-prohibition.md` - Created block-commands skill and moved git -C prohibition to settings.json (same file)

## Implementation Steps

1. **Delete block-commands skill directory**:
   - Remove `plugins/core/skills/block-commands/` entirely

2. **Verify no references exist**:
   - Confirm no other files reference `block-commands` skill

## Considerations

- This removes documentation only, not actual functionality
- The `.claude/settings.json` deny rules remain in local repositories but are not part of plugin distribution
- For plugin-based command blocking, bundled shell scripts that refuse to execute are more appropriate (as done with archive-ticket)

## Final Report

Deleted the block-commands skill directory. Verified that no other plugin files reference this skill. Documentation in .workaholic/specs/ and .workaholic/terms/ will be updated automatically by the documentation agents when /report runs.
