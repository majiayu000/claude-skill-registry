---
name: software-devtools
description: "Designs developer tools, SDKs, CLIs, IDE extensions, and code generators. Use when shaping DX, typed clients, code generation, or package distribution workflows."
compatibility: Portable core. Works on Claude Code and Codex.
version: "1.1"
last_validated: 2026-07-11
---

# Developer Experience & SDK Engineering

Build tools, SDKs, CLIs, IDE extensions, and code generators that other developers trust and adopt.

## Quick Reference

| Concern | Defaults |
|---|---|
| CLI framework (Node.js) | Commander.js, oclif, Ink (React for CLI) |
| CLI framework (Go) | Cobra + Viper |
| CLI framework (Rust) | clap + dialoguer |
| CLI framework (Python) | Click / Typer |
| SDK design | Typed clients, builder pattern, progressive disclosure |
| Code generation | OpenAPI Generator (self-hosted, free), Fern/Speakeasy (managed, idiomatic SDKs), GraphQL Codegen, Protobuf/Connect, custom AST transforms |
| IDE extensions | VS Code Extension API, JetBrains Plugin SDK, LSP (Language Server Protocol) |
| Package publishing | npm, PyPI, crates.io, NuGet, Maven Central |
| Developer docs | Mintlify, Docusaurus, Starlight, ReadMe, Fern |
| DX metrics | Time-to-first-API-call, SDK adoption, error rate, support tickets |

## When to Use This Skill

- Building a CLI tool for developers (argument parsing, subcommands, interactive prompts)
- Designing and implementing an SDK or client library for an API
- Creating code generators from OpenAPI, GraphQL, or Protobuf schemas
- Building VS Code extensions, JetBrains plugins, or Language Server Protocol implementations
- Publishing packages to registries (npm, PyPI, crates.io, NuGet)
- Measuring and improving developer experience metrics
- Building codemods or AST-based code transformation tools

## When NOT to Use This Skill

- **Building user-facing web or mobile apps** → [software-frontend](../software-frontend/SKILL.md), [software-mobile](../software-mobile/SKILL.md)
- **API design principles (not SDK implementation)** → [dev-api-design](../dev-api-design/SKILL.md)
- **Backend service implementation** → [software-backend](../software-backend/SKILL.md)
- **CI/CD pipeline and platform engineering** → [ops-devops-platform](../ops-devops-platform/SKILL.md)
- **Agent and skill development** → [agents-skills](../agents-skills/SKILL.md), [agents-mcp](../agents-mcp/SKILL.md)
- **Dependency auditing and upgrade strategy** → [dev-dependency-management](../dev-dependency-management/SKILL.md)

## Workflow

1. Classify the tool surface: CLI, SDK, code generator, editor extension, or codemod.
2. Route user-facing app work, backend services, or dependency-policy questions to the adjacent skill when appropriate.
3. Choose the implementation pattern from the decision tree and make the output contract explicit.
4. Apply the relevant guidance for packaging, DX, code generation, or editor integration.
5. Re-check registry, tooling, and platform specifics through the navigation references before final recommendations.

## ASCII Flow

```text
Developer tooling task
  -> Identify user, workflow, repo, and failure mode
  -> Choose CLI, script, IDE, CI, or service integration
  -> Define command shape, config, output, and exit codes
  -> Implement focused tool with tests and docs
  -> Verify current toolchain and platform behavior
  -> Capture migration, rollback, and adoption notes
```

## Decision Tree

```text
What kind of developer tool?
├─ Interactive terminal tool
│  └─ CLI framework per language (Commander.js / Cobra / clap / Typer)
│     ├─ Needs interactive prompts? → Ink, dialoguer, Typer, survey
│     └─ Needs scriptable output? → --json flag, structured stdout
├─ Library other devs import
│  └─ SDK with typed API, clear errors, minimal dependencies
│     ├─ Wrapping a REST API? → Typed client from OpenAPI spec
│     ├─ Wrapping a GraphQL API? → Codegen typed operations
│     └─ General-purpose library? → Builder pattern, progressive disclosure
├─ Editor integration
│  ├─ VS Code only? → VS Code Extension API (largest market share)
│  ├─ Multiple editors? → Language Server Protocol (LSP)
│  └─ JetBrains only? → IntelliJ Plugin SDK
├─ Generate code from schema
│  ├─ OpenAPI → OpenAPI Generator or custom templates
│  ├─ GraphQL → GraphQL Codegen with typed plugins
│  └─ Protobuf → buf + Connect or gRPC codegen
├─ Transform existing code
│  ├─ JavaScript/TypeScript → jscodeshift or ts-morph
│  ├─ Python → libcst
│  └─ Multi-language → custom AST tooling per parser
└─ Developer documentation portal
   ├─ Fast setup, good defaults → Mintlify or Starlight
   └─ Full React flexibility → Docusaurus
```

