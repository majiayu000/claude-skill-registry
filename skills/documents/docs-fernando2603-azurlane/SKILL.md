---
name: docs-fernando2603-azurlane
description: '- Overview'
---

# SKILL

- [Overview](#overview)
- [Future Planning](#future-planning)
- [Formula](#formula)
- [Data Structure](#data-structure)
- [Fetch](#fetch)


# Overview
The current structure of `skill.json` is straightforward, containing only maximum leveled skills with the following keys: `type`, `name`, `desc`, `icon`, and `max_level`. You can find the details in the [Data Structure](#data-structure) section. Additionally, `skill_icon.json` is provided for those who are only interested in the icon link.


# Future Planning
There are plans to enhance the `skill.json` structure in the future. While the complete structure is not finalized, the primary focus is on leveled skill descriptions that can be utilized without external dependencies. Currently, the challenge is the fact that `Typescript/Javascript` lacks the ability to use string formatting like `Python` or other programming languages, making deciding the structure more challenging. Although the option of including a fully repeating description is available, it is not considered efficient. Currently, you can use this [formula](#formula) instead to achieve this.

Some features to be implemented in the future include:
- Multi-level skill descriptions
- Skill triggering requirements
- Skill effects (buffs, damage, etc.)

> [!IMPORTANT]
> This is still in the "planning" phase, and its availability in the future is not guaranteed.


# Formula
This formula is for achieving leveled skill descriptions. In this formula, you need the following files from the [AzurLaneTools/AzurLaneData](https://github.com/AzurLaneTools/AzurLaneData/blob/main) repository:
- [skill_data_template.json](https://github.com/AzurLaneTools/AzurLaneData/blob/main/EN/ShareCfg/skill_data_template.json)
- [name_code.json](https://github.com/AzurLaneTools/AzurLaneData/blob/main/EN/ShareCfg/name_code.json)

The first thing we need to do is implement a function to resolve skill name and description that use format like this `{namecode:xx}` and then implement the main function that parse the skill data. Below is the formula example provided in `Typescript` and `Python`.

<details>
  <summary>Typescript</summary>

  ```Typescript
  // ** this is for example purpose, using 'fetch' in every run is not advisable **
  const REPO_LINK = "https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/EN/ShareCfg";
  const skill_data_template = await fetch(`${REPO_LINK}/skill_data_template.json`).then(res => res.json());
  const name_code = await fetch(`${REPO_LINK}/name_code.json`).then(res => res.json());

  function resolve_namecode(text: string): string
  {
    let line: string = text;

    // resolve namecode
    while (line.includes("namecode"))
    {
      for (const key in name_code)
      {
        const CODE_NAME: string = `{namecode:${key}}`;

        if (line.includes(CODE_NAME))
          line = line.replace(CODE_NAME, name_code[key].name);
      };
    };


    // remove irregular whitespace
    if (line.includes(" "))
      line = line.replaceAll(" ", " ");

    // remove </color>
    if (line.includes("</color>"))
      line = line.replaceAll("</color>", "");

    // using regex remove <color=#XXXXXX>
    while (line.includes("<color"))
      line = line.replace(/<color[^>]*>/, "");

    // using regex to replace two or more space into one
    line = line.replace(/\s{2,}/, " ");

    // strip to remove space in the start or end of the string
    return line.trim();
  };

  type Skill = {
    id: number;
    type: number;
    name: string;
    desc: string;
    max_level: number;
  };

  function skill(skill_id: number | string, level: number = 10, upgrade: boolean = false): Skill
  {
    // check if skill_id available in skill_data_template
    if (!skill_data_template.hasOwnProperty(skill_id))
      return null;

    // get needed data from skill_data_template
    const { type, name, desc, desc_add, max_level } = skill_data_template[skill_id];

    let temp_desc: string = desc;
    let temp_level: number = level;

    // check if level is less than max_level and more than 0
    if (level > max_level)
      temp_level = max_level;
    else if (level < 1)
      temp_level = 1;

    // parse skill description
    for (let i = 0; i < desc_add.length; i++)
    {
      // temp_level -1 because list start from 0
      const DESC_CURRENT: string = desc_add[i][temp_level - 1][0];
      let desc_replace: string = DESC_CURRENT; // example: "10%"

      // upgrade make the display like in skill upgrade screen (classroom)
      // it add upgrade increment value for next level
      // check if temp_level is not equal to max_level, since max_level doesn't have desc_upgrade
      if (upgrade && temp_level !== max_level)
        // some skill only have one desc_add length
        // so we implemented it by using next level data for backup if not available
        let desc_upgrade = desc_add[i][temp_level];

        if (desc_add[i][temp_level - 1].length === 2)
          desc_upgrade = desc_add[i][temp_level - 1][1];

        desc_replace += `(${desc_upgrade})`; // example: "10%(+2.5%)"

      // example pattern: $1 $2 $3
      temp_desc = desc.replaceAll(`$${i + 1}`, desc_replace);
    };

    return {
      id: parseInt(skill_id),
      type: type,
      name: resolve_namecode(name),
      desc: resolve_namecode(temp_desc),
      max_level: max_level
    };
  };

  // this function to compare skill lowest level with highest level
  // like you click on ship archive skill that show min~max
  // this doesn't work with skill obtained from limit break like all out assault
  // since all out assault just change the entire skill id instead of level upgrade
  function skill_compare(skill_id: string | number): Skill
  {
    if (!skill_data_template.hasOwnProperty(skill_id))
      return null;

    const { type, name, desc, desc_get_add, max_level } = skill_data_template[skill_id];

    const SKILL = {
      id: parseInt(skill_id),
      type: type,
      name: resolve_namecode(name),
      desc: resolve_namecode(desc),
      max_level: max_level
    };

    // skill only have one level like all out assault or meta operation siren skill
    // that can't be upgraded
    if (max_level === 1)
      return SKILL;

    // parse skill description
    for (let i = 0; i < desc_get_add.length; i++)
    {
      const DESC_CURRENT: string = desc_get_add[i][0];
      const DESC_UPGRADE: string = desc_get_add[i][1];

      SKILL.desc = desc.replaceAll(`$${i + 1}`, `${DESC_CURRENT}(${DESC_UPGRADE})`);
    };

    SKILL.desc = resolve_namecode(SKILL.desc);

    return SKILL;
  };
  ```
</details>

<details>
  <summary>Python</summary>

  ```Python
  # Python
  import re
  import json
  import requests
  from typing import Union, Optional, List
  from dataclasses import dataclass


  # ** this is for example purpose, using 'requests' in every run is not advisable **
  REPO_LINK = 'https://raw.githubusercontent.com/AzurLaneTools/AzurLaneData/main/EN/ShareCfg'
  skill_data_template = requests.get(f'{REPO_LINK}/skill_data_template.json').json()
  name_code = requests.get(f'{REPO_LINK}/name_code.json').json()


  def resolve_namecode(text: str) -> str:
    line: str = text

    # resolve namecode
    while 'namecode' in line:
      for key, value in name_code.items():
        CODE_NAME: str = f'{{namecode:{key}}}'

        if CODE_NAME in line:
          line = line.replace(CODE_NAME, value['name'])

    # remove irregular whitespace
    if ' ' in line:
      line = line.replace(' ', ' ')

    # remove </color>
    if '</color>' in line:
      line = line.replace('</color>', '')

    # using regex remove <color=#XXXXXX>
    while '<color' in line:
      line = re.sub(r'<color[^>]*>', '', line)

    # using regex to replace two or more space into one
    line = re.sub(r'\s{2,}', ' ', line)

    # strip to remove space in the start or end of the string
    return line.strip()


  # create a Skill dataclass for easier to access like javascript and cleaner
  @dataclass
  class Skill:
    id: int
    type: int
    name: str
    desc: str
    max_level: int


  def skill(skill_id: Union[int, str], level: int = 10, upgrade: bool = False) -> Optional[Skill]:
    # make skill_id into int since python dict int and str key is different
    # you can remove the isinstance and directly cast the skill_id into str
    # but i'll prefer this because it's more readable and intuitive
    if not isinstance(skill_id, str):
      skill_id = str(skill_id)

    # check if skill_id available in skill_data_template
    if skill_id not in skill_data_template:
      return None

    # get needed data from skill_data_template
    # unlike javascript, python can't deconstruct object/dict
    # so we will use 'get' since it's more safe with default value than direct access
    # since skill_data_template already checked before it is safe to direct access the data
    skill_data: any = skill_data_template[skill_id]
    skill_type: int = skill_data.get('type') or 0
    skill_name: str = skill_data.get('name') or ''
    skill_desc: str = skill_data.get('desc') or ''
    skill_desc_add: List = skill_data.get('desc_add') or []
    skill_max_level: int = skill_data.get('max_level') or 1

    temp_level: int = int(level)

    # check if level is less than skill_max_level and more than 0
    if level > skill_max_level:
      temp_level: int = skill_max_level
    elif level < 0:
      temp_level: int = 1

    # parse skill_description
    for i, desc in enumerate(skill_desc_get_add, start=1):
      # temp_level -1 because list start from 0
      DESC_CURRENT: str = desc[temp_level - 1][0]
      desc_replace: str = DESC_CURRENT # example: "10%"

      # upgrade make the display like in skill upgrade screen (classroom)
      # it add upgrade increment value for next level
      # check if temp_level is not equal to skill_max_level,
      # since skill_max_level doesn't have desc_upgrade
      if upgrade and temp_level != skill_max_level:
        # some skill only have one desc_add length
        # so we implemented it by using next level data for backup if not available
        desc_upgrade: str = desc[lock_level]

        if len(desc[lock_level - 1]) == 2:
          desc_upgrade = desc[lock_level - 1]

        desc_replace += f'({desc_upgrade})' # example: "10%(+2.5%)"

      # example pattern: $1 $2 $3
      skill_desc = skill_desc.replace(f'${i}', desc_replace);

    return Skill(
      id=int(skill_id),
      type=skill_type,
      name=resolve_namecode(skill_name),
      desc=resolve_namecode(skill_desc),
      max_level=skill_max_level
    )


  # this function to compare skill lowest level with highest level
  # like you click on ship archive skill that show min~max
  # this doesn't work with skill obtained from limit break like all out assault
  # since all out assault just change the entire skill id instead of level upgrade
  def skill_compare(skill_id: Union[str, int]) -> Optional[Skill]:
    if not isinstance(skill_id, str):
      skill_id = str(skill_id)

    if skill_id not in skill_data_template:
      return None

    skill_data: any = skill_data_template[skill_id]
    skill_type: int = skill_data.get('type') or 0
    skill_name: str = skill_data.get('name') or ''
    skill_desc: str = skill_data.get('desc') or ''
    skill_desc_get_add: List = skill_data.get('desc_get_add', [])
    skill_max_level: int = skill_data.get('max_level') or 1

    SKILL = Skill(
      id=int(skill_id),
      type=skill_type,
      name=resolve_namecode(skill_name),
      desc=resolve_namecode(skill_desc),
      max_level=skill_max_level
    )

    # skill only have one level like all out assault or meta operation siren skill
    # that can't be upgraded
    if skill_max_level == 1:
      return SKILL;

    # parse skill description
    for i, desc in enumerate(skill_desc_get_add, start=1):
      DESC_CURRENT: str = desc[0]
      DESC_UPGRADE: str = desc[1]

      skill_desc: str = skill_desc.replace(f'${i}', f'{DESC_CURRENT}({DESC_UPGRADE})')

    SKILL.desc = resolve_namecode(skill_desc)

    return SKILL
  ```
</details>


# Data Structure
```Typescript
type Link = string | null;

enum SkillType {
  OFFENSIVE = 1,
  DEFENSIVE = 2,
  SUPPORT   = 3
};

type Skill = {
  id: number;
  type: SkillType;
  name: string;
  desc: string;
  icon: Link;
  max_level: number;
};

// skill.json
type SkillData = {
  [skill_id: string]: Skill;
};

// skill_icon.json
type SkillIconData = {
  [skill_id: string]: Link;
};
```


# Fetch
- [skill.json](https://raw.githubusercontent.com/Fernando2603/AzurLane/main/skill.json)
```
https://raw.githubusercontent.com/Fernando2603/AzurLane/main/skill.json
```

- [skill_icon.json](https://raw.githubusercontent.com/Fernando2603/AzurLane/main/skill_icon.json)
```
https://raw.githubusercontent.com/Fernando2603/AzurLane/main/skill_icon.json
```