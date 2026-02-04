---
name: Spec
description: Fase 2 - Specification Protocol. Le PRD.md, aplica S.D.A completo (mapeia TODAS dependencias), define mudancas cirurgicas linha por linha e gera Spec.md. Preserva logica existente, mudancas minimas focadas.
---

# FASE 2: SPECIFICATION (SURGICAL PLANNING)

## Objetivo
Transformar PRD em especificacao tecnica precisa com mudancas cirurgicas linha por linha.

---

## INPUT OBRIGATORIO

### Carregar PRD
```bash
# Localizar PRD gerado na Fase 1
ls -la .claude/docs/PRD-*.md

# Ler PRD completo
cat .claude/docs/PRD-[nome-tarefa].md
```

---

## PROTOCOLO S.D.A COMPLETO

### FASE 1: SOLICITACAO (Arquivos Originais)

#### 1.1 Solicitar Todos os Arquivos do PRD
```bash
# Para cada arquivo listado no PRD, solicitar COMPLETO
# (Nunca trabalhar com snippets)

# Exemplo do PRD:
# "Arquivos a modificar: controllers/extratoController.js"

cat controllers/extratoController.js  # VER TUDO
```

#### 1.2 Analisar Linha por Linha
- Identificar funcoes principais
- Mapear variaveis usadas
- Entender fluxo de dados
- Detectar dependencias internas

### FASE 2: MAPEAMENTO DE DEPENDENCIAS

#### 2.1 Links Diretos (HTML)
```bash
grep -r "href=.*[nome-arquivo]" . --include="*.html"
```

#### 2.2 JavaScript Imports
```bash
grep -r "require.*[nome-arquivo]\|import.*[nome-arquivo]" . --include="*.js"
```

#### 2.3 IDs e Classes CSS
```bash
grep -r "#[id-elemento]" . --include="*.js" --include="*.css"
grep -r "\.[classe]" . --include="*.js" --include="*.css"
```

#### 2.4 Formularios e Rotas
```bash
grep -r "fetch.*[endpoint]\|action=.*[endpoint]" public/
```

### FASE 3: VERIFICACAO CRUZADA

#### 3.1 Solicitar Arquivos Dependentes
```bash
# Para cada dependencia encontrada, solicitar arquivo
cat [arquivo-que-importa].js
cat [arquivo-com-link].html
```

#### 3.2 Documentar Impactos
- **Arquivo A** usa funcao X -> Precisa atualizar importacao
- **Arquivo B** tem link para Y -> Precisa ajustar href

### FASE 4: IMPLEMENTACAO SEGURA

#### 4.1 Propor Alteracoes Minimas
```javascript
// ERRADO: Reescrever funcao inteira
async function calcularSaldo() {
  // ... 50 linhas de codigo novo
}

// CORRETO: Mudanca cirurgica
async function calcularSaldo() {
  // ... [codigo existente preservado]

  // [LINHA 45] ADICIONAR:
  const saldoAcertos = await calcularSaldoAcertos(participanteId);

  // ... [restante do codigo preservado]
  return saldoTotal + saldoAcertos; // [LINHA 78] MODIFICAR
}
```

---

## GERAR SPEC.MD

### Estrutura Obrigatoria
```markdown
# SPEC - [Nome da Funcionalidade]

**Data:** [data atual]
**Baseado em:** PRD-[nome].md
**Status:** Especificacao Tecnica

---

## Resumo da Implementacao
[1 paragrafo: O que sera feito tecnicamente]

---

## Arquivos a Modificar (Ordem de Execucao)

### 1. [Arquivo Principal] - Mudanca Primaria

**Path:** `[caminho completo]`
**Tipo:** Modificacao | Criacao | Delecao
**Impacto:** Alto | Medio | Baixo
**Dependentes:** [Arquivo X, Y, Z]

#### Mudancas Cirurgicas:

**Linha [num]: ADICIONAR**
```javascript
[codigo a adicionar]
```
**Motivo:** [Explicacao]

**Linha [num]: MODIFICAR**
```javascript
// ANTES:
[codigo antigo]

// DEPOIS:
[codigo novo]
```
**Motivo:** [Explicacao]

---

### 2. [Arquivo Dependente] - Ajuste de Integracao

**Path:** `[caminho completo]`
**Tipo:** Modificacao
**Impacto:** Baixo

#### Mudancas Cirurgicas:

**Linha [num]: ATUALIZAR IMPORTACAO**
```javascript
// ANTES:
import { funcaoAntiga } from './modulo';

