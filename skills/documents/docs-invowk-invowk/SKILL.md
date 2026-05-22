---
name: docs
description: Documentation workflow for website/ directory, Docusaurus, MDX snippets, i18n localization. Use when editing docs/, creating documentation pages, or updating WEBSITE_DOCS.md.
disable-model-invocation: false
---

# Docs and Website

This skill covers updating documentation and the Docusaurus website for Invowk.

Use this skill when working on:
- `website/` - Docusaurus documentation site
- `website/docs/` - Documentation pages
- `website/i18n/` - Internationalization
- Schema changes that require documentation updates

---

## Required Workflow

- Read `website/WEBSITE_DOCS.md` before any website edits.
- Use MDX + `<Snippet>` for all code/CLI/CUE blocks.
- Define snippets in `website/src/components/Snippet/snippets.ts` and reuse IDs across locales.
- Escape `${...}` inside snippets as `\${...}`.

---

## Documentation Sync Map

| Change | Update |
| --- | --- |
| `pkg/invkfile/invkfile_schema.cue` | `website/docs/reference/invkfile-schema.mdx` + affected docs/snippets |
| `pkg/invkmod/invkmod_schema.cue` | `website/docs/modules/` pages |
| `pkg/invkmod/operations*.go` | `website/docs/modules/` pages (validation, create, packaging, vendoring) |
| `internal/config/config_schema.cue` | `website/docs/reference/config-schema.mdx`, `website/docs/configuration/options.mdx` |
| `internal/runtime/container*.go` | `website/docs/runtime-modes/container.mdx` |
| `cmd/invowk/*.go` | `website/docs/reference/cli.mdx` + relevant feature docs |
| `cmd/invowk/module*.go` | `website/docs/modules/` pages + `website/docs/reference/cli.mdx` |
| `cmd/invowk/cmd_validate*.go` | `website/docs/dependencies/` pages |
| `cmd/invowk/tui_*.go` | `website/docs/tui/` pages + snippets |
| New features | Add/update docs under `website/docs/` and snippets as needed |

---

## Documentation Structure

```
website/docs/
|-- getting-started/     # Installation, quickstart, first invkfile
|-- core-concepts/       # Invkfile format, commands, implementations
|-- runtime-modes/       # Native, virtual, container execution
|-- dependencies/        # Tools, filepaths, capabilities, custom checks
|-- flags-and-arguments/ # CLI flags and positional arguments
|-- environment/         # Env files, env vars, precedence
|-- advanced/            # Interpreters, workdir, platform-specific
|-- modules/             # Module creation, validation, distribution
|-- tui/                 # TUI components reference
|-- configuration/       # Config file and options
`-- reference/           # CLI, invkfile schema, config schema
```

---

## Documentation Style Guide

- Use a friendly, approachable tone with occasional humor.
- Follow progressive disclosure: start simple, add complexity gradually.
- Include practical examples for each feature.
- Use admonitions for important callouts.
- Keep code examples concise and focused.

---

## Docs + i18n Checklist

- Always use `.mdx` (not `.md`) in `website/docs/` and translations.
- Treat `website/docs/` as the upcoming version; only touch versioned docs for backport fixes (see `website/WEBSITE_DOCS.md`).
- Update English first, then mirror the same `.mdx` path in `website/i18n/pt-BR/docusaurus-plugin-content-docs/current/`.
- Keep translations prose-only and reuse identical snippet IDs.
- Regenerate translation JSON when UI strings change: `cd website && npx docusaurus write-translations --locale pt-BR`.

---

## Documentation Testing

```bash
# Single locale development
cd website && npm start

# Brazilian Portuguese locale
cd website && npm start -- --locale pt-BR

# Full build (tests all locales)
cd website && npm run build

# Serve built site (for locale switching)
cd website && npm run serve
```

---

## Common Pitfalls

- **Missing i18n** - Website changes require updates to both `docs/` and `i18n/pt-BR/`.
- **Outdated documentation** - Check the Documentation Sync Map when modifying schemas or CLI.
