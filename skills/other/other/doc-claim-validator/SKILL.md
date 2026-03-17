---
name: doc-claim-validator
description: >-
  Validate that claims in documentation match codebase reality. Extracts verifiable
  assertions (file paths, commands, function references, behavioral claims, dependencies)
  from markdown docs and checks them against the actual project. Use after code changes,
  before releases, or when docs feel untrustworthy.
version: 1.0.0
tags: [documentation, validation, quality, verification]
triggers:
  - validate docs
  - verify documentation
  - doc claims
  - docs are wrong
  - documentation accuracy
  - check docs against code
dependencies:
  skills: [doc-maintenance]
  tools: [Grep, Glob, Read, Bash]
token_estimate: ~3000
---

# Documentation Claim Validator

Verify that what documentation *says* is actually *true* by extracting testable claims
and checking them against the codebase. Complements `doc-maintenance` (which handles
structural health) by handling **semantic accuracy**.

## When to Use

- After significant code changes (refactors, renames, API changes)
- Before releases — catch docs that describe removed or changed behavior
- When onboarding devs report "the docs are wrong"
- As a periodic trust audit on project documentation
- After running `doc-maintenance` to go deeper than structural checks

## Quick Reference

| Resource | Purpose | Load when |
|----------|---------|-----------|
| `scripts/extract_claims.py` | Deterministic claim extraction from markdown | Always (Phase 1) |
| `scripts/verify_claims.py` | Automated verification against codebase | Always (Phase 2) |
| `references/claim-taxonomy.md` | Full taxonomy of claim types with examples | Triaging unclear claims |

---

## Workflow Overview

```
Phase 1: Extract    → Pull verifiable claims from docs (deterministic script)
Phase 2: Verify     → Check claims against codebase (automated + AI)
Phase 3: Report     → Classify failures by severity and type
Phase 4: Remediate  → Fix or flag broken claims
```

---

## Phase 1: Extract Claims

Run the extraction script to parse all markdown files and pull out verifiable assertions:

```bash
python3 skills/doc-claim-validator/scripts/extract_claims.py [--json] [--root PATH] [--scope docs|manual|all]
```

The script extracts these claim types from markdown:

| Type | What it captures | Example in docs |
|------|-----------------|-----------------|
| `file_path` | Inline code matching file path patterns | `` `src/auth/login.ts` `` |
| `command` | Code blocks or inline code with shell commands | `` `npm run build` `` |
| `code_ref` | Function, class, method references in inline code | `` `authenticate()` `` |
| `import` | Import/require statements in code blocks | `import { Router } from 'express'` |
| `config` | Configuration keys, env vars, settings | `` `MAX_RETRIES=3` `` |
| `url` | External links (http/https) | `[docs](https://example.com)` |
| `dependency` | Package/library name claims | "Uses Redis for caching" |
| `behavioral` | Assertions about what code does | "The system retries 3 times" |

The first 6 types are extracted deterministically. The last 2 (`dependency`, `behavioral`) require
AI analysis and are handled in Phase 2.

**Output:** A structured list of claims with source file, line number, claim type, and the literal
text of the claim.

---

## Phase 2: Verify Claims

### Step 2a — Automated verification

Run the verification script on the extracted claims:

```bash
python3 skills/doc-claim-validator/scripts/verify_claims.py [--json] [--root PATH] [--claims-file PATH] [--check-staleness]
```

Pass `--check-staleness` to enable git-based drift analysis (see below).

The script checks each claim type differently:

| Claim type | Verification method | Pass condition |
|------------|-------------------|---------------|
| `file_path` | `os.path.exists()` | File exists at referenced path |
| `command` | `shutil.which()` + script check | Binary exists or script file exists |
| `code_ref` | `grep -r` for function/class name | Symbol found in codebase |
| `import` | Check module exists in project or deps | Module resolvable |
| `config` | Grep for config key in source | Key found in config files or code |
| `url` | HTTP HEAD request (optional, off by default) | Returns 2xx/3xx |

Pass `--check-urls` to enable URL verification (slow, requires network).

### Step 2b — AI-assisted verification

After the automated pass, dispatch haiku agents to verify claims the script cannot:

