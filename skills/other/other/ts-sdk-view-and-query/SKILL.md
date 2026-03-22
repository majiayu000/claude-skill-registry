---
name: ts-sdk-view-and-query
description:
  "How to read on-chain data in @aptos-labs/ts-sdk: view(), getBalance(), getAccountInfo(), getAccountResources(),
  getAccountModules(), getResource(). Triggers on: 'aptos.view', 'getBalance', 'getAccountInfo', 'getAccountResources',
  'SDK query', 'view function TypeScript'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: sdk
  tags: ["typescript", "sdk", "view", "balance", "account", "resources", "query"]
  priority: high
---

# TypeScript SDK: View and Query

## Purpose

Guide **read-only** access to chain data in `@aptos-labs/ts-sdk`: view functions, balance, account info, resources, and
modules.

## ALWAYS

1. **Use `aptos.getBalance({ accountAddress })` for APT balance** – not deprecated `getAccountCoinAmount` /
   `getAccountAPTAmount`.
2. **Use `aptos.view()` for Move view functions** – pass `function`, `functionArguments`, and optional `typeArguments`.
3. **Use `bigint` for u128/u256 view return values** – cast `result[0]` to `BigInt(...)` when the Move function returns
   u128/u256.
4. **Pass address as string or AccountAddress** – SDK accepts `AccountAddressInput` (string or `AccountAddress`).

## NEVER

1. **Do not use deprecated `getAccountCoinAmount` or `getAccountAPTAmount`** – use `getBalance()`.
2. **Do not use `number` for u128/u256** – precision loss; use `bigint`.
3. **Do not assume view returns are always strings** – types vary (number, bigint, string, boolean, array).

---

## getBalance (APT)

```typescript
const balance = await aptos.getBalance({
  accountAddress: account.accountAddress
});
// balance is bigint in octas (1 APT = 100_000_000 octas)
const apt = balance / 100_000_000n;
const remainder = balance % 100_000_000n;
console.log(`${apt}.${remainder.toString().padStart(8, "0")} APT`);
```

---

## getAccountInfo

```typescript
const accountInfo = await aptos.getAccountInfo({
  accountAddress: "0x1"
});
// accountInfo: { sequence_number, authentication_key, ... }
```

---

## view() – Move view functions

```typescript
// No type arguments
const result = await aptos.view({
  payload: {
    function: `${MODULE_ADDRESS}::counter::get_count`,
    functionArguments: [accountAddress]
  }
});
const count = Number(result[0]);

// With type arguments (e.g. coin type)
const balanceResult = await aptos.view({
  payload: {
    function: "0x1::coin::balance",
    typeArguments: ["0x1::aptos_coin::AptosCoin"],
    functionArguments: [accountAddress]
  }
});
const coinBalance = BigInt(balanceResult[0] as string);

// Multiple return values
// Move: public fun get_listing(addr): (address, u64, bool)
const [seller, price, isActive] = await aptos.view({
  payload: {
    function: `${MODULE_ADDRESS}::marketplace::get_listing`,
    functionArguments: [listingAddress]
  }
});
const listing = {
  seller: seller as string,
  price: BigInt(price as string),
  isActive: isActive as boolean
};
```

---

## getAccountResources

```typescript
const resources = await aptos.getAccountResources({
  accountAddress: account.accountAddress
});
// resources: Array<MoveResource>
const counterResource = resources.find((r) => r.type === `${MODULE_ADDRESS}::counter::Counter`);
```

---

## getAccountResource (single type)

```typescript
const resource = await aptos.getAccountResource({
  accountAddress: account.accountAddress,
  resourceType: `${MODULE_ADDRESS}::counter::Counter`
});
// resource.data has the struct fields
const value = (resource?.data as { value: number })?.value;
```

---

## getAccountModules

```typescript
const modules = await aptos.getAccountModules({
  accountAddress: modulePublisherAddress
});
// modules: MoveModuleBytecode[] (ABI, bytecode)
```

---

## getModule (single module by name)

```typescript
const module = await aptos.getModule({
  accountAddress: modulePublisherAddress,
  moduleName: "counter"
});
```

---

## Pagination (resources / modules)

Use cursor-based options when available:

```typescript
const { resources, cursor } = await aptos.getAccountResourcesPage({
  accountAddress: account.accountAddress,
  options: { limit: 10, cursor: nextCursor }
});
```

---

## Type handling for view results

| Move return type | TypeScript       | Example                                    |
| ---------------- | ---------------- | ------------------------------------------ |
| u8..u64          | number or bigint | `Number(result[0])` or `BigInt(result[0])` |
| u128, u256       | bigint           | `BigInt(result[0] as string)`              |
| address          | string           | `result[0] as string`                      |
| bool             | boolean          | `result[0] as boolean`                     |
| vector<T>        | array            | `result[0] as T[]`                         |

---

## Common mistakes

| Mistake                                   | Correct approach                                              |
| ----------------------------------------- | ------------------------------------------------------------- |
| Using getAccountCoinAmount                | Use `aptos.getBalance({ accountAddress })`                    |
| Using number for u128                     | Use `BigInt(result[0] as string)`                             |
| Forgetting typeArguments for generic view | Add `typeArguments: [coinType]` when Move function is generic |

---

## References

- SDK: `src/internal/view.ts`, `src/api/account.ts`, balance/getBalance in internal
- Pattern: [TYPESCRIPT_SDK.md](../../../../patterns/fullstack/TYPESCRIPT_SDK.md)
- Related: [ts-sdk-client](../ts-sdk-client/SKILL.md), [ts-sdk-types](../ts-sdk-types/SKILL.md),
  [use-ts-sdk](../use-ts-sdk/SKILL.md)
