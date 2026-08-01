---
name: cancelskill-md
description: Skill from iceBear67/mythicmobswiki
---

## Description
Cancels the execution of the [Metaskill][] when triggered


## Attributes
> *This mechanic has no attributes*


## Examples
```yml
SomeSkill:
  Skills:
  - message{m="Hello"} @server
  - cancelSkill ?isMonster #cancels the rest of the skill from executing if the condition is met
  - message{m="It appears i am not a monster! Yay!"} @server
```


## Aliases
- [x] cancel
- [x] return


  [Metaskill]: /Skills/Metaskills


<!--TAGS-->
<!--tag:Meta:Flow-->
