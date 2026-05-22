---
name: a11y-auditor
description: Auditor de acessibilidade WCAG 2.1 AA
---

Checklist automatizado WCAG 2.1 AA e validação de linguagem simples para cada mudança no código.

## Contexto

- TCU apontou falhas graves em inclusão digital governamental
- Público-alvo tem baixa escolaridade e pode ter deficiências visuais/motoras
- Acessibilidade não é opcional — é obrigatória por lei (LBI 13.146/2015)
- WCAG 2.1 nível AA é o padrão mínimo

## Checklist WCAG 2.1 AA

### Perceptível
```
1.1 Texto alternativo
  - [ ] Todas as imagens têm alt descritivo
  - [ ] Imagens decorativas têm alt=""
  - [ ] Ícones de ação têm aria-label

1.2 Conteúdo multimídia
  - [ ] Vídeos têm legenda
  - [ ] Áudios têm transcrição

1.3 Adaptável
  - [ ] Estrutura semântica correta (h1→h2→h3, não pular)
  - [ ] Tabelas têm headers (th)
  - [ ] Formulários têm labels associados
  - [ ] Ordem de leitura faz sentido visual e no DOM

1.4 Distinguível
  - [ ] Contraste texto/fundo ≥ 4.5:1 (normal) ou ≥ 3:1 (grande)
  - [ ] Texto pode ser ampliado até 200% sem perder conteúdo
  - [ ] Não usa apenas cor para transmitir informação
  - [ ] Espaçamento de texto ajustável
```

### Operável
```
2.1 Teclado
  - [ ] Todas as funções acessíveis por teclado
  - [ ] Sem armadilhas de foco (focus trap acidental)
  - [ ] Atalhos de teclado documentados

2.2 Tempo
  - [ ] Sem timeout automático (ou extensível)
  - [ ] Animações podem ser pausadas

2.3 Convulsões
  - [ ] Nada pisca mais que 3x por segundo

2.4 Navegável
  - [ ] Link "Pular para conteúdo principal" no topo
  - [ ] Títulos de página descritivos
  - [ ] Ordem de foco lógica (tabindex)
  - [ ] Links têm texto descritivo (não "clique aqui")

2.5 Modalidades de input
  - [ ] Área de toque mínima 44x44px (mobile: 48x48)
  - [ ] Gestos complexos têm alternativa simples
```

### Compreensível
```
3.1 Legível
  - [ ] Página tem lang="pt-BR"
  - [ ] Textos em linguagem simples (5ª série)
  - [ ] Abreviações explicadas na primeira ocorrência

3.2 Previsível
  - [ ] Navegação consistente entre páginas
  - [ ] Componentes com mesma função têm mesmo nome
  - [ ] Mudanças de contexto não acontecem sem aviso

3.3 Assistência de entrada
  - [ ] Erros identificados e descritos em texto
  - [ ] Labels e instruções claras
  - [ ] Sugestões de correção quando possível
  - [ ] Confirmação antes de enviar dados importantes
```

### Robusto
```
4.1 Compatível
  - [ ] HTML válido (sem erros de parser)
  - [ ] ARIA usado corretamente
  - [ ] Componentes customizados têm role + state + name
```

## Validação de Linguagem Simples

### Índice de Legibilidade
```python
# backend/app/services/legibilidade.py
def calcular_indice_legibilidade(texto: str) -> dict:
    """
    Adapta o Flesch Reading Ease para português brasileiro.
    Meta: >= 60 (fácil de ler para público com 5ª série).
    """
    sentencas = texto.count('.') + texto.count('!') + texto.count('?')
    palavras = len(texto.split())
    silabas = contar_silabas_pt(texto)

    if sentencas == 0 or palavras == 0:
        return {"score": 0, "nivel": "indefinido"}

    # Fórmula adaptada para português
    indice = 248.835 - (1.015 * (palavras / sentencas)) - (84.6 * (silabas / palavras))

    niveis = {
        (90, 100): "Muito fácil",
        (70, 89): "Fácil",
        (60, 69): "Adequado",       # meta mínima
        (40, 59): "Moderado",       # precisa simplificar
        (20, 39): "Difícil",        # reescrever
        (0, 19): "Muito difícil",   # reescrever urgente
    }

    nivel = "indefinido"
    for (min_val, max_val), nome in niveis.items():
        if min_val <= indice <= max_val:
            nivel = nome
            break

    return {
        "score": round(indice, 1),
        "nivel": nivel,
        "palavras": palavras,
        "sentencas": sentencas,
        "media_palavras_por_sentenca": round(palavras / sentencas, 1),
        "aprovado": indice >= 60,
    }
```

