---
name: organon-tools-developer
description: Enforces organon-tools ETHOS.md and PHILOSOPHY.md constraints during development. Use when adding CLI commands, verification gates, MCP tools, or fixing bugs in packages/tools/. Ensures 6 invariants (schema fidelity, test coverage, gates fail not warn, machine-parsable output, idempotency, semver) and 5 design principles (fail-fast, composability, testability, clarity).
protocol_id: PROTO-ORG-2
protocol_file: organon/protocols/PROTOCOLS.md
tools: [organon-verify, npm-test]
loads:
  - organon/domains/tools/ETHOS.md
  - organon/domains/tools/PHILOSOPHY.md
  - book-llms/three-layer-architecture.md
  - CLAUDE.md
context: fork
agent: general-purpose
---

# Organon Tools Developer Skill

> A Claude skill for agents developing organon-tools — ensures the tools that enforce methodology are built using methodology.

---

## When to Use This Skill

Use this skill when:
- Adding a new CLI command (`organon <command>`)
- Adding a new verification gate
- Adding a new MCP tool/prompt/resource
- Evolving the methodology specification (book-llms/)
- Fixing bugs or refactoring organon-tools code

**Purpose:** Ensure organon-tools development follows its own ETHOS.md constraints and PHILOSOPHY.md design decisions.

---

## Identity Check (Always Start Here)

Before any work, load and internalize:

1. **Read `organon/domains/tools/ETHOS.md`** - 6 invariants, 5 principles, 8 heuristics
2. **Read `organon/domains/tools/PHILOSOPHY.md`** - 5 design decisions and trade-offs
3. **Read `book-llms/three-layer-architecture.md`** - If working on verification gates

**Critical constraint:** This tool builds tools that enforce methodology. The builder must follow what it builds.

---

## The 6 Invariants (Never Violate)

From `organon/domains/tools/ETHOS.md`:

1. **Schema fidelity** - Frontmatter parser matches `book-llms/frontmatter-system.md` exactly
2. **Every command has tests** - No untested code ships
3. **Gates fail builds, not warn** - Verification gates produce pass/fail, never soft warnings
4. **Machine-parsable output** - All commands support `--format json`
5. **Idempotent operations** - Same input = same output, no side effects
6. **Breaking changes require major version bump** - CLI, JSON schema, frontmatter schema

**If your change violates any invariant, STOP and redesign.**

---

## The 5 Design Principles (Prioritized)

From `organon/domains/tools/ETHOS.md`:

1. **Schema fidelity over convenience** - When book-llms/ spec conflicts with ease-of-use, spec wins
2. **Fail-fast over forgiving** - Invalid input blocks execution, errors surface immediately
3. **Composability over monoliths** - Commands work in Unix pipelines
4. **Testability over implementation speed** - Pure functions with tests, thin CLI wrappers
5. **Clarity over brevity** - Error messages explain what failed and how to fix it

---

## Core Architecture Pattern

From `organon/domains/tools/PHILOSOPHY.md`:

```
src/
├── core/                   ← Pure functions (no I/O, no console, no process.exit)
│   ├── types.ts            ← FileSystem interface, result types
│   ├── <feature>.ts        ← Pure logic with tests
│   └── <feature>.test.ts   ← Vitest tests (>90% coverage)
├── cli/commands/           ← Thin wrappers (yargs handlers)
│   └── <command>.ts        ← Parse args → call core → format output
└── mcp/                    ← Thin MCP adapters
    ├── tools.ts            ← Wrap core functions as MCP tools
    └── prompts.ts          ← Methodology workflow templates
```

**Pattern:** Core logic is pure and testable. CLI and MCP are thin adapters.

---

## Workflow 1: Adding a New CLI Command

**Example:** Adding `organon check-links` command

1. **Design phase** (before coding):
   - [ ] What does it do? (one sentence)
   - [ ] Is it idempotent? (same input = same output?)
   - [ ] Does it support `--format json`?
   - [ ] What exit codes? (0 = success, 1 = failure)
   - [ ] Does it compose with other commands?

2. **Implementation phase**:
   ```bash
   # Create core utility (pure function)
   touch src/core/check-links.ts
   touch src/core/check-links.test.ts

   # Create CLI command wrapper
   touch src/cli/commands/check-links.ts
   ```

3. **Core utility structure** (`src/core/check-links.ts`):
   ```typescript
   import { FileSystem, Result } from './types';

   export interface CheckLinksOptions {
     projectRoot: string;
     // ... other options
   }

   export interface CheckLinksResult {
     success: boolean;
     brokenLinks: Array<{ file: string; link: string; reason: string }>;
   }

   export async function checkLinks(
     options: CheckLinksOptions,
     fs: FileSystem
   ): Promise<CheckLinksResult> {
     // Pure logic here - no console.log, no process.exit
     // Return structured results
   }
   ```

