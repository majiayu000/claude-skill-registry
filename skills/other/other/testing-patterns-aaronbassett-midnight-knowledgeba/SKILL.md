---
name: midnight-dapp:testing-patterns
description: Use when writing unit tests for Midnight contract interaction code, integration testing without ZK proofs, E2E testing with Playwright or Cypress, or setting up CI/CD pipelines for Midnight DApps.
---

# Testing Patterns

Test Midnight DApps efficiently using mocked providers, simulated wallets, and testnet integration strategies.

## When to Use

- Writing unit tests for contract interaction code
- Integration testing without real ZK proof generation
- E2E testing with Playwright or Cypress
- Setting up CI/CD pipelines for Midnight DApps
- Testing wallet connection flows without browser extension
- Validating transaction flows before testnet deployment

## Key Concepts

### The Testing Challenge

Midnight DApps face unique testing challenges:

| Challenge | Why It Matters | Solution |
|-----------|----------------|----------|
| **Proof generation takes seconds** | Tests would be too slow | Mock proof providers |
| **Wallet requires browser extension** | Can't run in CI/CD | Mock wallet provider |
| **Private state is local only** | Hard to verify in tests | Controlled test state |
| **Testnet requires real infrastructure** | Flaky in automation | Mock for unit tests, testnet for E2E |

### Testing Pyramid for Midnight DApps

```
           E2E (Testnet)
          /            \
         /  Real proofs  \
        /   Real wallet   \
       /    Slow (~min)    \
      /____________________\
             |
     Integration (Mocked)
    /                      \
   /   Mock proof provider   \
  /    Mock wallet provider   \
 /      Fast (~seconds)        \
/______________________________\
            |
       Unit Tests
      /          \
     /  Pure logic  \
    /   No providers  \
   /   Fast (~ms)      \
  /____________________\
```

### Mock vs Real: When to Use Each

| Test Type | Proof Provider | Wallet Provider | Use Case |
|-----------|---------------|-----------------|----------|
| **Unit** | N/A | N/A | Pure business logic |
| **Component** | Mock | Mock | UI components |
| **Integration** | Mock | Mock | Contract interactions |
| **E2E (local)** | Mock | Mock | Full user flows |
| **E2E (testnet)** | Real | Real (Lace) | Pre-deployment validation |

## References

| Document | Description |
|----------|-------------|
| [mocking-proofs.md](references/mocking-proofs.md) | Mock proof provider for fast tests |
| [mock-wallet-provider.md](references/mock-wallet-provider.md) | Simulating Lace wallet in tests |
| [testnet-workflows.md](references/testnet-workflows.md) | E2E testing against testnet |
| [web3-comparison.md](references/web3-comparison.md) | Hardhat/Foundry testing vs Midnight |

## Examples

| Example | Description |
|---------|-------------|
| [mock-proof-context/](examples/mock-proof-context/) | Mock proof provider and test utilities |
| [mock-wallet/](examples/mock-wallet/) | Fake wallet implementation for tests |
| [e2e-testnet/](examples/e2e-testnet/) | Playwright E2E test against testnet |

## Quick Start

### 1. Install Test Dependencies

```bash
pnpm add -D vitest @testing-library/react @playwright/test msw
```

### 2. Create Mock Proof Provider

```typescript
import { createMockProofProvider } from "./mockProofProvider";

// Returns dummy proofs instantly (no ZK computation)
const mockProofProvider = createMockProofProvider({
  latencyMs: 10, // Simulate realistic timing
});
```

### 3. Create Mock Wallet

```typescript
import { MockWallet } from "./MockWallet";

const mockWallet = new MockWallet({
  address: "addr_test1qz_mock_address_for_testing_purposes_xyz",
  balance: 1000000n,
  network: "testnet",
});

// Inject into window for components that check window.midnight
globalThis.window = {
  midnight: { mnLace: mockWallet.connector },
};
```

### 4. Write a Test

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { MockWallet } from "./MockWallet";
import { createMockProofProvider } from "./mockProofProvider";
import { TransferButton } from "../TransferButton";

