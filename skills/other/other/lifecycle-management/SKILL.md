---
name: midnight-tooling:lifecycle-management
description: Use when managing deployed contract lifecycles, inspecting contract state, backing up state before upgrades, planning contract migrations, implementing versioning strategies, or deprecating contracts gracefully.
---

# Contract Lifecycle Management

Manage deployed Midnight contracts throughout their lifecycle, including state inspection, backups, versioning, migrations, and graceful deprecation.

## When to Use

- Inspecting current contract state for debugging or monitoring
- Backing up contract state before upgrades
- Planning and executing contract migrations
- Implementing versioning strategies
- Deprecating old contract versions gracefully
- Managing multi-version contract deployments

## Key Concepts

### Contract Lifecycle Phases

```
┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌──────────┐
│ Deploy  │───▶│ Active  │───▶│ Migrate │───▶│ Sunset  │───▶│ Archived │
└─────────┘    └─────────┘    └─────────┘    └─────────┘    └──────────┘
                   │              │
                   │              ▼
                   │         ┌─────────┐
                   └────────▶│ Monitor │
                             └─────────┘
```

### Immutability Consideration

Midnight contracts are immutable once deployed. "Upgrades" require:

1. Deploying a new contract version
2. Migrating state from old to new contract
3. Updating references (e.g., in frontend, other contracts)
4. Deprecating the old version

### State Migration Patterns

| Pattern | Description | Use Case |
|---------|-------------|----------|
| Snapshot & Deploy | Export state, deploy new with state | Simple migrations |
| Proxy Pattern | Use proxy contract pointing to impl | Frequent upgrades |
| Dual-Write | Write to both old and new | Zero-downtime migrations |
| Lazy Migration | Migrate state on-demand | Large state migrations |

## References

| Document | Description |
|----------|-------------|
| [state-inspection.md](references/state-inspection.md) | Querying and analyzing contract state |
| [migration-patterns.md](references/migration-patterns.md) | Strategies for contract upgrades |

## Examples

| Example | Description |
|---------|-------------|
| [state-backup/](examples/state-backup/) | Export and backup contract state |
| [contract-upgrade/](examples/contract-upgrade/) | Migrate to new contract version |

## Quick Start

### 1. Inspect Current State

```typescript
import { connectContract } from '@midnight-ntwrk/midnight-js-contracts';
import { createIndexerClient } from '@midnight-ntwrk/midnight-js-indexer';

// Connect to contract
const contract = await connectContract({
  address: CONTRACT_ADDRESS,
  artifact: Contract,
  wallet,
  config,
});

// Query state via circuit
const state = await contract.query.get_state();
console.log('Current state:', state);

// Or query via indexer for raw state
const indexer = createIndexerClient({ url: config.indexer });
const rawState = await indexer.getContractState(CONTRACT_ADDRESS);
```

### 2. Backup State

```typescript
interface StateBackup {
  contractAddress: string;
  blockHeight: number;
  timestamp: string;
  state: Record<string, unknown>;
}

async function backupState(
  contract: ConnectedContract,
  indexer: IndexerClient
): Promise<StateBackup> {
  const state = await contract.query.get_full_state();
  const info = await indexer.getContractInfo(contract.address);

  return {
    contractAddress: contract.address,
    blockHeight: info.lastUpdateBlock,
    timestamp: new Date().toISOString(),
    state,
  };
}
```

### 3. Deploy New Version

```typescript
import { NewContract } from './build-v2/contract.cjs';

const newContract = await deployContract({
  wallet,
  artifact: NewContract,
  initialState: {
    ...backupData.state,
    version: 2,
  },
  config,
});

console.log('New version deployed at:', newContract.address);
```

## Common Patterns

### Version Registry

Track multiple contract versions:

