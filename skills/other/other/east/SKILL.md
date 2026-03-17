---
name: east
description: "East programming language - a statically typed, expression-based language embedded in TypeScript. Use when writing East programs with @elaraai/east. Triggers for: (1) Writing East functions with East.function() or East.asyncFunction(), (2) Defining types (IntegerType, StringType, ArrayType, StructType, VariantType, etc.), (3) Using platform functions with East.platform() or East.asyncPlatform(), (4) Compiling East programs with East.compile(), (5) Working with East expressions (arithmetic, collections, control flow), (6) Serializing East IR with .toIR() and EastIR.fromJSON(), (7) Standard library operations (formatting, rounding, generation)."
---

# East Language

A statically typed, expression-based programming language embedded in TypeScript. Write programs using a fluent API, compile to portable IR.

## Quick Start

```typescript
// Types and helpers are direct imports (NOT East.IntegerType)
import { East, IntegerType, StringType, ArrayType, NullType } from "@elaraai/east";

// 1. Define platform functions (East.platform)
const log = East.platform("log", [StringType], NullType);
const platform = [log.implement(console.log)];

// 2. Define East function (East.function)
const sumArray = East.function([ArrayType(IntegerType)], IntegerType, ($, arr) => {
    const total = $.let(arr.sum());
    $(log(East.str`Sum: ${total}`));
    $.return(total);
});

// 3. Compile and execute (East.compile)
const compiled = East.compile(sumArray, platform);
compiled([1n, 2n, 3n]);  // logs "Sum: 6", returns 6n
```

## Decision Tree: What Do You Need?

