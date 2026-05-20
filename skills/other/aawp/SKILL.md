---
name: aawp
version: 2.0.0
description: >
  AAWP (AI Agent Wallet Protocol) — the only crypto wallet protocol built exclusively
  for AI Agents on EVM-compatible blockchains and Solana. Not for humans. The signer is
  the AI Agent itself, cryptographically bound at wallet creation. Supports wallet lifecycle
  management, token transfers, DEX swaps, cross-chain bridging, Solana native trading
  (Pump.fun SDK + Jupiter), token launches, DCA automation, and price alerts.
environment:
  - name: AAWP_GUARDIAN_KEY
    description: "Private key for the Guardian gas-relay wallet (auto-generated in config/guardian.json if not set)"
    required: false
  - name: AAWP_GAS_KEY
    description: "Alias for AAWP_GUARDIAN_KEY"
    required: false
  - name: AAWP_WALLET
    description: "Pinned wallet address — prevents accidental operations on wrong wallet"
    required: false
  - name: AAWP_CONFIG
    description: "Override config directory path (default: ./config)"
    required: false
  - name: AAWP_CORE
    description: "Override native addon directory path (default: ./core)"
    required: false
  - name: AAWP_SKILL
    description: "Override skill root directory path"
    required: false
  - name: AAWP_AI_TOKEN
    description: "Daemon auth token (auto-generated at startup, not user-supplied)"
    required: false
credentials:
  - name: "Guardian Key"
    description: "ECDSA private key for the gas-relay wallet. Auto-generated on first provision and stored in config/guardian.json. Used ONLY to pay gas fees — never holds user assets."
  - name: "Encrypted Seed"
    description: "Agent signing seed, encrypted at rest. Generated during provisioning, stored in the .agent-config directory. This is the agent's on-chain signing authority."
persistence:
  - type: daemon
    description: "Local signing daemon (background process) listens on a Unix socket at /tmp/.aawp-daemon.*. Holds the signing key in memory during operation. Managed via ensure-daemon.sh / restart-daemon.sh."
  - type: files
    description: "Writes to config/ and .agent-config/ directories, plus a daemon PID lock under /tmp/."
  - type: cron
    description: "DCA strategies and price alerts register OpenClaw cron jobs for autonomous scheduled execution."
native_binary:
  file: core/aawp-core.node
  hash_file: core/aawp-core.node.hash
  description: >
    Precompiled Node.js N-API addon (linux-x64) for cryptographic operations.
    Built from Rust via napi-rs. Hash recorded in aawp-core.node.hash.
  source: "https://github.com/aawp-ai/aawp"
  verification: "On-chain factory approveBinary(hash) — only whitelisted builds can operate wallets"
  architecture: linux-x64
  runtime: "Node.js N-API (ABI stable)"
risk_disclosure: >
  This skill runs a persistent signing daemon and can autonomously submit
  on-chain transactions as the AI Agent. It manages encrypted private key material
  and a precompiled native binary. DCA/price-alert features register cron jobs.
  The on-chain factory enforces both binary approval and AI-exclusive ownership —
  only whitelisted AI Agent daemon builds can create or operate wallets. Humans
  cannot be the signer. Review the guardian architecture and verify binary
  provenance before installing.
---

# AAWP — AI Agent Wallet Protocol

