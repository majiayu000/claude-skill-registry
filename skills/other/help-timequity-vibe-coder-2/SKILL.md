---
name: mvp-help
description: |
  Help and documentation for Idea to MVP plugin.
  Use when: user asks about building MVPs, vibe coding, or available commands.
  Triggers: "help", "what can you do", "mvp help", "how to build".
---

# Idea to MVP Help

Vibe coding: describe your idea, get a deployed MVP.

## How It Works

```
You: "I want an app for tracking expenses"
     ↓
Claude: Asks clarifying questions
     ↓
Claude: Builds everything (hidden complexity)
     ↓
You: "✅ Done! [Preview] [Deploy]"
```

## Commands

| Command | Description |
|---------|-------------|
| `/mvp:brainstorm` | Refine idea with Socratic dialogue |
| `/mvp:idea` | Start from scratch with simple questions |
| `/mvp:build` | Create the app (full pipeline) |
| `/mvp:add` | Add feature to existing app |
| `/mvp:preview` | Show current state |
| `/mvp:deploy` | Publish to production |

## Skills (Hidden Pipeline)

These work automatically behind the scenes:

| Phase | Skills |
|-------|--------|
| Ideation | brainstorming, idea-validation |
| Planning | stack-selector, db-designer |
| Building | ui-generator, api-generator, feature-builder |
| Quality | test-driven-development, auto-testing, security-check |
| Polish | frontend-design, theme-factory, code-review-auto |
| Deploy | deploy-automation, verification-gate |

## Quick Start

### Have an idea?
```
/mvp:idea
```
Answer simple questions, get an app.

### Want to explore first?
```
/mvp:brainstorm
```
Refine your idea before building.

### Ready to build?
```
/mvp:build
```
Full pipeline: design → code → test → deploy.

## No Technical Jargon

You never need to know:
- What framework to use
- How to structure code
- What tests to write
- How to deploy

Just describe what you want. We handle the rest.

## Troubleshooting

### Плагин не обновляется после `/plugin`

Если после обновления плагина (`/plugin` → Update) изменения не применяются:

```bash
# Удалить кэш плагина
rm -rf ~/.claude/plugins/cache/vibe-coder

# Затем заново
/plugin
# → vibe-coder → Update
```

После этого перезапустить Claude Code.

### Команды не работают

1. Проверить что плагин установлен: `/plugin` → должен показать vibe-coder
2. Перезапустить Claude Code после установки/обновления
3. Если всё ещё не работает — удалить кэш (см. выше)
