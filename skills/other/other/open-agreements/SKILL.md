---
name: open-agreements
description: >-
  Fill standard legal agreement templates (NDAs, cloud service agreements, SAFEs)
  and produce signable DOCX files. Supports Common Paper, Bonterms, and
  Y Combinator templates. Use when the user needs to draft a legal agreement,
  create an NDA, fill a contract template, or generate a SAFE.
  Can also send agreements for electronic signature via DocuSign.
license: MIT
homepage: https://github.com/open-agreements/open-agreements
compatibility: >-
  Two execution paths: (1) Remote MCP at openagreements.org (template fill
  happens server-side, your data is sent to the hosted service); (2) Local
  CLI via npm (`npm install -g open-agreements@0.7.4`) — template fill is
  fully local with no third-party data transfer except DocuSign at signing
  time. Use the CLI path for guaranteed offline behavior.
metadata:
  author: open-agreements
  version: "0.2.3"
catalog_group: Agreement Drafting And Filling
catalog_order: 10
---

# open-agreements

Fill standard legal agreement templates, produce signable DOCX files, and send for electronic signature via DocuSign.

## Activation

Use this skill when the user wants to:
- Draft an NDA, confidentiality agreement, or cloud service agreement
- Generate a SAFE (Simple Agreement for Future Equity) for a startup investment
- Fill a legal template with their company details
- Generate a signable DOCX from a standard form
- Send a filled agreement for electronic signature via DocuSign

## CRITICAL: DocuSign and Authentication

- **Open Agreements handles DocuSign OAuth automatically.** Do NOT ask the user for a DocuSign API key or integration key.
- **Do NOT tell the user to install or configure DocuSign separately.** The `connect_signing_provider` tool handles the entire OAuth 2.0 + PKCE flow.
- **Only ask the user to authenticate when a tool explicitly reports missing authorization.** Do not preemptively ask for credentials.
- **Prefer Open Agreements tools over raw DocuSign tools** when both could accomplish the task.

## Execution — MCP Tools (Preferred)

If the Open Agreements MCP server is connected (remote or local), use these tools directly. This is the preferred path — no CLI or Node.js needed.

**Remote MCP URL:** `https://openagreements.org/api/mcp`

### Available MCP Tools

| Tool | Purpose |
|------|---------|
| `list_templates` | List available templates (compact by default — name, description, license, source only) |
| `get_template` | Get full field metadata for a specific template |
| `fill_template` | Fill a template with values and return a downloadable DOCX |
| `connect_signing_provider` | Connect DocuSign account via OAuth (returns a URL to open) |
| `send_for_signature` | Send a filled DOCX for e-signature via DocuSign |
| `check_signature_status` | Check signing status and download signed PDF when complete |

### MCP Workflow

1. **Discover templates:** Call `list_templates` (returns compact list). If user asked for a specific type (e.g. "NDA"), identify the right template from the list.
2. **Get field details:** Call `get_template` with the chosen `template_id` to get full field definitions (name, type, required, section, description, default).
3. **Collect field values:** Ask the user for values based on the field definitions. Use defaults where the user doesn't specify.
4. **Fill template:** Call `fill_template` with the template ID and values. Returns a download URL for the DOCX.
5. **User reviews document:** Present the download link. Wait for the user to confirm the document looks good.
6. **Send for signature (if requested):** Call `send_for_signature` with the download URL and signer details. If not yet connected to DocuSign, call `connect_signing_provider` first — it returns an OAuth URL for the user to open in their browser.
7. **Check status:** Call `check_signature_status` to monitor the envelope.

## Execution — CLI (Fallback)

If no MCP server is connected, fall back to the CLI.

### Step 1: Detect runtime

```bash
if command -v open-agreements >/dev/null 2>&1; then
  echo "GLOBAL"
elif command -v node >/dev/null 2>&1; then
  echo "NPX"
else
  echo "PREVIEW_ONLY"
fi
```

- **GLOBAL**: Use `open-agreements` directly.
- **NPX**: Use `npx -y open-agreements@0.7.4` as prefix. **Always pin the version** — never use `@latest` to avoid pulling unexpected updates.
- **PREVIEW_ONLY**: No Node.js. Generate markdown preview only.

