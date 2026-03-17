---
name: managing-chezmoi
description: Manage dotfiles with chezmoi. Use when adding files to chezmoi, running chezmoi add/apply/diff/status, debugging why changes aren't appearing, working with chezmoi templates or .chezmoiignore, understanding source vs target files, resolving merge conflicts, or asking "how do I manage this file with chezmoi". For chezmoi command uncertainties, use Context7 to fetch latest docs.
---

# Chezmoi Management

Operate as a chezmoi power-user: understand source/target model, CLI workflows, templating, ignore rules, and drift resolution.

## Quick Reference

**Commands & workflows:** See [commands-and-workflows.md](references/commands-and-workflows.md)
**Troubleshooting:** See [troubleshooting.md](references/troubleshooting.md)

## Default Workflow

1. **Inspect state**: `chezmoi status` and `chezmoi diff`
2. **Edit source directly**: modify files in this repo (the source state)
3. **Apply safely**: `chezmoi apply --dry-run -v`, then `chezmoi apply`
4. **Verify**: `chezmoi verify` after larger refactors

## Complexity Decision Tree

| Situation | Action |
|-----------|--------|
| Simple file change | Edit source → `chezmoi apply <target>` |
| New file to manage | `chezmoi add <target>` → `chezmoi apply` |
| Unexpected diffs | `chezmoi diff -v` → `chezmoi verify` → troubleshoot |
| Conditional behavior | Check templates + `chezmoi data` |
| Command uncertainty | Fetch docs via Context7 |

## Chezmoi Expertise Checklist

When helping with a request, consider:

- **Source vs target**: User might be editing the wrong side
- **Source file naming**: `dot_` prefixes, `private_` files, `.tmpl` suffix
- **Ignore rules**: `.chezmoiignore` patterns and conditionals
- **Templates**: `{{ ... }}` logic, `chezmoi data`
- **Safe operations**: Prefer dry-runs and diffs before applying

## Context7 Usage

When uncertain about chezmoi commands/flags or version-specific behavior:

1. Call `resolve-library-id` with `libraryName="chezmoi"`
2. Call `query-docs` with a targeted question
3. Prefer newest documented behavior
