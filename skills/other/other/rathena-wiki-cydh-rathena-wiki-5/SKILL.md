---
title: PC Checkskill
permalink: /PC_Checkskill/
---

Check Skill LVL on the character
--------------------------------

`int pc_checkskill(struct map_session_data *sd,int skill_id)`

`pc_checkskill(sd,SKILLID)>X)`

-   sd = Only players have skills (mobs are forced skill uses)
-   SKILLID = Skill ID, can be numeric (28=heal) or the client name (AL_HEAL=heal)
-   X = Skill Level (&gt;0 he only needs 1 point)
-   int = Return the skill level learned by player

Note: This can be used to check if the character has the skill or not (same as &gt;0)

`pc_checkskill(sd,SKILLID)`

[Category:Source_Functions](/Category:Source_Functions "wikilink")