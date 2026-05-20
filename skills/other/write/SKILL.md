---
name: write
description: "Use when writing technical content: documentation, changelogs, articles, pitches, sprint reviews, and presentation outlines. Handler-based with audience targeting."
effort: high
argument-hint: "docs|changelog|content <type>|--audience developer|manager|executive"
tags: [writing, documentation, changelog, content, communication]
---



# Technical Writing

Router skill for comprehensive technical writing. Dispatches to handler files based on content type. Always: clear structure, audience-appropriate, no fluff.

## When to Use

- Writing or updating documentation (README, API docs, guides).
- Generating changelogs from conventional commits.
- Creating pitch decks, sprint reviews, blog posts, architecture board presentations.
- NOT for code explanations -- use `/ai-explain`.
- NOT for code changes -- use `ai-build agent`.

## Routing

| Sub-command | Handler | Purpose |
|-------------|---------|---------|
| `docs` | `handlers/docs.md` | README, API docs, guides, wiki pages |
| `changelog` | `handlers/changelog.md` | Release notes from conventional commits |
| `content` | `handlers/content.md` | Articles, pitches, presentations, sprint reviews |

Default (no sub-command): `docs`.

## Audience Targeting

| Audience | Tone | Detail Level | Jargon |
|----------|------|-------------|--------|
| `developer` | Technical, precise | Implementation details | Full technical vocabulary |
| `manager` | Results-oriented | Impact and timeline | Minimal, explained when used |
| `executive` | Strategic | Business value and risk | None |

Default: `developer`.

## Quick Reference

```
/ai-write docs                              # documentation (default)
/ai-write changelog                         # release notes from commits
/ai-write content pitch                     # elevator pitch
/ai-write content sprint-review             # sprint review summary
/ai-write content blog                      # blog post
/ai-write content presentation              # presentation outline
/ai-write content architecture-board        # architecture decision for review
/ai-write content solution-intent           # solution intent document
/ai-write docs --audience manager           # manager-targeted docs
```

## Shared Rules

- Write what users can DO, not what you BUILT.
- Active voice. Present tense.
- No "basically", "simply", "just".
- Every section earns its place -- cut anything that does not serve the reader.
- Audience determines vocabulary, not quality.

## Integration

- Composes with `/ai-commit` documentation gate for auto-updates.
- Changelog mode follows Keep a Changelog format.
- Content mode adapts to audience tier.

## References

- `.ai-engineering/manifest.yml` -- governance documentation requirements.
$ARGUMENTS
