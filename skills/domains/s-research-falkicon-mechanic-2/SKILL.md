---
name: s-research
description: >
  Research WoW addon development topics using CLI tools, Blizzard UI source,
  and documentation. Covers API discovery, pattern research, and Ace3 usage.
  Use when investigating unfamiliar APIs, finding Blizzard patterns, or learning.
  Triggers: research, find, search, API, Blizzard UI, documentation, Ace3.
---

# Researching WoW APIs

Expert guidance for discovering and understanding World of Warcraft APIs and patterns.

## Related Commands

- [c-research](../../commands/c-research.md) - API research workflow

## CLI Commands (Use These First)

> **MANDATORY**: Always use CLI commands before manual exploration.

| Task | Command |
|------|---------|
| Search APIs (Offline) | `mech call api.search -i '{"query": "*Spell*"}'` |
| API Info | `mech call api.info -i '{"api_name": "C_Spell.GetSpellInfo"}'` |
| List by Namespace | `mech call api.list -i '{"namespace": "C_Spell"}'` |
| Search Icons | `mech call atlas.search -i '{"query": "sword"}'` |
| API Stats | `mech call api.stats` |

## Capabilities

1. **API Discovery** — Search 5000+ WoW APIs offline using static definitions
2. **Blizzard UI Research** — Find patterns in Blizzard's own Lua source code
3. **Ace3 Patterns** — Guidance on using common addon libraries (AceDB, AceEvent, etc.)
4. **Icon/Atlas Search** — Find UI assets and textures by name

## Routing Logic

| Request type | Load reference |
|--------------|----------------|
| Offline API lookup patterns | [references/api-research.md](references/api-research.md) |
| Blizzard UI source patterns | [references/blizzard-ui.md](references/blizzard-ui.md) |
| Ace3 library patterns | [references/ace3-patterns.md](references/ace3-patterns.md) |
| CLI Reference | [../../docs/cli-reference.md](../../docs/cli-reference.md) |

## Quick Reference

### Search WoW APIs
```bash
mech call api.search -i '{"query": "GetItem*", "namespace": "C_Item"}'
```

### Get Detailed API Info
```bash
mech call api.info -i '{"api_name": "C_Spell.GetSpellInfo"}'
```

### Search Icons
```bash
mech call atlas.search -i '{"query": "sword", "limit": 10}'
```

### Best Practices
- **Search First**: Use `api.search` before guessing API names.
- **Audit Blizzard**: Use ripgrep on local wow-ui-source to see how Blizzard uses an API.
- **Namespace Awareness**: Most modern APIs are in `C_` namespaces (e.g., `C_Timer`, `C_Spell`).