```
Task → What do you need?
    │
    ├─ Create East Expressions (East.*)
    │   ├─ From TypeScript value → East.value(tsValue) or East.value(tsValue, Type)
    │   ├─ String interpolation → East.str`Hello ${name}!`
    │   └─ Inside function body → $.let(value), $.const(value)
    │
    ├─ Define a Type (import from package, NOT East.*)
    │   ├─ Primitive → IntegerType, FloatType, StringType, BooleanType, DateTimeType, BlobType, NullType
    │   ├─ Collection → ArrayType(T), SetType(K), DictType(K, V), RefType(T)
    │   ├─ Compound → StructType({...}), VariantType({...}), RecursiveType(...)
    │   ├─ Function → FunctionType<I, O>, AsyncFunctionType<I, O>
    │   └─ Patch → PatchType(T) (compute patch type for any East type)
    │
    ├─ Create TypeScript Values for East Types
    │   ├─ NullType → null
    │   ├─ BooleanType → true, false
    │   ├─ IntegerType → 42n (bigint literal)
    │   ├─ FloatType → 3.14 (number literal)
    │   ├─ StringType → "hello"
    │   ├─ DateTimeType → new Date("2025-01-01T00:00:00Z")
    │   ├─ BlobType → new Uint8Array([...])
    │   ├─ ArrayType(T) → [1n, 2n, 3n]
    │   ├─ SetType(K) → new Set([1n, 2n, 3n])
    │   ├─ DictType(K, V) → new Map([["a", 1n], ["b", 2n]])
    │   ├─ StructType({...}) → { field1: value1, field2: value2 }
    │   ├─ VariantType({...}) (use helpers from package)
    │   │   ├─ Option type → some(value), none  ← preferred for Option/Maybe
    │   │   └─ Other variants → variant("caseName", value)
    │   └─ RefType(T) (use helper from package) → ref(value)
    │
    ├─ Write a Function (East.*)
    │   ├─ Synchronous → East.function([inputs], output, ($, ...args) => { ... })
    │   └─ Asynchronous → East.asyncFunction([inputs], output, ($, ...args) => { ... })
    │
    ├─ Compile and Execute (East.*)
    │   ├─ Sync function → East.compile(fn, platform)
    │   └─ Async function → East.compileAsync(fn, platform)
    │
    ├─ Use Platform Effects (East.*)
    │   ├─ Sync effect → East.platform("name", [inputs], output).implement(fn)
    │   └─ Async effect → East.asyncPlatform("name", [inputs], output).implement(fn)
    │
    ├─ Block Operations ($)
    │   ├─ Variables → $.let(value), $.const(value), $.assign(var, value)
    │   ├─ Execute → $(expr), $.return(value), $.error(message)
    │   ├─ Control Flow → $.if(...), $.while(...), $.for(...), $.match(...)
    │   └─ Error Handling → $.try(...).catch(...).finally(...)
    │
    ├─ Expression Operations
    │   ├─ Boolean
    │   │   ├─ Logic → .and($=>), .or($=>), .not(), .ifElse($=>,$=>)
    │   │   ├─ Bitwise → .bitAnd(), .bitOr(), .bitXor()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   ├─ Integer
    │   │   ├─ Math → .add()/.plus(), .subtract()/.sub()/.minus(), .multiply()/.mul()/.times(), .divide()/.div(), .remainder()/.mod()/.rem()/.modulo(), .pow(), .abs(), .sign(), .negate(), .log()
    │   │   ├─ Convert → .toFloat()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne(), .lessThan()/.less()/.lt(), .greaterThan()/.greater()/.gt(), .lessThanOrEqual()/.lessEqual()/.lte()/.le(), .greaterThanOrEqual()/.greaterEqual()/.gte()/.ge()
    │   ├─ Float
    │   │   ├─ Math → .add()/.plus(), .subtract()/.sub()/.minus(), .multiply()/.mul()/.times(), .divide()/.div(), .remainder()/.mod()/.rem()/.modulo(), .pow(), .abs(), .sign(), .negate()
    │   │   ├─ Advanced → .sqrt(), .exp(), .log(), .sin(), .cos(), .tan()
    │   │   ├─ Convert → .toInteger()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne(), .lessThan()/.less()/.lt(), .greaterThan()/.greater()/.gt(), .lessThanOrEqual()/.lessEqual()/.lte()/.le(), .greaterThanOrEqual()/.greaterEqual()/.gte()/.ge()
    │   ├─ String
    │   │   ├─ Transform → .concat(), .repeat(), .substring(), .upperCase(), .lowerCase(), .trim(), .trimStart(), .trimEnd()
    │   │   ├─ Replace → .replace(), .replaceAll(), .split()
    │   │   ├─ Query → .length(), .startsWith(), .endsWith(), .contains(), .indexOf(), .charAt()
    │   │   ├─ Parse → .parse(), .parseJson()
    │   │   ├─ Encode → .encodeUtf8(), .encodeUtf16()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne(), .lessThan()/.less()/.lt(), .greaterThan()/.greater()/.gt(), .lessThanOrEqual()/.lessEqual()/.lte()/.le(), .greaterThanOrEqual()/.greaterEqual()/.gte()/.ge()
    │   ├─ DateTime
    │   │   ├─ Components → .getYear(), .getMonth(), .getDayOfMonth(), .getDayOfWeek(), .getHour(), .getMinute(), .getSecond(), .getMillisecond()
    │   │   ├─ Arithmetic → .addDays(), .subtractDays(), .addHours(), .subtractHours(), .addMinutes(), .addSeconds(), .addMilliseconds(), .addWeeks()
    │   │   ├─ Duration → .durationDays(), .durationHours(), .durationMinutes(), .durationSeconds(), .durationMilliseconds(), .durationWeeks()
    │   │   ├─ Convert → .toEpochMilliseconds(), .printFormatted()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne(), .lessThan()/.less()/.lt(), .greaterThan()/.greater()/.gt(), .lessThanOrEqual()/.lessEqual()/.lte()/.le(), .greaterThanOrEqual()/.greaterEqual()/.gte()/.ge()
    │   ├─ Blob
    │   │   ├─ Read → .size(), .getUint8()
    │   │   ├─ Decode → .decodeUtf8(), .decodeUtf16(), .decodeBeast(), .decodeCsv()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   ├─ Array
    │   │   ├─ Read → .size(), .length(), .has(), .get(), .at(), .tryGet(), .getKeys()
    │   │   ├─ Mutate → .update(), .pushLast(), .popLast(), .pushFirst(), .popFirst(), .append(), .prepend(), .clear(), .sortInPlace(), .reverseInPlace()
    │   │   ├─ Transform → .copy(), .slice(), .concat(), .sort(), .reverse(), .map(), .filter(), .filterMap(), .flatMap()
    │   │   ├─ Search → .findFirst(), .findAll(), .firstMap(), .isSorted()
    │   │   ├─ Reduce → .reduce(), .every(), .some(), .sum(), .mean(), .maximum(), .minimum(), .findMaximum(), .findMinimum()
    │   │   ├─ Convert → .stringJoin(), .toSet(), .toDict(), .flattenToSet(), .flattenToDict(), .encodeCsv()
    │   │   ├─ Group → .groupReduce(), .groupSize(), .groupSum(), .groupMean(), .groupMinimum(), .groupMaximum(), .groupToArrays(), .groupToSets(), .groupToDicts(), .groupEvery(), .groupSome()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   ├─ Set
    │   │   ├─ Read → .size(), .has()
    │   │   ├─ Mutate → .insert(), .tryInsert(), .delete(), .tryDelete(), .clear(), .unionInPlace()
    │   │   ├─ Set Ops → .copy(), .union(), .intersection(), .difference(), .symmetricDifference(), .isSubsetOf(), .isSupersetOf(), .isDisjointFrom()
    │   │   ├─ Transform → .filter(), .filterMap(), .map(), .forEach(), .firstMap()
    │   │   ├─ Reduce → .reduce(), .every(), .some(), .sum(), .mean()
    │   │   ├─ Convert → .toArray(), .toSet(), .toDict(), .flattenToArray(), .flattenToSet(), .flattenToDict()
    │   │   ├─ Group → .groupReduce(), .groupSize(), .groupSum(), .groupMean(), .groupToArrays(), .groupToSets(), .groupToDicts(), .groupEvery(), .groupSome()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   ├─ Dict
    │   │   ├─ Read → .size(), .has(), .get(), .tryGet(), .keys(), .getKeys()
    │   │   ├─ Mutate → .insert(), .insertOrUpdate(), .update(), .merge(), .getOrInsert(), .delete(), .tryDelete(), .pop(), .swap(), .clear(), .unionInPlace()
    │   │   ├─ Transform → .copy(), .map(), .filter(), .filterMap(), .forEach(), .firstMap()
    │   │   ├─ Reduce → .reduce(), .every(), .some(), .sum(), .mean()
    │   │   ├─ Convert → .toArray(), .toSet(), .toDict(), .flattenToArray(), .flattenToSet(), .flattenToDict()
    │   │   ├─ Group → .groupReduce(), .groupSize(), .groupSum(), .groupMean(), .groupToArrays(), .groupToSets(), .groupToDicts(), .groupEvery(), .groupSome()
    │   │   └─ Compare → .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   ├─ Struct → .fieldName (direct property access)
    │   ├─ Variant → .match(), .unwrap(), .hasTag(), .getTag(), .equals()/.equal()/.eq(), .notEquals()/.notEqual()/.ne()
    │   └─ Ref → .get(), .update(), .merge()
    │
    ├─ Standard Library (East.*)
    │   ├─ Integer → East.Integer.printCommaSeperated(), .roundNearest(), .printOrdinal()
    │   ├─ Float → East.Float.roundToDecimals(), .printCurrency(), .printCompact()
    │   ├─ DateTime → East.DateTime.fromComponents(), .roundDownDay(), .parseFormatted()
    │   ├─ Array → East.Array.range(), .linspace(), .generate()
    │   ├─ Set → East.Set.generate()
    │   ├─ Dict → East.Dict.generate()
    │   ├─ Blob → East.Blob.encodeBeast(), blob.decodeCsv(), array.encodeCsv()
    │   └─ String → East.String.printJson(), East.String.printError()
    │
    ├─ Comparisons (East.*)
    │   ├─ Equality → East.equal()/.equals()/.eq(), East.notEqual()/.notEquals()/.ne()
    │   ├─ Ordering → East.less()/.lessThan()/.lt(), East.greater()/.greaterThan()/.gt()
    │   ├─ Bounds → East.lessEqual()/.lte()/.le(), East.greaterEqual()/.gte()/.ge()
    │   ├─ Identity → East.is() (reference equality for mutable types)
    │   └─ Utilities → East.min(), East.max(), East.clamp()
    │
    ├─ Conversion (East.*)
    │   └─ To string → East.print(expr)
    │
    ├─ Patch Operations (East.*)
    │   ├─ Compute diff → East.diff(before, after) → returns patch
    │   ├─ Apply patch → East.applyPatch(value, patch) → returns patched value
    │   ├─ Compose patches → East.composePatch(first, second, type) → returns combined patch
    │   └─ Invert patch → East.invertPatch(patch, type) → returns undo patch
    │
    └─ Serialization
        ├─ IR → fn.toIR(), ir.toJSON(), EastIR.fromJSON(data).compile(platform)
        └─ Data → East.Blob.encodeBeast(value, 'v2'), blob.decodeBeast(type, 'v2')
```