### Detector de Jargão
```python
JARGOES_GOVERNAMENTAIS = {
    "cadastro único": "cadastro do governo",
    "beneficiário": "pessoa que recebe",
    "elegível": "tem direito",
    "protocolar": "entregar papéis",
    "deferido": "aprovado",
    "indeferido": "negado",
    "vigência": "prazo",
    "per capita": "por pessoa",
    "renda familiar": "quanto a família ganha",
    "óbice": "problema",
    "extemporâneo": "fora do prazo",
    "certidão negativa": "documento que mostra que não deve nada",
    "NIS": "número do cadastro social",
}

def detectar_jargoes(texto: str) -> list[dict]:
    """Identifica jargões e sugere alternativas simples."""
    encontrados = []
    texto_lower = texto.lower()
    for jargao, alternativa in JARGOES_GOVERNAMENTAIS.items():
        if jargao in texto_lower:
            encontrados.append({
                "jargao": jargao,
                "alternativa": alternativa,
                "contexto": extrair_contexto(texto, jargao),
            })
    return encontrados
```

## Testes Automatizados

### Playwright + axe-core
```typescript
// frontend/tests/a11y/accessibility.test.ts
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

const PAGINAS = [
  { nome: 'Home', url: '/' },
  { nome: 'Catálogo', url: '/beneficios' },
  { nome: 'Elegibilidade', url: '/descobrir' },
];

for (const pagina of PAGINAS) {
  test(`Acessibilidade: ${pagina.nome}`, async ({ page }) => {
    await page.goto(pagina.url);

    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();

    expect(results.violations).toEqual([]);
  });
}

test('Contraste mínimo 4.5:1', async ({ page }) => {
  await page.goto('/');
  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze();
  expect(results.violations).toEqual([]);
});

test('Navegação por teclado', async ({ page }) => {
  await page.goto('/');
  // Tab deve mover foco visivelmente
  await page.keyboard.press('Tab');
  const focused = await page.evaluate(() => document.activeElement?.tagName);
  expect(focused).toBeTruthy();
});
```

### CI Pipeline
```yaml
# .github/workflows/a11y.yml
name: Accessibility Audit
on: [pull_request]

jobs:
  a11y:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run build
      - run: npx playwright install --with-deps
      - run: npx playwright test tests/a11y/
```

## Comandos
```bash
# Rodar auditoria completa
npx playwright test tests/a11y/

# Lighthouse acessibilidade
npx lighthouse http://localhost:5173 --only-categories=accessibility --output=json

# Validar HTML
npx html-validate frontend/dist/**/*.html

# Testar contraste
npx color-contrast-checker "#F99500" "#000000"
```

## Arquivos Relacionados
- `frontend/tests/a11y/` - Testes de acessibilidade
- `backend/app/services/legibilidade.py` - Índice de legibilidade
- `.github/workflows/a11y.yml` - Pipeline CI
- `.claude/skills/linguagem-simples.md` - Skill de linguagem simples (complementar)

## Referências
- WCAG 2.1: https://www.w3.org/WAI/WCAG21/quickref/
- LBI (Lei Brasileira de Inclusão): https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13146.htm
- axe-core: https://github.com/dequelabs/axe-core
- eMAG (Modelo de Acessibilidade do Governo): https://emag.governoeletronico.gov.br/
