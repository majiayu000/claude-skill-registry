---
name: randomskill-md
description: Skill from Zyyans/MythicMobs-wiki
---

Mechanic: RandomSkill
=====================

Executes a random skill from the list of supplied
[skills](skills/mechanics/skill). Will ignore any skills that are on
cooldown. There is no limit to how much skills can be added.

Attributes
----------

| Attribute | Aliases | Description                                             | Default |
|-----------|---------|---------------------------------------------------------|---------|
| skills    |         | The list of skills to execute, must be separated by a , |         |



Examples
--------

    Skills:
    - randomskill{skills=skill1,skill2,skill3}

Having problems overviewing your randomskill-syntax? Try this:

    Skills:
    - randomskill{
        skills=
        superskill,
        green_skill,
        skill3,
        grandSkill,
        7331
        }