## Reference Documentation

- **[API Reference](./reference/api.md)** - Complete function signatures, types, and arguments
- **[Examples](./reference/examples.md)** - Working code examples by use case

## Type System Summary

| Type | `ValueTypeOf<Type>` | Mutability |
|------|---------------------|------------|
| `NullType` | `null` | Immutable |
| `BooleanType` | `boolean` | Immutable |
| `IntegerType` | `bigint` | Immutable |
| `FloatType` | `number` | Immutable |
| `StringType` | `string` | Immutable |
| `DateTimeType` | `Date` | Immutable |
| `BlobType` | `Uint8Array` | Immutable |
| `ArrayType<T>` | `ValueTypeOf<T>[]` | **Mutable** |
| `SetType<K>` | `Set<ValueTypeOf<K>>` | **Mutable** |
| `DictType<K, V>` | `Map<ValueTypeOf<K>, ValueTypeOf<V>>` | **Mutable** |
| `RefType<T>` | `ref<ValueTypeOf<T>>` | **Mutable** |
| `StructType<Fields>` | `{...}` | Immutable |
| `VariantType<Cases>` | `variant` | Immutable |
| `FunctionType<I, O>` | Function | Immutable |
| `PatchType<T>` | `variant` | Immutable |

## Key Patterns

### TypeScript Values vs East Expressions

