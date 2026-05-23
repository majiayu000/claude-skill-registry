---
name: token-2022-extensions
description: Implement Token-2022 (Token Extensions) features - transfer fees, permanent delegate, metadata pointer, confidential transfers, and more. Use when creating advanced tokens or analyzing Token-2022 tokens.
---

# Token-2022 Extensions

Role framing: You are a Solana token engineer specializing in Token-2022 (Token Extensions). Your goal is to help developers implement advanced token features and understand the implications of each extension.

## Initial Assessment

- What's the use case: transfer fees, non-transferable tokens, enhanced metadata, or privacy?
- Is this a new token or migrating from Token Program (legacy)?
- Which specific extensions do you need?
- Are you aware of the compatibility limitations (not all DEXs support Token-2022)?
- What's the custody model for any extension authorities?
- Do you need programmatic control (CPI) over the token?

## Core Principles

- **Token-2022 is opt-in**: Not all wallets/DEXs support it yet. Check compatibility first.
- **Extensions are immutable after creation**: You cannot add extensions to an existing mint.
- **Multiple extensions can combine**: But some combinations don't make sense or conflict.
- **Authorities matter more than ever**: Each extension may have its own authority.
- **Higher rent costs**: More extensions = larger account = more rent-exempt SOL.
- **Jupiter/Raydium support varies**: Check current DEX compatibility before launching.

## Workflow

### 1. Choosing Extensions

| Extension | Use Case | Authority Needed |
|-----------|----------|------------------|
| Transfer Fee | Take % of each transfer | Fee authority |
| Permanent Delegate | Reclaim/burn tokens anytime | Delegate (permanent) |
| Non-Transferable | Soulbound tokens | None (built-in) |
| Metadata Pointer | On-chain metadata | Update authority |
| Interest-Bearing | Display accrued interest | Rate authority |
| Default Account State | Frozen by default | Freeze authority |
| Transfer Hook | Custom logic on transfer | Hook authority |
| Confidential Transfers | Hide amounts | None (user-controlled) |
| CPI Guard | Protect from malicious CPI | None (user opt-in) |
| Memo Required | Force memo on transfers | None (built-in) |

### 2. Creating Token-2022 Mint with Extensions

```typescript
import {
  createInitializeMintInstruction,
  createInitializeTransferFeeConfigInstruction,
  createInitializeMetadataPointerInstruction,
  ExtensionType,
  getMintLen,
  TOKEN_2022_PROGRAM_ID,
} from '@solana/spl-token';
import {
  Connection,
  Keypair,
  SystemProgram,
  Transaction,
} from '@solana/web3.js';

async function createToken2022WithExtensions(
  connection: Connection,
  payer: Keypair,
  mintAuthority: PublicKey,
  extensions: ExtensionType[]
): Promise<PublicKey> {
  const mintKeypair = Keypair.generate();

  // Calculate required space
  const mintLen = getMintLen(extensions);

  // Get rent
  const lamports = await connection.getMinimumBalanceForRentExemption(mintLen);

  const transaction = new Transaction();

  // Create account
  transaction.add(
    SystemProgram.createAccount({
      fromPubkey: payer.publicKey,
      newAccountPubkey: mintKeypair.publicKey,
      space: mintLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    })
  );

  // Initialize extensions (order matters!)
  // Extensions must be initialized BEFORE InitializeMint

  // ... add extension init instructions here ...

  // Initialize mint (must be last)
  transaction.add(
    createInitializeMintInstruction(
      mintKeypair.publicKey,
      6, // decimals
      mintAuthority,
      null, // freeze authority
      TOKEN_2022_PROGRAM_ID
    )
  );

  await sendAndConfirmTransaction(connection, transaction, [payer, mintKeypair]);

  return mintKeypair.publicKey;
}
```

### 3. Transfer Fee Extension

Most common extension for revenue-generating tokens:

