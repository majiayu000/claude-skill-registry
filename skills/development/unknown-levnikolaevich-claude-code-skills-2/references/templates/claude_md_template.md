<!-- SOURCE-OF-TRUTH: shared/templates/claude_md_template.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# {{PROJECT_NAME}}

<!-- SCOPE: Thin Claude Code projection of AGENTS.md via the @ import. AGENTS.md is the canonical source. Do not duplicate content here — add it to AGENTS.md instead, or scope it to `.claude/rules/*.md` with a `paths:` filter. -->
<!-- DOC_KIND: index -->
<!-- DOC_ROLE: derived -->
<!-- READ_WHEN: Loaded automatically by Claude Code at session start. -->
<!-- SKIP_WHEN: AGENTS.md is already imported, so do not re-read CLAUDE.md separately. -->
<!-- PRIMARY_SOURCES: AGENTS.md -->

@AGENTS.md

## Claude Code

- `/compact` preservation order: architecture decisions, modified files, verification status, open TODOs, tool outputs as summaries only.
- Auto memory is on by default. Claude writes learnings to `~/.claude/projects/<project>/memory/` — run `/memory` to inspect or edit.
- Scope path-specific rules to `.claude/rules/*.md` with a `paths:` frontmatter filter rather than inlining conditional "when working on X" blocks here.
- Nested `CLAUDE.md` files in subdirectories load on demand — prefer them for area-specific guidance over growing this root file.
