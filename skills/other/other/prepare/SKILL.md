---
name: prepare
description: Prepare a release by committing, versioning, updating docs and skills
---

# Prepare Release

1. **Commit** current changes

2. **Version** edited packages. Patch any edited subpackages without version changes. If a `jaypie` dependency is versioned, bump `jaypie` too. If `@jaypie/mcp` skills or release-notes change, patch `@jaypie/mcp`.

3. **Documentation and Skills** -- update anything impacted:
   - README.md (top-level)
   - CLAUDE.md (top- and package-level)
   - `packages/mcp/skills/`
   - `packages/mcp/release-notes/` for version bumps
   - `workspaces/documentation/docs/`

4. **Request to Shepherd** -- if approved, follow `/shepherd`
