---
name: openai-chatkit-setup
description: DEPRECATED - Use chatkit-frontend skill instead. This skill has been consolidated into the chatkit-frontend skill for better organization.
allowed-tools: Bash, Write, Read, Edit, Glob
deprecated: true
---

# OpenAI ChatKit Setup (DEPRECATED)

> **This skill has been deprecated and consolidated into `chatkit-frontend`.**
>
> Please use the `chatkit-frontend` skill instead for all ChatKit React frontend implementation.

## Migration

Use the consolidated skill:

```
.claude/skills/chatkit-frontend/SKILL.md
```

The `chatkit-frontend` skill includes:
- Complete ChatKit React setup with `@openai/chatkit-react`
- `useChatKit` hook configuration (api, theme, startScreen, events)
- Custom conversation sidebar integration
- Dark mode and theming support
- Widget integration patterns
- Migration guide from custom UI to ChatKit
- Comprehensive examples

## See Also

- [chatkit-frontend](../chatkit-frontend/SKILL.md) - **USE THIS INSTEAD**
- [chatkit-backend](../chatkit-backend/SKILL.md) - Backend SSE endpoint
