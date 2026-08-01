---
name: 01-quickstart-senpi-ai-docs
description: import Tabs from "@theme/Tabs";
---

import Tabs from "@theme/Tabs";
import TabItem from "@theme/TabItem";
import DeveloperSupport from "../../../partial/_developer_support.mdx";
import CopyPageButton from "@site/src/components/CopyPageButton";

# Execute Transactions In Skill

<CopyPageButton />

This guide will walk you through each step to execute transactions in your Skill.

For this guide, we'll be creating a new action named `transferAction` that will transfer ETH on Base from the user's agent wallet to another wallet requested by the user.

## Step 1: Create A New Action

First, create a new file named `transferAction.ts` in the `actions` folder. This file will contain an empty `Action` that named `transferAction` will similar structure as the `balanceAction`:

```ts title="packages/plugin-first-skill/src/actions/transferAction.ts"
import {
  type Action,
  type IAgentRuntime,
  type Memory,
  type HandlerCallback,
  type State,
  elizaLogger,
  type ActionExample,
  composeContext,
  generateObject,
  ModelClass,
} from "@moxie-protocol/core";
import { MoxieWalletClient } from "@moxie-protocol/moxie-agent-lib";

export const transferAction: Action = {
  name: "TRANSFER_BASE_ETH",
  similes: [
    "TRANSFER_ETH_ON_BASE",
    "TRANSFER_NATIVE_ETH_ON_BASE",
    "TRANSFER_BASE_TOKEN",
  ],
  description: "Transfer ETH token on Base from one wallet to another",
  suppressInitialMessage: true,
  validate: async () => true,
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    _options: { [key: string]: unknown },
    callback: HandlerCallback
  ) => {},
  examples: [] as ActionExample[][],
};
```

Before continuing to implement the transaction execution logic, let's add an `examples` field to help the agent to learn various question patterns:

```ts title="packages/plugin-first-skill/src/actions/transferAction.ts" {4}
// same as above

export const transferAction: Action = {
  examples: [
    [
      {
        user: "{{user1}}",
        content: {
          text: "Send 0.01 ETH to 0x114B242D931B47D5cDcEe7AF065856f70ee278C4",
        },
      },
      {
        user: "{{user2}}",
        content: {
          text: "Transfer completed successfully! Transaction hash: 0xdde850f9257365fffffc11324726ebdcf5b90b01c6eec9b3e7ab3e81fde6f14b",
          action: "TRANSFER_BASE_ETH",
        },
      },
    ],
  ] as ActionExample[][],
};
```

## Step 2: Execute Transactions

Once the basic action structure is set up, you can proceed to implement the transaction execution logic.

First, let's add some validation logic to ensure that the user's request is valid.

In order to do this, we'll utilize the LLM to extract the necessary information from the user's request, that is the `receiver` address and the `amount` to transfer:

```ts title="packages/plugin-first-skill/src/actions/transferAction.ts"
import { transferEthTemplate } from "../templates";
import { TransferEthSchema } from "../types";

export const transferAction: Action = {
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    _options: { [key: string]: unknown },
    callback: HandlerCallback
  ) => {
    try {
      elizaLogger.log("Starting TRANSFER_BASE_ETH handler...");

      // Initialize or update state
      if (!state) {
        state = (await runtime.composeState(message)) as State;
      } else {
        state = await runtime.updateRecentMessageState(state);
      }

      const context = composeContext({
        state,
        template: transferEthTemplate,
      });

      const transferDetails = await generateObject({
        runtime,
        context,
        modelClass: ModelClass.SMALL,
        schema: TransferEthSchema,
      });
    } catch (error) {
      elizaLogger.error("Error transfering Base ETH:", error);
      callback({
        text: "Failed to transfer Base ETH. Please check the logs.",
      });
    }
  },
};
```

where `transferEthTemplate` is a LLM prompt template to extract the `receiver` address and the `amount` to transfer from the user's request:

```ts title="packages/plugin-first-skill/src/templates.ts"
export const transferEthTemplate = `
Extract the following details to transfer ETH on Base:
- **amount** (Number): The amount of ETH on Base to transfer in wei.
- **toAddress** (String): The address to transfer the ETH to on Base. A valid Ethereum address following regex format: ^0x[a-fA-F0-9]{40}$

Provide the values in the following JSON format:

\`\`\`json
{
    "amount": number,
    "toAddress": string,
}
\`\`\`

Here are example messages and their corresponding responses:

**Message 1**

\`\`\`
Send 0.01 ETH to 0x114B242D931B47D5cDcEe7AF065856f70ee278C4
\`\`\`

**Response 1**

\`\`\`json
{
    "amount": 0.01,
    "toAddress": "0x114B242D931B47D5cDcEe7AF065856f70ee278C4",
}
\`\`\`

Here are the recent user messages for context:
{{recentMessages}}
`;
```

and `TransferEthSchema` is a JSON schema to validate the extracted `receiver` address and the `amount` to transfer:

```ts title="packages/plugin-first-skill/src/types.ts"
import { z } from "zod";