## SDK Design Principles

Keep the API surface small. Every public method is a commitment.

- **Progressive disclosure**: simple default usage with zero config, advanced options available but not required. `client.send(message)` works out of the box; `client.send(message, { retries: 3, timeout: 5000 })` is there when needed.
- **Builder / fluent pattern**: use for complex configuration — `new ClientBuilder().withAuth(token).withRetries(3).build()`. Avoid deep option objects with 20 fields.
- **Error messages that help**: include what went wrong, why, and how to fix it. Add docs links for common errors. Never expose raw HTTP status codes without context.
- **Typed responses**: return strongly typed objects, not raw JSON. Union types for error states. Discriminated unions over catch-all error types.
- **Semantic versioning**: truly breaking changes are major bumps. Additive features are minor. Bug fixes are patch. Document migration paths for every major version.
- **Minimal dependencies for core**: zero runtime dependencies is the goal. Use peer dependencies for optional integrations. Separate core from plugins.
- **Idiomatic per language**: a Python SDK should feel Pythonic, a Go SDK should feel like Go. Do not port Java patterns to JavaScript.

## CLI Development Patterns

- **Argument parsing**: positional args for required inputs, flags for options, subcommands for distinct operations. `tool <command> [args] [--flags]` is the universal pattern.
- **Subcommand structure**: group related operations. `tool auth login`, `tool auth logout`, `tool config set`. Keep depth to two levels maximum.
- **Interactive prompts**: confirm destructive actions, select from lists, prompt for missing required values. Use `--yes` / `-y` to skip prompts in CI. Keep interactive mode as a fallback when flags are missing — agents cannot press arrow keys or answer interactive prompts, so every input must be passable as a flag.
- **Progress indicators**: spinners for indeterminate work, progress bars for known-length operations. Always provide a `--quiet` / `--silent` flag.
- **Colored output**: use color for emphasis and status (green=success, red=error, yellow=warning). Respect `NO_COLOR` environment variable and `--no-color` flag.
- **Config file discovery**: `~/.config/toolname/config.yaml`, `.toolnamerc`, `toolname.config.js` — support a sensible hierarchy with local overrides.
- **Exit codes**: 0 for success, 1 for general errors, 2 for usage errors. Document non-zero codes in help text.
- **Shell completions**: generate completions for bash, zsh, fish. Ship them or provide `tool completions <shell>` command.
- **`--json` flag**: every command that produces output should support `--json` for machine-readable structured output. Scriptability is not optional.

## Agent-Friendly CLI Patterns

Agents are now primary CLI consumers alongside humans. Design for both.

- **Non-interactive first**: every input passable as a flag. If your CLI drops into a prompt mid-execution, an agent is stuck. Interactive mode is the fallback when flags are missing, not the primary path.
- **Progressive `--help` discovery**: don't dump all docs upfront. An agent runs `mycli`, sees subcommands, picks one, runs `mycli deploy --help`, gets what it needs. No wasted context on commands it won't use.
- **Examples in every `--help`**: agents pattern-match off `mycli deploy --env staging --tag v1.2.3` faster than they read a description. Every subcommand's help should include at least two usage examples.
- **Flags and stdin for everything**: agents think in pipelines. Accept `--stdin` for config import, support `--output tag-only` for chaining. Don't require positional args in unusual orders.
- **Fail fast with actionable errors**: if a required flag is missing, error immediately and show the correct invocation. Include a "did you mean?" or "available values" hint. Agents self-correct when given something to work with.
- **Idempotent commands**: agents retry constantly (network timeouts, context loss). Running the same deploy twice should return "already deployed, no-op", not create a duplicate.
- **`--dry-run` for destructive actions**: agents should preview what a deploy or deletion would do before committing. Let them validate the plan, then run it for real.
- **`--yes` / `--force` to skip confirmations**: humans get "are you sure?" prompts; agents pass `--yes` to bypass. Make the safe path the default but allow bypassing.
- **Predictable command structure**: if an agent learns `mycli service list`, it should be able to guess `mycli deploy list` and `mycli config list`. Pick a pattern (resource + verb or verb + resource) and use it everywhere.
- **Return data on success**: show the deployment ID, URL, and duration — not just a success emoji. Machine-parseable output lets agents chain results into subsequent commands.

