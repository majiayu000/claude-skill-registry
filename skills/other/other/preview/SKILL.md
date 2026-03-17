---
description: "Ver preview visual del proyecto. Toma screenshots, inicia dev server, muestra cambios en tiempo real."
user-invocable: true
argument-hint: "[url] [--port 3000] [--mobile]"
allowed-tools:
  - Bash
  - Read
  - WebFetch
  - mcp__playwright__*
  - mcp__puppeteer__*
---

# Preview Skill

Permite ver visualmente el proyecto mientras desarrollas.

## Flujo de Trabajo

### 1. Verificar Dev Server

```bash
# Verificar si ya hay un servidor corriendo
lsof -i :3000 2>/dev/null || echo "No server running"

# Si no hay servidor, iniciarlo en background
pnpm dev --port 3000 &
# o
npm run dev -- --port 3000 &
# o
bun dev --port 3000 &
```

### 2. Esperar a que el servidor esté listo

```bash
# Esperar hasta 30 segundos
for i in {1..30}; do
  curl -s http://localhost:3000 > /dev/null && break
  sleep 1
done
```

### 3. Tomar Screenshot con Playwright

Usar el MCP de Playwright para:

1. Navegar a `http://localhost:3000` (o la URL especificada)
2. Esperar a que la página cargue completamente
3. Tomar screenshot
4. Mostrar la imagen al usuario

### 4. Opciones de Viewport

| Opción | Viewport | Uso |
|--------|----------|-----|
| desktop | 1920x1080 | Default |
| tablet | 768x1024 | iPad |
| mobile | 375x812 | iPhone |

### 5. Páginas Comunes a Revisar

```
/              # Home
/login         # Auth
/dashboard     # Main app
/api/health    # API status
```

## Uso

```bash
# Preview de home
/preview

# Preview de página específica
/preview /dashboard

# Preview mobile
/preview --mobile

# Preview en puerto diferente
/preview --port 3001

# Preview de URL externa
/preview https://staging.myapp.com
```

## Output

Después de tomar el screenshot:
1. Mostrar la imagen directamente (Claude puede ver imágenes)
2. Describir lo que se ve
3. Identificar posibles problemas visuales
4. Sugerir mejoras de UI/UX

## Automatización

Para desarrollo continuo:
```bash
# Watch mode - tomar screenshot cada vez que hay cambios
fswatch -o src/ | while read; do
  # Trigger screenshot
  curl -s http://localhost:3000 > /dev/null && echo "Ready for screenshot"
done
```