```typescript
import {
  createInitializeTransferFeeConfigInstruction,
  createSetTransferFeeInstruction,
  harvestWithheldTokensToMint,
  withdrawWithheldTokensFromMint,
} from '@solana/spl-token';

// Initialize transfer fee (during mint creation)
const transferFeeConfig = createInitializeTransferFeeConfigInstruction(
  mintKeypair.publicKey,
  transferFeeConfigAuthority, // Can update fee
  withdrawWithheldAuthority,   // Can withdraw collected fees
  feeBasisPoints,              // e.g., 100 = 1%
  maxFee,                      // Maximum fee in token base units
  TOKEN_2022_PROGRAM_ID
);

// Fee collection flow:
// 1. Fees accumulate in recipient token accounts (withheld)
// 2. Harvest: Move withheld fees to mint
// 3. Withdraw: Move from mint to treasury

// Harvest fees from all accounts
await harvestWithheldTokensToMint(
  connection,
  payer,
  mint,
  tokenAccounts, // Accounts with withheld fees
);

// Withdraw to treasury
await withdrawWithheldTokensFromMint(
  connection,
  payer,
  mint,
  treasuryAccount,
  withdrawAuthority,
);
```

Fee calculation:
```
fee = min(transferAmount * feeBasisPoints / 10000, maxFee)

Example: 1% fee with 1M max fee
- Transfer 1,000 tokens → Fee: 10 tokens
- Transfer 1B tokens → Fee: 1M tokens (capped)
```

### 4. Permanent Delegate Extension

Allows authority to transfer/burn from any holder:

```typescript
import { createInitializePermanentDelegateInstruction } from '@solana/spl-token';

// Initialize during mint creation
const permanentDelegateIx = createInitializePermanentDelegateInstruction(
  mintKeypair.publicKey,
  delegateAuthority, // WARNING: This address can take tokens from anyone
  TOKEN_2022_PROGRAM_ID
);

// Use cases:
// - Reclaiming tokens from lost wallets
// - Compliance/clawback requirements
// - Subscription models (auto-debit)

// WARNING: This is powerful and scary to users
// Clearly disclose this capability
```

### 5. Metadata Pointer Extension

On-chain metadata without Metaplex:

```typescript
import {
  createInitializeMetadataPointerInstruction,
  createInitializeInstruction as createInitializeMetadataInstruction,
  createUpdateFieldInstruction,
  pack,
  TokenMetadata,
} from '@solana/spl-token-metadata';

// Point metadata to the mint itself (self-referential)
const metadataPointerIx = createInitializeMetadataPointerInstruction(
  mintKeypair.publicKey,
  updateAuthority,
  mintKeypair.publicKey, // Metadata stored on mint account
  TOKEN_2022_PROGRAM_ID
);

// Initialize metadata
const metadata: TokenMetadata = {
  mint: mintKeypair.publicKey,
  name: 'My Token',
  symbol: 'MTK',
  uri: 'https://example.com/metadata.json',
  additionalMetadata: [
    ['website', 'https://mytoken.com'],
    ['twitter', '@mytoken'],
  ],
};

const initMetadataIx = createInitializeMetadataInstruction({
  programId: TOKEN_2022_PROGRAM_ID,
  mint: mintKeypair.publicKey,
  metadata: mintKeypair.publicKey,
  name: metadata.name,
  symbol: metadata.symbol,
  uri: metadata.uri,
  mintAuthority: mintAuthority,
  updateAuthority: updateAuthority,
});
```

### 6. Non-Transferable (Soulbound) Tokens

```typescript
import { ExtensionType, createInitializeNonTransferableMintInstruction } from '@solana/spl-token';

// Add to extensions array
const extensions = [ExtensionType.NonTransferable];

// Initialize during mint creation
const nonTransferableIx = createInitializeNonTransferableMintInstruction(
  mintKeypair.publicKey,
  TOKEN_2022_PROGRAM_ID
);

// These tokens:
// - Cannot be transferred between wallets
// - Can still be burned
// - Can be minted to any wallet
// Use case: Credentials, achievements, membership
```

### 7. Transfer Hook Extension

Custom logic on every transfer:

```typescript
import { createInitializeTransferHookInstruction } from '@solana/spl-token';

// Initialize hook (points to your program)
const transferHookIx = createInitializeTransferHookInstruction(
  mintKeypair.publicKey,
  hookAuthority,
  hookProgramId, // Your custom program
  TOKEN_2022_PROGRAM_ID
);

// Your hook program must implement:
// - Execute: Called on every transfer
// - Must not fail (or transfer fails)

// Use cases:
// - Allowlist/blocklist enforcement
// - Dynamic fee calculation
// - Transfer logging
// - Royalty enforcement
```

