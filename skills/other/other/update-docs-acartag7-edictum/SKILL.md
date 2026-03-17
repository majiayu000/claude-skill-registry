---
name: update-docs
description: Sync documentation with code changes. Use on every PR that touches library code to keep docs accurate and consistent.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# Update Docs

Ensures documentation stays in sync with code changes. Run before or during every PR that touches library code.

## Before anything else

1. **Read CLAUDE.md** — understand tier boundaries (core vs ee/), dropped features, and session model
2. **Read .docs-style-guide.md** — binding terminology reference

## Step 1: Detect what changed

```bash
git diff main...HEAD --name-only
```

Map changes to affected docs:

| Source file | Affected doc pages |
|---|---|
| `src/edictum/pipeline.py`, `contracts.py` | concepts/how-it-works.md, architecture.md |
| `src/edictum/yaml_engine/` | contracts/yaml-reference.md, contracts/operators.md |
| `src/edictum/adapters/*.py` | corresponding adapters/*.md page |
| `src/edictum/session.py`, `limits.py` | concepts/contracts.md, architecture.md |
| `src/edictum/audit.py`, `telemetry.py` | audit/sinks.md, audit/telemetry.md |
| `src/edictum/cli/` | cli.md |
| `src/edictum/envelope.py` | concepts/principals.md, architecture.md |
| `pyproject.toml` (version) | install commands across docs |
| `src/edictum/__init__.py` (API) | quickstart.md, all adapter pages |

If no library code changed (docs-only PR), skip to Step 4.

## Step 2: Read the changed code

For each changed file:
1. Read the file and the diff (`git diff main...HEAD -- <file>`)
2. Identify: new public APIs, changed signatures, new classes, removed exports, changed behavior

## Step 3: Update affected docs

For each affected page:
1. Read the current doc
2. Skip if already correct
3. Update code examples, descriptions, YAML examples
4. **Verify terminology** against .docs-style-guide.md:
   - "contracts" not "policies" or "rules"
   - "denied" not "blocked"
   - "enforces" not "governs"
   - "pipeline" not "engine"
   - "tool call" not "function call"
   - "adapter" not "integration" or "plugin"
   - "observe mode" not "shadow mode"
   - "finding" / "findings" not "alert"
5. **Verify tier boundaries** against CLAUDE.md:
   - FileAuditSink is core (not ee/)
   - StdoutAuditSink is core
   - Webhook/Splunk/Datadog sinks are ee/
   - PIIDetector protocol is core, implementations are ee/
   - MemoryBackend is the only StorageBackend (no Redis/DB)
   - No references to dropped features

## Step 4: Update README if needed

If public API, install extras, framework support, or version changed:
1. Read README.md
2. Update affected sections
3. Ensure README matches docs/index.md positioning

## Step 5: Verify the build

```bash
python -m mkdocs build --strict 2>&1
```

Fix any broken links, missing pages, or YAML errors.

## Step 6: Report

Summarize:
- Which code files changed
- Which doc pages were updated (and what changed)
- Which doc pages were checked but needed no changes
- Build verification result

## Rules

- **Don't rewrite for the sake of rewriting.** Only update what the code change actually affects.
- **Don't add features that don't exist.** If code was added but not released, note it as unreleased.
- **Don't reference dropped features.** No Redis/DB StorageBackend, no reset_session().
- **Preserve the voice.** Match existing style — problem first, short paragraphs, code examples.
- **Check cross-links.** Verify links in updated pages still work.
- **README and homepage must stay aligned.** If you update one, check the other.
