---
name: projects-expert
description: Deep knowledge about Ryan's open source projects (openpkg-ts, doccov, secondlayer). Use when users ask about these tools, their features, usage, or output.
---

# Projects Expert

Provide accurate, detailed answers about Ryan's open source projects. Use the exact information below—do not fabricate features or output.

## Live Documentation (WebFetch)

For detailed or current information, fetch live docs from these URLs ONLY:

| Project | README URL |
|---------|------------|
| openpkg-ts (root) | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/README.md` |
| @openpkg-ts/cli | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/packages/cli/README.md` |
| @openpkg-ts/sdk | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/packages/sdk/README.md` |
| @openpkg-ts/spec | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/packages/spec/README.md` |
| @openpkg-ts/react | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/packages/react/README.md` |
| @openpkg-ts/adapters | `https://raw.githubusercontent.com/ryanwaits/openpkg-ts/main/packages/adapters/README.md` |

**When to fetch**: User asks for specific CLI flags, SDK methods, or detailed API examples not in the reference below.

**Do NOT fetch** for general "what is openpkg" questions—use the reference below first.

---

## openpkg-ts

TypeScript API extraction and documentation toolkit. Extract complete API specifications from source code, then generate docs for any framework.

**Deep dive**: Read `content/new-standard-who-dis/index.mdx` for Standard JSON Schema and runtime introspection details.

### Why

- **Zero manual docs** — Extract everything from TypeScript source
- **Framework agnostic** — Fumadocs, Docusaurus, Mintlify, or custom
- **Schema library support** — Zod, Valibot, ArkType, TypeBox (requires `--runtime` flag)
- **Version tracking** — Diff specs and get semver recommendations

### Install

```bash
npm install -g @openpkg-ts/cli
# or use directly
npx @openpkg-ts/cli <command>
```

### CLI Commands

#### list — List exports from entry point

```bash
openpkg list src/index.ts
# Output: JSON array of { name, kind, file, line, description }
```

#### get — Get detailed spec for single export

```bash
openpkg get src/index.ts createClient
# Output: JSON with { export, types }
```

#### snapshot — Generate full spec

```bash
openpkg snapshot src/index.ts -o openpkg.json      # Write to file
openpkg snapshot src/index.ts -o -                  # Stdout (pipeable)
openpkg snapshot src/index.ts --runtime             # Enable Zod/Valibot extraction
openpkg snapshot src/index.ts --only "use*,create*" # Filter exports
openpkg snapshot src/index.ts --ignore "*Internal"  # Exclude exports
openpkg snapshot src/index.ts --max-depth 4         # Type depth limit
openpkg snapshot src/index.ts --verify              # Exit 1 if any fail
```

| Flag | Description |
|------|-------------|
| `-o, --output <file>` | Output file (default: openpkg.json, `-` for stdout) |
| `--max-depth <n>` | Max type depth (default: 4) |
| `--skip-resolve` | Skip external type resolution |
| `--runtime` | Enable Standard Schema runtime extraction (Zod, Valibot) |
| `--only <exports>` | Filter exports (comma-separated, wildcards) |
| `--ignore <exports>` | Ignore exports (comma-separated, wildcards) |
| `--verify` | Exit 1 if any exports fail |

#### docs — Generate documentation from spec

```bash
openpkg docs openpkg.json -o api.md              # Markdown (default)
openpkg docs openpkg.json -f html -o api.html    # HTML
openpkg docs openpkg.json -f json                # JSON (simplified)
openpkg docs openpkg.json --split -o docs/api/   # One file per export
openpkg snapshot src/index.ts -o - | openpkg docs - -f md  # Pipeline
```

#### diff — Compare specs for breaking changes

```bash
openpkg diff old.json new.json
openpkg diff old.json new.json --summary
# Output: breaking, added, removed, changed, docsOnly, summary.semverBump
```

### Static vs Runtime Extraction

**CRITICAL**: Static analysis misses runtime constraints from schema libraries.

```typescript
// Source: z.string().email().min(3)
```

**Static only** (no `--runtime`):
```json
{ "type": "string" }
```

**With `--runtime`**:
```json
{ "type": "string", "format": "email", "minLength": 3 }
```

The `--runtime` flag:
- Detects TypeScript runtimes (bun, tsx, Node 22+)
- Executes entry file
- Finds Standard JSON Schema exports (`schema['~standard'].jsonSchema`)
- Merges runtime schemas with static analysis

**Always use `--runtime` when documenting packages with Zod, Valibot, ArkType, or TypeBox.**

### How It Works

```
TypeScript Source → [snapshot] → OpenPkg Spec (JSON) → [docs] → Markdown/HTML/JSON
```

The spec is the intermediate format—validate it, diff it, or feed it to any renderer.

### Packages

| Package | Description |
|---------|-------------|
| @openpkg-ts/cli | CLI: `list`, `get`, `snapshot`, `docs`, `diff` |
| @openpkg-ts/sdk | Programmatic SDK for extraction, rendering, querying |
| @openpkg-ts/spec | Spec types, validation, normalization, diffing, semver |
| @openpkg-ts/react | React components (headless + styled with Tailwind v4) |
| @openpkg-ts/ui | Low-level UI primitives (CodeHike, Radix) |
| @openpkg-ts/adapters | Framework adapters (Fumadocs) |

### SDK Primitives

```typescript
import { listExports, getExport, extractSpec, diffSpecs, createDocs } from '@openpkg-ts/sdk';

// List exports
const { exports } = await listExports({ entryFile: './src/index.ts' });

// Get single export
const { export: spec, types } = await getExport({ entryFile: './src/index.ts', exportName: 'myFunc' });

// Extract full spec
const { spec, diagnostics } = await extractSpec({
  entryFile: './src/index.ts',
  maxTypeDepth: 4,
  only: ['use*'],
  ignore: ['*Internal'],
});

// Generate docs
const docs = createDocs(spec);
const markdown = docs.toMarkdown();
const html = docs.toHTML();
```

