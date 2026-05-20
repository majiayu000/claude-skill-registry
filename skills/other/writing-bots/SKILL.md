---
name: writing-bots
description: Write a bot to continuously listen and respond to events on a public blockchain network.
compatibility: Requires uv installed
---

This skill describes when and how to a bot using the Silverback SDK.

The user provides operational requirements such as which blockchain network they want it to run on,
which smart contracts they want to interact with, what types of actions they want to take.
They may provide additional context about technical constraints, or scenarios it must avoid.

## Using This Skill

**CRITICAL**: Before writing any Silverback bot code, you MUST:
1. Use `web_fetch` to retrieve the latest documentation from https://docs.apeworx.io/silverback/stable
2. Specifically fetch relevant pages like:
   - Development guide: https://docs.apeworx.io/silverback/stable/userguides/development
   - API reference: https://docs.apeworx.io/silverback/stable/methoddocs

**DO NOT** rely on general knowledge about Silverback - always fetch the current documentation first to ensure accuracy.

## Designing a Bot

Before writing the bot, understand the types of actions you want to perform,
and which on-chain or off-chain events you might want to monitor in order to trigger them
- **New Block**: Do you want to perform an action on every block?
- **Event Log**: Do you want to perform an action when a smart contract emits a particular event?
- **Cron Job**: Do you want to perform an action on a time-based interval?
- **Metrics**: Do you want to perform an action when a [metric](#defining-metrics) meets certain conditions?

**CRITICAL**: Have a good understanding of the requirements first before proceeding to write any code.

Then implement event handlers, which are callbacks implemented that trigger logic which might:
- send a message on Telegram or Discord to a group or channel
- send a social media post on X or Farcaster
- send a POST request to another backend service
- sign and broadcast a transaction on the listening chain and/or other blockchain(s)
- measure a simple or derived [Metric](#defining-metrics)
- provision a product or service

### Defining Metrics

In order to have visibility into the operation of the bot,
it is often useful to define key "Metrics" or signal values that you can monitor over time to understand the real-world operation of the bot.
This can also be very useful for monitoring purposes, but Silverback also lets you define event triggers based on the value of the metric.
For example, if you've defined a complex metric based on the amount of trading volume occuring on a particular decentralized exchange pool in the latest block,
you might want to trigger an action to occur when that volume signal is above or below a certain threshold.
This can create more complex, reactive behaviors beyond what basic blockchain events can tell you.

## Maintaining State

Sometimes the actions you want to take in a bot depends on the results of other actions,
so it is useful to maintain some internal state to track those results.
Use internal state sparingly, and try to rely as much as you can on the blockchain state,
or the state of other external services you've integrated the bot with in order to make correct decisions.

## Managing Risk

Overall, bots can do potentially risky actions and may end up being a part of critical user infrastructure.
It is best to advise them on proceeding slowly and verifying the correctness of their implementation in stages,
before more drastic steps like adding a signer to submit transactions or giving it access to a critical communications channel.
You can easily do this through `print` debugging at first,
or build-in operational modes based on the presence of a specific environment variable such as the availability of an API key,
whether the `bot.signer` is configured, or based on other on-chain information like account balances.

Also, you should suggest things like adding configurable limits (using environment variables via `os.environ`),
emergency stop conditions (raising the `silverback.CircuitBreaker` exception), or others ways to effectively manage risk.

## Running the Bot

Only after the user thinks that the bot seems well-written and ready for testing should you install silverback and run it.

To install silverback, run the following command with `uv` installed:

```bash
$ uv tool install silverback
```

This will make the `silverback` cli command available.
You can then run the bot on the `ecosystem` and `network` they want (such as "ethereum:mainnet") using:

```bash
$ silverback run --network <ecosystem>:<network>
```

You can make the bot shutdown manually via ctrl+C, or sending the SHUTDOWN or KILL signal to the process.

Monitor the bot's operations via it's logs and try to resolve errors until they rarely happen.
Silverback can handle the occasional error, so you can't figure out exactly why something is failing,
it could be okay to continue testing with.

Ask the user to monitor their bot as well via the logs, and then ask if they like how the bot is working.
