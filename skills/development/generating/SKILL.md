---
name: generating
description: '!INCLUDE "./game-data/skill-create-scriptable-object.md"'
---

# How to create Attack Skill

!INCLUDE "./game-data/_skill-create-scriptable-object.md"

There are following configs

!INCLUDE "./game-data/_game-data-generic-config.md"

Then we're going to create `Buff Skill` so set `Skill Type` to `Active` and also set `Skill Attack Type` to `Normal` or `Based On Weapon` because it will attack other characters when use this skill.

![](../images/skills/003-3.png)

There are following configs for `Attack Skill`

!INCLUDE "./game-data/_skill-generic-config.md"

## Attack Configs

- `Skill Attack Type` how skill applies damages to enemies.
- `Damage Info` contains info about how skill applies damage to other characters ([See more](pages/018-damage-info ':target=__blank')). This will be in-use with `Normal` skill attack type only. If skill attack type is `Based On Weapon` it will use weapon's damage info.
- `Damage Amount` base damage amounts for this skill. This will be in-use with `Normal` skill attack type only. If skill attack type is `Based On Weapon` it will use weapon's damage amounts as base damage amounts.
- `Effectiveness Attributes` skill can increase more damage based on these attributes ([See more](pages/104-character-stats-and-relates-data?id=attribute ':target=__blank'))
- `Weapon Damage Inflictions` damage inflictions based on weapon damage amount.
- `Additional Damage Amounts` damage amounts that will be increasing while attacking target.
- `Increase Damage Amounts With Buffs` if this is `TRUE` applied buff damages will be included to skill attack damages.
- `Is Debuff` if this is `TRUE` an enemies will receive debuff.
- `Debuff` debuff which will applies to an enemies.

* * *

That's an configs for `Attack Skill`

!INCLUDE "./game-data/_game-data-put-to-database.md"