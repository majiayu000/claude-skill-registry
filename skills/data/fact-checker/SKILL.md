---
name: fact-checker
description: Protocolo Anti-Alucinacao. Valida TODAS as afirmacoes antes de responder. Usa MCPs, busca no codebase e verifica dados no MongoDB. NUNCA assume, SEMPRE verifica. Use quando precisar de respostas 100% factuais ou para validar informacoes criticas.
allowed-tools: Read, Grep, Glob, Bash, mcp__mongo__find_documents, mcp__mongo__list_collections, mcp__mongo__get_collection_schema, mcp__perplexity__perplexity_ask, mcp__perplexity__perplexity_search, mcp__context7__resolve-library-id, mcp__context7__query-docs
---

# Fact Checker Skill - Protocolo Anti-Alucinacao

## Missao
Eliminar alucinacoes garantindo que TODA afirmacao seja verificada em fonte primaria antes de ser apresentada ao usuario.

---

## REGRA DE OURO: VERIFICAR ANTES DE AFIRMAR

### NUNCA FACA:
- Assumir que um arquivo existe sem verificar
- Afirmar estrutura de dados sem consultar schema
- Citar numeros/estatisticas sem fonte
- Dizer "provavelmente" ou "deve ser"
- Inventar nomes de funcoes, variaveis ou arquivos
- Extrapolar comportamento sem evidencia no codigo

### SEMPRE FACA:
- Verificar existencia de arquivos com `Glob` ou `ls`
- Ler o arquivo ANTES de comentar sobre seu conteudo
- Consultar MongoDB para dados reais
- Usar Grep para localizar funcoes/variaveis
- Citar linha exata do codigo fonte
- Dizer "nao encontrei" quando nao encontrar

---

## PROTOCOLO DE VERIFICACAO (V.E.R.I.F.Y)

### V - Validate Existence (Validar Existencia)
Antes de mencionar qualquer arquivo, verificar se existe:

```bash
# ERRADO: Assumir que arquivo existe
"O arquivo controllers/pagamentoController.js..."

# CERTO: Verificar primeiro
ls -la controllers/ | grep -i pagamento
# Se nao encontrar:
find . -name "*pagamento*" -type f
```

### E - Extract Real Data (Extrair Dados Reais)
Nunca inventar dados. Sempre consultar fonte:

```bash
# Para dados do MongoDB:
mcp__mongo__find_documents({
  collection: "times",
  query: '{"temporada": 2026}',
  limit: 5
})

# Para estrutura de collections:
mcp__mongo__get_collection_schema({
  collection: "extratofinanceirocaches",
  sampleSize: 3
})
```

### R - Read Before Responding (Ler Antes de Responder)
NUNCA comentar sobre codigo sem ler:

```bash
# ERRADO: "A funcao calcularSaldo provavelmente faz X..."

# CERTO: Ler primeiro
cat controllers/extratoFinanceiroCacheController.js | grep -A 20 "calcularSaldo"
# Entao comentar com base no codigo real
```

### I - Investigate Dependencies (Investigar Dependencias)
Mapear conexoes reais entre arquivos:

```bash
# Quem usa esta funcao?
grep -rn "calcularSaldo" . --include="*.js"

# Quais arquivos importam este modulo?
grep -rn "require.*extratoFinanceiroCache" . --include="*.js"
```

### F - Find External Sources (Buscar Fontes Externas)
Para informacoes fora do codebase:

```javascript
// API/Framework documentation:
mcp__context7__query_docs({
  libraryId: "/expressjs/express",
  query: "middleware error handling"
})

// Informacoes nao-documentadas (API Cartola):
mcp__perplexity__perplexity_ask({
  messages: [{
    role: "user",
    content: "Quais endpoints da API Cartola FC retornam dados de mercado?"
  }]
})
```

### Y - Yield Uncertainty (Admitir Incerteza)
Quando nao encontrar evidencia:

```markdown
# ERRADO:
"A funcao X faz Y" (sem evidencia)

# CERTO:
"Nao encontrei a funcao X no codebase. Verifiquei em:
- controllers/ (0 resultados)
- services/ (0 resultados)
- routes/ (0 resultados)
Pode estar em outro local ou nao existir."
```

---

## NIVEIS DE CONFIANCA

### ALTA CONFIANCA (Afirmar)
Usar quando:
- Leu o arquivo e viu o codigo
- Consultou MongoDB e obteve dados
- Verificou com MCP e tem fonte

Formato:
```markdown
A funcao `calcularSaldo` em `controllers/extratoFinanceiroCacheController.js:142`
retorna o saldo calculado como Number.
[Fonte: leitura direta do arquivo]
```

### MEDIA CONFIANCA (Indicar)
Usar quando:
- Encontrou referencia mas nao o codigo completo
- MCP retornou informacao parcial
- Grep encontrou mas contexto incerto

Formato:
```markdown
Encontrei referencias a `calcularSaldo` em 3 arquivos:
- controllers/extratoFinanceiroCacheController.js:142
- services/financeiro.js:89
- public/js/fluxo-financeiro/core.js:201
Preciso ler os arquivos para confirmar comportamento.
```

