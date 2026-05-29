---
name: software-crypto-web3
description: Production-grade blockchain and Web3 development with Solidity (Ethereum/EVM), Rust (Solana), CosmWasm (Cosmos), including smart contract architecture, security patterns, gas optimization, testing strategies, DeFi protocols, and deployment workflows.
---

# Blockchain & Web3 Development Skill — Quick Reference

This skill equips blockchain developers with execution-ready patterns for building secure, gas-optimized smart contracts and decentralized applications. Apply these patterns when you need smart contract development, DeFi protocols, NFT implementations, security audits, or Web3 architecture.

**Modern Best Practices (Jan 2026)**: Solidity 0.8.33+, security-first development, explicit threat models, comprehensive testing (unit, integration, fork, invariant), audits/formal methods where warranted, upgrade safety (timelocks, governance, rollback plans), and defense-in-depth for key custody and signing.

---

## Quick Reference

| Task | Tool/Framework | Command | When to Use |
|------|----------------|---------|-------------|
| Solidity Development | Hardhat/Foundry | `npx hardhat init` or `forge init` | Ethereum/EVM smart contracts |
| Solana Programs | Anchor | `anchor init` | Solana blockchain development |
| Cosmos Contracts | CosmWasm | `cargo generate --git cosmwasm-template` | Cosmos ecosystem contracts |
| TON Contracts | Tact/FunC + Blueprint | `npm create ton@latest` | TON blockchain development |
| Testing (Solidity) | Foundry/Hardhat | `forge test` or `npx hardhat test` | Unit, fork, invariant tests |
| Security Audit | Slither/Mythril/Echidna | `slither .` | Static analysis, fuzzing |
| Gas Optimization | Foundry Gas Snapshots | `forge snapshot` | Benchmark and optimize gas |
| Deployment | Hardhat Deploy/Forge Script | `npx hardhat deploy` | Mainnet/testnet deployment |
| Verification | Etherscan API | `npx hardhat verify` | Source code verification |
| Upgradeable Contracts | OpenZeppelin Upgrades | `@openzeppelin/hardhat-upgrades` | Proxy-based upgrades |

# When to Use This Skill

Use this skill when you need:

