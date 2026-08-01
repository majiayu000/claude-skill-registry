---
name: stacks-agent
description: Stacks blockchain development intelligence for Codex.
---

# Stacks Agent - OpenAI Codex Skill

Stacks blockchain development intelligence for Codex.

## Skill Overview

AI-powered assistance for building on Stacks - Bitcoin's smart contract layer.

## Capabilities

- Generate and audit Clarity smart contracts
- SIP-010 fungible tokens and SIP-009 NFTs
- DeFi protocol integration (Alex, Velar, Bitflow, Zest)
- Security vulnerability detection and fixes
- Stacks.js frontend integration
- BNS name system operations
- PoX stacking and pool delegation
- Deployment guides (testnet, mainnet, devnet)

## Knowledge Base

170+ searchable entries across 8 domains:

```bash
python3 .shared/stacks-agent/scripts/search.py "<query>" --domain <domain>
```

**Domains**:
- `clarity` - 61 functions and types
- `templates` - 14 contract templates
- `security` - 15 security patterns
- `defi` - 15 DeFi protocols
- `stacksjs` - 30 JavaScript snippets
- `bns` - 10 name system operations
- `stacking` - 15 stacking guides
- `deployment` - 25 deployment steps

## Workflow

1. **Analyze** user request (contract type, features, network)
2. **Search** knowledge base for relevant patterns
3. **Generate** code following Clarity best practices
4. **Apply** security patterns automatically
5. **Provide** deployment instructions

## Code Generation Rules

### Always Include
- Access control checks (`tx-sender` validation)
- Error handling (`try!`, `unwrap!`)
- Input validation (`asserts!`)
- Named error constants (`ERR-*`)
- Kebab-case naming
- Documentation comments

### Never Include
- `unwrap-panic` in production code
- Hardcoded magic numbers
- Unvalidated external calls
- Missing return value checks

## Security Patterns

### Critical
- Validate `tx-sender` for sensitive operations
- Check all transfer return values
- Handle errors explicitly

### High
- Validate all inputs
- Prevent division by zero
- Update state before external calls

### Medium
- Prevent self-transfers
- Restrict minting functions
- Use `tx-sender` not `contract-caller`

## Example Outputs

### Token Contract
```clarity
(define-fungible-token my-token u1000000)
(define-constant ERR-UNAUTHORIZED (err u100))
(define-constant ERR-INVALID-AMOUNT (err u101))

(define-public (transfer (amount uint) (recipient principal))
  (begin
    (asserts! (> amount u0) ERR-INVALID-AMOUNT)
    (try! (ft-transfer? my-token amount tx-sender recipient))
    (ok true)))
```

### DeFi Integration
```clarity
;; Swap on Alex
(contract-call?
  'SP102V8P0F7JX67ARQ77WEA3D3CFB5XW39REDT0AM.amm-swap-pool-v1-1
  swap-helper
  .token-wstx
  .age000-governance-token
  u100000000
  u100000000
  u1000000
  u1)
```

## Networks

- **Mainnet**: SP... addresses (production)
- **Testnet**: ST... addresses (free STX for testing)
- **Devnet**: Local Clarinet development

## Standards

- SIP-010 (FT): `SP3FBR2AGK5H9QBDH3EEN6DF8EK8JY7RX8QJ5SVTE.sip-010-trait-ft-standard`
- SIP-009 (NFT): `SP2PABAF9FTAJYNFZH93XENAJ8FVY99RRM50D2JG9.nft-trait`

## Resources

- https://docs.stacks.co
- https://explorer.hiro.so
- https://github.com/hirosystems/clarinet

**Version**: 1.0.0
**Author**: kai-builder