**Agent 1 — Dependency claim verifier** (`subagent_type: "Explore"`, `model: "haiku"`):
Read `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`, or equivalent dependency
manifests. Cross-reference any doc claims about libraries, frameworks, or services used.
Report claims that reference dependencies not in the project.

**Agent 2 — Behavioral claim verifier** (`subagent_type: "Explore"`, `model: "haiku"`):
For each behavioral claim (e.g., "retries 3 times", "caches for 5 minutes", "validates
input before processing"), find the relevant code and verify the claim is accurate.
Report mismatches between documented behavior and actual implementation.

**Agent 3 — Code example verifier** (`subagent_type: "Explore"`, `model: "haiku"`):
For code blocks in docs that show usage examples, verify the function signatures,
parameter names, return types, and import paths match the current codebase. Report
examples that would fail if copy-pasted.

Launch all three agents in parallel.

### Step 2c — Git staleness scoring

For claims that **pass** existence checks, compute a drift score to surface likely-stale claims:

```bash
python3 skills/doc-claim-validator/scripts/verify_claims.py --check-staleness
```

For each passing claim, the script:
1. Gets the doc file's last git modification timestamp
2. Gets the target file(s) last git modification timestamp
3. Counts how many commits touched the target *after* the doc was last edited
4. Assigns a drift score: low (1-3 commits), medium (4-9), high (10+)

High-drift claims are the best candidates for AI review — the target changed heavily
but the doc didn't, so the doc is probably describing outdated behavior.

The staleness report is appended as a ranked table, sorted by score descending.

---

## Phase 3: Report

Merge automated and AI findings into a single report. Classify each failed claim:

### Severity

| Level | Meaning | Example |
|-------|---------|---------|
| **P0** | User-facing doc claims something that would break if followed | Tutorial shows deleted API endpoint |
| **P1** | Dev doc references nonexistent code construct | README references `auth.validate()` which was renamed |
| **P2** | Behavioral claim no longer accurate | "Retries 3 times" but retry logic was removed |
| **P3** | Dependency/import claim outdated | "Uses Express" but migrated to Fastify |
| **P4** | Minor inaccuracy, cosmetic | Config key renamed but behavior unchanged |

### Failure Categories

| Category | Description |
|----------|-------------|
| `missing_target` | Referenced file, function, or symbol doesn't exist |
| `wrong_signature` | Function exists but signature differs from doc |
| `stale_behavior` | Behavioral claim doesn't match implementation |
| `dead_dependency` | Doc references a dependency not in the project |
| `broken_example` | Code example would fail if executed |
| `dead_url` | External link returns 4xx/5xx |
| `phantom_config` | Config option referenced in docs doesn't exist in code |

---

## Phase 4: Remediate

For each failed claim, decide the action:

| Action | When | How |
|--------|------|-----|
| **Update doc** | Code is correct, doc is stale | Edit doc to match code |
| **Flag for review** | Unclear if code or doc is wrong | Create issue for human review |
| **Remove claim** | Referenced feature was deleted | Remove or rewrite section |
| **Update example** | Code example is outdated | Rewrite example against current code |

Route remediation to the appropriate agent per `doc-maintenance` conventions:
- `reference-builder` for API/CLI reference docs
- `technical-writer` for architecture and developer docs
- `learning-guide` for user-facing tutorials and guides

---

## Integration with doc-maintenance

This skill is designed to run **after** `doc-maintenance`:

```
doc-maintenance  →  Structural health (links, orphans, folders, staleness)
doc-claim-validator  →  Semantic accuracy (do claims match reality?)
```

The two skills share the same severity scale and remediation agent routing. Results from
both can be combined into a single documentation health report.

---

## Anti-Patterns

- Do not auto-fix behavioral claims — they require human judgment about intent
- Do not treat every inline code reference as a file path (`` `true` `` is not a file)
- Do not validate claims in archived docs (`docs/archive/`) — they're historical
- Do not fail on optional/conditional features — mark as "conditional" instead
- Do not check URLs by default — it's slow and flaky; opt-in only
- Do not validate code blocks marked with `<!-- no-verify -->` comment

---

## Bundled Resources

### Scripts
- `scripts/extract_claims.py` — Deterministic claim extraction from markdown files
- `scripts/verify_claims.py` — Automated verification of extracted claims against codebase

### References
- `references/claim-taxonomy.md` — Full taxonomy of claim types with extraction patterns and examples
