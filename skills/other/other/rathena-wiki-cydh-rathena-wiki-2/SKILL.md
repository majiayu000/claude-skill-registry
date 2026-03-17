---
title: Itemskill
permalink: /Itemskill/
---

Syntax
------

-   **itemskill** <skill id>, <skill level>;
-   **itemskill** &lt;"skill name"&gt;, <skill level>;

Description
-----------

This command meant for item scripts to replicate single-use skills in usable items. It will not work properly, if there is a visible dialog window or menu. If the skill is self or auto-targeting, it will be used immediately otherwise a target cursor is shown.

Examples
--------

`605,Anodyne,Anodyne,11,2000,0,100,,,,,10477567,2,,,,,{ itemskill 8,1; },{}`

When Anodyne is used, it will cast Endure (8), Level 1, as if the actual skill has been used from skill tree.

[Category:Script Command](/Category:Script_Command "wikilink")