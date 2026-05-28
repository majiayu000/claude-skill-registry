---
name: SND Plugin References
description: Tracking document for SND plugin skills, repository references, and missing documentation. Use this to find official sources and prioritize skill creation.
---

# SND Plugin Reference Tracker

This skill tracks all known FFXIV Dalamud plugins used with SND macros, their official repositories, and documentation status.

## Documented Skills (Verified)

| Skill | Plugin | Repository | IPC Status | Last Verified |
|-------|--------|------------|------------|---------------|
| snd-artisan | Artisan | [PunishXIV/Artisan](https://github.com/PunishXIV/Artisan) | Full IPC | 2025-12-11 |
| snd-autoretainer | AutoRetainer | [PunishXIV/AutoRetainerAPI](https://github.com/PunishXIV/AutoRetainerAPI) | Full IPC | 2025-12-11 |
| snd-bossmod | BossModReborn | [awgil/ffxiv_bossmod](https://github.com/awgil/ffxiv_bossmod) | Full IPC | 2025-12-11 |
| snd-deliveroo | Deliveroo | [VeraNala/Deliveroo](https://github.com/VeraNala/Deliveroo) (mirror) | Minimal (1 method) | 2025-12-11 |
| snd-glamourer | Glamourer | [Ottermandias/Glamourer](https://github.com/Ottermandias/Glamourer) | Full IPC | 2025-12-11 |
| snd-ice | ICE | [LeontopodiumNivale14/Ices-Cosmic-Exploration](https://github.com/LeontopodiumNivale14/Ices-Cosmic-Exploration) | Full IPC | 2025-12-11 |
| snd-lifestream | Lifestream | [NightmareXIV/Lifestream](https://github.com/NightmareXIV/Lifestream) | Full IPC | 2025-12-11 |
| snd-questionable | Questionable | [pot0to/Questionable](https://github.com/pot0to/Questionable) | Commands only | 2025-12-11 |
| snd-saucy | Saucy | [PunishXIV/Saucy](https://github.com/PunishXIV/Saucy) | Commands only | 2025-12-11 |
| snd-textadvance | TextAdvance | [NightmareXIV/TextAdvance](https://github.com/NightmareXIV/TextAdvance) | Full IPC | 2025-12-11 |
| snd-vnavmesh | vnavmesh | [awgil/ffxiv_navmesh](https://github.com/awgil/ffxiv_navmesh) | Full IPC | 2025-12-11 |
| snd-wrath | WrathCombo | [PunishXIV/WrathCombo](https://github.com/PunishXIV/WrathCombo) | Full IPC | 2025-12-11 |
| snd-yesalready | YesAlready | [PunishXIV/YesAlready](https://github.com/PunishXIV/YesAlready) | Commands only | 2025-12-11 |

## Missing Skills (Need Creation)

These plugins are used in reference scripts but don't have skill documentation yet:

| Priority | Plugin | Repository | IPC Source | Notes |
|----------|--------|------------|------------|-------|
| HIGH | AutoHook | [PunishXIV/AutoHook](https://github.com/PunishXIV/AutoHook) | Needs discovery | Fishing automation - required for FishingRaid |
| HIGH | Pandora | [PunishXIV/PandorasBox](https://github.com/PunishXIV/PandorasBox) | Needs discovery | QoL features - required for FishingRaid |
| HIGH | Visland | [ffxiv-visland/Visland](https://github.com/ffxiv-visland/Visland) | Needs discovery | Island Sanctuary automation |
| MEDIUM | Teleporter | [NightmareXIV/TeleporterPlugin](https://github.com/NightmareXIV/TeleporterPlugin) | Needs discovery | Alternative teleportation |
| MEDIUM | SimpleTweaks | [Caraxi/SimpleTweaksPlugin](https://github.com/Caraxi/SimpleTweaksPlugin) | Needs discovery | Various QoL tweaks |
| LOW | Discard Helper | Unknown | Needs discovery | Inventory discard automation |

## Reference Scripts

Scripts in the `Reference/` folder that document plugin usage:

| Script | Plugins Used | Status |
|--------|--------------|--------|
| FishingRaid_original.lua | AutoHook, Pandora, Visland, AutoRetainer, YesAlready, Teleporter, SimpleTweaks, Discard Helper | Analyzed |

## IPC File Patterns

When searching for IPC in plugin repositories, look for these common patterns:

```
IPC.cs
IPCProvider.cs
API.cs
*Api.cs
External/*IPC*.cs
Services/IPC/*
IPC/IPC*.cs
```

## Repository Organizations

Common GitHub organizations for FFXIV plugins:

| Organization | Plugins |
|--------------|---------|
| [PunishXIV](https://github.com/PunishXIV) | Artisan, AutoRetainer, Saucy, YesAlready, WrathCombo, AutoHook, PandorasBox, Deliveroo |
| [NightmareXIV](https://github.com/NightmareXIV) | Lifestream, TextAdvance, Teleporter |
| [Ottermandias](https://github.com/Ottermandias) | Glamourer, Penumbra |
| [awgil](https://github.com/awgil) | ffxiv_bossmod, ffxiv_navmesh |
| [Caraxi](https://github.com/Caraxi) | SimpleTweaksPlugin |

## Verification Workflow

When verifying or creating a new skill:

1. **Find Repository**: Search GitHub for the plugin name
2. **Locate IPC Files**: Search for patterns above in the repo
3. **Extract APIs**: Read the IPC source and document all public methods
4. **Create/Update Skill**: Write to `.claude/skills/snd-{pluginname}/SKILL.md`
5. **Include Source URL**: Always reference the exact IPC file path
6. **Test Examples**: Include working Lua code examples

## Notes

### Archived/Inaccessible Repos
- **Deliveroo**: Original at `git.carvel.li/liza/Deliveroo` is archived. Use GitHub mirror at VeraNala/Deliveroo
- **Ice**: Was incorrectly listed as `ffxivcode/Ice`. Correct repo is LeontopodiumNivale14/Ices-Cosmic-Exploration

### Plugins Without IPC
Some plugins only expose slash commands, not IPC:
- **Saucy**: Gold Saucer mini-game automation (not fishing!)
- **Questionable**: Quest automation
- **YesAlready**: Dialog auto-confirm

For these, document the slash commands instead.

### Common Mistakes Found
- Fabricated APIs that don't exist in source
- Wrong plugin purposes (e.g., Saucy was documented as "fishing" but it's for Gold Saucer)
- Outdated repository URLs
- Methods documented from old versions that no longer exist

Always verify against the actual source code!