4. **Write tests first** (`src/core/check-links.test.ts`):
   ```typescript
   import { describe, it, expect } from 'vitest';
   import { checkLinks } from './check-links';
   import { MockFileSystem } from './test-utils';

   describe('checkLinks', () => {
     it('detects broken links', async () => {
       const fs = new MockFileSystem({ ... });
       const result = await checkLinks({ projectRoot: '.' }, fs);
       expect(result.brokenLinks).toHaveLength(1);
     });

     // ... more tests
   });
   ```

5. **CLI wrapper** (`src/cli/commands/check-links.ts`):
   ```typescript
   import yargs from 'yargs';
   import { checkLinks } from '../../core/check-links';
   import { NodeFileSystem } from '../../core/node-fs';

   export const checkLinksCommand: yargs.CommandModule = {
     command: 'check-links',
     describe: 'Check for broken links in organon files',
     builder: (yargs) => {
       return yargs
         .option('format', {
           choices: ['human', 'json'] as const,
           default: 'human' as const,
         });
     },
     handler: async (args) => {
       const fs = new NodeFileSystem();
       const result = await checkLinks({ projectRoot: process.cwd() }, fs);

       if (args.format === 'json') {
         console.log(JSON.stringify(result, null, 2));
       } else {
         // Human-readable output
         if (result.brokenLinks.length === 0) {
           console.log('✓ No broken links found');
         } else {
           console.error('✗ Found broken links:');
           result.brokenLinks.forEach(l => {
             console.error(`  ${l.file}: ${l.link} (${l.reason})`);
           });
         }
       }

       process.exit(result.success ? 0 : 1);
     },
   };
   ```

6. **Register command** (in `src/cli/index.ts`):
   ```typescript
   import { checkLinksCommand } from './commands/check-links';

   yargs
     .command(checkLinksCommand)
     // ... other commands
   ```

7. **Verification checklist**:
   - [ ] Core function is pure (no I/O, no console, no process.exit)
   - [ ] Tests exist and pass (`npm test`)
   - [ ] Coverage >90% for core logic
   - [ ] Command supports `--format json`
   - [ ] Command is idempotent
   - [ ] Help text exists (`organon check-links --help`)
   - [ ] Error messages are clear and actionable
   - [ ] README.md updated with example usage
   - [ ] No TypeScript compilation errors (`npm run build`)

---

## Workflow 2: Adding a New Verification Gate

**Example:** Adding a "freshness" gate that checks last-modified dates

1. **Update specification first**:
   - [ ] Add gate description to `book-llms/three-layer-architecture.md`
   - [ ] Define what it checks, when it fails, how to fix
   - [ ] Commit spec changes before implementation

2. **Implementation** (follow Workflow 1 pattern):
   ```bash
   # Core logic
   touch src/core/verify-freshness.ts
   touch src/core/verify-freshness.test.ts
   ```

3. **Gate structure** (`src/core/verify-freshness.ts`):
   ```typescript
   import { FileSystem, VerificationResult } from './types';

   export async function verifyFreshness(
     projectRoot: string,
     fs: FileSystem
   ): Promise<VerificationResult> {
     return {
       gate: 'freshness',
       passed: boolean,
       errors: Array<{ file: string; message: string; fix: string }>,
       warnings: [], // Gates never warn, only fail
     };
   }
   ```

4. **Register gate** (in `src/core/verify.ts`):
   ```typescript
   import { verifyFreshness } from './verify-freshness';

   const GATES = {
     'freshness': verifyFreshness,
     // ... other gates
   };
   ```

5. **Test coverage requirements**:
   - [ ] 100% coverage for verification gate logic (stricter than general 90% requirement)
   - [ ] Test pass cases
   - [ ] Test all failure modes
   - [ ] Test fix suggestions are actionable

6. **Update CLI** (`src/cli/commands/verify.ts`):
   ```typescript
   .option('gate', {
     type: 'array',
     choices: ['frontmatter', 'references', 'triplets', 'coverage', 'freshness'],
     description: 'Run specific gates (defaults to all)',
   })
   ```

7. **Verification checklist**:
   - [ ] Spec updated in `book-llms/three-layer-architecture.md` FIRST
   - [ ] Gate fails builds (exit 1), never warns
   - [ ] 100% test coverage for gate logic
   - [ ] Error messages include file path, line number, and fix suggestion
   - [ ] Gate registered in verify.ts
   - [ ] CLI updated with new gate option
   - [ ] README.md documents the new gate
   - [ ] `organon verify --gate freshness` works

---

## Workflow 3: Adding a New MCP Tool/Prompt

**Example:** Adding `organon_check_dependencies` MCP tool

1. **Core function exists** (or create it following Workflow 1)

2. **Add MCP tool** (`src/mcp/tools.ts`):
   ```typescript
   {
     name: 'organon_check_dependencies',
     description: 'Check if organon file dependencies are satisfied',
     inputSchema: {
       type: 'object',
       properties: {
         file: { type: 'string', description: 'Path to organon file' },
       },
       required: ['file'],
     },
     handler: async (args) => {
       const result = await checkDependencies(args.file, fs);
       return {
         content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
       };
     },
   }
   ```

