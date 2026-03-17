---
title: Addtoskill
permalink: /Addtoskill/
---

[Category:Script_Command](/Category:Script_Command "wikilink")

Syntax
------

-   [addtoskill](/addtoskill "wikilink") <skill id>,<level>{,<flag>};
-   [skill](/skill "wikilink") <skill id>,<level>{,<flag>};

Description
-----------

These commands will give the invoking character a specified skill. This is also used for item scripts.

Parameters
----------

### Skill ID

Skill ID is the ID number of the skill in question as per . It is not known for certain whether this can be used to give a character a monster's skill, but you're welcome to try with the numbers given in .

### Level

The level at which the skill in question is given. If the flag has been set to 2, this parameter will be interpreted as a a stackable additional bonus to the existing skill level of the skill of the player.

### Flag

The flag parameter is optional, and defaults to 1 in '[skill](/skill "wikilink")' and to 2 in '[addtoskill](/addtoskill "wikilink")'.

`Flag - Description`
**`0`**` - The skill is given permanently.`
**`1`**` - The skill is given temporarily (Will be lost eventually, this is meant for card item`
`scripts usage).`
**`2`**` - The level parameter is to be interpreted as a stackable additional bonus to the skill`
`level. If the character did not have that skill previously, they will now at 0+(the level given).`

Examples
--------

`      //This will permanently give the character Stone Throw (TF_THROWSTONE,152), at level 1,`
`      `[`skill`](/skill "wikilink")` 152,1,0;`