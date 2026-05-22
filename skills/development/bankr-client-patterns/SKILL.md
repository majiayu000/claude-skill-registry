---
name: Bankr Dev - Client Patterns
description: This skill should be used when the user asks to "implement Bankr client", "write bankr-client.ts", "create API client for Bankr", "common files for Bankr project", "package.json for Bankr", "tsconfig for Bankr", "Bankr TypeScript patterns", "Bankr response types", or needs the reusable client code and common project files for Bankr API integrations.
version: 1.0.0
---

# Bankr Client Patterns

Reusable client code and common files for Bankr API projects.

## bankr-client.ts

The core API client module for all Bankr projects:

```typescript
import "dotenv/config";

const API_URL = process.env.BANKR_API_URL || "https://api.bankr.bot";
const API_KEY = process.env.BANKR_API_KEY;

// ============================================
// Types
// ============================================

export type JobStatus = "pending" | "processing" | "completed" | "failed" | "cancelled";

export interface JobStatusResponse {
  success: boolean;
  jobId: string;
  status: JobStatus;
  prompt: string;
  response?: string;
  transactions?: Transaction[];
  richData?: RichData[];
  statusUpdates?: StatusUpdate[];
  error?: string;
  createdAt: string;
  startedAt?: string;
  completedAt?: string;
  cancelledAt?: string;
  processingTime?: number;
  cancellable?: boolean;
}

export interface StatusUpdate {
  message: string;
  timestamp: string;
}

// Transaction types
export type Transaction =
  | SwapTransaction
  | ApprovalTransaction
  | TransferErc20Transaction
  | TransferEthTransaction
  | ConvertEthToWethTransaction
  | ConvertWethToEthTransaction
  | TransferNftTransaction
  | MintManifoldNftTransaction
  | MintSeaDropNftTransaction
  | BuyNftTransaction
  | AvantisTradeTransaction
  | SwapCrossChainTransaction
  | ManageBankrStakingTransaction;

interface BaseTransactionMetadata {
  __ORIGINAL_TX_DATA__: {
    chain: string;
    humanReadableMessage: string;
    inputTokenAddress: string;
    inputTokenAmount: string;
    inputTokenTicker: string;
    outputTokenAddress: string;
    outputTokenTicker: string;
    receiver: string;
  };
  transaction: {
    chainId: number;
    to: string;
    data: string;
    gas: string;
    gasPrice: string;
    value: string;
  };
}

export interface SwapTransaction {
  type: "swap";
  metadata: BaseTransactionMetadata & {
    approvalRequired?: boolean;
    approvalTx?: { to: string; data: string };
    permit2?: object;
  };
}

export interface ApprovalTransaction {
  type: "approval";
  metadata: BaseTransactionMetadata;
}

export interface TransferErc20Transaction {
  type: "transfer_erc20";
  metadata: BaseTransactionMetadata;
}

export interface TransferEthTransaction {
  type: "transfer_eth";
  metadata: BaseTransactionMetadata;
}

export interface ConvertEthToWethTransaction {
  type: "convert_eth_to_weth";
  metadata: BaseTransactionMetadata;
}

export interface ConvertWethToEthTransaction {
  type: "convert_weth_to_eth";
  metadata: BaseTransactionMetadata;
}

export interface TransferNftTransaction {
  type: "transfer_nft";
  metadata: BaseTransactionMetadata;
}

export interface MintManifoldNftTransaction {
  type: "mint_manifold_nft";
  metadata: BaseTransactionMetadata;
}

export interface MintSeaDropNftTransaction {
  type: "mint_seadrop_nft";
  metadata: BaseTransactionMetadata;
}

export interface BuyNftTransaction {
  type: "buy_nft";
  metadata: BaseTransactionMetadata;
}

export interface AvantisTradeTransaction {
  type: "avantisTrade";
  metadata: {
    chainId: number;
    description: string;
    to: string;
    data: string;
    value?: string;
  };
}

export interface SwapCrossChainTransaction {
  type: "swapCrossChain";
  metadata: {
    chainId: number;
    description: string;
    to: string;
    data: string;
    value: string;
  };
}

export interface ManageBankrStakingTransaction {
  type: "manage_bankr_staking";
  metadata: {
    chainId: number;
    description: string;
    to: string;
    data: string;
    value?: string;
  };
}

// Rich data types
export type RichData = SocialCard | Chart;

export interface SocialCard {
  type: "social-card";
  variant: "analysis";
  text: string;
}

export interface Chart {
  type: "chart";
  url: string;
}

// ============================================
// API Functions
// ============================================

export async function submitPrompt(prompt: string): Promise<{ jobId: string }> {
  if (!API_KEY) {
    throw new Error("BANKR_API_KEY not set. Get one at https://bankr.bot/api");
  }

  const response = await fetch(`${API_URL}/agent/prompt`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ prompt }),
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  const data = await response.json();
  if (!data.success) {
    throw new Error(data.error || "Failed to submit prompt");
  }

  return { jobId: data.jobId };
}

export async function getJobStatus(jobId: string): Promise<JobStatusResponse> {
  if (!API_KEY) {
    throw new Error("BANKR_API_KEY not set");
  }

  const response = await fetch(`${API_URL}/agent/job/${jobId}`, {
    headers: { "x-api-key": API_KEY },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  return response.json();
}

export async function cancelJob(jobId: string): Promise<JobStatusResponse> {
  if (!API_KEY) {
    throw new Error("BANKR_API_KEY not set");
  }

  const response = await fetch(`${API_URL}/agent/job/${jobId}/cancel`, {
    method: "POST",
    headers: {
      "x-api-key": API_KEY,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    const text = await response.text();
    throw new Error(`API error ${response.status}: ${text}`);
  }

  return response.json();
}

export async function waitForCompletion(
  jobId: string,
  onProgress?: (message: string) => void,
  options?: { pollInterval?: number; maxAttempts?: number }
): Promise<JobStatusResponse> {
  const pollInterval = options?.pollInterval || 2000;
  const maxAttempts = options?.maxAttempts || 150; // 5 minutes max
  let lastUpdateCount = 0;

  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    const status = await getJobStatus(jobId);

    // Report new status updates
    if (onProgress && status.statusUpdates) {
      for (let i = lastUpdateCount; i < status.statusUpdates.length; i++) {
        onProgress(status.statusUpdates[i].message);
      }
      lastUpdateCount = status.statusUpdates.length;
    }

    // Check for terminal states
    if (["completed", "failed", "cancelled"].includes(status.status)) {
      return status;
    }

    await new Promise((resolve) => setTimeout(resolve, pollInterval));
  }

  throw new Error("Job timed out after maximum attempts");
}

/**
 * Execute a Bankr prompt and wait for completion
 * Convenience function that combines submit + poll
 */
export async function execute(
  prompt: string,
  onProgress?: (message: string) => void
): Promise<JobStatusResponse> {
  const { jobId } = await submitPrompt(prompt);
  onProgress?.(`Job submitted: ${jobId}`);
  return waitForCompletion(jobId, onProgress);
}
```

