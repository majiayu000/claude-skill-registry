---
name: solidity-development
description: Solidity smart contract development workflow. Use when modifying smart contracts in apps/erc20-token/contracts/.
---

# Solidity Development Workflow

Workflow for Solidity smart contract changes.

## Prerequisites

**Use `git-workflow` Skill** for branch management, commit conventions, and PR creation.

## Applicable Directories

| Path | Description |
|------|-------------|
| `apps/erc20-token/contracts/` | Smart contract source files |
| `contracts/` | ABI files |

## Verification Commands

```bash
cd apps/erc20-token
npm install           # Install dependencies
truffle compile       # Compile contracts
truffle test          # Run tests
npm run lint          # Lint Solidity code
```

## Self-Review Checklist

### Code Quality

- [ ] Follows Solidity best practices
- [ ] Gas optimization considered
- [ ] Proper visibility modifiers
- [ ] Events emitted for state changes

### Security

- [ ] No reentrancy vulnerabilities
- [ ] Integer overflow/underflow protection
- [ ] Access control properly implemented
- [ ] No hardcoded addresses

### Testing

- [ ] Unit tests cover all functions
- [ ] Edge cases tested
- [ ] Gas consumption verified

## ABI Generation

After contract changes:

```bash
# 1. Compile
cd apps/erc20-token
truffle compile

# 2. Update ABI
cp build/contracts/Token.json ../../contracts/token.abi

# 3. Regenerate Go bindings (if needed)
make gen-abi
```

## Related Chain Context

- ETH (Ethereum)
- ERC20 (Token standard)

## Related Skills

- `git-workflow` - Branch, commit, PR workflow
- `github-issue-creation` - Task classification
