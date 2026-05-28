---
name: marketplace-workflow
description: Use when user explicitly says "marketplace", "move to marketplace", "publish to marketplace", or "add to my marketplace". Never use for creating skills/rules in dotfiles or project-level locations.
---

# Marketplace Workflow

Workflow for moving user-level content (`~/.claude/`) to [jasonkuhrt/claude-marketplace](https://github.com/jasonkuhrt/claude-marketplace).

## Paths

| What | Path |
|------|------|
| Marketplace repo (GitHub) | https://github.com/jasonkuhrt/claude-marketplace |
| Marketplace repo (local) | `~/projects/jasonkuhrt/claude-marketplace` |
| User-level source | `~/.claude/` |
| Collaborative projects | `~/projects/heartbeat-chat/*` |

## Workflow

1. **Identify target plugin**: Check existing plugins in marketplace. If thing fits one, use it. If none, multiple, or ambiguous, ask user with suggestions for new plugin name/concept.

2. **Check context**:
   - If in collaborative project (`~/projects/heartbeat-chat/*`): ask if plugin should install at project level instead of user level
   - Otherwise: default to user-level install

3. **Create/update plugin**: Add command/skill/rule to the target plugin in the marketplace repo.

4. **Install**: Configure plugin to install at appropriate level (user or project).

5. **Post-migration actions**: Use AskUserQuestion with multiSelect to offer:
   - "Remove source" - Delete original file(s) from source location (destructive)
   - "Commit to marketplace" - Create commit in marketplace repo
   - "Push to remote" - Push marketplace commits (only if commit was made)

## Existing Plugins

Check `~/projects/jasonkuhrt/claude-marketplace/plugins/` for current plugins before suggesting new ones.