### BAIXA CONFIANCA (Ressalvar)
Usar quando:
- Nao encontrou no codebase
- MCP nao retornou resultado
- Baseado em inferencia

Formato:
```markdown
NAO ENCONTREI esta funcao no codebase atual.
Busquei em: controllers/, services/, routes/, models/
Possibilidades:
1. Nome diferente do esperado
2. Funcao ainda nao implementada
3. Removida em refatoracao recente
```

---

## CHECKLIST DE VALIDACAO

Antes de responder, verificar:

### Para Afirmacoes sobre Codigo
- [ ] Li o arquivo que menciono?
- [ ] Citei linha exata?
- [ ] Verifiquei se funcao existe?
- [ ] Confirmei nome correto (case-sensitive)?

### Para Afirmacoes sobre Dados
- [ ] Consultei MongoDB?
- [ ] Dados sao da temporada correta?
- [ ] Verifiquei collection certa?
- [ ] Filtrei por liga_id (multi-tenant)?

### Para Afirmacoes sobre APIs/Libs
- [ ] Usei Context7 para docs oficiais?
- [ ] Versao da lib esta correta?
- [ ] Exemplo e compativel com Node.js?

### Para Afirmacoes sobre Regras de Negocio
- [ ] Encontrei no CLAUDE.md?
- [ ] Verificou modelo LigaRules?
- [ ] Consultou documentacao do sistema?

---

## SCRIPTS DE VERIFICACAO RAPIDA

### Verificar Existencia de Arquivo
```bash
# Por nome exato
ls -la [path/arquivo.js] 2>/dev/null || echo "ARQUIVO NAO EXISTE"

# Por padrao
find . -name "*[palavra-chave]*" -type f 2>/dev/null
```

### Verificar Funcao Existe
```bash
# Grep com contexto
grep -rn "function [nomeFuncao]\|[nomeFuncao]\s*=\s*function\|[nomeFuncao]\s*=\s*async" --include="*.js"
```

### Verificar Dados no MongoDB
```javascript
// Listar collections
mcp__mongo__list_collections()

// Buscar documentos
mcp__mongo__find_documents({
  collection: "times",
  query: '{"nome_time": {"$regex": "Flamengo", "$options": "i"}}',
  limit: 5
})

// Ver schema
mcp__mongo__get_collection_schema({ collection: "rodadas", sampleSize: 3 })
```

### Verificar Documentacao Externa
```javascript
// Docs oficiais (Context7)
mcp__context7__resolve_library_id({ query: "mongoose findOneAndUpdate", libraryName: "mongoose" })
mcp__context7__query_docs({ libraryId: "/mongoose/mongoose", query: "findOneAndUpdate options" })

// Info nao-documentada (Perplexity)
mcp__perplexity__perplexity_search({ query: "API Cartola FC endpoints 2026", max_results: 5 })
```

---

## TRATAMENTO DE ERROS

### Quando Arquivo Nao Existe
```markdown
VERIFICACAO: Arquivo `controllers/pagamentoController.js`
RESULTADO: NAO ENCONTRADO

Busca realizada:
1. `ls controllers/` - Nao listado
2. `find . -name "*pagamento*"` - 0 resultados
3. `grep -r "pagamento" controllers/` - 0 resultados

CONCLUSAO: Este arquivo NAO existe no codebase atual.
Arquivos de controllers existentes: [listar os reais]
```

### Quando Funcao Nao Existe
```markdown
VERIFICACAO: Funcao `processarPagamento`
RESULTADO: NAO ENCONTRADA

Busca realizada:
1. `grep -rn "processarPagamento" .` - 0 resultados
2. `grep -rn "processar.*pagamento" .` - 0 resultados

CONCLUSAO: Esta funcao NAO existe.
Funcoes similares encontradas:
- `registrarAcertoFinanceiro` em controllers/acertoFinanceiroController.js:45
- `calcularSaldo` em controllers/extratoFinanceiroCacheController.js:142
```

### Quando Dados Nao Existem
```markdown
VERIFICACAO: Collection `pagamentos`
RESULTADO: NAO ENCONTRADA

Collections existentes no banco:
- times
- rodadas
- extratofinanceirocaches
- fluxofinanceirocampos
- acertofinanceiros
- ligarules

CONCLUSAO: Collection `pagamentos` NAO existe.
Dados financeiros estao em: acertofinanceiros, fluxofinanceirocampos
```

---

## FORMATO DE RESPOSTA VERIFICADA

### Estrutura Padrao
```markdown
## [Topico/Pergunta]

### Verificacao Realizada
- [ ] Arquivo X lido: `path/arquivo.js`
- [ ] Collection Y consultada: `collection_name`
- [ ] MCP Z usado: Context7/Perplexity

### Resposta Verificada
[Resposta baseada APENAS em evidencias encontradas]

### Fontes
1. `path/arquivo.js:linha` - [o que encontrou]
2. MongoDB collection `X` - [dados relevantes]
3. MCP Context7 - [documentacao citada]

### Incertezas Remanescentes
- [Se houver algo que nao conseguiu verificar]
```

---

