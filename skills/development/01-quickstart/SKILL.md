---
name: 01-quickstart
description: import TabItem from "@theme/TabItem";
---

import TabItem from "@theme/TabItem";
import Tabs from "@theme/Tabs";
import DeveloperSupport from "../../../partial/_developer_support.mdx";
import CopyPageButton from "@site/src/components/CopyPageButton";

# Build Your First Skill

<CopyPageButton />

To develop an AI Agent Skill, you will be using the [Senpi Eliza Skills Framework](https://github.com/Senpi-ai/senpi-agent-skills) as the base for your development.

In this tutorial, you will learn how to create your first Senpi Skill for your AI Agent using the [Senpi Eliza Skills Framework](https://github.com/Senpi-ai/senpi-agent-skills).

The AI Agent Skill demonstrated here will have 2 `actions` defined for individual functionalities:

- `ETH_BALANCE_ON_BASE`: Check the balance of the agent's wallet on Base
- `TRANSFER_BASE_ETH`: Transfer ETH token on Base from user's agent wallet to another 0x address

These examples are relatively simple, but will give you a good understanding on the ins-and-outs of building an AI Agent Skill using the Senpi Eliza Skills Framework.

## Pre-requisites

AI Agent Skills are essentially custom Eliza plugins that you can build to enhance your AI Agents.

Before you begin development, please ensure you have all the prerequisites for the Eliza Framework:

- Node.js 23+
- pnpm 9+
- Git for version control
- A code editor (VS Code or VSCodium recommended)
- CUDA Toolkit (optional, for GPU acceleration)
- OpenAI API Key (for OpenAI models)

## Setup Your Environment

Once your have all the prerequisites, fork [**the Senpi Eliza Skills Framework repository**](https://github.com/Senpi-ai/senpi-agent-skills?tab=readme-ov-file#register-your-skills-to-senpi) and then clone it locally to your machine.

Once you cloned the repository, you can setup your environment with the following scripts:

```sh
cd senpi-agent-skills
cp .env.example .env
pnpm i --no-frozen-lockfile && pnpm build
```

In the newly created `.env` file, you can add the following environment variables for this tutorial:

```
OPENAI_API_KEY=      # OpenAI API key
PRIVATE_KEY=         # Private key for executing tx with Senpi Agent Lib, simulating agent wallet
RPC_URL=             # RPC URL for executing tx with Senpi Agent Lib
```

Feel fee to provide other relevant API keys if you are using other AI models for your agent.

## Step 1: Define a New Plugin

First, create a separate branch in your forked repository:

```sh
git checkout -b <new-branch>
```

Then, create a new skill by running the following command:

```sh
pnpm create:skills plugin-first-skill
```

Once the skill is created, a new folder `packages/plugin-first-skill` will be created. Then, open the `packages/plugin-first-skill/src/index.ts` file to define your plugin instance:

```ts title="packages/plugin-first-skill/src/index.ts"
// all import statements no changes

const samplePlugin: Plugin = {
  name: "my-first-senpi-skill",
  description:
    "This plugin is invoked when the user is asking for the current state of the Senpi protocol.",
  actions: [],
  providers: [],
  evaluators: [],
  services: [],
  clients: [],
};

export default samplePlugin;
```

## Step 2: Create New Action For The Agent

After defining your plugin, you will create a new Eliza provider and a new action to give your agent the ability to handle protocol-specific data.

Eliza action is a core components of the Eliza framework that help modularize and extend the functionality of your AI Agent.

An action defines how the agent responds to user inputs.

First, define an action that tells your agent how to respond when a user requests Senpi protocol information. To achieve this, you will need to fill out the following fields:

```ts
interface Action {
  // Unique identifier for the action
  name: string;
  // Array of alternative names/variations
  similes: string[];
  // Detailed explanation of the action's purpose
  description: string;
  // Function that checks if action is appropriate
  examples: ActionExample[][];
  // Demonstrates proper usage patterns
  handler: Handler;
  // Determines if the action can be executed
  validate: Validator;
  // When true, suppresses the initial response message before processing the action.
  // Useful for actions that generate their own responses (like image generation)
  suppressInitialMessage?: boolean;
}
```

Create a new file in the `src/actions` directory, and define the new action with your chosen `name`, `similes`, and `description`:

```ts title="packages/plugin-first-skill/src/actions/balanceAction.ts"
import type {
  Action,
  HandlerCallback,
  IAgentRuntime,
  Memory,
  State,
} from "@moxie-protocol/core";

const balanceAction: Action = {
  name: "ETH_BALANCE_ON_BASE",
  similes: [
    "CHECK_ETH_BALANCE_ON_BASE",
    "GET_ETH_BALANCE_ON_BASE",
    "VIEW_ETH_BALANCE_ON_BASE",
    "SHOW_ETH_BALANCE_ON_BASE",
    "WALLET_ETH_BALANCE_ON_BASE",
    "BASE_ETH_BALANCE_ON_BASE",
  ],
  description: "Check the balance of your agent wallet on Base",
  suppressInitialMessage: true,
} as Action;

export default balanceAction;
```

These metadata guide the AI Agent in selecting the appropriate action when a user sends prompts, so be sure to provide a clear and informative `name`, `similes`, and `description`.

If you would like to add any gating logic, then you can add additional if-else statements to the `validate` field where `false` is returned if the requests is invalid.

After that, define the `handler` field to retrieve the ETH balance of the agent's wallet and return this information to the user.

The `handler` field full code should look as following:

```ts title="packages/plugin-first-skill/src/actions/balanceAction.ts" {14}
import type {
  Action,
  HandlerCallback,
  IAgentRuntime,
  Memory,
  State,
} from "@moxie-protocol/core";
import { SenpiWalletClient } from "@moxie-protocol/moxie-agent-lib/src/wallet";
import { formatEther, http, createPublicClient } from "viem";
import { base } from "viem/chains";

const balanceAction: Action = {
  // ... same as above
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state?: State,
    options?: { [key: string]: unknown },
    callback?: HandlerCallback
  ) => {
    try {
      const publicClient = createPublicClient({
        chain: base,
        transport: http(),
      });
      // Get the agent's wallet instance from state
      const { address } = state.agentWallet as SenpiWalletClient;
      // Get the ETH balance of the agent's wallet
      const balance = await publicClient.getBalance({
        address: address as `0x${string}`,
      });
      const balanceAsEther = formatEther(balance);
      await callback?.({
        text: `The balance of your agent wallet is ${balanceAsEther} ETH.`,
      });
    } catch (error) {
      callback?.({
        text: `Sorry, there was an error fetching your agent wallet ETH balancedata: ${
          error instanceof Error ? error.message : "Unknown error"
        }`,
      });
      return false;
    }
  },
} as Action;

export default balanceAction;
```

Lastly, add an `examples` field to your action. By providing a range of prompts, the agent can learn different question patterns and how to respond appropriately:

```ts title="packages/plugin-first-skill/src/actions/balanceAction.ts" {11}
import type {
  Action,
  HandlerCallback,
  IAgentRuntime,
  Memory,
  State,
} from "@moxie-protocol/core";

const balanceAction: Action = {
  // ... same as above
  examples: [
    [
      {
        user: "{{user1}}",
        content: {
          text: "what is my current ETH balance on Base?",
        },
      },
      {
        user: "{{user2}}",
        content: {
          text: "The balance of your agent wallet is 0.01 ETH",
          action: "TOKEN_BALANCE_ON_BASE",
        },
      },
    ],
  ],
} as Action;

export default balanceAction;
```

Finally, integrate the provider and action above into your plugin by importing it and adding it to the actions array:

```ts title="packages/plugin-first-skill/src/index.ts" {8,9}
import { Action } from "@moxie-protocol/core";
import balanceAction from "../actions/balanceAction";

const samplePlugin: Plugin = {
  name: "my-first-creator-agent-skill",
  description: "My First Senpi Skill",
  actions: [balanceAction],
  providers: [],
  evaluators: [],
  services: [],
  clients: [],
};

export default samplePlugin;
```

and compile a build for your updated Skill by running:

```sh
pnpm build
```

Beyond adding actions, you can further tailor your Senpi Skill by incorporating custom providers, evaluators, or services to build more complex features for your AI Agent Skill.

## Step 3: Test Your Plugin With The Agent

To test your plugin, start the Senpi Eliza Skills Framework locally by running:

<Tabs>
    <TabItem value="npm" label="npm">

```bash
npm run start
```

    </TabItem>
    <TabItem value="yarn" label="yarn">

```bash
yarn start
```

    </TabItem>
    <TabItem value="pnpm" label="pnpm">

```bash
pnpm start
```

    </TabItem>
    <TabItem value="bun" label="bun">

```bash
bun start
```

    </TabItem>

</Tabs>

With the agent running, you can then start a client with a chat interface in a different terminal tab to test interactions with your AI Agent:

<Tabs>
    <TabItem value="npm" label="npm">

```bash
npm run start:client
```

    </TabItem>
    <TabItem value="yarn" label="yarn">

```bash
yarn start:client
```

    </TabItem>
    <TabItem value="pnpm" label="pnpm">

```bash
pnpm start:client
```

    </TabItem>
    <TabItem value="bun" label="bun">

```bash
bun start:client
```

    </TabItem>

</Tabs>

Try out various of the following prompts to test your newly created AI Agent Skills yourself:

- What is my current ETH balance on Base?
- How much ETH is in my agent wallet?
- Check my ETH balance on Base
- etc.

Congratulations! 🥳🎉 You have successfully created your first Senpi Skill for your AI Agent.

Next, you can proceed to [connect your skills to Senpi](./02-connect-skills-to-senpi.mdx) and offer your skills in the Senpi AI Agent ecosystem.

## More Resources

For adding more advanced features to your AI Agent, you can refer to the following resources to further develop your AI Agent Skills:

- [Eliza Developer Docs](https://eliza.how/docs/intro)
- [Eliza Architecture and Concepts](https://eliza.how/docs)

<DeveloperSupport />
