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

## drift

> Your code changed. Your docs didn't.

Detect documentation drift in TypeScript projects. 21 commands that catch when JSDoc, examples, and markdown fall out of sync with your actual API.

GitHub: https://github.com/ryanwaits/drift

### Architecture

```
Layer 0: @openpkg-ts/spec   (open standard)
Layer 1: @driftdev/sdk       (detection engine)
Layer 2: drift CLI           (21 commands)
```

### Commands

**Composed (Human Surface):** `scan`, `health`, `ci`
**Analysis (Agent Primitives):** `coverage`, `lint`, `examples`
**Extraction:** `extract`, `list`, `get`
**Comparison:** `diff`, `breaking`, `semver`, `changelog`
**Plumbing:** `report`, `release`, `context`, `init`, `config`, `cache`

### Drift Types

15 types across 4 categories:
- **structural** (7) — JSDoc types/params don't match code signature
- **semantic** (3) — deprecation, visibility, broken `{@link}` references
- **example** (4) — @example code has errors or doesn't work
- **prose** (1) — markdown docs import/reference non-existent exports

### Philosophy

- Two surfaces, one engine — composed commands for humans, primitives for agents
- Every primitive is individually addressable — `scan` is a convenience, not a gate
- Detection is the tool's job. Mutation is the agent's job.
- All commands output `{ok, data, meta}` JSON to stdout with `filePath` + `line`

### Claude Code Skill

Ships as `/drift`. Install the skill, then use inside any TypeScript project:
`/drift`, `/drift fix`, `/drift enrich`, `/drift review`, `/drift release`, `/drift docs/`

---

## secondlayer

Developer infrastructure for Stacks. Full blockchain toolkit — 10 packages.

GitHub: https://github.com/ryanwaits/secondlayer

### Architecture

```
@secondlayer/stacks        viem-style typed client (public, wallet, multisig)
@secondlayer/indexer        event indexer (reorg detection, gap backfill)
@secondlayer/views          SQL views on indexed chain data (define, deploy, diff, reindex)
@secondlayer/cli            contract codegen (Clarity → TypeScript)
@secondlayer/sdk            streams query client
@secondlayer/clarity-docs   Clarity documentation standard
@secondlayer/shared         DB (Kysely + Postgres), queues, logging, crypto
@secondlayer/api            Hono REST layer
@secondlayer/auth           auth middleware
@secondlayer/worker         background job processing
```

### @secondlayer/stacks

Viem-style client for Stacks. Public, wallet, and multisig clients with composable actions. HTTP, WebSocket, and fallback transports. Local and provider accounts. Chain definitions (mainnet, testnet, devnet). BNS, PoX, StackingDAO, subscriptions, address validation, STX formatting.

### @secondlayer/indexer

Consumes Stacks node events via HTTP. Parses blocks, transactions, contract events. Detects reorganizations, validates parent hashes, auto-backfills gaps. Enqueues jobs for active streams. Health endpoints for queue status.

### @secondlayer/views

Define SQL views on indexed blockchain data. `defineView`, `validateViewDefinition`, `generateViewSQL`, `deploySchema`, `diffSchema`, `reindexView`. PostgreSQL-backed.

### @secondlayer/cli — Contract Codegen

```bash
bun add -g @secondlayer/cli
secondlayer generate SP3K8BC0PPEVCV7NZ6QSRWPQ2JE9E5B6N3PA0KBR9.alex-vault
```

Config-driven with plugins: `clarinet()`, `actions()`, `react()`, `testing()`. Network inferred from address: `SP`/`SM` → mainnet, `ST`/`SN` → testnet.

```typescript
// Generated usage
const balance = await token.read.getBalance({ account: "SP..." })
await token.write.transfer({ amount: 100n, recipient: "SP..." })
await token.maps.balances.get("SP...")
await token.vars.totalSupply.get()
```

### Use Cases

- Typed Stacks client (like viem for Ethereum)
- Index Stacks events with reorg safety
- Define SQL views on chain data
- Generate type-safe contract bindings
- React hooks for dApps
- Testing with Clarinet SDK