3. **Add MCP prompt** (`src/mcp/prompts.ts`) - If it's a workflow:
   ```typescript
   {
     name: 'check-organon-dependencies',
     description: 'Workflow for verifying organon dependency chains',
     arguments: [
       { name: 'scope', description: 'Scope to check (product, domain, feature)', required: false },
     ],
     handler: async (args) => {
       return {
         messages: [
           {
             role: 'user',
             content: {
               type: 'text',
               text: `# Check Organon Dependencies Workflow\n\n...`,
             },
           },
         ],
       };
     },
   }
   ```

4. **Verification checklist**:
   - [ ] Tool wraps existing core function (don't duplicate logic)
   - [ ] Input schema is clear and validates properly
   - [ ] Output is structured JSON
   - [ ] Tool registered in `src/mcp/server.ts`
   - [ ] MCP-SETUP.md updated with usage example
   - [ ] Test with `organon mcp` and verify tool appears

---

## Workflow 4: Evolving the Methodology (RFC-Aware)

**Example:** Adding a new frontmatter field

**DANGER ZONE:** Changes to `book-llms/` affect ALL projects using Organon.

1. **RFC pattern** (from `book-llms/patterns.md`):
   - [ ] Create `book-llms/rfcs/RFC-NNN-<title>.md`
   - [ ] Document: Problem, Proposal, Trade-offs, Migration path
   - [ ] Get consensus (in this project: ensure it aligns with ETHOS.md)
   - [ ] Update spec (`book-llms/frontmatter-system.md`)
   - [ ] Update implementation (`packages/tools/src/core/frontmatter-parser.ts`)
   - [ ] Update tests
   - [ ] Document migration in CHANGELOG.md
   - [ ] Bump version (breaking = major, additive = minor)

2. **Breaking change checklist** (requires major version bump):
   - [ ] Does it change frontmatter schema? (breaking)
   - [ ] Does it change CLI interface? (breaking)
   - [ ] Does it change JSON output schema? (breaking)
   - [ ] Does it remove/rename a command? (breaking)
   - [ ] If any YES, bump major version

3. **Invariant check**:
   - **Schema fidelity:** Implementation must match spec exactly
   - **Breaking changes require major version bump:** Semver enforced

---

## Common Pitfalls (Don't Do This)

1. **❌ Adding logic to CLI commands** → ✅ Add to `src/core/`, CLI is thin wrapper
2. **❌ Using `console.log` in core functions** → ✅ Return structured results, CLI formats
3. **❌ Using `process.exit` in core functions** → ✅ Return success/failure, CLI exits
4. **❌ Writing tests after code** → ✅ Write tests first (TDD pattern)
5. **❌ Making gates warn instead of fail** → ✅ Gates fail builds (INV-TOOLS-3)
6. **❌ Skipping `--format json` support** → ✅ All commands must support it (INV-TOOLS-4)
7. **❌ Implementing before spec updated** → ✅ Update book-llms/ spec first
8. **❌ Auto-fixing invalid frontmatter** → ✅ Fail-fast, force user to fix (principle #2)

---

## Pre-Commit Verification

Before committing ANY code:

```bash
# 1. Tests pass
npm test

# 2. No TypeScript errors
npm run build

# 3. Self-verification (dogfooding)
npm run organon verify

# 4. Coverage check (>90% for core, 100% for gates)
npm run test:coverage
```

**If any fail, do not commit.**

---

## When in Doubt

1. **Check ETHOS.md** - Does this violate an invariant?
2. **Check PHILOSOPHY.md** - Does this align with design decisions?
3. **Check three-layer-architecture.md** - Is this the right pattern for gates?
4. **Ask:** Would this tool enforce what I'm about to build?

**Remember:** Organon-tools builds tools that enforce methodology. If you wouldn't want the tool to allow this pattern, don't implement it.

---

## Meta-Principle

> The tools that enforce constraints must be built with more discipline than the code they govern.

If organon-tools has untested code, how can it enforce test coverage on others?
If organon-tools has invalid frontmatter, how can it validate others?
If organon-tools violates its own ETHOS.md, the methodology loses credibility.

**Build the tools you wish existed when auditing someone else's work.**

---

## Error Recovery

| Failure | Recovery Action |
|---------|-----------------|
| Tests fail | Fix implementation to match test expectations. Do not skip or disable tests. |
| Coverage below threshold (>90% core, 100% gates) | Add missing test cases for uncovered branches. Use `npm run test:coverage` to identify gaps. |
| TypeScript compilation errors | Fix type issues. Do not use `any` or `@ts-ignore` as workarounds. |
| Gate warns instead of failing | Change gate to produce pass/fail exit codes. Invariant INV-TOOLS-3: gates fail builds, never warn. |
| `--format json` not supported | Add JSON output format. Invariant INV-TOOLS-4: all commands must support `--format json`. |
| Breaking change detected | Bump major version. Invariant INV-TOOLS-6: breaking changes require major version bump. |
| Spec not updated before implementation | Stop. Update `book-llms/` specification first, then implement to match. Spec is source of truth. |