### Spec Utilities

```typescript
import { validateSpec, normalize, diffSpec, recommendSemverBump } from '@openpkg-ts/spec';

validateSpec(spec);                    // Returns { ok, errors? }
const normalized = normalize(spec);    // Consistent structure
const diff = diffSpec(old, new);       // Compare specs
const { bump, reason } = recommendSemverBump(diff);  // 'major' | 'minor' | 'patch'
```

### React Components

```tsx
// Styled (Tailwind v4)
import { FullAPIReferencePage, FunctionPage, ClassPage } from '@openpkg-ts/react/styled';

// Headless (unstyled)
import { CollapsibleMethod, ParamTable, Signature } from '@openpkg-ts/react';
```

### Fumadocs Adapter

```typescript
import { loader } from 'fumadocs-core/source';
import { openpkgSource, openpkgPlugin } from '@openpkg-ts/adapters/fumadocs';

export const apiSource = loader({
  baseUrl: '/docs/api',
  source: openpkgSource({ spec }),
  plugins: [openpkgPlugin()],
});
```

### Use Cases

- Generate API documentation from TypeScript
- Detect breaking changes between versions
- Build custom doc sites with React components
- Integrate with Fumadocs, Docusaurus, Mintlify

---

## doccov

Documentation coverage and drift detection for TypeScript.

### Install

```bash
npm install -g @doccov/cli
```

### CLI Commands

```bash
# Generate spec (outputs to .doccov/{package}/)
doccov spec

# Check coverage (fail if below threshold)
doccov check --min-coverage 80

# Auto-fix drift issues
doccov check --fix
```

### Badges

Add a documentation health badge to your README:

```markdown
![Docs](https://api.doccov.com/badge/YOUR_ORG/YOUR_REPO?path=.doccov/your-package/doccov.json)
```

For scoped packages:
```markdown
![Docs](https://api.doccov.com/badge/YOUR_ORG/YOUR_REPO?path=.doccov/@your-org/pkg/doccov.json)
```

Requires `.doccov/{package}/doccov.json` committed to your default branch.

### Packages

| Package | Purpose |
|---------|---------|
| @doccov/spec | DocCov spec schema, validation |
| @doccov/sdk | Core SDK |
| @doccov/cli | CLI tool |

### Dependencies

Uses openpkg-ts under the hood for TypeScript extraction.

### Use Cases

- Enforce documentation coverage in CI
- Track documentation drift over time
- Display health badges on repos

---

## secondlayer

Type-safe contract interfaces, functions, and React hooks for Clarity smart contracts.

### Install

```bash
bun add -g @secondlayer/cli
```

### CLI Commands

```bash
# Generate from local .clar files
secondlayer generate ./contracts/token.clar -o ./src/generated.ts

# Generate from deployed contracts (network inferred from address)
secondlayer generate SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.alex-vault -o ./src/generated.ts

# Glob patterns
secondlayer generate "./contracts/*.clar" -o ./src/generated.ts

# With config file
secondlayer init   # creates secondlayer.config.ts
secondlayer generate
```

### Config File

```typescript
// secondlayer.config.ts
import { defineConfig } from '@secondlayer/cli'
import { clarinet, actions, react } from '@secondlayer/cli/plugins'

export default defineConfig({
  out: 'src/generated.ts',
  plugins: [
    clarinet(),  // parse local Clarinet project
    actions(),   // add read/write helpers
    react(),     // generate React hooks
  ],
})
```

### Generated Usage

#### Contract Calls

```typescript
import { token } from './generated/contracts'
import { makeContractCall, fetchCallReadOnlyFunction } from '@stacks/transactions'

// Works with @stacks/transactions directly
await makeContractCall({
  ...token.transfer({ amount: 100n, recipient: "SP..." }),
  network: 'mainnet',
})

await fetchCallReadOnlyFunction({
  ...token.getBalance({ account: "SP..." }),
  network: 'mainnet',
})
```

#### Read/Write Helpers (requires actions plugin)

```typescript
// Read-only
const balance = await token.read.getBalance({ account: "SP..." })

// Write (uses STX_SENDER_KEY env var)
await token.write.transfer({ amount: 100n, recipient: "SP..." })

// Or pass senderKey explicitly
await token.write.transfer({ amount: 100n, recipient: "SP..." }, "<sender-key>")
```

#### Contract State

```typescript
// Maps
const balance = await token.maps.balances.get("SP...")

// Variables
const supply = await token.vars.totalSupply.get()

// Constants
const max = await token.constants.maxSupply.get()
```

#### React Hooks (requires react plugin)

```typescript
import { useTokenTransfer, useTokenBalances } from './generated/hooks'

function App() {
  const { transfer, isRequestPending } = useTokenTransfer()
  const { data: balance } = useTokenBalances("SP...")

  return (
    <button onClick={() => transfer({ amount: 100n, recipient: "SP..." })}>
      Transfer
    </button>
  )
}
```

### Plugins

| Plugin | Description |
|--------|-------------|
| clarinet() | Parse local Clarinet project |
| actions() | Add `read`/`write` helpers |
| react() | Generate React hooks |
| testing() | Generate Clarinet SDK test helpers |

### Network Inference

Address prefix determines network:
- `SP`/`SM` → mainnet
- `ST`/`SN` → testnet

### Use Cases

- Type-safe Clarity contract interactions
- Generate React hooks for dApps
- Testing with Clarinet SDK
- Direct integration with @stacks/transactions
