---
name: mcp-registry
description: MCP server registry, auto-discovery, configuration, custom server development guide
---

# MCP Registry & Auto-Discovery

## MCP Nedir?

Model Context Protocol (MCP) - Claude'un dis sistemlerle (DB, API, browser, dosya sistemi) iletisim kurmasini saglayan standart protokol.

## Kurulu MCP Server'lar

Kontrol: `~/.mcp.json` dosyasini oku.

```bash
# Mevcut durumu gor
cd ~/.claude && python3 scripts/mcp/registry.py status
```

## Proje Icin MCP Onerisi

```bash
# Proje dizinindeki dosyalara gore oneri al
cd ~/.claude && python3 scripts/mcp/registry.py recommend /path/to/project

# Tum registry'yi gor
cd ~/.claude && python3 scripts/mcp/registry.py list
```

## Bilinen MCP Server'lar

### Resmi (Anthropic / MCP)

| Server | Kullanim | Sinyal Dosyalari |
|--------|---------|-----------------|
| github | GitHub API (repo, issue, PR) | .github/, .git/ |
| filesystem | Dosya sistemi erisimi | * |
| postgres | PostgreSQL DB | schema.prisma, *.sql, migrations/ |
| sqlite | SQLite DB | *.db, *.sqlite |
| docker | Docker yonetimi | Dockerfile, docker-compose.yml |
| puppeteer | Browser otomasyon | playwright.config.*, cypress.config.* |
| brave-search | Web arama | - |
| chrome-devtools | Browser debug | next.config.*, vite.config.* |
| kubernetes | K8s cluster | k8s/, kustomization.yaml |

### 3rd Party (Kurulu)

| Server | Kullanim | Durum |
|--------|---------|-------|
| browser-use | AI browser otomasyon | ~/.mcp.json'da |
| codebase-memory | Codebase indexing (64 dil) | ~/bin/codebase-memory-mcp |
| notion | Notion workspace | ~/.mcp.json'da |
| crawl4ai | Web crawling | pip, crwl CLI |

## ~/.mcp.json Konfigurasyonu

```json
{
  "mcpServers": {
    "server-adi": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-X"],
      "env": {
        "API_KEY": "..."
      }
    }
  }
}
```

### Ornek: GitHub MCP Ekleme

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxxx"
      }
    }
  }
}
```

### Ornek: PostgreSQL MCP

```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost:5432/db"]
    }
  }
}
```

## Ozel MCP Server Yazma

### Minimal Python MCP Server

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool aciklamasi"""
    return f"Sonuc: {param}"

@mcp.resource("resource://my-data")
def my_resource() -> str:
    """Resource aciklamasi"""
    return "data"

if __name__ == "__main__":
    mcp.run()
```

### Minimal TypeScript MCP Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "my-server", version: "1.0.0" }, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "my_tool",
    description: "Tool aciklamasi",
    inputSchema: { type: "object", properties: { param: { type: "string" } } }
  }]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => ({
  content: [{ type: "text", text: `Sonuc: ${request.params.arguments?.param}` }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

### mcp.json'a Ekleme

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python3",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## MCP Debug & Troubleshooting

### Server Baslatma Testi

```bash
# Server'in calistigini dogrula
echo '{"jsonrpc":"2.0","method":"initialize","params":{"capabilities":{}},"id":1}' | npx -y @modelcontextprotocol/server-github 2>/dev/null
```

### Yaygin Sorunlar

| Sorun | Cozum |
|-------|-------|
| "spawn ENOENT" | command path'i kontrol et, npx/python3 PATH'te mi? |
| "Connection refused" | Server'i manual calistir, hata mesajini oku |
| Tool gorunmuyor | Claude Code'u restart et (MCP session basinda yuklenir) |
| Timeout | args'a timeout flag ekle, veya network kontrol et |
| Auth hatasi | env degiskenlerini kontrol et (.env degil, mcp.json'a yaz) |
| Python version uyumsuzluk | Python 3.10+ gerekli, `python3 --version` kontrol et |
| pip kurulum hatasi | `pip3 install --user --break-system-packages <paket>` |

### Loglar

```bash
# Claude Code MCP loglarini gor
ls ~/.claude/logs/mcp*.log 2>/dev/null

# Server'i verbose modda calistir
DEBUG=* npx -y @modelcontextprotocol/server-github 2>&1 | head -50
```

## Auto-Discovery Hook

`mcp-discovery.ts` hook'u session basinda otomatik calisir:
- Proje dizinindeki dosyalari tarar
- Kurulu olmayan ama faydali MCP server'lari tespit eder
- systemMessage ile oneri gosterir
- Session basina 1 kez calisir

## Registry Script

```bash
cd ~/.claude && python3 scripts/mcp/registry.py recommend .  # Oneri
cd ~/.claude && python3 scripts/mcp/registry.py status       # Kurulu
cd ~/.claude && python3 scripts/mcp/registry.py list         # Tumu
```
