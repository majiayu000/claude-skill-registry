---
name: enable-feedback-hooks
description: Enable feedback capture hooks for the current project
argument-hint: "[--disable]"
---

# Enable Feedback Hooks

Opt-in the current project to capture feedback for Product Forge improvements.

## What This Does

When enabled, at the end of each Claude Code session:
1. **Haiku analyzes** the conversation for improvement opportunities
2. **Feedback is saved** to `~/.claude/learnings/` for later review
3. **No data leaves your machine** - feedback stays local until you sync

## Feedback Types Captured

- **Improvements** - Enhancements to existing skills, commands, or agents
- **Skill ideas** - New skills that could help others
- **Command ideas** - New commands that could be useful
- **Bug reports** - Issues with existing components
- **Patterns** - Reusable patterns from your project

## Enable for Current Project

Add the Stop hook to `.claude/settings.local.json`:

```bash
/enable-feedback-hooks
```

## Disable

Remove the hook from the current project:

```bash
/enable-feedback-hooks --disable
```

## How It Works

```
Session ends → Haiku analyzes → Saves to ~/.claude/learnings/
                                         ↓
                            Use /sync-feedback to review
```

## Privacy

- Feedback analysis happens locally via Haiku
- Feedback files stored only on your machine
- You review and choose what to submit via `/sync-feedback`
- Nothing is sent to Product Forge without your explicit action

## Execution Instructions

When the user runs this command:

### Enable Mode (default)

1. **Initialize learnings directory** if needed:
   ```bash
   ~/.claude/plugins/cache/product-forge-marketplace/scripts/hooks/init-learnings.sh
   ```

2. **Check if .claude directory exists**, create if needed:
   ```bash
   mkdir -p .claude
   ```

3. **Read existing settings.local.json** or create empty structure:
   ```bash
   # If exists, read it
   cat .claude/settings.local.json 2>/dev/null || echo '{}'
   ```

4. **Add the Stop hook configuration**:
   - Merge with existing hooks if any
   - Write the following hook configuration:

   ```json
   {
     "hooks": {
       "Stop": [
         {
           "hooks": [
             {
               "type": "prompt",
               "prompt": "Analyze this session for Product Forge feedback. Identify:\n1. Improvements to existing skills/commands/agents\n2. New skill/command ideas\n3. Bug reports\n4. Reusable patterns\n\nRespond JSON: {\"feedback\": [{\"type\": \"improvement|skill-idea|command-idea|bug-report|pattern\", \"title\": \"...\", \"description\": \"...\", \"target\": \"plugin/component\"}]} or {\"feedback\": []}",
               "timeout": 60
             },
             {
               "type": "command",
               "command": "python3 ~/.claude/plugins/cache/product-forge-marketplace/scripts/hooks/save-feedback.py",
               "timeout": 10
             }
           ]
         }
       ]
     }
   }
   ```

5. **Confirm success**:
   ```
   Feedback hooks enabled for this project.

   At the end of each session, Haiku will analyze the conversation
   for improvement opportunities and save them to ~/.claude/learnings/

   Use /sync-feedback to review and submit feedback to Product Forge.
   ```

### Disable Mode (--disable)

1. **Read existing settings.local.json**:
   ```bash
   cat .claude/settings.local.json
   ```

2. **Remove the Stop hook** while preserving other settings

3. **Write back the modified settings**

4. **Confirm**:
   ```
   Feedback hooks disabled for this project.
   Existing feedback in ~/.claude/learnings/ is preserved.
   ```

## Notes

- The hook configuration is stored in `.claude/settings.local.json` (not committed to git)
- Each project opts in independently
- Feedback is aggregated across all opted-in projects in `~/.claude/learnings/`
