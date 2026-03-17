---
name: aztec-deploy
description: Generate TypeScript deployment scripts for Aztec contracts with fee payment configuration. Use when deploying contracts, setting up deployment pipelines, or configuring fee payment methods.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Aztec Deployment Skill

Generate production-ready TypeScript deployment scripts for Aztec smart contracts.

## Subskills

Navigate to the appropriate section based on your task:

* [Deploy Script](./deploy-script.md) - Full deployment script template
* [Fee Payment](./fee-payment.md) - Fee payment methods and configuration
* [Environment Config](./environment-config.md) - Local network vs devnet setup

## Quick Start: Basic Deployment Script

```typescript
import { MyContract } from "../src/artifacts/MyContract.js";
import { type Logger, createLogger } from "@aztec/foundation/log";
import { SponsoredFeePaymentMethod } from "@aztec/aztec.js/fee";
import { setupWallet } from "../src/utils/setup_wallet.js";
import { getSponsoredFPCInstance } from "../src/utils/sponsored_fpc.js";
import { SponsoredFPCContractArtifact } from "@aztec/noir-contracts.js/SponsoredFPC";
import { deploySchnorrAccount } from "../src/utils/deploy_account.js";
import { getTimeouts } from "../config/config.js";

async function main() {
    const logger = createLogger('aztec:deploy');

    // 1. Setup wallet connection
    const wallet = await setupWallet();

    // 2. Setup sponsored fee payment
    const sponsoredFPC = await getSponsoredFPCInstance();
    await wallet.registerContract(sponsoredFPC, SponsoredFPCContractArtifact);
    const paymentMethod = new SponsoredFeePaymentMethod(sponsoredFPC.address);

    // 3. Deploy account (or use existing)
    const account = await deploySchnorrAccount(wallet);

    // 4. Deploy contract
    const { contract } = await MyContract.deploy(wallet, account.address).send({
        from: account.address,
        fee: { paymentMethod },
        wait: { timeout: getTimeouts().deployTimeout, returnReceipt: true }
    });

    logger.info(`Contract deployed at: ${contract.address}`);
}

main().catch(console.error);
```

## Deployment Workflow

1. **Setup Wallet** - Connect to Aztec node via PXE
2. **Configure Fees** - Setup sponsored or other fee payment
3. **Create Account** - Deploy Schnorr account or recover existing
4. **Deploy Contract** - Send deployment transaction
5. **Verify** - Confirm deployment succeeded

## Key Imports

```typescript
// Wallet and node connection
import { createAztecNodeClient } from '@aztec/aztec.js/node';
import { EmbeddedWallet } from '@aztec/wallets/embedded';

// Account management
import { Fr } from "@aztec/aztec.js/fields";
import { GrumpkinScalar } from "@aztec/foundation/curves/grumpkin";
import { AccountManager } from "@aztec/aztec.js/wallet";
import { AztecAddress } from "@aztec/aztec.js/addresses";

// Fee payment
import { SponsoredFeePaymentMethod } from "@aztec/aztec.js/fee";
import { SponsoredFPCContractArtifact } from "@aztec/noir-contracts.js/SponsoredFPC";

// Logging
import { type Logger, createLogger } from "@aztec/foundation/log";
```

## Using Aztec MCP Server

For detailed API documentation and deployment patterns, use the Aztec MCP tools:

```
# Sync repos first
aztec_sync_repos()

# Search for deployment patterns
aztec_search_code({ query: "deploy", filePattern: "*.ts" })

# Search documentation
aztec_search_docs({ query: "deployment" })
```

The `aztec-starter` repo has reference implementations of deployment scripts, devnet configuration, and integration test patterns.
