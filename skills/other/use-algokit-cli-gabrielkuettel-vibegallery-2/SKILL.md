---
name: use-algokit-cli
description: AlgoKit CLI commands for building, testing, and deploying Algorand applications. Use when building or compiling smart contracts, running test suites, deploying to localnet, managing local Algorand network, or understanding the development workflow. Strong triggers include "build the contract", "run the tests", "start localnet", "deploy to localnet", "algokit project run", "localnet status".
---

# AlgoKit Commands

Standard commands for Algorand development with AlgoKit CLI.

## Overview / Core Workflow

1. Write contract code
2. Build: `algokit project run build`
3. Write tests using generated clients
4. Test: `algokit project run test`
5. Deploy: `algokit project deploy localnet`

## How to proceed

1. **Build contracts:**
   ```bash
   algokit project run build
   ```
   This compiles contracts via Puya, generates ARC56 specs, and creates typed clients.

2. **Run tests:**
   ```bash
   algokit project run test
   ```
   Executes the test suite using Vitest.

3. **Start localnet (if needed):**
   ```bash
   algokit localnet start
   ```

4. **Deploy to localnet:**
   ```bash
   algokit project deploy localnet
   ```

5. **Check build artifacts:**
   - `artifacts/` — Compiled contracts, ARC56 specs
   - Generated client files for TypeScript/Python

## Important Rules / Guidelines

- **Always build before testing** — Tests use generated clients
- **Only deploy when explicitly requested** — Don't auto-deploy
- **Check localnet status** before deployment operations
- **Reset localnet** if you need a clean state

## Common Variations / Edge Cases

| Scenario | Command |
|----------|---------|
| Start local network | `algokit localnet start` |
| Stop local network | `algokit localnet stop` |
| Reset network state | `algokit localnet reset` |
| Check network status | `algokit localnet status` |
| Build fails | Check Puya compiler errors, fix contract code |
| Tests fail | Check test assertions, fix contract or test code |

## References / Further Reading

- [Full CLI Reference](./references/REFERENCE.md)
- [AlgoKit CLI Documentation](https://dev.algorand.co/algokit/cli/)
- [AlgoKit Project Commands](https://dev.algorand.co/reference/algokit-cli/#project)
