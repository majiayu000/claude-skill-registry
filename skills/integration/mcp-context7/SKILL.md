---
name: mcp-context7
description: Integración con Context7 MCP Server para obtener documentación actualizada de librerías.
trigger: context7 OR doc OR documentation OR library OR api
scope: global
---

# Context7 MCP Skill

## Description

Context7 provee documentación en tiempo real para 20,000+ librerías, evitando alucinaciones de la IA sobre versiones viejas.

## Setup de IDE (Cursor/Windsurf)

Para que el modelo (y nosotros) pueda usar Context7, configura tu cliente MCP:

### 1. Obtener API Key

Recomendado: Obtén una key gratis en [Context7 Dashboard](https://context7.com/dashboard).

### 2. Configuración (Local)

Agrega esto a tu `~/.cursor/mcp.json` o `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp", "--api-key", "TU_API_KEY_AQUI"]
    }
  }
}
```

## Uso

Simplemente invoca "use context7" en tu prompt desde el IDE.

### Ejemplos

- "Cómo configuro el middleware de Next.js 15? use context7"
- "Dame el código para subir archivos a Supabase Storage v2. use context7"

## Uso en Antigravity (CLI)

Si prefieres usar la terminal o estás en Antigravity:

1.  Asegúrate de tener `CONTEXT7_API_KEY` en tu `.env`.
2.  Ejecuta el script:

```bash
# Sintaxis: python scripts/ask_context7.py [libreria] [pregunta]
python scripts/ask_context7.py nextjs "how to use server actions"
python scripts/ask_context7.py google-genai "multimodal prompt example"
```
