---
name: prd-generator
description: |
  Gera PRD/Spec para o Ralph Loop atraves de perguntas iterativas.
  Use quando: (1) Usuario pede "cria PRD", "cria spec", "documenta feature",
  (2) Precisa estruturar requisitos antes de implementar,
  (3) Quer rodar Ralph Loop mas nao tem spec pronta.
---

# PRD Generator

Skill para criar especificacoes estruturadas atraves de dialogo iterativo.

## Fluxo de Trabalho

```
OBJETIVO → CONTEXTO → REQUISITOS → CRITERIOS → GERACAO
```

---

## FASE 1: OBJETIVO

### Perguntas Obrigatorias

1. **"O que voce quer construir?"**
   - Aguarde resposta antes de prosseguir

2. **"Qual problema isso resolve?"**
   - Entender a dor/necessidade

3. **"Quem vai usar isso?"**
   - Identificar usuarios/stakeholders

### Regra

> Faca UMA pergunta por vez. Nao sobrecarregue o usuario.

---

## FASE 2: CONTEXTO (Automatica)

### Acoes

1. **Pesquisar codebase** por termos relacionados:
   ```
   Grep: palavras-chave mencionadas pelo usuario
   Glob: arquivos de modulos relacionados
   ```

2. **Mostrar descobertas**:
   ```
   "Encontrei esses arquivos relacionados:
   - app/modulo/routes.py (rotas existentes)
   - app/modulo/models.py (modelo X tem campo Y)

   Isso esta relacionado ao que voce precisa?"
   ```

3. **Confirmar entendimento** antes de prosseguir

### Regra

> Sempre pesquise ANTES de perguntar detalhes tecnicos.
> Mostre o que encontrou para contextualizar.

---

## FASE 3: REQUISITOS

### Perguntas por Tipo

#### Feature Nova
- "Quais funcionalidades principais?"
- "Precisa de nova tela/rota?"
- "Quais dados precisa exibir/coletar?"

#### Bug Fix
- "Qual o comportamento atual?"
- "Qual o comportamento esperado?"
- "Como reproduzir?"

#### Integracao
- "Qual sistema externo?"
- "Quais dados sincronizar?"
- "Frequencia de sincronizacao?"

#### Refatoracao
- "O que esta ruim hoje?"
- "Como deveria ficar?"
- "Quais arquivos afetados?"

### Regra

> Adapte as perguntas ao tipo de tarefa identificado.

---

## FASE 4: CRITERIOS DE ACEITE

### Perguntas

1. **"Como saber se funcionou?"**
   - Criterios objetivos e verificaveis

2. **"Quais validacoes sao necessarias?"**
   - Campos obrigatorios, formatos, regras

3. **"Casos de erro a tratar?"**
   - O que pode dar errado

### Formato de Saida

Transformar respostas em checkboxes:
```markdown
## Criterios de Aceite

- [ ] Rota /nova-tela acessivel
- [ ] Formulario valida campos X, Y, Z
- [ ] Dados salvos no banco corretamente
- [ ] Mensagem de sucesso exibida
- [ ] Erro tratado com mensagem amigavel
```

---

## FASE 5: GERACAO

### Acoes

1. **Montar documento** no formato padrao

2. **Mostrar preview** ao usuario:
   ```
   "Vou gerar o seguinte documento:

   [PREVIEW DO CONTEUDO]

   Posso salvar em .claude/ralph-loop/specs/nome-feature.md?"
   ```

3. **Salvar arquivo** apos confirmacao

4. **Instruir proximo passo**:
   ```
   "Spec salva em .claude/ralph-loop/specs/nome-feature.md

   Para executar:
   ./ralph-loop.sh plan 3
   ```

### Formato do Documento

```markdown
# [Nome da Feature]

## Objetivo
[Descricao do problema e solucao]

## Requisitos

1. [Requisito 1]
2. [Requisito 2]
3. [Requisito 3]

## Criterios de Aceite

- [ ] [Criterio 1]
- [ ] [Criterio 2]
- [ ] [Criterio 3]

## Notas Tecnicas

### Arquivos Relacionados
- [arquivo1.py] - [descricao]
- [arquivo2.html] - [descricao]

### Padroes a Seguir
- Consultar CLAUDE.md para nomes de campos
- Usar filtro numero_br para formatacao
- Adicionar link no menu (base.html)
```

---

## REGRAS CRITICAS

### 1. Uma Pergunta Por Vez

```
ERRADO:
"Qual o objetivo? Quem vai usar? Quais funcionalidades?"

CERTO:
"Qual o objetivo?"
[aguarda resposta]
"Quem vai usar?"
[aguarda resposta]
```

### 2. Pesquisar Antes de Perguntar

```
ERRADO:
"Qual modelo usar?"

CERTO:
"Encontrei o modelo CarteiraPrincipal com campos X, Y, Z.
Voce quer usar esse modelo ou criar um novo?"
```

### 3. Confirmar Antes de Gerar

```
ERRADO:
[gera arquivo direto]

CERTO:
"Vou gerar esse documento: [preview]
Posso salvar?"
```

### 4. Instruir Proximo Passo

```
ERRADO:
"Pronto, arquivo salvo."

CERTO:
"Arquivo salvo em .claude/ralph-loop/specs/nome.md

Proximo passo:
./ralph-loop.sh plan 3"
```

---

## REFERENCIAS

- [question-framework.md](references/question-framework.md) - Perguntas detalhadas por tipo
- [spec-templates.md](references/spec-templates.md) - Templates completos

---

## EXEMPLOS DE USO

### Usuario diz: "cria um PRD para dashboard de vendas"

```
Skill: "O que voce quer ver nesse dashboard de vendas?"
User: "Total vendido no mes, top produtos, top clientes"

Skill: [pesquisa codebase]
       "Encontrei app/carteira/ com dados de pedidos.
        O modelo CarteiraPrincipal tem: num_pedido, cod_produto,
        preco_produto_pedido, qtd_produto_pedido.
        Posso usar esses dados?"

User: "Sim"

Skill: "Quem vai acessar esse dashboard?"
User: "Gerentes comerciais"

Skill: "Como saber se o dashboard esta correto?"
User: "Os totais batem com o relatorio do Odoo"

Skill: [monta preview]
       "Vou gerar:

       # Dashboard de Vendas

       ## Objetivo
       Dashboard para gerentes comerciais visualizarem...

       Posso salvar em .claude/ralph-loop/specs/dashboard-vendas.md?"

User: "Sim"

Skill: [salva arquivo]
       "Pronto! Arquivo salvo em .claude/ralph-loop/specs/dashboard-vendas.md

       Para implementar:
       ./ralph-loop.sh plan 3"
```
