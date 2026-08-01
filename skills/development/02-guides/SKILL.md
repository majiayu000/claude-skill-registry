---
name: 02-guides
description: import DeveloperSupport from "../../../partial/developersupport.mdx";
---

import DeveloperSupport from "../../../partial/_developer_support.mdx";
import CopyPageButton from "@site/src/components/CopyPageButton";

# Create A New Skill

<CopyPageButton />

To create a new Skill, you can simply run the following command from the Senpi Eliza Skills Framework:

```sh
pnpm create:skills plugin-<skill-name>
```

By executing this command, it will execute several actions in order:

1. Create a new directory for the skill under the `package/plugin-<skill-name>` directory using a template skill from `packages/_examples/plugin` directory.
2. Add the new `package/plugin-<skill-name>` to both the `characters/moxie.character.json` and the `agent/package.json` file.
3. Register the new skill to `registry/src/skills.json` file.
4. Executing `pnpm i --no-frozen-lockfile` to install the dependencies
5. Executing `pnpm build` to build the project for you

Once the command is executed, you can start making changes to the Skill and add features you want into the Skill.

<DeveloperSupport />
