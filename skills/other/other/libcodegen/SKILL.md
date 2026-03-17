---
name: libcodegen
description: >
  libcodegen - Protocol Buffer code generation. TypeGenerator, ServiceGenerator,
  and DefinitionGenerator transform .proto files into JavaScript types, gRPC
  service stubs, and type definitions. Use for generating code from protobuf
  schemas, automating service stub creation, and maintaining type consistency
  across services.
---

# libcodegen Skill

## When to Use

- Generating JavaScript types from Protocol Buffer schemas
- Creating gRPC service stubs automatically
- Updating generated code after .proto changes
- Maintaining type consistency across microservices

## Key Concepts

**TypeGenerator**: Generates JavaScript classes from protobuf message
definitions with proper type annotations.

**ServiceGenerator**: Creates gRPC service stubs with method signatures matching
the proto service definitions.

**DefinitionGenerator**: Generates type definitions for IDE support and
documentation.

## Usage Patterns

### Pattern 1: Generate types from protos

```javascript
import { TypeGenerator } from "@copilot-ld/libcodegen";

const generator = new TypeGenerator("./proto");
await generator.generate("./generated/types");
```

### Pattern 2: Generate service stubs

```javascript
import { ServiceGenerator } from "@copilot-ld/libcodegen";

const generator = new ServiceGenerator("./proto");
await generator.generate("./generated/services");
```

## Integration

Run via `make codegen` after modifying .proto files. Output used by libtype and
librpc.
