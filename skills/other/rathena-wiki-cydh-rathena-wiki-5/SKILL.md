---
title: Guildskill
permalink: /Guildskill/
---

Syntax
------

-   **guildskill** <skill id>,<level>;
-   **guildskill** "<skill name>",<level>;

Description
-----------

This command will bump up the specified guild skill by the specified number of levels. This refers to the invoking character and will only work if the invoking character is a member of a guild AND it's guild master, otherwise no failure message will be given and no error will occur, but nothing will happen - same about the guild skill trying to exceed the possible maximum. The full list of guild skills is available in (and RE equivalent), these are all the GD_ skills at the end.

The flag parameter is currently not functional and it's a mystery of what it would actually do. (Though probably, like for character skills, it would allow temporary bumping.) Using this command will bump the guild skill up permanently.

You might want to make a quest for getting a certain guild skill, make it hard enough that all the guild needs to help or something. Doing this for the Glory of the Guild skill, which allows your guild to use an emblem, is a good idea for a fun quest. (Wasting a level point on that is really annoying :D)

Examples
--------

This would give your character's guild one level of Approval (GD_APPROVAL ID 10000). Notice that if you try to add two levels of Approval, or add Approval when the guild already has it, it will only have one level of Approval afterwards.

**`guildskill`**` 10000,1,0;`

[Category:Script_Command](/Category:Script_Command "wikilink")