describe("TransferButton", () => {
  let mockWallet: MockWallet;
  let mockProofProvider: MockProofProvider;

  beforeEach(() => {
    mockWallet = new MockWallet({ balance: 1000n });
    mockProofProvider = createMockProofProvider();
  });

  it("should complete transfer with mocked providers", async () => {
    render(
      <TransferButton
        wallet={mockWallet.api}
        proofProvider={mockProofProvider}
        recipient="addr_test1..."
        amount={100n}
      />
    );

    fireEvent.click(screen.getByText("Transfer"));

    // No actual proof generation - instant!
    await screen.findByText("Transfer Complete");

    expect(mockWallet.getBalance()).toBe(900n);
  });
});
```

## Common Patterns

### Testing Contract State Reads

```typescript
import { describe, it, expect } from "vitest";
import { createMockContract } from "./testUtils";

describe("Contract State", () => {
  it("should read balance from contract state", async () => {
    const contract = createMockContract({
      state: {
        balances: new Map([["addr_test1...", 500n]]),
        totalSupply: 10000n,
      },
    });

    const balance = await contract.state.balances.get("addr_test1...");
    expect(balance).toBe(500n);
  });
});
```

### Testing Witness Execution

```typescript
import { describe, it, expect } from "vitest";
import { witnesses, createInitialPrivateState } from "../witnesses";

describe("Witnesses", () => {
  it("should return balance from private state", () => {
    const privateState = createInitialPrivateState(new Uint8Array(32));
    privateState.balance = 1000n;

    const context = { privateState, setPrivateState: () => {} };
    const balance = witnesses.get_balance(context);

    expect(balance).toBe(1000n);
  });

  it("should throw for expired credential", () => {
    const privateState = createInitialPrivateState(new Uint8Array(32));
    privateState.credentials.set("abc123", {
      expiry: BigInt(Date.now() / 1000 - 3600), // Expired 1 hour ago
      data: new Uint8Array(32),
    });

    const context = { privateState, setPrivateState: () => {} };

    expect(() =>
      witnesses.get_credential(context, hexToBytes("abc123"))
    ).toThrow("expired");
  });
});
```

### Testing Error Handling

```typescript
import { describe, it, expect, vi } from "vitest";
import { MockWallet } from "./MockWallet";

describe("Error Handling", () => {
  it("should handle user rejection", async () => {
    const wallet = new MockWallet();
    wallet.rejectNextTransaction("User rejected");

    await expect(
      wallet.api.submitTransaction(mockTx)
    ).rejects.toThrow("User rejected");
  });

  it("should handle proof server unavailable", async () => {
    const proofProvider = createMockProofProvider({
      shouldFail: true,
      errorMessage: "Proof server unavailable",
    });

    await expect(
      proofProvider.generateProof(mockCircuit, mockWitness)
    ).rejects.toThrow("Proof server unavailable");
  });
});
```

### Snapshot Testing for Disclosures

```typescript
import { describe, it, expect } from "vitest";
import { render } from "@testing-library/react";
import { DisclosureModal } from "../DisclosureModal";

describe("DisclosureModal", () => {
  it("should render disclosure summary correctly", () => {
    const disclosures = [
      { field: "age", label: "Your Age", value: "25" },
      { field: "country", label: "Country", value: "US" },
    ];

    const { container } = render(
      <DisclosureModal disclosures={disclosures} onConfirm={() => {}} />
    );

    expect(container).toMatchSnapshot();
  });
});
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Midnight DApp

on: [push, pull_request]

jobs:
  unit-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm test:unit
      - run: pnpm test:integration

  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm exec playwright install --with-deps

      # E2E with mocks - fast, reliable
      - run: pnpm test:e2e:mock

      # Optional: E2E with testnet (slower, requires secrets)
      # - run: pnpm test:e2e:testnet
      #   env:
      #     TESTNET_FAUCET_KEY: ${{ secrets.TESTNET_FAUCET_KEY }}
```

## Related Skills

- `proof-handling` - Understanding what to mock in proof generation
- `wallet-integration` - Understanding Lace wallet API to mock
- `error-handling` - Testing error scenarios
- `state-management` - Testing state synchronization

## Related Commands

- `/dapp-check` - Validates test configuration
- `/dapp-debug tests` - Diagnose test failures
