---
name: wordpress-mcp-dev
description: Build and maintain modern WordPress plugins and MCP servers, including hybrid WordPress+MCP products. Use when implementing plugin architecture (PHP, REST API, Gutenberg/admin/page-builder integrations), MCP tooling (TypeScript/Python, stdio/HTTP transport), security hardening, licensing/updates, and delivery workflows from scaffold to distribution.
---

# WordPress + MCP Development

Use this skill to ship production-grade WordPress plugins, MCP servers, or both together.

## Workflow

1. Identify target product shape: `plugin`, `mcp-server`, or `hybrid`.
2. Choose architecture and scaffold from the relevant reference.
3. Implement minimum viable vertical slice first:
   - Plugin: one secure REST route + one real feature path.
   - MCP: one read-only tool + one mutating tool with safe validation.
   - Hybrid: one plugin endpoint consumed by one MCP tool.
4. Add safety controls before expanding scope: capability checks, nonce/auth, sanitized errors, and rollback strategy.
5. Validate against checklists before release.

## Guardrails

- Keep plugin bootstrap thin; place behavior in namespaced classes.
- Prefix all plugin symbols to avoid collisions.
- Treat MCP tool schemas/descriptions as API contracts for model behavior.
- Return actionable errors and avoid leaking secrets.
- Prefer duplicate-first content edits for AI-assisted write operations.

## References

- Core guide: `references/full-guide.md`
- WordPress plugin architecture and security sections: `references/full-guide.md`
- MCP server design, transport, and tooling sections: `references/full-guide.md`
- Lifecycle, testing, and distribution checklists: `references/full-guide.md`