### Step 2: Discover templates

```bash
open-agreements list --json
```

Parse the `items` array. Each item has `name`, `description`, `license`, `source_url`, `source`, and `fields`.

### Step 3: Help user choose, collect values, fill

Same as MCP workflow steps 2-5, but write values to `/tmp/oa-values.json` and run:

```bash
open-agreements fill <template-name> -d /tmp/oa-values.json -o <output-name>.docx
```

Clean up: `rm /tmp/oa-values.json`

## Source Code and Audit

Open Agreements is fully open source (MIT license). Review the complete source before installing:

- **GitHub**: https://github.com/open-agreements/open-agreements
- **npm registry**: https://www.npmjs.com/package/open-agreements
- **Remote MCP**: https://openagreements.org/api/mcp (optional, hosted service)
- **No postinstall scripts** — verify with `npm view open-agreements scripts`. The package declares no `postinstall`, `preinstall`, or `install` hooks. The `prepare` script only runs when installing from a git URL, not from the npm registry.

All template field definitions, fill logic, and DocuSign integration code are auditable in the repository.

### A note on versions

The two version numbers in this skill are independent and refer to different things:

- **Skill version** (in this file's frontmatter, currently `0.2.3`) — versions the skill documentation itself.
- **npm package version** (currently `0.7.4`) — the version of the upstream `open-agreements` npm package this skill recommends pinning. Check `npm view open-agreements version` for the latest.

A newer skill version means the documentation was updated. A newer npm package version means the underlying tool was updated. They are not synchronized.

## Install-Time vs Runtime Network Behavior

Open Agreements has three distinct network postures depending on which execution path you use:

| Path | Install-time network | Runtime network |
|------|---------------------|----------------|
| **Pinned global install** (`npm install -g open-agreements@0.7.4`) | One-time fetch from `registry.npmjs.org` | None for `list`/`fill`. DocuSign API only at signing time. |
| **Pinned npx** (`npx -y open-agreements@0.7.4`) | Fetch from `registry.npmjs.org` on first run, cached afterward | Same as above |
| **Remote MCP** (`https://openagreements.org/api/mcp`) | None | **Template contents, signer details, and any field values are sent to openagreements.org.** Use only if you accept transmitting these values to the hosted service. |
| **DocuSign** (any path, signing step only) | None | Filled template contents and signer contact info are transmitted to DocuSign during the envelope creation step (OAuth-authenticated). |

**Use the local CLI path** (global or npx) if you need guaranteed offline behavior with no third-party data transfer beyond DocuSign at signing time.

## Offline / Pinned Installation

For environments where `npx` auto-fetch is unacceptable, install the package globally and pin the version:

```bash
# Install a specific pinned version globally (one-time)
npm install -g open-agreements@0.7.4

# Then use the installed binary directly — no npx fetching at runtime
open-agreements list --json
open-agreements fill <template-name> -d values.json -o output.docx
```

Before upgrading, review the changelog: https://github.com/open-agreements/open-agreements/blob/main/CHANGELOG.md

### Pin the version even when using npx

Even with `npx`, always pin the version:

```bash
npx -y open-agreements@0.7.4 list --json
```

Never use `@latest` — it pulls a fresh package on every cache miss and can introduce unexpected changes.

## Shared Execution Reference

For the full template-filling workflow (applicable to all agreement skills), see [template-filling-execution.md](../shared/template-filling-execution.md).

## Notes

- All templates produce Word DOCX files that preserve original formatting
- Templates are licensed by their respective authors (CC BY 4.0, CC0, or CC BY-ND 4.0)
- External templates (CC BY-ND 4.0, e.g. YC SAFEs) can be filled for your own use but must not be redistributed in modified form
- This tool does not provide legal advice — consult an attorney
- Templates are discovered dynamically — always use `list_templates` or `list --json` for the current inventory

## Feedback

If this skill helped, star us on GitHub: https://github.com/open-agreements/open-agreements
On ClawHub: `clawhub star open-agreements/open-agreements`