TypeScript values and East expressions are different. East methods only work on East expressions.

```typescript
// WRONG - Cannot call East methods on TypeScript values
const THRESHOLD = 100n;  // This is a TypeScript bigint
East.function([IntegerType], BooleanType, ($, x) => {
    $.return(x.greaterThan(THRESHOLD));  // ERROR: THRESHOLD has no .greaterThan()
});

// CORRECT - Wrap TypeScript values with East.value()
const THRESHOLD = 100n;
East.function([IntegerType], BooleanType, ($, x) => {
    $.return(x.greaterThan(East.value(THRESHOLD)));  // OK
});

// ALSO CORRECT - Use $.const() inside the function
East.function([IntegerType], BooleanType, ($, x) => {
    const threshold = $.const(THRESHOLD);  // Creates East expression
    $.return(x.greaterThan(threshold));    // OK
});
```

**Rule**: Function parameters are already East expressions. External TypeScript values must be wrapped with `East.value()` or bound with `$.const()`.

### Creating Variant Values
```typescript
import { variant, some, none, ref } from "@elaraai/east";

// Option types - use some() and none helpers (preferred)
const hasValue = some(42n);      // { type: "some", value: 42n }
const noValue = none;            // { type: "none", value: null }

// AVOID: variant("some", ...) and variant("none", ...) for Option types
// const hasValue = variant("some", 42n);  // works but use some() instead
// const noValue = variant("none", null);  // works but use none instead

// Other variant types - use variant()
const success = variant("ok", "done");
const failure = variant("error", "failed");

// Mutable references - use ref()
const counter = ref(0n);
```

### String Interpolation
```typescript
// East.str`` creates a StringExpr from a template
// Only East expressions can be interpolated, NOT plain TypeScript values

const MY_CONSTANT = 100n;  // TypeScript value

East.function([IntegerType], StringType, ($, x) => {
    // CORRECT - x is already an East expression (function parameter)
    const msg1 = $.let(East.str`Value: ${x}`);

    // CORRECT - wrap TypeScript constant with East.value()
    const msg2 = $.let(East.str`Threshold: ${East.value(MY_CONSTANT)}`);

    // CORRECT - use $.const() to create East expression first
    const threshold = $.const(MY_CONSTANT);
    const msg3 = $.let(East.str`Threshold: ${threshold}`);

    // WRONG - cannot interpolate plain TypeScript values
    // const msg4 = $.let(East.str`Threshold: ${MY_CONSTANT}`);  // ERROR

    $.return(msg1);
});
```

### Error Handling
```typescript
$.try($ => {
    $.assign(result, arr.get(index));
}).catch(($, message, stack) => {
    $.assign(result, -1n);
}).finally($ => {
    // cleanup
});
```

### Platform Function Implementations
```typescript
// Platform implementations are raw TypeScript functions that receive East values
// (bigint for Integer, number for Float, string for String, etc.)

// Sync platform - regular TypeScript function
const log = East.platform("log", [StringType], NullType);
const timeNs = East.platform("time_ns", [], IntegerType);

// Async platform - async TypeScript function
const fetchStatus = East.asyncPlatform("fetch_status", [StringType], StringType);

// Implementations receive/return TypeScript values matching East types
const platform = [
    log.implement(console.log),                          // (msg: string) => void
    timeNs.implement(() => process.hrtime.bigint()),     // () => bigint
    fetchStatus.implement(async (url: string) => {       // async function OK
        const response = await fetch(url);
        return `${response.status}`;
    }),
];

// In East code: NO await needed - async is handled automatically
const myFn = East.asyncFunction([StringType], NullType, ($, url) => {
    const t1 = $.let(timeNs());
    const status = $.let(fetchStatus(url));  // no await, just call it
    const t2 = $.let(timeNs());
    $(log(East.str`Fetched in ${t2.subtract(t1)} ns, status: ${status}`));
});

// Compile async functions with East.compileAsync
const compiled = East.compileAsync(myFn, platform);
await compiled("https://example.com");  // await at the outer TypeScript level
```
