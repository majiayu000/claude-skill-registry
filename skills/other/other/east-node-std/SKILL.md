---
name: east-node-std
description: "Node.js platform functions for the East language. Use when writing East programs that need Console I/O, FileSystem operations, HTTP Fetch requests, Cryptography, Time operations, Path manipulation, Random number generation, or Testing. Triggers for: (1) Writing East programs with @elaraai/east-node-std, (2) Using platform functions like Console.log, FileSystem.readFile, Fetch.get, Crypto.uuid, Time.now, Path.join, Random.normal, (3) Testing East code with describeEast and Assert."
---

# East Node Standard Library

Node.js platform functions for the East language. Enables East programs to interact with the filesystem, network, console, and other I/O operations.

## Quick Start

```typescript
import { East, StringType, NullType } from "@elaraai/east";
import { NodePlatform, Console, FileSystem } from "@elaraai/east-node-std";

const processFile = East.function(
    [StringType],
    NullType,
    ($, path) => {
        const content = $.let(FileSystem.readFile(path));
        $(Console.log(content));
    }
);

// Compile with NodePlatform (includes all platform functions)
const compiled = East.compile(processFile.toIR(), NodePlatform);
await compiled("input.txt");
```

## Decision Tree: Which Module to Use

```
Task → What do you need?
    │
    ├─ Console (stdout/stderr output)
    │   └─ .log(), .error(), .write()
    │
    ├─ FileSystem (read/write files and directories)
    │   ├─ Text → .readFile(), .writeFile(), .appendFile()
    │   ├─ Binary → .readFileBytes(), .writeFileBytes()
    │   ├─ Query → .exists(), .isFile(), .isDirectory()
    │   ├─ Directory → .createDirectory(), .readDirectory()
    │   └─ Delete → .deleteFile()
    │
    ├─ Fetch (HTTP requests)
    │   └─ .get(), .post(), .request()
    │
    ├─ Crypto (hashing, UUIDs, random bytes)
    │   └─ .uuid(), .randomBytes(), .hashSha256(), .hashSha256Bytes()
    │
    ├─ Time (timestamps and delays)
    │   └─ .now(), .sleep()
    │
    ├─ Path (path manipulation)
    │   └─ .join(), .resolve(), .dirname(), .basename(), .extname()
    │
    ├─ Random (statistical distributions)
    │   ├─ Basic → .uniform(), .normal(), .range()
    │   ├─ Continuous → .exponential(), .weibull(), .pareto(), .logNormal()
    │   ├─ Discrete → .bernoulli(), .binomial(), .geometric(), .poisson()
    │   ├─ Composite → .irwinHall(), .bates()
    │   └─ Control → .seed()
    │
    └─ Assert (testing with describeEast)
        └─ .is(), .equal(), .notEqual(), .less(), .lessEqual(), .greater(), .greaterEqual(), .between(), .throws(), .fail()
```

## Compiling East Programs

**Option 1: Use NodePlatform (all modules)**
```typescript
const compiled = East.compile(myFunction.toIR(), NodePlatform);
```

**Option 2: Use specific module implementations**
```typescript
const compiled = East.compile(myFunction.toIR(), [...Console.Implementation, ...FileSystem.Implementation]);
```

## Reference Documentation

- **[API Reference](./reference/api.md)** - Complete function signatures, types, and arguments for all modules
- **[Examples](./reference/examples.md)** - Working code examples by use case

## Available Modules

| Module | Import | Purpose |
|--------|--------|---------|
| Console | `import { Console } from "@elaraai/east-node-std"` | stdout/stderr output |
| FileSystem | `import { FileSystem } from "@elaraai/east-node-std"` | Read/write files and directories |
| Fetch | `import { Fetch } from "@elaraai/east-node-std"` | HTTP requests |
| Crypto | `import { Crypto } from "@elaraai/east-node-std"` | Hashing, UUIDs, random bytes |
| Time | `import { Time } from "@elaraai/east-node-std"` | Timestamps and sleep |
| Path | `import { Path } from "@elaraai/east-node-std"` | Path manipulation |
| Random | `import { Random } from "@elaraai/east-node-std"` | 14 statistical distributions |
| Assert | `import { Assert, describeEast } from "@elaraai/east-node-std"` | Testing utilities |

## Accessing Types

```typescript
import { Fetch } from "@elaraai/east-node-std";

// Access types via Module.Types.TypeName
const method = Fetch.Types.Method;
const config = Fetch.Types.RequestConfig;
const response = Fetch.Types.Response;
```