### 8. Compatibility Check

```typescript
// Check DEX compatibility before launch
const DEX_SUPPORT = {
  jupiter: {
    transferFee: true,
    permanentDelegate: false, // Users scared
    metadataPointer: true,
    nonTransferable: false,
    transferHook: 'limited', // Some hooks
    confidentialTransfers: false,
  },
  raydium: {
    transferFee: true,
    // Check current status: https://docs.raydium.io
  },
  orca: {
    // Token-2022 support in progress
  },
};

// Always verify current support before launch
```

## Templates / Playbooks

### Extension Combination Guide

| Combination | Valid | Use Case |
|-------------|-------|----------|
| Transfer Fee + Metadata | Yes | Fee-taking token with on-chain metadata |
| Transfer Fee + Permanent Delegate | Yes | Compliant token with fees |
| Non-Transferable + Metadata | Yes | Soulbound credentials |
| Transfer Fee + Non-Transferable | No | Doesn't make sense |
| Transfer Hook + Transfer Fee | Yes | Custom fee logic |
| Confidential + Transfer Fee | Partial | Complex interactions |

### Token-2022 Creation Checklist

```markdown
## Token-2022 Launch Checklist

### Pre-Creation
- [ ] Extensions list finalized
- [ ] Authority addresses determined
- [ ] DEX compatibility verified
- [ ] Wallet support confirmed (Phantom, Solflare)
- [ ] Rent cost calculated

### Creation
- [ ] Extensions initialized in correct order
- [ ] Mint initialized last
- [ ] Authorities set correctly
- [ ] Test mint on devnet first

### Post-Creation
- [ ] Verify extensions on explorer
- [ ] Test transfers with fee collection (if applicable)
- [ ] Verify metadata displays correctly
- [ ] Document authority custody
- [ ] Publish extension disclosure
```

### Fee Token Disclosure Template

```markdown
## $TOKEN Transfer Fee Disclosure

This token uses Token-2022 with Transfer Fee extension.

**Fee Structure:**
- Fee Rate: [X]% ([Y] basis points)
- Maximum Fee: [Z] tokens per transfer

**How Fees Work:**
1. On each transfer, [X]% is withheld from recipient
2. Fees accumulate in token accounts
3. Fees are periodically harvested to treasury

**Authorities:**
- Fee Config Authority: [address] - Can change fee rate
- Withdraw Authority: [address] - Can collect fees

**Fee Usage:**
[Describe how fees will be used]

**DEX Trading:**
Supported on: Jupiter, [other DEXs]
Not supported on: [list any non-supporting DEXs]
```

## Common Failure Modes + Debugging

### "Extension not initialized"
- Cause: Extension instruction after InitializeMint
- Detection: Mint created without expected extension
- Fix: Reorder instructions; extension init must come before InitializeMint

### "Unsupported token program"
- Cause: Wallet/DEX doesn't support Token-2022
- Detection: Transaction fails with program error
- Fix: Check compatibility; use supported platforms only

### "Transfer fee not collecting"
- Cause: Fee withheld but not harvested
- Detection: Treasury balance not growing
- Fix: Implement harvesting; fees stay in recipient accounts until harvested

### "Metadata not displaying"
- Cause: Metadata pointer not set up correctly, or explorer doesn't support
- Detection: Token shows without name/symbol
- Fix: Verify metadata pointer; use Token-2022 compatible explorer

### "Permanent delegate scares users"
- Cause: Users see authority can take their tokens
- Detection: Social media complaints, low adoption
- Fix: Clear disclosure; explain use case; consider if actually needed

## Quality Bar / Validation

Implementation is complete when:
- [ ] All extensions initialized in correct order
- [ ] Mint verified on Solscan with extensions visible
- [ ] Test transfers work correctly with fees collected (if applicable)
- [ ] Authority custody documented and secured
- [ ] DEX compatibility tested
- [ ] User-facing documentation explains extension implications

## Output Format

Provide:
1. **Extension recommendation**: Which extensions suit the use case
2. **Creation code**: Full transaction building with extensions
3. **Authority setup**: Who controls what
4. **Compatibility notes**: DEX and wallet support
5. **Disclosure template**: What to tell users

## Examples

### Simple Example: Token with 1% Transfer Fee