## Code Generation

- **Schema-driven**: OpenAPI spec to typed client, GraphQL schema to types and hooks, Protobuf to service stubs. The schema is the source of truth — generated code stays in sync automatically.
- **Template-based**: Handlebars, EJS, or custom template engines for project scaffolding and boilerplate generation. Templates should be overridable by consumers.
- **AST-based transforms**: jscodeshift for JavaScript/TypeScript codemods, ts-morph for TypeScript-specific transforms, libcst for Python. Use AST manipulation when regex replacement is fragile.
- **Golden rule**: generated code should look like human-written code. Run the project's formatter and linter on output. No `/* DO NOT EDIT */` walls of shame — use `.gitattributes` with `linguist-generated=true` instead.
- **Regeneration safety**: mark generated files clearly. Provide `--dry-run` to preview changes. Support partial regeneration (only changed schemas).
- **Custom generators**: when off-the-shelf generators do not fit, build custom ones. Parse the schema, walk the AST, emit code through templates. Test generated output by compiling and running it.

## IDE Extension Development

- **VS Code extension lifecycle**: `activate()` on first use of a contribution point, `deactivate()` for cleanup. Keep activation lightweight — defer heavy work.
- **Contribution points**: commands (command palette), views (sidebar panels, tree views), language features (syntax highlighting, snippets, hover info), debugging.
- **Language Server Protocol**: implement LSP for multi-editor support. One server, many clients (VS Code, Neovim, Emacs, Helix). Handles completions, diagnostics, go-to-definition, hover, formatting.
- **Webview panels**: for rich UIs inside the editor. Use message passing between extension and webview. Avoid heavy frameworks — keep webview bundles small.
- **Testing extensions**: use `@vscode/test-electron` for integration tests. Mock VS Code APIs for unit tests. Test LSP servers independently with protocol-level tests.
- **Distribution**: VS Code Marketplace (`.vsix` packages) remains the default for VS Code-proper users; Open VSX (Eclipse Foundation, vendor-neutral, reached 1.0 in 2026 with AWS/Google-backed managed hosting) is the registry for VS Code forks — Cursor, VSCodium, Windsurf, and others that cannot use Microsoft's marketplace terms. Publish to both when the extension should reach fork users. JetBrains Marketplace for IntelliJ plugins.

## Package Publishing Best Practices

- **Semantic versioning**: the version number is a contract. Truly breaking changes require a major bump — not just a changelog note.
- **Changelogs**: use conventional commits (`feat:`, `fix:`, `breaking:`) and auto-generate changelogs. Keep a human-readable `CHANGELOG.md` for significant releases.
- **Provenance and trusted publishing**: npm trusted publishing (OIDC from GitHub Actions or GitLab CI, no long-lived `NPM_TOKEN`) reached general availability in mid-2025 and is the current default for CI-published packages — provenance attestations are generated automatically under it, so the manual `--provenance` flag is only needed for non-OIDC publish paths. Sigstore backs the attestation signing. Verify current requirements (npm CLI version, supported CI providers) at npm's docs before wiring a release pipeline, since provider support has been expanding.
- **Dual CJS/ESM for Node.js**: ship both CommonJS and ES Modules. Use `exports` field in `package.json` for conditional resolution. Test both entry points.
- **Tree-shaking support**: use `sideEffects: false` in `package.json`. Avoid barrel files that defeat dead-code elimination. Export granularly.
- **Deprecation strategy**: deprecate old versions with `npm deprecate` or equivalent. Provide migration guides. Keep security patches flowing to previous major for 6-12 months.

### Pre-Publish Checklist

- [ ] Tests pass from a clean install (`rm -rf node_modules && npm ci && npm test`)
- [ ] Build output is current and committed (or generated in CI)
- [ ] `package.json` fields verified: `main`, `types`, `exports`, `files`
- [ ] Bundle size checked (use `bundlephobia`, `size-limit`, or `npm pack | gzip -c | wc -c`)
- [ ] Install tested from tarball: `npm pack && npm install ./pkg.tgz` in a fresh project
- [ ] Both CJS and ESM entry points import without error
- [ ] `CHANGELOG.md` updated; migration guide written for any breaking change
- [ ] Provenance attestation enabled — prefer npm trusted publishing (OIDC, CI `id-token: write` permission, no static token in CI) over the manual `--provenance` flag path
- [ ] Publish credentials scoped and short-lived: no long-lived npm/PyPI tokens sitting in CI secrets if trusted publishing is available for the registry; 2FA enforced on maintainer accounts