// DEPOIS:
import { funcaoAntiga, funcaoNova } from './modulo';
```

---

## Mapa de Dependencias

```
Arquivo Principal (controllers/extratoController.js)
    |-> routes/extrato-routes.js [MODIFICAR linha 23]
    |-> public/js/extrato/core.js [MODIFICAR linha 45]
    |-> public/participante/fronts/extrato.html [ADICIONAR botao]
```

---

## Validacoes de Seguranca

### Multi-Tenant
- [ ] Todas queries incluem `liga_id`
- [ ] Verificado isolamento entre ligas

**Queries Afetadas:**
```javascript
// [Arquivo] - Linha [num]
Model.find({
  liga_id: ligaId,  // VALIDADO
  // ...
});
```

### Autenticacao
- [ ] Rotas protegidas com middleware
- [ ] Verificacao de permissoes

**Middlewares Aplicados:**
```javascript
router.post('/endpoint',
  verificarAdmin,        // Protecao
  validarLigaId,         // Multi-tenant
  controller.acao
);
```

---

## Casos de Teste

### Teste 1: [Cenario Positivo]
**Setup:** [Condicao inicial]
**Acao:** [Passo a passo]
**Resultado Esperado:** [O que deve acontecer]

### Teste 2: [Cenario Negativo]
**Setup:** [Condicao inicial]
**Acao:** [Passo a passo com erro]
**Resultado Esperado:** [Tratamento de erro]

---

## Rollback Plan

### Em Caso de Falha
**Passos de Reversao:**
1. Reverter commit: `git revert [hash]`
2. Restaurar banco (se aplicavel)
3. Limpar cache

---

## Checklist de Validacao

### Antes de Implementar
- [ ] Todos os arquivos dependentes identificados
- [ ] Mudancas cirurgicas definidas linha por linha
- [ ] Impactos mapeados
- [ ] Testes planejados
- [ ] Rollback documentado

---

## Ordem de Execucao (Critico)

1. **Backend primeiro:**
   - Models (schema)
   - Controllers (logica)
   - Routes (endpoints)

2. **Frontend depois:**
   - JS (logica cliente)
   - HTML (UI)
   - CSS (estilos)

3. **Testes:**
   - Unitarios (se existirem)
   - Integracao
   - E2E (manual)

---

## Proximo Passo

**Comando para Fase 3:**
```
LIMPAR CONTEXTO e executar:
/code .claude/docs/SPEC-[nome].md
```

---

**Gerado por:** Spec Protocol v1.0
```

### Onde Salvar
```bash
path=".claude/docs/SPEC-[nome-tarefa-kebab-case].md"
```

---

## Checklist S.D.A (Verificacao Final)

### Arquivos Solicitados
- [ ] Arquivo original completo (nao snippet)
- [ ] Todos os dependentes identificados
- [ ] Arquivos relacionados analisados

### Dependencias Mapeadas
- [ ] JavaScript imports verificados
- [ ] Links HTML checados
- [ ] IDs e classes CSS validados
- [ ] Formularios e rotas mapeados

### Mudancas Documentadas
- [ ] Linha por linha especificada
- [ ] Codigo antes/depois claramente definido
- [ ] Motivo de cada mudanca explicado
- [ ] Impacto documentado

### Seguranca e Validacoes
- [ ] Multi-tenant validado (liga_id)
- [ ] Autenticacao verificada
- [ ] Rollback plan documentado
- [ ] Testes planejados

---

## Anti-Patterns (NAO FAZER)

### Modificar Sem Ver Original
```
ERRADO: "Vou adicionar linha 45 sem ver o arquivo"

CORRETO: cat [arquivo].js primeiro
         Analisar contexto da linha 45
         Garantir que mudanca nao quebra logica adjacente
```

### Ignorar Dependencias
```
ERRADO: "Modifico apenas o controller, o resto se resolve"

CORRETO: Mapear TODOS os arquivos que usam o controller
         Ajustar rotas, frontend, testes
         Verificar importacoes
```

### Reescrever Tudo
```
ERRADO: function novaFuncao() { /* 100 linhas novas */ }

CORRETO: Preservar funcao existente
         Adicionar apenas 2-3 linhas necessarias
         Manter compatibilidade
```

---

**STATUS:** SPEC PROTOCOL - SURGICAL & PRECISE
**Versao:** 1.0 (High Senior Edition)
