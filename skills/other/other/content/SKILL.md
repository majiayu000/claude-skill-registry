---
name: content
description: Generate posts, essays and images following brand guidelines. Use for tweets, essays, Telegram posts, and image generation. Load identity from ~/CybosVault/private/context/identity.md.
---

# Content Skill

Generate posts, essays and images following brand guidelines. Load identity from `~/CybosVault/private/context/identity.md`.

## Architecture

```
COMMAND (cyber-essay, cyber-tweet, etc.)
    │
    ▼
WORKFLOW (essay.md, tweet.md, telegram-post.md)
    │
    ├─► LOADS: context/style/voice-identity.md (shared persona)
    │
    └─► LOADS: context/writing-style-[en|ru].md (language-specific)
```

## Context Files

| File | Purpose |
|------|---------|
| `context/style/voice-identity.md` | **SHARED**: Persona, tone, anti-patterns |
| `context/style/writing-style-en.md` | **ENGLISH**: Essay structure, tweet format, style rules |
| `context/style/writing-style-ru.md` | **RUSSIAN**: Telegram format, Russian-specific rules |

## Workflows

| Workflow | Language | Output |
|----------|----------|--------|
| `workflows/essay.md` | English | Long-form essays |
| `workflows/tweet.md` | English | Twitter threads |
| `workflows/telegram-post.md` | Russian + English | Telegram posts with translations |
| `workflows/image.md` | - | Image generation |

## Agents

| Agent | Purpose |
|-------|---------|
| `content-writer` | Drafts content (loads style guides itself) |

Note: Image generation runs in main session (pipeline in `workflows/image.md`), not via spawned agent.

## Commands

| Command | Maps To |
|---------|---------|
| `/cyber-essay` | `workflows/essay.md` |
| `/cyber-tweet` | `workflows/tweet.md` |
| Telegram post request | `workflows/telegram-post.md` |
| `/cyber-image` | `workflows/image.md` |

## MCP Tools

- `mcp__nano-banana__generate_image`: Image generation (Gemini)
- `mcp__perplexity__perplexity_search`: Fact-checking
- `mcp__exa__search`: Recent news/data

## Output Locations

| Type | Location |
|------|----------|
| Posts | `~/CybosVault/private/content/posts/MMDD-<slug>-YY.md` |
| Essays | `~/CybosVault/private/content/essays/MMDD-<slug>-YY.md` |
| Tweets | `~/CybosVault/private/content/tweets/MMDD-<slug>-YY.md` |
| Images | `~/CybosVault/private/content/images/MMDD-<slug>-YY.png` |

## Key Rules

1. **Commands call workflows** - No embedded style in commands
2. **Workflows load context** - voice-identity.md + language-specific guide
3. **Agents reference files** - No embedded style in agents
4. **Single source of truth** - All style rules live in context files
