---
name: ts-sdk-address
description:
  "How to create and use AccountAddress in @aptos-labs/ts-sdk. Covers address format (AIP-40),
  from/fromString/fromStrict, special addresses, LONG vs SHORT form, and derived addresses (object, resource, token,
  user-derived). Triggers on: 'AccountAddress', 'AccountAddress.from', 'AIP-40', 'derived address',
  'createObjectAddress', 'createResourceAddress', 'createTokenAddress'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "address", "account-address", "aip-40"]
  priority: high
---

# TypeScript SDK: AccountAddress

## Purpose

Guide correct creation, parsing, and formatting of **account addresses** in `@aptos-labs/ts-sdk`. Addresses are 32-byte
values; string format follows **AIP-40**.

## ALWAYS

1. **Use `AccountAddress.from()` for flexible input** – accepts string (with or without `0x`), `Uint8Array`, or existing
   `AccountAddress`.
2. **Use addresses as `AccountAddress` or string in API** – SDK accepts `AccountAddressInput` (string or
   `AccountAddress`) in most APIs.
3. **Use `AccountAddress.fromStringStrict()` / `AccountAddress.fromStrict()`** when you need AIP-40 strict: LONG (0x +
   64 hex chars) or SHORT only for special (0x0–0xf).
4. **Use derived address helpers** from the SDK for object/resource/token addresses – do not hand-roll hashing.

## NEVER

1. **Do not use raw strings for comparison** – use `addr.equals(other)` or normalize with `AccountAddress.from()`.
2. **Do not assume SHORT form for non-special addresses** – non-special addresses must be LONG (64 hex chars) in strict
   mode.
3. **Do not use the `Hex` class for account addresses** – use `AccountAddress` only (per SDK docs).

---

## Address format (AIP-40)

- **Length:** 32 bytes (64 hex chars in LONG form).
- **String:** Must start with `0x`. LONG = `0x` + 64 hex chars; SHORT = shortest form (e.g. `0x1`, `0xf`).
- **Special addresses:** `0x0`–`0xf` (last byte &lt; 16, rest zero). These may be written in SHORT form (`0x1`, `0xa`).
- **Reference:** [AIP-40](https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-40.md).

---

## Creating AccountAddress

### From string (recommended: relaxed)

```typescript
import { AccountAddress } from "@aptos-labs/ts-sdk";

// Relaxed: accepts with or without 0x, SHORT or LONG
const addr1 = AccountAddress.from("0x1");
const addr2 = AccountAddress.from("0xaa86fe99004361f747f91342ca13c426ca0cccb0c1217677180c9493bad6ef0c");
const addr3 = AccountAddress.from("1"); // no 0x ok
```

### From string (strict AIP-40)

```typescript
// Strict: LONG (0x + 64 chars) or SHORT only for special (0x0–0xf)
const addrStrict = AccountAddress.fromStringStrict(
  "0x0000000000000000000000000000000000000000000000000000000000000001"
);
// Or use fromStrict for any AccountAddressInput
const a = AccountAddress.fromStrict("0x1"); // ok: special address in SHORT form
```

### From bytes

```typescript
const bytes = new Uint8Array(32);
bytes[31] = 1;
const addr = new AccountAddress(bytes);
// or
const addrFrom = AccountAddress.from(bytes);
```

### Built-in constants

```typescript
AccountAddress.ZERO; // 0x0
AccountAddress.ONE; // 0x1
AccountAddress.TWO; // 0x2
AccountAddress.THREE; // 0x3
AccountAddress.FOUR; // 0x4
AccountAddress.A; // 0xa
```

---

## String output

| Method                             | Use case                                           |
| ---------------------------------- | -------------------------------------------------- |
| `addr.toString()`                  | AIP-40 default: SHORT for special, LONG for others |
| `addr.toStringLong()`              | Always 0x + 64 hex chars                           |
| `addr.toStringShort()`             | Shortest form (no leading zeros)                   |
| `addr.toStringLongWithoutPrefix()` | 64 hex chars, no `0x`                              |

```typescript
const addr = AccountAddress.from("0x1");
addr.toString(); // "0x1"
addr.toStringLong(); // "0x0000...0001" (64 chars after 0x)
```

---

## Validation

```typescript
const result = AccountAddress.isValid({
  input: "0x1",
  strict: false
});
if (result.valid) {
  // use address
} else {
  console.log(result.invalidReason, result.invalidReasonMessage);
}
```

---

## Derived addresses (object / resource / token / user-derived)

Import from `@aptos-labs/ts-sdk` (via core):

```typescript
import {
  AccountAddress,
  createObjectAddress,
  createResourceAddress,
  createTokenAddress,
  createUserDerivedObjectAddress
} from "@aptos-labs/ts-sdk";
```

### Object address (e.g. named object)

```typescript
const creator = AccountAddress.from("0x120e79e45d21ef439963580c77a023e2729db799e96e61f878fac98fde5b9cc9");
const seed = "migration::migration_contract"; // or Uint8Array
const objectAddr = createObjectAddress(creator, seed);
// objectAddr.toString() => deterministic 0x... address
```

### Resource account address

```typescript
const creator = AccountAddress.from("0x41e724e1d4fce6472ffcb5c9886770893eb49489e3f531d0aa97bf951e66d70c");
const seed = "create_resource::create_resource";
const resourceAddr = createResourceAddress(creator, seed);
```

### Token (NFT) object address

```typescript
const creator = AccountAddress.from("0x9d518b9b84f327eafc5f6632200ea224a818a935ffd6be5d78ada250bbc44a6");
const collectionName = "SuperV Villains";
const tokenName = "Nami #5962";
const tokenAddr = createTokenAddress(creator, collectionName, tokenName);
// Internally: seed = `${collectionName}::${tokenName}` -> createObjectAddress(creator, seed)
```

### User-derived object address

```typescript
const sourceAddress = AccountAddress.from("0x653a60dab27fe8f3859414973d218e1b7551c778a8650a7055a85c0f8041b2a4");
const deriveFromAddress = AccountAddress.from("0xa");
const userDerivedAddr = createUserDerivedObjectAddress(sourceAddress, deriveFromAddress);
```

---

## Equality and serialization

```typescript
const a = AccountAddress.from("0x1");
const b = AccountAddress.from("0x0000000000000000000000000000000000000000000000000000000000000001");
a.equals(b); // true

// BCS: use serializer or SDK entry/script helpers in transaction building
```

---

## Common mistakes

| Mistake                               | Correct approach                                                                                              |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Using `Hex` for account address       | Use `AccountAddress` only                                                                                     |
| Comparing with `===` on strings       | Use `addr1.equals(addr2)` or compare after `AccountAddress.from()`                                            |
| Using SHORT for non-special in strict | Use LONG (0x + 64 hex chars) or `AccountAddress.from()` (relaxed)                                             |
| Hand-rolling object address hash      | Use `createObjectAddress` / `createTokenAddress` / `createResourceAddress` / `createUserDerivedObjectAddress` |

---

## References

- SDK: `src/core/accountAddress.ts`, `src/core/account/utils/address.ts`
- AIP-40: https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-40.md
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