### Supply-Chain Hardening (npm ecosystem)

The npm ecosystem has had large, self-propagating compromises — the "Shai-Hulud" worm (first wave September 2025, a second wave in November 2025) backdoored hundreds of popular packages via a malicious install script that harvested CI/CD secrets and used any npm tokens it found to publish trojanized versions of the maintainer's other packages, spreading worm-style across the registry. Treat this as the current baseline threat model for anything you publish or depend on, not a one-off incident:

- **Prefer trusted publishing (OIDC) over long-lived publish tokens** so there is no static npm token in CI for malware to steal and reuse.
- **Lock dependencies and commit the lockfile**; pin exact versions for CI/build tooling, and gate dependency bumps through review rather than auto-merge for anything with install/build scripts.
- **Treat `postinstall`/`preinstall` scripts as a red flag.** Audit them before allowing a new or updated dependency in; consider `npm install --ignore-scripts` in CI where the build does not need them.
- **Verify provenance attestations** on security-sensitive dependencies rather than trusting the package name and version alone.
- **Scope CI credentials tightly** (short-lived, least-privilege, no IMDS/cloud-key exposure to build steps that do not need it) — the worm's exfiltration path relied on broadly-scoped tokens and environment variables being reachable from install scripts.
- Apply the same scrutiny to editor-extension registries: 2026 saw malicious extensions distributed through open extension marketplaces, so treat "IDE Extension Development" installs (below) with the same install-time skepticism as npm packages.

## Tool-Adoption Judgment

Devtools churn fast — a new build tool, linter, or runtime claims a 10-100x speedup every few months. Most teams should not chase them. Judgment, not hype, decides the toolchain.

