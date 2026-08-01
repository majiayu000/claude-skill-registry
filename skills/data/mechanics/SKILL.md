---
name: mechanics
description: The SudoSkill mechanic allows you to force the targeted entity to “cast”
---

Mechanic: SudoSkill
===================

The SudoSkill mechanic allows you to force the targeted entity to “cast”
a MythicMobs meta skill, no mechanics can be used straight, they have to
be in a skill yaml.
This skill will inherit the previous targets in the stack from a
previous parent skill, and is even able to force players to use
MythicMobs skills:

    - SudoSkill{s=SkillName;setcasterastrigger=true/false(default)}

If *setcasterastrigger is true*, the trigger of the skill will be set to
the caster of the sudoskill. Else the trigger is the caster of the
skill.

Example
-------

Skill.yml:

    sudo:
      Skills:
      - arrowvolley{a=20;s=25;v=10;f=50;rd=200} @EIR{r=30}
      - message{msg="Triggername: <trigger.name>"} @world

Mob.yml:

    SudoMonkey:
      Type: villager
      Display: 'a Villager'
      Skills:
      - sudoskill{s=sudo;cat=true} @trigger ~onDamaged
