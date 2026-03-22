---
name: contract-development
description: Compile, deploy, simulate, and verify Solidity smart contracts with OpenZeppelin support.
metadata:
  tags: solidity, contract, deploy, compile, verify, etherscan, openzeppelin
---

## When to use

Use this skill when you are:
- Compiling Solidity source code (with or without OpenZeppelin imports)
- Deploying contracts to any supported EVM chain
- Verifying deployed contracts on Etherscan
- Simulating contract deployments on Gorlami forks before going live

## How to use

- [rules/compilation.md](rules/compilation.md) - Compiling Solidity with OZ import support
- [rules/deployment.md](rules/deployment.md) - Full deploy flow (MCP tool + script patterns)
- [rules/interactions.md](rules/interactions.md) - Read/write deployed contracts via MCP tools
- [rules/openzeppelin-v5.md](rules/openzeppelin-v5.md) - OZ v5+ import paths + Ownable patterns
- [rules/templates.md](rules/templates.md) - Copy/paste Solidity templates (OZ v5-compatible)
- [rules/verification.md](rules/verification.md) - Etherscan V2 standard-json-input verification
- [rules/simulation.md](rules/simulation.md) - Test deploys on Gorlami forks first
- [rules/gotchas.md](rules/gotchas.md) - Common pitfalls and requirements
