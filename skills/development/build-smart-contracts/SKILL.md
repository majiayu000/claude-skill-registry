---
name: build-smart-contracts
description: Build Algorand smart contracts using Algorand TypeScript (PuyaTs) or Algorand Python (PuyaPy). Use when creating new smart contracts from scratch, adding features or methods to existing contracts, understanding Algorand contract development patterns, or getting guidance on contract architecture. Strong triggers include "create a smart contract", "write a contract that...", "build a voting contract", "implement an NFT contract", "add a method to the contract".
---

# Building Smart Contracts

Create modern Algorand smart contracts in Algorand TypeScript or Algorand Python—statically-typed subsets compiled to TEAL bytecode by the Puya compiler.

## Overview / Core Workflow

1. Search Algorand documentation for concepts and best practices
2. Retrieve canonical examples from priority repositories
3. Generate code adapting examples to requirements
4. Include integration tests using generated clients
5. Build and test with AlgoKit commands

## How to proceed

1. **Search documentation first:**
   - Use `kappa_search_algorand_knowledge_sources` MCP tool for conceptual guidance
   - If MCP unavailable, use web search: "site:dev.algorand.co {concept}"
   - If no results, proceed with caution using known patterns

2. **Retrieve canonical examples:**
   - Priority 1: `algorandfoundation/devportal-code-examples`
   - Priority 2: `algorandfoundation/puya-ts` (examples/)
   - Priority 3: `algorandfoundation/algokit-typescript-template`
   - Always include corresponding test files

3. **Generate code:**
   - Default to TypeScript unless user explicitly requests Python
   - Adapt examples carefully, preserving safety checks
   - Follow syntax rules from `algorand-typescript` skill

4. **Include tests:**
   - Always include or suggest integration tests
   - Use generated clients for testing contracts
   - See `test-smart-contracts` skill for patterns

5. **Build and test:**
   ```bash
   algokit project run build   # Compile contracts
   algokit project run test    # Run tests
   ```

## Important Rules / Guidelines

- **NEVER use PyTEAL or Beaker** — these are legacy, superseded by Puya
- **NEVER write raw TEAL** — always use Algorand TypeScript/Python
- **NEVER import external libraries** into contract code
- **Default to TypeScript** unless user explicitly requests Python
- **Always search docs first** before writing code
- **Always retrieve examples** from priority repositories

## Common Variations / Edge Cases

| Scenario | Approach |
|----------|----------|
| Box storage patterns | Check `devportal-code-examples/contracts/BoxStorage/` |
| Inner transactions | Search for "itxn" patterns in puya-ts examples |
| ARC-4 methods | See `puya-ts/examples/hello_world_arc4/` |
| State management | Check GlobalState, LocalState patterns in examples |
| Python contracts | Use `algorandfoundation/puya` instead of puya-ts |
| Python syntax help | Consult `references/python/` subfolder for Python-specific patterns |

## References / Further Reading

- [Detailed Workflow](./references/REFERENCE.md)
- [Syntax Rules](../algorand-typescript/SKILL.md)
- [Testing Patterns](../test-smart-contracts/SKILL.md)
- [AlgoKit Commands](../use-algokit-cli/SKILL.md)
