---
name: skill-downloader
description: Download and install Claude Code skills from various sources. Supports GitHub repositories, compressed archives (.zip, .tar.gz, .skill), and direct URLs. Use when user wants to download, install, or add a skill from GitHub, URL, or archive file. Triggers on "download skill", "install skill", "add skill from", "get skill".
---

# Skill Downloader

Download and install Claude Code skills from multiple sources.

## Supported Sources

| Source Type | Examples |
|-------------|----------|
| GitHub Repository | `https://github.com/user/repo`, `github.com/user/repo` |
| Compressed Archive | `.zip`, `.tar.gz`, `.tgz`, `.skill` (renamed zip) |
| Direct URL | URL pointing to archive or skill folder |

## Usage

### Download from GitHub

```bash
python scripts/download_from_github.py <repo-url> <skill-path> --output <target-dir>
```

**Examples:**
```bash
# Official Anthropic skills
python scripts/download_from_github.py https://github.com/anthropics/skills skills/docx --output ./.claude/skills/

# Community skills (root level)
python scripts/download_from_github.py https://github.com/gked2121/claude-skills social-repurposer --output ./.claude/skills/

# Nested skill path
python scripts/download_from_github.py https://github.com/MadAppGang/claude-code skills/content-brief --output ./.claude/skills/
```

### Download from Archive

```bash
python scripts/download_from_archive.py <url-or-path> --output <target-dir>
```

**Examples:**
```bash
# From URL
python scripts/download_from_archive.py https://example.com/skills/my-skill.zip --output ./.claude/skills/

# From local file
python scripts/download_from_archive.py ./downloads/my-skill.tar.gz --output ./.claude/skills/

# .skill files (renamed zip)
python scripts/download_from_archive.py https://skillhub.club/download/awesome-skill.skill --output ./.claude/skills/
```

### Unified Download Command

```bash
python scripts/download_skill.py <source> --output <target-dir>
```

Automatically detects source type:
- GitHub URL → Uses git sparse checkout
- Archive URL/path → Downloads and extracts
- Directory path → Copies directly

**Examples:**
```bash
# Auto-detect GitHub
python scripts/download_skill.py https://github.com/anthropics/skills/tree/main/skills/docx --output ./.claude/skills/

# Auto-detect archive
python scripts/download_skill.py https://example.com/my-skill.zip --output ./.claude/skills/
```

## Validation

All download methods validate:
1. Skill folder contains `SKILL.md`
2. `SKILL.md` has valid YAML frontmatter with `name` and `description`
3. No malicious content patterns detected

## Output Structure

Downloaded skills are placed in:
```
<output-dir>/
└── <skill-name>/
    ├── SKILL.md        # Required
    ├── scripts/        # Optional
    └── ...
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Skill already exists | Target directory exists | Use `--force` to overwrite |
| SKILL.md not found | Invalid skill package | Verify source contains SKILL.md |
| Invalid archive | Corrupted or unsupported format | Check file integrity |
| Network error | Download failed | Retry or check URL |

## Integration with Workflow Creator

When used with workflow-creator, download skills to workflow's `.claude/skills/` directory:

```bash
# Create workflow first
python /path/to/workflow-creator/scripts/create_workflow.py my-workflow --path ./workflows

# Then download skills
python scripts/download_skill.py https://github.com/anthropics/skills/tree/main/skills/docx --output ./workflows/my-workflow/.claude/skills/
```

## Skill Sources Reference

Popular skill repositories:
- [Anthropic Official](https://github.com/anthropics/skills) - docx, pdf, pptx
- [gked2121/claude-skills](https://github.com/gked2121/claude-skills) - social-repurposer, canvas-design
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) - Collection
- [MadAppGang/claude-code](https://github.com/MadAppGang/claude-code) - SEO, content skills
- [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills) - twitter-reader, fact-checker
- [skillhub.club](https://www.skillhub.club) - 1000+ skills collection