> **📦 Installer-Only Package**
> The ClawHub/npm package (`aawp-skill`) contains only this manifest (SKILL.md), README, and a small `bin/install.js` bootstrap.
> The full runtime stack — native signing addon (`core/aawp-core.node`), wallet scripts (`scripts/*.js`), and daemon — is fetched from [github.com/aawp-ai/aawp](https://github.com/aawp-ai/aawp) during `bash scripts/provision.sh`.
> The native binary hash is verified on-chain via the AAWP factory (`approveBinary(hash)`) before any wallet operation is permitted.

> **⚠️ Human Approval Required**
> The following actions **must be confirmed by a human** before execution:
> - First-time provisioning (`provision.sh`) — generates and encrypts the agent signing seed
> - Wallet creation (`wallet-manager.js create`) — deploys on-chain contract
> - DCA / price-alert cron registration — grants the agent autonomous recurring transaction rights
> - Factory binary approval (`approveBinary`) — whitelists the running binary on all chains
>
> All other operations (balance checks, quotes, reads) are safe to run autonomously.

The only crypto wallet protocol built exclusively for AI Agents. Not for humans.

AAWP enforces a single invariant: the signer is the AI Agent itself — locked in at wallet creation, immutable, verifiable on-chain. AI Agents manage their own on-chain assets across EVM networks through a guardian-based architecture. Transactions are signed locally via a sharded-key daemon — no human approval per tx, with full recovery and freeze capabilities for the human guardian.

**Networks:** Ethereum · Base · BNB Chain · Polygon · Optimism · Arbitrum

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│  AI Agent (OpenClaw)                            │
│  ┌───────────────┐    ┌──────────────────────┐  │
│  │ wallet-manager│───▶│  Signing Daemon       │  │
│  │ dca / alerts  │    │  (Unix socket)        │  │
│  └───────────────┘    │  ┌──────────────────┐ │  │
│                       │  │ aawp-core.node   │ │  │
│                       │  │ (Rust N-API)     │ │  │
│                       │  └──────────────────┘ │  │
│                       └──────────┬───────────┘  │
│                                  │ sign          │
│  ┌───────────────┐               ▼              │
│  │ Guardian Key  │──▶ Pay gas ──▶ EVM Chain     │
│  │ (gas only)    │               │              │
│  └───────────────┘    ┌──────────▼───────────┐  │
│                       │ Smart Contract Wallet │  │
│                       │ (holds assets)        │  │
│                       └──────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**EVM:** Guardian pays gas → Wallet holds assets → Daemon signs (secp256k1).
**Solana:** AI Signer pays directly → Wallet PDA holds assets → Daemon signs (Ed25519).

Same seed, HKDF domain separation → cryptographically independent keys per chain family.

---

## Quick Reference

| Task | Command |
|------|---------|
| Create wallet | `wallet-manager.js --chain base create` |
| Check balance | `wallet-manager.js --chain base balance` |
| Send ETH | `wallet-manager.js --chain base send <to> <amount>` |
| Send ERC-20 | `wallet-manager.js --chain base send-token USDC <to> <amount>` |
| Get swap quote | `wallet-manager.js --chain base quote ETH USDC 0.01` |
| Execute swap | `wallet-manager.js --chain base swap ETH USDC 0.01` |
| Bridge cross-chain | `wallet-manager.js --chain base bridge ETH optimism 0.1` |
| Contract call | `wallet-manager.js --chain base call <addr> "fn(args)" ...` |
| Contract read | `wallet-manager.js --chain base read <addr> "fn() returns (uint)" ...` |
| DCA strategy | `dca.js add --chain base --from ETH --to USDC --amount 0.01 --cron "0 9 * * *"` |
| Price alert | `price-alert.js add --chain base --from ETH --to USDC --above 2600 --notify` |
| Cross-chain portfolio | `portfolio.js` |
| Single chain portfolio | `portfolio.js --chain base` |
| Limit order | `limit-order.js --chain base create ETH USDC 0.1 2700` |
| List orders | `limit-order.js --chain base list` |
| List NFTs | `nft.js --chain base balance` |
| NFT transfer | `nft.js --chain base transfer <contract> <tokenId> <to>` |
| NFT floor price | `nft.js --chain eth floor <contract>` |
| Yield rates | `yield.js --chain base rates` |
| Supply collateral | `yield.js --chain base supply USDC 1000` |
| Borrow | `yield.js --chain base borrow USDC 200` |
| Aave positions | `yield.js --chain base positions` |
| Diagnostics | `bash scripts/doctor.sh` |
| Backup | `wallet-manager.js backup ./backup.tar.gz` |
| **Solana** | |
| Solana status | `wallet-manager.js --chain solana status` |
| Solana balance | `wallet-manager.js --chain solana balance` |
| Solana swap (Pump) | `wallet-manager.js --chain solana swap SOL <mint> 0.1` |
| Solana swap (Jupiter) | `wallet-manager.js --chain solana swap SOL USDC 0.5 --pool jupiter` |
| Pump token info | `wallet-manager.js --chain solana pump-info <mint>` |
| Pump launch token | `wallet-manager.js --chain solana pump-create <name> <symbol> <uri> --buy 0.5` |
| Pump creator fees | `wallet-manager.js --chain solana pump-fees balance` |
| Pump incentives | `wallet-manager.js --chain solana pump-incentives` |
| Pump AMM liquidity | `wallet-manager.js --chain solana pump-lp deposit <mint> <amt>` |

All commands: `node scripts/wallet-manager.js --help`

---

## Getting Started

### 1. Provision

First run is automatic — `ensure-daemon.sh` detects a missing seed and provisions.

```bash
bash scripts/provision.sh            # Initialize
bash scripts/provision.sh --reset    # Full reset (⚠️ destroys existing wallet)
```

### 2. Create Wallet

```bash
node scripts/wallet-manager.js --chain base create
```

If the Guardian needs gas, you'll see a funding guide with the Guardian address and private key.

### 3. Pin & Fund

```bash
export AAWP_WALLET=0x...            # Pin your wallet address
# Send a small amount of native token to the wallet address
node scripts/wallet-manager.js --chain base balance
```

### 4. Test

```bash
node scripts/wallet-manager.js --chain base quote ETH USDC 0.001
node scripts/wallet-manager.js --chain base swap ETH USDC 0.001
```

> After fresh provisioning, verify the daemon binary hash is approved on the factory contract. If not, the factory owner must call `approveBinary(hash)`.

---

## Wallet Manager CLI

**Entry point:** `node scripts/wallet-manager.js`
**Chain flag:** `--chain <base|bsc|polygon|optimism|arbitrum|ethereum>`

### Wallet Lifecycle

```bash
wallet-manager.js --chain base status          # Status overview
wallet-manager.js --chain base balance         # Native + token balances
wallet-manager.js --chain base portfolio       # Full portfolio view
wallet-manager.js compute-address              # Predict wallet address
wallet-manager.js --chain base history         # Transaction history
wallet-manager.js --chain base upgrade-signer  # Rotate signer key
wallet-manager.js --chain base guardian-chains  # Guardian chain info
```

### Transfers

```bash
wallet-manager.js --chain base send <recipient> <amount>
wallet-manager.js --chain base send-token <symbol> <recipient> <amount>
```

### Trading

```bash
wallet-manager.js --chain base quote <from> <to> <amount>    # Preview (no gas)
wallet-manager.js --chain base swap <from> <to> <amount>     # Execute
wallet-manager.js --chain base bridge <token> <dest> <amount> # Cross-chain
```

### Approvals

```bash
wallet-manager.js --chain base approve <token> <spender> <amount>
wallet-manager.js --chain base allowance <token> <spender>
wallet-manager.js --chain base revoke <token> <spender>
```

### Contract Interaction

```bash
# Write (sends tx)
wallet-manager.js --chain base call <contract> "transfer(address,uint256)" 0xTo 1000

# Read (free)
wallet-manager.js --chain base read <contract> "balanceOf(address) returns (uint256)" 0xAddr

# Batch (atomic)
wallet-manager.js --chain base batch ./calls.json
```

Batch format:
```json
[
  { "to": "0x...", "sig": "approve(address,uint256)", "args": ["0x...", "1000000"] },
  { "to": "0x...", "sig": "transfer(address,uint256)", "args": ["0x...", "500000"] }
]
```

### Address Book

```bash
wallet-manager.js addr add <label> <address>
wallet-manager.js addr list
wallet-manager.js addr get <label>
wallet-manager.js addr remove <label>
```

### RPC & Backup

```bash
wallet-manager.js get-rpc
wallet-manager.js --chain base set-rpc <url|default>
wallet-manager.js backup ./backup.tar.gz
wallet-manager.js restore ./backup.tar.gz
```

---

## DCA Automation

**Entry point:** `node scripts/dca.js`

```bash
dca.js add --chain base --from ETH --to USDC --amount 0.01 --cron "0 9 * * *" --name "Daily ETH→USDC"
dca.js list
dca.js run <id>
dca.js history <id>
dca.js remove <id>
```

Registers an OpenClaw cron job that executes swaps on schedule.

---

## Price Alerts

**Entry point:** `node scripts/price-alert.js`

```bash
# Notification only
price-alert.js add --chain base --from ETH --to USDC --above 2600 --notify

# Auto-swap on trigger
price-alert.js add --chain base --from ETH --to USDC --below 2200 --notify --auto-swap 0.01

price-alert.js list
price-alert.js check
price-alert.js remove <id>
```

---

## Daemon Management

| Script | Purpose |
|--------|---------|
| `scripts/doctor.sh` | Full diagnostic check |
| `scripts/ensure-daemon.sh` | Start daemon if not running (auto-provisions on first run) |
| `scripts/restart-daemon.sh` | Force restart |

Run `doctor.sh` before sensitive operations or when signing seems off.

---

## Cross-Chain Portfolio View

**Entry point:** `node scripts/portfolio.js`
**Supported chains:** All 6 (base · eth · arb · op · polygon · bsc) — queried **in parallel**

### Commands

```bash
portfolio.js                      # Full cross-chain summary with USD values
portfolio.js --chain base         # Single chain only
portfolio.js --no-prices          # Skip CoinGecko pricing (faster)
portfolio.js --hide-zero          # Hide zero-balance tokens
portfolio.js --json               # Raw JSON output (for automation)
```

### Output Includes
- Native balance per chain (ETH / BNB / MATIC)
- All ERC-20 token balances via **Multicall3** (1 RPC call per chain)
- USD value per token (CoinGecko public API)
- **Total portfolio value** across all chains
- **Top 8 holdings** ranked by USD value with % allocation
- **Multi-chain holdings** — same token aggregated across chains

**Tokens tracked:** USDC, USDT, WETH, DAI, WBTC, BNB/WBNB, MATIC, ARB, OP, CAKE, AERO, GMX, PEPE, and more per chain.

---

## Limit Orders (CoW Protocol — Gasless)

**Entry point:** `node scripts/limit-order.js`
**Supported chains:** `eth` · `base` · `arb` · `op` · `polygon` (CoW Protocol) · `bsc` (1inch Limit Orders)

Orders are signed off-chain (EIP-712) and settled by solvers — **no gas on order creation** (except BSC cancel which is on-chain).

### Commands

```bash
limit-order.js --chain base create ETH USDC 0.1 2700      # Sell 0.1 ETH at ≥2700 USDC
limit-order.js --chain eth create USDC ETH 1000 0.00037   # Buy ETH with 1000 USDC
limit-order.js --chain base list                           # List open orders
limit-order.js --chain base history                        # All orders (filled/expired)
limit-order.js --chain base cancel <orderUid>              # Cancel open order
limit-order.js --chain base create ETH USDC 0.1 2700 --expiry 48   # 48h validity
```

**Notes:**
- First-time use requires one ERC-20 approval transaction (CoW VaultRelayer)
- `price` = amount of buyToken per 1 sellToken
- Orders persist in `config/limit-orders.json` for local tracking

---

## NFT Operations (ERC-721 & ERC-1155)

**Entry point:** `node scripts/nft.js`
**Supported chains:** All 6 chains (BSC via BscScan NFT API)

### Commands

```bash
nft.js --chain base balance                          # List all NFTs (via Alchemy public API)
nft.js --chain eth balance --contract 0xBC4C...      # NFTs from specific collection
nft.js --chain eth info 0xBC4C... 1234               # Token metadata, owner, traits
nft.js --chain base transfer 0xNFT... 42 0xTo...     # ERC-721 transfer
nft.js --chain base transfer 0xNFT... 42 0xTo... 5   # ERC-1155 transfer (amount=5)
nft.js --chain base approve 0xNFT... 0xOperator...   # setApprovalForAll = true
nft.js --chain base revoke  0xNFT... 0xOperator...   # setApprovalForAll = false
nft.js --chain base mint 0xContract...               # Call mint() on contract
nft.js --chain base mint 0xContract... 0xcalldata    # Mint with custom calldata
nft.js --chain eth floor 0xBC4C...                   # Floor price from OpenSea
```

**Notes:**
- `balance` auto-detects ERC-721 vs ERC-1155 and fetches metadata
- `info` resolves IPFS URIs and displays traits
- `floor` queries OpenSea public API; Blur link provided for ETH collections

---

## Yield / DeFi (Aave V3)

**Entry point:** `node scripts/yield.js`
**Supported chains:** `base` · `eth` · `arb` · `op` · `polygon` (Aave V3) · `bsc` (Venus Protocol)

### Commands

```bash
yield.js --chain base rates                    # Show supply/borrow APY for all tokens
yield.js --chain base positions                # Show active Aave positions & health factor
yield.js --chain base supply USDC 1000         # Supply 1000 USDC as collateral
yield.js --chain base withdraw USDC 500        # Withdraw 500 USDC
yield.js --chain base withdraw USDC max        # Full withdrawal
yield.js --chain base borrow USDC 200          # Borrow 200 USDC (variable rate, default)
yield.js --chain base borrow USDC 200 --rate stable   # Borrow at stable rate
yield.js --chain base repay USDC 200           # Repay partial debt
yield.js --chain base repay USDC max           # Full repayment
```

### Supported Tokens by Chain

| Chain   | Tokens |
|---------|--------|
| base    | USDC, WETH, cbBTC, USDbC |
| eth     | USDC, USDT, DAI, WBTC, WETH |
| arb     | USDC, USDT, WETH, WBTC, DAI |
| op      | USDC, USDT, WETH, WBTC, DAI |
| polygon | USDC, USDT, WETH, WBTC, DAI, WMATIC |

> **Safety note:** Always check your health factor after borrowing. Health factor < 1.0 triggers liquidation. Use `positions` to monitor.

---

## Token Launch (Clanker V4)

Deploy a token via your AAWP wallet as the on-chain deployer, admin, and LP fee recipient.

**Script:** `scripts/deploy-clanker.js`

### Supported chains

| Key | Chain | ChainId |
|-----|-------|---------|
| `base` | Base | 8453 |
| `eth` | Ethereum | 1 |
| `arb` | Arbitrum | 42161 |
| `unichain` | Unichain | 130 |
| `bera` | Berachain | 143 |
| `bsc` | BSC | 56 |

### Usage

```bash
# 1. Edit CONFIG at the top of the script
# 2. Preview (no broadcast)
node scripts/deploy-clanker.js --dry-run

# 3. Deploy
node scripts/deploy-clanker.js
```

### CONFIG reference

```js
const CONFIG = {
  chain:       'base',          // base | eth | arb | unichain | bera | bsc
  name:        'My Token',
  symbol:      'MTK',
  image:       'https://...',   // square image URL
  description: '...',
  website:     '',              // optional
  twitter:     '',              // optional

  initialMarketCap: 10,         // ETH (min ~10 ≈ $25K FDV)
  poolPositions:    'Standard', // Standard | Project | TwentyETH
  feeConfig:        'StaticBasic', // StaticBasic (1%) | DynamicBasic | Dynamic3
  devBuyEth:        0.003,      // ETH to buy at launch (0 to skip)

  vault: {
    enabled:     false,         // true = lock a portion of supply
    percentage:  20,            // % of supply (1–90)
    lockupDays:  7,             // cliff (min 7 days)
    vestingDays: 180,           // linear unlock after cliff
  },

  tokenAdmin:      null,        // null = AAWP wallet
  rewardRecipient: null,        // null = AAWP wallet (receives LP fees)
};
```

> **How it works:** the AAWP wallet calls `Clanker.deployToken()` directly (gas limit 8M).
> `tokenAdmin` and all LP fee rewards default to the AAWP wallet — the AI Agent owns its token end-to-end.

---

## Deployment Reference

AAWP contracts share identical addresses across all chains via CREATE2 vanity deployment:

| Contract | Address |
|----------|---------|
| **Factory Proxy** | `0xAAAA3Df87F112c743BbC57c4de1700C72eB7aaAA` |
| **Identity Proxy** | `0xAAAafBf6F88367C75A9B701fFb4684Df6bCA1D1d` |

Verified on: Etherscan · BaseScan · BscScan · PolygonScan · Optimistic Etherscan · Arbiscan

---

## Security

| Rule | Why |
|------|-----|
| **Fund the wallet, not the guardian** | Guardian only pays gas — your assets live in the wallet contract |
| **Pin wallet address** | `export AAWP_WALLET=0x...` prevents operating on wrong address |
| **Quote before swap** | Preview rates and slippage before executing |
| **Start small** | Test with minimal amounts on new chains or operations |
| **Never expose secrets** | Seeds, keys, shards must never appear in logs or chat |
| **Verify binary approval** | Confirm daemon hash is approved on factory after provisioning |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| `E_AI_GATE` / `hmac_mismatch` | Restart daemon: `bash scripts/restart-daemon.sh` |
| `InvalidSignature` | Verify signer alignment and binary approval on factory |
| `Call failed` | Check balance, gas, and transaction parameters |
| `E40` / `E41` | Kill duplicate daemon process, then restart |
| `BinaryNotApproved` | Factory owner must call `approveBinary(hash)` on all 6 chains |
| TX reverts with ~1M gas used | Add `--gas-limit 8000000` — Clanker V4 / Uniswap V4 ops need up to 6M |

---

## Solana Integration

AAWP natively supports Solana via a dedicated Anchor program. Same seed, HKDF domain separation (`aawp_solana_signer_v1_{hw_hex}`) → Ed25519 keypair independent from EVM secp256k1.

### Key Addresses

| Component | Address |
|-----------|---------|
| Program ID | `AAwpAAQSVAZYHvpUW5uz7zxqj7RYTYR6CZvWL9wf4qiS` |
| Network | Mainnet + Devnet (same ID) |
| AI Signer | `BrZhu5oBmqBPGMYA8TiUS2hMr2Kpg11q5PFpfK35Kgoi` |
| Wallet PDA | `CKeDtwBFaahwX3LuEo4us1XJd7hS2e45N25zDHjTUb4f` |
| Guardian | `BvbXW3uZG9YkzQmcYEnQ5qxTkTf1tQ5Jb4vHJ8HPM77P` |

### Architecture Differences from EVM

| | EVM | Solana |
|---|---|---|
| Signing | secp256k1 (ECDSA) | Ed25519 (EdDSA) |
| Wallet | CREATE2 deterministic | PDA (Program Derived Address) |
| Gas | Guardian relays | AI Signer pays directly |
| Identity | Soulbound ERC-5192 | Soulbound PDA |
| Token Standard | ERC-20 | SPL Token / Token-2022 |

### Solana CLI Commands

All commands use `--chain solana` flag:

```bash
# ── Core ──
wallet-manager --chain solana status
wallet-manager --chain solana balance
wallet-manager --chain solana compute-address
wallet-manager --chain solana send <to> <amount_SOL>
wallet-manager --chain solana price <token_or_mint>

# ── Swap (auto-routes: Pump bonding curve → Pump AMM → Jupiter) ──
wallet-manager --chain solana swap SOL <mint> 0.1              # buy with SOL
wallet-manager --chain solana swap <mint> SOL 1000000           # sell tokens
wallet-manager --chain solana swap SOL <mint> 0.1 --pool jupiter  # force Jupiter
wallet-manager --chain solana swap SOL USDC 0.5 --slippage 5

# ── Pump.fun: Token Info ──
wallet-manager --chain solana pump-info <mint>
wallet-manager --chain solana pump-quote buy <mint> <lamports>
wallet-manager --chain solana pump-quote sell <mint> <token_amount>
wallet-manager --chain solana pump-quote cost <mint> <token_amount>  # SOL cost for N tokens

# ── Pump.fun: Token Launch ──
wallet-manager --chain solana pump-create <name> <symbol> <metadata_uri>
wallet-manager --chain solana pump-create <name> <symbol> <uri> --buy 0.5  # create + first buy

# ── Pump.fun: Creator Fees ──
wallet-manager --chain solana pump-fees balance [creator_addr]
wallet-manager --chain solana pump-fees collect [creator_addr]
wallet-manager --chain solana pump-fees distribute <mint>
wallet-manager --chain solana pump-fees cashback

# ── Pump.fun: Fee Sharing ──
wallet-manager --chain solana pump-share <mint> <addr1:share1> <addr2:share2>

# ── Pump.fun: Token Incentives ──
wallet-manager --chain solana pump-incentives              # check unclaimed
wallet-manager --chain solana pump-incentives claim

# ── Pump.fun: AMM Liquidity ──
wallet-manager --chain solana pump-lp deposit <mint> <token_amount>
wallet-manager --chain solana pump-lp withdraw <mint> <lp_amount>

# ── Pump.fun: Volume ──
wallet-manager --chain solana pump-volume                  # stats
wallet-manager --chain solana pump-volume sync

# ── Pump.fun: Migrate ──
wallet-manager --chain solana pump-migrate <mint> <withdraw_authority>
```

### Swap Routing

The swap command uses a 3-tier routing strategy:

1. **Pump.fun Bonding Curve** (default) — direct on-chain via `@pump-fun/pump-sdk`, lowest latency for active Pump tokens
2. **Pump.fun AMM** — for graduated tokens that completed the bonding curve, uses `@pump-fun/pump-swap-sdk`
3. **Jupiter Metis** — fallback aggregator for non-Pump tokens or when Pump routes fail

Token-2022 is auto-detected. The SDK handles ATA creation, WSOL wrapping, and fee calculation.

### Daemon Commands

Solana signing uses the same AAWP daemon as EVM:

- `sol_address` — returns Ed25519 public key (no AI Gate needed)
- `sol_sign` — signs arbitrary message (requires AI Gate token)

AI Gate token is read from: `addon._a0()` → `/tmp/.aawp-ai-token` → `AAWP_AI_TOKEN` env.

### Source Locations

| Path | Contents |
|------|----------|
| `/root/aawp-solana/` | Anchor program source (factory, wallet, identity) |
| `/root/aawp-solana/target/deploy/aawp_solana.so` | Compiled program (318KB) |
| `/root/clawd/skills/aawp/lib/solana.js` | Core Solana module (address, sign, balance, PDA) |
| `/root/clawd/skills/aawp/lib/solana-swap.js` | Swap router (Pump → Jupiter) |
| `/root/clawd/skills/aawp/lib/pump.js` | Full Pump.fun SDK integration |
| `/root/aawp-solana/scripts/create-mainnet-wallet.mjs` | Mainnet wallet creation script |
| `/root/aawp-solana/tests/test_raw.mjs` | Raw instruction tests (7 tests) |

---

## File Structure

```
aawp/
├── SKILL.md                    # This document
├── WALLET_SETUP.md             # First-time setup guide
├── config/
│   ├── chains.json             # Network RPC & contract addresses
│   └── guardian.json           # Guardian wallet (auto-generated, gitignored)
├── scripts/
│   ├── wallet-manager.js       # Primary CLI
│   ├── dca.js                  # DCA automation
│   ├── price-alert.js          # Price alert system
│   ├── provision.sh            # Initial provisioning
│   ├── doctor.sh               # Diagnostics
│   ├── ensure-daemon.sh        # Daemon lifecycle
│   └── restart-daemon.sh       # Force restart
├── lib/
│   ├── solana.js               # Core Solana module (address, sign, balance, PDA)
│   ├── solana-swap.js          # Swap router (Pump SDK → Jupiter fallback)
│   └── pump.js                 # Full Pump.fun SDK integration
├── core/
│   ├── aawp-core.node          # Native signing addon (linux-x64)
│   ├── aawp-core.node.hash     # Binary integrity hash
│   ├── loader.js               # Addon loader
│   └── index.d.ts              # TypeScript declarations
└── daemon/                     # Daemon implementation
```
