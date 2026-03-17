---
name: midnight-tooling:contract-deployment
description: Use when deploying Compact contracts to Midnight testnet or mainnet, configuring network endpoints, handling deployment confirmation, troubleshooting failed deployments, or setting up deployment scripts for CI/CD.
---

# Contract Deployment

Deploy Compact smart contracts to Midnight testnet or mainnet with proper configuration, verification, and error handling.

## When to Use

- Deploying a compiled Compact contract for the first time
- Configuring network endpoints for deployment
- Handling deployment transaction confirmation
- Troubleshooting failed deployments
- Setting up deployment scripts for CI/CD

## Key Concepts

### Deployment Flow

1. **Compile contract** - Use `compact compile` to generate artifacts
2. **Configure network** - Set indexer, prover, and node endpoints
3. **Fund deployer** - Ensure account has sufficient tDUST (testnet) or DUST (mainnet)
4. **Submit transaction** - Deploy contract and wait for confirmation
5. **Verify deployment** - Query contract address on chain

### Network Configuration

| Network | Indexer | Prover | Use Case |
|---------|---------|--------|----------|
| Testnet | `indexer.testnet.midnight.network` | `prover.testnet.midnight.network` | Development, testing |
| Mainnet | `indexer.midnight.network` | `prover.midnight.network` | Production |

### Contract Artifacts

After `compact compile`, the output directory contains:
- `contract.cjs` - Contract bytecode and circuits
- `contract.d.cts` - TypeScript types for contract interface
- `circuit-keys/` - ZK circuit proving keys

## References

| Document | Description |
|----------|-------------|
| [deployment-config.md](references/deployment-config.md) | Network configuration and environment setup |
| [network-endpoints.md](references/network-endpoints.md) | Endpoint URLs and connection patterns |

## Examples

| Example | Description |
|---------|-------------|
| [single-contract/](examples/single-contract/) | Deploy a single contract |
| [multi-contract/](examples/multi-contract/) | Deploy multiple contracts with dependencies |

## Quick Start

### 1. Configure Network

```typescript
import { NetworkConfig } from '@midnight-ntwrk/midnight-js-types';

const config: NetworkConfig = {
  indexer: 'https://indexer.testnet.midnight.network',
  indexerWs: 'wss://indexer.testnet.midnight.network/ws',
  prover: 'https://prover.testnet.midnight.network',
};
```

### 2. Load Contract Artifacts

```typescript
import { Contract } from './contract.cjs';
import type { ContractTypes } from './contract.d.cts';

const contractArtifact = Contract;
```

### 3. Deploy

```typescript
import { deployContract } from '@midnight-ntwrk/midnight-js-contracts';

const deployedContract = await deployContract({
  wallet,
  artifact: contractArtifact,
  initialState: { /* initial ledger state */ },
  config,
});

console.log('Deployed at:', deployedContract.address);
```

## Common Patterns

### Environment-Based Configuration

```typescript
const getNetworkConfig = (): NetworkConfig => {
  const network = process.env.MIDNIGHT_NETWORK || 'testnet';

  if (network === 'mainnet') {
    return {
      indexer: 'https://indexer.midnight.network',
      indexerWs: 'wss://indexer.midnight.network/ws',
      prover: 'https://prover.midnight.network',
    };
  }

  return {
    indexer: 'https://indexer.testnet.midnight.network',
    indexerWs: 'wss://indexer.testnet.midnight.network/ws',
    prover: 'https://prover.testnet.midnight.network',
  };
};
```

### Deployment with Retry

```typescript
async function deployWithRetry(
  config: DeployConfig,
  maxRetries = 3
): Promise<DeployedContract> {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await deployContract(config);
    } catch (error) {
      if (attempt === maxRetries) throw error;
      console.log(`Attempt ${attempt} failed, retrying...`);
      await new Promise(r => setTimeout(r, 2000 * attempt));
    }
  }
  throw new Error('Deployment failed after retries');
}
```

### Deployment Verification

```typescript
async function verifyDeployment(
  address: string,
  indexer: IndexerClient
): Promise<boolean> {
  try {
    const contractInfo = await indexer.getContractInfo(address);
    return contractInfo !== null;
  } catch {
    return false;
  }
}
```

## Related Skills

- `midnight-setup` - Environment prerequisites before deployment
- `contract-calling` - Invoking deployed contracts
- `lifecycle-management` - Managing contracts post-deployment
- `midnight-ci` - Automated deployment in CI/CD

## Related Commands

- `/midnight:check` - Verify environment is ready for deployment
