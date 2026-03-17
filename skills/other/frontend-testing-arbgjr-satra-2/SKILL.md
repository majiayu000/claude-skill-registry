---
name: frontend-testing
description: |
  Testa aplicacoes web usando Playwright. Captura screenshots, executa E2E tests,
  analisa logs do browser. Integrado com qa-analyst para Phase 6.
  Use quando: testar frontend, capturar screenshots, validar UI, executar E2E.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
user-invocable: true
---

# Frontend Testing Skill

## Proposito

Testa aplicacoes web locais e remotas usando Playwright:
- **Screenshots**: Captura visual para validacao
- **E2E Tests**: Testes end-to-end automatizados
- **Browser Logs**: Analise de erros e warnings
- **Accessibility**: Validacao basica de a11y

## Principios de Design

### 1. Reconnaissance-Then-Action

Baseado no padrao do webapp-testing da Anthropic:

```
1. Navigate  → Ir para a pagina
2. Wait      → Aguardar network idle
3. Capture   → Screenshot ou DOM
4. Discover  → Identificar seletores do DOM renderizado
5. Interact  → Executar acoes com seletores descobertos
```

### 2. Server Lifecycle Management

Gerenciar servidor local automaticamente:

```bash
# Inicia servidor, executa teste, encerra servidor
python scripts/with_server.py --server "npm run dev" --port 3000 -- pytest tests/
```

### 3. Never Hardcode Selectors

Sempre descobrir seletores do DOM real, nunca assumir.

## Comandos

### /frontend-test {url}

Executa suite de testes E2E.

```bash
/frontend-test http://localhost:3000
/frontend-test https://staging.example.com
```

### /frontend-screenshot {url} {nome}

Captura screenshot de uma pagina.

```bash
/frontend-screenshot http://localhost:3000 homepage
/frontend-screenshot http://localhost:3000/login login-page
```

**Output**: `.agentic_sdlc/projects/{id}/screenshots/{nome}.png`

### /frontend-check {url}

Verifica saude basica da aplicacao.

```bash
/frontend-check http://localhost:3000
```

**Verifica**:
- Pagina carrega sem erros
- Console sem erros criticos
- Links nao quebrados
- Performance basica

## Workflow de Testes

### Setup com Servidor Local

```bash
# Single server
python scripts/with_server.py \
  --server "npm run dev" \
  --port 5173 \
  -- python scripts/run_tests.py

# Multiple servers (frontend + backend)
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python scripts/run_tests.py
```

### Captura de Screenshot

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()

    page.goto("http://localhost:3000")
    page.wait_for_load_state("networkidle")

    page.screenshot(path="screenshot.png", full_page=True)
    browser.close()
```

### Teste E2E Basico

```python
def test_login_flow(page):
    page.goto("http://localhost:3000/login")
    page.wait_for_load_state("networkidle")

    # Descobrir seletores do DOM real
    page.fill('[data-testid="email"]', 'test@example.com')
    page.fill('[data-testid="password"]', 'password123')
    page.click('[data-testid="submit"]')

    # Verificar redirecionamento
    page.wait_for_url("**/dashboard")
    assert "dashboard" in page.url
```

## Integracao com SDLC

### Phase 6 (Quality) - qa-analyst

```yaml
quality_gate:
  frontend_tests:
    required: true
    criteria:
      - "E2E tests passing"
      - "No console errors"
      - "Screenshots captured for review"

  commands:
    - "/frontend-test http://localhost:3000"
    - "/frontend-screenshot http://localhost:3000 homepage"
```

### Phase 7 (Release) - Evidencias

```yaml
release_artifacts:
  screenshots:
    - homepage.png
    - login-page.png
    - dashboard.png
  test_reports:
    - e2e-results.json
```

## Dependencias

### Obrigatorias

```bash
# Python
pip install playwright pytest-playwright

# Browser
playwright install chromium
```

### Opcionais

```bash
# Para testes visuais
pip install pixelmatch pillow

# Para acessibilidade
pip install axe-playwright-python
```

### Verificar Instalacao

```bash
python scripts/check_deps.py
```

## Boas Praticas

### 1. Sempre Aguardar Network Idle

```python
page.goto(url)
page.wait_for_load_state("networkidle")  # OBRIGATORIO
```

### 2. Usar data-testid

Preferir seletores `data-testid` sobre classes CSS:

```html
<!-- BOM -->
<button data-testid="submit-btn">Submit</button>

<!-- EVITAR -->
<button class="btn btn-primary submit">Submit</button>
```

### 3. Capturar Logs do Browser

```python
page.on("console", lambda msg: print(f"[{msg.type}] {msg.text}"))
page.on("pageerror", lambda err: print(f"[ERROR] {err}"))
```

### 4. Organizar Screenshots

```
.agentic_sdlc/projects/{id}/
└── screenshots/
    ├── before/           # Estado inicial
    ├── after/            # Apos mudancas
    └── regression/       # Comparacao visual
```

## Anti-Patterns

### NAO Fazer

```python
# ❌ Hardcoded selectors sem verificar DOM
page.click("#submit-btn")

# ❌ Sleep ao inves de wait
import time
time.sleep(5)

# ❌ Ignorar erros de console
# (nao configurar handler)
```

### Fazer

```python
# ✅ Descobrir seletor do DOM
submit = page.locator('[data-testid="submit"]')
if submit.count() > 0:
    submit.click()

# ✅ Wait explicito
page.wait_for_selector('[data-testid="result"]')

# ✅ Capturar todos os logs
errors = []
page.on("pageerror", lambda e: errors.append(e))
```

## Troubleshooting

### "Browser nao instalado"

```bash
playwright install chromium
# Ou todos os browsers
playwright install
```

### "Timeout ao carregar pagina"

Aumentar timeout:

```python
page.goto(url, timeout=60000)  # 60 segundos
```

### "Servidor nao iniciou"

Verificar porta:

```bash
lsof -i :3000
# Se ocupada, usar outra porta
python scripts/with_server.py --server "npm run dev" --port 3001 ...
```

### "Screenshot em branco"

Aguardar conteudo:

```python
page.wait_for_selector("main", state="visible")
page.screenshot(path="screenshot.png")
```

## Referencias

- [Playwright Python docs](https://playwright.dev/python/)
- [pytest-playwright](https://playwright.dev/python/docs/test-runners)
- [Anthropic webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)
