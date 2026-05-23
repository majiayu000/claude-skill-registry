---
name: Bankr x402 SDK - Client Patterns
description: This skill should be used when the user asks to "implement Bankr SDK client", "write bankr-client.ts", "create SDK client setup", "common files for SDK project", "package.json for Bankr SDK", "tsconfig for Bankr", "SDK TypeScript patterns", "execute SDK transactions", or needs the reusable client code and common project files for Bankr SDK integrations.
version: 1.0.0
---

# x402 SDK Client Patterns

Reusable client code and common files for Bankr SDK projects.

## bankr-client.ts

The core SDK client module for all Bankr SDK projects:

```typescript
import "dotenv/config";
import { BankrClient } from "@bankr/sdk";

// ============================================
// Validation
// ============================================

if (!process.env.BANKR_PRIVATE_KEY) {
  throw new Error(
    "BANKR_PRIVATE_KEY environment variable is required. " +
      "This wallet pays $0.01 USDC per request (needs USDC on Base)."
  );
}

// ============================================
// Client Setup
// ============================================

/**
 * Bankr SDK Client
 *
 * Provides AI-powered Web3 operations with x402 micropayments.
 * Each API request costs $0.01 USDC (paid from payment wallet on Base).
 *
 * @example
 * ```typescript
 * import { bankrClient } from "./bankr-client";
 *
 * // Token swap
 * const swap = await bankrClient.promptAndWait({
 *   prompt: "Swap 0.1 ETH to USDC on Base",
 * });
 *
 * // Check balances
 * const balances = await bankrClient.promptAndWait({
 *   prompt: "What are my token balances?",
 * });
 * ```
 *
 * @see https://www.npmjs.com/package/@bankr/sdk
 */
export const bankrClient = new BankrClient({
  // Required: Payment wallet private key
  // This wallet pays $0.01 USDC per API request (must have USDC on Base)
  privateKey: process.env.BANKR_PRIVATE_KEY as `0x${string}`,

  // Optional: Override receiving wallet address
  // If not set, tokens are sent to the payment wallet address
  walletAddress: process.env.BANKR_WALLET_ADDRESS,

  // Optional: API endpoint (defaults to production)
  ...(process.env.BANKR_API_URL && { baseUrl: process.env.BANKR_API_URL }),
});

// Export the wallet address for reference
export const walletAddress = bankrClient.getWalletAddress();

// ============================================
// Types (re-exported from SDK)
// ============================================

export type { JobStatusResponse, Transaction } from "@bankr/sdk";
```

---

## executor.ts

Transaction execution helper using viem:

```typescript
import { createWalletClient, http, type WalletClient } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { base, mainnet, polygon } from "viem/chains";
import type { Transaction } from "@bankr/sdk";

// Chain configuration
const chains = {
  8453: base,
  1: mainnet,
  137: polygon,
} as const;

// Create wallet client for transaction execution
const account = privateKeyToAccount(
  process.env.BANKR_PRIVATE_KEY as `0x${string}`
);

function getWalletClient(chainId: number): WalletClient {
  const chain = chains[chainId as keyof typeof chains];
  if (!chain) {
    throw new Error(`Unsupported chain ID: ${chainId}`);
  }

  return createWalletClient({
    account,
    chain,
    transport: http(),
  });
}

/**
 * Execute a transaction returned by the Bankr SDK
 *
 * @example
 * ```typescript
 * const result = await bankrClient.promptAndWait({
 *   prompt: "Swap 0.1 ETH to USDC",
 * });
 *
 * if (result.transactions?.length) {
 *   const hash = await executeTransaction(result.transactions[0]);
 *   console.log("Transaction:", hash);
 * }
 * ```
 */
export async function executeTransaction(tx: Transaction): Promise<string> {
  const txData = tx.metadata.transaction;
  const client = getWalletClient(txData.chainId);

  console.log(`Executing ${tx.type} on chain ${txData.chainId}...`);

  const hash = await client.sendTransaction({
    to: txData.to as `0x${string}`,
    data: txData.data as `0x${string}`,
    value: BigInt(txData.value || "0"),
    gas: BigInt(txData.gas),
  });

  console.log(`Transaction submitted: ${hash}`);
  return hash;
}

/**
 * Execute all transactions from a Bankr result
 */
export async function executeAllTransactions(
  transactions: Transaction[]
): Promise<string[]> {
  const hashes: string[] = [];

  for (const tx of transactions) {
    const hash = await executeTransaction(tx);
    hashes.push(hash);
  }

  return hashes;
}
```