---

## Common Files

### package.json

Base package.json for all Bankr projects:

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
    "dotenv": "^16.3.1"
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

**Web Service (Fastify):**
```json
"dependencies": {
  "fastify": "^4.25.0"
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
# Bankr API Configuration
BANKR_API_KEY=bk_your_api_key_here
BANKR_API_URL=https://api.bankr.bot

# Optional: Wallet address for context
BANKR_WALLET_ADDRESS=0x...
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
import { execute } from "./bankr-client";

const result = await execute("What is the price of ETH?", (msg) => {
  console.log("Progress:", msg);
});

console.log(result.response);
```

### With Error Handling

```typescript
import { execute } from "./bankr-client";

try {
  const result = await execute("Buy $50 of ETH on Base");

  if (result.status === "completed") {
    console.log("Success:", result.response);

    // Handle transactions
    if (result.transactions) {
      for (const tx of result.transactions) {
        console.log(`${tx.type}:`, tx.metadata.__ORIGINAL_TX_DATA__?.humanReadableMessage);
      }
    }
  } else if (result.status === "failed") {
    console.error("Failed:", result.error);
  }
} catch (error) {
  console.error("Error:", error.message);
}
```

### Manual Control

```typescript
import { submitPrompt, waitForCompletion, cancelJob } from "./bankr-client";

// Submit
const { jobId } = await submitPrompt("Analyze ETH market");

// Set up timeout
const timeout = setTimeout(() => {
  cancelJob(jobId);
}, 120000);

// Wait with custom options
const result = await waitForCompletion(jobId, console.log, {
  pollInterval: 2000,
  maxAttempts: 60,
});

clearTimeout(timeout);
```

---

## API Reference

Consult the `bankr-api-basics` skill for:
- Complete endpoint documentation
- Authentication details
- Response field descriptions
- Error codes and handling
