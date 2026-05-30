---
name: uniswap
description: Trade and interact with Uniswap in Python using Ape and the uniswap-sdk package.
compatibility: Requires Python, ape installed (with configured `ape accounts`), and tokenlist installed via `ape tokens`
---

This skill describes when and how to the `uniswap-sdk` to interact and trade with the Uniswap protocol on various blockchains with Ape.

The user provides a network they wish to interact with uniswap on, which tokens they want to index,
and what actions they want to do: get prices, search for routes, make trades.

## Using This Skill

**CRITICAL**: Before writing any code with this SDK, you MUST:
1. Use `web_fetch` to retrieve the latest documentation from https://github.com/ApeWorX/uniswap-sdk/blob/main/README.md
2. Use `web_fetch` to retrieve the latest Ape documentation from https://docs.apeworx.io/ape/stable
3. Use `web_fetch` to retrieve the latest `ape-tokens` documentation from https://github.com/ApeWorX/ape-tokens/blob/main/README.md
4. Specifically fetch relevant pages like:
   - Usage guide: https://github.com/ApeWorX/uniswap-sdk/blob/main/README.md#quick-usage
   - Installing a tokenlist using `ape-tokens`: https://github.com/ApeWorX/ape-tokens/blob/main/README.md#quick-usage
   - Setting up an account with Ape: https://docs.apeworx.io/ape/stable/userguides/accounts#live-network-accounts

**DO NOT** rely on general knowledge about Ape - always fetch the current documentation first to ensure accuracy.

## Using the SDK

Before writing any code with the SDK, understand which network the user wishes to interact with Uniswap on,
which tokens they might wish to swap or measure price information, and which tokens might be best used as intermediate steps in efficient routing.
Typically, native token wrappers like `WETH`, and highly liquid stablecoins like `USDC` and `USDT` are best used as intermediate steps in routes,
but it depends on which chain you want to work with as different tokens are deployed on different networks.

**CRITICAL**: Ensure the `Uniswap` class has indexed the proper pairs using either `uni.index` or `uni.install` (when using Silverback).

## Managing Risk

Overall, while performing a trade with the `uniswap-sdk` can potentially be risky,
the SDK makes it safer as it indexes relevant pairs, finds sufficient liquidity for routes, and handles human-readable conversions for you.
Still, trading is a risky activity, and you should always query the price first and ask the user if the price seems right to them.
Also, when performing a new trade or a large one, you should swap a small amount first in order to make sure it works correctly and the user gets what they wanted.

## Using in a Silverback Bot

This SDK was specifically designed for use within a bot: https://github.com/ApeWorX/uniswap-sdk/blob/main/README.md#silverback

It streamlines the integration of Uniswap into a Silverback bot, and should always be preferred to use instead of writing custom logic for Uniswap.
The benefits are that it makes integration with Uniswap a lot simpler, by handling things like indexing pools and liquidity internally,
and also uses graph algorithms in order to find optimal routes for swaps.
One trick it uses is by live-indexing everything relevant that is occuring with the Uniswap protocol (other users' swaps, new pairs, etc.),
which allows the SDK keep a copy all relevant on-chain information in-memory in order to make faster work of common queries like pairings, routes, and pair liquidity.