---

## Common Files

### package.json

Base package.json for all Bankr SDK projects:

```json
{
  "name": "{project-name}",
  "version": "0.1.0",
  "description": "{description}",
  "type": "module",
  "main": "dist/index.js",
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx src/index.ts"
  },
  "dependencies": {
    "@bankr/sdk": "^1.0.0",
    "dotenv": "^16.3.1",
    "viem": "^2.0.0"
  },
  "devDependencies": {
    "@types/node": "^20.10.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.0"
  }
}
```

#### Framework-Specific Dependencies

Add based on project template:

**Web Service (Express):**
```json
"dependencies": {
  "express": "^4.18.0"
},
"devDependencies": {
  "@types/express": "^4.17.21"
}
```

**CLI:**
```json
"dependencies": {
  "commander": "^12.0.0"
}
```

---

### tsconfig.json

TypeScript configuration:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

---

### .env.example

Environment variables template:

```bash
# Bankr SDK Configuration
# See: https://docs.bankr.bot

# Required: Payment wallet private key
# This wallet pays $0.01 USDC per API request (must have USDC on Base)
# Format: 64 hex characters with 0x prefix
BANKR_PRIVATE_KEY=0x

# Optional: Receiving wallet address
# Tokens from swaps/purchases go here. Defaults to payment wallet if not set.
# BANKR_WALLET_ADDRESS=0x

# Optional: API endpoint override (defaults to https://api.bankr.bot)
# BANKR_API_URL=https://api.bankr.bot
```

---

### .gitignore

Standard ignore patterns:

```
# Dependencies
node_modules/

# Build output
dist/

# Environment
.env
.env.local
.env.*.local

# Logs
*.log
npm-debug.log*

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Testing
coverage/
```

---

## Usage Patterns

### Basic Usage

```typescript
import { bankrClient } from "./bankr-client";

const result = await bankrClient.promptAndWait({
  prompt: "What is the price of ETH?",
  onStatusUpdate: (msg) => console.log("Progress:", msg),
});

console.log(result.response);
```

### With Transaction Execution

```typescript
import { bankrClient } from "./bankr-client";
import { executeTransaction } from "./executor";

const result = await bankrClient.promptAndWait({
  prompt: "Swap 0.1 ETH to USDC on Base",
});

if (result.status === "completed" && result.transactions?.length) {
  // Review before executing
  console.log("Transaction ready:", result.transactions[0].type);
  console.log("Details:", result.transactions[0].metadata.__ORIGINAL_TX_DATA__);

  // Execute
  const hash = await executeTransaction(result.transactions[0]);
  console.log("Executed:", hash);
}
```

### With Error Handling

```typescript
import { bankrClient } from "./bankr-client";
import { executeAllTransactions } from "./executor";

async function performSwap(prompt: string) {
  try {
    const result = await bankrClient.promptAndWait({
      prompt,
      onStatusUpdate: console.log,
    });

    if (result.status === "completed") {
      console.log("Success:", result.response);

      if (result.transactions?.length) {
        const hashes = await executeAllTransactions(result.transactions);
        console.log("Transactions:", hashes);
      }
    } else if (result.status === "failed") {
      console.error("Failed:", result.error);
    }
  } catch (error) {
    console.error("Error:", error.message);
  }
}
```

### Query Without Transactions

```typescript
import { bankrClient } from "./bankr-client";

// Balance queries don't return transactions
const balances = await bankrClient.promptAndWait({
  prompt: "What are my balances on Base?",
});

console.log(balances.response);

// Price queries
const price = await bankrClient.promptAndWait({
  prompt: "Price of DEGEN",
});

console.log(price.response);
```

---

## SDK Reference

Consult the `sdk-capabilities` skill for:
- Complete operation reference
- Supported chains and tokens
- Example prompts for each operation

Consult the `sdk-token-swaps` skill for:
- Swap patterns and approval handling
- Transaction execution details