- **Adoption gate, not a vibe check**: before swapping a load-bearing tool (bundler, test runner, package manager, CLI framework), require the new tool to clear three bars — (1) it fixes a measured pain, not a hypothetical one; (2) migration cost is bounded and reversible; (3) the team can name who owns the fallback plan if the new tool stalls. If any bar fails, stay put.
- **Stability beats speed for anything on the critical path.** A 2x faster linter that breaks CI intermittently costs more than it saves. Prefer the boring, widely-adopted default (the tool with years of production use, a large plugin ecosystem, and a maintainer team that isn't a single person) unless the team has a concrete, current bottleneck the boring tool cannot solve.
- **When NOT to migrate a toolchain**: the current tool still meets correctness and speed needs; the team is mid-release or mid-incident-response; the "faster" alternative is < 1.0 or has a churny API (breaking changes every few months); no one on the team has bandwidth to own the migration and its rollback. Rewrite build tooling in a dedicated, isolated window — never as a rider on unrelated feature work.
- **The DX metric that matters most day to day is local feedback-loop time**: seconds from save to test-result or save to reload, not headline benchmark numbers. A tool that trims CI minutes but adds friction to the local edit-test loop is a net DX loss for most teams.
- **Boring-tooling default for teams without a dedicated platform function**: pick the ecosystem's most-adopted, longest-lived option per language (see Quick Reference) and revisit only when a specific, named pain shows up — not on a schedule and not because a blog post said so.
- **Verify claims before committing to a rewrite.** Devtools marketing overstates stability and adoption; check current release cadence, open-issue trends, and whether the "default" status is actually shipped (opt-in and announced-only are not the same as default-on) before basing a migration decision on it.

## DX Metrics

| Metric | Target | Signal when off |
|--------|--------|-----------------|
| Local feedback-loop time (save → test result / reload) | < 2 seconds for unit tests, < 1 second for HMR | Slow inner loop kills iteration speed faster than any CI metric |
| Time-to-first-API-call | < 5 minutes from `npm install` | Onboarding friction; simplify the quickstart |
| Onboarding drop-off rate | Track per step in the guide | High drop-off at a specific step → missing example or broken link |
| SDK version adoption (latest major) | > 60% within 3 months of release | Breaking-change pain or missing migration docs |
| Error rate by method | < 1% for common operations | Fix SDK error messages and docs; don't just add FAQ entries |
| Support ticket clustering | Track top-3 recurring topics | Recurring questions → undiscoverable API surface |
| Developer NPS / satisfaction | Quarterly pulse; structured interviews | Quantitative metrics miss the "this feels bad" signals |

## Do / Avoid

**Do**

- Design the API surface for the 80% use case first; make the 20% possible but not mandatory.
- Write error messages that tell the developer what went wrong, why, and what to do about it.
- Ship shell completions, `--json` output, and `--help` with examples from day one.
- Test your SDK in the same way your consumers will use it — install from the registry, follow the quickstart.
- Run the project's formatter on generated code so it matches the surrounding codebase.
- Measure time-to-first-API-call and iterate on the onboarding flow until it drops below 5 minutes.
- Publish changelogs and migration guides for every major version.
- Respect `NO_COLOR`, `--quiet`, and `--yes` flags in every CLI tool.

**Avoid**

- Exposing internal implementation details (HTTP status codes, raw error bodies, internal IDs) through the public SDK surface.
- Adding dependencies to core packages that consumers do not need — use peer dependencies or plugins.
- Shipping generated code that looks auto-generated (inconsistent formatting, `__generated__` noise, excessive comments).
- Breaking backward compatibility in minor or patch releases.
- Building IDE extensions with heavy activation costs — defer expensive initialization.
- Skipping the pre-publish checklist (bundle size, type correctness, install test).
- Ignoring developer feedback and support ticket patterns as DX signals.
- Porting idioms from one language to another (Java patterns in a Python SDK, Ruby patterns in a Go CLI).

## Known Traps

- Letting the public SDK or CLI surface leak internal transport quirks, unstable IDs, or backend-specific retry semantics.
- Treating code generation as a one-time scaffolding concern instead of a product surface with readability, compatibility, and regeneration guarantees.
- Verifying a package only from the source tree rather than from the packed artifact consumers actually install.
- Building an IDE extension with heavy startup work in the activation path, then discovering the tool feels broken before it does anything useful.
- Shipping human-friendly output only, then discovering automation and agent workflows have no stable machine-readable contract.

## Common Anti-Patterns

- Exposing every backend feature immediately instead of curating the smallest stable developer surface.
- Using breaking output-format changes in CLIs or generators without versioning, feature flags, or migration notes.
- Building one monolithic package that mixes core runtime, integrations, templates, and experimental features.
- Measuring adoption only by install counts while ignoring time-to-first-success, support load, and version-upgrade pain.
- Designing tools for maintainers who know the internals instead of external developers who only see the docs and errors.

## Scenarios

Recipes keyed to DX or distribution moments. Each lists the shortest path to a ship-ready, consumer-safe outcome.

### S1 — SDK release with semver + changeset

1. Install `changesets` (`@changesets/cli`); run `changeset init` to create the `.changeset/` directory.
2. For each PR, contributors run `changeset` to declare the semver bump level and write a change summary.
3. On merge to `main`, the Changesets GitHub Action opens a "Release PR" that aggregates bumps and updates `CHANGELOG.md`.
4. Merge the Release PR; the action publishes to the registry and creates a Git tag.
5. Verify the published package with `npm pack` + install from tarball before merging the Release PR.
6. For breaking changes: include a migration guide in the changeset body; link it from the npm package README.

### S2 — CLI for AI agent consumption (structured errors, --json)

1. Add `--json` to every subcommand; on success, emit `{ "ok": true, "data": { ... } }`; on error, emit `{ "ok": false, "error": { "code": "...", "message": "..." } }`.
2. Use exit code 0 for success, 1 for runtime errors, 2 for usage errors; document codes in `--help`.
3. Make every required input passable as a flag; never rely on interactive prompts as the only path.
4. Add `--dry-run` to all destructive commands; agents validate the plan before committing.
5. Add `--yes` to skip confirmation prompts; agents pass it in automation contexts.
6. Run the CLI through an agent smoke test: have an LLM issue three chained commands using only `--help` output for discovery.

### S3 — OpenAPI to typed SDK generation pipeline

1. Confirm the OpenAPI spec is the source of truth; set up spec linting in CI. `spectral` is the long-time incumbent but has seen little investment since its Stoplight/SmartBear acquisition and lags OpenAPI 3.2 — check current maintenance activity before adopting it fresh, and consider Redocly's linter or a vendor SDK-generator's built-in linter as alternatives.
2. Choose a generator: `openapi-generator-cli` (free, self-hosted, Java-based, 50+ language targets) for full control and zero cost, or a managed generator such as `fern` (acquired by Postman in early 2026) or Speakeasy for idiomatic, low-maintenance SDKs with synced docs. Managed generators cost money and add a vendor dependency — pick them when SDK polish and low upkeep matter more than self-hosting.
3. Run generation in CI on every spec change; commit generated files with `linguist-generated=true` in `.gitattributes`.
4. Add a compile-only test that imports the generated client and calls one method; catches schema drift before release.
5. Run the project formatter on generated output; generated code must match the surrounding codebase style.
6. Version the generated SDK separately from the spec; publish via the changeset flow in S1.

### S4 — LSP for custom DSL: incremental parsing + diagnostics

1. Implement the language server using the LSP SDK for your language (e.g. `vscode-languageserver` for Node.js, `tower-lsp` for Rust).
2. Use a tree-sitter grammar or hand-written incremental parser; never re-parse the full document on every keystroke.
3. On `textDocument/didChange`, apply incremental edits to the parse tree; publish diagnostics via `textDocument/publishDiagnostics`.
4. Implement `textDocument/completion` and `textDocument/hover` using the AST node at the cursor position.
5. Write protocol-level tests with a mock LSP client; test diagnostics, completions, and hover independently of any editor.

### S5 — IDE extension auth + token refresh

1. Store tokens in the platform secret store (`vscode.SecretStorage`, not `globalState`); never in `settings.json`.
2. On extension activation, check for a stored token; if absent, open the auth flow via `vscode.env.openExternal` + a local callback server.
3. Before each API call, check token expiry; if within 60 seconds, refresh silently using the refresh token.
4. On `401` from the API, treat the token as revoked: clear stored credentials and re-trigger the auth flow.
5. Keep activation lightweight: defer the auth check and API calls until the user invokes a command, not at `activate()`.

## Navigation

### References
- [references/sdk-and-cli-checklist.md](references/sdk-and-cli-checklist.md) — SDK ergonomics, CLI conventions, and code-generation review checklist
- [references/publishing-and-support.md](references/publishing-and-support.md) — release, package-signing, docs, support, and deprecation workflow
- [references/mcp-server-development.md](references/mcp-server-development.md) — when and how to expose a developer tool as an MCP server; tool/resource/prompt design; testing and distribution
- [data/sources.json](data/sources.json) — official docs for SDK, CLI, IDE, and package-publishing ecosystems

### Related Skills

- [dev-api-design](../dev-api-design/SKILL.md) — API design principles and REST/GraphQL conventions
- [software-backend](../software-backend/SKILL.md) — General backend service patterns
- [software-frontend](../software-frontend/SKILL.md) — Frontend application development
- [ops-devops-platform](../ops-devops-platform/SKILL.md) — CI/CD pipeline and platform engineering
- [dev-dependency-management](../dev-dependency-management/SKILL.md) — Dependency auditing and upgrade strategy
- [docs-codebase](../docs-codebase/SKILL.md) — Codebase documentation standards

## Freshness Protocol

When users ask about current CLI frameworks, SDK patterns, code generation tools, or package publishing best practices, verify current information before answering.

### Trigger Conditions

- "What's the best CLI framework for [language]?"
- "How should I structure my SDK?"
- "What code generation tool should I use for OpenAPI/GraphQL?"
- "How do I publish to npm/PyPI/crates.io?"
- "Is [tool/framework] still maintained?"

### How to Freshness-Check

1. Start from [data/sources.json](data/sources.json) (official docs, release notes, framework comparisons).
2. Run a targeted web search for the specific tool or framework.
3. Check GitHub repository activity (last release date, open issues, commit frequency).

### What to Report

- **Current landscape**: what is stable and widely used now
- **Emerging trends**: what is gaining traction (and why)
- **Deprecated/declining**: what is falling out of favor (and why)
- **Recommendation**: default choice + 1-2 alternatives, with trade-offs

## Fact-Checking

- Known bugs, regressions, framework/compiler/runtime footguns, and version-specific crash or workaround guidance must be verified against current primary web sources before being treated as current fact.
- Use web search/web fetch to verify current external facts, versions, pricing, deadlines, regulations, or platform behavior before final answers.
- Prefer primary sources; report source links and dates for volatile information.
- If web access is unavailable, state the limitation and mark guidance as unverified.

## Learnings Loop

Before applying this skill on a non-trivial task, read `learnings.consolidated.md` in this directory (and `learnings.md` if present).

After applying it, if you encountered a pattern worth remembering, a mistake worth preventing, or a domain fact that surprised you, append one dated bullet to `learnings.md` via `agents-skills-feedback-loop/scripts/append_learning.py`. Do not modify `SKILL.md` itself.

