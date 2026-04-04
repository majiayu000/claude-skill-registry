---
name: resource-scout
description: Search and discover Claude Code skills and MCP servers from marketplaces, GitHub repositories, and registries. Use when (1) user asks to find skills for a specific task, (2) looking for MCP servers to connect external tools, (3) user mentions "find skill", "search MCP", "discover tools", or "what skills exist for X", (4) before creating a custom skill to check if one already exists.
---

# Resource Scout

Search and discover existing Claude Code skills and MCP servers before building custom solutions.

## Quick Search Strategy

**For Skills:**
1. WebSearch: `site:skillsmp.com [topic]` or `claude skill [topic]`
2. Check GitHub: `awesome-claude-skills [topic]`
3. Browse: skillhub.club, claudeskills.info

**For MCP:**
1. WebSearch: `MCP server [tool/service name]`
2. Check: glama.ai/mcp/servers, mcpmarket.com
3. Official: github.com/modelcontextprotocol/servers

## Skill Search Workflow

### Step 1: Define Need

Before searching, clarify:
- What task needs to be accomplished?
- What tools/services are involved?
- Is it a common pattern (git, testing, API) or domain-specific?

### Step 2: Search Marketplaces

**Primary sources (largest catalogs):**

| Source | URL | Best For |
|--------|-----|----------|
| SkillsMP | skillsmp.com | 71000+ skills, long-tail search |
| SkillHub.club | skillhub.club | AI-evaluated, quality filter |
| Claude Skills Hub | claudeskills.info | UI-friendly browsing |

**Search patterns:**
```
# On SkillsMP
[domain] skill          → "marketing skill", "database skill"
[framework] claude      → "react claude", "fastapi claude"
[task] automation       → "deployment automation"
```

### Step 3: Search GitHub

**Curated lists:**
- `github.com/keyuyuan/skillhub-awesome-skills` - 精选清单
- `github.com/VoltAgent/awesome-claude-skills` - 生态大全
- `github.com/ComposioHQ/awesome-claude-skills` - 大量通用技能

**Ready-to-use repositories:**
- `github.com/alirezarezvani/claude-skills` - Content/Marketing
- `github.com/gked2121/claude-skills` - Workflow思维
- `github.com/Microck/ordinary-claude-skills` - 超大集合
- `github.com/sickn33/antigravity-awesome-skills` - 结构化

**Search command:**
```bash
# Use WebSearch tool
site:github.com "claude skill" [topic]
site:github.com "SKILL.md" [topic]
```

### Step 4: Evaluate & Install

When skill found:
1. Check last update date (prefer recent)
2. Review SKILL.md for quality
3. Check if has scripts/references
4. Install with skill-downloader or manual copy

## MCP Server Search Workflow

### Step 1: Identify Integration Need

Common patterns:
- Database access → postgres, mysql, sqlite MCP
- GitHub workflow → github MCP
- Cloud services → AWS, GCP, Azure MCPs
- Communication → slack, discord MCPs
- File systems → filesystem MCP

### Step 2: Search Official Sources

**Primary:**
- Official registry: `registry.modelcontextprotocol.io`
- Official repo: `github.com/modelcontextprotocol/servers`

**Directories:**
| Source | URL | Features |
|--------|-----|----------|
| Glama | glama.ai/mcp/servers | Stars, downloads, updates |
| MCP Market | mcpmarket.com | Skills + MCP combined |
| mcpservers.org | mcpservers.org | Categorized |
| PulseMCP | pulsemcp.com/servers | Daily updates |
| Smithery | smithery.ai | Registry/distribution |

### Step 3: Search GitHub

```bash
# Use WebSearch tool
site:github.com "mcp server" [service]
site:github.com "@modelcontextprotocol" [service]
```

**Awesome lists:**
- `github.com/punkpeye/awesome-mcp-servers`
- `github.com/wong2/awesome-mcp-servers`

### Step 4: Verify & Configure

When MCP found:
1. Check compatibility (stdio vs HTTP)
2. Review required environment variables
3. Test connection locally
4. Add to `.claude/settings.json`

## Search by Category

### Development Tools
```
Skills: "code review skill", "git commit skill", "testing skill"
MCP: "github mcp", "gitlab mcp", "jira mcp"
```

### Databases
```
Skills: "database skill", "sql skill", "migration skill"
MCP: "postgres mcp", "mysql mcp", "mongodb mcp"
```

### Content & Marketing
```
Skills: "content creator skill", "seo skill", "social media skill"
MCP: "wordpress mcp", "notion mcp"
```

### Cloud & DevOps
```
Skills: "deployment skill", "kubernetes skill", "terraform skill"
MCP: "aws mcp", "gcp mcp", "azure mcp"
```

### AI & Data
```
Skills: "data analysis skill", "ml skill"
MCP: "openai mcp", "huggingface mcp"
```

## Complete Source Reference

See [references/sources.md](references/sources.md) for full directory of all skill and MCP sources with detailed descriptions.

## Best Practices

1. **Search before build** - Always check existing resources first
2. **Prefer maintained** - Choose skills with recent updates
3. **Check quality** - Review SKILL.md structure and content
4. **Consider combining** - Multiple simple skills > one complex custom
5. **Verify security** - Review MCP permissions and token scopes
