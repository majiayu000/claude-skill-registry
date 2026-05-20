---
name: ts-sdk-types
description:
  "Move to TypeScript type mapping in @aptos-labs/ts-sdk: u64/u128/u256 as bigint, address as string, TypeTag,
  functionArguments and typeArguments. Triggers on: 'typeArguments', 'functionArguments', 'Move to TypeScript', 'type
  mapping', 'TypeTag', 'bigint u128'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "types", "typetag", "bigint", "move"]
  priority: high
---

# TypeScript SDK: Types (Move ↔ TypeScript)

## Purpose

Guide **type mapping** between Move and TypeScript when using `@aptos-labs/ts-sdk`: numeric types (especially
u128/u256), address, TypeTag, and `functionArguments` / `typeArguments`.

## ALWAYS

1. **Use `bigint` for u128 and u256** – in both view results and `functionArguments`; JavaScript `number` loses
   precision above 2^53.
2. **Use `string` for address in payloads** – e.g. `"0x1"` or `accountAddress.toString()`; SDK accepts
   `AccountAddressInput` (string or AccountAddress).
3. **Use `typeArguments` for generic Move functions** – e.g. coin type `["0x1::aptos_coin::AptosCoin"]` for
   `coin::balance` or `coin::transfer`.
4. **Cast view results explicitly** when you know the Move return type – e.g. `BigInt(result[0] as string)` for u128.

## NEVER

1. **Do not use `number` for u128/u256** – precision loss; use `bigint`.
2. **Do not pass raw number for large u64 in entry/view** – use `bigint` if value can exceed Number.MAX_SAFE_INTEGER.
3. **Do not omit typeArguments** when the Move function has type parameters (e.g. `balance<CoinType>`).

---

## Move → TypeScript (summary)

| Move type           | TypeScript type            | Example                                              |
| ------------------- | -------------------------- | ---------------------------------------------------- |
| u8, u16, u32        | number                     | `255`, `65535`                                       |
| u64                 | number \| bigint           | Prefer bigint for large values                       |
| u128, u256          | bigint                     | `BigInt("340282366920938463463374607431768211455")`  |
| i8..i64 (Move 2.3+) | number \| bigint           | Use bigint for i64 when large                        |
| i128, i256          | bigint                     | `BigInt("-...")`                                     |
| bool                | boolean                    | `true`                                               |
| address             | string                     | `"0x1"`                                              |
| signer              | —                          | Not passed from TS; signer is the transaction sender |
| vector<u8>          | Uint8Array \| string (hex) | `new Uint8Array([1,2,3])` or hex                     |
| vector<T>           | T[]                        | `[1, 2, 3]`                                          |
| String              | string                     | `"hello"`                                            |
| Object<T>           | string (object address)    | `objectAddress.toString()`                           |
| Option<T>           | T \| null                  | Value or `null`                                      |

---

## functionArguments

Order and types must match the Move entry/view function parameters:

```typescript
// Move: public fun transfer<CoinType>(to: address, amount: u64)
await aptos.transaction.build.simple({
  sender: account.accountAddress,
  data: {
    function: "0x1::coin::transfer",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [
      "0xrecipient...", // address as string
      1000n // u64 as bigint (or number if small)
    ]
  }
});
```

---

## typeArguments

For generic Move functions, pass full type strings (`address::module::StructName`):

```typescript
// Move: balance<CoinType>(addr): u64
typeArguments: ["0x1::aptos_coin::AptosCoin"];

// Move: transfer<CoinType>(to, amount)
typeArguments: ["0x1::aptos_coin::AptosCoin"];
```

---

## View return types

```typescript
const result = await aptos.view({
  payload: {
    function: "0x1::coin::balance",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [accountAddress]
  }
});
// result is an array; u128 often returned as string in JSON
const balance = BigInt(result[0] as string);
```

---

## TypeTag (advanced)

When building payloads programmatically or parsing type strings:

```typescript
import { TypeTag } from "@aptos-labs/ts-sdk";

// Parser for type tag strings
import { parseTypeTag } from "@aptos-labs/ts-sdk";
const tag = parseTypeTag("0x1::aptos_coin::AptosCoin");
```

Use `typeArguments` as string array in simple cases; use TypeTag when the SDK API expects it.

---

## Object / resource address in arguments

Pass object address as string (LONG or SHORT per AIP-40):

```typescript
functionArguments: [
  nftObjectAddress.toString(), // or "0x..."
  price
];
```

---

## Common mistakes

| Mistake                                  | Correct approach                                    |
| ---------------------------------------- | --------------------------------------------------- |
| Passing number for u128 amount           | Use `1000000n` or `BigInt("...")`                   |
| Omitting typeArguments for coin::balance | Add `typeArguments: ["0x1::aptos_coin::AptosCoin"]` |
| Using result[0] as number for u128       | Use `BigInt(result[0] as string)`                   |
| Wrong order of functionArguments         | Match Move parameter order exactly                  |

---

## References

- SDK: `src/transactions/typeTag/`, `src/transactions/instances/transactionArgument.ts`, view and build APIs
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-view-and-query](../ts-sdk-view-and-query/SKILL.md),
  [ts-sdk-transactions](../ts-sdk-transactions/SKILL.md), [use-ts-sdk](../use-ts-sdk/SKILL.md)
