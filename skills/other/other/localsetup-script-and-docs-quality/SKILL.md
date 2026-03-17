---
name: localsetup-script-and-docs-quality
description: "Markdown/encoding standards, script generation quality, file creation discipline, documentation discipline. Use when generating scripts, creating/editing markdown or docs."
metadata:
  version: "1.1"
---

# Script and docs quality

## 15. Markdown compatibility (CRITICAL)

- **ASCII-first:** No Unicode emoji, box-drawing, or arrow symbols in markdown. Use [OK], [FAIL], [WARNING], [YES], [NO]; use -> not arrow; use * or - for bullets.
- **No EM dash:** Do not use the EM dash character (—, U+2014) in any user-facing text. Use a space and hyphen ( - ) or a plain hyphen instead.
- **Encoding:** UTF-8; prefer pure ASCII. Verify in markdown preview before committing.

## 16. Script generation quality (all languages)

- **Comments:** Header with purpose, usage, parameters; document each function; descriptive names.
- **Error handling:** Try-catch (or equivalent); validate inputs; check prerequisites; no silent failures.
- **STDOUT:** All scripts output to console; pipeable; STDOUT for normal, STDERR for errors.
- **Structure:** Break into functions; clear error messages with source/trace; actionable guidance.
- **Bash:** set -euo pipefail, trap for cleanup. **Python:** type hints, docstrings, context managers. **PowerShell:** try/catch/finally, Write-* cmdlets.

## 17. External input hardening (mandatory)

- Treat every external input as hostile: CLI arguments, filesystem content, network payloads, copied text, imported archives.
- Sanitize untrusted strings before parsing and before printing: strip control characters, normalize whitespace, enforce max length.
- Validate type, schema, and allowed ranges before use; reject invalid values with clear error text.
- Exception handling must be explicit and actionable: print source, exception type, and message to STDERR; return non-zero exit when task cannot continue.
- Never swallow errors (`except: pass`, silent `|| true` on critical operations). Partial-failure mode is allowed only when warnings are emitted and processing decisions are explicit.

## 7. File creation discipline

- Before creating any file: verify it belongs; minimal approach; "Is this essential?" Consolidate rather than duplicate.

## 2. Documentation discipline

- **_localsetup/docs/ is ONLY for framework documentation.** Not for IDE setup or external tool guides. All docs must have status (ACTIVE/PROPOSAL/DRAFT/DEPRECATED/ARCHIVED). Check status before assuming a feature is implemented. See [DOCUMENT_LIFECYCLE_MANAGEMENT.md](../../docs/DOCUMENT_LIFECYCLE_MANAGEMENT.md).
- **Platform default for any generated docs/output:** Use rich markdown (code blocks, lists, typography, links for in-repo refs, glyphs where they help), humanized prose. See [OUTPUT_AND_DOC_GENERATION.md](../../docs/OUTPUT_AND_DOC_GENERATION.md).