```typescript
interface ContractVersion {
  version: number;
  address: string;
  deployedAt: string;
  status: 'active' | 'deprecated' | 'archived';
}

class VersionRegistry {
  private versions: ContractVersion[] = [];

  addVersion(version: ContractVersion): void {
    this.versions.push(version);
  }

  getActiveVersion(): ContractVersion | undefined {
    return this.versions.find((v) => v.status === 'active');
  }

  deprecateVersion(version: number): void {
    const v = this.versions.find((v) => v.version === version);
    if (v) {
      v.status = 'deprecated';
    }
  }

  getAllVersions(): ContractVersion[] {
    return [...this.versions].sort((a, b) => b.version - a.version);
  }
}
```

### Health Monitoring

```typescript
interface ContractHealth {
  address: string;
  isResponding: boolean;
  lastActivity: Date | null;
  stateConsistent: boolean;
  warnings: string[];
}

async function checkContractHealth(
  contract: ConnectedContract,
  indexer: IndexerClient
): Promise<ContractHealth> {
  const warnings: string[] = [];
  let isResponding = false;
  let lastActivity: Date | null = null;
  let stateConsistent = true;

  try {
    // Test responsiveness
    await contract.query.get_version();
    isResponding = true;
  } catch {
    warnings.push('Contract not responding to queries');
  }

  try {
    // Check last activity
    const info = await indexer.getContractInfo(contract.address);
    lastActivity = new Date(info.lastUpdateTimestamp);

    // Warn if inactive for long time
    const daysSinceActivity = (Date.now() - lastActivity.getTime()) / (1000 * 60 * 60 * 24);
    if (daysSinceActivity > 30) {
      warnings.push(`No activity for ${daysSinceActivity.toFixed(0)} days`);
    }
  } catch {
    warnings.push('Could not fetch contract info');
  }

  return {
    address: contract.address,
    isResponding,
    lastActivity,
    stateConsistent,
    warnings,
  };
}
```

### Migration Script Template

```typescript
interface MigrationPlan {
  sourceVersion: number;
  targetVersion: number;
  sourceAddress: string;
  steps: MigrationStep[];
}

interface MigrationStep {
  name: string;
  execute: () => Promise<void>;
  rollback?: () => Promise<void>;
}

async function executeMigration(plan: MigrationPlan): Promise<string> {
  console.log(`Migrating from v${plan.sourceVersion} to v${plan.targetVersion}`);

  const completedSteps: MigrationStep[] = [];

  try {
    for (const step of plan.steps) {
      console.log(`Executing: ${step.name}`);
      await step.execute();
      completedSteps.push(step);
    }

    console.log('Migration completed successfully');
    return 'success';
  } catch (error) {
    console.error('Migration failed, rolling back...');

    // Rollback in reverse order
    for (const step of completedSteps.reverse()) {
      if (step.rollback) {
        try {
          await step.rollback();
        } catch (rollbackError) {
          console.error(`Rollback failed for ${step.name}`);
        }
      }
    }

    throw error;
  }
}
```

### Graceful Deprecation

```typescript
async function deprecateContract(
  oldContract: ConnectedContract,
  newContractAddress: string
): Promise<void> {
  // 1. Set deprecation flag in old contract (if supported)
  try {
    await oldContract.call.set_deprecated({
      successor: newContractAddress,
    });
    console.log('Old contract marked as deprecated');
  } catch {
    console.log('Contract does not support deprecation flag');
  }

  // 2. Log deprecation for monitoring
  console.log(`Contract ${oldContract.address} deprecated`);
  console.log(`Successor: ${newContractAddress}`);

  // 3. Update documentation and client configurations
  // (manual step or integrate with your deployment system)
}
```

## State Inspection Queries

Common state inspection operations:

```typescript
// Get all accounts with balances
const accounts = await contract.query.get_all_accounts();

// Get contract metadata
const metadata = await contract.query.get_metadata();

// Get specific state field
const owner = await contract.query.get_owner();

// Get state at specific block (via indexer)
const historicalState = await indexer.getContractStateAtBlock(
  CONTRACT_ADDRESS,
  blockHeight
);
```

## Related Skills

- `contract-deployment` - Deploying new contract versions
- `contract-calling` - Interacting with contracts
- `midnight-indexer` plugin - Advanced state queries

## Related Commands

- `/midnight:check` - Verify environment configuration