export const TransferEthSchema = z.object({
  amount: z.number().min(0),
  toAddress: z.string(),
});
```

Once implemented, `transferDetails` will contain the extracted `receiver` address and the `amount` to transfer, which we can validation logic to check if the extracted values are valid by adding the lines below:

```ts title="packages/plugin-first-skill/src/actions/transferAction.ts"
export const transferAction: Action = {
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    _options: { [key: string]: unknown },
    callback: HandlerCallback
  ) => {
    try {
      // same as above

      const { toAddress, amount: value } = transferDetails.object as {
        toAddress: string;
        amount: number;
      };

      // Validate amount is defined and greater than 0
      if (!value || value <= 0) {
        callback({ text: "Transfer amount must be greater than 0" });
        return true;
      }

      // Validate ethereum address format
      const ethAddressRegex = /^0x[a-fA-F0-9]{40}$/;
      if (!ethAddressRegex.test(toAddress)) {
        callback({ text: "Invalid Ethereum address format" });
        return true;
      }
    } catch (error) {
      elizaLogger.error("Error transfering Base ETH:", error);
      callback({
        text: "Failed to transfer Base ETH. Please check the logs.",
      });
    }
  },
};
```

If all the validation checks pass, we can proceed to execute the transaction by adding the lines below:

```ts title="packages/plugin-first-skill/src/actions/transferAction.ts" {17,20}
export const transferAction: Action = {
  handler: async (
    runtime: IAgentRuntime,
    message: Memory,
    state: State,
    _options: { [key: string]: unknown },
    callback: HandlerCallback
  ) => {
    try {
      // same as above

      const formattedValue = value * 1e18;

      elizaLogger.log(
        `Transfering ${formattedValue} wei to address ${toAddress}...`
      );
      // Get the agent's wallet instance from state
      const wallet = state.agentWallet as MoxieWalletClient;

      // Execute transaction on the agent's wallet
      const { hash } = await wallet.sendTransaction("8543", {
        toAddress,
        value: formattedValue,
      });

      elizaLogger.success(
        `Transfer completed successfully! Transaction hash: ${hash}`
      );
      await callback?.(
        {
          text: `Transfer completed successfully! Transaction hash: ${hash}`,
        },
        []
      );
      return true;
    } catch (error) {
      elizaLogger.error("Error transfering Base ETH:", error);
      callback({
        text: "Failed to transfer Base ETH. Please check the logs.",
      });
    }
  },
};
```

The execution of the transaction is done by calling the `sendTransaction` method on the agent's wallet instance that is injected from the runtime's state.

## Step 3: Add The Action To Your Skill

Lastly, add the `transferAction` to your skill:

```ts title="packages/plugin-first-skill/src/index.ts" {9}
import { Action } from "@moxie-protocol/core";
import balanceAction from "../actions/balanceAction";
import balanceProvider from "../providers/balanceProvider";
import transferAction from "../actions/transferAction";

const samplePlugin: Plugin = {
  name: "my-first-creator-agent-skill",
  description: "My First Senpi Skill",
  actions: [balanceAction, transferAction],
  providers: [balanceProvider],
  evaluators: [],
  services: [],
  clients: [],
};

export default samplePlugin;
```

For testing, simply re-build your skill:

<Tabs>
    <TabItem value="npm" label="npm">

```bash
npm run build
```

    </TabItem>
    <TabItem value="yarn" label="yarn">

```bash
yarn build
```

    </TabItem>
    <TabItem value="pnpm" label="pnpm">

```bash
pnpm build
```

    </TabItem>
    <TabItem value="bun" label="bun">

```bash
bun build
```

    </TabItem>

</Tabs>

and run the agent with the following command:

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

You should be able to test the `transferAction` by asking the agent in the client Frontend app to transfer ETH to a specific address by using the following few prompts :

- Send 0.01 ETH to 0x114B242D931B47D5cDcEe7AF065856f70ee278C4
- Move 0.05 ETH to 0x114B242D931B47D5cDcEe7AF065856f70ee278C4
- Pay 0.001 ETH to 0x114B242D931B47D5cDcEe7AF065856f70ee278C4
- etc.

And once you're done with the changes, you can add this new action to `skills.json` file and re-submit you Skill again for review on your changes.

Congratulations! 🥳🎉 You've successfully added a new action to your skill and executed a transaction in your skill.

<DeveloperSupport />