- Smart contract development (Solidity, Rust, CosmWasm)
- DeFi protocol implementation (AMM, lending, staking, yield farming)
- NFT and token standards (ERC20, ERC721, ERC1155, SPL tokens)
- DAO governance systems
- Cross-chain bridges and interoperability
- Gas optimization and storage patterns
- Smart contract security audits
- Testing strategies (Foundry, Hardhat, Anchor)
- Oracle integration (Chainlink, Pyth)
- Upgradeable contract patterns (proxies, diamonds)
- Web3 frontend integration (ethers.js, web3.js, @solana/web3.js)
- Blockchain indexing (The Graph, subgraphs)
- MEV protection and flashbots
- Layer 2 scaling solutions (Optimism, Arbitrum, zkSync)
- **Backend crypto integration** (.NET/C#, multi-provider architecture, CQRS)
- Webhook handling and signature validation (Fireblocks, custodial providers)
- Event-driven architecture with Kafka for crypto payments
- Transaction lifecycle management and monitoring
- Wallet management (custodial vs non-custodial)

## Decision Tree: Blockchain Platform Selection

```text
Project needs: [Use Case]
    ├─ EVM-compatible smart contracts?
    │   ├─ Complex testing needs → Foundry (Solidity tests, fuzzing, gas snapshots)
    │   ├─ TypeScript ecosystem → Hardhat (plugins, TypeScript, Ethers.js)
    │   └─ Enterprise features → NestJS + Hardhat
    │
    ├─ High throughput/low fees?
    │   ├─ Rust-based → Solana (Anchor framework)
    │   ├─ EVM L2 → Arbitrum/Optimism (Ethereum security, lower gas)
    │   └─ Telegram integration → TON (Tact/FunC contracts)
    │
    ├─ Interoperability across chains?
    │   ├─ Cosmos ecosystem → CosmWasm (IBC protocol)
    │   ├─ Multi-chain DeFi → LayerZero or Wormhole
    │   └─ Bridge development → Custom bridge contracts
    │
    ├─ Token standard implementation?
    │   ├─ Fungible tokens → ERC20 (OpenZeppelin), SPL Token (Solana)
    │   ├─ NFTs → ERC721/ERC1155 (OpenZeppelin), Metaplex (Solana)
    │   └─ Semi-fungible → ERC1155 (gaming, fractionalized NFTs)
    │
    ├─ DeFi protocol development?
    │   ├─ AMM/DEX → Uniswap V3 fork or custom (x*y=k, concentrated liquidity)
    │   ├─ Lending → Compound/Aave fork (collateralized borrowing)
    │   └─ Staking/Yield → Custom reward distribution contracts
    │
    ├─ Upgradeable contracts required?
    │   ├─ Transparent Proxy → OpenZeppelin (admin/user separation)
    │   ├─ UUPS → Gas-efficient (upgrade logic in implementation)
    │   └─ Diamond Standard → Modular functionality (EIP-2535)
    │
    └─ Backend integration?
        ├─ .NET/C# → Multi-provider architecture (see Backend Integration Patterns)
        ├─ Node.js → Ethers.js/Web3.js + Prisma
        └─ Python → Web3.py + FastAPI
```

**Chain-Specific Considerations:**

- **Ethereum/EVM**: Security-first, higher gas costs, largest ecosystem
- **Solana**: Performance-first, Rust required, lower fees
- **Cosmos**: Interoperability-first, IBC native, growing ecosystem
- **TON**: Telegram-first, async contracts, unique architecture

See [resources/](resources/) for chain-specific best practices.

---

## Security-First Patterns (Jan 2026)

> **Security baseline**: Assume an adversarial environment. Treat contracts and signing infrastructure as public, attackable APIs.

### Custody, Keys, and Signing (Core)

Key management is the dominant risk driver in production crypto systems. Use general key management guidance as a baseline (NIST SP 800-57) https://csrc.nist.gov/publications/detail/sp/800-57-part-1/rev-5/final

| Model | Who holds keys | Typical use | Primary risks | Default controls |
|------|-----------------|------------|---------------|------------------|
| Non-custodial | End user wallet | Consumer apps, self-custody | Phishing, approvals, UX errors | Hardware wallet support, clear signing UX, allowlists |
| Custodial | Your service (HSM/MPC) | Exchanges, payments, B2B | Key theft, insider threat, ops mistakes | HSM/MPC, separation of duties, limits/approvals, audit logs |
| Hybrid | Split responsibility | Enterprises | Complex failure modes | Explicit recovery/override paths, runbooks |

Do:
- Separate hot/warm/cold signing paths with limits and approvals [Inference]
- Require dual control for high-value transfers (policy engine + human approval) [Inference]
- Keep an immutable audit trail for signing requests (who/what/when/why) [Inference]

Avoid:
- Storing private keys in databases or application config
- Reusing signing keys across environments (dev/staging/prod)
- Hot-wallet automation without rate limits and circuit breakers [Inference]

### Checks-Effects-Interactions (CEI) Pattern

**Mandatory** for all state-changing functions.

```solidity
// Correct: CEI pattern
function withdraw(uint256 amount) external {
    // 1. CHECKS: Validate conditions
    require(balances[msg.sender] >= amount, "Insufficient balance");

    // 2. EFFECTS: Update state BEFORE external calls
    balances[msg.sender] -= amount;

    // 3. INTERACTIONS: External calls LAST
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success, "Transfer failed");
}

// Wrong: External call before state update (reentrancy risk)
function withdrawUnsafe(uint256 amount) external {
    require(balances[msg.sender] >= amount);
    (bool success, ) = msg.sender.call{value: amount}("");
    require(success);
    balances[msg.sender] -= amount; // Too late!
}
```

### Formal Verification

| Tool | Purpose | When to Use |
|------|---------|-------------|
| SMTChecker | Built-in Solidity checker | Every contract |
| Certora | Property-based verification | DeFi protocols, high-value |
| Halmos | Symbolic testing | Complex invariants |

```solidity
// Certora CVL rule example
rule balanceNeverNegative(address user) {
    env e;
    require balances[user] >= 0;
    deposit(e);
    assert balances[user] >= 0;
}
```

### MEV Protection

| Strategy | Implementation |
|----------|----------------|
| Private mempool | Flashbots Protect, MEV Blocker |
| Commit-reveal | Hash commitment, reveal after deadline |
| Batch auctions | CoW Protocol, Gnosis Protocol |
| Encrypted mempools | Shutter Network |

```solidity
// Commit-reveal pattern
mapping(address => bytes32) public commitments;

function commit(bytes32 hash) external {
    commitments[msg.sender] = hash;
}

function reveal(uint256 value, bytes32 salt) external {
    require(
        keccak256(abi.encodePacked(value, salt)) == commitments[msg.sender],
        "Invalid reveal"
    );
    // Process revealed value
}
```

---

### Optional: AI/Automation Extensions

> **Note**: AI-assisted smart contract tools. Skip if not using AI tooling.

#### AI-Assisted Auditing

| Tool | Purpose |
|------|---------|
| Slither AI | Enhanced static analysis |
| Olympix | AI vulnerability detection |
| Auditless | Automated audit reports |

#### LLM Limitations in Smart Contracts

**Do not rely on LLMs for:**

- Security-critical logic verification
- Gas optimization calculations
- Complex mathematical proofs

**Use LLMs for:**

- Boilerplate generation (tests, docs)
- Code explanation and review prep
- Initial vulnerability hypotheses (verify manually)

---

## Navigation

**Resources**

- [resources/blockchain-best-practices.md](resources/blockchain-best-practices.md) — Universal blockchain patterns and security
- [resources/backend-integration-best-practices.md](resources/backend-integration-best-practices.md) — .NET/C# crypto integration patterns (CQRS, Kafka, multi-provider)
- [resources/solidity-best-practices.md](resources/solidity-best-practices.md) — Solidity/EVM-specific guidance
- [resources/rust-solana-best-practices.md](resources/rust-solana-best-practices.md) — Solana + Anchor patterns
- [resources/cosmwasm-best-practices.md](resources/cosmwasm-best-practices.md) — Cosmos/CosmWasm guidance
- [resources/ton-best-practices.md](resources/ton-best-practices.md) — TON contracts (Tact/Fift/FunC) and deployment
- [../software-security-appsec/resources/smart-contract-security-auditing.md](../software-security-appsec/resources/smart-contract-security-auditing.md) — Smart contract audit workflows and tools (see software-security-appsec skill)
- [README.md](README.md) — Folder overview and usage notes
- [data/sources.json](data/sources.json) — Curated external references per chain
- Shared secure review checklist: [../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md](../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md)

**Templates**
- Ethereum/EVM: [templates/ethereum/template-solidity-hardhat.md](templates/ethereum/template-solidity-hardhat.md), [templates/ethereum/template-solidity-foundry.md](templates/ethereum/template-solidity-foundry.md)
- Solana: [templates/solana/template-rust-anchor.md](templates/solana/template-rust-anchor.md)
- Cosmos: [templates/cosmos/template-cosmwasm.md](templates/cosmos/template-cosmwasm.md)
- TON: [templates/ton/template-tact-blueprint.md](templates/ton/template-tact-blueprint.md), [templates/ton/template-func-blueprint.md](templates/ton/template-func-blueprint.md)
- Bitcoin: [templates/bitcoin/template-bitcoin-core.md](templates/bitcoin/template-bitcoin-core.md)

**Related Skills**

- [../software-security-appsec/SKILL.md](../software-security-appsec/SKILL.md) — Security hardening, threat modeling, OWASP vulnerabilities
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — System decomposition, modularity, dependency design
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — Infrastructure, CI/CD, observability for blockchain nodes
- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API integration with smart contracts, RPC nodes, indexers
- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience, circuit breakers, retry logic for chains
- [../software-code-review/SKILL.md](../software-code-review/SKILL.md) — Code review patterns and quality gates
- [../dev-api-design/SKILL.md](../dev-api-design/SKILL.md) — RESTful design for Web3 APIs and dApp backends

---

## Operational Playbooks
- [resources/operational-playbook.md](resources/operational-playbook.md) — Smart contract architecture, security-first workflows, and platform-specific patterns