## ANTI-PATTERNS (O QUE NAO FAZER)

### 1. Resposta Inventada
```markdown
# ERRADO
"O sistema usa a funcao `processarCompra()` para gerenciar transacoes..."
(Sem ter verificado se essa funcao existe)

# CERTO
Primeiro: grep -rn "processarCompra" . --include="*.js"
Se nao encontrar: "Nao encontrei funcao `processarCompra`. Funcoes de transacao encontradas: [listar as reais]"
```

### 2. Estrutura de Dados Inventada
```markdown
# ERRADO
"O documento de participante tem campos: nome, email, saldo..."
(Sem consultar schema real)

# CERTO
Primeiro: mcp__mongo__get_collection_schema({ collection: "times", sampleSize: 3 })
Entao: "O schema real inclui: id, nome_time, nome_cartoleiro, ativo, temporada..."
```

### 3. Numero/Estatistica Inventada
```markdown
# ERRADO
"O sistema tem aproximadamente 50 participantes..."
(Sem consultar banco)

# CERTO
Primeiro: mcp__mongo__find_documents({ collection: "times", query: '{"temporada": 2026}', limit: 100 })
Entao: "Encontrei X participantes na temporada 2026."
```

### 4. Path de Arquivo Inventado
```markdown
# ERRADO
"Edite o arquivo src/controllers/userController.js..."
(Sem verificar estrutura real)

# CERTO
Primeiro: ls -la controllers/ && find . -name "*user*" -type f
Entao: Citar path REAL encontrado ou informar que nao existe
```

---

## QUANDO ATIVAR ESTE PROTOCOLO

### Uso Automatico (Sempre Ativo)
- Afirmacoes sobre codigo existente
- Mencao a arquivos especificos
- Citacao de funcoes/variaveis
- Dados numericos/estatisticas

### Uso Explicito (Usuario Solicita)
- `/fact-checker [afirmacao]` - Verificar afirmacao especifica
- "Verifique se..." - Validar informacao
- "Confirme que..." - Checar existencia
- "E verdade que..." - Fact-check

---

## METRICAS DE QUALIDADE

### Taxa de Verificacao
- META: 100% das afirmacoes sobre codigo verificadas
- META: 100% dos dados do banco consultados antes de citar
- META: 0% de "provavelmente", "deve ser", "acho que"

### Indicadores de Alucinacao
Se encontrar estes padroes na resposta, PARAR e verificar:
- "provavelmente"
- "deve existir"
- "imagino que"
- "normalmente"
- "geralmente"
- "pelo que sei"
- Path que nao foi verificado
- Nome de funcao que nao foi buscado

---

## INTEGRACAO COM OUTRAS SKILLS

### Com `/pesquisa`
Fact-checker valida PRD gerado, confirmando que arquivos listados existem.

### Com `/spec`
Fact-checker verifica se funcoes/modulos citados no SPEC sao reais.

### Com `/code`
Fact-checker valida que imports e dependencias existem antes de implementar.

### Com `/audit-financa`
Fact-checker confirma dados financeiros consultando MongoDB diretamente.

---

## EXEMPLO COMPLETO

### Pergunta do Usuario
"Como funciona o calculo de saldo no sistema?"

### Processo de Verificacao
```
1. BUSCAR funcoes de saldo:
   grep -rn "saldo\|calcular" controllers/ services/ --include="*.js"

2. LER arquivo encontrado:
   cat controllers/extratoFinanceiroCacheController.js

3. CONSULTAR dados reais:
   mcp__mongo__get_collection_schema({ collection: "extratofinanceirocaches" })

4. VERIFICAR documentacao:
   cat CLAUDE.md | grep -A 20 "Fluxo Financeiro"
```

### Resposta Verificada
```markdown
## Calculo de Saldo no Sistema

### Verificacao Realizada
- [x] Arquivo lido: `controllers/extratoFinanceiroCacheController.js`
- [x] Collection consultada: `extratofinanceirocaches`
- [x] CLAUDE.md verificado

### Resposta Verificada
O saldo e calculado em `controllers/extratoFinanceiroCacheController.js:142-180`.
A funcao `calcularSaldoFinal()` soma:
1. `ganho_rodada` de cada rodada (collection `rodadas`)
2. Campos manuais (collection `fluxofinanceirocampos`)
3. Acertos financeiros (collection `acertofinanceiros`)

**IMPORTANTE:** O saldo NUNCA e persistido, sempre calculado em tempo real.
[Fonte: CLAUDE.md secao "Financial Calculation Pattern"]

### Fontes
1. `controllers/extratoFinanceiroCacheController.js:142` - funcao calcularSaldoFinal
2. `CLAUDE.md:1870-1878` - padrao de calculo financeiro
3. MongoDB schema `extratofinanceirocaches` - campos time_id, temporada, ganho_rodada

### Incertezas Remanescentes
- Nenhuma. Todas as afirmacoes verificadas no codigo.
```

---

**STATUS:** FACT-CHECKER PROTOCOL - ZERO HALLUCINATION MODE

**Versao:** 1.0

**Principio:** "Se nao verificou, nao afirme."
