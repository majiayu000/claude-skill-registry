---
name: webapp-testing
description: Testes E2E com Playwright
---

Utiliza o MCP `playwright` configurado em `.mcp.json`.

## Iniciar Browser
```
mcp__playwright__browser_navigate url="http://localhost:5173"
```

## Acoes Comuns

### Navegar
```
mcp__playwright__browser_navigate url="http://localhost:5173/beneficios"
```

### Clicar em Elemento
```
mcp__playwright__browser_click selector="button[data-testid='enviar']"
mcp__playwright__browser_click selector=".chat-input button"
```

### Digitar Texto
```
mcp__playwright__browser_type selector="input[name='cpf']" text="12345678901"
mcp__playwright__browser_type selector=".chat-input textarea" text="quero consultar meus beneficios"
```

### Capturar Screenshot
```
mcp__playwright__browser_screenshot
```

### Ler Conteudo da Pagina
```
mcp__playwright__browser_snapshot
```

## Fluxos de Teste

### 1. Testar Chat do Agente
```
# Navegar para home
mcp__playwright__browser_navigate url="http://localhost:5173"

# Digitar mensagem
mcp__playwright__browser_type selector=".chat-input textarea" text="quais beneficios tenho direito?"

# Enviar
mcp__playwright__browser_click selector="button[type='submit']"

# Aguardar resposta (snapshot para verificar)
mcp__playwright__browser_snapshot
```

### 2. Testar Consulta de Beneficios
```
# Navegar para pagina de beneficios
mcp__playwright__browser_navigate url="http://localhost:5173/beneficios"

# Preencher CPF
mcp__playwright__browser_type selector="input[name='cpf']" text="12345678901"

# Consultar
mcp__playwright__browser_click selector="button[data-testid='consultar']"

# Screenshot do resultado
mcp__playwright__browser_screenshot
```

### 3. Testar Admin Dashboard
```
mcp__playwright__browser_navigate url="http://localhost:5173/admin"
mcp__playwright__browser_snapshot
```

## Debug de Testes
```
# Ver estado atual da pagina
mcp__playwright__browser_snapshot

# Screenshot para analise visual
mcp__playwright__browser_screenshot

# Console do browser
mcp__playwright__browser_console
```

## Seletores Uteis

| Elemento | Seletor |
|----------|---------|
| Input CPF | `input[name='cpf']` |
| Botao Enviar | `button[type='submit']` |
| Chat Input | `.chat-input textarea` |
| Mensagem | `.chat-message` |
| Card Beneficio | `.beneficio-card` |

## Pre-requisitos
- Frontend rodando: `cd frontend && npm run dev`
- Backend rodando: `cd backend && uvicorn app.main:app --reload`
