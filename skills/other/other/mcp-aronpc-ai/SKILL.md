---
name: mcp
description: >-
  Valida funcionalidades usando MCP tools (Browser, API, Database). Use quando precisar validar implementações com ferramentas MCP, testar via browser, ou verificar integrações de API.
compatibility: MCP tools
metadata:
  author: aronpc
  version: 1.0.0
  category: devops
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# mcp

## Resumo
Valida aplicações usando MCP tools para browser automation, API e database testing.

## Skills Relacionadas

| Skill | Quando usar junto |
|-------|-------------------|
| `qa` | Para validação completa de qualidade |
| `ui-ux` | Para validação visual de melhorias |
| `coder` | Para validar implementações |
| `pr-review` | Para evidências visuais em reviews |

## Quando usar

Use esta skill quando precisar:
- Validar aplicações Electron
- Testar UI web com browser automation
- Verificar APIs
- Validar database migrations

**Não use para:**
- QA de código (use qa-validation)
- Code review (use github-pr-review)

---

## Electron App Validation

### Pré-requisitos
- `ELECTRON_MCP_ENABLED=true`
- App rodando com `--remote-debugging-port=9222`

### Ferramentas Disponíveis

| Ferramenta | Propósito |
|------------|-----------|
| `mcp__electron__get_electron_window_info` | Informações da janela |
| `mcp__electron__take_screenshot` | Capturar screenshot |
| `mcp__electron__send_command_to_electron` | Click, fill, eval JS |
| `mcp__electron__read_electron_logs` | Logs do console |

### Fluxo de Validação

1. Conectar à app
2. Capturar screenshot
3. Analisar estrutura da página
4. Verificar elementos de UI
5. Verificar logs do console

---

## Web Browser Validation

### Ferramentas Disponíveis (Puppeteer)

| Ferramenta | Propósito |
|------------|-----------|
| `mcp__puppeteer__puppeteer_navigate` | Navegar para URL |
| `mcp__puppeteer__puppeteer_screenshot` | Capturar screenshot |
| `mcp__puppeteer__puppeteer_click` | Clicar em elemento |
| `mcp__puppeteer__puppeteer_fill` | Preencher input |
| `mcp__puppeteer__puppeteer_evaluate` | Executar JS |

### Fluxo de Validação

1. Navegar para página
2. Capturar screenshot
3. Verificar elementos existentes
4. Testar interações
5. Verificar console por erros

---

## API Validation

### Passos

1. Verificar endpoints existentes
2. Testar respostas dos endpoints
3. Verificar tratamento de erros
4. Verificar formato de resposta

### Exemplo

```bash
# Test endpoint
curl -X GET http://localhost:8000/api/resource | jq .

# Test with auth
curl -X GET http://localhost:8000/api/protected \
  -H "Authorization: Bearer $TOKEN"
```

---

## Database Validation

### Passos

1. Verificar migrations existentes
2. Verificar aplicação de migrations
3. Verificar schema com models
4. Verificar integridade dos dados

### Comandos por Framework

| Framework | Command |
|-----------|---------|
| Django | `python manage.py showmigrations` |
| Prisma | `npx prisma migrate status` |
| Laravel | `php artisan migrate:status` |
| Rails | `rails db:migrate:status` |

---

## Documentar Resultados

```
VALIDATION REPORT:
- Electron: PASS/FAIL
  - Connection: YES/NO
  - Screenshots: [list]
  - Console Errors: [list]

- Browser: PASS/FAIL
  - Page load: YES/NO
  - Interactions: PASS/FAIL
  - Console Errors: [list]

- API: PASS/FAIL
  - Endpoints: [tested list]
  - Responses: PASS/FAIL

- Database: PASS/FAIL
  - Migrations: APPLIED/PENDING
  - Schema: CORRECT/DRIFT
```

---

## Referências

- `references/electron-validation.md` - Validação Electron detalhada
- `references/browser-validation.md` - Puppeteer checks
- `references/api-validation.md` - REST/GraphQL validation
- `references/database-validation.md` - Schema e data checks
