---
name: converter
description: 'Cross-platform skill converter. Parse AgentOps skills into a universal bundle format, then convert to target platforms (Codex, Cursor). Triggers: convert, converter, convert skill, export skill, cross-platform.'
metadata:
  tier: cross-vendor
  dependencies: []
---

# /converter -- Cross-Platform Skill Converter

Parse AgentOps skills into a universal SkillBundle format, then convert to target agent platforms.

## Quick Start

```bash
/converter skills/council codex     # Convert council skill to Codex format
/converter skills/vibe cursor       # Convert vibe skill to Cursor format
/converter --all codex              # Convert all skills to Codex
```

## Pipeline

The converter runs a three-stage pipeline:

```
parse --> convert --> write
```

### Stage 1: Parse

Read the source skill directory and produce a SkillBundle:

- Extract YAML frontmatter from SKILL.md (between `---` markers)
- Collect the markdown body (everything after the closing `---`)
- Enumerate all files in `references/` and `scripts/`
- Assemble into a SkillBundle (see `references/skill-bundle-schema.md`)

### Stage 2: Convert

Transform the SkillBundle into the target platform's format:

| Target | Output Format | Status |
|--------|---------------|--------|
| `codex` | Codex SKILL.md + prompt.md | Implemented |
| `cursor` | Cursor .mdc rule + optional mcp.json | Implemented |

The Codex adapter produces a `SKILL.md` (body + inlined references + scripts as code blocks) and a `prompt.md` (Codex prompt referencing the skill). Descriptions are truncated to 1024 chars at a word boundary if needed.

The Cursor adapter produces a `<name>.mdc` rule file with YAML frontmatter (`description`, `globs`, `alwaysApply: false`) and body content. References are inlined into the body, scripts are included as code blocks. Output is budget-fitted to 100KB max -- references are omitted largest-first if the total exceeds the limit. If the skill references MCP servers, a `mcp.json` stub is also generated.

### Stage 3: Write

Write the converted output to disk.

- **Default output directory:** `.agents/converter/<target>/<skill-name>/`
- **Write semantics:** Clean-write. The target directory is deleted before writing. No merge with existing content.

## CLI Usage

```bash
# Convert a single skill
bash skills/converter/scripts/convert.sh <skill-dir> <target> [output-dir]

# Convert all skills
bash skills/converter/scripts/convert.sh --all <target> [output-dir]
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `skill-dir` | Yes (or `--all`) | Path to skill directory (e.g. `skills/council`) |
| `target` | Yes | Target platform: `codex`, `cursor`, or `test` |
| `output-dir` | No | Override output location. Default: `.agents/converter/<target>/<skill-name>/` |
| `--all` | No | Convert all skills in `skills/` directory |

## Supported Targets

- **codex** -- Convert to OpenAI Codex format (SKILL.md + prompt.md). Output: `<dir>/SKILL.md` and `<dir>/prompt.md`.
- **cursor** -- Convert to Cursor rules format (`.mdc` rule file + optional `mcp.json`). Output: `<dir>/<name>.mdc` and optionally `<dir>/mcp.json`.
- **test** -- Emit the raw SkillBundle as structured markdown. Useful for debugging the parse stage.

## Extending

To add a new target platform:

1. Add a conversion function to `scripts/convert.sh` (pattern: `convert_<target>`)
2. Update the target table above
3. Add reference docs to `references/` if the target format needs documentation

## Examples

### Converting a single skill to Codex format

**User says:** `/converter skills/council codex`

**What happens:**
1. The converter parses `skills/council/SKILL.md` frontmatter, markdown body, and any `references/` and `scripts/` files into a SkillBundle.
2. The Codex adapter transforms the bundle into a `SKILL.md` (body + inlined references + scripts as code blocks) and a `prompt.md` (Codex prompt referencing the skill).
3. Output is written to `.agents/converter/codex/council/`.

**Result:** A Codex-compatible skill package ready to use with OpenAI Codex CLI.

### Batch-converting all skills to Cursor rules

**User says:** `/converter --all cursor`

**What happens:**
1. The converter scans every directory under `skills/` and parses each into a SkillBundle.
2. The Cursor adapter transforms each bundle into a `.mdc` rule file with YAML frontmatter and body content, budget-fitted to 100KB max. Skills referencing MCP servers also get a `mcp.json` stub.
3. Each skill's output is written to `.agents/converter/cursor/<skill-name>/`.

**Result:** All skills are available as Cursor rules, ready to drop into a `.cursor/rules/` directory.

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `parse error: no frontmatter found` | SKILL.md is missing the `---` delimited YAML frontmatter block | Add frontmatter with at least `name:` and `description:` fields, or run `/heal-skill --fix` on the skill first |
| Cursor `.mdc` output is missing references | Total bundle size exceeded the 100KB budget limit | The converter omits references largest-first to fit the budget. Split large reference files or move non-essential content to external docs |
| Output directory already has old files | Previous conversion artifacts remain | This is expected -- the converter clean-writes by deleting the target directory before writing. If old files persist, manually delete `.agents/converter/<target>/<skill>/` |
| `--all` skips a skill directory | The directory has no `SKILL.md` file | Ensure each skill directory contains a valid `SKILL.md`. Run `/heal-skill` to detect empty directories |
| Codex `prompt.md` description is truncated | The skill description exceeds 1024 characters | This is by design. The converter truncates at a word boundary to fit Codex limits. Shorten the description in SKILL.md frontmatter if the truncation point is awkward |

## References

- `references/skill-bundle-schema.md` -- SkillBundle interchange format specification
