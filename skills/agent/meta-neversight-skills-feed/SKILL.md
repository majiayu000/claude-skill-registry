---
name: meta
description: Execute Claude Code commands in the telegram_agent project directory. Use when the user wants to work on the telegram agent itself, fix bugs, add features, or modify the bot code. This is a COMMAND HANDLER, not a script executor.
---

# Meta Skill - Command Handler

⚠️ **IMPORTANT**: This skill is a COMMAND HANDLER registration. It tells the bot to handle `/meta` commands by spawning Claude Code Agent SDK sessions in the telegram_agent directory.

## What This Does

Registers `/meta` as a command handler that:
1. Takes the user's prompt after `/meta`
2. Spawns a Claude Code Agent SDK session
3. Sets working directory to `~/ai_projects/telegram_agent`
4. Returns responses in Telegram

## Implementation

The actual command handler needs to be registered in the telegram bot codebase at:
- `src/bot/handlers/claude_commands.py` - Add meta command handler
- `src/bot/bot.py` - Register the command

## Usage Pattern

User types in Telegram:
```
/meta fix the rate limiting bug
/meta add better logging
/meta refactor authentication
```

Bot spawns Claude Agent SDK with:
- Working directory: `~/ai_projects/telegram_agent`
- Prompt: User's text after `/meta`
- Same infrastructure as `/claude` command

## Example User Requests

- `/meta fix bug in message handler`
- `/meta add error recovery to file sending`
- `/meta refactor the session management`
- `/meta improve the keyboard layout`

## Implementation Notes

Must use `ClaudeCodeService` with custom `cwd` parameter:
```python
service.execute_prompt(
    prompt=user_prompt,
    cwd="/Users/server/ai_projects/telegram_agent"
)
```