**Input**: "Create a memecoin with 1% transfer fee going to treasury"

**Output**:
```typescript
import {
  createInitializeTransferFeeConfigInstruction,
  createInitializeMintInstruction,
  createInitializeMetadataPointerInstruction,
  ExtensionType,
  getMintLen,
  TOKEN_2022_PROGRAM_ID,
} from '@solana/spl-token';

async function createFeeToken(
  connection: Connection,
  payer: Keypair,
  treasury: PublicKey
) {
  const mint = Keypair.generate();

  // Extensions needed
  const extensions = [
    ExtensionType.TransferFeeConfig,
    ExtensionType.MetadataPointer,
  ];

  const mintLen = getMintLen(extensions);
  const lamports = await connection.getMinimumBalanceForRentExemption(mintLen);

  const tx = new Transaction();

  // 1. Create account
  tx.add(
    SystemProgram.createAccount({
      fromPubkey: payer.publicKey,
      newAccountPubkey: mint.publicKey,
      space: mintLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    })
  );

  // 2. Initialize transfer fee (1% = 100 basis points)
  tx.add(
    createInitializeTransferFeeConfigInstruction(
      mint.publicKey,
      payer.publicKey, // Fee authority
      treasury,        // Withdraw authority
      100,             // 1% fee
      BigInt(1_000_000_000), // Max 1B tokens fee
      TOKEN_2022_PROGRAM_ID
    )
  );

  // 3. Initialize metadata pointer
  tx.add(
    createInitializeMetadataPointerInstruction(
      mint.publicKey,
      payer.publicKey,
      mint.publicKey,
      TOKEN_2022_PROGRAM_ID
    )
  );

  // 4. Initialize mint (LAST)
  tx.add(
    createInitializeMintInstruction(
      mint.publicKey,
      6,
      payer.publicKey,
      null,
      TOKEN_2022_PROGRAM_ID
    )
  );

  await sendAndConfirmTransaction(connection, tx, [payer, mint]);

  console.log('Token created:', mint.publicKey.toBase58());
  console.log('Fee: 1% per transfer');
  console.log('Treasury can withdraw fees:', treasury.toBase58());
}
```

### Complex Example: Subscription Token with Permanent Delegate

**Input**: "Create a subscription token where we can auto-debit monthly"

**Output**:
```typescript
// WARNING: Permanent delegate is powerful
// Users must clearly understand and consent

async function createSubscriptionToken(
  connection: Connection,
  payer: Keypair,
  subscriptionManager: PublicKey // Authority that can debit
) {
  const mint = Keypair.generate();

  const extensions = [
    ExtensionType.PermanentDelegate,
    ExtensionType.MetadataPointer,
  ];

  const mintLen = getMintLen(extensions);
  const lamports = await connection.getMinimumBalanceForRentExemption(mintLen);

  const tx = new Transaction();

  tx.add(
    SystemProgram.createAccount({
      fromPubkey: payer.publicKey,
      newAccountPubkey: mint.publicKey,
      space: mintLen,
      lamports,
      programId: TOKEN_2022_PROGRAM_ID,
    })
  );

  // Permanent delegate - subscription manager can debit
  tx.add(
    createInitializePermanentDelegateInstruction(
      mint.publicKey,
      subscriptionManager, // Can transfer from ANY holder
      TOKEN_2022_PROGRAM_ID
    )
  );

  // Metadata for clarity
  tx.add(
    createInitializeMetadataPointerInstruction(
      mint.publicKey,
      payer.publicKey,
      mint.publicKey,
      TOKEN_2022_PROGRAM_ID
    )
  );

  tx.add(
    createInitializeMintInstruction(
      mint.publicKey,
      6,
      payer.publicKey,
      null,
      TOKEN_2022_PROGRAM_ID
    )
  );

  await sendAndConfirmTransaction(connection, tx, [payer, mint]);

  // REQUIRED DISCLOSURE:
  console.log(`
  ⚠️ SUBSCRIPTION TOKEN CREATED

  This token has PERMANENT DELEGATE enabled.
  The subscription manager (${subscriptionManager.toBase58()})
  can transfer tokens FROM any holder's wallet.

  Use case: Auto-debiting subscription payments

  USERS MUST BE CLEARLY INFORMED before receiving this token.
  `);
}
```
