---
title: Areamobuseskill
permalink: /Areamobuseskill/
---

Syntax
------

-   **areamobuseskill** "<map name>",<x>,<y>,<range>,<mob id>,<skill id>,<skill level>,<cast time>,<cancelable>,<emotion>,<target type>;
-   **areamobuseskill** "<map name>",<x>,<y>,<range>,<mob id>,"<skill name>",<skill level>,<cast time>,<cancelable>,<emotion>,<target type>;

Description
-----------

This command will make all monsters of the specified mob ID in the specified area use the specified skill. Map name, x, and y define the center of the area which extending <range> cells in each direction (e.g. a range of 3 would create a 7x7 square). The skill can be specified by skill ID or name. <cast time> is in milliseconds (1000 = 1 second), and the rest should be self-explanatory.

<target type> can be:

| Value | Description                                           |
|-------|-------------------------------------------------------|
| 0     | Cast the specified skill to self.                     |
| 1     | Cast the specified skill to the mob's current target. |
| 2     | Cast the specified skill to the mob's master.         |
| 3     | Random target.                                        |

Example
-------

`   // Spawn 1 Shining Plant in the 5x5 area centered on (155,188) `
`   `[`areamonster`](/areamonster "wikilink")` "prontera",153,186,157,190,"Shining Plant",1083,1; `
`   `
`   // Make the plant cast level 10 Cold Bolt on a random target `
`   `**`areamobuseskill`**` "prontera",155,188,2,1083,"MG_COLDBOLT",10,3000,1,e_gg,3; `

[Category:Script_Command](/Category:Script_Command "wikilink")